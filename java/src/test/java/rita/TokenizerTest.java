package rita;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Map;
import org.junit.jupiter.api.Test;

/**
 * Ported line-by-line from <code>js/test/tokenizer-tests.js</code>.
 *
 * <p>Mapping: {@code expect(x).eql([...])} -> {@code assertArrayEquals}, {@code expect(x).eq(y)}
 * -> {@code assertEquals}, {@code expect(x).eq(true)} -> {@code assertTrue}. JS option objects
 * ({@code { sort: true }}) become {@link Map} literals; JS truthy values are kept verbatim
 * (e.g. {@code splitContractions: 1}) so the Java implementation must coerce them the same way.
 */
class TokenizerTest {

    @Test
    void shouldCallTokens() {

        String[] tokens;

        tokens = RiTa.tokens("A small one is like a big one.");
        assertArrayEquals(new String[] {"a", "small", "one", "is", "like", "big"}, tokens);

        tokens = RiTa.tokens("One escaped, she'd thought.", Map.of("splitContractions", true));
        assertArrayEquals(new String[] {"one", "escaped", "she", "had", "thought"}, tokens);

        String input = "She wrote: \"I don't paint anymore. For a while she thought it was just a phase that she'd gotten over.\"";

        tokens = RiTa.tokens(input);
        assertArrayEquals(new String[] {
            "she", "wrote", "i",
            "don't", "paint", "anymore",
            "for", "a", "while",
            "thought", "it", "was",
            "just", "phase", "that",
            "she'd", "gotten", "over"
        }, tokens);

        tokens = RiTa.tokens(input);
        assertArrayEquals(new String[] {
            "she", "wrote", "i",
            "don't", "paint", "anymore",
            "for", "a", "while",
            "thought", "it", "was",
            "just", "phase", "that",
            "she'd", "gotten", "over"
        }, tokens);

        tokens = RiTa.tokens(input, Map.of("sort", true));
        assertArrayEquals(new String[] {
            "a", "anymore", "don't",
            "for", "gotten", "i",
            "it", "just",
            "over", "paint", "phase",
            "she", "she'd", "that", "thought",
            "was", "while", "wrote"
        }, tokens);

        tokens = RiTa.tokens(input, Map.of("caseSensitive", true));
        assertArrayEquals(new String[] {
            "She", "wrote", "I",
            "don't", "paint", "anymore",
            "For", "a", "while",
            "she", "thought", "it",
            "was", "just", "phase",
            "that", "she'd", "gotten",
            "over"
        }, tokens);

        tokens = RiTa.tokens(input, Map.of("caseSensitive", true, "sort", true));
        assertArrayEquals(new String[] {
            "For", "I", "She",
            "a", "anymore", "don't",
            "gotten", "it", "just",
            "over", "paint", "phase",
            "she", "she'd", "that",
            "thought", "was", "while",
            "wrote"
        }, tokens);

        tokens = RiTa.tokens(input, Map.of("ignoreStopWords", true));
        assertArrayEquals(new String[] {
            "wrote", "paint",
            "anymore", "while",
            "thought", "phase",
            "she'd", "gotten"
        }, tokens);

        tokens = RiTa.tokens(input, Map.of("splitContractions", true));
        assertArrayEquals(new String[] {
            "she", "wrote", "i",
            "do", "not", "paint", "anymore",
            "for", "a", "while",
            "thought", "it", "was",
            "just", "phase", "that",
            "had", "gotten", "over"
        }, tokens);

        tokens = RiTa.tokens(input, Map.of("splitContractions", true, "sort", true));
        assertArrayEquals(new String[] {
            "a", "anymore", "do",
            "for", "gotten", "had", "i",
            "it", "just", "not",
            "over", "paint", "phase",
            "she", "that", "thought",
            "was", "while",
            "wrote"
        }, tokens);

        tokens = RiTa.tokens(input, Map.of("splitContractions", true, "includePunct", true));
        assertArrayEquals(new String[] {
            "she", "wrote", ":",
            "\"", "i", "do",
            "not", "paint", "anymore",
            ".", "for", "a",
            "while", "thought", "it",
            "was", "just", "phase",
            "that", "had", "gotten",
            "over"
        }, tokens);
    }

    @Test
    void shouldHandleTokenizeThenUntokenize() {
        String[] sentences = {
            "this is www.google.com",
            "it is 'hell'"
        };
        String[][] tokens = {
            {"this", "is", "www.google.com"},
            {"it", "is", "'", "hell", "'"},
        };
        for (int i = 0; i < sentences.length; i++) {
            String[] usingTokenize = RiTa.tokenize(sentences[i]);
            assertArrayEquals(tokens[i], usingTokenize);
            String usingUntokenize = RiTa.untokenize(usingTokenize);
            assertEquals(sentences[i], usingUntokenize);
        }
    }

    @Test
    void shouldHandleTokenizeThenUntokenizeTags() {
        String[] strings = {
            "<a>link</a>",
            "<span class=\"test\">in line</span>",
            "<!DOCTYPE html> <head><title>Test Page</title></head>",
            "<!--comment lines-->",
            "<p>this <br>is</br> a <br>paragraph <br/></p>",
            "<p>Link <a herf=\"https://hk.search.yahoo.com/search?p=cute+cat\">here</a> is about <span class=\"cat\">cute cat</span></p> <img src=\"cutecat.com/catpic001.jpg\" width=\"600\" />",
            "<p>a paragraph with an <span class=\"test\">in line element</span> and a <a href=\"https://www.google.com\">link to google</a>.</p>",
            "a <br/> b"
        };
        String[][] tokens = {
            {"<a>", "link", "</a>"},
            {"<span class=\"test\">", "in", "line", "</span>"},
            {"<!DOCTYPE html>", "<head>", "<title>", "Test", "Page", "</title>", "</head>"},
            {"<!--comment lines-->"},
            {"<p>", "this", "<br>", "is", "</br>", "a", "<br>", "paragraph", "<br/>", "</p>"},
            {"<p>", "Link", "<a herf=\"https://hk.search.yahoo.com/search?p=cute+cat\">", "here", "</a>", "is", "about", "<span class=\"cat\">", "cute", "cat", "</span>", "</p>", "<img src=\"cutecat.com/catpic001.jpg\" width=\"600\" />"},
            {"<p>", "a", "paragraph", "with", "an", "<span class=\"test\">", "in", "line", "element", "</span>", "and", "a", "<a href=\"https://www.google.com\">", "link", "to", "google", "</a>", ".", "</p>"},
            {"a", "<br/>", "b"}
        };
        assertEquals(strings.length, tokens.length);
        for (int i = 0; i < strings.length; i++) {
            String[] afterTokenize = RiTa.tokenize(strings[i]);
            assertArrayEquals(tokens[i], afterTokenize);
            String afterUntokenize = RiTa.untokenize(afterTokenize);
            assertEquals(strings[i], afterUntokenize);
        }
    }

