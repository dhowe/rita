# AUTO-GENERATED from js/test/grammar-tests.js by scripts/js-to-py-tests.js — do not edit by hand.
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

class TestGrammar:
    # (var hoisted to module scope)
    def test_should_call_rita_grammar_for_a_blank_grammar(self):
        rg = RiTa.grammar()
        assert (isinstance(rg, RiTa.RiGrammar))
    def test_should_call_rigrammar_fromjson_rules(self):
        rules = JsDict({"start": "Meet $person.name. $person.pronoun.cap() drives $person.car.art().", "#person": "$sam | $lucy"})
        rg = RiTa.RiGrammar.from_json(json.dumps(rules))
        assert (isinstance(rg, RiTa.RiGrammar))
    def test_should_allow_constructions_from_object_or_string(self):
        rules = JsDict({"start": "Meet $person.name. $person.pronoun.cap() drives $person.car.art().", "#person": "$sam | $lucy"})
        rg1 = RiTa.grammar(rules)
        rg2 = RiTa.grammar(json.dumps(rules))
        rg3 = RiTa.RiGrammar.from_json(json.dumps(rules))
        assert (rg1.to_json() == rg2.to_json())
        assert (rg1.to_json() == rg3.to_json())
    def test_should_call_rita_grammar_expand(self):
        context = JsDict({"lucy": {"name": "Lucy", "pronoun": "she", "car": "Acura"}, "sam": {"name": "Sam", "pronoun": "he", "car": "Subaru"}})
        rules = JsDict({"start": "Meet $person.name. $person.pronoun.cap() drives $person.car.art().", "#person": "$sam | $lucy"})
        result = RiTa.grammar(rules, context).expand()
        assert (result in ["Meet Lucy. She drives an Acura.", "Meet Sam. He drives a Subaru."])
    @pytest.mark.skip(reason="disabled in JS")  # /*LTR*/
    def test_should_reference_context_from_transforms(self):
        context = JsDict({"characters": [{"name": "Lucy", "pronoun": "she", "car": "Acura"}, {"name": "Sam", "pronoun": "he", "car": "Subaru"}], "chooseChar": _fn_1})
        rules = JsDict({"start": "$person=$chooseChar() $sentence", "sentence": "$Meet $person.name. $person.pronoun.cap() drives $person.car.art().", "#person": "$sam | $lucy"})
        result = RiTa.grammar(rules, context).expand()
        assert (result in ["Meet Lucy. She drives an Acura.", "Meet Sam. He drives a Subaru."])

T = JsDict({"trace": 1})

def _fn_1(*args):
    console.log("chooseChar:", _typeof(lambda: self))
    return "OK"

