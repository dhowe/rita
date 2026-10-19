package rita;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Lexicon — port of {@code js/src/lexicon.js}.
 *
 * <p>The data layer (dictionary load + phone/POS lookups) is implemented; the search/rhyme/
 * alliteration algorithms remain stubs until their dependencies (analyzer, tagger, conjugator,
 * inflector) are ported.
 */
public class Lexicon {

    /**
     * The lexicon data, keyed by word to {@code [phones, pos]} entries (the value is a
     * {@code List<Object>} of size 2). Mirrors the JS {@code lexicon.data} property: tests mutate
     * or swap it to exercise cache invalidation.
     */
    public Map<String, Object> data = loadData();

    /** Number of dictionary entries. Mirrors JS {@code size()}. */
    public int size() {
        return data.size();
    }

    public List<String> rhymesSync(String word, Map<String, Object> options) {
        Map<String, Object> opts = parseArgs(options);
        if (word == null || word.isEmpty() || word.length() < 2) {
            return new ArrayList<>();
        }
        String phone = lastStressedPhoneToEnd(word);
        List<String> words = _getWords();
        if (phone == null) {
            return new ArrayList<>();
        }
        if (truthy(opts.get("shuffle"))) {
            words = RiTa.randomizer.shuffle(words);
        }
        List<String> result = new ArrayList<>();
        int limit = (int) Util.numOpt(opts, "limit", 10);
        for (int i = 0; i < words.size(); i++) {
            String w = words.get(i);
            Object entry = this.data.get(w);
            if (w.equals(word) || !checkCriteria(w, entry, opts)) {
                continue;
            }
            if (opts.get("targetPos") != null) {
                w = matchPos(w, entry, opts, false);
                if (w == null) {
                    continue;
                }
                if (!w.equals(words.get(i))) {
                    entry = this.data.get(w);
                }
            }
            String phones = entry != null ? phonesOf(entry) : rawPhones(w);
            if (phones != null && phones.endsWith(phone)) {
                result.add(w);
            }
            if (result.size() == limit) {
                break;
            }
        }
        return result;
    }

    public List<String> searchSync(Object pattern, Map<String, Object> options) {
        List<String> words = _getWords();
        if (pattern == null && options == null) {
            return words;
        }
        ParseResult pr = parseRegex(pattern, options);
        Map<String, Object> opts = parseArgs(pr.opts);
        if (truthy(opts.get("shuffle"))) {
            words = RiTa.randomizer.shuffle(words);
        }
        List<String> result = new ArrayList<>();
        int limit = (int) Util.numOpt(opts, "limit", 10);
        for (int i = 0; i < words.size(); i++) {
            String w = words.get(i);
            Object entry = this.data.get(w);
            if (!checkCriteria(w, entry, opts)) {
                continue;
            }
            if (opts.get("targetPos") != null) {
                w = matchPos(w, entry, opts, truthy(opts.get("strictPos")));
                if (w == null) {
                    continue;
                }
                if (!w.equals(words.get(i))) {
                    entry = this.data.get(w);
                }
            }
            if (pr.regex == null || regexMatch(w, entry, pr.regex, (String) opts.get("type"))) {
                result.add(w);
                if (result.size() == limit) {
                    break;
                }
            }
        }
        return result;
    }

    public List<String> alliterationsSync(String theWord, Map<String, Object> options) {
        Map<String, Object> opts = parseArgs(options);
        if (theWord == null || theWord.isEmpty() || theWord.length() < 2) {
            return new ArrayList<>();
        }
        if (RiTa.isVowel(Util.charAt(theWord, 0))) {
            return new ArrayList<>();
        }
        String fss = firstStressedSyl(theWord);
        if (fss == null) {
            return new ArrayList<>();
        }
        String phone = firstPhone(fss);
        List<String> words = _getWords();
        if (phone == null) {
            return new ArrayList<>();
        }
        if (truthy(opts.get("shuffle"))) {
            words = RiTa.randomizer.shuffle(words);
        }
        List<String> result = new ArrayList<>();
        int limit = (int) Util.numOpt(opts, "limit", 10);
        for (int i = 0; i < words.size(); i++) {
            String w = words.get(i);
            if (w.equals(theWord) || !checkCriteria(w, data.get(w), opts)) {
                continue;
            }
            Object data2 = data.get(w);
            if (opts.get("targetPos") != null) {
                w = matchPos(w, data2, opts, false);
                if (w == null) {
                    continue;
                }
                if (!w.equals(words.get(i))) {
                    data2 = data.get(w);
                }
            }
            String c2 = firstPhone(firstStressedSyl(w));
            if (phone.equals(c2)) {
                result.add(w);
            }
            if (result.size() == limit) {
                break;
            }
        }
        return result;
    }

