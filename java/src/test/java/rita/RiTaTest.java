package rita;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;

/**
 * Ported line-by-line from <code>js/test/rita-tests.js</code>. Every JS assertion maps to a Java
 * assertion: {@code ok(x)} -> {@code assertTrue}, {@code ok(!x)} -> {@code assertFalse},
 * {@code eql/eq} -> {@code assertEquals}/{@code assertArrayEquals}, {@code def} -> {@code assertNotNull},
 * {@code to.be.within(a,b)} -> {@code assertTrue(v>=a && v<=b)}, {@code to.have.members} -> order-independent
 * set/sort compare, {@code to.throw()} -> {@code assertThrows}.
 *
 * <p>JS bad-input asserts that pass a number or {@code undefined} to a String parameter
 * ({@code isAbbrev(1)}, {@code isVowel(undefined)}, {@code isConsonant()}) are not portable to the
 * typed Java API and are documented inline rather than ported.
 */
class RiTaTest {

    @Test
    void shouldHaveAccessToStatics() {
        // JS guards on `typeof process` and compares RiTa.VERSION to process.env.npm_package_version;
        // that environment plumbing is not portable to the JVM. The single JS assertion reduces to a
        // version sanity check.
        assertFalse(RiTa.VERSION == null || RiTa.VERSION.isEmpty());
    }

    @Test
    void shouldCallEvaluate() {
        String res;
        res = RiTa.evaluate("The [ox | ox | ox].pluralize run", 0);
        assertEquals("The oxen run", res);
        res = RiTa.evaluate("It was [honor].art to meet you", 0);
        assertEquals("It was an honor to meet you", res);
    }

    @Test
    void shouldCallAddTransform() {
        Object addRhyme = (Object) new java.util.function.Function<String, String>() {
            @Override
            public String apply(String word) {
                List<String> res = RiTa.lexicon.rhymesSync(word, Map.of("limit", 1));
                return word + " rhymes with " + RiTa.random(res);
            }
        };
        assertNull(RiTa.riscript.transforms.get("rhymes"));
        assertFalse(RiTa.riscript.transforms.containsKey("rhymes"));
        RiTa.addTransform("rhymes", addRhyme);
        assertNotNull(RiTa.riscript.transforms.get("rhymes"));
        assertTrue(RiTa.riscript.transforms.containsKey("rhymes"));
        String res = RiTa.evaluate("The [dog | dog | dog].rhymes");
        assertEquals("The dog rhymes with cog", res);
        RiTa.removeTransform("rhymes");
        assertFalse(RiTa.riscript.transforms.containsKey("rhymes"));

        res = RiTa.evaluate("The [dog | dog | dog].rhymes", 0, Map.of("silent", true));
        assertEquals("The dog.rhymes", res);
    }

    @Test
    void shouldCallRandom() {
        assertTrue(RiTa.random(10) >= 0 && RiTa.random(10) <= 10);
        assertTrue(RiTa.random(1, 10) >= 1 && RiTa.random(1, 10) <= 10);
        assertTrue(RiTa.random() >= 0 && RiTa.random() <= 1);
    }

    @Test
    void shouldCallRandi() {
        assertTrue(RiTa.randi(10) >= 0 && RiTa.randi(10) <= 9);
        assertTrue(RiTa.randi(1, 10) >= 1 && RiTa.randi(1, 10) <= 9);
        assertEquals(0, RiTa.randi());

        int a = RiTa.randi(1, 10);
        assertTrue(a == (int) a);
        int b = RiTa.randi(10);
        assertTrue(b == (int) b);
    }

    @Test
    void shouldCallRandomOrdering() {
        assertArrayEquals(new int[] {0}, RiTa.randomOrdering(1));
        assertTrue(setOf(RiTa.randomOrdering(2)).equals(Set.of(0, 1)));
        assertEquals(List.of("a"), RiTa.randomOrdering(List.of("a")));
        assertTrue(new HashSet<>(RiTa.randomOrdering(List.of("a", "b"))).equals(Set.of("a", "b")));

        int[] ro = RiTa.randomOrdering(4); // (also remove util-tests.js)
        assertEquals(4, ro.length);
        assertTrue(setOf(ro).equals(Set.of(0, 1, 2, 3)));
        List<Integer> arr = List.of(0, 3, 5, 7);
        List<Integer> ro2 = RiTa.randomOrdering(arr);
        assertEquals(4, ro2.size());
        assertTrue(new HashSet<>(ro2).equals(new HashSet<>(arr)));
    }

    @Test
    void shouldCallIsQuestion() {
        assertTrue(RiTa.isQuestion("what"));
        assertTrue(RiTa.isQuestion("what"));
        assertTrue(RiTa.isQuestion("what is this"));
        assertTrue(RiTa.isQuestion("what is this?"));
        assertTrue(RiTa.isQuestion("Does it?"));
        assertTrue(RiTa.isQuestion("Would you believe it?"));
        assertTrue(RiTa.isQuestion("Have you been?"));
        assertTrue(RiTa.isQuestion("Is this yours?"));
        assertTrue(RiTa.isQuestion("Are you done?"));
        assertTrue(RiTa.isQuestion("what is this? , where is that?"));
        assertTrue(RiTa.isQuestion("Will you come tomorrow?"));
        assertTrue(RiTa.isQuestion("Would you do that?"));
        assertFalse(RiTa.isQuestion("That is not a toy This is an apple"));
        assertFalse(RiTa.isQuestion("string"));
        assertFalse(RiTa.isQuestion("?"));
        assertFalse(RiTa.isQuestion(""));
    }

