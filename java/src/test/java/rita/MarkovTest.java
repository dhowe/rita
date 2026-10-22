package rita;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static rita.TestReflect.opts;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;

/**
 * Ported from <code>js/test/markov-tests.js</code>.
 *
 * <p>Mapping notes:
 * <ul>
 *   <li>{@code RiMarkov.generate(...)} returns {@code Object} — a {@code String} when
 *       {@code numSentences==1}, otherwise a {@code List<String>} (mirrors the JS union return).
 *       Helpers {@link #str}/{@link #list} cast.</li>
 *   <li>JS generators ({@code stream}) map to {@link Iterable}; {@code [...gen]} -> {@link #drain}.</li>
 *   <li>JS regex {@code /re/.test(s)} -> {@link #re} (unanchored {@code find}, matching JS).</li>
 *   <li>Custom tokenizer/untokenizer -> {@link Function} lambdas.</li>
 *   <li>{@code it.skip} blocks are kept as {@code @Disabled}; {@code 0 && it(...)} disabled
 *       blocks are omitted.</li>
 * </ul>
 */
class MarkovTest {

    private static final String sample = TestData.SAMPLE;
    private static final String sample2 = TestData.SAMPLE2;
    private static final String sample3 = TestData.SAMPLE3;
    private static final String sample4 = TestData.SAMPLE4;
    private static final String exampleStr = TestData.EXAMPLE_STR;
    private static final List<String> exampleTokens = TestData.EXAMPLE_TOKENS;

    @Test
    void shouldCallRiMarkov() {
        RiMarkov rm = RiTa.markov(3);
        assertInstanceOf(Object.class, rm);
        assertEquals(0, rm.size());
    }

    @Test
    void shouldCallRiTaMarkov() {
        RiMarkov rm = RiTa.markov(3);
        assertInstanceOf(Object.class, rm);
        assertEquals(0, rm.size());

        rm = RiTa.markov(3, opts("text", "The dog ran away"));
        assertEquals(6, rm.size());

        rm = RiTa.markov(3, opts("text", ""));
        assertEquals(0, rm.size());
        final RiMarkov rm2 = rm;
        assertThrows(Exception.class, () -> rm2.generate());

        rm = RiTa.markov(3, opts("text", sample));
        assertTrue(str(rm.generate()).length() > 0);

        rm = RiTa.markov(3, opts("text", "Too short."));
        final RiMarkov rm3 = rm;
        assertThrows(Exception.class, () -> rm3.generate());

        assertThrows(Exception.class, () -> RiTa.markov(3, opts("text", 1)));
        assertThrows(Exception.class, () -> RiTa.markov(3, opts("text", false)));

        rm = RiTa.markov(3, opts("sentences", List.of("Sentence one.", "Sentence two.")));
        assertEquals(10, rm.size());

        rm = RiTa.markov(3, opts("sentences", Arrays.asList(RiTa.sentences(sample))));
        assertTrue(str(rm.generate()).length() > 0);
    }

    @Test
    void shouldCallRandomPSelect() {
        RandGen random = RiTa.randomizer;
        assertThrows(Exception.class, () -> random.pselect());
        assertEquals(0, random.pselect(new double[]{1}));

        double[] weights = {1.0, 2, 6, -2.5, 0};
        double[] expected = {2, 2, 1.75, 1.55};
        double[] temps = {0.5, 1, 2, 10};
        List<double[]> distrs = new ArrayList<>();
        for (double t : temps) {
            distrs.add(random.ndist(weights, t));
        }
        List<Double> results = new ArrayList<>();
        int numTests = 100;
        for (double[] sm : distrs) {
            int sum = 0;
            for (int j = 0; j < numTests; j++) {
                sum += random.pselect(sm);
            }
            results.add(sum / (double) numTests);
        }
        assertEquals(expected[0], results.get(0), 0.1);
        assertEquals(expected[1], results.get(1), 0.2);
        assertEquals(expected[2], results.get(2), 0.4);
        assertEquals(expected[3], results.get(3), 1.0);

        double[][] distr = {{1, 2, 3, 4}, {0.1, 0.2, 0.3, 0.4}, {0.2, 0.3, 0.4, 0.5}};
        double[] expected2 = {3, 0.3, 0.3857};
        for (int k = 0; k < 10; k++) {
            List<Double> res = new ArrayList<>();
            for (double[] sm : distr) {
                double sum = 0;
                for (int j = 0; j < 1000; j++) {
                    sum += random.pselect2(sm);
                }
                res.add(sum / 1000.0);
            }
            assertEquals(expected2[0], res.get(0), 0.5);
            assertEquals(expected2[1], res.get(1), 0.05);
            assertEquals(expected2[2], res.get(2), 0.05);
        }
    }

    @Test
    void shouldCallRandomPSelectIndex() {
        RandGen random = RiTa.randomizer;
        assertThrows(Exception.class, () -> random.pselect());
        assertEquals(0, random.pselectIndex(new double[]{1}));

        double[] weights = {1.0, 2, 6, -2.5, 0};
        double[] expected = {2, 2, 1.75, 1.55};
        double[] temps = {0.5, 1, 2, 10};
        List<double[]> distrs = new ArrayList<>();
        for (double t : temps) {
            distrs.add(random.ndist(weights, t));
        }
        List<Double> results = new ArrayList<>();
        int numTests = 100;
        for (double[] sm : distrs) {
            int sum = 0;
            for (int j = 0; j < numTests; j++) {
                sum += random.pselectIndex(sm);
            }
            results.add(sum / (double) numTests);
        }
        assertEquals(expected[0], results.get(0), 0.1);
        assertEquals(expected[1], results.get(1), 0.2);
        assertEquals(expected[2], results.get(2), 0.4);
        assertEquals(expected[3], results.get(3), 1.0);

        double[][] distr = {{1, 2, 3, 4}, {0.1, 0.2, 0.3, 0.4}, {0.2, 0.3, 0.4, 0.5}};
        double[] expected2 = {3, 0.3, 0.3857};
        for (int k = 0; k < 10; k++) {
            List<Double> res = new ArrayList<>();
            for (double[] sm : distr) {
                double sum = 0;
                for (int j = 0; j < 1000; j++) {
                    sum += random.pselect2(sm);
                }
                res.add(sum / 1000.0);
            }
            assertEquals(expected2[0], res.get(0), 0.5);
            assertEquals(expected2[1], res.get(1), 0.05);
            assertEquals(expected2[2], res.get(2), 0.05);
        }
    }

    @Test
    void shouldCallRandomNdist() {
        RandGen random = RiTa.randomizer;
        // expect(() => Random.ndist([1.0, 2, 6, -2.5, 0])).to.throw  (no temp -> negative weight throws)
        assertThrows(Exception.class, () -> random.ndist(new double[]{1.0, 2, 6, -2.5, 0}));

        double[] weights = {2, 1};
        double[] expected = {0.666, 0.333};
        double[] results = random.ndist(weights);
        for (int i = 0; i < results.length; i++) {
            assertEquals(expected[i], results[i], 0.01);
        }
        weights = new double[]{7, 1, 2};
        expected = new double[]{0.7, 0.1, 0.2};
        results = random.ndist(weights);
        for (int i = 0; i < results.length; i++) {
            assertEquals(expected[i], results[i], 0.01);
        }
    }

