import argparse
import json
import os
import re
import ssl
from dataclasses import dataclass
from datetime import datetime
from difflib import SequenceMatcher
from html import unescape
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import HTTPRedirectHandler, HTTPSHandler, Request, build_opener as urllib_build_opener

from src_pipeline.config import (
    DEFAULT_BASE_URL,
    DEFAULT_CONTEXT_OUTPUT_FILE,
    DEFAULT_FAKE200_REQUEST_SAMPLE_FILE,
    DEFAULT_FAKE200_RESPONSE_SAMPLE_FILE,
    DEFAULT_HOME_REQUEST_SAMPLE_FILE,
    DEFAULT_HOME_RESPONSE_SAMPLE_FILE,
    DEFAULT_RUNTIME_REPORT_FILE,
)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
SPA_MARKERS = (
    "/_nuxt/",
    "_payload.json",
    "data-capo",
    "<!doctype html",
    "<html",
    "__nuxt",
)
API_LIKE_HINTS = (
    "/api/",
    "-server/",
    "/merchant/",
    "/admin/",
    "/login-server/",
    "/qrcode-server/",
    "/app-version-manage-server/",
)
RESULT_LABELS = {
    "spa_fallback_200": "疑似伪 200 / SPA 兜底",
    "json_api": "更像真实接口（JSON/结构化响应）",
    "html_page": "返回 HTML 页面",
    "redirect": "发生重定向",
    "manual_check": "需人工复核",
    "request_error": "请求失败",
    "unknown": "未能判定",
}


@dataclass
class ContextEntry:
    tier: str
    route: str
    method: str = "?"
    auth: str = "?"
    content_type: str = "?"
    source_file: str = ""
    snippet: str = ""


@dataclass
class RawHttpResponse:
    status_line: str
    status_code: int
    headers: dict
    body: str


@dataclass
class Baseline:
    homepage_title: str = ""
    homepage_markers: tuple = ()
    homepage_normalized_body: str = ""
    homepage_status: int = 0
    sample_fake_title: str = ""
    sample_fake_similarity: float = 0.0
    sample_fake_verdict: str = "unknown"
    sample_paths_loaded: tuple = ()


class NoRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def build_parser():
    parser = argparse.ArgumentParser(
        description="校验 API 是否返回伪 200 / SPA 单页应用兜底 HTML"
    )
    parser.add_argument(
        "--context-report",
        default=DEFAULT_CONTEXT_OUTPUT_FILE,
        help="api_context.py 生成的上下文报告，默认: %(default)s",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="接口请求基准域名，默认: %(default)s",
    )
    parser.add_argument(
        "--homepage-request-sample",
        default=DEFAULT_HOME_REQUEST_SAMPLE_FILE,
        help="主页样本请求文件，默认: %(default)s",
    )
    parser.add_argument(
        "--homepage-response-sample",
        default=DEFAULT_HOME_RESPONSE_SAMPLE_FILE,
        help="主页样本响应文件，默认: %(default)s",
    )
    parser.add_argument(
        "--fake-request-sample",
        default=DEFAULT_FAKE200_REQUEST_SAMPLE_FILE,
        help="伪 200 样本请求文件，默认: %(default)s",
    )
    parser.add_argument(
        "--fake-response-sample",
        default=DEFAULT_FAKE200_RESPONSE_SAMPLE_FILE,
        help="伪 200 样本响应文件，默认: %(default)s",
    )
    parser.add_argument(
        "--offline-only",
        action="store_true",
        help="只做离线样本自检与接口整理，不主动请求线上接口",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="单个接口请求超时秒数，默认: %(default)s",
    )
    parser.add_argument(
        "-o", "--output",
        default=DEFAULT_RUNTIME_REPORT_FILE,
        help="输出 Markdown 报告路径，默认: %(default)s",
    )
    return parser


def validate_args(args):
    if args.timeout <= 0:
        print("[!] --timeout 必须大于 0")
        return False
    return True


