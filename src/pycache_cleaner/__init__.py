import argparse

from icecream import ic

from pycache_cleaner.cleaner import Cleaner, DeleteCleaner, DryRunCleaner
from pycache_cleaner.scanner import CacheScanner, CacheScan

ic.configureOutput(lineWrapWidth=10**6)


def main() -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="CLI version of pycache cleaner"
    )
    parser.add_argument(
        "-f", "--folder", type=str, help="Folder for seeking and cleaning from caches"
    )
    parser.add_argument(
        "--test", action="store_true", help="Ping check: prints 'pong' if it works"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without deleting",
    )

    arguments: argparse.Namespace = parser.parse_args()
    if arguments.test:
        ic("pong")
        return 0
    if not arguments.folder:
        parser.error("the -f/--folder argument is required")

    scanning = f"Scanning for Python cache files in: {arguments.folder}"
    ic(scanning)
    scan: CacheScan = CacheScanner().scan(arguments.folder)
    ic.configureOutput(prefix="\tic| ")
    for path in scan.dirs:
        line = f"\t{path}"
        ic(line)
    for path in scan.files:
        line = f"\t{path}"
        ic(line)
    ic.configureOutput(prefix="ic| ")
    found = f"Found {scan.count} cache item(s): {len(scan.dirs)} dir(s), {len(scan.files)} file(s)"
    ic(found)

    cleaner: Cleaner = DryRunCleaner() if arguments.dry_run else DeleteCleaner()
    cleaner.clean(scan)

    done = f"Done: {scan.count} cache item(s) handled"
    ic(done)
    return 0
