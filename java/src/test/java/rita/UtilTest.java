package rita;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

/**
 * Tests for {@link Util} — port of the reference cases in <code>python/test_util.py</code>
 * (itself ported from the JS util module), with expected values verified against the JS
 * implementation via node.
 */
class UtilTest {

    // ---- RE ---------------------------------------------------------------------------

    @Test
    void reApplies() {
        RE rule = new RE(".*s$", 1, "es");
        assertTrue(rule.applies("cats"));
        assertTrue(rule.applies("dogs"));
        assertFalse(rule.applies("dog"));
        assertFalse(rule.applies("cat"));
    }

    @Test
    void reFireWithOffset() {
        RE rule = new RE(".*s$", 1, "es");
        assertEquals("cates", rule.fire("cats"));
        assertEquals("doges", rule.fire("dogs"));
    }

    @Test
    void reFireNoOffset() {
        RE rule = new RE(".*", 0, "s");
        assertEquals("cats", rule.fire("cat"));
        assertEquals("dogs", rule.fire("dog"));
    }

    @Test
    void reTruncate() {
        RE rule = new RE(".*y$", 1, "ies");
        assertEquals("happ", rule.truncate("happy"));
        assertEquals("funn", rule.truncate("funny"));
    }

    @Test
    void reTruncateMultipleChars() {
        RE rule = new RE(".*", 3, "ing");
        assertEquals("runn", rule.truncate("running"));
    }

    @Test
    void reNoTruncate() {
        RE ruleNoOffset = new RE(".*", 0, "s");
        assertEquals("cat", ruleNoOffset.truncate("cat"));
    }

    @Test
    void reToString() {
        assertEquals("/abc/", new RE("abc", 1, "x").toString());
    }

    // ---- isNum ------------------------------------------------------------------------

    @Test
    void isNumIntegers() {
        assertTrue(Util.isNum(42));
        assertTrue(Util.isNum(0));
        assertTrue(Util.isNum(-5));
    }

    @Test
    void isNumFloats() {
        assertTrue(Util.isNum(3.14));
        assertTrue(Util.isNum(-2.5));
        assertTrue(Util.isNum(0.0));
    }

    @Test
    void isNumStringNumbers() {
        assertTrue(Util.isNum("123"));
        assertTrue(Util.isNum("3.14"));
        assertTrue(Util.isNum("-42"));
    }

    @Test
    void isNumNonNumbers() {
        assertFalse(Util.isNum("abc"));
        assertFalse(Util.isNum("12x"));
        assertFalse(Util.isNum("12abc"));
        assertFalse(Util.isNum(null));
        assertFalse(Util.isNum(""));
        assertFalse(Util.isNum(new ArrayList<>()));
        assertFalse(Util.isNum(new HashMap<>()));
    }

    // ---- numOpt -----------------------------------------------------------------------

    @Test
    void numOpt() {
        Map<String, Object> opts = new HashMap<>();
        opts.put("temp", 0.5);
        opts.put("count", 10);
        opts.put("zero", 0);
        opts.put("invalid", "foo");

        assertEquals(0.5, Util.numOpt(opts, "temp"), 1e-9);
        assertEquals(10, (int) Util.numOpt(opts, "count"));
        assertEquals(0, (int) Util.numOpt(opts, "zero")); // zero is valid
        assertEquals(42, (int) Util.numOpt(opts, "invalid", 42));
        assertEquals(99, (int) Util.numOpt(opts, "missing", 99));
        assertEquals(7, (int) Util.numOpt(null, "any", 7));
    }

    // ---- syllablesToPhones ------------------------------------------------------------

    @Test
    void syllablesToPhonesSimple() {
        // "cat" = k-ae1-t
        List<Util.Syllable> syllables = List.of(
            new Util.Syllable(List.of("1"), List.of("k"), List.of("ae"), List.of("t")));
        assertEquals("k-ae1-t", Util.syllablesToPhones(syllables));
    }

    @Test
    void syllablesToPhonesNoStress() {
        List<Util.Syllable> syllables = List.of(
            new Util.Syllable(new ArrayList<>(), List.of("k"), List.of("ae"), List.of("t")));
        assertEquals("k-ae-t", Util.syllablesToPhones(syllables));
    }

    @Test
    void syllablesToPhonesMulti() {
        // "began" = b-ih g-ae1-n
        List<Util.Syllable> syllables = List.of(
            new Util.Syllable(new ArrayList<>(), List.of("b"), List.of("ih"), List.of()),
            new Util.Syllable(List.of("1"), List.of("g"), List.of("ae"), List.of("n")));
        assertEquals("b-ih g-ae1-n", Util.syllablesToPhones(syllables));
    }

    @Test
    void syllablesToPhonesComplexOnset() {
        // "strong" = s-t-r-ao1-ng
        List<Util.Syllable> syllables = List.of(
            new Util.Syllable(List.of("1"), List.of("s", "t", "r"), List.of("ao"), List.of("ng")));
        assertEquals("s-t-r-ao1-ng", Util.syllablesToPhones(syllables));
    }

    @Test
    void syllablesToPhonesAbandon() {
        // ah/b-ae-n/d-ah-n
        List<Util.Syllable> syllables = List.of(
            new Util.Syllable(new ArrayList<>(), List.of(), List.of("ah"), List.of()),
            new Util.Syllable(List.of("1"), List.of("b"), List.of("ae"), List.of("n")),
            new Util.Syllable(new ArrayList<>(), List.of("d"), List.of("ah"), List.of("n")));
        assertEquals("ah b-ae1-n d-ah-n", Util.syllablesToPhones(syllables));
    }

