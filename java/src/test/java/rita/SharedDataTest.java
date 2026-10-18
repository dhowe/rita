package rita;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

/**
 * Verifies the shared-data pipeline: {@code shared/rita_dict.json} must be staged onto
 * the classpath at {@code rita/rita_dict.json} by the {@code syncSharedData} task. This
 * is the load path every dictionary lookup will use once {@code Lexicon} is ported.
 */
class SharedDataTest {

    @Test
    void canonicalDictionaryIsOnTheClasspath() throws Exception {
        try (InputStream in = SharedDataTest.class.getResourceAsStream("/rita/rita_dict.json")) {
            assertNotNull(in, "rita/rita_dict.json missing from classpath; is syncSharedData running?");
            String json = new String(in.readAllBytes(), StandardCharsets.UTF_8);
            assertTrue(json.startsWith("{"), "unexpected dictionary format");
            assertTrue(json.contains("\"abalone\""), "expected a known entry in the dictionary");
        }
    }

    @Test
    void versionResourceIsExpanded() throws Exception {
        try (InputStream in = SharedDataTest.class.getResourceAsStream("/rita/version.properties")) {
            assertNotNull(in, "rita/version.properties missing from classpath");
            String props = new String(in.readAllBytes(), StandardCharsets.UTF_8);
            assertTrue(props.matches("(?s).*version=\\d+\\.\\d+\\.\\d+.*"), "version not expanded: " + props);
        }
    }
}
