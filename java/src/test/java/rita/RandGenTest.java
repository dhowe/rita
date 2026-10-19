package rita;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

/**
 * Ported from <code>js/test/randgen-tests.js</code>.
 *
 * <p>Both suites replay the golden vectors in <code>shared/randgen-fixtures.json</code> (generated
 * by <code>scripts/gen-randgen-fixtures.js</code> from the JS reference), so the Mersenne Twister
 * and every method layered on it are asserted byte-identical across the two implementations.
 */
class RandGenTest {

    private static final double EPS = 0.0; // exact double equality (the whole point)

    @Test
    void shouldReproduceSeededSequences() {
        JsonObject f = Fixtures.read("randgen-fixtures");
        for (var element : f.getAsJsonArray("sequences")) {
            JsonObject s = element.getAsJsonObject();
            int seed = s.get("seed").getAsInt();
            JsonArray values = s.getAsJsonArray("values");
            RiTa.randomSeed(seed);
            for (int i = 0; i < values.size(); i++) {
                assertEquals(values.get(i).getAsDouble(), RiTa.random(), EPS,
                    "seed " + seed + " index " + i);
            }
        }
    }

    @Test
    void shouldBeReproducibleAcrossReseeds() {
        RiTa.randomSeed(42);
        double[] first = new double[10];
        for (int i = 0; i < 10; i++) {
            first[i] = RiTa.random();
        }
        RiTa.randomSeed(42);
        for (int i = 0; i < 10; i++) {
            assertEquals(first[i], RiTa.random(), EPS);
        }
    }

    @Test
    void shouldDifferAcrossSeeds() {
        RiTa.randomSeed(1);
        double[] a = new double[10];
        for (int i = 0; i < 10; i++) {
            a[i] = RiTa.random();
        }
        RiTa.randomSeed(2);
        boolean allEqual = true;
        for (int i = 0; i < 10; i++) {
            if (a[i] != RiTa.random()) {
                allEqual = false;
            }
        }
        assertTrue(!allEqual, "different seeds produced identical streams");
    }

    @Test
    void shouldReturnFloatsInRange() {
        RiTa.randomSeed(7);
        for (int i = 0; i < 1000; i++) {
            double v = RiTa.random();
            assertTrue(v >= 0 && v < 1, "out of range: " + v);
        }
    }

    @Test
    void shouldCallPselect() {
        assertThrows(RuntimeException.class, () -> RiTa.randomizer.pselect());
        RiTa.randomSeed(1);
        assertEquals(0, RiTa.randomizer.pselect(new double[] {1}));
        JsonObject f = Fixtures.read("randgen-fixtures").getAsJsonObject("pselect");
        assertEquals(ints(f.getAsJsonArray("expected")),
            replay(f.get("seed").getAsInt(), () -> RiTa.randomizer.pselect(doublesArr(f.getAsJsonArray("probs")))));
    }

    @Test
    void shouldCallPselectIndex() {
        assertThrows(RuntimeException.class, () -> RiTa.randomizer.pselectIndex(new double[0]));
        RiTa.randomSeed(1);
        assertEquals(0, RiTa.randomizer.pselectIndex(new double[] {1}));
        JsonObject f = Fixtures.read("randgen-fixtures").getAsJsonObject("pselectIndex");
        assertEquals(ints(f.getAsJsonArray("expected")),
            replay(f.get("seed").getAsInt(), () -> RiTa.randomizer.pselectIndex(doublesArr(f.getAsJsonArray("probs")))));
    }

    @Test
    void shouldCallPselect2() {
        JsonObject f = Fixtures.read("randgen-fixtures").getAsJsonObject("pselect2");
        assertEquals(doubles(f.getAsJsonArray("expected")),
            replayD(f.get("seed").getAsInt(), () -> RiTa.randomizer.pselect2(doublesArr(f.getAsJsonArray("weights")))));
    }

    @Test
    void shouldCallPselectObj() {
        assertThrows(RuntimeException.class, () -> RiTa.randomizer.pselectObj());
        JsonObject f = Fixtures.read("randgen-fixtures").getAsJsonObject("pselectObj");
        Map<String, Double> dist = new LinkedHashMap<>();
        f.getAsJsonObject("dist").entrySet().forEach(e -> dist.put(e.getKey(), e.getValue().getAsDouble()));
        List<String> got = new ArrayList<>();
        RiTa.randomSeed(f.get("seed").getAsInt());
        for (int i = 0; i < 5; i++) {
            got.add(RiTa.randomizer.pselectObj(dist));
        }
        List<String> expected = new ArrayList<>();
        f.getAsJsonArray("expected").forEach(e -> expected.add(e.getAsString()));
        assertEquals(expected, got);
    }

    @Test
    void shouldCallNdist() {
        assertThrows(RuntimeException.class, () -> RiTa.randomizer.ndist(new double[] {1, 2, 6, -2.5, 0}));
        JsonObject f = Fixtures.read("randgen-fixtures");
        assertArray(doublesArr(f.getAsJsonObject("ndist").getAsJsonArray("expected")),
            RiTa.randomizer.ndist(doublesArr(f.getAsJsonObject("ndist").getAsJsonArray("weights"))));
        // NOTE: Math.exp is not guaranteed bit-identical across JS engines and Java, so the
        // softmax (temp) path is asserted to a small epsilon rather than exactly.
        JsonObject t = f.getAsJsonObject("ndistTemp");
        assertArrayEps(doublesArr(t.getAsJsonArray("expected")),
            RiTa.randomizer.ndist(doublesArr(t.getAsJsonArray("weights")), t.get("temp").getAsDouble()));
        JsonObject t1 = f.getAsJsonObject("ndistTemp1");
        assertArrayEps(doublesArr(t1.getAsJsonArray("expected")),
            RiTa.randomizer.ndist(doublesArr(t1.getAsJsonArray("weights")), t1.get("temp").getAsDouble()));
        double[] d = RiTa.randomizer.ndist(new double[] {3, 7, 11});
        double sum = 0;
        for (double v : d) {
            sum += v;
        }
        assertTrue(Math.abs(sum - 1) < 1e-12);
    }

