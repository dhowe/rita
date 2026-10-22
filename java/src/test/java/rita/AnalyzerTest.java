package rita;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/**
 * Ported from <code>js/test/analyzer-tests.js</code>.
 *
 * <p>Mapping notes:
 * <ul>
 *   <li>{@code expect(x).eq(y)} -> {@code assertEquals}; {@code .eql([...])} -> {@code assertEquals}
 *       on lists; {@code .eql(true)}/{@code .is.true} -> {@code assertTrue}; {@code .eq(undefined)}
 *       -> {@code assertNull}.</li>
 *   <li>JS option objects -> {@code Map.of(...)} (or {@code HashMap} when a null value is needed).</li>
 *   <li>The JS {@code hasLex} flag is {@code true}; both branches of the ternaries are kept verbatim
 *       so the suite reads identically.</li>
 *   <li>JS blocks disabled with {@code 0 && expect(...)} are omitted, matching the JS behaviour.</li>
 *   <li>JS {@code expect(() => RiTa.singularize([1])).to.throw()} tests runtime type coercion of a
 *       non-string argument. Java is statically typed, so the equivalent call does not compile;
 *       those two assertions (and the pluralize equivalents) are documented here and omitted.</li>
 * </ul>
 */
class AnalyzerTest {

    // mirrors `let hasLex = true` in the JS suite
    private static final boolean HAS_LEX = true;

    /**
     * Reset the mutable global flag before each test. Tests that flip {@code SILENCE_LTS} restore it
     * in a trailing statement, but while the implementation is still a stub the call in between throws
     * before the restore runs — so the flag would leak into the next test. This keeps each test
     * independent without altering any assertion.
     */
    @BeforeEach
    void resetGlobals() {
        RiTa.SILENCE_LTS = false;
    }

    @Test
    void shouldCallAnalyzerAnalyze() {
        RiTa.Analysis data = RiTa.analyzer.analyze("abandon");
        assertEquals("ah-b-ae-n-d-ah-n", data.phones);
        assertEquals("0/1/0", data.stresses);
        assertEquals("ah/b-ae-n/d-ah-n", data.syllables);
    }

    @Test
    void shouldCallAnalyzeWord() {
        boolean tmp = RiTa.SILENCE_LTS;
        RiTa.SILENCE_LTS = true;

        RiTa.Analysis data = RiTa.analyzer.analyzeWord("abandon");
        assertEquals("ah-b-ae-n-d-ah-n", data.phones);
        assertEquals("0/1/0", data.stresses);
        assertEquals("ah/b-ae-n/d-ah-n", data.syllables);

        data = RiTa.analyzer.analyzeWord("z");
        assertEquals("z", data.phones);
        assertEquals("0", data.stresses);
        assertEquals("z", data.syllables);

        data = RiTa.analyzer.analyzeWord("cloze");
        assertEquals("k-l-ow-z", data.phones);
        assertEquals("1", data.stresses);
        assertEquals("k-l-ow-z", data.syllables);

        RiTa.SILENCE_LTS = tmp;
    }

    @Test
    void shouldCallAnalyzeWordWithLts() {
        boolean tmp = RiTa.SILENCE_LTS;
        RiTa.SILENCE_LTS = true;

        RiTa.Analysis data = RiTa.analyzer.analyzeWord("1903");
        assertEquals("w-ah-n-n-ih-n-z-ih-r-ow-th-r-iy", data.phones);
        assertEquals("0/0/0/0/0", data.stresses);
        assertEquals("w-ah-n/n-ih-n/z-ih/r-ow/th-r-iy", data.syllables);

        RiTa.SILENCE_LTS = tmp;
    }

    @Test
    void shouldCallAnalyzeLts() {
        assertEquals(false, RiTa.SILENCE_LTS);
        RiTa.Analysis feats = RiTa.analyze("cloze", Map.of("silent", 1));
        assertEquals("nn", feats.pos);
        assertEquals("cloze", feats.tokens);
        assertEquals("k-l-ow-z", feats.syllables);
    }

    @Test
    void shouldCallSyllablesLts() {
        String result = RiTa.syllables("The Laggin", Map.of("silent", 1));
        assertEquals("dh-ah l-ae/g-ih-n", result, "got '" + result + "'");
    }

    @Test
    void shouldCallAnalyze() {
        // JS: expect(RiTa.analyze('')).eql({ tokens:'', pos:'', stresses:'', phones:'', syllables:'' })
        assertEquals(Map.of("tokens", "", "pos", "", "stresses", "", "phones", "", "syllables", ""),
            RiTa.analyze("").toMap());

        RiTa.Analysis feats;

        feats = RiTa.analyze("clothes");
        assertEquals("nns", feats.pos);
        assertEquals("clothes", feats.tokens);
        assertEquals("k-l-ow-dh-z", feats.syllables);

        feats = RiTa.analyze("chevrolet");
        assertEquals("chevrolet", feats.tokens);
        assertEquals(HAS_LEX ? "sh-eh-v/r-ow/l-ey" : "ch-eh-v/r-ow/l-ah-t", feats.syllables);

        if (!HAS_LEX) {
            return; // NOTE: below currently fail without lexicon
        }

        boolean tmp = RiTa.SILENCE_LTS;
        RiTa.SILENCE_LTS = true;
        feats = RiTa.analyze("1903");
        assertEquals("w-ah-n-n-ih-n-z-ih-r-ow-th-r-iy", feats.phones);
        assertEquals("0/0/0/0/0", feats.stresses);
        assertEquals("w-ah-n/n-ih-n/z-ih/r-ow/th-r-iy", feats.syllables);
        assertEquals("1903", feats.tokens);
        assertEquals("cd", feats.pos);
        RiTa.SILENCE_LTS = tmp;

        feats = RiTa.analyze("the clothes");
        assertEquals("dt nns", feats.pos);
        assertEquals("the clothes", feats.tokens);
        assertEquals("dh-ah k-l-ow-dh-z", feats.syllables);

        feats = RiTa.analyze("yoyo");
        assertEquals("nn", feats.pos);
        assertEquals("yoyo", feats.tokens);
        assertEquals("y-ow/y-ow", feats.syllables);

        feats = RiTa.analyze("abandon");
        assertEquals("vb", feats.pos);
        assertEquals("ah-b-ae-n-d-ah-n", feats.phones);
        assertEquals("abandon", feats.tokens);
        assertEquals("0/1/0", feats.stresses);
        assertEquals("ah/b-ae-n/d-ah-n", feats.syllables);

        // https://github.com/dhowe/rita/issues/177
        feats = RiTa.analyze("bit");
        assertEquals("vbd", feats.pos);
        assertEquals("b-ih-t", feats.syllables);

        // 'bit': as a vbd
        feats = RiTa.analyze("It bit me.");
        assertEquals("prp vbd prp .", feats.pos);
        // 'bit': as an nn
        feats = RiTa.analyze("Give the duck a bit of bread.");
        assertEquals("vb dt nn dt nn in nn .", feats.pos);

        feats = RiTa.analyze("broke");
        assertEquals("vbd", feats.pos);
        assertEquals("b-r-ow-k", feats.syllables);
        feats = RiTa.analyze("I broke my leg.");
        assertEquals("prp vbd prp$ nn .", feats.pos);

        feats = RiTa.analyze("The show has ended.");
        assertEquals("dt nn vbz vbn .", feats.pos);

        feats = RiTa.analyze("She oversaw it.");
        assertEquals("prp vbd prp .", feats.pos);

        // remade as a vbd
        feats = RiTa.analyze("She remade this video.");
        assertEquals("prp vbd dt nn .", feats.pos);
        // remade as a vbn -- disabled in JS via `0 &&`
        RiTa.analyze("They will be remade into something else.");

        // become
        feats = RiTa.analyze("She becomes a companion to a foreigner.");
        assertEquals("prp vbz dt nn to dt nn .", feats.pos);
        // disabled in JS via `0 &&`
        RiTa.analyze("She has become a companion to a foreigner.");
    }

