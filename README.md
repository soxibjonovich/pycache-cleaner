# pycache-cleaner

A CLI tool that finds and removes Python cache artifacts (`__pycache__`, `.pyc`, `.pytest_cache`, etc.) from a project tree.

## Features

- Recursively scans a folder for common Python cache directories and bytecode files
- Skips excluded dirs (`.git`, `.venv`, `.idea`, ...) and symlinks to avoid infinite recursion
- `--dry-run` shows what would be removed without touching anything
- `--test` ping check to verify the install works

## Installation

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run pyclean --test
```

Or install as a tool:

```bash
uv tool install .
pyclean --test
```

## Usage

```bash
pyclean [-h] [-f FOLDER] [--test] [--dry-run]
```

| Option | Description |
| ------ | ----------- |
| `-f, --folder` | Folder to scan and clean (required) |
| `--test` | Ping check: prints `pong` if it works |
| `--dry-run` | Print what would be removed, without deleting |

### Examples

```bash
pyclean -f ~/projects/my_app          # scan and delete caches
pyclean -f . --dry-run                # preview only
pyclean --test                        # smoke test -> pong
```

## What it targets

- **Directories**: `__pycache__`, `.pytest_cache`, `.ruff_cache`, `.mypy_cache`, `.black`
- **Files**: `*.pyc`, `*.pyo`, `*.pyd`
- **Excluded from traversal**: `.git`, `.venv`, `venv`, `.zed`, `.vscode`, `.idea`

## Design

The project is split into three modules:

- `scanner.py` — recursive tree walker; returns a `CacheScan` (separate dir/file lists). Prunes excluded dirs and symlinks, so it stays fast on large trees.
- `cleaner.py` — **Strategy pattern**: `Cleaner` is the interface, `DeleteCleaner` and `DryRunCleaner` are swappable implementations. Adding a new behavior (e.g. move-to-trash) means adding one class.
- `__init__.py` — thin CLI glue; picks the cleaner based on `--dry-run`.

```
src/pycache_cleaner/
├── __init__.py   # argparse CLI entry
├── __main__.py   # python -m pycache_cleaner
├── scanner.py    # CacheScanner / CacheScan
└── cleaner.py    # Cleaner strategies
```

## Development

```bash
uv sync           # create venv + install deps
uv run pyclean -f . --dry-run
```
