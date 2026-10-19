package rita;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

/**
 * Suffix-gram language model — port of {@code js/src/model.js} (exported as {@code RiTa.Model}).
 *
 * <p>Mirrors the JS {@code SuffixGram} base class. Fields mirror the JS object; the
 * {@code tokenize}/{@code untokenize} options are modelled as {@link Function}s. Subclasses
 * (see {@link BackoffModel}) override {@link #build(Map)}.
 */
public class Model {

    public static boolean SILENT = false;

    /** Option keys (mirrors {@code SuffixGram.options}). */
    public static final String[] options = {
        "debug", "ready", "suffixes", "compressed", "startToken", "endToken", "tokenize", "untokenize",
    };

    /** Serialized field names (mirrors {@code SuffixGram.__dict__}). */
    public static final String[] __dict__ = {
        "ready", "startToken", "endToken", "tokenize", "untokenize", "tokens", "tokenCount", "suffixes",
    };

    /** Default tokenizer: {@code RiTa.tokenize} wrapped as a function. */
    public static final Function<String, List<String>> DEFAULT_TOKENIZE =
        s -> Arrays.asList(rita.RiTa.tokenize(s));

    /** Default untokenizer: {@code RiTa.untokenize} wrapped as a function. */
    public static final Function<List<String>, String> DEFAULT_UNTOKENIZE =
        l -> rita.RiTa.untokenize(l.toArray(new String[0]));

    // instance fields
    public boolean debug = false;
    public boolean ready = false;
    public boolean compressed = false;
    public String startToken = SuffixArray.SEQ_START_TOKEN;
    public String endToken = SuffixArray.SEQ_END_TOKEN;
    public Function<String, List<String>> tokenize = DEFAULT_TOKENIZE;
    public Function<List<String>, String> untokenize = DEFAULT_UNTOKENIZE;
    public List<String> tokens = new ArrayList<>();
    public int tokenCount = 0;
    public SuffixArray suffixes = null;

    public Model() {
    }

    public Model(Object input) {
        this(input, null);
    }

    /** JS {@code constructor(input, opts)}. */
    @SuppressWarnings("unchecked")
    public Model(Object input, Map<String, Object> opts) {
        // only an options object
        if (input instanceof Map && opts == null) {
            opts = (Map<String, Object>) input;
            input = null;
        }

        // initialize with options or default values
        if (opts != null) {
            if (opts.containsKey("debug")) {
                debug = truthy(opts.get("debug"));
            }
            if (opts.containsKey("ready")) {
                ready = truthy(opts.get("ready"));
            }
            if (opts.containsKey("compressed")) {
                compressed = truthy(opts.get("compressed"));
            }
            if (opts.get("startToken") != null) {
                startToken = (String) opts.get("startToken");
            }
            if (opts.get("endToken") != null) {
                endToken = (String) opts.get("endToken");
            }
            if (opts.get("tokenize") != null) {
                tokenize = (Function<String, List<String>>) opts.get("tokenize");
            }
            if (opts.get("untokenize") != null) {
                untokenize = (Function<List<String>, String>) opts.get("untokenize");
            }
        }

        if (input == null && opts != null) {
            if (opts.containsKey("text")) {
                Object t = opts.get("text");
                if (!(t instanceof String)) {
                    throw new RuntimeException("String required for `text` option, got " + typeName(t));
                }
                input = t;
            }
            else if (opts.containsKey("tokens")) {
                Object t = opts.get("tokens");
                if (!(t instanceof List)) {
                    throw new RuntimeException("Array of tokens required for `tokens` option");
                }
                input = t;
            }
            else if (opts.containsKey("sentences")) {
                Object s = opts.get("sentences");
                if (!(s instanceof List)) {
                    throw new RuntimeException("Array of sentences required for `sentences` option");
                }
                input = _tokenizeSentences((List<String>) s);
            }
        }

        if (input != null) {
            if (input instanceof List) {
                addTokens((List<String>) input);
            }
            else if (input instanceof String) {
                addText((String) input);
            }
            else {
                throw new RuntimeException("String or array required");
            }
            build(); // build the model immediately by default
        }
    }

    /** JS {@code toJSON()} — {@code Object.assign({}, this)}. */
    public Map<String, Object> toJSON() {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("ready", ready);
        m.put("startToken", startToken);
        m.put("endToken", endToken);
        m.put("tokenCount", tokenCount);
        m.put("debug", debug);
        m.put("compressed", compressed);
        m.put("tokens", tokens);
        m.put("suffixes", suffixes);
        return m;
    }

    /** JS {@code build()} — not implemented on the base class. */
    public Model build() {
        throw new RuntimeException("Model.build() not implemented");
    }

    /** JS {@code build(opts)} — not implemented on the base class. */
    public Model build(Map<String, Object> opts) {
        throw new RuntimeException("Model.build() not implemented");
    }

