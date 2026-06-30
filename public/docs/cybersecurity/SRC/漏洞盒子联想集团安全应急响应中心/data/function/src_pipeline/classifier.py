import argparse
import os
import re

from src_pipeline.config import DEFAULT_CLASSIFY_OUTPUT_FILE, DEFAULT_SOURCE_DIR

TIER_1 = ["/admin", "/manage", "/system/", "/user/delete", "/user/remove",
          "/audit", "/config", "/role", "/permission", "/account/",
          "/merchant/", "/enterprise/", "/order/"]
TIER_2 = ["/query", "/export", "/download", "/getDetail", "/getById",
          "/search", "/list", "/save", "/update", "/add", "/remove",
          "/delete", "/upload", "/login", "/register", "/userinfo",
          "/send", "/check", "/settle", "/doLogin", "/fastLogin"]
TIER_3 = ["/log", "/static/", "/version", "/feedback", "/captcha",
          "/sms", "/region", "/address", "/warranty", "/news",
          "/brand", "/position", "/job/config", "/machineType"]

TARGET_DOMAINS = ["lenovo", "baiying", "motorola"]

STATIC_EXT = (".js", ".css", ".png", ".jpg", ".jpeg", ".gif", ".svg",
              ".woff", ".ttf", ".ico", ".map", ".woff2", ".eot")

NOISE_SENSITIVE = [
    r'ref_key\s*:\s*"',
    r'metaKey\s*:\s*"',
    r'keywords\s*:\s*"',
    r'key\s*[=!]==?\s*"',
    r'"trigger-keys"\s*:',
    r'configuration\s*:\s*"',
    r'throwBadOptionException',
    r'keyWord\s*=',
    r'keyword\s*=',
    r'keyValueSeparator',
    r'keydown\s*:',
    r'keypress\s*:',
    r'keyup\s*:',
    r'bytoken\s*=',
]

NOISE_URL = re.compile(
    r"\.(?:jpg|jpeg|png|gif|svg|ico|woff|woff2|ttf|eot|css|js|map)"
    r"(?:\?.*)?(?:#.*)?$",
    re.IGNORECASE,
)

NUXT_PAGE_PATTERNS = [
    r"/_payload\.json$",
    r"/[a-z]+[-]?[a-z]*$",
    r"^/[a-z]+/{PARAM}",
]


def build_parser():
    parser = argparse.ArgumentParser(
        description="从 HaE 导出结果中分类 API、页面路由和敏感字符串"
    )
    parser.add_argument(
        "-s", "--source-dir", "--input-dir",
        dest="source_dir",
        default=DEFAULT_SOURCE_DIR,
        help="HaE 导出目录，默认: %(default)s",
    )
    parser.add_argument(
        "--linkfinder",
        help="显式指定 Linkfinder.txt 路径，优先级高于 --source-dir",
    )
    parser.add_argument(
        "--all-url",
        dest="all_url",
        help="显式指定 ALL URL.txt 路径，优先级高于 --source-dir",
    )
    parser.add_argument(
        "--sensitive",
        help="显式指定 Sensitive Field.txt 路径，优先级高于 --source-dir",
    )
    parser.add_argument(
        "-o", "--output",
        default=DEFAULT_CLASSIFY_OUTPUT_FILE,
        help="输出报告路径，默认: %(default)s",
    )
    return parser


def resolve_source_paths(args):
    source_dir = args.source_dir
    return {
        "source_dir": os.path.abspath(source_dir),
        "linkfinder": os.path.abspath(args.linkfinder or os.path.join(source_dir, "Linkfinder.txt")),
        "all_url": os.path.abspath(args.all_url or os.path.join(source_dir, "ALL URL.txt")),
        "sensitive": os.path.abspath(args.sensitive or os.path.join(source_dir, "Sensitive Field.txt")),
        "output": os.path.abspath(args.output),
    }


def is_file_ref(line):
    if line.startswith("./") or line.startswith("../"):
        return True
    if line.endswith(STATIC_EXT):
        return True
    if re.match(r"^https?://", line):
        return False
    if re.match(r"^/[a-zA-Z]", line):
        return False
    return True