    @Test
    void shouldCallRandomNdistTemp() {
        RandGen random = RiTa.randomizer;
        double[] weights = {1.0, 2, 6, -2.5, 0};
        double[][] expected = {
            {0, 0, 1, 0, 0},
            {0.0066, 0.018, 0.97, 0.0002, 0.0024},
            {0.064, 0.11, 0.78, 0.011, 0.039},
            {0.19, 0.21, 0.31, 0.13, 0.17},
        };
        double[][] results = {
            random.ndist(weights, 0.5),
            random.ndist(weights, 1),
            random.ndist(weights, 2),
            random.ndist(weights, 10)
        };
        for (int i = 0; i < results.length; i++) {
            for (int j = 0; j < results[i].length; j++) {
                assertEquals(expected[i][j], results[i][j], 0.01);
            }
        }
    }

    @Test
    void shouldThrowOnGenerateForEmptyModel() {
        RiMarkov rm = new RiMarkov(4, opts("maxLengthMatch", 6));
        assertThrows(Exception.class, () -> rm.generate(5));
    }

    @Test
    void shouldThrowOnFailedGenerate() {
        RiMarkov rm = new RiMarkov(4, opts("maxLengthMatch", 6));
        rm.addText(sample);
        final RiMarkov rm1 = rm;
        assertThrows(Exception.class, () -> rm1.generate(5));

        rm = new RiMarkov(4, opts("maxLengthMatch", 5));
        rm.addSentences(Arrays.asList(RiTa.sentences(sample)));
        final RiMarkov rm2 = rm;
        assertThrows(Exception.class, () -> rm2.generate(5));

        rm = new RiMarkov(4, opts("maxAttempts", 1));
        rm.addText("Hi.");
        final RiMarkov rm3 = rm;
        assertThrows(Exception.class, () -> rm3.generate(5));
    }

    @Test
    void shouldApplyCustomTokenizers() {
        List<String> sents = List.of("asdfasdf-", "aqwerqwer+", "asdfasdf*");
        Function<String, List<String>> tokenize = s -> chars(s);
        Function<List<String>, String> untokenize = l -> String.join("", l);

        RiMarkov rm = new RiMarkov(4, opts("tokenize", tokenize, "untokenize", untokenize));
        rm.addSentences(sents);

        int sum = 2 * sents.size();
        for (String s : sents) {
            sum += s.length();
        }
        assertEquals(sum, rm.size());
    }

    @Test
    void shouldComputeStartDistrib() {
        List<String> sents = List.of("asdfasdf-", "asqwerqwer+", "aqadaqdf*");
        Function<String, List<String>> tokenize = s -> chars(s);
        Function<List<String>, String> untokenize = l -> String.join("", l);

        RiMarkov rm = new RiMarkov(4, opts("tokenize", tokenize, "untokenize", untokenize));
        rm.addSentences(sents).build();

        assertEquals(List.of("a"), new ArrayList<>(rm.model.suffixes.startIndexDist().keySet()));
    }

    @Test
    void riMarkovGenerateRestart() {
        List<String> sents = List.of("asdfasdf-", "asqwerqwer+", "aqadaqdf*");
        Function<String, List<String>> tokenize = s -> chars(s);
        Function<List<String>, String> untokenize = l -> String.join("", l);

        RiMarkov rm = new RiMarkov(4, opts("tokenize", tokenize, "untokenize", untokenize));
        rm.addSentences(sents).build();

        assertEquals(List.of("a"), new ArrayList<>(rm.model.suffixes.startIndexDist().keySet()));

        for (int i = 0; i < 10; i++) {
            String result = str(rm.generate(2, List.of("a", "s"), opts("maxLength", 20)));
            assertTrue(re(result, "^as[a-z]+[-+*]$"));
        }
    }

    @Test
    void shouldGenerateNonEnglishSentences() {
        String text = "家 安 春 夢 家 安 春 夢 ！ 家 安 春 夢 德 安 春 夢 ？ 家 安 春 夢 安 安 春 夢 。";
        List<String> sentArray = matchAll(text, "[^，；。？！]+[，；。？！]");
        RiMarkov rm = new RiMarkov(3);
        rm.addSentences(sentArray);
        List<String> result = list(rm.generate(opts("prompt", List.of("家"), "numSentences", 5)));
        assertEquals(5, result.size());
        assertTrue(re(result.get(0), "^[^，；。？！]+[，；。？！]$"));
        for (String r : result) {
            assertTrue(re(r, "^[^，；。？！]+[，；。？！]$"));
        }
    }

    @Test
    void shouldApplyCustomChineseTokenizers() {
        String text = "家安春夢家安春夢！家安春夢德安春夢？家安春夢安安春夢。";
        List<String> sents = matchAll(text, "[^，；。？！]+[，；。？！]");
        Function<String, List<String>> tokenize = s -> chars(s);
        Function<List<String>, String> untokenize = l -> String.join("", l);

        RiMarkov rm = new RiMarkov(3, opts("tokenize", tokenize, "untokenize", untokenize));
        rm.addSentences(sents);
        List<String> result = list(rm.generate(opts("prompt", List.of("家"), "numSentences", 5)));
        assertEquals(5, result.size());
        assertTrue(re(result.get(0), "^[^，；。？！]+[，；。？！]$"));
        for (String r : result) {
            assertTrue(re(r, "^[^，；。？！]+[，；。？！]$"));
        }
    }

    @Test
    void shouldCallGenerate1() {
        RiMarkov rm = new RiMarkov(5);
        rm.addText(sample);
        String sent = str(rm.generate());
        assertInstanceOf(String.class, (Object) sent);
        assertEquals(sent.substring(0, 1).toUpperCase(), sent.substring(0, 1));
        assertTrue(re(sent, "[!?.]$"));
    }

    @Test
    void shouldCallGenerate2() {
        RiMarkov rm = new RiMarkov(4);
        rm.addText(sample);
        String sent = str(rm.generate(opts("prompt", List.of("I"))));
        assertInstanceOf(String.class, (Object) sent);
        assertEquals("I", sent.substring(0, 1));
        assertTrue(re(sent, "[!?.]$"));
    }

    @Test
    void shouldCallGenerate3() {
        RiMarkov rm = new RiMarkov(4);
        rm.addText(sample);
        List<String> sents = list(rm.generate(opts("numSentences", 3)));
        assertEquals(3, sents.size());
        for (String s : sents) {
            assertEquals(s.substring(0, 1).toUpperCase(), s.substring(0, 1));
            assertTrue(re(s, "[!?.]$"), "FAIL: bad last char in '" + s + "'");
        }
    }