    // ---- syllablesFromPhones ----------------------------------------------------------

    @Test
    void syllablesFromPhonesSimple() {
        String result = Util.syllablesFromPhones("k-ae1-t");
        assertTrue(result.contains("ae1"));
        assertTrue(result.contains("k"));
        assertTrue(result.contains("t"));
        assertEquals("k-ae1-t", result);
    }

    @Test
    void syllablesFromPhonesArrayMulti() {
        // JS splits on '-' only; the array form gives clean phonemes -> two syllables
        String result = Util.syllablesFromPhones(Arrays.asList("k", "ae1", "t", "ih", "ng"));
        assertEquals("k-ae1 t-ih-ng", result);
    }

    @Test
    void syllablesFromPhonesCloze() {
        String result = Util.syllablesFromPhones("k-l-ow1-z");
        assertEquals(0, spaces(result));
        assertTrue(result.contains("ow1"));
    }

    @Test
    void syllablesFromPhonesClothes() {
        String result = Util.syllablesFromPhones("k-l-ow-dh-z");
        assertEquals(0, spaces(result));
    }

    @Test
    void syllablesFromPhonesEmpty() {
        assertEquals("", Util.syllablesFromPhones(""));
        assertEquals("", Util.syllablesFromPhones((String) null));
    }

    @Test
    void syllablesFromPhonesInvalid() {
        assertThrows(RuntimeException.class, () -> Util.syllablesFromPhones("k-xx-t"));
        assertThrows(RuntimeException.class, () -> Util.syllablesFromPhones("foo"));
    }

    @Test
    void syllablesRoundtrip() {
        List<Util.Syllable> original = List.of(
            new Util.Syllable(List.of("1"), List.of("k"), List.of("ae"), List.of("t")));
        String phonesStr = Util.syllablesToPhones(original);
        String reconstructed = Util.syllablesFromPhones(phonesStr);
        assertTrue(reconstructed.contains("k"));
        assertTrue(reconstructed.contains("ae1"));
        assertTrue(reconstructed.contains("t"));
    }

    /** Number of spaces in a string (JS {@code str.split(' ').length - 1}). */
    private static int spaces(String s) {
        int n = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == ' ') {
                n++;
            }
        }
        return n;
    }

    // ---- Phones -----------------------------------------------------------------------

    @Test
    void consonantsCoverage() {
        List<String> c = Util.Phones.consonants;
        for (String p : List.of("k", "t", "p", "b", "d", "g", "f", "v", "s", "z", "sh", "th",
            "dh", "m", "n", "ng", "l", "r")) {
            assertTrue(c.contains(p), p);
        }
        assertFalse(c.contains("ae"));
        assertFalse(c.contains("iy"));
    }

    @Test
    void vowelsCoverage() {
        List<String> v = Util.Phones.vowels;
        for (String p : List.of("aa", "ae", "ah", "ao", "eh", "ih", "iy", "ow", "uh", "uw",
            "ay", "aw", "ey", "oy")) {
            assertTrue(v.contains(p), p);
        }
        assertFalse(v.contains("k"));
        assertFalse(v.contains("t"));
    }

    @Test
    void onsetsSimple() {
        List<String> o = Util.Phones.onsets;
        for (String p : List.of("k", "t", "p", "b")) {
            assertTrue(o.contains(p), p);
        }
        assertTrue(o.contains(""));
    }

    @Test
    void onsetsClusters() {
        List<String> o = Util.Phones.onsets;
        for (String p : List.of("k r", "s t", "s p", "p l", "s t r", "s k r")) {
            assertTrue(o.contains(p), p);
        }
    }

    // ---- Numbers ----------------------------------------------------------------------

    @Test
    void fromWordsBasics() {
        Map<String, Integer> n = Util.Numbers.fromWords;
        assertEquals(0, (int) n.get("zero"));
        assertEquals(1, (int) n.get("one"));
        assertEquals(2, (int) n.get("two"));
        assertEquals(3, (int) n.get("three"));
        assertEquals(10, (int) n.get("ten"));
        assertEquals(20, (int) n.get("twenty"));
        assertEquals(90, (int) n.get("ninety"));
    }

    @Test
    void fromWordsTeens() {
        Map<String, Integer> n = Util.Numbers.fromWords;
        assertEquals(11, (int) n.get("eleven"));
        assertEquals(12, (int) n.get("twelve"));
        assertEquals(13, (int) n.get("thirteen"));
        assertEquals(19, (int) n.get("nineteen"));
    }

    @Test
    void toWordsBasics() {
        Map<String, String> w = Util.Numbers.toWords;
        assertEquals("zero", w.get("0"));
        assertEquals("one", w.get("1"));
        assertEquals("two", w.get("2"));
        assertEquals("ten", w.get("10"));
        assertEquals("twenty", w.get("20"));
        assertEquals("ninety", w.get("90"));
    }

    @Test
    void numbersRoundtrip() {
        Map<String, Integer> from = Util.Numbers.fromWords;
        Map<String, String> to = Util.Numbers.toWords;
        for (String word : List.of("zero", "one", "two", "ten", "twenty", "thirty", "eleven",
            "twelve", "fifteen")) {
            assertEquals(word, to.get(String.valueOf(from.get(word))));
        }
    }
}