def load_text_file(path):
    if not path or not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def parse_raw_http_response(text):
    if not text.strip():
        return RawHttpResponse("", 0, {}, "")

    parts = re.split(r"\r?\n\r?\n", text, maxsplit=1)
    header_text = parts[0]
    body = parts[1] if len(parts) > 1 else ""

    lines = header_text.splitlines()
    status_line = lines[0].strip() if lines else ""
    status_match = re.search(r"\s(\d{3})\b", status_line)
    status_code = int(status_match.group(1)) if status_match else 0

    headers = {}
    current_name = None
    for line in lines[1:]:
        if line.startswith((" ", "\t")) and current_name:
            headers[current_name] = headers[current_name] + " " + line.strip()
            continue
        if ":" not in line:
            continue
        name, value = line.split(":", 1)
        current_name = name.strip().lower()
        headers[current_name] = value.strip()

    return RawHttpResponse(status_line, status_code, headers, body)


def parse_request_line(request_text):
    first_line = request_text.splitlines()[0].strip() if request_text.strip() else ""
    match = re.match(r"([A-Z]+)\s+(\S+)\s+HTTP/", first_line)
    if not match:
        return "", ""
    return match.group(1).upper(), match.group(2)


def extract_title(body):
    match = re.search(r"<title[^>]*>(.*?)</title>", body, re.IGNORECASE | re.DOTALL)
    if not match:
        return ""
    title = unescape(match.group(1))
    return re.sub(r"\s+", " ", title).strip()


def normalize_html(body):
    text = unescape(body or "")
    text = text.lower()
    text = re.sub(r"https?://[^\s\"'<>]+", "http://host/", text)
    text = re.sub(r"/_payload\.json\?[a-z0-9\-]+", "/_payload.json", text)
    text = re.sub(r"/_nuxt/[a-z0-9._-]+", "/_nuxt/asset", text)
    text = re.sub(r"\b[a-f0-9]{32,64}\b", "<hash>", text)
    text = re.sub(
        r"\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b",
        "<uuid>",
        text,
    )
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def similarity_ratio(left, right):
    if not left or not right:
        return 0.0
    return SequenceMatcher(None, left[:200000], right[:200000]).ratio()


def find_spa_markers(body):
    body_lower = (body or "").lower()
    return tuple(marker for marker in SPA_MARKERS if marker in body_lower)


def is_json_response(content_type, body):
    content_type = (content_type or "").lower()
    stripped = (body or "").lstrip()

    if "json" in content_type:
        return True
    if not stripped or stripped[0] not in "{[":
        return False

    try:
        json.loads(stripped)
    except Exception:
        return False
    return True


def is_html_response(content_type, body):
    content_type = (content_type or "").lower()
    stripped = (body or "").lstrip().lower()
    if "text/html" in content_type:
        return True
    return stripped.startswith("<!doctype html") or stripped.startswith("<html")


def route_looks_api(route):
    route_lower = route.lower()
    return any(hint in route_lower for hint in API_LIKE_HINTS)


def parse_context_report(path):
    if not os.path.exists(path):
        print(f"[!] 未找到上下文报告: {path}")
        return []

    entries = []
    current = None
    current_tier = "未分组"
    in_code_block = False

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")

            if line.startswith("## "):
                current_tier = line[3:].strip()
                continue

            route_match = re.match(r"^### `(.+)`$", line)
            if route_match:
                if current:
                    entries.append(current)
                current = ContextEntry(tier=current_tier, route=route_match.group(1).strip())
                in_code_block = False
                continue

            if not current:
                continue

            if line.startswith("```"):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                current.snippet += line + "\n"
                continue

            match = re.match(r"^\| 方法 \| \*\*(.+?)\*\* \|$", line)
            if match:
                current.method = match.group(1).strip()
                continue

            match = re.match(r"^\| 鉴权 \| (.+?) \|$", line)
            if match:
                current.auth = match.group(1).strip()
                continue

            match = re.match(r"^\| Content-Type \| (.+?) \|$", line)
            if match:
                current.content_type = match.group(1).strip()
                continue

            match = re.match(r"^\| 来源文件 \| `(.+?)` \|$", line)
            if match:
                current.source_file = match.group(1).strip()
                continue

    if current:
        entries.append(current)

    return entries