    @Test
    void shouldCallGenerate4() {
        RiMarkov rm = new RiMarkov(3);
        rm.addText(sample);
        String s = str(rm.generate(opts("minLength", 5, "maxLength", 35)));
        assertEquals(s.substring(0, 1).toUpperCase(), s.substring(0, 1), "FAIL: bad first char in '" + s + "'");
        assertTrue(re(s, "[!?.]$"), "FAIL: bad last char in '" + s + "'");
        int num = RiTa.tokenize(s).length;
        assertTrue(num >= 5 && num <= 35, num + " not within 5-35");
    }

    @Test
    void shouldCallGenerate5() {
        RiMarkov rm = new RiMarkov(3);
        rm.addText(sample2);
        String res = str(rm.generate(opts("prompt", List.of("One", "reason"))));
        assertTrue(res.startsWith("One reason"));
        assertTrue(re(res, "^[A-Z][a-z ,I]+[.?!]$"));
        assertTrue(re(res, "[!?.]$"));

        rm = new RiMarkov(3, opts("trace", 0));
        rm.addText(sample2);
        res = str(rm.generate());
        assertTrue(re(res, "^[A-Z]"));
        assertTrue(re(res, "[!?.]$"));

        rm = new RiMarkov(3, opts("trace", 0));
        rm.addText(sample2);
        List<String> resList = list(rm.generate(opts("maxLength", 20, "numSentences", 2)));
        assertEquals(2, resList.size());
        for (String r : resList) {
            assertTrue(re(r, "^[A-Z]"));
            assertTrue(re(r, "[!?.]$"));
        }
    }

    @Test
    void shouldCallGenerateMinMaxLength() {
        RiMarkov rm = new RiMarkov(3);
        int minLength = 7, maxLength = 20;
        rm.addText(sample);
        List<String> sents = list(rm.generate(3, opts("minLength", minLength, "maxLength", maxLength, "numSentences", 3)));
        assertEquals(3, sents.size());
        for (String s : sents) {
            assertEquals(s.substring(0, 1).toUpperCase(), s.substring(0, 1));
            assertTrue(re(s, "[!?.]$"), "FAIL: bad last char in '" + s + "'");
            int num = RiTa.tokenize(s).length;
            assertTrue(num >= minLength && num <= maxLength, num + " not within " + minLength + "-" + maxLength);
        }
    }

    @Test
    void shouldCallGenerateMinMaxLengthCombineWithAbove() {
        RiMarkov rm = new RiMarkov(4);
        rm.addText(sample);
        for (int i = 0; i < 3; i++) {
            int minLength = 3 + i, maxLength = 10 + i;
            String s = str(rm.generate(opts("minLength", minLength, "maxLength", maxLength)));
            assertEquals(s.substring(0, 1).toUpperCase(), s.substring(0, 1), "FAIL: bad first char in '" + s + "'");
            assertTrue(re(s, "[!?.]$"), "FAIL: bad last char in '" + s + "'");
            int num = RiTa.tokenize(s).length;
            assertTrue(num >= minLength && num <= maxLength, num + " not within " + minLength + "-" + maxLength);
        }
    }

    @Test
    void shouldCallGeneratePrompt() {
        RiMarkov rm = new RiMarkov(4);
        List<String> start = List.of("One");
        rm.addText(sample);
        String s = str(rm.generate(opts("prompt", start)));
        assertTrue(s.startsWith(String.join(" ", start)));

        start = List.of("Achieving");
        String res = str(rm.generate(opts("prompt", start)));
        assertInstanceOf(String.class, (Object) res);
        assertTrue(res.startsWith(String.join(" ", start)));

        start = List.of("I");
        List<String> arr = list(rm.generate(opts("prompt", start, "numSentences", 2)));
        assertInstanceOf(List.class, (Object) arr);
        assertEquals(2, arr.size());
        assertTrue(arr.get(0).startsWith(String.join(" ", start)));

        start = List.of("Not-exist");
        final List<String> notExist = start;
        assertThrows(Exception.class, () -> rm.generate(opts("prompt", notExist)));
        assertThrows(Exception.class, () -> rm.generate(opts("prompt", notExist, "numSentences", 1)));
        assertThrows(Exception.class, () -> rm.generate(opts("prompt", notExist, "numSentences", 2)));

        start = List.of("I and she");
        final List<String> iAndShe = start;
        assertThrows(Exception.class, () -> rm.generate(opts("prompt", iAndShe, "numSentences", 2)));

        start = List.of("");
        assertEquals(2, list(rm.generate(opts("prompt", start, "numSentences", 2))).size());

        start = List.of(" ");
        final List<String> space = start;
        assertThrows(Exception.class, () -> rm.generate(opts("prompt", space, "numSentences", 2)));
    }

    @Test
    void shouldCallGeneratePromptArray() {
        RiMarkov rm = new RiMarkov(4);
        List<String> start = List.of("One");
        rm.addText(sample);
        for (int i = 0; i < 5; i++) {
            String s = str(rm.generate(opts("prompt", start)));
            assertTrue(s.startsWith(String.join(" ", start)));
        }

        start = List.of("Achieving");
        for (int i = 0; i < 5; i++) {
            String res = str(rm.generate(opts("prompt", start)));
            assertInstanceOf(String.class, (Object) res);
            assertTrue(res.startsWith(String.join(" ", start)));
        }

        start = List.of("I");
        for (int i = 0; i < 5; i++) {
            List<String> arr = list(rm.generate(2, opts("prompt", start, "numSentences", 2)));
            assertEquals(2, arr.size());
            assertTrue(arr.get(0).startsWith(String.join(" ", start)));
        }

        rm = new RiMarkov(4);
        rm.addText(sample);
        start = List.of("One", "reason");
        for (int i = 0; i < 1; i++) {
            String s = str(rm.generate(opts("prompt", start)));
            assertTrue(s.startsWith(String.join(" ", start)));
        }

        start = List.of("Achieving", "personal");
        for (int i = 0; i < 5; i++) {
            String res = str(rm.generate(opts("prompt", start)));
            assertInstanceOf(String.class, (Object) res);
            assertTrue(res.startsWith(String.join(" ", start)));
        }

        start = List.of("I", "also");
        for (int i = 0; i < 5; i++) {
            String res = str(rm.generate(opts("prompt", start)));
            assertInstanceOf(String.class, (Object) res);
            assertTrue(res.startsWith(String.join(" ", start)));
        }
    }

    @Test
    @Disabled
    void shouldCallGenerateAllowDuplicates() {
        RiMarkov rm = RiTa.markov(3, opts("text", sample3));
        for (int index = 0; index < 10; index++) {
            String res = str(rm.generate(opts("allowDuplicates", false)));
            assertTrue(!sample3.contains(res));
        }
    }

    @Test
    void shouldCallGenerateTemp() {
        RiMarkov rm = RiTa.markov(3, opts("text", sample3));
        for (int index = 0; index < 1; index++) {
            assertTrue(str(rm.generate(opts("temperature", 0))).length() > 0);
            assertTrue(str(rm.generate(opts("temperature", 1))).length() > 0);
            assertTrue(str(rm.generate(opts("temperature", 0.1))).length() > 0);
            assertTrue(str(rm.generate(opts("temperature", 100))).length() > 0);
        }
    }

