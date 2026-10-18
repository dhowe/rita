package rita;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.stream.Stream;
import org.junit.jupiter.api.Test;

/**
 * Ported from <code>js/test/stemmer-tests.js</code>.
 *
 * <p>The JS suite contains ~6400 lines of {@code test("word", "stem")} calls. Per the agreed
 * approach those pairs are extracted verbatim into
 * <code>shared/stemmer-fixtures.json</code> (see <code>scripts/gen-stemmer-fixtures.js</code>)
 * and driven from data here, so both implementations assert the identical word/stem pairs in
 * the identical order, grouped by the identical block names.
 *
 * <p>The JS helper {@code function test(i, o) { expect(RiTa.stem(i)).eq(o); }} maps to the
 * loop body below; each pair is one assertion, exactly as in JS.
 */
class StemmerTest {

    @Test
    void shouldTestStem1() {
        assertStemBlock("Should test stem1");
    }

    @Test
    void shouldTestStem2() {
        assertStemBlock("Should test stem2");
    }

    /**
     * Guards the data-driven port: the fixture must contain exactly the pairs present in
     * <code>js/test/stemmer-tests.js</code>, so the Java suite can never silently drift from
     * the JS source of truth.
     */
    @Test
    void fixtureCoversEveryJsAssertion() throws IOException {
        Path jsSource = findJsSource();
        long jsCount;
        try (Stream<String> lines = Files.lines(jsSource, StandardCharsets.UTF_8)) {
            jsCount = lines
                .filter((line) -> line.matches("^\\s*test\\(\"(?:[^\"\\\\]|\\\\.)*\",\\s*\"(?:[^\"\\\\]|\\\\.)*\"\\);?\\s*$"))
                .count();
        }

        JsonObject fixture = Fixtures.read("stemmer-fixtures");
        long fixtureCount = 0;
        for (var block : fixture.getAsJsonArray("stem")) {
            fixtureCount += block.getAsJsonObject().getAsJsonArray("pairs").size();
        }
        assertEquals(jsCount, fixtureCount,
            "shared/stemmer-fixtures.json is stale; re-run scripts/gen-stemmer-fixtures.js");
    }

    @Test
    void shouldCallStemAll() {
        JsonObject stemAll = Fixtures.read("stemmer-fixtures").getAsJsonObject("stemAll");
        String[] input = toStringArray(stemAll.getAsJsonArray("input"));
        String[] expected = toStringArray(stemAll.getAsJsonArray("expected"));
        String[] output = RiTa.Stemmer.stemAll(input);
        for (int i = 0; i < input.length; i++) {
            assertEquals(expected[i], output[i], "stemAll(" + input[i] + ")");
        }
    }

    private static String[] toStringArray(JsonArray array) {
        String[] result = new String[array.size()];
        for (int i = 0; i < result.length; i++) {
            result[i] = array.get(i).getAsString();
        }
        return result;
    }

    /** Asserts every [input, expected] pair of the named block, in order. */
    private static void assertStemBlock(String blockName) {
        JsonArray pairs = Fixtures.pairs(Fixtures.read("stemmer-fixtures"), blockName);
        for (int i = 0; i < pairs.size(); i++) {
            JsonArray pair = pairs.get(i).getAsJsonArray();
            String input = pair.get(0).getAsString();
            String expected = pair.get(1).getAsString();
            assertEquals(expected, RiTa.stem(input), "stem(\"" + input + "\") at index " + i);
        }
    }

    /**
     * Locates js/test/stemmer-tests.js relative to the java project directory, so the
     * parity guard works from either the repo root or the java/ directory.
     */
    private static Path findJsSource() {
        Path dir = Path.of("").toAbsolutePath();
        for (int i = 0; i < 4 && dir != null; i++, dir = dir.getParent()) {
            Path candidate = dir.resolve("js").resolve("test").resolve("stemmer-tests.js");
            if (Files.exists(candidate)) {
                return candidate;
            }
        }
        throw new UncheckedIOException(new IOException(
            "Could not locate js/test/stemmer-tests.js from " + Path.of("").toAbsolutePath()));
    }
}
