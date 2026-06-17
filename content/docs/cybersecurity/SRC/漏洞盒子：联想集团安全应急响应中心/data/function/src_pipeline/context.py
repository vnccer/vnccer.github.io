import argparse
import asyncio
import glob
import os
import re
from urllib.parse import urljoin

from src_pipeline.config import (
    DEFAULT_BASE_URL,
    DEFAULT_CONCURRENT,
    DEFAULT_CONTEXT_OUTPUT_FILE,
    DEFAULT_JS_DIR,
    DEFAULT_PRIORITY_FILE,
    DEFAULT_SOURCE_DIR,
)

FULL_URL_PATTERNS = [
    re.compile(r'https?://[^\s"\'<>]+/_nuxt/[A-Za-z0-9_\-]+\.js(?:\?[^\s"\'<>]*)?'),
    re.compile(r'https?://[^\s"\'<>]+/_nuxt/builds/meta/[A-Za-z0-9_\-]+\.json(?:\?[^\s"\'<>]*)?'),
    re.compile(r'https?://[^\s"\'<>]+(?:/[A-Za-z0-9_\-./]*)?_payload\.json(?:\?[^\s"\'<>]*)?'),
]
RELATIVE_URL_PATTERNS = [
    re.compile(r'/_nuxt/[A-Za-z0-9_\-]+\.js(?:\?[^\s"\'<>]*)?'),
    re.compile(r'/_nuxt/builds/meta/[A-Za-z0-9_\-]+\.json(?:\?[^\s"\'<>]*)?'),
    re.compile(r'(?:/[A-Za-z0-9_\-./]*)?_payload\.json(?:\?[^\s"\'<>]*)?'),
]
BASE_URL_PATTERN = re.compile(r'ZQm=(https?://[^\],\s]+)')
FULL_URL_STRIPPER = re.compile(r'https?://[^\s"\'<>]+')


class Color:
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"


def build_parser():
    parser = argparse.ArgumentParser(
        description="下载 Nuxt JS/JSON 资源，并从 bundle 中补全 API 上下文"
    )
    parser.add_argument(
        "-s", "--source-dir",
        default=DEFAULT_SOURCE_DIR,
        help="下载源目录，默认扫描其中全部 .txt 文件，默认: %(default)s",
    )
    parser.add_argument(
        "--download-source",
        action="append",
        default=[],
        help="额外追加一个下载源文本文件，可重复指定",
    )
    parser.add_argument(
        "--priority-file",
        default=DEFAULT_PRIORITY_FILE,
        help="classify_apis.py 生成的优先级报告，默认: %(default)s",
    )
    parser.add_argument(
        "--js-dir",
        default=DEFAULT_JS_DIR,
        help="下载后的 JS/JSON 目录，默认: %(default)s",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="相对路径补全时使用的默认基准域名，默认: %(default)s",
    )
    parser.add_argument(
        "-o", "--output",
        default=DEFAULT_CONTEXT_OUTPUT_FILE,
        help="输出 Markdown 报告路径，默认: %(default)s",
    )
    parser.add_argument(
        "-c", "--concurrent",
        type=int,
        default=DEFAULT_CONCURRENT,
        help="下载并发数，默认: %(default)s",
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="跳过下载阶段，只基于现有下载目录生成上下文报告",
    )
    parser.add_argument(
        "--download-only",
        action="store_true",
        help="只执行下载，不生成 api_context_report.md",
    )
    return parser


def normalize_url(url):
    return url.rstrip("'\"`),;]>}")


def discover_source_files(source_dir, extra_sources):
    source_files = []

    if source_dir:
        if os.path.isdir(source_dir):
            for name in sorted(os.listdir(source_dir)):
                if name.lower().endswith(".txt"):
                    source_files.append(os.path.abspath(os.path.join(source_dir, name)))
        elif os.path.isfile(source_dir):
            source_files.append(os.path.abspath(source_dir))

    for path in extra_sources:
        if os.path.isfile(path):
            source_files.append(os.path.abspath(path))

    deduped = []
    seen = set()
    for path in source_files:
        if path not in seen:
            deduped.append(path)
            seen.add(path)
    return deduped


