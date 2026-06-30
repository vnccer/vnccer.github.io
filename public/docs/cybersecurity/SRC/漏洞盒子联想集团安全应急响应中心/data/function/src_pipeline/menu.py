from src_pipeline.source_utils import (
    discover_source_dirs,
    get_base_dir,
    is_source_dir,
    resolve_initial_source_dir,
)


def prompt_choice(prompt, valid_choices):
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print("[!] 请输入有效编号")


def choose_source_dir(current_source_dir=None):
    base_dir = get_base_dir()
    candidates = discover_source_dirs(base_dir)

    print("\n请选择数据源目录:")
    if candidates:
        for index, path in enumerate(candidates, start=1):
            marker = " (当前)" if current_source_dir and path == current_source_dir else ""
            print(f"{index}. {path}{marker}")
    else:
        print("1. 当前目录下未发现候选数据源，建议手动输入")

    manual_index = len(candidates) + 1
    print(f"{manual_index}. 手动输入目录路径")
    print("0. 返回上一级")

    valid_choices = {"0", str(manual_index)}
    valid_choices.update(str(index) for index in range(1, len(candidates) + 1))
    choice = prompt_choice("请输入编号: ", valid_choices)

    if choice == "0":
        return current_source_dir

    if choice == str(manual_index):
        while True:
            raw_path = input("请输入目录路径: ").strip().strip('"')
            if not raw_path:
                print("[!] 路径不能为空")
                continue
            if is_source_dir(raw_path):
                return raw_path
            print("[!] 该目录不是有效的数据源目录，至少应包含 Linkfinder.txt / ALL URL.txt / Sensitive Field.txt")

    return candidates[int(choice) - 1]


def ensure_source_dir(current_source_dir=None):
    source_dir = resolve_initial_source_dir(current_source_dir)
    if source_dir:
        return source_dir

    print("[!] 当前未找到默认数据源目录，请先选择数据源")
    return choose_source_dir(current_source_dir)


def run_classify(source_dir):
    import classify_apis

    return classify_apis.main(["--source-dir", source_dir])


def run_download(source_dir):
    import api_context

    return api_context.main(["--source-dir", source_dir, "--download-only"])


def run_context_only(source_dir):
    import api_context

    return api_context.main(["--source-dir", source_dir, "--skip-download"])


def run_full_pipeline(source_dir):
    result = run_classify(source_dir)
    if result != 0:
        return result

    import api_context

    return api_context.main(["--source-dir", source_dir])


def run_runtime_validate():
    import runtime_validate
    from src_pipeline.config import DEFAULT_CONTEXT_OUTPUT_FILE

    return runtime_validate.main(["--context-report", DEFAULT_CONTEXT_OUTPUT_FILE])


def print_main_menu(source_dir):
    print("\n" + "=" * 70)
    print("联想百应 SRC Python 流水线")
    print("=" * 70)
    print(f"当前数据源目录: {source_dir or '(未选择)'}")
    print()
    print("请选择你的使用方式:")
    print("1. 仅进行 JS/JSON 下载")
    print("2. 仅进行 API 分类（生成 reports/api_priority_report.txt）")
    print("3. 仅补全 API 上下文（跳过下载，生成 reports/api_context_report.md）")
    print("4. 执行完整流水线（分类 -> 下载 -> 上下文）")
    print("5. 选择数据源目录")
    print("6. 校验接口是否为伪 200 / SPA 兜底（生成 reports/api_runtime_validation_report.md）")
    print("0. 退出")


def run_interactive_menu(initial_source_dir=None):
    source_dir = resolve_initial_source_dir(initial_source_dir)

    while True:
        print_main_menu(source_dir)
        choice = prompt_choice("请输入编号: ", {"0", "1", "2", "3", "4", "5", "6"})

        if choice == "0":
            print("[*] 已退出")
            return 0

        if choice == "5":
            source_dir = choose_source_dir(source_dir)
            continue

        if choice == "6":
            return run_runtime_validate()

        source_dir = ensure_source_dir(source_dir)
        if not source_dir:
            print("[!] 未选择有效数据源目录")
            continue

        if choice == "1":
            return run_download(source_dir)
        if choice == "2":
            return run_classify(source_dir)
        if choice == "3":
            return run_context_only(source_dir)
        if choice == "4":
            return run_full_pipeline(source_dir)

    return 0
