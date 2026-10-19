package rita;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Function;
import java.util.function.Predicate;

/**
 * Backoff language model — port of {@code js/src/backoff.js} (exported as
 * {@code RiTa.BackoffModel}). Extends {@link Model} as in JS.
 */
public class BackoffModel extends Model {

    public static boolean SILENT = true;

    /** JS {@code generationDefaults} — canonical generation tunables. */
    public static final Map<String, Object> generationDefaults = new LinkedHashMap<>();
    static {
        generationDefaults.put("debug", false);
        generationDefaults.put("minLength", 5);
        generationDefaults.put("maxLength", 999);
        generationDefaults.put("maxAttempts", 999);
        generationDefaults.put("maxBacktracks", 9999);
        generationDefaults.put("forceOriginal", false);
        generationDefaults.put("maxLengthMatch", Double.POSITIVE_INFINITY);
        generationDefaults.put("temp", 1.0);
        generationDefaults.put("topK", 20);
        generationDefaults.put("depth", 50);
        generationDefaults.put("allowSpecial", false);
        generationDefaults.put("sortByProb", false);
    }

    /** JS {@code generationAliases} — option-key aliases. */
    public static final Map<String, String> generationAliases = Map.of(
        "dbug", "debug", "minTokens", "minLength", "maxTokens", "maxLength",
        "temperature", "temp", "mlm", "maxLengthMatch");

    /** JS {@code generationIgnorable} — accepted non-tunable keys. */
    public static final List<String> generationIgnorable = List.of(
        "numSentences", "generateUntil", "allowDuplicates", "prompt", "n", "trace");

    /** Internal generation-tree node (mirrors the JS {@code {token,prob,isEnd,children}}). */
    private static final class Node {
        String token;
        double prob;
        boolean isEnd;
        List<Node> children = new ArrayList<>();
    }

    /** A recorded choice point during backtracking generation. */
    private static final class ChoicePoint {
        Set<String> triedTokens = new LinkedHashSet<>();
        boolean isSentenceEnd = false;
    }

    public BackoffModel() {
    }

    public BackoffModel(Object input) {
        super(input, null);
    }

    public BackoffModel(Object input, Map<String, Object> opts) {
        super(input, opts);
    }

    public static BackoffModel fromJSON(String json) {
        return fromJSON(Json.parseObject(json));
    }

    /** JS {@code fromJSON(json)} — {@code Object.assign(new BackoffModel(), obj)}. */
    @SuppressWarnings("unchecked")
    public static BackoffModel fromJSON(Map<String, Object> obj) {
        BackoffModel model = new BackoffModel();
        if (obj.containsKey("debug")) {
            model.debug = truthy(obj.get("debug"));
        }
        if (obj.containsKey("ready")) {
            model.ready = truthy(obj.get("ready"));
        }
        if (obj.containsKey("compressed")) {
            model.compressed = truthy(obj.get("compressed"));
        }
        if (obj.get("startToken") != null) {
            model.startToken = (String) obj.get("startToken");
        }
        if (obj.get("endToken") != null) {
            model.endToken = (String) obj.get("endToken");
        }
        if (obj.get("tokenCount") != null) {
            model.tokenCount = ((Number) obj.get("tokenCount")).intValue();
        }
        model.tokens = obj.containsKey("tokens") ? (List<String>) obj.get("tokens") : null;
        Object sfx = obj.get("suffixes");
        if (sfx instanceof SuffixArray) {
            model.suffixes = (SuffixArray) sfx;
        }
        else if (sfx instanceof List) {
            model.suffixes = SuffixArray.fromRecords((List<?>) sfx);
        }
        return model;
    }

    /** JS {@code toJSON()} — adds {@code n} to the model's own fields. */
    @Override
    public Map<String, Object> toJSON() {
        return super.toJSON();
    }

    // ---------------- generation ----------------

    /** JS {@code generateSentences(n, prompt, opts)} — always returns an array of strings. */
    public List<String> generateSentences(int n, List<String> prompt, Map<String, Object> opts) {
        return backtrackingGenerate(n, prompt, opts == null ? Map.of() : opts);
    }