    @Test
    void shouldTreatHyphenatedWordsAsSingleTokens() {
        boolean lts = RiTa.SILENCE_LTS;
        RiTa.SILENCE_LTS = true; // disable LTS logging

        // pool1: all parts in dict
        String[] pool1 = {"mother-in-law", "father-in-law", "sister-in-law", "brother-in-law", "off-site", "up-to-date", "state-of-the-art", "self-esteem", "merry-go-round", "man-eating", "twenty-one", "twenty-first", "thirty-second", "happy-go-lucky", "editor-in-chief", "over-the-counter", "long-term", "high-speed", "in-depth", "full-length", "part-time", "sun-dried", "well-off", "well-known", "gift-wrap", "follow-up", "well-being", "good-looking", "knee-length", "runner-up", "tip-off", "blush-on", "sugar-free", "ice-cold", "far-flung", "high-rise", "life-size", "king-size", "next-door", "full-time", "forty-acre", "on-campus", "family-run", "low-grade", "round-trip"};
        String[][] feats1 = {
            {"nn", "mother-in-law", "m-ah-dh-er-ih-n-l-ao", "1/0-0-1", "m-ah/dh-er/ih-n/l-ao"},
            {"nn", "father-in-law", "f-aa-dh-er-ih-n-l-ao", "1/0-0-1", "f-aa/dh-er/ih-n/l-ao"},
            {"nn", "sister-in-law", "s-ih-s-t-er-ih-n-l-ao", "1/0-0-1", "s-ih/s-t-er/ih-n/l-ao"},
            {"nn", "brother-in-law", "b-r-ah-dh-er-ih-n-l-ao", "1/0-0-1", "b-r-ah/dh-er/ih-n/l-ao"},
            {"jj", "off-site", "ao-f-s-ay-t", "1-1", "ao-f/s-ay-t"},
            {"jj", "up-to-date", "ah-p-t-uw-d-ey-t", "1-1-1", "ah-p/t-uw/d-ey-t"},
            {"nn", "state-of-the-art", "s-t-ey-t-ah-v-dh-ah-aa-r-t", "1-1-0-1", "s-t-ey-t/ah-v/dh-ah/aa-r-t"},
            {"nn", "self-esteem", "s-eh-l-f-ah-s-t-iy-m", "1-0/1", "s-eh-l-f/ah/s-t-iy-m"},
            {"nn", "merry-go-round", "m-eh-r-iy-g-ow-r-aw-n-d", "1/0-1-1", "m-eh/r-iy/g-ow/r-aw-n-d"},
            {"jj", "man-eating", "m-ae-n-iy-t-ih-ng", "1-1/0", "m-ae-n/iy/t-ih-ng"},
            {"cd", "twenty-one", "t-w-eh-n-t-iy-w-ah-n", "1/0-1", "t-w-eh-n/t-iy/w-ah-n"},
            {"jj", "twenty-first", "t-w-eh-n-t-iy-f-er-s-t", "1/0-1", "t-w-eh-n/t-iy/f-er-s-t"},
            {"jj", "thirty-second", "th-er-t-iy-s-eh-k-ah-n-d", "1/0-1/0", "th-er/t-iy/s-eh/k-ah-n-d"},
            {"jj", "happy-go-lucky", "hh-ae-p-iy-g-ow-l-ah-k-iy", "1/0-1-1/0", "hh-ae/p-iy/g-ow/l-ah/k-iy"},
            {"nn", "editor-in-chief", "eh-d-ah-t-er-ih-n-ch-iy-f", "1/0/0-0-1", "eh/d-ah/t-er/ih-n/ch-iy-f"},
            {"jj", "over-the-counter", "ow-v-er-dh-ah-k-aw-n-t-er", "1/0-0-1/0", "ow/v-er/dh-ah/k-aw-n/t-er"},
            {"jj", "long-term", "l-ao-ng-t-er-m", "1-1", "l-ao-ng/t-er-m"},
            {"jj", "high-speed", "hh-ay-s-p-iy-d", "1-1", "hh-ay/s-p-iy-d"},
            {"jj", "in-depth", "ih-n-d-eh-p-th", "0-1", "ih-n/d-eh-p-th"},
            {"jj", "full-length", "f-uh-l-l-eh-ng-k-th", "1-1", "f-uh-l/l-eh-ng-k-th"},
            {"jj", "part-time", "p-aa-r-t-t-ay-m", "1-1", "p-aa-r-t/t-ay-m"},
            {"jj", "sun-dried", "s-ah-n-d-r-ay-d", "1-1", "s-ah-n/d-r-ay-d"},
            {"jj", "well-off", "w-eh-l-ao-f", "1-1", "w-eh-l/ao-f"},
            {"jj", "well-known", "w-eh-l-n-ow-n", "1-1", "w-eh-l/n-ow-n"},
            {"nn", "gift-wrap", "g-ih-f-t-r-ae-p", "1-1", "g-ih-f-t/r-ae-p"},
            {"nn", "follow-up", "f-aa-l-ow-ah-p", "1/0-1", "f-aa/l-ow/ah-p"},
            {"nn", "well-being", "w-eh-l-b-iy-ih-ng", "1-1/0", "w-eh-l/b-iy/ih-ng"},
            {"jj", "good-looking", "g-uh-d-l-uh-k-ih-ng", "1-1/0", "g-uh-d/l-uh/k-ih-ng"},
            {"jj", "knee-length", "n-iy-l-eh-ng-k-th", "1-1", "n-iy/l-eh-ng-k-th"},
            {"nn", "runner-up", "r-ah-n-er-ah-p", "1/0-1", "r-ah/n-er/ah-p"},
            {"nn", "tip-off", "t-ih-p-ao-f", "1-1", "t-ih-p/ao-f"},
            {"nn", "blush-on", "b-l-ah-sh-aa-n", "1-1", "b-l-ah-sh/aa-n"},
            {"jj", "sugar-free", "sh-uh-g-er-f-r-iy", "1/0-1", "sh-uh/g-er/f-r-iy"},
            {"jj", "ice-cold", "ay-s-k-ow-l-d", "1-1", "ay-s/k-ow-l-d"},
            {"jj", "far-flung", "f-aa-r-f-l-ah-ng", "1-1", "f-aa-r/f-l-ah-ng"},
            {"nn", "high-rise", "hh-ay-r-ay-z", "1-1", "hh-ay/r-ay-z"},
            {"jj", "life-size", "l-ay-f-s-ay-z", "1-1", "l-ay-f/s-ay-z"},
            {"jj", "king-size", "k-ih-ng-s-ay-z", "1-1", "k-ih-ng/s-ay-z"},
            {"jj", "next-door", "n-eh-k-s-t-d-ao-r", "1-1", "n-eh-k-s-t/d-ao-r"},
            {"jj", "full-time", "f-uh-l-t-ay-m", "1-1", "f-uh-l/t-ay-m"},
            {"jj", "forty-acre", "f-ao-r-t-iy-ey-k-er", "1/0-1/0", "f-ao-r/t-iy/ey/k-er"},
            {"jj", "on-campus", "aa-n-k-ae-m-p-ah-s", "1-1/0", "aa-n/k-ae-m/p-ah-s"},
            {"jj", "family-run", "f-ae-m-ah-l-iy-r-ah-n", "1/0/0-1", "f-ae/m-ah/l-iy/r-ah-n"},
            {"jj", "low-grade", "l-ow-g-r-ey-d", "1-1", "l-ow/g-r-ey-d"},
            {"jj", "round-trip", "r-aw-n-d-t-r-ih-p", "1-1", "r-aw-n-d/t-r-ih-p"}
        };
        for (int i = 0; i < pool1.length; i++) {
            RiTa.Analysis feats = RiTa.analyze(pool1[i]);
            assertEquals(feats1[i][0], feats.pos, "[pos]fail at " + pool1[i]);
            assertEquals(feats1[i][1], feats.tokens, "[tokens]fail at " + pool1[i]);
            assertEquals(feats1[i][2], feats.phones, "[phones]fail at " + pool1[i]);
            assertEquals(feats1[i][3], feats.stresses, "[stresses]fail at " + pool1[i]);
            assertEquals(feats1[i][4], feats.syllables, "[syllables]fail at " + pool1[i]);
            assertEquals(List.of(feats.tokens.split(" ")), List.of(RiTa.tokenize(pool1[i])));
        }

        // pool2A: the missing part is a transformation of a word in dict
        String[] pool2A = {"oft-cited", "deeply-nested", "empty-handed", "sergeant-at-arms", "left-handed", "long-haired", "breath-taking", "self-centered", "single-minded", "short-tempered", "one-sided", "warm-blooded", "cold-blooded", "bell-bottoms", "corn-fed", "able-bodied"};
        String[][] feats2A = {
            {"jj", "oft-cited", "ao-f-t-s-ih-t-ah-d", "1-1/0", "ao-f-t/s-ih/t-ah-d"},
            {"jj", "deeply-nested", "d-iy-p-l-iy-n-eh-s-t-ah-d", "1/0-1/0", "d-iy-p/l-iy/n-eh/s-t-ah-d"},
            {"jj", "empty-handed", "eh-m-p-t-iy-hh-ae-n-d-ah-d", "1/0-1/0", "eh-m-p/t-iy/hh-ae-n/d-ah-d"},
            {"nn", "sergeant-at-arms", "s-aa-r-jh-ah-n-t-ae-t-aa-r-m-z", "1/0-1-1", "s-aa-r/jh-ah-n-t/ae-t/aa-r-m-z"},
            {"jj", "left-handed", "l-eh-f-t-hh-ae-n-d-ah-d", "1-1/0", "l-eh-f-t/hh-ae-n/d-ah-d"},
            {"jj", "long-haired", "l-ao-ng-hh-eh-r-d", "1-1", "l-ao-ng/hh-eh-r-d"},
            {"jj", "breath-taking", "b-r-eh-th-t-ey-k-ih-ng", "1-1/0", "b-r-eh-th/t-ey/k-ih-ng"},
            {"jj", "self-centered", "s-eh-l-f-s-eh-n-t-er-d", "1-1/0", "s-eh-l-f/s-eh-n/t-er-d"},
            {"jj", "single-minded", "s-ih-ng-g-ah-l-m-ay-n-d-ah-d", "1/0-1/0", "s-ih-ng/g-ah-l/m-ay-n/d-ah-d"},
            {"jj", "short-tempered", "sh-ao-r-t-t-eh-m-p-er-d", "1-1/0", "sh-ao-r-t/t-eh-m/p-er-d"},
            {"jj", "one-sided", "w-ah-n-s-ay-d-ah-d", "1-1/0", "w-ah-n/s-ay/d-ah-d"},
            {"jj", "warm-blooded", "w-ao-r-m-b-l-ah-d-ah-d", "1-1/0", "w-ao-r-m/b-l-ah/d-ah-d"},
            {"jj", "cold-blooded", "k-ow-l-d-b-l-ah-d-ah-d", "1-1/0", "k-ow-l-d/b-l-ah/d-ah-d"},
            {"nn", "bell-bottoms", "b-eh-l-b-aa-t-ah-m-z", "1-1/0", "b-eh-l/b-aa/t-ah-m-z"},
            {"jj", "corn-fed", "k-ao-r-n-f-eh-d", "1-1", "k-ao-r-n/f-eh-d"},
            {"jj", "able-bodied", "ey-b-ah-l-b-aa-d-iy-d", "1/0-1/0", "ey/b-ah-l/b-aa/d-iy-d"}
        };
        for (int i = 0; i < pool2A.length; i++) {
            RiTa.Analysis feats = RiTa.analyze(pool2A[i]);
            assertEquals(feats2A[i][0], feats.pos, "[pos]fail at " + pool2A[i]);
            assertEquals(feats2A[i][1], feats.tokens, "[tokens]fail at " + pool2A[i]);
            assertEquals(feats2A[i][2], feats.phones, "[phones]fail at " + pool2A[i]);
            assertEquals(feats2A[i][3], feats.stresses, "[stresses]fail at " + pool2A[i]);
            assertEquals(feats2A[i][4], feats.syllables, "[syllables]fail at " + pool2A[i]);
            assertEquals(List.of(feats.tokens.split(" ")), List.of(RiTa.tokenize(pool2A[i])));
        }

        // pool2B: the missing part has no connection to any word in dict
        String[] pool2B = {"de-emphasize", "re-apply", "ho-hum", "co-manage", "co-manager", "neo-liberalism", "u-turn", "x-ray", "a-frame", "high-tech", "nitty-gritty"};
        String[][] feats2B = {
            {"vb", "de-emphasize", "d-ih-eh-m-f-ah-s-ay-z", "0-1/0/0", "d-ih/eh-m/f-ah/s-ay-z"},
            {"vb", "re-apply", "r-iy-ah-p-l-ay1", "0-0/1", "r-iy/ah/p-l-ay1"},
            {"uh", "ho-hum", "hh-ow-hh-ah-m", "0-1", "hh-ow/hh-ah-m"},
            {"vb", "co-manage", "k-ow-m-ae-n-ah-jh", "0-1/0", "k-ow/m-ae/n-ah-jh"},
            {"nn", "co-manager", "k-ow-m-ae-n-ah-jh-er", "0-1/0/0", "k-ow/m-ae/n-ah/jh-er"},
            {"nn", "neo-liberalism", "n-iy-ow-l-ih-b-er-ah-l-ih-z-ah-m", "0/0-1/0/0/0/0", "n-iy/ow/l-ih/b-er/ah/l-ih/z-ah-m"},
            {"nn", "u-turn", "y-uw-t-er-n", "1-1", "y-uw/t-er-n"},
            {"nn", "x-ray", "eh-k-z-r-ey", "1-1", "eh-k-z/r-ey"},
            {"nn", "a-frame", "ey-f-r-ey-m", "1-1", "ey/f-r-ey-m"},
            {"jj", "high-tech", "hh-ay-t-eh-k", "1-1", "hh-ay/t-eh-k"},
            {"nn", "nitty-gritty", "n-ih-t-iy-g-r-ih-t-iy", "1/0-1/0", "n-ih/t-iy/g-r-ih/t-iy"}
        };
        for (int i = 0; i < pool2B.length; i++) {
            RiTa.Analysis feats = RiTa.analyze(pool2B[i]);
            assertEquals(feats2B[i][0], feats.pos, "[pos]fail at " + pool2B[i]);
            // LTS related error, see https://github.com/dhowe/rita/issues/185
            if (List.of("de-emphasize", "re-apply", "u-turn", "x-ray").contains(pool2B[i])) {
                continue;
            }
            assertEquals(feats2B[i][1], feats.tokens, "[tokens]fail at " + pool2B[i]);
            assertEquals(feats2B[i][2], feats.phones, "[phones]fail at " + pool2B[i]);
            assertEquals(feats2B[i][3], feats.stresses, "[stresses]fail at " + pool2B[i]);
            assertEquals(feats2B[i][4], feats.syllables, "[syllables]fail at " + pool2B[i]);
            assertEquals(List.of(feats.tokens.split(" ")), List.of(RiTa.tokenize(pool2B[i])));
        }

        // pool3: all parts are not in dict
        String[] pool3 = {"co-op", "roly-poly", "topsy-turvy"};
        String[][] feats3 = {
            {"nn", "co-op", "k-ow-ah-p", "0-0", "k-ow/ah-p"},
            {"jj", "roly-poly", "r-ow-l-iy-p-aa-l-iy", "1/0-1/0", "r-ow/l-iy/p-aa/l-iy"},
            {"jj", "topsy-turvy", "t-aa-p-s-iy-t-er-v-iy", "1/0-1/0", "t-aa-p/s-iy/t-er/v-iy"}
        };
        for (int i = 0; i < pool3.length; i++) {
            RiTa.Analysis feats = RiTa.analyze(pool3[i]);
            assertEquals(feats3[i][0], feats.pos, "[pos]fail at " + pool3[i]);
            assertEquals(feats3[i][1], feats.tokens, "[tokens]fail at " + pool3[i]);
            assertEquals(feats3[i][2], feats.phones, "[phones]fail at " + pool3[i]);
            assertEquals(feats3[i][3], feats.stresses, "[stresses]fail at " + pool3[i]);
            assertEquals(feats3[i][4], feats.syllables, "[syllables]fail at " + pool3[i]);
            assertEquals(List.of(feats.tokens.split(" ")), List.of(RiTa.tokenize(pool3[i])));
        }
        RiTa.SILENCE_LTS = lts; // reset
    }

