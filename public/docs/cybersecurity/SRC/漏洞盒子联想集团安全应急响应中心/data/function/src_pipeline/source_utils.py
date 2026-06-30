import os

from src_pipeline.config import DATA_DIR, DEFAULT_SOURCE_DIR, SOURCE_HINT_FILES


def get_base_dir():
    return str(DATA_DIR)


def is_source_dir(path):
    if not os.path.isdir(path):
        return False

    try:
        names = set(os.listdir(path))
    except OSError:
        return False

    if SOURCE_HINT_FILES.issubset(names):
        return True
    return any(name.lower().endswith(".txt") for name in names)


def discover_source_dirs(base_dir):
    candidates = []
    default_dir = os.path.abspath(DEFAULT_SOURCE_DIR)

    if is_source_dir(default_dir):
        candidates.append(default_dir)

    for name in sorted(os.listdir(base_dir)):
        path = os.path.abspath(os.path.join(base_dir, name))
        if path == default_dir:
            continue
        if is_source_dir(path):
            candidates.append(path)

    return candidates


def resolve_initial_source_dir(initial_source_dir=None):
    base_dir = get_base_dir()
    if initial_source_dir and is_source_dir(initial_source_dir):
        return os.path.abspath(initial_source_dir)

    default_dir = os.path.abspath(DEFAULT_SOURCE_DIR)
    if is_source_dir(default_dir):
        return default_dir

    candidates = discover_source_dirs(base_dir)
    if candidates:
        return candidates[0]
    return None
