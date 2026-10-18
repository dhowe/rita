package rita;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Shared helpers — port of {@code js/src/util.js}.
 *
 * <p>Models the JS module 1:1: the static helpers ({@code syllablesToPhones},
 * {@code syllablesFromPhones}, {@code hasOwn}, {@code isNum}, {@code numOpt}), the data tables
 * ({@code Numbers}, {@code Phones}), and the {@code RE} regular-expression wrapper.
 */
public class Util {

    private Util() {
    }

    /** JS {@code Object.prototype.hasOwnProperty} — own-property test. */
    public static boolean hasOwn(Map<String, ?> obj, String key) {
        return obj != null && obj.containsKey(key);
    }

    /** JS {@code isNum} — {@code !isNaN(parseFloat(n)) && isFinite(n)}. */
    public static boolean isNum(Object n) {
        if (n == null) {
            return false;
        }
        if (n instanceof Number) {
            return Double.isFinite(((Number) n).doubleValue());
        }
        if (n instanceof String) {
            String s = (String) n;
            // JS: parseFloat(s) must be non-NaN AND Number(s) must be finite. Number(s) coerces the
            // whole string, so "12abc" fails (parseFloat=12 but Number=NaN) while "123"/" 12 " pass.
            return !Double.isNaN(parseFloat(s)) && !Double.isNaN(jsNumber(s))
                && Double.isFinite(jsNumber(s));
        }
        return false;
    }

    /** JS {@code numOpt(opts, name, def)} — numeric option or the default. */
    public static double numOpt(Map<String, Object> opts, String name, double def) {
        Object v = (opts == null) ? null : opts.get(name);
        return isNum(v) ? toDouble(v) : def;
    }

    /** JS {@code numOpt(opts, name)} — default 0. */
    public static double numOpt(Map<String, Object> opts, String name) {
        return numOpt(opts, name, 0);
    }

    private static double toDouble(Object v) {
        if (v instanceof Number) {
            return ((Number) v).doubleValue();
        }
        return parseFloat((String) v);
    }

    /**
     * JS {@code parseFloat} semantics: parse the longest leading numeric prefix, else NaN
     * (e.g. {@code "12abc"} -> 12, {@code "abc"} -> NaN, {@code " 12 "} -> 12).
     */
    static double parseFloat(String s) {
        if (s == null) {
            return Double.NaN;
        }
        s = s.trim();
        if (s.isEmpty()) {
            return Double.NaN;
        }
        Matcher m = FLOAT_PREFIX.matcher(s);
        if (m.lookingAt()) {
            try {
                return Double.parseDouble(m.group());
            } catch (NumberFormatException e) {
                return Double.NaN;
            }
        }
        return Double.NaN;
    }

    private static final Pattern FLOAT_PREFIX =
        Pattern.compile("[+-]?(\\d+\\.?\\d*|\\.\\d+)([eE][+-]?\\d+)?");

    /**
     * JS {@code Number(s)} coercion: trims whitespace, maps the empty string to 0, and parses the
     * entire remaining string as a number (NaN if anything is left over). Unlike {@link #parseFloat},
     * trailing junk ({@code "12abc"}) yields NaN.
     */
    static double jsNumber(String s) {
        if (s == null) {
            return Double.NaN;
        }
        String t = s.trim();
        if (t.isEmpty()) {
            return 0;
        }
        if (t.equalsIgnoreCase("Infinity") || t.equalsIgnoreCase("+Infinity")) {
            return Double.POSITIVE_INFINITY;
        }
        if (t.equalsIgnoreCase("-Infinity")) {
            return Double.NEGATIVE_INFINITY;
        }
        Matcher m = FULL_NUMBER.matcher(t);
        if (m.matches()) {
            try {
                return Double.parseDouble(t);
            } catch (NumberFormatException e) {
                return Double.NaN;
            }
        }
        return Double.NaN;
    }

    private static final Pattern FULL_NUMBER =
        Pattern.compile("[+-]?((\\d+\\.?\\d*|\\.\\d+)([eE][+-]?\\d+)?|Infinity)");

    // ---- syllable <-> phone helpers -------------------------------------------------

    /**
     * A syllable in the FreeTTS form used by JS: {@code [stress, onset, nucleus, coda]}, where
     * {@code stress} is a 0-or-1 element list, {@code nucleus} a 1-element list, and onset/coda
     * lists of phonemes. Mirrors the JS array-of-arrays structure.
     */
    public static final class Syllable {
        public List<String> stress;
        public List<String> onset;
        public List<String> nucleus;
        public List<String> coda;

        public Syllable(List<String> stress, List<String> onset, List<String> nucleus, List<String> coda) {
            this.stress = stress;
            this.onset = onset;
            this.nucleus = nucleus;
            this.coda = coda;
        }
    }

    /** JS {@code syllablesToPhones} — a syllabification to a dash/space-joined phone string. */
    public static String syllablesToPhones(List<Syllable> syllables) {
        List<String> ret = new ArrayList<>();
        for (Syllable syl : syllables) {
            String stress = syl.stress.isEmpty() ? null : syl.stress.get(0);
            List<String> nucleus = syl.nucleus;

            // JS mutates nucleus[0] += stress in place; here we compute the stressed nucleus locally
            // so the caller's (possibly immutable) lists are never modified.
            List<String> stressedNucleus = new ArrayList<>(nucleus);
            if (stress != null && !stressedNucleus.isEmpty()) {
                stressedNucleus.set(0, stressedNucleus.get(0) + stress);
            }

            List<String> data = new ArrayList<>();
            data.addAll(syl.onset);
            data.addAll(stressedNucleus);
            data.addAll(syl.coda);
            ret.add(String.join("-", data));
        }
        return String.join(" ", ret);
    }

