# AUTO-GENERATED from js/test/tagger-tests.js by scripts/js-to-py-tests.js — do not edit by hand.
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

class TestTagger:
    # (var hoisted to module scope)
    def test_should_call_pos_array(self):
        if not (hasLex):
            pytest.skip("mocha this.skip")
        assert (RiTa.pos([]) == [])
        assert (RiTa.pos(["deal"]) == ["nn"])
        assert (RiTa.pos(["freed"]) == ["jj"])
        assert (RiTa.pos(["the"]) == ["dt"])
        assert (RiTa.pos(["a"]) == ["dt"])
        assert (RiTa.pos(re.split(" ", "the top seed")) == ["dt", "jj", "nn"])
        assert (RiTa.pos(re.split(" ", "by illegal means")) == ["in", "jj", "nn"])
        assert (RiTa.pos(re.split(" ", "He outnumbers us")) == ["prp", "vbz", "prp"])
        assert (RiTa.pos(re.split(" ", "I outnumber you")) == ["prp", "vbp", "prp"])
        assert (RiTa.pos(re.split(" ", "Elephants dance")) == ["nns", "vbp"])
        assert (RiTa.pos(re.split(" ", "the boy dances")) == ["dt", "nn", "vbz"])
        assert (RiTa.pos(re.split(" ", "Dave dances")) == ["nnp", "vbz"])
    def test_should_call_simple_pos_array(self):
        assert (RiTa.pos([], JsDict({"simple": True})) == [])
        assert (RiTa.pos(["freed"], JsDict({"simple": True})) == ["a"])
        assert (RiTa.pos(["the"], JsDict({"simple": True})) == ["-"])
        assert (RiTa.pos(["a"], JsDict({"simple": True})) == ["-"])
        assert (RiTa.pos(re.split(" ", "the top seed"), JsDict({"simple": True})) == ["-", "a", "n"])
        assert (RiTa.pos(re.split(" ", "by illegal means"), JsDict({"simple": True})) == ["-", "a", "n"])
        assert (RiTa.pos(re.split(" ", "He outnumbers us"), JsDict({"simple": True})) == ["-", "v", "-"])
        assert (RiTa.pos(re.split(" ", "I outnumber you"), JsDict({"simple": True})) == ["-", "v", "-"])
        assert (RiTa.pos(re.split(" ", "Elephants dance"), JsDict({"simple": True})) == ["n", "v"])
        assert (RiTa.pos(re.split(" ", "the boy dances"), JsDict({"simple": True})) == ["-", "n", "v"])
    def test_should_call_posinline_array_simple(self):
        result = None
        answer = None
        txt = None
        assert (RiTa.pos_inline([], JsDict({"simple": True})) == "")
        assert (RiTa.pos_inline(["asdfaasd"], JsDict({"simple": True})) == "asdfaasd/n")
        result = RiTa.pos_inline(["clothes"], JsDict({"simple": True}))
        answer = "clothes/n"
        assert (result == answer)
        result = RiTa.pos_inline(["teeth"], JsDict({"simple": True}))
        answer = "teeth/n"
        assert (result == answer)
        result = RiTa.pos_inline(re.split(" ", "There is a cat"), JsDict({"simple": True}))
        answer = "There/- is/v a/- cat/n"
        assert (result == answer)
        result = RiTa.pos_inline(RiTa.tokenize("The boy, dressed in red, ate an apple."), JsDict({"simple": True}))
        answer = "The/- boy/n , dressed/v in/- red/a , ate/v an/- apple/n ."
        assert (result == answer)
        txt = "The dog ran faster than the other dog. But the other dog was prettier."
        result = RiTa.pos_inline(RiTa.tokenize(txt), JsDict({"simple": True}))
        answer = "The/- dog/n ran/v faster/r than/- the/- other/a dog/n . But/- the/- other/a dog/n was/v prettier/a ."
        assert (result == answer)

    def test_should_handle_inflected_verbs(self):
        assert (RiTa.pos("disbelieves") == ["vbz"])
        assert (RiTa.pos("disbelieves", JsDict({"simple": 1})) == ["v"])
        assert (RiTa.pos("fates") == ["nns"])
        assert (RiTa.pos("fates", JsDict({"simple": 1})) == ["n"])
        assert (RiTa.pos("hates") == ["vbz"])
        assert (RiTa.pos("hates", JsDict({"simple": 1})) == ["v"])
        assert (RiTa.pos("hated") == ["vbd"])
        assert (RiTa.pos("hated", JsDict({"simple": 1})) == ["v"])
        assert (RiTa.pos("hating") == ["vbg"])
        assert (RiTa.pos("hating", JsDict({"simple": 1})) == ["v"])
        assert (RiTa.pos("He rode the horse") == ["prp", "vbd", "dt", "nn"])
        assert (RiTa.pos("He has ridden the horse") == ["prp", "vbz", "vbn", "dt", "nn"])
        assert (RiTa.pos("He rowed the boat") == ["prp", "vbd", "dt", "nn"])
        assert (RiTa.pos("He has rowed the boat") == ["prp", "vbz", "vbn", "dt", "nn"])
    def test_should_call_pos(self):
        result = None
        answer = None
        resultArr = None
        answerArr = None
        txt = None
        assert (RiTa.pos("") == [])
        assert (RiTa.pos(",") == [","])
        assert (RiTa.pos(" ") == [])
        assert (RiTa.pos("freed") == ["jj"])
        assert (RiTa.pos("biped") == ["nn"])
        assert (RiTa.pos("greed") == ["nn"])
        assert (RiTa.pos("creed") == ["nn"])
        assert (RiTa.pos("weed") == ["nn"])
        assert (RiTa.pos("broke") == ["vbd"])
        assert (RiTa.pos("broke", JsDict({"simple": 1})) == ["v"])
        assert (RiTa.pos("committed") == ["vbn"])
        assert (RiTa.pos("committed", JsDict({"simple": 1})) == ["v"])
        assert (RiTa.pos("outpaced") == ["vbd"])
        assert (RiTa.pos("outpaced", JsDict({"simple": 1})) == ["v"])
        assert (RiTa.pos("concerned") == ["vbd"])
        assert (RiTa.pos("concerned", JsDict({"simple": 1})) == ["v"])
        assert (RiTa.pos("committed") == ["vbn"])
        assert (RiTa.pos("committed", JsDict({"simple": 1})) == ["v"])
        assert (RiTa.pos("the top seed") == ["dt", "jj", "nn"])
        assert (RiTa.pos("by illegal means") == ["in", "jj", "nn"])
        assert (RiTa.pos("Joannie Smith ran away") == ["nnp", "nnp", "vbd", "rb"])
        result = RiTa.pos("mammal")
        answer = ["nn"]
        assert (result == answer)
        result = RiTa.pos("asfaasd")
        answer = ["nn"]
        assert (result == answer)
        result = RiTa.pos("innings")
        answer = ["nns"]
        assert (result == answer)
        result = RiTa.pos("clothes")
        answer = ["nns"]
        assert (result == answer)
        result = RiTa.pos("clothes")
        answer = ["nns"]
        assert (result == answer)
        result = RiTa.pos("teeth")
        answer = ["nns"]
        assert (result == answer)
        result = RiTa.pos("memories")
        answer = ["nns"]
        assert (result == answer)
        assert (RiTa.pos("flunks") == ["vbz"])
        assert (RiTa.pos("outnumbers") == ["vbz"])
        assert (RiTa.pos("He outnumbers us") == ["prp", "vbz", "prp"])
        assert (RiTa.pos("I outnumber you") == ["prp", "vbp", "prp"])
        resultArr = RiTa.pos("Elephants dance")
        answerArr = ["nns", "vbp"]
        assert (answerArr == resultArr)
        result = RiTa.pos("the boy dances")
        answer = ["dt", "nn", "vbz"]
        assert (result == answer)
        result = RiTa.pos("he dances")
        answer = ["prp", "vbz"]
        assert (result == answer)
        resultArr = RiTa.pos("Dave dances")
        answerArr = ["nnp", "vbz"]
        assert (answerArr == resultArr)
        result = RiTa.pos("running")
        answer = ["vbg"]
        assert (result == answer)
        result = RiTa.pos("asserting")
        answer = ["vbg"]
        assert (result == answer)
        result = RiTa.pos("assenting")
        answer = ["vbg"]
        assert (result == answer)
        result = RiTa.pos("Dave")
        answer = ["nnp"]
        assert (result == answer)
        result = RiTa.pos("They feed the cat")
        answer = ["prp", "vbp", "dt", "nn"]
        assert (result == answer)
        result = RiTa.pos("There is a cat.")
        answer = ["ex", "vbz", "dt", "nn", "."]
        assert (result == answer)
        result = RiTa.pos("The boy, dressed in red, ate an apple.")
        answer = ["dt", "nn", ",", "vbn", "in", "jj", ",", "vbd", "dt", "nn", "."]
        assert (result == answer)
        txt = "The dog ran faster than the other dog.  But the other dog was prettier."
        result = RiTa.pos(txt)
        answer = ["dt", "nn", "vbd", "rbr", "in", "dt", "jj", "nn", ".", "cc", "dt", "jj", "nn", "vbd", "jjr", "."]
        assert (result == answer)
        assert (RiTa.pos("is") == ["vbz"])
        assert (RiTa.pos("am") == ["vbp"])
        assert (RiTa.pos("be") == ["vb"])
        result = RiTa.pos("There is a cat.")
        answer = ["ex", "vbz", "dt", "nn", "."]
        assert (result == answer)
        result = RiTa.pos("There was a cat.")
        answer = ["ex", "vbd", "dt", "nn", "."]
        assert (result == answer)
        result = RiTa.pos("I am a cat.")
        answer = ["prp", "vbp", "dt", "nn", "."]
        assert (result == answer)
        result = RiTa.pos("I was a cat.")
        answer = ["prp", "vbd", "dt", "nn", "."]
        assert (result == answer)
        assert (RiTa.pos("flunk") == ["vb"])
        assert (RiTa.pos("He flunks the test") == ["prp", "vbz", "dt", "nn"])
        assert (RiTa.pos("he") == ["prp"])
        assert (RiTa.pos("outnumber") == ["vb"])
        assert (RiTa.pos("I outnumbered you") == ["prp", "vbd", "prp"])
        assert (RiTa.pos("She outnumbered us") == ["prp", "vbd", "prp"])
        assert (RiTa.pos("I am outnumbering you") == ["prp", "vbp", "vbg", "prp"])
        assert (RiTa.pos("I have outnumbered you") == ["prp", "vbp", "vbd", "prp"])
        checks = ["emphasis", "stress", "discus", "colossus", "fibrosis", "digitalis", "pettiness", "mess", "cleanliness", "orderliness", "bronchitis", "preparedness", "highness"]
        i = 0
        j = len(checks)
        for i in range(0, j, 1):
            assert (RiTa.pos(checks[i]) == ["nn"])
        assert (RiTa.pos("a light blue sky") == ["dt", "jj", "jj", "nn"])
        assert (RiTa.pos("He is running toward me") == ["prp", "vbz", "vbg", "in", "prp"])
        assert (RiTa.pos("She is riding a bike") == ["prp", "vbz", "vbg", "dt", "nn"])
        assert (RiTa.pos("he stands still, thinking about the words") == ["prp", "vbz", "rb", ",", "vbg", "in", "dt", "nns"])
        assert (RiTa.pos("She walked out of the room smoking") == ["prp", "vbd", "in", "in", "dt", "nn", "vbg"])
        assert (RiTa.pos("He kept saying his adventure story") == ["prp", "vbd", "vbg", "prp$", "nn", "nn"])
        assert (RiTa.pos("Drinking is his hobby") == ["vbg", "vbz", "prp$", "nn"])
        assert (RiTa.pos("The kid playing at the corner is the boss") == ["dt", "nn", "vbg", "in", "dt", "nn", "vbz", "dt", "nn"])
        assert (RiTa.pos("She is the leader of the reading group") == ["prp", "vbz", "dt", "nn", "in", "dt", "vbg", "nn"])
        assert (RiTa.pos("I love working") == ["prp", "vbp", "vbg"])
        assert (RiTa.pos("I was thinking about buying a car") == ["prp", "vbd", "vbg", "in", "vbg", "dt", "nn"])
        assert (RiTa.pos("lancer") == ["nn"])
        assert (RiTa.pos("dancer") == ["nn"])
        assert (RiTa.pos("builder") == ["nn"])
        assert (RiTa.pos("programmer") == ["nn"])
        assert (RiTa.pos("mixer") == ["nn"])
        assert (RiTa.pos("He is a dancer") == ["prp", "vbz", "dt", "nn"])
        assert (RiTa.pos("She is a body bulider") == ["prp", "vbz", "dt", "nn", "nn"])
        assert (RiTa.pos("I am a programmer") == ["prp", "vbp", "dt", "nn"])
        assert (RiTa.pos("I have gone alone in there") == ["prp", "vbp", "vbn", "rb", "in", "nn"])
        assert (RiTa.pos("We stopped and went on from there") == ["prp", "vbd", "cc", "vbd", "in", "in", "nn"])
        assert (RiTa.pos("She lives there") == ["prp", "vbz", "rb"])
        assert (RiTa.pos("He was standing there") == ["prp", "vbd", "vbg", "rb"])
        assert (RiTa.pos("There are good reasons to save the world") == ["ex", "vbp", "jj", "nns", "to", "vb", "dt", "nn"])
        assert (RiTa.pos("There is a pig") == ["ex", "vbz", "dt", "nn"])
        assert (RiTa.pos("There isn't a world that is worth saving") == ["ex", "vbz", "dt", "nn", "in", "vbz", "jj", "vbg"])
    def test_should_call_posinline(self):
        result = None
        answer = None
        txt = None
        assert (RiTa.pos_inline("") == "")
        assert (RiTa.pos_inline(" ") == "")
        assert (RiTa.pos_inline("asdfaasd") == "asdfaasd/nn")
        result = RiTa.pos_inline("clothes")
        answer = "clothes/nns"
        assert (result == answer)
        result = RiTa.pos_inline("teeth")
        answer = "teeth/nns"
        assert (result == answer)
        result = RiTa.pos_inline("There is a cat.")
        answer = "There/ex is/vbz a/dt cat/nn ."
        assert (result == answer)
        result = RiTa.pos_inline("The boy, dressed in red, ate an apple.")
        answer = "The/dt boy/nn , dressed/vbn in/in red/jj , ate/vbd an/dt apple/nn ."
        assert (result == answer)
        txt = "The dog ran faster than the other dog.  But the other dog was prettier."
        result = RiTa.pos_inline(txt)
        answer = "The/dt dog/nn ran/vbd faster/rbr than/in the/dt other/jj dog/nn . But/cc the/dt other/jj dog/nn was/vbd prettier/jjr ."
        assert (result == answer)

        txt = "The mosquito bit me."
        result = RiTa.pos_inline(txt)
        answer = "The/dt mosquito/nn bit/vbd me/prp ."
        assert (result == answer)

        txt = "Give the duck a bit of bread."
        result = RiTa.pos_inline(txt)
        answer = "Give/vb the/dt duck/nn a/dt bit/nn of/in bread/nn ."
        assert (result == answer)

        txt = "The show has ended."
        result = RiTa.pos_inline(txt)
        answer = "The/dt show/nn has/vbz ended/vbn ."
        assert (result == answer)

        txt = "She remade this video."
        result = RiTa.pos_inline(txt)
        answer = "She/prp remade/vbd this/dt video/nn ."
        assert (result == answer)

        txt = "They will be remade into something else."
        result = RiTa.pos_inline(txt)
        answer = "They/prp will/md be/vb remade/vbn into/in something/nn else/rb ."
        (0) and (expect(result).eq(answer))

        txt = "She sold her apartment."
        result = RiTa.pos_inline(txt)
        answer = "She/prp sold/vbd her/prp$ apartment/nn ."
        (0) and (expect(result).eq(answer))

        txt = "Her apartment was sold."
        result = RiTa.pos_inline(txt)
        answer = "Her/prp$ apartment/nn was/vbd sold/vbn ."
        assert (result == answer)

        txt = "She resold her apartment."
        result = RiTa.pos_inline(txt)
        answer = "She/prp resold/vbd her/prp$ apartment/nn ."
        assert (result == answer)

        txt = "Her apartment was resold."
        result = RiTa.pos_inline(txt)
        answer = "Her/prp$ apartment/nn was/vbd resold/vbn ."
        (0) and (expect(result).eq(answer))

        txt = "He led a team of crows into battle."
        result = RiTa.pos_inline(txt)
        answer = "He/prp led/vbd a/dt team/nn of/in crows/nns into/in battle/nn ."
        assert (result == answer)

        txt = "He led a team of crows into battle."
        result = RiTa.pos_inline(txt)
        answer = "He/prp led/vbd a/dt team/nn of/in crows/nns into/in battle/nn ."
        assert (result == answer)

    def test_should_call_pos_simple(self):
        result = None
        answer = None
        txt = None
        assert (RiTa.pos("biped", JsDict({"simple": True})) == ["n"])
        assert (RiTa.pos("greed", JsDict({"simple": True})) == ["n"])
        assert (RiTa.pos("creed", JsDict({"simple": True})) == ["n"])
        assert (RiTa.pos("weed", JsDict({"simple": True})) == ["n"])
        assert (RiTa.pos("is", JsDict({"simple": True})) == ["v"])
        assert (RiTa.pos("am", JsDict({"simple": True})) == ["v"])
        assert (RiTa.pos("be", JsDict({"simple": True})) == ["v"])
        assert (RiTa.pos("freed", JsDict({"simple": True})) == ["a"])
        assert (RiTa.pos("the top seed", JsDict({"simple": True})) == ["-", "a", "n"])
        assert (RiTa.pos("", JsDict({"simple": True})) == [])
    def test_should_call_posinline_simple(self):
        result = None
        answer = None
        txt = None
        assert (RiTa.pos_inline("", JsDict({"simple": True})) == "")
        assert (RiTa.pos_inline("asdfaasd", JsDict({"simple": True})) == "asdfaasd/n")
        result = RiTa.pos_inline("clothes", JsDict({"simple": True}))
        answer = "clothes/n"
        assert (result == answer)
        result = RiTa.pos_inline("clothes", JsDict({"simple": True}))
        answer = "clothes/n"
        assert (result == answer)
        result = RiTa.pos_inline("teeth", JsDict({"simple": True}))
        answer = "teeth/n"
        assert (result == answer)
        result = RiTa.pos_inline("There is a cat.", JsDict({"simple": True}))
        answer = "There/- is/v a/- cat/n ."
        assert (result == answer)
        result = RiTa.pos_inline("The boy, dressed in red, ate an apple.", JsDict({"simple": True}))
        answer = "The/- boy/n , dressed/v in/- red/a , ate/v an/- apple/n ."
        assert (result == answer)
        txt = "The dog ran faster than the other dog.  But the other dog was prettier."
        result = RiTa.pos_inline(txt, JsDict({"simple": True}))
        answer = "The/- dog/n ran/v faster/r than/- the/- other/a dog/n . But/- the/- other/a dog/n was/v prettier/a ."
        assert (result == answer)
        result = RiTa.pos_inline("teeth", JsDict({"simple": True}))
        answer = "teeth/n"
        assert (result == answer)
        result = RiTa.pos_inline("There is a cat.", JsDict({"simple": True}))
        answer = "There/- is/v a/- cat/n ."
        assert (result == answer)
        result = RiTa.pos_inline("The boy, dressed in red, ate an apple.", JsDict({"simple": True}))
        answer = "The/- boy/n , dressed/v in/- red/a , ate/v an/- apple/n ."
        assert (result == answer)
        txt = "The dog ran faster than the other dog.  But the other dog was prettier."
        result = RiTa.pos_inline(txt, JsDict({"simple": True}))
        answer = "The/- dog/n ran/v faster/r than/- the/- other/a dog/n . But/- the/- other/a dog/n was/v prettier/a ."
        assert (result == answer)

    def test_should_call_isadverb(self):
        assert ((not (RiTa.is_adverb(""))) is True)
        assert ((not (RiTa.is_adverb())) is True)
        assert ((not (RiTa.is_adverb(42))) is True)
        assert ((not (RiTa.is_adverb(["lively"]))) is True)
        assert ((not (RiTa.is_adverb("swim"))) is True)
        assert ((not (RiTa.is_adverb("walk"))) is True)
        assert ((not (RiTa.is_adverb("walker"))) is True)
        assert ((not (RiTa.is_adverb("beautiful"))) is True)
        assert ((not (RiTa.is_adverb("dance"))) is True)
        assert ((not (RiTa.is_adverb("dancing"))) is True)
        assert ((not (RiTa.is_adverb("dancer"))) is True)
        assert ((not (RiTa.is_adverb("wash"))) is True)
        assert ((not (RiTa.is_adverb("walk"))) is True)
        assert ((not (RiTa.is_adverb("play"))) is True)
        assert ((not (RiTa.is_adverb("throw"))) is True)
        assert ((not (RiTa.is_adverb("drink"))) is True)
        assert ((not (RiTa.is_adverb("eat"))) is True)
        assert ((not (RiTa.is_adverb("chew"))) is True)
        assert ((not (RiTa.is_adverb("wet"))) is True)
        assert ((not (RiTa.is_adverb("dry"))) is True)
        assert ((not (RiTa.is_adverb("furry"))) is True)
        assert ((not (RiTa.is_adverb("sad"))) is True)
        assert ((not (RiTa.is_adverb("happy"))) is True)
        assert ((not (RiTa.is_adverb("dogs"))) is True)
        assert ((not (RiTa.is_adverb("wind"))) is True)
        assert ((not (RiTa.is_adverb("dolls"))) is True)
        assert ((not (RiTa.is_adverb("frogs"))) is True)
        assert ((not (RiTa.is_adverb("ducks"))) is True)
        assert ((not (RiTa.is_adverb("flowers"))) is True)
        assert ((not (RiTa.is_adverb("fish"))) is True)
        assert ((RiTa.is_adverb("truthfully")) is True)
        assert ((RiTa.is_adverb("kindly")) is True)
        assert ((RiTa.is_adverb("bravely")) is True)
        assert ((RiTa.is_adverb("doggedly")) is True)
        assert ((RiTa.is_adverb("sleepily")) is True)
        assert ((RiTa.is_adverb("scarily")) is True)
        assert ((RiTa.is_adverb("excitedly")) is True)
        assert ((RiTa.is_adverb("energetically")) is True)
        assert ((RiTa.is_adverb("hard")) is True)
    def test_should_call_isnoun(self):
        assert ((RiTa.is_noun("thieves")) is True), "thieves"
        assert ((RiTa.is_noun("calves")) is True)
        assert ((not (RiTa.is_noun("scarily"))) is True)
        assert ((RiTa.is_noun("boxes")) is True)
        assert ((RiTa.is_noun("swim")) is True)
        assert ((RiTa.is_noun("walk")) is True)
        assert ((RiTa.is_noun("walker")) is True)
        assert ((RiTa.is_noun("dance")) is True)
        assert ((RiTa.is_noun("dancer")) is True)
        assert ((RiTa.is_noun("cats")) is True)
        assert ((RiTa.is_noun("teeth")) is True)
        assert ((RiTa.is_noun("apples")) is True)
        assert ((RiTa.is_noun("buses")) is True)
        assert ((RiTa.is_noun("prognoses")) is True)
        assert ((RiTa.is_noun("oxen")) is True)
        assert ((RiTa.is_noun("theses")) is True)
        assert ((RiTa.is_noun("stimuli")) is True)
        assert ((RiTa.is_noun("crises")) is True)
        assert ((RiTa.is_noun("wash")) is True)
        assert ((RiTa.is_noun("walk")) is True)
        assert ((RiTa.is_noun("play")) is True)
        assert ((RiTa.is_noun("throw")) is True)
        assert ((RiTa.is_noun("duck")) is True)
        assert ((RiTa.is_noun("dog")) is True)
        assert ((RiTa.is_noun("drink")) is True)
        assert ((not (RiTa.is_noun("abates"))) is True)
        assert ((not (RiTa.is_noun("eat"))) is True)
        assert ((not (RiTa.is_noun("chew"))) is True)
        assert ((not (RiTa.is_noun("moved"))) is True)
        assert ((not (RiTa.is_noun("went"))) is True)
        assert ((not (RiTa.is_noun("spent"))) is True)
        assert ((not (RiTa.is_noun("hard"))) is True)
        assert ((not (RiTa.is_noun("dry"))) is True)
        assert ((not (RiTa.is_noun("furry"))) is True)
        assert ((not (RiTa.is_noun("sad"))) is True)
        assert ((not (RiTa.is_noun("happy"))) is True)
        assert ((not (RiTa.is_noun("beautiful"))) is True)
        assert ((RiTa.is_noun("dogs")) is True)
        assert ((RiTa.is_noun("wind")) is True)
        assert ((RiTa.is_noun("dolls")) is True)
        assert ((RiTa.is_noun("frogs")) is True)
        assert ((RiTa.is_noun("ducks")) is True)
        assert ((RiTa.is_noun("flower")) is True)
        assert ((RiTa.is_noun("fish")) is True)
        assert ((RiTa.is_noun("wet")) is True)
        assert ((RiTa.is_noun("ducks")) is True)
        assert ((RiTa.is_noun("flowers")) is True)
        assert ((not (RiTa.is_noun("truthfully"))) is True)
        assert ((not (RiTa.is_noun("kindly"))) is True)
        assert ((not (RiTa.is_noun("bravely"))) is True)
        assert ((not (RiTa.is_noun("scarily"))) is True)
        assert ((not (RiTa.is_noun("sleepily"))) is True)
        assert ((not (RiTa.is_noun("excitedly"))) is True)
        assert ((not (RiTa.is_noun("energetically"))) is True)
        assert ((not (RiTa.is_noun(""))) is True)
        assert ((not (RiTa.is_noun())) is True)
        assert ((not (RiTa.is_noun(42))) is True)
        assert ((not (RiTa.is_noun(["rabbit"]))) is True)
        assert ((not (RiTa.is_noun("heard"))) is True), _jsstr("heard: ") + _jsstr(RiTa.tagger.all_tags("heard"))
        assert ((not (RiTa.is_noun("deterred"))) is True)
    def test_should_call_isverb(self):
        assert (RiTa.is_verb("abandons") == True)
        assert ((RiTa.is_verb("dance")) is True)
        assert ((RiTa.is_verb("swim")) is True)
        assert ((RiTa.is_verb("walk")) is True)
        assert ((RiTa.is_verb("dances")) is True)
        assert ((RiTa.is_verb("swims")) is True)
        assert ((RiTa.is_verb("walks")) is True)
        assert ((RiTa.is_verb("costs")) is True)
        assert ((RiTa.is_verb("danced")) is True)
        assert ((RiTa.is_verb("swam")) is True)
        assert ((RiTa.is_verb("walked")) is True)
        assert ((RiTa.is_verb("costed")) is True)
        assert ((RiTa.is_verb("satisfies")) is True)
        assert ((RiTa.is_verb("falsifies")) is True)
        assert ((RiTa.is_verb("beautifies")) is True)
        assert ((RiTa.is_verb("repossesses")) is True)
        assert ((not (RiTa.is_verb("dancer"))) is True)
        assert ((not (RiTa.is_verb("walker"))) is True)
        assert ((not (RiTa.is_verb("beautiful"))) is True)
        assert ((RiTa.is_verb("eat")) is True), "eat"
        assert ((RiTa.is_verb("chew")) is True)
        assert ((RiTa.is_verb("throw")) is True)
        assert ((RiTa.is_verb("walk")) is True)
        assert ((RiTa.is_verb("wash")) is True)
        assert ((RiTa.is_verb("drink")) is True)
        assert ((RiTa.is_verb("fish")) is True)
        assert ((RiTa.is_verb("wind")) is True)
        assert ((RiTa.is_verb("wet")) is True)
        assert ((RiTa.is_verb("dry")) is True)
        assert ((not (RiTa.is_verb("hard"))) is True)
        assert ((not (RiTa.is_verb("furry"))) is True)
        assert ((not (RiTa.is_verb("sad"))) is True)
        assert ((not (RiTa.is_verb("happy"))) is True)
        assert ((not (RiTa.is_verb("dolls"))) is True)
        assert ((not (RiTa.is_verb("frogs"))) is True)
        assert ((RiTa.is_verb("flowers")) is True)
        assert ((RiTa.is_verb("ducks")) is True)
        assert ((not (RiTa.is_verb("truthfully"))) is True)
        assert ((not (RiTa.is_verb("kindly"))) is True)
        assert ((not (RiTa.is_verb("bravely"))) is True)
        assert ((not (RiTa.is_verb("scarily"))) is True)
        assert ((not (RiTa.is_verb("sleepily"))) is True)
        assert ((not (RiTa.is_verb("excitedly"))) is True)
        assert ((not (RiTa.is_verb("energetically"))) is True)
        assert ((RiTa.is_verb("hates")) is True)
        assert ((RiTa.is_verb("hated")) is True)
        assert ((RiTa.is_verb("hating")) is True)
        assert ((RiTa.is_verb("dancing")) is True)
        assert ((RiTa.is_verb("flowers")) is True)
        assert ((RiTa.is_verb("hates")) is True)
        assert ((RiTa.is_verb("hated")) is True)
        assert ((RiTa.is_verb("ridden")) is True)
        assert ((RiTa.is_verb("rode")) is True)
        assert ((RiTa.is_verb("abetted")) is True)
        assert ((RiTa.is_verb("abetting")) is True)
        assert ((RiTa.is_verb("abutted")) is True)
        assert ((RiTa.is_verb("abutting")) is True)
        assert ((RiTa.is_verb("abuts")) is True)
        assert ((RiTa.is_verb("abut")) is True)
        assert ((RiTa.is_verb("misdeal")) is True)
        assert ((RiTa.is_verb("misdeals")) is True)
        assert ((RiTa.is_verb("misdealt")) is True)
        assert ((not (RiTa.is_verb(""))) is True)
        assert ((not (RiTa.is_verb())) is True)
        assert ((not (RiTa.is_verb(42))) is True)
        assert ((not (RiTa.is_verb(["work"]))) is True)
    def test_should_call_isadjective(self):
        assert ((not (RiTa.is_adjective("swim"))) is True)
        assert ((not (RiTa.is_adjective("walk"))) is True)
        assert ((not (RiTa.is_adjective("walker"))) is True)
        assert ((RiTa.is_adjective("beautiful")) is True)
        assert ((not (RiTa.is_adjective("dance"))) is True)
        assert ((not (RiTa.is_adjective("dancing"))) is True)
        assert ((not (RiTa.is_adjective("dancer"))) is True)
        assert ((not (RiTa.is_adjective("wash"))) is True)
        assert ((not (RiTa.is_adjective("walk"))) is True)
        assert ((not (RiTa.is_adjective("play"))) is True)
        assert ((not (RiTa.is_adjective("throw"))) is True)
        assert ((not (RiTa.is_adjective("drink"))) is True)
        assert ((not (RiTa.is_adjective("eat"))) is True)
        assert ((not (RiTa.is_adjective("chew"))) is True)
        assert ((RiTa.is_adjective("hard")) is True)
        assert ((RiTa.is_adjective("wet")) is True)
        assert ((RiTa.is_adjective("dry")) is True)
        assert ((RiTa.is_adjective("furry")) is True)
        assert ((RiTa.is_adjective("sad")) is True)
        assert ((RiTa.is_adjective("happy")) is True)
        assert ((RiTa.is_adjective("kindly")) is True)
        assert ((not (RiTa.is_adjective("dogs"))) is True)
        assert ((not (RiTa.is_adjective("wind"))) is True)
        assert ((not (RiTa.is_adjective("dolls"))) is True)
        assert ((not (RiTa.is_adjective("frogs"))) is True)
        assert ((not (RiTa.is_adjective("ducks"))) is True)
        assert ((not (RiTa.is_adjective("flowers"))) is True)
        assert ((not (RiTa.is_adjective("fish"))) is True)
        assert ((not (RiTa.is_adjective("truthfully"))) is True)
        assert ((not (RiTa.is_adjective("bravely"))) is True)
        assert ((not (RiTa.is_adjective("scarily"))) is True)
        assert ((not (RiTa.is_adjective("sleepily"))) is True)
        assert ((not (RiTa.is_adjective("excitedly"))) is True)
        assert ((not (RiTa.is_adjective("energetically"))) is True)
        assert ((not (RiTa.is_adjective(""))) is True)
        assert ((not (RiTa.is_adjective())) is True)
        assert ((not (RiTa.is_adjective(42))) is True)
        assert ((not (RiTa.is_adjective(["happy"]))) is True)
    def test_should_call_alltags(self):
        assert (RiTa.tagger.all_tags("monkey") == ["nn"])
        assert (RiTa.tagger.all_tags("monkeys") == ["nns"])
        assert (RiTa.tagger.all_tags("") == [])
        assert (RiTa.tagger.all_tags(["monkey"]) == [])
        assert (RiTa.tagger.all_tags("hates", JsDict({"noDerivations": True})) == [])
        assert (RiTa.tagger.all_tags("satisfies") == ["vbz"])
        assert (RiTa.tagger.all_tags("falsifies") == ["vbz"])
        assert ("vbz" in RiTa.tagger.all_tags("hates"))
        assert ("nns" in RiTa.tagger.all_tags("hates"))
        assert ("nns" in RiTa.tagger.all_tags("cakes"))
        assert ("vbz" in RiTa.tagger.all_tags("repossesses"))
        assert ("nns" in RiTa.tagger.all_tags("thieves"))
        assert ("vbz" in RiTa.tagger.all_tags("thieves"))
        assert ("vbd" in RiTa.tagger.all_tags("hated"))
        assert ("vbn" in RiTa.tagger.all_tags("hated"))
        assert ("vbd" in RiTa.tagger.all_tags("owed"))
        assert ("vbn" in RiTa.tagger.all_tags("owed"))
        assert ("vbg" in RiTa.tagger.all_tags("assenting"))
        assert ("vbg" in RiTa.tagger.all_tags("hating"))
        assert ("nns" in RiTa.tagger.all_tags("feet"))
        assert ("nns" in RiTa.tagger.all_tags("men"))
        assert ("nn" in RiTa.tagger.all_tags("ashdj"))
        assert ("rb" in RiTa.tagger.all_tags("kahsdly"))
        assert ("nns" in RiTa.tagger.all_tags("asdkasws"))
        assert (RiTa.tagger.all_tags("bit") == ["vbd", "nn", "rb"])
        assert (RiTa.tagger.all_tags("broke") == ["vbd", "jj", "rb"])
        assert (RiTa.tagger.all_tags("called") == ["vbd", "vbn"])
        assert (RiTa.tagger.all_tags("committed") == ["vbn", "jj", "vbd"])
        assert (RiTa.tagger.all_tags("computerized") == ["jj", "vbd", "vbn"])
        assert (RiTa.tagger.all_tags("concerned") == ["vbd", "jj", "vbn"])

        assert (RiTa.tagger.all_tags("discriminated") == ["vbd", "vbn", "jj"])
        assert (RiTa.tagger.all_tags("ended") == ["vbd", "jj", "vbn"])
        assert (RiTa.tagger.all_tags("expected") == ["vbn", "vbd", "jj"])
        assert (RiTa.tagger.all_tags("finished") == ["vbd", "jj", "vbn"])
        assert (RiTa.tagger.all_tags("gained") == ["vbd", "vbn"])
        assert (RiTa.tagger.all_tags("got") == ["vbd", "vbn"])
        assert (RiTa.tagger.all_tags("increased") == ["vbn", "jj", "vbd"])
        assert (RiTa.tagger.all_tags("involved") == ["vbn", "vbd", "jj"])
        assert (RiTa.tagger.all_tags("launched") == ["vbn", "vbd"])
        assert (RiTa.tagger.all_tags("led") == ["vbd", "vbn"])
        assert (RiTa.tagger.all_tags("lived") == ["vbd", "vbn"])
        assert (RiTa.tagger.all_tags("oversaw") == ["vbd"])
        assert (RiTa.tagger.all_tags("paled") == ["vbd", "vbn"])
        assert (RiTa.tagger.all_tags("prepaid") == ["jj", "vbd", "vbn"])

        assert (RiTa.tagger.all_tags("pressured") == ["vbn", "jj", "vbd"])
        assert (RiTa.tagger.all_tags("proliferated") == ["vbn", "vbd"])
        assert (RiTa.tagger.all_tags("remade") == ["vbd", "vbn"])
        assert (RiTa.tagger.all_tags("reopened") == ["vbd", "vbn"])
        assert (RiTa.tagger.all_tags("reported") == ["vbd", "jj", "vbn"])
        assert (RiTa.tagger.all_tags("resold") == ["vbd", "vbn"])
        assert (RiTa.tagger.all_tags("settled") == ["vbd", "vbn", "jj"])
        assert (RiTa.tagger.all_tags("started") == ["vbd", "jj", "vbn"])
    def test_should_call_hastag(self):
        assert ((not (RiTa.tagger.has_tag())) is True)
        assert ((not (RiTa.tagger.has_tag("nn adj", "nn"))) is True)
        assert ((RiTa.tagger.has_tag(RiTa.tagger.all_tags("monkey"), "nn")) is True)
    def test_should_call_inlinetags(self):
        assert (RiTa.tagger.inline_tags() == "")
        assert (RiTa.tagger.inline_tags([]) == "")
        with pytest.raises(Exception):
            RiTa.tagger.inline_tags(["I", "am", "Pikachu"], [], "/")
        assert (RiTa.tagger.inline_tags(["I", "am", "happy", "."], ["prp", "vbp", "jj", "."]) == "I/prp am/vbp happy/jj .")
        assert (RiTa.tagger.inline_tags(["I", "am", "happy", "."], ["prp", "vbp", "jj", "."], ";") == "I;prp am;vbp happy;jj .")
    def test_should_call_tag(self):
        assert (RiTa.tagger.tag([]) == [])
        assert (RiTa.tagger.tag() == [])
        assert (RiTa.tagger.tag([], JsDict({"inline": True})) == "")
        assert (RiTa.tagger.tag(["I", "am", "happy", "."], JsDict({"simple": True})) == ["-", "v", "a", "-"])
        assert (RiTa.tagger.tag(["I", "am", "happy", "."], JsDict({"simple": True, "inline": True})) == "I/- am/v happy/a .")
        assert (RiTa.tagger.tag(["I", "roll", "a", "9", "."], JsDict({"inline": True})) == "I/prp roll/vbp a/dt 9/cd .")
        assert (RiTa.tagger.tag(["A", "badguy", "."], JsDict({"inline": True})) == "A/dt badguy/nn .")
        assert (RiTa.tagger.tag(["A", "C", "level", "grade", "."], JsDict({"inline": True})) == "A/dt C/C level/jj grade/nn .")
        assert (RiTa.tagger.tag(["The", "run", "was", "great", "."], JsDict({"inline": True})) == "The/dt run/nn was/vbd great/jj .")
        assert (RiTa.tagger.tag(["They", "are", "the", "beaten", "."], JsDict({"inline": True})) == "They/prp are/vbp the/dt beaten/nn .")
        assert (RiTa.tagger.tag(["A", "diss", "."], JsDict({"inline": True})) == "A/dt diss/nns .")
        assert (RiTa.tagger.tag(["The", "soon", "."], JsDict({"inline": True})) == "The/dt soon/jj .")
        assert (RiTa.tagger.tag(["The", "sooner", "."], JsDict({"inline": True})) == "The/dt sooner/jjr .")
        assert (RiTa.tagger.tag(["The", "soonest", "."], JsDict({"inline": True})) == "The/dt soonest/jjs .")
        assert (RiTa.tagger.tag(["It", "is", "59876", "."], JsDict({"inline": True})) == "It/prp is/vbz 59876/cd .")
        assert (RiTa.tagger.tag(["I", "teabaged", "."], JsDict({"inline": True})) == "I/prp teabaged/vbn .")
        assert (RiTa.tagger.tag(["Sun", "teabaged", "."], JsDict({"inline": True})) == "Sun/nn teabaged/vbn .")
        assert (RiTa.tagger.tag(["The", "worker", "proletarianized", "."], JsDict({"inline": True})) == "The/dt worker/nn proletarianized/vbn .")
        assert (RiTa.tagger.tag(["The", "fortunately", "."], JsDict({"inline": True})) == "The/dt fortunately/rb .")
        assert (RiTa.tagger.tag(["He", "is", "goodly", "working", "."], JsDict({"inline": True})) == "He/prp is/vbz goodly/rb working/vbg .")
        assert (RiTa.tagger.tag(["It", "is", "nonexistional", "."], JsDict({"inline": True})) == "It/prp is/vbz nonexistional/jj .")
        assert (RiTa.tagger.tag(["It", "is", "mammal", "."], JsDict({"inline": True})) == "It/prp is/vbz mammal/nn .")
        assert (RiTa.tagger.tag(["It", "is", "onal", "."], JsDict({"inline": True})) == "It/prp is/vbz onal/nn .")
        assert (RiTa.tagger.tag(["We", "must", "place", "it", "."], JsDict({"inline": True})) == "We/prp must/md place/vb it/prp .")
        assert (RiTa.tagger.tag(["We", "must", "teabag", "him", "."], JsDict({"inline": True})) == "We/prp must/md teabag/vb him/prp .")
        assert (RiTa.tagger.tag(["He", "has", "played", "it", "."], JsDict({"inline": True})) == "He/prp has/vbz played/vbn it/prp .")
        assert (RiTa.tagger.tag(["He", "gets", "played", "."], JsDict({"inline": True})) == "He/prp gets/vbz played/vbn .")
        assert (RiTa.tagger.tag(["The", "morning", "."], JsDict({"inline": True})) == "The/dt morning/nn .")
        assert (RiTa.tagger.tag(["They", "are", "fishing", "."], JsDict({"inline": True})) == "They/prp are/vbp fishing/vbg .")
        assert (RiTa.tagger.tag(["He", "dances", "."], JsDict({"inline": True})) == "He/prp dances/vbz .")
        assert (RiTa.tagger.tag(["The", "dog", "dances", "."], JsDict({"inline": True})) == "The/dt dog/nn dances/vbz .")
        assert (RiTa.tagger.tag(["Dave", "dances", "."], JsDict({"inline": True})) == "Dave/nnp dances/vbz .")
        assert (RiTa.tagger.tag(["Taipei", "."], JsDict({"inline": True})) == "Taipei/nnp .")
        assert (RiTa.tagger.tag(["Buddhas", "."], JsDict({"inline": True})) == "Buddhas/nnps .")
        assert (RiTa.tagger.tag(["In", "Beijing", "."], JsDict({"inline": True})) == "In/in Beijing/nnp .")
        assert (RiTa.tagger.tag(["One", "of", "the", "Beats", "."], JsDict({"inline": True})) == "One/cd of/in the/dt Beats/nnps .")
        assert (RiTa.tagger.tag(["Taipei", "is", "a", "big", "city", "."], JsDict({"inline": True})) == "Taipei/nnp is/vbz a/dt big/jj city/nn .")
        assert (RiTa.tagger.tag(["Buddhas", "in", "this", "temple", "have", "a", "history", "of", "500", "years", "."], JsDict({"inline": True})) == "Buddhas/nnps in/in this/dt temple/nn have/vbp a/dt history/nn of/in 500/cd years/nns .")
        assert (RiTa.tagger.tag(["Balls", "on", "the", "floor", "."], JsDict({"inline": True})) == "Balls/nns on/in the/dt floor/nn .")
        assert (RiTa.tagger.tag(["dances", "."], JsDict({"inline": True})) == "dances/nns .")
        assert (RiTa.tagger.tag(["dances", "and", "performances", "."], JsDict({"inline": True})) == "dances/nns and/cc performances/nns .")
        assert (RiTa.tagger.tag(["cakes", "quickly", "."], JsDict({"inline": True})) == "cakes/nns quickly/rb .")
        assert (RiTa.tagger.tag(["dances", "quickly", "."], JsDict({"inline": True})) == "dances/vbz quickly/rb .")
        assert (RiTa.tagger.tag(["David", "cakes", "."], JsDict({"inline": True})) == "David/nnp cakes/nns .")
        assert (RiTa.tagger.tag(["David", "laughs", "and", "dances", "."], JsDict({"inline": True})) == "David/nnp laughs/vbz and/cc dances/vbz .")
        assert (RiTa.tagger.tag(["counterattacks", "."], JsDict({"inline": True})) == "counterattacks/nns .")
        assert (RiTa.tagger.tag(["Monkeys", "run", "."], JsDict({"inline": True})) == "Monkeys/nns run/vbp .")
        assert (RiTa.tagger.tag(["Monkeys", "attack", "."], JsDict({"inline": True})) == "Monkeys/nns attack/vbp .")
        assert (RiTa.tagger.tag(["A", "light", "blue", "sky", "."], JsDict({"inline": True})) == "A/dt light/jj blue/jj sky/nn .")
        assert (RiTa.tagger.tag(["It", "broke", "."], JsDict({"inline": True})) == "It/prp broke/vbd .")
        assert (RiTa.tagger.tag(["It", "outpaced", "that", "."], JsDict({"inline": True})) == "It/prp outpaced/vbd that/in .")
        assert (RiTa.tagger.tag(["She", "remade", "this", "video", "."], JsDict({"inline": True})) == "She/prp remade/vbd this/dt video/nn .")
        assert (RiTa.tagger.tag(["She", "has", "remade", "this", "video", "."], JsDict({"inline": True})) == "She/prp has/vbz remade/vbn this/dt video/nn .")
        (0) and (expect(RiTa.tagger.tag(["The", "video", "was", "remade", "."], JsDict({"inline": True}))).eq("The/dt video/nn was/vbd remade/vbn ."))
        (0) and (expect(RiTa.tagger.tag(["Being", "literate", "didn't", "stop", "him", "from", "being", "discriminated", "against", "."], JsDict({"inline": True}))).eq("Being/vbg literate/jj didn't/vbd stop/vb him/prp from/in being/vbg discriminated/vbn against/in ."))
    def test_should_handle_hyphenated_words(self):
        pool = ["He is my father-in-law.", "We have a off-site meeting yesterday.", "I know a great place for an off-site.", "a state-of-the-art computer", "The girls wanted the merry-go-round to go faster.", "He ate twenty-one burgers today.", "The politician arrived by high-speed railway.", "People doing yoga benefit from an increased feeling of well-being.", "There is a life-size statue of the dragon in the park.", "He has a king-size bed in his room.", "I am taking a full-time job now", "The cost for the round-trip ticket is 2000 dollars.", "The cost is 2000 dollars for the round-trip.", "He come back empty-handed", "She is left-handed", "I like the dress of the long-haired girl in the photo.", "His move was breath-taking.", "Snakes are cold-blooded.", "People liked to wear bell-bottoms in the 80s.", "This shop mainly sells corn-fed meat.", "I withdraw the application and re-apply for another position.", "Our co-manager believe in neo-liberalism.", "He did a u-turn.", "We are not going to get down to the nitty-gritty analysis of value for money.", "The game require co-op with your teammates.", "He was a roly-poly little man."]
        answers = [["prp", "vbz", "prp$", "nn", "."], ["prp", "vbp", "dt", "jj", "vbg", "nn", "."], ["prp", "vbp", "dt", "jj", "nn", "in", "dt", "nn", "."], ["dt", "jj", "nn"], ["dt", "nns", "vbd", "dt", "nn", "to", "vb", "rbr", "."], ["prp", "vbd", "cd", "nns", "nn", "."], ["dt", "nn", "vbd", "in", "jj", "nn", "."], ["nn", "vbg", "nn", "nn", "in", "dt", "jj", "vbg", "in", "nn", "."], ["ex", "vbz", "dt", "jj", "nn", "in", "dt", "nn", "in", "dt", "nn", "."], ["prp", "vbz", "dt", "jj", "nn", "in", "prp$", "nn", "."], ["prp", "vbp", "vbg", "dt", "jj", "nn", "rb"], ["dt", "nn", "in", "dt", "jj", "nn", "vbz", "cd", "nns", "."], ["dt", "nn", "vbz", "cd", "nns", "in", "dt", "nn", "."], ["prp", "vbp", "rb", "jj"], ["prp", "vbz", "jj"], ["prp", "vbp", "dt", "nn", "in", "dt", "jj", "nn", "in", "dt", "nn", "."], ["prp$", "nn", "vbd", "jj", "."], ["nns", "vbp", "jj", "."], ["nn", "vbd", "to", "vb", "nn", "in", "dt", "nns", "."], ["dt", "nn", "rb", "nns", "jj", "nn", "."], ["prp", "vbp", "dt", "nn", "cc", "vb", "in", "dt", "nn", "."], ["prp$", "nn", "vbp", "in", "nn", "."], ["prp", "vbd", "dt", "nn", "."], ["prp", "vbp", "rb", "vbg", "to", "vb", "rb", "to", "dt", "nn", "nn", "in", "nn", "in", "nn", "."], ["dt", "nn", "vb", "nn", "in", "prp$", "nns", "."], ["prp", "vbd", "dt", "jj", "jj", "nn", "."]]
        for i, a in enumerate(answers):
            assert (RiTa.pos(pool[i]) == a)

hasLex = True

def _fn_1(*args):
    RiTa.tagger.inline_tags(["I", "am", "Pikachu"], [], "/")

