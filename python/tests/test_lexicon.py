# AUTO-GENERATED from js/test/lexicon-tests.js by scripts/js-to-py-tests.js — do not edit by hand.
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

class TestLexicon:
    # mocha this.slow — ignored
    pass
    # mocha this.timeout — ignored
    pass
    def test_should_call_hasword(self):
        i = 0
        for i in range(0, 10, 1):
            assert ((RiTa.has_word(RiTa.random_word())) is True)
        assert ((RiTa.has_word("random")) is True)
        assert ((RiTa.has_word("dog")) is True)
        assert ((RiTa.has_word("men")) is True)
        assert ((RiTa.has_word("happily")) is True)
        assert ((RiTa.has_word("play")) is True)
        assert ((RiTa.has_word("plays")) is True)
        assert ((RiTa.has_word("played")) is True)
        assert ((RiTa.has_word("written")) is True)
        assert ((RiTa.has_word("dogs")) is True)
        assert ((RiTa.has_word("oxen")) is True)
        assert ((RiTa.has_word("mice")) is True)
        assert ((RiTa.has_word("dogs", JsDict({"noDerivations": True}))) is False)
        assert ((RiTa.has_word("played", JsDict({"noDerivations": True}))) is False)
        assert ((RiTa.has_word("cats", JsDict({"noDerivations": True}))) is False)
        assert ((RiTa.has_word("bunning")) is False)
        assert ((RiTa.has_word("coyes")) is False)
        assert ((RiTa.has_word("soes")) is False)
        assert ((RiTa.has_word("knews")) is False)
        assert ((RiTa.has_word("fastering")) is False)
        assert ((RiTa.has_word("loosering")) is False)
        assert ((RiTa.has_word("knews")) is False)
        assert ((RiTa.has_word("barkness")) is False)
        assert ((RiTa.has_word("horne")) is False)
        assert ((RiTa.has_word("haye")) is False)
        assert ((RiTa.has_word("bites")) is True)
        assert ((RiTa.has_word("bit")) is True)
        assert ((RiTa.has_word("bitted")) is False)
        assert ((RiTa.has_word("breaks")) is True)
        assert ((RiTa.has_word("broke")) is True)
        assert ((RiTa.has_word("brokes")) is False)
        assert ((RiTa.has_word("broked")) is False)
        assert ((RiTa.has_word("concerned")) is True)
        assert ((RiTa.has_word("concerneded")) is False)
        assert ((RiTa.has_word("concerneds")) is False)
        assert ((RiTa.has_word("outpaced")) is True)
        assert ((RiTa.has_word("outpaceded")) is False)
        assert ((RiTa.has_word("outpaceds")) is False)
        assert ((RiTa.has_word("reported")) is True)
        assert ((RiTa.has_word("reporteds")) is False)
        assert ((RiTa.has_word("reporteded")) is False)
        assert ((RiTa.has_word("build")) is True)
        assert ((RiTa.has_word("built")) is True)
        assert ((RiTa.has_word("called")) is True)
        assert ((RiTa.has_word("calleds")) is False)
        assert ((RiTa.has_word("calleded")) is False)
        assert ((RiTa.has_word("commits")) is True)
        assert ((RiTa.has_word("committed")) is True)
        assert ((RiTa.has_word("committeds")) is False)
        assert ((RiTa.has_word("committeded")) is False)
        assert ((RiTa.has_word("computerized")) is True)
        assert ((RiTa.has_word("computerizeds")) is False)
        assert ((RiTa.has_word("computerizeded")) is False)
        assert ((RiTa.has_word("gets")) is True)
        assert ((RiTa.has_word("got")) is True)
        assert ((RiTa.has_word("gots")) is False)
        assert ((RiTa.has_word("gotten")) is True)
        assert ((RiTa.has_word("leads")) is True)
        assert ((RiTa.has_word("led")) is True)
        assert ((RiTa.has_word("leds")) is False)
        assert ((RiTa.has_word("oversaw")) is True)
        assert ((RiTa.has_word("overseen")) is True)
        assert ((RiTa.has_word("oversaws")) is False)
        assert ((RiTa.has_word("overseened")) is False)
        assert ((RiTa.has_word("remakes")) is True)
        assert ((RiTa.has_word("remade")) is True)
        assert ((RiTa.has_word("remaded")) is False)
        assert ((RiTa.has_word("discriminates")) is True)
        assert ((RiTa.has_word("discriminated")) is True)
        assert ((RiTa.has_word("discriminateds")) is False)
        assert ((RiTa.has_word("launched")) is True)
        assert ((RiTa.has_word("launcheds")) is False)
        assert ((RiTa.has_word("launcheded")) is False)
        assert ((RiTa.has_word("starts")) is True)
        assert ((RiTa.has_word("started")) is True)
        assert ((RiTa.has_word("starteds")) is False)
    def test_should_call_randomword(self):
        result = None
        result = RiTa.random_word()
        assert (((len(result)) > (0)) is True), _jsstr("randomWord: ") + _jsstr(result)
        assert (((result) == (RiTa.random_word())) is False), _jsstr(_jsstr("randomWord returned same result '") + _jsstr(result)) + _jsstr("'")
        result = RiTa.random_word(JsDict({"numSyllables": 3}))
        assert (((len(result)) > (0)) is True), _jsstr("3 syllables: ") + _jsstr(result)
        result = RiTa.random_word(JsDict({"numSyllables": 5}))
        assert (((len(result)) > (0)) is True), _jsstr("5 syllables: ") + _jsstr(result)
    def test_should_not_mutate_the_caller_options_object(self):
        opts = JsDict(JsDict({"numSyllables": 2}))
        RiTa.random_word(opts)
        assert ((opts in "limit") is False), "randomWord leaked limit"
        assert ((opts in "shuffle") is False), "randomWord leaked shuffle"
        opts = JsDict({"pos": "nn"})
        RiTa.search_sync(_re_compile("^a"), opts)
        assert ((opts in "targetPos") is False), "search leaked targetPos"
        assert ((opts in "minDistance") is False), "search leaked minDistance"
        opts = JsDict({"limit": 5})
        RiTa.rhymes_sync("cat", opts)
        assert ((opts in "maxLength") is False), "rhymes leaked maxLength"
    def test_should_call_randomword_with_regex(self):
        result = RiTa.random_word("^a")
        assert ((_re_compile("^a").search(result) is not None) is True)
        assert (((len(result)) > (3)) is True)
        result = RiTa.random_word("^apple$")
        assert (result == "apple")
        result = RiTa.random_word("le")
        assert (("le" in result) is True)
        results = []
        i = 0
        for i in range(0, 10, 1):
            results.append(RiTa.random_word("^a"))
        assert (((len(results)) == (10)) is True)
        i = 0
        while (i) < ((len(results)) - (1)):
            if (results[i]) == (results[(i) + (1)]):
                results.splice(i, 1)
            else:
                i += 1
        assert (((len(results)) > (1)) is True)
        result = RiTa.random_word(_re_compile("^a"))
        assert ((_re_compile("^a").search(result) is not None) is True)
        assert (((len(result)) > (3)) is True)
        result = RiTa.random_word(_re_compile("^apple$"))
        assert (result == "apple")
        result = RiTa.random_word(_re_compile("le"))
        assert (("le" in result) is True)
        result = RiTa.random_word("^a")
        assert ((result.startswith(_jsstr("a"))) is True)
        results = []
        i = 0
        for i in range(0, 10, 1):
            results.append(RiTa.random_word(_re_compile("^a")))
        assert (((len(results)) == (10)) is True)
    def test_should_call_randomword_with_stress_regex(self):
        result = RiTa.random_word("0/1/0", JsDict({"type": "stresses"}))
        assert ((len(result)) > (3))
        assert ("0/1/0" in RiTa.analyze(result).stresses)
        result = RiTa.random_word("^0/1/0$", JsDict({"type": "stresses"}))
        assert (RiTa.analyze(result).stresses == "0/1/0")
        result = RiTa.random_word("010", JsDict({"type": "stresses"}))
        assert (("0/1/0" in RiTa.analyze(result).stresses) is True)
        result = RiTa.random_word("^010$", JsDict({"type": "stresses"}))
        assert (RiTa.analyze(result).stresses == "0/1/0")
        result = RiTa.random_word(_re_compile("0\\/1\\/0"), JsDict({"type": "stresses"}))
        assert (("0/1/0" in RiTa.analyze(result).stresses) is True)
        result = RiTa.random_word(_re_compile("^0\\/1\\/0\\/0$"), JsDict({"type": "stresses"}))
        assert (RiTa.analyze(result).stresses == "0/1/0/0")
    def test_should_call_randomword_with_phones_regex(self):
        result = RiTa.random_word("^th", JsDict({"type": "phones"}))
        assert ((len(result)) > (3))
        assert ((_re_compile("^th").search(RiTa.analyze(result).phones) is not None) is True)
        result = RiTa.random_word("v$", JsDict({"type": "phones"}))
        assert ((_re_compile("v$").search(RiTa.analyze(result).phones) is not None) is True)
        result = RiTa.random_word("^b-ih-l-iy-v$", JsDict({"type": "phones"}))
        assert (result == "believe")
        result = RiTa.random_word("ae", JsDict({"type": "phones"}))
        assert (("ae" in RiTa.analyze(result).phones) is True)
        result = RiTa.random_word(_re_compile("^th"), JsDict({"type": "phones"}))
        assert ((len(result)) > (3))
        assert ((_re_compile("^th").search(RiTa.analyze(result).phones) is not None) is True)
        result = RiTa.random_word(_re_compile("v$"), JsDict({"type": "phones"}))
        assert ((_re_compile("v$").search(RiTa.analyze(result).phones) is not None) is True)
        result = RiTa.random_word(_re_compile("^b-ih-l-iy-v$"), JsDict({"type": "phones"}))
        assert (result == "believe")
        result = RiTa.random_word(_re_compile("ae"), JsDict({"type": "phones"}))
        assert (("ae" in RiTa.analyze(result).phones) is True)
    def test_should_call_randomword_with_opts_regex(self):
        result = RiTa.random_word(JsDict({"regex": "^a"}))
        assert ((_re_compile("^a").search(result) is not None) is True)
        assert (((len(result)) > (3)) is True)
        result = RiTa.random_word(JsDict({"regex": _re_compile("^a")}))
        assert ((_re_compile("^a").search(result) is not None) is True)
        assert (((len(result)) > (3)) is True)
        result = RiTa.random_word(JsDict({"regex": "0/1/0", "type": "stresses"}))
        assert ((len(result)) > (3))
        assert (("0/1/0" in RiTa.analyze(result).stresses) is True)
        result = RiTa.random_word(JsDict({"regex": _re_compile("0\\/1\\/0"), "type": "stresses"}))
        assert (("0/1/0" in RiTa.analyze(result).stresses) is True)
        result = RiTa.random_word(JsDict({"regex": "^th", "type": "phones"}))
        assert ((len(result)) > (3))
        assert ((_re_compile("^th").search(RiTa.analyze(result).phones) is not None) is True)
        result = RiTa.random_word(JsDict({"regex": _re_compile("^th"), "type": "phones"}))
        assert ((len(result)) > (3))
        assert ((_re_compile("^th").search(RiTa.analyze(result).phones) is not None) is True)
    def test_should_handle_an_augmented_lexicon(self):
        toAdd = JsDict(JsDict({"deg": ["d-eh1-g", "nn"], "wadly": ["w-ae1-d l-iy", "rb"]}))
        lex = RiTa.lexicon
        for w in list(toAdd.keys()):
            RiTa.lexicon.data[w] = toAdd[w]
        assert (lex.has_word("run"))
        assert (lex.has_word("walk"))
        assert (lex.has_word("deg"))
        assert (lex.has_word("wadly"))
        assert (lex.is_alliteration("wadly", "welcome"))
        for w in list(toAdd.keys()):
            RiTa.lexicon.data[w]
    def test_should_handle_a_custom_lexicon(self):
        lex = RiTa.lexicon
        orig = lex.data
        lex.data = JsDict({"dog": ["d-ao1-g", "nn"], "cat": ["k-ae1-t", "nn"], "happily": ["hh-ae1 p-ah l-iy", "rb"], "walk": ["w-ao1-k", "vb vbp nn"], "welcome": ["w-eh1-l k-ah-m", "jj nn vb vbp"], "sadly": ["s-ae1-d l-iy", "rb"]})
        assert ((lex.has_word("run")) is False)
        assert ((lex.has_word("walk")) is True)
        assert ((lex.is_alliteration("walk", "welcome")) is True)
        lex.data = orig
    def test_should_call_randomword_with_pos(self):
        with pytest.raises(Exception):
            return RiTa.random_word(JsDict({"pos": "xxx"}))
        result = None
        pos = ["nn", "jj", "jjr", "wp"]
        j = 0
        for j in range(0, len(pos), 1):
            result = RiTa.random_word(JsDict({"pos": pos[j]}))
            best = RiTa.tagger.all_tags(result)[0]
            assert (pos[j] == best)
        i = 0
        for i in range(0, 5, 1):
            result = RiTa.random_word(JsDict({"pos": "nns"}))
            if not (RiTa.inflector.is_plural(result)):
                console.warn(_jsstr(_jsstr(_jsstr(_jsstr(_jsstr(_jsstr(_jsstr("Pluralize/Singularize problem: randomWord(nns) was '") + _jsstr(result)) + _jsstr("' (")) + _jsstr("isPlural=")) + _jsstr(RiTa.inflector.is_plural(result))) + _jsstr("), singularized is '")) + _jsstr(RiTa.singularize(result))) + _jsstr("'"))
            pos = RiTa.lexicon._pos_data(result)
            assert (((not (pos)) or ((_indexof(pos, "vbg")) < (0))) is True), _jsstr("randomWord nns: ") + _jsstr(result)
            assert ((not (result.endswith(_jsstr("ness")))) is True), _jsstr("randomWord nns: ") + _jsstr(result)
            assert ((not (result.endswith(_jsstr("isms")))) is True), _jsstr("randomWord nns: ") + _jsstr(result)
        result = RiTa.random_word(JsDict({"pos": "v"}))
        assert (((len(result)) > (0)) is True), _jsstr("randomWord v=") + _jsstr(result)
        result = RiTa.random_word(JsDict({"pos": "nn"}))
        assert (((len(result)) > (0)) is True), _jsstr("randomWord nn: ") + _jsstr(result)
        result = RiTa.random_word(JsDict({"pos": "nns"}))
        assert (((len(result)) > (0)) is True), _jsstr("randomWord nns=") + _jsstr(result)
        result = RiTa.random_word(JsDict({"pos": "n"}))
        assert (((len(result)) > (0)) is True), _jsstr("randomWord n=") + _jsstr(result)
        result = RiTa.random_word(JsDict({"pos": "v"}))
        assert (((len(result)) > (0)) is True), _jsstr("randomWord v=") + _jsstr(result)
        result = RiTa.random_word(JsDict({"pos": "rp"}))
        assert (((len(result)) > (0)) is True), _jsstr("randomWord rp=") + _jsstr(result)
        results = []
        i = 0
        for i in range(0, 10, 1):
            results.append(RiTa.random_word(JsDict({"pos": "nns"})))
            assert (((_typeof(lambda: results[(len(results)) - (1)])) == ("string")) is True)
        assert (((len(results)) == (10)) is True)
        i = 0
        while (i) < ((len(results)) - (1)):
            if (results[i]) == (results[(i) + (1)]):
                results.splice(i, 1)
            else:
                i += 1
        assert (((len(results)) > (1)) is True)
    def test_should_call_randomword_with_syllables(self):
        i = None
        result = None
        syllables = None
        num = None
        result = RiTa.random_word(JsDict({"numSyllables": 3}))
        syllables = RiTa.syllables(result)
        num = len(syllables.split(RiTa.SYLLABLE_BOUNDARY))
        assert (((len(result)) > (0)) is True), _jsstr("failed1 on: ") + _jsstr(result)
        assert (((num) == (3)) is True), _jsstr(_jsstr(result) + _jsstr(": ")) + _jsstr(syllables)
        result = RiTa.random_word(JsDict({"numSyllables": 5}))
        syllables = RiTa.syllables(result)
        num = len(syllables.split(RiTa.SYLLABLE_BOUNDARY))
        assert (len(result) > 0)
        assert (((num) == (5)) is True), _jsstr(_jsstr(result) + _jsstr(": ")) + _jsstr(syllables)
    def test_should_call_search_without_regex(self):
        assert (len(RiTa.search()) > 20000)
        assert (len(RiTa.search(JsDict({"limit": 11}))) == 11)
        assert (RiTa.search(JsDict({"pos": "n"})) == ["abalone", "abandonment", "abbey", "abbot", "abbreviation", "abdomen", "abduction", "aberration", "ability", "abnormality"])
        res = RiTa.search(JsDict({"numSyllables": 2}))
        assert (res == ["abashed", "abate", "abbey", "abbot", "abduct", "abet", "abhor", "abide", "abject", "ablaze"])
        assert (RiTa.search(JsDict({"numSyllables": 2, "pos": "n"})) == ["abbey", "abbot", "abode", "abscess", "absence", "abstract", "abuse", "abyss", "accent", "access"])
        assert (RiTa.search(JsDict({"numSyllables": 1, "pos": "n"})) == ["ace", "ache", "act", "age", "aid", "aide", "aim", "air", "aisle", "ale"])
        search = RiTa.search(JsDict({"pos": "vb", "limit": -(1)}))
        assert (("concerned" in search) is False)
        assert (("committed" in search) is False)
        assert (("called" in search) is False)
        assert (("computerized" in search) is False)
        search = RiTa.search(JsDict({"pos": "vbd", "limit": -(1)}))
        assert (("concerned" in search) is True)
        assert (("committed" in search) is True)
        assert (("called" in search) is True)
        assert (("computerized" in search) is True)
        (0) and (expect("conclude" in search).to.be.true)
        search = RiTa.search(JsDict({"pos": "vbn", "limit": -(1)}))
        assert (("concerned" in search) is True)
        assert (("committed" in search) is True)
        assert (("called" in search) is True)
        assert (("computerized" in search) is True)
        (0) and (expect("conclude" in search).to.be.true)
    def test_should_call_search_with_letters(self):
        assert (RiTa.search("phant") == ["elephant", "elephantine", "phantom", "sycophantic", "triumphant", "triumphantly"])
        assert (RiTa.search(_re_compile("phant")) == ["elephant", "elephantine", "phantom", "sycophantic", "triumphant", "triumphantly"])
        assert (RiTa.search(JsDict({"regex": "phant"})) == ["elephant", "elephantine", "phantom", "sycophantic", "triumphant", "triumphantly"])
        assert (RiTa.search(JsDict({"regex": _re_compile("phant")})) == ["elephant", "elephantine", "phantom", "sycophantic", "triumphant", "triumphantly"])
    def test_should_call_search_with_phones_limit(self):
        result = RiTa.search(_re_compile("f-a[eh]-n-t"), JsDict({"type": "phones", "limit": 10}))
        assert (result == ["elephant", "elephantine", "fantasia", "fantasize", "fantastic", "fantastically", "fantasy", "infant", "infantile", "infantry"])
        result = RiTa.search("f-ah-n-t", JsDict({"type": "phones", "limit": 5}))
        assert (result == ["elephant", "infant", "infantile", "infantry", "oftentimes"])
        result = RiTa.search(JsDict({"regex": _re_compile("f-a[eh]-n-t"), "type": "phones", "limit": 10}))
        assert (result == ["elephant", "elephantine", "fantasia", "fantasize", "fantastic", "fantastically", "fantasy", "infant", "infantile", "infantry"])
    def test_should_call_search_with_phones_no_limit_and_shuffle(self):
        result = RiTa.search(JsDict({"regex": "f-ah-n-t", "type": "phones", "limit": -(1)}))
        assert (result == ["elephant", "infant", "infantile", "infantry", "oftentimes", "triumphant", "triumphantly"])
        result2 = RiTa.search(JsDict({"regex": "f-ah-n-t", "type": "phones", "limit": -(1), "shuffle": True}))
        assert (sorted(result2) == result)
    def test_should_call_search_with_pos_phones_sylls_limit(self):
        res = RiTa.search("f-ah-n-t", JsDict({"type": "phones", "pos": "n", "limit": 3, "numSyllables": 2}))
        assert (res == ["infant"])
    def test_should_call_search_with_pos_phones_limit(self):
        res = RiTa.search("f-ah-n-t", JsDict({"type": "phones", "pos": "n", "limit": 3}))
        assert (res == ["elephant", "infant", "infantry"])
        res = RiTa.search(_re_compile("f-a[eh]-n-t"), JsDict({"type": "phones", "pos": "v", "limit": 5}))
        assert (res == ["fantasize"])
    def test_should_call_search_with_pos_regex(self):
        res = RiTa.search(_re_compile("cares$"), JsDict({"pos": "nns", "limit": -(1)}))
        assert (res == ["cares", "scares"])
        res = RiTa.search(_re_compile("^rice$"), JsDict({"pos": "nns", "limit": -(1)}))
        assert (res == ["rice"])
    def test_should_call_search_with_pos_letters(self):
        res = RiTa.search("cause", JsDict({"pos": "nns"}))
        assert (res == ["causes", "causeways"])
        res = RiTa.search("gain", JsDict({"pos": "vbd", "numSyllables": 1}))
        assert (res == ["gained"])
        res = RiTa.search("end", JsDict({"pos": "vbd", "minLength": 2, "limit": -(1)}))
        assert (("ended" in res) is True)
        res = RiTa.search("commit", JsDict({"pos": "vbd"}))
        assert (("committed" in res) is True)
        res = RiTa.search("involve", JsDict({"pos": "vbd"}))
        assert (("involved" in res) is True)
        res = RiTa.search("outpace", JsDict({"pos": "vbn"}))
        assert (res == ["outpaced"])
        res = RiTa.search("paid", JsDict({"pos": "vbd"}))
        assert (("prepaid" in res) is True)
        res = RiTa.search("made", JsDict({"pos": "vbd"}))
        assert (("remade" in res) is True)
        res = RiTa.search("re", JsDict({"pos": "vbd", "limit": -(1)}))
        assert (("reopened" in res) is True)
        assert (("resold" in res) is True)
    def test_should_call_search_with_simple_pos_phones_limit(self):
        assert (RiTa.search(_re_compile("f-a[eh]-n-t"), JsDict({"type": "phones", "pos": "vb", "limit": 5})) == ["fantasize"])
        assert (RiTa.search("f-ah-n-t", JsDict({"type": "phones", "pos": "nns", "limit": 3})) == ["elephants", "infants", "infantries"])
    def test_should_call_search_with_pos_stress_limit(self):
        assert (RiTa.search("010", JsDict({"type": "stresses", "limit": 5, "pos": "n"})) == ["abalone", "abandonment", "abbreviation", "abdomen", "abduction"])
        assert (RiTa.search("010", JsDict({"type": "stresses", "limit": 5, "pos": "n", "numSyllables": 3})) == ["abdomen", "abduction", "abortion", "abruptness", "absorber"])
        assert (RiTa.search("010", JsDict({"type": "stresses", "limit": 5, "pos": "nns"})) == ["abalone", "abandonments", "abbreviations", "abductions", "abilities"])
        assert (RiTa.search(_re_compile("0\\/1\\/0"), JsDict({"type": "stresses", "limit": 5, "pos": "nns"})) == ["abalone", "abandonments", "abbreviations", "abductions", "abilities"])
        assert (RiTa.search("010", JsDict({"type": "stresses", "limit": 5, "pos": "nns", "numSyllables": 3})) == ["abductions", "abortions", "absorbers", "abstentions", "abstractions"])
    def test_should_call_search_with_stresses_limit(self):
        assert (RiTa.search("010000", JsDict({"type": "stresses", "limit": 5})) == ["accountability", "anticipatory", "appreciatively", "authoritarianism", "colonialism"])
        assert (RiTa.search("010000", JsDict({"type": "stresses", "limit": 5, "maxLength": 11})) == ["colonialism", "imperialism", "materialism"])
        assert (RiTa.search("010000", JsDict({"type": "stresses", "limit": 5, "minLength": 12})) == ["accountability", "anticipatory", "appreciatively", "authoritarianism", "conciliatory"])
        assert (RiTa.search("0/1/0/0/0/0", JsDict({"type": "stresses", "limit": 5})) == ["accountability", "anticipatory", "appreciatively", "authoritarianism", "colonialism"])
        assert (RiTa.search(JsDict({"regex": "010000", "type": "stresses", "limit": 5})) == ["accountability", "anticipatory", "appreciatively", "authoritarianism", "colonialism"])
        assert (RiTa.search(JsDict({"regex": "010000", "type": "stresses", "limit": 5, "maxLength": 11})) == ["colonialism", "imperialism", "materialism"])
        assert (RiTa.search(JsDict({"regex": "010000", "type": "stresses", "limit": 5, "minLength": 12})) == ["accountability", "anticipatory", "appreciatively", "authoritarianism", "conciliatory"])
        assert (RiTa.search(JsDict({"regex": "0/1/0/0/0/0", "type": "stresses", "limit": 5})) == ["accountability", "anticipatory", "appreciatively", "authoritarianism", "colonialism"])
    def test_should_call_search_with_stress_regex_limit(self):
        assert (RiTa.search(_re_compile("0\\/1\\/0\\/0\\/0\\/0"), JsDict({"type": "stresses", "limit": 5})) == ["accountability", "anticipatory", "appreciatively", "authoritarianism", "colonialism"])
        assert (RiTa.search(JsDict({"regex": _re_compile("0\\/1\\/0\\/0\\/0\\/0"), "type": "stresses", "limit": 5})) == ["accountability", "anticipatory", "appreciatively", "authoritarianism", "colonialism"])
    def test_should_call_randomword_pos_syls(self):
        def fail(result=None, epos=None, *args):
            test = (result[-(2)]) if (result.endswith(_jsstr("es"))) else (result)
            ent = RiTa.lexicon[test]
            return _jsstr(_jsstr(_jsstr(_jsstr(_jsstr(_jsstr(_jsstr("(") + _jsstr(epos)) + _jsstr(") Fail: ")) + _jsstr(result)) + _jsstr(": expected ")) + _jsstr(epos)) + _jsstr(", got ")) + _jsstr((ent[1]) if (ent) else ("null"))
        result = None
        syllables = None
        result = RiTa.random_word(JsDict({"numSyllables": 3, "pos": "vbz"}))
        assert (((len(result)) > (0)) is True), _jsstr("randomWord vbz: ") + _jsstr(result)
        syllables = RiTa.syllables(result)
        assert (len(syllables.split(RiTa.SYLLABLE_BOUNDARY)) == 3)
        assert (RiTa.is_verb(result) == True)
        result = RiTa.random_word(JsDict({"numSyllables": 1, "pos": "n"}))
        assert (((len(result)) > (0)) is True), _jsstr("randomWord n: ") + _jsstr(result)
        syllables = RiTa.syllables(result)
        assert (len(syllables.split(RiTa.SYLLABLE_BOUNDARY)) == 1)
        assert (RiTa.is_noun(result) == True)
        result = RiTa.random_word(JsDict({"numSyllables": 1, "pos": "nns"}))
        assert (((len(result)) > (0)) is True), _jsstr("randomWord nns: ") + _jsstr(result)
        syllables = RiTa.syllables(result)
        assert (len(syllables.split(RiTa.SYLLABLE_BOUNDARY)) == 1)
        assert (RiTa.is_noun(result) == True)
        result = RiTa.random_word(JsDict({"numSyllables": 5, "pos": "nns"}))
        assert (((len(result)) > (0)) is True), _jsstr("randomWord nns: ") + _jsstr(result)
        syllables = RiTa.syllables(result)
        count = len(syllables.split(RiTa.SYLLABLE_BOUNDARY))
        if (count) != (5):
            console.warn(_jsstr(_jsstr(_jsstr(_jsstr("Syllabifier problem: ") + _jsstr(result)) + _jsstr(".syllables was ")) + _jsstr(count)) + _jsstr(", expected 5"))
        assert (RiTa.is_noun(result) == True)
    def test_should_call_alliterations_numsyllables(self):
        result = RiTa.alliterations("cat", JsDict({"minLength": 1, "numSyllables": 7}))
        assert (result == ["electrocardiogram", "electromechanical", "telecommunications"])
        i = 0
        for i in range(0, len(result), 1):
            assert ((RiTa.is_alliteration(result[i], "cat")) is True), _jsstr("FAIL2: ") + _jsstr(result[i])
    def test_should_call_alliterations_pos(self):
        res = None
        res = RiTa.alliterations("cat", JsDict({"numSyllables": 7, "pos": "n"}))
        assert (res == ["electrocardiogram", "telecommunications"])
        i = 0
        for i in range(0, len(res), 1):
            assert ((RiTa.is_alliteration(res[i], "cat")) is True), _jsstr("FAIL2: ") + _jsstr(res[i])
        res = RiTa.alliterations("cat", JsDict({"minLength": 14, "pos": "v"}))
        for r in res:
            assert (((len(r)) >= (14)) is True)
        assert (res == ["counterbalance"])
        res = RiTa.alliterations("dog", JsDict({"minLength": 13, "pos": "rb", "limit": 11}))
        for r in res:
            assert (((len(r)) >= (13)) is True)
        assert (res == ["coincidentally", "conditionally", "confidentially", "contradictorily", "devastatingly", "expeditiously", "paradoxically", "predominantly", "traditionally", "unconditionally", "unpredictably"])
        res = RiTa.alliterations("freedom", JsDict({"minLength": 14, "pos": "nns"}))
        for r in res:
            assert (((len(r)) >= (14)) is True)
        assert (res == ["featherbeddings", "fundamentalists", "pharmaceuticals", "photosyntheses", "reconfigurations", "sophistications"])
    def test_should_call_alliterations(self):
        result = None
        result = RiTa.alliterations("", JsDict({"silent": 1}))
        assert (((len(result)) < (1)) is True)
        result = RiTa.alliterations("#$%^&*", JsDict({"silent": 1}))
        assert (((len(result)) < (1)) is True)
        result = RiTa.alliterations("umbrella", JsDict({"silent": 1}))
        assert (((len(result)) < (1)) is True), "failed on 'umbrella'"
        result = RiTa.alliterations("cat", JsDict({"limit": 100}))
        assert (((len(result)) == (100)) is True), "failed on 'cat'"
        assert (("cat" in result) is False)
        i = 0
        for i in range(0, len(result), 1):
            assert ((RiTa.is_alliteration(result[i], "cat")) is True)
        result = RiTa.alliterations("dog", JsDict({"limit": 100}))
        assert (("dog" in result) is False)
        assert (((len(result)) == (100)) is True), "failed on 'dog'"
        i = 0
        for i in range(0, len(result), 1):
            assert ((RiTa.is_alliteration(result[i], "dog")) is True)
        result = RiTa.alliterations("dog", JsDict({"minLength": 15}))
        assert ((((len(result)) > (0)) and ((len(result)) < (5))) is True), _jsstr("got length=") + _jsstr(len(result))
        i = 0
        for i in range(0, len(result), 1):
            assert ((RiTa.is_alliteration(result[i], "dog")) is True), _jsstr("FAIL1: ") + _jsstr(result[i])
        result = RiTa.alliterations("cat", JsDict({"minLength": 16}))
        assert ((((len(result)) > (0)) and ((len(result)) < (15))) is True), "failed on 'cat'"
        i = 0
        for i in range(0, len(result), 1):
            assert ((RiTa.is_alliteration(result[i], "cat")) is True), _jsstr("FAIL2: ") + _jsstr(result[i])
        result = RiTa.alliterations("khatt", JsDict({"minLength": 16}))
        assert ((((len(result)) > (0)) and ((len(result)) < (15))) is True), "failed on 'khatt'"
        i = 0
        for i in range(0, len(result), 1):
            assert ((RiTa.is_alliteration(result[i], "cat")) is True), _jsstr("FAIL2: ") + _jsstr(result[i])
        assert (RiTa.alliterations("a") == [])
        assert (RiTa.alliterations("I") == [])
        assert (RiTa.alliterations("K") == [])
    def test_should_call_rhymessync(self):
        assert (RiTa.lexicon.rhymes_sync("dog", JsDict({"limit": 1})) == ["cog"])
        assert (RiTa.lexicon.rhymes_sync("dog", JsDict({"limit": 2})) == ["cog", "log"])
        assert (RiTa.lexicon.rhymes_sync("dog") == ["cog", "log"])
    def test_should_call_rhymes(self):
        assert (len(RiTa.rhymes("cat")) == 10)
        assert (("hat" in RiTa.rhymes("cat")) is True)
        assert (("mellow" in RiTa.rhymes("yellow")) is True)
        assert (("boy" in RiTa.rhymes("toy")) is True)
        assert (("drab" in RiTa.rhymes("crab")) is True)
        assert (("house" in RiTa.rhymes("mouse")) is True)
        assert (("polo" in RiTa.rhymes("apple")) is False)
        assert (("these" in RiTa.rhymes("this")) is False)
        assert (("house" in RiTa.rhymes("hose")) is False)
        assert (("mellow" in RiTa.rhymes("sieve")) is False)
        assert (("grab" in RiTa.rhymes("swag")) is False)
        assert (("eight" in RiTa.rhymes("weight", JsDict({"limit": 1000}))) is True)
        assert (("weight" in RiTa.rhymes("eight", JsDict({"limit": 1000}))) is True)
        assert (("give" in RiTa.rhymes("sieve", JsDict({"limit": 1000}))) is True)
        assert (("more" in RiTa.rhymes("shore", JsDict({"limit": 1000}))) is True)
        assert (("sense" in RiTa.rhymes("tense", JsDict({"limit": 1000}))) is True)
        assert (("fog" in RiTa.rhymes("bog")) is True)
        assert (("log" in RiTa.rhymes("dog")) is True)
        assert (RiTa.rhymes("a") == [])
        assert (RiTa.rhymes("I") == [])
        assert (RiTa.rhymes("Z") == [])
        assert (RiTa.rhymes("B") == [])
        assert (RiTa.rhymes("K") == [])
    def test_should_call_rhymes_pos(self):
        assert (("hat" in RiTa.rhymes("cat", JsDict({"pos": "v"}))) is False)
        assert (("mellow" in RiTa.rhymes("yellow", JsDict({"pos": "a"}))) is True)
        assert (("boy" in RiTa.rhymes("toy", JsDict({"pos": "n"}))) is True)
        assert (("give" in RiTa.rhymes("sieve", JsDict({"pos": "n"}))) is False)
        assert (("condense" in RiTa.rhymes("tense", JsDict({"pos": "v"}))) is True)
        assert (("drab" in RiTa.rhymes("crab", JsDict({"pos": "n"}))) is False)
        assert (("more" in RiTa.rhymes("shore", JsDict({"pos": "v"}))) is False)
        assert (("house" in RiTa.rhymes("mouse", JsDict({"pos": "nn"}))) is True)
        assert (("eight" in RiTa.rhymes("weight", JsDict({"pos": "vb"}))) is False)
        assert (("weight" in RiTa.rhymes("eight", JsDict({"pos": "nn", "limit": 1000}))) is True)
        assert (("polo" in RiTa.rhymes("apple", JsDict({"pos": "v"}))) is False)
        assert (("these" in RiTa.rhymes("this", JsDict({"pos": "v"}))) is False)
        assert (("house" in RiTa.rhymes("hose", JsDict({"pos": "v"}))) is False)
        assert (("mellow" in RiTa.rhymes("sieve", JsDict({"pos": "v"}))) is False)
        assert (("grab" in RiTa.rhymes("swag", JsDict({"pos": "v"}))) is False)
        rhyme = RiTa.rhymes("spreads", JsDict({"pos": "vbz", "limit": 1000}))
        assert (("discriminateds" in rhyme) is False)
        assert (("endeds" in rhyme) is False)
        assert (("finisheds" in rhyme) is False)
        assert (("reporteds" in rhyme) is False)
        assert (("proliferateds" in rhyme) is False)
        assert (("outpaceds" in rhyme) is False)
        assert (("liveds" in rhyme) is False)
        assert (("bit" in RiTa.rhymes("hit", JsDict({"pos": "vb"}))) is False)
        assert (("bit" in RiTa.rhymes("hit", JsDict({"pos": "vbd"}))) is True)
        assert (("broke" in RiTa.rhymes("stroke", JsDict({"pos": "vb"}))) is False)
        assert (("broke" in RiTa.rhymes("stroke", JsDict({"pos": "vbd"}))) is True)
        assert (("involved" in RiTa.rhymes("evolved", JsDict({"pos": "vb"}))) is False)
        assert (("involved" in RiTa.rhymes("evolved", JsDict({"pos": "vbd"}))) is True)
    def test_should_call_rhymes_pos_nid(self):
        rhymes = RiTa.rhymes("abated", JsDict({"pos": "vbd", "limit": 1000}))
        assert (("allocated" in rhymes) is True)
        assert (("annihilated" in rhymes) is True)
        assert (("condensed" in rhymes) is False)
    def test_should_call_rhymes_numsyllables(self):
        assert (("hat" in RiTa.rhymes("cat", JsDict({"numSyllables": 1}))) is True)
        assert (("hat" in RiTa.rhymes("cat", JsDict({"numSyllables": 2}))) is False)
        assert (("hat" in RiTa.rhymes("cat", JsDict({"numSyllables": 3}))) is False)
        assert (("mellow" in RiTa.rhymes("yellow", JsDict({"numSyllables": 2}))) is True)
        assert (("mellow" in RiTa.rhymes("yellow", JsDict({"numSyllables": 3}))) is False)
        rhymes = RiTa.rhymes("abated", JsDict({"numSyllables": 3}))
        assert (("elated" in rhymes) is True)
        assert (("abated" in rhymes) is False)
        assert (("allocated" in rhymes) is False)
        assert (("condensed" in rhymes) is False)
    def test_should_call_rhymes_wordlength(self):
        assert (("hat" in RiTa.rhymes("cat", JsDict({"minLength": 4}))) is False)
        assert (("hat" in RiTa.rhymes("cat", JsDict({"maxLength": 2}))) is False)
        rhymes = RiTa.rhymes("abated", JsDict({"pos": "vbd", "maxLength": 9}))
        assert (("allocated" in rhymes) is True)
        assert (("annihilated" in rhymes) is False)
        assert (("condensed" in rhymes) is False)
    def test_should_call_spellslike(self):
        result = None
        result = RiTa.spells_like("")
        eql(result, [])
        result = RiTa.spells_like("banana")
        eql(result, ["banal", "bonanza", "cabana", "manna"])
        result = RiTa.spells_like("tornado")
        eql(result, ["torpedo"])
        result = RiTa.spells_like("ice")
        eql(result, ["ace", "dice", "iced", "icy", "ire", "lice", "nice", "rice", "vice"])
    @pytest.mark.skip(reason="disabled in JS")  # /*LTR*/
    def test_should_call_spellslike_minlimit(self):
        result = None
        result = RiTa.spells_like("")
        eql(result, [])
        result = RiTa.spells_like("banana", JsDict({"minLimit": 5}))
        eql(result, ["angina", "arena", "bacon", "balance", "ban"])
        result = RiTa.spells_like("tornado", JsDict({"minLimit": 10}))
        eql(result, ["condo", "forbade", "horned", "ornate", "thread", "tirade", "toad", "toenail", "tomato", "tonal"])
        result = RiTa.spells_like("ice", JsDict({"minLimit": 4}))
        eql(result, ["ace", "dice", "iced", "icy", "ire", "lice", "nice", "rice", "vice"])
    def test_should_call_spellslike_options(self):
        result = None
        result = RiTa.spells_like("banana", JsDict({"minLength": 6, "maxLength": 6}))
        eql(result, ["cabana"])
        result = RiTa.spells_like("banana", JsDict({"minLength": 6, "maxLength": 6}))
        eql(result, ["cabana"])
        result = RiTa.spells_like("banana", JsDict({"minDistance": 1}))
        eql(result, ["banal", "bonanza", "cabana", "manna"])
        result = RiTa.spells_like("ice", JsDict({"maxLength": 3}))
        eql(result, ["ace", "icy", "ire"])
        result = RiTa.spells_like("ice", JsDict({"minDistance": 2, "minLength": 3, "maxLength": 3, "limit": 1000}))
        for r in result:
            assert (((len(r)) == (3)) is True)
        assert (((len(result)) > (10)) is True)
        result = RiTa.spells_like("ice", JsDict({"minDistance": 0, "minLength": 3, "maxLength": 3}))
        eql(result, ["ace", "icy", "ire"])
        result = RiTa.spells_like("ice", JsDict({"minLength": 3, "maxLength": 3}))
        for r in result:
            assert (((len(r)) == (3)) is True)
        eql(result, ["ace", "icy", "ire"])
        result = RiTa.spells_like("ice", JsDict({"minLength": 3, "maxLength": 3, "pos": "n"}))
        for r in result:
            assert (((len(r)) == (3)) is True)
        eql(result, ["ace", "ire"])
        result = RiTa.spells_like("ice", JsDict({"minLength": 4, "maxLength": 4, "pos": "v", "limit": 5}))
        for r in result:
            assert (((len(r)) == (4)) is True)
        eql(result, ["ache", "bide", "bite", "cite", "dine"])
        result = RiTa.spells_like("ice", JsDict({"minLength": 4, "maxLength": 4, "pos": "nns", "limit": 5}))
        for r in result:
            assert (((len(r)) == (4)) is True)
        eql(result, ["dice", "rice"])
        result = RiTa.spells_like("ice", JsDict({"minLength": 4, "maxLength": 4, "pos": "nns", "minDistance": 3, "limit": 5}))
        for r in result:
            assert (((len(r)) == (4)) is True)
        eql(result, ["axes", "beef", "deer", "dibs", "fame"])
        result = RiTa.spells_like("abated", JsDict({"pos": "vbd"}))
        assert (("abetted" in result) is True)
        assert (("aborted" in result) is True)
        assert (("condensed" in result) is False)
        assert (("lived" in RiTa.spells_like("lined", JsDict({"pos": "vb"}))) is False)
        assert (("lived" in RiTa.spells_like("lined", JsDict({"pos": "vbd"}))) is True)
        assert (("led" in RiTa.spells_like("let", JsDict({"pos": "vb"}))) is False)
        assert (("led" in RiTa.spells_like("let", JsDict({"pos": "vbd"}))) is True)
        assert (("broke" in RiTa.spells_like("brake", JsDict({"pos": "vb"}))) is False)
        assert (("broke" in RiTa.spells_like("brake", JsDict({"pos": "vbd"}))) is True)
        assert (("oversaw" in RiTa.spells_like("overseas", JsDict({"pos": "vb"}))) is False)
        assert (("oversaw" in RiTa.spells_like("overseas", JsDict({"pos": "vbd"}))) is True)
        rhyme = RiTa.spells_like("spreads", JsDict({"pos": "vbz", "limit": 1000}))
        assert (("discriminateds" in rhyme) is False)
        assert (("endeds" in rhyme) is False)
        assert (("finisheds" in rhyme) is False)
        assert (("reporteds" in rhyme) is False)
        assert (("proliferateds" in rhyme) is False)
        assert (("outpaceds" in rhyme) is False)
        assert (("lived" in rhyme) is False)
    def test_should_call_soundslike(self):
        eql(RiTa.sounds_like("tornado", JsDict({"type": "sound"})), ["torpedo"])
        result = RiTa.sounds_like("try", JsDict({"limit": 20}))
        answer = ["cry", "dry", "fry", "pry", "rye", "tie", "tray", "tree", "tribe", "tried", "tripe", "trite", "true", "wry"]
        eql(result, answer)
        result = RiTa.sounds_like("try", JsDict({"minDistance": 2, "limit": 20}))
        assert (((len(result)) > (len(answer))) is True)
        result = RiTa.sounds_like("happy")
        eql(result, answer = ["happier", "hippie"])
        result = RiTa.sounds_like("happy", JsDict({"minDistance": 2}))
        assert (((len(result)) > (len(answer))) is True)
        result = RiTa.sounds_like("cat", JsDict({"type": "sound"}))
        eql(result, ["bat", "cab", "cache", "calf", "calve", "can", "can't", "cap", "cash", "cast"])
        result = RiTa.sounds_like("cat", JsDict({"type": "sound", "limit": 5}))
        eql(result, ["bat", "cab", "cache", "calf", "calve"])
        result = RiTa.sounds_like("cat", JsDict({"type": "sound", "limit": 1000, "minLength": 2, "maxLength": 4}))
        eql(result, ["at", "bat", "cab", "calf", "can", "cap", "cash", "cast", "chat", "coat", "cot", "curt", "cut", "fat", "hat", "kit", "kite", "mat", "matt", "pat", "rat", "sat", "that", "vat"])
        result = RiTa.sounds_like("cat", JsDict({"type": "sound", "minLength": 4, "maxLength": 5, "pos": "jj"}))
        eql(result, answer = ["catty", "curt"])
        result = RiTa.sounds_like("cat", JsDict({"minDistance": 2}))
        assert (((len(result)) > (len(answer))) is True)
    def test_should_call_soundslike_pos(self):
        result = RiTa.sounds_like("abated", JsDict({"pos": "vbd"}))
        assert (("abetted" in result) is True)
        assert (("debated" in result) is True)
        assert (("condensed" in result) is False)
        assert (("built" in RiTa.sounds_like("build", JsDict({"pos": "vb", "limit": 1000}))) is False)
        assert (("computerized" in RiTa.sounds_like("computerize", JsDict({"pos": "vb", "limit": 1000}))) is False)
        assert (("concerned" in RiTa.sounds_like("concern", JsDict({"pos": "vb"}))) is False)
        assert (("committed" in RiTa.sounds_like("commit", JsDict({"pos": "vb"}))) is False)
        assert (("involved" in RiTa.sounds_like("involve", JsDict({"pos": "vb"}))) is False)
        assert (("gained" in RiTa.sounds_like("grained", JsDict({"pos": "vb"}))) is False)
        assert (("remade" in RiTa.sounds_like("premade", JsDict({"pos": "vbd"}))) is True)
        assert (("discriminated" in RiTa.sounds_like("incriminate", JsDict({"pos": "vbd"}))) is True)
        assert (("pinched" in RiTa.sounds_like("paunched", JsDict({"pos": "vbd"}))) is True)
    def test_should_call_soundslike_matchspelling(self):
        result = None
        result = RiTa.sounds_like("try", JsDict({"matchSpelling": True}))
        eql(result, ["cry", "dry", "fry", "pry", "tray"])
        result = RiTa.sounds_like("try", JsDict({"matchSpelling": True, "maxLength": 3}))
        eql(result, ["cry", "dry", "fry", "pry", "wry"])
        result = RiTa.sounds_like("try", JsDict({"matchSpelling": True, "minLength": 4}))
        eql(result, ["tray"])
        result = RiTa.sounds_like("try", JsDict({"matchSpelling": True, "limit": 3}))
        eql(result, ["cry", "dry", "fry"])
        result = RiTa.sounds_like("daddy", JsDict({"matchSpelling": True}))
        eql(result, ["dandy", "paddy"])
        result = RiTa.sounds_like("banana", JsDict({"matchSpelling": True}))
        eql(result, ["bonanza"])
        result = RiTa.sounds_like("abated", JsDict({"pos": "vbd", "matchSpelling": True}))
        assert (len(result) == 2)
        assert (("abetted" in result) is True)
        assert (("awaited" in result) is True)
    def test_should_call_isrhyme(self):
        assert ((not (RiTa.is_rhyme("apple", "polo"))) is True)
        assert ((not (RiTa.is_rhyme("this", "these"))) is True)
        assert ((RiTa.is_rhyme("cat", "hat")) is True)
        assert ((RiTa.is_rhyme("yellow", "mellow")) is True)
        assert ((RiTa.is_rhyme("toy", "boy")) is True)
        assert ((RiTa.is_rhyme("solo", "tomorrow")) is True)
        assert ((RiTa.is_rhyme("tense", "sense")) is True)
        assert ((RiTa.is_rhyme("crab", "drab")) is True)
        assert ((RiTa.is_rhyme("shore", "more")) is True)
        assert ((not (RiTa.is_rhyme("hose", "house"))) is True)
        assert ((not (RiTa.is_rhyme("sieve", "mellow"))) is True)
        assert ((RiTa.is_rhyme("mouse", "house")) is True)
        assert ((RiTa.is_rhyme("yo", "bro")) is True)
        assert ((not (RiTa.is_rhyme("swag", "grab"))) is True)
        assert ((not (RiTa.is_rhyme("", ""))) is True)
        assert ((RiTa.is_rhyme("weight", "eight")) is True)
        assert ((RiTa.is_rhyme("eight", "weight")) is True)
        assert ((RiTa.is_rhyme("abated", "debated")) is True)
        if (_typeof(lambda: NOLEX)) != ("undefined"):
            assert ((RiTa.is_rhyme("sieve", "give")) is True)
    def test_should_call_isalliteration(self):
        assert ((RiTa.is_alliteration("knife", "gnat")) is True)
        assert ((RiTa.is_alliteration("knife", "naughty")) is True)
        assert ((RiTa.is_alliteration("sally", "silly")) is True)
        assert ((RiTa.is_alliteration("sea", "seven")) is True)
        assert ((RiTa.is_alliteration("silly", "seven")) is True)
        assert ((RiTa.is_alliteration("sea", "sally")) is True)
        assert ((RiTa.is_alliteration("big", "bad")) is True)
        assert ((RiTa.is_alliteration("bad", "big")) is True)
        assert ((RiTa.is_alliteration("BIG", "bad")) is True)
        assert ((RiTa.is_alliteration("big", "BAD")) is True)
        assert ((RiTa.is_alliteration("BIG", "BAD")) is True)
        assert ((not (RiTa.is_alliteration("", ""))) is True)
        assert ((not (RiTa.is_alliteration("wind", "withdraw"))) is True)
        assert ((not (RiTa.is_alliteration("solo", "tomorrow"))) is True)
        assert ((not (RiTa.is_alliteration("solo", "yoyo"))) is True)
        assert ((not (RiTa.is_alliteration("yoyo", "jojo"))) is True)
        assert ((not (RiTa.is_alliteration("cat", "access"))) is True)
        assert ((RiTa.is_alliteration("unsung", "sine")) is True)
        assert ((RiTa.is_alliteration("job", "gene")) is True)
        assert ((RiTa.is_alliteration("jeans", "gentle")) is True)
        assert ((RiTa.is_alliteration("abet", "better")) is True)
        assert ((RiTa.is_alliteration("never", "knight")) is True)
        assert ((RiTa.is_alliteration("knight", "navel")) is True)
        assert ((RiTa.is_alliteration("cat", "kitchen")) is True)
        assert ((not (RiTa.is_alliteration("octopus", "oblong"))) is True)
        assert ((not (RiTa.is_alliteration("omen", "open"))) is True)
        assert ((not (RiTa.is_alliteration("amicable", "atmosphere"))) is True)
        assert ((RiTa.is_alliteration("abated", "abetted")) is True)
        if (_typeof(lambda: NOLEX)) != ("undefined"):
            assert ((RiTa.is_alliteration("this", "these")) is True)
            assert ((RiTa.is_alliteration("psychology", "cholera")) is True)
            assert ((RiTa.is_alliteration("consult", "sultan")) is True)
            assert ((RiTa.is_alliteration("monsoon", "super")) is True)
    @pytest.mark.skip(reason="disabled in JS")  # /*LTR*/
    def test_should_call_findstem(self):
        lex = RiTa.lexicon
        assert (lex.find_stem("chang") == "change")
        assert (lex.find_stem("accid") == "accident")
        assert (lex.find_stem("accept") == "accept")
        assert (lex.find_stem("bear") == "bear")
        assert (lex.find_stem("bodi") == "bodied")
        assert (lex.find_stem("book") == "book")
        assert (lex.find_stem("box") == "box")
        assert (lex.find_stem("across") == "across")
        assert (lex.find_stem("activ") == "active")
        assert (lex.find_stem("adulter") == "adulterer")
        assert (lex.find_stem("allianc") == "alliance")
        assert (lex.find_stem("beautifi") == "beautify")
        assert (lex.find_stem("bestsel") == "bestseller")
        assert (lex.find_stem("blond") == "blond")
        assert (lex.find_stem("borderlin") == "borderline")
        assert (lex.find_stem("brave") == "brave")
        assert (lex.find_stem("calor") == "caloric")
        assert (lex.find_stem("central") == "central")
        assert (lex.find_stem("certifi") == "certified")
        assert (lex.find_stem("choppi") == "choppy")
        assert (lex.find_stem("cigarett") == "cigarette")
        assert (lex.find_stem("cogniz") == "cognizant")
        assert (lex.find_stem("delicatessen") == "delicatessen")
        assert (lex.find_stem("disaffect") == "disaffected")
        assert (lex.find_stem("dog") == "dog")
        assert (lex.find_stem("drachma") == "drachma")
        assert (lex.find_stem("dualism") == "dualism")
        assert (lex.find_stem("dwell") == "dwell")
        assert (lex.find_stem("earthenwar") == "earthenware")
        assert (lex.find_stem("efficaci") == "efficacious")
        assert (lex.find_stem("elus") == "elusive")
        assert (lex.find_stem("emiss") == "emission")
        assert (lex.find_stem("environment") == "environmental")
        assert (lex.find_stem("fisherman") == "fisherman")
        assert (lex.find_stem("fragil") == "fragile")
        assert (lex.find_stem("fundamentalist") == "fundamentalist")
        assert (lex.find_stem("futil") == "futile")
        assert (lex.find_stem("fuzz") == "fuzz")
        assert (lex.find_stem("garag") == "garage")
        assert (lex.find_stem("gass") == "gass")
        assert (lex.find_stem("govern") == "govern")
        assert (lex.find_stem("groov") == "groove")
        assert (lex.find_stem("guttur") == "guttural")
        assert (lex.find_stem("hamburg") == "hamburger")
        assert (lex.find_stem("haphazard") == "haphazard")
        assert (lex.find_stem("haunt") == "haunt")
        assert (lex.find_stem("headlong") == "headlong")
        assert (lex.find_stem("hubbub") == "hubbub")
        assert (lex.find_stem("hungrili") == "hungrily")
        assert (lex.find_stem("hypoglycem") == "hypoglycemic")
    @pytest.mark.skip(reason="disabled in JS")  # /*LTR*/
    def test_should_call_findstem_for_words_not_in_dict(self):
        assert (lex.find_stem("abut") == None)
        assert (lex.find_stem("airdrop") == None)
        assert (lex.find_stem("waylay") == None)
        assert (lex.find_stem("backslid") == None)
        assert (lex.find_stem("bejewel") == None)
        assert (lex.find_stem("blab") == None)
        assert (lex.find_stem("brutifi") == None)
        assert (lex.find_stem("bullwhip") == None)
        assert (lex.find_stem("catnap") == None)
        assert (lex.find_stem("clop") == None)
        assert (lex.find_stem("verbifi") == None)
        assert (lex.find_stem("dandifi") == None)
        assert (lex.find_stem("declassifi") == None)
        assert (lex.find_stem("disbar") == None)
        assert (lex.find_stem("disint") == None)
        assert (lex.find_stem("empanel") == None)
        assert (lex.find_stem("fib") == None)
        assert (lex.find_stem("flog") == None)
        assert (lex.find_stem("ghostwritten") == None)
        assert (lex.find_stem("glom") == None)
        assert (lex.find_stem("hypertrophi") == None)
        assert (lex.find_stem("interlaid") == None)
        assert (lex.find_stem("jut") == None)
        assert (lex.find_stem("miscarri") == None)
        assert (lex.find_stem("mortifi") == None)
        assert (lex.find_stem("overbid") == None)
        assert (lex.find_stem("overgrow") == None)
        assert (lex.find_stem("quickstep") == None)
        assert (lex.find_stem("recommit") == None)
        assert (lex.find_stem("rewound") == None)
        assert (lex.find_stem("scram") == None)
        assert (lex.find_stem("sightseen") == None)
        assert (lex.find_stem("skydov") == None)
        assert (lex.find_stem("unplug") == None)
        assert (lex.find_stem("stencil") == None)
        assert (lex.find_stem("spellbind") == None)
        assert (lex.find_stem("subjectifi") == None)
        assert (lex.find_stem("sup") == None)
        assert (lex.find_stem("syllabifi") == None)
        assert (lex.find_stem("snog") == None)
        assert (lex.find_stem("unmak") == None)
        assert (lex.find_stem("stupefi") == None)
        assert (lex.find_stem("sulli") == None)
        assert (lex.find_stem("tram") == None)
        assert (lex.find_stem("underpay") == None)
        assert (lex.find_stem("understudi") == None)
        assert (lex.find_stem("unpin") == None)
        assert (lex.find_stem("unzip") == None)
        assert (lex.find_stem("whir") == None)
        assert (lex.find_stem("yakk") == None)
        assert (lex.find_stem("yap") == None)
        assert (lex.find_stem("body") == None)
        assert (lex.find_stem("justify") == None)
        assert (lex.find_stem("cancelled") == None)
        assert (lex.find_stem("trolling") == None)
        assert (lex.find_stem("change") == None)
    def test_should_correctly_call_tophonearray(self):
        raw = RiTa.lexicon.raw_phones("tornado", False)
        result = RiTa.lexicon._to_phone_array(raw)
        ans = ["t", "ao", "r", "n", "ey", "d", "ow"]
        assert (result == ans)
    # (helper hoisted to module scope)

def eql(output=None, expected=None, msg=None, *args):
    assert (output == expected)

