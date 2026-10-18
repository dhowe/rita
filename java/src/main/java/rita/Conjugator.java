package rita;

import java.util.Map;

/**
 * Verb conjugator — stub for {@code js/src/conjugator.js}. Methods throw until ported.
 */
public class Conjugator {

    /** Memoized stem lookups, keyed by word (mirrors JS {@code _stemCache}). */
    public Map<String, String> _stemCache = new java.util.LinkedHashMap<>();

    /** The lexicon data object the cache was built against (mirrors JS {@code _stemCacheRef}). */
    public Map<String, Object> _stemCacheRef = null;

    public String conjugate(String verbWord, Map<String, Object> options) {
        throw RiTa.notPorted("conjugator.conjugate");
    }

    /** JS {@code conjugate(verbWord, "1SPr")} — string-form options. */
    public String conjugate(String verbWord, String args) {
        throw RiTa.notPorted("conjugator.conjugate");
    }

    /** JS {@code conjugate()} — undefined input throws. */
    public String conjugate() {
        throw RiTa.notPorted("conjugator.conjugate");
    }

    public String presentPart(String verbWord) {
        throw RiTa.notPorted("conjugator.presentPart");
    }

    public String pastPart(String verbWord) {
        throw RiTa.notPorted("conjugator.pastPart");
    }

    public String unconjugate(String conjugated, Map<String, Object> options) {
        throw RiTa.notPorted("conjugator.unconjugate");
    }

    public String unconjugate(String conjugated) {
        throw RiTa.notPorted("conjugator.unconjugate");
    }

    /** Maps a stem to its verb form via longest-prefix match (mirrors JS {@code _handleStem}). */
    public String _handleStem(String word) {
        throw RiTa.notPorted("conjugator._handleStem");
    }

    @Override
    public String toString() {
        throw RiTa.notPorted("conjugator.toString");
    }
}
