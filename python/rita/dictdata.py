"""
rita/data.py — locate the canonical RiTa dictionary.

The dictionary lives in ``shared/rita_dict.json`` in the mono-repo, but that
directory is not part of an installed wheel, so ``scripts/gen-dicts.js`` also
copies it into ``rita/data/`` as package data.  This module resolves the path
in that order:

1. the mono-repo ``shared/rita_dict.json`` — used in a source checkout, so the
   package tracks the canonical file without a rebuild;
2. bundled package data (``rita/data/rita_dict.json``) — what an installed
   wheel/sdist actually contains.

The first existing candidate wins, so a checkout and an install both work.
"""

import json
import os

# candidate paths, most authoritative first
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.normpath(os.path.join(_HERE, '..', '..', 'shared', 'rita_dict.json'))
_DATA = os.path.join(_HERE, 'data', 'rita_dict.json')

_CANDIDATES = [_REPO, _DATA]


def dict_path():
    """Absolute path to the canonical rita_dict.json, or None if not found."""
    for p in _CANDIDATES:
        if os.path.exists(p):
            return p
    return None


def load_dict():
    """Load and parse the canonical dictionary."""
    p = dict_path()
    if p is None:
        raise FileNotFoundError(
            'rita_dict.json not found; expected it at %s or %s' % (_DATA, _REPO))
    with open(p, encoding='utf-8') as f:
        return json.load(f)