    /** JS {@code generationPaths(n, prompt, options)} — list of {tokens, prob, inInput}. */
    public List<Map<String, Object>> generationPaths(int n, List<String> prompt, Map<String, Object> options) {
        Map<String, Object> opts = resolveOpts(n, options, List.of("numSentences"));
        List<Node> tree = buildTree(n, prompt, opts, (int) numOpt(opts, "depth", 50));

        List<List<Map<String, Object>>> paths = new ArrayList<>();
        List<Map<String, Object>> promptNodes = new ArrayList<>();
        for (String t : prompt) {
            promptNodes.add(nodeMap(t, 1));
        }
        collectPaths(tree, promptNodes, paths);

        if (truthy(opts.get("sortByProb"))) {
            paths.sort((a, b) -> Double.compare(pathProb(b, prompt.size()), pathProb(a, prompt.size())));
        }

        int size = prompt.size();
        List<Double> raw = new ArrayList<>();
        double total = 0;
        for (List<Map<String, Object>> p : paths) {
            double r = pathProb(p, size);
            raw.add(r);
            total += r;
        }

        List<Map<String, Object>> result = new ArrayList<>();
        for (int i = 0; i < paths.size(); i++) {
            List<Map<String, Object>> tokens = paths.get(i);
            List<String> tokenStrings = new ArrayList<>();
            for (Map<String, Object> nd : tokens) {
                tokenStrings.add((String) nd.get("token"));
            }
            Map<String, Object> rec = new LinkedHashMap<>();
            rec.put("tokens", tokens);
            rec.put("prob", raw.get(i) / total);
            rec.put("inInput", suffixes.hasPrefix(tokenStrings));
            result.add(rec);
        }
        return result;
    }

    /** JS {@code pathGenerator(n, prompt, options)} — generator yielding paths. */
    public Iterator<Map<String, Object>> pathGenerator(int n, List<String> prompt, Map<String, Object> options) {
        Map<String, Object> opts = resolveOpts(n, options);
        List<Map<String, Object>> promptNodes = new ArrayList<>();
        for (String t : prompt) {
            promptNodes.add(nodeMap(t, 1));
        }
        List<Node> tree = buildTree(n, prompt, opts);
        if (tree.isEmpty()) {
            if (truthy(opts.get("forceOriginal"))) {
                throw new RuntimeException("forceOriginal: no original completions found for prompt ["
                    + String.join(" ", prompt) + "]");
            }
            return Collections.emptyIterator();
        }
        List<Map<String, Object>> out = new ArrayList<>();
        walkPaths(tree, promptNodes, prompt.size(), out);
        return out.iterator();
    }

