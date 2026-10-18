package rita;

import java.util.List;
import java.util.Map;

/**
 * Seeded random generator (Mersenne Twister) — stub for {@code js/src/randgen.js}.
 * Methods throw until ported.
 */
public class RandGen {

    public void seed(int seed) {
        throw RiTa.notPorted("randomizer.seed");
    }

    public double random() {
        throw RiTa.notPorted("randomizer.random");
    }

    public double random(double n) {
        throw RiTa.notPorted("randomizer.random");
    }

    public double random(double min, double max) {
        throw RiTa.notPorted("randomizer.random");
    }

    public <T> T random(List<T> array) {
        throw RiTa.notPorted("randomizer.random");
    }

    public <T> T random(T[] array) {
        throw RiTa.notPorted("randomizer.random");
    }

    public int[] randomOrdering(int k) {
        throw RiTa.notPorted("randomizer.randomOrdering");
    }

    public <T> List<T> randomOrdering(List<T> array) {
        throw RiTa.notPorted("randomizer.randomOrdering");
    }

    public <T> List<T> shuffle(List<T> array) {
        throw RiTa.notPorted("randomizer.shuffle");
    }

    /** JS {@code pselect(probs)} — returns the selected index. */
    public int pselect(double[] probs) {
        throw RiTa.notPorted("randomizer.pselect");
    }

    public int pselectIndex(double[] probs) {
        throw RiTa.notPorted("randomizer.pselectIndex");
    }

    /** JS {@code pselect2(weights)} — returns the selected *value*. */
    public double pselect2(double[] weights) {
        throw RiTa.notPorted("randomizer.pselect2");
    }

    /** JS {@code pselectObj(dist)} — returns the selected key. */
    public String pselectObj(Map<String, Double> dist) {
        throw RiTa.notPorted("randomizer.pselectObj");
    }

    /** JS {@code ndist(weights, temp)} — normalised distribution (softmax if temp given). */
    public double[] ndist(double[] weights) {
        throw RiTa.notPorted("randomizer.ndist");
    }

    public double[] ndist(double[] weights, double temp) {
        throw RiTa.notPorted("randomizer.ndist");
    }

    public double randomBias(double min, double max, double bias, double influence) {
        throw RiTa.notPorted("randomizer.randomBias");
    }
}