def extract_query_keys(snippet):
    seen = []
    for key in re.findall(r"[?&]([A-Za-z_][A-Za-z0-9_]*)=", snippet or ""):
        if key not in seen:
            seen.append(key)
    return seen


def extract_route_expression(snippet, route):
    if not snippet:
        return ""

    candidates = [route, route.rstrip("/")]
    index = -1
    matched = ""
    for candidate in candidates:
        if not candidate:
            continue
        index = snippet.find(candidate)
        if index != -1:
            matched = candidate
            break

    if index == -1:
        return snippet[:180]

    start = max(0, index - 8)
    tail = snippet[start:index + len(matched) + 220]
    boundary_markers = (
        ")}function",
        "};function",
        ");function",
        ")}var ",
        "}),",
        ";\n",
        "\nfunction",
    )
    cut_positions = [tail.find(marker) for marker in boundary_markers if tail.find(marker) != -1]
    if cut_positions:
        tail = tail[:min(cut_positions)]
    return tail


def build_test_path(entry):
    path = entry.route
    reasons = []
    route_expression = extract_route_expression(entry.snippet, entry.route)

    if "{PARAM}" in path:
        path = path.replace("{PARAM}", "1")
        reasons.append("将 {PARAM} 自动替换为 1")

    if path.endswith("/") and path != "/":
        path = path + "1"
        reasons.append("检测到尾部斜杠，自动补位路径参数 1")

    existing_keys = set(re.findall(r"[?&]([A-Za-z_][A-Za-z0-9_]*)=", path))
    query_keys = [key for key in extract_query_keys(route_expression) if key not in existing_keys]
    if query_keys:
        connector = "&" if "?" in path else "?"
        path = path + connector + "&".join(f"{key}=1" for key in query_keys)
        reasons.append("根据调用片段补齐查询参数: " + ", ".join(query_keys))

    return path, reasons


def build_absolute_url(base_url, path):
    return urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


def build_baseline(args):
    homepage_response_text = load_text_file(args.homepage_response_sample)
    fake_response_text = load_text_file(args.fake_response_sample)
    homepage_request_text = load_text_file(args.homepage_request_sample)
    fake_request_text = load_text_file(args.fake_request_sample)

    homepage_response = parse_raw_http_response(homepage_response_text)
    fake_response = parse_raw_http_response(fake_response_text)

    baseline = Baseline()
    baseline.sample_paths_loaded = tuple(
        path for path in (
            args.homepage_request_sample,
            args.homepage_response_sample,
            args.fake_request_sample,
            args.fake_response_sample,
        )
        if os.path.exists(path)
    )

    baseline.homepage_status = homepage_response.status_code
    baseline.homepage_title = extract_title(homepage_response.body)
    baseline.homepage_markers = find_spa_markers(homepage_response.body)
    baseline.homepage_normalized_body = normalize_html(homepage_response.body)

    if fake_response.body and baseline.homepage_normalized_body:
        baseline.sample_fake_title = extract_title(fake_response.body)
        baseline.sample_fake_similarity = similarity_ratio(
            baseline.homepage_normalized_body,
            normalize_html(fake_response.body),
        )

        sample_entry = ContextEntry(
            tier="样本",
            route=parse_request_line(fake_request_text)[1] or "/sample/fake200",
            method=parse_request_line(fake_request_text)[0] or "GET",
            auth="无",
            snippet="",
        )
        verdict = classify_response(
            sample_entry,
            sample_entry.route,
            fake_response.status_code,
            fake_response.headers.get("content-type", ""),
            fake_response.body,
            baseline,
        )
        baseline.sample_fake_verdict = verdict["result"]

    return baseline


def create_http_opener():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    return urllib_build_opener(NoRedirectHandler(), HTTPSHandler(context=ssl_context))