    @Test
    void shouldGenerateAcrossSentences() {
        RiMarkov rm = new RiMarkov(3, opts("trace", 0));
        rm.addText(sample2);
        assertEquals(3, rm.n);

        List<String> sents = list(rm.generate(opts("numSentences", 3)));
        assertEquals(3, sents.size());

        for (String sent : sents) {
            String[] toks = RiTa.tokenize(sent);
            for (int j = 0; j <= toks.length - rm.n; j++) {
                String[] part = Arrays.copyOfRange(toks, j, j + rm.n);
                String res = RiTa.untokenize(part);
                assertTrue(sample2.contains(res), "output not found in text: \"" + res + "\"");
            }
        }

        String[] corpusSents = RiTa.sentences(sample2);
        Set<String> validStarts = new HashSet<>();
        Set<String> validEnds = new HashSet<>();
        for (String s : corpusSents) {
            String[] t = RiTa.tokenize(s);
            validStarts.add(t[0]);
            validEnds.add(t[t.length - 1]);
        }
        for (String sent : sents) {
            String[] toks = RiTa.tokenize(sent);
            assertTrue(validStarts.contains(toks[0]), "bad sentence start: \"" + toks[0] + "\"");
            assertTrue(validEnds.contains(toks[toks.length - 1]), "bad sentence end: \"" + toks[toks.length - 1] + "\"");
        }
    }

    @Test
    void shouldCallGenerateMlm1() {
        int mlms = 8;
        String theText = sample4;
        RiMarkov rm = new RiMarkov(3, opts("maxLengthMatch", mlms, "trace", 0));
        rm.addText(theText);
        List<String> sents = list(rm.generate(opts("numSentences", 2)));
        for (String sent : sents) {
            String[] toks = RiTa.tokenize(sent);
            for (int j = 0; j <= toks.length - rm.n; j++) {
                String res = RiTa.untokenize(Arrays.copyOfRange(toks, j, j + rm.n));
                assertTrue(theText.contains(res), "output not found in text: \"" + res + "\"");
            }
            for (int j = 0; j <= toks.length - (mlms + 1); j++) {
                String res = RiTa.untokenize(Arrays.copyOfRange(toks, j, j + (mlms + 1)));
                assertTrue(!theText.contains(res), "Got \"" + sent + "\"\n\nBut \"" + res + "\" was found in input");
            }
        }
    }

    @Test
    void shouldCallGenerateMlm2() {
        int mlms = 9;
        RiMarkov rm = new RiMarkov(3, opts("maxLengthMatch", mlms, "trace", 0));
        rm.addText(sample2);
        List<String> sents = list(rm.generate(opts("numSentences", 3)));
        for (String sent : sents) {
            String[] toks = RiTa.tokenize(sent);
            for (int j = 0; j <= toks.length - rm.n; j++) {
                String res = RiTa.untokenize(Arrays.copyOfRange(toks, j, j + rm.n));
                assertTrue(sample2.contains(res), "output not found in text: \"" + res + "\"");
            }
            for (int j = 0; j <= toks.length - (mlms + 1); j++) {
                String res = RiTa.untokenize(Arrays.copyOfRange(toks, j, j + (mlms + 1)));
                assertTrue(!sample2.contains(res), "Got \"" + sent + "\"\n\nBut \"" + res + "\" was found in input");
            }
        }
    }

    @Test
    void shouldCallGenerateWithTightMaxLengthMatchMinLength() {
        RiMarkov rm = new RiMarkov(3, opts("maxLengthMatch", 6, "trace", 0));
        rm.addText(sample + " " + sample4);
        List<String> sents = list(rm.generate(opts("numSentences", 4, "minLength", 8)));
        assertEquals(4, sents.size());
    }

    @Test
    void shouldCallCompletions() {
        RiMarkov rm = new RiMarkov(4);
        rm.addText(sample);

        assertEquals(List.of("to"), rm.completions(List.of("people", "lie", "is")));
        assertEquals(List.of("to"), rm.completions(List.of("One", "reason", "people", "lie", "is")));
        assertEquals(List.of(".", "is"), rm.completions(List.of("personal", "power")));
        assertEquals(List.of("confident"), rm.completions(List.of("to", "be", "more")));

        List<String> iRes = new ArrayList<>(rm.completions(List.of("I")));
        List<String> expec = new ArrayList<>(List.of("did", "claimed", "had", "said", "could",
            "wanted", "also", "achieved", "embarrassed"));
        Collections.sort(iRes);
        Collections.sort(expec);
        assertEquals(expec, iRes);

        assertEquals(List.of(), rm.completions(List.of("XXX")));

        rm = new RiMarkov(4);
        rm.addText(sample2);

        assertEquals(List.of("did"), rm.completions(List.of("I"), List.of("not")));
        assertEquals(List.of("personal"), rm.completions(List.of("achieve"), List.of("power")));
        assertEquals(List.of("personal"), rm.completions(List.of("to", "achieve"), List.of("power")));
        assertEquals(List.of("personal"), rm.completions(List.of("achieve"), List.of("power")));
        assertEquals(List.of("not", "occasionally"), rm.completions(List.of("I", "did")));
        assertEquals(List.of("not", "occasionally"), rm.completions(List.of("I", "did"), List.of("want")));

        final RiMarkov rm2 = rm;
        assertThrows(Exception.class, () ->
            rm2.completions(List.of("I", "did", "not", "occasionally"), List.of("want")));

        boolean tmp = RiTa.SILENT;
        RiTa.SILENT = true;
        assertEquals(List.of(), rm2.completions(List.of("I", "non-exist"), List.of("want")));
        assertEquals(List.of(), rm2.completions(List.of("I", "non-exist"), List.of("want")));
        RiTa.SILENT = tmp;
    }

    @Test
    void shouldCallProbabilities() {
        RiMarkov rm = new RiMarkov(3);
        rm.addText(sample);

        assertEquals(Map.of("people", 1.0), rm.probabilities(List.of("reason")));
        assertEquals(Map.of("lie", 1.0), rm.probabilities(List.of("people")));
        assertEquals(Map.of("power", 1.0), rm.probabilities(List.of("personal")));
        assertEquals(Map.of("time", 0.5, "party", 0.5), rm.probabilities(List.of("the")));
        assertEquals(Map.of("to", 0.3333333333333333, ".", 0.3333333333333333, "helpful", 0.3333333333333333),
            rm.probabilities(List.of("is")));
        assertEquals(Map.of(), rm.probabilities(List.of("XXX")));
    }

