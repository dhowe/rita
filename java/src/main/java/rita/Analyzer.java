package rita;

import java.util.List;
import java.util.Map;

/**
 * Phonetic analyzer — stub for {@code js/src/analyzer.js}. Methods throw until ported.
 */
public class Analyzer {

    public RiTa.Analysis analyze(String input, Map<String, Object> options) {
        throw RiTa.notPorted("analyzer.analyze");
    }

    public RiTa.Analysis analyze(String input) {
        throw RiTa.notPorted("analyzer.analyze");
    }

    public RiTa.Analysis analyzeWord(String word, Map<String, Object> options) {
        throw RiTa.notPorted("analyzer.analyzeWord");
    }

    public RiTa.Analysis analyzeWord(String word) {
        throw RiTa.notPorted("analyzer.analyzeWord");
    }

    /** Returns the phone list, or null when the input yields no phones (JS undefined). */
    public List<String> computePhones(String word, Map<String, Object> options) {
        throw RiTa.notPorted("analyzer.computePhones");
    }

    public List<String> computePhones(String word) {
        throw RiTa.notPorted("analyzer.computePhones");
    }

    /** Maps phones to a stress string; null input returns null (JS undefined). */
    public String phonesToStress(String phones) {
        throw RiTa.notPorted("analyzer.phonesToStress");
    }

    // ---- static IPA helpers (mirror Analyzer.syllablesToIpa etc. in js/src/analyzer.js) ----

    public static String syllablesToIpa(String syllables, String stresses) {
        throw RiTa.notPorted("Analyzer.syllablesToIpa");
    }

    public static String syllablesToIpa(String syllables, String stresses, boolean includeBoundaries) {
        throw RiTa.notPorted("Analyzer.syllablesToIpa");
    }

    public static String phonesToIpa(String phones) {
        throw RiTa.notPorted("Analyzer.phonesToIpa");
    }

    public static String arpabetToIpa(String arpabet) {
        throw RiTa.notPorted("Analyzer.arpabetToIpa");
    }
}