def fetch_url(opener, url, timeout):
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
        },
        method="GET",
    )

    try:
        response = opener.open(request, timeout=timeout)
        status = getattr(response, "status", None) or response.getcode()
        headers = {key.lower(): value for key, value in response.headers.items()}
        body_bytes = response.read()
        encoding = response.headers.get_content_charset() or "utf-8"
        body = body_bytes.decode(encoding, errors="replace")
        return {
            "status": status,
            "headers": headers,
            "body": body,
            "final_url": response.geturl(),
            "error": "",
        }
    except HTTPError as exc:
        headers = {key.lower(): value for key, value in exc.headers.items()} if exc.headers else {}
        body_bytes = exc.read() if hasattr(exc, "read") else b""
        body = body_bytes.decode("utf-8", errors="replace")
        return {
            "status": exc.code,
            "headers": headers,
            "body": body,
            "final_url": exc.geturl() if hasattr(exc, "geturl") else url,
            "error": str(exc),
        }
    except URLError as exc:
        return {
            "status": 0,
            "headers": {},
            "body": "",
            "final_url": url,
            "error": str(exc.reason),
        }
    except Exception as exc:
        return {
            "status": 0,
            "headers": {},
            "body": "",
            "final_url": url,
            "error": str(exc),
        }


def classify_response(entry, tested_path, status, content_type, body, baseline):
    reasons = []
    markers = find_spa_markers(body)
    title = extract_title(body)
    normalized = normalize_html(body)
    similarity = similarity_ratio(baseline.homepage_normalized_body, normalized)
    api_like = route_looks_api(entry.route)
    result = "unknown"

    if status == 0:
        result = "request_error"
        if body:
            reasons.append("请求失败，但目标返回了部分响应体")
        return {
            "result": result,
            "title": title,
            "similarity": similarity,
            "markers": markers,
            "reasons": reasons,
        }

    if 300 <= status < 400:
        result = "redirect"
        reasons.append(f"HTTP 状态码为 {status}，属于重定向响应")
        return {
            "result": result,
            "title": title,
            "similarity": similarity,
            "markers": markers,
            "reasons": reasons,
        }

    if is_json_response(content_type, body):
        result = "json_api"
        reasons.append("Content-Type 或响应体特征更像 JSON/结构化数据")
        if status in (401, 403):
            reasons.append(f"返回 {status}，更像鉴权失败而非前端兜底")
        return {
            "result": result,
            "title": title,
            "similarity": similarity,
            "markers": markers,
            "reasons": reasons,
        }

    if is_html_response(content_type, body):
        if title:
            reasons.append(f"返回 HTML，页面标题为：{title}")
        if markers:
            reasons.append("命中 SPA/Nuxt 标记: " + ", ".join(markers[:4]))
        if baseline.homepage_title and title == baseline.homepage_title:
            reasons.append("页面标题与主页样本完全一致")
        if similarity >= 0.90:
            reasons.append(f"与主页样本相似度较高: {similarity:.3f}")
        elif similarity >= 0.75:
            reasons.append(f"与主页样本存在明显相似: {similarity:.3f}")

        if status == 200 and api_like and len(markers) >= 3 and (
            title == baseline.homepage_title or similarity >= 0.88
        ):
            result = "spa_fallback_200"
        elif status == 200:
            result = "html_page"
        else:
            result = "unknown"

        return {
            "result": result,
            "title": title,
            "similarity": similarity,
            "markers": markers,
            "reasons": reasons,
        }

    if status in (401, 403):
        result = "manual_check"
        reasons.append(f"返回 {status}，需要结合鉴权状态继续人工判断")
    else:
        reasons.append("响应既不像 JSON，也不像 SPA HTML")

    return {
        "result": result,
        "title": title,
        "similarity": similarity,
        "markers": markers,
        "reasons": reasons,
    }


def result_advice(result_key, auth):
    if result_key == "spa_fallback_200":
        return "优先视为伪 200 候选，先与主页 HTML 做 diff，再决定是否继续 Burp 手测。"
    if result_key == "json_api":
        if auth != "无":
            return "更像真实接口；建议补真实 Token 后继续测鉴权、越权和参数处理。"
        return "更像真实接口；建议继续做越权、参数污染、注入和业务逻辑测试。"
    if result_key == "html_page":
        return "该路由当前更像返回网页而非数据接口，建议确认它是不是前端页面或网关页。"
    if result_key == "redirect":
        return "查看 Location、登录态和网关跳转逻辑，确认是否被重定向到登录或主页。"
    if result_key == "manual_check":
        return "需要真实参数或真实登录态，建议从浏览器实际操作流量中抓一条原始请求再复测。"
    if result_key == "request_error":
        return "请求失败，建议检查网络、证书、WAF 或稍后重试。"
    return "暂未形成稳定结论，建议结合 Burp 原始响应继续人工判断。"