    @Test
    void shouldCallTokenizeSplitContractions() {
        String[] inputs = {
            "That's why this is our place.",
            "that's why he'll win.",
            "that's why I'd lost."
        };
        String[][] outputs = {
            {"That", "is", "why", "this", "is", "our", "place", "."},
            {"that", "is", "why", "he", "will", "win", "."},
            {"that", "is", "why", "I", "had", "lost", "."}
        };
        for (int i = 0; i < inputs.length; i++) {
            // JS passes the truthy number 1; keep it verbatim so the Java impl coerces identically.
            String[] res = RiTa.tokenize(inputs[i], Map.of("splitContractions", 1));
            assertArrayEquals(outputs[i], res);
        }
    }

    @Test
    void shouldTokenizeCompoundWords() {

        assertArrayEquals(new String[] {"snow-capped"}, RiTa.tokenize("snow-capped"));
        assertArrayEquals(new String[] {"whole-hearted"}, RiTa.tokenize("whole-hearted"));
        assertArrayEquals(new String[] {"dun-colored"}, RiTa.tokenize("dun-colored"));
    }

    @Test
    void shouldCallTokenizeOnly() {

        assertArrayEquals(new String[] {""}, RiTa.tokenize(""));
        assertArrayEquals(new String[] {""}, RiTa.tokenize(" "));
        assertArrayEquals(new String[] {"The", "dog"}, RiTa.tokenize("The dog"));
        assertArrayEquals(new String[] {"The", "programs", "."}, RiTa.tokenize("The programs."));
        assertArrayEquals(new String[] {"The", "find", "."}, RiTa.tokenize("The find."));
        assertArrayEquals(new String[] {"The", "bancor", "."}, RiTa.tokenize("The bancor.", Map.of("debug", 0)));
        assertArrayEquals(new String[] {"The", "prof.", "ate", "."}, RiTa.tokenize("The prof. ate.", Map.of("debug", 0)));
        assertArrayEquals(new String[] {"The", "snow-capped", "peaks"}, RiTa.tokenize("The snow-capped peaks"));
        assertArrayEquals(new String[] {"The", "whole-hearted", "sighs"}, RiTa.tokenize("The whole-hearted sighs"));
        assertArrayEquals(new String[] {"The", "dun-colored", "hills"}, RiTa.tokenize("The dun-colored hills"));

        String input;
        String[] output, expected;

        input = "According to the prof. climate change was real.";
        expected = new String[] {"According", "to", "the", "prof.", "climate", "change", "was", "real", "."};
        output = RiTa.tokenize(input);
        assertArrayEquals(expected, output);

        input = "The student said 'learning is fun'";
        expected = new String[] {"The", "student", "said", "'", "learning", "is", "fun", "'"};
        output = RiTa.tokenize(input);
        assertArrayEquals(expected, output);

        input = "\"Oh God,\" he thought.";
        expected = new String[] {"\"", "Oh", "God", ",", "\"", "he", "thought", "."};
        output = RiTa.tokenize(input);
        assertArrayEquals(expected, output);

        input = "The boy, dressed in red, ate an apple.";
        expected = new String[] {"The", "boy", ",", "dressed", "in", "red", ",", "ate", "an", "apple", "."};
        output = RiTa.tokenize(input);
        assertArrayEquals(expected, output);

        input = "why? Me?huh?!";
        assertArrayEquals(new String[] {"why", "?", "Me", "?", "huh", "?", "!"}, RiTa.tokenize(input));

        input = "123 123 1 2 3 1,1 1.1 23.45.67 22/05/2012 12th May,2012";
        assertArrayEquals(new String[] {"123", "123", "1", "2", "3", "1", ",", "1", "1.1", "23.45", ".", "67", "22/05/2012", "12th", "May", ",", "2012"}, RiTa.tokenize(input));

        input = "The boy screamed, \"Where is my apple?\"";
        assertArrayEquals(new String[] {"The", "boy", "screamed", ",", "\"", "Where", "is", "my", "apple", "?", "\""}, RiTa.tokenize(input));

        input = "The boy screamed, \u201CWhere is my apple?\u201D";
        assertArrayEquals(new String[] {"The", "boy", "screamed", ",", "\u201C", "Where", "is", "my", "apple", "?", "\u201D"}, RiTa.tokenize(input));

        input = "The boy screamed, 'Where is my apple?'";
        assertArrayEquals(new String[] {"The", "boy", "screamed", ",", "'", "Where", "is", "my", "apple", "?", "'"}, RiTa.tokenize(input));

        input = "The boy screamed, \u2018Where is my apple?\u2019";
        assertArrayEquals(new String[] {"The", "boy", "screamed", ",", "\u2018", "Where", "is", "my", "apple", "?", "\u2019"}, RiTa.tokenize(input));

        input = "dog, e.g. the cat.";
        assertArrayEquals(new String[] {"dog", ",", "e.g.", "the", "cat", "."}, RiTa.tokenize(input));

        input = "dog, i.e. the cat.";
        assertArrayEquals(new String[] {"dog", ",", "i.e.", "the", "cat", "."}, RiTa.tokenize(input));

        input = "What does e.g. mean? E.g. is used to introduce a few examples, not a complete list.";
        assertArrayEquals(new String[] {"What", "does", "e.g.", "mean", "?", "E.g.", "is", "used", "to", "introduce", "a", "few", "examples", ",", "not", "a", "complete", "list", "."}, RiTa.tokenize(input));

        input = "What does i.e. mean? I.e. means in other words.";
        assertArrayEquals(new String[] {"What", "does", "i.e.", "mean", "?", "I.e.", "means", "in", "other", "words", "."}, RiTa.tokenize(input));

        // reference :PENN treebank tokenization document :ftp://ftp.cis.upenn.edu/pub/treebank/public_html/tokenization.html
        //            and aslo English punctuation Wiki page Latin abbreviations Wiki page
        // These cases are declared but not asserted in the JS source either; kept as a
        // record of the known-failing inputs.
        String[] inputs = {"A simple sentence.",
            "that's why this is our place).",
            "most, punctuation; is. split: from! adjoining words?",
            "double quotes \"OK\"", //Treebank tokenization document says double quotes (") are changed to doubled single forward- and backward- quotes (`` and '') tho
            "face-to-face class", // hyphenated words -> https://github.com/dhowe/rita/issues/65
            "\"it is strange\", said John, \"Katherine does not drink alchol.\"",
            "\"What?!\", John yelled.",
            //tests below this line don't pass
            "John's Katherine's Jack's Linda's students' people's",
            "more abbreviations: a.m. p.m. Cap. c. et al. etc. P.S. Ph.D R.I.P vs. v. Mr. Ms. Dr. Pf. Mx. Ind. Inc. Corp. Co,.Ltd. Co,. Ltd. Co. Lid. Ltd.",
            "(testing) [brackets] {all} \u27E8kinds\u27E9",
            "elipsis dots... another elipsis dots\u2026",
            "children's parents' won't gonna I'm"
        };
        String[][] outputs = {
            {"A", "simple", "sentence", "."},
            {"that's", "why", "this", "is", "our", "place", ")", "."},
            {"most", ",", "punctuation", ";", "is", ".", "split", ":", "from", "!", "adjoining", "words", "?"},
            {"double", "quotes", "\"", "OK", "\""},
            {"face", "-", "to", "-", "face", "class"},
            {"\"", "it", "is", "strange", "\"", ",", "said", "John", ",", "\"", "Katherine", "does", "not", "drink", "alchol", ".", "\""},
            {"\"", "What", "?", "!", "\"", ",", "John", "yelled", "."},
            //test below this line don't pass
            {"John", "'s", "katherine", "'s", "Jack", "'s", "Linda", "'s", "students", "'", "people", "'s"},
            {"more", "abbreviations", ":", "a.m.", "p.m.", "Cap.", "c.", "et al.", "etc.", "P.S.", "Ph.D", "R.I.P", "vs.", "v.", "Mr.", "Ms.", "Dr.", "Pf.", "Mx.", "Ind.", "Inc.", "Corp.", "Co.,Ltd", "Co., Ltd", "Co. Ltd.", "Ltd."},
            {"(", "testing", ")", "[", "brackets", "]", "{", "all", "}", "\u27E8", "kinds", "\u27E9"}, //this might not need to be fix coz \u27E8\u27E9 is rarely seen
            {"elipsis", "dots", "...", "another", "elipsis", "dots", "\u2026"},
            {"children", "'s", "parents", "'", "wo", "n't", "gon", "na", "I", "'m"}
        };
        // Declared but never asserted in the JS source either; kept verbatim for reference.
        // (The JS suite leaves these inputs/outputs unused — see the "don't pass" comments.)
        // Deliberately no assertion here, to match the JS source exactly.

        // contractions -------------------------

        String txt1 = "Dr. Chan is talking slowly with Mr. Cheng, and they're friends."; // strange but same as RiTa-java
        String txt2 = "He can't didn't couldn't shouldn't wouldn't eat.";
        String txt3 = "Wouldn't he eat?";
        String txt4 = "It's not that I can't.";
        String txt5 = "We've found the cat.";
        String txt6 = "We didn't find the cat.";

        RiTa.SPLIT_CONTRACTIONS = true;
        assertArrayEquals(new String[] {"Dr.", "Chan", "is", "talking", "slowly", "with", "Mr.", "Cheng", ",", "and", "they", "are", "friends", "."}, RiTa.tokenize(txt1));
        assertArrayEquals(new String[] {"He", "can", "not", "did", "not", "could", "not", "should", "not", "would", "not", "eat", "."}, RiTa.tokenize(txt2));
        assertArrayEquals(new String[] {"Would", "not", "he", "eat", "?"}, RiTa.tokenize(txt3));
        assertArrayEquals(new String[] {"It", "is", "not", "that", "I", "can", "not", "."}, RiTa.tokenize(txt4));
        assertArrayEquals(new String[] {"We", "have", "found", "the", "cat", "."}, RiTa.tokenize(txt5));
        assertArrayEquals(new String[] {"We", "did", "not", "find", "the", "cat", "."}, RiTa.tokenize(txt6));

        RiTa.SPLIT_CONTRACTIONS = false;
        assertArrayEquals(new String[] {"Dr.", "Chan", "is", "talking", "slowly", "with", "Mr.", "Cheng", ",", "and", "they're", "friends", "."}, RiTa.tokenize(txt1));
        assertArrayEquals(new String[] {"He", "can't", "didn't", "couldn't", "shouldn't", "wouldn't", "eat", "."}, RiTa.tokenize(txt2));
        assertArrayEquals(new String[] {"Wouldn't", "he", "eat", "?"}, RiTa.tokenize(txt3));
        assertArrayEquals(new String[] {"It's", "not", "that", "I", "can't", "."}, RiTa.tokenize(txt4));
        assertArrayEquals(new String[] {"We've", "found", "the", "cat", "."}, RiTa.tokenize(txt5));
        assertArrayEquals(new String[] {"We", "didn't", "find", "the", "cat", "."}, RiTa.tokenize(txt6));
    }

