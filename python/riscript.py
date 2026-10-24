"""
Compatibility shim — the RiScript implementation now lives in ``rita.riscript``.

Kept so that ``import riscript`` keeps working for older scripts and examples.
"""

from rita.riscript import *          # noqa: F401,F403
from rita.riscript import (          # noqa: F401
    RiScript,
    RiGrammar,
    DEFAULT_TRANSFORMS,
)
