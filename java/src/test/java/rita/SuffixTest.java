package rita;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

/**
 * Ported from <code>js/test/suffix-tests.spec.js</code>.
 *
 * <p>Mapping notes:
 * <ul>
 *   <li>{@code expect(x).to.deep.equal(y)} -> {@code assertEquals}; {@code assert.deepStrictEqual}
 *       on {@code int[]} -> {@code assertArrayEquals}.</li>
 *   <li>JS dynamic field access {@code obj[f]} / {@code Object.keys(obj)} (used by the
 *       to/fromJSON round-trip) are mirrored with the reflection helpers {@link #fieldOf} and
 *       {@link #keysOf}.</li>
 *   <li>{@code seqmap.filter(e => e)} (truthy entries) -> {@link #truthy}.</li>
 *   <li>JS {@code .to.throw()} -> {@code assertThrows}; {@code .to.throw} without parens is a
 *       chai no-op and is kept only where it carried an assertion.</li>
 * </ul>
 */
class SuffixTest {

    static final String SEQ_START_TOKEN = SuffixArray.SEQ_START_TOKEN;
    static final String SEQ_END_TOKEN = SuffixArray.SEQ_END_TOKEN;

    static final List<String> exampleTokens = List.of(
        SEQ_START_TOKEN,
        "The", "brown",
        "fox", "jumps",
        "over", "the",
        "lazy", "dog",
        ".",
        SEQ_END_TOKEN,
        SEQ_START_TOKEN,
        "The", "brown",
        "dog", "wept",
        "over", "the",
        "treat", ".",
        SEQ_END_TOKEN);