    @Test
    void shouldTokenizeTags() {

        // html tags (rita#103)
        String[] inputs = {
            "<br>",
            "<br/>",
            "</br>",
            "<a>link</a>",
            "<!DOCTYPE html>",
            "<span>inline</span>",
            "<h1>header</h1>",
            "<!-- this is a comment -->", //? should this be divided?
            "<a href=\"www.google.com\">a link to google</a>",
            "<p>this<br>is</br>a<br>paragraph<br/></p>",
            "<p>Link <a herf=\"https://hk.search.yahoo.com/search?p=cute+cat\">here</a> is about <span class=\"cat\">cute cat</span></p><img src=\"cutecat.com/catpic001.jpg\" width=\"600\" />",
            "1 < 2 and 3 > 2."
        };

        String[][] outputs = {
            {"<br>"},
            {"<br/>"},
            {"</br>"},
            {"<a>", "link", "</a>"},
            {"<!DOCTYPE html>"},
            {"<span>", "inline", "</span>"},
            {"<h1>", "header", "</h1>"},
            {"<!-- this is a comment -->"},
            {"<a href=\"www.google.com\">", "a", "link", "to", "google", "</a>"},
            {"<p>", "this", "<br>", "is", "</br>", "a", "<br>", "paragraph", "<br/>", "</p>"},
            {"<p>", "Link", "<a herf=\"https://hk.search.yahoo.com/search?p=cute+cat\">", "here", "</a>", "is", "about", "<span class=\"cat\">", "cute", "cat", "</span>", "</p>", "<img src=\"cutecat.com/catpic001.jpg\" width=\"600\" />"},
            {"1", "<", "2", "and", "3", ">", "2", "."}
        };
        assertEquals(inputs.length, outputs.length);
        for (int i = 0; i < inputs.length; i++) {
            String[] res = RiTa.tokenize(inputs[i]);
            assertArrayEquals(outputs[i], res);
        }
    }