def extract_urls_from_text(text, fallback_base_url):
    urls = set()

    for pattern in FULL_URL_PATTERNS:
        for match in pattern.finditer(text):
            urls.add(normalize_url(match.group(0)))

    for line in text.splitlines():
        base_match = BASE_URL_PATTERN.search(line)
        base_url = normalize_url(base_match.group(1)) if base_match else fallback_base_url
        if not base_url:
            continue

        line_without_full_urls = FULL_URL_STRIPPER.sub(" ", line)
        for pattern in RELATIVE_URL_PATTERNS:
            for match in pattern.finditer(line_without_full_urls):
                relative_url = normalize_url(match.group(0))
                absolute_url = normalize_url(urljoin(base_url.rstrip("/") + "/", relative_url.lstrip("/")))
                urls.add(absolute_url)

    return urls


def collect_download_urls(source_files, fallback_base_url):
    urls = set()
    per_source_counts = []

    for path in source_files:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except OSError:
            per_source_counts.append((path, 0))
            continue

        found = extract_urls_from_text(text, fallback_base_url)
        urls.update(found)
        per_source_counts.append((path, len(found)))

    return sorted(urls), per_source_counts


def url_to_filename(url):
    if "/builds/meta/" in url:
        return "nuxt_build_meta.json"
    if "_payload.json" in url:
        suffix = url.split("?", 1)[-1].split("-")[0] if "?" in url else "payload"
        return f"_payload_{suffix}.json"
    return url.split("?", 1)[0].rsplit("/", 1)[-1]


async def download_asset(session, semaphore, output_dir, url):
    filename = url_to_filename(url)
    save_path = os.path.join(output_dir, filename)

    if os.path.exists(save_path):
        return "skip", filename

    async with semaphore:
        try:
            async with session.get(url, timeout=15) as response:
                if response.status != 200:
                    return "http_error", f"{filename} [{response.status}]"
                data = await response.read()
                with open(save_path, "wb") as f:
                    f.write(data)
                return "ok", filename
        except Exception as exc:
            return "fail", f"{filename} | {exc}"


async def download_all(urls, output_dir, concurrent):
    try:
        import aiohttp
    except ImportError:
        print("[!] 缺少依赖 aiohttp，请先安装后再执行下载阶段")
        return False

    os.makedirs(output_dir, exist_ok=True)

    if not urls:
        print("[!] 未找到任何可下载的 URL")
        return False

    existing = set(os.listdir(output_dir))
    needed = [url for url in urls if url_to_filename(url) not in existing]
    if not needed:
        print(f"[*] {len(urls)} 个文件均已存在，跳过下载")
        return True

    print(f"[*] 需要下载 {len(needed)}/{len(urls)} 个文件 ...")
    semaphore = asyncio.Semaphore(concurrent)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [download_asset(session, semaphore, output_dir, url) for url in needed]
        results = await asyncio.gather(*tasks)

    ok_count = sum(1 for status, _ in results if status == "ok")
    fail_messages = [message for status, message in results if status in {"http_error", "fail"}]
    print(f"[*] 下载完成: 成功={ok_count} 失败={len(fail_messages)} 目录={os.path.abspath(output_dir)}")
    for message in fail_messages[:10]:
        print(f"    [{Color.RED}FAIL{Color.RESET}] {message}")
    if len(fail_messages) > 10:
        print(f"    ... 其余 {len(fail_messages) - 10} 条失败省略")
    return True


def parse_priority_report(filepath):
    if not os.path.exists(filepath):
        print(f"[!] 未找到 {filepath}，请先运行 classify_apis.py")
        return [], [], []

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    t1, t2, t3 = [], [], []
    current_tier = None

    for line in text.split("\n"):
        stripped = line.strip()
        if "第一梯队" in stripped:
            current_tier = 1
            continue
        if "第二梯队" in stripped:
            current_tier = 2
            continue
        if "第三梯队" in stripped:
            current_tier = 3
            continue
        if ("未分类 API" in stripped or "页面路由" in stripped or
                "目标域名 URL" in stripped or "敏感字符串" in stripped):
            current_tier = None
            continue
        if current_tier is None:
            continue
        if line.startswith("  /") and not line.endswith((".jpg", ".png", ".gif", ".mp4", ".apk", ".exe", ".html")):
            route = line.strip()
            if "http" in route:
                continue
            if current_tier == 1:
                t1.append(route)
            elif current_tier == 2:
                t2.append(route)
            elif current_tier == 3:
                t3.append(route)

    return t1, t2, t3


