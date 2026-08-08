import pathlib
from collections.abc import Sequence
from dataclasses import dataclass

CACHE_DIR_NAMES: frozenset[str] = frozenset(
    {
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        ".black",
    }
)

CACHE_FILE_SUFFIXES: frozenset[str] = frozenset({".pyc", ".pyo", ".pyd"})

EXCLUDED_DIR_NAMES: frozenset[str] = frozenset(
    {
        ".git",
        ".zed",
        ".vscode",
        ".idea",
        ".venv",
        "venv",
    }
)


@dataclass(frozen=True)
class CacheScan:
    dirs: Sequence[pathlib.Path]
    files: Sequence[pathlib.Path]

    @property
    def count(self) -> int:
        return len(self.dirs) + len(self.files)


class CacheScanner:
    def scan(self, folder: str | pathlib.Path) -> CacheScan:
        root = pathlib.Path(folder)
        if not root.is_dir():
            raise NotADirectoryError(f"{folder!r} is not a directory")

        dirs: list[pathlib.Path] = []
        files: list[pathlib.Path] = []
        self._scan(root, dirs, files)
        return CacheScan(dirs=dirs, files=files)

    def _scan(
        self,
        path: pathlib.Path,
        dirs: list[pathlib.Path],
        files: list[pathlib.Path],
    ) -> None:
        for item in path.iterdir():
            if item.is_dir():
                if item.name in CACHE_DIR_NAMES:
                    dirs.append(item)
                elif item.name not in EXCLUDED_DIR_NAMES and not item.is_symlink():
                    self._scan(item, dirs, files)
            elif item.is_file() and item.suffix in CACHE_FILE_SUFFIXES:
                files.append(item)


def find_cache_paths(folder: str | pathlib.Path) -> CacheScan:
    """Convenience one-shot API: scan and return all cache paths."""
    return CacheScanner().scan(folder)