    @Test
    void shouldHandleArticlize() {
        boolean tmp = RiTa.SILENCE_LTS;
        RiTa.SILENCE_LTS = true;
        assertEquals("an honor", RiTa.articlize("honor"));

        String[] data = {
            "dog", "a dog",
            "ant", "an ant",
            "eagle", "an eagle",
            "ermintrout", "an ermintrout",
            "honor", "an honor"
        };
        for (int i = 0; i < data.length; i += 2) {
            assertEquals(data[i + 1], RiTa.articlize(data[i]));
        }

        RiTa.SILENCE_LTS = tmp;
    }

    @Test
    void shouldHandleArticlizePhrases() {
        String[] data = {
            "black dog", "a black dog",
            "black ant", "a black ant",
            "orange ant", "an orange ant",
            "great honor", "a great honor"
        };
        for (int i = 0; i < data.length; i += 2) {
            assertEquals(data[i + 1], RiTa.articlize(data[i]));
        }
    }

    @Test
    void shouldCallIsAbbrev() {
        assertTrue(RiTa.isAbbrev("Dr."));
        assertTrue(RiTa.isAbbrev("dr."));
        assertTrue(RiTa.isAbbrev("DR."));
        assertTrue(RiTa.isAbbrev("Dr. "));
        assertTrue(RiTa.isAbbrev(" Dr."));
        assertTrue(RiTa.isAbbrev("Prof."));
        assertTrue(RiTa.isAbbrev("prof."));

        assertFalse(RiTa.isAbbrev("Dr"));
        assertFalse(RiTa.isAbbrev("Doctor"));
        assertFalse(RiTa.isAbbrev("Doctor."));
        assertFalse(RiTa.isAbbrev("PRFO."));
        assertFalse(RiTa.isAbbrev("PrFo."));
        assertFalse(RiTa.isAbbrev("Professor"));
        assertFalse(RiTa.isAbbrev("professor"));
        assertFalse(RiTa.isAbbrev("PROFESSOR"));
        assertFalse(RiTa.isAbbrev("Professor."));
        assertFalse(RiTa.isAbbrev("@#$%^&*()"));
        assertFalse(RiTa.isAbbrev(""));
        assertFalse(RiTa.isAbbrev(null));
        // ok(!RiTa.isAbbrev(undefined));  -- non-portable: no undefined in Java
        // ok(!RiTa.isAbbrev(1));          -- non-portable: number input to a String parameter

        assertTrue(RiTa.isAbbrev("Dr.", Map.of("caseSensitive", true)));
        assertTrue(RiTa.isAbbrev("Dr. ", Map.of("caseSensitive", true)));
        assertTrue(RiTa.isAbbrev(" Dr.", Map.of("caseSensitive", true)));
        assertTrue(RiTa.isAbbrev("Prof.", Map.of("caseSensitive", true)));

        assertFalse(RiTa.isAbbrev("dr.", Map.of("caseSensitive", true)));
        assertFalse(RiTa.isAbbrev("DR.", Map.of("caseSensitive", true)));
        assertFalse(RiTa.isAbbrev("Dr", Map.of("caseSensitive", true)));
        assertFalse(RiTa.isAbbrev("Doctor", Map.of("caseSensitive", true)));
        assertFalse(RiTa.isAbbrev("Doctor.", Map.of("caseSensitive", true)));
        assertFalse(RiTa.isAbbrev("prof.", Map.of("caseSensitive", true)));
        assertFalse(RiTa.isAbbrev("PRFO.", Map.of("caseSensitive", true)));
        assertFalse(RiTa.isAbbrev("PrFo.", Map.of("caseSensitive", true)));
        assertFalse(RiTa.isAbbrev("Professor", Map.of("caseSensitive", true)));
        assertFalse(RiTa.isAbbrev("professor", Map.of("caseSensitive", true)));
        assertFalse(RiTa.isAbbrev("PROFESSOR", Map.of("caseSensitive", true)));
        assertFalse(RiTa.isAbbrev("Professor.", Map.of("caseSensitive", true)));
        assertFalse(RiTa.isAbbrev("@#$%^&*()", Map.of("caseSensitive", true)));
        assertFalse(RiTa.isAbbrev("", Map.of("caseSensitive", true)));
        assertFalse(RiTa.isAbbrev(null, Map.of("caseSensitive", true)));
        // ok(!RiTa.isAbbrev(undefined, {caseSensitive:true})); -- non-portable
        // ok(!RiTa.isAbbrev(1, {caseSensitive:true}));         -- non-portable
    }