    @Test
    void shouldCallUntokenize() {

        // JS calls untokenize() and untokenize(0) both yield ""; in Java both are null input.
        assertEquals("", RiTa.untokenize(null));
        assertEquals("", RiTa.untokenize(null));
        assertEquals("", RiTa.untokenize(new String[] {""}));
        assertEquals("", RiTa.untokenize(new String[] {" "}));

        String[] input;
        String output, expected;

        expected = "We should consider the students' learning";
        input = new String[] {"We", "should", "consider", "the", "students", "'", "learning"};
        output = RiTa.untokenize(input);
        assertEquals(expected, output);

        expected = "The boy, dressed in red, ate an apple.";
        input = new String[] {"The", "boy", ",", "dressed", "in", "red", ",", "ate", "an", "apple", "."};
        output = RiTa.untokenize(input);
        assertEquals(expected, output);

        expected = "We should consider the students\u2019 learning";
        output = RiTa.untokenize(new String[] {"We", "should", "consider", "the", "students", "\u2019", "learning"});
        assertEquals(expected, output);

        expected = "The boy screamed, 'Where is my apple?'";
        input = new String[] {"The", "boy", "screamed", ",", "'", "Where", "is", "my", "apple", "?", "'"};
        output = RiTa.untokenize(input);
        assertEquals(expected, output);

        expected = "Dr. Chan is talking slowly with Mr. Cheng, and they're friends."; // strange but same as RiTa-java
        output = RiTa.untokenize(new String[] {"Dr", ".", "Chan", "is", "talking", "slowly", "with", "Mr", ".", "Cheng", ",", "and", "they're", "friends", "."});
        assertEquals(expected, output);

        String expectedStr;

        expectedStr = "why? Me? huh?!";
        output = RiTa.untokenize(new String[] {"why", "?", "Me", "?", "huh", "?", "!"});
        assertEquals(expectedStr, output);

        expectedStr = "123 123 1 2 3 1, 1 1. 1 23. 45. 67 22/05/2012 12th May, 2012";
        output = RiTa.untokenize(new String[] {"123", "123", "1", "2", "3", "1", ",", "1", "1", ".", "1", "23", ".", "45", ".", "67", "22/05/2012", "12th", "May", ",", "2012"});
        assertEquals(expectedStr, output);

        expectedStr = "\"Oh God,\" he thought.";
        output = RiTa.untokenize(new String[] {"\"", "Oh", "God", ",", "\"", "he", "thought", "."});
        assertEquals(expectedStr, output);

        expected = "The boy screamed, 'Where is my apple?'";
        output = RiTa.untokenize(new String[] {"The", "boy", "screamed", ",", "'", "Where", "is", "my", "apple", "?", "'"});
        assertEquals(expected, output);

        expectedStr = "She screamed, \"Oh God!\"";
        output = RiTa.untokenize(new String[] {"She", "screamed", ",", "\"", "Oh", "God", "!", "\""});
        assertEquals(expectedStr, output);

        expectedStr = "She screamed: \"Oh God!\"";
        output = RiTa.untokenize(new String[] {"She", "screamed", ":", "\"", "Oh", "God", "!", "\""});
        assertEquals(expectedStr, output);

        expectedStr = "\"Oh, God\", he thought, \"not rain!\"";
        output = RiTa.untokenize(new String[] {"\"", "Oh", ",", "God", "\"", ",", "he", "thought", ",", "\"", "not", "rain", "!", "\""});
        assertEquals(expectedStr, output);

        expected = "The student said 'learning is fun'";
        output = RiTa.untokenize(new String[] {"The", "student", "said", "'", "learning", "is", "fun", "'"});
        assertEquals(expected, output);

        expected = "dog, e.g. the cat.";
        output = RiTa.untokenize(new String[] {"dog", ",", "e.g.", "the", "cat", "."});
        assertEquals(expected, output);

        expected = "dog, i.e. the cat.";
        output = RiTa.untokenize(new String[] {"dog", ",", "i.e.", "the", "cat", "."});
        assertEquals(expected, output);

        expected = "What does e.g. mean? E.g. is used to introduce a few examples, not a complete list.";
        output = RiTa.untokenize(new String[] {"What", "does", "e.g.", "mean", "?", "E.g.", "is", "used", "to", "introduce", "a", "few", "examples", ",", "not", "a", "complete", "list", "."});
        assertEquals(expected, output);

        expected = "What does i.e. mean? I.e. means in other words.";
        output = RiTa.untokenize(new String[] {"What", "does", "i.e.", "mean", "?", "I.e.", "means", "in", "other", "words", "."});
        assertEquals(expected, output);

        // more tests

        String[] outputs = {"A simple sentence.",
            "that's why this is our place).",
            "this is for semicolon; that is for else",
            "this is for 2^3 2*3",
            "this is for $30 and #30",
            "this is for 30\u00B0C or 30\u2103",
            "this is for a/b a\u2044b",
            "this is for \u00ABguillemets\u00BB",
            "this... is\u2026 for ellipsis",
            "this line is 'for' single \u2018quotation\u2019 mark",
            "Katherine\u2019s cat and John's cat",
            "this line is for (all) [kind] {of} \u27E8brackets\u27E9 done",
            "this line is for the-dash",
            "30% of the student love day-dreaming.",
            "\"that test line\"",
            "my email address is name@domin.com",
            "it is www.google.com",
            "that is www6.cityu.edu.hk"
        };

        String[][] inputs = {
            {"A", "simple", "sentence", "."},
            {"that's", "why", "this", "is", "our", "place", ")", "."},
            {"this", "is", "for", "semicolon", ";", "that", "is", "for", "else"},
            {"this", "is", "for", "2", "^", "3", "2", "*", "3"},
            {"this", "is", "for", "$", "30", "and", "#", "30"},
            {"this", "is", "for", "30", "\u00B0", "C", "or", "30", "\u2103"},
            {"this", "is", "for", "a", "/", "b", "a", "\u2044", "b"},
            {"this", "is", "for", "\u00AB", "guillemets", "\u00BB"},
            {"this", "...", "is", "\u2026", "for", "ellipsis"},
            {"this", "line", "is", "'", "for", "'", "single", "\u2018", "quotation", "\u2019", "mark"},
            {"Katherine", "\u2019", "s", "cat", "and", "John", "'", "s", "cat"},
            {"this", "line", "is", "for", "(", "all", ")", "[", "kind", "]", "{", "of", "}", "\u27E8", "brackets", "\u27E9", "done"},
            {"this", "line", "is", "for", "the", "-", "dash"},
            {"30", "%", "of", "the", "student", "love", "day", "-", "dreaming", "."},
            {"\"", "that", "test", "line", "\""},
            {"my", "email", "address", "is", "name", "@", "domin", ".", "com"},
            {"it", "is", "www", ".", "google", ".", "com"},
            {"that", "is", "www6", ".", "cityu", ".", "edu", ".", "hk"}
        };

        assertEquals(inputs.length, outputs.length);
        for (int i = 0; i < inputs.length; i++) {
            assertEquals(outputs[i], RiTa.untokenize(inputs[i]));
        }
    }