    static final List<String> longerTokens = List.of(
        "<s>", "Little", "humps", "of", "sand", ",", "of", "water", "mixed", "with", "sand", "so", "thoroughly", "that", "granules", "of", "this", "new", "matter", "have", "the", "texture", "of", "firn", ",", "stick", "out", "smartly", "where", "the", "surf", "used", "to", "pound", "the", "shore", ",", "and", "beyond", "that", "a", "great", "frozen", "slab", "opens", "out", "like", "a", "cold", "hand", ",", "lined", "with", "the", "details", "of", "waves", ",", "crests", ",", "white", "horses", "of", "snow", ",", "a", "fleeting", "image", "of", "air", "in", "a", "furtive", "coupling", "of", "wind", "and", "spray", ",", "an", "alphabet", "of", "meanings", "receding", "to", "the", "horizon", ",", "repeated", "to", "infinity", ",", "an", "infinity", "of", "vibrations", "and", "still-born", "interferences", ".", "</s>",
        "<s>", "But", "it\u2019s", "a", "splendid", "funeral", ";", "all", "around", ",", "in", "the", "strong", "wind", ",", "thousands", "of", "snowflakes", "are", "crowding", ",", "each", "one", "a", "crystal", "star", "with", "its", "own", "particular", "design", ".", "</s>",
        "<s>", "The", "path", "was", "like", "those", "that", "wind", "from", "the", "crest", "of", "the", "Downs", "south", "to", "the", "sea", ".", "</s>",
        "<s>", "That", "seems", "to", "even", "things", ",", "for", "those", "who", "regard", "it", "as", "a", "balance", ",", "or", "think", "the", "wind", "blows", "one", "way", ".", "</s>",
        "<s>", "And", "they", "hadn\u2019t", "invented", "wind", "and", "rain", ",", "so", "the", "footprints", "stayed", "where", "they", "were", ".", "</s>",
        "<s>", "They", "hadn\u2019t", "invented", "wind", "and", "rain", ",", "remember", ".", "</s>",
        "<s>", "In", "winter", ",", "when", "the", "wind", "blows", "hard", "and", "there\u2019s", "no", "one", "about", "in", "these", "out-of-the-way", "places", ",", "I", "like", "to", "hear", "the", "flag", "crack", "like", "a", "whip", "with", "the", "fish", "swimming", "in", "the", "sky", "as", "if", "it", "were", "alive", ".", "</s>",
        "<s>", "But", "in", "high", "winter", ",", "the", "flag", "thrashes", "up", "there", "with", "its", "fish", "in", "the", "air", ",", "trembling", "with", "cold", ",", "wind", "and", "sky", ".", "</s>",
        "<s>", "I", "see", "the", "iron", "fences", "and", "the", "shallow", "ditches", "of", "the", "countryside", "the", "mild", "wind", "has", "travelled", "over", ".", "</s>",
        "<s>", "I", "cannot", "join", "together", "the", "mild", "wind", "and", "the", "shallow", "ditches", ",", "I", "cannot", "lay", "the", "light", "across", "the", "world", "and", "then", "watch", "it", "slide", "away", ".", "</s>",
        "<s>", "In", "the", "mirror", ",", "the", "wind", "from", "the", "south", "spins", ",", "carrying", "leaves", "and", "feathers", ".", "</s>",
        "<s>", "In", "the", "wind", "from", "the", "desert", "the", "needles", "bend", "and", "my", "hour", "is", "past", ".", "</s>",
        "<s>", "Everywhere", "the", "light", "wind", "blows", ",", "the", "breeze", "that", "provokes", "the", "immense", "whiplash", "each", "time", "it", "unwinds", "in", "the", "air", ".", "</s>",
        "<s>", "The", "light", "wind", "rises", "from", "the", "meadows", "of", "the", "past", ",", "and", "hurries", "closer", "to", "our", "time", ".", "</s>",
        "<s>", "A", "great", "wind", "is", "blowing", "from", "the", "centre", ".", "</s>",
        "<s>", "Hearths", "that", "were", "red", "yesterday", "are", "now", "dead", "ashes", ",", "and", "the", "wind", "blowing", "through", "the", "burst-open", "windows", ".", "</s>",
        "<s>", "A", "sudden", "icy", "wind", "struck", "me", ";", "I", "felt", "my", "legs", "go", "numb", ".", "</s>",
        "<s>", "Secret", "the", "meeting", "in", "time", "and", "place", ",", "the", "time", "of", "the", "off-shore", "wind", ",", "the", "place", "where", "the", "loyalty", "is", "divided", ".", "</s>",
        "<s>", "Green", "is", "almost", "uniformly", "spread", "over", "the", "plants", ",", "the", "wind", "follows", "the", "birds", ",", "no", "one", "risks", "seeing", "the", "stones", "die", ".", "</s>",
        "<s>", "The", "wind", "roars", "up", "the", "avenue", ".", "</s>",
        "<s>", "The", "wind", "falls", ",", "the", "rain", "slides", "silver", "down", "the", "glass", ".", "</s>",
        "<s>", "The", "wind", "drives", "straightly", ";", "the", "flame", "stoops", "slightly", ".", "</s>",
        "<s>", "At", "sunset", ",", "when", "there", "was", "no", "wind", ",", "and", "the", "pine-smoke", "from", "over", "by", "the", "sawmill", "hugged", "the", "earth", ",", "and", "you", "couldn\u2019t", "see", "more", "than", "a", "few", "feet", "in", "front", ",", "her", "sudden", "darting", "past", "you", "was", "a", "bit", "of", "vivid", "color", ",", "like", "a", "black", "bird", "that", "flashes", "in", "light", ".", "</s>",
        "<s>", "In", "sad", "times", ",", "hurt", "seabirds", "come", "to", "wail", "in", "ice", "white", "wind", ",", "alone", ",", "and", "wail", "in", "starlight", "wells", ",", "cold", "pits", "of", "evening", ",", "and", "endings", ",", "flinging", "rounds", "of", "flame", "sheeted", "balls", "of", "jagged", "bone", ",", "eaten", ",", "with", "remains", "of", "torn", "flowers", ",", "overwhelming", "after-thoughts", ",", "binding", "loves", ",", "classic", "pains", ",", "casting", "elongated", "shadows", ",", "of", "early", "blue", ".", "</s>",
        "<s>", "Will", "you", "come", "to", "visit", "me", "in", "hospital", "?", ";", "I", "stood", "up", ",", "I", "sat", "down", ",", "I", "stood", "up", "again", ";", "the", "clock", "slowed", "down", ",", "the", "post", "came", "late", ",", "the", "afternoon", "turned", "cool", ";", "the", "cat", "licked", "his", "coat", ",", "tore", "the", "chair", "to", "shreds", ",", "slept", "in", "a", "drawer", "that", "didn\u2019t", "close", ";", "I", "entered", "a", "room", ",", "I", "felt", "my", "skin", "shiver", ",", "then", "dissolve", ",", "I", "lighted", "a", "candle", ",", "I", "saw", "something", "move", ",", "I", "recognized", "the", "shadow", "to", "be", "my", "own", "hand", ",", "I", "felt", "myself", "to", "be", "one", "thing", ";", "the", "wind", "was", "hard", ",", "the", "house", "swayed", ",", "the", "angiosperms", "prospered", ",", "the", "mammal-like", "reptiles", "vanished", "Is", "the", "Heaven", "to", "be", "above", "?", "</s>");

