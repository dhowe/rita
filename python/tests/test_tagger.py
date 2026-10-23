# AUTO-GENERATED from js/test/tagger-tests.js by scripts/js-to-py-tests.js — do not edit by hand.
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
    RiTa.tagger.inlineTags(["I", "am", "Pikachu"], [], "/")

class TestTagger:
    hasLex = True
    def test_should_call_pos_array(self):
        if not (hasLex):
            pytest.skip("mocha this.skip")
        assert (RiTa.pos([]) == [])
        assert (RiTa.pos(["deal"]) == ["nn"])
        assert (RiTa.pos(["freed"]) == ["jj"])
        assert (RiTa.pos(["the"]) == ["dt"])
        assert (RiTa.pos(["a"]) == ["dt"])
        assert (RiTa.pos("the top seed".split(__re_compile(" "))) == ["dt", "jj", "nn"])
        assert (RiTa.pos("by illegal means".split(__re_compile(" "))) == ["in", "jj", "nn"])
        assert (RiTa.pos("He outnumbers us".split(__re_compile(" "))) == ["prp", "vbz", "prp"])
        assert (RiTa.pos("I outnumber you".split(__re_compile(" "))) == ["prp", "vbp", "prp"])
        assert (RiTa.pos("Elephants dance".split(__re_compile(" "))) == ["nns", "vbp"])
        assert (RiTa.pos("the boy dances".split(__re_compile(" "))) == ["dt", "nn", "vbz"])
        assert (RiTa.pos("Dave dances".split(__re_compile(" "))) == ["nnp", "vbz"])
    def test_should_call_simple_pos_array(self):
        assert (RiTa.pos([], {"simple": True}) == [])
        assert (RiTa.pos(["freed"], {"simple": True}) == ["a"])
        assert (RiTa.pos(["the"], {"simple": True}) == ["-"])
        assert (RiTa.pos(["a"], {"simple": True}) == ["-"])
        assert (RiTa.pos("the top seed".split(__re_compile(" ")), {"simple": True}) == ["-", "a", "n"])
        assert (RiTa.pos("by illegal means".split(__re_compile(" ")), {"simple": True}) == ["-", "a", "n"])
        assert (RiTa.pos("He outnumbers us".split(__re_compile(" ")), {"simple": True}) == ["-", "v", "-"])
        assert (RiTa.pos("I outnumber you".split(__re_compile(" ")), {"simple": True}) == ["-", "v", "-"])
        assert (RiTa.pos("Elephants dance".split(__re_compile(" ")), {"simple": True}) == ["n", "v"])
        assert (RiTa.pos("the boy dances".split(__re_compile(" ")), {"simple": True}) == ["-", "n", "v"])
    def test_should_call_posinline_array_simple(self):
        result = None
        answer = None
        txt = None
        assert (RiTa.posInline([], {"simple": True}) == "")
        assert (RiTa.posInline(["asdfaasd"], {"simple": True}) == "asdfaasd/n")
        result = RiTa.posInline(["clothes"], {"simple": True})
        answer = "clothes/n"
        assert (result == answer)
        result = RiTa.posInline(["teeth"], {"simple": True})
        answer = "teeth/n"
        assert (result == answer)
        result = RiTa.posInline("There is a cat".split(__re_compile(" ")), {"simple": True})
        answer = "There/- is/v a/- cat/n"
        assert (result == answer)
        result = RiTa.posInline(RiTa.tokenize("The boy, dressed in red, ate an apple."), {"simple": True})
        answer = "The/- boy/n , dressed/v in/- red/a , ate/v an/- apple/n ."
        assert (result == answer)
        txt = "The dog ran faster than the other dog. But the other dog was prettier."
        result = RiTa.posInline(RiTa.tokenize(txt), {"simple": True})
        answer = "The/- dog/n ran/v faster/r than/- the/- other/a dog/n . But/- the/- other/a dog/n was/v prettier/a ."
        assert (result == answer)

    def test_should_handle_inflected_verbs(self):
        assert (RiTa.pos("disbelieves") == ["vbz"])
        assert (RiTa.pos("disbelieves", {"simple": 1}) == ["v"])
        assert (RiTa.pos("fates") == ["nns"])
        assert (RiTa.pos("fates", {"simple": 1}) == ["n"])
        assert (RiTa.pos("hates") == ["vbz"])
        assert (RiTa.pos("hates", {"simple": 1}) == ["v"])
        assert (RiTa.pos("hated") == ["vbd"])
        assert (RiTa.pos("hated", {"simple": 1}) == ["v"])
        assert (RiTa.pos("hating") == ["vbg"])
        assert (RiTa.pos("hating", {"simple": 1}) == ["v"])
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
        assert (RiTa.pos("broke", {"simple": 1}) == ["v"])
        assert (RiTa.pos("committed") == ["vbn"])
        assert (RiTa.pos("committed", {"simple": 1}) == ["v"])
        assert (RiTa.pos("outpaced") == ["vbd"])
        assert (RiTa.pos("outpaced", {"simple": 1}) == ["v"])
        assert (RiTa.pos("concerned") == ["vbd"])
        assert (RiTa.pos("concerned", {"simple": 1}) == ["v"])
        assert (RiTa.pos("committed") == ["vbn"])
        assert (RiTa.pos("committed", {"simple": 1}) == ["v"])
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
        for i in range(j):
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
        assert (RiTa.posInline("") == "")
        assert (RiTa.posInline(" ") == "")
        assert (RiTa.posInline("asdfaasd") == "asdfaasd/nn")
        result = RiTa.posInline("clothes")
        answer = "clothes/nns"
        assert (result == answer)
        result = RiTa.posInline("teeth")
        answer = "teeth/nns"
        assert (result == answer)
        result = RiTa.posInline("There is a cat.")
        answer = "There/ex is/vbz a/dt cat/nn ."
        assert (result == answer)
        result = RiTa.posInline("The boy, dressed in red, ate an apple.")
        answer = "The/dt boy/nn , dressed/vbn in/in red/jj , ate/vbd an/dt apple/nn ."
        assert (result == answer)
        txt = "The dog ran faster than the other dog.  But the other dog was prettier."
        result = RiTa.posInline(txt)
        answer = "The/dt dog/nn ran/vbd faster/rbr than/in the/dt other/jj dog/nn . But/cc the/dt other/jj dog/nn was/vbd prettier/jjr ."
        assert (result == answer)

        txt = "The mosquito bit me."
        result = RiTa.posInline(txt)
        answer = "The/dt mosquito/nn bit/vbd me/prp ."
        assert (result == answer)

        txt = "Give the duck a bit of bread."
        result = RiTa.posInline(txt)
        answer = "Give/vb the/dt duck/nn a/dt bit/nn of/in bread/nn ."
        assert (result == answer)

        txt = "The show has ended."
        result = RiTa.posInline(txt)
        answer = "The/dt show/nn has/vbz ended/vbn ."
        assert (result == answer)

        txt = "She remade this video."
        result = RiTa.posInline(txt)
        answer = "She/prp remade/vbd this/dt video/nn ."
        assert (result == answer)

        txt = "They will be remade into something else."
        result = RiTa.posInline(txt)
        answer = "They/prp will/md be/vb remade/vbn into/in something/nn else/rb ."
        (0) and (expect(result).eq(answer))

        txt = "She sold her apartment."
        result = RiTa.posInline(txt)
        answer = "She/prp sold/vbd her/prp$ apartment/nn ."
        (0) and (expect(result).eq(answer))

        txt = "Her apartment was sold."
        result = RiTa.posInline(txt)
        answer = "Her/prp$ apartment/nn was/vbd sold/vbn ."
        assert (result == answer)

        txt = "She resold her apartment."
        result = RiTa.posInline(txt)
        answer = "She/prp resold/vbd her/prp$ apartment/nn ."
        assert (result == answer)

        txt = "Her apartment was resold."
        result = RiTa.posInline(txt)
        answer = "Her/prp$ apartment/nn was/vbd resold/vbn ."
        (0) and (expect(result).eq(answer))

        txt = "He led a team of crows into battle."
        result = RiTa.posInline(txt)
        answer = "He/prp led/vbd a/dt team/nn of/in crows/nns into/in battle/nn ."
        assert (result == answer)

        txt = "He led a team of crows into battle."
        result = RiTa.posInline(txt)
        answer = "He/prp led/vbd a/dt team/nn of/in crows/nns into/in battle/nn ."
        assert (result == answer)

    def test_should_call_pos_simple(self):
        result = None
        answer = None
        txt = None
        assert (RiTa.pos("biped", {"simple": True}) == ["n"])
        assert (RiTa.pos("greed", {"simple": True}) == ["n"])
        assert (RiTa.pos("creed", {"simple": True}) == ["n"])
        assert (RiTa.pos("weed", {"simple": True}) == ["n"])
        assert (RiTa.pos("is", {"simple": True}) == ["v"])
        assert (RiTa.pos("am", {"simple": True}) == ["v"])
        assert (RiTa.pos("be", {"simple": True}) == ["v"])
        assert (RiTa.pos("freed", {"simple": True}) == ["a"])
        assert (RiTa.pos("the top seed", {"simple": True}) == ["-", "a", "n"])
        assert (RiTa.pos("", {"simple": True}) == [])
    def test_should_call_posinline_simple(self):
        result = None
        answer = None
        txt = None
        assert (RiTa.posInline("", {"simple": True}) == "")
        assert (RiTa.posInline("asdfaasd", {"simple": True}) == "asdfaasd/n")
        result = RiTa.posInline("clothes", {"simple": True})
        answer = "clothes/n"
        assert (result == answer)
        result = RiTa.posInline("clothes", {"simple": True})
        answer = "clothes/n"
        assert (result == answer)
        result = RiTa.posInline("teeth", {"simple": True})
        answer = "teeth/n"
        assert (result == answer)
        result = RiTa.posInline("There is a cat.", {"simple": True})
        answer = "There/- is/v a/- cat/n ."
        assert (result == answer)
        result = RiTa.posInline("The boy, dressed in red, ate an apple.", {"simple": True})
        answer = "The/- boy/n , dressed/v in/- red/a , ate/v an/- apple/n ."
        assert (result == answer)
        txt = "The dog ran faster than the other dog.  But the other dog was prettier."
        result = RiTa.posInline(txt, {"simple": True})
        answer = "The/- dog/n ran/v faster/r than/- the/- other/a dog/n . But/- the/- other/a dog/n was/v prettier/a ."
        assert (result == answer)
        result = RiTa.posInline("teeth", {"simple": True})
        answer = "teeth/n"
        assert (result == answer)
        result = RiTa.posInline("There is a cat.", {"simple": True})
        answer = "There/- is/v a/- cat/n ."
        assert (result == answer)
        result = RiTa.posInline("The boy, dressed in red, ate an apple.", {"simple": True})
        answer = "The/- boy/n , dressed/v in/- red/a , ate/v an/- apple/n ."
        assert (result == answer)
        txt = "The dog ran faster than the other dog.  But the other dog was prettier."
        result = RiTa.posInline(txt, {"simple": True})
        answer = "The/- dog/n ran/v faster/r than/- the/- other/a dog/n . But/- the/- other/a dog/n was/v prettier/a ."
        assert (result == answer)

    def test_should_call_isadverb(self):
        assert ((not (RiTa.isAdverb(""))) is True)
        assert ((not (RiTa.isAdverb())) is True)
        assert ((not (RiTa.isAdverb(42))) is True)
        assert ((not (RiTa.isAdverb(["lively"]))) is True)
        assert ((not (RiTa.isAdverb("swim"))) is True)
        assert ((not (RiTa.isAdverb("walk"))) is True)
        assert ((not (RiTa.isAdverb("walker"))) is True)
        assert ((not (RiTa.isAdverb("beautiful"))) is True)
        assert ((not (RiTa.isAdverb("dance"))) is True)
        assert ((not (RiTa.isAdverb("dancing"))) is True)
        assert ((not (RiTa.isAdverb("dancer"))) is True)
        assert ((not (RiTa.isAdverb("wash"))) is True)
        assert ((not (RiTa.isAdverb("walk"))) is True)
        assert ((not (RiTa.isAdverb("play"))) is True)
        assert ((not (RiTa.isAdverb("throw"))) is True)
        assert ((not (RiTa.isAdverb("drink"))) is True)
        assert ((not (RiTa.isAdverb("eat"))) is True)
        assert ((not (RiTa.isAdverb("chew"))) is True)
        assert ((not (RiTa.isAdverb("wet"))) is True)
        assert ((not (RiTa.isAdverb("dry"))) is True)
        assert ((not (RiTa.isAdverb("furry"))) is True)
        assert ((not (RiTa.isAdverb("sad"))) is True)
        assert ((not (RiTa.isAdverb("happy"))) is True)
        assert ((not (RiTa.isAdverb("dogs"))) is True)
        assert ((not (RiTa.isAdverb("wind"))) is True)
        assert ((not (RiTa.isAdverb("dolls"))) is True)
        assert ((not (RiTa.isAdverb("frogs"))) is True)
        assert ((not (RiTa.isAdverb("ducks"))) is True)
        assert ((not (RiTa.isAdverb("flowers"))) is True)
        assert ((not (RiTa.isAdverb("fish"))) is True)
        assert ((RiTa.isAdverb("truthfully")) is True)
        assert ((RiTa.isAdverb("kindly")) is True)
        assert ((RiTa.isAdverb("bravely")) is True)
        assert ((RiTa.isAdverb("doggedly")) is True)
        assert ((RiTa.isAdverb("sleepily")) is True)
        assert ((RiTa.isAdverb("scarily")) is True)
        assert ((RiTa.isAdverb("excitedly")) is True)
        assert ((RiTa.isAdverb("energetically")) is True)
        assert ((RiTa.isAdverb("hard")) is True)
    def test_should_call_isnoun(self):
        assert ((RiTa.isNoun("thieves")) is True), "thieves"
        assert ((RiTa.isNoun("calves")) is True)
        assert ((not (RiTa.isNoun("scarily"))) is True)
        assert ((RiTa.isNoun("boxes")) is True)
        assert ((RiTa.isNoun("swim")) is True)
        assert ((RiTa.isNoun("walk")) is True)
        assert ((RiTa.isNoun("walker")) is True)
        assert ((RiTa.isNoun("dance")) is True)
        assert ((RiTa.isNoun("dancer")) is True)
        assert ((RiTa.isNoun("cats")) is True)
        assert ((RiTa.isNoun("teeth")) is True)
        assert ((RiTa.isNoun("apples")) is True)
        assert ((RiTa.isNoun("buses")) is True)
        assert ((RiTa.isNoun("prognoses")) is True)
        assert ((RiTa.isNoun("oxen")) is True)
        assert ((RiTa.isNoun("theses")) is True)
        assert ((RiTa.isNoun("stimuli")) is True)
        assert ((RiTa.isNoun("crises")) is True)
        assert ((RiTa.isNoun("wash")) is True)
        assert ((RiTa.isNoun("walk")) is True)
        assert ((RiTa.isNoun("play")) is True)
        assert ((RiTa.isNoun("throw")) is True)
        assert ((RiTa.isNoun("duck")) is True)
        assert ((RiTa.isNoun("dog")) is True)
        assert ((RiTa.isNoun("drink")) is True)
        assert ((not (RiTa.isNoun("abates"))) is True)
        assert ((not (RiTa.isNoun("eat"))) is True)
        assert ((not (RiTa.isNoun("chew"))) is True)
        assert ((not (RiTa.isNoun("moved"))) is True)
        assert ((not (RiTa.isNoun("went"))) is True)
        assert ((not (RiTa.isNoun("spent"))) is True)
        assert ((not (RiTa.isNoun("hard"))) is True)
        assert ((not (RiTa.isNoun("dry"))) is True)
        assert ((not (RiTa.isNoun("furry"))) is True)
        assert ((not (RiTa.isNoun("sad"))) is True)
        assert ((not (RiTa.isNoun("happy"))) is True)
        assert ((not (RiTa.isNoun("beautiful"))) is True)
        assert ((RiTa.isNoun("dogs")) is True)
        assert ((RiTa.isNoun("wind")) is True)
        assert ((RiTa.isNoun("dolls")) is True)
        assert ((RiTa.isNoun("frogs")) is True)
        assert ((RiTa.isNoun("ducks")) is True)
        assert ((RiTa.isNoun("flower")) is True)
        assert ((RiTa.isNoun("fish")) is True)
        assert ((RiTa.isNoun("wet")) is True)
        assert ((RiTa.isNoun("ducks")) is True)
        assert ((RiTa.isNoun("flowers")) is True)
        assert ((not (RiTa.isNoun("truthfully"))) is True)
        assert ((not (RiTa.isNoun("kindly"))) is True)
        assert ((not (RiTa.isNoun("bravely"))) is True)
        assert ((not (RiTa.isNoun("scarily"))) is True)
        assert ((not (RiTa.isNoun("sleepily"))) is True)
        assert ((not (RiTa.isNoun("excitedly"))) is True)
        assert ((not (RiTa.isNoun("energetically"))) is True)
        assert ((not (RiTa.isNoun(""))) is True)
        assert ((not (RiTa.isNoun())) is True)
        assert ((not (RiTa.isNoun(42))) is True)
        assert ((not (RiTa.isNoun(["rabbit"]))) is True)
        assert ((not (RiTa.isNoun("heard"))) is True), ("heard: ") + (RiTa.tagger.allTags("heard"))
        assert ((not (RiTa.isNoun("deterred"))) is True)
    def test_should_call_isverb(self):
        assert (RiTa.isVerb("abandons") == True)
        assert ((RiTa.isVerb("dance")) is True)
        assert ((RiTa.isVerb("swim")) is True)
        assert ((RiTa.isVerb("walk")) is True)
        assert ((RiTa.isVerb("dances")) is True)
        assert ((RiTa.isVerb("swims")) is True)
        assert ((RiTa.isVerb("walks")) is True)
        assert ((RiTa.isVerb("costs")) is True)
        assert ((RiTa.isVerb("danced")) is True)
        assert ((RiTa.isVerb("swam")) is True)
        assert ((RiTa.isVerb("walked")) is True)
        assert ((RiTa.isVerb("costed")) is True)
        assert ((RiTa.isVerb("satisfies")) is True)
        assert ((RiTa.isVerb("falsifies")) is True)
        assert ((RiTa.isVerb("beautifies")) is True)
        assert ((RiTa.isVerb("repossesses")) is True)
        assert ((not (RiTa.isVerb("dancer"))) is True)
        assert ((not (RiTa.isVerb("walker"))) is True)
        assert ((not (RiTa.isVerb("beautiful"))) is True)
        assert ((RiTa.isVerb("eat")) is True), "eat"
        assert ((RiTa.isVerb("chew")) is True)
        assert ((RiTa.isVerb("throw")) is True)
        assert ((RiTa.isVerb("walk")) is True)
        assert ((RiTa.isVerb("wash")) is True)
        assert ((RiTa.isVerb("drink")) is True)
        assert ((RiTa.isVerb("fish")) is True)
        assert ((RiTa.isVerb("wind")) is True)
        assert ((RiTa.isVerb("wet")) is True)
        assert ((RiTa.isVerb("dry")) is True)
        assert ((not (RiTa.isVerb("hard"))) is True)
        assert ((not (RiTa.isVerb("furry"))) is True)
        assert ((not (RiTa.isVerb("sad"))) is True)
        assert ((not (RiTa.isVerb("happy"))) is True)
        assert ((not (RiTa.isVerb("dolls"))) is True)
        assert ((not (RiTa.isVerb("frogs"))) is True)
        assert ((RiTa.isVerb("flowers")) is True)
        assert ((RiTa.isVerb("ducks")) is True)
        assert ((not (RiTa.isVerb("truthfully"))) is True)
        assert ((not (RiTa.isVerb("kindly"))) is True)
        assert ((not (RiTa.isVerb("bravely"))) is True)
        assert ((not (RiTa.isVerb("scarily"))) is True)
        assert ((not (RiTa.isVerb("sleepily"))) is True)
        assert ((not (RiTa.isVerb("excitedly"))) is True)
        assert ((not (RiTa.isVerb("energetically"))) is True)
        assert ((RiTa.isVerb("hates")) is True)
        assert ((RiTa.isVerb("hated")) is True)
        assert ((RiTa.isVerb("hating")) is True)
        assert ((RiTa.isVerb("dancing")) is True)
        assert ((RiTa.isVerb("flowers")) is True)
        assert ((RiTa.isVerb("hates")) is True)
        assert ((RiTa.isVerb("hated")) is True)
        assert ((RiTa.isVerb("ridden")) is True)
        assert ((RiTa.isVerb("rode")) is True)
        assert ((RiTa.isVerb("abetted")) is True)
        assert ((RiTa.isVerb("abetting")) is True)
        assert ((RiTa.isVerb("abutted")) is True)
        assert ((RiTa.isVerb("abutting")) is True)
        assert ((RiTa.isVerb("abuts")) is True)
        assert ((RiTa.isVerb("abut")) is True)
        assert ((RiTa.isVerb("misdeal")) is True)
        assert ((RiTa.isVerb("misdeals")) is True)
        assert ((RiTa.isVerb("misdealt")) is True)
        assert ((not (RiTa.isVerb(""))) is True)
        assert ((not (RiTa.isVerb())) is True)
        assert ((not (RiTa.isVerb(42))) is True)
        assert ((not (RiTa.isVerb(["work"]))) is True)
    def test_should_call_isadjective(self):
        assert ((not (RiTa.isAdjective("swim"))) is True)
        assert ((not (RiTa.isAdjective("walk"))) is True)
        assert ((not (RiTa.isAdjective("walker"))) is True)
        assert ((RiTa.isAdjective("beautiful")) is True)
        assert ((not (RiTa.isAdjective("dance"))) is True)
        assert ((not (RiTa.isAdjective("dancing"))) is True)
        assert ((not (RiTa.isAdjective("dancer"))) is True)
        assert ((not (RiTa.isAdjective("wash"))) is True)
        assert ((not (RiTa.isAdjective("walk"))) is True)
        assert ((not (RiTa.isAdjective("play"))) is True)
        assert ((not (RiTa.isAdjective("throw"))) is True)
        assert ((not (RiTa.isAdjective("drink"))) is True)
        assert ((not (RiTa.isAdjective("eat"))) is True)
        assert ((not (RiTa.isAdjective("chew"))) is True)
        assert ((RiTa.isAdjective("hard")) is True)
        assert ((RiTa.isAdjective("wet")) is True)
        assert ((RiTa.isAdjective("dry")) is True)
        assert ((RiTa.isAdjective("furry")) is True)
        assert ((RiTa.isAdjective("sad")) is True)
        assert ((RiTa.isAdjective("happy")) is True)
        assert ((RiTa.isAdjective("kindly")) is True)
        assert ((not (RiTa.isAdjective("dogs"))) is True)
        assert ((not (RiTa.isAdjective("wind"))) is True)
        assert ((not (RiTa.isAdjective("dolls"))) is True)
        assert ((not (RiTa.isAdjective("frogs"))) is True)
        assert ((not (RiTa.isAdjective("ducks"))) is True)
        assert ((not (RiTa.isAdjective("flowers"))) is True)
        assert ((not (RiTa.isAdjective("fish"))) is True)
        assert ((not (RiTa.isAdjective("truthfully"))) is True)
        assert ((not (RiTa.isAdjective("bravely"))) is True)
        assert ((not (RiTa.isAdjective("scarily"))) is True)
        assert ((not (RiTa.isAdjective("sleepily"))) is True)
        assert ((not (RiTa.isAdjective("excitedly"))) is True)
        assert ((not (RiTa.isAdjective("energetically"))) is True)
        assert ((not (RiTa.isAdjective(""))) is True)
        assert ((not (RiTa.isAdjective())) is True)
        assert ((not (RiTa.isAdjective(42))) is True)
        assert ((not (RiTa.isAdjective(["happy"]))) is True)
    def test_should_call_alltags(self):
        assert (RiTa.tagger.allTags("monkey") == ["nn"])
        assert (RiTa.tagger.allTags("monkeys") == ["nns"])
        assert (RiTa.tagger.allTags("") == [])
        assert (RiTa.tagger.allTags(["monkey"]) == [])
        assert (RiTa.tagger.allTags("hates", {"noDerivations": True}) == [])
        assert (RiTa.tagger.allTags("satisfies") == ["vbz"])
        assert (RiTa.tagger.allTags("falsifies") == ["vbz"])
        assert ("vbz" in RiTa.tagger.allTags("hates"))
        assert ("nns" in RiTa.tagger.allTags("hates"))
        assert ("nns" in RiTa.tagger.allTags("cakes"))
        assert ("vbz" in RiTa.tagger.allTags("repossesses"))
        assert ("nns" in RiTa.tagger.allTags("thieves"))
        assert ("vbz" in RiTa.tagger.allTags("thieves"))
        assert ("vbd" in RiTa.tagger.allTags("hated"))
        assert ("vbn" in RiTa.tagger.allTags("hated"))
        assert ("vbd" in RiTa.tagger.allTags("owed"))
        assert ("vbn" in RiTa.tagger.allTags("owed"))
        assert ("vbg" in RiTa.tagger.allTags("assenting"))
        assert ("vbg" in RiTa.tagger.allTags("hating"))
        assert ("nns" in RiTa.tagger.allTags("feet"))
        assert ("nns" in RiTa.tagger.allTags("men"))
        assert ("nn" in RiTa.tagger.allTags("ashdj"))
        assert ("rb" in RiTa.tagger.allTags("kahsdly"))
        assert ("nns" in RiTa.tagger.allTags("asdkasws"))
        assert (RiTa.tagger.allTags("bit") == ["vbd", "nn", "rb"])
        assert (RiTa.tagger.allTags("broke") == ["vbd", "jj", "rb"])
        assert (RiTa.tagger.allTags("called") == ["vbd", "vbn"])
        assert (RiTa.tagger.allTags("committed") == ["vbn", "jj", "vbd"])
        assert (RiTa.tagger.allTags("computerized") == ["jj", "vbd", "vbn"])
        assert (RiTa.tagger.allTags("concerned") == ["vbd", "jj", "vbn"])

        assert (RiTa.tagger.allTags("discriminated") == ["vbd", "vbn", "jj"])
        assert (RiTa.tagger.allTags("ended") == ["vbd", "jj", "vbn"])
        assert (RiTa.tagger.allTags("expected") == ["vbn", "vbd", "jj"])
        assert (RiTa.tagger.allTags("finished") == ["vbd", "jj", "vbn"])
        assert (RiTa.tagger.allTags("gained") == ["vbd", "vbn"])
        assert (RiTa.tagger.allTags("got") == ["vbd", "vbn"])
        assert (RiTa.tagger.allTags("increased") == ["vbn", "jj", "vbd"])
        assert (RiTa.tagger.allTags("involved") == ["vbn", "vbd", "jj"])
        assert (RiTa.tagger.allTags("launched") == ["vbn", "vbd"])
        assert (RiTa.tagger.allTags("led") == ["vbd", "vbn"])
        assert (RiTa.tagger.allTags("lived") == ["vbd", "vbn"])
        assert (RiTa.tagger.allTags("oversaw") == ["vbd"])
        assert (RiTa.tagger.allTags("paled") == ["vbd", "vbn"])
        assert (RiTa.tagger.allTags("prepaid") == ["jj", "vbd", "vbn"])

        assert (RiTa.tagger.allTags("pressured") == ["vbn", "jj", "vbd"])
        assert (RiTa.tagger.allTags("proliferated") == ["vbn", "vbd"])
        assert (RiTa.tagger.allTags("remade") == ["vbd", "vbn"])
        assert (RiTa.tagger.allTags("reopened") == ["vbd", "vbn"])
        assert (RiTa.tagger.allTags("reported") == ["vbd", "jj", "vbn"])
        assert (RiTa.tagger.allTags("resold") == ["vbd", "vbn"])
        assert (RiTa.tagger.allTags("settled") == ["vbd", "vbn", "jj"])
        assert (RiTa.tagger.allTags("started") == ["vbd", "jj", "vbn"])
    def test_should_call_hastag(self):
        assert ((not (RiTa.tagger.hasTag())) is True)
        assert ((not (RiTa.tagger.hasTag("nn adj", "nn"))) is True)
        assert ((RiTa.tagger.hasTag(RiTa.tagger.allTags("monkey"), "nn")) is True)
    def test_should_call_inlinetags(self):
        assert (RiTa.tagger.inlineTags() == "")
        assert (RiTa.tagger.inlineTags([]) == "")
        with pytest.raises(Exception):
            RiTa.tagger.inlineTags(["I", "am", "Pikachu"], [], "/")
        assert (RiTa.tagger.inlineTags(["I", "am", "happy", "."], ["prp", "vbp", "jj", "."]) == "I/prp am/vbp happy/jj .")
        assert (RiTa.tagger.inlineTags(["I", "am", "happy", "."], ["prp", "vbp", "jj", "."], ";") == "I;prp am;vbp happy;jj .")
    def test_should_call_tag(self):
        assert (RiTa.tagger.tag([]) == [])
        assert (RiTa.tagger.tag() == [])
        assert (RiTa.tagger.tag([], {"inline": True}) == "")
        assert (RiTa.tagger.tag(["I", "am", "happy", "."], {"simple": True}) == ["-", "v", "a", "-"])
        assert (RiTa.tagger.tag(["I", "am", "happy", "."], {"simple": True, "inline": True}) == "I/- am/v happy/a .")
        assert (RiTa.tagger.tag(["I", "roll", "a", "9", "."], {"inline": True}) == "I/prp roll/vbp a/dt 9/cd .")
        assert (RiTa.tagger.tag(["A", "badguy", "."], {"inline": True}) == "A/dt badguy/nn .")
        assert (RiTa.tagger.tag(["A", "C", "level", "grade", "."], {"inline": True}) == "A/dt C/C level/jj grade/nn .")
        assert (RiTa.tagger.tag(["The", "run", "was", "great", "."], {"inline": True}) == "The/dt run/nn was/vbd great/jj .")
        assert (RiTa.tagger.tag(["They", "are", "the", "beaten", "."], {"inline": True}) == "They/prp are/vbp the/dt beaten/nn .")
        assert (RiTa.tagger.tag(["A", "diss", "."], {"inline": True}) == "A/dt diss/nns .")
        assert (RiTa.tagger.tag(["The", "soon", "."], {"inline": True}) == "The/dt soon/jj .")
        assert (RiTa.tagger.tag(["The", "sooner", "."], {"inline": True}) == "The/dt sooner/jjr .")
        assert (RiTa.tagger.tag(["The", "soonest", "."], {"inline": True}) == "The/dt soonest/jjs .")
        assert (RiTa.tagger.tag(["It", "is", "59876", "."], {"inline": True}) == "It/prp is/vbz 59876/cd .")
        assert (RiTa.tagger.tag(["I", "teabaged", "."], {"inline": True}) == "I/prp teabaged/vbn .")
        assert (RiTa.tagger.tag(["Sun", "teabaged", "."], {"inline": True}) == "Sun/nn teabaged/vbn .")
        assert (RiTa.tagger.tag(["The", "worker", "proletarianized", "."], {"inline": True}) == "The/dt worker/nn proletarianized/vbn .")
        assert (RiTa.tagger.tag(["The", "fortunately", "."], {"inline": True}) == "The/dt fortunately/rb .")
        assert (RiTa.tagger.tag(["He", "is", "goodly", "working", "."], {"inline": True}) == "He/prp is/vbz goodly/rb working/vbg .")
        assert (RiTa.tagger.tag(["It", "is", "nonexistional", "."], {"inline": True}) == "It/prp is/vbz nonexistional/jj .")
        assert (RiTa.tagger.tag(["It", "is", "mammal", "."], {"inline": True}) == "It/prp is/vbz mammal/nn .")
        assert (RiTa.tagger.tag(["It", "is", "onal", "."], {"inline": True}) == "It/prp is/vbz onal/nn .")
        assert (RiTa.tagger.tag(["We", "must", "place", "it", "."], {"inline": True}) == "We/prp must/md place/vb it/prp .")
        assert (RiTa.tagger.tag(["We", "must", "teabag", "him", "."], {"inline": True}) == "We/prp must/md teabag/vb him/prp .")
        assert (RiTa.tagger.tag(["He", "has", "played", "it", "."], {"inline": True}) == "He/prp has/vbz played/vbn it/prp .")
        assert (RiTa.tagger.tag(["He", "gets", "played", "."], {"inline": True}) == "He/prp gets/vbz played/vbn .")
        assert (RiTa.tagger.tag(["The", "morning", "."], {"inline": True}) == "The/dt morning/nn .")
        assert (RiTa.tagger.tag(["They", "are", "fishing", "."], {"inline": True}) == "They/prp are/vbp fishing/vbg .")
        assert (RiTa.tagger.tag(["He", "dances", "."], {"inline": True}) == "He/prp dances/vbz .")
        assert (RiTa.tagger.tag(["The", "dog", "dances", "."], {"inline": True}) == "The/dt dog/nn dances/vbz .")
        assert (RiTa.tagger.tag(["Dave", "dances", "."], {"inline": True}) == "Dave/nnp dances/vbz .")
        assert (RiTa.tagger.tag(["Taipei", "."], {"inline": True}) == "Taipei/nnp .")
        assert (RiTa.tagger.tag(["Buddhas", "."], {"inline": True}) == "Buddhas/nnps .")
        assert (RiTa.tagger.tag(["In", "Beijing", "."], {"inline": True}) == "In/in Beijing/nnp .")
        assert (RiTa.tagger.tag(["One", "of", "the", "Beats", "."], {"inline": True}) == "One/cd of/in the/dt Beats/nnps .")
        assert (RiTa.tagger.tag(["Taipei", "is", "a", "big", "city", "."], {"inline": True}) == "Taipei/nnp is/vbz a/dt big/jj city/nn .")
        assert (RiTa.tagger.tag(["Buddhas", "in", "this", "temple", "have", "a", "history", "of", "500", "years", "."], {"inline": True}) == "Buddhas/nnps in/in this/dt temple/nn have/vbp a/dt history/nn of/in 500/cd years/nns .")
        assert (RiTa.tagger.tag(["Balls", "on", "the", "floor", "."], {"inline": True}) == "Balls/nns on/in the/dt floor/nn .")
        assert (RiTa.tagger.tag(["dances", "."], {"inline": True}) == "dances/nns .")
        assert (RiTa.tagger.tag(["dances", "and", "performances", "."], {"inline": True}) == "dances/nns and/cc performances/nns .")
        assert (RiTa.tagger.tag(["cakes", "quickly", "."], {"inline": True}) == "cakes/nns quickly/rb .")
        assert (RiTa.tagger.tag(["dances", "quickly", "."], {"inline": True}) == "dances/vbz quickly/rb .")
        assert (RiTa.tagger.tag(["David", "cakes", "."], {"inline": True}) == "David/nnp cakes/nns .")
        assert (RiTa.tagger.tag(["David", "laughs", "and", "dances", "."], {"inline": True}) == "David/nnp laughs/vbz and/cc dances/vbz .")
        assert (RiTa.tagger.tag(["counterattacks", "."], {"inline": True}) == "counterattacks/nns .")
        assert (RiTa.tagger.tag(["Monkeys", "run", "."], {"inline": True}) == "Monkeys/nns run/vbp .")
        assert (RiTa.tagger.tag(["Monkeys", "attack", "."], {"inline": True}) == "Monkeys/nns attack/vbp .")
        assert (RiTa.tagger.tag(["A", "light", "blue", "sky", "."], {"inline": True}) == "A/dt light/jj blue/jj sky/nn .")
        assert (RiTa.tagger.tag(["It", "broke", "."], {"inline": True}) == "It/prp broke/vbd .")
        assert (RiTa.tagger.tag(["It", "outpaced", "that", "."], {"inline": True}) == "It/prp outpaced/vbd that/in .")
        assert (RiTa.tagger.tag(["She", "remade", "this", "video", "."], {"inline": True}) == "She/prp remade/vbd this/dt video/nn .")
        assert (RiTa.tagger.tag(["She", "has", "remade", "this", "video", "."], {"inline": True}) == "She/prp has/vbz remade/vbn this/dt video/nn .")
        (0) and (expect(RiTa.tagger.tag(["The", "video", "was", "remade", "."], {"inline": True})).eq("The/dt video/nn was/vbd remade/vbn ."))
        (0) and (expect(RiTa.tagger.tag(["Being", "literate", "didn't", "stop", "him", "from", "being", "discriminated", "against", "."], {"inline": True})).eq("Being/vbg literate/jj didn't/vbd stop/vb him/prp from/in being/vbg discriminated/vbn against/in ."))
    def test_should_handle_hyphenated_words(self):
        pool = ["He is my father-in-law.", "We have a off-site meeting yesterday.", "I know a great place for an off-site.", "a state-of-the-art computer", "The girls wanted the merry-go-round to go faster.", "He ate twenty-one burgers today.", "The politician arrived by high-speed railway.", "People doing yoga benefit from an increased feeling of well-being.", "There is a life-size statue of the dragon in the park.", "He has a king-size bed in his room.", "I am taking a full-time job now", "The cost for the round-trip ticket is 2000 dollars.", "The cost is 2000 dollars for the round-trip.", "He come back empty-handed", "She is left-handed", "I like the dress of the long-haired girl in the photo.", "His move was breath-taking.", "Snakes are cold-blooded.", "People liked to wear bell-bottoms in the 80s.", "This shop mainly sells corn-fed meat.", "I withdraw the application and re-apply for another position.", "Our co-manager believe in neo-liberalism.", "He did a u-turn.", "We are not going to get down to the nitty-gritty analysis of value for money.", "The game require co-op with your teammates.", "He was a roly-poly little man."]
        answers = [["prp", "vbz", "prp$", "nn", "."], ["prp", "vbp", "dt", "jj", "vbg", "nn", "."], ["prp", "vbp", "dt", "jj", "nn", "in", "dt", "nn", "."], ["dt", "jj", "nn"], ["dt", "nns", "vbd", "dt", "nn", "to", "vb", "rbr", "."], ["prp", "vbd", "cd", "nns", "nn", "."], ["dt", "nn", "vbd", "in", "jj", "nn", "."], ["nn", "vbg", "nn", "nn", "in", "dt", "jj", "vbg", "in", "nn", "."], ["ex", "vbz", "dt", "jj", "nn", "in", "dt", "nn", "in", "dt", "nn", "."], ["prp", "vbz", "dt", "jj", "nn", "in", "prp$", "nn", "."], ["prp", "vbp", "vbg", "dt", "jj", "nn", "rb"], ["dt", "nn", "in", "dt", "jj", "nn", "vbz", "cd", "nns", "."], ["dt", "nn", "vbz", "cd", "nns", "in", "dt", "nn", "."], ["prp", "vbp", "rb", "jj"], ["prp", "vbz", "jj"], ["prp", "vbp", "dt", "nn", "in", "dt", "jj", "nn", "in", "dt", "nn", "."], ["prp$", "nn", "vbd", "jj", "."], ["nns", "vbp", "jj", "."], ["nn", "vbd", "to", "vb", "nn", "in", "dt", "nns", "."], ["dt", "nn", "rb", "nns", "jj", "nn", "."], ["prp", "vbp", "dt", "nn", "cc", "vb", "in", "dt", "nn", "."], ["prp$", "nn", "vbp", "in", "nn", "."], ["prp", "vbd", "dt", "nn", "."], ["prp", "vbp", "rb", "vbg", "to", "vb", "rb", "to", "dt", "nn", "nn", "in", "nn", "in", "nn", "."], ["dt", "nn", "vb", "nn", "in", "prp$", "nns", "."], ["prp", "vbd", "dt", "jj", "jj", "nn", "."]]
        for a, i in answers:
            assert (RiTa.pos(pool[i]) == a)

