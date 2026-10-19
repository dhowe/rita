package rita;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Key-Word-In-Context concordance — port of {@code js/src/concorder.js}.
 *
 * <p>The JS model is a null-prototype object ({@code Object.create(null)}) so that words
 * matching {@code Object.prototype} members (e.g. {@code constructor}) cannot collide with
 * inherited properties; a {@link LinkedHashMap} gives the same isolation plus insertion order.
 */
public class Concorder {

    /** A model entry: the word, its comparison key, and the indexes where it occurs. */
    private static final class Entry {
        final String word;
        final String key;
        final List<Integer> indexes = new ArrayList<>();

        Entry(String word, String key) {
            this.word = word;
            this.key = key;
        }
    }

    private List<String> words;
    private boolean ignoreCase = false;
    private boolean ignoreStopWords = false;
    private boolean ignorePunctuation = false;
    private List<String> wordsToIgnore = List.of();
    private Map<String, Entry> model = null;

    /** JS {@code concordance(text, options)}. */
    @SuppressWarnings("unchecked")
    public Map<String, Integer> concordance(Object text, Map<String, Object> options) {
        List<String> toks = toStringList(text);
        this.words = (toks != null) ? toks : java.util.Arrays.asList(RiTa.tokenize((String) text));
        this.ignoreCase = truthy(options, "ignoreCase");
        this.ignoreStopWords = truthy(options, "ignoreStopWords");
        this.ignorePunctuation = truthy(options, "ignorePunctuation");
        this.wordsToIgnore = (options != null && options.get("wordsToIgnore") instanceof List)
            ? (List<String>) options.get("wordsToIgnore")
            : List.of();

        _buildModel();

        Map<String, Integer> result = new LinkedHashMap<>();
        for (Map.Entry<String, Entry> e : model.entrySet()) {
            result.put(e.getKey(), e.getValue().indexes.size());
        }
        return result;
    }

    public Map<String, Integer> concordance(String text, Map<String, Object> options) {
        return concordance((Object) text, options);
    }

    public Map<String, Integer> concordance(String text) {
        return concordance((Object) text, null);
    }

    /** JS {@code concordance()} — undefined text throws. */
    public Map<String, Integer> concordance() {
        return concordance((Object) null, null);
    }

    /** JS {@code kwic(word, opts)} — opts is an options map or an int (numWords). */
    public List<String> kwic(String keyword, Object opts) {
        int numWords = 6;
        if (opts instanceof Map) {
            @SuppressWarnings("unchecked")
            Map<String, Object> o = (Map<String, Object>) opts;
            if (o.get("numWords") instanceof Number) {
                numWords = ((Number) o.get("numWords")).intValue();
            }
            Object text = o.get("text");
            if (text instanceof String && !((String) text).isEmpty()) {
                concordance(text, o);
            }
            Object wordList = o.get("words");
            List<String> wordArr = toStringList(wordList);
            if (wordArr != null && !wordArr.isEmpty()) {
                concordance(wordArr, o);
            }
        }
        else if (opts instanceof Number) {
            numWords = ((Number) opts).intValue();
        }

        if (model == null) {
            throw new RuntimeException("Call concordance() first");
        }

        List<String> result = new ArrayList<>();
        Entry value = _lookup(keyword);
        if (value != null) {
            List<Integer> idxs = value.indexes;
            for (int i = 0; i < idxs.size(); i++) {
                int idx = idxs.get(i);
                int from = Math.max(0, idx - numWords);
                int to = Math.min(words.size(), idx + numWords + 1);
                List<String> sub = words.subList(from, to);
                if (i < 1 || (idxs.get(i) - idxs.get(i - 1)) > numWords) {
                    result.add(RiTa.untokenize(new ArrayList<>(sub).toArray(new String[0])));
                }
            }
        }
        return result;
    }

    public List<String> kwic(String keyword, Map<String, Object> options) {
        return kwic(keyword, (Object) options);
    }

    public List<String> kwic(String keyword) {
        return kwic(keyword, (Object) null);
    }

    public List<String> kwic(String keyword, int numWords) {
        return kwic(keyword, (Object) numWords);
    }

    /** JS {@code count(word)}. */
    public int count(String word) {
        Entry value = _lookup(word);
        return (value != null) ? value.indexes.size() : 0;
    }

    // ---------------- private ----------------

    private void _buildModel() {
        if (words == null || words.isEmpty()) {
            throw new RuntimeException("No text in model");
        }
        model = new LinkedHashMap<>();
        for (int j = 0; j < words.size(); j++) {
            String word = words.get(j);
            if (_isIgnorable(word)) {
                continue;
            }
            Entry entry = _lookup(word);
            if (entry == null) {
                entry = new Entry(word, _compareKey(word));
                model.put(entry.key, entry);
            }
            entry.indexes.add(j);
        }
    }

    private boolean _isIgnorable(String key) {
        if (ignorePunctuation && RiTa.isPunct(key)) {
            return true;
        }
        if (ignoreStopWords && RiTa.isStopWord(key)) {
            return true;
        }
        for (String word : wordsToIgnore) {
            if (key.equals(word) || (ignoreCase && key.equalsIgnoreCase(word))) {
                return true;
            }
        }
        return false;
    }

    private String _compareKey(String word) {
        return ignoreCase ? word.toLowerCase() : word;
    }

    private Entry _lookup(String word) {
        if (model == null) {
            return null;
        }
        return model.get(_compareKey(word));
    }

    private static boolean truthy(Map<String, Object> opts, String key) {
        return opts != null && Model.truthy(opts.get(key));
    }

    /** Coerces a List or String[] to List<String>; null otherwise. */
    @SuppressWarnings("unchecked")
    private static List<String> toStringList(Object o) {
        if (o instanceof List) {
            return (List<String>) o;
        }
        if (o instanceof String[]) {
            return java.util.Arrays.asList((String[]) o);
        }
        return null;
    }
}