    public List<String> spellsLikeSync(String word, Map<String, Object> options) {
        if (word == null || word.isEmpty()) {
            return new ArrayList<>();
        }
        Map<String, Object> opts = new java.util.LinkedHashMap<>(options == null ? Map.of() : options);
        opts.put("type", "letter");
        return byTypeSync(word, opts);
    }

    public List<String> soundsLikeSync(String word, Map<String, Object> options) {
        if (word == null || word.isEmpty()) {
            return new ArrayList<>();
        }
        Map<String, Object> opts = options == null ? new java.util.LinkedHashMap<>() : new java.util.LinkedHashMap<>(options);
        if (truthy(opts.get("matchSpelling"))) {
            return bySoundAndLetterSync(word, opts);
        }
        opts.put("type", "sound");
        return byTypeSync(word, opts);
    }

    public String randomWord(Object pattern, Map<String, Object> options) {
        Map<String, Object> opts;
        if (pattern == null && options == null) {
            return (String) RiTa.random(_getWords());
        }
        if (!(pattern instanceof String) && pattern != null && options == null) {
            // single argument which is opts
            opts = new java.util.LinkedHashMap<>((Map<String, Object>) pattern);
            pattern = null;
        } else {
            opts = new java.util.LinkedHashMap<>(options == null ? Map.of() : options);
        }
        opts.put("limit", 1);
        opts.put("shuffle", true);
        opts.put("strictPos", true);
        opts.put("minLength", Util.numOpt(opts, "minLength", 4));

        List<String> result = searchSync(pattern, opts);
        if (result.isEmpty() && opts.containsKey("pos")) {
            opts.put("strictPos", false);
            result = searchSync(pattern, opts);
        }
        if (result.isEmpty()) {
            throw new RuntimeException("No words matching constraints: " + opts);
        }
        return result.get(0);
    }

    public boolean isRhyme(String word1, String word2) {
        if (word1 == null || word2 == null || word1.toUpperCase().equals(word2.toUpperCase())) {
            return false;
        }
        String p1r = rawPhones(word1);
        String p2r = rawPhones(word2);
        if (p1r != null && p1r.equals(p2r)) {
            return false;
        }
        String p1 = lastStressedVowelPhonemeToEnd(word1);
        String p2 = lastStressedVowelPhonemeToEnd(word2);
        return p1 != null && p2 != null && p1.equals(p2);
    }

    /** JS {@code rawPhones(word)} — no LTS suppression. */
    public String rawPhones(String word) {
        return rawPhones(word, false);
    }

    /**
     * JS {@code rawPhones(word, opts)} — returns the raw phone string from the dictionary, or
     * null when absent. When {@code noLts} is false and the word is missing, the LTS engine is
     * consulted (via the analyzer); that path is not yet wired.
     */
    public String rawPhones(String word, boolean noLts) {
        Object[] rdata = lookupRaw(word);
        if (rdata != null && rdata.length > 0) {
            return (String) rdata[0];
        }
        if (!noLts) {
            List<String> phones = RiTa.analyzer.computePhones(word);
            if (phones != null && !phones.isEmpty()) {
                return Util.syllablesFromPhones(phones);
            }
        }
        return null;
    }

    /** JS {@code hasWord(word)} — exact dictionary membership. */
    public boolean hasWord(String word) {
        return hasWord(word, Map.of());
    }

