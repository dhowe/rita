# AUTO-GENERATED from js/test/lexicon-tests.js by scripts/js-to-py-tests.js — do not edit by hand.
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

def eql(output, expected, msg):
    assert (output == expected)

class TestLexicon:
    # mocha this.slow — ignored
    pass
    # mocha this.timeout — ignored
    pass
    def test_should_call_hasword(self):
        i = 0
        for i in range(10):
            assert ((RiTa.hasWord(RiTa.randomWord())) is True)
        assert ((RiTa.hasWord("random")) is True)
        assert ((RiTa.hasWord("dog")) is True)
        assert ((RiTa.hasWord("men")) is True)
        assert ((RiTa.hasWord("happily")) is True)
        assert ((RiTa.hasWord("play")) is True)
        assert ((RiTa.hasWord("plays")) is True)
        assert ((RiTa.hasWord("played")) is True)
        assert ((RiTa.hasWord("written")) is True)
        assert ((RiTa.hasWord("dogs")) is True)
        assert ((RiTa.hasWord("oxen")) is True)
        assert ((RiTa.hasWord("mice")) is True)
        assert ((RiTa.hasWord("dogs", {"noDerivations": True})) is False)
        assert ((RiTa.hasWord("played", {"noDerivations": True})) is False)
        assert ((RiTa.hasWord("cats", {"noDerivations": True})) is False)
        assert ((RiTa.hasWord("bunning")) is False)
        assert ((RiTa.hasWord("coyes")) is False)
        assert ((RiTa.hasWord("soes")) is False)
        assert ((RiTa.hasWord("knews")) is False)
        assert ((RiTa.hasWord("fastering")) is False)
        assert ((RiTa.hasWord("loosering")) is False)
        assert ((RiTa.hasWord("knews")) is False)
        assert ((RiTa.hasWord("barkness")) is False)
        assert ((RiTa.hasWord("horne")) is False)
        assert ((RiTa.hasWord("haye")) is False)
        assert ((RiTa.hasWord("bites")) is True)
        assert ((RiTa.hasWord("bit")) is True)
        assert ((RiTa.hasWord("bitted")) is False)
        assert ((RiTa.hasWord("breaks")) is True)
        assert ((RiTa.hasWord("broke")) is True)
        assert ((RiTa.hasWord("brokes")) is False)
        assert ((RiTa.hasWord("broked")) is False)
        assert ((RiTa.hasWord("concerned")) is True)
        assert ((RiTa.hasWord("concerneded")) is False)
        assert ((RiTa.hasWord("concerneds")) is False)
        assert ((RiTa.hasWord("outpaced")) is True)
        assert ((RiTa.hasWord("outpaceded")) is False)
        assert ((RiTa.hasWord("outpaceds")) is False)
        assert ((RiTa.hasWord("reported")) is True)
        assert ((RiTa.hasWord("reporteds")) is False)
        assert ((RiTa.hasWord("reporteded")) is False)
        assert ((RiTa.hasWord("build")) is True)
        assert ((RiTa.hasWord("built")) is True)
        assert ((RiTa.hasWord("called")) is True)
        assert ((RiTa.hasWord("calleds")) is False)
        assert ((RiTa.hasWord("calleded")) is False)
        assert ((RiTa.hasWord("commits")) is True)
        assert ((RiTa.hasWord("committed")) is True)
        assert ((RiTa.hasWord("committeds")) is False)
        assert ((RiTa.hasWord("committeded")) is False)
        assert ((RiTa.hasWord("computerized")) is True)
        assert ((RiTa.hasWord("computerizeds")) is False)
        assert ((RiTa.hasWord("computerizeded")) is False)
        assert ((RiTa.hasWord("gets")) is True)
        assert ((RiTa.hasWord("got")) is True)
        assert ((RiTa.hasWord("gots")) is False)
        assert ((RiTa.hasWord("gotten")) is True)
        assert ((RiTa.hasWord("leads")) is True)
        assert ((RiTa.hasWord("led")) is True)
        assert ((RiTa.hasWord("leds")) is False)
        assert ((RiTa.hasWord("oversaw")) is True)
        assert ((RiTa.hasWord("overseen")) is True)
        assert ((RiTa.hasWord("oversaws")) is False)
        assert ((RiTa.hasWord("overseened")) is False)
        assert ((RiTa.hasWord("remakes")) is True)
        assert ((RiTa.hasWord("remade")) is True)
        assert ((RiTa.hasWord("remaded")) is False)
        assert ((RiTa.hasWord("discriminates")) is True)
        assert ((RiTa.hasWord("discriminated")) is True)
        assert ((RiTa.hasWord("discriminateds")) is False)
        assert ((RiTa.hasWord("launched")) is True)
        assert ((RiTa.hasWord("launcheds")) is False)
        assert ((RiTa.hasWord("launcheded")) is False)
        assert ((RiTa.hasWord("starts")) is True)
        assert ((RiTa.hasWord("started")) is True)
        assert ((RiTa.hasWord("starteds")) is False)
    def test_should_call_randomword(self):
        result = None
        result = RiTa.randomWord()
        assert (((len(result)) > (0)) is True), ("randomWord: ") + (result)
        assert (((result) == (RiTa.randomWord())) is False), (("randomWord returned same result '") + (result)) + ("'")
        result = RiTa.randomWord({"numSyllables": 3})
        assert (((len(result)) > (0)) is True), ("3 syllables: ") + (result)
        result = RiTa.randomWord({"numSyllables": 5})
        assert (((len(result)) > (0)) is True), ("5 syllables: ") + (result)
    def test_should_not_mutate_the_caller_options_object(self):
        opts = {"numSyllables": 2}
        RiTa.randomWord(opts)
        assert ((opts in "limit") is False), "randomWord leaked limit"
        assert ((opts in "shuffle") is False), "randomWord leaked shuffle"
        opts = {"pos": "nn"}
        RiTa.searchSync(__re_compile("^a"), opts)
        assert ((opts in "targetPos") is False), "search leaked targetPos"
        assert ((opts in "minDistance") is False), "search leaked minDistance"
        opts = {"limit": 5}
        RiTa.rhymesSync("cat", opts)
        assert ((opts in "maxLength") is False), "rhymes leaked maxLength"
    def test_should_call_randomword_with_regex(self):
        result = RiTa.randomWord("^a")
        assert ((__re_compile("^a").search(result) is not None) is True)
        assert (((len(result)) > (3)) is True)
        result = RiTa.randomWord("^apple$")
        assert (result == "apple")
        result = RiTa.randomWord("le")
        assert (("le" in result) is True)
        results = []
        i = 0
        for i in range(10):
            results.append(RiTa.randomWord("^a"))
        assert (((len(results)) == (10)) is True)
        i = 0
        while (i) < ((len(results)) - (1)):
            if (results[i]) == (results[(i) + (1)]):
                results.splice(i, 1)
            else:
                i += 1
        assert (((len(results)) > (1)) is True)
        result = RiTa.randomWord(__re_compile("^a"))
        assert ((__re_compile("^a").search(result) is not None) is True)
        assert (((len(result)) > (3)) is True)
        result = RiTa.randomWord(__re_compile("^apple$"))
        assert (result == "apple")
        result = RiTa.randomWord(__re_compile("le"))
        assert (("le" in result) is True)
        result = RiTa.randomWord("^a")
        assert ((result.startswith("a")) is True)
        results = []
        i = 0
        for i in range(10):
            results.append(RiTa.randomWord(__re_compile("^a")))
        assert (((len(results)) == (10)) is True)
    def test_should_call_randomword_with_stress_regex(self):
        result = RiTa.randomWord("0/1/0", {"type": "stresses"})
        assert ((len(result)) > (3))
        assert ("0/1/0" in RiTa.analyze(result).stresses)
        result = RiTa.randomWord("^0/1/0$", {"type": "stresses"})
        assert (RiTa.analyze(result).stresses == "0/1/0")
        result = RiTa.randomWord("010", {"type": "stresses"})
        assert (("0/1/0" in RiTa.analyze(result).stresses) is True)
        result = RiTa.randomWord("^010$", {"type": "stresses"})
        assert (RiTa.analyze(result).stresses == "0/1/0")
        result = RiTa.randomWord(__re_compile("0\\/1\\/0"), {"type": "stresses"})
        assert (("0/1/0" in RiTa.analyze(result).stresses) is True)
        result = RiTa.randomWord(__re_compile("^0\\/1\\/0\\/0$"), {"type": "stresses"})
        assert (RiTa.analyze(result).stresses == "0/1/0/0")
    def test_should_call_randomword_with_phones_regex(self):
        result = RiTa.randomWord("^th", {"type": "phones"})
        assert ((len(result)) > (3))
        assert ((__re_compile("^th").search(RiTa.analyze(result).phones) is not None) is True)
        result = RiTa.randomWord("v$", {"type": "phones"})
        assert ((__re_compile("v$").search(RiTa.analyze(result).phones) is not None) is True)
        result = RiTa.randomWord("^b-ih-l-iy-v$", {"type": "phones"})
        assert (result == "believe")
        result = RiTa.randomWord("ae", {"type": "phones"})
        assert (("ae" in RiTa.analyze(result).phones) is True)
        result = RiTa.randomWord(__re_compile("^th"), {"type": "phones"})
        assert ((len(result)) > (3))
        assert ((__re_compile("^th").search(RiTa.analyze(result).phones) is not None) is True)
        result = RiTa.randomWord(__re_compile("v$"), {"type": "phones"})
        assert ((__re_compile("v$").search(RiTa.analyze(result).phones) is not None) is True)
        result = RiTa.randomWord(__re_compile("^b-ih-l-iy-v$"), {"type": "phones"})
        assert (result == "believe")
        result = RiTa.randomWord(__re_compile("ae"), {"type": "phones"})
        assert (("ae" in RiTa.analyze(result).phones) is True)
    def test_should_call_randomword_with_opts_regex(self):
        result = RiTa.randomWord({"regex": "^a"})
        assert ((__re_compile("^a").search(result) is not None) is True)
        assert (((len(result)) > (3)) is True)
        result = RiTa.randomWord({"regex": __re_compile("^a")})
        assert ((__re_compile("^a").search(result) is not None) is True)
        assert (((len(result)) > (3)) is True)
        result = RiTa.randomWord({"regex": "0/1/0", "type": "stresses"})
        assert ((len(result)) > (3))
        assert (("0/1/0" in RiTa.analyze(result).stresses) is True)
        result = RiTa.randomWord({"regex": __re_compile("0\\/1\\/0"), "type": "stresses"})
        assert (("0/1/0" in RiTa.analyze(result).stresses) is True)
        result = RiTa.randomWord({"regex": "^th", "type": "phones"})
        assert ((len(result)) > (3))
        assert ((__re_compile("^th").search(RiTa.analyze(result).phones) is not None) is True)
        result = RiTa.randomWord({"regex": __re_compile("^th"), "type": "phones"})
        assert ((len(result)) > (3))
        assert ((__re_compile("^th").search(RiTa.analyze(result).phones) is not None) is True)
    def test_should_handle_an_augmented_lexicon(self):
        toAdd = {"deg": ["d-eh1-g", "nn"], "wadly": ["w-ae1-d l-iy", "rb"]}
        lex = RiTa.lexicon
        for w in list(obj.keys()):
            RiTa.lexicon.data[w] = toAdd[w]
        assert (lex.hasWord("run"))
        assert (lex.hasWord("walk"))
        assert (lex.hasWord("deg"))
        assert (lex.hasWord("wadly"))
        assert (lex.isAlliteration("wadly", "welcome"))
        for w in list(obj.keys()):
            RiTa.lexicon.data[w]
    def test_should_handle_a_custom_lexicon(self):
        lex = RiTa.lexicon
        orig = lex.data
        lex.data = {"dog": ["d-ao1-g", "nn"], "cat": ["k-ae1-t", "nn"], "happily": ["hh-ae1 p-ah l-iy", "rb"], "walk": ["w-ao1-k", "vb vbp nn"], "welcome": ["w-eh1-l k-ah-m", "jj nn vb vbp"], "sadly": ["s-ae1-d l-iy", "rb"]}
        assert ((lex.hasWord("run")) is False)
        assert ((lex.hasWord("walk")) is True)
        assert ((lex.isAlliteration("walk", "welcome")) is True)
        lex.data = orig
    def test_should_call_randomword_with_pos(self):
        with pytest.raises(Exception):
            return RiTa.randomWord({"pos": "xxx"})
        result = None
        pos = ["nn", "jj", "jjr", "wp"]
        j = 0
        for j in range(len(pos)):
            result = RiTa.randomWord({"pos": pos[j]})
            best = RiTa.tagger.allTags(result)[0]
            assert (pos[j] == best)
        i = 0
        for i in range(5):
            result = RiTa.randomWord({"pos": "nns"})
            if not (RiTa.inflector.isPlural(result)):
                console.warn(((((((("Pluralize/Singularize problem: randomWord(nns) was '") + (result)) + ("' (")) + ("isPlural=")) + (RiTa.inflector.isPlural(result))) + ("), singularized is '")) + (RiTa.singularize(result))) + ("'"))
            pos = RiTa.lexicon._posData(result)
            assert (((not (pos)) or ((__indexof(pos, "vbg")) < (0))) is True), ("randomWord nns: ") + (result)
            assert ((not (result.endswith("ness"))) is True), ("randomWord nns: ") + (result)
            assert ((not (result.endswith("isms"))) is True), ("randomWord nns: ") + (result)
        result = RiTa.randomWord({"pos": "v"})
        assert (((len(result)) > (0)) is True), ("randomWord v=") + (result)
        result = RiTa.randomWord({"pos": "nn"})
        assert (((len(result)) > (0)) is True), ("randomWord nn: ") + (result)
        result = RiTa.randomWord({"pos": "nns"})
        assert (((len(result)) > (0)) is True), ("randomWord nns=") + (result)
        result = RiTa.randomWord({"pos": "n"})
        assert (((len(result)) > (0)) is True), ("randomWord n=") + (result)
        result = RiTa.randomWord({"pos": "v"})
        assert (((len(result)) > (0)) is True), ("randomWord v=") + (result)
        result = RiTa.randomWord({"pos": "rp"})
        assert (((len(result)) > (0)) is True), ("randomWord rp=") + (result)
        results = []
        i = 0
        for i in range(10):
            results.append(RiTa.randomWord({"pos": "nns"}))
            assert (((__typeof(results[(len(results)) - (1)])) == ("string")) is True)
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
        result = RiTa.randomWord({"numSyllables": 3})
        syllables = RiTa.syllables(result)
        num = len(syllables.split(RiTa.SYLLABLE_BOUNDARY))
        assert (((len(result)) > (0)) is True), ("failed1 on: ") + (result)
        assert (((num) == (3)) is True), ((result) + (": ")) + (syllables)
        result = RiTa.randomWord({"numSyllables": 5})
        syllables = RiTa.syllables(result)
        num = len(syllables.split(RiTa.SYLLABLE_BOUNDARY))
        assert (len(result) > 0)
        assert (((num) == (5)) is True), ((result) + (": ")) + (syllables)
    def test_should_call_search_without_regex(self):
        assert (len(RiTa.search()) > 20000)
        assert (len(RiTa.search({"limit": 11})) == 11)
        assert (RiTa.search({"pos": "n"}) == ["abalone", "abandonment", "abbey", "abbot", "abbreviation", "abdomen", "abduction", "aberration", "ability", "abnormality"])
        res = RiTa.search({"numSyllables": 2})
        assert (res == ["abashed", "abate", "abbey", "abbot", "abduct", "abet", "abhor", "abide", "abject", "ablaze"])
        assert (RiTa.search({"numSyllables": 2, "pos": "n"}) == ["abbey", "abbot", "abode", "abscess", "absence", "abstract", "abuse", "abyss", "accent", "access"])
        assert (RiTa.search({"numSyllables": 1, "pos": "n"}) == ["ace", "ache", "act", "age", "aid", "aide", "aim", "air", "aisle", "ale"])
        search = RiTa.search({"pos": "vb", "limit": -(1)})
        assert (("concerned" in search) is False)
        assert (("committed" in search) is False)
        assert (("called" in search) is False)
        assert (("computerized" in search) is False)
        search = RiTa.search({"pos": "vbd", "limit": -(1)})
        assert (("concerned" in search) is True)
        assert (("committed" in search) is True)
        assert (("called" in search) is True)
        assert (("computerized" in search) is True)
        (0) and (expect("conclude" in search).to.be.true)
        search = RiTa.search({"pos": "vbn", "limit": -(1)})
        assert (("concerned" in search) is True)
        assert (("committed" in search) is True)
        assert (("called" in search) is True)
        assert (("computerized" in search) is True)
        (0) and (expect("conclude" in search).to.be.true)
    def test_should_call_search_with_letters(self):
        assert (RiTa.search("phant") == ["elephant", "elephantine", "phantom", "sycophantic", "triumphant", "triumphantly"])
        assert (RiTa.search(__re_compile("phant")) == ["elephant", "elephantine", "phantom", "sycophantic", "triumphant", "triumphantly"])
        assert (RiTa.search({"regex": "phant"}) == ["elephant", "elephantine", "phantom", "sycophantic", "triumphant", "triumphantly"])
        assert (RiTa.search({"regex": __re_compile("phant")}) == ["elephant", "elephantine", "phantom", "sycophantic", "triumphant", "triumphantly"])
    def test_should_call_search_with_phones_limit(self):
        result = RiTa.search(__re_compile("f-a[eh]-n-t"), {"type": "phones", "limit": 10})
        assert (result == ["elephant", "elephantine", "fantasia", "fantasize", "fantastic", "fantastically", "fantasy", "infant", "infantile", "infantry"])
        result = RiTa.search("f-ah-n-t", {"type": "phones", "limit": 5})
        assert (result == ["elephant", "infant", "infantile", "infantry", "oftentimes"])
        result = RiTa.search({"regex": __re_compile("f-a[eh]-n-t"), "type": "phones", "limit": 10})
        assert (result == ["elephant", "elephantine", "fantasia", "fantasize", "fantastic", "fantastically", "fantasy", "infant", "infantile", "infantry"])
    def test_should_call_search_with_phones_no_limit_and_shuffle(self):
        result = RiTa.search({"regex": "f-ah-n-t", "type": "phones", "limit": -(1)})
        assert (result == ["elephant", "infant", "infantile", "infantry", "oftentimes", "triumphant", "triumphantly"])
        result2 = RiTa.search({"regex": "f-ah-n-t", "type": "phones", "limit": -(1), "shuffle": True})
        assert (sorted(result2) == result)
    def test_should_call_search_with_pos_phones_sylls_limit(self):
        res = RiTa.search("f-ah-n-t", {"type": "phones", "pos": "n", "limit": 3, "numSyllables": 2})
        assert (res == ["infant"])
    def test_should_call_search_with_pos_phones_limit(self):
        res = RiTa.search("f-ah-n-t", {"type": "phones", "pos": "n", "limit": 3})
        assert (res == ["elephant", "infant", "infantry"])
        res = RiTa.search(__re_compile("f-a[eh]-n-t"), {"type": "phones", "pos": "v", "limit": 5})
        assert (res == ["fantasize"])
    def test_should_call_search_with_pos_regex(self):
        res = RiTa.search(__re_compile("cares$"), {"pos": "nns", "limit": -(1)})
        assert (res == ["cares", "scares"])
        res = RiTa.search(__re_compile("^rice$"), {"pos": "nns", "limit": -(1)})
        assert (res == ["rice"])
    def test_should_call_search_with_pos_letters(self):
        res = RiTa.search("cause", {"pos": "nns"})
        assert (res == ["causes", "causeways"])
        res = RiTa.search("gain", {"pos": "vbd", "numSyllables": 1})
        assert (res == ["gained"])
        res = RiTa.search("end", {"pos": "vbd", "minLength": 2, "limit": -(1)})
        assert (("ended" in res) is True)
        res = RiTa.search("commit", {"pos": "vbd"})
        assert (("committed" in res) is True)
        res = RiTa.search("involve", {"pos": "vbd"})
        assert (("involved" in res) is True)
        res = RiTa.search("outpace", {"pos": "vbn"})
        assert (res == ["outpaced"])
        res = RiTa.search("paid", {"pos": "vbd"})
        assert (("prepaid" in res) is True)
        res = RiTa.search("made", {"pos": "vbd"})
        assert (("remade" in res) is True)
        res = RiTa.search("re", {"pos": "vbd", "limit": -(1)})
        assert (("reopened" in res) is True)
        assert (("resold" in res) is True)
    def test_should_call_search_with_simple_pos_phones_limit(self):
        assert (RiTa.search(__re_compile("f-a[eh]-n-t"), {"type": "phones", "pos": "vb", "limit": 5}) == ["fantasize"])
        assert (RiTa.search("f-ah-n-t", {"type": "phones", "pos": "nns", "limit": 3}) == ["elephants", "infants", "infantries"])
    def test_should_call_search_with_pos_stress_limit(self):
        assert (RiTa.search("010", {"type": "stresses", "limit": 5, "pos": "n"}) == ["abalone", "abandonment", "abbreviation", "abdomen", "abduction"])
        assert (RiTa.search("010", {"type": "stresses", "limit": 5, "pos": "n", "numSyllables": 3}) == ["abdomen", "abduction", "abortion", "abruptness", "absorber"])
        assert (RiTa.search("010", {"type": "stresses", "limit": 5, "pos": "nns"}) == ["abalone", "abandonments", "abbreviations", "abductions", "abilities"])
        assert (RiTa.search(__re_compile("0\\/1\\/0"), {"type": "stresses", "limit": 5, "pos": "nns"}) == ["abalone", "abandonments", "abbreviations", "abductions", "abilities"])
        assert (RiTa.search("010", {"type": "stresses", "limit": 5, "pos": "nns", "numSyllables": 3}) == ["abductions", "abortions", "absorbers", "abstentions", "abstractions"])
    def test_should_call_search_with_stresses_limit(self):
        assert (RiTa.search("010000", {"type": "stresses", "limit": 5}) == ["accountability", "anticipatory", "appreciatively", "authoritarianism", "colonialism"])
        assert (RiTa.search("010000", {"type": "stresses", "limit": 5, "maxLength": 11}) == ["colonialism", "imperialism", "materialism"])
        assert (RiTa.search("010000", {"type": "stresses", "limit": 5, "minLength": 12}) == ["accountability", "anticipatory", "appreciatively", "authoritarianism", "conciliatory"])
        assert (RiTa.search("0/1/0/0/0/0", {"type": "stresses", "limit": 5}) == ["accountability", "anticipatory", "appreciatively", "authoritarianism", "colonialism"])
        assert (RiTa.search({"regex": "010000", "type": "stresses", "limit": 5}) == ["accountability", "anticipatory", "appreciatively", "authoritarianism", "colonialism"])
        assert (RiTa.search({"regex": "010000", "type": "stresses", "limit": 5, "maxLength": 11}) == ["colonialism", "imperialism", "materialism"])
        assert (RiTa.search({"regex": "010000", "type": "stresses", "limit": 5, "minLength": 12}) == ["accountability", "anticipatory", "appreciatively", "authoritarianism", "conciliatory"])
        assert (RiTa.search({"regex": "0/1/0/0/0/0", "type": "stresses", "limit": 5}) == ["accountability", "anticipatory", "appreciatively", "authoritarianism", "colonialism"])
    def test_should_call_search_with_stress_regex_limit(self):
        assert (RiTa.search(__re_compile("0\\/1\\/0\\/0\\/0\\/0"), {"type": "stresses", "limit": 5}) == ["accountability", "anticipatory", "appreciatively", "authoritarianism", "colonialism"])
        assert (RiTa.search({"regex": __re_compile("0\\/1\\/0\\/0\\/0\\/0"), "type": "stresses", "limit": 5}) == ["accountability", "anticipatory", "appreciatively", "authoritarianism", "colonialism"])
    def test_should_call_randomword_pos_syls(self):
        def fail(result, epos):
            test = (result[-(2)]) if (result.endswith("es")) else (result)
            ent = RiTa.lexicon[test]
            return ((((((("(") + (epos)) + (") Fail: ")) + (result)) + (": expected ")) + (epos)) + (", got ")) + ((ent[1]) if (ent) else ("null"))
        result = None
        syllables = None
        result = RiTa.randomWord({"numSyllables": 3, "pos": "vbz"})
        assert (((len(result)) > (0)) is True), ("randomWord vbz: ") + (result)
        syllables = RiTa.syllables(result)
        assert (len(syllables.split(RiTa.SYLLABLE_BOUNDARY)) == 3)
        assert (RiTa.isVerb(result) == True)
        result = RiTa.randomWord({"numSyllables": 1, "pos": "n"})
        assert (((len(result)) > (0)) is True), ("randomWord n: ") + (result)
        syllables = RiTa.syllables(result)
        assert (len(syllables.split(RiTa.SYLLABLE_BOUNDARY)) == 1)
        assert (RiTa.isNoun(result) == True)
        result = RiTa.randomWord({"numSyllables": 1, "pos": "nns"})
        assert (((len(result)) > (0)) is True), ("randomWord nns: ") + (result)
        syllables = RiTa.syllables(result)
        assert (len(syllables.split(RiTa.SYLLABLE_BOUNDARY)) == 1)
        assert (RiTa.isNoun(result) == True)
        result = RiTa.randomWord({"numSyllables": 5, "pos": "nns"})
        assert (((len(result)) > (0)) is True), ("randomWord nns: ") + (result)
        syllables = RiTa.syllables(result)
        count = len(syllables.split(RiTa.SYLLABLE_BOUNDARY))
        if (count) != (5):
            console.warn((((("Syllabifier problem: ") + (result)) + (".syllables was ")) + (count)) + (", expected 5"))
        assert (RiTa.isNoun(result) == True)
    def test_should_call_alliterations_numsyllables(self):
        result = RiTa.alliterations("cat", {"minLength": 1, "numSyllables": 7})
        assert (result == ["electrocardiogram", "electromechanical", "telecommunications"])
        i = 0
        for i in range(len(result)):
            assert ((RiTa.isAlliteration(result[i], "cat")) is True), ("FAIL2: ") + (result[i])
    def test_should_call_alliterations_pos(self):
        res = None
        res = RiTa.alliterations("cat", {"numSyllables": 7, "pos": "n"})
        assert (res == ["electrocardiogram", "telecommunications"])
        i = 0
        for i in range(len(res)):
            assert ((RiTa.isAlliteration(res[i], "cat")) is True), ("FAIL2: ") + (res[i])
        res = RiTa.alliterations("cat", {"minLength": 14, "pos": "v"})
        for r in res:
            assert (((len(r)) >= (14)) is True)
        assert (res == ["counterbalance"])
        res = RiTa.alliterations("dog", {"minLength": 13, "pos": "rb", "limit": 11})
        for r in res:
            assert (((len(r)) >= (13)) is True)
        assert (res == ["coincidentally", "conditionally", "confidentially", "contradictorily", "devastatingly", "expeditiously", "paradoxically", "predominantly", "traditionally", "unconditionally", "unpredictably"])
        res = RiTa.alliterations("freedom", {"minLength": 14, "pos": "nns"})
        for r in res:
            assert (((len(r)) >= (14)) is True)
        assert (res == ["featherbeddings", "fundamentalists", "pharmaceuticals", "photosyntheses", "reconfigurations", "sophistications"])
    def test_should_call_alliterations(self):
        result = None
        result = RiTa.alliterations("", {"silent": 1})
        assert (((len(result)) < (1)) is True)
        result = RiTa.alliterations("#$%^&*", {"silent": 1})
        assert (((len(result)) < (1)) is True)
        result = RiTa.alliterations("umbrella", {"silent": 1})
        assert (((len(result)) < (1)) is True), "failed on 'umbrella'"
        result = RiTa.alliterations("cat", {"limit": 100})
        assert (((len(result)) == (100)) is True), "failed on 'cat'"
        assert (("cat" in result) is False)
        i = 0
        for i in range(len(result)):
            assert ((RiTa.isAlliteration(result[i], "cat")) is True)
        result = RiTa.alliterations("dog", {"limit": 100})
        assert (("dog" in result) is False)
        assert (((len(result)) == (100)) is True), "failed on 'dog'"
        i = 0
        for i in range(len(result)):
            assert ((RiTa.isAlliteration(result[i], "dog")) is True)
        result = RiTa.alliterations("dog", {"minLength": 15})
        assert ((((len(result)) > (0)) and ((len(result)) < (5))) is True), ("got length=") + (len(result))
        i = 0
        for i in range(len(result)):
            assert ((RiTa.isAlliteration(result[i], "dog")) is True), ("FAIL1: ") + (result[i])
        result = RiTa.alliterations("cat", {"minLength": 16})
        assert ((((len(result)) > (0)) and ((len(result)) < (15))) is True), "failed on 'cat'"
        i = 0
        for i in range(len(result)):
            assert ((RiTa.isAlliteration(result[i], "cat")) is True), ("FAIL2: ") + (result[i])
        result = RiTa.alliterations("khatt", {"minLength": 16})
        assert ((((len(result)) > (0)) and ((len(result)) < (15))) is True), "failed on 'khatt'"
        i = 0
        for i in range(len(result)):
            assert ((RiTa.isAlliteration(result[i], "cat")) is True), ("FAIL2: ") + (result[i])
        assert (RiTa.alliterations("a") == [])
        assert (RiTa.alliterations("I") == [])
        assert (RiTa.alliterations("K") == [])
    def test_should_call_rhymessync(self):
        assert (RiTa.lexicon.rhymesSync("dog", {"limit": 1}) == ["cog"])
        assert (RiTa.lexicon.rhymesSync("dog", {"limit": 2}) == ["cog", "log"])
        assert (RiTa.lexicon.rhymesSync("dog") == ["cog", "log"])
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
        assert (("eight" in RiTa.rhymes("weight", {"limit": 1000})) is True)
        assert (("weight" in RiTa.rhymes("eight", {"limit": 1000})) is True)
        assert (("give" in RiTa.rhymes("sieve", {"limit": 1000})) is True)
        assert (("more" in RiTa.rhymes("shore", {"limit": 1000})) is True)
        assert (("sense" in RiTa.rhymes("tense", {"limit": 1000})) is True)
        assert (("fog" in RiTa.rhymes("bog")) is True)
        assert (("log" in RiTa.rhymes("dog")) is True)
        assert (RiTa.rhymes("a") == [])
        assert (RiTa.rhymes("I") == [])
        assert (RiTa.rhymes("Z") == [])
        assert (RiTa.rhymes("B") == [])
        assert (RiTa.rhymes("K") == [])
    def test_should_call_rhymes_pos(self):
        assert (("hat" in RiTa.rhymes("cat", {"pos": "v"})) is False)
        assert (("mellow" in RiTa.rhymes("yellow", {"pos": "a"})) is True)
        assert (("boy" in RiTa.rhymes("toy", {"pos": "n"})) is True)
        assert (("give" in RiTa.rhymes("sieve", {"pos": "n"})) is False)
        assert (("condense" in RiTa.rhymes("tense", {"pos": "v"})) is True)
        assert (("drab" in RiTa.rhymes("crab", {"pos": "n"})) is False)
        assert (("more" in RiTa.rhymes("shore", {"pos": "v"})) is False)
        assert (("house" in RiTa.rhymes("mouse", {"pos": "nn"})) is True)
        assert (("eight" in RiTa.rhymes("weight", {"pos": "vb"})) is False)
        assert (("weight" in RiTa.rhymes("eight", {"pos": "nn", "limit": 1000})) is True)
        assert (("polo" in RiTa.rhymes("apple", {"pos": "v"})) is False)
        assert (("these" in RiTa.rhymes("this", {"pos": "v"})) is False)
        assert (("house" in RiTa.rhymes("hose", {"pos": "v"})) is False)
        assert (("mellow" in RiTa.rhymes("sieve", {"pos": "v"})) is False)
        assert (("grab" in RiTa.rhymes("swag", {"pos": "v"})) is False)
        rhyme = RiTa.rhymes("spreads", {"pos": "vbz", "limit": 1000})
        assert (("discriminateds" in rhyme) is False)
        assert (("endeds" in rhyme) is False)
        assert (("finisheds" in rhyme) is False)
        assert (("reporteds" in rhyme) is False)
        assert (("proliferateds" in rhyme) is False)
        assert (("outpaceds" in rhyme) is False)
        assert (("liveds" in rhyme) is False)
        assert (("bit" in RiTa.rhymes("hit", {"pos": "vb"})) is False)
        assert (("bit" in RiTa.rhymes("hit", {"pos": "vbd"})) is True)
        assert (("broke" in RiTa.rhymes("stroke", {"pos": "vb"})) is False)
        assert (("broke" in RiTa.rhymes("stroke", {"pos": "vbd"})) is True)
        assert (("involved" in RiTa.rhymes("evolved", {"pos": "vb"})) is False)
        assert (("involved" in RiTa.rhymes("evolved", {"pos": "vbd"})) is True)
    def test_should_call_rhymes_pos_nid(self):
        rhymes = RiTa.rhymes("abated", {"pos": "vbd", "limit": 1000})
        assert (("allocated" in rhymes) is True)
        assert (("annihilated" in rhymes) is True)
        assert (("condensed" in rhymes) is False)
    def test_should_call_rhymes_numsyllables(self):
        assert (("hat" in RiTa.rhymes("cat", {"numSyllables": 1})) is True)
        assert (("hat" in RiTa.rhymes("cat", {"numSyllables": 2})) is False)
        assert (("hat" in RiTa.rhymes("cat", {"numSyllables": 3})) is False)
        assert (("mellow" in RiTa.rhymes("yellow", {"numSyllables": 2})) is True)
        assert (("mellow" in RiTa.rhymes("yellow", {"numSyllables": 3})) is False)
        rhymes = RiTa.rhymes("abated", {"numSyllables": 3})
        assert (("elated" in rhymes) is True)
        assert (("abated" in rhymes) is False)
        assert (("allocated" in rhymes) is False)
        assert (("condensed" in rhymes) is False)
    def test_should_call_rhymes_wordlength(self):
        assert (("hat" in RiTa.rhymes("cat", {"minLength": 4})) is False)
        assert (("hat" in RiTa.rhymes("cat", {"maxLength": 2})) is False)
        rhymes = RiTa.rhymes("abated", {"pos": "vbd", "maxLength": 9})
        assert (("allocated" in rhymes) is True)
        assert (("annihilated" in rhymes) is False)
        assert (("condensed" in rhymes) is False)
    def test_should_call_spellslike(self):
        result = None
        result = RiTa.spellsLike("")
        eql(result, [])
        result = RiTa.spellsLike("banana")
        eql(result, ["banal", "bonanza", "cabana", "manna"])
        result = RiTa.spellsLike("tornado")
        eql(result, ["torpedo"])
        result = RiTa.spellsLike("ice")
        eql(result, ["ace", "dice", "iced", "icy", "ire", "lice", "nice", "rice", "vice"])
    @pytest.mark.skip(reason="disabled in JS")  # /*LTR*/
    def test_should_call_spellslike_minlimit(self):
        result = None
        result = RiTa.spellsLike("")
        eql(result, [])
        result = RiTa.spellsLike("banana", {"minLimit": 5})
        eql(result, ["angina", "arena", "bacon", "balance", "ban"])
        result = RiTa.spellsLike("tornado", {"minLimit": 10})
        eql(result, ["condo", "forbade", "horned", "ornate", "thread", "tirade", "toad", "toenail", "tomato", "tonal"])
        result = RiTa.spellsLike("ice", {"minLimit": 4})
        eql(result, ["ace", "dice", "iced", "icy", "ire", "lice", "nice", "rice", "vice"])
    def test_should_call_spellslike_options(self):
        result = None
        result = RiTa.spellsLike("banana", {"minLength": 6, "maxLength": 6})
        eql(result, ["cabana"])
        result = RiTa.spellsLike("banana", {"minLength": 6, "maxLength": 6})
        eql(result, ["cabana"])
        result = RiTa.spellsLike("banana", {"minDistance": 1})
        eql(result, ["banal", "bonanza", "cabana", "manna"])
        result = RiTa.spellsLike("ice", {"maxLength": 3})
        eql(result, ["ace", "icy", "ire"])
        result = RiTa.spellsLike("ice", {"minDistance": 2, "minLength": 3, "maxLength": 3, "limit": 1000})
        for r in result:
            assert (((len(r)) == (3)) is True)
        assert (((len(result)) > (10)) is True)
        result = RiTa.spellsLike("ice", {"minDistance": 0, "minLength": 3, "maxLength": 3})
        eql(result, ["ace", "icy", "ire"])
        result = RiTa.spellsLike("ice", {"minLength": 3, "maxLength": 3})
        for r in result:
            assert (((len(r)) == (3)) is True)
        eql(result, ["ace", "icy", "ire"])
        result = RiTa.spellsLike("ice", {"minLength": 3, "maxLength": 3, "pos": "n"})
        for r in result:
            assert (((len(r)) == (3)) is True)
        eql(result, ["ace", "ire"])
        result = RiTa.spellsLike("ice", {"minLength": 4, "maxLength": 4, "pos": "v", "limit": 5})
        for r in result:
            assert (((len(r)) == (4)) is True)
        eql(result, ["ache", "bide", "bite", "cite", "dine"])
        result = RiTa.spellsLike("ice", {"minLength": 4, "maxLength": 4, "pos": "nns", "limit": 5})
        for r in result:
            assert (((len(r)) == (4)) is True)
        eql(result, ["dice", "rice"])
        result = RiTa.spellsLike("ice", {"minLength": 4, "maxLength": 4, "pos": "nns", "minDistance": 3, "limit": 5})
        for r in result:
            assert (((len(r)) == (4)) is True)
        eql(result, ["axes", "beef", "deer", "dibs", "fame"])
        result = RiTa.spellsLike("abated", {"pos": "vbd"})
        assert (("abetted" in result) is True)
        assert (("aborted" in result) is True)
        assert (("condensed" in result) is False)
        assert (("lived" in RiTa.spellsLike("lined", {"pos": "vb"})) is False)
        assert (("lived" in RiTa.spellsLike("lined", {"pos": "vbd"})) is True)
        assert (("led" in RiTa.spellsLike("let", {"pos": "vb"})) is False)
        assert (("led" in RiTa.spellsLike("let", {"pos": "vbd"})) is True)
        assert (("broke" in RiTa.spellsLike("brake", {"pos": "vb"})) is False)
        assert (("broke" in RiTa.spellsLike("brake", {"pos": "vbd"})) is True)
        assert (("oversaw" in RiTa.spellsLike("overseas", {"pos": "vb"})) is False)
        assert (("oversaw" in RiTa.spellsLike("overseas", {"pos": "vbd"})) is True)
        rhyme = RiTa.spellsLike("spreads", {"pos": "vbz", "limit": 1000})
        assert (("discriminateds" in rhyme) is False)
        assert (("endeds" in rhyme) is False)
        assert (("finisheds" in rhyme) is False)
        assert (("reporteds" in rhyme) is False)
        assert (("proliferateds" in rhyme) is False)
        assert (("outpaceds" in rhyme) is False)
        assert (("lived" in rhyme) is False)
    def test_should_call_soundslike(self):
        eql(RiTa.soundsLike("tornado", {"type": "sound"}), ["torpedo"])
        result = RiTa.soundsLike("try", {"limit": 20})
        answer = ["cry", "dry", "fry", "pry", "rye", "tie", "tray", "tree", "tribe", "tried", "tripe", "trite", "true", "wry"]
        eql(result, answer)
        result = RiTa.soundsLike("try", {"minDistance": 2, "limit": 20})
        assert (((len(result)) > (len(answer))) is True)
        result = RiTa.soundsLike("happy")
        eql(result, answer = ["happier", "hippie"])
        result = RiTa.soundsLike("happy", {"minDistance": 2})
        assert (((len(result)) > (len(answer))) is True)
        result = RiTa.soundsLike("cat", {"type": "sound"})
        eql(result, ["bat", "cab", "cache", "calf", "calve", "can", "can't", "cap", "cash", "cast"])
        result = RiTa.soundsLike("cat", {"type": "sound", "limit": 5})
        eql(result, ["bat", "cab", "cache", "calf", "calve"])
        result = RiTa.soundsLike("cat", {"type": "sound", "limit": 1000, "minLength": 2, "maxLength": 4})
        eql(result, ["at", "bat", "cab", "calf", "can", "cap", "cash", "cast", "chat", "coat", "cot", "curt", "cut", "fat", "hat", "kit", "kite", "mat", "matt", "pat", "rat", "sat", "that", "vat"])
        result = RiTa.soundsLike("cat", {"type": "sound", "minLength": 4, "maxLength": 5, "pos": "jj"})
        eql(result, answer = ["catty", "curt"])
        result = RiTa.soundsLike("cat", {"minDistance": 2})
        assert (((len(result)) > (len(answer))) is True)
    def test_should_call_soundslike_pos(self):
        result = RiTa.soundsLike("abated", {"pos": "vbd"})
        assert (("abetted" in result) is True)
        assert (("debated" in result) is True)
        assert (("condensed" in result) is False)
        assert (("built" in RiTa.soundsLike("build", {"pos": "vb", "limit": 1000})) is False)
        assert (("computerized" in RiTa.soundsLike("computerize", {"pos": "vb", "limit": 1000})) is False)
        assert (("concerned" in RiTa.soundsLike("concern", {"pos": "vb"})) is False)
        assert (("committed" in RiTa.soundsLike("commit", {"pos": "vb"})) is False)
        assert (("involved" in RiTa.soundsLike("involve", {"pos": "vb"})) is False)
        assert (("gained" in RiTa.soundsLike("grained", {"pos": "vb"})) is False)
        assert (("remade" in RiTa.soundsLike("premade", {"pos": "vbd"})) is True)
        assert (("discriminated" in RiTa.soundsLike("incriminate", {"pos": "vbd"})) is True)
        assert (("pinched" in RiTa.soundsLike("paunched", {"pos": "vbd"})) is True)
    def test_should_call_soundslike_matchspelling(self):
        result = None
        result = RiTa.soundsLike("try", {"matchSpelling": True})
        eql(result, ["cry", "dry", "fry", "pry", "tray"])
        result = RiTa.soundsLike("try", {"matchSpelling": True, "maxLength": 3})
        eql(result, ["cry", "dry", "fry", "pry", "wry"])
        result = RiTa.soundsLike("try", {"matchSpelling": True, "minLength": 4})
        eql(result, ["tray"])
        result = RiTa.soundsLike("try", {"matchSpelling": True, "limit": 3})
        eql(result, ["cry", "dry", "fry"])
        result = RiTa.soundsLike("daddy", {"matchSpelling": True})
        eql(result, ["dandy", "paddy"])
        result = RiTa.soundsLike("banana", {"matchSpelling": True})
        eql(result, ["bonanza"])
        result = RiTa.soundsLike("abated", {"pos": "vbd", "matchSpelling": True})
        assert (len(result) == 2)
        assert (("abetted" in result) is True)
        assert (("awaited" in result) is True)
    def test_should_call_isrhyme(self):
        assert ((not (RiTa.isRhyme("apple", "polo"))) is True)
        assert ((not (RiTa.isRhyme("this", "these"))) is True)
        assert ((RiTa.isRhyme("cat", "hat")) is True)
        assert ((RiTa.isRhyme("yellow", "mellow")) is True)
        assert ((RiTa.isRhyme("toy", "boy")) is True)
        assert ((RiTa.isRhyme("solo", "tomorrow")) is True)
        assert ((RiTa.isRhyme("tense", "sense")) is True)
        assert ((RiTa.isRhyme("crab", "drab")) is True)
        assert ((RiTa.isRhyme("shore", "more")) is True)
        assert ((not (RiTa.isRhyme("hose", "house"))) is True)
        assert ((not (RiTa.isRhyme("sieve", "mellow"))) is True)
        assert ((RiTa.isRhyme("mouse", "house")) is True)
        assert ((RiTa.isRhyme("yo", "bro")) is True)
        assert ((not (RiTa.isRhyme("swag", "grab"))) is True)
        assert ((not (RiTa.isRhyme("", ""))) is True)
        assert ((RiTa.isRhyme("weight", "eight")) is True)
        assert ((RiTa.isRhyme("eight", "weight")) is True)
        assert ((RiTa.isRhyme("abated", "debated")) is True)
        if (__typeof(NOLEX)) != ("undefined"):
            assert ((RiTa.isRhyme("sieve", "give")) is True)
    def test_should_call_isalliteration(self):
        assert ((RiTa.isAlliteration("knife", "gnat")) is True)
        assert ((RiTa.isAlliteration("knife", "naughty")) is True)
        assert ((RiTa.isAlliteration("sally", "silly")) is True)
        assert ((RiTa.isAlliteration("sea", "seven")) is True)
        assert ((RiTa.isAlliteration("silly", "seven")) is True)
        assert ((RiTa.isAlliteration("sea", "sally")) is True)
        assert ((RiTa.isAlliteration("big", "bad")) is True)
        assert ((RiTa.isAlliteration("bad", "big")) is True)
        assert ((RiTa.isAlliteration("BIG", "bad")) is True)
        assert ((RiTa.isAlliteration("big", "BAD")) is True)
        assert ((RiTa.isAlliteration("BIG", "BAD")) is True)
        assert ((not (RiTa.isAlliteration("", ""))) is True)
        assert ((not (RiTa.isAlliteration("wind", "withdraw"))) is True)
        assert ((not (RiTa.isAlliteration("solo", "tomorrow"))) is True)
        assert ((not (RiTa.isAlliteration("solo", "yoyo"))) is True)
        assert ((not (RiTa.isAlliteration("yoyo", "jojo"))) is True)
        assert ((not (RiTa.isAlliteration("cat", "access"))) is True)
        assert ((RiTa.isAlliteration("unsung", "sine")) is True)
        assert ((RiTa.isAlliteration("job", "gene")) is True)
        assert ((RiTa.isAlliteration("jeans", "gentle")) is True)
        assert ((RiTa.isAlliteration("abet", "better")) is True)
        assert ((RiTa.isAlliteration("never", "knight")) is True)
        assert ((RiTa.isAlliteration("knight", "navel")) is True)
        assert ((RiTa.isAlliteration("cat", "kitchen")) is True)
        assert ((not (RiTa.isAlliteration("octopus", "oblong"))) is True)
        assert ((not (RiTa.isAlliteration("omen", "open"))) is True)
        assert ((not (RiTa.isAlliteration("amicable", "atmosphere"))) is True)
        assert ((RiTa.isAlliteration("abated", "abetted")) is True)
        if (__typeof(NOLEX)) != ("undefined"):
            assert ((RiTa.isAlliteration("this", "these")) is True)
            assert ((RiTa.isAlliteration("psychology", "cholera")) is True)
            assert ((RiTa.isAlliteration("consult", "sultan")) is True)
            assert ((RiTa.isAlliteration("monsoon", "super")) is True)
    @pytest.mark.skip(reason="disabled in JS")  # /*LTR*/
    def test_should_call_findstem(self):
        lex = RiTa.lexicon
        assert (lex.findStem("chang") == "change")
        assert (lex.findStem("accid") == "accident")
        assert (lex.findStem("accept") == "accept")
        assert (lex.findStem("bear") == "bear")
        assert (lex.findStem("bodi") == "bodied")
        assert (lex.findStem("book") == "book")
        assert (lex.findStem("box") == "box")
        assert (lex.findStem("across") == "across")
        assert (lex.findStem("activ") == "active")
        assert (lex.findStem("adulter") == "adulterer")
        assert (lex.findStem("allianc") == "alliance")
        assert (lex.findStem("beautifi") == "beautify")
        assert (lex.findStem("bestsel") == "bestseller")
        assert (lex.findStem("blond") == "blond")
        assert (lex.findStem("borderlin") == "borderline")
        assert (lex.findStem("brave") == "brave")
        assert (lex.findStem("calor") == "caloric")
        assert (lex.findStem("central") == "central")
        assert (lex.findStem("certifi") == "certified")
        assert (lex.findStem("choppi") == "choppy")
        assert (lex.findStem("cigarett") == "cigarette")
        assert (lex.findStem("cogniz") == "cognizant")
        assert (lex.findStem("delicatessen") == "delicatessen")
        assert (lex.findStem("disaffect") == "disaffected")
        assert (lex.findStem("dog") == "dog")
        assert (lex.findStem("drachma") == "drachma")
        assert (lex.findStem("dualism") == "dualism")
        assert (lex.findStem("dwell") == "dwell")
        assert (lex.findStem("earthenwar") == "earthenware")
        assert (lex.findStem("efficaci") == "efficacious")
        assert (lex.findStem("elus") == "elusive")
        assert (lex.findStem("emiss") == "emission")
        assert (lex.findStem("environment") == "environmental")
        assert (lex.findStem("fisherman") == "fisherman")
        assert (lex.findStem("fragil") == "fragile")
        assert (lex.findStem("fundamentalist") == "fundamentalist")
        assert (lex.findStem("futil") == "futile")
        assert (lex.findStem("fuzz") == "fuzz")
        assert (lex.findStem("garag") == "garage")
        assert (lex.findStem("gass") == "gass")
        assert (lex.findStem("govern") == "govern")
        assert (lex.findStem("groov") == "groove")
        assert (lex.findStem("guttur") == "guttural")
        assert (lex.findStem("hamburg") == "hamburger")
        assert (lex.findStem("haphazard") == "haphazard")
        assert (lex.findStem("haunt") == "haunt")
        assert (lex.findStem("headlong") == "headlong")
        assert (lex.findStem("hubbub") == "hubbub")
        assert (lex.findStem("hungrili") == "hungrily")
        assert (lex.findStem("hypoglycem") == "hypoglycemic")
    @pytest.mark.skip(reason="disabled in JS")  # /*LTR*/
    def test_should_call_findstem_for_words_not_in_dict(self):
        assert (lex.findStem("abut") == None)
        assert (lex.findStem("airdrop") == None)
        assert (lex.findStem("waylay") == None)
        assert (lex.findStem("backslid") == None)
        assert (lex.findStem("bejewel") == None)
        assert (lex.findStem("blab") == None)
        assert (lex.findStem("brutifi") == None)
        assert (lex.findStem("bullwhip") == None)
        assert (lex.findStem("catnap") == None)
        assert (lex.findStem("clop") == None)
        assert (lex.findStem("verbifi") == None)
        assert (lex.findStem("dandifi") == None)
        assert (lex.findStem("declassifi") == None)
        assert (lex.findStem("disbar") == None)
        assert (lex.findStem("disint") == None)
        assert (lex.findStem("empanel") == None)
        assert (lex.findStem("fib") == None)
        assert (lex.findStem("flog") == None)
        assert (lex.findStem("ghostwritten") == None)
        assert (lex.findStem("glom") == None)
        assert (lex.findStem("hypertrophi") == None)
        assert (lex.findStem("interlaid") == None)
        assert (lex.findStem("jut") == None)
        assert (lex.findStem("miscarri") == None)
        assert (lex.findStem("mortifi") == None)
        assert (lex.findStem("overbid") == None)
        assert (lex.findStem("overgrow") == None)
        assert (lex.findStem("quickstep") == None)
        assert (lex.findStem("recommit") == None)
        assert (lex.findStem("rewound") == None)
        assert (lex.findStem("scram") == None)
        assert (lex.findStem("sightseen") == None)
        assert (lex.findStem("skydov") == None)
        assert (lex.findStem("unplug") == None)
        assert (lex.findStem("stencil") == None)
        assert (lex.findStem("spellbind") == None)
        assert (lex.findStem("subjectifi") == None)
        assert (lex.findStem("sup") == None)
        assert (lex.findStem("syllabifi") == None)
        assert (lex.findStem("snog") == None)
        assert (lex.findStem("unmak") == None)
        assert (lex.findStem("stupefi") == None)
        assert (lex.findStem("sulli") == None)
        assert (lex.findStem("tram") == None)
        assert (lex.findStem("underpay") == None)
        assert (lex.findStem("understudi") == None)
        assert (lex.findStem("unpin") == None)
        assert (lex.findStem("unzip") == None)
        assert (lex.findStem("whir") == None)
        assert (lex.findStem("yakk") == None)
        assert (lex.findStem("yap") == None)
        assert (lex.findStem("body") == None)
        assert (lex.findStem("justify") == None)
        assert (lex.findStem("cancelled") == None)
        assert (lex.findStem("trolling") == None)
        assert (lex.findStem("change") == None)
    def test_should_correctly_call_tophonearray(self):
        raw = RiTa.lexicon.rawPhones("tornado", False)
        result = RiTa.lexicon._toPhoneArray(raw)
        ans = ["t", "ao", "r", "n", "ey", "d", "ow"]
        assert (result == ans)
    # (helper hoisted to module scope)