def load_linkfinder(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = [line.strip() for line in f if line.strip()]
    routes = []
    for line in lines:
        if not is_file_ref(line):
            cleaned = re.sub(r"\$\{[^}]+\}", "{PARAM}", line)
            cleaned = re.sub(r"\?.*", "", cleaned)
            routes.append(cleaned)
    return sorted(set(routes))


def load_urls(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = [line.strip() for line in f if line.strip()]
    urls = []
    noise = 0
    for line in lines:
        if not any(domain in line.lower() for domain in TARGET_DOMAINS):
            continue
        if NOISE_URL.search(line):
            noise += 1
            continue
        urls.append(line)
    if noise:
        print(f"    [URL] 已过滤 {noise} 条静态资源")
    return sorted(set(urls))


def is_noise_sensitive(line):
    for pattern in NOISE_SENSITIVE:
        if re.search(pattern, line, re.IGNORECASE):
            return True
    return False


def load_sensitive(filepath):
    if not os.path.exists(filepath):
        return []
    trigger_words = [
        "token", "secret", "appId", "apiKey", "password", "appsecret",
        "signature", "ak", "sk", "authorization", "bearer", "accessKey",
        "appkey", "app_key",
    ]
    key_pattern = re.compile(
        r'(?:^|[^a-z])key[^a-z].{0,20}["\']([a-f0-9]{16,64})["\']',
        re.IGNORECASE,
    )

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = [line.strip() for line in f if line.strip()]

    hits = []
    noise_count = 0
    for line in lines:
        line_lower = line.lower()
        if is_noise_sensitive(line):
            noise_count += 1
            continue

        matched = any(trigger in line_lower for trigger in trigger_words)
        if not matched and not key_pattern.search(line):
            continue
        hits.append(line)

    if noise_count:
        print(f"    [敏感字段] 已过滤 {noise_count} 条框架噪声")
    return sorted(set(hits))


def is_page_route(route):
    if re.search(r"/\w+\.\w+$", route):
        return True
    for pattern in NUXT_PAGE_PATTERNS:
        if re.search(pattern, route):
            return True
    return False


def classify(route):
    route_lower = route.lower()
    for keyword in TIER_1:
        if keyword in route_lower:
            return 1, keyword
    for keyword in TIER_2:
        if keyword in route_lower:
            return 2, keyword
    for keyword in TIER_3:
        if keyword in route_lower:
            return 3, keyword
    if is_page_route(route):
        return 0, "page"
    return 4, ""


def write_report(output_path, source_paths, routes, urls, sensitive, t1, t2, t3, t4, pages):
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        def write_line(text=""):
            f.write(text + "\n")

        write_line("=" * 70)
        write_line("  API 接口优先级分类报告 — 联想百应 SRC")
        write_line("=" * 70)
        write_line()
        write_line("数据来源:")
        write_line(f"  Source Dir:  {source_paths['source_dir']}")
        write_line(f"  Linkfinder:  {source_paths['linkfinder']}")
        write_line(f"  ALL URL:     {source_paths['all_url']}")
        write_line(f"  Sensitive:   {source_paths['sensitive']}")
        write_line()
        write_line("统计:")
        write_line(f"  Linkfinder:  {len(routes)} 条去重路由")
        write_line(f"  ALL URL:     {len(urls)} 条目标域名 URL")
        write_line(f"  Sensitive:   {len(sensitive)} 条敏感字符串")
        write_line()
        write_line(
            f"  优先级分布: 高危={len(t1)}  中危={len(t2)}  低危={len(t3)}  "
            f"未分类={len(t4)}  页面路由={len(pages)}"
        )
        write_line()

        sections = [
            ("第一梯队 [高危] — 核心业务与管理", t1),
            ("第二梯队 [中危] — 数据交互", t2),
            ("第三梯队 [低危] — 常规功能", t3),
            ("未分类 API", t4),
            ("页面路由 (Nuxt 前端页面，非 API)", pages),
        ]

        for title, items in sections:
            write_line("=" * 70)
            write_line(f"  {title} ({len(items)} 条)")
            write_line("=" * 70)
            if items:
                for item in sorted(items):
                    write_line(f"  {item}")
            else:
                write_line("  (无)")
            write_line()

        write_line("=" * 70)
        write_line(f"  目标域名 URL — 子域名泄露 ({len(urls)} 条)")
        write_line("=" * 70)
        for item in urls:
            write_line(f"  {item}")
        write_line()

        write_line("=" * 70)
        write_line(f"  敏感字符串 — 可能硬编码凭据 ({len(sensitive)} 条)")
        write_line("=" * 70)
        for item in sensitive:
            write_line(f"  {item}")


def run_classify_args(args):
    source_paths = resolve_source_paths(args)

    existing_inputs = [
        path for key, path in source_paths.items()
        if key in {"linkfinder", "all_url", "sensitive"} and os.path.exists(path)
    ]
    if not existing_inputs:
        print("[!] 未找到任何输入文件，请检查 --source-dir 或单文件参数")
        return 1

    routes = load_linkfinder(source_paths["linkfinder"])
    urls = load_urls(source_paths["all_url"])
    sensitive = load_sensitive(source_paths["sensitive"])

    t1, t2, t3, t4, pages = [], [], [], [], []
    for route in routes:
        tier, _ = classify(route)
        if tier == 1:
            t1.append(route)
        elif tier == 2:
            t2.append(route)
        elif tier == 3:
            t3.append(route)
        elif tier == 0:
            pages.append(route)
        else:
            t4.append(route)

    write_report(
        source_paths["output"],
        source_paths,
        routes,
        urls,
        sensitive,
        t1,
        t2,
        t3,
        t4,
        pages,
    )

    print(f"[*] 分类完成 -> {source_paths['output']}")
    print(f"    Source Dir:        {source_paths['source_dir']}")
    print(f"    第一梯队(高危):    {len(t1)} 条")
    print(f"    第二梯队(中危):    {len(t2)} 条")
    print(f"    第三梯队(低危):    {len(t3)} 条")
    print(f"    未分类 API:        {len(t4)} 条")
    print(f"    页面路由(非API):   {len(pages)} 条")
    print(f"    子域名泄露:        {len(urls)} 条")
    print(f"    敏感字符串:        {len(sensitive)} 条")
    return 0
