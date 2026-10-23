# AUTO-GENERATED from js/test/analyzer-tests.js by scripts/js-to-py-tests.js — do not edit by hand.
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

class TestAnalyzer:
    # (var hoisted to module scope)
    def test_should_call_analyzer_analyze(self):
        data = RiTa.analyzer.analyze("abandon")
        assert (data.phones == "ah-b-ae-n-d-ah-n")
        assert (data.stresses == "0/1/0")
        assert (data.syllables == "ah/b-ae-n/d-ah-n")
    def test_should_call_analyzeword(self):
        tmp = RiTa.SILENCE_LTS
        RiTa.SILENCE_LTS = True
        data = RiTa.analyzer.analyze_word("abandon")
        assert (data.phones == "ah-b-ae-n-d-ah-n")
        assert (data.stresses == "0/1/0")
        assert (data.syllables == "ah/b-ae-n/d-ah-n")
        data = RiTa.analyzer.analyze_word("z")
        assert (data.phones == "z")
        assert (data.stresses == "0")
        assert (data.syllables == "z")
        data = RiTa.analyzer.analyze_word("cloze")
        assert (data.phones == "k-l-ow-z")
        assert (data.stresses == "1")
        assert (data.syllables == "k-l-ow-z")
        RiTa.SILENCE_LTS = tmp
    def test_should_call_analyzeword_with_lts(self):
        if not (hasLex):
            pytest.skip("mocha this.skip")
        tmp = RiTa.SILENCE_LTS
        RiTa.SILENCE_LTS = True
        data = RiTa.analyzer.analyze_word("1903")
        assert (data.phones == "w-ah-n-n-ih-n-z-ih-r-ow-th-r-iy")
        assert (data.stresses == "0/0/0/0/0")
        assert (data.syllables == "w-ah-n/n-ih-n/z-ih/r-ow/th-r-iy")
        RiTa.SILENCE_LTS = tmp
    def test_should_call_analyze_lts(self):
        assert (RiTa.SILENCE_LTS == False)
        feats = None
        feats = RiTa.analyze("cloze", {"silent": 1})
        assert (feats.pos == "nn")
        assert (feats.tokens == "cloze")
        assert (feats.syllables == "k-l-ow-z")
    def test_should_call_syllables_lts(self):
        result = RiTa.syllables("The Laggin", {"silent": 1})
        assert (result == "dh-ah l-ae/g-ih-n")
    def test_should_call_analyze(self):
        assert (RiTa.analyze("") == {"tokens": "", "pos": "", "stresses": "", "phones": "", "syllables": ""})
        feats = None
        feats = RiTa.analyze("clothes")
        assert (feats.pos == "nns")
        assert (feats.tokens == "clothes")
        assert (feats.syllables == "k-l-ow-dh-z")
        feats = RiTa.analyze("chevrolet")
        assert (feats.tokens == "chevrolet")
        assert (feats.syllables == ("sh-eh-v/r-ow/l-ey") if (hasLex) else ("ch-eh-v/r-ow/l-ah-t"))
        if not (hasLex):
            return
        tmp = RiTa.SILENCE_LTS
        RiTa.SILENCE_LTS = True
        feats = RiTa.analyze("1903")
        assert (feats.phones == "w-ah-n-n-ih-n-z-ih-r-ow-th-r-iy")
        assert (feats.stresses == "0/0/0/0/0")
        assert (feats.syllables == "w-ah-n/n-ih-n/z-ih/r-ow/th-r-iy")
        assert (feats.tokens == "1903")
        assert (feats.pos == "cd")
        RiTa.SILENCE_LTS = tmp
        feats = RiTa.analyze("the clothes")
        assert (feats.pos == "dt nns")
        assert (feats.tokens == "the clothes")
        assert (feats.syllables == "dh-ah k-l-ow-dh-z")
        feats = RiTa.analyze("yoyo")
        assert (feats.pos == "nn")
        assert (feats.tokens == "yoyo")
        assert (feats.syllables == "y-ow/y-ow")
        feats = RiTa.analyze("abandon")
        eq(feats["pos"], "vb")
        eq(feats["phones"], "ah-b-ae-n-d-ah-n")
        eq(feats["tokens"], "abandon")
        eq(feats["stresses"], "0/1/0")
        eq(feats["syllables"], "ah/b-ae-n/d-ah-n")
        feats = RiTa.analyze("bit")
        assert (feats.pos == "vbd")
        assert (feats.syllables == "b-ih-t")
        feats = RiTa.analyze("It bit me.")
        assert (feats.pos == "prp vbd prp .")
        feats = RiTa.analyze("Give the duck a bit of bread.")
        assert (feats.pos == "vb dt nn dt nn in nn .")
        feats = RiTa.analyze("broke")
        assert (feats.pos == "vbd")
        assert (feats.syllables == "b-r-ow-k")
        feats = RiTa.analyze("I broke my leg.")
        assert (feats.pos == "prp vbd prp$ nn .")
        feats = RiTa.analyze("The show has ended.")
        assert (feats.pos == "dt nn vbz vbn .")
        feats = RiTa.analyze("She oversaw it.")
        assert (feats.pos == "prp vbd prp .")
        feats = RiTa.analyze("She remade this video.")
        assert (feats.pos == "prp vbd dt nn .")
        feats = RiTa.analyze("They will be remade into something else.")
        (0) and (expect(feats.pos).eq("prp md vb vbn in nn rb ."))
        feats = RiTa.analyze("She becomes a companion to a foreigner.")
        assert (feats.pos == "prp vbz dt nn to dt nn .")
        feats = RiTa.analyze("She has become a companion to a foreigner.")
        (0) and (expect(feats.pos).eq("prp vbz vbn dt jj to dt nn ."))
    def test_should_treat_hyphenated_words_as_single_tokens(self):
        lts = RiTa.SILENCE_LTS
        RiTa.SILENCE_LTS = True
        pool1 = ["mother-in-law", "father-in-law", "sister-in-law", "brother-in-law", "off-site", "up-to-date", "state-of-the-art", "self-esteem", "merry-go-round", "man-eating", "twenty-one", "twenty-first", "thirty-second", "happy-go-lucky", "editor-in-chief", "over-the-counter", "long-term", "high-speed", "in-depth", "full-length", "part-time", "sun-dried", "well-off", "well-known", "gift-wrap", "follow-up", "well-being", "good-looking", "knee-length", "runner-up", "tip-off", "blush-on", "sugar-free", "ice-cold", "far-flung", "high-rise", "life-size", "king-size", "next-door", "full-time", "forty-acre", "on-campus", "family-run", "low-grade", "round-trip"]
        feats1 = [{"pos": "nn", "tokens": "mother-in-law", "phones": "m-ah-dh-er-ih-n-l-ao", "stresses": "1/0-0-1", "syllables": "m-ah/dh-er/ih-n/l-ao"}, {"pos": "nn", "tokens": "father-in-law", "phones": "f-aa-dh-er-ih-n-l-ao", "stresses": "1/0-0-1", "syllables": "f-aa/dh-er/ih-n/l-ao"}, {"pos": "nn", "tokens": "sister-in-law", "phones": "s-ih-s-t-er-ih-n-l-ao", "stresses": "1/0-0-1", "syllables": "s-ih/s-t-er/ih-n/l-ao"}, {"pos": "nn", "tokens": "brother-in-law", "phones": "b-r-ah-dh-er-ih-n-l-ao", "stresses": "1/0-0-1", "syllables": "b-r-ah/dh-er/ih-n/l-ao"}, {"pos": "jj", "tokens": "off-site", "phones": "ao-f-s-ay-t", "stresses": "1-1", "syllables": "ao-f/s-ay-t"}, {"pos": "jj", "tokens": "up-to-date", "phones": "ah-p-t-uw-d-ey-t", "stresses": "1-1-1", "syllables": "ah-p/t-uw/d-ey-t"}, {"pos": "nn", "tokens": "state-of-the-art", "phones": "s-t-ey-t-ah-v-dh-ah-aa-r-t", "stresses": "1-1-0-1", "syllables": "s-t-ey-t/ah-v/dh-ah/aa-r-t"}, {"pos": "nn", "tokens": "self-esteem", "phones": "s-eh-l-f-ah-s-t-iy-m", "stresses": "1-0/1", "syllables": "s-eh-l-f/ah/s-t-iy-m"}, {"pos": "nn", "tokens": "merry-go-round", "phones": "m-eh-r-iy-g-ow-r-aw-n-d", "stresses": "1/0-1-1", "syllables": "m-eh/r-iy/g-ow/r-aw-n-d"}, {"pos": "jj", "tokens": "man-eating", "phones": "m-ae-n-iy-t-ih-ng", "stresses": "1-1/0", "syllables": "m-ae-n/iy/t-ih-ng"}, {"pos": "cd", "tokens": "twenty-one", "phones": "t-w-eh-n-t-iy-w-ah-n", "stresses": "1/0-1", "syllables": "t-w-eh-n/t-iy/w-ah-n"}, {"pos": "jj", "tokens": "twenty-first", "phones": "t-w-eh-n-t-iy-f-er-s-t", "stresses": "1/0-1", "syllables": "t-w-eh-n/t-iy/f-er-s-t"}, {"pos": "jj", "tokens": "thirty-second", "phones": "th-er-t-iy-s-eh-k-ah-n-d", "stresses": "1/0-1/0", "syllables": "th-er/t-iy/s-eh/k-ah-n-d"}, {"pos": "jj", "tokens": "happy-go-lucky", "phones": "hh-ae-p-iy-g-ow-l-ah-k-iy", "stresses": "1/0-1-1/0", "syllables": "hh-ae/p-iy/g-ow/l-ah/k-iy"}, {"pos": "nn", "tokens": "editor-in-chief", "phones": "eh-d-ah-t-er-ih-n-ch-iy-f", "stresses": "1/0/0-0-1", "syllables": "eh/d-ah/t-er/ih-n/ch-iy-f"}, {"pos": "jj", "tokens": "over-the-counter", "phones": "ow-v-er-dh-ah-k-aw-n-t-er", "stresses": "1/0-0-1/0", "syllables": "ow/v-er/dh-ah/k-aw-n/t-er"}, {"pos": "jj", "tokens": "long-term", "phones": "l-ao-ng-t-er-m", "stresses": "1-1", "syllables": "l-ao-ng/t-er-m"}, {"pos": "jj", "tokens": "high-speed", "phones": "hh-ay-s-p-iy-d", "stresses": "1-1", "syllables": "hh-ay/s-p-iy-d"}, {"pos": "jj", "tokens": "in-depth", "phones": "ih-n-d-eh-p-th", "stresses": "0-1", "syllables": "ih-n/d-eh-p-th"}, {"pos": "jj", "tokens": "full-length", "phones": "f-uh-l-l-eh-ng-k-th", "stresses": "1-1", "syllables": "f-uh-l/l-eh-ng-k-th"}, {"pos": "jj", "tokens": "part-time", "phones": "p-aa-r-t-t-ay-m", "stresses": "1-1", "syllables": "p-aa-r-t/t-ay-m"}, {"pos": "jj", "tokens": "sun-dried", "phones": "s-ah-n-d-r-ay-d", "stresses": "1-1", "syllables": "s-ah-n/d-r-ay-d"}, {"pos": "jj", "tokens": "well-off", "phones": "w-eh-l-ao-f", "stresses": "1-1", "syllables": "w-eh-l/ao-f"}, {"pos": "jj", "tokens": "well-known", "phones": "w-eh-l-n-ow-n", "stresses": "1-1", "syllables": "w-eh-l/n-ow-n"}, {"pos": "nn", "tokens": "gift-wrap", "phones": "g-ih-f-t-r-ae-p", "stresses": "1-1", "syllables": "g-ih-f-t/r-ae-p"}, {"pos": "nn", "tokens": "follow-up", "phones": "f-aa-l-ow-ah-p", "stresses": "1/0-1", "syllables": "f-aa/l-ow/ah-p"}, {"pos": "nn", "tokens": "well-being", "phones": "w-eh-l-b-iy-ih-ng", "stresses": "1-1/0", "syllables": "w-eh-l/b-iy/ih-ng"}, {"pos": "jj", "tokens": "good-looking", "phones": "g-uh-d-l-uh-k-ih-ng", "stresses": "1-1/0", "syllables": "g-uh-d/l-uh/k-ih-ng"}, {"pos": "jj", "tokens": "knee-length", "phones": "n-iy-l-eh-ng-k-th", "stresses": "1-1", "syllables": "n-iy/l-eh-ng-k-th"}, {"pos": "nn", "tokens": "runner-up", "phones": "r-ah-n-er-ah-p", "stresses": "1/0-1", "syllables": "r-ah/n-er/ah-p"}, {"pos": "nn", "tokens": "tip-off", "phones": "t-ih-p-ao-f", "stresses": "1-1", "syllables": "t-ih-p/ao-f"}, {"pos": "nn", "tokens": "blush-on", "phones": "b-l-ah-sh-aa-n", "stresses": "1-1", "syllables": "b-l-ah-sh/aa-n"}, {"pos": "jj", "tokens": "sugar-free", "phones": "sh-uh-g-er-f-r-iy", "stresses": "1/0-1", "syllables": "sh-uh/g-er/f-r-iy"}, {"pos": "jj", "tokens": "ice-cold", "phones": "ay-s-k-ow-l-d", "stresses": "1-1", "syllables": "ay-s/k-ow-l-d"}, {"pos": "jj", "tokens": "far-flung", "phones": "f-aa-r-f-l-ah-ng", "stresses": "1-1", "syllables": "f-aa-r/f-l-ah-ng"}, {"pos": "nn", "tokens": "high-rise", "phones": "hh-ay-r-ay-z", "stresses": "1-1", "syllables": "hh-ay/r-ay-z"}, {"pos": "jj", "tokens": "life-size", "phones": "l-ay-f-s-ay-z", "stresses": "1-1", "syllables": "l-ay-f/s-ay-z"}, {"pos": "jj", "tokens": "king-size", "phones": "k-ih-ng-s-ay-z", "stresses": "1-1", "syllables": "k-ih-ng/s-ay-z"}, {"pos": "jj", "tokens": "next-door", "phones": "n-eh-k-s-t-d-ao-r", "stresses": "1-1", "syllables": "n-eh-k-s-t/d-ao-r"}, {"pos": "jj", "tokens": "full-time", "phones": "f-uh-l-t-ay-m", "stresses": "1-1", "syllables": "f-uh-l/t-ay-m"}, {"pos": "jj", "tokens": "forty-acre", "phones": "f-ao-r-t-iy-ey-k-er", "stresses": "1/0-1/0", "syllables": "f-ao-r/t-iy/ey/k-er"}, {"pos": "jj", "tokens": "on-campus", "phones": "aa-n-k-ae-m-p-ah-s", "stresses": "1-1/0", "syllables": "aa-n/k-ae-m/p-ah-s"}, {"pos": "jj", "tokens": "family-run", "phones": "f-ae-m-ah-l-iy-r-ah-n", "stresses": "1/0/0-1", "syllables": "f-ae/m-ah/l-iy/r-ah-n"}, {"pos": "jj", "tokens": "low-grade", "phones": "l-ow-g-r-ey-d", "stresses": "1-1", "syllables": "l-ow/g-r-ey-d"}, {"pos": "jj", "tokens": "round-trip", "phones": "r-aw-n-d-t-r-ih-p", "stresses": "1-1", "syllables": "r-aw-n-d/t-r-ih-p"}]
        i = 0
        for i in range(len(pool1)):
            feats = RiTa.analyze(pool1[i])
            eq(feats.pos, feats1[i].pos, ("[pos]fail at ") + (pool1[i]))
            eq(feats.tokens, feats1[i].tokens, ("[tokens]fail at ") + (pool1[i]))
            eq(feats.phones, feats1[i].phones, ("[phones]fail at ") + (pool1[i]))
            eq(feats.stresses, feats1[i].stresses, ("[stresses]fail at ") + (pool1[i]))
            eq(feats.syllables, feats1[i].syllables, ("[syllables]fail at ") + (pool1[i]))
            eql(feats.tokens.split(" "), RiTa.tokenize(pool1[i]))
        pool2A = ["oft-cited", "deeply-nested", "empty-handed", "sergeant-at-arms", "left-handed", "long-haired", "breath-taking", "self-centered", "single-minded", "short-tempered", "one-sided", "warm-blooded", "cold-blooded", "bell-bottoms", "corn-fed", "able-bodied"]
        feats2A = [{"pos": "jj", "tokens": "oft-cited", "phones": "ao-f-t-s-ih-t-ah-d", "stresses": "1-1/0", "syllables": "ao-f-t/s-ih/t-ah-d"}, {"pos": "jj", "tokens": "deeply-nested", "phones": "d-iy-p-l-iy-n-eh-s-t-ah-d", "stresses": "1/0-1/0", "syllables": "d-iy-p/l-iy/n-eh/s-t-ah-d"}, {"pos": "jj", "tokens": "empty-handed", "phones": "eh-m-p-t-iy-hh-ae-n-d-ah-d", "stresses": "1/0-1/0", "syllables": "eh-m-p/t-iy/hh-ae-n/d-ah-d"}, {"pos": "nn", "tokens": "sergeant-at-arms", "phones": "s-aa-r-jh-ah-n-t-ae-t-aa-r-m-z", "stresses": "1/0-1-1", "syllables": "s-aa-r/jh-ah-n-t/ae-t/aa-r-m-z"}, {"pos": "jj", "tokens": "left-handed", "phones": "l-eh-f-t-hh-ae-n-d-ah-d", "stresses": "1-1/0", "syllables": "l-eh-f-t/hh-ae-n/d-ah-d"}, {"pos": "jj", "tokens": "long-haired", "phones": "l-ao-ng-hh-eh-r-d", "stresses": "1-1", "syllables": "l-ao-ng/hh-eh-r-d"}, {"pos": "jj", "tokens": "breath-taking", "phones": "b-r-eh-th-t-ey-k-ih-ng", "stresses": "1-1/0", "syllables": "b-r-eh-th/t-ey/k-ih-ng"}, {"pos": "jj", "tokens": "self-centered", "phones": "s-eh-l-f-s-eh-n-t-er-d", "stresses": "1-1/0", "syllables": "s-eh-l-f/s-eh-n/t-er-d"}, {"pos": "jj", "tokens": "single-minded", "phones": "s-ih-ng-g-ah-l-m-ay-n-d-ah-d", "stresses": "1/0-1/0", "syllables": "s-ih-ng/g-ah-l/m-ay-n/d-ah-d"}, {"pos": "jj", "tokens": "short-tempered", "phones": "sh-ao-r-t-t-eh-m-p-er-d", "stresses": "1-1/0", "syllables": "sh-ao-r-t/t-eh-m/p-er-d"}, {"pos": "jj", "tokens": "one-sided", "phones": "w-ah-n-s-ay-d-ah-d", "stresses": "1-1/0", "syllables": "w-ah-n/s-ay/d-ah-d"}, {"pos": "jj", "tokens": "warm-blooded", "phones": "w-ao-r-m-b-l-ah-d-ah-d", "stresses": "1-1/0", "syllables": "w-ao-r-m/b-l-ah/d-ah-d"}, {"pos": "jj", "tokens": "cold-blooded", "phones": "k-ow-l-d-b-l-ah-d-ah-d", "stresses": "1-1/0", "syllables": "k-ow-l-d/b-l-ah/d-ah-d"}, {"pos": "nn", "tokens": "bell-bottoms", "phones": "b-eh-l-b-aa-t-ah-m-z", "stresses": "1-1/0", "syllables": "b-eh-l/b-aa/t-ah-m-z"}, {"pos": "jj", "tokens": "corn-fed", "phones": "k-ao-r-n-f-eh-d", "stresses": "1-1", "syllables": "k-ao-r-n/f-eh-d"}, {"pos": "jj", "tokens": "able-bodied", "phones": "ey-b-ah-l-b-aa-d-iy-d", "stresses": "1/0-1/0", "syllables": "ey/b-ah-l/b-aa/d-iy-d"}]
        i = 0
        for i in range(len(pool2A)):
            feats = RiTa.analyze(pool2A[i])
            eq(feats.pos, feats2A[i].pos, ("[pos]fail at ") + (pool2A[i]))
            eq(feats.tokens, feats2A[i].tokens, ("[tokens]fail at ") + (pool2A[i]))
            eq(feats.phones, feats2A[i].phones, ("[phones]fail at ") + (pool2A[i]))
            eq(feats.stresses, feats2A[i].stresses, ("[stresses]fail at ") + (pool2A[i]))
            eq(feats.syllables, feats2A[i].syllables, ("[syllables]fail at ") + (pool2A[i]))
            eql(feats.tokens.split(" "), RiTa.tokenize(pool2A[i]))
        pool2B = ["de-emphasize", "re-apply", "ho-hum", "co-manage", "co-manager", "neo-liberalism", "u-turn", "x-ray", "a-frame", "high-tech", "nitty-gritty"]
        feats2B = [{"pos": "vb", "tokens": "de-emphasize", "phones": "d-ih-eh-m-f-ah-s-ay-z", "stresses": "0-1/0/0", "syllables": "d-ih/eh-m/f-ah/s-ay-z"}, {"pos": "vb", "tokens": "re-apply", "phones": "r-iy-ah-p-l-ay1", "stresses": "0-0/1", "syllables": "r-iy/ah/p-l-ay1"}, {"pos": "uh", "tokens": "ho-hum", "phones": "hh-ow-hh-ah-m", "stresses": "0-1", "syllables": "hh-ow/hh-ah-m"}, {"pos": "vb", "tokens": "co-manage", "phones": "k-ow-m-ae-n-ah-jh", "stresses": "0-1/0", "syllables": "k-ow/m-ae/n-ah-jh"}, {"pos": "nn", "tokens": "co-manager", "phones": "k-ow-m-ae-n-ah-jh-er", "stresses": "0-1/0/0", "syllables": "k-ow/m-ae/n-ah/jh-er"}, {"pos": "nn", "tokens": "neo-liberalism", "phones": "n-iy-ow-l-ih-b-er-ah-l-ih-z-ah-m", "stresses": "0/0-1/0/0/0/0", "syllables": "n-iy/ow/l-ih/b-er/ah/l-ih/z-ah-m"}, {"pos": "nn", "tokens": "u-turn", "phones": "y-uw-t-er-n", "stresses": "1-1", "syllables": "y-uw/t-er-n"}, {"pos": "nn", "tokens": "x-ray", "phones": "eh-k-z-r-ey", "stresses": "1-1", "syllables": "eh-k-z/r-ey"}, {"pos": "nn", "tokens": "a-frame", "phones": "ey-f-r-ey-m", "stresses": "1-1", "syllables": "ey/f-r-ey-m"}, {"pos": "jj", "tokens": "high-tech", "phones": "hh-ay-t-eh-k", "stresses": "1-1", "syllables": "hh-ay/t-eh-k"}, {"pos": "nn", "tokens": "nitty-gritty", "phones": "n-ih-t-iy-g-r-ih-t-iy", "stresses": "1/0-1/0", "syllables": "n-ih/t-iy/g-r-ih/t-iy"}]
        i = 0
        for i in range(len(pool2B)):
            feats = RiTa.analyze(pool2B[i])
            eq(feats.pos, feats2B[i].pos, ("[pos]fail at ") + (pool2B[i]))
            if pool2B[i] in ["de-emphasize", "re-apply", "u-turn", "x-ray"]:
                continue
            eq(feats.tokens, feats2B[i].tokens, ("[tokens]fail at ") + (pool2B[i]))
            eq(feats.phones, feats2B[i].phones, ("[phones]fail at ") + (pool2B[i]))
            eq(feats.stresses, feats2B[i].stresses, ("[stresses]fail at ") + (pool2B[i]))
            eq(feats.syllables, feats2B[i].syllables, ("[syllables]fail at ") + (pool2B[i]))
            eql(feats.tokens.split(" "), RiTa.tokenize(pool2B[i]))
        pool3 = ["co-op", "roly-poly", "topsy-turvy"]
        feats3 = [{"pos": "nn", "tokens": "co-op", "phones": "k-ow-ah-p", "stresses": "0-0", "syllables": "k-ow/ah-p"}, {"pos": "jj", "tokens": "roly-poly", "phones": "r-ow-l-iy-p-aa-l-iy", "stresses": "1/0-1/0", "syllables": "r-ow/l-iy/p-aa/l-iy"}, {"pos": "jj", "tokens": "topsy-turvy", "phones": "t-aa-p-s-iy-t-er-v-iy", "stresses": "1/0-1/0", "syllables": "t-aa-p/s-iy/t-er/v-iy"}]
        i = 0
        for i in range(len(pool3)):
            feats = RiTa.analyze(pool3[i])
            eq(feats.pos, feats3[i].pos, ("[pos]fail at ") + (pool3[i]))
            eq(feats.tokens, feats3[i].tokens, ("[tokens]fail at ") + (pool3[i]))
            eq(feats.phones, feats3[i].phones, ("[phones]fail at ") + (pool3[i]))
            eq(feats.stresses, feats3[i].stresses, ("[stresses]fail at ") + (pool3[i]))
            eq(feats.syllables, feats3[i].syllables, ("[syllables]fail at ") + (pool3[i]))
            eql(feats.tokens.split(" "), RiTa.tokenize(pool3[i]))
        RiTa.SILENCE_LTS = lts
    def test_should_handle_dashes(self):
        lts = RiTa.SILENCE_LTS
        RiTa.SILENCE_LTS = True
        sentence = "Teaching‒the profession has always appealed to me."
        feats = RiTa.analyze(sentence)
        eq(feats["pos"], "vbg ‒ dt nn vbz rb vbd to prp .")
        eq(feats["tokens"], "Teaching ‒ the profession has always appealed to me .")
        eql(feats["tokens"].split(" "), RiTa.tokenize(sentence))
        sentence = "The teacher assigned pages 101–181 for tonight's reading material. "
        feats = RiTa.analyze(sentence)
        eq(feats["pos"], "dt nn vbn nns cd – cd in nns vbg jj .")
        eq(feats["tokens"], "The teacher assigned pages 101 – 181 for tonight's reading material .")
        eql(feats["tokens"].split(" "), RiTa.tokenize(sentence))
        sentence = "Type two hyphens—without a space before, after, or between them."
        feats = RiTa.analyze(sentence)
        eq(feats["pos"], "nn cd nns — in dt nn in , in , cc in prp .")
        eq(feats["tokens"], "Type two hyphens — without a space before , after , or between them .")
        eql(feats["tokens"].split(" "), RiTa.tokenize(sentence))
        sentence = "Phones, hand-held computers, and built-in TVs—each a possible distraction—can lead to a dangerous situation if used while driving."
        feats = RiTa.analyze(sentence)
        eq(feats["pos"], "nns , jj nns , cc jj nnps — dt dt jj nn — md vb to dt jj nn in vbn in vbg .")
        eq(feats["tokens"], "Phones , hand-held computers , and built-in TVs — each a possible distraction — can lead to a dangerous situation if used while driving .")
        eql(feats["tokens"].split(" "), RiTa.tokenize(sentence))
        sentence = "He is afraid of two things--spiders and senior prom."
        feats = RiTa.analyze(sentence)
        eq(feats["pos"], "prp vbz jj in cd nns -- nns cc jj nn .")
        eq(feats["tokens"], "He is afraid of two things -- spiders and senior prom .")
        eql(feats["tokens"].split(" "), RiTa.tokenize(sentence))
        RiTa.SILENCE_LTS = lts
    def test_should_call_stresses(self):
        result = None
        answer = None
        word = None
        eq(RiTa.stresses(""), "")
        eq(RiTa.stresses("women"), "1/0", "women")
        if not (hasLex):
            return
        eq(RiTa.stresses("The emperor had no clothes on"), "0 1/0/0 1 1 1 1")
        eq(RiTa.stresses("The emperor had no clothes on."), "0 1/0/0 1 1 1 1 .")
        eq(RiTa.stresses("The emperor had no clothes on. The King is fat."), "0 1/0/0 1 1 1 1 . 0 1 1 1 .")
        word = "to present, to export, to decide, to begin"
        result = RiTa.stresses(word)
        answer = ("1 1/0 , 1 1/0 , 1 0/1 , 1 0/1") if (hasLex) else ("1 1/1 , 1 0/1 , 1 0/1 , 1 1/1")
        eq(result, answer, word)
        word = "The dog ran faster than the other dog.  But the other dog was prettier."
        result = RiTa.stresses(word)
        answer = "0 1 1 1/0 1 0 1/0 1 . 1 0 1/0 1 1 1/0/0 ."
        eq(result, answer, word)
        eq(RiTa.stresses("chevrolet"), ("0/0/1") if (hasLex) else ("1/0/0"), "chevrolet")
        eq(RiTa.stresses("genuine"), ("1/0/0") if (hasLex) else ("1/0/1"), "genuine")
        word = "to preSENT, to exPORT, to deCIDE, to beGIN"
        result = RiTa.stresses(word)
        answer = ("1 1/0 , 1 1/0 , 1 0/1 , 1 0/1") if (hasLex) else ("1 1/1 , 1 0/1 , 1 0/1 , 1 1/1")
        eq(result, answer, word)
    def test_should_call_phones(self):
        silent = RiTa.SILENCE_LTS
        RiTa.SILENCE_LTS = True
        result = None
        answer = None
        eq(RiTa.phones(""), "")
        eq(RiTa.phones("b"), "b")
        eq(RiTa.phones("B"), "b")
        eq(RiTa.phones("The"), "dh-ah")
        eq(RiTa.phones("The."), "dh-ah .")
        eq(RiTa.phones("flowers"), "f-l-aw-er-z")
        eq(RiTa.phones("mice"), "m-ay-s")
        eq(RiTa.phones("ant"), "ae-n-t")
        result = RiTa.phones("The boy jumped over the wild dog.")
        answer = ("dh-ah b-oy jh-ah-m-p-t ow-v-er dh-ah w-ay-l-d d-ao-g .") if (hasLex) else ("dh-ah b-oy jh-ah-m-p-t ow-v-er dh-ah w-ay-l-d d-aa-g .")
        eq(result, answer)
        result = RiTa.phones("The boy ran to the store.")
        answer = ("dh-ah b-oy r-ae-n t-uw dh-ah s-t-ao-r .") if (hasLex) else ("dh-ah b-oy r-ah-n t-ow dh-ah s-t-ao-r .")
        eq(result, answer)
        result = RiTa.phones("The dog ran faster than the other dog.  But the other dog was prettier.")
        answer = ("dh-ah d-ao-g r-ae-n f-ae-s-t-er dh-ae-n dh-ah ah-dh-er d-ao-g . b-ah-t dh-ah ah-dh-er d-ao-g w-aa-z p-r-ih-t-iy-er .") if (hasLex) else ("dh-ah d-aa-g r-ah-n f-ae-s-t-er th-ae-n dh-ah ah-dh-er d-aa-g . b-ah-t dh-ah ah-dh-er d-aa-g w-ah-z p-r-eh-t-iy-er .")
        eq(result, answer)
        eq(RiTa.phones("quiche"), ("k-iy-sh") if (hasLex) else ("k-w-ih-sh"))
        eq(RiTa.phones("said"), ("s-eh-d") if (hasLex) else ("s-ey-d"))
        eq(RiTa.phones("chevrolet"), ("sh-eh-v-r-ow-l-ey") if (hasLex) else ("ch-eh-v-r-ow-l-ah-t"))
        eq(RiTa.phones("women"), ("w-ih-m-eh-n") if (hasLex) else ("w-ow-m-eh-n"))
        eq(RiTa.phones("genuine"), ("jh-eh-n-y-uw-w-ah-n") if (hasLex) else ("jh-eh-n-y-ah-ay-n"))
        if not (hasLex):
            return
        assert (RiTa.phones("deforestations") == "d-ih-f-ao-r-ih-s-t-ey-sh-ah-n-z")
        assert (RiTa.phones("schizophrenias") == "s-k-ih-t-s-ah-f-r-iy-n-iy-ah-z")
        RiTa.SILENCE_LTS = silent
    def test_should_call_syllables(self):
        silent = RiTa.SILENCE_LTS
        RiTa.SILENCE_LTS = True
        assert (RiTa.syllables("") == "")
        assert (RiTa.syllables("clothes") == "k-l-ow-dh-z")
        assert (RiTa.syllables("1903") == ("w-ah-n/n-ih-n/z-ih/r-ow/th-r-iy") if (hasLex) else ("1903"))
        nums = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        i = 0
        for i in range(10):
            istr = (i) + ("")
            assert (RiTa.syllables(istr) == (RiTa.syllables(nums[i])) if (hasLex) else (istr))
        assert (RiTa.syllables("deforestations") == ("d-ih/f-ao/r-ih/s-t-ey/sh-ah-n-z") if (hasLex) else ("d-ah/f-ao-r/s-t-ey/sh-ah-n-z"))
        assert (RiTa.syllables("chevrolet") == ("sh-eh-v/r-ow/l-ey") if (hasLex) else ("ch-eh-v/r-ow/l-ah-t"))
        assert (RiTa.syllables("women") == ("w-ih/m-eh-n") if (hasLex) else ("w-ow/m-eh-n"))
        assert (RiTa.syllables("genuine") == ("jh-eh-n/y-uw/w-ah-n") if (hasLex) else ("jh-eh-n/y-ah/ay-n"))
        input = None
        expected = None
        input = "The emperor had no clothes on."
        expected = ("dh-ah eh-m/p-er/er hh-ae-d n-ow k-l-ow-dh-z aa-n .") if (hasLex) else ("dh-ah eh-m/p-er/er hh-ae-d n-ow k-l-ow-dh-z ah-n .")
        assert (RiTa.syllables(input) == expected)
        input = "The dog ran faster than the other dog. But the other dog was prettier."
        expected = ("dh-ah d-ao-g r-ae-n f-ae/s-t-er dh-ae-n dh-ah ah/dh-er d-ao-g . b-ah-t dh-ah ah/dh-er d-ao-g w-aa-z p-r-ih/t-iy/er .") if (hasLex) else ("dh-ah d-aa-g r-ah-n f-ae/s-t-er th-ae-n dh-ah ah/dh-er d-aa-g . b-ah-t dh-ah ah/dh-er d-aa-g w-ah-z p-r-eh/t-iy/er .")
        assert (RiTa.syllables(input) == expected)
        input = "The dog ran faster than the other dog. But the other dog was prettier."
        expected = ("dh-ah d-ao-g r-ae-n f-ae/s-t-er dh-ae-n dh-ah ah/dh-er d-ao-g . b-ah-t dh-ah ah/dh-er d-ao-g w-aa-z p-r-ih/t-iy/er .") if (hasLex) else ("dh-ah d-aa-g r-ah-n f-ae/s-t-er th-ae-n dh-ah ah/dh-er d-aa-g . b-ah-t dh-ah ah/dh-er d-aa-g w-ah-z p-r-eh/t-iy/er .")
        assert (RiTa.syllables(input) == expected)
        input = "The emperor had no clothes on."
        expected = ("dh-ah eh-m/p-er/er hh-ae-d n-ow k-l-ow-dh-z aa-n .") if (hasLex) else ("dh-ah eh-m/p-er/er hh-ae-d n-ow k-l-ow-dh-z ah-n .")
        assert (RiTa.syllables(input) == expected)
        RiTa.SILENCE_LTS = silent
    def test_should_pluralize_phrases(self):
        input = None
        expected = None
        input = "set of choice"
        expected = "set of choices"
        assert (RiTa.pluralize(input) == expected)
        input = "bag of chocolate"
        expected = "bag of chocolates"
        assert (RiTa.pluralize(input) == expected)
        input = "gaggle of goose"
        expected = "gaggle of geese"
        assert (RiTa.pluralize(input) == expected)
    def test_should_do_nothing_when_input_to_pluralize_is_already_plural(self):
        tests = ["tidings", "schnapps", "canvases", "censuses", "bonuses", "isthmuses", "thermoses", "circuses", "tongs", "emeriti"]
        for i, t in enumerate(tests):
            res = RiTa.pluralize(t, {"dbug": 0})
            if (res) != (t):
                console.error(((((i) + (") Fail: ")) + (t)) + (" -> ")) + (res))
            assert (RiTa.pluralize(t) == t)
    def test_should_return_true_for_already_plural_nouns(self):
        tests = ["tidings", "schnapps", "canvases", "censuses", "bonuses", "isthmuses", "thermoses", "circuses", "tongs", "emeriti"]
        for i, t in enumerate(tests):
            res = RiTa.inflector.is_plural(t, {"dbug": 0})
            if not (res):
                console.error(((((i) + (") Fail: ")) + (t)) + (" -> ")) + (res))
            assert ((res) is True)
    def test_should_handle_singular_nouns_in_tagger_alltags(self):
        if not (hasLex):
            pytest.skip("mocha this.skip")
        tests = ["tiding", "census", "bonus", "thermos", "circus"]
        for i, t in enumerate(tests):
            res = RiTa.tagger.all_tags(t, False)
            if not ("nn" in res):
                console.error(((((i) + (") Fail: ")) + (t)) + (" -> ")) + (json.dumps(res)))
            assert (("nn" in res) is True)
    def test_should_handle_number_singular_plural(self):
        assert (RiTa.inflector.is_plural("dreariness", {"dbug": 0}) == True)
        assert (RiTa.singularize() == "")
        assert (RiTa.singularize("") == "")
        with pytest.raises(Exception):
            RiTa.singularize([1])
        with pytest.raises(Exception):
            RiTa.singularize(1)
        assert (RiTa.pluralize() == "")
        assert (RiTa.pluralize("") == "")
        with pytest.raises(Exception):
            RiTa.pluralize([1])
        with pytest.raises(Exception):
            RiTa.pluralize(1)
        testPairs = ["abysses", "abyss", "knives", "knife", "dazes", "daze", "hives", "hive", "dives", "dive", "octopuses", "octopus", "abalone", "abalone", "wildlife", "wildlife", "minutiae", "minutia", "spoofs", "spoof", "proofs", "proof", "roofs", "roof", "disbeliefs", "disbelief", "beliefs", "belief", "indices", "index", "accomplices", "accomplice", "prognoses", "prognosis", "taxis", "taxi", "chiefs", "chief", "monarchs", "monarch", "lochs", "loch", "stomachs", "stomach", "Chinese", "Chinese", "people", "person", "humans", "human", "germans", "german", "romans", "roman", "memoranda", "memorandum", "data", "datum", "geese", "goose", "femurs", "femur", "appendices", "appendix", "theses", "thesis", "alumni", "alumnus", "solos", "solo", "music", "music", "oxen", "ox", "money", "money", "beef", "beef", "tobacco", "tobacco", "cargo", "cargo", "golf", "golf", "grief", "grief", "cakes", "cake", "tomatoes", "tomato", "photos", "photo", "smallpox", "smallpox", "toes", "toe", "mice", "mouse", "lice", "louse", "children", "child", "gases", "gas", "buses", "bus", "happiness", "happiness", "apotheoses", "apotheosis", "stimuli", "stimulus", "dogs", "dog", "feet", "foot", "teeth", "tooth", "deer", "deer", "sheep", "sheep", "shrimp", "shrimp", "men", "man", "women", "woman", "congressmen", "congressman", "aldermen", "alderman", "freshmen", "freshman", "firemen", "fireman", "grandchildren", "grandchild", "menus", "menu", "gurus", "guru", "hardness", "hardness", "fish", "fish", "ooze", "ooze", "enterprises", "enterprise", "treatises", "treatise", "houses", "house", "chemises", "chemise", "aquatics", "aquatics", "mechanics", "mechanics", "quarters", "quarter", "motifs", "motif", "turf", "turf", "macaroni", "macaroni", "spaghetti", "spaghetti", "potpourri", "potpourri", "electrolysis", "electrolysis", "series", "series", "crises", "crisis", "corpora", "corpus", "shortness", "shortness", "dreariness", "dreariness", "unwillingness", "unwillingness", "moose", "moose", "lives", "life", "additives", "additive", "epochs", "epoch", "ranchs", "ranch", "alcoves", "alcove", "memories", "memory", "grooves", "groove", "universes", "universe", "toothbrushes", "toothbrush", "clashes", "clash", "addresses", "address", "flashes", "flash", "conclaves", "conclave", "promises", "promise", "spouses", "spouse", "branches", "branch", "lapses", "lapse", "quizes", "quiz", "spyglasses", "spyglass", "overpasses", "overpass", "clones", "clones", "microwaves", "microwave", "hypotheses", "hypothesis", "pretenses", "pretense", "latches", "latch", "fetuses", "fetus", "lighthouses", "lighthouse", "genuses", "genus", "zombies", "zombie", "hearses", "hearse", "trenches", "trench", "paradoxes", "paradox", "hippies", "hippie", "yuppies", "yuppie", "purses", "purse", "hatches", "hatch", "witches", "witch", "sinuses", "sinus", "phrases", "phrase", "arches", "arch", "duplexes", "duplex", "missives", "missive", "madhouses", "madhouse", "pauses", "pause", "heroes", "hero", "sketches", "sketch", "meshes", "mesh", "brasses", "brass", "marshes", "marsh", "masses", "mass", "impulses", "impulse", "pelvises", "pelvis", "fetishes", "fetish", "gashes", "gash", "directives", "directive", "calories", "calorie", "moves", "move", "expanses", "expanse", "briefcases", "briefcase", "media", "medium", "millennia", "millennium", "consortia", "consortium", "concerti", "concerto", "septa", "septum", "termini", "terminus", "larvae", "larva", "vertebrae", "vertebra", "memorabilia", "memorabilium", "hooves", "hoof", "thieves", "thief", "rabbis", "rabbi", "flu", "flu", "safaris", "safari", "sheaves", "sheaf", "uses", "use", "pinches", "pinch", "catharses", "catharsis", "hankies", "hanky", "whizzes", "whiz", "selves", "self", "bookshelves", "bookshelf", "wheezes", "wheeze", "diagnoses", "diagnosis", "blondes", "blonde", "eyes", "eye", "swine", "swine", "cognoscenti", "cognoscenti", "bonsai", "bonsai", "rice", "rice", "clothes", "clothes", "goddesses", "goddess", "tresses", "tress", "murderesses", "murderess", "kisses", "kiss"]
        res1 = None
        res2 = None
        res3 = None
        res4 = None
        Util = RiTa.Util
        dbug = 0
        i = 0
        for i in range(len(testPairs)):
            (dbug) and (console.log(((testPairs[i]) + ("/")) + (testPairs[(i) + (1)])))
            plural = testPairs[i]
            singular = testPairs[(i) + (1)]
            res1 = RiTa.singularize(plural, {"dbug": dbug})
            res2 = RiTa.pluralize(singular, {"dbug": dbug})
            res3 = RiTa.inflector.is_plural(plural, {"dbug": dbug})
            res4 = RiTa.inflector.is_plural(singular, {"dbug": dbug})
            assert (res1 == singular)
            assert (res2 == plural)
            assert (res3 == True)
            isMass = singular.lower() in RiTa.MASS_NOUNS
            isModal = singular.endswith(_jsstr("ness"))
            if (not (isMass)) and (not (isModal)):
                assert (res4 == False)
    def test_should_call_phonestostress(self):
        assert (RiTa.analyzer.phones_to_stress() == None)
        assert (RiTa.analyzer.phones_to_stress(" ") == "")
        assert (RiTa.analyzer.phones_to_stress("ah b-ae1-n d-ah-n") == "0/1/0")
    def test_should_not_pluralize_singularize_uncountables(self):
        assert (RiTa.pluralize("honey") == "honey")
        assert (RiTa.pluralize("pasta") == "pasta")
        assert (RiTa.pluralize("advice") == "advice")
        assert (RiTa.pluralize("fanfare") == "fanfare")
        assert (RiTa.pluralize("medicare") == "medicare")
        assert (RiTa.pluralize("childcare") == "childcare")
        assert (RiTa.singularize("honey") == "honey")
        assert (RiTa.singularize("pasta") == "pasta")
        assert (RiTa.singularize("advice") == "advice")
        assert (RiTa.singularize("fanfare") == "fanfare")
        assert (RiTa.singularize("medicare") == "medicare")
        assert (RiTa.singularize("childcare") == "childcare")
    def test_should_call_isplural(self):
        assert (RiTa.inflector.is_plural() == False)
        assert (RiTa.inflector.is_plural("") == False)
        assert (RiTa.inflector.is_plural("octopus", {"dbug": 0}) == False)
        assert (RiTa.inflector.is_plural("sheep") == True)
        assert (RiTa.inflector.is_plural("apples") == True)
        assert (RiTa.inflector.is_plural("leaves", {"debug": False}) == True)
        assert (RiTa.inflector.is_plural("feet", {"debug": False}) == True)
        assert (RiTa.inflector.is_plural("beaux", {"debug": False}) == False)
        assert (RiTa.inflector.is_plural("child", {"debug": False}) == False)
        assert (RiTa.inflector.is_plural("abbots", {"debug": False}) == True)
        assert (RiTa.inflector.is_plural("happiness") == True)
        assert (RiTa.inflector.is_plural("pasta") == True)
        assert (RiTa.inflector.is_plural("honey") == True)
        assert (RiTa.inflector.is_plural("fanfare") == True)
        assert (RiTa.inflector.is_plural("medicare") == True)
        assert (RiTa.inflector.is_plural("childcare") == True)
    def test_should_call_computephones(self):
        assert (RiTa.analyzer.compute_phones("leo") == ["l", "iy", "ow"])
        assert (RiTa.analyzer.compute_phones() == None)
        assert (RiTa.analyzer.compute_phones(".") == None)
        assert (RiTa.analyzer.compute_phones("") == None)
        assert (RiTa.analyzer.compute_phones(",") == None)
        assert (RiTa.analyzer.compute_phones("你好", {"silent": True}) == None)
        assert (RiTa.analyzer.compute_phones("Künste", {"silent": True}) == None)
        assert (RiTa.analyzer.compute_phones("leo", {"silent": True}) == ["l", "iy", "ow"])
        assert (RiTa.analyzer.compute_phones("student's") == ["s", "t", "uw1", "d", "eh1", "n", "t", "z"])
        assert (RiTa.analyzer.compute_phones("-1", {"silent": True}) == None)
        if not (hasLex):
            return
        assert (RiTa.analyzer.compute_phones("1") == ["w", "ah", "n"])
        assert (RiTa.analyzer.compute_phones("50") == ["f", "ay", "v", "z", "ih", "r", "ow"])
    def test_should_call_analyze_with_ipaphones_option(self):
        feats = RiTa.analyze("", {"ipaPhones": True})
        assert (feats.phones == "")
        feats = RiTa.analyze("cat", {"ipaPhones": True})
        assert (feats.phones == "kæt")
        assert (feats.syllables == "k-ae-t")
        assert (feats.stresses == "1")
        feats = RiTa.analyze("abandon", {"ipaPhones": True})
        assert (feats.phones == "əˈbændən")
        feats = RiTa.analyze("the", {"ipaPhones": True})
        assert (feats.phones == "ðə")
        feats = RiTa.analyze("The birch canoe slid on the smooth planks", {"ipaPhones": True})
        assert (feats.phones == "ðə bɜrtʃ kəˈnuː slɪd ɑːn ðə smuːð plæŋkz")
        feats = RiTa.analyze("The dog ran.", {"ipaPhones": True})
        assert (feats.phones == "ðə dɔːɡ ɹæn")
        feats = RiTa.analyze("abandon")
        assert (feats.phones == "ah-b-ae-n-d-ah-n")
        feats = RiTa.analyze("abandon", {"ipaPhones": False})
        assert (feats.phones == "ah-b-ae-n-d-ah-n")
    def test_should_call_phones_with_ipaphones_option(self):
        assert (RiTa.phones("", {"ipaPhones": True}) == "")
        assert (RiTa.phones("cat", {"ipaPhones": True}) == "kæt")
        assert (RiTa.phones("abandon", {"ipaPhones": True}) == "əˈbændən")
        assert (RiTa.phones("the", {"ipaPhones": True}) == "ðə")
        assert (RiTa.phones("The birch canoe slid on the smooth planks", {"ipaPhones": True}) == "ðə bɜrtʃ kəˈnuː slɪd ɑːn ðə smuːð plæŋkz")
        assert (RiTa.phones("abandon") == "ah-b-ae-n-d-ah-n")
        assert (RiTa.phones("abandon", {"ipaPhones": False}) == "ah-b-ae-n-d-ah-n")
    def test_should_call_syllables_with_ipaphones_option(self):
        assert (RiTa.syllables("abandon", {"ipaPhones": True}) == "ə/ˈbæn/dən")
        assert (RiTa.syllables("the", {"ipaPhones": True}) == "ðə")
        assert (RiTa.syllables("The birch canoe slid on the smooth planks", {"ipaPhones": True}) == "ðə bɜrtʃ kə/ˈnuː slɪd ɑːn ðə smuːð plæŋkz")
        assert (RiTa.syllables("The dog ran.", {"ipaPhones": True}) == "ðə dɔːɡ ɹæn")
        assert (RiTa.syllables("abandon") == "ah/b-ae-n/d-ah-n")
    # (helper hoisted to module scope)
    # (helper hoisted to module scope)
    # (helper hoisted to module scope)

hasLex = True

def ok(a=None, m=None, *args):
    assert ((a) is True), m

def eq(a=None, b=None, m=None, *args):
    assert (a == b)

def eql(a=None, b=None, m=None, *args):
    assert (a == b)

def _fn_1(*args):
    RiTa.singularize([1])

def _fn_2(*args):
    RiTa.singularize(1)

def _fn_3(*args):
    RiTa.pluralize([1])

def _fn_4(*args):
    RiTa.pluralize(1)