    @Test
    void shouldUntokenizeTags() {

        String[][] inputs = {
            {"1", "<", "2"},
            {"<", "a", ">"},
            {"<", "a", ">", "link", "<", "/", "a", ">"},
            {"<", "span", ">", "some", "text", "here", "<", "/", "span", ">"},
            {"<", "p", ">", "some", "text", "<", "br", "/", ">", "new", "line", "<", "/", "p", ">"},
            {"something", "<", "a", "href", "=", "\"", "www", ".", "google", ".", "com", "\"", ">", "link", "to", "google", "<", "/", "a", ">"},
            {"<", "!", "DOCTYPE", "html", ">"},
            {"<", "p", ">", "1", "<", "2", "is", "truth", "<", "/", "p", ">"},
            {"a", "<", "!", "-", "-", "code", "comment", "-", "-", ">", "b"}
        };

        String[] outputs = {
            "1 < 2",
            "<a>",
            "<a>link</a>",
            "<span>some text here</span>",
            "<p>some text <br/> new line</p>",
            "something <a href = \"www.google.com\">link to google</a>",
            "<!DOCTYPE html>",
            "<p>1 < 2 is truth</p>",
            "a <!--code comment--> b"
        };

        assertEquals(inputs.length, outputs.length);
        for (int i = 0; i < inputs.length; i++) {
            assertEquals(outputs[i], RiTa.untokenize(inputs[i]));
        }
    }