    /** JS {@code syllablesFromPhones(string)} — phone string (dash-delimited) to syllabified phones. */
    public static String syllablesFromPhones(String input) {
        if (input == null || input.isEmpty()) {
            return "";
        }
        return syllablesFromPhones(Arrays.asList(input.split("-")));
    }

    /** JS {@code syllablesFromPhones(array)} — adapted from FreeTTS. */
    public static String syllablesFromPhones(List<String> input) {
        if (input == null || input.isEmpty()) {
            return "";
        }

        List<String> internuclei = new ArrayList<>();
        List<Syllable> syllables = new ArrayList<>();

        for (String raw : input) {
            String phoneme = raw.trim();
            if (phoneme.isEmpty()) {
                continue;
            }

            String stress = null;
            String last = phoneme.substring(phoneme.length() - 1);
            if (isNum(last)) {
                stress = last;
                phoneme = phoneme.substring(0, phoneme.length() - 1);
            }

            if (Phones.vowels.contains(phoneme)) {

                // Split the consonants seen since the last nucleus into coda and onset,
                // choosing the largest valid onset.
                List<String> coda = new ArrayList<>();
                List<String> onset = new ArrayList<>(internuclei);
                for (int split = 0; split < internuclei.size() + 1; split++) {
                    coda = new ArrayList<>(internuclei.subList(0, split));
                    onset = new ArrayList<>(internuclei.subList(split, internuclei.size()));
                    boolean valid = Phones.onsets.contains(String.join(" ", onset));
                    if (valid || syllables.isEmpty() || onset.isEmpty()) {
                        break;
                    }
                }

                // Tack the coda onto the previous syllable's coda (can't if this is the first).
                if (!syllables.isEmpty()) {
                    syllables.get(syllables.size() - 1).coda.addAll(coda);
                }

                // Make a new syllable out of the onset and nucleus.
                syllables.add(new Syllable(
                    stress == null ? new ArrayList<>() : new ArrayList<>(List.of(stress)),
                    new ArrayList<>(onset),
                    new ArrayList<>(List.of(phoneme)),
                    new ArrayList<>()));

                internuclei = new ArrayList<>();
            } else if (!Phones.consonants.contains(phoneme) && !phoneme.equals(" ")) {
                throw new RuntimeException("Invalid phoneme: " + phoneme);
            } else { // a consonant
                internuclei.add(phoneme);
            }
        }

        // Trailing consonants (or a word with no nucleus at all).
        if (!internuclei.isEmpty()) {
            if (syllables.isEmpty()) {
                syllables.add(new Syllable(new ArrayList<>(), new ArrayList<>(internuclei),
                    new ArrayList<>(), new ArrayList<>()));
            } else {
                syllables.get(syllables.size() - 1).coda.addAll(internuclei);
            }
        }
        return syllablesToPhones(syllables);
    }

    // ---- data tables ----------------------------------------------------------------

    /** JS {@code Util.Numbers}. */
    public static final class Numbers {
        private Numbers() {
        }

        public static final Map<String, Integer> fromWords = new LinkedHashMap<>();
        public static final Map<String, String> toWords = new LinkedHashMap<>();

        static {
            String[] words = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
                "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty", "sixty",
                "seventy", "eighty", "ninety"};
            int[] vals = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                30, 40, 50, 60, 70, 80, 90};
            for (int i = 0; i < words.length; i++) {
                fromWords.put(words[i], vals[i]);
                toWords.put(String.valueOf(vals[i]), words[i]);
            }
        }
    }

    /** JS {@code Util.Phones}. */
    public static final class Phones {
        private Phones() {
        }

        public static final List<String> consonants = List.of(
            "b", "ch", "d", "dh", "f", "g", "hh", "jh", "k", "l", "m",
            "n", "ng", "p", "r", "s", "sh", "t", "th", "v", "w", "y", "z", "zh");

        public static final List<String> vowels = List.of(
            "aa", "ae", "ah", "ao", "aw", "ax", "ay", "eh", "er", "ey", "ih",
            "iy", "ow", "oy", "uh", "uw");

        public static final List<String> onsets = List.of(
            "p", "t", "k", "b", "d", "g", "f", "v", "th", "dh", "s", "z",
            "sh", "ch", "jh", "m", "n", "r", "l", "hh", "w", "y", "p r", "t r",
            "k r", "b r", "d r", "g r", "f r", "th r", "sh r", "p l", "k l", "b l",
            "g l", "f l", "s l", "t w", "k w", "d w", "s w", "s p", "s t", "s k",
            "s f", "s m", "s n", "g w", "sh w", "s p r", "s p l", "s t r", "s k r",
            "s k w", "s k l", "th w", "zh", "p y", "k y", "b y", "f y", "hh y",
            "v y", "th y", "m y", "s p y", "s k y", "g y", "hh w", "");
    }

    // ---- RE factory (JS: Util.RE = (a,b,c) => new RE(a,b,c)) -------------------------

    public static RE RE(String regex, int offset, String suffix) {
        return new RE(regex, offset, suffix);
    }

    // ---- legacy helpers kept from the stub ------------------------------------------

    public static boolean isString(Object o) {
        return o instanceof String;
    }

    public static boolean isLetter(char c) {
        return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= 0xC0 && c <= 0xFF);
    }
}
