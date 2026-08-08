import pathlib

from icecream import ic

CACHE_TARGETS = {
    "dirs": {
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        ".black",
    },
    "extensions": {
        ".pyc",
        ".pyo",
        ".pyd"
    },
    "exclude": {
        ".git",
        ".zed",
        ".vscode",
        ".idea",
        ".venv",
        "venv"
    }
}
def main():
    import argparse

    parser = argparse.ArgumentParser(description="CLI version of pycache cleaner")
    parser.add_argument("-f", "--folder", type=str, help="Folder for seeking and cleaning from caches")
    parser.add_argument("--test", action="store_true", help="Ping check: prints 'pong' if it works")

    arguments = parser.parse_args()
    if arguments.test:
        ic("pong")
        return
    if not arguments.folder:
        parser.error("the -f/--folder argument is required")
    clean_caches(arguments.folder)

def clean_caches(folder: str):
    ic(f"Scanning for Python cache files in: {pathlib.Path(folder).resolve()}")
    folders = seek_cache_folders(folder)
    remove_folders(folders)

def seek_cache_folders(folder: str):
    folders: list[pathlib.Path] = []
    path = pathlib.Path(folder)

    for item in path.iterdir():
        if item.is_dir() and item.name in CACHE_TARGETS["dirs"]:
            ic("Matched cache dir", item)
            folders.append(item)
            continue
        if item.is_file() and item.suffix in CACHE_TARGETS["extensions"]:
            ic("Matched cache file", item)
            folders.append(item)
            continue
        if item.is_dir() and not item.is_symlink() and item.name not in CACHE_TARGETS["exclude"]:
            sub_folders: list[pathlib.Path] = seek_cache_folders(item.resolve())
            folders.extend(sub_folders)

    ic("Scan complete", folder, folders)
    return folders

def remove_folders(folders: list[pathlib.Path]):
    import shutil

    for folder in folders:
        if folder.is_dir():
            shutil.rmtree(folder)
            ic("Removed folder", folder)
        elif folder.is_file():
            folder.unlink()
            ic("Removed file", folder)
