import sys

from src_pipeline.runtime_validator import build_parser, run_runtime_args


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        from pipeline_menu import run_interactive_menu

        return run_interactive_menu()

    args = build_parser().parse_args(argv)
    return run_runtime_args(args)


if __name__ == "__main__":
    sys.exit(main())
