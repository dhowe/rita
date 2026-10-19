package rita;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Phonetic analyzer — stub for {@code js/src/analyzer.js}. Methods throw until ported.
 */
public class Analyzer {

    private Map<String, RiTa.Analysis> cache = new java.util.HashMap<>();
    private Map<String, Object> cacheRef = null; // tracks lexicon.data identity for invalidation
    private LetterToSound lts = null;

    public RiTa.Analysis analyze(String input, Map<String, Object> options) {
        String[] words = RiTa.tokenize(input);
        String[] tags = RiTa.pos(input, options); // tags are not cached

        RiTa.Analysis features = new RiTa.Analysis();
        StringBuilder phones = new StringBuilder();
        StringBuilder stresses = new StringBuilder();
        StringBuilder syllables = new StringBuilder();
        features.pos = String.join(" ", tags);
        features.tokens = String.join(" ", words);

        for (String word : words) {
            RiTa.Analysis r = analyzeWord(word, options);
            phones.append(" ").append(r.phones);
            stresses.append(" ").append(r.stresses);
            syllables.append(" ").append(r.syllables);
        }
        features.phones = phones.toString().trim();
        features.stresses = stresses.toString().trim();
        features.syllables = syllables.toString().trim();
        return features;
    }

    public RiTa.Analysis analyze(String input) {
        return analyze(input, Map.of());
    }

    /** JS {@code computePhones(word, opts)} — the LTS phone list, or null. */
    public List<String> computePhones(String word, Map<String, Object> options) {
        if (lts == null) {
            lts = new LetterToSound();
        }
        return lts.buildPhones(word, options);
    }

    public List<String> computePhones(String word) {
        return computePhones(word, Map.of());
    }

    /** JS {@code phonesToStress(phones)} — a slash-delimited stress string, or null. */
    public String phonesToStress(String phones) {
        if (phones == null || phones.isEmpty()) {
            return null;
        }
        String[] syls = phones.split(" ", -1);
        StringBuilder stress = new StringBuilder();
        for (int j = 0; j < syls.length; j++) {
            if (syls[j].isEmpty()) {
                continue;
            }
            stress.append(syls[j].contains("1") ? "1" : "0");
            if (j < syls.length - 1) {
                stress.append("/");
            }
        }
        return stress.toString();
    }

    public RiTa.Analysis analyzeWord(String word, Map<String, Object> options) {
        // invalidate the cache if the lexicon data was swapped out
        Map<String, Object> lexData = RiTa.lexicon.data;
        if (cacheRef != lexData) {
            cache = new java.util.HashMap<>();
            cacheRef = lexData;
        }

        RiTa.Analysis result = RiTa.CACHING ? cache.get(word) : null;
        if (result == null) {
            String phones = word, syllables = word, stresses = word;

            Object rawPhones = RiTa.lexicon.rawPhones(word, true);
            if (rawPhones == null) {
                rawPhones = computeRawPhones(word, options);
            }

            if (rawPhones != null) {
                if (rawPhones instanceof String) {
                    String raw = (String) rawPhones;
                    String sp = raw.replace("1", "").replace(" ", "-") + " ";
                    phones = "dh ".equals(sp) ? "dh-ah " : sp;
                    String ss = raw.replace(" ", "/").replace("1", "") + " ";
                    syllables = "dh ".equals(ss) ? "dh-ah " : ss;
                    stresses = phonesToStress(raw);
                } else {
                    // hyphenated (#HWF): a list of raw phone strings
                    List<?> parts = (List<?>) rawPhones;
                    StringBuilder ps = new StringBuilder();
                    StringBuilder syls = new StringBuilder();
                    StringBuilder strs = new StringBuilder();
                    for (int i = 0; i < parts.size(); i++) {
                        String p = (String) parts.get(i);
                        String sp = p.replace("1", "").replace(" ", "-");
                        ps.append("dh ".equals(sp) ? "dh-ah " : sp);
                        String ss = p.replace(" ", "/").replace("1", "");
                        syls.append("dh ".equals(ss) ? "dh-ah " : ss);
                        strs.append(phonesToStress(p));
                        if (i < parts.size() - 1) {
                            ps.append("-");
                            syls.append("/");
                            strs.append("-");
                        }
                    }
                    phones = ps.toString();
                    syllables = syls.toString();
                    stresses = strs.toString();
                }
            }

            result = new RiTa.Analysis();
            result.phones = phones.trim();
            result.stresses = stresses.trim();
            result.syllables = syllables.trim();

            if (RiTa.CACHING) {
                cache.put(word, result);
            }
        }
        return result;
    }