    @Test
    void suffixArrayConstructor() {
        SuffixArray sa;

        sa = new SuffixArray(List.of("b", "c", "a"));
        assertEquals(3, sa.data.length);
        assertEquals(List.of(), truthy(sa.seqmap));
        assertArrayEquals(new int[]{2, 0, 1}, sa.data);

        sa = new SuffixArray(List.of("b", "c", "ab", "a"), Map.of("debug", 0));
        assertEquals(4, sa.data.length);
        assertEquals(List.of(), truthy(sa.seqmap));
        assertArrayEquals(new int[]{3, 2, 0, 1}, sa.data);

        sa = new SuffixArray(List.of("banana", "ananas"));
        assertEquals(2, sa.data.length);
        assertEquals(List.of(), truthy(sa.seqmap));
        assertArrayEquals(new int[]{1, 0}, sa.data);

        sa = new SuffixArray(exampleTokens);
        assertTrue(sa instanceof SuffixArray);
        assertTrue(sa.data != null);
        assertEquals(21, sa.data.length);
        assertArrayEquals(new int[]{
            19, 9, 20, 10, 11, 0, 12,
            1, 13, 2, 8, 14, 3, 4,
            7, 5, 16, 6, 17, 18, 15}, sa.data);
    }

    @Test
    void suffixArrayCompressed() {
        SuffixArray sa = new SuffixArray(exampleTokens);
        assertTrue(sa instanceof SuffixArray);
        assertTrue(sa.data != null);
        assertEquals(21, sa.data.length);
        assertArrayEquals(new int[]{
            19, 9, 20, 10, 11, 0, 12,
            1, 13, 2, 8, 14, 3, 4,
            7, 5, 16, 6, 17, 18, 15}, sa.data);
    }

    @Test
    void suffixArrayArrayCompare() {
        assertEquals(0, SuffixArray.arrayCompare(List.of(), List.of("a")));
        assertEquals(1, SuffixArray.arrayCompare(List.of("a", "b"), List.of("a")));
        assertEquals(2, SuffixArray.arrayCompare(List.of("a", "b", "c"), List.of("a", "b")));
        assertEquals(2, SuffixArray.arrayCompare(List.of("a", "b"), List.of("a", "b", "c")));
        assertEquals(2, SuffixArray.arrayCompare(List.of("a", "b"), List.of("a", "b", "c", "d")));
        assertEquals(2, SuffixArray.arrayCompare(List.of("The", "dog", "ate"), List.of("The", "dog", "ran")));
        assertEquals(-1, SuffixArray.arrayCompare(List.of(), List.of()));
        assertEquals(-1, SuffixArray.arrayCompare(List.of("a"), List.of("a")));
        assertEquals(-1, SuffixArray.arrayCompare(List.of("The", "dog", "ate"), List.of("The", "dog", "ate")));
    }