    @Test
    void shouldHandleDashes() {
        // https://github.com/dhowe/rita/issues/176
        boolean lts = RiTa.SILENCE_LTS;
        RiTa.SILENCE_LTS = true; // disable LTS logging

        // U+2012
        String sentence = "Teaching‒the profession has always appealed to me.";
        RiTa.Analysis feats = RiTa.analyze(sentence);
        assertEquals("vbg ‒ dt nn vbz rb vbd to prp .", feats.pos);
        assertEquals("Teaching ‒ the profession has always appealed to me .", feats.tokens);
        assertEquals(List.of(feats.tokens.split(" ")), List.of(RiTa.tokenize(sentence)));

        // U+2013
        sentence = "The teacher assigned pages 101–181 for tonight's reading material. ";
        feats = RiTa.analyze(sentence);
        assertEquals("dt nn vbn nns cd – cd in nns vbg jj .", feats.pos);
        assertEquals("The teacher assigned pages 101 – 181 for tonight's reading material .", feats.tokens);
        assertEquals(List.of(feats.tokens.split(" ")), List.of(RiTa.tokenize(sentence)));

        // U+2014
        sentence = "Type two hyphens—without a space before, after, or between them.";
        feats = RiTa.analyze(sentence);
        assertEquals("nn cd nns — in dt nn in , in , cc in prp .", feats.pos);
        assertEquals("Type two hyphens — without a space before , after , or between them .", feats.tokens);
        assertEquals(List.of(feats.tokens.split(" ")), List.of(RiTa.tokenize(sentence)));

        // U+2014
        sentence = "Phones, hand-held computers, and built-in TVs—each a possible distraction—can lead to a dangerous situation if used while driving.";
        feats = RiTa.analyze(sentence);
        assertEquals("nns , jj nns , cc jj nnps — dt dt jj nn — md vb to dt jj nn in vbn in vbg .", feats.pos);
        assertEquals("Phones , hand-held computers , and built-in TVs — each a possible distraction — can lead to a dangerous situation if used while driving .", feats.tokens);
        assertEquals(List.of(feats.tokens.split(" ")), List.of(RiTa.tokenize(sentence)));

        // "--"
        sentence = "He is afraid of two things--spiders and senior prom.";
        feats = RiTa.analyze(sentence);
        assertEquals("prp vbz jj in cd nns -- nns cc jj nn .", feats.pos);
        assertEquals("He is afraid of two things -- spiders and senior prom .", feats.tokens);
        assertEquals(List.of(feats.tokens.split(" ")), List.of(RiTa.tokenize(sentence)));

        RiTa.SILENCE_LTS = lts;
    }

