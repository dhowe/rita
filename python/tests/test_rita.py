# AUTO-GENERATED from js/test/rita-tests.js by scripts/js-to-py-tests.js — do not edit by hand.
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

class TestCore:
    def test_should_have_access_to_statics(self):
        if (_typeof(lambda: process)) == ("undefined"):
            return
        if (process.env.NODE_ENV) != ("dev"):
            if (_typeof(lambda: process.env.npm_package_version)) == ("undefined"):
                console.warn("[WARN] No package version: ignore if running in vscode ")
            else:
                eql(RiTa.VERSION, process.env.npm_package_version, _jsstr(_jsstr("bad version number=\"") + _jsstr(RiTa.VERSION)) + _jsstr("\", "))
    def test_should_call_evaluate(self):
        res = None
        res = RiTa.evaluate("The [ox | ox | ox].pluralize run", 0)
        assert (res == "The oxen run")
        res = RiTa.evaluate("It was [honor].art to meet you", 0)
        assert (res == "It was an honor to meet you")
    def test_should_call_addtransform(self):
        def addRhyme(word=None, *args):
            res = RiTa.lexicon.rhymes_sync(word, JsDict({"limit": 1}))
            return _jsstr(_jsstr(word) + _jsstr(" rhymes with ")) + _jsstr(RiTa.random(res))
        assert ((RiTa.riscript.transforms.rhymes) is None)
        assert ((hasattr(RiTa.riscript.transforms, "rhymes")) is False)
        RiTa.add_transform("rhymes", addRhyme)
        assert not ((RiTa.riscript.transforms.rhymes) is None)
        assert ((hasattr(RiTa.riscript.transforms, "rhymes")) is True)
        res = RiTa.evaluate("The [dog | dog | dog].rhymes")
        assert (res == "The dog rhymes with cog")
        RiTa.remove_transform("rhymes")
        assert ((hasattr(RiTa.riscript.transforms, "rhymes")) is False)
        res = RiTa.evaluate("The [dog | dog | dog].rhymes", 0, JsDict({"silent": True}))
        assert (res == "The dog.rhymes")
    def test_should_call_random(self):
        assert (0 <= RiTa.random(10) <= 10)
        assert (1 <= RiTa.random(1, 10) <= 10)
        assert (0 <= RiTa.random() <= 1)
    def test_should_call_randi(self):
        assert (0 <= RiTa.randi(10) <= 9)
        assert (1 <= RiTa.randi(1, 10) <= 9)
        assert (RiTa.randi() == 0)
        assert ((_is_integer)(RiTa.randi(1, 10)))
        assert ((_is_integer)(RiTa.randi(10)))
    def test_should_call_randomordering(self):
        assert (RiTa.random_ordering(1) == [0])
        assert (set(RiTa.random_ordering(2)) == set([0, 1]))
        assert (RiTa.random_ordering(["a"]) == ["a"])
        assert (set(RiTa.random_ordering(["a", "b"])) == set(["a", "b"]))
        ro = RiTa.random_ordering(4)
        assert (len(ro) == 4)
        assert (set(ro) == set([0, 1, 2, 3]))
        arr = [0, 3, 5, 7]
        ro = RiTa.random_ordering(arr)
        assert (len(ro) == 4)
        assert (set(ro) == set(arr))
    def test_should_call_isquestion(self):
        ok(RiTa.is_question("what"))
        ok(RiTa.is_question("what"))
        ok(RiTa.is_question("what is this"))
        ok(RiTa.is_question("what is this?"))
        ok(RiTa.is_question("Does it?"))
        ok(RiTa.is_question("Would you believe it?"))
        ok(RiTa.is_question("Have you been?"))
        ok(RiTa.is_question("Is this yours?"))
        ok(RiTa.is_question("Are you done?"))
        ok(RiTa.is_question("what is this? , where is that?"))
        ok(RiTa.is_question("Will you come tomorrow?"))
        ok(RiTa.is_question("Would you do that?"))
        ok(not (RiTa.is_question("That is not a toy This is an apple")))
        ok(not (RiTa.is_question("string")))
        ok(not (RiTa.is_question("?")))
        ok(not (RiTa.is_question("")))
    def test_should_handle_articlize(self):
        tmp = RiTa.SILENCE_LTS
        RiTa.SILENCE_LTS = True
        assert (RiTa.articlize("honor") == "an honor")
        data = ["dog", "a dog", "ant", "an ant", "eagle", "an eagle", "ermintrout", "an ermintrout", "honor", "an honor"]
        i = 0
        for i in range(0, len(data), 2):
            assert (RiTa.articlize(data[i]) == data[(i) + (1)])
        RiTa.SILENCE_LTS = tmp
    def test_should_handle_articlize_phrases(self):
        data = ["black dog", "a black dog", "black ant", "a black ant", "orange ant", "an orange ant", "great honor", "a great honor"]
        i = 0
        for i in range(0, len(data), 2):
            assert (RiTa.articlize(data[i]) == data[(i) + (1)])
    def test_should_call_isabbrev(self):
        ok(RiTa.is_abbrev("Dr."))
        ok(RiTa.is_abbrev("dr."))
        ok(RiTa.is_abbrev("DR."))
        ok(RiTa.is_abbrev("Dr. "))
        ok(RiTa.is_abbrev(" Dr."))
        ok(RiTa.is_abbrev("Prof."))
        ok(RiTa.is_abbrev("prof."))
        ok(not (RiTa.is_abbrev("Dr")))
        ok(not (RiTa.is_abbrev("Doctor")))
        ok(not (RiTa.is_abbrev("Doctor.")))
        ok(not (RiTa.is_abbrev("PRFO.")))
        ok(not (RiTa.is_abbrev("PrFo.")))
        ok(not (RiTa.is_abbrev("Professor")))
        ok(not (RiTa.is_abbrev("professor")))
        ok(not (RiTa.is_abbrev("PROFESSOR")))
        ok(not (RiTa.is_abbrev("Professor.")))
        ok(not (RiTa.is_abbrev("@#$%^&*()")))
        ok(not (RiTa.is_abbrev("")))
        ok(not (RiTa.is_abbrev(None)))
        ok(not (RiTa.is_abbrev(None)))
        ok(not (RiTa.is_abbrev(1)))
        ok(RiTa.is_abbrev("Dr.", JsDict({"caseSensitive": True})))
        ok(RiTa.is_abbrev("Dr. ", JsDict({"caseSensitive": True})))
        ok(RiTa.is_abbrev(" Dr.", JsDict({"caseSensitive": True})))
        ok(RiTa.is_abbrev("Prof.", JsDict({"caseSensitive": True})))
        ok(not (RiTa.is_abbrev("dr.", JsDict({"caseSensitive": True}))))
        ok(not (RiTa.is_abbrev("DR.", JsDict({"caseSensitive": True}))))
        ok(not (RiTa.is_abbrev("Dr", JsDict({"caseSensitive": True}))))
        ok(not (RiTa.is_abbrev("Doctor", JsDict({"caseSensitive": True}))))
        ok(not (RiTa.is_abbrev("Doctor.", JsDict({"caseSensitive": True}))))
        ok(not (RiTa.is_abbrev("prof.", JsDict({"caseSensitive": True}))))
        ok(not (RiTa.is_abbrev("PRFO.", JsDict({"caseSensitive": True}))))
        ok(not (RiTa.is_abbrev("PrFo.", JsDict({"caseSensitive": True}))))
        ok(not (RiTa.is_abbrev("Professor", JsDict({"caseSensitive": True}))))
        ok(not (RiTa.is_abbrev("professor", JsDict({"caseSensitive": True}))))
        ok(not (RiTa.is_abbrev("PROFESSOR", JsDict({"caseSensitive": True}))))
        ok(not (RiTa.is_abbrev("Professor.", JsDict({"caseSensitive": True}))))
        ok(not (RiTa.is_abbrev("@#$%^&*()", JsDict({"caseSensitive": True}))))
        ok(not (RiTa.is_abbrev("", JsDict({"caseSensitive": True}))))
        ok(not (RiTa.is_abbrev(None, JsDict({"caseSensitive": True}))))
        ok(not (RiTa.is_abbrev(None, JsDict({"caseSensitive": True}))))
        ok(not (RiTa.is_abbrev(1, JsDict({"caseSensitive": True}))))
    def test_should_call_ispunct(self):
        ok(not (RiTa.is_punct("What the")))
        ok(not (RiTa.is_punct("What ! the")))
        ok(not (RiTa.is_punct(".#\"\\!@i$%&_+=}<>")))
        ok(RiTa.is_punct("!"))
        ok(RiTa.is_punct("?"))
        ok(RiTa.is_punct("?!"))
        ok(RiTa.is_punct("."))
        ok(RiTa.is_punct(".."))
        ok(RiTa.is_punct("..."))
        ok(RiTa.is_punct("...."))
        ok(RiTa.is_punct("%..."))
        ok(not (RiTa.is_punct("! ")))
        ok(not (RiTa.is_punct(" !")))
        ok(not (RiTa.is_punct("!  ")))
        ok(not (RiTa.is_punct("  !")))
        ok(not (RiTa.is_punct("!  ")))
        ok(not (RiTa.is_punct("   !")))
        punct = None
        punct = "$%&^,"
        i = 0
        for i in range(0, len(punct), 1):
            ok(RiTa.is_punct(punct[i]), _jsstr("fail at:") + _jsstr(punct[i]))
        punct = ",;:!?)([].#\"\\!@$%&}<>|-/\\*{^"
        i = 0
        for i in range(0, len(punct), 1):
            ok(RiTa.is_punct(punct[i]), _jsstr("fail at:") + _jsstr(punct[i]))
        punct = "\"��������`'"
        i = 0
        for i in range(0, len(punct), 1):
            ok(RiTa.is_punct(punct[i]), _jsstr("fail at:") + _jsstr(punct[i]))
        punct = "\"��������`',;:!?)([].#\"\\!@$%&}<>|-/\\*{^"
        i = 0
        for i in range(0, len(punct), 1):
            ok(RiTa.is_punct(punct[i]), _jsstr("fail at:") + _jsstr(punct[i]))
        nopunct = "Helloasdfnals  FgG   \t kjdhfakjsdhf askjdfh aaf98762348576"
        i = 0
        for i in range(0, len(nopunct), 1):
            ok(not (RiTa.is_punct(nopunct[i])))
        ok(not (RiTa.is_punct("")))
        assert ((RiTa.is_punct("你")) is False)
        chineseCharacters = "這是一些隨機的中文字後來開始都會發揮吧首度落後兩分看來都是廢話卡卡聖誕賀卡還是阿塞德就回家啊哈薩克話說快時間啊但我阿拉斯加生命太短暂了不应该用来记恨人生在世谁都会有错误但我们很快会死去我们的罪过将会随我们的身体一起消失只留下精神的火花这就是我从来不想报复从来不认为生活不公平的原因我平静的生活"
        i = 0
        for i in range(0, len(chineseCharacters), 1):
            ok(not (RiTa.is_punct(chineseCharacters[i])), _jsstr("fail at ") + _jsstr(chineseCharacters[i]))
    def test_should_call_isstopword(self):
        stopWords = ["and", "a", "of", "in", "i", "you", "is", "to", "that", "it", "for", "on", "have", "with", "this", "be", "not", "are", "as", "was", "but", "or", "from", "my", "at", "if", "they", "your", "all", "he", "by", "one", "me", "what", "so", "can", "will", "do", "an", "about", "we", "just", "would", "there", "no", "like", "out", "his", "has", "up", "more", "who", "when", "don't", "some", "had", "them", "any", "their", "it's", "only", "which", "i'm", "been", "other", "were", "how", "then", "now", "her", "than", "she", "well", "also", "us", "very", "because", "am", "here", "could", "even", "him", "into", "our", "much", "too", "did", "should", "over", "want", "these", "may", "where", "most", "many", "those", "does", "why", "please", "off", "going", "its", "i've", "down", "that's", "can't", "you're", "didn't", "another", "around", "must", "few", "doesn't", "the", "every", "yes", "each", "maybe", "i'll", "away", "doing", "oh", "else", "isn't", "he's", "there's", "hi", "won't", "ok", "they're", "yeah", "mine", "we're", "what's", "shall", "she's", "hello", "okay", "here's", "less", "didn't", "said"]
        nonStopWords = ["apple", "orange", "cat", "dog", "play", "study", "worked", "paper"]
        for w in stopWords:
            ok(RiTa.is_stop_word(w), _jsstr(w) + _jsstr(" should be stop word"))
        for w in nonStopWords:
            ok(not (RiTa.is_stop_word(w)), _jsstr(w) + _jsstr(" should not be stop word"))
    def test_should_call_isconsonant(self):
        vowels = list("aeiou")
        for l in vowels:
            ok(not (RiTa.is_consonant(l)))
        ok(not (RiTa.is_consonant(None)))
        ok(not (RiTa.is_consonant()))
        ok(not (RiTa.is_consonant("word")))
        ok(not (RiTa.is_consonant("")))
        someConsonants = list("bdfks")
        for l in someConsonants:
            ok(RiTa.is_consonant(l))
    def test_should_call_tokenize(self):
        assert (RiTa.tokenize("") == [""])
        assert (RiTa.tokenize("The dog") == ["The", "dog"])
        input = None
        expected = None
        output = None
        input = "The student said 'learning is fun'"
        expected = ["The", "student", "said", "'", "learning", "is", "fun", "'"]
        output = RiTa.tokenize(input)
        assert (output == expected)
        input = "\"Oh God,\" he thought."
        expected = ["\"", "Oh", "God", ",", "\"", "he", "thought", "."]
        output = RiTa.tokenize(input)
        assert (output == expected)
        input = "The boy, dressed in red, ate an apple."
        expected = ["The", "boy", ",", "dressed", "in", "red", ",", "ate", "an", "apple", "."]
        output = RiTa.tokenize(input)
        assert (output == expected)
        input = "why? Me?huh?!"
        expected = ["why", "?", "Me", "?", "huh", "?", "!"]
        output = RiTa.tokenize(input)
        assert (output == expected)
        input = "123 123 1 2 3 1,1 1.1 23.45.67 22/05/2012 12th May,2012"
        expected = ["123", "123", "1", "2", "3", "1", ",", "1", "1.1", "23.45", ".", "67", "22/05/2012", "12th", "May", ",", "2012"]
        output = RiTa.tokenize(input)
        assert (output == expected)
        input = "The boy screamed, \"Where is my apple?\""
        expected = ["The", "boy", "screamed", ",", "\"", "Where", "is", "my", "apple", "?", "\""]
        output = RiTa.tokenize(input)
        assert (output == expected)
        input = "The boy screamed, “Where is my apple?”"
        expected = ["The", "boy", "screamed", ",", "“", "Where", "is", "my", "apple", "?", "”"]
        output = RiTa.tokenize(input)
        assert (output == expected)
        input = "The boy screamed, 'Where is my apple?'"
        expected = ["The", "boy", "screamed", ",", "'", "Where", "is", "my", "apple", "?", "'"]
        output = RiTa.tokenize(input)
        assert (output == expected)
        input = "The boy screamed, ‘Where is my apple?’"
        expected = ["The", "boy", "screamed", ",", "‘", "Where", "is", "my", "apple", "?", "’"]
        output = RiTa.tokenize(input)
        assert (output == expected)
        input = "dog, e.g. the cat."
        expected = ["dog", ",", "e.g.", "the", "cat", "."]
        output = RiTa.tokenize(input)
        assert (output == expected)
        input = "dog, i.e. the cat."
        expected = ["dog", ",", "i.e.", "the", "cat", "."]
        output = RiTa.tokenize(input)
        assert (output == expected)
        input = "What does e.g. mean? E.g. is used to introduce a few examples, not a complete list."
        expected = ["What", "does", "e.g.", "mean", "?", "E.g.", "is", "used", "to", "introduce", "a", "few", "examples", ",", "not", "a", "complete", "list", "."]
        output = RiTa.tokenize(input)
        assert (output == expected)
        input = "What does i.e. mean? I.e. means in other words."
        expected = ["What", "does", "i.e.", "mean", "?", "I.e.", "means", "in", "other", "words", "."]
        output = RiTa.tokenize(input)
        assert (output == expected)
        input = "it cost $30"
        expected = ["it", "cost", "$", "30"]
        output = RiTa.tokenize(input)
        assert (output == expected)
        input = "calculate 2^3"
        expected = ["calculate", "2", "^", "3"]
        output = RiTa.tokenize(input)
        assert (output == expected)
        input = "30% of the students"
        expected = ["30", "%", "of", "the", "students"]
        output = RiTa.tokenize(input)
        assert (output == expected)
        input = "it's 30°C outside"
        expected = ["it", "is", "30", "°", "C", "outside"]
        RiTa.SPLIT_CONTRACTIONS = True
        output = RiTa.tokenize(input)
        RiTa.SPLIT_CONTRACTIONS = False
        assert (output == expected)
        inputs = ["A simple sentence.", "that's why this is our place).", "most, punctuation; is. split: from! adjoining words?", "double quotes \"OK\"", "face-to-face class", "\"it is strange\", said John, \"Katherine does not drink alchol.\"", "\"What?!\", John yelled.", "more abbreviations: a.m. p.m. Cap. c. et al. etc. P.S. Ph.D R.I.P vs. v. Mr. Ms. Dr. Pf. Mx. Ind. Inc. Corp. Co.,Ltd. Co., Ltd. Co. Ltd. Ltd. Prof.", "elipsis dots... another elipsis dots…", "(testing) [brackets] {all} ⟨kinds⟩"]
        outputs = [["A", "simple", "sentence", "."], ["that's", "why", "this", "is", "our", "place", ")", "."], ["most", ",", "punctuation", ";", "is", ".", "split", ":", "from", "!", "adjoining", "words", "?"], ["double", "quotes", "\"", "OK", "\""], ["face-to-face", "class"], ["\"", "it", "is", "strange", "\"", ",", "said", "John", ",", "\"", "Katherine", "does", "not", "drink", "alchol", ".", "\""], ["\"", "What", "?", "!", "\"", ",", "John", "yelled", "."], ["more", "abbreviations", ":", "a.m.", "p.m.", "Cap.", "c.", "et al.", "etc.", "P.S.", "Ph.D", "R.I.P", "vs.", "v.", "Mr.", "Ms.", "Dr.", "Pf.", "Mx.", "Ind.", "Inc.", "Corp.", "Co.,Ltd.", "Co., Ltd.", "Co. Ltd.", "Ltd.", "Prof."], ["elipsis", "dots", "...", "another", "elipsis", "dots", "…"], ["(", "testing", ")", "[", "brackets", "]", "{", "all", "}", "⟨", "kinds", "⟩"]]
        assert (len(inputs) == len(outputs))
        i = 0
        for i in range(0, len(inputs), 1):
            assert (RiTa.tokenize(inputs[i]) == outputs[i])
        txt1 = "Dr. Chan is talking slowly with Mr. Cheng, and they're friends."
        txt2 = "He can't didn't couldn't shouldn't wouldn't eat."
        txt3 = "Wouldn't he eat?"
        txt4 = "It's not that I can't."
        txt5 = "We've found the cat."
        txt6 = "We didn't find the cat."
        RiTa.SPLIT_CONTRACTIONS = True
        assert (RiTa.tokenize(txt1) == ["Dr.", "Chan", "is", "talking", "slowly", "with", "Mr.", "Cheng", ",", "and", "they", "are", "friends", "."])
        assert (RiTa.tokenize(txt2) == ["He", "can", "not", "did", "not", "could", "not", "should", "not", "would", "not", "eat", "."])
        assert (RiTa.tokenize(txt3) == ["Would", "not", "he", "eat", "?"])
        assert (RiTa.tokenize(txt4) == ["It", "is", "not", "that", "I", "can", "not", "."])
        assert (RiTa.tokenize(txt5) == ["We", "have", "found", "the", "cat", "."])
        assert (RiTa.tokenize(txt6) == ["We", "did", "not", "find", "the", "cat", "."])
        RiTa.SPLIT_CONTRACTIONS = False
        assert (RiTa.tokenize(txt1) == ["Dr.", "Chan", "is", "talking", "slowly", "with", "Mr.", "Cheng", ",", "and", "they're", "friends", "."])
        assert (RiTa.tokenize(txt2) == ["He", "can't", "didn't", "couldn't", "shouldn't", "wouldn't", "eat", "."])
        assert (RiTa.tokenize(txt3) == ["Wouldn't", "he", "eat", "?"])
        assert (RiTa.tokenize(txt4) == ["It's", "not", "that", "I", "can't", "."])
        assert (RiTa.tokenize(txt5) == ["We've", "found", "the", "cat", "."])
        assert (RiTa.tokenize(txt6) == ["We", "didn't", "find", "the", "cat", "."])
    def test_should_call_untokenize(self):
        input = None
        output = None
        expected = None
        assert (RiTa.untokenize([""]) == "")
        expected = "We should consider the students' learning"
        input = ["We", "should", "consider", "the", "students", "'", "learning"]
        output = RiTa.untokenize(input)
        assert (output == expected)
        expected = "The boy, dressed in red, ate an apple."
        input = ["The", "boy", ",", "dressed", "in", "red", ",", "ate", "an", "apple", "."]
        output = RiTa.untokenize(input)
        assert (output == expected)
        expected = "We should consider the students’ learning"
        input = ["We", "should", "consider", "the", "students", "’", "learning"]
        output = RiTa.untokenize(input)
        assert (output == expected)
        expected = "The boy screamed, 'Where is my apple?'"
        input = ["The", "boy", "screamed", ",", "'", "Where", "is", "my", "apple", "?", "'"]
        output = RiTa.untokenize(input)
        assert (output == expected)
        expected = "Dr. Chan is talking slowly with Mr. Cheng, and they're friends."
        input = ["Dr", ".", "Chan", "is", "talking", "slowly", "with", "Mr", ".", "Cheng", ",", "and", "they're", "friends", "."]
        output = RiTa.untokenize(input)
        assert (output == expected)
        input = ["why", "?", "Me", "?", "huh", "?", "!"]
        expected = "why? Me? huh?!"
        output = RiTa.untokenize(input)
        assert (output == expected)
        input = ["123", "123", "1", "2", "3", "1", ",", "1", "1", ".", "1", "23", ".", "45", ".", "67", "22/05/2012", "12th", "May", ",", "2012"]
        expected = "123 123 1 2 3 1, 1 1. 1 23. 45. 67 22/05/2012 12th May, 2012"
        output = RiTa.untokenize(input)
        assert (output == expected)
        input = ["\"", "Oh", "God", ",", "\"", "he", "thought", "."]
        expected = "\"Oh God,\" he thought."
        output = RiTa.untokenize(input)
        assert (output == expected)
        expected = "The boy screamed, 'Where is my apple?'"
        input = ["The", "boy", "screamed", ",", "'", "Where", "is", "my", "apple", "?", "'"]
        output = RiTa.untokenize(input)
        assert (output == expected)
        input = ["She", "screamed", ",", "\"", "Oh", "God", "!", "\""]
        expected = "She screamed, \"Oh God!\""
        output = RiTa.untokenize(input)
        assert (output == expected)
        input = ["She", "screamed", ":", "\"", "Oh", "God", "!", "\""]
        expected = "She screamed: \"Oh God!\""
        output = RiTa.untokenize(input)
        assert (output == expected)
        input = ["\"", "Oh", ",", "God", "\"", ",", "he", "thought", ",", "\"", "not", "rain", "!", "\""]
        expected = "\"Oh, God\", he thought, \"not rain!\""
        output = RiTa.untokenize(input)
        assert (output == expected)
        expected = "The student said 'learning is fun'"
        input = ["The", "student", "said", "'", "learning", "is", "fun", "'"]
        output = RiTa.untokenize(input)
        assert (output == expected)
        expected = "dog, e.g. the cat."
        input = ["dog", ",", "e.g.", "the", "cat", "."]
        output = RiTa.untokenize(input)
        assert (output == expected)
        expected = "dog, i.e. the cat."
        input = ["dog", ",", "i.e.", "the", "cat", "."]
        output = RiTa.untokenize(input)
        assert (output == expected)
        expected = "What does e.g. mean? E.g. is used to introduce a few examples, not a complete list."
        input = ["What", "does", "e.g.", "mean", "?", "E.g.", "is", "used", "to", "introduce", "a", "few", "examples", ",", "not", "a", "complete", "list", "."]
        output = RiTa.untokenize(input)
        assert (output == expected)
        expected = "What does i.e. mean? I.e. means in other words."
        input = ["What", "does", "i.e.", "mean", "?", "I.e.", "means", "in", "other", "words", "."]
        output = RiTa.untokenize(input)
        assert (output == expected)
        outputs = ["A simple sentence.", "that's why this is our place).", "this is for semicolon; that is for else", "this is for 2^3 2*3", "this is for $30 and #30", "this is for 30°C or 30℃", "this is for a/b a⁄b", "this is for «guillemets»", "this... is… for ellipsis", "this line is 'for' single ‘quotation’ mark", "Katherine’s cat and John's cat", "this line is for (all) [kind] {of} ⟨brackets⟩ done", "this line is for the-dash", "30% of the student love day-dreaming.", "\"that test line\"", "my email address is name@domin.com", "it is www.google.com", "that is www6.cityu.edu.hk"]
        inputs = [["A", "simple", "sentence", "."], ["that's", "why", "this", "is", "our", "place", ")", "."], ["this", "is", "for", "semicolon", ";", "that", "is", "for", "else"], ["this", "is", "for", "2", "^", "3", "2", "*", "3"], ["this", "is", "for", "$", "30", "and", "#", "30"], ["this", "is", "for", "30", "°", "C", "or", "30", "℃"], ["this", "is", "for", "a", "/", "b", "a", "⁄", "b"], ["this", "is", "for", "«", "guillemets", "»"], ["this", "...", "is", "…", "for", "ellipsis"], ["this", "line", "is", "'", "for", "'", "single", "‘", "quotation", "’", "mark"], ["Katherine", "’", "s", "cat", "and", "John", "'", "s", "cat"], ["this", "line", "is", "for", "(", "all", ")", "[", "kind", "]", "{", "of", "}", "⟨", "brackets", "⟩", "done"], ["this", "line", "is", "for", "the", "-", "dash"], ["30", "%", "of", "the", "student", "love", "day", "-", "dreaming", "."], ["\"", "that", "test", "line", "\""], ["my", "email", "address", "is", "name", "@", "domin", ".", "com"], ["it", "is", "www", ".", "google", ".", "com"], ["that", "is", "www6", ".", "cityu", ".", "edu", ".", "hk"]]
        assert (len(inputs) == len(outputs))
        i = 0
        for i in range(0, len(inputs), 1):
            assert (RiTa.untokenize(inputs[i]) == outputs[i])
    def test_should_call_concordance(self):
        data = RiTa.concordance("The dog ate the cat")
        assert (len(list(data.keys())) == 5)
        assert (data["the"] == 1)
        assert (data["The"] == 1)
        assert (data["THE"] == None)
        data = RiTa.concordance("The dog ate the cat", JsDict({"ignoreCase": False, "ignoreStopWords": False, "ignorePunctuation": False}))
        assert (len(list(data.keys())) == 5)
        assert (data["the"] == 1)
        assert (data["The"] == 1)
        assert (data["THE"] == None)
        data = RiTa.concordance("The dog ate the cat", JsDict({"ignoreCase": True}))
        assert (len(list(data.keys())) == 4)
        assert (data["the"] == 2)
        assert (data["The"] == None)
        assert (data["THE"] == None)
        data = RiTa.concordance("The Dog ate the cat.", JsDict({"ignoreCase": True, "ignoreStopWords": True, "ignorePunctuation": True}))
        assert (len(list(data.keys())) == 3)
        assert (data["dog"] == 1)
        assert (data["the"] == None)
        assert (data["THE"] == None)
        data = RiTa.concordance("The dog ate the cat")
        assert (len(list(data.keys())) == 5)
        assert (data["the"] == 1)
        assert (data["The"] == 1)
        assert (data["THE"] == None)
        data = RiTa.concordance("'What a wonderful world;!:,?.'\"", JsDict({"ignorePunctuation": True}))
        assert (len(list(data.keys())) == 4)
        assert (data["!"] == None)
        data = RiTa.concordance("The dog ate the cat", JsDict({"ignoreStopWords": True}))
        assert (len(list(data.keys())) == 3)
        assert (data["The"] == None)
        data = RiTa.concordance("It was a dream of you.", JsDict({"ignoreStopWords": True}))
        assert (len(list(data.keys())) == 2)
        assert (data["It"] == None)
        assert (data["dream"] == 1)
        assert (data["."] == 1)
        data = RiTa.concordance("Fresh fried fish, Fish fresh fried.", JsDict({"wordsToIgnore": ["fish"], "ignoreCase": True, "ignorePunctuation": True}))
        assert (len(list(data.keys())) == 2)
        assert (data["fish"] == None)
        assert (data["fresh"] == 2)
        assert (data["fried"] == 2)
        with pytest.raises(Exception):
            return RiTa.concordance()
        c = RiTa.concorder
        c.concordance("dog dog dog cat cat cat cat cat")
        assert (c.count("cat") == 5)
        assert (c.count("dog") == 3)
        assert (c.count("fox") == 0)
    def test_should_call_kwic(self):
        result = None
        RiTa.concordance("A sentence includes cat.")
        result = RiTa.kwic("cat")
        assert (result[0] == "A sentence includes cat.")
        RiTa.concordance("Cats are beautiful.")
        result = RiTa.kwic("cat")
        assert (len(result) == 0)
        RiTa.concordance("This is a very very long sentence includes cat with many many words after it and before it.")
        result = RiTa.kwic("cat")
        assert (result[0] == "a very very long sentence includes cat with many many words after it")
        RiTa.concordance("A sentence includes cat in the middle. Another sentence includes cat in the middle.")
        result = RiTa.kwic("cat")
        assert (result[0] == "A sentence includes cat in the middle. Another sentence")
        assert (result[1] == "the middle. Another sentence includes cat in the middle.")
        RiTa.concordance("A sentence includes cat. Another sentence includes cat.")
        result = RiTa.kwic("cat")
        assert (result[0] == "A sentence includes cat. Another sentence includes cat.")
        assert (result[1] == None)
        RiTa.concordance("A sentence includes cat. Another sentence includes cat.")
        result = RiTa.kwic("cat", 4)
        assert (result[0] == "A sentence includes cat. Another sentence includes")
        assert (result[1] == ". Another sentence includes cat.")
        RiTa.concordance("The dog ate the cat, what a tragedy! Little Kali loves the cat, it was her best friend.")
        result = RiTa.kwic("cat", 4)
        assert (result[0] == "The dog ate the cat, what a tragedy")
        assert (result[1] == "Little Kali loves the cat, it was her")
        RiTa.concordance("A sentence includes cat. Another sentence includes cat.")
        result = RiTa.kwic("cat", JsDict({"numWords": 4}))
        assert (result[0] == "A sentence includes cat. Another sentence includes")
        assert (result[1] == ". Another sentence includes cat.")
        RiTa.concordance("The dog ate the cat, what a tragedy! Little Kali loves the cat, it was her best friend.")
        result = RiTa.kwic("cat", JsDict({"numWords": 4}))
        assert (result[0] == "The dog ate the cat, what a tragedy")
        assert (result[1] == "Little Kali loves the cat, it was her")
        result = RiTa.kwic("fish", JsDict({"text": "The dog ate the cat that ate the fish."}))
        assert (len(result) == 1)
        assert (result[0] == "ate the cat that ate the fish.")
        result = RiTa.kwic("fish", JsDict({"words": RiTa.tokenize("The dog ate the cat that ate the fish.")}))
        assert (len(result) == 1)
        assert (result[0] == "ate the cat that ate the fish.")
        result = RiTa.kwic("fish", JsDict({"words": RiTa.tokenize("The dog ate the cat that ate the fish. He yelled at the dog and buy a new fish."), "numWords": 7}))
        assert (len(result) == 2)
        assert (result[0] == "dog ate the cat that ate the fish. He yelled at the dog and")
        assert (result[1] == "at the dog and buy a new fish.")
        result = RiTa.kwic("fish", JsDict({"text": "The dog ate the cat that ate the fish. He yelled at the dog and buy a new fish.", "numWords": 7}))
        assert (len(result) == 2)
        assert (result[0] == "dog ate the cat that ate the fish. He yelled at the dog and")
        assert (result[1] == "at the dog and buy a new fish.")
    def test_should_call_sentences(self):
        input = None
        expected = None
        output = None
        eql(RiTa.sentences(""), [""])
        input = "Stealth's Open Frame, OEM style LCD monitors are designed for special mounting applications. The slim profile packaging provides an excellent solution for building into kiosks, consoles, machines and control panels. If you cannot find an off the shelf solution call us today about designing a custom solution to fit your exact needs."
        expected = ["Stealth's Open Frame, OEM style LCD monitors are designed for special mounting applications.", "The slim profile packaging provides an excellent solution for building into kiosks, consoles, machines and control panels.", "If you cannot find an off the shelf solution call us today about designing a custom solution to fit your exact needs."]
        output = RiTa.sentences(input)
        eql(output, expected)
        input = "\"The boy went fishing.\", he said. Then he went away."
        expected = ["\"The boy went fishing.\", he said.", "Then he went away."]
        output = RiTa.sentences(input)
        eql(output, expected)
        input = "The dog"
        output = RiTa.sentences(input)
        eql(output, [input])
        input = "I guess the dog ate the baby."
        output = RiTa.sentences(input)
        eql(output, [input])
        input = "Oh my god, the dog ate the baby!"
        output = RiTa.sentences(input)
        expected = ["Oh my god, the dog ate the baby!"]
        eql(output, expected)
        input = "Which dog ate the baby?"
        output = RiTa.sentences(input)
        expected = ["Which dog ate the baby?"]
        eql(output, expected)
        input = "'Yes, it was a dog that ate the baby', he said."
        output = RiTa.sentences(input)
        expected = ["'Yes, it was a dog that ate the baby', he said."]
        eql(output, expected)
        input = "The baby belonged to Mr. and Mrs. Stevens. They will be very sad."
        output = RiTa.sentences(input)
        expected = ["The baby belonged to Mr. and Mrs. Stevens.", "They will be very sad."]
        eql(output, expected)
        input = "\"The baby belonged to Mr. and Mrs. Stevens. They will be very sad.\""
        output = RiTa.sentences(input)
        expected = ["\"The baby belonged to Mr. and Mrs. Stevens.", "They will be very sad.\""]
        eql(output, expected)
        input = "“The baby belonged to Mr. and Mrs. Stevens. They will be very sad.”"
        output = RiTa.sentences(input)
        expected = ["“The baby belonged to Mr. and Mrs. Stevens.", "They will be very sad.”"]
        eql(output, expected)
        input = "\"My dear Mr. Bennet. Netherfield Park is let at last.\""
        output = RiTa.sentences(input)
        expected = ["\"My dear Mr. Bennet.", "Netherfield Park is let at last.\""]
        eql(output, expected)
        input = "“My dear Mr. Bennet. Netherfield Park is let at last.”"
        output = RiTa.sentences(input)
        expected = ["“My dear Mr. Bennet.", "Netherfield Park is let at last.”"]
        eql(output, expected)
        input = "She wrote: \"I don't paint anymore. For a while I thought it was just a phase that I'd get over.\""
        output = RiTa.sentences(input)
        expected = ["She wrote: \"I don't paint anymore.", "For a while I thought it was just a phase that I'd get over.\""]
        eql(output, expected)
        input = " I had a visit from my \"friend\" the tax man."
        output = RiTa.sentences(input)
        expected = ["I had a visit from my \"friend\" the tax man."]
        eql(output, expected)
    @pytest.mark.skip(reason="disabled in JS")  # /*LTR*/
    def test_should_call_gettransforms(self):
        transforms = RiTa.get_transforms()
        expected = ["articlize", "capitalize", "uppercase", "quotify", "norepeat", "pluralize", "art", "cap", "uc", "qq", "nr", "s"]
        for t in expected:
            ok(hasattr(transforms, t), _jsstr("fail at ") + _jsstr(t))
    @pytest.mark.skip(reason="disabled in JS")  # /*LTR*/
    def test_should_call_findstem(self):
        ok(RiTa.find_stem("dog"))
        ok(RiTa.find_stem("cat"))
        ok(RiTa.find_stem("play"))
        ok(RiTa.find_stem("run"))
        ok(not (RiTa.find_stem("dogs")))
        ok(not (RiTa.find_stem("played")))
        ok(not (RiTa.find_stem("writing")))
    def test_should_not_match_object_prototype_members_in_the_lexicon(self):
        for w in ["toString", "constructor", "valueOf", "hasOwnProperty", "__proto__", "isPrototypeOf"]:
            ok(not (RiTa.has_word(w)), _jsstr(w) + _jsstr(" should not be a word"))
        ok(RiTa.has_word("dog"), "dog should still be a word")
    def test_should_handle_words_matching_object_prototype_members_in_concordance(self):
        data = RiTa.concordance("constructor toString watch")
        assert (data == JsDict({"constructor": 1, "toString": 1, "watch": 1}))
        ok((len(RiTa.kwic("watch"))) == (1))
        ok((len(RiTa.kwic("toString"))) == (1))
        ok((len(RiTa.kwic("nonexistentword"))) == (0))
    def test_should_call_isvowel_and_isconsonant_case_insensitively(self):
        ok(RiTa.is_vowel("A"))
        ok(RiTa.is_vowel("a"))
        ok(RiTa.is_consonant("B"))
        ok(RiTa.is_consonant("b"))
        ok(not (RiTa.is_vowel("B")))
        ok(not (RiTa.is_consonant("A")))
        ok(not (RiTa.is_consonant("1")))
        ok(not (RiTa.is_consonant("")))
        ok(not (RiTa.is_vowel("")))
        ok(not (RiTa.is_consonant(None)))
        assert ((RiTa.is_vowel("")) is False)
        assert ((RiTa.is_consonant("")) is False)
        assert ((RiTa.is_vowel(None)) is False)
        assert ((RiTa.is_consonant(None)) is False)
    def test_should_return_strict_booleans_from_ispunct_and_isabbrev(self):
        assert ((RiTa.is_punct("")) is False)
        assert ((RiTa.is_punct(",")) is True)
        assert ((RiTa.is_abbrev(123)) is False)
        assert ((RiTa.is_abbrev(None)) is False)
        assert ((RiTa.is_abbrev("Dr.")) is True)
    def test_should_cache_analyzer_results_and_invalidate_on_lexicon_swap(self):
        ok(RiTa.CACHING, "CACHING should default to true")
        orig = RiTa.lexicon.data
        try:
            before = RiTa.phones("cat")
            ok((len(before)) > (0))
            RiTa.lexicon.data = JsDict({"cat": ["s-ae1-t", "nn"]})
            assert (RiTa.phones("cat") == "s-ae-t")
            RiTa.lexicon.data = orig
            assert (RiTa.phones("cat") == before)
        finally:
            RiTa.lexicon.data = orig
    def test_should_use_o_1_set_mirrors_consistent_with_the_word_lists(self):
        def check(arr=None, set=None, *args):
            for w in arr:
                assert ((w in set) is True), _jsstr("missing ") + _jsstr(w)
        check(RiTa.STOP_WORDS, RiTa.STOP_WORDS_SET)
        check(RiTa.MASS_NOUNS, RiTa.MASS_NOUNS_SET)
        check(RiTa.QUESTIONS, RiTa.QUESTIONS_SET)
        assert (("notarealstopword" in RiTa.STOP_WORDS_SET) is False)
        assert (("notarealmassnoun" in RiTa.MASS_NOUNS_SET) is False)
    def test_should_honor_reassignment_of_the_word_lists(self):
        orig = RiTa.STOP_WORDS
        try:
            RiTa.STOP_WORDS = ["zebraterm"]
            assert ((RiTa.is_stop_word("zebraterm")) is True)
            assert ((RiTa.is_stop_word("the")) is False)
        finally:
            RiTa.STOP_WORDS = orig
        assert ((RiTa.is_stop_word("the")) is True)
    def test_should_honor_in_place_mutation_of_the_word_lists(self):
        list = RiTa.STOP_WORDS
        len = len(list)
        try:
            list.append("quokkaterm")
            assert ((RiTa.is_stop_word("quokkaterm")) is True)
            assert (RiTa.STOP_WORDS_SET.size == set(list).size)
            list.pop()
            assert ((RiTa.is_stop_word("quokkaterm")) is False)
        finally:
            if (len(list)) > (len):
                del list[len:]
        assert (("quokkaterm" in RiTa.STOP_WORDS_SET) is False)
    # (helper hoisted to module scope)
    # (helper hoisted to module scope)
    # (helper hoisted to module scope)
    # (helper hoisted to module scope)

def ok(a=None, m=None, *args):
    assert ((a) is True), m

def def_(res=None, m=None, *args):
    assert not ((res) is None), m

def eql(a=None, b=None, m=None, *args):
    assert (a == b)

def eq(a=None, b=None, m=None, *args):
    assert (a == b)

