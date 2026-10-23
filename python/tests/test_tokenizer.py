# AUTO-GENERATED from js/test/tokenizer-tests.js by scripts/js-to-py-tests.js — do not edit by hand.
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

class TestTokenizer:
    def test_should_call_tokens(self):
        tokens = None
        tokens = RiTa.tokens("A small one is like a big one.")
        assert (tokens == ["a", "small", "one", "is", "like", "big"])
        tokens = RiTa.tokens("One escaped, she'd thought.", {"splitContractions": True})
        assert (tokens == ["one", "escaped", "she", "had", "thought"])
        input = "She wrote: \"I don't paint anymore. For a while she thought it was just a phase that she'd gotten over.\""
        tokens = RiTa.tokens(input)
        assert (tokens == ["she", "wrote", "i", "don't", "paint", "anymore", "for", "a", "while", "thought", "it", "was", "just", "phase", "that", "she'd", "gotten", "over"])
        tokens = RiTa.tokens(input)
        assert (tokens == ["she", "wrote", "i", "don't", "paint", "anymore", "for", "a", "while", "thought", "it", "was", "just", "phase", "that", "she'd", "gotten", "over"])
        tokens = RiTa.tokens(input, {"sort": True})
        assert (tokens == ["a", "anymore", "don't", "for", "gotten", "i", "it", "just", "over", "paint", "phase", "she", "she'd", "that", "thought", "was", "while", "wrote"])
        tokens = RiTa.tokens(input, {"caseSensitive": True})
        assert (tokens == ["She", "wrote", "I", "don't", "paint", "anymore", "For", "a", "while", "she", "thought", "it", "was", "just", "phase", "that", "she'd", "gotten", "over"])
        tokens = RiTa.tokens(input, {"caseSensitive": True, "sort": True})
        assert (tokens == ["For", "I", "She", "a", "anymore", "don't", "gotten", "it", "just", "over", "paint", "phase", "she", "she'd", "that", "thought", "was", "while", "wrote"])
        tokens = RiTa.tokens(input, {"ignoreStopWords": True})
        assert (tokens == ["wrote", "paint", "anymore", "while", "thought", "phase", "she'd", "gotten"])
        tokens = RiTa.tokens(input, {"splitContractions": True})
        assert (tokens == ["she", "wrote", "i", "do", "not", "paint", "anymore", "for", "a", "while", "thought", "it", "was", "just", "phase", "that", "had", "gotten", "over"])
        tokens = RiTa.tokens(input, {"splitContractions": True, "sort": True})
        assert (tokens == ["a", "anymore", "do", "for", "gotten", "had", "i", "it", "just", "not", "over", "paint", "phase", "she", "that", "thought", "was", "while", "wrote"])
        tokens = RiTa.tokens(input, {"splitContractions": True, "includePunct": True})
        assert (tokens == ["she", "wrote", ":", "\"", "i", "do", "not", "paint", "anymore", ".", "for", "a", "while", "thought", "it", "was", "just", "phase", "that", "had", "gotten", "over"])
    def test_should_handle_tokenize_then_untokenize(self):
        sentences = ["this is www.google.com", "it is 'hell'"]
        tokens = [["this", "is", "www.google.com"], ["it", "is", "'", "hell", "'"]]
        i = 0
        for i in range(len(sentences)):
            usingTokenize = RiTa.tokenize(sentences[i])
            assert (usingTokenize == tokens[i])
            usingUntokenize = RiTa.untokenize(usingTokenize)
            assert (usingUntokenize == sentences[i])

    def test_should_handle_tokenize_then_untokenize_tags(self):
        strings = ["<a>link</a>", "<span class=\"test\">in line</span>", "<!DOCTYPE html> <head><title>Test Page</title></head>", "<!--comment lines-->", "<p>this <br>is</br> a <br>paragraph <br/></p>", "<p>Link <a herf=\"https://hk.search.yahoo.com/search?p=cute+cat\">here</a> is about <span class=\"cat\">cute cat</span></p> <img src=\"cutecat.com/catpic001.jpg\" width=\"600\" />", "<p>a paragraph with an <span class=\"test\">in line element</span> and a <a href=\"https://www.google.com\">link to google</a>.</p>", "a <br/> b"]
        tokens = [["<a>", "link", "</a>"], ["<span class=\"test\">", "in", "line", "</span>"], ["<!DOCTYPE html>", "<head>", "<title>", "Test", "Page", "</title>", "</head>"], ["<!--comment lines-->"], ["<p>", "this", "<br>", "is", "</br>", "a", "<br>", "paragraph", "<br/>", "</p>"], ["<p>", "Link", "<a herf=\"https://hk.search.yahoo.com/search?p=cute+cat\">", "here", "</a>", "is", "about", "<span class=\"cat\">", "cute", "cat", "</span>", "</p>", "<img src=\"cutecat.com/catpic001.jpg\" width=\"600\" />"], ["<p>", "a", "paragraph", "with", "an", "<span class=\"test\">", "in", "line", "element", "</span>", "and", "a", "<a href=\"https://www.google.com\">", "link", "to", "google", "</a>", ".", "</p>"], ["a", "<br/>", "b"]]
        assert (len(strings) == len(tokens))
        i = 0
        for i in range(len(strings)):
            afterTokenize = RiTa.tokenize(strings[i])
            assert (afterTokenize == tokens[i])
            afterUntokenize = RiTa.untokenize(afterTokenize)
            assert (afterUntokenize == strings[i])
    def test_should_call_tokenize_splitcontractions(self):
        inputs = ["That's why this is our place.", "that's why he'll win.", "that's why I'd lost."]
        outputs = [["That", "is", "why", "this", "is", "our", "place", "."], ["that", "is", "why", "he", "will", "win", "."], ["that", "is", "why", "I", "had", "lost", "."]]
        i = 0
        for i in range(len(inputs)):
            res = RiTa.tokenize(inputs[i], {"splitContractions": 1})
            assert (res == outputs[i])
    def test_should_tokenize_compound_words(self):
        assert (RiTa.tokenize("snow-capped") == ["snow-capped"])
        assert (RiTa.tokenize("whole-hearted") == ["whole-hearted"])
        assert (RiTa.tokenize("dun-colored") == ["dun-colored"])
    def test_should_call_tokenize_only(self):
        assert (RiTa.tokenize("") == [""])
        assert (RiTa.tokenize(" ") == [""])
        assert (RiTa.tokenize("The dog") == ["The", "dog"])
        assert (RiTa.tokenize("The programs.") == ["The", "programs", "."])
        assert (RiTa.tokenize("The find.") == ["The", "find", "."])
        assert (RiTa.tokenize("The bancor.", {"debug": 0}) == ["The", "bancor", "."])
        assert (RiTa.tokenize("The prof. ate.", {"debug": 0}) == ["The", "prof.", "ate", "."])
        assert (RiTa.tokenize("The snow-capped peaks") == ["The", "snow-capped", "peaks"])
        assert (RiTa.tokenize("The whole-hearted sighs") == ["The", "whole-hearted", "sighs"])
        assert (RiTa.tokenize("The dun-colored hills") == ["The", "dun-colored", "hills"])
        input = None
        expected = None
        output = None
        input = "According to the prof. climate change was real."
        expected = ["According", "to", "the", "prof.", "climate", "change", "was", "real", "."]
        output = RiTa.tokenize(input)
        assert (output == expected)
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
        inputs = ["A simple sentence.", "that's why this is our place).", "most, punctuation; is. split: from! adjoining words?", "double quotes \"OK\"", "face-to-face class", "\"it is strange\", said John, \"Katherine does not drink alchol.\"", "\"What?!\", John yelled.", "John's Katherine's Jack's Linda's students' people's", "more abbreviations: a.m. p.m. Cap. c. et al. etc. P.S. Ph.D R.I.P vs. v. Mr. Ms. Dr. Pf. Mx. Ind. Inc. Corp. Co,.Ltd. Co,. Ltd. Co. Lid. Ltd.", "(testing) [brackets] {all} ⟨kinds⟩", "elipsis dots... another elipsis dots…", "children's parents' won't gonna I'm"]
        outputs = [["A", "simple", "sentence", "."], ["that's", "why", "this", "is", "our", "place", ")", "."], ["most", ",", "punctuation", ";", "is", ".", "split", ":", "from", "!", "adjoining", "words", "?"], ["double", "quotes", "\"", "OK", "\""], ["face", "-", "to", "-", "face", "class"], ["\"", "it", "is", "strange", "\"", ",", "said", "John", ",", "\"", "Katherine", "does", "not", "drink", "alchol", ".", "\""], ["\"", "What", "?", "!", "\"", ",", "John", "yelled", "."], ["John", "'s", "katherine", "'s", "Jack", "'s", "Linda", "'s", "students", "'", "people", "'s"], ["more", "abbreviations", ":", "a.m.", "p.m.", "Cap.", "c.", "et al.", "etc.", "P.S.", "Ph.D", "R.I.P", "vs.", "v.", "Mr.", "Ms.", "Dr.", "Pf.", "Mx.", "Ind.", "Inc.", "Corp.", "Co.,Ltd", "Co., Ltd", "Co. Ltd.", "Ltd."], ["(", "testing", ")", "[", "brackets", "]", "{", "all", "}", "⟨", "kinds", "⟩"], ["elipsis", "dots", "...", "another", "elipsis", "dots", "…"], ["children", "'s", "parents", "'", "wo", "n't", "gon", "na", "I", "'m"]]
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
    def test_should_tokenize_tags(self):
        inputs = ["<br>", "<br/>", "</br>", "<a>link</a>", "<!DOCTYPE html>", "<span>inline</span>", "<h1>header</h1>", "<!-- this is a comment -->", "<a href=\"www.google.com\">a link to google</a>", "<p>this<br>is</br>a<br>paragraph<br/></p>", "<p>Link <a herf=\"https://hk.search.yahoo.com/search?p=cute+cat\">here</a> is about <span class=\"cat\">cute cat</span></p><img src=\"cutecat.com/catpic001.jpg\" width=\"600\" />", "1 < 2 and 3 > 2."]
        outputs = [["<br>"], ["<br/>"], ["</br>"], ["<a>", "link", "</a>"], ["<!DOCTYPE html>"], ["<span>", "inline", "</span>"], ["<h1>", "header", "</h1>"], ["<!-- this is a comment -->"], ["<a href=\"www.google.com\">", "a", "link", "to", "google", "</a>"], ["<p>", "this", "<br>", "is", "</br>", "a", "<br>", "paragraph", "<br/>", "</p>"], ["<p>", "Link", "<a herf=\"https://hk.search.yahoo.com/search?p=cute+cat\">", "here", "</a>", "is", "about", "<span class=\"cat\">", "cute", "cat", "</span>", "</p>", "<img src=\"cutecat.com/catpic001.jpg\" width=\"600\" />"], ["1", "<", "2", "and", "3", ">", "2", "."]]
        assert (len(inputs) == len(outputs))
        i = 0
        for i in range(len(inputs)):
            res = RiTa.tokenize(inputs[i])
            assert (res == outputs[i])
    def test_should_call_untokenize(self):
        assert (RiTa.untokenize() == "")
        assert (RiTa.untokenize(0) == "")
        assert (RiTa.untokenize([""]) == "")
        assert (RiTa.untokenize([" "]) == "")
        input = None
        output = None
        expected = None
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
        for i in range(len(inputs)):
            assert (RiTa.untokenize(inputs[i]) == outputs[i])
    def test_should_untokenize_tags(self):
        inputs = [["1", "<", "2"], ["<", "a", ">"], ["<", "a", ">", "link", "<", "/", "a", ">"], ["<", "span", ">", "some", "text", "here", "<", "/", "span", ">"], ["<", "p", ">", "some", "text", "<", "br", "/", ">", "new", "line", "<", "/", "p", ">"], ["something", "<", "a", "href", "=", "\"", "www", ".", "google", ".", "com", "\"", ">", "link", "to", "google", "<", "/", "a", ">"], ["<", "!", "DOCTYPE", "html", ">"], ["<", "p", ">", "1", "<", "2", "is", "truth", "<", "/", "p", ">"], ["a", "<", "!", "-", "-", "code", "comment", "-", "-", ">", "b"]]
        outputs = ["1 < 2", "<a>", "<a>link</a>", "<span>some text here</span>", "<p>some text <br/> new line</p>", "something <a href = \"www.google.com\">link to google</a>", "<!DOCTYPE html>", "<p>1 < 2 is truth</p>", "a <!--code comment--> b"]
        assert (len(inputs) == len(outputs))
        i = 0
        for i in range(len(inputs)):
            assert (RiTa.untokenize(inputs[i]) == outputs[i])
    def test_should_call_sentences(self):
        input = "Stealth's Open Frame, OEM style LCD monitors are designed for special mounting applications. The slim profile packaging provides an excellent solution for building into kiosks, consoles, machines and control panels. If you cannot find an off the shelf solution call us today about designing a custom solution to fit your exact needs."
        expected = ["Stealth's Open Frame, OEM style LCD monitors are designed for special mounting applications.", "The slim profile packaging provides an excellent solution for building into kiosks, consoles, machines and control panels.", "If you cannot find an off the shelf solution call us today about designing a custom solution to fit your exact needs."]
        output = RiTa.sentences(input)
        assert (output == expected)
        input = "Stealth's Open Frame, OEM style LCD monitors are designed for special mounting applications.\n\nThe slim profile packaging provides an excellent solution for building into kiosks, consoles, machines and control panels.\r\n If you cannot find an off the shelf solution call us today about designing a custom solution to fit your exact needs."
        expected = ["Stealth's Open Frame, OEM style LCD monitors are designed for special mounting applications.", "The slim profile packaging provides an excellent solution for building into kiosks, consoles, machines and control panels.", "If you cannot find an off the shelf solution call us today about designing a custom solution to fit your exact needs."]
        output = RiTa.sentences(input)
        assert (output == expected)
        input = "\"The boy went fishing.\", he said. Then he went away."
        expected = ["\"The boy went fishing.\", he said.", "Then he went away."]
        output = RiTa.sentences(input)
        assert (output == expected)
        input = "The dog"
        output = RiTa.sentences(input)
        assert (output == [input])
        input = "I guess the dog ate the baby."
        output = RiTa.sentences(input)
        assert (output == [input])
        input = "Oh my god, the dog ate the baby!"
        output = RiTa.sentences(input)
        expected = ["Oh my god, the dog ate the baby!"]
        assert (output == expected)
        input = "Which dog ate the baby?"
        output = RiTa.sentences(input)
        expected = ["Which dog ate the baby?"]
        assert (output == expected)
        input = "'Yes, it was a dog that ate the baby', he said."
        output = RiTa.sentences(input)
        expected = ["'Yes, it was a dog that ate the baby', he said."]
        assert (output == expected)
        input = "The baby belonged to Mr. and Mrs. Stevens. They will be very sad."
        output = RiTa.sentences(input)
        expected = ["The baby belonged to Mr. and Mrs. Stevens.", "They will be very sad."]
        assert (output == expected)
        input = "\"The baby belonged to Mr. and Mrs. Stevens. They will be very sad.\""
        output = RiTa.sentences(input)
        expected = ["\"The baby belonged to Mr. and Mrs. Stevens.", "They will be very sad.\""]
        assert (output == expected)
        input = "“The baby belonged to Mr. and Mrs. Stevens. They will be very sad.”"
        output = RiTa.sentences(input)
        expected = ["“The baby belonged to Mr. and Mrs. Stevens.", "They will be very sad.”"]
        assert (output == expected)
        input = "\"My dear Mr. Bennet. Netherfield Park is let at last.\""
        output = RiTa.sentences(input)
        expected = ["\"My dear Mr. Bennet.", "Netherfield Park is let at last.\""]
        assert (output == expected)
        input = "“My dear Mr. Bennet. Netherfield Park is let at last.”"
        output = RiTa.sentences(input)
        expected = ["“My dear Mr. Bennet.", "Netherfield Park is let at last.”"]
        assert (output == expected)
        input = "She wrote: \"I don't paint anymore. For a while I thought it was just a phase that I'd get over.\""
        output = RiTa.sentences(input)
        expected = ["She wrote: \"I don't paint anymore.", "For a while I thought it was just a phase that I'd get over.\""]
        assert (output == expected)
        input = " I had a visit from my \"friend\" the tax man."
        output = RiTa.sentences(input)
        expected = ["I had a visit from my \"friend\" the tax man."]
        assert (output == expected)
        assert (RiTa.sentences("") == [""])
        assert (RiTa.sentences("Today I would make something. A 4.7 inch gun. It was noon.") == ["Today I would make something.", "A 4.7 inch gun.", "It was noon."])
    def test_should_handle_dashes(self):
        input = "Type two hyphens—without a space before, after, or between them."
        output = RiTa.sentences(input)
        expected = ["Type two hyphens—without a space before, after, or between them."]
        assert (output == expected)
        input = "After a split second of hesitation, the second baseman leaped for the ball—or, rather, limped for it."
        output = RiTa.sentences(input)
        expected = ["After a split second of hesitation, the second baseman leaped for the ball—or, rather, limped for it."]
        assert (output == expected)
        sentence = "Type two hyphens--without a space—before, after, or between them."
        output = ["Type", "two", "hyphens", "--", "without", "a", "space", "—", "before", ",", "after", ",", "or", "between", "them", "."]
        assert (RiTa.tokenize(sentence) == output)
        assert (RiTa.untokenize(output) == sentence)
        sentence = "Phones, hand-held computers, and built-in TVs—each a possible distraction—can lead to a dangerous situation if used while driving."
        output = ["Phones", ",", "hand-held", "computers", ",", "and", "built-in", "TVs", "—", "each", "a", "possible", "distraction", "—", "can", "lead", "to", "a", "dangerous", "situation", "if", "used", "while", "driving", "."]
        assert (RiTa.tokenize(sentence) == output)
        sentence = "He is afraid of two things--spiders and senior prom."
        output = ["He", "is", "afraid", "of", "two", "things", "--", "spiders", "and", "senior", "prom", "."]
        assert (RiTa.tokenize(sentence) == output)
        assert (RiTa.untokenize(output) == sentence)
        sentence = "The teacher assigned pages 101–181 for tonight's reading material."
        output = ["The", "teacher", "assigned", "pages", "101", "–", "181", "for", "tonight's", "reading", "material", "."]
        assert (RiTa.tokenize(sentence) == output)
        assert (RiTa.untokenize(output) == sentence)
    def test_should_handle_decimal_numbers(self):
        assert (RiTa.tokenize("27.3") == ["27.3"])
        assert (RiTa.tokenize("-27.3") == ["-27.3"])
        assert (RiTa.tokenize("1.9e10") == ["1.9e10"])
        assert (RiTa.tokenize("200,000.51") == ["200,000.51"])
        assert (RiTa.tokenize("-200,000.51") == ["-200,000.51"])
        assert (RiTa.tokenize("His score was 91.2") == ["His", "score", "was", "91.2"])
        assert (RiTa.tokenize("He owed 200,000 dollars.") == ["He", "owed", "200,000", "dollars", "."])
        assert (RiTa.tokenize("He owed 200,000.") == ["He", "owed", "200,000", "."])
        assert (RiTa.tokenize("He owed 200,000.50.") == ["He", "owed", "200,000.50", "."])
        assert (RiTa.tokenize("A 4.7 inch gun.") == ["A", "4.7", "inch", "gun", "."])
    def test_should_handle_decimal_numbers_in_untokenize(self):
        assert (RiTa.untokenize(["27.3"]) == "27.3")
        assert (RiTa.untokenize(["-27.3"]) == "-27.3")
        assert (RiTa.untokenize(["1.9e10"]) == "1.9e10")
        assert (RiTa.untokenize(["200,000.51"]) == "200,000.51")
        assert (RiTa.untokenize(["-200,000.51"]) == "-200,000.51")
        assert (RiTa.untokenize(["His", "score", "was", "91.2"]) == "His score was 91.2")
        assert (RiTa.untokenize(["He", "owed", "200,000", "dollars", "."]) == "He owed 200,000 dollars.")
        assert (RiTa.untokenize(["He", "owed", "200,000", "."]) == "He owed 200,000.")
        assert (RiTa.untokenize(["He", "owed", "200,000.50", "."]) == "He owed 200,000.50.")
    def test_should_handle_line_breaks(self):
        assert (RiTa.untokenize(RiTa.tokenize("A CARAFE, THAT IS A BLIND GLASS.\nA kind in glass and a cousin.")) == "A CARAFE, THAT IS A BLIND GLASS.\nA kind in glass and a cousin.")
        assert (RiTa.untokenize(RiTa.tokenize("A CARAFE, THAT IS A BLIND GLASS.\r\nA kind in glass and a cousin.")) == "A CARAFE, THAT IS A BLIND GLASS.\r\nA kind in glass and a cousin.")
    def test_should_handle_numbers_with_commas(self):
        input = None
        expected = None
        output = None
        input = "It was 19,700 square inches, the equivalent of 409 A5 pages."
        expected = ["It", "was", "19,700", "square", "inches", ",", "the", "equivalent", "of", "409", "A5", "pages", "."]
        output = RiTa.tokenize(input)
        assert (output == expected)
    def test_should_tokenize_underscores_to_spaces(self):
        assert (RiTa.tokenize("a_là") == ["a là"])
        assert (RiTa.tokenize("a_la") == ["a la"])
        assert (RiTa.tokenize("à_la") == ["à la"])
        assert (RiTa.tokenize("lá_bas") == ["lá bas"])
        assert (RiTa.tokenize("la_bas") == ["la bas"])
        assert (RiTa.tokenize("la_bas") == ["la bas"])
        assert (RiTa.tokenize("comment_ça-va") == ["comment ça-va"])
        assert (RiTa.tokenize("el_águila") == ["el águila"])
        assert (RiTa.tokenize("9_inches") == ["9 inches"])
    def test_should_treat_urls_emails_as_single_tokens(self):
        output = RiTa.tokenize("example.example@gmail.com")
        assert (output == ["example.example@gmail.com"])
        output = RiTa.tokenize("an.example-email_address@gmail.com")
        assert (output == ["an.example-email_address@gmail.com"])
        output = RiTa.tokenize("an.email.address@yahoo.com")
        assert (output == ["an.email.address@yahoo.com"])
        output = RiTa.tokenize("MY.EMAIL.ADDRESS@YAHOO.COM")
        assert (output == ["MY.EMAIL.ADDRESS@YAHOO.COM"])
        assert (RiTa.untokenize(output) == "MY.EMAIL.ADDRESS@YAHOO.COM")
        output = RiTa.tokenize("This is my email address: email-address@gmail.com.")
        assert (output == ["This", "is", "my", "email", "address", ":", "email-address@gmail.com", "."])
        assert (RiTa.untokenize(output) == "This is my email address: email-address@gmail.com.")
        output = RiTa.tokenize("www.example.com/an_example_page")
        assert (output == ["www.example.com/an_example_page"])
        output = RiTa.tokenize("https://example.com/an_example_page")
        assert (output == ["https://example.com/an_example_page"])
        output = RiTa.tokenize("https://example.org/index.html")
        assert (output == ["https://example.org/index.html"])
        output = RiTa.tokenize("http://example.com/An_Example_Page")
        assert (output == ["http://example.com/An_Example_Page"])
    def test_should_handle_line_breaks_2(self):
        assert (RiTa.untokenize(RiTa.tokenize("A CARAFE, THAT IS A BLIND GLASS.\nA kind in glass and a cousin.")) == "A CARAFE, THAT IS A BLIND GLASS.\nA kind in glass and a cousin.")
        assert (RiTa.untokenize(RiTa.tokenize("A CARAFE, THAT IS A BLIND GLASS.\r\nA kind in glass and a cousin.")) == "A CARAFE, THAT IS A BLIND GLASS.\r\nA kind in glass and a cousin.")
    def test_should_space_dashes_like_ellipses(self):
        assert (RiTa.untokenize(RiTa.tokenize("sight absolute? —and in a")) == "sight absolute? —and in a")
        assert (RiTa.untokenize(RiTa.tokenize("Bang! Bang! —shot th")) == "Bang! Bang! —shot th")
        assert (RiTa.untokenize(["absolute", "?", "—", "and"]).startswith(RiTa.untokenize(["absolute", "?", "—"])) == True)
        assert (RiTa.untokenize(["and", "—", "shot"]) == "and—shot")
        assert (RiTa.untokenize(["face", "-", "to", "-", "face", "class"]) == "face-to-face class")
        assert (RiTa.untokenize(["the", "-", "dash"]) == "the-dash")
        assert (RiTa.untokenize(["day", "-", "dreaming"]) == "day-dreaming")
        assert (RiTa.untokenize(["things", "--", "spiders"]) == "things--spiders")
    def test_should_roundtrip_ellipses_as_single_raw_tokens(self):
        assert (RiTa.tokenize("the loss. . . ocean") == ["the", "loss", ". . .", "ocean"])
        assert (RiTa.tokenize("the loss... ocean") == ["the", "loss", "...", "ocean"])
        assert (RiTa.tokenize("the loss.. ocean") == ["the", "loss", "..", "ocean"])
        assert (RiTa.tokenize("the loss. . ocean") == ["the", "loss", ". .", "ocean"])
        assert (RiTa.tokenize("the loss.... ocean") == ["the", "loss", "....", "ocean"])
        assert (RiTa.tokenize("the loss. . . . . ocean") == ["the", "loss", ". . . . .", "ocean"])
        assert (RiTa.untokenize(RiTa.tokenize("the loss. . . ocean")) == "the loss. . . ocean")
        assert (RiTa.untokenize(RiTa.tokenize("the loss.... ocean")) == "the loss.... ocean")
        assert (RiTa.untokenize(RiTa.tokenize("a.. b.... c")) == "a.. b.... c")
        assert (RiTa.untokenize(RiTa.tokenize("away. . .. But")) == "away. . .. But")
        assert (RiTa.untokenize(RiTa.tokenize("darkness. . . , the Book")) == "darkness. . . , the Book")
        assert (RiTa.untokenize(RiTa.tokenize("knew very well. ... And")) == "knew very well. ... And")
        assert (RiTa.untokenize(RiTa.tokenize("oh, didn’t I! ... Now")) == "oh, didn’t I! ... Now")
        assert (RiTa.untokenize(RiTa.tokenize("certain... But")) == "certain... But")
        assert (RiTa.untokenize(RiTa.tokenize("well... so")) == "well... so")
        assert (RiTa.untokenize(["I", "!", "...", "Now"]).startswith(RiTa.untokenize(["I", "!", "..."])) == True)
        assert (RiTa.untokenize(["very", "well", "...", "so"]).startswith(RiTa.untokenize(["very", "well", "..."])) == True)
        assert (RiTa.tokenize("e.g. the cat.") == ["e.g.", "the", "cat", "."])
        assert (RiTa.tokenize("Pi is 3.14.") == ["Pi", "is", "3.14", "."])
        assert (RiTa.tokenize("Mr. and Mrs. Stevens.") == ["Mr.", "and", "Mrs", ".", "Stevens", "."])
        assert (RiTa.untokenize(RiTa.tokenize("end. Next")) == "end. Next")
        assert (RiTa.untokenize(RiTa.tokenize("the loss . . . ocean")) == "the loss. . . ocean")