    @Test
    void shouldCallStresses() {
        String result;
        String answer;
        String word;

        assertEquals("", RiTa.stresses(""));
        assertEquals("1/0", RiTa.stresses("women"), "women");

        if (!HAS_LEX) {
            return; // NOTE: below may fail without lexicon
        }

        assertEquals("0 1/0/0 1 1 1 1", RiTa.stresses("The emperor had no clothes on"));
        assertEquals("0 1/0/0 1 1 1 1 .", RiTa.stresses("The emperor had no clothes on."));
        assertEquals("0 1/0/0 1 1 1 1 . 0 1 1 1 .", RiTa.stresses("The emperor had no clothes on. The King is fat."));

        word = "to present, to export, to decide, to begin";
        result = RiTa.stresses(word);
        answer = HAS_LEX ? "1 1/0 , 1 1/0 , 1 0/1 , 1 0/1" : "1 1/1 , 1 0/1 , 1 0/1 , 1 1/1";
        assertEquals(answer, result, word);

        word = "The dog ran faster than the other dog.  But the other dog was prettier.";
        result = RiTa.stresses(word);
        answer = "0 1 1 1/0 1 0 1/0 1 . 1 0 1/0 1 1 1/0/0 .";
        assertEquals(answer, result, word);

        // different without lexicon ------------------------------------------

        assertEquals(HAS_LEX ? "0/0/1" : "1/0/0", RiTa.stresses("chevrolet"), "chevrolet");
        assertEquals(HAS_LEX ? "1/0/0" : "1/0/1", RiTa.stresses("genuine"), "genuine");

        word = "to preSENT, to exPORT, to deCIDE, to beGIN";
        result = RiTa.stresses(word);
        answer = HAS_LEX ? "1 1/0 , 1 1/0 , 1 0/1 , 1 0/1" : "1 1/1 , 1 0/1 , 1 0/1 , 1 1/1";
        assertEquals(answer, result, word);
    }