    @Test
    void shouldCallShuffle() {
        JsonObject f = Fixtures.read("randgen-fixtures").getAsJsonObject("shuffle");
        List<Integer> input = intsBoxed(f.getAsJsonArray("input"));
        RiTa.randomSeed(f.get("seed").getAsInt());
        List<Integer> got = RiTa.randomizer.shuffle(input);
        assertEquals(ints(f.getAsJsonArray("expected")), got);
        // is a permutation
        List<Integer> sorted = new ArrayList<>(got);
        java.util.Collections.sort(sorted);
        assertEquals(input, sorted);
    }

    @Test
    void shouldCallRandomOrdering() {
        assertEquals(0, RiTa.randomOrdering(1)[0]);
        assertEquals(List.of("a"), RiTa.randomOrdering(List.of("a")));
        JsonObject f = Fixtures.read("randgen-fixtures").getAsJsonObject("randomOrdering");
        RiTa.randomSeed(f.get("seed").getAsInt());
        int[] got = RiTa.randomOrdering(f.get("k").getAsInt());
        assertEquals(ints(f.getAsJsonArray("expected")).toString(), java.util.Arrays.toString(got));
        // JS also asserts randomOrdering('x') throws; not portable (Java has no string overload).
    }

    @Test
    void shouldCallRandomWithRanges() {
        JsonObject f = Fixtures.read("randgen-fixtures");
        JsonObject r1 = f.getAsJsonObject("random1");
        assertEquals(doubles(r1.getAsJsonArray("expected")),
            replayD(r1.get("seed").getAsInt(), () -> RiTa.random(r1.get("k").getAsInt())));
        JsonObject r2 = f.getAsJsonObject("random2");
        assertEquals(doubles(r2.getAsJsonArray("expected")),
            replayD(r2.get("seed").getAsInt(),
                () -> RiTa.random(r2.get("min").getAsInt(), r2.get("max").getAsInt())));
        JsonObject ra = f.getAsJsonObject("randomArray");
        RiTa.randomSeed(ra.get("seed").getAsInt());
        assertEquals(ra.get("expected").getAsInt(),
            RiTa.random(intsBoxed(ra.getAsJsonArray("array"))));
    }

    @Test
    void shouldCallRandomBias() {
        JsonObject b = Fixtures.read("randgen-fixtures").getAsJsonObject("randomBias");
        assertEquals(doubles(b.getAsJsonArray("expected")),
            replayD(b.get("seed").getAsInt(),
                () -> RiTa.randomizer.randomBias(b.get("min").getAsDouble(), b.get("max").getAsDouble(),
                    b.get("bias").getAsDouble(), b.get("influence").getAsDouble())));
    }

    @Test
    void shouldHonorRandomSeed() {
        RiTa.randomSeed(42);
        JsonArray expected = null;
        for (var e : Fixtures.read("randgen-fixtures").getAsJsonArray("sequences")) {
            if (e.getAsJsonObject().get("seed").getAsInt() == 42) {
                expected = e.getAsJsonObject().getAsJsonArray("values");
            }
        }
        for (int i = 0; i < 10; i++) {
            assertEquals(expected.get(i).getAsDouble(), RiTa.random(), EPS);
        }
    }

    @Test
    void shouldCallRandi() {
        RiTa.randomSeed(42);
        assertEquals(3, RiTa.randi(10)); // floor(0.3745... * 10)
        assertEquals(12, RiTa.randi(5, 15)); // floor(0.7965... * 10 + 5)
        assertNotEquals(0, RiTa.randi(1000));
    }

    // ---- helpers --------------------------------------------------------------------

    private static void assertArray(double[] expected, double[] actual) {
        assertArrayEquals(expected, actual, EPS);
    }

    private static void assertArrayEps(double[] expected, double[] actual) {
        assertArrayEquals(expected, actual, 1e-15);
    }

    private static List<Integer> ints(JsonArray array) {
        List<Integer> out = new ArrayList<>();
        for (var e : array) {
            out.add(e.getAsInt());
        }
        return out;
    }

    private static List<Integer> intsBoxed(JsonArray array) {
        return ints(array);
    }

    private static List<Double> doubles(JsonArray array) {
        List<Double> out = new ArrayList<>();
        for (var e : array) {
            out.add(e.getAsDouble());
        }
        return out;
    }

    private static double[] doublesArr(JsonArray array) {
        double[] out = new double[array.size()];
        for (int i = 0; i < out.length; i++) {
            out[i] = array.get(i).getAsDouble();
        }
        return out;
    }

    private static List<Integer> replay(int seed, java.util.function.IntSupplier fn) {
        RiTa.randomSeed(seed);
        List<Integer> out = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            out.add(fn.getAsInt());
        }
        return out;
    }

    private static List<Double> replayD(int seed, java.util.function.DoubleSupplier fn) {
        RiTa.randomSeed(seed);
        List<Double> out = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            out.add(fn.getAsDouble());
        }
        return out;
    }
}
