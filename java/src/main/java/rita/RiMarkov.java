package rita;

import java.util.Iterator;
import java.util.List;
import java.util.Map;

/**
 * Markov chain generator — stub for {@code js/src/markov.js} (exported as {@code RiTa.RiMarkov}).
 * Methods throw until ported.
 */
public class RiMarkov {

    public static RiTa RiTa = null;

    /** n-gram order (mirrors {@code this.n}). */
    public int n = -1;
    /** The underlying model (mirrors {@code this.model}). */
    public BackoffModel model;
    /** Instance generation defaults copied from opts (mirrors {@code this.opts}). */
    public Map<String, Object> opts = new java.util.LinkedHashMap<>();
    /** Raw input text, kept for error messages (mirrors {@code this.input}). */
    public Object input;

    public RiMarkov() {
    }

    public RiMarkov(int n) {
        throw RiTa.notPorted("RiMarkov.constructor");
    }

    public RiMarkov(int n, Map<String, Object> opts) {
        throw RiTa.notPorted("RiMarkov.constructor");
    }

    /** JS {@code new RiMarkov(text)} / {@code new RiMarkov({opts})} / {@code new RiMarkov(text, opts)}. */
    public RiMarkov(Object input) {
        throw RiTa.notPorted("RiMarkov.constructor");
    }

    public RiMarkov(Object input, Map<String, Object> opts) {
        throw RiTa.notPorted("RiMarkov.constructor");
    }

    public static RiMarkov fromJSON(String json) {
        throw RiTa.notPorted("RiMarkov.fromJSON");
    }

    public String toJSON() {
        throw RiTa.notPorted("RiMarkov.toJSON");
    }

    public BackoffModel addText(String text) {
        throw RiTa.notPorted("RiMarkov.addText");
    }

    public BackoffModel addText(Object input) {
        throw RiTa.notPorted("RiMarkov.addText");
    }

    public BackoffModel addSentences(List<String> sentences) {
        throw RiTa.notPorted("RiMarkov.addSentences");
    }

    public BackoffModel addTokens(List<String> tokens) {
        throw RiTa.notPorted("RiMarkov.addTokens");
    }

    // ---- generate (union return: String when numSentences==1, else List<String>) ----

    public Object generate() {
        throw RiTa.notPorted("RiMarkov.generate");
    }

    public Object generate(int n) {
        throw RiTa.notPorted("RiMarkov.generate");
    }

    public Object generate(Map<String, Object> opts) {
        throw RiTa.notPorted("RiMarkov.generate");
    }

    /** JS {@code generate(n, opts)} — n-gram order plus options, empty prompt. */
    public Object generate(int n, Map<String, Object> opts) {
        throw RiTa.notPorted("RiMarkov.generate");
    }

    /** JS {@code generate(prompt, opts)} — prompt array plus options. */
    public Object generate(Object prompt, Map<String, Object> opts) {
        throw RiTa.notPorted("RiMarkov.generate");
    }

    public Object generate(int n, Object prompt, Map<String, Object> opts) {
        throw RiTa.notPorted("RiMarkov.generate");
    }

    /** JS {@code generate(n, prompt, opts)} where n may be undefined. */
    public Object generate(Object n, Object prompt, Map<String, Object> opts) {
        throw RiTa.notPorted("RiMarkov.generate");
    }

    // ---- stream (yields tokens) ----

    public Iterable<String> stream(int n, Object prompt, Map<String, Object> opts) {
        throw RiTa.notPorted("RiMarkov.stream");
    }

    public Iterable<String> stream(Object prompt, Map<String, Object> opts) {
        throw RiTa.notPorted("RiMarkov.stream");
    }

    public Iterable<String> stream(Map<String, Object> opts) {
        throw RiTa.notPorted("RiMarkov.stream");
    }

    // ---- completions ----

    public List<String> completions(List<String> pre) {
        throw RiTa.notPorted("RiMarkov.completions");
    }

    public List<String> completions(List<String> pre, List<String> post) {
        throw RiTa.notPorted("RiMarkov.completions");
    }

    public List<String> completions(List<String> pre, List<String> post, Map<String, Object> opts) {
        throw RiTa.notPorted("RiMarkov.completions");
    }

    // ---- probabilities / probability ----

    public Map<String, Double> probabilities() {
        throw RiTa.notPorted("RiMarkov.probabilities");
    }

    public Map<String, Double> probabilities(List<String> tokens) {
        throw RiTa.notPorted("RiMarkov.probabilities");
    }

    /** JS {@code probabilities(non-array)} — throws (tokens must be an array). */
    public Map<String, Double> probabilities(Object tokens) {
        throw RiTa.notPorted("RiMarkov.probabilities");
    }

    public Map<String, Double> probabilities(List<String> tokens, Map<String, Object> opts) {
        throw RiTa.notPorted("RiMarkov.probabilities");
    }

    /** @deprecated — throws in JS. */
    public double probability(List<String> prompt) {
        throw RiTa.notPorted("RiMarkov.probability");
    }

    public double probability(List<String> prompt, Object next) {
        throw RiTa.notPorted("RiMarkov.probability");
    }

    /** JS {@code probability(non-array, ...)} — throws (prompt must be an array). */
    public double probability(Object prompt, Object next) {
        throw RiTa.notPorted("RiMarkov.probability");
    }

    public double probability(String token) {
        throw RiTa.notPorted("RiMarkov.probability");
    }

    public int size() {
        throw RiTa.notPorted("RiMarkov.size");
    }

    public SuffixArray suffixes() {
        throw RiTa.notPorted("RiMarkov.suffixes");
    }

    @Override
    public String toString() {
        throw RiTa.notPorted("RiMarkov.toString");
    }
}