    @Test
    void shouldCallPhones() {
        boolean silent = RiTa.SILENCE_LTS;
        RiTa.SILENCE_LTS = true;

        String result;
        String answer;

        assertEquals("", RiTa.phones(""));
        assertEquals("b", RiTa.phones("b"));
        assertEquals("b", RiTa.phones("B"));
        assertEquals("dh-ah", RiTa.phones("The"));
        assertEquals("dh-ah .", RiTa.phones("The."));
        assertEquals("f-l-aw-er-z", RiTa.phones("flowers"));
        assertEquals("m-ay-s", RiTa.phones("mice"));
        assertEquals("ae-n-t", RiTa.phones("ant"));

        // different without lexicon ------------------------------------------

        result = RiTa.phones("The boy jumped over the wild dog.");
        answer = HAS_LEX ? "dh-ah b-oy jh-ah-m-p-t ow-v-er dh-ah w-ay-l-d d-ao-g ." : "dh-ah b-oy jh-ah-m-p-t ow-v-er dh-ah w-ay-l-d d-aa-g .";
        assertEquals(answer, result);

        result = RiTa.phones("The boy ran to the store.");
        answer = HAS_LEX ? "dh-ah b-oy r-ae-n t-uw dh-ah s-t-ao-r ." : "dh-ah b-oy r-ah-n t-ow dh-ah s-t-ao-r .";
        assertEquals(answer, result);

        result = RiTa.phones("The dog ran faster than the other dog.  But the other dog was prettier.");
        answer = HAS_LEX
            ? "dh-ah d-ao-g r-ae-n f-ae-s-t-er dh-ae-n dh-ah ah-dh-er d-ao-g . b-ah-t dh-ah ah-dh-er d-ao-g w-aa-z p-r-ih-t-iy-er ."
            : "dh-ah d-aa-g r-ah-n f-ae-s-t-er th-ae-n dh-ah ah-dh-er d-aa-g . b-ah-t dh-ah ah-dh-er d-aa-g w-ah-z p-r-eh-t-iy-er .";
        assertEquals(answer, result);

        assertEquals(HAS_LEX ? "k-iy-sh" : "k-w-ih-sh", RiTa.phones("quiche"));
        assertEquals(HAS_LEX ? "s-eh-d" : "s-ey-d", RiTa.phones("said"));
        assertEquals(HAS_LEX ? "sh-eh-v-r-ow-l-ey" : "ch-eh-v-r-ow-l-ah-t", RiTa.phones("chevrolet"));
        assertEquals(HAS_LEX ? "w-ih-m-eh-n" : "w-ow-m-eh-n", RiTa.phones("women"));
        assertEquals(HAS_LEX ? "jh-eh-n-y-uw-w-ah-n" : "jh-eh-n-y-ah-ay-n", RiTa.phones("genuine"));

        if (!HAS_LEX) {
            return; // NOTE: below may fail without lexicon
        }

        assertEquals("d-ih-f-ao-r-ih-s-t-ey-sh-ah-n-z", RiTa.phones("deforestations"));
        assertEquals("s-k-ih-t-s-ah-f-r-iy-n-iy-ah-z", RiTa.phones("schizophrenias"));

        RiTa.SILENCE_LTS = silent;
    }

