package rita;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Seeded random generator (Mersenne Twister) — port of {@code js/src/randgen.js}.
 *
 * <p>Reproduces the JS bit-for-bit: the MT core ({@code seed}/{@code _rndi}/{@code _rndf}) is
 * identical across RiTa v3 and v4, so seeded sequences match the golden vectors in
 * {@code shared/randgen-fixtures.json}.
 */
public class RandGen {

    private final int N = 624;
    private final int M = 397;
    private final int MATRIX_A = 0x9908b0df;
    private final int UPPER_MASK = 0x80000000;
    private final int LOWER_MASK = 0x7fffffff;
    private final int[] mag01 = {0x0, MATRIX_A};

    private final int[] mt = new int[N];
    private int mti = N + 1;

    public RandGen() {
        seed((int) System.currentTimeMillis());
    }

    /** Seeds the generator, mirroring JS {@code seed(num)} with {@code num >>> 0}. */
    public void seed(int num) {
        mt[0] = num;
        for (mti = 1; mti < N; mti++) {
            long s = (mt[mti - 1] ^ (mt[mti - 1] >>> 30)) & 0xffffffffL;
            mt[mti] = (int) (1812433253L * s + mti);
        }
    }

    /** Returns a shuffled copy of the input (Fisher-Yates, drawing {@code random(len)} each step). */
    public <T> List<T> shuffle(List<T> array) {
        List<T> out = new ArrayList<>(array);
        int len = out.size();
        for (int i = len - 1; i >= 0; i--) {
            int p = (int) Math.floor(random(len));
            T t = out.get(i);
            out.set(i, out.get(p));
            out.set(p, t);
        }
        return out;
    }

    /** Random ordering of {@code [0, k)}. */
    public int[] randomOrdering(int k) {
        List<Integer> o = new ArrayList<>();
        for (int i = 0; i < k; i++) {
            o.add(i);
        }
        shuffleInPlace(o);
        int[] result = new int[k];
        for (int i = 0; i < k; i++) {
            result[i] = o.get(i);
        }
        return result;
    }

    /** Random ordering of the input list (returns a new list). */
    public <T> List<T> randomOrdering(List<T> array) {
        List<T> o = new ArrayList<>(array);
        shuffleInPlace(o);
        return o;
    }

    private <T> void shuffleInPlace(List<T> o) {
        for (int i = o.size(); i != 0;) {
            int j = (int) Math.floor(random() * i);
            i--;
            T x = o.get(i);
            o.set(i, o.get(j));
            o.set(j, x);
        }
    }

    /** Selects an index from a probability distribution. */
    public int pselect(double[] probs) {
        if (probs == null || probs.length == 0) {
            throw new RuntimeException("Array required");
        }
        return pselectIndex(probs);
    }

    /** JS {@code pselect()} with no args — throws ('Array required'). */
    public int pselect() {
        throw new RuntimeException("Array required");
    }

    /** Selects an index from a probability distribution (same algorithm as {@link #pselect}). */
    public int pselectIndex(double[] probs) {
        if (probs == null || probs.length == 0) {
            throw new RuntimeException("arg required");
        }
        double point = _rndf();
        double cutoff = 0;
        for (int i = 0; i < probs.length - 1; ++i) {
            cutoff += probs[i];
            if (point < cutoff) {
                return i;
            }
        }
        return probs.length - 1;
    }

    /** JS {@code pselect2(weights)} — returns the selected *value*. */
    public double pselect2(double[] weightsArray) {
        double sum = 0;
        for (double w : weightsArray) {
            sum += w;
        }
        double rand = _rndf() * sum;
        for (double w : weightsArray) {
            rand -= w;
            if (rand < 0) {
                return w;
            }
        }
        return weightsArray[weightsArray.length - 1];
    }

    /** JS {@code pselectObj(dist)} — returns the selected key. */
    public String pselectObj(Map<String, Double> dist) {
        if (dist == null) {
            throw new RuntimeException("arg required");
        }
        double point = _rndf();
        double cutoff = 0;
        String last = null;
        for (Map.Entry<String, Double> e : dist.entrySet()) {
            last = e.getKey();
            cutoff += e.getValue();
            if (point < cutoff) {
                return e.getKey();
            }
        }
        return last;
    }

    /** JS {@code pselectObj()} with no args — throws ('arg required'). */
    public String pselectObj() {
        throw new RuntimeException("arg required");
    }

    /** Normalised distribution (softmax if {@code temp} given). */
    public double[] ndist(double[] weights) {
        return ndist(weights, 0);
    }

    public double[] ndist(double[] weights, double temp) {
        double[] probs = new double[weights.length];
        double sum = 0;
        if (temp == 0) {
            for (int i = 0; i < weights.length; i++) {
                if (weights[i] < 0) {
                    throw new RuntimeException("Weights must be positive");
                }
                sum += weights[i];
                probs[i] = weights[i];
            }
        } else {
            if (temp < 0.01) {
                temp = 0.01;
            }
            for (int i = 0; i < weights.length; i++) {
                double pr = Math.exp(weights[i] / temp);
                sum += pr;
                probs[i] = pr;
            }
        }
        for (int i = 0; i < probs.length; i++) {
            probs[i] /= sum;
        }
        return probs;
    }

    /** JS {@code random()} — float in [0, 1). */
    public double random() {
        return _rndf();
    }

    /** JS {@code random(k)} — float in [0, k). */
    public double random(double k) {
        return _rndf() * k;
    }

    /** JS {@code random(j, k)} — float in [j, k). */
    public double random(double min, double max) {
        return _rndf() * (max - min) + min;
    }

    /** JS {@code random(arr)} — a random element of the list. */
    public <T> T random(List<T> array) {
        return array.get((int) Math.floor(_rndf() * array.size()));
    }

    /** JS {@code random(arr)} — a random element of the array. */
    public <T> T random(T[] array) {
        return array[(int) Math.floor(_rndf() * array.length)];
    }

    /** JS {@code randomBias(min, max, bias, influence)} — float biased toward {@code bias}. */
    public double randomBias(double min, double max, double bias, double influence) {
        double base = _rndf() * max + min;
        double mix = _rndf() * influence;
        return base * (1 - mix) + bias * mix;
    }

    // //////////////////////////////////////////////////////////////////////////////////

    private int _rndi() {
        int y, kk;
        if (mti >= N) {
            if (mti == N + 1) {
                seed(5489);
            }
            for (kk = 0; kk < N - M; kk++) {
                y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK);
                mt[kk] = mt[kk + M] ^ (y >>> 1) ^ mag01[y & 0x1];
            }
            for (; kk < N - 1; kk++) {
                y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK);
                mt[kk] = mt[kk + (M - N)] ^ (y >>> 1) ^ mag01[y & 0x1];
            }
            y = (mt[N - 1] & UPPER_MASK) | (mt[0] & LOWER_MASK);
            mt[N - 1] = mt[M - 1] ^ (y >>> 1) ^ mag01[y & 0x1];
            mti = 0;
        }
        y = mt[mti++];
        y ^= (y >>> 11);
        y ^= (y << 7) & 0x9d2c5680;
        y ^= (y << 15) & 0xefc60000;
        y ^= (y >>> 18);
        return y;
    }

    private double _rndf() {
        return (_rndi() & 0xffffffffL) * (1.0 / 4294967296.0);
    }
}
