# AUTO-GENERATED from js/test/harvard-tests.js by scripts/js-to-py-tests.js — do not edit by hand.
# Mirrors the JS suite 1:1 (describe/it/expect).
import json
import math
import os
import re
import time
import types
import functools
from functools import cmp_to_key
import pytest

_JS_TEST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "js", "test")

from rita import RiTa
from rita.util import JsDict

# --- JS compatibility shims -------------------------------------------
console = type("console", (), {"log": staticmethod(print), "warn": staticmethod(print), "error": staticmethod(print)})
obj = type("obj", (), {"keys": staticmethod(lambda d: list(d.keys())), "values": staticmethod(lambda d: list(d.values()))})
arr = type("arr", (), {"isArray": staticmethod(lambda x: isinstance(x, list)), "from": staticmethod(_arr_from)}) if False else None
def _arr_from(x, fn=None):
    if isinstance(x, dict) and "length" in x:
        return [fn() if fn else None for _ in range(x["length"])]
    return list(x)
arr = type("arr", (), {"isArray": staticmethod(lambda x: isinstance(x, list)), "from": staticmethod(_arr_from)})
def _typeof(fn):
    try: x = fn()
    except NameError: return "undefined"
    except AttributeError: return "undefined"
    if x is None: return "undefined"
    if isinstance(x, bool): return "boolean"
    if isinstance(x, str): return "string"
    if isinstance(x, (int, float)): return "number"
    if callable(x): return "function"
    return "object"
def _indexof(a, x):
    try: return a.index(x)
    except ValueError: return -1
def _re_compile(p):
    return re.compile(p)
def readFileSync(p):
    return open(p).read()
def existsSync(p):
    return os.path.exists(p)
def _is_integer(x):
    return isinstance(x, int) and not isinstance(x, bool)
def _is_finite(x):
    return isinstance(x, (int, float)) and x == x and x not in (float("inf"), float("-inf"))
def _is_nan(x):
    return isinstance(x, float) and x != x
def _url(rel):
    if rel.startswith("./"):
        rel = rel[2:]
    return os.path.normpath(os.path.join(_JS_TEST_DIR, rel))
def expect(*a, **k):
    return a[0]
def _jsstr(x):
    # JS String(x): arrays coerce to comma-joined, others to str().
    if isinstance(x, list):
        return ",".join(_jsstr(e) for e in x)
    if x is None:
        return "None"
    if x is True:
        return "true"
    if x is False:
        return "false"
    return str(x)
def _hasprop(x, k):
    # JS expect(obj).to.have.property(k): key membership for dicts, attr for objects.
    if isinstance(x, dict):
        return k in x
    return hasattr(x, k)

data = json.loads(readFileSync(_url("./harvard-data.json")), object_hook=JsDict)

sentences = [d[0] for d in data]

class TestHarvard:
    def test_should_tokenize_and_untokenize_all_sentences_without_loss(self):
        mismatches = 0
        for s in sentences:
            result = RiTa.untokenize(RiTa.tokenize(s))
            if (result) != (s):
                console.warn(f"  MISMATCH:\n    expected: {s}\n    got:      {result}")
                mismatches += 1
        assert (mismatches == 0), f"{mismatches} tokenize/untokenize mismatches"
    def test_should_assign_correct_pos_tags_to_all_sentences(self):
        mismatches = 0
        i = 0
        for i in range(0, len(sentences), 1):
            s = sentences[i]
            _, expectedToks, expectedTags = data[i]
            actualToks = RiTa.tokenize(s)
            actualTags = RiTa.pos(actualToks)
            assert (actualToks == expectedToks), f"sentence {(i) + (1)} tokens"
            if (json.dumps(actualTags)) != (json.dumps(expectedTags)):
                console.warn(f"  TAG MISMATCH [{(i) + (1)}]: {s}")
                console.warn(f"    expected: {json.dumps(expectedTags)}")
                console.warn(f"    got:      {json.dumps(actualTags)}")
                mismatches += 1
        assert (mismatches == 0), f"{mismatches} POS tag mismatches"
    def test_should_produce_correct_phonemes_for_all_sentences(self):
        mismatches = 0
        skipped = 0
        RiTa.SILENCE_LTS = True
        i = 0
        for i in range(0, len(sentences), 1):
            sentence, _, _, expectedIpa = data[i]
            s = sentence.replace(_re_compile("[.!?,]+$"), "", 1)
            actualIpa = _jsstr(_jsstr("/") + _jsstr(syllablesToIpa(RiTa.syllables(s), RiTa.stresses(s)))) + _jsstr("/")
            if (actualIpa) != (expectedIpa):
                console.warn(f"  PHONE MISMATCH [{(i) + (1)}]: {sentence}")
                console.warn(f"    expected: {expectedIpa}")
                console.warn(f"    got:      {actualIpa}")
                mismatches += 1
        assert (mismatches == 0), f"{mismatches} phoneme mismatches"
        RiTa.SILENCE_LTS = False