    /**
     * JS {@code hasWord(word, opts)}. The exact-match path is a dictionary lookup; otherwise the
     * derivation path checks plural forms and conjugations, exactly as in JS.
     */
    public boolean hasWord(String word, Map<String, Object> options) {
        if (word == null || word.isEmpty()) {
            return false;
        }
        String token = word.toLowerCase();
        boolean exists = data.containsKey(token);
        boolean noDerivations = truthy(options.get("noDerivations"));
        if (noDerivations || exists) {
            return exists;
        }

        // 1) Check if word might be a plural form of a noun in the lexicon, e.g. 'dogs' or 'oxen'
        String sing = RiTa.singularize(token);
        if (sing != null && data.containsKey(sing) && RiTa.tagger.allTags(sing).contains("nn")) {
            return true;
        }

        // 2) Check if word might be a conjugated form of a verb in the lexicon, e.g. 'changed'
        String vlemma = RiTa.conjugator.unconjugate(token, options);
        if (vlemma != null && data.containsKey(vlemma)
            && RiTa.tagger.allTags(vlemma).contains("vb")) {
            return true;
        }

        return false;
    }

    public boolean isAlliteration(String word1, String word2) {
        if (word1 == null || word2 == null || word1.isEmpty()) {
            return false;
        }
        String c1 = firstPhone(firstStressedSyl(word1));
        String c2 = firstPhone(firstStressedSyl(word2));
        return c1 != null && c2 != null && !RiTa.isVowel(c1.substring(0, 1)) && c1.equals(c2);
    }

    /** JS {@code _firstPhone(rawPhones)} — the first phone of a raw phone string. */
    String firstPhone(String rawPhones) {
        if (rawPhones != null && !rawPhones.isEmpty()) {
            return rawPhones.split(RiTa.PHONE_BOUNDARY)[0];
        }
        return null;
    }

    /** JS {@code _firstStressedSyl(word)} — the first stressed syllable of the raw phones. */
    String firstStressedSyl(String word) {
        String raw = rawPhones(word); // dict first, LTS fallback (matches JS)
        if (raw == null) {
            return null;
        }
        int idx = raw.indexOf(RiTa.STRESS);
        if (idx >= 0) {
            idx--;
            while (true) {
                if (idx < 0) { // single-stressed syllable
                    idx = 0;
                    break;
                }
                if (raw.charAt(idx) == ' ') {
                    break;
                }
                idx--;
            }
            String firstToEnd = idx == 0 ? raw : raw.substring(idx).trim();
            int sp = firstToEnd.indexOf(' ');
            return sp < 0 ? firstToEnd : firstToEnd.substring(0, sp);
        }
        return null;
    }

    /** JS {@code isMassNoun(w)} — mass nouns and the -ness/-ism heuristic. */
    public boolean isMassNoun(String w) {
        return w.endsWith("ness") || w.endsWith("ism") || RiTa.MASS_NOUNS_SET.contains(w);
    }

    /** The POS data string for a word (e.g. "nn nns"), or null. Mirrors JS {@code _posData}. */
    public String _posData(String word) {
        Object[] rdata = lookupRaw(word);
        if (rdata != null && rdata.length == 2) {
            return (String) rdata[1];
        }
        return null;
    }

    /** Splits a raw phone string into its phone list. Mirrors JS {@code _toPhoneArray}. */
    public List<String> _toPhoneArray(String raw) {
        List<String> out = new ArrayList<>();
        for (String p : raw.replaceAll("[01]", "").replaceAll(" ", "-").split("-")) {
            out.add(p);
        }
        return out;
    }

    /** JS {@code _posArr(word)} — the POS tags as a list, or null. */
    public List<String> _posArr(String word) {
        String pos = _posData(word);
        return pos == null ? null : List.of(pos.split(" "));
    }

    /** JS {@code _lookupRaw(word)} — the {@code [phones, pos]} entry, or null. */
    Object[] lookupRaw(String word) {
        if (word == null) {
            return null;
        }
        Object v = data.get(word.toLowerCase());
        if (v instanceof List) {
            List<?> list = (List<?>) v;
            return list.toArray();
        }
        return null;
    }