def is_known_http_method(method):
    return method.upper() in {"GET", "POST", "PUT", "PATCH", "DELETE"}


def should_keep_in_compact_report(item):
    entry = item["entry"]
    if item["result"] == "spa_fallback_200":
        return False
    if route_looks_api(entry.route):
        return True
    return is_known_http_method(entry.method)


def is_priority_candidate(item):
    return item["result"] in {"json_api", "redirect", "unknown"}


def format_compact_note(item):
    notes = []

    if item["result"] == "manual_check":
        if item["entry"].method.upper() != "GET":
            notes.append("非 GET，未自动请求")
        elif item["status"] in {"401", "403", 401, 403}:
            notes.append(f"返回 {item['status']}，更像鉴权/登录限制")
        else:
            notes.append("需要真实参数或真实登录态")
    elif item["result"] == "html_page":
        notes.append("返回 HTML，但未命中主页型 SPA 兜底")
    elif item["result"] == "request_error":
        notes.append("请求失败")
    elif item["result"] == "redirect":
        notes.append(f"返回 {item['status']} 重定向")
    elif item["result"] == "json_api":
        notes.append("响应更像真实 JSON 接口")
    elif item["result"] == "unknown":
        notes.append("未命中伪 200 特征")

    if item["similarity"] and item["similarity"] < 0.88:
        notes.append(f"主页相似度 {item['similarity']:.3f}")
    if item["request_error"]:
        notes.append(item["request_error"])

    return "；".join(notes) or "可继续复核"


def build_compact_report(results, baseline, args):
    lines = []
    now_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    excluded = [item for item in results if item["result"] == "spa_fallback_200"]
    kept = [item for item in results if should_keep_in_compact_report(item)]
    priority = [item for item in kept if is_priority_candidate(item)]
    manual = [item for item in kept if not is_priority_candidate(item)]

    lines.append("# 排除伪 200 后的接口名单")
    lines.append("")
    lines.append("> 在线校验已自动剔除命中 SPA 兜底特征的接口，下面保留的是后续仍值得继续手测或人工复核的目标。")
    lines.append("")
    lines.append(f"**生成时间:** {now_text}")
    lines.append("")
    lines.append(f"**基准域名:** {args.base_url}")
    lines.append("")
    lines.append(f"**主页样本标题:** {baseline.homepage_title or '未提取到'}")
    lines.append("")
    lines.append("## 结果概览")
    lines.append("")
    lines.append("| 项目 | 数量 |")
    lines.append("|---|---|")
    lines.append(f"| 总接口数 | {len(results)} |")
    lines.append(f"| 已排除伪 200 | {len(excluded)} |")
    lines.append(f"| 保留接口数 | {len(kept)} |")
    lines.append(f"| 可优先继续测试 | {len(priority)} |")
    lines.append(f"| 需人工复核 | {len(manual)} |")
    lines.append("")

    lines.append("## 可优先继续测试")
    lines.append("")
    if priority:
        lines.append("| 方法 | 接口 | 鉴权 | HTTP 状态 | 结论 | 备注 |")
        lines.append("|---|---|---|---|---|---|")
        for item in priority:
            entry = item["entry"]
            lines.append(
                f"| {entry.method} | `{entry.route}` | {entry.auth} | {item['status'] or '—'} | "
                f"{RESULT_LABELS[item['result']]} | {format_compact_note(item)} |"
            )
    else:
        lines.append("当前没有自动判定为可直接继续测试的接口。")
    lines.append("")

    lines.append("## 需人工复核")
    lines.append("")
    if manual:
        lines.append("| 方法 | 接口 | 鉴权 | HTTP 状态 | 结论 | 备注 |")
        lines.append("|---|---|---|---|---|---|")
        for item in manual:
            entry = item["entry"]
            lines.append(
                f"| {entry.method} | `{entry.route}` | {entry.auth} | {item['status'] or '—'} | "
                f"{RESULT_LABELS[item['result']]} | {format_compact_note(item)} |"
            )
    else:
        lines.append("当前没有需要人工复核的保留接口。")
    lines.append("")

    lines.append("## 说明")
    lines.append("")
    lines.append(f"- 已自动排除的伪 200 接口数量: {len(excluded)}")
    lines.append("- 当前版本仍只自动请求 GET；POST/PUT/PATCH/DELETE 默认保留到“需人工复核”。")
    lines.append("- 页面路由类噪声已在精简输出中尽量压缩，只保留更像接口的目标。")

    return "\n".join(lines)