    @Test
    void suffixArrayArrayCompareSlices() {
        List<String> arr = List.of("a", "b", "c", "d");
        assertEquals(0, SuffixArray.arrayCompareSlices(arr, 0, 0, 0, 1));
        assertEquals(1, SuffixArray.arrayCompareSlices(arr, 0, 2, 0, 1));
        assertEquals(2, SuffixArray.arrayCompareSlices(arr, 0, 3, 0, 2));
        assertEquals(2, SuffixArray.arrayCompareSlices(arr, 0, 2, 0, 3));
        assertEquals(2, SuffixArray.arrayCompareSlices(arr, 0, 2, 0, 4));
        assertEquals(1, SuffixArray.arrayCompareSlices(arr, 1, 2, 1, 4));
    }

    @Test
    void suffixArrayJson() {
        SuffixArray sa = new SuffixArray(exampleTokens);
        String json = sa.toJSON();

        SuffixArray sa2 = SuffixArray.fromJSON(json);
        assertEquals(keysOf(sa), keysOf(sa2));
        assertTrue(sa2 instanceof SuffixArray);
        for (String f : SuffixArray.__dict__) {
            assertDeep(fieldOf(sa2, f), fieldOf(sa, f), "1. failed on \"" + f + "\"");
        }

        SuffixArray sa3 = SuffixArray.fromJSON(json);
        assertTrue(sa3 instanceof SuffixArray);
        for (String f : SuffixArray.__dict__) {
            assertDeep(fieldOf(sa3, f), fieldOf(sa, f), "2. failed on" + f + "\"");
        }
        assertEquals(keysOf(sa), keysOf(sa3));
    }

    @Test
    void suffixArrayRandSeqStart() {
        SuffixArray model = new SuffixArray(exampleTokens);
        List<Integer> starts = new ArrayList<>();
        for (int i = 0; i < model.seqmap.length; i++) {
            if (model.seqmap[i] == 1) {
                starts.add(i);
            }
        }
        List<String> decoded = new ArrayList<>();
        for (int idx : starts) {
            @SuppressWarnings("unchecked")
            List<Integer> enc = (List<Integer>) model.input.get(idx + 1);
            decoded.add(String.join(" ", model._decode(enc)));
        }
        assertEquals(List.of("The", "The"), decoded);
        assertEquals("The", model.randSeqStart());
    }

    @Test
    void suffixArrayRandSeqStartHonorsSeed() {
        List<String> toks = List.of(
            SEQ_START_TOKEN, "The", "dog", "ran", SEQ_END_TOKEN,
            SEQ_START_TOKEN, "A", "cat", "sat", SEQ_END_TOKEN,
            SEQ_START_TOKEN, "Some", "bird", "flew", SEQ_END_TOKEN);
        SuffixArray model = new SuffixArray(toks);
        try {
            assertEquals(draw(model, 1), draw(model, 1));
            assertTrue(!draw(model, 1).equals(draw(model, 500)));
        } finally {
            RiTa.randomSeed((int) (System.currentTimeMillis()));
        }
    }