    /** JS {@code _getWords()} — the dictionary keys (cached by data identity). */
    public List<String> _getWords() {
        if (wordsCacheRef != data) {
            wordsCache = new ArrayList<>(data.keySet());
            wordsCacheRef = data;
        }
        return wordsCache;
    }

    private List<String> wordsCache;
    private Map<String, Object> wordsCacheRef;

    // ---- internals ------------------------------------------------------------------

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

    // ---- search / rhyme / alliteration helpers (port of js/src/lexicon.js) ----------------

    /** The phones string of a {@code [phones, pos]} entry, or null. */
    private static String phonesOf(Object data) {
        if (data instanceof List) {
            Object p = ((List<?>) data).get(0);
            return p == null ? null : p.toString();
        }
        return null;
    }

    /** The pos string of a {@code [phones, pos]} entry, or null. */
    private static String posOf(Object data) {
        if (data instanceof List) {
            Object p = ((List<?>) data).get(1);
            return p == null ? null : p.toString();
        }
        return null;
    }

    /** JS {@code _lastStressedPhoneToEnd(word)}. */
    String lastStressedPhoneToEnd(String word) {
        if (word == null || word.isEmpty()) {
            return null;
        }
        String raw = rawPhones(word);
        if (raw == null) {
            return null;
        }
        int idx = raw.lastIndexOf(RiTa.STRESS);
        if (idx >= 0) {
            idx--;
            String c = Util.charAt(raw, idx);
            while (!c.equals("-") && !c.equals(" ")) {
                idx--;
                if (idx < 0) {
                    return raw; // single-stressed syllable
                }
                c = Util.charAt(raw, idx);
            }
        }
        return idx + 1 >= 0 ? raw.substring(Math.max(0, idx + 1)) : raw;
    }

    /** JS {@code _lastStressedVowelPhonemeToEnd(word)}. */
    String lastStressedVowelPhonemeToEnd(String word) {
        String raw = lastStressedPhoneToEnd(word);
        if (raw == null) {
            return null;
        }
        String[] syllables = raw.split(" ", -1);
        String lastSyllable = syllables[syllables.length - 1].replaceAll("[^a-z-1 ]", "");
        int idx = -1;
        for (int i = 0; i < lastSyllable.length(); i++) {
            if (RiTa.VOWELS.indexOf(lastSyllable.charAt(i)) >= 0) {
                idx = i;
                break;
            }
        }
        return lastSyllable.substring(Math.max(0, idx));
    }

    /** JS {@code _checkCriteria(word, rdata, opts)}. */
    private boolean checkCriteria(String word, Object data, Map<String, Object> opts) {
        int maxLength = (int) Util.numOpt(opts, "maxLength", Integer.MAX_VALUE);
        int minLength = (int) Util.numOpt(opts, "minLength", 3);
        if (word.length() > maxLength) {
            return false;
        }
        if (word.length() < minLength) {
            return false;
        }
        double numSyllables = Util.numOpt(opts, "numSyllables", 0);
        if (numSyllables > 0) {
            String phones = phonesOf(data);
            if (phones == null) {
                return false;
            }
            int syls = phones.split(" ").length;
            if (numSyllables != syls) {
                return false;
            }
        }
        return true;
    }