    @Test
    void shouldCallSentences() {

        String input = "Stealth's Open Frame, OEM style LCD monitors are designed for special mounting applications. The slim profile packaging provides an excellent solution for building into kiosks, consoles, machines and control panels. If you cannot find an off the shelf solution call us today about designing a custom solution to fit your exact needs.";
        String[] expected = {"Stealth's Open Frame, OEM style LCD monitors are designed for special mounting applications.", "The slim profile packaging provides an excellent solution for building into kiosks, consoles, machines and control panels.", "If you cannot find an off the shelf solution call us today about designing a custom solution to fit your exact needs."};
        String[] output = RiTa.sentences(input);
        assertArrayEquals(expected, output);

        input = "Stealth's Open Frame, OEM style LCD monitors are designed for special mounting applications.\n\nThe slim profile packaging provides an excellent solution for building into kiosks, consoles, machines and control panels.\r\n If you cannot find an off the shelf solution call us today about designing a custom solution to fit your exact needs.";
        expected = new String[] {"Stealth's Open Frame, OEM style LCD monitors are designed for special mounting applications.", "The slim profile packaging provides an excellent solution for building into kiosks, consoles, machines and control panels.", "If you cannot find an off the shelf solution call us today about designing a custom solution to fit your exact needs."};
        output = RiTa.sentences(input);
        assertArrayEquals(expected, output);

        input = "\"The boy went fishing.\", he said. Then he went away.";
        expected = new String[] {"\"The boy went fishing.\", he said.", "Then he went away."};
        output = RiTa.sentences(input);
        assertArrayEquals(expected, output);

        input = "The dog";
        output = RiTa.sentences(input);
        assertArrayEquals(new String[] {input}, output);

        input = "I guess the dog ate the baby.";
        output = RiTa.sentences(input);
        assertArrayEquals(new String[] {input}, output);

        input = "Oh my god, the dog ate the baby!";
        output = RiTa.sentences(input);
        expected = new String[] {"Oh my god, the dog ate the baby!"};
        assertArrayEquals(expected, output);

        input = "Which dog ate the baby?";
        output = RiTa.sentences(input);
        expected = new String[] {"Which dog ate the baby?"};
        assertArrayEquals(expected, output);

        input = "'Yes, it was a dog that ate the baby', he said.";
        output = RiTa.sentences(input);
        expected = new String[] {"'Yes, it was a dog that ate the baby', he said."};
        assertArrayEquals(expected, output);

        input = "The baby belonged to Mr. and Mrs. Stevens. They will be very sad.";
        output = RiTa.sentences(input);
        expected = new String[] {"The baby belonged to Mr. and Mrs. Stevens.", "They will be very sad."};
        assertArrayEquals(expected, output);

        // More quotation marks
        input = "\"The baby belonged to Mr. and Mrs. Stevens. They will be very sad.\"";
        output = RiTa.sentences(input);
        expected = new String[] {"\"The baby belonged to Mr. and Mrs. Stevens.", "They will be very sad.\""};
        assertArrayEquals(expected, output);

        input = "\u201CThe baby belonged to Mr. and Mrs. Stevens. They will be very sad.\u201D";
        output = RiTa.sentences(input);
        expected = new String[] {"\u201CThe baby belonged to Mr. and Mrs. Stevens.", "They will be very sad.\u201D"};
        assertArrayEquals(expected, output);

        //https://github.com/dhowe/RiTa/issues/498
        input = "\"My dear Mr. Bennet. Netherfield Park is let at last.\"";
        output = RiTa.sentences(input);
        expected = new String[] {"\"My dear Mr. Bennet.", "Netherfield Park is let at last.\""};
        assertArrayEquals(expected, output);

        input = "\u201CMy dear Mr. Bennet. Netherfield Park is let at last.\u201D";
        output = RiTa.sentences(input);
        expected = new String[] {"\u201CMy dear Mr. Bennet.", "Netherfield Park is let at last.\u201D"};
        assertArrayEquals(expected, output);
        /*******************************************/

        input = "She wrote: \"I don't paint anymore. For a while I thought it was just a phase that I'd get over.\"";
        output = RiTa.sentences(input);
        expected = new String[] {"She wrote: \"I don't paint anymore.", "For a while I thought it was just a phase that I'd get over.\""};
        assertArrayEquals(expected, output);

        input = " I had a visit from my \"friend\" the tax man.";
        output = RiTa.sentences(input);
        expected = new String[] {"I had a visit from my \"friend\" the tax man."};
        assertArrayEquals(expected, output);

        assertArrayEquals(new String[] {""}, RiTa.sentences(""));

        assertArrayEquals(new String[] {"Today I would make something.", "A 4.7 inch gun.", "It was noon."},
            RiTa.sentences("Today I would make something. A 4.7 inch gun. It was noon."));
    }

    @Test
    void shouldHandleDashes() {
        //sentences
        String input = "Type two hyphens\u2014without a space before, after, or between them.";
        String[] output = RiTa.sentences(input);
        String[] expected = {"Type two hyphens\u2014without a space before, after, or between them."};
        assertArrayEquals(expected, output);

        input = "After a split second of hesitation, the second baseman leaped for the ball\u2014or, rather, limped for it.";
        output = RiTa.sentences(input);
        expected = new String[] {"After a split second of hesitation, the second baseman leaped for the ball\u2014or, rather, limped for it."};
        assertArrayEquals(expected, output);

        //tokenize and untokenize
        String sentence = "Type two hyphens--without a space\u2014before, after, or between them.";
        String[] tokens = {"Type", "two", "hyphens", "--", "without", "a", "space", "\u2014", "before", ",", "after", ",", "or", "between", "them", "."};
        assertArrayEquals(tokens, RiTa.tokenize(sentence));
        assertEquals(sentence, RiTa.untokenize(tokens));

        sentence = "Phones, hand-held computers, and built-in TVs\u2014each a possible distraction\u2014can lead to a dangerous situation if used while driving.";
        tokens = new String[] {"Phones", ",", "hand-held", "computers", ",", "and", "built-in", "TVs", "\u2014", "each", "a", "possible", "distraction", "\u2014", "can", "lead", "to", "a", "dangerous", "situation", "if", "used", "while", "driving", "."};
        assertArrayEquals(tokens, RiTa.tokenize(sentence));

        sentence = "He is afraid of two things--spiders and senior prom.";
        tokens = new String[] {"He", "is", "afraid", "of", "two", "things", "--", "spiders", "and", "senior", "prom", "."};
        assertArrayEquals(tokens, RiTa.tokenize(sentence));
        assertEquals(sentence, RiTa.untokenize(tokens));

        sentence = "The teacher assigned pages 101\u2013181 for tonight's reading material.";
        tokens = new String[] {"The", "teacher", "assigned", "pages", "101", "\u2013", "181", "for", "tonight's", "reading", "material", "."};
        assertArrayEquals(tokens, RiTa.tokenize(sentence));
        assertEquals(sentence, RiTa.untokenize(tokens));
    }