    /** JS {@code streamTokens(n, prompt, options)} — generator yielding tokens. */
    public Iterator<String> streamTokens(int n, List<String> prompt, Map<String, Object> options) {
        Map<String, Object> opts = resolveOpts(n, options, List.of("generateUntil", "numSentences"));
        if (truthy(opts.get("forceOriginal"))) {
            throw new RuntimeException("`forceOriginal` invalid for streamTokens");
        }
        int minLength = (int) numOpt(opts, "minLength", 5);
        int maxLength = (int) numOpt(opts, "maxLength", 999);
        double maxLengthMatch = numOpt(opts, "maxLengthMatch", Double.POSITIVE_INFINITY);
        double temp = numOpt(opts, "temp", 1);
        boolean allowSpecial = truthy(opts.get("allowSpecial"));
        boolean debug = truthy(opts.get("debug"));

        Object generateUntil = opts.get("generateUntil");
        if (generateUntil == null) {
            generateUntil = endToken;
        }
        final Predicate<String> isUntil = untilPredicate(generateUntil);
        final boolean checkLength = Double.isFinite(maxLengthMatch);
        final int mlm = (int) maxLengthMatch;

        Map<String, Object> saOpts = new LinkedHashMap<>();
        saOpts.put("temp", temp);
        saOpts.put("n", n);

        List<String> context = new ArrayList<>(prompt);
        List<String> yielded = new ArrayList<>();
        int generated = 0;
        while (generated < maxLength) {
            List<String> query = lastK(context, n - 1);
            Map<String, Double> dist = context.size() > n - 1
                ? orElse(suffixes.pdist(context, saOpts), suffixes.pdist(query, saOpts))
                : suffixes.pdist(query, saOpts);

            while ((dist == null || dist.isEmpty()) && query.size() > 1) {
                query = new ArrayList<>(query.subList(1, query.size()));
                dist = suffixes.pdist(query, saOpts);
            }
            if (dist == null) {
                break;
            }

            String chosenToken = null;
            double weightSum = 0;
            int totalSoFar = prompt.size() + generated;

            for (Map.Entry<String, Double> e : dist.entrySet()) {
                String token = e.getKey();
                double prob = e.getValue();
                if (isSpecial(token)) {
                    if (totalSoFar < minLength) {
                        continue;
                    }
                }
                else if (checkLength) {
                    List<String> nonSpecial = filterSpecial(context);
                    List<String> seq = new ArrayList<>(lastK(nonSpecial, mlm));
                    seq.add(token);
                    if (seq.size() > mlm && suffixes.hasPrefix(seq)) {
                        continue;
                    }
                }
                weightSum += prob;
                if (Model.random() * weightSum < prob) {
                    chosenToken = token;
                }
            }

            if (chosenToken == null) {
                break;
            }
            String token = chosenToken;
            List<String> generatedSoFar = new ArrayList<>(context.subList(prompt.size(), context.size()));

            if (!isSpecial(token) && isUntil.test(token) && totalSoFar + 1 >= minLength) {
                yielded.add(token);
                break;
            }
            if (isSpecial(token)) {
                if (isUntil.test(token) && totalSoFar + 1 >= minLength) {
                    if (allowSpecial) {
                        yielded.add(token);
                    }
                    break;
                }
                if (allowSpecial) {
                    yielded.add(token);
                }
                context.add(token);
                generated++;
                continue;
            }
            yielded.add(token);
            context.add(token);
            generated++;
        }
        return yielded.iterator();
    }

    // ---------------- private ----------------