def validate_entry(entry, opener, args, baseline):
    if entry.method.upper() != "GET":
        return {
            "entry": entry,
            "tested_path": entry.route,
            "tested_url": build_absolute_url(args.base_url, entry.route),
            "status": "",
            "content_type": "",
            "result": "manual_check",
            "reasons": ["当前版本只自动校验 GET，避免误触发写操作"],
            "advice": result_advice("manual_check", entry.auth),
            "title": "",
            "similarity": 0.0,
            "markers": (),
            "request_error": "",
        }

    tested_path, build_reasons = build_test_path(entry)
    tested_url = build_absolute_url(args.base_url, tested_path)

    if args.offline_only:
        reasons = ["已启用 --offline-only，未主动请求线上接口"]
        reasons.extend(build_reasons)
        return {
            "entry": entry,
            "tested_path": tested_path,
            "tested_url": tested_url,
            "status": "",
            "content_type": "",
            "result": "manual_check",
            "reasons": reasons,
            "advice": result_advice("manual_check", entry.auth),
            "title": "",
            "similarity": 0.0,
            "markers": (),
            "request_error": "",
        }

    response = fetch_url(opener, tested_url, args.timeout)
    content_type = response["headers"].get("content-type", "")
    verdict = classify_response(
        entry,
        tested_path,
        response["status"],
        content_type,
        response["body"],
        baseline,
    )
    reasons = list(build_reasons)
    reasons.extend(verdict["reasons"])
    if response["error"] and response["status"]:
        reasons.append(f"请求过程附带异常信息: {response['error']}")

    return {
        "entry": entry,
        "tested_path": tested_path,
        "tested_url": tested_url,
        "status": response["status"] or "",
        "content_type": content_type,
        "result": verdict["result"],
        "reasons": reasons,
        "advice": result_advice(verdict["result"], entry.auth),
        "title": verdict["title"],
        "similarity": verdict["similarity"],
        "markers": verdict["markers"],
        "request_error": response["error"] if response["status"] == 0 else "",
    }