    /** JS {@code _matchPos(word, rdata, opts, strict)} — the (possibly inflected) word, or null. */
    private String matchPos(String word, Object data, Map<String, Object> opts, boolean strict) {
        if (data == null) {
            return null;
        }
        String targetPos = (String) opts.get("targetPos");
        String[] posArr = posOf(data).split(" ");
        boolean contains = false;
        for (String p : posArr) {
            if (p.equals(targetPos)) {
                contains = true;
                break;
            }
        }
        if (!contains || (strict && !targetPos.equals(posArr[0]))) {
            return null;
        }
        String result = word;
        if (truthy(opts.get("pluralize"))) {
            if (word.endsWith("ness") || word.endsWith("ism")) {
                return null;
            }
            result = RiTa.pluralize(word);
            if (!RiTa.isNoun(result)) {
                return null;
            }
        } else if (truthy(opts.get("conjugate"))) {
            result = reconjugate(word, (String) opts.get("pos"));
        }
        if (!result.equals(word)) {
            double numSyllables = Util.numOpt(opts, "numSyllables", 0);
            if (numSyllables > 0) {
                String syls = RiTa.analyzer.analyzeWord(result, Map.of("silent", true)).syllables;
                int num = syls.split(RiTa.SYLLABLE_BOUNDARY).length;
                if (num != numSyllables) {
                    return null;
                }
            }
            int minLength = (int) Util.numOpt(opts, "minLength", 3);
            int maxLength = (int) Util.numOpt(opts, "maxLength", Integer.MAX_VALUE);
            if (result.length() < minLength || result.length() > maxLength) {
                return null;
            }
        }
        return result;
    }

    /** JS {@code _reconjugate(word, pos)}. */
    private String reconjugate(String word, String pos) {
        switch (pos) {
            case "vbd":
                return RiTa.conjugate(word, Map.of("number", RiTa.SINGULAR, "person", RiTa.FIRST, "tense", RiTa.PAST));
            case "vbg":
                return RiTa.presentPart(word);
            case "vbn":
                return RiTa.pastPart(word);
            case "vbp":
                return word;
            case "vbz":
                return RiTa.conjugate(word, Map.of("number", RiTa.SINGULAR, "person", RiTa.THIRD, "tense", RiTa.PRESENT));
            default:
                throw new RuntimeException("Unexpected pos: " + pos);
        }
    }

    /** JS {@code _byTypeSync(theWord, opts)} — min-edit-distance matching by sound or letter. */
    private List<String> byTypeSync(String theWord, Map<String, Object> options) {
        Map<String, Object> opts = parseArgs(options);
        String input = theWord.toLowerCase();
        boolean matchSound = "sound".equals(opts.get("type"));
        List<String> variations = List.of(input, input + "s", input + "es");
        Object phonesA = matchSound ? toPhoneArray(rawPhones(input)) : input;
        if (phonesA == null) {
            return new ArrayList<>();
        }
        int minDistance = (int) Util.numOpt(opts, "minDistance", 1);
        int limit = limitOf(opts);
        List<String> words = _getWords();
        if (truthy(opts.get("shuffle"))) {
            words = RiTa.randomizer.shuffle(words);
        }
        List<String> result = new ArrayList<>();
        int minVal = Integer.MAX_VALUE;
        for (int i = 0; i < words.size(); i++) {
            String w = words.get(i);
            Object entry = this.data.get(w);
            if (variations.contains(w)) {
                continue;
            }
            if (!checkCriteria(w, entry, opts)) {
                continue;
            }
            if (truthy(opts.get("targetPos"))) {
                w = matchPos(w, entry, opts, false);
                if (w == null) {
                    continue;
                }
                if (!w.equals(words.get(i))) {
                    entry = this.data.get(w);
                }
            }
            Object phonesB = w;
            if (matchSound) {
                String phones = entry != null ? phonesOf(entry) : rawPhones(w);
                if (phones == null) {
                    continue;
                }
                phonesB = phones.replace("1", "").replace(" ", "-").split("-");
            }
            int med = minEditDist(phonesA, phonesB);
            if (med >= minDistance && med < minVal) {
                minVal = med;
                result = new ArrayList<>();
                result.add(w);
            } else if (med == minVal && result.size() < limit) {
                result.add(w);
            }
        }
        return result.size() > limit ? new ArrayList<>(result.subList(0, limit)) : result;
    }

    /** JS {@code _bySoundAndLetterSync(word, opts)}. */
    private List<String> bySoundAndLetterSync(String word, Map<String, Object> options) {
        Map<String, Object> soundOpts = new java.util.LinkedHashMap<>(options);
        soundOpts.put("type", "sound");
        Map<String, Object> letterOpts = new java.util.LinkedHashMap<>(options);
        letterOpts.put("type", "letter");
        List<String> bySound = byTypeSync(word, soundOpts);
        List<String> byLetter = byTypeSync(word, letterOpts);
        if (bySound.isEmpty() || byLetter.isEmpty()) {
            return new ArrayList<>();
        }
        int limit = limitOf(options);
        List<String> inter = intersect(bySound, byLetter);
        return inter.size() > limit ? new ArrayList<>(inter.subList(0, limit)) : inter;
    }