    /** JS {@code size()} — number of tokens (includes special tokens). */
    public int size() {
        if (!ready) {
            build();
        }
        return tokenCount;
    }

    /** JS {@code toString(opts)}. */
    public String toString(Map<String, Object> opts) {
        if (!ready) {
            build();
        }
        return suffixes.toString(opts);
    }

    @Override
    public String toString() {
        return toString(null);
    }

    /** JS {@code addText(rawText)}. */
    public Model addText(String rawText) {
        if (rawText == null) {
            throw new RuntimeException("String required: if adding an array see addTokens() or addSentences()");
        }
        return rawText.isEmpty() ? this : addSentences(Arrays.asList(rita.RiTa.sentences(rawText)));
    }

    /** JS {@code addText(...)} — non-string input throws. */
    public Model addText(Object input) {
        if (!(input instanceof String)) {
            throw new RuntimeException("String required: if adding an array see addTokens() or addSentences()");
        }
        return addText((String) input);
    }

    /** JS {@code addSentences(sentences)}. */
    public Model addSentences(List<String> sentences) {
        return addTokens(_tokenizeSentences(sentences));
    }

    /** JS {@code addTokens(tokens)}. */
    public Model addTokens(List<String> tokens) {
        this.ready = false;
        if (tokens != null && !tokens.isEmpty() && tokens.get(0) instanceof String) {
            if (this.tokens == null) {
                this.tokens = new ArrayList<>();
            }
            this.tokens.addAll(tokens);
        }
        else {
            throw new RuntimeException("Array of individual tokens required, got "
                + (tokens == null ? "undefined" : typeName(tokens)));
        }
        return this;
    }

    /** JS {@code _decode(indices)}. */
    public List<String> _decode(List<Integer> indices) {
        if (!ready) {
            build();
        }
        return suffixes._decode(indices);
    }

    /** JS {@code randSeqStart()}. */
    public String randSeqStart() {
        if (!ready) {
            build();
        }
        return suffixes.randSeqStart();
    }

    /** JS {@code _tokenizeSentences(sentences)}. */
    protected List<String> _tokenizeSentences(List<String> sentences) {
        List<String> toks = new ArrayList<>();
        for (String s : sentences) {
            toks.add(startToken);
            toks.addAll(tokenize.apply(s));
            toks.add(endToken);
        }
        return toks;
    }

    // ---------------- statics ----------------

    /** JS {@code isObject(obj)} — plain object literal (a Map here). */
    public static boolean isObject(Object obj) {
        return obj instanceof Map;
    }

    /** JS {@code SuffixGram.random()} — shared seeded RNG. */
    public static double random() {
        return rita.RiTa.randomizer.random();
    }

    /** JS {@code cleanDist(dist, indent, nosort)}. */
    public static String cleanDist(Map<String, Double> dist, int indent, boolean nosort) {
        List<Map.Entry<String, Double>> entries = new ArrayList<>(dist.entrySet());
        if (!nosort) {
            entries.sort((a, b) -> Double.compare(b.getValue(), a.getValue()));
        }
        boolean truncated = false;
        if (entries.size() > 10) {
            entries = new ArrayList<>(entries.subList(0, 15));
            truncated = true;
        }
        StringBuilder pad = new StringBuilder();
        for (int i = 0; i < indent + 2; i++) {
            pad.append(' ');
        }
        StringBuilder acc = new StringBuilder();
        for (int i = 0; i < entries.size(); i++) {
            Map.Entry<String, Double> e = entries.get(i);
            acc.append(pad).append(e.getKey()).append(": ")
                .append(String.format(java.util.Locale.ROOT, "%.2f", e.getValue())).append(",");
            if (i < entries.size() - 1) {
                acc.append('\n');
            }
        }
        return (truncated ? acc + "\n" + pad + "..." : acc.toString());
    }

    static boolean truthy(Object o) {
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

    static String typeName(Object o) {
        if (o == null) {
            return "undefined";
        }
        if (o instanceof List) {
            return "object";
        }
        if (o instanceof String) {
            return "string";
        }
        if (o instanceof Boolean) {
            return "boolean";
        }
        if (o instanceof Number) {
            return "number";
        }
        return "object";
    }

    /** Deep structural equality mirroring chai's {@code .eql} used by the JS tests. */
    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (other == null || getClass() != other.getClass()) {
            return false;
        }
        Model m = (Model) other;
        return ready == m.ready
            && compressed == m.compressed
            && debug == m.debug
            && tokenCount == m.tokenCount
            && java.util.Objects.equals(startToken, m.startToken)
            && java.util.Objects.equals(endToken, m.endToken)
            && java.util.Objects.equals(tokens, m.tokens)
            && java.util.Objects.equals(suffixes, m.suffixes);
    }

    @Override
    public int hashCode() {
        return java.util.Objects.hash(ready, compressed, debug, tokenCount, startToken, endToken, tokens, suffixes);
    }
}