def detect_context(code_snippet, api_path):
    snippet = code_snippet.strip()
    escaped_path = re.escape(api_path.rstrip("/"))

    method = "?"
    close = re.search(
        r'\.(get|post|put|delete|patch)\s*\(\s*["\'`]' + escaped_path,
        snippet,
        re.IGNORECASE,
    )
    if close:
        method = close.group(1).upper()
    else:
        index = snippet.find(api_path.rstrip("/"))
        if index > 0:
            prefix = snippet[max(0, index - 100):index]
            match = re.search(r"\.(get|post|put|delete|patch)\s*\(", prefix, re.IGNORECASE)
            if match:
                method = match.group(1).upper()

    auth = "无"
    index = snippet.find(api_path.rstrip("/"))
    window = snippet[max(0, index - 200):index + 200]
    auth_patterns = [
        (r"headers\s*:\s*[A-Za-z]", "Token"),
        (r"(?:Token|token)\s*:\s*\w", "Token"),
        (r"(?:Authorization|authorization)\s*:", "Authorization"),
        (r"(?:Bearer|bearer)", "Bearer"),
        (r"(?:X-Auth|x-auth|X-Token|x-token)", "自定义Header"),
    ]
    for pattern, label in auth_patterns:
        if re.search(pattern, window):
            auth = label
            break

    content_type = "?"
    content_type_patterns = [
        (r"application/json", "application/json"),
        (r"x-www-form-urlencoded", "x-www-form-urlencoded"),
        (r"multipart/form-data", "multipart/form-data"),
        (r'Content-Type\s*:\s*["\'][^"\']+["\']', None),
    ]
    for pattern, override in content_type_patterns:
        match = re.search(pattern, window, re.IGNORECASE)
        if match:
            content_type = override or match.group(0)
            break
    if content_type == "?" and method in ("POST", "PUT", "PATCH"):
        content_type = "application/json"
    if content_type == "?" and method == "GET":
        content_type = "—"

    params = []
    function_match = re.search(r"function\s+\w+\s*\(([^)]*)\)", window)
    if function_match and function_match.group(1).strip():
        params = [param.strip() for param in function_match.group(1).split(",")]

    return {
        "method": method,
        "auth": auth,
        "content_type": content_type,
        "params": params,
    }


def search_bundle_files(api_path, js_dir):
    search_path = api_path.rstrip("/")
    variants = [re.escape(search_path)]
    if search_path != api_path:
        variants.append(re.escape(api_path))

    yielded = set()
    patterns = []
    for variant in variants:
        patterns.append(re.compile(rb"([\s\S]{0,200})(" + variant.encode() + rb")([\s\S]{0,200})"))

    file_patterns = [
        os.path.join(js_dir, "*.js"),
        os.path.join(js_dir, "*.json"),
    ]

    for pattern_path in file_patterns:
        for file_path in sorted(glob.glob(pattern_path)):
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
            except OSError:
                continue

            for pattern in patterns:
                for match in pattern.finditer(content):
                    before = match.group(1).decode("utf-8", errors="replace")
                    after = match.group(3).decode("utf-8", errors="replace")
                    snippet = before + search_path + after
                    snippet_hash = hash(snippet)
                    if snippet_hash in yielded:
                        continue
                    yielded.add(snippet_hash)
                    yield os.path.basename(file_path), snippet