    /** JS {@code backtrackingGenerate(n, prompt, opts)}. */
    private List<String> backtrackingGenerate(int n, List<String> prompt, Map<String, Object> opts) {
        Map<String, Object> resolved = resolveOpts(n, opts);
        int numSentences = opts.containsKey("numSentences") && opts.get("numSentences") != null
            ? ((Number) opts.get("numSentences")).intValue() : 2;
        int maxBacktracks = (int) numOpt(resolved, "maxBacktracks", 9999);
        int perMax = (int) numOpt(resolved, "maxLength", 999);
        int perMin = (int) numOpt(resolved, "minLength", 5);
        double mlm = numOpt(resolved, "maxLengthMatch", Double.POSITIVE_INFINITY);
        int maxAttempts = (int) numOpt(resolved, "maxAttempts", 999);
        double temp = numOpt(resolved, "temp", 1);
        boolean debug = truthy(resolved.get("debug"));
        final int mlmI = (int) mlm;
        final boolean checkLength = Double.isFinite(mlm);

        Map<String, Object> saOpts = new LinkedHashMap<>();
        saOpts.put("temp", temp);
        saOpts.put("n", n);

        List<String> nonEmptyPrompt = new ArrayList<>();
        for (String t : prompt) {
            if (t != null && !t.isEmpty()) {
                nonEmptyPrompt.add(t);
            }
        }
        List<String> validPrompt = new ArrayList<>();
        for (String t : nonEmptyPrompt) {
            if (!t.trim().isEmpty()) {
                validPrompt.add(t);
            }
        }
        if (!nonEmptyPrompt.isEmpty() && validPrompt.isEmpty()) {
            throw new RuntimeException("prompt contains only whitespace tokens");
        }

        if (!validPrompt.isEmpty()) {
            Map<String, Double> dist = suffixes.pdist(validPrompt, Map.of("n", n));
            if (dist == null || dist.isEmpty()) {
                throw new RuntimeException("generate() failed: prompt [" + String.join(", ", validPrompt)
                    + "] not found in model");
            }
            if (numSentences == 1) {
                Map<String, Double> startDist = suffixes.startIndexDist();
                Double v = startDist.get(validPrompt.get(0));
                if (v == null || v == 0) {
                    throw new RuntimeException("generate() failed: prompt token '" + validPrompt.get(0)
                        + "' is not a sentence start");
                }
            }
        }

        for (int attempts = 1; attempts <= maxAttempts; attempts++) {
            List<String> context = new ArrayList<>(randomStarter(validPrompt));
            int floor = context.size();
            Map<Integer, ChoicePoint> choicePoints = new LinkedHashMap<>();
            List<Integer> sentenceStarts = new ArrayList<>();
            sentenceStarts.add(0);

            int[] endsSeen = {0};
            int backtracks = 0;
            boolean gaveUp = false;

            while (endsSeen[0] < numSentences) {
                if (backtracks > maxBacktracks) {
                    gaveUp = true;
                    break;
                }
                int pos = context.size();
                int curStart = sentenceStarts.get(sentenceStarts.size() - 1);
                int tokensInSentence = pos - curStart;

                List<String> query = lastK(context, n - 1);
                Map<String, Double> dist = suffixes.pdist(query, saOpts);
                ChoicePoint existing = choicePoints.get(pos);
                Set<String> tried = existing != null ? existing.triedTokens : new LinkedHashSet<>();

                if (dist == null || dist.isEmpty()) {
                    if (!backtrack(context, choicePoints, sentenceStarts, floor, endsSeen)) {
                        gaveUp = true;
                        break;
                    }
                    backtracks++;
                    continue;
                }

                List<String[]> candidates = new ArrayList<>();
                for (Map.Entry<String, Double> e : dist.entrySet()) {
                    String token = e.getKey();
                    double prob = e.getValue();
                    if (tried.contains(token)) {
                        continue;
                    }
                    if (token.equals(endToken)) {
                        if (tokensInSentence < perMin) {
                            continue;
                        }
                    }
                    else if (checkLength && !isSpecial(token)) {
                        List<String> nonSpecial = filterSpecial(context);
                        List<String> seq = new ArrayList<>(lastK(nonSpecial, mlmI));
                        seq.add(token);
                        if (seq.size() > mlmI && suffixes.hasPrefix(seq)) {
                            continue;
                        }
                    }
                    candidates.add(new String[] {token, String.valueOf(prob)});
                }

                if (candidates.isEmpty()) {
                    if (!backtrack(context, choicePoints, sentenceStarts, floor, endsSeen)) {
                        gaveUp = true;
                        break;
                    }
                    backtracks++;
                    continue;
                }

                String token = weightedSelect(candidates);
                tried.add(token);
                ChoicePoint cp = new ChoicePoint();
                cp.triedTokens = tried;
                cp.isSentenceEnd = false;
                choicePoints.put(pos, cp);

                if (token.equals(endToken)) {
                    int sentLen = tokensInSentence;
                    if (sentLen < perMin || sentLen > perMax) {
                        continue;
                    }
                    context.add(token);
                    cp.isSentenceEnd = true;
                    endsSeen[0]++;
                    sentenceStarts.add(context.size());
                    continue;
                }
                context.add(token);
            }

            if (!gaveUp && endsSeen[0] == numSentences) {
                return splitIntoSentences(context, sentenceStarts);
            }
        }
        throw new RuntimeException("backoff failed after " + maxAttempts + " attempts");
    }