    @Test
    void shouldCallSyllables() {
        boolean silent = RiTa.SILENCE_LTS;
        RiTa.SILENCE_LTS = true;
        assertEquals("", RiTa.syllables(""));
        assertEquals("k-l-ow-dh-z", RiTa.syllables("clothes"));

        // different without lexicon ------------------------------------------

        assertEquals(HAS_LEX ? "w-ah-n/n-ih-n/z-ih/r-ow/th-r-iy" : "1903", RiTa.syllables("1903"));

        String[] nums = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};
        for (int i = 0; i < 10; i++) {
            String istr = i + "";
            assertEquals(HAS_LEX ? RiTa.syllables(nums[i]) : istr, RiTa.syllables(istr));
        }

        assertEquals(HAS_LEX ? "d-ih/f-ao/r-ih/s-t-ey/sh-ah-n-z" : "d-ah/f-ao-r/s-t-ey/sh-ah-n-z", RiTa.syllables("deforestations"));
        assertEquals(HAS_LEX ? "sh-eh-v/r-ow/l-ey" : "ch-eh-v/r-ow/l-ah-t", RiTa.syllables("chevrolet"));
        assertEquals(HAS_LEX ? "w-ih/m-eh-n" : "w-ow/m-eh-n", RiTa.syllables("women"));
        assertEquals(HAS_LEX ? "jh-eh-n/y-uw/w-ah-n" : "jh-eh-n/y-ah/ay-n", RiTa.syllables("genuine"));

        String input;
        String expected;

        input = "The emperor had no clothes on.";
        expected = HAS_LEX ? "dh-ah eh-m/p-er/er hh-ae-d n-ow k-l-ow-dh-z aa-n ." : "dh-ah eh-m/p-er/er hh-ae-d n-ow k-l-ow-dh-z ah-n .";
        assertEquals(expected, RiTa.syllables(input));

        input = "The dog ran faster than the other dog. But the other dog was prettier.";
        expected = HAS_LEX ? "dh-ah d-ao-g r-ae-n f-ae/s-t-er dh-ae-n dh-ah ah/dh-er d-ao-g . b-ah-t dh-ah ah/dh-er d-ao-g w-aa-z p-r-ih/t-iy/er ." : "dh-ah d-aa-g r-ah-n f-ae/s-t-er th-ae-n dh-ah ah/dh-er d-aa-g . b-ah-t dh-ah ah/dh-er d-aa-g w-ah-z p-r-eh/t-iy/er .";
        assertEquals(expected, RiTa.syllables(input));

        input = "The dog ran faster than the other dog. But the other dog was prettier.";
        expected = HAS_LEX ? "dh-ah d-ao-g r-ae-n f-ae/s-t-er dh-ae-n dh-ah ah/dh-er d-ao-g . b-ah-t dh-ah ah/dh-er d-ao-g w-aa-z p-r-ih/t-iy/er ." : "dh-ah d-aa-g r-ah-n f-ae/s-t-er th-ae-n dh-ah ah/dh-er d-aa-g . b-ah-t dh-ah ah/dh-er d-aa-g w-ah-z p-r-eh/t-iy/er .";
        assertEquals(expected, RiTa.syllables(input));

        input = "The emperor had no clothes on.";
        expected = HAS_LEX ? "dh-ah eh-m/p-er/er hh-ae-d n-ow k-l-ow-dh-z aa-n ." : "dh-ah eh-m/p-er/er hh-ae-d n-ow k-l-ow-dh-z ah-n .";
        assertEquals(expected, RiTa.syllables(input));

