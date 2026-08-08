import argparse

from icecream import ic

from pycache_cleaner.cleaner import Cleaner, DeleteCleaner, DryRunCleaner
from pycache_cleaner.scanner import CacheScanner


def main() -> None:
    parser = argparse.ArgumentParser(description="CLI version of pycache cleaner")
    parser.add_argument("-f", "--folder", type=str, help="Folder for seeking and cleaning from caches")
    parser.add_argument("--test", action="store_true", help="Ping check: prints 'pong' if it works")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be removed without deleting")

    arguments = parser.parse_args()
    if arguments.test:
        ic("pong")
        return
    if not arguments.folder:
        parser.error("the -f/--folder argument is required")

    ic(f"Scanning for Python cache files in: {arguments.folder}")
    scan = CacheScanner().scan(arguments.folder)
    ic("Scan complete", scan.dirs, scan.files)

    cleaner: Cleaner = DryRunCleaner() if arguments.dry_run else DeleteCleaner()
    cleaner.clean(scan)

    ic("Done", scan.count, "cache item(s) handled")