    @Test
    void shouldCallProbabilitiesArray() {
        RiMarkov rm = new RiMarkov(4);
        rm.addText(sample2);

        assertEquals(Map.of("time", 0.5, "party", 0.5), rm.probabilities(List.of("the")));
        assertEquals(Map.of("to", 1.0), rm.probabilities(List.of("people", "lie", "is")));
        assertEquals(Map.of("to", 0.3333333333333333, ".", 0.3333333333333333, "helpful", 0.3333333333333333),
            rm.probabilities(List.of("is")));
        assertEquals(Map.of(".", 0.5, "is", 0.5), rm.probabilities(List.of("personal", "power")));
        assertEquals(Map.of("confident", 1.0), rm.probabilities(List.of("to", "be", "more")));
        assertEquals(Map.of(), rm.probabilities(List.of("XXX")));
        assertEquals(Map.of(), rm.probabilities(List.of("personal", "XXX")));
        assertEquals(Map.of("not", 0.6666666666666666, "occasionally", 0.3333333333333333),
            rm.probabilities(List.of("I", "did")));
    }

    @Test
    @Disabled
    void shouldCallProbability() {
        String text;
        RiMarkov rm;
        text = "the dog ate the boy the";
        rm = new RiMarkov(3);
        rm.addText(text);
        assertEquals(0.5, rm.probability(List.of("the")));
        assertEquals(1.0 / 6, rm.probability(List.of("dog")));
        assertEquals(0, rm.probability(List.of("cat")));

        text = "the dog ate the boy that the dog found.";
        rm = new RiMarkov(3);
        rm.addText(text);
        assertEquals(0.3, rm.probability(List.of("the")));
        assertEquals(0.2, rm.probability(List.of("dog")));
        assertEquals(0, rm.probability(List.of("cat")));

        rm = new RiMarkov(3);
        rm.addText(sample);
        assertEquals(0.017045454545454544, rm.probability(List.of("power")));
        assertEquals(0, rm.probability(List.of("Non-exist")));
    }

    @Test
    @Disabled
    void shouldCallProbabilityArray() {
        RiMarkov rm = new RiMarkov(3);
        rm.addText(sample);
        assertEquals(1.0 / 3, rm.probability(List.of("personal", "power", "is")));
        assertEquals(0, rm.probability(List.of("personal", "powXer", "is")));
        assertEquals(1.0 / 2, rm.probability(List.of("someone", "who", "pretends")));
        assertEquals(0, rm.probability(List.of()));
    }

    @Test
    void shouldCallAddText() {
        RiMarkov rm = new RiMarkov(4);
        String[] sents = RiTa.sentences(sample);
        int count = 0;
        for (String s : sents) {
            count += RiTa.tokenize(s).length + 2;
        }
        rm.addSentences(Arrays.asList(sents));
        assertEquals(count, rm.size());
    }

    @Test
    void shouldCallSize() {
        RiMarkov rm = new RiMarkov(4);
        assertEquals(0, rm.size());

        String[] tokens = RiTa.tokenize(sample);
        String[] sents = RiTa.sentences(sample);
        rm = new RiMarkov(3);
        rm.addText(sample);
        assertEquals(tokens.length + (2 * sents.length), rm.size());

        RiMarkov rm2 = new RiMarkov(3);
        rm2.addSentences(Arrays.asList(sents));
        assertEquals(rm.size(), rm2.size());
    }

    @Test
    void shouldSerializeAndDeserialize() {
        RiMarkov rm = new RiMarkov(3);
        String json = rm.toJSON();
        RiMarkov copy = RiMarkov.fromJSON(json);
        markovEquals(rm, copy);

        rm = new RiMarkov(3);
        rm.addText("I ate the dog.");
        copy = RiMarkov.fromJSON(rm.toJSON());
        markovEquals(rm, copy);

        rm = new RiMarkov(3);
        rm.addText("I ate the dog.");
        copy = RiMarkov.fromJSON(rm.toJSON());
        markovEquals(rm, copy);
        assertEquals(str(rm.generate()), str(copy.generate()));
    }

    @Test
    void riMarkovConstructorBackoff() {
        BackoffModel lm1 = new BackoffModel();
        assertInstanceOf(BackoffModel.class, lm1);
        assertTrue(lm1 instanceof Object);
        assertEquals(0, lm1.size());

        lm1 = new BackoffModel(exampleTokens);
        assertInstanceOf(SuffixArray.class, lm1.suffixes);
        assertEquals(21, lm1.size());

        BackoffModel lm2 = new BackoffModel(exampleStr);
        assertInstanceOf(SuffixArray.class, lm2.suffixes);
        assertEquals(21, lm2.size());

        assertThrows(Exception.class, () -> new BackoffModel(123));
        // JS `new BackoffModel([sentences])` is a 2-D array (one nested array); Java's
        // List.of(String[]) spreads to 1-D, so wrap as a single Object element to mirror JS.
        assertThrows(Exception.class, () -> new BackoffModel(List.of((Object) RiTa.sentences(exampleStr))));
    }

    @Test
    void shouldThrowOnGenerateForEmptyModelBackoff() {
        BackoffModel rm = new BackoffModel(opts("maxLengthMatch", 6));
        assertThrows(Exception.class, () -> rm.generateSentences(5, List.of(), Map.of()));
    }

    @Test
    void shouldThrowOnFailedGenerateBackoff() {
        BackoffModel rm = new BackoffModel(opts("maxLengthMatch", 6));
        rm.addText(sample);
        final BackoffModel rm1 = rm;
        assertThrows(Exception.class, () -> rm1.generateSentences(5, List.of(), Map.of()));

        rm = new BackoffModel(opts("maxLengthMatch", 5));
        rm.addSentences(Arrays.asList(RiTa.sentences(sample)));
        final BackoffModel rm2 = rm;
        assertThrows(Exception.class, () -> rm2.generateSentences(5, List.of(), Map.of()));

        rm = new BackoffModel(opts("maxAttempts", 1));
        rm.addText("This is a text that is too short.");
        final BackoffModel rm3 = rm;
        assertThrows(Exception.class, () -> rm3.generateSentences(5, List.of(), Map.of()));
    }

    @Test
    void shouldCallAddTextWithString() {
        BackoffModel rm = new BackoffModel(opts("maxLengthMatch", 6));
        rm.addText(sample).build();
        assertTrue(rm.size() > 0);
        assertEquals(new BackoffModel(sample, opts("maxLengthMatch", 6)), rm);
    }

    @Test
    void shouldCallAddTextWithTokenArray() {
        BackoffModel rm = new BackoffModel(opts("maxLengthMatch", 6));
        rm.addTokens(exampleTokens).build();
        assertTrue(rm.size() > 0);
        assertEquals(new BackoffModel(exampleTokens, opts("maxLengthMatch", 6)), rm);
    }

    @Test
    void shouldCallAddSentencesWithSentenceArray() {
        BackoffModel rm = new BackoffModel(opts("maxLengthMatch", 6));
        rm.addSentences(Arrays.asList(RiTa.sentences(sample))).build();
        assertTrue(rm.size() > 0);
        assertEquals(new BackoffModel(sample, opts("maxLengthMatch", 6)), rm);
    }

