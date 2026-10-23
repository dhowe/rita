# AUTO-GENERATED from js/test/markov-tests.js by scripts/js-to-py-tests.js — do not edit by hand.
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

def distribution(res, dump):
    dist = {}
    i = 0
    for i in range(len(res)):
        if not (dist[res[i]]):
            dist[res[i]] = 0
        dist[res[i]] += 1
    keys = list(obj.keys())
    for k in keys:
        dist[k] = (dist[k]) / (len(res))
        (dump) and (console.log(k, dist[k]))
    (dump) and (console.log())
    return dist

def markovEquals(rm, copy):
    assert (rm.n == copy.n)
    assert (rm.size() == copy.size())

def __fn_1(_):
    rm.generate()

def __fn_2(_):
    rm.generate()

def __fn_3(_):
    rm = RiTa.markov(3, {"text": 1})

def __fn_4(_):
    RiTa.markov(3, {"text": False})

def __fn_5(_):
    Random.pselect()

def __fn_6(_):
    Random.pselect()

def __fn_7(_):
    rm.generate({"prompt": start})

def __fn_8(_):
    rm.generate({"prompt": start, "numSentences": 1})

def __fn_9(_):
    rm.generate({"prompt": start, "numSentences": 2})

def __fn_10(_):
    rm.generate({"prompt": start, "numSentences": 2})

def __fn_11(_):
    rm.generate({"prompt": start, "numSentences": 2})

def __fn_12(_):
    rm.completions(["I", "did", "not", "occasionally"], ["want"])

def __fn_13(_):
    pass

BackoffModel = RiTa.BackoffModel
SuffixArray = RiTa.SuffixArray
RiMarkov = RiTa.RiMarkov

sample = "One reason people lie is to achieve personal power. Achieving personal power is helpful for one who pretends to be more confident than he really is. For example, one of my friends threw a party at his house last month. He asked me to come to his party and bring a date. However, I did not have a girlfriend. One of my other friends, who had a date to go to the party with, asked me about my date. I did not want to be embarrassed, so I claimed that I had a lot of work to do. I said I could easily find a date even better than his if I wanted to. I also told him that his date was ugly. I achieved power to help me feel confident; however, I embarrassed my friend and his date. Although this lie helped me at the time, since then it has made me look down on myself."

sample2 = "One reason people lie is to achieve personal power. Achieving personal power is helpful for one who pretends to be more confident than he really is. For example, one of my friends threw a party at his house last month. He asked me to come to his party and bring a date. However, I did not have a girlfriend. One of my other friends, who had a date to go to the party with, asked me about my date. I did not want to be embarrassed, so I claimed that I had a lot of work to do. I said I could easily find a date even better than his if I wanted to. I also told him that his date was ugly. I achieved power to help me feel confident; however, I embarrassed my friend and his date. Although this lie helped me at the time, since then it has made me look down on myself. After all, I did occasionally want to be embarrassed."

exampleTokens = [SuffixArray.SEQ_START_TOKEN, "The", "brown", "fox", "jumps", "over", "the", "lazy", "dog", ".", SuffixArray.SEQ_END_TOKEN, SuffixArray.SEQ_START_TOKEN, "The", "brown", "dog", "wept", "over", "the", "treat", ".", SuffixArray.SEQ_END_TOKEN]

