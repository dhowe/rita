package rita;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

/**
 * Ported from <code>js/test/lexicon-tests.js</code>.
 *
 * <p>Mapping notes:
 * <ul>
 *   <li>JS {@code await RiTa.search(...)} etc. are synchronous here (no await).</li>
 *   <li>JS regex literals passed as the pattern argument become the equivalent pattern string
 *       (the Java API takes an {@code Object} pattern).</li>
 *   <li>{@code expect(x).eql([...])} -> {@code assertEquals(List.of(...), x)}; {@code .to.be.true}
 *       -> {@code assertTrue}; {@code .to.be.false} -> {@code assertFalse}; {@code .gt(n)} ->
 *       {@code assertTrue(x > n)}.</li>
 *   <li>JS blocks disabled with {@code 0 && it(...)} are omitted entirely.</li>
 *   <li>The {@code typeof NOLEX !== 'undefined'} branches are dead when a lexicon is present and
 *       are omitted.</li>
 * </ul>
 */
class LexiconTest {

    @Test
    void shouldCallHasWord() {
        for (int i = 0; i < 10; i++) {
            assertTrue(RiTa.hasWord(RiTa.randomWord()));
        }
        assertTrue(RiTa.hasWord("random"));
        assertTrue(RiTa.hasWord("dog"));
        assertTrue(RiTa.hasWord("men"));
        assertTrue(RiTa.hasWord("happily"));
        assertTrue(RiTa.hasWord("play"));
        assertTrue(RiTa.hasWord("plays"));
        assertTrue(RiTa.hasWord("played"));
        assertTrue(RiTa.hasWord("written"));
        assertTrue(RiTa.hasWord("dogs"));
        assertTrue(RiTa.hasWord("oxen"));
        assertTrue(RiTa.hasWord("mice"));

        assertFalse(RiTa.hasWord("dogs", Map.of("noDerivations", true)));
        assertFalse(RiTa.hasWord("played", Map.of("noDerivations", true)));
        assertFalse(RiTa.hasWord("cats", Map.of("noDerivations", true)));

        // https://github.com/dhowe/rita/issues/139
        assertFalse(RiTa.hasWord("bunning"));
        assertFalse(RiTa.hasWord("coyes"));
        assertFalse(RiTa.hasWord("soes"));
        assertFalse(RiTa.hasWord("knews"));
        assertFalse(RiTa.hasWord("fastering"));
        assertFalse(RiTa.hasWord("loosering"));
        assertFalse(RiTa.hasWord("knews"));

        assertFalse(RiTa.hasWord("barkness"));
        assertFalse(RiTa.hasWord("horne"));
        assertFalse(RiTa.hasWord("haye"));

        // https://github.com/dhowe/rita/issues/177
        assertTrue(RiTa.hasWord("bites"));
        assertTrue(RiTa.hasWord("bit"));
        assertFalse(RiTa.hasWord("bitted"));

        assertTrue(RiTa.hasWord("breaks"));
        assertTrue(RiTa.hasWord("broke"));
        assertFalse(RiTa.hasWord("brokes"));
        assertFalse(RiTa.hasWord("broked"));

        assertTrue(RiTa.hasWord("concerned"));
        assertFalse(RiTa.hasWord("concerneded"));
        assertFalse(RiTa.hasWord("concerneds"));

        assertTrue(RiTa.hasWord("outpaced"));
        assertFalse(RiTa.hasWord("outpaceded"));
        assertFalse(RiTa.hasWord("outpaceds"));

        assertTrue(RiTa.hasWord("reported"));
        assertFalse(RiTa.hasWord("reporteds"));
        assertFalse(RiTa.hasWord("reporteded"));

        assertTrue(RiTa.hasWord("build"));
        assertTrue(RiTa.hasWord("built"));

        assertTrue(RiTa.hasWord("called"));
        assertFalse(RiTa.hasWord("calleds"));
        assertFalse(RiTa.hasWord("calleded"));

        assertTrue(RiTa.hasWord("commits"));
        assertTrue(RiTa.hasWord("committed"));
        assertFalse(RiTa.hasWord("committeds"));
        assertFalse(RiTa.hasWord("committeded"));

        assertTrue(RiTa.hasWord("computerized"));
        assertFalse(RiTa.hasWord("computerizeds"));
        assertFalse(RiTa.hasWord("computerizeded"));

        assertTrue(RiTa.hasWord("gets"));
        assertTrue(RiTa.hasWord("got"));
        assertFalse(RiTa.hasWord("gots"));
        assertTrue(RiTa.hasWord("gotten"));

        assertTrue(RiTa.hasWord("leads"));
        assertTrue(RiTa.hasWord("led"));
        assertFalse(RiTa.hasWord("leds"));

        assertTrue(RiTa.hasWord("oversaw"));
        assertTrue(RiTa.hasWord("overseen"));
        assertFalse(RiTa.hasWord("oversaws"));
        assertFalse(RiTa.hasWord("overseened"));

        assertTrue(RiTa.hasWord("remakes"));
        assertTrue(RiTa.hasWord("remade"));
        assertFalse(RiTa.hasWord("remaded"));

        assertTrue(RiTa.hasWord("discriminates"));
        assertTrue(RiTa.hasWord("discriminated"));
        assertFalse(RiTa.hasWord("discriminateds"));

        assertTrue(RiTa.hasWord("launched"));
        assertFalse(RiTa.hasWord("launcheds"));
        assertFalse(RiTa.hasWord("launcheded"));

        assertTrue(RiTa.hasWord("starts"));
        assertTrue(RiTa.hasWord("started"));
        assertFalse(RiTa.hasWord("starteds"));
    }

    @Test
    void shouldCallRandomWord() {
        String result = RiTa.randomWord();
        assertTrue(result.length() > 0, "randomWord: " + result);
        assertFalse(result.equals(RiTa.randomWord()), "randomWord returned same result '" + result + "'");

        result = RiTa.randomWord(Map.of("numSyllables", 3));
        assertTrue(result.length() > 0, "3 syllables: " + result);

        result = RiTa.randomWord(Map.of("numSyllables", 5));
        assertTrue(result.length() > 0, "5 syllables: " + result);
    }

    @Test
    void shouldNotMutateTheCallerOptionsObject() {
        // Regression: randomWord/search/rhymes previously wrote derived defaults onto the
        // options object passed in, so a reused literal accumulated state across calls.
        Map<String, Object> opts = new java.util.HashMap<>(Map.of("numSyllables", 2));
        RiTa.randomWord(opts);
        assertFalse(opts.containsKey("limit"), "randomWord leaked limit");
        assertFalse(opts.containsKey("shuffle"), "randomWord leaked shuffle");

        opts = new java.util.HashMap<>(Map.of("pos", "nn"));
        RiTa.searchSync("^a", opts);
        assertFalse(opts.containsKey("targetPos"), "search leaked targetPos");
        assertFalse(opts.containsKey("minDistance"), "search leaked minDistance");

        opts = new java.util.HashMap<>(Map.of("limit", 5));
        RiTa.rhymesSync("cat", opts);
        assertFalse(opts.containsKey("maxLength"), "rhymes leaked maxLength");
    }