        RiTa.SILENCE_LTS = silent;
    }

    @Test
    void shouldPluralizePhrases() {
        String input;
        String expected;
        input = "set of choice";
        expected = "set of choices";
        assertEquals(expected, RiTa.pluralize(input));

        input = "bag of chocolate";
        expected = "bag of chocolates";
        assertEquals(expected, RiTa.pluralize(input));

        input = "gaggle of goose";
        expected = "gaggle of geese";
        assertEquals(expected, RiTa.pluralize(input));
    }

    @Test
    void shouldDoNothingWhenInputToPluralizeIsAlreadyPlural() {
        // same for mass nouns
        String[] tests = {"tidings", "schnapps", "canvases", "censuses", "bonuses", "isthmuses", "thermoses", "circuses", "tongs", "emeriti"};
        for (String t : tests) {
            RiTa.pluralize(t, Map.of("dbug", 0));
            assertEquals(t, RiTa.pluralize(t));
        }
    }

    @Test
    void shouldReturnTrueForAlreadyPluralNouns() {
        String[] tests = {"tidings", "schnapps", "canvases", "censuses", "bonuses", "isthmuses", "thermoses", "circuses", "tongs", "emeriti"};
        for (String t : tests) {
            boolean res = RiTa.inflector.isPlural(t, Map.of("dbug", 0));
            assertTrue(res);
        }
    }

    @Test
    void shouldHandleSingularNounsInTaggerAllTags() {
        String[] tests = {"tiding", "census", "bonus", "thermos", "circus"};
        for (String t : tests) {
            List<String> res = Arrays.asList(RiTa.tagger.allTags(t, false));
            assertTrue(res.contains("nn"));
        }
    }

    @Test
    void shouldHandleNumberSingularPlural() {
        assertTrue(RiTa.inflector.isPlural("dreariness", Map.of("dbug", 0)));

        assertEquals("", RiTa.singularize());
        assertEquals("", RiTa.singularize(""));
        // JS: expect(() => RiTa.singularize([1])).to.throw() — not portable to a typed language.
        // JS: expect(() => RiTa.singularize(1)).to.throw() — ditto.

        assertEquals("", RiTa.pluralize());
        assertEquals("", RiTa.pluralize(""));
        // JS: expect(() => RiTa.pluralize([1])).to.throw() — not portable.
        // JS: expect(() => RiTa.pluralize(1)).to.throw() — ditto.

        String[] testPairs = {
            "abysses", "abyss", "knives", "knife", "dazes", "daze", "hives", "hive", "dives", "dive",
            "octopuses", "octopus", "abalone", "abalone", "wildlife", "wildlife", "minutiae", "minutia",
            "spoofs", "spoof", "proofs", "proof", "roofs", "roof", "disbeliefs", "disbelief", "beliefs", "belief",
            "indices", "index", "accomplices", "accomplice", "prognoses", "prognosis", "taxis", "taxi",
            "chiefs", "chief", "monarchs", "monarch", "lochs", "loch", "stomachs", "stomach", "Chinese", "Chinese",
            "people", "person", "humans", "human", "germans", "german", "romans", "roman", "memoranda", "memorandum",
            "data", "datum", "geese", "goose", "femurs", "femur", "appendices", "appendix", "theses", "thesis",
            "alumni", "alumnus", "solos", "solo", "music", "music", "oxen", "ox", "money", "money", "beef", "beef",
            "tobacco", "tobacco", "cargo", "cargo", "golf", "golf", "grief", "grief", "cakes", "cake",
            "tomatoes", "tomato", "photos", "photo", "smallpox", "smallpox", "toes", "toe", "mice", "mouse",
            "lice", "louse", "children", "child", "gases", "gas", "buses", "bus", "happiness", "happiness",
            "apotheoses", "apotheosis", "stimuli", "stimulus", "dogs", "dog", "feet", "foot", "teeth", "tooth",
            "deer", "deer", "sheep", "sheep", "shrimp", "shrimp", "men", "man", "women", "woman",
            "congressmen", "congressman", "aldermen", "alderman", "freshmen", "freshman", "firemen", "fireman",
            "grandchildren", "grandchild", "menus", "menu", "gurus", "guru", "hardness", "hardness", "fish", "fish",
            "ooze", "ooze", "enterprises", "enterprise", "treatises", "treatise", "houses", "house",
            "chemises", "chemise", "aquatics", "aquatics", "mechanics", "mechanics", "quarters", "quarter",
            "motifs", "motif", "turf", "turf", "macaroni", "macaroni", "spaghetti", "spaghetti",
            "potpourri", "potpourri", "electrolysis", "electrolysis", "series", "series", "crises", "crisis",
            "corpora", "corpus", "shortness", "shortness", "dreariness", "dreariness", "unwillingness", "unwillingness",
            "moose", "moose", "lives", "life", "additives", "additive", "epochs", "epoch", "ranchs", "ranch",
            "alcoves", "alcove", "memories", "memory", "grooves", "groove", "universes", "universe",
            "toothbrushes", "toothbrush", "clashes", "clash", "addresses", "address", "flashes", "flash",
            "conclaves", "conclave", "promises", "promise", "spouses", "spouse", "branches", "branch",
            "lapses", "lapse", "quizes", "quiz", "spyglasses", "spyglass", "overpasses", "overpass",
            "clones", "clones", "microwaves", "microwave", "hypotheses", "hypothesis", "pretenses", "pretense",
            "latches", "latch", "fetuses", "fetus", "lighthouses", "lighthouse", "genuses", "genus",
            "zombies", "zombie", "hearses", "hearse", "trenches", "trench", "paradoxes", "paradox",
            "hippies", "hippie", "yuppies", "yuppie", "purses", "purse", "hatches", "hatch", "witches", "witch",
            "sinuses", "sinus", "phrases", "phrase", "arches", "arch", "duplexes", "duplex", "missives", "missive",
            "madhouses", "madhouse", "pauses", "pause", "heroes", "hero", "sketches", "sketch", "meshes", "mesh",
            "brasses", "brass", "marshes", "marsh", "masses", "mass", "impulses", "impulse", "pelvises", "pelvis",
            "fetishes", "fetish", "gashes", "gash", "directives", "directive", "calories", "calorie", "moves", "move",
            "expanses", "expanse", "briefcases", "briefcase", "media", "medium", "millennia", "millennium",
            "consortia", "consortium", "concerti", "concerto", "septa", "septum", "termini", "terminus",
            "larvae", "larva", "vertebrae", "vertebra", "memorabilia", "memorabilium", "hooves", "hoof",
            "thieves", "thief", "rabbis", "rabbi", "flu", "flu", "safaris", "safari", "sheaves", "sheaf",
            "uses", "use", "pinches", "pinch", "catharses", "catharsis", "hankies", "hanky", "whizzes", "whiz",
            "selves", "self", "bookshelves", "bookshelf", "wheezes", "wheeze", "diagnoses", "diagnosis",
            "blondes", "blonde", "eyes", "eye", "swine", "swine", "cognoscenti", "cognoscenti", "bonsai", "bonsai",
            "rice", "rice", "clothes", "clothes", "goddesses", "goddess", "tresses", "tress",
            "murderesses", "murderess", "kisses", "kiss"
        };
        String res1;
        String res2;
        boolean res3;
        boolean res4;

        for (int i = 0; i < testPairs.length; i += 2) {
            String plural = testPairs[i];
            String singular = testPairs[i + 1];

            res1 = RiTa.singularize(plural);
            res2 = RiTa.pluralize(singular);
            res3 = RiTa.inflector.isPlural(plural);
            res4 = RiTa.inflector.isPlural(singular);

            // singularize
            assertEquals(singular, res1, "FAIL1: singularize(" + plural
                + ") was " + res1 + ", but expected " + singular + "\n        "
                + "pluralize(" + singular + ") was " + res2 + "\n\n");

            // pluralize
            assertEquals(plural, res2, "FAIL2: pluralize(" + singular
                + ") was " + res2 + ", but expected " + plural + "\n        "
                + "singularize(" + plural + ") was " + res1 + "\n\n");

            // isPlural
            assertTrue(res3, "FAIL3: isPlural(" + plural + ") was false for plural noun\n\n");

            // isPlural
            boolean isMass = RitaMassNouns.values().contains(singular.toLowerCase());
            boolean isModal = singular.endsWith("ness");
            if (!isMass && !isModal) {
                assertEquals(false, res4, "FAIL4: isPlural(" + singular + ") was true for singular noun,"
                    + " isMassNoun=" + isMass + "\n\n");
            }
        }
    }

    @Test
    void shouldCallPhonesToStress() {
        assertNull(RiTa.analyzer.phonesToStress(null));
        assertEquals("", RiTa.analyzer.phonesToStress(" "));
        assertEquals("0/1/0", RiTa.analyzer.phonesToStress("ah b-ae1-n d-ah-n"));
    }

    @Test
    void shouldNotPluralizeOrSingularizeUncountables() {
        assertEquals("honey", RiTa.pluralize("honey"));
        assertEquals("pasta", RiTa.pluralize("pasta"));
        assertEquals("advice", RiTa.pluralize("advice"));
        assertEquals("fanfare", RiTa.pluralize("fanfare"));
        assertEquals("medicare", RiTa.pluralize("medicare"));
        assertEquals("childcare", RiTa.pluralize("childcare"));

        assertEquals("honey", RiTa.singularize("honey"));
        assertEquals("pasta", RiTa.singularize("pasta"));
        assertEquals("advice", RiTa.singularize("advice"));
        assertEquals("fanfare", RiTa.singularize("fanfare"));
        assertEquals("medicare", RiTa.singularize("medicare"));
        assertEquals("childcare", RiTa.singularize("childcare"));
    }

    @Test
    void shouldCallIsPlural() {
        assertEquals(false, RiTa.inflector.isPlural());
        assertEquals(false, RiTa.inflector.isPlural(""));

        assertEquals(false, RiTa.inflector.isPlural("octopus", Map.of("dbug", 0)));
        assertTrue(RiTa.inflector.isPlural("sheep"));
        assertTrue(RiTa.inflector.isPlural("apples"));
        assertTrue(RiTa.inflector.isPlural("leaves", Map.of("debug", false)));
        assertTrue(RiTa.inflector.isPlural("feet", Map.of("debug", false)));
        assertEquals(false, RiTa.inflector.isPlural("beaux", Map.of("debug", false)));
        assertEquals(false, RiTa.inflector.isPlural("child", Map.of("debug", false)));
        assertTrue(RiTa.inflector.isPlural("abbots", Map.of("debug", false)));
        assertTrue(RiTa.inflector.isPlural("happiness"));

        assertTrue(RiTa.inflector.isPlural("pasta"));
        assertTrue(RiTa.inflector.isPlural("honey"));
        assertTrue(RiTa.inflector.isPlural("fanfare"));
        assertTrue(RiTa.inflector.isPlural("medicare"));
        assertTrue(RiTa.inflector.isPlural("childcare"));
    }

    @Test
    void shouldCallComputePhones() {
        assertEquals(List.of("l", "iy", "ow"), RiTa.analyzer.computePhones("leo"));

        // bad inputs -> return undefined
        assertNull(RiTa.analyzer.computePhones(null));
        assertNull(RiTa.analyzer.computePhones("."));
        assertNull(RiTa.analyzer.computePhones(""));
        assertNull(RiTa.analyzer.computePhones(","));

        // non-english input -> return undefined
        assertNull(RiTa.analyzer.computePhones("你好", Map.of("silent", true)));
        assertNull(RiTa.analyzer.computePhones("Künste", Map.of("silent", true)));
        assertEquals(List.of("l", "iy", "ow"), RiTa.analyzer.computePhones("leo", Map.of("silent", true)));

        // with "'"
        assertEquals(List.of("s", "t", "uw1", "d", "eh1", "n", "t", "z"), RiTa.analyzer.computePhones("student's"));

        // numbers
        assertNull(RiTa.analyzer.computePhones("-1", Map.of("silent", true))); // TODO:

        if (!HAS_LEX) {
            return; // NOTE: below currently fail without lexicon
        }

        assertEquals(List.of("w", "ah", "n"), RiTa.analyzer.computePhones("1"));
        assertEquals(List.of("f", "ay", "v", "z", "ih", "r", "ow"), RiTa.analyzer.computePhones("50"));
    }

    @Test
    void shouldCallAnalyzeWithIpaPhonesOption() {
        // empty input
        RiTa.Analysis feats = RiTa.analyze("", Map.of("ipaPhones", true));
        assertEquals("", feats.phones);

        // single monosyllabic word — no stress marker
        feats = RiTa.analyze("cat", Map.of("ipaPhones", true));
        assertEquals("kæt", feats.phones);
        assertEquals("k-ae-t", feats.syllables); // syllables still Arpabet
        assertEquals("1", feats.stresses);       // stresses unchanged

        // single polysyllabic word — stressed syllable gets ˈ
        feats = RiTa.analyze("abandon", Map.of("ipaPhones", true));
        assertEquals("əˈbændən", feats.phones);

        // unstressed 'the' → ðə
        feats = RiTa.analyze("the", Map.of("ipaPhones", true));
        assertEquals("ðə", feats.phones);

        // multi-word sentence
        feats = RiTa.analyze("The birch canoe slid on the smooth planks", Map.of("ipaPhones", true));
        assertEquals("ðə bɜrtʃ kəˈnuː slɪd ɑːn ðə smuːð plæŋkz", feats.phones);

        // sentence with punctuation — punctuation tokens are skipped in IPA output
        feats = RiTa.analyze("The dog ran.", Map.of("ipaPhones", true));
        assertEquals("ðə dɔːɡ ɹæn", feats.phones);

        // ipaPhones: false (default) returns Arpabet
        feats = RiTa.analyze("abandon");
        assertEquals("ah-b-ae-n-d-ah-n", feats.phones);

        feats = RiTa.analyze("abandon", Map.of("ipaPhones", false));
        assertEquals("ah-b-ae-n-d-ah-n", feats.phones);
    }

    @Test
    void shouldCallPhonesWithIpaPhonesOption() {
        // mirrors RiTa.analyze — same logic, just returns the string directly
        assertEquals("", RiTa.phones("", Map.of("ipaPhones", true)));
        assertEquals("kæt", RiTa.phones("cat", Map.of("ipaPhones", true)));
        assertEquals("əˈbændən", RiTa.phones("abandon", Map.of("ipaPhones", true)));
        assertEquals("ðə", RiTa.phones("the", Map.of("ipaPhones", true)));
        assertEquals("ðə bɜrtʃ kəˈnuː slɪd ɑːn ðə smuːð plæŋkz",
            RiTa.phones("The birch canoe slid on the smooth planks", Map.of("ipaPhones", true)));

        // default (no option) still returns Arpabet
        assertEquals("ah-b-ae-n-d-ah-n", RiTa.phones("abandon"));
        assertEquals("ah-b-ae-n-d-ah-n", RiTa.phones("abandon", Map.of("ipaPhones", false)));
    }

    @Test
    void shouldCallSyllablesWithIpaPhonesOption() {
        // syllable boundaries preserved as '/' in IPA output
        assertEquals("ə/ˈbæn/dən", RiTa.syllables("abandon", Map.of("ipaPhones", true)));
        assertEquals("ðə", RiTa.syllables("the", Map.of("ipaPhones", true)));
        assertEquals("ðə bɜrtʃ kə/ˈnuː slɪd ɑːn ðə smuːð plæŋkz",
            RiTa.syllables("The birch canoe slid on the smooth planks", Map.of("ipaPhones", true)));

        // punctuation skipped
        assertEquals("ðə dɔːɡ ɹæn", RiTa.syllables("The dog ran.", Map.of("ipaPhones", true)));

        // default still returns Arpabet with boundaries
        assertEquals("ah/b-ae-n/d-ah-n", RiTa.syllables("abandon"));
    }

    /** Mirrors {@code RiTa.MASS_NOUNS} for the isMass check in the number test. */
    private static final class RitaMassNouns {
        static List<String> values() {
            return RiTa.MASS_NOUNS;
        }
    }
}
