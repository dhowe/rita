package rita;

import java.util.List;
import java.util.Map;

/**
 * Suffix-gram language model — stub for {@code js/src/model.js} (exported as {@code RiTa.Model}).
 * Fields mirror the JS object; methods throw until ported.
 */
public class Model {

    public static boolean SILENT = false;
    public static RiTa RiTa = null;

    /** Option keys (mirrors SuffixGram.options). */
    public static final String[] options = {
        "debug", "ready", "suffixes", "compressed", "startToken", "endToken", "tokenize", "untokenize",
    };

    /** Serialized field names (mirrors SuffixGram.__dict__). */
    public static final String[] __dict__ = {
        "ready", "startToken", "endToken", "tokenize", "untokenize", "tokens", "tokenCount", "suffixes",
    };

    // instance fields
    public boolean ready = false;
    public String startToken = SuffixArray.SEQ_START_TOKEN;
    public String endToken = SuffixArray.SEQ_END_TOKEN;
    public Object tokenize;
    public Object untokenize;
    public List<String> tokens;
    public int tokenCount = 0;
    public List<Object> input;
    public int[] seqmap;
    public SuffixArray suffixes;

    public Model() {
    }

    public Model(Object input) {
        throw RiTa.notPorted("Model.constructor");
    }

    public Model(Object input, Map<String, Object> opts) {
        throw RiTa.notPorted("Model.constructor");
    }

    public static Model fromJSON(String json) {
        throw RiTa.notPorted("Model.fromJSON");
    }

    public Map<String, Object> toJSON() {
        throw RiTa.notPorted("Model.toJSON");
    }

    public int size() {
        throw RiTa.notPorted("Model.size");
    }

    /** JS {@code build(opts)} — returns {@code this} for chaining. */
    public Model build(Map<String, Object> opts) {
        throw RiTa.notPorted("Model.build");
    }

    public Model build() {
        throw RiTa.notPorted("Model.build");
    }

    /** JS {@code addText(text)} — returns {@code this}. */
    public Model addText(String text) {
        throw RiTa.notPorted("Model.addText");
    }

    /** JS {@code addText(...)} — non-string input throws. */
    public Model addText(Object input) {
        throw RiTa.notPorted("Model.addText");
    }

    /** JS {@code addSentences(sentences)} — returns {@code this}. */
    public Model addSentences(List<String> sentences) {
        throw RiTa.notPorted("Model.addSentences");
    }

    /** JS {@code addTokens(tokens)} — returns {@code this}. */
    public Model addTokens(List<String> tokens) {
        throw RiTa.notPorted("Model.addTokens");
    }

    public List<String> _decode(List<Integer> indices) {
        throw RiTa.notPorted("Model._decode");
    }

    public int randSeqStart() {
        throw RiTa.notPorted("Model.randSeqStart");
    }

    public String toString(Map<String, Object> opts) {
        throw RiTa.notPorted("Model.toString");
    }
}
