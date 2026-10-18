package rita;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;

/**
 * Loads the shared test fixtures staged onto the test classpath by {@code syncFixtures}
 * (see java/build.gradle.kts). The canonical copies live in <code>shared/</code> so the JS
 * and Java suites are driven by byte-identical data.
 */
final class Fixtures {

    private Fixtures() {
    }

    /**
     * Reads a fixture from <code>fixtures/&lt;name&gt;.json</code> on the test classpath.
     *
     * @param name the fixture name, e.g. {@code "stemmer-fixtures"}
     * @return the parsed object
     */
    static JsonObject read(String name) {
        JsonElement root = readTree(name);
        if (!root.isJsonObject()) {
            throw new IllegalStateException("Fixture " + name + " is not a JSON object");
        }
        return root.getAsJsonObject();
    }

    /**
     * Reads a fixture whose top-level value is a JSON array (e.g. harvard-data.json).
     *
     * @param name the fixture name
     * @return the parsed array
     */
    static JsonArray readArray(String name) {
        JsonElement root = readTree(name);
        if (!root.isJsonArray()) {
            throw new IllegalStateException("Fixture " + name + " is not a JSON array");
        }
        return root.getAsJsonArray();
    }

    private static JsonElement readTree(String name) {
        String path = "fixtures/" + name + ".json";
        try (InputStream in = Fixtures.class.getClassLoader().getResourceAsStream(path)) {
            if (in == null) {
                throw new IllegalStateException(
                    "Fixture not found on classpath: " + path + " (is the syncFixtures task running?)");
            }
            try (Reader reader = new InputStreamReader(in, StandardCharsets.UTF_8)) {
                return JsonParser.parseReader(reader);
            }
        } catch (IOException e) {
            throw new UncheckedIOException("Failed to read fixture " + path, e);
        }
    }

    /** Returns the [input, expected] pairs of a named stem block. */
    static JsonArray pairs(JsonObject fixture, String blockName) {
        for (var element : fixture.getAsJsonArray("stem")) {
            JsonObject block = element.getAsJsonObject();
            if (blockName.equals(block.get("name").getAsString())) {
                return block.getAsJsonArray("pairs");
            }
        }
        throw new IllegalStateException("No stem block named '" + blockName + "' in fixture");
    }
}