def build_report(entries, results, baseline, args):
    if not args.offline_only:
        return build_compact_report(results, baseline, args)

    lines = []
    now_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = {}
    for item in results:
        summary[item["result"]] = summary.get(item["result"], 0) + 1

    lines.append("# API 运行时校验报告")
    lines.append("")
    lines.append("> 目标: 识别高危/中危/低危 API 中哪些请求实际上返回了 SPA 单页应用兜底 HTML，而不是后端真实接口数据。")
    lines.append("")
    lines.append(f"**生成时间:** {now_text}")
    lines.append("")
    lines.append(f"**上下文报告:** {os.path.abspath(args.context_report)}")
    lines.append("")
    lines.append(f"**基准域名:** {args.base_url}")
    lines.append("")
    lines.append(f"**运行模式:** {'离线样本模式' if args.offline_only else '在线请求 + 离线样本基线'}")
    lines.append("")
    lines.append("## 样本基线")
    lines.append("")
    lines.append("| 项目 | 值 |")
    lines.append("|---|---|")
    lines.append(f"| 主页样本状态码 | {baseline.homepage_status or '未加载'} |")
    lines.append(f"| 主页样本标题 | {baseline.homepage_title or '未提取到'} |")
    lines.append(
        f"| 主页样本 SPA 标记 | {', '.join(baseline.homepage_markers) if baseline.homepage_markers else '未提取到'} |"
    )
    lines.append(
        f"| 伪 200 样本与主页相似度 | {baseline.sample_fake_similarity:.3f} |"
        if baseline.sample_fake_similarity
        else "| 伪 200 样本与主页相似度 | 未计算 |"
    )
    lines.append(
        f"| 伪 200 样本判定 | {RESULT_LABELS.get(baseline.sample_fake_verdict, baseline.sample_fake_verdict)} |"
    )
    lines.append(
        f"| 已加载样本文件 | {', '.join(os.path.basename(path) for path in baseline.sample_paths_loaded) if baseline.sample_paths_loaded else '未找到样本文件'} |"
    )
    lines.append("")
    lines.append("## 判定摘要")
    lines.append("")
    lines.append("| 结论 | 数量 |")
    lines.append("|---|---|")
    for key in (
        "spa_fallback_200",
        "json_api",
        "html_page",
        "redirect",
        "manual_check",
        "request_error",
        "unknown",
    ):
        lines.append(f"| {RESULT_LABELS[key]} | {summary.get(key, 0)} |")
    lines.append("")
    lines.append("## 逐条结果")
    lines.append("")

    for item in results:
        entry = item["entry"]
        lines.append(f"### `{entry.route}`")
        lines.append("")
        lines.append("| 项目 | 值 |")
        lines.append("|---|---|")
        lines.append(f"| 分组 | {entry.tier} |")
        lines.append(f"| 方法 | **{entry.method}** |")
        lines.append(f"| 鉴权 | {entry.auth} |")
        lines.append(f"| 测试路径 | `{item['tested_path']}` |")
        lines.append(f"| 测试 URL | `{item['tested_url']}` |")
        lines.append(f"| HTTP 状态 | {item['status'] or '未请求'} |")
        lines.append(f"| Content-Type | {item['content_type'] or '—'} |")
        lines.append(f"| 结论 | **{RESULT_LABELS[item['result']]}** |")
        if item["title"]:
            lines.append(f"| 页面标题 | {item['title']} |")
        if item["similarity"]:
            lines.append(f"| 与主页样本相似度 | {item['similarity']:.3f} |")
        if item["markers"]:
            lines.append(f"| 命中 SPA 标记 | {', '.join(item['markers'])} |")
        if entry.source_file:
            lines.append(f"| 来源文件 | `{entry.source_file}` |")
        lines.append("")
        lines.append("**判定依据:**")
        for reason in item["reasons"] or ["暂无"]:
            lines.append(f"- {reason}")
        lines.append("")
        lines.append(f"**建议:** {item['advice']}")
        lines.append("")
        if item["request_error"]:
            lines.append(f"**请求异常:** `{item['request_error']}`")
            lines.append("")

    return "\n".join(lines)


def run_runtime_args(args):
    if not validate_args(args):
        return 1

    context_report = os.path.abspath(args.context_report)
    output_file = os.path.abspath(args.output)
    args.context_report = context_report
    args.output = output_file

    entries = parse_context_report(context_report)
    if not entries:
        print("[!] 未从 api_context_report.md 中解析到任何接口")
        print("[!] 请先运行: python function/api_context.py")
        return 1

    print(f"[*] 已解析上下文条目: {len(entries)} 个")
    baseline = build_baseline(args)
    if baseline.homepage_title:
        print(f"[*] 已加载主页样本标题: {baseline.homepage_title}")
    else:
        print("[!] 未加载到主页样本，部分相似度判断会变弱")

    opener = None if args.offline_only else create_http_opener()
    results = []

    for index, entry in enumerate(entries, start=1):
        print(f"[*] [{index}/{len(entries)}] 校验 {entry.method} {entry.route}")
        results.append(validate_entry(entry, opener, args, baseline))

    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    report = build_report(entries, results, baseline, args)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"[*] 运行时校验报告已生成 -> {output_file}")
    return 0
