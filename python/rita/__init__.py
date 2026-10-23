"""
rita — Python port of RiTa (https://rednoise.org/rita)

Public API re-exports. Additional modules (Tagger, Lexicon, etc.) will be
added as each phase of the port is completed.
"""

from rita.util import Util, RE
from rita.randgen import RandGen
from rita.rita_lts import LetterToSound
from rita.stemmer import Stemmer
from rita.tagger import Tagger
from rita.analyzer import Analyzer
from rita.lexicon import Lexicon
from rita.markov import RiMarkov
from rita.concorder import Concorder
from rita.rita import RiTa

# RiScript / RiGrammar (already fully ported)
import sys
import os

# riscript.py lives at project root, not inside the rita/ package
_root = os.path.dirname(os.path.dirname(__file__))
if _root not in sys.path:
    sys.path.insert(0, _root)

from riscript import RiScript, RiGrammar  # noqa: E402

__all__ = [
    "RiScript",
    "RiGrammar",
    "RandGen",
    "Util",
    "RE",
    "LetterToSound",
    "Stemmer",
    "Tagger",
    "Analyzer",
    "Lexicon",
    "RiMarkov",
    "Concorder",
    "RiTa",
]
