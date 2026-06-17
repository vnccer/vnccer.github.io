import sys

from api_context import main
from pipeline_menu import run_interactive_menu


if __name__ == "__main__":
    argv = sys.argv[1:]
    if not argv:
        sys.exit(run_interactive_menu())
    if "--download-only" not in argv:
        argv = ["--download-only"] + argv
    sys.exit(main(argv))