    @Test
    void shouldSplitOnCustomTokenizersBackoff() {
        String start = SuffixArray.SEQ_START_TOKEN;
        String end = SuffixArray.SEQ_END_TOKEN;
        List<String> sents = List.of("asdfasdf-", "aqwerqwer+", "asdfasdf*");
        int chars = sents.size() * 2;
        for (String s : sents) {
            chars += s.length();
        }
        Function<String, List<String>> tokenize = s -> chars(s);
        Function<List<String>, String> untokenize = l -> String.join("", l);

        BackoffModel rm = new BackoffModel(opts("tokenize", tokenize, "untokenize", untokenize));
        rm.addSentences(sents).build();
        assertEquals(chars, rm.size());

        List<String> toks = new ArrayList<>();
        for (String s : sents) {
            toks.add(start);
            toks.addAll(chars(s));
            toks.add(end);
        }
        assertEquals(new BackoffModel(toks).size(), rm.size());
    }

    @Test
    void riMarkovConstructorTextForm() {
        RiMarkov rm = new RiMarkov(exampleStr);
        assertInstanceOf(RiMarkov.class, rm);
        assertInstanceOf(BackoffModel.class, rm.model);
        assertTrue(rm.size() > 0);

        RiMarkov rm2 = new RiMarkov(3, opts("text", exampleStr));
        assertEquals(3, rm2.n);
        assertEquals(rm.model.size(), rm2.model.size());

        RiMarkov rm3 = new RiMarkov((Object) opts("text", exampleStr));
        assertEquals(rm.model.size(), rm3.model.size());

        RiMarkov rm4 = new RiMarkov(exampleStr, opts("n", 4));
        assertEquals(4, rm4.n);
    }

    @Test
    void riMarkovAddTextAddSentencesAddTokensSize() {
        RiMarkov rm1 = new RiMarkov(exampleStr);
        RiMarkov rm2 = new RiMarkov();
        rm2.addText(exampleStr);
        assertEquals(rm1.size(), rm2.size());

        RiMarkov rm3 = new RiMarkov();
        rm3.addSentences(Arrays.asList(RiTa.sentences(exampleStr)));
        assertEquals(rm1.size(), rm3.size());

        RiMarkov rm4 = new RiMarkov();
        rm4.addTokens(exampleTokens);
        assertEquals(rm1.size(), rm4.size());

        assertEquals(21, rm1.size());
        assertEquals(0, new RiMarkov().size());

        final RiMarkov rm5 = rm2;
        assertThrows(Exception.class, () -> rm5.addText((Object) 123));
    }

    @Test
    void riMarkovToJsonFromJson() {
        RiMarkov rm = new RiMarkov(exampleStr);
        String json = rm.toJSON();
        assertInstanceOf(String.class, (Object) json);

        RiMarkov copy = RiMarkov.fromJSON(json);
        assertInstanceOf(RiMarkov.class, copy);
        assertEquals(rm.size(), copy.size());

        RiMarkov copy2 = RiMarkov.fromJSON(json);
        assertInstanceOf(RiMarkov.class, copy2);
        assertEquals(rm.size(), copy2.size());

        List<String> orig = rm.completions(List.of("The", "brown"));
        List<String> after = copy2.completions(List.of("The", "brown"));
        assertEquals(orig, after);
    }

    @Test
    void riMarkovGenerateNumSentences() {
        RiMarkov rm = new RiMarkov(sample);
        rm.n = 3;
        Map<String, Object> o = opts("minTokens", 3, "maxTokens", 20);

        String[] norm = rm.generate(3, List.of("I"), o);
        assertEquals(1, norm.length);
        assertTrue(norm[0].length() > 0);

        String[] one = rm.generate(3, List.of("I"), merge(o, "numSentences", 1));
        assertEquals(1, one.length);
        assertTrue(one[0].length() > 0);

        String[] two = rm.generate(3, List.of("I"), merge(o, "numSentences", 2));
        assertEquals(2, two.length);
        for (String s : two) {
            assertTrue(s.length() > 0);
        }

        String[] three = rm.generate(3, List.of("I"), opts("numSentences", 3));
        assertEquals(3, three.length);
    }

    @Test
    void riMarkovCompletionsSingleArray() {
        RiMarkov rm = new RiMarkov(exampleStr);
        List<String> nexts = rm.completions(List.of("The", "brown"));
        assertInstanceOf(List.class, (Object) nexts);
        assertTrue(nexts.contains("fox"));
        assertTrue(nexts.contains("dog"));
        for (String t : nexts) {
            assertTrue(!re(t, "^<.*>$"));
        }
        assertEquals(2, nexts.size());

        assertEquals(List.of("jumps"), rm.completions(List.of("brown", "fox")));
        assertEquals(List.of(), rm.completions(List.of("never", "seen")));

        List<String> nextsSpecial = rm.completions(List.of("dog", "."), null, opts("allowSpecial", true));
        assertTrue(nextsSpecial.contains(SuffixArray.SEQ_END_TOKEN));

        for (String t : rm.completions(List.of("dog", "."))) {
            assertTrue(!re(t, "^<.*>$"));
        }

        RiMarkov rm2 = new RiMarkov(sample);
        rm2.n = 4;
        assertEquals(List.of("to"), rm2.completions(List.of("people", "lie", "is")));
        assertEquals(List.of("to"), rm2.completions(List.of("One", "reason", "people", "lie", "is")));
        assertEquals(List.of(".", "is"), rm2.completions(List.of("personal", "power")));
        assertEquals(List.of("confident"), rm2.completions(List.of("to", "be", "more")));
        List<String> iCompletions = rm2.completions(List.of("I"));
        for (String w : List.of("did", "claimed", "had", "said", "could", "wanted", "also", "achieved", "embarrassed")) {
            assertTrue(iCompletions.contains(w));
        }
        assertEquals(List.of(), rm2.completions(List.of("XXX")));
    }

    @Test
    void riMarkovCompletionsTwoArrays() {
        RiMarkov rm = new RiMarkov(exampleStr);
        rm.n = 4;
        List<String> middle = rm.completions(List.of("The"), List.of("fox"));
        assertInstanceOf(List.class, (Object) middle);
        assertTrue(middle.contains("brown"));
        for (String t : middle) {
            assertTrue(!re(t, "^<.*>$"));
        }
        assertTrue(rm.completions(List.of("The"), List.of("fox"), opts("allowSpecial", true)).contains("brown"));

        RiMarkov rm2 = new RiMarkov(sample2);
        rm2.n = 4;
        assertEquals(List.of("did"), rm2.completions(List.of("I"), List.of("not")));
        assertEquals(List.of("personal"), rm2.completions(List.of("achieve"), List.of("power")));
        assertEquals(List.of("personal"), rm2.completions(List.of("to", "achieve"), List.of("power")));
        assertEquals(List.of("not", "occasionally"), rm2.completions(List.of("I", "did")));
        assertEquals(List.of("not", "occasionally"), rm2.completions(List.of("I", "did"), List.of("want")));

        assertThrows(Exception.class, () ->
            rm2.completions(List.of("I", "did", "not", "occasionally"), List.of("want")));
    }

