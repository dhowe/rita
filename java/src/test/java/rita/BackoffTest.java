package rita;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static rita.TestReflect.fieldOf;
import static rita.TestReflect.opts;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.function.Predicate;
import org.junit.jupiter.api.Test;

/**
 * Ported from <code>js/test/backoff-tests.js</code>.
 *
 * <p>Mapping notes:
 * <ul>
 *   <li>JS generator objects ({@code pathGenerator}, {@code streamTokens}) map to
 *       {@link Iterator}; {@code [...gen]} becomes {@link #drain}; {@code gen.next().done}
 *       maps to {@code hasNext()}.</li>
 *   <li>JS path records {@code {tokens:[{token,prob}], prob, inInput}} map to
 *       {@code Map<String,Object>}.</li>
 *   <li>JS option objects -> {@link #opts}; {@code {...base, k:v}} -> {@code merge}.</li>
 *   <li>Custom tokenizer/untokenizer functions -> {@link Function} lambdas (unused by the
 *       stub, which throws before invoking them).</li>
 * </ul>
 */
class BackoffTest {

    private static final String exampleStr = TestData.EXAMPLE_STR;
    private static final List<String> exampleTokens = TestData.EXAMPLE_TOKENS;
    private static final String sample = TestData.SAMPLE;

    @Test
    void backoffModelConstructor() {
        BackoffModel lm1 = new BackoffModel(exampleTokens);
        assertInstanceOf(BackoffModel.class, lm1);
        assertInstanceOf(SuffixArray.class, lm1.suffixes);
        assertEquals(21, lm1.size());

        BackoffModel lm2 = new BackoffModel(exampleStr);
        assertInstanceOf(BackoffModel.class, lm2);
        assertInstanceOf(SuffixArray.class, lm2.suffixes);
        assertEquals(21, lm2.size());

        assertThrows(Exception.class, () -> new BackoffModel(4));
        // JS `new BackoffModel([sentences])` is a 2-D array (one nested array); Java's
        // List.of(String[]) spreads to 1-D, so wrap as a single Object element to mirror JS.
        assertThrows(Exception.class, () -> new BackoffModel(List.of((Object) RiTa.sentences(exampleStr))));
    }

    @Test
    @SuppressWarnings("unchecked")
    void backoffModelSuffixesFind() {
        BackoffModel lm = new BackoffModel(exampleStr + " Then we ate.");
        SuffixArray sa = lm.suffixes;
        int[] mm = sa.find(List.of("T"), opts("debug", 0));
        assertEquals(0, mm[1] - mm[0]);

        mm = sa.find(List.of("The"), opts("debug", 0));
        assertEquals(2, mm[1] - mm[0]);
    }

    @Test
    void backoffModelJson() {
        BackoffModel bom = new BackoffModel(exampleStr);
        BackoffModel copy = BackoffModel.fromJSON(bom.toJSON());

        assertEquals(bom.tokenCount, copy.tokenCount);
        assertEquals(bom.tokens, copy.tokens);
        assertInstanceOf(BackoffModel.class, copy);
        assertEquals(keysOfSuffixes(bom), keysOfSuffixes(copy));

        for (String f : Model.options) {
            assertTrue(fieldOf(copy, f) != null, f);
            assertEquals(fieldOf(bom, f), fieldOf(copy, f), f);
        }
        for (String f : SuffixArray.__dict__) {
            Object b = fieldOf(bom.suffixes, f);
            Object c = fieldOf(copy.suffixes, f);
            assertTrue(c != null, f);
            assertDeep(c, b, f);
        }
    }

