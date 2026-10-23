# AUTO-GENERATED from js/test/backoff-tests.js by scripts/js-to-py-tests.js — do not edit by hand.
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

BackoffModel = RiTa.BackoffModel
SuffixArray = RiTa.SuffixArray

exampleStr = "The brown fox jumps over the lazy dog. The brown dog wept over the treat."

exampleTokens = [SuffixArray.SEQ_START_TOKEN, "The", "brown", "fox", "jumps", "over", "the", "lazy", "dog", ".", SuffixArray.SEQ_END_TOKEN, SuffixArray.SEQ_START_TOKEN, "The", "brown", "dog", "wept", "over", "the", "treat", ".", SuffixArray.SEQ_END_TOKEN]

sample = "One reason people lie is to achieve personal power. Achieving personal power is helpful for one who pretends to be more confident than he really is. For example, one of my friends threw a party at his house last month. He asked me to come to his party and bring a date. However, I did not have a girlfriend. One of my other friends, who had a date to go to the party with, asked me about my date. I did not want to be embarrassed, so I claimed that I had a lot of work to do. I said I could easily find a date even better than his if I wanted to. I also told him that his date was ugly. I achieved power to help me feel confident; however, I embarrassed my friend and his date. Although this lie helped me at the time, since then it has made me look down on myself."

