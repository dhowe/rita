package rita;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Lexicon — port of {@code js/src/lexicon.js}.
 *
 * <p>The data layer (dictionary load + phone/POS lookups) is implemented; the search/rhyme/
 * alliteration algorithms remain stubs until their dependencies (analyzer, tagger, conjugator,
 * inflector) are ported.
 */
public class Lexicon {

    /**
     * The lexicon data, keyed by word to {@code [phones, pos]} entries (the value is a
     * {@code List<Object>} of size 2). Mirrors the JS {@code lexicon.data} property: tests mutate
     * or swap it to exercise cache invalidation.
     */
    public Map<String, Object> data = loadData();

    /** Number of dictionary entries. Mirrors JS {@code size()}. */
    public int size() {
        return data.size();
    }

    public List<String> rhymesSync(String word, Map<String, Object> options) {
        throw RiTa.notPorted("lexicon.rhymesSync");
    }

    public List<String> searchSync(Object pattern, Map<String, Object> options) {
        throw RiTa.notPorted("lexicon.searchSync");
    }

    /** JS {@code rawPhones(word)} — no LTS suppression. */
    public String rawPhones(String word) {
        return rawPhones(word, false);
    }

    /**
     * JS {@code rawPhones(word, opts)} — returns the raw phone string from the dictionary, or
     * null when absent. When {@code noLts} is false and the word is missing, the LTS engine is
     * consulted (via the analyzer); that path is not yet wired.
     */
    public String rawPhones(String word, boolean noLts) {
        Object[] rdata = lookupRaw(word);
        if (rdata != null && rdata.length > 0) {
            return (String) rdata[0];
        }
        if (!noLts) {
            List<String> phones = RiTa.analyzer.computePhones(word);
            if (phones != null && !phones.isEmpty()) {
                return Util.syllablesFromPhones(phones);
            }
        }
        return null;
    }

    /** JS {@code hasWord(word)} — exact dictionary membership. */
    public boolean hasWord(String word) {
        return hasWord(word, Map.of());
    }

    /**
     * JS {@code hasWord(word, opts)}. The exact-match path is implemented; the derivation path
     * (plural/conjugation) needs tagger/conjugator/inflector and throws until those are ported.
     */
    public boolean hasWord(String word, Map<String, Object> options) {
        if (word == null || word.isEmpty()) {
            return false;
        }
        String token = word.toLowerCase();
        boolean exists = data.containsKey(token);
        boolean noDerivations = truthy(options.get("noDerivations"));
        if (noDerivations || exists) {
            return exists;
        }
        throw RiTa.notPorted("lexicon.hasWord.derivations");
    }

    public boolean isAlliteration(String word1, String word2) {
        throw RiTa.notPorted("lexicon.isAlliteration");
    }

    /** The POS data string for a word (e.g. "nn nns"), or null. Mirrors JS {@code _posData}. */
    public String _posData(String word) {
        Object[] rdata = lookupRaw(word);
        if (rdata != null && rdata.length == 2) {
            return (String) rdata[1];
        }
        return null;
    }

    /** Splits a raw phone string into its phone list. Mirrors JS {@code _toPhoneArray}. */
    public List<String> _toPhoneArray(String raw) {
        List<String> out = new ArrayList<>();
        for (String p : raw.replaceAll("[01]", "").replaceAll(" ", "-").split("-")) {
            out.add(p);
        }
        return out;
    }

    /** JS {@code _posArr(word)} — the POS tags as a list, or null. */
    public List<String> _posArr(String word) {
        String pos = _posData(word);
        return pos == null ? null : List.of(pos.split(" "));
    }

    /** JS {@code _lookupRaw(word)} — the {@code [phones, pos]} entry, or null. */
    Object[] lookupRaw(String word) {
        if (word == null) {
            return null;
        }
        Object v = data.get(word.toLowerCase());
        if (v instanceof List) {
            List<?> list = (List<?>) v;
            return list.toArray();
        }
        return null;
    }

    /** JS {@code _getWords()} — the dictionary keys (cached by data identity). */
    public List<String> _getWords() {
        if (wordsCacheRef != data) {
            wordsCache = new ArrayList<>(data.keySet());
            wordsCacheRef = data;
        }
        return wordsCache;
    }

    private List<String> wordsCache;
    private Map<String, Object> wordsCacheRef;

    // ---- internals ------------------------------------------------------------------

    private static boolean truthy(Object o) {
        if (o == null) {
            return false;
        }
        if (o instanceof Boolean) {
            return (Boolean) o;
        }
        if (o instanceof Number) {
            return ((Number) o).doubleValue() != 0;
        }
        if (o instanceof String) {
            return !((String) o).isEmpty();
        }
        return true;
    }

    /** Loads the canonical dictionary from the jar resource {@code rita/rita_dict.json}. */
    private static Map<String, Object> loadData() {
        Map<String, Object> out = new LinkedHashMap<>();
        try (InputStream in = Lexicon.class.getResourceAsStream("/rita/rita_dict.json")) {
            if (in == null) {
                throw new RuntimeException("Missing dictionary resource: /rita/rita_dict.json");
            }
            try (Reader r = new InputStreamReader(in, StandardCharsets.UTF_8)) {
                Map<String, Object> raw = Json.parseObject(readAll(r));
                for (Map.Entry<String, Object> e : raw.entrySet()) {
                    List<?> entry = (List<?>) e.getValue();
                    List<Object> pair = new ArrayList<>(2);
                    pair.add(entry.get(0));
                    pair.add(entry.get(1));
                    out.put(e.getKey(), pair);
                }
            }
        } catch (Exception e) {
            throw new RuntimeException("Failed to load rita_dict.json", e);
        }
        return out;
    }

    private static String readAll(Reader r) throws java.io.IOException {
        StringBuilder sb = new StringBuilder(1 << 20);
        char[] buf = new char[8192];
        int n;
        while ((n = r.read(buf)) != -1) {
            sb.append(buf, 0, n);
        }
        return sb.toString();
    }
}