    @Test
    void riMarkovGenerateRestart2() {
        List<String> sents = List.of("asdfasdf-", "asqwerqwer+", "aqadaqdf*");
        Function<String, List<String>> tokenize = s -> chars(s);
        Function<List<String>, String> untokenize = l -> String.join("", l);

        RiMarkov rm = new RiMarkov(4, opts("tokenize", tokenize, "untokenize", untokenize));
        rm.addSentences(sents).build();
        assertEquals(List.of("a"), new ArrayList<>(rm.model.suffixes.startIndexDist().keySet()));

        for (int i = 0; i < 10; i++) {
            String result = str(rm.generate(2, List.of("a", "s"), opts("maxTokens", 20)));
            assertTrue(re(result, "^as[a-z]+[-+*]$"));
        }
    }

    @Test
    void riMarkovGenerate() {
        RiMarkov rm = new RiMarkov(exampleStr);
        rm.n = 3;
        String text = str(rm.generate(3, List.of("The", "brown"), opts("minTokens", 2, "maxTokens", 10)));
        assertInstanceOf(String.class, (Object) text);
        assertTrue(text.length() > 0);
        assertTrue(text.startsWith("The brown"));

        rm.n = 3;
        String text2 = str(rm.generate(List.of("The", "brown"), opts("minTokens", 2, "maxTokens", 10)));
        assertInstanceOf(String.class, (Object) text2);
        assertTrue(text2.length() > 0);
        assertTrue(text2.startsWith("The brown"));

        assertThrows(Exception.class, () -> rm.generate(3, "The brown", Map.of()));

        RiMarkov rm2 = new RiMarkov(exampleStr);
        assertThrows(Exception.class, () -> rm2.generate(null, List.of("The"), Map.of()));
    }

    @Test
    @Disabled
    void riMarkovProbability() {
        RiMarkov rm = new RiMarkov(exampleStr);
        assertEquals(0, rm.probability(List.of("xyz")));
        assertTrue(rm.probability(List.of("the")) > 0);
        assertTrue(rm.probability(List.of("the")) > rm.probability(List.of("fox")));
        double pSeq1 = rm.probability(List.of("The", "brown"));
        double pSeq2 = rm.probability(List.of("The", "brown", "fox"));
        assertTrue(pSeq1 > 0);
        assertTrue(pSeq2 > 0);
        assertTrue(pSeq1 > pSeq2);
        assertEquals(0, rm.probability(List.of("brown", "fox", "lazy")));
        assertEquals(0.5, rm.probability(List.of("The", "brown"), "fox"), 0.01);
        assertEquals(0.5, rm.probability(List.of("The", "brown"), "dog"), 0.01);
        assertTrue(rm.probability(List.of("The", "brown"), List.of("fox", "jumps")) > 0);
        assertEquals(0, rm.probability(List.of("The", "brown"), "xyz"));
        assertTrue(rm.probability(List.of(), List.of("The")) > 0);
        assertThrows(Exception.class, () -> rm.probability("not-an-array", "token"));

        RiMarkov rm2 = new RiMarkov("the dog ate the boy the");
        assertEquals(3.0 / rm2.model.suffixes.length, rm2.probability("the"), 1e-9);
        assertEquals(1.0 / rm2.model.suffixes.length, rm2.probability("dog"), 1e-9);
        assertEquals(0, rm2.probability("cat"));

        RiMarkov rm3 = new RiMarkov("the dog ate the boy that the dog found.");
        assertEquals(3.0 / rm3.model.suffixes.length, rm3.probability("the"), 1e-9);
        assertEquals(2.0 / rm3.model.suffixes.length, rm3.probability("dog"), 1e-9);
        assertEquals(0, rm3.probability("cat"));

        RiMarkov rm4 = new RiMarkov(sample);
        assertEquals(0, rm4.probability("Non-exist"));
        assertEquals(0, rm4.probability(List.of()));
        assertTrue(rm4.probability(Arrays.asList("personal", "power", "is")) > 0);
        assertEquals(0, rm4.probability(Arrays.asList("personal", "powXer", "is")));
    }

    @Test
    void riMarkovProbabilities() {
        RiMarkov rm = new RiMarkov(exampleStr);
        Map<String, Double> dist = rm.probabilities(List.of("The", "brown"));
        assertTrue(dist.containsKey("fox"));
        assertTrue(dist.containsKey("dog"));
        for (String t : dist.keySet()) {
            assertTrue(!re(t, "^<.*>$"));
        }
        assertEquals(1.0, sum(dist), 1e-9);
        for (double p : dist.values()) {
            assertTrue(p > 0);
        }

        Map<String, Double> dist2 = rm.probabilities(List.of("brown", "fox"));
        assertEquals(List.of("jumps"), new ArrayList<>(dist2.keySet()));
        assertEquals(1.0, dist2.get("jumps"), 1e-9);

        assertEquals(Map.of(), rm.probabilities(List.of("never", "seen")));
        assertTrue(rm.probabilities(List.of("dog", "."), opts("allowSpecial", true))
            .containsKey(SuffixArray.SEQ_END_TOKEN));
        for (String t : rm.probabilities(List.of("dog", ".")).keySet()) {
            assertTrue(!re(t, "^<.*>$"));
        }

        Map<String, Double> startDist = rm.probabilities();
        assertTrue(startDist.keySet().size() > 0);
        for (String t : startDist.keySet()) {
            assertTrue(!re(t, "^<.*>$"));
        }
        assertThrows(Exception.class, () -> rm.probabilities((Object) "not-an-array"));

        RiMarkov rm2 = new RiMarkov(sample);
        assertEquals(Map.of("people", 1.0), rm2.probabilities(List.of("reason")));
        assertEquals(Map.of("lie", 1.0), rm2.probabilities(List.of("people")));
        assertEquals(Map.of("power", 1.0), rm2.probabilities(List.of("personal")));
        Map<String, Double> theProbs = rm2.probabilities(List.of("the"));
        assertEquals(List.of("party", "time"), sortedKeys(theProbs));
        assertEquals(1.0, theProbs.get("time") + theProbs.get("party"), 1e-9);
        Map<String, Double> isProbs = rm2.probabilities(List.of("is"));
        assertEquals(List.of(".", "helpful", "to"), sortedKeys(isProbs));
        assertEquals(1.0, sum(isProbs), 1e-9);
        assertEquals(Map.of(), rm2.probabilities(List.of("XXX")));

        RiMarkov rm3 = new RiMarkov(sample2);
        assertEquals(Map.of("to", 1.0), rm3.probabilities(List.of("people", "lie", "is")));
        Map<String, Double> pp = rm3.probabilities(List.of("personal", "power"));
        assertEquals(List.of(".", "is"), sortedKeys(pp));
        assertEquals(1.0, pp.get(".") + pp.get("is"), 1e-9);
        assertEquals(Map.of("confident", 1.0), rm3.probabilities(List.of("to", "be", "more")));
        assertEquals(Map.of(), rm3.probabilities(List.of("XXX")));
        assertEquals(Map.of(), rm3.probabilities(List.of("personal", "XXX")));
        Map<String, Double> didProbs = rm3.probabilities(List.of("I", "did"));
        assertEquals(List.of("not", "occasionally"), sortedKeys(didProbs));
        assertEquals(1.0, didProbs.get("not") + didProbs.get("occasionally"), 1e-9);
        assertTrue(didProbs.get("not") > didProbs.get("occasionally"));
    }

