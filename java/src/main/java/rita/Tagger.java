package rita;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Pattern;

/**
 * Part-of-speech tagger — port of {@code js/src/tagger.js}.
 */
public class Tagger {

    static final List<String> ADJS = List.of("jj", "jjr", "jjs");
    static final List<String> ADVS = List.of("rb", "rbr", "rbs", "rp");
    static final List<String> NOUNS = List.of("nn", "nns", "nnp", "nnps");
    static final List<String> VERBS = List.of("vb", "vbd", "vbg", "vbn", "vbp", "vbz");
    static final List<String> EX_BE = List.of("is", "are", "was", "were", "isn't", "aren't", "wasn't", "weren't");

    static final Map<String, String> HYPHENATEDS = new LinkedHashMap<>();
    static {
        HYPHENATEDS.put("well-being", "nn");
        HYPHENATEDS.put("knee-length", "jj");
        HYPHENATEDS.put("king-size", "jj");
        HYPHENATEDS.put("ho-hum", "uh");
        HYPHENATEDS.put("roly-poly", "jj");
        HYPHENATEDS.put("nitty-gritty", "nn");
        HYPHENATEDS.put("topsy-turvy", "jj");
    }

    static final List<String> VERB_PREFIX = List.of(
        "de", "over", "re", "dis", "un", "mis", "out", "pre", "post", "co", "fore", "inter", "sub", "trans", "under");
    static final List<String> NOUN_PREFIX = List.of(
        "anti", "auto", "de", "dis", "un", "non", "co", "over", "under", "up", "down", "hyper", "mono", "bi", "uni",
        "di", "semi", "omni", "mega", "mini", "macro", "micro", "counter", "ex", "mal", "neo", "out", "poly",
        "pseudo", "super", "sub", "sur", "tele", "tri", "ultra", "vice");
    static final List<String> ARTICLES = List.of("the", "a", "an", "some");

    private static final String HYPH = "__HYPH__";

    // Precompiled context-transformation regexes.
    private static final Pattern NOT_END_S_S = Pattern.compile("^.*[^s]s$");
    private static final Pattern NN_PRP = Pattern.compile("^(nn|prp)$");
    private static final Pattern VBZ_ONLY = Pattern.compile("^(vbz)$");
    private static final Pattern NN_PRP_NNP = Pattern.compile("^(nn|prp|nnp)$");
    private static final Pattern CAP = Pattern.compile("^[A-Z]");
    private static final Pattern NNS_NNPS_PRP = Pattern.compile("^(nns|nnps|prp)$");
    private static final Pattern VB_DGN = Pattern.compile("^vb[dgn]");
    private static final Pattern JJ_RS = Pattern.compile("^jj[rs]?");
    private static final Pattern VB_GDP = Pattern.compile("^(vb[gdp])");

    // ---- API ------------------------------------------------------------------------

    public boolean isVerb(String word, Map<String, Object> opts) {
        Conjugator conj = RiTa.conjugator;
        if (isNoLexIrregularVerb(word)) {
            return true;
        }
        if (conj.IRREG_VERBS_LEX_VB.containsKey(word)) {
            return true;
        }
        if (conj.IRREG_VERBS_NOLEX.containsKey(word)) {
            return true;
        }
        List<String> pos = allTags(word, opts);
        return anyIn(pos, VERBS);
    }

    public boolean isVerb(String word) {
        return isVerb(word, Map.of());
    }

    public boolean isNoun(String word) {
        List<String> pos = allTags(word, Map.of("noGuessing", true));
        return anyIn(pos, NOUNS);
    }

    public boolean isAdverb(String word) {
        return anyIn(allTags(word), ADVS);
    }

    public boolean isAdjective(String word) {
        return anyIn(allTags(word), ADJS);
    }

    public boolean hasTag(List<String> choices, String tag) {
        if (choices == null) {
            return false;
        }
        return String.join(",", choices).indexOf(tag) > -1;
    }

    /** JS {@code hasTag(nonArray, tag)} — a non-array first argument is never tagged. */
    public boolean hasTag(String choices, String tag) {
        return false;
    }

    /** JS {@code hasTag()} — undefined choices are not tagged. */
    public boolean hasTag() {
        return false;
    }

