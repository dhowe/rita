# AUTO-GENERATED from js/test/grammar-tests.js by scripts/js-to-py-tests.js — do not edit by hand.
# Mirrors the JS suite 1:1 (describe/it/expect).
import json
import math
import os
import re
import types
import functools
from functools import cmp_to_key
import pytest

_JS_TEST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "js", "test")

from rita import RiTa

# --- JS compatibility shims -------------------------------------------
console = type("console", (), {"log": staticmethod(print), "warn": staticmethod(print), "error": staticmethod(print)})
obj = type("obj", (), {"keys": staticmethod(lambda d: list(d.keys())), "values": staticmethod(lambda d: list(d.values()))})
arr = type("arr", (), {"isArray": staticmethod(lambda x: isinstance(x, list)), "from": staticmethod(_arr_from)}) if False else None
def _arr_from(x, fn=None):
    if isinstance(x, dict) and "length" in x:
        return [fn() if fn else None for _ in range(x["length"])]
    return list(x)
arr = type("arr", (), {"isArray": staticmethod(lambda x: isinstance(x, list)), "from": staticmethod(_arr_from)})
def __typeof(x):
    if x is None: return "undefined"
    if isinstance(x, bool): return "boolean"
    if isinstance(x, str): return "string"
    if isinstance(x, (int, float)): return "number"
    if callable(x): return "function"
    return "object"
def __indexof(a, x):
    try: return a.index(x)
    except ValueError: return -1
def __re_compile(p):
    return re.compile(p)
def readFileSync(p):
    return open(p).read()
def existsSync(p):
    return os.path.exists(p)
def __is_integer(x):
    return isinstance(x, int) and not isinstance(x, bool)
def __is_finite(x):
    return isinstance(x, (int, float)) and x == x and x not in (float("inf"), float("-inf"))
def __is_nan(x):
    return isinstance(x, float) and x != x
def __url(rel):
    if rel.startswith("./"):
        rel = rel[2:]
    return os.path.normpath(os.path.join(_JS_TEST_DIR, rel))
def expect(*a, **k):
    return a[0]

def __fn_1(_):
    console.log("chooseChar:", __typeof(self))
    return "OK"

class TestGrammar:
    T = {"trace": 1}
    def test_should_call_rita_grammar_for_a_blank_grammar(self):
        rg = RiTa.grammar()
        assert (isinstance(rg, RiTa.RiGrammar))
    def test_should_call_rigrammar_fromjson_rules(self):
        rules = {"start": "Meet $person.name. $person.pronoun.cap() drives $person.car.art().", "#person": "$sam | $lucy"}
        rg = RiTa.RiGrammar.fromJSON(json.dumps(rules))
        assert (isinstance(rg, RiTa.RiGrammar))
    def test_should_allow_constructions_from_object_or_string(self):
        rules = {"start": "Meet $person.name. $person.pronoun.cap() drives $person.car.art().", "#person": "$sam | $lucy"}
        rg1 = RiTa.grammar(rules)
        rg2 = RiTa.grammar(json.dumps(rules))
        rg3 = RiTa.RiGrammar.fromJSON(json.dumps(rules))
        assert (rg1.toJSON() == rg2.toJSON())
        assert (rg1.toJSON() == rg3.toJSON())
    def test_should_call_rita_grammar_expand(self):
        context = {"lucy": {"name": "Lucy", "pronoun": "she", "car": "Acura"}, "sam": {"name": "Sam", "pronoun": "he", "car": "Subaru"}}
        rules = {"start": "Meet $person.name. $person.pronoun.cap() drives $person.car.art().", "#person": "$sam | $lucy"}
        result = RiTa.grammar(rules, context).expand()
        assert (result in ["Meet Lucy. She drives an Acura.", "Meet Sam. He drives a Subaru."])
    @pytest.mark.skip(reason="disabled in JS")  # /*LTR*/
    def test_should_reference_context_from_transforms(self):
        context = {"characters": [{"name": "Lucy", "pronoun": "she", "car": "Acura"}, {"name": "Sam", "pronoun": "he", "car": "Subaru"}], "chooseChar": __fn_1}
        rules = {"start": "$person=$chooseChar() $sentence", "sentence": "$Meet $person.name. $person.pronoun.cap() drives $person.car.art().", "#person": "$sam | $lucy"}
        result = RiTa.grammar(rules, context).expand()
        assert (result in ["Meet Lucy. She drives an Acura.", "Meet Sam. He drives a Subaru."])

