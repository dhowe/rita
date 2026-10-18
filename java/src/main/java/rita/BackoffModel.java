package rita;

import java.util.Iterator;
import java.util.List;
import java.util.Map;

/**
 * Backoff language model — stub for {@code js/src/backoff.js} (exported as
 * {@code RiTa.BackoffModel}). Extends {@link Model} as in JS. Methods throw until ported.
 */
public class BackoffModel extends Model {

    public static boolean SILENT = true;

    /** JS {@code generationDefaults} — canonical generation tunables. */
    public static final Map<String, Object> generationDefaults = new java.util.LinkedHashMap<>();
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

    public BackoffModel() {
    }

    public BackoffModel(Object input) {
        throw RiTa.notPorted("BackoffModel.constructor");
    }

    public BackoffModel(Object input, Map<String, Object> opts) {
        throw RiTa.notPorted("BackoffModel.constructor");
    }

    public static BackoffModel fromJSON(String json) {
        throw RiTa.notPorted("BackoffModel.fromJSON");
    }

    public static BackoffModel fromJSON(Map<String, Object> obj) {
        throw RiTa.notPorted("BackoffModel.fromJSON");
    }

    /** JS {@code generateSentences(n, prompt, opts)} — always returns an array of strings. */
    public List<String> generateSentences(int n, List<String> prompt, Map<String, Object> opts) {
        throw RiTa.notPorted("BackoffModel.generateSentences");
    }

    /** JS {@code generationPaths(n, prompt, opts)} — list of {tokens, prob, inInput}. */
    public List<Map<String, Object>> generationPaths(int n, List<String> prompt, Map<String, Object> opts) {
        throw RiTa.notPorted("BackoffModel.generationPaths");
    }

    /** JS {@code pathGenerator(n, prompt, opts)} — generator yielding paths. */
    public Iterator<Map<String, Object>> pathGenerator(int n, List<String> prompt, Map<String, Object> opts) {
        throw RiTa.notPorted("BackoffModel.pathGenerator");
    }

    /** JS {@code streamTokens(n, prompt, opts)} — generator yielding tokens. */
    public Iterator<String> streamTokens(int n, List<String> prompt, Map<String, Object> opts) {
        throw RiTa.notPorted("BackoffModel.streamTokens");
    }

    /** JS {@code resolveOpts(n, options, ignorableKeys)} — validates/normalises options. */
    public static Map<String, Object> resolveOpts(int n, Map<String, Object> options) {
        throw RiTa.notPorted("BackoffModel.resolveOpts");
    }

    public static Map<String, Object> resolveOpts(int n, Map<String, Object> options, List<String> ignorableKeys) {
        throw RiTa.notPorted("BackoffModel.resolveOpts");
    }

    /** JS {@code pselect(dist)} — selects a key from a token->prob map. */
    public String pselect(Map<String, Double> dist) {
        throw RiTa.notPorted("BackoffModel.pselect");
    }

    @Override
    public BackoffModel build(Map<String, Object> opts) {
        throw RiTa.notPorted("BackoffModel.build");
    }

    @Override
    public BackoffModel build() {
        throw RiTa.notPorted("BackoffModel.build");
    }

    @Override
    public BackoffModel addText(String text) {
        throw RiTa.notPorted("BackoffModel.addText");
    }

    @Override
    public BackoffModel addText(Object input) {
        throw RiTa.notPorted("BackoffModel.addText");
    }

    @Override
    public BackoffModel addSentences(List<String> sentences) {
        throw RiTa.notPorted("BackoffModel.addSentences");
    }

    @Override
    public BackoffModel addTokens(List<String> tokens) {
        throw RiTa.notPorted("BackoffModel.addTokens");
    }
}