    @Test
    void shouldHandleDecimalNumbers() {
        // Support number formats:  	3.14529, 1.9e10, 123,340.00, -255.34
        assertArrayEquals(new String[] {"27.3"}, RiTa.tokenize("27.3"));
        assertArrayEquals(new String[] {"-27.3"}, RiTa.tokenize("-27.3"));
        assertArrayEquals(new String[] {"1.9e10"}, RiTa.tokenize("1.9e10"));
        assertArrayEquals(new String[] {"200,000.51"}, RiTa.tokenize("200,000.51"));
        assertArrayEquals(new String[] {"-200,000.51"}, RiTa.tokenize("-200,000.51"));
        assertArrayEquals(new String[] {"His", "score", "was", "91.2"}, RiTa.tokenize("His score was 91.2"));
        assertArrayEquals(new String[] {"He", "owed", "200,000", "dollars", "."}, RiTa.tokenize("He owed 200,000 dollars."));
        assertArrayEquals(new String[] {"He", "owed", "200,000", "."}, RiTa.tokenize("He owed 200,000."));
        assertArrayEquals(new String[] {"He", "owed", "200,000.50", "."}, RiTa.tokenize("He owed 200,000.50."));

        assertArrayEquals(new String[] {"A", "4.7", "inch", "gun", "."}, RiTa.tokenize("A 4.7 inch gun."));
    }

    @Test
    void shouldHandleDecimalNumbersInUntokenize() {
        // Support number formats:  	3.14529, 1.9e10, 123,340.00, -255.34
        assertEquals("27.3", RiTa.untokenize(new String[] {"27.3"}));
        assertEquals("-27.3", RiTa.untokenize(new String[] {"-27.3"}));
        assertEquals("1.9e10", RiTa.untokenize(new String[] {"1.9e10"}));
        assertEquals("200,000.51", RiTa.untokenize(new String[] {"200,000.51"}));
        assertEquals("-200,000.51", RiTa.untokenize(new String[] {"-200,000.51"}));
        assertEquals("His score was 91.2", RiTa.untokenize(new String[] {"His", "score", "was", "91.2"}));
        assertEquals("He owed 200,000 dollars.", RiTa.untokenize(new String[] {"He", "owed", "200,000", "dollars", "."}));
        assertEquals("He owed 200,000.", RiTa.untokenize(new String[] {"He", "owed", "200,000", "."}));
        assertEquals("He owed 200,000.50.", RiTa.untokenize(new String[] {"He", "owed", "200,000.50", "."}));
    }

    @Test
    void shouldHandleLineBreaks() {
        assertEquals("A CARAFE, THAT IS A BLIND GLASS.\nA kind in glass and a cousin.",
            RiTa.untokenize(RiTa.tokenize("A CARAFE, THAT IS A BLIND GLASS.\nA kind in glass and a cousin.")));
        assertEquals("A CARAFE, THAT IS A BLIND GLASS.\r\nA kind in glass and a cousin.",
            RiTa.untokenize(RiTa.tokenize("A CARAFE, THAT IS A BLIND GLASS.\r\nA kind in glass and a cousin.")));
    }

    @Test
    void shouldHandleNumbersWithCommas() {
        String input = "It was 19,700 square inches, the equivalent of 409 A5 pages.";
        String[] expected = {
            "It", "was",
            "19,700", "square",
            "inches", ",",
            "the", "equivalent",
            "of", "409",
            "A5", "pages",
            "."
        };
        String[] output = RiTa.tokenize(input);
        assertArrayEquals(expected, output);
    }

    @Test
    void shouldTokenizeUnderscoresToSpaces() {
        assertArrayEquals(new String[] {"a là"}, RiTa.tokenize("a_là"));
        assertArrayEquals(new String[] {"a la"}, RiTa.tokenize("a_la"));
        assertArrayEquals(new String[] {"à la"}, RiTa.tokenize("à_la"));
        assertArrayEquals(new String[] {"lá bas"}, RiTa.tokenize("lá_bas"));
        assertArrayEquals(new String[] {"la bas"}, RiTa.tokenize("la_bas"));
        assertArrayEquals(new String[] {"la bas"}, RiTa.tokenize("la_bas"));
        assertArrayEquals(new String[] {"comment ça-va"}, RiTa.tokenize("comment_ça-va"));
        assertArrayEquals(new String[] {"el águila"}, RiTa.tokenize("el_águila"));
        assertArrayEquals(new String[] {"9 inches"}, RiTa.tokenize("9_inches"));
    }

    @Test
    void shouldTreatUrlsEmailsAsSingleTokens() {
        String[] output = RiTa.tokenize("example.example@gmail.com");
        assertArrayEquals(new String[] {"example.example@gmail.com"}, output);

        output = RiTa.tokenize("an.example-email_address@gmail.com");
        assertArrayEquals(new String[] {"an.example-email_address@gmail.com"}, output);

        output = RiTa.tokenize("an.email.address@yahoo.com");
        assertArrayEquals(new String[] {"an.email.address@yahoo.com"}, output);

        output = RiTa.tokenize("MY.EMAIL.ADDRESS@YAHOO.COM");
        assertArrayEquals(new String[] {"MY.EMAIL.ADDRESS@YAHOO.COM"}, output);
        assertEquals("MY.EMAIL.ADDRESS@YAHOO.COM", RiTa.untokenize(output));

        output = RiTa.tokenize("This is my email address: email-address@gmail.com.");
        assertArrayEquals(new String[] {"This", "is", "my", "email", "address", ":", "email-address@gmail.com", "."}, output);
        assertEquals("This is my email address: email-address@gmail.com.", RiTa.untokenize(output));

        //urls
        //without http(s)
        output = RiTa.tokenize("www.example.com/an_example_page");
        assertArrayEquals(new String[] {"www.example.com/an_example_page"}, output);
        //with underscores
        output = RiTa.tokenize("https://example.com/an_example_page");
        assertArrayEquals(new String[] {"https://example.com/an_example_page"}, output);
        //with suffix
        output = RiTa.tokenize("https://example.org/index.html");
        assertArrayEquals(new String[] {"https://example.org/index.html"}, output);
        //with capital letters
        output = RiTa.tokenize("http://example.com/An_Example_Page");
        assertArrayEquals(new String[] {"http://example.com/An_Example_Page"}, output);
    }

