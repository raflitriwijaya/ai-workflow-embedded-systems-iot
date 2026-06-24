"""Pytest bootstrap: make the ``eval_harness`` package importable regardless of
the directory pytest is invoked from."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