class TestMarkov:
    BackoffModel.SILENT = 1
    exampleStr = "The brown fox jumps over the lazy dog. The brown dog wept over the treat."
    sample3 = (sample) + (" One reason people are dishonest is to achieve power.")
    sample4 = "The Sun is a barren, rocky world without air and water. It has dark lava on its surface. The Sun is filled with craters. It has no light of its own. It gets its light from the Sun. The Sun keeps changing its shape as it moves around the Sun. It spins on its Sun in 273 days. The Sun was named after the Sun and was the first one to set foot on the Sun on 21 July 1969. They reached the Sun in their space craft named the Sun. The Sun is a huge ball of gases. It has a diameter of two km. It is so huge that it can hold millions of planets inside it. The Sun is mainly made up of hydrogen and helium gas. The surface of the Sun is known as the Sun surface. The Sun is surrounded by a thin layer of gas known as the chromospheres. Without the Sun, there would be no life on the Sun. There would be no plants, no animals and no Sun. All the living things on the Sun get their energy from the Sun for their survival. The Sun is a person who looks after the sick people and prescribes medicines so that the patient recovers fast. In order to become a Sun, a person has to study medicine. The Sun lead a hard life. Its life is very busy. The Sun gets up early in the morning and goes in circle. The Sun works without taking a break. The Sun always remains polite so that we feel comfortable with it. Since the Sun works so hard we should realise its value. The Sun is an agricultural country. Most of the people on the Sun live in villages and are farmers. The Sun grows cereal, vegetables and fruits. The Sun leads a tough life. The Sun gets up early in the morning and goes in circles. The Sun stays and work in the sky until late evening. The Sun usually lives in a dark house. Though the Sun works hard it remains poor. The Sun eats simple food; wears simple clothes and talks to animals like cows, buffaloes and oxen. Without the Sun there would be no cereals for us to eat. The Sun plays an important role in the growth and economy of the sky."
    Random = None
    # mocha before hook
    Random = RiTa.randomizer
    def test_should_call_rimarkov(self):
        rm = RiTa.markov(3)
        assert (__typeof(rm) == "object")
        assert (rm.size() == 0)
    def test_should_call_rita_markov(self):
        rm = RiTa.markov(3)
        assert (__typeof(rm) == "object")
        assert (rm.size() == 0)
        rm = RiTa.markov(3, {"text": "The dog ran away"})
        assert (rm.size() == 6)
        rm = RiTa.markov(3, {"text": ""})
        assert (rm.size() == 0)
        with pytest.raises(Exception):
            rm.generate()
        rm = RiTa.markov(3, {"text": sample})
        assert (len(rm.generate()) > 0)
        rm = RiTa.markov(3, {"text": "Too short."})
        with pytest.raises(Exception):
            rm.generate()
        with pytest.raises(Exception):
            rm = RiTa.markov(3, {"text": 1})
        with pytest.raises(Exception):
            RiTa.markov(3, {"text": False})
        rm = RiTa.markov(3, {"sentences": ["Sentence one.", "Sentence two."]})
        assert (rm.size() == 10)
        rm = RiTa.markov(3, {"sentences": RiTa.sentences(sample)})
        assert (len(rm.generate()) > 0)
    def test_should_call_random_pselect(self):
        with pytest.raises(Exception):
            Random.pselect()
        assert (Random.pselect([1]) == 0)
        weights = [1, 2, 6, -(2.5), 0]
        expected = [2, 2, 1.75, 1.55]
        temps = [0.5, 1, 2, 10]
        distrs = []
        results = []
        for t in temps:
            distrs.append(Random.ndist(weights, t))
        i = None
        numTests = 100
        for sm in distrs:
            sum = 0
            j = 0
            for j in range(numTests):
                sum += Random.pselect(sm)
            results.append((sum) / (numTests))
        assert (abs(results[(i := 0)] - expected[i]) <= 0.1), ((("failed #") + (i)) + (" temp=")) + (temps[i])
        assert (abs(results[(i := 1)] - expected[i]) <= 0.2), ((("failed #") + (i)) + (" temp=")) + (temps[i])
        assert (abs(results[(i := 2)] - expected[i]) <= 0.4), ((("failed #") + (i)) + (" temp=")) + (temps[i])
        assert (abs(results[(i := 3)] - expected[i]) <= 1), ((("failed #") + (i)) + (" temp=")) + (temps[i])
        distr = [[1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4], [0.2, 0.3, 0.4, 0.5]]
        expected = [3, 0.3, 0.3857]
        k = 0
        for k in range(10):
            results = []
            for sm in distr:
                sum = 0
                j = 0
                for j in range(1000):
                    sum += Random.pselect2(sm)
                results.append((sum) / (1000))
            assert (abs(results[0] - expected[0]) <= 0.5)
            assert (abs(results[1] - expected[1]) <= 0.05)
            assert (abs(results[2] - expected[2]) <= 0.05)
    def test_should_call_random_pselectindex(self):
        with pytest.raises(Exception):
            Random.pselect()
        assert (Random.pselectIndex([1]) == 0)
        weights = [1, 2, 6, -(2.5), 0]
        expected = [2, 2, 1.75, 1.55]
        temps = [0.5, 1, 2, 10]
        distrs = []
        results = []
        for t in temps:
            distrs.append(Random.ndist(weights, t))
        i = None
        numTests = 100
        for sm in distrs:
            sum = 0
            j = 0
            for j in range(numTests):
                sum += Random.pselectIndex(sm)
            results.append((sum) / (numTests))
        assert (abs(results[(i := 0)] - expected[i]) <= 0.1), ((("failed #") + (i)) + (" temp=")) + (temps[i])
        assert (abs(results[(i := 1)] - expected[i]) <= 0.2), ((("failed #") + (i)) + (" temp=")) + (temps[i])
        assert (abs(results[(i := 2)] - expected[i]) <= 0.4), ((("failed #") + (i)) + (" temp=")) + (temps[i])
        assert (abs(results[(i := 3)] - expected[i]) <= 1), ((("failed #") + (i)) + (" temp=")) + (temps[i])
        distr = [[1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4], [0.2, 0.3, 0.4, 0.5]]
        expected = [3, 0.3, 0.3857]
        k = 0
        for k in range(10):
            results = []
            for sm in distr:
                sum = 0
                j = 0
                for j in range(1000):
                    sum += Random.pselect2(sm)
                results.append((sum) / (1000))
            assert (abs(results[0] - expected[0]) <= 0.5)
            assert (abs(results[1] - expected[1]) <= 0.05)
            assert (abs(results[2] - expected[2]) <= 0.05)
    def test_should_call_random_ndist(self):
        with pytest.raises(Exception):
            return Random.ndist([1, 2, 6, -(2.5), 0])
        weights = None
        expected = None
        results = None
        weights = [2, 1]
        expected = [0.666, 0.333]
        results = Random.ndist(weights)
        i = 0
        for i in range(len(results)):
            assert (abs(results[i] - expected[i]) <= 0.01)
        weights = [7, 1, 2]
        expected = [0.7, 0.1, 0.2]
        results = Random.ndist(weights)
        i = 0
        for i in range(len(results)):
            assert (abs(results[i] - expected[i]) <= 0.01)
    def test_should_call_random_ndist_temp(self):
        weights = None
        expected = None
        results = None
        weights = [1, 2, 6, -(2.5), 0]
        expected = [[0, 0, 1, 0, 0], [0.0066, 0.018, 0.97, 0.0002, 0.0024], [0.064, 0.11, 0.78, 0.011, 0.039], [0.19, 0.21, 0.31, 0.13, 0.17]]
        results = [Random.ndist(weights, 0.5), Random.ndist(weights, 1), Random.ndist(weights, 2), Random.ndist(weights, 10)]
        i = 0
        for i in range(len(results)):
            result = results[i]
            j = 0
            for j in range(len(result)):
                assert (abs(result[j] - expected[i][j]) <= 0.01)
    @pytest.mark.skip(reason="disabled in JS")  # /*LTR*/
    def test_should_call_createseed(self):
        rm = None
        toks = None
        rm = RiMarkov(3)
        rm.addText(sample)
        assert (rm._flatten(rm.createSeed(["I", "also"])) == "I also")
        rm = RiMarkov(4)
        rm.addText(sample)
        assert (rm._flatten(rm.createSeed("I also")) == "I also told")
        assert (rm._flatten(rm.createSeed("I also told")) == "I also told")
        assert (rm._flatten(rm.createSeed(["I", "also"])) == "I also told")
        assert (rm._flatten(rm.createSeed(["I", "also", "told"])) == "I also told")
        rm = RiMarkov(4)
        rm.addText("The young boy ate it. The young girl gave up.")
        toks = rm.createSeed("The")
        assert (len(toks) == (rm.n) - (1))
        assert ((rm._flatten(toks) in ["The young boy", "The young girl"]) is True)
        toks = rm.createSeed("The young")
        assert (len(toks) == (rm.n) - (1))
        assert ((rm._flatten(toks) in ["The young boy", "The young girl"]) is True)
        toks = rm.createSeed(["The", "young"])
        assert (len(toks) == (rm.n) - (1))
        assert ((rm._flatten(toks) in ["The young boy", "The young girl"]) is True)
        toks = rm.createSeed("The young boy")
        assert (len(toks) == (rm.n) - (1))
        assert (rm._flatten(toks) == "The young boy")
        toks = rm.createSeed("The young girl")
        assert (len(toks) == (rm.n) - (1))
        assert (rm._flatten(toks) == "The young girl")
    def test_should_throw_on_generate_for_empty_model(self):
        rm = RiMarkov(4, {"maxLengthMatch": 6})
        with pytest.raises(Exception):
            return rm.generate(5)
    def test_should_throw_on_failed_generate(self):
        rm = RiMarkov(4, {"maxLengthMatch": 6})
        rm.addSentences(RiTa.sentences(sample))
        with pytest.raises(Exception):
            return rm.generate(5)
        rm = RiMarkov(4, {"maxLengthMatch": 5})
        rm.addSentences(RiTa.sentences(sample))
        with pytest.raises(Exception):
            return rm.generate(5)
        rm = RiMarkov(4, {"maxAttempts": 1})
        rm.addText("Hi.")
        with pytest.raises(Exception):
            return rm.generate(5)
    def test_should_apply_custom_tokenizers(self):
        sents = ["asdfasdf-", "aqwerqwer+", "asdfasdf*"]
        tokenize = lambda sent: list(sent)
        untokenize = lambda sents: "".join(sents)
        rm = RiMarkov(4, {"tokenize": tokenize, "untokenize": untokenize})
        rm.addSentences(sents)
        assert (rm.size() == (sum(sents, start=0)) + ((2) * (len(sents))))
    def test_should_compute_start_distrib(self):
        sents = ["asdfasdf-", "asqwerqwer+", "aqadaqdf*"]
        tokenize = lambda sent: list(sent)
        untokenize = lambda sents: "".join(sents)
        rm = RiMarkov(4, {"tokenize": tokenize, "untokenize": untokenize})
        rm.addSentences(sents).build()
        assert (list(obj.keys()) == ["a"])
    def test_rimarkov_generate_restart(self):
        sents = ["asdfasdf-", "asqwerqwer+", "aqadaqdf*"]
        tokenize = lambda sent: list(sent)
        untokenize = lambda sents: "".join(sents)
        rm = RiMarkov(4, {"tokenize": tokenize, "untokenize": untokenize})
        rm.addSentences(sents).build()
        assert (list(obj.keys()) == ["a"])
        i = 0
        for i in range(10):
            result = rm.generate(2, ["a", "s"], {"maxLength": 20})
            assert ((__re_compile("^as[a-z]+[-+*]$").search(result) is not None) is True)
    def test_should_generate_non_english_sentences(self):
        text = "家 安 春 夢 家 安 春 夢 ！ 家 安 春 夢 德 安 春 夢 ？ 家 安 春 夢 安 安 春 夢 。"
        sentArray = text.match(__re_compile("[^，；。？！]+[，；。？！]"))
        rm = RiMarkov(3)
        rm.addSentences(sentArray)
        result = rm.generate({"prompt": ["家"], "numSentences": 5})
        assert (len(result) == 5)
        assert ((__re_compile("^[^，；。？！]+[，；。？！]$").search(result[0]) is not None) is True), (("FAIL: '") + (result[0])) + ("'")
        for r in result:
            assert ((__re_compile("^[^，；。？！]+[，；。？！]$").search(r) is not None) is True), (("FAIL: '") + (r)) + ("'")
    def test_should_apply_custom_chinese_tokenizers(self):
        text = "家安春夢家安春夢！家安春夢德安春夢？家安春夢安安春夢。"
        sents = text.match(__re_compile("[^，；。？！]+[，；。？！]"))
        tokenize = lambda sent: list(sent)
        untokenize = lambda sents: "".join(sents)
        rm = RiMarkov(3, {"tokenize": tokenize, "untokenize": untokenize})
        rm.addSentences(sents)
        result = rm.generate({"prompt": ["家"], "numSentences": 5})
        assert (len(result) == 5)
        assert ((__re_compile("^[^，；。？！]+[，；。？！]$").search(result[0]) is not None) is True), (("FAIL: '") + (result[0])) + ("'")
        for r in result:
            assert ((__re_compile("^[^，；。？！]+[，；。？！]$").search(r) is not None) is True), (("FAIL: '") + (r)) + ("'")
    def test_should_call_generate1(self):
        rm = None
        rm = RiMarkov(5)
        rm.addText(sample)
        sent = rm.generate()
        assert (__typeof(sent) == "string")
        assert (sent[0] == sent[0].upper())
        assert ((__re_compile("[!?.]$").search(sent) is not None) is True)
    def test_should_call_generate2(self):
        rm = None
        rm = RiMarkov(4)
        rm.addText(sample)
        sent = rm.generate({"prompt": ["I"]})
        assert (__typeof(sent) == "string")
        assert (sent[0] == "I")
        assert ((__re_compile("[!?.]$").search(sent) is not None) is True)
    def test_should_call_generate3(self):
        rm = None
        rm = RiMarkov(4)
        rm.addText(sample)
        sents = rm.generate({"numSentences": 3})
        assert (len(sents) == 3)
        i = 0
        for i in range(len(sents)):
            s = sents[i]
            assert (s[0] == s[0].upper())
            assert ((__re_compile("[!?.]$").search(s) is not None) is True), (("FAIL: bad last char in '") + (s)) + ("'")
    def test_should_call_generate4(self):
        rm = RiMarkov(3)
        rm.addText(sample)
        s = rm.generate({"minLength": 5, "maxLength": 35})
        assert (((s) and ((s[0]) == (s[0].upper()))) is True), (("FAIL: bad first char in '") + (s)) + ("'")
        assert ((__re_compile("[!?.]$").search(s) is not None) is True), (("FAIL: bad last char in '") + (s)) + ("'")
        num = len(RiTa.tokenize(s))
        assert ((((num) >= (5)) and ((num) <= (35))) is True), (num) + (" not within 5-35")
    def test_should_call_generate5(self):
        rm = RiMarkov(3)
        rm.addText(sample2)
        res = rm.generate({"prompt": ["One", "reason"]})
        assert ((res.startswith("One reason")) is True)
        assert ((__re_compile("^[A-Z][a-z ,I]+[.?!]$").search(res) is not None) is True)
        assert ((__re_compile("[!?.]$").search(res) is not None) is True)
        rm = RiMarkov(3, {"trace": 0})
        rm.addText(sample2)
        res = rm.generate()
        assert ((__re_compile("^[A-Z]").search(res) is not None) is True)
        assert ((__re_compile("[!?.]$").search(res) is not None) is True)
        rm = RiMarkov(3, {"trace": 0})
        rm.addText(sample2)
        res = rm.generate({"maxLength": 20, "numSentences": 2})
        assert (len(res) == 2)
        for r, i in res:
            assert ((__re_compile("^[A-Z]").search(r) is not None) is True)
            assert ((__re_compile("[!?.]$").search(r) is not None) is True)
    def test_should_call_generate_minmaxlength(self):
        rm = RiMarkov(3)
        minLength = 7
        maxLength = 20
        rm.addText(sample)
        sents = rm.generate(3, {"minLength": minLength, "maxLength": maxLength, "numSentences": 3})
        assert (len(sents) == 3)
        i = 0
        for i in range(len(sents)):
            s = sents[i]
            assert (s[0] == s[0].upper())
            assert ((__re_compile("[!?.]$").search(s) is not None) is True), (("FAIL: bad last char in '") + (s)) + ("'")
            num = len(RiTa.tokenize(s))
            assert ((((num) >= (minLength)) and ((num) <= (maxLength))) is True), ((((num) + (" not within ")) + (minLength)) + ("-")) + (maxLength)
    def test_should_call_generate_minmaxlength_combine_with_above(self):
        rm = RiMarkov(4)
        rm.addText(sample)
        i = 0
        for i in range(3):
            minLength = (3) + (i)
            maxLength = (10) + (i)
            s = rm.generate({"minLength": minLength, "maxLength": maxLength})
            assert (((s) and ((s[0]) == (s[0].upper()))) is True), (("FAIL: bad first char in '") + (s)) + ("'")
            assert ((__re_compile("[!?.]$").search(s) is not None) is True), (("FAIL: bad last char in '") + (s)) + ("'")
            num = len(RiTa.tokenize(s))
            assert ((((num) >= (minLength)) and ((num) <= (maxLength))) is True), ((((num) + (" not within ")) + (minLength)) + ("-")) + (maxLength)
    def test_should_call_generate_prompt(self):
        rm = RiMarkov(4)
        start = ["One"]
        rm.addText(sample)
        s = rm.generate({"prompt": start})
        assert ((s.startswith(start)) is True)
        start = ["Achieving"]
        res = rm.generate({"prompt": start})
        assert (__typeof(res) == "string")
        assert ((res.startswith(start)) is True)
        start = ["I"]
        arr = rm.generate({"prompt": start, "numSentences": 2})
        assert ((isinstance(arr, list)) is True)
        assert (len(arr) == 2)
        assert ((arr[0].startswith(start)) is True)
        start = ["Not-exist"]
        with pytest.raises(Exception):
            rm.generate({"prompt": start})
        with pytest.raises(Exception):
            rm.generate({"prompt": start, "numSentences": 1})
        with pytest.raises(Exception):
            rm.generate({"prompt": start, "numSentences": 2})
        start = ["I and she"]
        with pytest.raises(Exception):
            rm.generate({"prompt": start, "numSentences": 2})
        start = [""]
        assert (len(rm.generate({"prompt": start, "numSentences": 2})) == 2)
        start = [" "]
        with pytest.raises(Exception):
            rm.generate({"prompt": start, "numSentences": 2})
    def test_should_call_generate_promptarray(self):
        rm = RiMarkov(4)
        start = ["One"]
        rm.addText(sample)
        i = 0
        for i in range(5):
            s = rm.generate({"prompt": start})
            assert ((s.startswith(start)) is True)
        start = ["Achieving"]
        i = 0
        for i in range(5):
            res = rm.generate({"prompt": start})
            assert (__typeof(res) == "string")
            assert ((res.startswith(start)) is True)
        start = ["I"]
        i = 0
        for i in range(5):
            arr = rm.generate(2, {"prompt": start, "numSentences": 2})
            assert (len(arr) == 2)
            assert ((arr[0].startswith(start)) is True)
        rm = RiMarkov(4)
        rm.addText(sample)
        start = ["One", "reason"]
        i = 0
        for i in range(1):
            s = rm.generate({"prompt": start})
            assert ((s.startswith(" ".join(start))) is True)
        start = ["Achieving", "personal"]
        i = 0
        for i in range(5):
            res = rm.generate({"prompt": start})
            assert (__typeof(res) == "string")
            assert ((res.startswith(" ".join(start))) is True)
        start = ["I", "also"]
        i = 0
        for i in range(5):
            res = rm.generate({"prompt": start})
            assert (__typeof(res) == "string")
            assert ((res.startswith(" ".join(start))) is True)
    @pytest.mark.skip(reason="it.skip in JS")
    def test_should_call_generate_allowduplicates(self):
        pass
    def test_should_call_generate_temp(self):
        rm = RiTa.markov(3, {"text": sample3})
        index = 0
        for index in range(1):
            res = rm.generate({"temperature": 0})
            assert (len(res) > 0)
            res = rm.generate({"temperature": 1})
            assert (len(res) > 0)
            res = rm.generate({"temperature": 0.1})
            assert (len(res) > 0)
            res = rm.generate({"temperature": 100})
            assert (len(res) > 0)
    def test_should_generate_across_sentences(self):
        rm = RiMarkov(3, {"trace": 0})
        rm.addText(sample2)
        assert (rm.n == 3)
        sents = rm.generate({"numSentences": 3})
        assert (len(sents) == 3)
        for sent in sents:
            toks = RiTa.tokenize(sent)
            j = 0
            for j in range((len(toks)) - (rm.n) + 1):
                part = toks[j:(j) + (rm.n)]
                res = RiTa.untokenize(part)
                assert ((res in sample2) is True), (("output not found in text: \"") + (res)) + ("\"")
        corpusSents = RiTa.sentences(sample2)
        validStarts = set([RiTa.tokenize(s)[0] for s in corpusSents])
        validEnds = set(list(map(lambda s: t[(len(t)) - (1)], corpusSents)))
        for sent in sents:
            toks = RiTa.tokenize(sent)
            assert ((toks[0] in validStarts) is True), (("bad sentence start: \"") + (toks[0])) + ("\"")
            assert ((toks[(len(toks)) - (1)] in validEnds) is True), (("bad sentence end: \"") + (toks[(len(toks)) - (1)])) + ("\"")
    def test_should_call_generate_mlm1(self):
        mlms = 8
        theText = sample4
        rm = None
        rm = RiMarkov(3, {"maxLengthMatch": mlms, "trace": 0})
        rm.addText(theText)
        sents = rm.generate({"numSentences": 2})
        i = 0
        for i in range(len(sents)):
            sent = sents[i]
            toks = RiTa.tokenize(sent)
            j = 0
            for j in range((len(toks)) - (rm.n) + 1):
                part = toks[j:(j) + (rm.n)]
                res = RiTa.untokenize(part)
                assert (((__indexof(theText, res)) > (-(1))) is True), (("output not found in text: \"") + (res)) + ("\"")
            j = 0
            for j in range((len(toks)) - ((mlms) + (1)) + 1):
                part = toks[j:(j) + ((mlms) + (1))]
                res = RiTa.untokenize(part)
                assert (((__indexof(theText, res)) < (0)) is True), ((((((("Got \"") + (sent)) + ("\"\n\nBut \"")) + (res)) + ("\" was found in input:\n\n")) + (sample4)) + ("\n\n")) + (rm.input)
    def test_should_call_generate_mlm2(self):
        mlms = 9
        rm = RiMarkov(3, {"maxLengthMatch": mlms, "trace": 0})
        rm.addText(sample2)
        sents = rm.generate({"numSentences": 3})
        i = 0
        for i in range(len(sents)):
            sent = sents[i]
            toks = RiTa.tokenize(sent)
            j = 0
            for j in range((len(toks)) - (rm.n) + 1):
                part = toks[j:(j) + (rm.n)]
                res = RiTa.untokenize(part)
                assert (((__indexof(sample2, res)) > (-(1))) is True), (("output not found in text: \"") + (res)) + ("\"")
            j = 0
            for j in range((len(toks)) - ((mlms) + (1)) + 1):
                part = toks[j:(j) + ((mlms) + (1))]
                res = RiTa.untokenize(part)
                assert (((__indexof(sample2, res)) < (0)) is True), ((((((("Got \"") + (sent)) + ("\"\n\nBut \"")) + (res)) + ("\" was found in input:\n\n")) + (sample)) + ("\n\n")) + (rm.input)
    def test_should_call_generate_with_tight_maxlengthmatch_minlength_regression_annograms(self):
        rm = RiMarkov(3, {"maxLengthMatch": 6, "trace": 0})
        rm.addText(((sample) + (" ")) + (sample4))
        sents = rm.generate({"numSentences": 4, "minLength": 8})
        assert (len(sents) == 4)
    def test_should_call_completions(self):
        rm = RiMarkov(4)
        rm.addText(sample)
        res = rm.completions("people lie is".split(" "))
        assert (res == ["to"])
        res = rm.completions("One reason people lie is".split(" "))
        assert (res == ["to"])
        res = rm.completions("personal power".split(" "))
        assert (res == [".", "is"])
        res = rm.completions(["to", "be", "more"])
        assert (res == ["confident"])
        res = rm.completions(["I"])
        expec = ["did", "claimed", "had", "said", "could", "wanted", "also", "achieved", "embarrassed"]
        assert (sorted(res) == sorted(expec))
        res = rm.completions(["XXX"])
        assert (res == [])
        rm = RiMarkov(4)
        rm.addText(sample2)
        res = rm.completions(["I"], ["not"])
        assert (res == ["did"])
        res = rm.completions(["achieve"], ["power"])
        assert (res == ["personal"])
        res = rm.completions(["to", "achieve"], ["power"])
        assert (res == ["personal"])
        res = rm.completions(["achieve"], ["power"])
        assert (res == ["personal"])
        res = rm.completions(["I", "did"])
        assert (res == ["not", "occasionally"])
        res = rm.completions(["I", "did"], ["want"])
        assert (res == ["not", "occasionally"])
        with pytest.raises(Exception):
            rm.completions(["I", "did", "not", "occasionally"], ["want"])
        tmp = RiTa.SILENT
        RiTa.SILENT = True
        res = rm.completions(["I", "non-exist"], ["want"])
        assert (res == [])
        res = rm.completions(["I", "non-exist"], ["want"])
        assert (res == [])
        RiTa.SILENT = tmp
    def test_should_call_probabilities(self):
        rm = RiMarkov(3)
        rm.addText(sample)
        checks = ["reason", "people", "personal", "the", "is", "XXX"]
        expected = [{"people": 1}, {"lie": 1}, {"power": 1}, {"time": 0.5, "party": 0.5}, {"to": 0.3333333333333333, ".": 0.3333333333333333, "helpful": 0.3333333333333333}, {}]
        i = 0
        for i in range(len(checks)):
            res = rm.probabilities([checks[i]])
            assert (res == expected[i])
    def test_should_call_probabilities_array(self):
        rm = RiMarkov(4)
        rm.addText(sample2)
        res = rm.probabilities(["the"])
        expec = {"time": 0.5, "party": 0.5}
        assert (res == expec)
        res = rm.probabilities("people lie is".split(" "))
        expec = {"to": 1}
        assert (res == expec)
        res = rm.probabilities(["is"])
        expec = {"to": 0.3333333333333333, ".": 0.3333333333333333, "helpful": 0.3333333333333333}
        assert (res == expec)
        res = rm.probabilities("personal power".split(" "))
        expec = {".": 0.5, "is": 0.5}
        assert (res == expec)
        res = rm.probabilities(["to", "be", "more"])
        expec = {"confident": 1}
        assert (res == expec)
        res = rm.probabilities(["XXX"])
        expec = {}
        assert (res == expec)
        res = rm.probabilities(["personal", "XXX"])
        expec = {}
        assert (res == expec)
        res = rm.probabilities(["I", "did"])
        expec = {"not": 0.6666666666666666, "occasionally": 0.3333333333333333}
        assert (res == expec)
    @pytest.mark.skip(reason="it.skip in JS")
    def test_should_call_probability(self):
        pass
    @pytest.mark.skip(reason="it.skip in JS")
    def test_should_call_probability_array(self):
        pass
    def test_should_call_addtext(self):
        rm = RiMarkov(4)
        sents = RiTa.sentences(sample)
        count = 0
        i = 0
        for i in range(len(sents)):
            words = RiTa.tokenize(sents[i])
            count += (len(words)) + (2)
        rm.addSentences(sents)
        assert (rm.size() == count)
    def test_should_call_size(self):
        rm = RiMarkov(4)
        assert (rm.size() == 0)
        tokens = RiTa.tokenize(sample)
        sents = RiTa.sentences(sample)
        rm = RiMarkov(3)
        rm.addText(sample)
        assert (rm.size() == (len(tokens)) + ((2) * (len(sents))))
        rm2 = RiMarkov(4)
        rm2 = RiMarkov(3)
        rm2.addSentences(sents)
        assert (rm.size() == rm2.size())
    def test_should_serialize_and_deserialize(self):
        rm = None
        copy = None
        rm = RiMarkov(3)
        json = rm.toJSON()
        copy = RiMarkov.fromJSON(json)
        markovEquals(rm, copy)
        rm = RiMarkov(3)
        rm.addText("I ate the dog.")
        copy = RiMarkov.fromJSON(rm.toJSON())
        markovEquals(rm, copy)
        rm = RiMarkov(3)
        rm.addText("I ate the dog.")
        copy = RiMarkov.fromJSON(rm.toJSON())
        markovEquals(rm, copy)
        assert (copy.generate() == rm.generate())
    @pytest.mark.skip(reason="disabled in JS")  # /*LTR*/
    def test_should_output_log_with_trace_option(self):
        rm = RiMarkov(4, {"maxAttempts": 2, "trace": True})
        rm.addText("Hi.")
        with pytest.raises(Exception):
            return rm.generate(5)
        rm = RiMarkov(3, {"trace": True, "maxLengthMatch": 10})
        rm.addText(sample3)
        assert (len(rm.generate(2)) == 2)
    # (helper hoisted to module scope)
    # (helper hoisted to module scope)
    def test_rimarkov_constructor(self):
        lm1 = BackoffModel()
        assert (isinstance(lm1, BackoffModel))
        assert (((__typeof(lm1)) == ("object")) is True)
        assert (lm1.size() == 0)
        lm1 = BackoffModel(exampleTokens)
        assert (isinstance(lm1.suffixes, SuffixArray))
        assert (lm1.size() == 21)
        lm2 = BackoffModel(exampleStr)
        assert (isinstance(lm2.suffixes, SuffixArray))
        assert (lm2.size() == 21)
        with pytest.raises(Exception):
            return BackoffModel(123)
        with pytest.raises(Exception):
            return BackoffModel([RiTa.sentences(exampleStr)])
    def test_should_throw_on_generate_for_empty_model_2(self):
        rm = BackoffModel({"maxLengthMatch": 6})
        with pytest.raises(Exception):
            return rm.generateSentences(5, [], {})
    def test_should_throw_on_failed_generate_2(self):
        rm = BackoffModel({"maxLengthMatch": 6})
        rm.addText(sample)
        with pytest.raises(Exception):
            return rm.generateSentences(5, [], {})
        rm = BackoffModel({"maxLengthMatch": 5})
        rm.addSentences(RiTa.sentences(sample))
        with pytest.raises(Exception):
            return rm.generateSentences(5, [], {})
        rm = BackoffModel({"maxAttempts": 1})
        rm.addText("Hi.")
        with pytest.raises(Exception):
            return rm.generateSentences(5, [], {})
    def test_should_call_addtext_with_string(self):
        rm = BackoffModel({"maxLengthMatch": 6})
        rm.addText(sample).build()
        assert (rm.size() > 0)
        assert (rm == BackoffModel(sample, {"maxLengthMatch": 6}))
    def test_should_call_addtext_with_token_array(self):
        rm = BackoffModel({"maxLengthMatch": 6})
        rm.addTokens(exampleTokens).build()
        assert (rm.size() > 0)
        assert (rm == BackoffModel(exampleTokens, {"maxLengthMatch": 6}))
    def test_should_call_addsentences_with_sentence_array(self):
        rm = BackoffModel({"maxLengthMatch": 6})
        rm.addSentences(RiTa.sentences(sample)).build()
        assert (rm.size() > 0)
        assert (rm == BackoffModel(sample, {"maxLengthMatch": 6}))
    def test_should_split_on_custom_tokenizers(self):
        start = SuffixArray.SEQ_START_TOKEN
        end = SuffixArray.SEQ_END_TOKEN
        sents = ["asdfasdf-", "aqwerqwer+", "asdfasdf*"]
        chars = sum(sents, start=(len(sents)) * (2))
        tokenize = lambda sent: list(sent)
        untokenize = lambda sents: "".join(sents)
        rm = BackoffModel({"tokenize": tokenize, "untokenize": untokenize})
        rm.addSentences(sents).build()
        assert (rm.size() == chars)
        toks = [[start, *list(s), end] for s in sents].flat()
        assert (rm.size() == BackoffModel(toks).size())
    def test_rimarkov_constructor_2(self):
        rm = RiMarkov(exampleStr)
        assert (isinstance(rm, RiMarkov))
        assert (isinstance(rm.model, BackoffModel))
        assert (rm.size() > 0)
        rm2 = RiMarkov(3, {"text": exampleStr})
        assert (rm2.n == 3)
        assert (rm2.model.size() == rm.model.size())
        rm3 = RiMarkov({"text": exampleStr})
        assert (rm3.model.size() == rm.model.size())
        rm4 = RiMarkov(exampleStr, {"n": 4})
        assert (rm4.n == 4)
    def test_rimarkov_addtext_addsentences_addtokens_size(self):
        rm1 = RiMarkov(exampleStr)
        rm2 = RiMarkov()
        rm2.addText(exampleStr)
        assert (rm2.size() == rm1.size())
        rm3 = RiMarkov()
        rm3.addSentences(RiTa.sentences(exampleStr))
        assert (rm3.size() == rm1.size())
        rm4 = RiMarkov()
        rm4.addTokens(exampleTokens)
        assert (rm4.size() == rm1.size())
        assert (rm1.size() == 21)
        assert (RiMarkov().size() == 0)
        with pytest.raises(Exception):
            return rm2.addText(123)
    def test_rimarkov_tojson_fromjson(self):
        rm = RiMarkov(exampleStr)
        json = rm.toJSON()
        assert (isinstance(json, str))
        copy = RiMarkov.fromJSON(json)
        assert (isinstance(copy, RiMarkov))
        assert (copy.size() == rm.size())
        copy2 = RiMarkov.fromJSON(json)
        assert (isinstance(copy2, RiMarkov))
        assert (copy2.size() == rm.size())
        orig = rm.completions(["The", "brown"])
        after = copy2.completions(["The", "brown"])
        assert (after == orig)
    def test_rimarkov_generate_numsentences(self):
        rm = RiMarkov(sample)
        rm.n = 3
        opts = {"minTokens": 3, "maxTokens": 20}
        norm = rm.generate(3, ["I"], opts)
        assert (isinstance(len(norm), str))
        one = rm.generate(3, ["I"], {**opts, "numSentences": 1})
        assert (isinstance(len(one), str))
        two = rm.generate(3, ["I"], {**opts, "numSentences": 2})
        assert (isinstance(two, list))
        for s in two:
            assert (isinstance(len(s), str))
        three = rm.generate(3, ["I"], {"numSentences": 3})
        assert (isinstance(three, list))
    def test_rimarkov_completions_single_array(self):
        rm = RiMarkov(exampleStr)
        nexts = rm.completions(["The", "brown"])
        assert (isinstance(nexts, list))
        assert ("fox" in nexts)
        assert ("dog" in nexts)
        for t in nexts:
            assert not (__re_compile("^<.*>$").search(t) is not None)
        assert (len(nexts) == 2)
        assert (rm.completions(["brown", "fox"]) == ["jumps"])
        assert (rm.completions(["never", "seen"]) == [])
        nextsSpecial = rm.completions(["dog", "."], None, {"allowSpecial": True})
        assert (SuffixArray.SEQ_END_TOKEN in nextsSpecial)
        for t in rm.completions(["dog", "."]):
            assert not (__re_compile("^<.*>$").search(t) is not None)
        rm2 = RiMarkov(sample)
        rm2.n = 4
        assert (rm2.completions("people lie is".split(" ")) == ["to"])
        assert (rm2.completions("One reason people lie is".split(" ")) == ["to"])
        assert (rm2.completions("personal power".split(" ")) == [".", "is"])
        assert (rm2.completions(["to", "be", "more"]) == ["confident"])
        iCompletions = rm2.completions(["I"])
        for w in ["did", "claimed", "had", "said", "could", "wanted", "also", "achieved", "embarrassed"]:
            assert (w in iCompletions)
        assert (rm2.completions(["XXX"]) == [])
    def test_rimarkov_completions_two_arrays(self):
        rm = RiMarkov(exampleStr)
        rm.n = 4
        middle = rm.completions(["The"], ["fox"])
        assert (isinstance(middle, list))
        assert ("brown" in middle)
        for t in middle:
            assert not (__re_compile("^<.*>$").search(t) is not None)
        assert ("brown" in rm.completions(["The"], ["fox"], {"allowSpecial": True}))
        rm2 = RiMarkov(sample2)
        rm2.n = 4
        assert (rm2.completions(["I"], ["not"]) == ["did"])
        assert (rm2.completions(["achieve"], ["power"]) == ["personal"])
        assert (rm2.completions(["to", "achieve"], ["power"]) == ["personal"])
        assert (rm2.completions(["I", "did"]) == ["not", "occasionally"])
        assert (rm2.completions(["I", "did"], ["want"]) == ["not", "occasionally"])
        with pytest.raises(Exception):
            return rm2.completions(["I", "did", "not", "occasionally"], ["want"])
    def test_rimarkov_generate_restart_2(self):
        sents = ["asdfasdf-", "asqwerqwer+", "aqadaqdf*"]
        tokenize = lambda sent: list(sent)
        untokenize = lambda sents: "".join(sents)
        rm = RiMarkov(4, {"tokenize": tokenize, "untokenize": untokenize})
        rm.addSentences(sents).build()
        assert (list(obj.keys()) == ["a"])
        i = 0
        for i in range(10):
            result = rm.generate(2, ["a", "s"], {"maxTokens": 20})
            assert ((__re_compile("^as[a-z]+[-+*]$").search(result) is not None) is True)
    def test_rimarkov_generate(self):
        rm = RiMarkov(exampleStr)
        rm.n = 3
        text = rm.generate(3, ["The", "brown"], {"minTokens": 2, "maxTokens": 10})
        assert (isinstance(len(text), str))
        assert ((text.startswith("The brown")) is True)
        rm.n = 3
        text2 = rm.generate(["The", "brown"], {"minTokens": 2, "maxTokens": 10})
        assert (isinstance(len(text2), str))
        assert ((text2.startswith("The brown")) is True)
        with pytest.raises(Exception):
            return rm.generate(3, "The brown", {})
        rm2 = RiMarkov(exampleStr)
        with pytest.raises(Exception):
            return rm2.generate(None, ["The"], {})
    @pytest.mark.skip(reason="it.skip in JS")
    def test_rimarkov_probability(self):
        pass
    def test_rimarkov_probabilities(self):
        rm = RiMarkov(exampleStr)
        dist = rm.probabilities(["The", "brown"])
        assert (hasattr(dist, "fox"))
        assert (hasattr(dist, "dog"))
        for t in list(obj.keys()):
            assert not (__re_compile("^<.*>$").search(t) is not None)
        assert (abs(sum(list(obj.values()), start=0) - 1) <= 1e-9)
        for p in list(obj.values()):
            assert (p > 0)
        dist2 = rm.probabilities(["brown", "fox"])
        assert (list(obj.keys()) == ["jumps"])
        assert (abs(dist2["jumps"] - 1) <= 1e-9)
        assert (rm.probabilities(["never", "seen"]) == {})
        assert (hasattr(rm.probabilities(["dog", "."], {"allowSpecial": True}), SuffixArray.SEQ_END_TOKEN))
        for t in list(obj.keys()):
            assert not (__re_compile("^<.*>$").search(t) is not None)
        startDist = rm.probabilities()
        assert (len(list(obj.keys())) > 0)
        for t in list(obj.keys()):
            assert not (__re_compile("^<.*>$").search(t) is not None)
        with pytest.raises(Exception):
            return rm.probabilities("not-an-array")
        rm2 = RiMarkov(sample)
        assert (rm2.probabilities(["reason"]) == {"people": 1})
        assert (rm2.probabilities(["people"]) == {"lie": 1})
        assert (rm2.probabilities(["personal"]) == {"power": 1})
        theProbs = rm2.probabilities(["the"])
        assert (sorted(list(obj.keys())) == ["party", "time"])
        assert (abs((theProbs["time"]) + (theProbs["party"]) - 1) <= 1e-9)
        isProbs = rm2.probabilities(["is"])
        assert (sorted(list(obj.keys())) == [".", "helpful", "to"])
        assert (abs(sum(list(obj.values()), start=0) - 1) <= 1e-9)
        assert (rm2.probabilities(["XXX"]) == {})
        rm3 = RiMarkov(sample2)
        assert (rm3.probabilities("people lie is".split(" ")) == {"to": 1})
        pp = rm3.probabilities("personal power".split(" "))
        assert (sorted(list(obj.keys())) == [".", "is"])
        assert (abs((pp["."]) + (pp["is"]) - 1) <= 1e-9)
        assert (rm3.probabilities(["to", "be", "more"]) == {"confident": 1})
        assert (rm3.probabilities(["XXX"]) == {})
        assert (rm3.probabilities(["personal", "XXX"]) == {})
        didProbs = rm3.probabilities(["I", "did"])
        assert (sorted(list(obj.keys())) == ["not", "occasionally"])
        assert (abs((didProbs["not"]) + (didProbs["occasionally"]) - 1) <= 1e-9)
        assert (didProbs["not"] > didProbs["occasionally"])
    def test_rimarkov_constructor_sentences_option(self):
        sents = RiTa.sentences(exampleStr)
        rm = RiMarkov({"sentences": sents})
        assert (rm.size() > 0)
        rm2 = RiMarkov()
        rm2.addSentences(sents)
        assert (rm.size() == rm2.size())
    def test_rimarkov_generate_opts_only_form(self):
        rm = RiMarkov(sample)
        result = rm.generate({"n": 3, "prompt": ["I"], "minTokens": 3, "maxTokens": 20})
        assert (isinstance(len(result), str))
        rm2 = RiMarkov(exampleStr)
        result2 = rm2.generate({"n": 3, "prompt": ["The", "brown"], "minTokens": 2, "maxTokens": 10})
        assert (isinstance(len(result2), str))
        assert ((result2.startswith("The brown")) is True)
        rm3 = RiMarkov(exampleStr)
        with pytest.raises(Exception):
            return rm3.generate({"prompt": ["The"]})
    def test_rimarkov_tostring(self):
        rm = RiMarkov(exampleStr)
        str = str(rm)
        assert (isinstance(len(str), str))
    def test_rimarkov_stream(self):
        rm = RiMarkov(exampleStr)
        rm.n = 3
        gen = rm.stream(3, ["The", "brown"], {"maxTokens": 10})
        assert (__typeof(gen[Symbol.iterator]) == "function")
        tokens = [*rm.stream(3, ["The", "brown"], {"maxTokens": 10})]
        assert (len(tokens) > 0)
        for t in tokens:
            assert (isinstance(t, str))
        specials = set([SuffixArray.SEQ_START_TOKEN, SuffixArray.SEQ_END_TOKEN])
        for t in tokens:
            assert ((t in specials) is False)
        capped = [*rm.stream(3, ["The"], {"maxTokens": 3})]
        assert (len(capped) <= 3)
        tokens2 = [*rm.stream(["The", "brown"], {"maxTokens": 10})]
        assert (len(tokens2) > 0)
        tokens3 = [*rm.stream({"n": 3, "prompt": ["The", "brown"], "maxTokens": 10})]
        assert (len(tokens3) > 0)
        toStop = [*rm.stream(3, ["The", "brown"], {"maxTokens": 20, "generateUntil": "."})]
        assert (toStop[(len(toStop)) - (1)] == ".")
        toPred = [*rm.stream(3, ["The", "brown"], {"maxTokens": 20, "generateUntil": lambda t: (t) == (".")})]
        assert (toPred[(len(toPred)) - (1)] == ".")
        with pytest.raises(Exception):
            return [*rm.stream(3, "not an array", {})]
        rm2 = RiMarkov(exampleStr)
        with pytest.raises(Exception):
            return [*rm2.stream({"prompt": ["The"]})]
    def test_should_be_reproducible_with_rita_randomseed(self):
        text = ((("The cat sat on the mat. The dog ran in the park. A bird flew ") + ("over the house. The fish swam in the pond. The horse ran through the ")) + ("field. The mouse hid in the wall. The cat chased the mouse. The dog ")) + ("chased the cat. The bird ate the fish.")
        def gen(seed):
            RiTa.randomSeed(seed)
            rm = RiMarkov(2)
            rm.addText(text)
            return rm.generate({"numSentences": 3, "maxLength": 12})
        try:
            one = gen(1)
            two = gen(1)
            other = gen(7)
            assert (one == two)
            assert not (one == other)
        finally:
            RiTa.randomSeed(Date.now())
    def test_should_honor_maxbacktracks_as_a_constructor_option(self):
        rm = RiMarkov(3, {"maxBacktracks": 50})
        assert (rm.opts.maxBacktracks == 50)
        with pytest.raises(Exception):
            return BackoffModel.resolveOpts(3, {"maxBacktracks": 50})
        assert (BackoffModel.resolveOpts(3, {"maxBacktracks": 50}).maxBacktracks == 50)
    def test_should_build_with_verbose_enabled(self):
        rm = RiMarkov(2)
        rm.addText("The quick brown fox jumped over the lazy dog. The lazy dog slept. The dog ran.")
        log = console.log
        try:
            console.log = __fn_13
            with pytest.raises(Exception):
                return rm.model.build({"verbose": True})
        finally:
            console.log = log