    /** JS {@code _intersect(a1, a2)} — elements of a1 that appear in a2, in a1 order. */
    private static List<String> intersect(List<String> a1, List<String> a2) {
        List<String> out = new ArrayList<>();
        for (String e : a1) {
            if (a2.contains(e)) {
                out.add(e);
            }
        }
        return out;
    }

    /** JS {@code minEditDist(source, target)} — Levenshtein over chars (String) or phones (List). */
    static int minEditDist(Object source, Object target) {
        List<String> s = toCharList(source);
        List<String> t = toCharList(target);
        int sLen = s.size(), tLen = t.size();
        int[] prev = new int[tLen + 1];
        int[] curr = new int[tLen + 1];
        for (int j = 0; j <= tLen; j++) {
            prev[j] = j;
        }
        for (int i = 1; i <= sLen; i++) {
            curr[0] = i;
            String sI = s.get(i - 1);
            for (int j = 1; j <= tLen; j++) {
                int cost = sI.equals(t.get(j - 1)) ? 0 : 1;
                curr[j] = Math.min(Math.min(prev[j] + 1, curr[j - 1] + 1), prev[j - 1] + cost);
            }
            int[] tmp = prev;
            prev = curr;
            curr = tmp;
        }
        return prev[tLen];
    }

    private static List<String> toCharList(Object o) {
        List<String> out = new ArrayList<>();
        if (o instanceof String) {
            String s = (String) o;
            for (int i = 0; i < s.length(); i++) {
                out.add(String.valueOf(s.charAt(i)));
            }
        } else if (o instanceof String[]) {
            for (String e : (String[]) o) {
                out.add(e);
            }
        } else if (o instanceof List) {
            for (Object e : (List<?>) o) {
                out.add(String.valueOf(e));
            }
        }
        return out;
    }

    /** JS {@code _toPhoneArray(raw)} — the phone list of a raw phone string, or null. */
    private static List<String> toPhoneArray(String raw) {
        if (raw == null) {
            return null;
        }
        return List.of(raw.replaceAll("[01]", "").replaceAll(" ", "-").split("-"));
    }

    /** JS {@code _parseArgs(options)} — fills in defaults and derives pluralize/conjugate/targetPos. */
    private Map<String, Object> parseArgs(Map<String, Object> options) {
        Map<String, Object> opts = new java.util.LinkedHashMap<>(options == null ? Map.of() : options);
        double limit = Util.numOpt(opts, "limit", 10);
        if (limit < 1) {
            limit = Integer.MAX_VALUE;
        }
        opts.put("limit", limit);
        opts.put("minDistance", Util.numOpt(opts, "minDistance", 1));
        opts.put("numSyllables", Util.numOpt(opts, "numSyllables", 0));
        opts.put("maxLength", Util.numOpt(opts, "maxLength", Integer.MAX_VALUE));
        opts.put("minLength", Util.numOpt(opts, "minLength", 3));

        Object tposObj = opts.get("pos");
        String tpos = (tposObj instanceof String && !((String) tposObj).isEmpty()) ? (String) tposObj : null;
        if (tpos != null) {
            opts.put("pluralize", "nns".equals(tpos));
            opts.put("conjugate", tpos.charAt(0) == 'v' && tpos.length() > 2);
            if (tpos.charAt(0) == 'n') {
                tpos = "nn";
            } else if (tpos.charAt(0) == 'v') {
                tpos = "vb";
            } else if (tpos.equals("r")) {
                tpos = "rb";
            } else if (tpos.equals("a")) {
                tpos = "jj";
            }
        }
        opts.put("targetPos", tpos);
        return opts;
    }