class TestMarkovBackoff:
    BackoffModel.SILENT = 1
    def test_backoffmodel_constructor(self):
        lm1 = BackoffModel(exampleTokens)
        assert (isinstance(lm1, BackoffModel))
        assert (isinstance(lm1.suffixes, SuffixArray))
        assert (lm1.size() == 21)
        lm2 = BackoffModel(exampleStr)
        assert (isinstance(lm2, BackoffModel))
        assert (isinstance(lm2.suffixes, SuffixArray))
        assert (lm2.size() == 21)
        with pytest.raises(Exception):
            return BackoffModel(4)
        with pytest.raises(Exception):
            return BackoffModel([RiTa.sentences(exampleStr)])
    def test_backoffmodel_suffixes_find(self):
        lm = BackoffModel((exampleStr) + (" Then we ate."))
        sa = lm.suffixes
        min = None
        max = None
        min, max = sa.find(["T"], {"debug": 0})
        assert ((max) - (min) == 0)
        min, max = sa.find(["The"], {"debug": 0})
        assert ((max) - (min) == 2)
    # mocha .timeout(3000)
    def test_backoffmodel_to_fromjson(self):
        bom = BackoffModel(exampleStr)
        copy = BackoffModel.fromJSON(bom.toJSON())
        assert (bom.tokenCount == copy.tokenCount)
        assert (bom.tokens == copy.tokens)
        assert (isinstance(copy, BackoffModel))
        assert (sorted(list(obj.keys())) == sorted(list(obj.keys())))
        for f in BackoffModel.options:
            assert not ((copy[f]) is None), f
            assert (copy[f] == bom[f]), f
        for f in SuffixArray.__dict__:
            assert not ((copy.suffixes[f]) is None), f
            assert (copy.suffixes[f] == bom.suffixes[f]), f
    def test_backoffmodel_generationpaths(self):
        lm = BackoffModel(exampleStr)
        prompt = ["The", "brown"]
        opts = {"minLength": 1, "maxLength": 10}
        paths = lm.generationPaths(3, prompt, opts)
        assert (isinstance(paths, list))
        assert (len(paths) > 0)
        for __it in paths:
            tokens = __it["tokens"]
            prob = __it["prob"]
            inInput = __it["inInput"]
            assert (isinstance(tokens, list))
            assert (len(tokens) > len(prompt))
            assert (isinstance(prob, (int, float)))
            assert (isinstance(inInput, bool))
            for i, t in enumerate(prompt):
                assert (tokens[i].token == t)
        total = sum(paths, start=0)
        assert (abs(total - 1) <= 1e-9)
        firstGenTokens = [p.tokens[len(prompt)].token for p in paths]
        assert ("fox" in firstGenTokens)
        assert ("dog" in firstGenTokens)
        sorted = lm.generationPaths(3, prompt, {**opts, "sortByProb": True})
        i = 1
        for i in range(len(sorted)):
            assert (sorted[(i) - (1)].prob >= sorted[i].prob)
        origPaths = lm.generationPaths(3, prompt, {**opts, "forceOriginal": True})
        for __it in origPaths:
            inInput = __it["inInput"]
            assert ((inInput) is False)
    def test_backoffmodel_pathgenerator(self):
        lm = BackoffModel(exampleStr)
        prompt = ["The", "brown"]
        opts = {"minLength": 1, "maxLength": 10}
        generated = []
        for entry in lm.pathGenerator(3, prompt, opts):
            generated.append(entry)
        assert (len(generated) > 0)
        allPaths = lm.generationPaths(3, prompt, opts)
        assert (len(generated) == len(allPaths))
        for __it in generated:
            tokens = __it["tokens"]
            prob = __it["prob"]
            assert (isinstance(len(tokens), list))
            assert (isinstance(prob, (int, float)))
            for i, t in enumerate(prompt):
                assert (tokens[i].token == t)
        gen = lm.pathGenerator(3, prompt, opts)
        first = gen.next()
        assert ((first.done) is False)
        assert (isinstance(first.value.tokens, list))
        lm2 = BackoffModel(sample)
        samplePrompt = "I did not".split(" ")
        with pytest.raises(Exception):
            g = lm2.pathGenerator(3, samplePrompt, {**opts, "forceOriginal": True})
            g.next()
    def test_backoffmodel_streamtokens(self):
        lm = BackoffModel(sample)
        prompt = "I did not".split(" ")
        opts = {"minLength": 4, "maxLength": 20}
        tokens = [*lm.streamTokens(3, prompt, opts)]
        assert (isinstance(tokens, list))
        assert (len(tokens) >= opts.minLength)
        assert (len(tokens) <= opts.maxLength)
        for t in tokens:
            assert (isinstance(t, str))
        specials = set([SuffixArray.SEQ_START_TOKEN, SuffixArray.SEQ_END_TOKEN])
        for t in tokens:
            assert ((t in specials) is False)
        tokens = [*lm.streamTokens(3, prompt, {**opts, "allowSpecial": True})]
        assert (tokens[(len(tokens)) - (1)] == SuffixArray.SEQ_END_TOKEN)
        tokens = [*lm.streamTokens(3, prompt, {**opts, "generateUntil": "."})]
        assert (tokens[(len(tokens)) - (1)] == ".")
        tokens = [*lm.streamTokens(3, prompt, {**opts, "generateUntil": lambda t=None: (t) == (".")})]
        assert (tokens[(len(tokens)) - (1)] == ".")
        tokens = [*lm.streamTokens(3, prompt, {**opts, "minLength": 3, "generateUntil": lambda t=None: ((t) == ("be")) or ((t) == ("girlfriend"))})]
        assert (tokens[(len(tokens)) - (1)] in ["be", "girlfriend"])
        validFollowers = set(["have", "want"])
        i = 0
        for i in range(5):
            tokens = [*lm.streamTokens(3, prompt, {"minLength": 1, "maxLength": 5})]
            assert (len(tokens) <= 5)
            assert ((tokens[0] in validFollowers) is True)
    def test_backoffmodel_streamtokens_maxlengthmatch(self):
        lm = BackoffModel(sample)
        prompt = "I did not".split(" ")
        opts = {"minLength": 4, "maxLength": 20}
        with pytest.raises(Exception):
            return [*lm.streamTokens(4, prompt, {**opts, "maxLengthMatch": 3})]
        free = [*lm.streamTokens(3, prompt, {**opts, "maxLengthMatch": float("inf")})]
        assert (len(free) >= opts.minLength)
        n = 3
        mlm = 5
        i = 0
        for i in range(10):
            tokens = [*lm.streamTokens(n, prompt, {**opts, "maxLengthMatch": mlm})]
            assert (isinstance(tokens, list))
            full = [*prompt, *tokens]
            j = (len(prompt)) - (1)
            for j in range((len(full)) - ((mlm) + (1)) + 1):
                window = full[j:((j) + (mlm)) + (1)]
                windowStr = " ".join(window)
                assert ((windowStr in sample) is False), f"verbatim window found: \"{windowStr}\""
    def test_backoffmodel_generatesentences(self):
        lm = BackoffModel(sample)
        prompt = ["I"]
        opts = {"minLength": 3, "maxLength": 20}
        three = lm.generateSentences(3, prompt, opts)
        assert (isinstance(three, list))
        for s in three:
            assert (isinstance(len(s), str))
        two = lm.generateSentences(3, prompt, {**opts, "numSentences": 2})
        assert (isinstance(two, list))
        for s in two:
            assert (isinstance(len(s), str))
        one = lm.generateSentences(3, prompt, {**opts, "numSentences": 1})
        assert (isinstance(one, list))
        assert (isinstance(len(one[0]), str))
        specials = set([SuffixArray.SEQ_START_TOKEN, SuffixArray.SEQ_END_TOKEN])
        for s in three:
            for t in RiTa.tokenize(s):
                assert ((t in specials) is False)
    def test_backoffmodel_generationpaths_options(self):
        lm = BackoffModel(exampleStr)
        prompt = ["The", "brown"]
        base = {"minLength": 1, "maxLength": 10}
        narrow = lm.generationPaths(3, prompt, {**base, "topK": 1})
        assert (isinstance(len(narrow), list))
        for __it in narrow:
            tokens = __it["tokens"]
            prob = __it["prob"]
            assert (isinstance(tokens, list))
            assert (isinstance(prob, (int, float)))
        shallow = lm.generationPaths(3, prompt, {**base, "depth": 2})
        deep = lm.generationPaths(3, prompt, {**base, "depth": 20})
        assert (isinstance(shallow, list))
        assert (len(shallow) <= (len(deep)) + (1))
        with pytest.raises(Exception):
            return lm.generationPaths(3, prompt, {**base, "temp": 0.5})
        with pytest.raises(Exception):
            return lm.generationPaths(3, prompt, {**base, "temp": 2})
        with pytest.raises(Exception):
            return lm.generationPaths(3, prompt, {**base, "badKey": True})
        with pytest.raises(Exception):
            return lm.streamTokens(3, prompt, {**base, "badKey": True}).next()

def __fn_1(_):
    g = lm2.pathGenerator(3, samplePrompt, {**opts, "forceOriginal": True})
    g.next()