    public String inlineTags(String[] words, String[] tags, String delimiter) {
        if (words == null || words.length == 0) {
            return "";
        }
        if (tags == null || words.length != tags.length) {
            throw new RuntimeException("Tagger: invalid state: words(" + (words == null ? 0 : words.length)
                + ")=" + Arrays.toString(words) + " tags(" + (tags == null ? "undefined" : tags.length) + ")="
                + Arrays.toString(tags));
        }
        delimiter = (delimiter == null || delimiter.isEmpty()) ? "/" : delimiter;
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < words.length; i++) {
            sb.append(words[i]);
            if (!RiTa.isPunct(words[i])) {
                sb.append(delimiter).append(tags[i]);
            }
            sb.append(' ');
        }
        return sb.toString().trim();
    }

    public String inlineTags(String[] words, String[] tags) {
        return inlineTags(words, tags, null);
    }

    public String inlineTags(String[] words) {
        return inlineTags(words, null, null);
    }

    /** JS {@code inlineTags()} — undefined words yield the empty string. */
    public String inlineTags() {
        return "";
    }

    public List<String> allTags(String word, Map<String, Object> options) {
        List<String> tags = new ArrayList<>();
        boolean noGuessing = truthy(options.get("noGuessing"));
        boolean noDerivations = truthy(options.get("noDerivations"));
        boolean noGuessingOnHyphenated = truthy(options.get("noGuessingOnHyphenated"));
        boolean simple = truthy(options.get("simple"));

        if (word != null && !word.isEmpty()) {
            List<String> posData = RiTa.lexicon._posArr(word);
            if (posData != null && !posData.isEmpty()) {
                tags = new ArrayList<>(posData);
            } else if (word.contains("-") && noGuessingOnHyphenated) {
                tags = new ArrayList<>();
            } else if (!noDerivations) {
                tags = derivePosData(word, noGuessing);
            }
        }

        if (simple) {
            tags = simplify(tags);
        }
        return tags;
    }

    public List<String> allTags(String word, boolean simple) {
        return allTags(word, Map.of("simple", simple));
    }

    public List<String> allTags(String word) {
        return allTags(word, Map.of());
    }

    /** JS {@code allTags(array)} — a non-string input yields no tags. */
    public List<String> allTags(String[] words) {
        return new ArrayList<>();
    }

    public Object tag(String word, Map<String, Object> options) {
        return tagCore(word, options);
    }

    public String[] tag(String word) {
        return (String[]) tagCore(word, Map.of());
    }

    public Object tag(String[] words, Map<String, Object> options) {
        return tagCore(words, options);
    }

    public String[] tag(String[] words) {
        return (String[]) tagCore(words, Map.of());
    }

    /** JS {@code tag()} — undefined input yields an empty tag array. */
    public String[] tag() {
        return new String[0];
    }

    // ---- core -----------------------------------------------------------------------

    private Object tagCore(Object input, Map<String, Object> opts) {
        boolean inline = truthy(opts.get("inline"));
        boolean simple = truthy(opts.get("simple"));

        String[] words;
        if (input == null) {
            return inline ? "" : new String[0];
        }
        if (input instanceof String) {
            String s = (String) input;
            if (s.trim().isEmpty()) {
                return inline ? "" : new String[0];
            }
            words = RiTa.tokenize(s);
        } else {
            words = (String[]) input;
        }
        if (words.length == 0) {
            return inline ? "" : new String[0];
        }

        String[] result = new String[words.length];
        @SuppressWarnings("unchecked")
        List<String>[] choices = new List[words.length];

        for (int i = 0; i < words.length; i++) {
            String word = words[i];
            if (word == null || word.isEmpty()) {
                continue;
            }
            if (RiTa.isPunct(word)) {
                result[i] = word;
            } else if (word.length() == 1) {
                result[i] = handleSingleLetter(word);
            } else {
                List<String> opts2 = allTags(word, Map.of("noGuessingOnHyphenated", true));
                choices[i] = opts2;
                result[i] = opts2.isEmpty() ? HYPH : opts2.get(0);
            }
        }

        String[] tags = applyContext(words, result, choices);

        if (simple) {
            for (int i = 0; i < tags.length; i++) {
                tags[i] = simpleTag(tags[i]);
            }
        }

        return inline ? inlineTags(words, tags, null) : tags;
    }

    private String[] applyContext(String[] words, String[] result, List<String>[] choices) {
        for (int i = 0; i < words.length; i++) {
            String word = words[i];
            if (word == null || word.isEmpty()) {
                continue;
            }
            String tag = result[i];
            if (tag == null) {
                tag = "";
            }

            // transform 1a: DT, {VBD | VBP | VB} --> DT, NN
            if (i > 0 && "dt".equals(result[i - 1])) {
                if (tag.startsWith("vb")) {
                    tag = "nn";
                    if (NOT_END_S_S.matcher(word).find() && !RiTa.MASS_NOUNS_SET.contains(word)) {
                        tag = "nns";
                    }
                } else if (tag.startsWith("rb")) {
                    tag = (tag.length() > 2) ? "jj" + tag.charAt(2) : "jj";
                }
            }

            // transform 2: noun -> cd if numeric
            if (tag.startsWith("n") && Util.isNum(word)) {
                tag = "cd";
            }

            // transform 3: noun -> vbn if ends with ed after nn/prp
            if (i > 0 && tag.startsWith("n") && word.endsWith("ed") && result[i - 1] != null
                && NN_PRP.matcher(result[i - 1]).find() && !word.endsWith("eed")) {
                tag = "vbn";
            }

            // transform 4: any type -> rb if ends in ly
            if (word.endsWith("ly")) {
                tag = "rb";
            }

            // transform 5: nn -> jj if ends with al (not mammal)
            if (word.length() > 4 && tag.startsWith("nn") && word.endsWith("al") && !word.equals("mammal")) {
                tag = "jj";
            }

            // transform 6: nn -> vb if preceded by modal
            if (i > 0 && tag.startsWith("nn") && result[i - 1] != null && result[i - 1].startsWith("md")) {
                tag = "vb";
            }

            // transform 7: vbd -> vbn when following vbz
            if (tag.equals("vbd") && i > 0 && result[i - 1] != null && VBZ_ONLY.matcher(result[i - 1]).find()) {
                tag = "vbn";
            }

            // transform 8: nn -> vbg if ends with ing and has vbg choice
            if (tag.startsWith("nn") && word.endsWith("ing") && hasTag(choices[i], "vbg")) {
                tag = "vbg";
            }

            // transform 9: nns -> vbz when following nn/prp/nnp and has vbz choice
            if (i > 0 && tag.equals("nns") && hasTag(choices[i], "vbz") && result[i - 1] != null
                && NN_PRP_NNP.matcher(result[i - 1]).find()) {
                tag = "vbz";
            }

            // transform 10: nn -> nnp/nnps if capitalized
            if (tag.startsWith("nn") && CAP.matcher(word).find()) {
                String sing = RiTa.singularize(word.toLowerCase());
                if (words.length == 1 || i > 0 || (i == 0 && !lexHas("nn", sing))) {
                    tag = tag.endsWith("s") ? "nnps" : "nnp";
                }
            }

            // transform 11: nns -> vbz when followed by adverb and has vbz choice
            if (i < result.length - 1 && tag.equals("nns") && result[i + 1] != null
                && result[i + 1].startsWith("rb") && hasTag(choices[i], "vbz")) {
                tag = "vbz";
            }

            // transform 12: nns -> vbz
            if (tag.equals("nns")) {
                if (i > 0 && result[i - 1] != null
                    && List.of("nn", "prp", "cc", "nnp").contains(result[i - 1])) {
                    if (lexHas("vb", RiTa.singularize(word))) {
                        tag = "vbz";
                    }
                } else if (words.length == 1 && choices[i] != null && choices[i].size() < 2) {
                    String sing = RiTa.singularize(word.toLowerCase());
                    if (!lexHas("nn", sing) && lexHas("vb", sing)) {
                        tag = "vbz";
                    }
                }
            }

            // transform 13: vb/nn -> vbp when following nns/nnps/prp
            if (tag.equals("vb") || (tag.equals("nn") && hasTag(choices[i], "vb"))) {
                if (i > 0 && result[i - 1] != null && NNS_NNPS_PRP.matcher(result[i - 1]).find()) {
                    tag = "vbp";
                }
            }

            // issue#83 sequential adjectives
            if (tag.equals("nn") && containsFrom(result, i + 1, "nn")) {
                int idx = indexOfFrom(result, i + 1, "nn");
                boolean allJJ = true;
                for (int k = 0; k < idx; k++) {
                    if (!"jj".equals(result[i + 1 + k])) {
                        allJJ = false;
                        break;
                    }
                }
                if (allJJ && allTags(word).contains("jj")) {
                    tag = "jj";
                }
            }

            // issue#148 "there"
            if (word.toLowerCase().equals("there")) {
                if (i + 1 < words.length && EX_BE.contains(words[i + 1])) {
                    tag = "ex";
                }
                if (i > 0 && "in".equals(result[i - 1])) {
                    tag = "nn";
                }
            }

            // issue#65 #HWF hyphenated words
            if (word.contains("-")) {
                if (!HYPH.equals(result[i])) {
                    continue; // in dict
                }
                if (word.equals("--")) {
                    continue;
                }
                if (HYPHENATEDS.containsKey(word)) {
                    result[i] = HYPHENATEDS.get(word);
                    continue;
                }
                tag = tagCompoundWord(word, tag, result, words, i);
            }

            result[i] = tag;
        }
        return result;
    }

    private String tagCompoundWord(String word, String tag, String[] result, String[] context, int i) {
        String[] parts = word.split("-");
        String firstPart = parts[0];
        String lastPart = parts[parts.length - 1];
        List<String> firstPartAllTags = allTags(firstPart);
        List<String> lastPartAllTags = allTags(lastPart);

        if (parts.length == 2 && VERB_PREFIX.contains(parts[0]) && startsWith(lastPartAllTags, "vb")) {
            tag = firstMatch(lastPartAllTags, "vb");
        } else if (parts.length == 2 && NOUN_PREFIX.contains(parts[0]) && startsWith(lastPartAllTags, "nn")) {
            tag = firstMatch(lastPartAllTags, "nn");
        } else if (startsWith(firstPartAllTags, "cd")) {
            boolean allCD = true;
            for (int z = 1; z < parts.length; z++) {
                if (!startsWith(allTags(parts[z]), "cd")) {
                    allCD = false;
                    break;
                }
            }
            tag = allCD ? "cd" : "jj";
        } else if (startsWith(firstPartAllTags, "jj") && parts.length == 2 && startsWith(lastPartAllTags, "nn")) {
            tag = "jj";
        } else if (firstPartAllTags.contains("vb") && !startsWith(firstPartAllTags, "jj")) {
            if (parts.length == 2 && lastPartAllTags.contains("in")) {
                tag = "nn";
            } else if (parts.length == 2 && anyMatch(lastPartAllTags, VB_GDP) && !lastPartAllTags.contains("vb")) {
                tag = "jj";
            } else if (parts.length == 2 && startsWith(lastPartAllTags, "jj")) {
                tag = "jj";
            } else {
                tag = "nn";
            }
        } else if ((anyMatch(lastPartAllTags, JJ_RS) && !startsWith(lastPartAllTags, "nn"))
            || anyMatch(lastPartAllTags, VB_DGN)) {
            tag = "jj";
        } else if (startsWith(lastPartAllTags, "n")) {
            if (startsWith(firstPartAllTags, "in") || startsWith(firstPartAllTags, "rb")) {
                tag = "jj";
            } else {
                boolean lastNounIsMajor = true;
                for (int z = 0; z < parts.length - 1; z++) {
                    List<String> t = allTags(parts[z]);
                    if (!(startsWith(t, "j") || startsWith(t, "n") || t.contains("dt") || t.contains("in"))) {
                        lastNounIsMajor = false;
                        break;
                    }
                }
                tag = lastNounIsMajor ? "nn" : "jj";
            }
        } else if (startsWith(firstPartAllTags, "n")) {
            tag = RiTa.inflector.isPlural(parts[0]) ? "nns" : "nn";
        } else {
            tag = "nn";
        }

        // change according to context
        if (i + 1 < result.length && result[i + 1] != null && result[i + 1].startsWith("n") && tag.startsWith("n")) {
            tag = "jj";
        } else if (tag.equals("jj") && i + 1 < result.length && result[i + 1] != null
            && result[i + 1].startsWith("v")) {
            tag = "rb";
        } else if (tag.equals("jj") && i - 1 >= 0 && context[i - 1] != null
            && ARTICLES.contains(context[i - 1].toLowerCase().trim())) {
            if (i + 1 >= context.length || (result[i + 1] != null && result[i + 1].matches("^(v|cc|in|md|w)"))
                || RiTa.isPunct(context[i + 1])) {
                tag = "nn";
            }
        }
        return tag;
    }

    // ---- derivation -----------------------------------------------------------------

    private List<String> derivePosData(String word, boolean noGuessing) {
        if (word.equals("the") || word.equals("a")) {
            return new ArrayList<>(List.of("dt"));
        }
        Lexicon lex = RiTa.lexicon;
        int len = word.length();

        if (word.endsWith("ress")) {
            List<String> pos = lex._posArr(word.substring(0, len - 3));
            if (pos != null && pos.contains("vb")) {
                return new ArrayList<>(List.of("nn"));
            }
            pos = lex._posArr(word.substring(0, len - 4));
            if (pos != null && pos.contains("vb")) {
                return new ArrayList<>(List.of("nn"));
            }
        }

        if (word.endsWith("or")) {
            List<String> pos = lex._posArr(word.substring(0, len - 2));
            if (pos != null && pos.contains("vb")) {
                return new ArrayList<>(List.of("nn"));
            }
            pos = lex._posArr(word.substring(0, len - 2) + "e");
            if (pos != null && pos.contains("vb")) {
                return new ArrayList<>(List.of("nn"));
            }
        }

        if (word.endsWith("er")) {
            List<String> pos = lex._posArr(word.substring(0, len - 2));
            if (pos != null && pos.contains("vb")) {
                return new ArrayList<>(List.of("nn"));
            }
            pos = lex._posArr(word.substring(0, len - 1));
            if (pos != null && pos.contains("vb")) {
                return new ArrayList<>(List.of("nn"));
            }
            if (Util.charAt(word, len - 3).equals(Util.charAt(word, len - 4))) {
                pos = lex._posArr(Util.substring(word, 0, len - 3)); // programmer
                if (pos != null && pos.contains("vb")) {
                    return new ArrayList<>(List.of("nn"));
                }
            }
        }

        if (word.endsWith("ies")) {
            String check = word.substring(0, len - 3) + "y";
            List<String> pos = lex._posArr(check);
            if (pos != null && pos.contains("vb")) {
                return new ArrayList<>(List.of("vbz"));
            }
        } else if (word.endsWith("s")) {
            List<String> result = new ArrayList<>();
            checkPluralNounOrVerb(word.substring(0, len - 1), result);
            if (word.endsWith("es")) {
                checkPluralNounOrVerb(word.substring(0, len - 2), result);
                checkPluralNounOrVerb(RiTa.singularize(word), result);
            }
            if (!result.isEmpty()) {
                return result;
            }
        }

        if (word.endsWith("ed")) {
            List<String> pos = lex._posArr(word.substring(0, len - 1));
            if (pos == null) {
                pos = lex._posArr(word.substring(0, len - 2));
            }
            if (pos == null) {
                pos = lex._posArr(Util.substring(word, 0, len - 3));
            }
            if (pos != null && pos.contains("vb")) {
                return new ArrayList<>(List.of("vbd", "vbn"));
            }
        }

        if (word.endsWith("ing")) {
            String stem = word.substring(0, len - 3);
            if (!stem.isEmpty()) {
                List<String> pos = lex._posArr(stem);
                if (pos != null && pos.contains("vb")) {
                    return new ArrayList<>(List.of("vbg", "nn"));
                } else {
                    pos = lex._posArr(stem + "e");
                    if (pos != null && pos.contains("vb")) {
                        return new ArrayList<>(List.of("vbg", "nn"));
                    }
                }
                if (Util.charAt(word, len - 4).equals(Util.charAt(word, len - 5))) {
                    pos = lex._posArr(stem.substring(0, stem.length() - 1));
                    if (pos != null && pos.contains("vb")) {
                        return new ArrayList<>(List.of("vbg", "nn"));
                    }
                }
            }
        }

        if (word.endsWith("ly")) {
            String stem = word.substring(0, len - 2);
            if (!stem.isEmpty()) {
                List<String> pos = lex._posArr(stem);
                if (pos != null && pos.contains("jj")) {
                    return new ArrayList<>(List.of("rb"));
                }
                if (stem.charAt(stem.length() - 1) == 'i') {
                    pos = lex._posArr(stem.substring(0, stem.length() - 1) + "y");
                    if (pos != null && pos.contains("jj")) {
                        return new ArrayList<>(List.of("rb"));
                    }
                }
            }
        }

        if (isLikelyPlural(word)) {
            return new ArrayList<>(List.of("nns"));
        }

        if (Conjugator.IRREG_PAST_PART.contains(word)) {
            return new ArrayList<>(List.of("vbd"));
        }

        if (noGuessing) {
            return new ArrayList<>();
        }
        if (word.endsWith("ly")) {
            return new ArrayList<>(List.of("rb"));
        }
        if (word.endsWith("s")) {
            return new ArrayList<>(List.of("nns"));
        }
        return new ArrayList<>(List.of("nn"));
    }

    private void checkPluralNounOrVerb(String stem, List<String> result) {
        List<String> pos = RiTa.lexicon._posArr(stem);
        if (pos != null) {
            if (pos.contains("nn")) {
                result.add("nns");
            }
            if (pos.contains("vb")) {
                result.add("vbz");
            }
        }
        if (pos == null || !pos.contains("vbz")) {
            if (isNoLexIrregularVerb(stem)) {
                result.add("vbz");
            }
        }
    }

    private boolean isLikelyPlural(String word) {
        return lexHas("n", RiTa.singularize(word));
    }

    private boolean isNoLexIrregularVerb(String stem) {
        return Conjugator.IRREG_VERBS_NOLEX.containsValue(stem);
    }

    private String handleSingleLetter(String c) {
        if (c.equals("a") || c.equals("A")) {
            return "dt";
        }
        if (c.compareTo("0") >= 0 && c.compareTo("9") <= 0) {
            return "cd";
        }
        return c.equals("I") ? "prp" : c;
    }

    private boolean lexHas(String pos, String word) {
        if (word == null) {
            return false;
        }
        List<String> tags = RiTa.lexicon._posArr(word);
        if (tags == null) {
            return false;
        }
        for (String t : tags) {
            if (pos.equals(t)) {
                return true;
            }
            if (pos.equals("n") && NOUNS.contains(t)) {
                return true;
            }
            if (pos.equals("v") && VERBS.contains(t)) {
                return true;
            }
            if (pos.equals("r") && ADVS.contains(t)) {
                return true;
            }
            if (pos.equals("a") && ADJS.contains(t)) {
                return true;
            }
        }
        return false;
    }

    // ---- helpers --------------------------------------------------------------------

    private static List<String> simplify(List<String> tags) {
        List<String> out = new ArrayList<>(tags.size());
        for (String t : tags) {
            if (NOUNS.contains(t)) {
                out.add("n");
            } else if (VERBS.contains(t)) {
                out.add("v");
            } else if (ADJS.contains(t)) {
                out.add("a");
            } else if (ADVS.contains(t)) {
                out.add("r");
            } else {
                out.add("-");
            }
        }
        return out;
    }

    private static String simpleTag(String t) {
        if (NOUNS.contains(t)) {
            return "n";
        }
        if (VERBS.contains(t)) {
            return "v";
        }
        if (ADJS.contains(t)) {
            return "a";
        }
        if (ADVS.contains(t)) {
            return "r";
        }
        return "-";
    }

    private static boolean anyIn(List<String> tags, List<String> set) {
        for (String t : tags) {
            if (set.contains(t)) {
                return true;
            }
        }
        return false;
    }

    private static boolean startsWith(List<String> tags, String prefix) {
        for (String t : tags) {
            if (t.startsWith(prefix)) {
                return true;
            }
        }
        return false;
    }

    private static String firstMatch(List<String> tags, String prefix) {
        for (String t : tags) {
            if (t.startsWith(prefix)) {
                return t;
            }
        }
        return null;
    }

    private static boolean anyMatch(List<String> tags, Pattern p) {
        for (String t : tags) {
            if (p.matcher(t).find()) {
                return true;
            }
        }
        return false;
    }

    private static boolean containsFrom(String[] arr, int from, String target) {
        for (int i = from; i < arr.length; i++) {
            if (target.equals(arr[i])) {
                return true;
            }
        }
        return false;
    }

    private static int indexOfFrom(String[] arr, int from, String target) {
        for (int i = from; i < arr.length; i++) {
            if (target.equals(arr[i])) {
                return i - from;
            }
        }
        return -1;
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
}
