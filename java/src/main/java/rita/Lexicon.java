package rita;

import java.util.List;
import java.util.Map;

/**
 * Lexicon — stub for {@code js/src/lexicon.js}. Methods throw until ported.
 */
public class Lexicon {

    /**
     * The lexicon data, keyed by word to {@code [phones, pos]} entries. Mirrors the JS
     * {@code lexicon.data} property: tests mutate or swap it to exercise cache invalidation.
     */
    public Map<String, Object> data = new java.util.LinkedHashMap<>();

    public List<String> rhymesSync(String word, Map<String, Object> options) {
        throw RiTa.notPorted("lexicon.rhymesSync");
    }

    public List<String> searchSync(Object pattern, Map<String, Object> options) {
        throw RiTa.notPorted("lexicon.searchSync");
    }

    public String rawPhones(String word) {
        throw RiTa.notPorted("lexicon.rawPhones");
    }

    public String rawPhones(String word, boolean normalize) {
        throw RiTa.notPorted("lexicon.rawPhones");
    }

    public boolean hasWord(String word) {
        throw RiTa.notPorted("lexicon.hasWord");
    }

    public boolean hasWord(String word, Map<String, Object> options) {
        throw RiTa.notPorted("lexicon.hasWord");
    }

    public boolean isAlliteration(String word1, String word2) {
        throw RiTa.notPorted("lexicon.isAlliteration");
    }

    /** The POS data string for a word (e.g. "nn nns"), or null. Mirrors JS {@code _posData}. */
    public String _posData(String word) {
        throw RiTa.notPorted("lexicon._posData");
    }

    /** Splits a raw phone string into its phone list. Mirrors JS {@code _toPhoneArray}. */
    public List<String> _toPhoneArray(String raw) {
        throw RiTa.notPorted("lexicon._toPhoneArray");
    }
}