    private static List<String> draw(SuffixArray model, int seed) {
        RiTa.randomSeed(seed);
        List<String> out = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            out.add(model.randSeqStart());
        }
        return out;
    }

    @Test
    void suffixArrayFind() {
        SuffixArray sa;
        int[] mm;
        List<String> patt;
        List<List<String>> tokens;
        int count;

        sa = new SuffixArray(List.of("b", "c", "ab", "a"));
        assertEquals(List.of("c", "ab", "a"), sa.tokensFor(3));

        patt = List.of("ab");
        mm = sa.find(patt);
        tokens = sa.tokensForRange(mm[0], mm[1]);
        assertEquals(List.of(List.of("ab", "a")), tokens);
        assertPrefixes(tokens, patt);

        patt = List.of("ab", "a");
        mm = sa.find(patt);
        tokens = sa.tokensForRange(mm[0], mm[1]);
        assertPrefixes(tokens, patt);

        sa = new SuffixArray(List.of("b", "c", "ab", "a", "ab", "a", "c"));
        patt = List.of("ab", "a");
        mm = sa.find(patt);
        tokens = sa.tokensForRange(mm[0], mm[1]);
        assertPrefixes(tokens, patt);

        sa = new SuffixArray(exampleTokens, Map.of("debug", 0));
        patt = List.of("The", "brown");
        mm = sa.find(patt);
        count = mm[1] - mm[0];
        assertEquals(2, count);
        tokens = sa.tokensForRange(mm[0], mm[1]);
        assertPrefixes(tokens, patt);

        patt = List.of("over", "the");
        mm = sa.find(patt);
        count = mm[1] - mm[0];
        assertEquals(2, count);
        tokens = sa.tokensForRange(mm[0], mm[1]);
        assertPrefixes(tokens, patt);

        patt = List.of("The", "brown", "dog");
        mm = sa.find(patt);
        count = mm[1] - mm[0];
        assertEquals(1, count);
        tokens = sa.tokensForRange(mm[0], mm[1]);
        assertPrefixes(tokens, patt);

        mm = sa.find(List.of());
        count = mm[1] - mm[0];
        assertEquals(2, count);
        tokens = sa.tokensForRange(mm[0], mm[1]);
        for (List<String> t : tokens) {
            assertEquals(SEQ_START_TOKEN, t.get(0));
            assertEquals(SEQ_END_TOKEN, t.get(t.size() - 1));
        }

        sa = new SuffixArray(longerTokens);
        mm = sa.find(List.of("wind", "and", "the"));
        assertEquals(1, mm[1] - mm[0]);
    }

    @Test
    void suffixArrayTokensFor() {
        SuffixArray sa = new SuffixArray(List.of("b", "c", "ab", "a"));
        assertEquals(List.of("c", "ab", "a"), sa.tokensFor(3));

        sa = new SuffixArray(exampleTokens);
        List<String> toks = sa.tokensFor(11);
        assertEquals(List.of(
            "dog", "wept",
            "over", "the",
            "treat", ".",
            "</s>"), toks);
    }

    @Test
    void suffixArrayIsUnique() {
        SuffixArray sa = new SuffixArray(exampleTokens);
        assertTrue(!sa.isUnique(exampleTokens));
        assertTrue(!sa.isUnique(exampleTokens.subList(1, exampleTokens.size())));
        assertTrue(sa.isUnique(List.of("The", "clown", "dog", "wept", "over", "the", "treat", ".", "</s>")));
        assertTrue(!sa.isUnique(List.of("The", "brown", "dog", "wept", "over", "the", "treat", ".", "</s>")));
        assertTrue(sa.isUnique(List.of(
            SEQ_START_TOKEN,
            "The", "brown",
            "fox", "jumps",
            "over", "the",
            "treat", ".",
            SEQ_END_TOKEN)));
    }

    @Test
    void suffixArrayPdist() {
        Map<String, Double> dist;
        SuffixArray sa = new SuffixArray(exampleTokens);

        dist = sa.pdist(List.of("The", "brown"));
        assertEquals(Map.of("fox", 0.5, "dog", 0.5), dist);

        dist = sa.pdist(List.of(SEQ_END_TOKEN));
        assertEquals(Map.of(SEQ_START_TOKEN, 1.0), dist);

        dist = sa.pdist(List.of(".", SEQ_END_TOKEN));
        assertEquals(Map.of(SEQ_START_TOKEN, 1.0), dist);

        dist = sa.pdist(List.of("dog", ".", SEQ_END_TOKEN));
        assertEquals(Map.of(SEQ_START_TOKEN, 1.0), dist);

        List<String> inp = new ArrayList<>(exampleTokens);
        inp.addAll(List.of(SEQ_START_TOKEN, "The", "brown", "dog", "leapt", "over", "the", "fence", ".", SEQ_END_TOKEN,
            SEQ_START_TOKEN, "The", "brown", "dog", ".", SEQ_END_TOKEN));
        sa = new SuffixArray(inp);

        dist = sa.pdist(List.of("The", "brown"));
        assertEquals(Map.of("dog", 0.8807970779778824, "fox", 0.11920292202211755), dist);

        dist = sa.pdist(List.of("The", "brown"), Map.of("temp", 0));
        assertEquals(Map.of("fox", 0.25, "dog", 0.75), dist);

        dist = sa.pdist(List.of("leapt", "over", "the"));
        assertEquals(Map.of("fence", 1.0), dist);
    }

    @Test
    void suffixArrayHasSuffix() {
        boolean res;
        List<String> patt;
        SuffixArray sa = new SuffixArray(exampleTokens);
        patt = List.of("The", "brown", "dog", "wept", "over", "the", "treat", ".", "</s>");
        res = sa.hasSuffix(patt);
        assertEquals(true, res);

        patt = List.of("<s>", "The", "brown", "dog", "wept", "over", "the", "treat", ".", "</s>");
        res = sa.hasSuffix(patt);
        assertEquals(true, res);
        patt = List.of("<s>", "The", "brown", "dog", "wept", "over", "the", "treat", ".");
        res = sa.hasSuffix(patt);
        assertEquals(false, res);
        patt = List.of("<s>", "The", "brown", "dogs", "wept", "over", "the", "treat", ".", "</s>");
        res = sa.hasSuffix(patt);
        assertEquals(false, res);
        patt = List.of("The", "brown");
        res = sa.hasSuffix(patt);
        assertEquals(false, res);
    }

    @Test
    void suffixArrayHasPrefix() {
        boolean res;
        List<String> patt;
        SuffixArray sa;

        sa = new SuffixArray(List.of("<s>", "The", "dog", "ate", ".", "</s>"), Map.of("debug", 0));
        assertEquals(true, sa.hasPrefix(List.of("The", "dog"), Map.of("debug", 0)));
        assertEquals(true, sa.hasPrefix(List.of("The", "dog", "ate", ".", "</s>")));
        assertEquals(true, sa.hasPrefix(List.of("The", "dog", "ate", ".")));
        assertEquals(true, sa.hasPrefix(List.of("The", "dog", "ate")));
        assertEquals(true, sa.hasPrefix(List.of("The")));
        assertEquals(false, sa.hasPrefix(List.of("The", "fox", "ate", ".", "</s>")));
        assertEquals(false, sa.hasPrefix(List.of("The", "fox", "ate", ".")));
        assertEquals(false, sa.hasPrefix(List.of("The", "fox", "ate")));
        assertEquals(false, sa.hasPrefix(List.of("The", "fox")));

        sa = new SuffixArray(exampleTokens);
        patt = List.of("The", "brown", "dog", "wept", "over", "the", "treat", ".", "</s>");
        res = sa.hasPrefix(patt);
        assertEquals(true, res);
        patt = List.of("<s>", "The", "brown", "dog", "wept", "over", "the", "treat", ".", "</s>");
        res = sa.hasPrefix(patt);
        assertEquals(true, res);
        patt = List.of("The", "brown");
        res = sa.hasPrefix(patt);
        assertEquals(true, res);

        patt = List.of("The", "brown", "fox", "wept");
        res = sa.hasPrefix(patt);
        assertEquals(false, res);
        patt = List.of("<s>", "The", "brown", "dog", "over", "the", "treat", ".");
        res = sa.hasPrefix(patt);
        assertEquals(false, res);
        patt = List.of("<s>", "The", "brown", "dogs", "wept", "over", "the", "treat", ".", "</s>");
        res = sa.hasPrefix(patt);
        assertEquals(false, res);
        patt = List.of("The", "brown", "cat");
        res = sa.hasPrefix(patt);
        assertEquals(false, res);
    }

    @Test
    void suffixArrayNormaliseDist() {
        assertEquals(Map.of(), SuffixArray.normaliseDist(Map.of()));
        assertEquals(Map.of("fox", 0.25, "dog", 0.75),
            SuffixArray.normaliseDist(Map.of("fox", 1.0, "dog", 3.0)));
        Map<String, Double> rnd = new HashMap<>();
        rnd.put("fox", 1 + Math.random() * 999);
        rnd.put("dog", 1 + Math.random() * 999);
        Map<String, Double> res = SuffixArray.normaliseDist(rnd);
        assertEquals(1.0, sum(res), 0.0001);
        assertThrows(Exception.class, () -> SuffixArray.normaliseDist(null));
        assertThrows(Exception.class, () -> SuffixArray.normaliseDist(Map.of("a", -1.0)));
    }

    @Test
    void suffixArrayNormaliseDistFloats() {
        Map<String, Double> res = SuffixArray.normaliseDist(Map.of("fox", 0.5));
        assertEquals(1.0, res.get("fox"), 0.0001);

        res = SuffixArray.normaliseDist(Map.of("fox", 0.333333));
        assertEquals(1.0, res.get("fox"), 0.0001);

        res = SuffixArray.normaliseDist(Map.of("fox", 0.1, "dog", 0.3));
        assertEquals(0.25, res.get("fox"), 0.0001);
        assertEquals(0.75, res.get("dog"), 0.0001);

        Map<String, Double> rnd = new HashMap<>();
        rnd.put("fox", 0.1 + Math.random() * 0.999);
        rnd.put("dog", 0.1 + Math.random() * 0.999);
        res = SuffixArray.normaliseDist(rnd);
        assertEquals(1.0, sum(res), 0.0001);
    }

    @Test
    void suffixArrayToString() {
        SuffixArray sa;
        String expected;
        sa = new SuffixArray(List.of("b", "c", "a"));
        assertArrayEquals(new int[]{2, 0, 1}, sa.data);
        expected = "\n[\n  0: [a],\n  1: [b,c,a],\n  2: [c,a],\n]\n";
        assertEquals(expected, sa.toString());
        assertEquals(expected, sa.toString(Map.of("maxTokens", 3)));
        assertEquals(expected, sa.toString(Map.of("maxTokens", 2)));
        assertEquals(expected, sa.toString(Map.of("maxTokens", 1)));

        sa = new SuffixArray(List.of("b", "c", "ab", "a"));
        expected = "\n[\n  0: [a],\n  1: [ab,a],\n  2: [b,c,ab,a],\n  3: [c,ab,a],\n]\n";
        assertEquals(expected, sa.toString());

        sa = new SuffixArray(List.of("banana", "ananas"));
        expected = "\n[\n  0: [ananas],\n  1: [banana,ananas],\n]\n";
        assertEquals(expected, sa.toString());
    }

    // ---------------- helpers ----------------

    private static double sum(Map<String, Double> m) {
        double s = 0;
        for (double v : m.values()) {
            s += v;
        }
        return s;
    }

    private static void assertPrefixes(List<List<String>> tokens, List<String> patt) {
        for (List<String> t : tokens) {
            for (int i = 0; i < patt.size(); i++) {
                assertEquals(patt.get(i), t.get(i));
            }
        }
    }

    private static List<Integer> truthy(int[] seqmap) {
        List<Integer> out = new ArrayList<>();
        for (int v : seqmap) {
            if (v != 0) {
                out.add(v);
            }
        }
        return out;
    }

    private static void assertDeep(Object a, Object b, String msg) {
        if (a instanceof int[] && b instanceof int[]) {
            assertArrayEquals((int[]) a, (int[]) b, msg);
        } else if (a instanceof Object[] && b instanceof Object[]) {
            assertArrayEquals((Object[]) a, (Object[]) b, msg);
        } else {
            assertEquals(a, b, msg);
        }
    }

    private static Object fieldOf(Object o, String name) {
        for (Class<?> c = o.getClass(); c != null; c = c.getSuperclass()) {
            try {
                Field f = c.getDeclaredField(name);
                f.setAccessible(true);
                return f.get(o);
            } catch (NoSuchFieldException ignored) {
                // keep walking up the hierarchy
            } catch (IllegalAccessException e) {
                throw new RuntimeException(e);
            }
        }
        return null;
    }

    private static List<String> keysOf(Object o) {
        List<String> keys = new ArrayList<>();
        for (Class<?> c = o.getClass(); c != null; c = c.getSuperclass()) {
            for (Field f : c.getDeclaredFields()) {
                if (!Modifier.isStatic(f.getModifiers())) {
                    keys.add(f.getName());
                }
            }
        }
        Collections.sort(keys);
        return keys;
    }
}