    @Test
    void shouldHandleLineBreaksAgain() {
        assertEquals("A CARAFE, THAT IS A BLIND GLASS.\nA kind in glass and a cousin.",
            RiTa.untokenize(RiTa.tokenize("A CARAFE, THAT IS A BLIND GLASS.\nA kind in glass and a cousin.")));
        assertEquals("A CARAFE, THAT IS A BLIND GLASS.\r\nA kind in glass and a cousin.",
            RiTa.untokenize(RiTa.tokenize("A CARAFE, THAT IS A BLIND GLASS.\r\nA kind in glass and a cousin.")));
    }

    @Test
    void shouldSpaceDashesLikeEllipses() {
        // A dash token is glued to a preceding word but spaced after punctuation,
        // and -- like the ellipsis rule -- this must not depend on isLast, so that
        // untokenize of a token window matches the same tokens in full text.
        assertEquals("sight absolute? \u2014and in a", RiTa.untokenize(RiTa.tokenize("sight absolute? \u2014and in a")));
        assertEquals("Bang! Bang! \u2014shot th", RiTa.untokenize(RiTa.tokenize("Bang! Bang! \u2014shot th")));
        // isLast-independence: the window must be a prefix of the full-text form.
        assertTrue(RiTa.untokenize(new String[] {"absolute", "?", "\u2014", "and"})
            .startsWith(RiTa.untokenize(new String[] {"absolute", "?", "\u2014"})));
        assertEquals("and\u2014shot", RiTa.untokenize(new String[] {"and", "\u2014", "shot"}));

        // Hyphenated words and dashes between words are unchanged.
        assertEquals("face-to-face class", RiTa.untokenize(new String[] {"face", "-", "to", "-", "face", "class"}));
        assertEquals("the-dash", RiTa.untokenize(new String[] {"the", "-", "dash"}));
        assertEquals("day-dreaming", RiTa.untokenize(new String[] {"day", "-", "dreaming"}));
        assertEquals("things--spiders", RiTa.untokenize(new String[] {"things", "--", "spiders"}));
    }

    @Test
    void shouldRoundtripEllipsesAsSingleRawTokens() {
        // Any run of 2+ periods (whitespace allowed between) becomes ONE token that
        // keeps its exact original spelling, so untokenize returns it verbatim.
        assertArrayEquals(new String[] {"the", "loss", ". . .", "ocean"}, RiTa.tokenize("the loss. . . ocean"));
        assertArrayEquals(new String[] {"the", "loss", "...", "ocean"}, RiTa.tokenize("the loss... ocean"));
        assertArrayEquals(new String[] {"the", "loss", "..", "ocean"}, RiTa.tokenize("the loss.. ocean"));
        assertArrayEquals(new String[] {"the", "loss", ". .", "ocean"}, RiTa.tokenize("the loss. . ocean"));
        assertArrayEquals(new String[] {"the", "loss", "....", "ocean"}, RiTa.tokenize("the loss.... ocean"));
        assertArrayEquals(new String[] {"the", "loss", ". . . . .", "ocean"}, RiTa.tokenize("the loss. . . . . ocean"));

        // Dot count and internal spacing are preserved exactly.
        assertEquals("the loss. . . ocean", RiTa.untokenize(RiTa.tokenize("the loss. . . ocean")));
        assertEquals("the loss.... ocean", RiTa.untokenize(RiTa.tokenize("the loss.... ocean")));
        assertEquals("a.. b.... c", RiTa.untokenize(RiTa.tokenize("a.. b.... c")));
        assertEquals("away. . .. But", RiTa.untokenize(RiTa.tokenize("away. . .. But")));
        assertEquals("darkness. . . , the Book", RiTa.untokenize(RiTa.tokenize("darkness. . . , the Book")));

        // A run that follows punctuation or a token ending in a dot keeps the space
        // before it, and a run glued to a word stays glued.
        assertEquals("knew very well. ... And", RiTa.untokenize(RiTa.tokenize("knew very well. ... And")));
        assertEquals("oh, didn\u2019t I! ... Now", RiTa.untokenize(RiTa.tokenize("oh, didn\u2019t I! ... Now")));
        assertEquals("certain... But", RiTa.untokenize(RiTa.tokenize("certain... But")));
        assertEquals("well... so", RiTa.untokenize(RiTa.tokenize("well... so")));

        // Spacing must not depend on whether the run is the last token, so that
        // untokenize of a token window matches the same tokens in full text.
        assertTrue(RiTa.untokenize(new String[] {"I", "!", "...", "Now"})
            .startsWith(RiTa.untokenize(new String[] {"I", "!", "..."})));
        assertTrue(RiTa.untokenize(new String[] {"very", "well", "...", "so"})
            .startsWith(RiTa.untokenize(new String[] {"very", "well", "..."})));

        // Single dots are untouched: abbreviations, decimals and sentence ends.
        assertArrayEquals(new String[] {"e.g.", "the", "cat", "."}, RiTa.tokenize("e.g. the cat."));
        assertArrayEquals(new String[] {"Pi", "is", "3.14", "."}, RiTa.tokenize("Pi is 3.14."));
        assertArrayEquals(new String[] {"Mr.", "and", "Mrs", ".", "Stevens", "."}, RiTa.tokenize("Mr. and Mrs. Stevens."));
        assertEquals("end. Next", RiTa.untokenize(RiTa.tokenize("end. Next")));

        // Known limitation: whitespace before the first dot is not part of the token,
        // so "word . . ." canonicalizes to the glued "word. . ." form.
        assertEquals("the loss. . . ocean", RiTa.untokenize(RiTa.tokenize("the loss . . . ocean")));
    }
}