def build_report(t1, t2, t3, js_dir):
    lines = []
    all_files = glob.glob(os.path.join(js_dir, "*"))
    all_routes = [(1, route) for route in t1] + [(2, route) for route in t2] + [(3, route) for route in t3]
    tier_labels = {
        1: "高危 — 核心业务与管理",
        2: "中危 — 数据交互",
        3: "低危 — 常规功能",
    }

    lines.append("# API 上下文分析报告")
    lines.append("")
    lines.append("> 自动从 JS bundle 中提取 API 的请求方式、鉴权、参数")
    lines.append("")
    lines.append(f"**数据来源:** {os.path.abspath(js_dir)} 下 {len(all_files)} 个文件 (JS + JSON)")
    lines.append("")

    current_tier = 0
    found_count = 0
    body_lines = []

    for tier, route in all_routes:
        if tier != current_tier:
            current_tier = tier
            body_lines.append(f"## {tier_labels[tier]}")
            body_lines.append("")

        body_lines.append(f"### `{route}`")
        body_lines.append("")

        contexts = list(search_bundle_files(route, js_dir))
        if not contexts:
            body_lines.append("| 项目 | 值 |")
            body_lines.append("|---|---|")
            body_lines.append("| 状态 | :x: 未在 JS bundle 中找到 |")
            body_lines.append("")
            continue

        found_count += 1
        filename, snippet = contexts[0]
        context = detect_context(snippet, route)

        body_lines.append("| 项目 | 值 |")
        body_lines.append("|---|---|")
        body_lines.append(f"| 方法 | **{context['method']}** |")
        body_lines.append(f"| 鉴权 | {context['auth']} |")
        body_lines.append(f"| Content-Type | {context['content_type']} |")
        if context["params"]:
            body_lines.append(f"| 参数 | `{', '.join(context['params'])}` |")
        body_lines.append(f"| 来源文件 | `{filename}` |")
        body_lines.append("")
        body_lines.append("**调用代码片段:**")
        body_lines.append("```javascript")
        body_lines.append(snippet[:600])
        body_lines.append("```")
        body_lines.append("")

        if len(contexts) > 1:
            body_lines.append(f"*（另有 {len(contexts) - 1} 处额外引用，见源文件）*")
            body_lines.append("")

    lines.append(f"**匹配率:** {found_count}/{len(all_routes)} 个 API 在 JS bundle 中找到上下文")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.extend(body_lines)

    return "\n".join(lines)


def validate_args(args):
    if args.concurrent <= 0:
        print("[!] --concurrent 必须大于 0")
        return False
    if args.download_only and args.skip_download:
        print("[!] --download-only 与 --skip-download 不能同时使用")
        return False
    return True


def run_context_args(args):
    if not validate_args(args):
        return 1

    source_dir = os.path.abspath(args.source_dir)
    priority_file = os.path.abspath(args.priority_file)
    js_dir = os.path.abspath(args.js_dir)
    output_file = os.path.abspath(args.output)

    source_files = discover_source_files(source_dir, args.download_source)

    if not args.skip_download:
        if source_files:
            print(f"[*] 下载源文件: {len(source_files)} 个")
            urls, per_source_counts = collect_download_urls(source_files, args.base_url)
            for path, count in per_source_counts:
                print(f"    - {path} -> {count} 条匹配")
            print(f"[*] 共提取 {len(urls)} 个唯一 JS/JSON 下载 URL")

            if os.name == "nt":
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            download_ok = asyncio.run(download_all(urls, js_dir, args.concurrent))
            if args.download_only:
                return 0 if download_ok else 1
        else:
            print("[!] 未找到任何下载源文本文件，跳过下载阶段")
            if args.download_only:
                return 1
    elif args.download_only:
        print("[!] --download-only 与 --skip-download 不能同时使用")
        return 1

    bundle_files = glob.glob(os.path.join(js_dir, "*.js")) + glob.glob(os.path.join(js_dir, "*.json"))
    if not bundle_files:
        print(f"[!] 未找到任何已下载的 JS/JSON 文件: {js_dir}")
        return 1

    t1, t2, t3 = parse_priority_report(priority_file)
    if not t1 and not t2 and not t3:
        print("[!] 未从优先级报告中解析到任何 API 路由")
        print("[!] 请先运行: python function/classify_apis.py")
        return 1

    print(f"[*] 解析到 API 路由: 高危={len(t1)}  中危={len(t2)}  低危={len(t3)}")
    print("[*] 正在 JS/JSON 文件中搜索 API 上下文 ...")
    report = build_report(t1, t2, t3, js_dir)

    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"[*] 上下文报告已生成 -> {output_file}")
    return 0
