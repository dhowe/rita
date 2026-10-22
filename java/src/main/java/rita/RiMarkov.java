package rita;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Markov model — port of {@code js/src/markov.js} (exported as {@code RiMarkov}).
 *
 * <p>Delegates generation to {@link BackoffModel}. The polymorphic {@code (n, prompt, opts)}
 * argument patterns of {@code generate}/{@code stream} are normalised by {@link #_resolveArgs}.
 */
public class RiMarkov {

    public int n = -1;
    public BackoffModel model;
    public Map<String, Object> opts = new LinkedHashMap<>();

    public RiMarkov() {
        this(null, null);
    }

    public RiMarkov(int n) {
        this((Object) n, null);
    }

    public RiMarkov(int n, Map<String, Object> opts) {
        this((Object) n, opts);
    }

    public RiMarkov(Object input) {
        this(input, null);
    }

    /** JS {@code constructor(input, opts)}. */
    @SuppressWarnings("unchecked")
    public RiMarkov(Object input, Map<String, Object> opts) {
        this.n = -1;
        if (input instanceof Number) {
            // v3.x compatibility: first arg is the n-gram order
            this.n = ((Number) input).intValue();
            if (opts != null) {
                Object t = opts.get("text");
                if (!truthy(t)) {
                    t = opts.get("tokens");
                }
                input = t;
            }
            else {
                input = null;
            }
        }
        else if (input instanceof Map && opts == null) {
            opts = (Map<String, Object>) input;
            Object t = opts.get("text");
            if (!truthy(t)) {
                t = opts.get("tokens");
            }
            input = t;
        }

        if (opts != null && opts.get("n") instanceof Number) {
            this.n = ((Number) opts.get("n")).intValue();
        }

        // save any generation-relevant opts for use as per-instance defaults
        this.opts = new LinkedHashMap<>();
        if (opts != null) {
            for (String key : BackoffModel.generationDefaults.keySet()) {
                if (opts.get(key) != null) {
                    this.opts.put(key, opts.get(key));
                }
            }
        }

        this.model = new BackoffModel(input, opts);
    }

    // ---------------- generation ----------------

    /** JS {@code stream(n, prompt, opts)} — generator of tokens. */
    public Iterable<String> stream(Object n, Object prompt, Map<String, Object> opts) {
        Object[] resolved = _resolveArgs(n, prompt, opts);
        @SuppressWarnings("unchecked")
        List<String> promptList = (List<String>) resolved[0];
        @SuppressWarnings("unchecked")
        Map<String, Object> callOpts = (Map<String, Object>) resolved[1];
        Map<String, Object> merged = new LinkedHashMap<>(this.opts);
        merged.putAll(callOpts);
        if (!model.ready) {
            model.build();
        }
        final IteratorHolder holder = new IteratorHolder(model.streamTokens(this.n, promptList, merged));
        return () -> holder.it;
    }

    public Iterable<String> stream(int n, Object prompt, Map<String, Object> opts) {
        return stream((Object) n, prompt, opts);
    }

    public Iterable<String> stream(int n, Map<String, Object> opts) {
        return stream((Object) n, opts, null);
    }

    public Iterable<String> stream(List<String> prompt, Map<String, Object> opts) {
        return stream((Object) prompt, opts, null);
    }

    public Iterable<String> stream(Map<String, Object> opts) {
        return stream((Object) opts, null, null);
    }

    /**
     * JS {@code generate(n, prompt, opts)} — returns the generated sentences as a
     * {@code String[]} (one element per {@code numSentences}, default 1). Use
     * {@link #generate1} for the single-sentence convenience that returns a {@code String}.
     */
    public String[] generate(Object n, Object prompt, Map<String, Object> opts) {
        Object[] resolved = _resolveArgs(n, prompt, opts);
        @SuppressWarnings("unchecked")
        List<String> promptList = (List<String>) resolved[0];
        @SuppressWarnings("unchecked")
        Map<String, Object> callOpts = (Map<String, Object>) resolved[1];
        Map<String, Object> merged = new LinkedHashMap<>(this.opts);
        merged.putAll(callOpts);
        if (!model.ready) {
            model.build();
        }
        int numSentences = merged.get("numSentences") != null
            ? ((Number) merged.get("numSentences")).intValue() : 1;
        Map<String, Object> genOpts = new LinkedHashMap<>(merged);
        genOpts.put("numSentences", numSentences);
        List<String> result = model.generateSentences(this.n, promptList, genOpts);
        return result.toArray(new String[0]);
    }

    /** Single-sentence form of {@link #generate}: returns the first generated sentence. */
    public String generate1(Object n, Object prompt, Map<String, Object> opts) {
        String[] result = generate(n, prompt, opts);
        return result.length > 0 ? result[0] : "";
    }

    public String[] generate() {
        return generate(null, null, null);
    }

    public String[] generate(int n) {
        return generate((Object) n, null, null);
    }

    public String[] generate(Map<String, Object> opts) {
        return generate((Object) opts, null, null);
    }

    public String[] generate(int n, Map<String, Object> opts) {
        return generate((Object) n, opts, null);
    }

    public String[] generate(List<String> prompt, Map<String, Object> opts) {
        return generate((Object) prompt, opts, null);
    }

    public String[] generate(int n, Object prompt, Map<String, Object> opts) {
        return generate((Object) n, prompt, opts);
    }

    public String generate1() {
        return generate1(null, null, null);
    }

    public String generate1(int n) {
        return generate1((Object) n, null, null);
    }

    public String generate1(Map<String, Object> opts) {
        return generate1((Object) opts, null, null);
    }

    public String generate1(int n, Map<String, Object> opts) {
        return generate1((Object) n, opts, null);
    }

    public String generate1(List<String> prompt, Map<String, Object> opts) {
        return generate1((Object) prompt, opts, null);
    }

    public String generate1(int n, Object prompt, Map<String, Object> opts) {
        return generate1((Object) n, prompt, opts);
    }

    /** JS {@code addText}. */
    public Model addText(String text) {
        return model.addText(text);
    }

    public Model addText(Object input) {
        return model.addText(input);
    }

    /** JS {@code addSentences}. */
    public Model addSentences(List<String> sentences) {
        return model.addSentences(sentences);
    }

    /** JS {@code addTokens}. */
    public Model addTokens(List<String> tokens) {
        return model.addTokens(tokens);
    }

    /** JS {@code completions(pre, post, opts)}. */
    @SuppressWarnings("unchecked")
    public List<String> completions(List<String> pre, List<String> post, Map<String, Object> opts) {
        if (pre == null) {
            throw new RuntimeException("Array required for pre");
        }
        boolean allowSpecial = opts != null && truthy(opts.get("allowSpecial"));
        if (!model.ready) {
            model.build();
        }

        if (post == null) {
            Map<String, Double> dist = model.suffixes.pdist(pre);
            if (dist == null) {
                return new ArrayList<>();
            }
            List<Map.Entry<String, Double>> entries = new ArrayList<>(dist.entrySet());
            entries.sort((a, b) -> Double.compare(b.getValue(), a.getValue()));
            List<String> out = new ArrayList<>();
            for (Map.Entry<String, Double> e : entries) {
                String t = e.getKey();
                if (allowSpecial || (!t.equals(model.startToken) && !t.equals(model.endToken))) {
                    out.add(t);
                }
            }
            return out;
        }

        List<String> result = new ArrayList<>();
        if (pre.size() + post.size() >= (this.n != -1 ? this.n : 3)) {
            throw new RuntimeException("pre.length + post.length must be less than n ("
                + (this.n != -1 ? this.n : 3) + ")");
        }
        Map<String, Double> dist = model.suffixes.pdist(pre);
        if (dist == null) {
            return result;
        }
        for (String w : dist.keySet()) {
            if (!allowSpecial && (w.equals(model.startToken) || w.equals(model.endToken))) {
                continue;
            }
            List<String> seq = new ArrayList<>(pre);
            seq.add(w);
            seq.addAll(post);
            if (model.suffixes.hasPrefix(seq)) {
                result.add(w);
            }
        }
        return result;
    }

    public List<String> completions(List<String> pre, List<String> post) {
        return completions(pre, post, Map.of());
    }

    public List<String> completions(List<String> pre) {
        return completions(pre, null, Map.of());
    }

    /** JS {@code probability} — deprecated. */
    public double probability(List<String> prompt, Object next) {
        throw new RuntimeException("probability() is deprecated. Use probabilities() to get the "
            + "full distribution, or compute probability of a sequence with completions() and pdist().");
    }

    public double probability(List<String> prompt) {
        throw new RuntimeException("probability() is deprecated. Use probabilities() to get the "
            + "full distribution, or compute probability of a sequence with completions() and pdist().");
    }

    public double probability(String prompt) {
        throw new RuntimeException("probability() is deprecated. Use probabilities() to get the "
            + "full distribution, or compute probability of a sequence with completions() and pdist().");
    }

    public double probability(String prompt, Object next) {
        throw new RuntimeException("probability() is deprecated. Use probabilities() to get the "
            + "full distribution, or compute probability of a sequence with completions() and pdist().");
    }

    /** JS {@code probabilities(tokens, opts)}. */
    public Map<String, Double> probabilities(Object tokens, Map<String, Object> opts) {
        if (!model.ready) {
            model.build();
        }
        if (tokens == null) {
            tokens = List.of(model.startToken);
        }
        if (!(tokens instanceof List)) {
            throw new RuntimeException("tokens[] required");
        }
        Map<String, Object> pdistOpts = new LinkedHashMap<>();
        double temp = (opts != null && truthy(opts.get("temp"))) ? ((Number) opts.get("temp")).doubleValue() : 0;
        pdistOpts.put("temp", temp);
        Map<String, Double> dist = model.suffixes.pdist((List<String>) tokens, pdistOpts);
        Map<String, Double> out = new LinkedHashMap<>();
        if (dist == null) {
            return out;
        }
        boolean allowSpecial = opts != null && truthy(opts.get("allowSpecial"));
        for (Map.Entry<String, Double> e : dist.entrySet()) {
            String t = e.getKey();
            if (allowSpecial || (!t.equals(model.startToken) && !t.equals(model.endToken))) {
                out.put(t, e.getValue());
            }
        }
        return out;
    }

    public Map<String, Double> probabilities(List<String> tokens) {
        return probabilities((Object) tokens, Map.of());
    }

    public Map<String, Double> probabilities(Object tokens) {
        return probabilities(tokens, Map.of());
    }

    public Map<String, Double> probabilities(List<String> tokens, Map<String, Object> opts) {
        return probabilities((Object) tokens, opts);
    }

    public Map<String, Double> probabilities() {
        return probabilities((Object) null, Map.of());
    }

    /** JS {@code size()}. */
    public int size() {
        return model.size();
    }

    /** JS {@code toString(opts)}. */
    public String toString(Map<String, Object> opts) {
        return model.toString(opts);
    }

    @Override
    public String toString() {
        return model.toString(null);
    }

    /** JS {@code toJSON()}. */
    public String toJSON() {
        if (!model.ready) {
            model.build();
        }
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("n", this.n != 0 ? this.n : -1);
        data.putAll(model.toJSON());
        return Json.write(data);
    }

    /** JS {@code static fromJSON(json)}. */
    public static RiMarkov fromJSON(String json) {
        if (json == null) {
            throw new RuntimeException("String required for fromJSON()");
        }
        RiMarkov rm = new RiMarkov();
        Map<String, Object> parsed = Json.parseObject(json);
        Object n = parsed.remove("n");
        rm.model = BackoffModel.fromJSON(parsed);
        rm.n = n instanceof Number ? ((Number) n).intValue() : -1;
        return rm;
    }

    /**
     * JS {@code _resolveArgs(n, prompt, opts)} — normalise the polymorphic argument patterns
     * into {@code {prompt, opts}} and update {@code this.n}.
     */
    @SuppressWarnings("unchecked")
    private Object[] _resolveArgs(Object n, Object prompt, Map<String, Object> opts) {
        if (n instanceof Map) {
            opts = new LinkedHashMap<>((Map<String, Object>) n);
            prompt = opts.get("prompt") != null ? opts.get("prompt") : new ArrayList<>();
            n = opts.remove("n");
            opts.remove("prompt");
        }
        else if (n instanceof List) {
            opts = prompt != null ? (Map<String, Object>) prompt : new LinkedHashMap<>();
            prompt = n;
            n = opts.get("n");
        }
        else if (prompt instanceof Map) {
            opts = new LinkedHashMap<>((Map<String, Object>) prompt);
            prompt = opts.get("prompt") != null ? opts.get("prompt") : new ArrayList<>();
            opts.remove("prompt");
        }

        if (!(prompt instanceof List)) {
            if (prompt == null) {
                prompt = new ArrayList<>();
            }
            else {
                throw new RuntimeException("Array required for prompt");
            }
        }

        if (n instanceof Number) {
            this.n = ((Number) n).intValue();
        }
        else if (opts != null && opts.get("n") instanceof Number) {
            this.n = ((Number) opts.get("n")).intValue();
        }
        if (this.n < 1) {
            throw new RuntimeException("n must be specified before calling generate() or stream()");
        }
        return new Object[] {prompt, opts != null ? opts : new LinkedHashMap<>()};
    }

    private static boolean truthy(Object o) {
        return Model.truthy(o);
    }

    /** Holds the (single-use) token iterator returned by {@link #stream}. */
    private static final class IteratorHolder {
        final java.util.Iterator<String> it;

        IteratorHolder(java.util.Iterator<String> it) {
            this.it = it;
        }
    }
}
