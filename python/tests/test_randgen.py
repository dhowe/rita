# AUTO-GENERATED from js/test/randgen-tests.js by scripts/js-to-py-tests.js — do not edit by hand.
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

fixtureUrl = next((u for u in [_url(p) for p in ["../../shared/randgen-fixtures.json", "../../../shared/randgen-fixtures.json"]] if existsSync(u)), None)

if not (fixtureUrl):
    raise Exception(Exception(_jsstr("randgen-fixtures.json not found relative to ") + _jsstr(__file__)))

fixtures = json.loads(readFileSync(fixtureUrl), object_hook=JsDict)

R = RiTa.randomizer

class TestRandGen:
    # mocha this.timeout — ignored
    pass
    def test_should_reproduce_the_seeded_sequences(self):
        for __it in fixtures.sequences:
            seed = __it["seed"]
            values = __it["values"]
            R.seed(seed)
            got = [R.random() for _ in values]
            assert (got == values), _jsstr("seed ") + _jsstr(seed)
    def test_should_be_reproducible_across_reseeds(self):
        R.seed(42)
        first = [R.random() for _ in range(10)]
        R.seed(42)
        second = [R.random() for _ in range(10)]
        assert (first == second)
    def test_should_differ_across_seeds(self):
        R.seed(1)
        a = [R.random() for _ in range(10)]
        R.seed(2)
        b = [R.random() for _ in range(10)]
        assert not (a == b)
    def test_should_return_floats_in_0_1(self):
        R.seed(7)
        i = 0
        for i in range(0, 1000, 1):
            v = R.random()
            assert (v >= 0)
            assert (v < 1)
    def test_should_call_pselect(self):
        with pytest.raises(Exception):
            R.pselect()
        R.seed(1)
        assert (R.pselect([1]) == 0)
        assert (fixtures.pselect.expected == replay(fixtures.pselect.seed, lambda *args: R.pselect(fixtures.pselect.probs)))
    def test_should_call_pselectindex(self):
        with pytest.raises(Exception):
            R.pselect_index()
        R.seed(1)
        assert (R.pselect_index([1]) == 0)
        assert (fixtures.pselectIndex.expected == replay(fixtures.pselectIndex.seed, lambda *args: R.pselect_index(fixtures.pselectIndex.probs)))
    def test_should_call_pselect2(self):
        assert (fixtures.pselect2.expected == replay(fixtures.pselect2.seed, lambda *args: R.pselect2(fixtures.pselect2.weights)))
    def test_should_call_pselectobj(self):
        with pytest.raises(Exception):
            R.pselect_obj()
        assert (fixtures.pselectObj.expected == replay(fixtures.pselectObj.seed, lambda *args: R.pselect_obj(fixtures.pselectObj.dist)))
    def test_should_call_ndist(self):
        with pytest.raises(Exception):
            return R.ndist([1, 2, 6, -(2.5), 0])
        assert (R.ndist([1, 2, 6, 0]) == fixtures.ndist.expected)
        assert (R.ndist([1, 2, 3], 0.5) == fixtures.ndistTemp.expected)
        assert (R.ndist([1, 2, 3], 1) == fixtures.ndistTemp1.expected)
        d = R.ndist([3, 7, 11])
        assert (abs(sum(d, start=0) - 1) <= 1e-12)
    def test_should_call_shuffle(self):
        assert (fixtures.shuffle.expected == once(fixtures.shuffle.seed, lambda *args: R.shuffle(fixtures.shuffle.input)))
        out = sorted([*fixtures.shuffle.expected])
        assert (out == fixtures.shuffle.input)
    def test_should_call_randomordering(self):
        assert (R.random_ordering(1) == [0])
        assert (R.random_ordering(["a"]) == ["a"])
        assert (fixtures.randomOrdering.expected == once(fixtures.randomOrdering.seed, lambda *args: R.random_ordering(fixtures.randomOrdering.k)))
        ro = R.random_ordering(5)
        assert (sorted([*ro]) == [0, 1, 2, 3, 4])
        with pytest.raises(Exception):
            R.random_ordering("x")
    def test_should_call_random_with_ranges(self):
        assert (fixtures.random1.expected == replay(fixtures.random1.seed, lambda *args: R.random(fixtures.random1.k)))
        assert (fixtures.random2.expected == replay(fixtures.random2.seed, lambda *args: R.random(fixtures.random2.min, fixtures.random2.max)))
        assert (fixtures.randomArray.expected == once(fixtures.randomArray.seed, lambda *args: R.random(fixtures.randomArray.array)))
    def test_should_call_randombias(self):
        b = fixtures.randomBias
        assert (b.expected == replay(b.seed, lambda *args: R.random_bias(b.min, b.max, b.bias, b.influence)))
    def test_should_honor_rita_randomseed(self):
        RiTa.random_seed(42)
        viaRiTa = [RiTa.random() for _ in range(10)]
        expected = next((s for s in fixtures.sequences if (s.seed) == (42)), None).values
        assert (viaRiTa == expected)
    def test_should_call_randi(self):
        RiTa.random_seed(42)
        assert (RiTa.randi(10) == 3)
        assert (RiTa.randi(5, 15) == 12)

def replay(seed=None, fn=None, *args):
    R.seed(seed)
    return [fn() for _ in range(5)]

def once(seed=None, fn=None, *args):
    R.seed(seed)
    return fn()

def _fn_1(*args):
    R.pselect()

def _fn_2(*args):
    R.pselect_index()

def _fn_3(*args):
    R.pselect_obj()

def _fn_4(*args):
    R.random_ordering("x")