    @Test
    void shouldCallIsPunct() {
        assertFalse(RiTa.isPunct("What the"));
        assertFalse(RiTa.isPunct("What ! the"));
        assertFalse(RiTa.isPunct(".#\"\\!@i$%&_+=}<>"));

        assertTrue(RiTa.isPunct("!"));
        assertTrue(RiTa.isPunct("?"));
        assertTrue(RiTa.isPunct("?!"));
        assertTrue(RiTa.isPunct("."));
        assertTrue(RiTa.isPunct(".."));
        assertTrue(RiTa.isPunct("..."));
        assertTrue(RiTa.isPunct("...."));
        assertTrue(RiTa.isPunct("%..."));

        assertFalse(RiTa.isPunct("! "));
        // space
        assertFalse(RiTa.isPunct(" !"));
        // space
        assertFalse(RiTa.isPunct("!  "));
        // double space
        assertFalse(RiTa.isPunct("  !"));
        // double space
        assertFalse(RiTa.isPunct("!  "));
        // tab space
        assertFalse(RiTa.isPunct("   !"));

        String punct;

        punct = "$%&^,";
        for (int i = 0; i < punct.length(); i++) {
            assertTrue(RiTa.isPunct(String.valueOf(punct.charAt(i))), "fail at:" + punct.charAt(i));
        }

        punct = ",;:!?)([].#\"\\!@$%&}<>|-/\\*{^";
        for (int i = 0; i < punct.length(); i++) {
            assertTrue(RiTa.isPunct(String.valueOf(punct.charAt(i))), "fail at:" + punct.charAt(i));
        }

        // TODO: also test multiple characters strings here ****
        punct = "\"\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD`'";
        for (int i = 0; i < punct.length(); i++) {
            assertTrue(RiTa.isPunct(String.valueOf(punct.charAt(i))), "fail at:" + punct.charAt(i));
        }

        punct = "\"\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD\uFFFD`',;:!?)([].#\"\\!@$%&}<>|-/\\*{^";
        for (int i = 0; i < punct.length(); i++) {
            assertTrue(RiTa.isPunct(String.valueOf(punct.charAt(i))), "fail at:" + punct.charAt(i));
        }

        // TODO: and here...
        String nopunct = "Helloasdfnals  FgG   \t kjdhfakjsdhf askjdfh aaf98762348576";
        for (int i = 0; i < nopunct.length(); i++) {
            assertFalse(RiTa.isPunct(String.valueOf(nopunct.charAt(i))));
        }

        assertFalse(RiTa.isPunct(""));

        // chinese character
        assertFalse(RiTa.isPunct("你")); // -> move to knownIssues
        String chineseCharacters = "這是一些隨機的中文字後來開始都會發揮吧首度落後兩分看來都是廢話卡卡聖誕賀卡還是阿塞德就回家啊哈薩克話說快時間啊但我阿拉斯加生命太短暂了不应该用来记恨人生在世谁都会有错误但我们很快会死去我们的罪过将会随我们的身体一起消失只留下精神的火花这就是我从来不想报复从来不认为生活不公平的原因我平静的生活";
        for (int i = 0; i < chineseCharacters.length(); i++) {
            assertFalse(RiTa.isPunct(String.valueOf(chineseCharacters.charAt(i))), "fail at " + chineseCharacters.charAt(i));
        }
    }

    @Test
    void shouldCallIsStopWord() {
        String[] stopWords = {"and", "a", "of", "in", "i", "you", "is", "to", "that", "it", "for", "on", "have", "with", "this", "be", "not", "are", "as", "was", "but", "or", "from", "my", "at", "if", "they", "your", "all", "he", "by", "one", "me", "what", "so", "can", "will", "do", "an", "about", "we", "just", "would", "there", "no", "like", "out", "his", "has", "up", "more", "who", "when", "don't", "some", "had", "them", "any", "their", "it's", "only", "which", "i'm", "been", "other", "were", "how", "then", "now", "her", "than", "she", "well", "also", "us", "very", "because", "am", "here", "could", "even", "him", "into", "our", "much", "too", "did", "should", "over", "want", "these", "may", "where", "most", "many", "those", "does", "why", "please", "off", "going", "its", "i've", "down", "that's", "can't", "you're", "didn't", "another", "around", "must", "few", "doesn't", "the", "every", "yes", "each", "maybe", "i'll", "away", "doing", "oh", "else", "isn't", "he's", "there's", "hi", "won't", "ok", "they're", "yeah", "mine", "we're", "what's", "shall", "she's", "hello", "okay", "here's", "less", "didn't", "said"};
        String[] nonStopWords = {"apple", "orange", "cat", "dog", "play", "study", "worked", "paper"};
        for (String w : stopWords) {
            assertTrue(RiTa.isStopWord(w), w + " should be stop word");
        }
        for (String w : nonStopWords) {
            assertFalse(RiTa.isStopWord(w), w + " should not be stop word");
        }
    }

    @Test
    void shouldCallIsConsonant() {
        String vowels = "aeiou";
        for (int i = 0; i < vowels.length(); i++) {
            assertFalse(RiTa.isConsonant(String.valueOf(vowels.charAt(i))));
        }
        assertFalse(RiTa.isConsonant(null));
        // ok(!RiTa.isConsonant()); -- non-portable: no-arg (undefined) call
        assertFalse(RiTa.isConsonant("word"));
        assertFalse(RiTa.isConsonant(""));
        String someConsonants = "bdfks";
        for (int i = 0; i < someConsonants.length(); i++) {
            assertTrue(RiTa.isConsonant(String.valueOf(someConsonants.charAt(i))));
        }
    }