    @Test
    @SuppressWarnings("unchecked")
    void backoffModelGenerationPaths() {
        BackoffModel lm = new BackoffModel(exampleStr);
        List<String> prompt = List.of("The", "brown");
        Map<String, Object> base = opts("minLength", 1, "maxLength", 10);

        List<Map<String, Object>> paths = lm.generationPaths(3, prompt, base);
        assertInstanceOf(List.class, paths);
        assertTrue(paths.size() > 0);

        for (Map<String, Object> p : paths) {
            List<Map<String, Object>> tokens = (List<Map<String, Object>>) p.get("tokens");
            assertTrue(tokens.size() > prompt.size());
            double prob = ((Number) p.get("prob")).doubleValue();
            assertTrue(prob > 0);
            assertInstanceOf(Boolean.class, p.get("inInput"));
            for (int i = 0; i < prompt.size(); i++) {
                assertEquals(prompt.get(i), tokens.get(i).get("token"));
            }
        }

        double total = 0;
        for (Map<String, Object> p : paths) {
            total += ((Number) p.get("prob")).doubleValue();
        }
        assertEquals(1.0, total, 1e-9);

        List<Object> firstGenTokens = new ArrayList<>();
        for (Map<String, Object> p : paths) {
            List<Map<String, Object>> tokens = (List<Map<String, Object>>) p.get("tokens");
            firstGenTokens.add(tokens.get(prompt.size()).get("token"));
        }
        assertTrue(firstGenTokens.contains("fox"));
        assertTrue(firstGenTokens.contains("dog"));

        List<Map<String, Object>> sorted = lm.generationPaths(3, prompt, merge(base, "sortByProb", true));
        for (int i = 1; i < sorted.size(); i++) {
            double prev = ((Number) sorted.get(i - 1).get("prob")).doubleValue();
            double cur = ((Number) sorted.get(i).get("prob")).doubleValue();
            assertTrue(prev >= cur);
        }

        List<Map<String, Object>> origPaths = lm.generationPaths(3, prompt, merge(base, "forceOriginal", true));
        for (Map<String, Object> p : origPaths) {
            assertFalse((Boolean) p.get("inInput"));
        }
    }

    @Test
    @SuppressWarnings("unchecked")
    void backoffModelPathGenerator() {
        BackoffModel lm = new BackoffModel(exampleStr);
        List<String> prompt = List.of("The", "brown");
        Map<String, Object> base = opts("minLength", 1, "maxLength", 10);

        List<Map<String, Object>> generated = new ArrayList<>();
        Iterator<Map<String, Object>> gen = lm.pathGenerator(3, prompt, base);
        while (gen.hasNext()) {
            generated.add(gen.next());
        }
        assertTrue(generated.size() > 0);

        List<Map<String, Object>> allPaths = lm.generationPaths(3, prompt, base);
        assertEquals(allPaths.size(), generated.size());

        for (Map<String, Object> e : generated) {
            List<Map<String, Object>> tokens = (List<Map<String, Object>>) e.get("tokens");
            assertTrue(tokens.size() > prompt.size());
            assertTrue(((Number) e.get("prob")).doubleValue() > 0);
            for (int i = 0; i < prompt.size(); i++) {
                assertEquals(prompt.get(i), tokens.get(i).get("token"));
            }
        }

        Iterator<Map<String, Object>> gen2 = lm.pathGenerator(3, prompt, base);
        assertTrue(gen2.hasNext());
        assertInstanceOf(List.class, gen2.next().get("tokens"));

        BackoffModel lm2 = new BackoffModel(sample);
        List<String> samplePrompt = List.of("I", "did", "not");
        // should not throw — there are original continuations
        Iterator<Map<String, Object>> g = lm2.pathGenerator(3, samplePrompt, merge(base, "forceOriginal", true));
        g.next();
    }

    @Test
    void backoffModelStreamTokens() {
        BackoffModel lm = new BackoffModel(sample);
        List<String> prompt = List.of("I", "did", "not");
        Map<String, Object> base = opts("minLength", 4, "maxLength", 20);

        List<String> tokens = drain(lm.streamTokens(3, prompt, base));
        assertInstanceOf(List.class, tokens);
        assertTrue(tokens.size() >= 4);
        assertTrue(tokens.size() <= 20);
        for (String t : tokens) {
            assertInstanceOf(String.class, t);
        }

        tokens = drain(lm.streamTokens(3, prompt, merge(base, "allowSpecial", true)));
        assertEquals(SuffixArray.SEQ_END_TOKEN, tokens.get(tokens.size() - 1));

        tokens = drain(lm.streamTokens(3, prompt, merge(base, "generateUntil", ".")));
        assertEquals(".", tokens.get(tokens.size() - 1));

        tokens = drain(lm.streamTokens(3, prompt,
            merge(base, "generateUntil", (Predicate<String>) t -> t.equals("."))));
        assertEquals(".", tokens.get(tokens.size() - 1));

        tokens = drain(lm.streamTokens(3, prompt, merge(base, "minLength", 3,
            "generateUntil", (Predicate<String>) t -> t.equals("be") || t.equals("girlfriend"))));
        assertTrue(List.of("be", "girlfriend").contains(tokens.get(tokens.size() - 1)));

        for (int i = 0; i < 5; i++) {
            tokens = drain(lm.streamTokens(3, prompt, opts("minLength", 1, "maxLength", 5)));
            assertTrue(tokens.size() <= 5);
            assertTrue(List.of("have", "want").contains(tokens.get(0)));
        }
    }

