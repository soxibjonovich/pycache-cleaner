import shutil
import pathlib
from abc import ABC, abstractmethod

from icecream import ic

from pycache_cleaner.scanner import CacheScan


class Cleaner(ABC):
    """Strategy: how to handle a found cache scan."""

    @abstractmethod
    def clean(self, scan: CacheScan) -> None: ...


class DeleteCleaner(Cleaner):
    def clean(self, scan: CacheScan) -> None:
        for path in scan.dirs:
            shutil.rmtree(path)
            ic("Removed folder", path)
        for path in scan.files:
            path.unlink()
            ic("Removed file", path)


class DryRunCleaner(Cleaner):
    def clean(self, scan: CacheScan) -> None:
        for path in scan.dirs:
            ic("Would remove folder", path)
        for path in scan.files:
            ic("Would remove file", path)