    @Test
    void shouldCallRandomWordWithRegex() {
        // regex string as first parameter
        String result = RiTa.randomWord("^a");
        assertTrue(result.startsWith("a"));
        assertTrue(result.length() > 3);

        result = RiTa.randomWord("^apple$");
        assertEquals("apple", result);

        result = RiTa.randomWord("le");
        assertTrue(result.contains("le"));

        List<String> results = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            results.add(RiTa.randomWord("^a"));
        }
        assertEquals(10, results.size());

        int i = 0;
        while (i < results.size() - 1) {
            if (results.get(i).equals(results.get(i + 1))) {
                results.remove(i);
            } else {
                i++;
            }
        }
        // 10 words not the same
        assertTrue(results.size() > 1);

        // regex object as first parameter (pattern string in Java)
        result = RiTa.randomWord("^a");
        assertTrue(result.startsWith("a"));
        assertTrue(result.length() > 3);

        result = RiTa.randomWord("^apple$");
        assertEquals("apple", result);

        result = RiTa.randomWord("le");
        assertTrue(result.contains("le"));

        result = RiTa.randomWord("^a");
        assertTrue(result.startsWith("a"));

        results = new ArrayList<>();
        for (int j = 0; j < 10; j++) {
            results.add(RiTa.randomWord("^a"));
        }
        assertEquals(10, results.size());
    }

    @Test
    void shouldCallRandomWordWithStressRegex() {
        String result = RiTa.randomWord("0/1/0", Map.of("type", "stresses"));
        assertTrue(result.length() > 3);
        assertTrue(RiTa.analyze(result).stresses.contains("0/1/0"));

        result = RiTa.randomWord("^0/1/0$", Map.of("type", "stresses"));
        assertEquals("0/1/0", RiTa.analyze(result).stresses);

        result = RiTa.randomWord("010", Map.of("type", "stresses"));
        assertTrue(RiTa.analyze(result).stresses.contains("0/1/0"));

        result = RiTa.randomWord("^010$", Map.of("type", "stresses"));
        assertEquals("0/1/0", RiTa.analyze(result).stresses);

        result = RiTa.randomWord("0/1/0", Map.of("type", "stresses"));
        assertTrue(RiTa.analyze(result).stresses.contains("0/1/0"));

        result = RiTa.randomWord("^0/1/0/0$", Map.of("type", "stresses"));
        assertEquals("0/1/0/0", RiTa.analyze(result).stresses);
    }

    @Test
    void shouldCallRandomWordWithPhonesRegex() {
        String result = RiTa.randomWord("^th", Map.of("type", "phones"));
        assertTrue(result.length() > 3);
        assertTrue(RiTa.analyze(result).phones.startsWith("th"));

        result = RiTa.randomWord("v$", Map.of("type", "phones"));
        assertTrue(RiTa.analyze(result).phones.endsWith("v"));

        result = RiTa.randomWord("^b-ih-l-iy-v$", Map.of("type", "phones"));
        assertEquals("believe", result);

        result = RiTa.randomWord("ae", Map.of("type", "phones"));
        assertTrue(RiTa.analyze(result).phones.contains("ae"));

        result = RiTa.randomWord("^th", Map.of("type", "phones"));
        assertTrue(result.length() > 3);
        assertTrue(RiTa.analyze(result).phones.startsWith("th"));

        result = RiTa.randomWord("v$", Map.of("type", "phones"));
        assertTrue(RiTa.analyze(result).phones.endsWith("v"));

        result = RiTa.randomWord("^b-ih-l-iy-v$", Map.of("type", "phones"));
        assertEquals("believe", result);

        result = RiTa.randomWord("ae", Map.of("type", "phones"));
        assertTrue(RiTa.analyze(result).phones.contains("ae"));
    }

    @Test
    void shouldCallRandomWordWithOptsRegex() {
        // as one of the field in opts
        String result = RiTa.randomWord(Map.of("regex", "^a"));
        assertTrue(result.startsWith("a"));
        assertTrue(result.length() > 3);

        result = RiTa.randomWord(Map.of("regex", "^a"));
        assertTrue(result.startsWith("a"));
        assertTrue(result.length() > 3);

        result = RiTa.randomWord(Map.of("regex", "0/1/0", "type", "stresses"));
        assertTrue(result.length() > 3);
        assertTrue(RiTa.analyze(result).stresses.contains("0/1/0"));

        result = RiTa.randomWord(Map.of("regex", "0/1/0", "type", "stresses"));
        assertTrue(RiTa.analyze(result).stresses.contains("0/1/0"));

        result = RiTa.randomWord(Map.of("regex", "^th", "type", "phones"));
        assertTrue(result.length() > 3);
        assertTrue(RiTa.analyze(result).phones.startsWith("th"));

        result = RiTa.randomWord(Map.of("regex", "^th", "type", "phones"));
        assertTrue(result.length() > 3);
        assertTrue(RiTa.analyze(result).phones.startsWith("th"));
    }

    @Test
    void shouldHandleAnAugmentedLexicon() {
        Map<String, Object> toAdd = new java.util.LinkedHashMap<>();
        toAdd.put("deg", List.of("d-eh1-g", "nn"));
        toAdd.put("wadly", List.of("w-ae1-d l-iy", "rb"));
        Lexicon lex = RiTa.lexicon;
        for (String w : toAdd.keySet()) {
            RiTa.lexicon.data.put(w, toAdd.get(w));
        }
        assertTrue(lex.hasWord("run"));
        assertTrue(lex.hasWord("walk"));
        assertTrue(lex.hasWord("deg"));
        assertTrue(lex.hasWord("wadly"));
        assertTrue(lex.isAlliteration("wadly", "welcome"));
        for (String w : toAdd.keySet()) {
            RiTa.lexicon.data.remove(w);
        }
    }

    @Test
    void shouldHandleACustomLexicon() {
        Lexicon lex = RiTa.lexicon;
        Map<String, Object> orig = lex.data;
        Map<String, Object> custom = new java.util.LinkedHashMap<>();
        custom.put("dog", List.of("d-ao1-g", "nn"));
        custom.put("cat", List.of("k-ae1-t", "nn"));
        custom.put("happily", List.of("hh-ae1 p-ah l-iy", "rb"));
        custom.put("walk", List.of("w-ao1-k", "vb vbp nn"));
        custom.put("welcome", List.of("w-eh1-l k-ah-m", "jj nn vb vbp"));
        custom.put("sadly", List.of("s-ae1-d l-iy", "rb"));
        lex.data = custom;

        assertFalse(lex.hasWord("run"));
        assertTrue(lex.hasWord("walk"));
        assertTrue(lex.isAlliteration("walk", "welcome"));
        lex.data = orig;
    }

    @Test
    void shouldCallRandomWordWithPos() {
        assertThrows(Exception.class, () -> RiTa.randomWord(Map.of("pos", "xxx")));

        String result;
        String[] pos = {"nn", "jj", "jjr", "wp"};
        for (String p : pos) {
            result = RiTa.randomWord(Map.of("pos", p));
            String best = RiTa.tagger.allTags(result).get(0);
            assertEquals(p, best, result);
        }

        for (int i = 0; i < 5; i++) {
            result = RiTa.randomWord(Map.of("pos", "nns"));
            if (!RiTa.inflector.isPlural(result)) {
                // For now, just warn here as there are too many edge cases (see #521)
                System.err.println("Pluralize/Singularize problem: randomWord(nns) was '" + result
                    + "' (isPlural=" + RiTa.inflector.isPlural(result) + "), singularized is '"
                    + RiTa.singularize(result) + "'");
            }
            // TODO: occasional problem here, examples: beaux

            // No nn & vbg, No -ness, -ism
            String posData = RiTa.lexicon._posData(result);
            assertTrue(posData == null || !posData.contains("vbg"), "randomWord nns: " + result);
            assertTrue(!result.endsWith("ness"), "randomWord nns: " + result);
            assertTrue(!result.endsWith("isms"), "randomWord nns: " + result);
        }

        result = RiTa.randomWord(Map.of("pos", "v"));
        assertTrue(result.length() > 0, "randomWord v=" + result);

        result = RiTa.randomWord(Map.of("pos", "nn"));
        assertTrue(result.length() > 0, "randomWord nn: " + result);

        result = RiTa.randomWord(Map.of("pos", "nns"));
        assertTrue(result.length() > 0, "randomWord nns=" + result);

        result = RiTa.randomWord(Map.of("pos", "n"));
        assertTrue(result.length() > 0, "randomWord n=" + result);

        result = RiTa.randomWord(Map.of("pos", "v"));
        assertTrue(result.length() > 0, "randomWord v=" + result);

        result = RiTa.randomWord(Map.of("pos", "rp"));
        assertTrue(result.length() > 0, "randomWord rp=" + result);

        List<String> results = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            results.add(RiTa.randomWord(Map.of("pos", "nns")));
            assertTrue(results.get(results.size() - 1) instanceof String);
        }

        assertEquals(10, results.size());

        int i = 0;
        while (i < results.size() - 1) {
            if (results.get(i).equals(results.get(i + 1))) {
                results.remove(i);
            } else {
                i++;
            }
        }
        assertTrue(results.size() > 1); // 10 words not the same
    }

    @Test
    void shouldCallRandomWordWithSyllables() {
        String result = RiTa.randomWord(Map.of("numSyllables", 3));
        String syllables = RiTa.syllables(result);
        int num = syllables.split(RiTa.SYLLABLE_BOUNDARY).length;
        assertTrue(result.length() > 0, "failed1 on: " + result);
        assertEquals(3, num, result + ": " + syllables); // "3 syllables: "

        result = RiTa.randomWord(Map.of("numSyllables", 5));
        syllables = RiTa.syllables(result);
        num = syllables.split(RiTa.SYLLABLE_BOUNDARY).length;
        assertTrue(result.length() > 0, "failed2 on " + result);
        assertEquals(5, num, result + ": " + syllables); // "5 syllables: "
    }

    @Test
    void shouldCallSearchWithoutRegex() {
        assertTrue(RiTa.search().length > 20000); // all words
        assertEquals(11, RiTa.search(Map.of("limit", 11)).length);

        assertEquals(List.of("abalone", "abandonment", "abbey", "abbot", "abbreviation", "abdomen",
            "abduction", "aberration", "ability", "abnormality"),
            Arrays.asList(RiTa.search(Map.of("pos", "n"))));

        assertEquals(List.of("abashed", "abate", "abbey", "abbot", "abduct", "abet", "abhor",
            "abide", "abject", "ablaze"),
            Arrays.asList(RiTa.search(Map.of("numSyllables", 2))));

        assertEquals(List.of("abbey", "abbot", "abode", "abscess", "absence", "abstract", "abuse",
            "abyss", "accent", "access"),
            Arrays.asList(RiTa.search(Map.of("numSyllables", 2, "pos", "n"))));

        assertEquals(List.of("ace", "ache", "act", "age", "aid", "aide", "aim", "air", "aisle", "ale"),
            Arrays.asList(RiTa.search(Map.of("numSyllables", 1, "pos", "n"))));

        List<String> search = Arrays.asList(RiTa.search(Map.of("pos", "vb", "limit", -1)));
        assertFalse(search.contains("concerned"));
        assertFalse(search.contains("committed"));
        assertFalse(search.contains("called"));
        assertFalse(search.contains("computerized"));

        search = Arrays.asList(RiTa.search(Map.of("pos", "vbd", "limit", -1)));
        assertTrue(search.contains("concerned"));
        assertTrue(search.contains("committed"));
        assertTrue(search.contains("called"));
        assertTrue(search.contains("computerized"));
        // JS: 0 && expect(search.includes("conclude")) — disabled.

        search = Arrays.asList(RiTa.search(Map.of("pos", "vbn", "limit", -1)));
        assertTrue(search.contains("concerned"));
        assertTrue(search.contains("committed"));
        assertTrue(search.contains("called"));
        assertTrue(search.contains("computerized"));
        // JS: 0 && expect(search.includes("conclude")) — disabled.
    }

    @Test
    void shouldCallSearchWithLetters() {
        List<String> expected = List.of("elephant", "elephantine", "phantom", "sycophantic",
            "triumphant", "triumphantly");
        assertEquals(expected, Arrays.asList(RiTa.search("phant")));
        assertEquals(expected, Arrays.asList(RiTa.search("phant")));
        assertEquals(expected, Arrays.asList(RiTa.search(Map.of("regex", "phant"))));
        assertEquals(expected, Arrays.asList(RiTa.search(Map.of("regex", "phant"))));
    }

    @Test
    void shouldCallSearchWithPhonesLimit() {
        // omitting no limit tests as they are a bit slow
        List<String> result = Arrays.asList(RiTa.search("f-a[eh]-n-t", Map.of("type", "phones", "limit", 10)));
        assertEquals(List.of("elephant", "elephantine", "fantasia", "fantasize", "fantastic",
            "fantastically", "fantasy", "infant", "infantile", "infantry"), result);

        result = Arrays.asList(RiTa.search("f-ah-n-t", Map.of("type", "phones", "limit", 5)));
        assertEquals(List.of("elephant", "infant", "infantile", "infantry", "oftentimes"), result);

        // regex in options
        result = Arrays.asList(RiTa.search(Map.of("regex", "f-a[eh]-n-t", "type", "phones", "limit", 10)));
        assertEquals(List.of("elephant", "elephantine", "fantasia", "fantasize", "fantastic",
            "fantastically", "fantasy", "infant", "infantile", "infantry"), result);
    }

    @Test
    void shouldCallSearchWithPhonesNoLimitAndShuffle() {
        List<String> result = Arrays.asList(RiTa.search(Map.of("regex", "f-ah-n-t", "type", "phones", "limit", -1)));
        assertEquals(List.of("elephant", "infant", "infantile", "infantry", "oftentimes",
            "triumphant", "triumphantly"), result);

        List<String> result2 = new ArrayList<>(Arrays.asList(RiTa.search(Map.of("regex", "f-ah-n-t", "type", "phones", "limit", -1, "shuffle", true))));
        Collections.sort(result2);
        assertEquals(result, result2);
    }

    @Test
    void shouldCallSearchWithPosPhonesSyllsLimit() {
        List<String> res = Arrays.asList(RiTa.search("f-ah-n-t", Map.of("type", "phones", "pos", "n", "limit", 3, "numSyllables", 2)));
        assertEquals(List.of("infant"), res);
    }

    @Test
    void shouldCallSearchWithPosPhonesLimit() {
        List<String> res = Arrays.asList(RiTa.search("f-ah-n-t", Map.of("type", "phones", "pos", "n", "limit", 3)));
        assertEquals(List.of("elephant", "infant", "infantry"), res);

        res = Arrays.asList(RiTa.search("f-a[eh]-n-t", Map.of("type", "phones", "pos", "v", "limit", 5)));
        assertEquals(List.of("fantasize"), res);
    }

    @Test
    void shouldCallSearchWithPosRegex() {
        List<String> res = Arrays.asList(RiTa.search("cares$", Map.of("pos", "nns", "limit", -1)));
        assertEquals(List.of("cares", "scares"), res);

        res = Arrays.asList(RiTa.search("^rice$", Map.of("pos", "nns", "limit", -1)));
        assertEquals(List.of("rice"), res);
    }

    @Test
    void shouldCallSearchWithPosLetters() {
        List<String> res = Arrays.asList(RiTa.search("cause", Map.of("pos", "nns")));
        assertEquals(List.of("causes", "causeways"), res);

        // https://github.com/dhowe/rita/issues/177
        res = Arrays.asList(RiTa.search("gain", Map.of("pos", "vbd", "numSyllables", 1)));
        assertEquals(List.of("gained"), res);
        res = Arrays.asList(RiTa.search("end", Map.of("pos", "vbd", "minLength", 2, "limit", -1)));
        assertTrue(res.contains("ended"));
        res = Arrays.asList(RiTa.search("commit", Map.of("pos", "vbd")));
        assertTrue(res.contains("committed"));
        res = Arrays.asList(RiTa.search("involve", Map.of("pos", "vbd")));
        assertTrue(res.contains("involved"));
        res = Arrays.asList(RiTa.search("outpace", Map.of("pos", "vbn")));
        assertEquals(List.of("outpaced"), res);
        res = Arrays.asList(RiTa.search("paid", Map.of("pos", "vbd")));
        assertTrue(res.contains("prepaid"));
        res = Arrays.asList(RiTa.search("made", Map.of("pos", "vbd")));
        assertTrue(res.contains("remade"));
        res = Arrays.asList(RiTa.search("re", Map.of("pos", "vbd", "limit", -1)));
        assertTrue(res.contains("reopened"));
        assertTrue(res.contains("resold"));
    }

    @Test
    void shouldCallSearchWithSimplePosPhonesLimit() {
        assertEquals(List.of("fantasize"),
            Arrays.asList(RiTa.search("f-a[eh]-n-t", Map.of("type", "phones", "pos", "vb", "limit", 5))));
        assertEquals(List.of("elephants", "infants", "infantries"),
            Arrays.asList(RiTa.search("f-ah-n-t", Map.of("type", "phones", "pos", "nns", "limit", 3))));
    }

    @Test
    void shouldCallSearchWithPosStressLimit() {
        assertEquals(List.of("abalone", "abandonment", "abbreviation", "abdomen", "abduction"),
            Arrays.asList(RiTa.search("010", Map.of("type", "stresses", "limit", 5, "pos", "n"))));

        assertEquals(List.of("abdomen", "abduction", "abortion", "abruptness", "absorber"),
            Arrays.asList(RiTa.search("010", Map.of("type", "stresses", "limit", 5, "pos", "n", "numSyllables", 3))));

        assertEquals(List.of("abalone", "abandonments", "abbreviations", "abductions", "abilities"),
            Arrays.asList(RiTa.search("010", Map.of("type", "stresses", "limit", 5, "pos", "nns"))));

        assertEquals(List.of("abalone", "abandonments", "abbreviations", "abductions", "abilities"),
            Arrays.asList(RiTa.search("0/1/0", Map.of("type", "stresses", "limit", 5, "pos", "nns"))));

        assertEquals(List.of("abductions", "abortions", "absorbers", "abstentions", "abstractions"),
            Arrays.asList(RiTa.search("010", Map.of("type", "stresses", "limit", 5, "pos", "nns", "numSyllables", 3))));
    }

    @Test
    void shouldCallSearchWithStressesLimit() {
        assertEquals(List.of("accountability", "anticipatory", "appreciatively", "authoritarianism", "colonialism"),
            Arrays.asList(RiTa.search("010000", Map.of("type", "stresses", "limit", 5))));

        assertEquals(List.of("colonialism", "imperialism", "materialism"),
            Arrays.asList(RiTa.search("010000", Map.of("type", "stresses", "limit", 5, "maxLength", 11))));
        assertEquals(List.of("accountability", "anticipatory", "appreciatively", "authoritarianism", "conciliatory"),
            Arrays.asList(RiTa.search("010000", Map.of("type", "stresses", "limit", 5, "minLength", 12))));
        assertEquals(List.of("accountability", "anticipatory", "appreciatively", "authoritarianism", "colonialism"),
            Arrays.asList(RiTa.search("0/1/0/0/0/0", Map.of("type", "stresses", "limit", 5))));
        assertEquals(List.of("accountability", "anticipatory", "appreciatively", "authoritarianism", "colonialism"),
            Arrays.asList(RiTa.search(Map.of("regex", "010000", "type", "stresses", "limit", 5))));

        assertEquals(List.of("colonialism", "imperialism", "materialism"),
            Arrays.asList(RiTa.search(Map.of("regex", "010000", "type", "stresses", "limit", 5, "maxLength", 11))));
        assertEquals(List.of("accountability", "anticipatory", "appreciatively", "authoritarianism", "conciliatory"),
            Arrays.asList(RiTa.search(Map.of("regex", "010000", "type", "stresses", "limit", 5, "minLength", 12))));
        assertEquals(List.of("accountability", "anticipatory", "appreciatively", "authoritarianism", "colonialism"),
            Arrays.asList(RiTa.search(Map.of("regex", "0/1/0/0/0/0", "type", "stresses", "limit", 5))));
    }

    @Test
    void shouldCallSearchWithStressRegexLimit() {
        assertEquals(List.of("accountability", "anticipatory", "appreciatively", "authoritarianism", "colonialism"),
            Arrays.asList(RiTa.search("0/1/0/0/0/0", Map.of("type", "stresses", "limit", 5))));

        // regex in options
        assertEquals(List.of("accountability", "anticipatory", "appreciatively", "authoritarianism", "colonialism"),
            Arrays.asList(RiTa.search(Map.of("regex", "0/1/0/0/0/0", "type", "stresses", "limit", 5))));
    }

    @Test
    void shouldCallRandomWordPosSyls() {
        String result;
        String syllables;

        result = RiTa.randomWord(Map.of("numSyllables", 3, "pos", "vbz"));
        assertTrue(result.length() > 0, "randomWord vbz: " + result);
        syllables = RiTa.syllables(result);
        assertEquals(3, syllables.split(RiTa.SYLLABLE_BOUNDARY).length, "GOT: " + result + " (" + syllables + ")");
        assertEquals(true, RiTa.isVerb(result), fail(result, "vbz"));

        result = RiTa.randomWord(Map.of("numSyllables", 1, "pos", "n"));
        assertTrue(result.length() > 0, "randomWord n: " + result);
        syllables = RiTa.syllables(result);
        assertEquals(1, syllables.split(RiTa.SYLLABLE_BOUNDARY).length, "GOT: " + result + " (" + syllables + ")");
        assertEquals(true, RiTa.isNoun(result), fail(result, "n"));

        result = RiTa.randomWord(Map.of("numSyllables", 1, "pos", "nns"));
        assertTrue(result.length() > 0, "randomWord nns: " + result);
        syllables = RiTa.syllables(result);
        assertEquals(1, syllables.split(RiTa.SYLLABLE_BOUNDARY).length, "GOT: " + result + " (" + syllables + ")");
        assertEquals(true, RiTa.isNoun(result), fail(result, "nns"));
        // TODO: ? still failing occasionally on: proves, torpedoes, strives, times, etc. ?

        result = RiTa.randomWord(Map.of("numSyllables", 5, "pos", "nns"));
        assertTrue(result.length() > 0, "randomWord nns: " + result);
        syllables = RiTa.syllables(result);
        int count = syllables.split(RiTa.SYLLABLE_BOUNDARY).length;
        if (count != 5) {
            System.err.println("Syllabifier problem: " + result + ".syllables was " + count + ", expected 5");
        }
        assertEquals(true, RiTa.isNoun(result), fail(result, "nns"));
    }

    @Test
    void shouldCallAlliterationsNumSyllables() {
        List<String> result = Arrays.asList(RiTa.alliterations("cat", Map.of("minLength", 1, "numSyllables", 7)));
        assertEquals(List.of("electrocardiogram", "electromechanical", "telecommunications"), result);
        for (String r : result) {
            assertTrue(RiTa.isAlliteration(r, "cat"), "FAIL2: " + r);
        }
    }

    @Test
    void shouldCallAlliterationsPos() {
        List<String> res;

        res = Arrays.asList(RiTa.alliterations("cat", Map.of("numSyllables", 7, "pos", "n")));
        assertEquals(List.of("electrocardiogram", "telecommunications"), res);
        for (String r : res) {
            assertTrue(RiTa.isAlliteration(r, "cat"), "FAIL2: " + r);
        }

        res = Arrays.asList(RiTa.alliterations("cat", Map.of("minLength", 14, "pos", "v")));
        for (String r : res) {
            assertTrue(r.length() >= 14);
        }
        assertEquals(List.of("counterbalance"), res);

        res = Arrays.asList(RiTa.alliterations("dog", Map.of("minLength", 13, "pos", "rb", "limit", 11)));
        for (String r : res) {
            assertTrue(r.length() >= 13);
        }
        assertEquals(List.of("coincidentally", "conditionally", "confidentially", "contradictorily",
            "devastatingly", "expeditiously", "paradoxically", "predominantly", "traditionally",
            "unconditionally", "unpredictably"), res);

        res = Arrays.asList(RiTa.alliterations("freedom", Map.of("minLength", 14, "pos", "nns")));
        for (String r : res) {
            assertTrue(r.length() >= 14);
        }
        assertEquals(List.of("featherbeddings", "fundamentalists", "pharmaceuticals",
            "photosyntheses", "reconfigurations", "sophistications"), res);
    }

    @Test
    void shouldCallAlliterations() {
        List<String> result;

        result = Arrays.asList(RiTa.alliterations("", Map.of("silent", 1)));
        assertTrue(result.size() < 1);

        result = Arrays.asList(RiTa.alliterations("#$%^&*", Map.of("silent", 1)));
        assertTrue(result.size() < 1);

        result = Arrays.asList(RiTa.alliterations("umbrella", Map.of("silent", 1)));
        assertTrue(result.size() < 1, "failed on 'umbrella'");

        result = Arrays.asList(RiTa.alliterations("cat", Map.of("limit", 100)));
        assertEquals(100, result.size(), "failed on 'cat'");
        assertFalse(result.contains("cat"));
        for (String r : result) {
            assertTrue(RiTa.isAlliteration(r, "cat"));
        }

        result = Arrays.asList(RiTa.alliterations("dog", Map.of("limit", 100)));
        assertFalse(result.contains("dog"));
        assertEquals(100, result.size(), "failed on 'dog'");
        for (String r : result) {
            assertTrue(RiTa.isAlliteration(r, "dog"));
        }

        result = Arrays.asList(RiTa.alliterations("dog", Map.of("minLength", 15)));
        assertTrue(result.size() > 0 && result.size() < 5, "got length=" + result.size());
        for (String r : result) {
            assertTrue(RiTa.isAlliteration(r, "dog"), "FAIL1: " + r);
        }

        result = Arrays.asList(RiTa.alliterations("cat", Map.of("minLength", 16)));
        assertTrue(result.size() > 0 && result.size() < 15, "failed on 'cat'");
        for (String r : result) {
            assertTrue(RiTa.isAlliteration(r, "cat"), "FAIL2: " + r);
        }

        result = Arrays.asList(RiTa.alliterations("khatt", Map.of("minLength", 16)));
        assertTrue(result.size() > 0 && result.size() < 15, "failed on 'khatt'");
        for (String r : result) {
            assertTrue(RiTa.isAlliteration(r, "cat"), "FAIL2: " + r);
        }

        // for one letter words should return []
        assertEquals(List.of(), Arrays.asList(RiTa.alliterations("a", Map.of())));
        assertEquals(List.of(), Arrays.asList(RiTa.alliterations("I", Map.of())));
        assertEquals(List.of(), Arrays.asList(RiTa.alliterations("K", Map.of())));
    }

    @Test
    void shouldCallRhymesSync() {
        assertEquals(List.of("cog"), RiTa.lexicon.rhymesSync("dog", Map.of("limit", 1)));
        assertEquals(List.of("cog", "log"), RiTa.lexicon.rhymesSync("dog", Map.of("limit", 2)));
        assertEquals(List.of("cog", "log"), RiTa.lexicon.rhymesSync("dog", Map.of())); // TODO: should be more ?
    }

    @Test
    void shouldCallRhymes() {
        assertEquals(10, Arrays.asList(RiTa.rhymes("cat", Map.of())).size());
        assertTrue(Arrays.asList(RiTa.rhymes("cat", Map.of())).contains("hat"));
        assertTrue(Arrays.asList(RiTa.rhymes("yellow", Map.of())).contains("mellow"));
        assertTrue(Arrays.asList(RiTa.rhymes("toy", Map.of())).contains("boy"));
        assertTrue(Arrays.asList(RiTa.rhymes("crab", Map.of())).contains("drab"));

        assertTrue(Arrays.asList(RiTa.rhymes("mouse", Map.of())).contains("house"));
        assertFalse(Arrays.asList(RiTa.rhymes("apple", Map.of())).contains("polo"));
        assertFalse(Arrays.asList(RiTa.rhymes("this", Map.of())).contains("these"));

        assertFalse(Arrays.asList(RiTa.rhymes("hose", Map.of())).contains("house"));
        assertFalse(Arrays.asList(RiTa.rhymes("sieve", Map.of())).contains("mellow"));
        assertFalse(Arrays.asList(RiTa.rhymes("swag", Map.of())).contains("grab"));

        assertTrue(Arrays.asList(RiTa.rhymes("weight", Map.of("limit", 1000))).contains("eight"));
        assertTrue(Arrays.asList(RiTa.rhymes("eight", Map.of("limit", 1000))).contains("weight"));
        assertTrue(Arrays.asList(RiTa.rhymes("sieve", Map.of("limit", 1000))).contains("give"));
        assertTrue(Arrays.asList(RiTa.rhymes("shore", Map.of("limit", 1000))).contains("more"));
        assertTrue(Arrays.asList(RiTa.rhymes("tense", Map.of("limit", 1000))).contains("sense"));

        assertTrue(Arrays.asList(RiTa.rhymes("bog", Map.of())).contains("fog"));
        assertTrue(Arrays.asList(RiTa.rhymes("dog", Map.of())).contains("log"));

        // for single letter word return []
        assertEquals(List.of(), Arrays.asList(RiTa.rhymes("a", Map.of())));
        assertEquals(List.of(), Arrays.asList(RiTa.rhymes("I", Map.of())));
        assertEquals(List.of(), Arrays.asList(RiTa.rhymes("Z", Map.of())));
        assertEquals(List.of(), Arrays.asList(RiTa.rhymes("B", Map.of())));
        assertEquals(List.of(), Arrays.asList(RiTa.rhymes("K", Map.of())));
    }

    @Test
    void shouldCallRhymesPos() {
        assertFalse(Arrays.asList(RiTa.rhymes("cat", Map.of("pos", "v"))).contains("hat"));
        assertTrue(Arrays.asList(RiTa.rhymes("yellow", Map.of("pos", "a"))).contains("mellow"));
        assertTrue(Arrays.asList(RiTa.rhymes("toy", Map.of("pos", "n"))).contains("boy"));
        assertFalse(Arrays.asList(RiTa.rhymes("sieve", Map.of("pos", "n"))).contains("give"));

        assertTrue(Arrays.asList(RiTa.rhymes("tense", Map.of("pos", "v"))).contains("condense"));
        assertFalse(Arrays.asList(RiTa.rhymes("crab", Map.of("pos", "n"))).contains("drab"));
        assertFalse(Arrays.asList(RiTa.rhymes("shore", Map.of("pos", "v"))).contains("more"));

        assertTrue(Arrays.asList(RiTa.rhymes("mouse", Map.of("pos", "nn"))).contains("house"));

        assertFalse(Arrays.asList(RiTa.rhymes("weight", Map.of("pos", "vb"))).contains("eight"));
        assertTrue(Arrays.asList(RiTa.rhymes("eight", Map.of("pos", "nn", "limit", 1000))).contains("weight"));

        assertFalse(Arrays.asList(RiTa.rhymes("apple", Map.of("pos", "v"))).contains("polo"));
        assertFalse(Arrays.asList(RiTa.rhymes("this", Map.of("pos", "v"))).contains("these"));

        assertFalse(Arrays.asList(RiTa.rhymes("hose", Map.of("pos", "v"))).contains("house"));
        assertFalse(Arrays.asList(RiTa.rhymes("sieve", Map.of("pos", "v"))).contains("mellow"));
        assertFalse(Arrays.asList(RiTa.rhymes("swag", Map.of("pos", "v"))).contains("grab"));

        // https://github.com/dhowe/rita/issues/177
        List<String> rhyme = Arrays.asList(RiTa.rhymes("spreads", Map.of("pos", "vbz", "limit", 1000)));
        assertFalse(rhyme.contains("discriminateds"));
        assertFalse(rhyme.contains("endeds"));
        assertFalse(rhyme.contains("finisheds"));
        assertFalse(rhyme.contains("reporteds"));
        assertFalse(rhyme.contains("proliferateds"));
        assertFalse(rhyme.contains("outpaceds"));
        assertFalse(rhyme.contains("liveds"));
        assertFalse(Arrays.asList(RiTa.rhymes("hit", Map.of("pos", "vb"))).contains("bit"));
        assertTrue(Arrays.asList(RiTa.rhymes("hit", Map.of("pos", "vbd"))).contains("bit"));
        assertFalse(Arrays.asList(RiTa.rhymes("stroke", Map.of("pos", "vb"))).contains("broke"));
        assertTrue(Arrays.asList(RiTa.rhymes("stroke", Map.of("pos", "vbd"))).contains("broke"));
        assertFalse(Arrays.asList(RiTa.rhymes("evolved", Map.of("pos", "vb"))).contains("involved"));
        assertTrue(Arrays.asList(RiTa.rhymes("evolved", Map.of("pos", "vbd"))).contains("involved"));
    }

    @Test
    void shouldCallRhymesPosNid() {
        // special case, where word is not in dictionary
        List<String> rhymes = Arrays.asList(RiTa.rhymes("abated", Map.of("pos", "vbd", "limit", 1000)));
        assertTrue(rhymes.contains("allocated"));
        assertTrue(rhymes.contains("annihilated"));
        assertFalse(rhymes.contains("condensed"));
    }

    @Test
    void shouldCallRhymesNumSyllables() {
        assertTrue(Arrays.asList(RiTa.rhymes("cat", Map.of("numSyllables", 1))).contains("hat"));
        assertFalse(Arrays.asList(RiTa.rhymes("cat", Map.of("numSyllables", 2))).contains("hat"));
        assertFalse(Arrays.asList(RiTa.rhymes("cat", Map.of("numSyllables", 3))).contains("hat"));

        assertTrue(Arrays.asList(RiTa.rhymes("yellow", Map.of("numSyllables", 2))).contains("mellow"));
        assertFalse(Arrays.asList(RiTa.rhymes("yellow", Map.of("numSyllables", 3))).contains("mellow"));

        // special case, where word is not in dictionary
        List<String> rhymes = Arrays.asList(RiTa.rhymes("abated", Map.of("numSyllables", 3)));
        assertTrue(rhymes.contains("elated"));
        assertFalse(rhymes.contains("abated"));
        assertFalse(rhymes.contains("allocated"));
        assertFalse(rhymes.contains("condensed"));
    }

    @Test
    void shouldCallRhymesWordLength() {
        assertFalse(Arrays.asList(RiTa.rhymes("cat", Map.of("minLength", 4))).contains("hat"));
        assertFalse(Arrays.asList(RiTa.rhymes("cat", Map.of("maxLength", 2))).contains("hat"));

        // special case, where word is not in dictionary
        List<String> rhymes = Arrays.asList(RiTa.rhymes("abated", Map.of("pos", "vbd", "maxLength", 9)));
        assertTrue(rhymes.contains("allocated"));
        assertFalse(rhymes.contains("annihilated"));
        assertFalse(rhymes.contains("condensed"));
    }

    @Test
    void shouldCallSpellsLike() {
        List<String> result;

        result = Arrays.asList(RiTa.spellsLike("", Map.of()));
        assertEquals(List.of(), result);

        result = Arrays.asList(RiTa.spellsLike("banana", Map.of()));
        assertEquals(List.of("banal", "bonanza", "cabana", "manna"), result);

        result = Arrays.asList(RiTa.spellsLike("tornado", Map.of()));
        assertEquals(List.of("torpedo"), result);

        result = Arrays.asList(RiTa.spellsLike("ice", Map.of()));
        assertEquals(List.of("ace", "dice", "iced", "icy", "ire", "lice", "nice", "rice", "vice"), result);
    }

    @Test
    void shouldCallSpellsLikeOptions() {
        List<String> result;

        result = Arrays.asList(RiTa.spellsLike("banana", Map.of("minLength", 6, "maxLength", 6)));
        assertEquals(List.of("cabana"), result);

        result = Arrays.asList(RiTa.spellsLike("banana", Map.of("minLength", 6, "maxLength", 6)));
        assertEquals(List.of("cabana"), result);

        result = Arrays.asList(RiTa.spellsLike("banana", Map.of("minDistance", 1)));
        assertEquals(List.of("banal", "bonanza", "cabana", "manna"), result);

        result = Arrays.asList(RiTa.spellsLike("ice", Map.of("maxLength", 3)));
        assertEquals(List.of("ace", "icy", "ire"), result);

        result = Arrays.asList(RiTa.spellsLike("ice", Map.of("minDistance", 2, "minLength", 3, "maxLength", 3, "limit", 1000)));
        for (String r : result) {
            assertEquals(3, r.length());
        }
        assertTrue(result.size() > 10);

        result = Arrays.asList(RiTa.spellsLike("ice", Map.of("minDistance", 0, "minLength", 3, "maxLength", 3)));
        assertEquals(List.of("ace", "icy", "ire"), result);

        result = Arrays.asList(RiTa.spellsLike("ice", Map.of("minLength", 3, "maxLength", 3)));
        for (String r : result) {
            assertEquals(3, r.length());
        }
        assertEquals(List.of("ace", "icy", "ire"), result);

        result = Arrays.asList(RiTa.spellsLike("ice", Map.of("minLength", 3, "maxLength", 3, "pos", "n")));
        for (String r : result) {
            assertEquals(3, r.length());
        }
        assertEquals(List.of("ace", "ire"), result);

        result = Arrays.asList(RiTa.spellsLike("ice", Map.of("minLength", 4, "maxLength", 4, "pos", "v", "limit", 5)));
        for (String r : result) {
            assertEquals(4, r.length());
        }
        assertEquals(List.of("ache", "bide", "bite", "cite", "dine"), result);

        result = Arrays.asList(RiTa.spellsLike("ice", Map.of("minLength", 4, "maxLength", 4, "pos", "nns", "limit", 5)));
        for (String r : result) {
            assertEquals(4, r.length());
        }
        assertEquals(List.of("dice", "rice"), result);

        result = Arrays.asList(RiTa.spellsLike("ice", Map.of("minLength", 4, "maxLength", 4, "pos", "nns", "minDistance", 3, "limit", 5)));
        for (String r : result) {
            assertEquals(4, r.length());
        }
        assertEquals(List.of("axes", "beef", "deer", "dibs", "fame"), result);

        // special case, where word is not in dictionary
        result = Arrays.asList(RiTa.spellsLike("abated", Map.of("pos", "vbd")));
        assertTrue(result.contains("abetted"));
        assertTrue(result.contains("aborted"));
        assertFalse(result.contains("condensed"));

        // https://github.com/dhowe/rita/issues/177
        assertFalse(Arrays.asList(RiTa.spellsLike("lined", Map.of("pos", "vb"))).contains("lived"));
        assertTrue(Arrays.asList(RiTa.spellsLike("lined", Map.of("pos", "vbd"))).contains("lived"));
        assertFalse(Arrays.asList(RiTa.spellsLike("let", Map.of("pos", "vb"))).contains("led"));
        assertTrue(Arrays.asList(RiTa.spellsLike("let", Map.of("pos", "vbd"))).contains("led"));
        assertFalse(Arrays.asList(RiTa.spellsLike("brake", Map.of("pos", "vb"))).contains("broke"));
        assertTrue(Arrays.asList(RiTa.spellsLike("brake", Map.of("pos", "vbd"))).contains("broke"));
        assertFalse(Arrays.asList(RiTa.spellsLike("overseas", Map.of("pos", "vb"))).contains("oversaw"));
        assertTrue(Arrays.asList(RiTa.spellsLike("overseas", Map.of("pos", "vbd"))).contains("oversaw"));

        List<String> rhyme = Arrays.asList(RiTa.spellsLike("spreads", Map.of("pos", "vbz", "limit", 1000)));
        assertFalse(rhyme.contains("discriminateds"));
        assertFalse(rhyme.contains("endeds"));
        assertFalse(rhyme.contains("finisheds"));
        assertFalse(rhyme.contains("reporteds"));
        assertFalse(rhyme.contains("proliferateds"));
        assertFalse(rhyme.contains("outpaceds"));
        assertFalse(rhyme.contains("lived"));
    }

    @Test
    void shouldCallSoundsLike() {
        assertEquals(List.of("torpedo"), Arrays.asList(RiTa.soundsLike("tornado", Map.of("type", "sound"))));

        List<String> result = Arrays.asList(RiTa.soundsLike("try", Map.of("limit", 20)));
        List<String> answer = List.of("cry", "dry", "fry", "pry", "rye", "tie", "tray", "tree",
            "tribe", "tried", "tripe", "trite", "true", "wry");
        assertEquals(answer, result);

        result = Arrays.asList(RiTa.soundsLike("try", Map.of("minDistance", 2, "limit", 20)));
        assertTrue(result.size() > answer.size()); // more

        result = Arrays.asList(RiTa.soundsLike("happy", Map.of()));
        assertEquals(answer = List.of("happier", "hippie"), result);

        result = Arrays.asList(RiTa.soundsLike("happy", Map.of("minDistance", 2)));
        assertTrue(result.size() > answer.size()); // more

        result = Arrays.asList(RiTa.soundsLike("cat", Map.of("type", "sound")));
        assertEquals(List.of("bat", "cab", "cache", "calf", "calve", "can", "can't", "cap", "cash", "cast"), result);

        result = Arrays.asList(RiTa.soundsLike("cat", Map.of("type", "sound", "limit", 5)));
        assertEquals(List.of("bat", "cab", "cache", "calf", "calve"), result);

        result = Arrays.asList(RiTa.soundsLike("cat", Map.of("type", "sound", "limit", 1000, "minLength", 2, "maxLength", 4)));
        assertEquals(List.of("at", "bat", "cab", "calf", "can", "cap", "cash", "cast", "chat", "coat",
            "cot", "curt", "cut", "fat", "hat", "kit", "kite", "mat", "matt", "pat", "rat", "sat",
            "that", "vat"), result);

        result = Arrays.asList(RiTa.soundsLike("cat", Map.of("type", "sound", "minLength", 4, "maxLength", 5, "pos", "jj")));
        assertEquals(answer = List.of("catty", "curt"), result);

        result = Arrays.asList(RiTa.soundsLike("cat", Map.of("minDistance", 2)));
        assertTrue(result.size() > answer.size());
    }

    @Test
    void shouldCallSoundsLikePos() {
        List<String> result = Arrays.asList(RiTa.soundsLike("abated", Map.of("pos", "vbd")));
        assertTrue(result.contains("abetted"));
        assertTrue(result.contains("debated"));
        assertFalse(result.contains("condensed"));

        // https://github.com/dhowe/rita/issues/177
        assertFalse(Arrays.asList(RiTa.soundsLike("build", Map.of("pos", "vb", "limit", 1000))).contains("built"));
        assertFalse(Arrays.asList(RiTa.soundsLike("computerize", Map.of("pos", "vb", "limit", 1000))).contains("computerized"));
        assertFalse(Arrays.asList(RiTa.soundsLike("concern", Map.of("pos", "vb"))).contains("concerned"));
        assertFalse(Arrays.asList(RiTa.soundsLike("commit", Map.of("pos", "vb"))).contains("committed"));
        assertFalse(Arrays.asList(RiTa.soundsLike("involve", Map.of("pos", "vb"))).contains("involved"));
        assertFalse(Arrays.asList(RiTa.soundsLike("grained", Map.of("pos", "vb"))).contains("gained"));

        assertTrue(Arrays.asList(RiTa.soundsLike("premade", Map.of("pos", "vbd"))).contains("remade"));
        assertTrue(Arrays.asList(RiTa.soundsLike("incriminate", Map.of("pos", "vbd"))).contains("discriminated"));
        assertTrue(Arrays.asList(RiTa.soundsLike("paunched", Map.of("pos", "vbd"))).contains("pinched")); // launched ?
    }

    @Test
    void shouldCallSoundsLikeMatchSpelling() {
        List<String> result;
        result = Arrays.asList(RiTa.soundsLike("try", Map.of("matchSpelling", true)));
        assertEquals(List.of("cry", "dry", "fry", "pry", "tray"), result);

        result = Arrays.asList(RiTa.soundsLike("try", Map.of("matchSpelling", true, "maxLength", 3)));
        assertEquals(List.of("cry", "dry", "fry", "pry", "wry"), result);

        result = Arrays.asList(RiTa.soundsLike("try", Map.of("matchSpelling", true, "minLength", 4)));
        assertEquals(List.of("tray"), result);

        result = Arrays.asList(RiTa.soundsLike("try", Map.of("matchSpelling", true, "limit", 3)));
        assertEquals(List.of("cry", "dry", "fry"), result);

        result = Arrays.asList(RiTa.soundsLike("daddy", Map.of("matchSpelling", true)));
        assertEquals(List.of("dandy", "paddy"), result);

        result = Arrays.asList(RiTa.soundsLike("banana", Map.of("matchSpelling", true)));
        assertEquals(List.of("bonanza"), result);

        result = Arrays.asList(RiTa.soundsLike("abated", Map.of("pos", "vbd", "matchSpelling", true)));
        assertEquals(2, result.size());
        assertTrue(result.contains("abetted"));
        assertTrue(result.contains("awaited"));
    }

    @Test
    void shouldCallIsRhyme() {
        assertFalse(RiTa.isRhyme("apple", "polo"));
        assertFalse(RiTa.isRhyme("this", "these"));

        assertTrue(RiTa.isRhyme("cat", "hat"));
        assertTrue(RiTa.isRhyme("yellow", "mellow"));
        assertTrue(RiTa.isRhyme("toy", "boy"));

        assertTrue(RiTa.isRhyme("solo", "tomorrow"));
        assertTrue(RiTa.isRhyme("tense", "sense"));
        assertTrue(RiTa.isRhyme("crab", "drab"));
        assertTrue(RiTa.isRhyme("shore", "more"));
        assertFalse(RiTa.isRhyme("hose", "house"));
        assertFalse(RiTa.isRhyme("sieve", "mellow"));

        assertTrue(RiTa.isRhyme("mouse", "house"));
        // expect(!RiTa.isRhyme("solo", "yoyo")) — why??
        // expect(!RiTa.isRhyme("yoyo", "jojo")) — Known Issues

        assertTrue(RiTa.isRhyme("yo", "bro"));
        assertFalse(RiTa.isRhyme("swag", "grab"));
        assertFalse(RiTa.isRhyme("", ""));

        assertTrue(RiTa.isRhyme("weight", "eight"));
        assertTrue(RiTa.isRhyme("eight", "weight"));

        assertTrue(RiTa.isRhyme("abated", "debated"));

        // fail without lexicon — NOLEX branch is dead when a lexicon is present.
    }

    @Test
    void shouldCallIsAlliteration() {
        assertTrue(RiTa.isAlliteration("knife", "gnat")); // gnat=lts
        assertTrue(RiTa.isAlliteration("knife", "naughty"));

        assertTrue(RiTa.isAlliteration("sally", "silly"));
        assertTrue(RiTa.isAlliteration("sea", "seven"));
        assertTrue(RiTa.isAlliteration("silly", "seven"));
        assertTrue(RiTa.isAlliteration("sea", "sally"));

        assertTrue(RiTa.isAlliteration("big", "bad"));
        assertTrue(RiTa.isAlliteration("bad", "big")); // swap position

        assertTrue(RiTa.isAlliteration("BIG", "bad")); // CAPITAL LETTERS
        assertTrue(RiTa.isAlliteration("big", "BAD")); // CAPITAL LETTERS
        assertTrue(RiTa.isAlliteration("BIG", "BAD")); // CAPITAL LETTERS

        // False
        assertFalse(RiTa.isAlliteration("", ""));
        assertFalse(RiTa.isAlliteration("wind", "withdraw"));
        assertFalse(RiTa.isAlliteration("solo", "tomorrow"));
        assertFalse(RiTa.isAlliteration("solo", "yoyo"));
        assertFalse(RiTa.isAlliteration("yoyo", "jojo"));
        assertFalse(RiTa.isAlliteration("cat", "access"));

        assertTrue(RiTa.isAlliteration("unsung", "sine"));
        assertTrue(RiTa.isAlliteration("job", "gene"));
        assertTrue(RiTa.isAlliteration("jeans", "gentle"));

        assertTrue(RiTa.isAlliteration("abet", "better"));
        assertTrue(RiTa.isAlliteration("never", "knight"));
        assertTrue(RiTa.isAlliteration("knight", "navel"));
        assertTrue(RiTa.isAlliteration("cat", "kitchen"));

        // not counting assonance
        assertFalse(RiTa.isAlliteration("octopus", "oblong"));
        assertFalse(RiTa.isAlliteration("omen", "open"));
        assertFalse(RiTa.isAlliteration("amicable", "atmosphere"));

        assertTrue(RiTa.isAlliteration("abated", "abetted"));

        // fail without lexicon — NOLEX branch is dead when a lexicon is present.
    }

    @Test
    void shouldCorrectlyCallToPhoneArray() {
        String raw = RiTa.lexicon.rawPhones("tornado", false);
        List<String> result = RiTa.lexicon._toPhoneArray(raw);
        List<String> ans = List.of("t", "ao", "r", "n", "ey", "d", "ow");
        assertEquals(ans, result);
    }

    private static String fail(String result, String epos) {
        String test = result.endsWith("es") ? result.substring(0, result.length() - 2) : result;
        Object ent = RiTa.lexicon.data.get(test);
        return "(" + epos + ") Fail: " + result + ": expected " + epos + ", got "
            + (ent != null ? ent : "null");
    }
}