    @Test
    void backoffModelStreamTokensMaxLengthMatch() {
        BackoffModel lm = new BackoffModel(sample);
        List<String> prompt = List.of("I", "did", "not");
        Map<String, Object> base = opts("minLength", 4, "maxLength", 20);

        assertThrows(Exception.class, () ->
            drain(lm.streamTokens(4, prompt, merge(base, "maxLengthMatch", 3))));

        List<String> free = drain(lm.streamTokens(3, prompt,
            merge(base, "maxLengthMatch", Double.POSITIVE_INFINITY)));
        assertTrue(free.size() >= 4);

        int n = 3, mlm = 5;
        for (int i = 0; i < 10; i++) {
            List<String> tokens = drain(lm.streamTokens(n, prompt, merge(base, "maxLengthMatch", mlm)));
            assertInstanceOf(List.class, tokens);
            List<String> full = new ArrayList<>(prompt);
            full.addAll(tokens);
            for (int j = prompt.size() - 1; j <= full.size() - (mlm + 1); j++) {
                String windowStr = String.join(" ", full.subList(j, j + mlm + 1));
                assertTrue(!sample.contains(windowStr), "verbatim window found: \"" + windowStr + "\"");
            }
        }
    }

    @Test
    void backoffModelGenerateSentences() {
        BackoffModel lm = new BackoffModel(sample);
        List<String> prompt = List.of("I");
        Map<String, Object> base = opts("minLength", 3, "maxLength", 20);

        List<String> three = lm.generateSentences(3, prompt, base);
        assertInstanceOf(List.class, three);
        assertEquals(2, three.size());
        for (String s : three) {
            assertInstanceOf(String.class, s);
            assertTrue(s.length() > 0);
        }

        List<String> two = lm.generateSentences(3, prompt, merge(base, "numSentences", 2));
        assertEquals(2, two.size());
        for (String s : two) {
            assertInstanceOf(String.class, s);
            assertTrue(s.length() > 0);
        }

        List<String> one = lm.generateSentences(3, prompt, merge(base, "numSentences", 1));
        assertEquals(1, one.size());
        assertInstanceOf(String.class, one.get(0));
        assertTrue(one.get(0).length() > 0);

        for (String s : three) {
            for (String t : RiTa.tokenize(s)) {
                assertTrue(!t.equals(SuffixArray.SEQ_START_TOKEN) && !t.equals(SuffixArray.SEQ_END_TOKEN));
            }
        }
    }

    @Test
    void backoffModelGenerationPathsOptions() {
        BackoffModel lm = new BackoffModel(exampleStr);
        List<String> prompt = List.of("The", "brown");
        Map<String, Object> base = opts("minLength", 1, "maxLength", 10);

        List<Map<String, Object>> narrow = lm.generationPaths(3, prompt, merge(base, "topK", 1));
        assertInstanceOf(List.class, narrow);
        assertTrue(narrow.size() > 0);
        for (Map<String, Object> p : narrow) {
            assertInstanceOf(List.class, p.get("tokens"));
            assertTrue(((Number) p.get("prob")).doubleValue() > 0);
        }

        List<Map<String, Object>> shallow = lm.generationPaths(3, prompt, merge(base, "depth", 2));
        List<Map<String, Object>> deep = lm.generationPaths(3, prompt, merge(base, "depth", 20));
        assertInstanceOf(List.class, shallow);
        assertTrue(shallow.size() <= deep.size() + 1);

        // temp: valid values do not throw
        lm.generationPaths(3, prompt, merge(base, "temp", 0.5));
        lm.generationPaths(3, prompt, merge(base, "temp", 2.0));

        assertThrows(Exception.class, () -> lm.generationPaths(3, prompt, merge(base, "badKey", true)));
        assertThrows(Exception.class, () -> lm.streamTokens(3, prompt, merge(base, "badKey", true)).next());
    }

    // ---------------- helpers ----------------

    private static List<String> drain(Iterator<String> it) {
        List<String> out = new ArrayList<>();
        while (it.hasNext()) {
            out.add(it.next());
        }
        return out;
    }

    private static List<String> keysOfSuffixes(BackoffModel m) {
        return TestReflect.keysOf(m.suffixes);
    }

    private static Map<String, Object> merge(Map<String, Object> base, Object... extra) {
        return TestReflect.merge(base, extra);
    }

    private static void assertDeep(Object a, Object b, String msg) {
        if (a instanceof int[] && b instanceof int[]) {
            org.junit.jupiter.api.Assertions.assertArrayEquals((int[]) a, (int[]) b, msg);
        } else {
            assertEquals(a, b, msg);
        }
    }
}