    /**
     * JS {@code backtrack} — pops one token, adjusting sentence bookkeeping. Returns false if
     * the floor was reached (cannot backtrack further). The {@code backtracks}/{@code endsSeen}
     * counters are passed as single-element arrays so the mutation is visible to the caller.
     */
    private boolean backtrack(List<String> context, Map<Integer, ChoicePoint> choicePoints,
        List<Integer> sentenceStarts, int floor, int[] endsSeen) {
        if (context.size() <= floor) {
            return false;
        }
        int poppedIdx = context.size() - 1;
        context.remove(poppedIdx);
        ChoicePoint cp = choicePoints.get(poppedIdx);
        if (cp != null && cp.isSentenceEnd) {
            endsSeen[0]--;
            sentenceStarts.remove(sentenceStarts.size() - 1);
        }
        if (cp != null) {
            cp.isSentenceEnd = false;
        }
        return true;
    }

    private List<String> randomStarter(List<String> validPrompt) {
        if (!validPrompt.isEmpty()) {
            return new ArrayList<>(validPrompt);
        }
        List<String> out = new ArrayList<>();
        out.add(rita.RiTa.randomizer.pselectObj(suffixes.startIndexDist()));
        return out;
    }

    private List<String> splitIntoSentences(List<String> context, List<Integer> sentenceStarts) {
        List<String> sentences = new ArrayList<>();
        List<Integer> bounds = new ArrayList<>();
        bounds.add(0);
        for (int i = 1; i < sentenceStarts.size(); i++) {
            bounds.add(sentenceStarts.get(i));
        }
        for (int i = 0; i < bounds.size() - 1; i++) {
            List<String> slice = new ArrayList<>(context.subList(bounds.get(i), bounds.get(i + 1)));
            slice.removeIf(t -> t.equals(startToken) || t.equals(endToken));
            sentences.add(untokenize.apply(slice));
        }
        return sentences;
    }

    private String weightedSelect(List<String[]> candidates) {
        String chosen = candidates.get(candidates.size() - 1)[0];
        double weightSum = 0;
        for (String[] c : candidates) {
            double prob = Double.parseDouble(c[1]);
            weightSum += prob;
            if (Model.random() * weightSum < prob) {
                chosen = c[0];
            }
        }
        return chosen;
    }

    /** JS {@code build(opts)}. */
    @Override
    public BackoffModel build(Map<String, Object> opts) {
        this.tokenCount = 0;
        if (tokens != null && !tokens.isEmpty()) {
            this.suffixes = new SuffixArray(tokens, opts == null ? Map.of() : opts);
            this.tokenCount = tokens.size();
            this.tokens = null;
            this.ready = true;
        }
        return this;
    }

    @Override
    public BackoffModel build() {
        return build(Map.of());
    }

    /** JS {@code pselect(dist)} — selects a key from a token-&gt;prob map. */
    public String pselect(Map<String, Double> dist) {
        if (dist == null) {
            throw new RuntimeException("object required");
        }
        double cutoff = 0;
        double point = Model.random();
        List<String> keys = new ArrayList<>(dist.keySet());
        for (int i = 0; i < keys.size() - 1; i++) {
            cutoff += dist.get(keys.get(i));
            if (point < cutoff) {
                return keys.get(i);
            }
        }
        return keys.get(keys.size() - 1);
    }

    /** JS {@code resolveOpts(n, options, ignorableKeys)}. */
    public static Map<String, Object> resolveOpts(int n, Map<String, Object> options) {
        return resolveOpts(n, options, List.of());
    }

