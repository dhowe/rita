package rita;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Suffix array — port of {@code js/src/suffixes.js}. Builds a (optionally compressed) suffix
 * array over a token sequence and supports prefix/suffix search, next-token probability
 * distributions, and JSON (de)serialization.
 *
 * <p>Representation note: the public {@link #input} field stores each token as a singleton
 * {@code List} (so {@code input.get(i)} is a list, matching the JS test's
 * {@code _decode(input[i+1])} usage), while the algorithm operates on the flat {@link #seq}.
 * In compressed mode {@code seq} holds encoded {@code Integer}s; in uncompressed mode it holds
 * the original {@code String} tokens (the mode used by the Markov/Backoff models).
 */
public class SuffixArray {

    public static final String SEQ_START_TOKEN = "<s>";
    public static final String SEQ_END_TOKEN = "</s>";
    public static boolean SILENT = true;
    public static int XOVER_WINDOW = 8;
    public static boolean USE_COMPRESSION = true;

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
    public List<Object> input = new ArrayList<>();
    public int[] seqmap = new int[0];
    public int[] data = new int[0];
    public int[] xovers = new int[0];
    public String startToken = SEQ_START_TOKEN;
    public String endToken = SEQ_END_TOKEN;
    public int xoverWindow = XOVER_WINDOW;
    public boolean compressed = USE_COMPRESSION;
    public List<String> decoder;
    public Map<String, Integer> encoder;

    /** Flat sequence backing the algorithm: Integer (compressed) or String (uncompressed). */
    private Object[] seq = new Object[0];
    private List<Object> _startIndexes = null;
    private Map<String, Double> _startIndexDist = null;

    public SuffixArray() {
    }

    public SuffixArray(List<String> tokens) {
        this(tokens, Map.of());
    }

    public SuffixArray(List<String> tokens, Map<String, Object> opts) {
        if (opts != null) {
            if (opts.get("startToken") != null) {
                startToken = (String) opts.get("startToken");
            }
            if (opts.get("endToken") != null) {
                endToken = (String) opts.get("endToken");
            }
            if (opts.get("xoverWindow") != null) {
                xoverWindow = (int) Util.numOpt(opts, "xoverWindow", xoverWindow);
            }
            if (opts.get("compressed") != null) {
                compressed = truthy(opts.get("compressed"));
            }
        }
        if (tokens != null) {
            List<Object> comp = compressed ? compressTokens(tokens) : wrapRaw(tokens);
            build(comp);
        }
    }

    /** JS {@code compressTokens} — build the word↔index map and return the compressed input. */
    private List<Object> compressTokens(List<String> input) {
        if (input == null || input.isEmpty()) {
            return new ArrayList<>();
        }
        List<String> words = new ArrayList<>(new java.util.LinkedHashSet<>(input));
        Collections.sort(words);
        decoder = new ArrayList<>(words);
        encoder = new LinkedHashMap<>();
        for (int i = 0; i < decoder.size(); i++) {
            encoder.put(decoder.get(i), i);
        }
        List<Object> compressed = new ArrayList<>(input.size());
        for (String w : input) {
            compressed.add(new ArrayList<>(List.of(encoder.get(w))));
        }
        return compressed;
    }

    /** Uncompressed view: each token wrapped in a singleton list, so {@code input.get(i)} is a list. */
    private List<Object> wrapRaw(List<String> input) {
        List<Object> out = new ArrayList<>(input.size());
        for (String w : input) {
            List<Object> one = new ArrayList<>();
            one.add(w);
            out.add(one);
        }
        return out;
    }

    public static SuffixArray fromJSON(String json) {
        return fromRecords((List<?>) Json.parse(json));
    }

    /** Rebuilds a SuffixArray from the serialized record list (meta record + per-index records). */
    public static SuffixArray fromRecords(List<?> records) {
        Map<String, Object> meta = (Map<String, Object>) records.get(0);
        SuffixArray sa = new SuffixArray();
        sa.startToken = (String) meta.get("startToken");
        sa.endToken = (String) meta.get("endToken");
        sa.xoverWindow = asInt(meta.get("xoverWindow"));
        sa.compressed = truthy(meta.get("compressed"));
        sa.length = asInt(meta.get("length"));
        List<?> dec = (List<?>) meta.get("decoder");
        sa.decoder = new ArrayList<>(dec.size());
        for (int i = 0; i < dec.size(); i++) {
            sa.decoder.add((String) dec.get(i));
        }
        Map<String, Object> enc = (Map<String, Object>) meta.get("encoder");
        sa.encoder = new LinkedHashMap<>();
        for (Map.Entry<String, Object> e : enc.entrySet()) {
            sa.encoder.put(e.getKey(), asInt(e.getValue()));
        }
        int n = records.size() - 1;
        sa.input = new ArrayList<>(n);
        sa.seq = new Object[n];
        sa.data = new int[n];
        sa.xovers = new int[n];
        sa.seqmap = new int[n];
        for (int i = 0; i < n; i++) {
            Map<String, Object> rec = (Map<String, Object>) records.get(i + 1);
            List<?> inp = (List<?>) rec.get("input");
            List<Object> vals = new ArrayList<>(inp.size());
            for (Object o : inp) {
                vals.add(sa.compressed ? (Object) asInt(o) : (Object) String.valueOf(o));
            }
            sa.input.add(vals);
            sa.seq[i] = vals.isEmpty() ? null : vals.get(0);
            sa.data[i] = asInt(rec.get("data"));
            sa.xovers[i] = asInt(rec.get("xover"));
            sa.seqmap[i] = asInt(rec.get("seqmap"));
        }
        return sa;
    }

    public String toJSON() {
        StringBuilder sb = new StringBuilder();
        sb.append('[');
        sb.append('{');
        sb.append("\"startToken\":").append(str(startToken)).append(',');
        sb.append("\"endToken\":").append(str(endToken)).append(',');
        sb.append("\"xoverWindow\":").append(xoverWindow).append(',');
        sb.append("\"compressed\":").append(compressed).append(',');
        sb.append("\"length\":").append(length).append(',');
        sb.append("\"decoder\":[");
        for (int i = 0; i < decoder.size(); i++) {
            if (i > 0) {
                sb.append(',');
            }
            sb.append(str(decoder.get(i)));
        }
        sb.append("],\"encoder\":{");
        int k = 0;
        for (Map.Entry<String, Integer> e : encoder.entrySet()) {
            if (k++ > 0) {
                sb.append(',');
            }
            sb.append(str(e.getKey())).append(':').append(e.getValue());
        }
        sb.append("}}");
        for (int i = 0; i < length; i++) {
            sb.append(",{\"input\":[");
            List<?> inp = (List<?>) input.get(i);
            for (int j = 0; j < inp.size(); j++) {
                if (j > 0) {
                    sb.append(',');
                }
                Object v = inp.get(j);
                sb.append(v instanceof String ? str((String) v) : v);
            }
            sb.append("],\"data\":").append(data[i])
                .append(",\"xover\":").append(xovers[i])
                .append(",\"seqmap\":").append(seqmap[i]).append('}');
        }
        sb.append(']');
        return sb.toString();
    }

    /** JS {@code find(query, opts)} — the [min, max] index range of suffixes starting with query. */
    public int[] find(List<String> query, Map<String, Object> opts) {
        if (query == null || query.isEmpty()) {
            query = List.of(startToken);
        }
        List<Object> enc = encode(query);
        Integer start = binsearch(enc, true);
        Integer end = binsearch(enc, false);
        return (start == null || end == null) ? new int[] {0, 0} : new int[] {start, end + 1};
    }

    public int[] find(List<String> query) {
        return find(query, Map.of());
    }

    /** JS {@code normaliseDist(mapping, temp)}. */
    public static Map<String, Double> normaliseDist(Map<String, Double> mapping) {
        return normaliseDist(mapping, 0);
    }

    public static Map<String, Double> normaliseDist(Map<String, Double> mapping, double temp) {
        if (mapping == null) {
            throw new RuntimeException("No mapping");
        }
        Map<String, Double> tdist = new java.util.LinkedHashMap<>();
        if (mapping.isEmpty()) {
            return tdist;
        }
        if (temp == 0) {
            double total = 0;
            for (double v : mapping.values()) {
                total += v;
            }
            for (Map.Entry<String, Double> e : mapping.entrySet()) {
                if (e.getValue() < 0) {
                    throw new RuntimeException("Negative count");
                }
                tdist.put(e.getKey(), e.getValue() / total);
            }
        } else {
            temp = Math.max(temp, 0.01);
            double total = 0;
            for (Map.Entry<String, Double> e : mapping.entrySet()) {
                if (e.getValue() < 0) {
                    throw new RuntimeException("Negative count");
                }
                double pr = Math.exp(e.getValue() / temp);
                tdist.put(e.getKey(), pr);
                total += pr;
            }
            for (Map.Entry<String, Double> e : tdist.entrySet()) {
                e.setValue(e.getValue() / total);
            }
        }
        return tdist;
    }

    /** JS {@code tokensFor(index, len)}. */
    public List<String> tokensFor(int index, int len) {
        if (index < 0 || index > data.length) {
            throw new RuntimeException("Index out of range: " + index);
        }
        int start = data[index];
        return decodeList(seqSlice(start, start + len));
    }

    public List<String> tokensFor(int index) {
        if (index < 0 || index > data.length) {
            throw new RuntimeException("Index out of range: " + index);
        }
        return decodeList(seqSlice(data[index], seq.length));
    }

    public List<List<String>> tokensForRange(int min, int max) {
        if (min < 0 || min >= data.length) {
            throw new RuntimeException("Index out of range");
        }
        if (max < 0) {
            max = data.length - 1;
        }
        List<List<String>> lines = new ArrayList<>();
        for (int i = min; i < max; i++) {
            lines.add(decodeList(seqSlice(data[i], seq.length)));
        }
        return lines;
    }

    public boolean hasPrefix(List<String> query) {
        return hasPrefix(query, Map.of());
    }

    public boolean hasPrefix(List<String> query, Map<String, Object> opts) {
        List<Object> enc = encode(query);
        if (enc == null || enc.isEmpty()) {
            return false;
        }
        int low = 0, high = data.length - 1;
        while (low <= high) {
            int mid = (low + high) >>> 1;
            if (isSubArray(mid, enc)) {
                return true;
            }
            if (lt(mid, enc)) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return false;
    }

    public boolean hasSuffix(List<String> query) {
        List<Object> enc = encode(query);
        int low = 0, high = data.length - 1;
        while (low <= high) {
            int mid = (low + high) >>> 1;
            if (arrayEquals(mid, enc)) {
                return true;
            }
            if (lt(mid, enc)) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return false;
    }

    public boolean isUnique(List<String> sequence) {
        if (sequence == null || sequence.isEmpty()) {
            throw new RuntimeException("Invalid sequence");
        }
        return !hasPrefix(sequence);
    }

    /** JS {@code pdist(query, opts)} — the next-token probability distribution. */
    public Map<String, Double> pdist(List<String> query) {
        return pdist(query, Map.of());
    }

    public Map<String, Double> pdist(List<String> query, Map<String, Object> opts) {
        if (query == null || query.isEmpty()
            || (query.size() == 1 && query.get(0).equals(startToken))) {
            return normalize(startIndexDist());
        }
        int[] mm = find(query, opts);
        Map<String, Double> probDist = distFromIndexes(mm[0], mm[1], query.size());
        if (probDist == null) {
            return null;
        }
        double temp = opts == null ? 1 : Util.numOpt(opts, "temp", 1);
        List<String> tokens = new ArrayList<>(probDist.keySet());
        List<Double> logits = new ArrayList<>();
        for (String t : tokens) {
            logits.add(probDist.get(t));
        }
        List<Double> ndist = softmax(logits, temp);
        Map<String, Double> result = new java.util.LinkedHashMap<>();
        for (int i = 0; i < tokens.size(); i++) {
            result.put(tokens.get(i), ndist.get(i));
        }
        return result;
    }

    private Map<String, Double> distFromIndexes(int min, int max, int queryLength) {
        if (max > min) {
            Map<String, Double> probs = new java.util.LinkedHashMap<>();
            for (int i = min; i < max; i++) {
                int idx = data[i] + queryLength;
                if (idx < seq.length) {
                    String next = decode(seq[idx]);
                    probs.merge(next, 1.0, Double::sum);
                }
            }
            return probs;
        }
        return null;
    }

    /** JS {@code startIndexDist()} — distribution of sentence-start tokens. */
    public Map<String, Double> startIndexDist() {
        if (_startIndexDist == null) {
            List<String> indexes = decodeList(startIndexes());
            _startIndexDist = createDist(indexes, true);
        }
        return _startIndexDist;
    }

    /** JS {@code startIndexes()} — the encoded token following each start token. */
    public List<Object> startIndexes() {
        if (_startIndexes == null) {
            List<Object> indexes = new ArrayList<>();
            for (int i = 0; i < seqmap.length; i++) {
                if (seqmap[i] == 1) {
                    indexes.add(seq[i + 1]);
                }
            }
            _startIndexes = indexes;
        }
        return _startIndexes;
    }

    /** JS {@code randSeqStart()} — a random sentence-start token. */
    public String randSeqStart() {
        List<Object> indexes = startIndexes();
        Object start = indexes.get((int) Math.floor(random() * indexes.size()));
        return decode(start);
    }

    /** JS {@code _decode(index)} — the token at a compressed index. */
    public String _decode(int index) {
        return compressed ? decoder.get(index) : String.valueOf(seq[index]);
    }

    public List<String> _decode(List<Integer> indices) {
        return decodeList(new ArrayList<Object>(indices));
    }

    /** JS {@code build(s)} — (re)build the suffix array from a (compressed) sequence. */
    public void build(List<Object> comp) {
        int len = comp.size();
        seq = new Object[len];
        for (int i = 0; i < len; i++) {
            List<?> one = (List<?>) comp.get(i);
            seq[i] = one.isEmpty() ? null : one.get(0);
        }
        Object[] ranks = new Object[len];
        int[] data = new int[len];
        int[] tmp = new int[len];
        int[] starts = new int[len];
        int[] xovers = new int[len];
        Object startIndex = compressed ? (Object) encoder.get(startToken) : (Object) startToken;
        for (int i = 0; i < len; i++) {
            data[i] = i;
            ranks[i] = seq[i];
            starts[i] = eq(seq[i], startIndex) ? 1 : 0;
        }

        Integer[] order = new Integer[len];
        for (int i = 0; i < len; i++) {
            order[i] = i;
        }
        final Object[] ranksRef = ranks;
        final int lenF = len;
        int gap = 1;
        if (len > 1) {
            do {
                final int g = gap;
                Arrays.sort(order, (x, y) -> cmpRanks(x, y, g, ranksRef, lenF));
                for (int i = 1; i < len; i++) {
                    tmp[i] = tmp[i - 1] + (cmpRanks(order[i - 1], order[i], g, ranksRef, lenF) == -1 ? 1 : 0);
                }
                boolean finalPass = tmp[len - 1] >= len - 1;
                for (int i = 0; i < len; i++) {
                    ranks[order[i]] = tmp[i];
                    if (finalPass && i + 1 < len) {
                        int aStart = order[i], aEnd = order[i] + xoverWindow;
                        int bStart = order[i + 1], bEnd = order[i + 1] + xoverWindow;
                        xovers[i] = arrayCompareSlices(seq, aStart, aEnd, bStart, bEnd);
                    }
                }
                gap <<= 1;
            } while (tmp[len - 1] < len - 1);
        }
        if (len > 0) {
            xovers[len - 1] = -1;
        }

        this.input = comp;
        this.data = orderToInts(order);
        this.xovers = xovers;
        this.seqmap = starts;
        this.length = len;
    }

    /** JS {@code cmp(x, y)} inside build — compares ranks[x], ranks[y] with a gap offset. When
     *  one side runs past the end, JS compares the raw offset indices ({@code rawcmp(y, x)}). */
    private static int cmpRanks(int x, int y, int gap, Object[] ranks, int len) {
        int c = rawcmp(ranks[x], ranks[y]);
        if (c != 0) {
            return c;
        }
        int xx = x + gap, yy = y + gap;
        if (xx < len && yy < len) {
            return rawcmp(ranks[xx], ranks[yy]);
        }
        return Integer.compare(yy, xx);
    }

    /** JS {@code rawcmp(a, b)} — numeric for Integers, lexicographic for Strings. */
    private static int rawcmp(Object a, Object b) {
        if (eq(a, b)) {
            return 0;
        }
        if (a instanceof Number && b instanceof Number) {
            return Integer.compare(((Number) a).intValue(), ((Number) b).intValue());
        }
        return String.valueOf(a).compareTo(String.valueOf(b));
    }

    private static int[] orderToInts(Integer[] order) {
        int[] out = new int[order.length];
        for (int i = 0; i < order.length; i++) {
            out[i] = order[i];
        }
        return out;
    }

    // ---- internals ------------------------------------------------------------------

    private Integer binsearch(List<Object> query, boolean isFirst) {
        int low = 0, high = data.length - 1;
        int result = -1;
        while (low <= high) {
            int mid = (low + high) >>> 1;
            if (isSubArray(mid, query)) {
                result = mid;
                if (isFirst) {
                    high = mid - 1;
                } else {
                    low = mid + 1;
                }
            } else if (lt(mid, query)) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return result == -1 ? null : result;
    }

    private boolean lt(int idx, List<Object> query) {
        int position = data[idx];
        for (int i = 0; i < query.size(); i++) {
            if (position + i >= seq.length) {
                return true;
            }
            Object c = seq[position + i];
            if (!eq(c, query.get(i))) {
                return rawcmp(c, query.get(i)) < 0;
            }
        }
        return false;
    }

    private boolean isSubArray(int index, List<Object> query) {
        int position = data[index];
        for (int i = 0; i < query.size(); i++) {
            if (position + i >= seq.length || !eq(seq[position + i], query.get(i))) {
                return false;
            }
        }
        return true;
    }

    private boolean arrayEquals(int index, List<Object> query) {
        int position = data[index];
        int len = seq.length - position;
        if (len != query.size()) {
            return false;
        }
        for (int i = 0; i < len; i++) {
            if (!eq(seq[position + i], query.get(i))) {
                return false;
            }
        }
        return true;
    }

    /** JS {@code arrayCompareSlices} over an Object[] (internal, used by build). JS reads
     *  out-of-range indices as {@code undefined}, so a slice running past the end compares
     *  unequal at the first such index. */
    static int arrayCompareSlices(Object[] arr, int aStart, int aEnd, int bStart, int bEnd) {
        int lenA = Math.min(arr.length, aEnd - aStart);
        int lenB = Math.min(arr.length, bEnd - bStart);
        if (lenA != lenB) {
            return Math.min(lenA, lenB);
        }
        int len = Math.min(lenA, lenB);
        for (int i = 0; i < len; i++) {
            if (!eq(get(arr, aStart + i), get(arr, bStart + i))) {
                return i;
            }
        }
        return -1;
    }

    /** JS {@code arrayCompareSlices(arr, ...)} over a List<String> (public/test). */
    public static int arrayCompareSlices(List<String> arr, int aStart, int aEnd, int bStart, int bEnd) {
        int lenA = Math.min(arr.size(), aEnd - aStart);
        int lenB = Math.min(arr.size(), bEnd - bStart);
        if (lenA != lenB) {
            return Math.min(lenA, lenB);
        }
        int len = Math.min(lenA, lenB);
        for (int i = 0; i < len; i++) {
            if (!java.util.Objects.equals(get(arr, aStart + i), get(arr, bStart + i))) {
                return i;
            }
        }
        return -1;
    }

    /** JS array access: {@code null} (undefined) for an out-of-range index. */
    private static Object get(Object[] arr, int i) {
        return (i >= 0 && i < arr.length) ? arr[i] : null;
    }

    private static String get(List<String> arr, int i) {
        return (i >= 0 && i < arr.size()) ? arr.get(i) : null;
    }

    /** JS {@code arrayCompare(a, b)} — index of first difference, or -1 if equal. */
    public static int arrayCompare(List<String> a, List<String> b) {
        if (a == null || b == null) {
            return -1;
        }
        int len = Math.min(a.size(), b.size());
        if (a.size() != b.size()) {
            return len;
        }
        for (int i = 0; i < len; i++) {
            if (!a.get(i).equals(b.get(i))) {
                return i;
            }
        }
        return -1;
    }

    /** JS {@code _encode(arg)} — tokens to indices (compressed) or unchanged (uncompressed). */
    private List<Object> encode(List<String> arg) {
        if (!compressed) {
            return new ArrayList<Object>(arg);
        }
        List<Object> out = new ArrayList<>(arg.size());
        for (String t : arg) {
            out.add(encoder.get(t));
        }
        return out;
    }

    private String decode(Object v) {
        return compressed ? decoder.get((Integer) v) : String.valueOf(v);
    }

    private List<String> decodeList(List<Object> indices) {
        List<String> out = new ArrayList<>(indices.size());
        for (Object v : indices) {
            out.add(decode(v));
        }
        return out;
    }

    private List<Object> seqSlice(int from, int to) {
        int start = Math.max(0, Math.min(from, seq.length));
        int end = Math.max(start, Math.min(to, seq.length));
        List<Object> out = new ArrayList<>(end - start);
        for (int i = start; i < end; i++) {
            out.add(seq[i]);
        }
        return out;
    }

    private Map<String, Double> createDist(List<String> arr, boolean normalise) {
        Map<String, Double> dist = new java.util.LinkedHashMap<>();
        for (String s : arr) {
            dist.merge(s, 1.0, Double::sum);
        }
        return normalise ? normaliseDist(dist) : dist;
    }

    private static Map<String, Double> normalize(Map<String, Double> dist) {
        double total = 0;
        for (double v : dist.values()) {
            total += v;
        }
        Map<String, Double> out = new java.util.LinkedHashMap<>();
        for (Map.Entry<String, Double> e : dist.entrySet()) {
            out.put(e.getKey(), e.getValue() / total);
        }
        return out;
    }

    private static List<Double> softmax(List<Double> logits, double temp) {
        if (temp == 0) {
            Map<String, Double> m = new java.util.LinkedHashMap<>();
            for (int i = 0; i < logits.size(); i++) {
                m.put(String.valueOf(i), logits.get(i));
            }
            Map<String, Double> norm = normalize(m);
            List<Double> out = new ArrayList<>();
            for (int i = 0; i < logits.size(); i++) {
                out.add(norm.get(String.valueOf(i)));
            }
            return out;
        }
        temp = Math.max(temp, 0.000001);
        List<Double> scaled = new ArrayList<>();
        double sum = 0;
        for (double v : logits) {
            double e = exp(v / temp);
            scaled.add(e);
            sum += e;
        }
        List<Double> out = new ArrayList<>();
        for (double v : scaled) {
            out.add(v / sum);
        }
        return out;
    }

    /**
     * Correctly-rounded {@code exp}, matching V8's {@code Math.exp}. Java's {@code Math.exp} is
     * accurate to 1 ulp but not always correctly rounded, which diverges from the JS ground truth
     * in the softmax path (e.g. {@code exp(1)}). This cold-path helper uses a BigDecimal series so
     * the result rounds to the same double as JS.
     */
    static double exp(double x) {
        if (x == 0) {
            return 1.0;
        }
        if (!Double.isFinite(x)) {
            return Math.exp(x);
        }
        if (x > 709.78) {
            return Double.POSITIVE_INFINITY;
        }
        if (x < -745) {
            return 0.0;
        }
        int k = (int) Math.rint(x * 1.4426950408889634);
        java.math.BigDecimal r = java.math.BigDecimal.valueOf(x)
            .subtract(LN2.multiply(java.math.BigDecimal.valueOf(k), EXP_MC), EXP_MC);
        java.math.BigDecimal sum = java.math.BigDecimal.ONE;
        java.math.BigDecimal term = java.math.BigDecimal.ONE;
        for (int n = 1; n < 80; n++) {
            term = term.multiply(r, EXP_MC).divide(java.math.BigDecimal.valueOf(n), EXP_MC);
            sum = sum.add(term, EXP_MC);
            if (term.abs().compareTo(java.math.BigDecimal.valueOf(1e-40)) < 0) {
                break;
            }
        }
        java.math.BigDecimal scale = (k >= 0)
            ? new java.math.BigDecimal(java.math.BigInteger.ONE.shiftLeft(k), EXP_MC)
            : java.math.BigDecimal.ONE.divide(
                new java.math.BigDecimal(java.math.BigInteger.ONE.shiftLeft(-k), EXP_MC), EXP_MC);
        return sum.multiply(scale, EXP_MC).doubleValue();
    }

    private static final java.math.MathContext EXP_MC =
        new java.math.MathContext(50, java.math.RoundingMode.HALF_EVEN);
    private static final java.math.BigDecimal LN2 = new java.math.BigDecimal(
        "0.69314718055994530941723212145817656807550013436025525412068000949339362196969471560586332699641868754200146749385822645537097307847831",
        EXP_MC);

    private static double random() {
        return rita.RiTa.randomizer.random();
    }

    private static boolean eq(Object a, Object b) {
        if (a == null || b == null) {
            return a == b;
        }
        if (a instanceof Number && b instanceof Number) {
            return ((Number) a).intValue() == ((Number) b).intValue();
        }
        return String.valueOf(a).equals(String.valueOf(b));
    }

    private static int asInt(Object o) {
        return o instanceof Number ? ((Number) o).intValue() : Integer.parseInt(o.toString());
    }

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

    private static String str(String s) {
        return "\"" + s.replace("\\", "\\\\").replace("\"", "\\\"") + "\"";
    }

    @Override
    public String toString() {
        return toString(Map.of());
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
        SuffixArray s = (SuffixArray) other;
        return length == s.length
            && xoverWindow == s.xoverWindow
            && compressed == s.compressed
            && java.util.Objects.equals(startToken, s.startToken)
            && java.util.Objects.equals(endToken, s.endToken)
            && java.util.Objects.equals(decoder, s.decoder)
            && java.util.Objects.equals(encoder, s.encoder)
            && java.util.Objects.equals(input, s.input)
            && java.util.Arrays.equals(seqmap, s.seqmap)
            && java.util.Arrays.equals(data, s.data)
            && java.util.Arrays.equals(xovers, s.xovers);
    }

    @Override
    public int hashCode() {
        return java.util.Objects.hash(length, xoverWindow, compressed, startToken, endToken,
            decoder, encoder, input, java.util.Arrays.hashCode(seqmap),
            java.util.Arrays.hashCode(data), java.util.Arrays.hashCode(xovers));
    }

    /** JS {@code toString(opts)} — a readable dump of the sorted suffixes. */
    public String toString(Map<String, Object> opts) {
        StringBuilder s = new StringBuilder("\n[\n");
        int tokensPer = opts == null ? 20 : (int) Util.numOpt(opts, "maxLength", 20);
        if (tokensPer < 1) {
            tokensPer = Integer.MAX_VALUE;
        }
        for (int i = 0; i < data.length; i++) {
            int idx = data[i];
            List<String> tokens = decodeList(seqSlice(idx, idx + tokensPer));
            boolean truncated = seq.length - idx > tokensPer;
            if (truncated) {
                tokens.add("...");
            }
            s.append("  ").append(i).append(": [").append(String.join(",", tokens)).append("],\n");
        }
        return s + "]\n";
    }
}