    @Test
    void riMarkovConstructorSentencesOption() {
        String[] sents = RiTa.sentences(exampleStr);
        RiMarkov rm = new RiMarkov((Object) opts("sentences", Arrays.asList(sents)));
        assertTrue(rm.size() > 0);

        RiMarkov rm2 = new RiMarkov();
        rm2.addSentences(Arrays.asList(sents));
        assertEquals(rm.size(), rm2.size());
    }

    @Test
    void riMarkovGenerateOptsOnlyForm() {
        RiMarkov rm = new RiMarkov(sample);
        String[] result = rm.generate(opts("n", 3, "prompt", List.of("I"), "minTokens", 3, "maxTokens", 20));
        assertEquals(1, result.length);
        assertTrue(result[0].length() > 0);

        RiMarkov rm2 = new RiMarkov(exampleStr);
        String[] result2 = rm2.generate(opts("n", 3, "prompt", List.of("The", "brown"), "minTokens", 2, "maxTokens", 10));
        assertEquals(1, result2.length);
        assertTrue(result2[0].length() > 0);
        assertTrue(result2[0].startsWith("The brown"));

        RiMarkov rm3 = new RiMarkov(exampleStr);
        assertThrows(Exception.class, () -> rm3.generate(opts("prompt", List.of("The"))));
    }

    @Test
    void riMarkovToString() {
        RiMarkov rm = new RiMarkov(exampleStr);
        String str = rm.toString();
        assertInstanceOf(String.class, (Object) str);
        assertTrue(str.length() > 0);
    }

    @Test
    void riMarkovStream() {
        RiMarkov rm = new RiMarkov(exampleStr);
        rm.n = 3;
        Iterable<String> gen = rm.stream(3, List.of("The", "brown"), opts("maxTokens", 10));
        assertInstanceOf(Iterable.class, gen);

        List<String> tokens = drain(rm.stream(3, List.of("The", "brown"), opts("maxTokens", 10)));
        assertTrue(tokens.size() > 0);
        for (String t : tokens) {
            assertInstanceOf(String.class, (Object) t);
        }
        Set<String> specials = new HashSet<>(List.of(SuffixArray.SEQ_START_TOKEN, SuffixArray.SEQ_END_TOKEN));
        for (String t : tokens) {
            assertTrue(!specials.contains(t));
        }

        List<String> capped = drain(rm.stream(3, List.of("The"), opts("maxTokens", 3)));
        assertTrue(capped.size() <= 3);

        List<String> tokens2 = drain(rm.stream(List.of("The", "brown"), opts("maxTokens", 10)));
        assertTrue(tokens2.size() > 0);

        List<String> tokens3 = drain(rm.stream(opts("n", 3, "prompt", List.of("The", "brown"), "maxTokens", 10)));
        assertTrue(tokens3.size() > 0);

        List<String> toStop = drain(rm.stream(3, List.of("The", "brown"), opts("maxTokens", 20, "generateUntil", ".")));
        assertEquals(".", toStop.get(toStop.size() - 1));

        List<String> toPred = drain(rm.stream(3, List.of("The", "brown"),
            opts("maxTokens", 20, "generateUntil", (Predicate<String>) t -> t.equals("."))));
        assertEquals(".", toPred.get(toPred.size() - 1));

        assertThrows(Exception.class, () -> drain(rm.stream(3, "not an array", Map.of())));

        RiMarkov rm2 = new RiMarkov(exampleStr);
        assertThrows(Exception.class, () -> drain(rm2.stream(opts("prompt", List.of("The")))));
    }

    @Test
    void shouldBeReproducibleWithRandomSeed() {
        String text = "The cat sat on the mat. The dog ran in the park. A bird flew "
            + "over the house. The fish swam in the pond. The horse ran through the "
            + "field. The mouse hid in the wall. The cat chased the mouse. The dog "
            + "chased the cat. The bird ate the fish.";
        try {
            List<String> one = gen(text, 1);
            List<String> two = gen(text, 1);
            List<String> other = gen(text, 7);
            assertEquals(one, two);
            assertNotEquals(one, other);
        } finally {
            RiTa.randomSeed((int) (System.currentTimeMillis()));
        }
    }

    private static List<String> gen(String text, int seed) {
        RiTa.randomSeed(seed);
        RiMarkov rm = new RiMarkov(2);
        rm.addText(text);
        return list(rm.generate(opts("numSentences", 3, "maxLength", 12)));
    }

    @Test
    void shouldHonorMaxBacktracks() {
        RiMarkov rm = new RiMarkov(3, opts("maxBacktracks", 50));
        assertEquals(50, ((Number) rm.opts.get("maxBacktracks")).intValue());
        BackoffModel.resolveOpts(3, opts("maxBacktracks", 50));
        assertEquals(50, ((Number) BackoffModel.resolveOpts(3, opts("maxBacktracks", 50)).get("maxBacktracks")).intValue());
    }

    @Test
    void shouldBuildWithVerboseEnabled() {
        RiMarkov rm = new RiMarkov(2);
        rm.addText("The quick brown fox jumped over the lazy dog. The lazy dog slept. The dog ran.");
        rm.model.build(opts("verbose", true));
    }

    // ---------------- helpers ----------------

    private static void markovEquals(RiMarkov rm, RiMarkov copy) {
        assertEquals(rm.n, copy.n);
        assertEquals(rm.size(), copy.size());
    }

    /** First sentence of a generate() result (the single-sentence convenience). */
    private static String str(String[] result) {
        return result.length == 0 ? "" : result[0];
    }

    private static List<String> list(String[] result) {
        return Arrays.asList(result);
    }

    private static List<String> drain(Iterable<String> it) {
        List<String> out = new ArrayList<>();
        for (String s : it) {
            out.add(s);
        }
        return out;
    }

    private static List<String> chars(String s) {
        List<String> out = new ArrayList<>();
        for (int i = 0; i < s.length(); i++) {
            out.add(String.valueOf(s.charAt(i)));
        }
        return out;
    }

    private static boolean re(String s, String regex) {
        return Pattern.compile(regex).matcher(s).find();
    }

    private static List<String> matchAll(String text, String regex) {
        List<String> out = new ArrayList<>();
        Matcher m = Pattern.compile(regex).matcher(text);
        while (m.find()) {
            out.add(m.group());
        }
        return out;
    }

    private static double sum(Map<String, Double> m) {
        double s = 0;
        for (double v : m.values()) {
            s += v;
        }
        return s;
    }

    private static List<String> sortedKeys(Map<String, Double> m) {
        List<String> keys = new ArrayList<>(m.keySet());
        Collections.sort(keys);
        return keys;
    }

    private static Map<String, Object> merge(Map<String, Object> base, Object... extra) {
        return TestReflect.merge(base, extra);
    }
}