    public RiTa.Analysis analyzeWord(String word) {
        return analyzeWord(word, Map.of());
    }

    /** JS {@code _computeRawPhones(word, lex, opts)}. Returns a String, a List<String>, or null. */
    private Object computeRawPhones(String word, Map<String, Object> opts) {
        return word.contains("-") ? computePhonesHyph(word, opts) : computePhonesWord(word, opts, false);
    }

    /** JS {@code _computePhonesHyph(word, lex, opts)} — a list of raw phone strings per part. */
    private List<String> computePhonesHyph(String word, Map<String, Object> opts) {
        List<String> rawPhones = new java.util.ArrayList<>();
        for (String part : word.split("-", -1)) {
            String p = computePhonesWord(part, opts, true);
            if (p != null && !p.isEmpty()) {
                rawPhones.add(p);
            }
        }
        return rawPhones;
    }

    /** JS {@code _computePhonesWord(word, lex, opts, isPart)}. */
    private String computePhonesWord(String word, Map<String, Object> opts, boolean isPart) {
        String rawPhones = null;
        if (isPart) {
            rawPhones = RiTa.lexicon.rawPhones(word, true);
        }
        // if it's a simple plural ending in 's' and the singular is in the lexicon, add '-z'
        if (rawPhones == null && word.endsWith("s")) {
            String sing = RiTa.singularize(word);
            rawPhones = RiTa.lexicon.rawPhones(sing, true);
            if (rawPhones != null) {
                rawPhones += "-z";
            }
        }

        // if no phones yet, try the lts engine
        if (rawPhones == null) {
            List<String> ltsPhones = computePhones(word, opts);
            if (ltsPhones != null && !ltsPhones.isEmpty()) {
                rawPhones = Util.syllablesFromPhones(ltsPhones);
            }
        }
        return rawPhones;
    }

    // ---- static IPA helpers (mirror Analyzer.syllablesToIpa etc. in js/src/analyzer.js) ----

    /** Arpabet (lowercase, no stress digits) to IPA, per https://en.wikipedia.org/wiki/ARPABET. */
    static final Map<String, String> ARPABET_TO_IPA = new java.util.LinkedHashMap<>();

    static {
        // Vowels
        ARPABET_TO_IPA.put("aa", "ɑ");
        ARPABET_TO_IPA.put("ae", "æ");
        ARPABET_TO_IPA.put("ah", "ʌ");
        ARPABET_TO_IPA.put("ao", "ɔ");
        ARPABET_TO_IPA.put("aw", "aʊ");
        ARPABET_TO_IPA.put("ax", "ə");
        ARPABET_TO_IPA.put("ay", "aɪ");
        ARPABET_TO_IPA.put("eh", "ɛ");
        ARPABET_TO_IPA.put("er", "ɜr");
        ARPABET_TO_IPA.put("ey", "eɪ");
        ARPABET_TO_IPA.put("ih", "ɪ");
        ARPABET_TO_IPA.put("ix", "ɨ");
        ARPABET_TO_IPA.put("iy", "i");
        ARPABET_TO_IPA.put("ow", "oʊ");
        ARPABET_TO_IPA.put("oy", "ɔɪ");
        ARPABET_TO_IPA.put("uh", "ʊ");
        ARPABET_TO_IPA.put("uw", "u");
        // Consonants
        ARPABET_TO_IPA.put("b", "b");
        ARPABET_TO_IPA.put("ch", "tʃ");
        ARPABET_TO_IPA.put("d", "d");
        ARPABET_TO_IPA.put("dh", "ð");
        ARPABET_TO_IPA.put("dx", "ɾ");
        ARPABET_TO_IPA.put("el", "l̩");
        ARPABET_TO_IPA.put("em", "m̩");
        ARPABET_TO_IPA.put("en", "n̩");
        ARPABET_TO_IPA.put("f", "f");
        ARPABET_TO_IPA.put("g", "ɡ");
        ARPABET_TO_IPA.put("hh", "h");
        ARPABET_TO_IPA.put("jh", "dʒ");
        ARPABET_TO_IPA.put("k", "k");
        ARPABET_TO_IPA.put("l", "l");
        ARPABET_TO_IPA.put("m", "m");
        ARPABET_TO_IPA.put("n", "n");
        ARPABET_TO_IPA.put("ng", "ŋ");
        ARPABET_TO_IPA.put("p", "p");
        ARPABET_TO_IPA.put("q", "ʔ");
        ARPABET_TO_IPA.put("r", "ɹ");
        ARPABET_TO_IPA.put("s", "s");
        ARPABET_TO_IPA.put("sh", "ʃ");
        ARPABET_TO_IPA.put("t", "t");
        ARPABET_TO_IPA.put("th", "θ");
        ARPABET_TO_IPA.put("v", "v");
        ARPABET_TO_IPA.put("w", "w");
        ARPABET_TO_IPA.put("wh", "ʍ");
        ARPABET_TO_IPA.put("y", "j");
        ARPABET_TO_IPA.put("z", "z");
        ARPABET_TO_IPA.put("zh", "ʒ");
    }

