# AUTO-GENERATED from js/test/conjugator-tests.js by scripts/js-to-py-tests.js — do not edit by hand.
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
    RiTa.conjugate()

def __fn_2(_):
    RiTa.conjugate("")

def __fn_3(_):
    RiTa.conjugate("walk", "invalid args")

hasLex = True

class TestConjugator:
    def test_should_call_pastpart(self):
        assert (RiTa.pastPart("pen") == "penned")
        assert (RiTa.pastPart("red") == "red")
        assert (RiTa.pastPart("sleep") == "slept")
        assert (RiTa.pastPart("withhold") == "withheld")
        assert (RiTa.pastPart("cut") == "cut")
        assert (RiTa.pastPart("go") == "gone")
        assert (RiTa.pastPart("swim") == "swum")
        assert (RiTa.pastPart("would") == "would")
        assert (RiTa.pastPart("might") == "might")
        assert (RiTa.pastPart("run") == "run")
        assert (RiTa.pastPart("speak") == "spoken")
        assert (RiTa.pastPart("break") == "broken")
        assert (RiTa.pastPart("plead") == "pled")
        assert (RiTa.pastPart("") == "")
        assert (RiTa.pastPart("shrink") == "shrunk")
        assert (RiTa.pastPart("stink") == "stunk")
        assert (RiTa.pastPart("study") == "studied")
        assert (RiTa.pastPart("bite") == "bitten")
        assert (RiTa.pastPart("break") == "broken")
        assert (RiTa.pastPart("call") == "called")
        assert (RiTa.pastPart("commit") == "committed")
        assert (RiTa.pastPart("computerize") == "computerized")
        assert (RiTa.pastPart("concern") == "concerned")
        assert (RiTa.pastPart("discriminate") == "discriminated")
        assert (RiTa.pastPart("end") == "ended")
        assert (RiTa.pastPart("expect") == "expected")
        assert (RiTa.pastPart("finish") == "finished")
        assert (RiTa.pastPart("gain") == "gained")
        assert (RiTa.pastPart("get") == "gotten")
        assert (RiTa.pastPart("increase") == "increased")
        assert (RiTa.pastPart("involve") == "involved")
        assert (RiTa.pastPart("launch") == "launched")
        assert (RiTa.pastPart("lead") == "led")
        assert (RiTa.pastPart("live") == "lived")
        assert (RiTa.pastPart("outpace") == "outpaced")
        assert (RiTa.pastPart("oversee") == "overseen")
        assert (RiTa.pastPart("oversell") == "oversold")
        assert (RiTa.pastPart("pale") == "paled")
        assert (RiTa.pastPart("prepay") == "prepaid")
        assert (RiTa.pastPart("pressure") == "pressured")
        assert (RiTa.pastPart("proliferate") == "proliferated")
        assert (RiTa.pastPart("remake") == "remade")
        assert (RiTa.pastPart("reopen") == "reopened")
        assert (RiTa.pastPart("report") == "reported")
        assert (RiTa.pastPart("resell") == "resold")
        assert (RiTa.pastPart("settle") == "settled")
        assert (RiTa.pastPart("bite") == "bitten")
        assert (RiTa.pastPart("break") == "broken")
        assert (RiTa.pastPart("build") == "built")
        assert (RiTa.pastPart("enter") == "entered")
        assert (RiTa.pastPart("own") == "owned")
        assert (RiTa.pastPart("plan") == "planned")
        assert (RiTa.pastPart("rent") == "rented")
        assert (RiTa.pastPart("repurchase") == "repurchased")
        assert (RiTa.pastPart("roast") == "roasted")
        assert (RiTa.pastPart("start") == "started")
        assert (RiTa.pastPart("bust") == "busted")
        assert (RiTa.pastPart("heart") == "hearted")
        assert (RiTa.pastPart("closet") == "closeted")
        assert (RiTa.pastPart("bear") == "borne")
        if hasLex:
            assert (RiTa.pastPart("hopped") == "hopped")
            assert (RiTa.pastPart("hated") == "hated")
            assert (RiTa.pastPart("created") == "created")
            assert (RiTa.pastPart("committed") == "committed")
            assert (RiTa.pastPart("submitted") == "submitted")
            assert (RiTa.pastPart("come") == "come")
            assert (RiTa.pastPart("forgotten") == "forgotten")
            assert (RiTa.pastPart("arisen") == "arisen")
            assert (RiTa.pastPart("eaten") == "eaten")
            assert (RiTa.pastPart("chosen") == "chosen")
            assert (RiTa.pastPart("frozen") == "frozen")
            assert (RiTa.pastPart("stolen") == "stolen")
            assert (RiTa.pastPart("worn") == "worn")
            assert (RiTa.pastPart("broken") == "broken")
            assert (RiTa.pastPart("written") == "written")
            assert (RiTa.pastPart("ridden") == "ridden")
            assert (RiTa.pastPart("drawn") == "drawn")
            assert (RiTa.pastPart("known") == "known")
            assert (RiTa.pastPart("grown") == "grown")
            assert (RiTa.pastPart("done") == "done")
            assert (RiTa.pastPart("gone") == "gone")
            assert (RiTa.pastPart("awake") == "awoken")
            assert (RiTa.pastPart("become") == "become")
            assert (RiTa.pastPart("drink") == "drunk")
            assert (RiTa.pastPart("run") == "run")
            assert (RiTa.pastPart("shine") == "shone")
            assert (RiTa.pastPart("grown") == "grown")
            assert (RiTa.pastPart("heard") == "heard")
    def test_should_call_presentpart(self):
        assert (RiTa.presentPart("") == "")
        assert (RiTa.presentPart("sleep") == "sleeping")
        assert (RiTa.presentPart("withhold") == "withholding")
        assert (RiTa.presentPart("cut") == "cutting")
        assert (RiTa.presentPart("go") == "going")
        assert (RiTa.presentPart("run") == "running")
        assert (RiTa.presentPart("speak") == "speaking")
        assert (RiTa.presentPart("break") == "breaking")
        assert (RiTa.presentPart("become") == "becoming")
        assert (RiTa.presentPart("plead") == "pleading")
        assert (RiTa.presentPart("awake") == "awaking")
        assert (RiTa.presentPart("study") == "studying")
        assert (RiTa.presentPart("lie") == "lying")
        assert (RiTa.presentPart("swim") == "swimming")
        assert (RiTa.presentPart("run") == "running")
        assert (RiTa.presentPart("dig") == "digging")
        assert (RiTa.presentPart("set") == "setting")
        assert (RiTa.presentPart("speak") == "speaking")
        assert (RiTa.presentPart("bring") == "bringing")
        assert (RiTa.presentPart("speak") == "speaking")
        assert (RiTa.presentPart("study ") == "studying")
        assert (RiTa.presentPart(" study") == "studying")
        assert (RiTa.presentPart("hoe") == "hoeing")
        assert (RiTa.presentPart("shoe") == "shoeing")
        if hasLex:
            assert (RiTa.pastPart("awake") == "awoken")
            assert (RiTa.pastPart("become") == "become")
            assert (RiTa.pastPart("drink") == "drunk")
            assert (RiTa.pastPart("run") == "run")
            assert (RiTa.pastPart("shine") == "shone")
    def test_should_conjugate_vbds(self):
        if not (hasLex):
            pytest.skip("mocha this.skip")
        assert (RiTa.conjugate("go", {"number": RiTa.SINGULAR, "person": RiTa.FIRST, "tense": RiTa.PAST}) == "went")
        assert (RiTa.conjugate("run", {"number": RiTa.SINGULAR, "person": RiTa.FIRST, "tense": RiTa.PAST}) == "ran")
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
        assert ("swum" == RiTa.pastPart("swim"))
        assert (RiTa.conjugate("be", {"form": RiTa.GERUND}) == "being")
        assert (RiTa.conjugate("are", {"number": RiTa.PLURAL, "person": RiTa.SECOND, "tense": RiTa.PAST}) == "were")
        s = ["swim", "need", "open"]
        a = ["swims", "needs", "opens"]
        args = {"tense": RiTa.PRESENT, "number": RiTa.SINGULAR, "person": RiTa.THIRD}
        with pytest.raises(Exception):
            return RiTa.conjugate(args)
        with pytest.raises(Exception):
            return RiTa.conjugate("", args)
        i = 0
        for i in range(len(s)):
            c = RiTa.conjugate(s[i], args)
            assert (c == a[i])
        args = {"tense": RiTa.PRESENT, "number": RiTa.SINGULAR, "person": RiTa.THIRD, "passive": True}
        a = ["is swum", "is needed", "is opened"]
        i = 0
        for i in range(len(s)):
            assert (RiTa.conjugate(s[i], args) == a[i])
        args = {"number": RiTa.SINGULAR, "person": RiTa.FIRST, "tense": RiTa.PAST}
        assert (RiTa.conjugate("swim", args) == "swam")
        s = ["swim", "need", "open"]
        a = ["swam", "needed", "opened"]
        assert (((len(a)) == (len(s))) is True)
        i = 0
        for i in range(len(s)):
            c = RiTa.conjugate(s[i], args)
            assert (c == a[i])
        args = {"number": RiTa.PLURAL, "person": RiTa.SECOND, "tense": RiTa.PAST}
        a = ["swam", "needed", "opened"]
        assert (((len(a)) == (len(s))) is True)
        i = 0
        for i in range(len(s)):
            assert (RiTa.conjugate(s[i], args) == a[i])
        args = {"number": RiTa.PLURAL, "person": RiTa.SECOND, "tense": RiTa.FUTURE}
        a = ["will swim", "will need", "will open"]
        assert (((len(a)) == (len(s))) is True)
        i = 0
        for i in range(len(s)):
            assert (RiTa.conjugate(s[i], args) == a[i])
        args = {"tense": RiTa.PAST, "number": RiTa.SINGULAR, "person": RiTa.THIRD}
        a = ["swam", "needed", "opened"]
        assert (((len(a)) == (len(s))) is True)
        i = 0
        for i in range(len(s)):
            c = RiTa.conjugate(s[i], args)
            assert (c == a[i])
        args = {"tense": RiTa.PAST, "number": RiTa.SINGULAR, "person": RiTa.THIRD, "form": RiTa.INFINITIVE}
        a = ["to swim", "to need", "to open"]
        assert (((len(a)) == (len(s))) is True)
        i = 0
        for i in range(len(s)):
            c = RiTa.conjugate(s[i], args)
            assert (c == a[i])
        args = {"tense": RiTa.PAST, "number": RiTa.SINGULAR, "person": RiTa.THIRD, "passive": True}
        s = ["scorch", "burn", "hit"]
        a = ["was scorched", "was burned", "was hit"]
        assert (((len(a)) == (len(s))) is True)
        i = 0
        for i in range(len(s)):
            c = RiTa.conjugate(s[i], args)
            assert (c == a[i])
        s = ["swim", "need", "open"]
        args = {"tense": RiTa.PRESENT, "number": RiTa.SINGULAR, "person": RiTa.THIRD, "form": RiTa.INFINITIVE, "progressive": True}
        a = ["to be swimming", "to be needing", "to be opening"]
        assert (((len(a)) == (len(s))) is True)
        i = 0
        for i in range(len(s)):
            c = RiTa.conjugate(s[i], args)
            assert (c == a[i])
        args = {"tense": RiTa.PRESENT, "number": RiTa.SINGULAR, "person": RiTa.THIRD, "form": RiTa.INFINITIVE, "perfect": True}
        a = ["to have swum", "to have needed", "to have opened"]
        assert (((len(a)) == (len(s))) is True)
        i = 0
        for i in range(len(s)):
            c = RiTa.conjugate(s[i], args)
            assert (c == a[i])
        args = {"number": RiTa.PLURAL, "person": RiTa.SECOND, "tense": RiTa.PAST}
        assert (RiTa.conjugate("barter", args) == "bartered")
        assert (RiTa.conjugate("run", args) == "ran")
        args = {"number": RiTa.PLURAL, "person": RiTa.SECOND, "tense": RiTa.PAST}
        s = ["compete", "complete", "eject"]
        a = ["competed", "completed", "ejected"]
        i = 0
        for i in range(len(s)):
            assert (RiTa.conjugate(s[i], args) == a[i])
        args = {"number": RiTa.PLURAL, "person": RiTa.SECOND, "tense": RiTa.PAST, "interrogative": True}
        s = ["compete", "complete", "eject"]
        a = ["compete", "complete", "eject"]
        i = 0
        for i in range(len(s)):
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
        for w, i in original:
            assert (RiTa.conjugate(w, {"person": RiTa.THIRD, "passive": True}) == expected[i])
        expected = ["is running", "is walking", "is swimming", "is creating"]
        for w, i in original:
            assert (RiTa.conjugate(w, {"person": RiTa.THIRD, "progressive": True}) == expected[i])
        expected = ["run", "walk", "swim", "create"]
        for w, i in original:
            assert (RiTa.conjugate(w, {"person": RiTa.THIRD, "interrogative": True}) == expected[i])
        expected = ["has run", "has walked", "has swum", "has created"]
        for w, i in original:
            assert (RiTa.conjugate(w, {"person": RiTa.THIRD, "perfect": True}) == expected[i])
        expected = ["being run", "being walked", "being swum", "being created"]
        for w, i in original:
            assert (RiTa.conjugate(w, {"person": RiTa.THIRD, "passive": True, "form": RiTa.GERUND}) == expected[i])
        expected = ["being running", "being walking", "being swimming", "being creating"]
        for w, i in original:
            assert (RiTa.conjugate(w, {"person": RiTa.THIRD, "progressive": True, "form": RiTa.GERUND}) == expected[i])
        expected = ["running", "walking", "swimming", "creating"]
        for w, i in original:
            assert (RiTa.conjugate(w, {"person": RiTa.THIRD, "interrogative": True, "form": RiTa.GERUND}) == expected[i])
        expected = ["having run", "having walked", "having swum", "having created"]
        for w, i in original:
            assert (RiTa.conjugate(w, {"person": RiTa.THIRD, "perfect": True, "form": RiTa.GERUND}) == expected[i])
        expected = ["to be run", "to be walked", "to be swum", "to be created"]
        for w, i in original:
            assert (RiTa.conjugate(w, {"person": RiTa.THIRD, "passive": True, "form": RiTa.INFINITIVE}) == expected[i])
        expected = ["to be running", "to be walking", "to be swimming", "to be creating"]
        for w, i in original:
            assert (RiTa.conjugate(w, {"person": RiTa.THIRD, "progressive": True, "form": RiTa.INFINITIVE}) == expected[i])
        expected = ["to run", "to walk", "to swim", "to create"]
        for w, i in original:
            assert (RiTa.conjugate(w, {"person": RiTa.THIRD, "interrogative": True, "form": RiTa.INFINITIVE}) == expected[i])
        expected = ["to have run", "to have walked", "to have swum", "to have created"]
        for w, i in original:
            assert (RiTa.conjugate(w, {"person": RiTa.THIRD, "perfect": True, "form": RiTa.INFINITIVE}) == expected[i])
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
        plurPast2 = {"number": RiTa.PLURAL, "person": RiTa.SECOND, "tense": RiTa.PAST}
        plurPres2 = {"number": RiTa.PLURAL, "person": RiTa.SECOND, "tense": RiTa.PRESENT}
        singPres3 = {"number": RiTa.SINGULAR, "person": RiTa.THIRD, "tense": RiTa.PRESENT}
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
        opts = {"number": RiTa.PLURAL, "person": RiTa.SECOND, "tense": RiTa.PAST}
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
        if (__typeof(NOLEX)) != ("undefined"):
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
        opt = {"number": RiTa.SINGULAR, "person": RiTa.FIRST, "tense": RiTa.PAST}
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
        opt = {"tense": RiTa.PRESENT, "number": RiTa.SINGULAR, "perfect": True}
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
            assert (conj._handleStem(w) == w)
        assert (conj._handleStem("alien") == "alienate")
        assert (conj._handleStem("bath") == "bathe")
        assert (conj._handleStem("central") == "centralize")
    def test_should_invalidate_the_stem_cache_on_lexicon_swap(self):
        conj = RiTa.conjugator
        orig = RiTa.lexicon.data
        try:
            before = conj._handleStem("alien")
            assert (before == "alienate")
            assert (conj._stemCache.size > 0)
            RiTa.lexicon.data = {**orig}
            conj._handleStem("alien")
            assert (conj._stemCacheRef == RiTa.lexicon.data)
            assert (conj._stemCache.size == 1)
            assert (conj._handleStem("alien") == before)
        finally:
            RiTa.lexicon.data = orig