    /** The resolved limit as an int, clamped to Integer.MAX_VALUE. */
    private static int limitOf(Map<String, Object> opts) {
        double d = Util.numOpt(opts, "limit", 10);
        if (d < 1 || d > Integer.MAX_VALUE) {
            return Integer.MAX_VALUE;
        }
        return (int) d;
    }

    /** JS {@code _parseRegex(regex, opts)} — resolves the pattern and options. */
    private ParseResult parseRegex(Object pattern, Map<String, Object> options) {
        Map<String, Object> opts = options;
        java.util.regex.Pattern regex = null;
        if (pattern instanceof String) {
            String s = (String) pattern;
            if (opts != null && "stresses".equals(opts.get("type"))) {
                s = expandStressRegex(s);
            }
            regex = java.util.regex.Pattern.compile(s);
        } else if (pattern instanceof Map || (pattern == null && opts != null)) {
            if (opts == null) {
                opts = (Map<String, Object>) pattern;
            }
            Object r = opts.get("regex");
            if (r instanceof String) {
                String s = (String) r;
                String type = (String) opts.get("type");
                if (type != null && type.matches("^stress(es)?$")) {
                    s = expandStressRegex(s);
                }
                regex = java.util.regex.Pattern.compile(s);
            }
        }
        return new ParseResult(regex, opts == null ? Map.of() : opts);
    }

    /** JS: insert '/' between adjacent 0/1 digits when the string is a bare stress pattern. */
    private static String expandStressRegex(String s) {
        if (!s.matches("^\\^?[01]+\\$?$")) {
            return s;
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            sb.append(c);
            if ((c == '0' || c == '1') && i + 1 < s.length() && (s.charAt(i + 1) == '0' || s.charAt(i + 1) == '1')) {
                sb.append("/");
            }
        }
        return sb.toString();
    }

    /** JS {@code _regexMatch(word, data, regex, type)}. */
    private boolean regexMatch(String word, Object data, java.util.regex.Pattern regex, String type) {
        if ("stresses".equals(type)) {
            String phones = data != null ? phonesOf(data) : rawPhones(word);
            String stresses = RiTa.analyzer.phonesToStress(phones);
            return stresses != null && regex.matcher(stresses).find();
        } else if ("phones".equals(type)) {
            String phones = data != null ? phonesOf(data) : rawPhones(word);
            if (phones == null) {
                return false;
            }
            phones = phones.replace("1", "").replace(" ", "-");
            return regex.matcher(phones).find();
        }
        return regex.matcher(word).find();
    }

    /** The resolved regex + options from {@link #parseRegex}. */
    private static final class ParseResult {
        final java.util.regex.Pattern regex;
        final Map<String, Object> opts;

        ParseResult(java.util.regex.Pattern regex, Map<String, Object> opts) {
            this.regex = regex;
            this.opts = opts;
        }
    }


    /** Loads the canonical dictionary from the jar resource {@code rita/rita_dict.json}. */
    private static Map<String, Object> loadData() {
        Map<String, Object> out = new LinkedHashMap<>();
        try (InputStream in = Lexicon.class.getResourceAsStream("/rita/rita_dict.json")) {
            if (in == null) {
                throw new RuntimeException("Missing dictionary resource: /rita/rita_dict.json");
            }
            try (Reader r = new InputStreamReader(in, StandardCharsets.UTF_8)) {
                Map<String, Object> raw = Json.parseObject(readAll(r));
                for (Map.Entry<String, Object> e : raw.entrySet()) {
                    List<?> entry = (List<?>) e.getValue();
                    List<Object> pair = new ArrayList<>(2);
                    pair.add(entry.get(0));
                    pair.add(entry.get(1));
                    out.put(e.getKey(), pair);
                }
            }
        } catch (Exception e) {
            throw new RuntimeException("Failed to load rita_dict.json", e);
        }
        return out;
    }

    private static String readAll(Reader r) throws java.io.IOException {
        StringBuilder sb = new StringBuilder(1 << 20);
        char[] buf = new char[8192];
        int n;
        while ((n = r.read(buf)) != -1) {
            sb.append(buf, 0, n);
        }
        return sb.toString();
    }
}
