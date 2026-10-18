package rita;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertArrayEquals;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import org.junit.jupiter.api.Test;

/**
 * Ported from <code>js/test/harvard-tests.js</code>. Driven by the shared Harvard fixture
 * (720 sentences, each {@code [sentence, tokens, tags, ipa, phones]}), so both implementations
 * assert against byte-identical data.
 *
 * <p>The JS suite counts mismatches across all sentences and asserts the count is zero; the
 * same accumulation is preserved here so a single bad sentence fails with the JS-style message.
 */
class HarvardTest {

    @Test
    void shouldTokenizeAndUntokenizeAllSentencesWithoutLoss() {
        JsonArray data = Fixtures.readArray("harvard-data");
        int mismatches = 0;
        for (int i = 0; i < data.size(); i++) {
            String s = data.get(i).getAsJsonArray().get(0).getAsString();
            String result = RiTa.untokenize(RiTa.tokenize(s));
            if (!result.equals(s)) {
                mismatches++;
            }
        }
        assertEquals(0, mismatches, mismatches + " tokenize/untokenize mismatches");
    }

    @Test
    void shouldAssignCorrectPosTagsToAllSentences() {
        JsonArray data = Fixtures.readArray("harvard-data");
        int mismatches = 0;
        for (int i = 0; i < data.size(); i++) {
            JsonArray row = data.get(i).getAsJsonArray();
            String[] expectedToks = toStringArray(row.get(1).getAsJsonArray());
            String[] expectedTags = toStringArray(row.get(2).getAsJsonArray());
            String[] actualToks = RiTa.tokenize(row.get(0).getAsString());
            // verify tokens (one assertion per sentence, as in JS)
            assertArrayEquals(expectedToks, actualToks, "sentence " + (i + 1) + " tokens");
            String[] actualTags = RiTa.pos(actualToks);
            if (!java.util.Arrays.equals(actualTags, expectedTags)) {
                mismatches++;
            }
        }
        assertEquals(0, mismatches, mismatches + " POS tag mismatches");
    }

    @Test
    void shouldProduceCorrectPhonemesForAllSentences() {
        JsonArray data = Fixtures.readArray("harvard-data");
        int mismatches = 0;
        RiTa.SILENCE_LTS = true;
        for (int i = 0; i < data.size(); i++) {
            JsonArray row = data.get(i).getAsJsonArray();
            String sentence = row.get(0).getAsString();
            String expectedIpa = row.get(3).getAsString();
            String s = sentence.replaceAll("[.!?,]+$", "");
            String actualIpa = "/" + Analyzer.syllablesToIpa(RiTa.syllables(s), RiTa.stresses(s)) + "/";
            if (!actualIpa.equals(expectedIpa)) {
                mismatches++;
            }
        }
        assertEquals(0, mismatches, mismatches + " phoneme mismatches");
        RiTa.SILENCE_LTS = false;
    }

    private static String[] toStringArray(JsonArray array) {
        String[] result = new String[array.size()];
        for (int i = 0; i < result.length; i++) {
            result[i] = array.get(i).getAsString();
        }
        return result;
    }
}