    @SuppressWarnings("unchecked")
    public static Map<String, Object> resolveOpts(int n, Map<String, Object> options, List<String> ignorableKeys) {
        if (options != null && !isObject(options)) {
            throw new RuntimeException("Options must be an object");
        }
        Map<String, Object> resolved = new LinkedHashMap<>(options == null ? Map.of() : options);

        for (String key : new ArrayList<>(resolved.keySet())) {
            if (generationAliases.containsKey(key)) {
                String canonical = generationAliases.get(key);
                if (!resolved.containsKey(canonical) || resolved.get(canonical) == null) {
                    resolved.put(canonical, resolved.get(key));
                }
                resolved.remove(key);
            }
        }
        for (Map.Entry<String, Object> e : generationDefaults.entrySet()) {
            if (!resolved.containsKey(e.getKey()) || resolved.get(e.getKey()) == null) {
                resolved.put(e.getKey(), e.getValue());
            }
        }
        List<String> allowed = new ArrayList<>(generationIgnorable);
        allowed.addAll(ignorableKeys);
        for (String key : new ArrayList<>(resolved.keySet())) {
            if (!generationDefaults.containsKey(key) && !allowed.contains(key)) {
                throw new RuntimeException("Invalid option key: " + key);
            }
        }
        double mlm = numOpt(resolved, "maxLengthMatch", Double.POSITIVE_INFINITY);
        if (Double.isFinite(mlm) && mlm < n) {
            throw new RuntimeException("maxLengthMatch (" + mlm + ") must be >= n (" + n + ")");
        }
        if (Double.isFinite(n) && n > 1) {
            resolved.put("n", n);
        }
        return resolved;
    }

    /** JS {@code buildTree(n, prompt, opts, depth, tokensSoFar)}. */
    private List<Node> buildTree(int n, List<String> prompt, Map<String, Object> opts) {
        return buildTree(n, prompt, opts, (int) numOpt(opts, "depth", 50), 0);
    }

    private List<Node> buildTree(int n, List<String> prompt, Map<String, Object> opts, int depth) {
        return buildTree(n, prompt, opts, depth, 0);
    }

    private List<Node> buildTree(int n, List<String> prompt, Map<String, Object> opts, int depth, int tokensSoFar) {
        if (depth == 0) {
            return new ArrayList<>();
        }
        int topK = (int) numOpt(opts, "topK", 20);
        double temp = numOpt(opts, "temp", 1);
        int minLength = (int) numOpt(opts, "minLength", 5);
        int maxLength = (int) numOpt(opts, "maxLength", 999);
        double maxLengthMatch = numOpt(opts, "maxLengthMatch", Double.POSITIVE_INFINITY);
        boolean forceOriginal = truthy(opts.get("forceOriginal"));
        final int mlm = (int) maxLengthMatch;
        final boolean checkLength = Double.isFinite(maxLengthMatch);

        if (!ready) {
            build();
        }
        Map<String, Object> saOpts = new LinkedHashMap<>();
        saOpts.put("temp", temp);
        saOpts.put("n", n);
        List<String> query = lastK(prompt, n - 1);
        Map<String, Double> dist = suffixes.pdist(query, saOpts);
        if ((dist == null || dist.isEmpty()) && query.size() > 1) {
            dist = suffixes.pdist(new ArrayList<>(query.subList(1, query.size())), saOpts);
        }
        if (dist == null) {
            return new ArrayList<>();
        }

        List<Map.Entry<String, Double>> entries = new ArrayList<>(dist.entrySet());
        entries.sort((a, b) -> Double.compare(b.getValue(), a.getValue()));
        if (entries.size() > topK) {
            entries = new ArrayList<>(entries.subList(0, topK));
        }
        double entryTotal = 0;
        for (Map.Entry<String, Double> e : entries) {
            entryTotal += e.getValue();
        }

        List<Node> nodes = new ArrayList<>();
        for (Map.Entry<String, Double> e : entries) {
            String token = e.getKey();
            double prob = e.getValue() / entryTotal;
            boolean isEnd = token.equals(endToken) || token.equals(startToken);
            if (isEnd && tokensSoFar < minLength) {
                continue;
            }
            if (!isEnd && tokensSoFar >= maxLength) {
                continue;
            }
            if (!isEnd && checkLength) {
                List<String> seq = new ArrayList<>(lastK(prompt, mlm));
                seq.add(token);
                if (seq.size() > mlm && suffixes.hasPrefix(seq)) {
                    continue;
                }
            }
            if (isEnd && forceOriginal && suffixes.hasPrefix(prompt)) {
                continue;
            }
            Node node = new Node();
            node.token = token;
            node.prob = prob;
            node.isEnd = isEnd;
            if (!isEnd && depth > 1) {
                List<String> nextPrompt = new ArrayList<>(prompt);
                nextPrompt.add(token);
                node.children = buildTree(n, nextPrompt, opts, depth - 1, tokensSoFar + 1);
            }
            if (!isEnd && node.children.isEmpty()) {
                continue;
            }
            nodes.add(node);
        }
        return nodes;
    }