    public static String syllablesToIpa(String syllables, String stresses) {
        return syllablesToIpa(syllables, stresses, false);
    }

    /** JS {@code Analyzer.syllablesToIpa(syllables, stresses, keepBoundaries)}. */
    public static String syllablesToIpa(String syllables, String stresses, boolean keepBoundaries) {
        String[] sylWords = syllables.split(" ", -1);
        String[] strWords = stresses.split(" ", -1);
        List<String> ipaWords = new ArrayList<>();
        int strIdx = 0;
        for (String word : sylWords) {
            // Skip punctuation tokens (single non-alphanumeric characters like ',')
            if (word.length() == 1 && !isLowerAlphaSlashDash(word.charAt(0))) {
                strIdx++;
                continue;
            }
            String[] syls = word.split("/", -1);
            String[] strs = (strIdx < strWords.length ? strWords[strIdx] : "0").split("/", -1);
            strIdx++;
            boolean isMonosyllable = syls.length == 1;
            List<String> ipaSyls = new ArrayList<>();
            for (int si = 0; si < syls.length; si++) {
                boolean stressed = si < strs.length && "1".equals(strs[si]);
                StringBuilder phones = new StringBuilder();
                for (String p : syls[si].split("-", -1)) {
                    if ("ah".equals(p)) {
                        phones.append(stressed ? "ʌ" : "ə");
                        continue;
                    }
                    if ("er".equals(p)) {
                        phones.append(stressed ? "ɜr" : "ər");
                        continue;
                    }
                    String ipa = ARPABET_TO_IPA.getOrDefault(p, p);
                    if (stressed && (p.equals("aa") || p.equals("iy") || p.equals("ao") || p.equals("uw"))) {
                        phones.append(ipa).append("ː");
                    } else {
                        phones.append(ipa);
                    }
                }
                ipaSyls.add(stressed && !isMonosyllable ? "ˈ" + phones : phones.toString());
            }
            ipaWords.add(keepBoundaries ? String.join("/", ipaSyls) : String.join("", ipaSyls));
        }
        return String.join(" ", ipaWords);
    }

    /** JS {@code Analyzer.phonesToIpa(phones)}. */
    public static String phonesToIpa(String phones) {
        String[] words = phones.split(" ", -1);
        List<String> out = new ArrayList<>();
        for (String word : words) {
            StringBuilder sb = new StringBuilder();
            for (String p : word.split("-", -1)) {
                sb.append(ARPABET_TO_IPA.getOrDefault(p, p));
            }
            out.add(sb.toString());
        }
        return String.join(" ", out);
    }

    public static String arpabetToIpa(String arpabet) {
        return ARPABET_TO_IPA.getOrDefault(arpabet, arpabet);
    }

    private static boolean isLowerAlphaSlashDash(char c) {
        return (c >= 'a' && c <= 'z') || c == '/' || c == '-';
    }
}
