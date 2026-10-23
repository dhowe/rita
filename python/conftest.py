# Ensures the python/ directory is importable so `from rita import RiTa` resolves
# to python/rita/ once the port exists. Tests are auto-generated from js/test/ by
# scripts/js-to-py-tests.js — regenerate rather than editing test_*.py by hand.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