    /** JS {@code collectPaths}. */
    private static void collectPaths(List<Node> nodes, List<Map<String, Object>> currentPath,
        List<List<Map<String, Object>>> accumulator) {
        for (Node node : nodes) {
            if (node.isEnd) {
                continue;
            }
            List<Map<String, Object>> path = new ArrayList<>(currentPath);
            path.add(nodeMap(node.token, node.prob));
            boolean allEnd = true;
            for (Node c : node.children) {
                if (!c.isEnd) {
                    allEnd = false;
                    break;
                }
            }
            if (node.children.isEmpty() || allEnd) {
                accumulator.add(path);
            }
            else {
                collectPaths(node.children, path, accumulator);
            }
        }
    }

    /** JS {@code walk} generator (pathGenerator) — collects paths eagerly. */
    private static void walkPaths(List<Node> nodes, List<Map<String, Object>> currentPath, int promptLen,
        List<Map<String, Object>> out) {
        for (Node node : nodes) {
            if (node.isEnd) {
                continue;
            }
            List<Map<String, Object>> path = new ArrayList<>(currentPath);
            path.add(nodeMap(node.token, node.prob));
            boolean allEnd = true;
            for (Node c : node.children) {
                if (!c.isEnd) {
                    allEnd = false;
                    break;
                }
            }
            if (node.children.isEmpty() || allEnd) {
                Map<String, Object> rec = new LinkedHashMap<>();
                rec.put("tokens", path);
                rec.put("prob", pathProb(path, promptLen));
                out.add(rec);
            }
            else {
                walkPaths(node.children, path, promptLen, out);
            }
        }
    }

    // ---------------- helpers ----------------

    private static Map<String, Object> nodeMap(String token, double prob) {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("token", token);
        m.put("prob", prob);
        return m;
    }

    private static double pathProb(List<Map<String, Object>> path, int skip) {
        double p = 1;
        for (int i = skip; i < path.size(); i++) {
            p *= ((Number) path.get(i).get("prob")).doubleValue();
        }
        return p;
    }

    private static boolean isSpecial(String token) {
        return token != null && token.startsWith("<") && token.endsWith(">");
    }

    private static List<String> filterSpecial(List<String> tokens) {
        List<String> out = new ArrayList<>();
        for (String t : tokens) {
            if (!isSpecial(t)) {
                out.add(t);
            }
        }
        return out;
    }

    /** JS {@code arr.slice(-k)} — last k elements (whole array when k &lt;= 0 or k &gt;= length). */
    private static List<String> lastK(List<String> arr, int k) {
        if (k <= 0) {
            return new ArrayList<>(arr);
        }
        int start = Math.max(0, arr.size() - k);
        return new ArrayList<>(arr.subList(start, arr.size()));
    }

    /** JS {@code a || b} — falls back only on null/undefined (empty map is truthy in JS). */
    private static Map<String, Double> orElse(Map<String, Double> a, Map<String, Double> b) {
        return a != null ? a : b;
    }

    @SuppressWarnings("unchecked")
    private static Predicate<String> untilPredicate(Object generateUntil) {
        if (generateUntil instanceof Predicate) {
            return (Predicate<String>) generateUntil;
        }
        if (generateUntil instanceof java.util.function.BiPredicate) {
            java.util.function.BiPredicate<String, List<String>> f =
                (java.util.function.BiPredicate<String, List<String>>) generateUntil;
            return t -> f.test(t, List.of());
        }
        String s = String.valueOf(generateUntil);
        return t -> t.equals(s);
    }

    private static double numOpt(Map<String, Object> opts, String key, double def) {
        Object v = opts.get(key);
        return v instanceof Number ? ((Number) v).doubleValue() : def;
    }
}