    @Test
    void shouldCallTokenize() {
        assertArrayEquals(new String[] {""}, RiTa.tokenize(""));
        assertArrayEquals(new String[] {"The", "dog"}, RiTa.tokenize("The dog"));

        String input, expected, output;

        input = "The student said 'learning is fun'";
        expected = "The student said ' learning is fun '";
        output = String.join(" ", RiTa.tokenize(input));
        assertArrayEquals(new String[] {"The", "student", "said", "'", "learning", "is", "fun", "'"}, RiTa.tokenize(input));

        input = "\"Oh God,\" he thought.";
        output = String.join(" ", RiTa.tokenize(input));
        assertArrayEquals(new String[] {"\"", "Oh", "God", ",", "\"", "he", "thought", "."}, RiTa.tokenize(input));

        input = "The boy, dressed in red, ate an apple.";
        output = String.join(" ", RiTa.tokenize(input));
        assertArrayEquals(new String[] {"The", "boy", ",", "dressed", "in", "red", ",", "ate", "an", "apple", "."}, RiTa.tokenize(input));

        input = "why? Me?huh?!";
        output = String.join(" ", RiTa.tokenize(input));
        assertArrayEquals(new String[] {"why", "?", "Me", "?", "huh", "?", "!"}, RiTa.tokenize(input));

        input = "123 123 1 2 3 1,1 1.1 23.45.67 22/05/2012 12th May,2012";
        output = String.join(" ", RiTa.tokenize(input));
        assertArrayEquals(new String[] {"123", "123", "1", "2", "3", "1", ",", "1", "1.1", "23.45", ".", "67", "22/05/2012", "12th", "May", ",", "2012"}, RiTa.tokenize(input));

        input = "The boy screamed, \"Where is my apple?\"";
        output = String.join(" ", RiTa.tokenize(input));
        assertArrayEquals(new String[] {"The", "boy", "screamed", ",", "\"", "Where", "is", "my", "apple", "?", "\""}, RiTa.tokenize(input));

        input = "The boy screamed, \u201CWhere is my apple?\u201D";
        output = String.join(" ", RiTa.tokenize(input));
        assertArrayEquals(new String[] {"The", "boy", "screamed", ",", "\u201C", "Where", "is", "my", "apple", "?", "\u201D"}, RiTa.tokenize(input));

        input = "The boy screamed, 'Where is my apple?'";
        output = String.join(" ", RiTa.tokenize(input));
        assertArrayEquals(new String[] {"The", "boy", "screamed", ",", "'", "Where", "is", "my", "apple", "?", "'"}, RiTa.tokenize(input));

        input = "The boy screamed, \u2018Where is my apple?\u2019";
        output = String.join(" ", RiTa.tokenize(input));
        assertArrayEquals(new String[] {"The", "boy", "screamed", ",", "\u2018", "Where", "is", "my", "apple", "?", "\u2019"}, RiTa.tokenize(input));

        input = "dog, e.g. the cat.";
        output = String.join(" ", RiTa.tokenize(input));
        assertArrayEquals(new String[] {"dog", ",", "e.g.", "the", "cat", "."}, RiTa.tokenize(input));

        input = "dog, i.e. the cat.";
        output = String.join(" ", RiTa.tokenize(input));
        assertArrayEquals(new String[] {"dog", ",", "i.e.", "the", "cat", "."}, RiTa.tokenize(input));

        input = "What does e.g. mean? E.g. is used to introduce a few examples, not a complete list.";
        output = String.join(" ", RiTa.tokenize(input));
        assertArrayEquals(new String[] {"What", "does", "e.g.", "mean", "?", "E.g.", "is", "used", "to", "introduce", "a", "few", "examples", ",", "not", "a", "complete", "list", "."}, RiTa.tokenize(input));

        input = "What does i.e. mean? I.e. means in other words.";
        output = String.join(" ", RiTa.tokenize(input));
        assertArrayEquals(new String[] {"What", "does", "i.e.", "mean", "?", "I.e.", "means", "in", "other", "words", "."}, RiTa.tokenize(input));

        input = "it cost $30";
        output = String.join(" ", RiTa.tokenize(input));
        assertArrayEquals(new String[] {"it", "cost", "$", "30"}, RiTa.tokenize(input));

        input = "calculate 2^3";
        output = String.join(" ", RiTa.tokenize(input));
        assertArrayEquals(new String[] {"calculate", "2", "^", "3"}, RiTa.tokenize(input));

        input = "30% of the students";
        output = String.join(" ", RiTa.tokenize(input));
        assertArrayEquals(new String[] {"30", "%", "of", "the", "students"}, RiTa.tokenize(input));

        input = "it's 30\u00B0C outside";
        String[] expected2 = {"it", "is", "30", "\u00B0", "C", "outside"};
        RiTa.SPLIT_CONTRACTIONS = true;
        String[] out2 = RiTa.tokenize(input);
        RiTa.SPLIT_CONTRACTIONS = false;
        assertArrayEquals(expected2, out2);

        // reference :PENN treebank tokenization document
        String[] inputs = {"A simple sentence.",
            "that's why this is our place).",
            "most, punctuation; is. split: from! adjoining words?",
            "double quotes \"OK\"",
            "face-to-face class",
            "\"it is strange\", said John, \"Katherine does not drink alchol.\"",
            "\"What?!\", John yelled.",
            "more abbreviations: a.m. p.m. Cap. c. et al. etc. P.S. Ph.D R.I.P vs. v. Mr. Ms. Dr. Pf. Mx. Ind. Inc. Corp. Co.,Ltd. Co., Ltd. Co. Ltd. Ltd. Prof.",
            "elipsis dots... another elipsis dots\u2026",
            "(testing) [brackets] {all} \u27E8kinds\u27E9",
        };

        String[][] outputs = {
            {"A", "simple", "sentence", "."},
            {"that's", "why", "this", "is", "our", "place", ")", "."},
            {"most", ",", "punctuation", ";", "is", ".", "split", ":", "from", "!", "adjoining", "words", "?"},
            {"double", "quotes", "\"", "OK", "\""},
            {"face-to-face", "class"},
            {"\"", "it", "is", "strange", "\"", ",", "said", "John", ",", "\"", "Katherine", "does", "not", "drink", "alchol", ".", "\""},
            {"\"", "What", "?", "!", "\"", ",", "John", "yelled", "."},
            {"more", "abbreviations", ":", "a.m.", "p.m.", "Cap.", "c.", "et al.", "etc.", "P.S.", "Ph.D", "R.I.P", "vs.", "v.", "Mr.", "Ms.", "Dr.", "Pf.", "Mx.", "Ind.", "Inc.", "Corp.", "Co.,Ltd.", "Co., Ltd.", "Co. Ltd.", "Ltd.", "Prof."},
            {"elipsis", "dots", "...", "another", "elipsis", "dots", "\u2026"},
            {"(", "testing", ")", "[", "brackets", "]", "{", "all", "}", "\u27E8", "kinds", "\u27E9"},
        };

        assertEquals(inputs.length, outputs.length);
        for (int i = 0; i < inputs.length; i++) {
            assertArrayEquals(outputs[i], RiTa.tokenize(inputs[i]));
        }

        // contractions -------------------------

        String txt1 = "Dr. Chan is talking slowly with Mr. Cheng, and they're friends.";
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
    void shouldCallUntokenize() {
        String input, output, expected;

        assertEquals("", RiTa.untokenize(new String[] {""}));

        expected = "We should consider the students' learning";
        input = "We should consider the students ' learning";
        output = RiTa.untokenize(new String[] {"We", "should", "consider", "the", "students", "'", "learning"});
        assertEquals(expected, output);

        expected = "The boy, dressed in red, ate an apple.";
        input = "The boy , dressed in red , ate an apple .";
        output = RiTa.untokenize(new String[] {"The", "boy", ",", "dressed", "in", "red", ",", "ate", "an", "apple", "."});
        assertEquals(expected, output);

        expected = "We should consider the students\u2019 learning";
        output = RiTa.untokenize(new String[] {"We", "should", "consider", "the", "students", "\u2019", "learning"});
        assertEquals(expected, output);

        expected = "The boy screamed, 'Where is my apple?'";
        output = RiTa.untokenize(new String[] {"The", "boy", "screamed", ",", "'", "Where", "is", "my", "apple", "?", "'"});
        assertEquals(expected, output);

        expected = "Dr. Chan is talking slowly with Mr. Cheng, and they're friends.";
        output = RiTa.untokenize(new String[] {"Dr", ".", "Chan", "is", "talking", "slowly", "with", "Mr", ".", "Cheng", ",", "and", "they're", "friends", "."});
        assertEquals(expected, output);

        output = RiTa.untokenize(new String[] {"why", "?", "Me", "?", "huh", "?", "!"});
        assertEquals("why? Me? huh?!", output);

        output = RiTa.untokenize(new String[] {"123", "123", "1", "2", "3", "1", ",", "1", "1", ".", "1", "23", ".", "45", ".", "67", "22/05/2012", "12th", "May", ",", "2012"});
        assertEquals("123 123 1 2 3 1, 1 1. 1 23. 45. 67 22/05/2012 12th May, 2012", output);

        output = RiTa.untokenize(new String[] {"\"", "Oh", "God", ",", "\"", "he", "thought", "."});
        assertEquals("\"Oh God,\" he thought.", output);

        expected = "The boy screamed, 'Where is my apple?'";
        output = RiTa.untokenize(new String[] {"The", "boy", "screamed", ",", "'", "Where", "is", "my", "apple", "?", "'"});
        assertEquals(expected, output);

        output = RiTa.untokenize(new String[] {"She", "screamed", ",", "\"", "Oh", "God", "!", "\""});
        assertEquals("She screamed, \"Oh God!\"", output);

        output = RiTa.untokenize(new String[] {"She", "screamed", ":", "\"", "Oh", "God", "!", "\""});
        assertEquals("She screamed: \"Oh God!\"", output);

        output = RiTa.untokenize(new String[] {"\"", "Oh", ",", "God", "\"", ",", "he", "thought", ",", "\"", "not", "rain", "!", "\""});
        assertEquals("\"Oh, God\", he thought, \"not rain!\"", output);

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

        // refer to english punctuation marks list on Wiki

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
    void shouldCallConcordance() {
        Map<String, Integer> data = RiTa.concordance("The dog ate the cat");
        assertEquals(5, data.size());
        assertEquals(1, (int) data.get("the"));
        assertEquals(1, (int) data.get("The"));
        assertNull(data.get("THE"));

        data = RiTa.concordance("The dog ate the cat", Map.of(
            "ignoreCase", false,
            "ignoreStopWords", false,
            "ignorePunctuation", false));

        assertEquals(5, data.size());
        assertEquals(1, (int) data.get("the"));
        assertEquals(1, (int) data.get("The"));
        assertNull(data.get("THE")); // same result

        data = RiTa.concordance("The dog ate the cat", Map.of("ignoreCase", true));
        assertEquals(4, data.size());
        assertEquals(2, (int) data.get("the"));
        assertNull(data.get("The"));
        assertNull(data.get("THE"));

        data = RiTa.concordance("The Dog ate the cat.", Map.of(
            "ignoreCase", true,
            "ignoreStopWords", true,
            "ignorePunctuation", true));

        assertEquals(3, data.size());
        assertEquals(1, (int) data.get("dog"));
        assertNull(data.get("the"));
        assertNull(data.get("THE"));

        // opts should be back to default
        data = RiTa.concordance("The dog ate the cat");
        assertEquals(5, data.size());
        assertEquals(1, (int) data.get("the"));
        assertEquals(1, (int) data.get("The"));
        assertNull(data.get("THE"));

        data = RiTa.concordance("'What a wonderful world;!:,?.'\"", Map.of("ignorePunctuation", true));
        assertEquals(4, data.size());
        assertNull(data.get("!"));

        data = RiTa.concordance("The dog ate the cat", Map.of("ignoreStopWords", true));
        assertEquals(3, data.size());
        assertNull(data.get("The"));

        data = RiTa.concordance("It was a dream of you.", Map.of("ignoreStopWords", true));
        assertEquals(2, data.size());
        assertNull(data.get("It"));
        assertEquals(1, (int) data.get("dream"));
        assertEquals(1, (int) data.get("."));

        data = RiTa.concordance("Fresh fried fish, Fish fresh fried.", Map.of(
            "wordsToIgnore", List.of("fish"),
            "ignoreCase", true,
            "ignorePunctuation", true));
        assertEquals(2, data.size());
        assertNull(data.get("fish"));
        assertEquals(2, (int) data.get("fresh"));
        assertEquals(2, (int) data.get("fried"));

        // throw
        assertThrows(Exception.class, () -> RiTa.concordance());

        // count
        Concorder c = RiTa.concorder;
        c.concordance("dog dog dog cat cat cat cat cat");
        assertEquals(5, c.count("cat"));
        assertEquals(3, c.count("dog"));
        assertEquals(0, c.count("fox"));
    }

    @Test
    void shouldCallKwic() {
        List<String> result;
        RiTa.concordance("A sentence includes cat.");
        result = RiTa.kwic("cat");
        assertEquals("A sentence includes cat.", result.get(0));

        RiTa.concordance("Cats are beautiful.");
        result = RiTa.kwic("cat");
        assertEquals(0, result.size());

        RiTa.concordance("This is a very very long sentence includes cat with many many words after it and before it.");
        result = RiTa.kwic("cat");
        assertEquals("a very very long sentence includes cat with many many words after it", result.get(0));

        RiTa.concordance("A sentence includes cat in the middle. Another sentence includes cat in the middle.");
        result = RiTa.kwic("cat");
        assertEquals("A sentence includes cat in the middle. Another sentence", result.get(0));
        assertEquals("the middle. Another sentence includes cat in the middle.", result.get(1));

        RiTa.concordance("A sentence includes cat. Another sentence includes cat.");
        result = RiTa.kwic("cat");
        assertEquals("A sentence includes cat. Another sentence includes cat.", result.get(0));
        assertNull(result.size() > 1 ? result.get(1) : null);

        RiTa.concordance("A sentence includes cat. Another sentence includes cat.");
        result = RiTa.kwic("cat", 4);
        assertEquals("A sentence includes cat. Another sentence includes", result.get(0));
        assertEquals(". Another sentence includes cat.", result.get(1));

        RiTa.concordance("The dog ate the cat, what a tragedy! Little Kali loves the cat, it was her best friend.");
        result = RiTa.kwic("cat", 4);
        assertEquals("The dog ate the cat, what a tragedy", result.get(0));
        assertEquals("Little Kali loves the cat, it was her", result.get(1));

        RiTa.concordance("A sentence includes cat. Another sentence includes cat.");
        result = RiTa.kwic("cat", Map.of("numWords", 4));
        assertEquals("A sentence includes cat. Another sentence includes", result.get(0));
        assertEquals(". Another sentence includes cat.", result.get(1));

        RiTa.concordance("The dog ate the cat, what a tragedy! Little Kali loves the cat, it was her best friend.");
        result = RiTa.kwic("cat", Map.of("numWords", 4));
        assertEquals("The dog ate the cat, what a tragedy", result.get(0));
        assertEquals("Little Kali loves the cat, it was her", result.get(1));

        // use options.text or options.words to override kwic model
        result = RiTa.kwic("fish", Map.of("text", "The dog ate the cat that ate the fish."));
        assertEquals(1, result.size());
        assertEquals("ate the cat that ate the fish.", result.get(0));

        result = RiTa.kwic("fish", Map.of("words", RiTa.tokenize("The dog ate the cat that ate the fish.")));
        assertEquals(1, result.size());
        assertEquals("ate the cat that ate the fish.", result.get(0));

        result = RiTa.kwic("fish", Map.of("words", RiTa.tokenize("The dog ate the cat that ate the fish. He yelled at the dog and buy a new fish."), "numWords", 7));
        assertEquals(2, result.size());
        assertEquals("dog ate the cat that ate the fish. He yelled at the dog and", result.get(0));
        assertEquals("at the dog and buy a new fish.", result.get(1));

        result = RiTa.kwic("fish", Map.of("text", "The dog ate the cat that ate the fish. He yelled at the dog and buy a new fish.", "numWords", 7));
        assertEquals(2, result.size());
        assertEquals("dog ate the cat that ate the fish. He yelled at the dog and", result.get(0));
        assertEquals("at the dog and buy a new fish.", result.get(1));
    }

    @Test
    void shouldCallSentences() {
        String input, expected, output;

        assertArrayEquals(new String[] {""}, RiTa.sentences(""));

        input = "Stealth's Open Frame, OEM style LCD monitors are designed for special mounting applications. The slim profile packaging provides an excellent solution for building into kiosks, consoles, machines and control panels. If you cannot find an off the shelf solution call us today about designing a custom solution to fit your exact needs.";
        String[] expected1 = {"Stealth's Open Frame, OEM style LCD monitors are designed for special mounting applications.", "The slim profile packaging provides an excellent solution for building into kiosks, consoles, machines and control panels.", "If you cannot find an off the shelf solution call us today about designing a custom solution to fit your exact needs."};
        output = String.join("\n", RiTa.sentences(input));
        assertArrayEquals(expected1, RiTa.sentences(input));

        input = "\"The boy went fishing.\", he said. Then he went away.";
        expected = "\"The boy went fishing.\", he said.\nThen he went away.";
        output = String.join("\n", RiTa.sentences(input));
        assertArrayEquals(new String[] {"\"The boy went fishing.\", he said.", "Then he went away."}, RiTa.sentences(input));

        input = "The dog";
        output = String.join("\n", RiTa.sentences(input));
        assertArrayEquals(new String[] {input}, RiTa.sentences(input));

        input = "I guess the dog ate the baby.";
        output = String.join("\n", RiTa.sentences(input));
        assertArrayEquals(new String[] {input}, RiTa.sentences(input));

        input = "Oh my god, the dog ate the baby!";
        output = String.join("\n", RiTa.sentences(input));
        assertArrayEquals(new String[] {"Oh my god, the dog ate the baby!"}, RiTa.sentences(input));

        input = "Which dog ate the baby?";
        output = String.join("\n", RiTa.sentences(input));
        assertArrayEquals(new String[] {"Which dog ate the baby?"}, RiTa.sentences(input));

        input = "'Yes, it was a dog that ate the baby', he said.";
        output = String.join("\n", RiTa.sentences(input));
        assertArrayEquals(new String[] {"'Yes, it was a dog that ate the baby', he said."}, RiTa.sentences(input));

        input = "The baby belonged to Mr. and Mrs. Stevens. They will be very sad.";
        output = String.join("\n", RiTa.sentences(input));
        assertArrayEquals(new String[] {"The baby belonged to Mr. and Mrs. Stevens.", "They will be very sad."}, RiTa.sentences(input));

        // More quotation marks
        input = "\"The baby belonged to Mr. and Mrs. Stevens. They will be very sad.\"";
        output = String.join("\n", RiTa.sentences(input));
        assertArrayEquals(new String[] {"\"The baby belonged to Mr. and Mrs. Stevens.", "They will be very sad.\""}, RiTa.sentences(input));

        input = "\u201CThe baby belonged to Mr. and Mrs. Stevens. They will be very sad.\u201D";
        output = String.join("\n", RiTa.sentences(input));
        assertArrayEquals(new String[] {"\u201CThe baby belonged to Mr. and Mrs. Stevens.", "They will be very sad.\u201D"}, RiTa.sentences(input));

        // https://github.com/dhowe/RiTa/issues/498
        input = "\"My dear Mr. Bennet. Netherfield Park is let at last.\"";
        output = String.join("\n", RiTa.sentences(input));
        assertArrayEquals(new String[] {"\"My dear Mr. Bennet.", "Netherfield Park is let at last.\""}, RiTa.sentences(input));

        input = "\u201CMy dear Mr. Bennet. Netherfield Park is let at last.\u201D";
        output = String.join("\n", RiTa.sentences(input));
        assertArrayEquals(new String[] {"\u201CMy dear Mr. Bennet.", "Netherfield Park is let at last.\u201D"}, RiTa.sentences(input));

        input = "She wrote: \"I don't paint anymore. For a while I thought it was just a phase that I'd get over.\"";
        output = String.join("\n", RiTa.sentences(input));
        assertArrayEquals(new String[] {"She wrote: \"I don't paint anymore.", "For a while I thought it was just a phase that I'd get over.\""}, RiTa.sentences(input));

        input = " I had a visit from my \"friend\" the tax man.";
        output = String.join("\n", RiTa.sentences(input));
        assertArrayEquals(new String[] {"I had a visit from my \"friend\" the tax man."}, RiTa.sentences(input));
    }

    @Disabled("JS: 0 && it(...) — disabled block")
    @Test
    void shouldCallGetTransforms() {
        Set<String> transforms = RiTa.getTransforms();
        String[] expected = {"articlize", "capitalize", "uppercase", "quotify", "norepeat", "pluralize", "art", "cap", "uc", "qq", "nr", "s"};
        for (String t : expected) {
            assertTrue(transforms.contains(t), "fail at " + t);
        }
    }

    @Disabled("JS: false && it(...) — disabled block")
    @Test
    void shouldCallFindStem() {
        assertTrue(RiTa.findStem("dog"));
        assertTrue(RiTa.findStem("cat"));
        assertTrue(RiTa.findStem("play"));
        assertTrue(RiTa.findStem("run"));
        assertFalse(RiTa.findStem("dogs"));
        assertFalse(RiTa.findStem("played"));
        assertFalse(RiTa.findStem("writing"));
    }

    @Test
    void shouldNotMatchObjectPrototypeMembersInTheLexicon() {
        // Regression: prototype-chain leaks made hasWord() true for inherited props
        String[] words = {"toString", "constructor", "valueOf", "hasOwnProperty", "__proto__", "isPrototypeOf"};
        for (String w : words) {
            assertFalse(RiTa.hasWord(w), w + " should not be a word");
        }
        assertTrue(RiTa.hasWord("dog"), "dog should still be a word");
    }

    @Test
    void shouldHandleWordsMatchingObjectPrototypeMembersInConcordance() {
        // Regression: Concorder used a plain {} so keys like 'constructor' collided with inherited members
        Map<String, Integer> data = RiTa.concordance("constructor toString watch");
        assertEquals(Map.of("constructor", 1, "toString", 1, "watch", 1), data);
        assertEquals(1, RiTa.kwic("watch").size());
        assertEquals(1, RiTa.kwic("toString").size());
        assertEquals(0, RiTa.kwic("nonexistentword").size());
    }

    @Test
    void shouldCallIsVowelAndIsConsonantCaseInsensitively() {
        // Regression: uppercase letters were silently rejected
        assertTrue(RiTa.isVowel("A"));
        assertTrue(RiTa.isVowel("a"));
        assertTrue(RiTa.isConsonant("B"));
        assertTrue(RiTa.isConsonant("b"));
        assertFalse(RiTa.isVowel("B"));
        assertFalse(RiTa.isConsonant("A"));
        assertFalse(RiTa.isConsonant("1"));
        assertFalse(RiTa.isConsonant(""));
        assertFalse(RiTa.isVowel(""));
        // ok(!RiTa.isConsonant(undefined)); -- non-portable

        // must return strict booleans
        assertFalse(RiTa.isVowel(""));
        assertFalse(RiTa.isConsonant(""));
        // assertFalse(RiTa.isVowel(undefined));     -- non-portable
        // assertFalse(RiTa.isConsonant(undefined)); -- non-portable
    }

    @Test
    void shouldReturnStrictBooleansFromIsPunctAndIsAbbrev() {
        // Regression: isPunct('') returned '' and isAbbrev(1) returned undefined
        assertFalse(RiTa.isPunct(""));
        assertTrue(RiTa.isPunct(","));
        // assertFalse(RiTa.isAbbrev(123)); -- non-portable: number input to a String parameter
        assertFalse(RiTa.isAbbrev(null));
        assertTrue(RiTa.isAbbrev("Dr."));
    }

    @Test
    void shouldCacheAnalyzerResultsAndInvalidateOnLexiconSwap() {
        // Regression: RiTa.CACHING was never initialized, so the cache was dead
        assertTrue(RiTa.CACHING, "CACHING should default to true");

        Map<String, Object> orig = RiTa.lexicon.data;
        try {
            String before = RiTa.phones("cat");
            assertTrue(before.length() > 0);

            // swapping in a custom lexicon must invalidate stale cached phones
            Map<String, Object> custom = new LinkedHashMap<>();
            custom.put("cat", List.of("s-ae1-t", "nn"));
            RiTa.lexicon.data = custom;
            assertEquals("s-ae-t", RiTa.phones("cat"));

            // restoring the default dict must invalidate again
            RiTa.lexicon.data = orig;
            assertEquals(before, RiTa.phones("cat"));
        } finally {
            RiTa.lexicon.data = orig;
        }
    }

    @Test
    void shouldUseO1SetMirrorsConsistentWithTheWordLists() {
        // Regression: membership was tested via Array.includes (O(n)); the Set mirrors must agree
        check(RiTa.STOP_WORDS, RiTa.STOP_WORDS_SET);
        check(RiTa.MASS_NOUNS, RiTa.MASS_NOUNS_SET);
        check(RiTa.QUESTIONS, RiTa.QUESTIONS_SET);

        // and must not contain non-members
        assertFalse(RiTa.STOP_WORDS_SET.contains("notarealstopword"));
        assertFalse(RiTa.MASS_NOUNS_SET.contains("notarealmassnoun"));
    }

    @Test
    void shouldHonorReassignmentOfTheWordLists() {
        // Regression: the Set mirrors must rebuild when a list is reassigned
        List<String> orig = RiTa.STOP_WORDS;
        try {
            RiTa.STOP_WORDS = new ArrayList<>(List.of("zebraterm"));
            assertTrue(RiTa.isStopWord("zebraterm"));
            assertFalse(RiTa.isStopWord("the"));
        } finally {
            RiTa.STOP_WORDS = orig;
        }
        assertTrue(RiTa.isStopWord("the"));
    }

    @Test
    void shouldHonorInPlaceMutationOfTheWordLists() {
        // Regression: the mirror length-check must detect push/pop on the same array object
        List<String> list = RiTa.STOP_WORDS;
        int len = list.size();
        try {
            list.add("quokkaterm");
            assertTrue(RiTa.isStopWord("quokkaterm"));
            assertEquals(new HashSet<>(list).size(), RiTa.STOP_WORDS_SET.size());
            list.remove(list.size() - 1);
            assertFalse(RiTa.isStopWord("quokkaterm"));
        } finally {
            if (list.size() > len) {
                list.subList(len, list.size()).clear();
            }
        }
        assertFalse(RiTa.STOP_WORDS_SET.contains("quokkaterm"));
    }

    // ---- helpers --------------------------------------------------------------------

    private static void check(List<String> arr, Set<String> set) {
        for (String w : arr) {
            assertTrue(set.contains(w), "missing " + w);
        }
    }

    private static Set<Integer> setOf(int[] a) {
        Set<Integer> s = new HashSet<>();
        for (int v : a) {
            s.add(v);
        }
        return s;
    }
}
