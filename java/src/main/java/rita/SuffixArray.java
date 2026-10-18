package rita;

import java.util.List;
import java.util.Map;

/**
 * Suffix array — stub for {@code js/src/suffixes.js}. Fields mirror the JS object so tests
 * that read them compile; methods throw until ported.
 */
public class SuffixArray {

    public static final String SEQ_START_TOKEN = "<s>";
    public static final String SEQ_END_TOKEN = "</s>";
    public static boolean SILENT = true;
    public static int XOVER_WINDOW = 8;
    public static boolean USE_COMPRESSION = true;
    public static RiTa RiTa = null;

    /** Field names serialized by toJSON/fromJSON (mirrors SuffixArray.__dict__). */
    public static final String[] __dict__ = {
        "startToken", "endToken", "xoverWindow", "compressed", "length", "decoder", "encoder",
        "input", "seqmap", "data", "xovers",
    };

    /** Field names copied from a serialized meta record (mirrors SuffixArray.__props__). */
    public static final String[] __props__ = {
        "startToken", "endToken", "xoverWindow", "compressed", "length", "decoder", "encoder",
    };

    // instance fields (public so tests can read them like JS)
    public int length = 0;
    public List<Object> input;
    public int[] seqmap;
    public int[] data;
    public int[] ranks;
    public int[] xovers;
    public String startToken = SEQ_START_TOKEN;
    public String endToken = SEQ_END_TOKEN;
    public int xoverWindow = XOVER_WINDOW;
    public boolean compressed = USE_COMPRESSION;
    public String[] decoder;
    public Map<String, Integer> encoder;

    public SuffixArray() {
    }

    public SuffixArray(List<String> tokens) {
        throw RiTa.notPorted("SuffixArray.constructor");
    }

    public SuffixArray(List<String> tokens, Map<String, Object> opts) {
        throw RiTa.notPorted("SuffixArray.constructor");
    }

    public static SuffixArray fromJSON(String json) {
        throw RiTa.notPorted("SuffixArray.fromJSON");
    }

    public String toJSON() {
        throw RiTa.notPorted("SuffixArray.toJSON");
    }

    /** JS {@code arrayCompare(a, b)} — length of the common prefix, or -1 when equal. */
    public static int arrayCompare(List<String> a, List<String> b) {
        throw RiTa.notPorted("SuffixArray.arrayCompare");
    }

    /** JS {@code arrayCompareSlices(arr, aStart, aEnd, bStart, bEnd)}. */
    public static int arrayCompareSlices(List<String> arr, int aStart, int aEnd, int bStart, int bEnd) {
        throw RiTa.notPorted("SuffixArray.arrayCompareSlices");
    }

    /** JS {@code normaliseDist(mapping, temp)}. */
    public static Map<String, Double> normaliseDist(Map<String, Double> mapping) {
        throw RiTa.notPorted("SuffixArray.normaliseDist");
    }

    public static Map<String, Double> normaliseDist(Map<String, Double> mapping, double temp) {
        throw RiTa.notPorted("SuffixArray.normaliseDist");
    }

    /** Returns {min, max} indices for the token sequence. */
    public int[] find(List<String> tokens, Map<String, Object> opts) {
        throw RiTa.notPorted("SuffixArray.find");
    }

    public int[] find(List<String> tokens) {
        throw RiTa.notPorted("SuffixArray.find");
    }

    public boolean hasPrefix(List<String> tokens) {
        throw RiTa.notPorted("SuffixArray.hasPrefix");
    }

    public boolean hasPrefix(List<String> tokens, Map<String, Object> opts) {
        throw RiTa.notPorted("SuffixArray.hasPrefix");
    }

    public boolean hasSuffix(List<String> tokens) {
        throw RiTa.notPorted("SuffixArray.hasSuffix");
    }

    public boolean isUnique(List<String> tokens) {
        throw RiTa.notPorted("SuffixArray.isUnique");
    }

    public Map<String, Double> pdist(List<String> tokens) {
        throw RiTa.notPorted("SuffixArray.pdist");
    }

    public Map<String, Double> pdist(List<String> tokens, Map<String, Object> opts) {
        throw RiTa.notPorted("SuffixArray.pdist");
    }

    public List<String> tokensFor(int index) {
        throw RiTa.notPorted("SuffixArray.tokensFor");
    }

    public List<String> tokensFor(int index, int n) {
        throw RiTa.notPorted("SuffixArray.tokensFor");
    }

    public List<List<String>> tokensForRange(int min, int max) {
        throw RiTa.notPorted("SuffixArray.tokensForRange");
    }

    /** JS {@code startIndexDist()} — distribution of sentence-start tokens. */
    public Map<String, Double> startIndexDist() {
        throw RiTa.notPorted("SuffixArray.startIndexDist");
    }

    /** JS {@code startIndexes()} — indices of sentence starts. */
    public List<Integer> startIndexes() {
        throw RiTa.notPorted("SuffixArray.startIndexes");
    }

    /** JS {@code randSeqStart()} — a random sentence-start token. */
    public String randSeqStart() {
        throw RiTa.notPorted("SuffixArray.randSeqStart");
    }

    /** JS {@code _decode(index)} — the token at a compressed index. */
    public String _decode(int index) {
        throw RiTa.notPorted("SuffixArray._decode");
    }

    public List<String> _decode(List<Integer> indices) {
        throw RiTa.notPorted("SuffixArray._decode");
    }

    /** JS {@code build(s)} — (re)build the suffix array from tokens. */
    public void build(List<String> tokens) {
        throw RiTa.notPorted("SuffixArray.build");
    }

    @Override
    public String toString() {
        throw RiTa.notPorted("SuffixArray.toString");
    }

    public String toString(Map<String, Object> opts) {
        throw RiTa.notPorted("SuffixArray.toString");
    }
}
