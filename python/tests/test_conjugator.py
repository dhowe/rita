# AUTO-GENERATED from js/test/conjugator-tests.js by scripts/js-to-py-tests.js — do not edit by hand.
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

hasLex = True

class TestConjugator:
    def test_should_call_pastpart(self):
        assert (RiTa.past_part("pen") == "penned")
        assert (RiTa.past_part("red") == "red")
        assert (RiTa.past_part("sleep") == "slept")
        assert (RiTa.past_part("withhold") == "withheld")
        assert (RiTa.past_part("cut") == "cut")
        assert (RiTa.past_part("go") == "gone")
        assert (RiTa.past_part("swim") == "swum")
        assert (RiTa.past_part("would") == "would")
        assert (RiTa.past_part("might") == "might")
        assert (RiTa.past_part("run") == "run")
        assert (RiTa.past_part("speak") == "spoken")
        assert (RiTa.past_part("break") == "broken")
        assert (RiTa.past_part("plead") == "pled")
        assert (RiTa.past_part("") == "")
        assert (RiTa.past_part("shrink") == "shrunk")
        assert (RiTa.past_part("stink") == "stunk")
        assert (RiTa.past_part("study") == "studied")
        assert (RiTa.past_part("bite") == "bitten")
        assert (RiTa.past_part("break") == "broken")
        assert (RiTa.past_part("call") == "called")
        assert (RiTa.past_part("commit") == "committed")
        assert (RiTa.past_part("computerize") == "computerized")
        assert (RiTa.past_part("concern") == "concerned")
        assert (RiTa.past_part("discriminate") == "discriminated")
        assert (RiTa.past_part("end") == "ended")
        assert (RiTa.past_part("expect") == "expected")
        assert (RiTa.past_part("finish") == "finished")
        assert (RiTa.past_part("gain") == "gained")
        assert (RiTa.past_part("get") == "gotten")
        assert (RiTa.past_part("increase") == "increased")
        assert (RiTa.past_part("involve") == "involved")
        assert (RiTa.past_part("launch") == "launched")
        assert (RiTa.past_part("lead") == "led")
        assert (RiTa.past_part("live") == "lived")
        assert (RiTa.past_part("outpace") == "outpaced")
        assert (RiTa.past_part("oversee") == "overseen")
        assert (RiTa.past_part("oversell") == "oversold")
        assert (RiTa.past_part("pale") == "paled")
        assert (RiTa.past_part("prepay") == "prepaid")
        assert (RiTa.past_part("pressure") == "pressured")
        assert (RiTa.past_part("proliferate") == "proliferated")
        assert (RiTa.past_part("remake") == "remade")
        assert (RiTa.past_part("reopen") == "reopened")
        assert (RiTa.past_part("report") == "reported")
        assert (RiTa.past_part("resell") == "resold")
        assert (RiTa.past_part("settle") == "settled")
        assert (RiTa.past_part("bite") == "bitten")
        assert (RiTa.past_part("break") == "broken")
        assert (RiTa.past_part("build") == "built")
        assert (RiTa.past_part("enter") == "entered")
        assert (RiTa.past_part("own") == "owned")
        assert (RiTa.past_part("plan") == "planned")
        assert (RiTa.past_part("rent") == "rented")
        assert (RiTa.past_part("repurchase") == "repurchased")
        assert (RiTa.past_part("roast") == "roasted")
        assert (RiTa.past_part("start") == "started")
        assert (RiTa.past_part("bust") == "busted")
        assert (RiTa.past_part("heart") == "hearted")
        assert (RiTa.past_part("closet") == "closeted")
        assert (RiTa.past_part("bear") == "borne")
        if hasLex:
            assert (RiTa.past_part("hopped") == "hopped")
            assert (RiTa.past_part("hated") == "hated")
            assert (RiTa.past_part("created") == "created")
            assert (RiTa.past_part("committed") == "committed")
            assert (RiTa.past_part("submitted") == "submitted")
            assert (RiTa.past_part("come") == "come")
            assert (RiTa.past_part("forgotten") == "forgotten")
            assert (RiTa.past_part("arisen") == "arisen")
            assert (RiTa.past_part("eaten") == "eaten")
            assert (RiTa.past_part("chosen") == "chosen")
            assert (RiTa.past_part("frozen") == "frozen")
            assert (RiTa.past_part("stolen") == "stolen")
            assert (RiTa.past_part("worn") == "worn")
            assert (RiTa.past_part("broken") == "broken")
            assert (RiTa.past_part("written") == "written")
            assert (RiTa.past_part("ridden") == "ridden")
            assert (RiTa.past_part("drawn") == "drawn")
            assert (RiTa.past_part("known") == "known")
            assert (RiTa.past_part("grown") == "grown")
            assert (RiTa.past_part("done") == "done")
            assert (RiTa.past_part("gone") == "gone")
            assert (RiTa.past_part("awake") == "awoken")
            assert (RiTa.past_part("become") == "become")
            assert (RiTa.past_part("drink") == "drunk")
            assert (RiTa.past_part("run") == "run")
            assert (RiTa.past_part("shine") == "shone")
            assert (RiTa.past_part("grown") == "grown")
            assert (RiTa.past_part("heard") == "heard")
    def test_should_call_presentpart(self):
        assert (RiTa.present_part("") == "")
        assert (RiTa.present_part("sleep") == "sleeping")
        assert (RiTa.present_part("withhold") == "withholding")
        assert (RiTa.present_part("cut") == "cutting")
        assert (RiTa.present_part("go") == "going")
        assert (RiTa.present_part("run") == "running")
        assert (RiTa.present_part("speak") == "speaking")
        assert (RiTa.present_part("break") == "breaking")
        assert (RiTa.present_part("become") == "becoming")
        assert (RiTa.present_part("plead") == "pleading")
        assert (RiTa.present_part("awake") == "awaking")
        assert (RiTa.present_part("study") == "studying")
        assert (RiTa.present_part("lie") == "lying")
        assert (RiTa.present_part("swim") == "swimming")
        assert (RiTa.present_part("run") == "running")
        assert (RiTa.present_part("dig") == "digging")
        assert (RiTa.present_part("set") == "setting")
        assert (RiTa.present_part("speak") == "speaking")
        assert (RiTa.present_part("bring") == "bringing")
        assert (RiTa.present_part("speak") == "speaking")
        assert (RiTa.present_part("study ") == "studying")
        assert (RiTa.present_part(" study") == "studying")
        assert (RiTa.present_part("hoe") == "hoeing")
        assert (RiTa.present_part("shoe") == "shoeing")
        if hasLex:
            assert (RiTa.past_part("awake") == "awoken")
            assert (RiTa.past_part("become") == "become")
            assert (RiTa.past_part("drink") == "drunk")
            assert (RiTa.past_part("run") == "run")
            assert (RiTa.past_part("shine") == "shone")
    def test_should_conjugate_vbds(self):
        if not (hasLex):
            pytest.skip("mocha this.skip")
        assert (RiTa.conjugate("go", JsDict({"number": RiTa.SINGULAR, "person": RiTa.FIRST, "tense": RiTa.PAST})) == "went")
        assert (RiTa.conjugate("run", JsDict({"number": RiTa.SINGULAR, "person": RiTa.FIRST, "tense": RiTa.PAST})) == "ran")
    def test_should_call_conjugate(self):
        if not (hasLex):
            pytest.skip("mocha this.skip")
        args = None
        s = None
        a = None
        c = None
        assert (RiTa.conjugate("walk") == "walk")
        with pytest.raises(Exception):
            RiTa.conjugate()
        with pytest.raises(Exception):
            RiTa.conjugate("")
        assert ("swum" == RiTa.past_part("swim"))
        assert (RiTa.conjugate("be", JsDict({"form": RiTa.GERUND})) == "being")
        assert (RiTa.conjugate("are", JsDict({"number": RiTa.PLURAL, "person": RiTa.SECOND, "tense": RiTa.PAST})) == "were")
        s = ["swim", "need", "open"]
        a = ["swims", "needs", "opens"]
        args = JsDict({"tense": RiTa.PRESENT, "number": RiTa.SINGULAR, "person": RiTa.THIRD})
        with pytest.raises(Exception):
            return RiTa.conjugate(args)
        with pytest.raises(Exception):
            return RiTa.conjugate("", args)
        i = 0
        for i in range(0, len(s), 1):
            c = RiTa.conjugate(s[i], args)
            assert (c == a[i])
        args = JsDict({"tense": RiTa.PRESENT, "number": RiTa.SINGULAR, "person": RiTa.THIRD, "passive": True})
        a = ["is swum", "is needed", "is opened"]
        i = 0
        for i in range(0, len(s), 1):
            assert (RiTa.conjugate(s[i], args) == a[i])
        args = JsDict({"number": RiTa.SINGULAR, "person": RiTa.FIRST, "tense": RiTa.PAST})
        assert (RiTa.conjugate("swim", args) == "swam")
        s = ["swim", "need", "open"]
        a = ["swam", "needed", "opened"]
        assert (((len(a)) == (len(s))) is True)
        i = 0
        for i in range(0, len(s), 1):
            c = RiTa.conjugate(s[i], args)
            assert (c == a[i])
        args = JsDict({"number": RiTa.PLURAL, "person": RiTa.SECOND, "tense": RiTa.PAST})
        a = ["swam", "needed", "opened"]
        assert (((len(a)) == (len(s))) is True)
        i = 0
        for i in range(0, len(s), 1):
            assert (RiTa.conjugate(s[i], args) == a[i])
        args = JsDict({"number": RiTa.PLURAL, "person": RiTa.SECOND, "tense": RiTa.FUTURE})
        a = ["will swim", "will need", "will open"]
        assert (((len(a)) == (len(s))) is True)
        i = 0
        for i in range(0, len(s), 1):
            assert (RiTa.conjugate(s[i], args) == a[i])
        args = JsDict({"tense": RiTa.PAST, "number": RiTa.SINGULAR, "person": RiTa.THIRD})
        a = ["swam", "needed", "opened"]
        assert (((len(a)) == (len(s))) is True)
        i = 0
        for i in range(0, len(s), 1):
            c = RiTa.conjugate(s[i], args)
            assert (c == a[i])
        args = JsDict({"tense": RiTa.PAST, "number": RiTa.SINGULAR, "person": RiTa.THIRD, "form": RiTa.INFINITIVE})
        a = ["to swim", "to need", "to open"]
        assert (((len(a)) == (len(s))) is True)
        i = 0
        for i in range(0, len(s), 1):
            c = RiTa.conjugate(s[i], args)
            assert (c == a[i])
        args = JsDict({"tense": RiTa.PAST, "number": RiTa.SINGULAR, "person": RiTa.THIRD, "passive": True})
        s = ["scorch", "burn", "hit"]
        a = ["was scorched", "was burned", "was hit"]
        assert (((len(a)) == (len(s))) is True)
        i = 0
        for i in range(0, len(s), 1):
            c = RiTa.conjugate(s[i], args)
            assert (c == a[i])
        s = ["swim", "need", "open"]
        args = JsDict({"tense": RiTa.PRESENT, "number": RiTa.SINGULAR, "person": RiTa.THIRD, "form": RiTa.INFINITIVE, "progressive": True})
        a = ["to be swimming", "to be needing", "to be opening"]
        assert (((len(a)) == (len(s))) is True)
        i = 0
        for i in range(0, len(s), 1):
            c = RiTa.conjugate(s[i], args)
            assert (c == a[i])
        args = JsDict({"tense": RiTa.PRESENT, "number": RiTa.SINGULAR, "person": RiTa.THIRD, "form": RiTa.INFINITIVE, "perfect": True})
        a = ["to have swum", "to have needed", "to have opened"]
        assert (((len(a)) == (len(s))) is True)
        i = 0
        for i in range(0, len(s), 1):
            c = RiTa.conjugate(s[i], args)
            assert (c == a[i])
        args = JsDict({"number": RiTa.PLURAL, "person": RiTa.SECOND, "tense": RiTa.PAST})
        assert (RiTa.conjugate("barter", args) == "bartered")
        assert (RiTa.conjugate("run", args) == "ran")
        args = JsDict({"number": RiTa.PLURAL, "person": RiTa.SECOND, "tense": RiTa.PAST})
        s = ["compete", "complete", "eject"]
        a = ["competed", "completed", "ejected"]
        i = 0
        for i in range(0, len(s), 1):
            assert (RiTa.conjugate(s[i], args) == a[i])
        args = JsDict({"number": RiTa.PLURAL, "person": RiTa.SECOND, "tense": RiTa.PAST, "interrogative": True})
        s = ["compete", "complete", "eject"]
        a = ["compete", "complete", "eject"]
        i = 0
        for i in range(0, len(s), 1):
            assert (RiTa.conjugate(s[i], args) == a[i])
        with pytest.raises(Exception):
            RiTa.conjugate("walk", "invalid args")
        assert (RiTa.conjugate("walk", "1SPr") == "walk")
        assert (RiTa.conjugate("walk", "1PPr") == "walk")
        assert (RiTa.conjugate("walk", "2SPr") == "walk")
        assert (RiTa.conjugate("walk", "3SPr") == "walks")
        assert (RiTa.conjugate("walk", "1SFu") == "will walk")
        assert (RiTa.conjugate("walk", "1SPa") == "walked")
        assert (RiTa.conjugate("walk", "2PPa") == "walked")
        assert (RiTa.conjugate("is", "3PPa") == "were")
        assert (RiTa.conjugate("is", "2SPa") == "were")
        assert (RiTa.conjugate("is", "3SPa") == "was")
        assert (RiTa.conjugate("is", "2PPa") == "were")
        original = ["run", "walk", "swim", "create"]
        expected = ["is run", "is walked", "is swum", "is created"]
        for i, w in enumerate(original):
            assert (RiTa.conjugate(w, JsDict({"person": RiTa.THIRD, "passive": True})) == expected[i])
        expected = ["is running", "is walking", "is swimming", "is creating"]
        for i, w in enumerate(original):
            assert (RiTa.conjugate(w, JsDict({"person": RiTa.THIRD, "progressive": True})) == expected[i])
        expected = ["run", "walk", "swim", "create"]
        for i, w in enumerate(original):
            assert (RiTa.conjugate(w, JsDict({"person": RiTa.THIRD, "interrogative": True})) == expected[i])
        expected = ["has run", "has walked", "has swum", "has created"]
        for i, w in enumerate(original):
            assert (RiTa.conjugate(w, JsDict({"person": RiTa.THIRD, "perfect": True})) == expected[i])
        expected = ["being run", "being walked", "being swum", "being created"]
        for i, w in enumerate(original):
            assert (RiTa.conjugate(w, JsDict({"person": RiTa.THIRD, "passive": True, "form": RiTa.GERUND})) == expected[i])
        expected = ["being running", "being walking", "being swimming", "being creating"]
        for i, w in enumerate(original):
            assert (RiTa.conjugate(w, JsDict({"person": RiTa.THIRD, "progressive": True, "form": RiTa.GERUND})) == expected[i])
        expected = ["running", "walking", "swimming", "creating"]
        for i, w in enumerate(original):
            assert (RiTa.conjugate(w, JsDict({"person": RiTa.THIRD, "interrogative": True, "form": RiTa.GERUND})) == expected[i])
        expected = ["having run", "having walked", "having swum", "having created"]
        for i, w in enumerate(original):
            assert (RiTa.conjugate(w, JsDict({"person": RiTa.THIRD, "perfect": True, "form": RiTa.GERUND})) == expected[i])
        expected = ["to be run", "to be walked", "to be swum", "to be created"]
        for i, w in enumerate(original):
            assert (RiTa.conjugate(w, JsDict({"person": RiTa.THIRD, "passive": True, "form": RiTa.INFINITIVE})) == expected[i])
        expected = ["to be running", "to be walking", "to be swimming", "to be creating"]
        for i, w in enumerate(original):
            assert (RiTa.conjugate(w, JsDict({"person": RiTa.THIRD, "progressive": True, "form": RiTa.INFINITIVE})) == expected[i])
        expected = ["to run", "to walk", "to swim", "to create"]
        for i, w in enumerate(original):
            assert (RiTa.conjugate(w, JsDict({"person": RiTa.THIRD, "interrogative": True, "form": RiTa.INFINITIVE})) == expected[i])
        expected = ["to have run", "to have walked", "to have swum", "to have created"]
        for i, w in enumerate(original):
            assert (RiTa.conjugate(w, JsDict({"person": RiTa.THIRD, "perfect": True, "form": RiTa.INFINITIVE})) == expected[i])
        RiTa.conjugate("swim", "2PPa")
        assert (RiTa.conjugate("walked", "3SPr") == "walks")
        assert (RiTa.conjugate("changed", "3SPr") == "changes")
        assert (RiTa.conjugate("spent", "3SPr") == "spends")
        assert (RiTa.conjugate("eaten", "3SPr") == "eats")
        RiTa.conjugate("swim", "2PPa")
    def test_should_call_tostring(self):
        if not (hasLex):
            pytest.skip("mocha this.skip")
        assert (str(RiTa.conjugator) == "  ---------------------\n  Passive = false\n  Perfect = false\n  Progressive = false\n  ---------------------\n  Number = 8\n  Person = 2\n  Tense = 4\n  ---------------------\n")
    def test_should_accept_stems(self):
        plurPast2 = JsDict(JsDict({"number": RiTa.PLURAL, "person": RiTa.SECOND, "tense": RiTa.PAST}))
        plurPres2 = JsDict(JsDict({"number": RiTa.PLURAL, "person": RiTa.SECOND, "tense": RiTa.PRESENT}))
        singPres3 = JsDict(JsDict({"number": RiTa.SINGULAR, "person": RiTa.THIRD, "tense": RiTa.PRESENT}))
        stem = RiTa.stem("walking")
        assert (RiTa.conjugate(stem, plurPast2) == "walked")
        assert (RiTa.conjugate(stem, plurPres2) == "walk")
        assert (RiTa.conjugate(stem, singPres3) == "walks")
        stem = RiTa.stem("writing")
        assert (RiTa.conjugate(stem, plurPast2) == "wrote")
        assert (RiTa.conjugate(stem, plurPres2) == "write")
        assert (RiTa.conjugate(stem, singPres3) == "writes")
        stem = RiTa.stem("asked")
        assert (RiTa.conjugate(stem, plurPast2) == "asked")
        assert (RiTa.conjugate(stem, plurPres2) == "ask")
        assert (RiTa.conjugate(stem, singPres3) == "asks")
        stem = RiTa.stem("changed")
        assert (RiTa.conjugate(stem, plurPast2) == "changed")
        assert (RiTa.conjugate(stem, plurPres2) == "change")
        assert (RiTa.conjugate(stem, singPres3) == "changes")
        stem = RiTa.stem("admired")
        assert (RiTa.conjugate(stem, plurPast2) == "admired")
        assert (RiTa.conjugate(stem, plurPres2) == "admire")
        assert (RiTa.conjugate(stem, singPres3) == "admires")
        stem = RiTa.stem("cured")
        assert (RiTa.conjugate(stem, plurPast2) == "cured")
        assert (RiTa.conjugate(stem, plurPres2) == "cure")
        assert (RiTa.conjugate(stem, singPres3) == "cures")
        stem = RiTa.stem("studies")
        assert (RiTa.conjugate(stem, plurPast2) == "studied")
        assert (RiTa.conjugate(stem, plurPres2) == "study")
        assert (RiTa.conjugate(stem, singPres3) == "studies")
    def test_should_accept_stem_pairs(self):
        opts = JsDict(JsDict({"number": RiTa.PLURAL, "person": RiTa.SECOND, "tense": RiTa.PAST}))
        pairs = [["accompanying", "accompanied"], ["feeling", "felt"], ["placating", "placated"], ["centralizing", "centralized"], ["humanized", "humanized"], ["boosted", "boosted"], ["wearing", "wore"], ["aroused", "aroused"], ["rising", "rose"], ["raising", "raised"], ["vibrating", "vibrated"], ["injection", "injected"], ["vibration", "vibrated"]]
        for p in pairs:
            res = RiTa.conjugate(RiTa.stem(p[0]), opts)
            assert (res == p[1])
    def test_should_call_unconjugate(self):
        if not (hasLex):
            pytest.skip("mocha this.skip")
        assert (RiTa.conjugator.unconjugate("trepanning") == "trepan")
        assert (RiTa.conjugator.unconjugate("plays") == "play")
        assert (RiTa.conjugator.unconjugate("takes") == "take")
        assert (RiTa.conjugator.unconjugate("gets") == "get")
        assert (RiTa.conjugator.unconjugate("comes") == "come")
        assert (RiTa.conjugator.unconjugate("goes") == "go")
        assert (RiTa.conjugator.unconjugate("teaches") == "teach")
        assert (RiTa.conjugator.unconjugate("fixes") == "fix")
        assert (RiTa.conjugator.unconjugate("misses") == "miss")
        assert (RiTa.conjugator.unconjugate("studies") == "study")
        assert (RiTa.conjugator.unconjugate("tries") == "try")
        assert (RiTa.conjugator.unconjugate("carries") == "carry")
        assert (RiTa.conjugator.unconjugate("wishes") == "wish")
        assert (RiTa.conjugator.unconjugate("blitzes") == "blitz")
        assert (RiTa.conjugator.unconjugate("watched") == "watch")
        assert (RiTa.conjugator.unconjugate("planted") == "plant")
        assert (RiTa.conjugator.unconjugate("watered") == "water")
        assert (RiTa.conjugator.unconjugate("pulled") == "pull")
        assert (RiTa.conjugator.unconjugate("picked") == "pick")
        assert (RiTa.conjugator.unconjugate("liked") == "like")
        assert (RiTa.conjugator.unconjugate("moved") == "move")
        assert (RiTa.conjugator.unconjugate("tasted") == "taste")
        assert (RiTa.conjugator.unconjugate("tried") == "try")
        assert (RiTa.conjugator.unconjugate("studied") == "study")
        assert (RiTa.conjugator.unconjugate("carried") == "carry")
        assert (RiTa.conjugator.unconjugate("digged") == "dig")
        assert (RiTa.conjugator.unconjugate("flagged") == "flag")
        assert (RiTa.conjugator.unconjugate("blowing") == "blow")
        assert (RiTa.conjugator.unconjugate("raining") == "rain")
        assert (RiTa.conjugator.unconjugate("coming") == "come")
        assert (RiTa.conjugator.unconjugate("having") == "have")
        assert (RiTa.conjugator.unconjugate("running") == "run")
        assert (RiTa.conjugator.unconjugate("putting") == "put")
        assert (RiTa.conjugator.unconjugate("sitting") == "sit")
        assert (RiTa.conjugator.unconjugate("pulling") == "pull")
        assert (RiTa.conjugator.unconjugate("has") == "have")
        assert (RiTa.conjugator.unconjugate("had") == "have")
        assert (RiTa.conjugator.unconjugate("sat") == "sit")
        assert (RiTa.conjugator.unconjugate("shown") == "show")
        assert (RiTa.conjugator.unconjugate("ate") == "eat")
        assert (RiTa.conjugator.unconjugate("went") == "go")
        assert (RiTa.conjugator.unconjugate("met") == "meet")
        assert (RiTa.conjugator.unconjugate("have") == "have")
        assert (RiTa.conjugator.unconjugate("eat") == "eat")
        assert (RiTa.conjugator.unconjugate("play") == "play")
        assert (RiTa.conjugator.unconjugate("go") == "go")
        assert (RiTa.conjugator.unconjugate("do") == "do")
        assert (RiTa.conjugator.unconjugate("spooning") == "spoon")
        assert (RiTa.conjugator.unconjugate("mepanning") == "mepan")
        assert (RiTa.conjugator.unconjugate("muddling") == "muddle")
        if (_typeof(lambda: NOLEX)) != ("undefined"):
            assert (RiTa.conjugator.unconjugate("gets") == "get")
            assert (RiTa.conjugator.unconjugate("comes") == "come")
            assert (RiTa.conjugator.unconjugate("goes") == "go")
            assert (RiTa.conjugator.unconjugate("teaches") == "teach")
            assert (RiTa.conjugator.unconjugate("fixes") == "fix")
            assert (RiTa.conjugator.unconjugate("misses") == "miss")
            assert (RiTa.conjugator.unconjugate("studies") == "study")
            assert (RiTa.conjugator.unconjugate("tries") == "try")
            assert (RiTa.conjugator.unconjugate("carries") == "carry")
            assert (RiTa.conjugator.unconjugate("wishes") == "wish")
            assert (RiTa.conjugator.unconjugate("blitzes") == "blitz")
            assert (RiTa.conjugator.unconjugate("watered") == "water")
            assert (RiTa.conjugator.unconjugate("pulled") == "pull")
            assert (RiTa.conjugator.unconjugate("picked") == "pick")
            assert (RiTa.conjugator.unconjugate("liked") == "like")
            assert (RiTa.conjugator.unconjugate("moved") == "move")
            assert (RiTa.conjugator.unconjugate("tasted") == "taste")
            assert (RiTa.conjugator.unconjugate("tried") == "try")
            assert (RiTa.conjugator.unconjugate("studied") == "study")
            assert (RiTa.conjugator.unconjugate("carried") == "carry")
            assert (RiTa.conjugator.unconjugate("digged") == "dig")
            assert (RiTa.conjugator.unconjugate("flagged") == "flag")
            assert (RiTa.conjugator.unconjugate("raining") == "rain")
            assert (RiTa.conjugator.unconjugate("coming") == "come")
            assert (RiTa.conjugator.unconjugate("having") == "have")
            assert (RiTa.conjugator.unconjugate("running") == "run")
            assert (RiTa.conjugator.unconjugate("putting") == "put")
            assert (RiTa.conjugator.unconjugate("sitting") == "sit")
            assert (RiTa.conjugator.unconjugate("pulling") == "pull")
        assert (RiTa.conjugator.unconjugate("bitten") == "bite")
        assert (RiTa.conjugator.unconjugate("broken") == "break")
        assert (RiTa.conjugator.unconjugate("committed") == "commit")
        assert (RiTa.conjugator.unconjugate("computerized") == "computerize")
        assert (RiTa.conjugator.unconjugate("concerned") == "concern")
        assert (RiTa.conjugator.unconjugate("discriminated") == "discriminate")
        assert (RiTa.conjugator.unconjugate("ended") == "end")
        assert (RiTa.conjugator.unconjugate("expected") == "expect")
        assert (RiTa.conjugator.unconjugate("finished") == "finish")
        assert (RiTa.conjugator.unconjugate("gained") == "gain")
        assert (RiTa.conjugator.unconjugate("gotten") == "get")
        assert (RiTa.conjugator.unconjugate("increased") == "increase")
        assert (RiTa.conjugator.unconjugate("involved") == "involve")
        assert (RiTa.conjugator.unconjugate("launched") == "launch")
        assert (RiTa.conjugator.unconjugate("led") == "lead")
        assert (RiTa.conjugator.unconjugate("lived") == "live")
        assert (RiTa.conjugator.unconjugate("outpaced") == "outpace")
        assert (RiTa.conjugator.unconjugate("overseen") == "oversee")
        assert (RiTa.conjugator.unconjugate("paled") == "pale")
        assert (RiTa.conjugator.unconjugate("prepaid") == "prepay")
        assert (RiTa.conjugator.unconjugate("pressured") == "pressure")
        assert (RiTa.conjugator.unconjugate("proliferated") == "proliferate")
        assert (RiTa.conjugator.unconjugate("remade") == "remake")
        assert (RiTa.conjugator.unconjugate("reopened") == "reopen")
        assert (RiTa.conjugator.unconjugate("reported") == "report")
        assert (RiTa.conjugator.unconjugate("sold") == "sell")
        assert (RiTa.conjugator.unconjugate("resold") == "resell")
        assert (RiTa.conjugator.unconjugate("settled") == "settle")
        assert (RiTa.conjugator.unconjugate("started") == "start")
        assert (RiTa.conjugator.unconjugate("were") == "be")
        assert (RiTa.conjugator.unconjugate("bitten") == "bite")
        assert (RiTa.conjugator.unconjugate("broken") == "break")
        assert (RiTa.conjugator.unconjugate("owned") == "own")
        assert (RiTa.conjugator.unconjugate("planned") == "plan")
        assert (RiTa.conjugator.unconjugate("rented") == "rent")
        assert (RiTa.conjugator.unconjugate("repurchased") == "repurchase")
        assert (RiTa.conjugator.unconjugate("roasted") == "roast")
        assert (RiTa.conjugator.unconjugate("busted") == "bust")
        assert (RiTa.conjugator.unconjugate("grown") == "grow")
        assert (RiTa.conjugator.unconjugate("blown") == "blow")
        assert (RiTa.conjugator.unconjugate("heard") == "hear")
    def test_should_conjugate_verbs(self):
        opt = JsDict(JsDict({"number": RiTa.SINGULAR, "person": RiTa.FIRST, "tense": RiTa.PAST}))
        assert (RiTa.conjugate("bite", opt) == "bit")
        assert (RiTa.conjugate("break", opt) == "broke")
        assert (RiTa.conjugate("call", opt) == "called")
        assert (RiTa.conjugate("commit", opt) == "committed")
        assert (RiTa.conjugate("computerize", opt) == "computerized")
        assert (RiTa.conjugate("concern", opt) == "concerned")
        assert (RiTa.conjugate("discriminate", opt) == "discriminated")
        assert (RiTa.conjugate("end", opt) == "ended")
        assert (RiTa.conjugate("expect", opt) == "expected")
        assert (RiTa.conjugate("finish", opt) == "finished")
        assert (RiTa.conjugate("gain", opt) == "gained")
        assert (RiTa.conjugate("get", opt) == "got")
        assert (RiTa.conjugate("increase", opt) == "increased")
        assert (RiTa.conjugate("involve", opt) == "involved")
        assert (RiTa.conjugate("launch", opt) == "launched")
        assert (RiTa.conjugate("lead", opt) == "led")
        assert (RiTa.conjugate("live", opt) == "lived")
        assert (RiTa.conjugate("concern", opt) == "concerned")
        assert (RiTa.conjugate("oversee", opt) == "oversaw")
        assert (RiTa.conjugate("pale", opt) == "paled")
        assert (RiTa.conjugate("prepay", opt) == "prepaid")
        assert (RiTa.conjugate("pressure", opt) == "pressured")
        assert (RiTa.conjugate("proliferate", opt) == "proliferated")
        assert (RiTa.conjugate("remake", opt) == "remade")
        assert (RiTa.conjugate("reopen", opt) == "reopened")
        assert (RiTa.conjugate("report", opt) == "reported")
        assert (RiTa.conjugate("resell", opt) == "resold")
        assert (RiTa.conjugate("settle", opt) == "settled")
        assert (RiTa.conjugate("start", opt) == "started")
        opt = JsDict({"tense": RiTa.PRESENT, "number": RiTa.SINGULAR, "perfect": True})
        assert (RiTa.conjugate("bite", opt) == "have bitten")
        assert (RiTa.conjugate("break", opt) == "have broken")
        assert (RiTa.conjugate("build", opt) == "have built")
        assert (RiTa.conjugate("enter", opt) == "have entered")
        assert (RiTa.conjugate("own", opt) == "have owned")
        assert (RiTa.conjugate("plan", opt) == "have planned")
        assert (RiTa.conjugate("rent", opt) == "have rented")
        assert (RiTa.conjugate("repurchase", opt) == "have repurchased")
        assert (RiTa.conjugate("roast", opt) == "have roasted")
    def test_should_handle_stem_lookup_correctly(self):
        conj = RiTa.conjugator
        for w in ["be", "been", "goes", "running", "walked", "bettering"]:
            assert (conj._handle_stem(w) == w)
        assert (conj._handle_stem("alien") == "alienate")
        assert (conj._handle_stem("bath") == "bathe")
        assert (conj._handle_stem("central") == "centralize")
    def test_should_invalidate_the_stem_cache_on_lexicon_swap(self):
        conj = RiTa.conjugator
        orig = RiTa.lexicon.data
        try:
            before = conj._handle_stem("alien")
            assert (before == "alienate")
            assert (conj._stemCache.size > 0)
            RiTa.lexicon.data = JsDict({**orig})
            conj._handle_stem("alien")
            assert (conj._stemCacheRef == RiTa.lexicon.data)
            assert (conj._stemCache.size == 1)
            assert (conj._handle_stem("alien") == before)
        finally:
            RiTa.lexicon.data = orig

def _fn_1(*args):
    RiTa.conjugate()

def _fn_2(*args):
    RiTa.conjugate("")

def _fn_3(*args):
    RiTa.conjugate("walk", "invalid args")

