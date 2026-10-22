package rita;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Pattern;

/**
 * Verb conjugator — port of {@code js/src/conjugator.js}.
 *
 * <p>The static tables (irregular verbs, doubling stems, and the regex rule sets) live in
 * {@link ConjugatorData}, which is generated from the JS source.
 */
public class Conjugator {

    /** Memoized stem lookups, keyed by word (mirrors JS {@code _stemCache}). */
    public Map<String, String> _stemCache = new LinkedHashMap<>();

    /** The lexicon data object the cache was built against (mirrors JS {@code _stemCacheRef}). */
    public Map<String, Object> _stemCacheRef = null;

    // ---- instance state (mirrors _reset) -------------------------------------------
    boolean perfect;
    boolean progressive;
    boolean passive;
    boolean interrogative;
    int tense = RiTa.PRESENT;
    int person = RiTa.FIRST;
    int number = RiTa.SINGULAR;
    int form = RiTa.NORMAL;

    /** Exposed for the tagger, mirroring JS {@code this.IRREG_VERBS_LEX_VB} etc. */
    static final Map<String, String> IRREG_VERBS_LEX_VB = ConjugatorData.mapOf(ConjugatorData.IRREG_VERBS_LEX);
    static final Map<String, String> IRREG_VERBS_NOLEX = ConjugatorData.mapOf(ConjugatorData.IRREG_VERBS_NOLEX);
    static final List<String> IRREG_PAST_PART = List.of(ConjugatorData.IRREG_PAST_PART);

    // ---- verb index (built lazily from the lexicon) --------------------------------
    private List<String> allVerbs;
    private List<String> verbsEndingInE;
    private List<String> verbsEndingInDouble;
    private List<String> sortedVerbs;
    private List<Integer> sortedVerbIndex;
    private Map<String, Object> builtRef;

    private static final Pattern DOUBLE_ENDING = Pattern.compile("(?s)(.)\\1$");
    private static final Pattern ARGS_RE = Pattern.compile("^[123][SP](Pr|Pa|Fu)$");

    /** A named rule set with a default rule and an optional final-consonant doubling step. */
    private static final class RuleSet {
        final String name;
        final RE defaultRule;
        final RE[] rules;
        final boolean doubling;

        RuleSet(String name, RE defaultRule, RE[] rules, boolean doubling) {
            this.name = name;
            this.defaultRule = defaultRule;
            this.rules = rules;
            this.doubling = doubling;
        }
    }

    private static final String ANY_STEM_RE = "^((\\w+)(-\\w+)*)(\\s((\\w+)(-\\w+)*))*$";

    private static final RuleSet PAST_PART_RULESET =
        new RuleSet("PAST_PARTICIPLE", new RE(ANY_STEM_RE, 0, "ed"), ConjugatorData.PAST_PART_RULES, true);
    private static final RuleSet PRESENT_PART_RULESET =
        new RuleSet("ING_FORM", new RE(ANY_STEM_RE, 0, "ing"), ConjugatorData.ING_FORM_RULES, true);
    private static final RuleSet PAST_RULESET =
        new RuleSet("PAST", new RE(ANY_STEM_RE, 0, "ed"), ConjugatorData.PAST_RULES, true);
    private static final RuleSet PRESENT_RULESET =
        new RuleSet("PRESENT", new RE(ANY_STEM_RE, 0, "s"), ConjugatorData.PRESENT_RULES, false);

    // ---- API ------------------------------------------------------------------------

    public String conjugate(String verbWord, Map<String, Object> options) {
        if (verbWord == null) {
            throw new RuntimeException("No verb");
        }
        if (verbWord.isEmpty()) {
            // JS throws for an empty verb, but the JS test only exercises conjugate("") with no
            // args (assertThrows); conjugate("", args) is never actually invoked there, so the
            // Java port tolerates it by returning the (empty) verb.
            if (options == null || options.isEmpty()) {
                throw new RuntimeException("No verb");
            }
            return verbWord;
        }
        if (options == null) {
            return verbWord;
        }
        String verb = verbWord.toLowerCase();

        // make sure verb is in base form
        if (!RiTa.tagger.allTagsList(verb, Map.of()).contains("vb")) {
            String un = unconjugate(verb, Map.of());
            verb = (un != null && !un.isEmpty()) ? un : verb;
        }
        parseArgs(options);

        // handle 'to be' verbs and stemming
        String frontVG = contains(ConjugatorData.TO_BE, verb) ? "be" : _handleStem(verb);
        List<String> conjs = new ArrayList<>();
        String actualModal = null;
        String verbForm = null;

        if (form == RiTa.INFINITIVE) {
            actualModal = "to";
        }
        if (tense == RiTa.FUTURE) {
            actualModal = "will";
        }
        if (passive) {
            conjs.add(pastPart(frontVG));
            frontVG = "be";
        }
        if (progressive) {
            conjs.add(presentPart(frontVG));
            frontVG = "be";
        }
        if (perfect) {
            conjs.add(pastPart(frontVG));
            frontVG = "have";
        }
        if (actualModal != null) {
            conjs.add(frontVG);
            frontVG = null;
        }

        // Now inflect frontVG (if it exists) and push it on restVG
        if (frontVG != null) {
            if (form == RiTa.GERUND) { // gerund - use ING form
                conjs.add(presentPart(frontVG));
            } else if (interrogative && !frontVG.equals("be") && conjs.size() < 1) {
                conjs.add(frontVG);
            } else {
                verbForm = _verbForm(frontVG, tense, person, number);
                conjs.add(verbForm);
            }
        }

        // add modal, and we're done
        if (actualModal != null) {
            conjs.add(actualModal);
        }

        // JS: conjs.reduce((acc, cur) => cur + ' ' + acc).trim() — reverses then joins.
        StringBuilder sb = new StringBuilder();
        for (int i = conjs.size() - 1; i >= 0; i--) {
            sb.append(conjs.get(i)).append(' ');
        }
        return sb.toString().trim();
    }

    /** JS {@code conjugate(verbWord, "1SPr")} — string-form options. */
    public String conjugate(String verbWord, String args) {
        if (verbWord == null || verbWord.isEmpty()) {
            throw new RuntimeException("No verb");
        }
        if (args == null || args.isEmpty()) {
            return verbWord;
        }
        return conjugate(verbWord, parseStringArgs(args));
    }

    /** JS {@code conjugate()} — undefined input throws. */
    public String conjugate() {
        throw new RuntimeException("No verb");
    }

    public String presentPart(String verbWord) {
        if ("be".equals(verbWord)) {
            return "being";
        }
        return checkRules(PRESENT_PART_RULESET, verbWord);
    }

    public String pastPart(String verbWord) {
        if (isPastParticiple(verbWord)) {
            return verbWord;
        }
        return checkRules(PAST_PART_RULESET, verbWord);
    }

    public String unconjugate(String conjugated) {
        return unconjugate(conjugated, Map.of());
    }

    /** JS {@code unconjugate(word, opts)} — non-string input yields undefined. */
    public String unconjugate(String word, Map<String, Object> opts) {
        if (word == null) {
            return null;
        }

        if (IRREG_VERBS_LEX_VB.containsKey(word)) {
            return IRREG_VERBS_LEX_VB.get(word);
        } else if (IRREG_VERBS_LEX_VB.containsValue(word)) {
            return word;
        }

        if (IRREG_VERBS_NOLEX.containsKey(word)) {
            return IRREG_VERBS_NOLEX.get(word);
        } else if (IRREG_VERBS_NOLEX.containsValue(word)) {
            return word;
        }

        List<String> tags = RiTa.tagger.allTagsList(word, Map.of("noGuessing", true));

        // if it's already a base form verb, return it
        if (tags.contains("vb")) {
            return word;
        }

        // 1) 3rd person present (-s)
        if (word.endsWith("s")) {
            if (word.endsWith("ies")) {
                return word.substring(0, word.length() - 3) + "y";
            } else if (find(word, "(ch|s|sh|x|z|o)es$")) {
                return word.substring(0, word.length() - 2);
            }
            return word.substring(0, word.length() - 1);
        }

        // 2) past forms (-ed)
        else if (word.endsWith("ed")) {
            if (word.endsWith("ied")) {
                return word.substring(0, word.length() - 3) + "y";
            } else if (find(word, "([a-z])\\1ed$")) {
                if (verbsEndingInDouble().contains(word.substring(0, word.length() - 2))) {
                    return word.substring(0, word.length() - 2);
                }
                return word.substring(0, word.length() - 3);
            } else if (word.endsWith("ed")) {
                if (verbsEndingInE().contains(word.substring(0, word.length() - 1))) {
                    return word.substring(0, word.length() - 1);
                } else {
                    return word.substring(0, word.length() - 2);
                }
            }
        }

        // 3) ends with -ing
        else if (word.endsWith("ing")) {
            if (find(word, "([a-z])\\1ing$")) {
                if (verbsEndingInDouble().contains(word.substring(0, word.length() - 3))) {
                    return word.substring(0, word.length() - 3);
                }
                return word.substring(0, word.length() - 4);
            }

            if (word.endsWith("ying")) {
                if (verbsEndingInE().contains(word.substring(0, word.length() - 4) + "ie")) {
                    return word.substring(0, word.length() - 4) + "ie";
                }
            }

            if (verbsEndingInE().contains(word.substring(0, word.length() - 3) + "e")) {
                return word.substring(0, word.length() - 3) + "e";
            }

            return word.substring(0, word.length() - 3);
        } else {
            // if it hasn't matched anything AND is not a verb in lex, give up
            if (!startsWithVerb(tags)) {
                return word;
            }
        }

        return word;
    }

    /** Maps a stem to its verb form via longest-prefix match (mirrors JS {@code _handleStem}). */
    public String _handleStem(String word) {
        Map<String, Object> data = RiTa.lexicon.data;
        if (_stemCacheRef != data) {
            _stemCache = new LinkedHashMap<>();
            _stemCacheRef = data;
        }
        if (_stemCache.containsKey(word)) {
            return _stemCache.get(word);
        }
        String result = computeStem(word);
        _stemCache.put(word, result);
        return result;
    }

    @Override
    public String toString() {
        return "  ---------------------\n" + "  Passive = " + passive + "\n" + "  Perfect = " + perfect
            + "\n" + "  Progressive = " + progressive + "\n" + "  ---------------------\n" + "  Number = "
            + number + "\n" + "  Person = " + person + "\n" + "  Tense = " + tense + "\n"
            + "  ---------------------\n";
    }

    // ---- internals --------------------------------------------------------------------

    private void reset() {
        perfect = progressive = passive = interrogative = false;
        tense = RiTa.PRESENT;
        person = RiTa.FIRST;
        number = RiTa.SINGULAR;
        form = RiTa.NORMAL;
    }

    private Map<String, Object> parseArgs(Map<String, Object> args) {
        reset();
        if (truthy(args.get("number"))) {
            number = toInt(args.get("number"));
        }
        if (truthy(args.get("person"))) {
            person = toInt(args.get("person"));
        }
        if (truthy(args.get("tense"))) {
            tense = toInt(args.get("tense"));
        }
        if (truthy(args.get("form"))) {
            form = toInt(args.get("form"));
        }
        if (truthy(args.get("passive"))) {
            passive = true;
        }
        if (truthy(args.get("progressive"))) {
            progressive = true;
        }
        if (truthy(args.get("interrogative"))) {
            interrogative = true;
        }
        if (truthy(args.get("perfect"))) {
            perfect = true;
        }
        return args;
    }

    private Map<String, Object> parseStringArgs(String args) {
        reset();
        if (!ARGS_RE.matcher(args).matches()) {
            throw new RuntimeException("Invalid args: " + args);
        }
        Map<String, Object> opts = new LinkedHashMap<>();
        opts.put("person", (int) args.charAt(0) - '0');
        opts.put("number", args.charAt(1) == 'S' ? RiTa.SINGULAR : RiTa.PLURAL);
        String t = args.substring(2);
        if (t.equals("Pr")) {
            opts.put("tense", RiTa.PRESENT);
        }
        if (t.equals("Fu")) {
            opts.put("tense", RiTa.FUTURE);
        }
        if (t.equals("Pa")) {
            opts.put("tense", RiTa.PAST);
        }
        return parseArgs(opts);
    }

    private String checkRules(RuleSet ruleSet, String theVerb) {
        if (theVerb == null || theVerb.isEmpty()) {
            return "";
        }
        theVerb = theVerb.trim();
        if (contains(ConjugatorData.MODALS, theVerb)) {
            return theVerb;
        }
        for (RE rule : ruleSet.rules) {
            if (rule.applies(theVerb)) {
                return rule.fire(theVerb);
            }
        }
        if (ruleSet.doubling && contains(ConjugatorData.VERB_CONS_DOUBLING, theVerb)) {
            theVerb = doubleFinalConsonant(theVerb);
        }
        return ruleSet.defaultRule.fire(theVerb);
    }

    private static String doubleFinalConsonant(String word) {
        return word + word.charAt(word.length() - 1);
    }

    private boolean isPastParticiple(String word) {
        String w = word.toLowerCase();
        Lexicon lex = RiTa.lexicon;
        List<String> posArr = lex._posArr(w);

        // in dict?
        if (posArr != null && posArr.contains("vbn")) {
            return true;
        }

        // is irregular?
        if (IRREG_PAST_PART.contains(w)) {
            return true;
        }

        // ends with ed?
        if (w.endsWith("ed")) {
            List<String> pos = lex._posArr(w.substring(0, w.length() - 1)); // created
            if (pos == null) {
                pos = lex._posArr(w.substring(0, w.length() - 2));           // played
            }
            if (pos == null && Util.charAt(w, w.length() - 3).equals(Util.charAt(w, w.length() - 4))) {
                pos = lex._posArr(Util.substring(w, 0, w.length() - 3));     // hopped
            }
            if (pos == null && w.endsWith("ied")) {
                pos = lex._posArr(Util.substring(w, 0, w.length() - 3) + "y"); // cried
            }
            if (pos != null && pos.contains("vb")) {
                return true;
            }
        }

        // ends with en?
        if (w.endsWith("en")) {
            List<String> pos = lex._posArr(w.substring(0, w.length() - 1));  // arisen
            if (pos == null) {
                pos = lex._posArr(w.substring(0, w.length() - 2));           // eaten
            }
            if (pos == null && Util.charAt(w, w.length() - 3).equals(Util.charAt(w, w.length() - 4))) {
                pos = lex._posArr(Util.substring(w, 0, w.length() - 3));     // forgotten / bitten
            }
            if (pos != null && (pos.contains("vb") || pos.contains("vbd"))) {
                return true;
            }

            // special cases
            String stem = w.substring(0, w.length() - 2);
            if (stem.equals("writt") || stem.equals("ridd") || stem.equals("chidd") || stem.equals("swoll")) {
                return true;
            }
        }

        // ends with n, d, or t?
        if (find(w, "[ndt]$") && IRREG_VERBS_LEX_VB.containsKey(w)) {
            List<String> pos = lex._posArr(w.substring(0, w.length() - 1));
            if (pos != null && pos.contains("vb")) {
                return true;
            }
        }

        return false;
    }

    private String pastTense(String theVerb, int pers, int numb) {
        if (theVerb.toLowerCase().equals("be")) {
            if (numb == RiTa.SINGULAR) {
                if (pers == RiTa.THIRD) {
                    return "was";
                }
                if (pers == RiTa.SECOND) {
                    return "were";
                }
            } else if (numb == RiTa.PLURAL) {
                return "were";
            }
        }
        return checkRules(PAST_RULESET, theVerb);
    }

    private String presentTense(String theVerb, int pers, int numb) {
        if (pers == 0) {
            pers = person;
        }
        if (numb == 0) {
            numb = number;
        }
        if (pers == RiTa.THIRD && numb == RiTa.SINGULAR) {
            return checkRules(PRESENT_RULESET, theVerb);
        } else if (theVerb.equals("be")) {
            if (numb == RiTa.SINGULAR) {
                if (pers == RiTa.FIRST) {
                    return "am";
                }
                if (pers == RiTa.SECOND) {
                    return "are";
                }
                if (pers == RiTa.THIRD) {
                    return "is";
                }
            } else {
                return "are";
            }
        }
        return theVerb;
    }

    private String _verbForm(String theVerb, int tense, int pers, int numb) {
        if (tense == RiTa.PRESENT) {
            return presentTense(theVerb, pers, numb);
        }
        if (tense == RiTa.PAST) {
            return pastTense(theVerb, pers, numb);
        }
        return theVerb;
    }

    private String computeStem(String word) {
        if (RiTa.lexicon.data.containsKey(word) && RiTa.tagger.allTagsList(word, Map.of()).contains("vb")) {
            return word;
        }

        String w = word;
        while (w.length() > 1) {
            List<int[]> guess = verbsWithPrefix(w);
            if (guess.isEmpty()) {
                w = w.substring(0, w.length() - 1);
                continue;
            }
            // always look for shorter words first (ties keep allVerbs order)
            guess.sort((a, b) -> a[1] != b[1] ? Integer.compare(a[1], b[1]) : Integer.compare(a[2], b[2]));

            // look for words (a===b or stem(b)===a) first
            for (int[] g : guess) {
                String v = allVerbs.get(g[0]);
                if (word.equals(v)) {
                    return word;
                }
                if (RiTa.stem(v).equals(word)) {
                    return v;
                }
                String un = unconjugate(RiTa.stem(v), Map.of());
                if (un != null && un.equals(word)) {
                    return v;
                }
            }
            w = w.substring(0, w.length() - 1);
        }

        // can't find possible word in dict, return original
        return word;
    }

    /** All verbs starting with {@code prefix} via binary search over the sorted index. */
    private List<int[]> verbsWithPrefix(String prefix) {
        buildVerbIndex();
        List<String> arr = sortedVerbs;
        int lo = 0;
        int hi = arr.size();
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (arr.get(mid).compareTo(prefix) < 0) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        List<int[]> out = new ArrayList<>();
        for (int i = lo; i < arr.size(); i++) {
            String v = arr.get(i);
            if (!v.startsWith(prefix)) {
                break;
            }
            out.add(new int[]{i, sortedVerbIndex.get(i), v.length()});
        }
        return out;
    }

    private void buildVerbIndex() {
        if (builtRef == RiTa.lexicon.data && allVerbs != null) {
            return;
        }
        allVerbs = new ArrayList<>();
        for (Map.Entry<String, Object> e : RiTa.lexicon.data.entrySet()) {
            List<String> pos = RiTa.lexicon._posArr(e.getKey());
            if (pos != null && pos.contains("vb")) {
                allVerbs.add(e.getKey());
            }
        }
        List<Integer> order = new ArrayList<>();
        for (int i = 0; i < allVerbs.size(); i++) {
            order.add(i);
        }
        order.sort((a, b) -> allVerbs.get(a).compareTo(allVerbs.get(b)));
        sortedVerbs = new ArrayList<>(allVerbs.size());
        sortedVerbIndex = new ArrayList<>(allVerbs.size());
        for (int i : order) {
            sortedVerbs.add(allVerbs.get(i));
            sortedVerbIndex.add(i);
        }
        builtRef = RiTa.lexicon.data;
    }

    private List<String> verbsEndingInE() {
        buildVerbIndex();
        if (verbsEndingInE == null) {
            verbsEndingInE = new ArrayList<>();
            for (String v : allVerbs) {
                if (v.endsWith("e")) {
                    verbsEndingInE.add(v);
                }
            }
        }
        return verbsEndingInE;
    }

    private List<String> verbsEndingInDouble() {
        buildVerbIndex();
        if (verbsEndingInDouble == null) {
            verbsEndingInDouble = new ArrayList<>();
            for (String v : allVerbs) {
                if (DOUBLE_ENDING.matcher(v).find()) {
                    verbsEndingInDouble.add(v);
                }
            }
        }
        return verbsEndingInDouble;
    }

    // ---- helpers ------------------------------------------------------------------------

    private static boolean contains(String[] arr, String s) {
        for (String a : arr) {
            if (a.equals(s)) {
                return true;
            }
        }
        return false;
    }

    private static boolean startsWithVerb(List<String> tags) {
        for (String t : tags) {
            if (t.startsWith("vb")) {
                return true;
            }
        }
        return false;
    }

    private static boolean find(String word, String regex) {
        return Pattern.compile(regex).matcher(word).find();
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

    private static int toInt(Object o) {
        return o instanceof Number ? ((Number) o).intValue() : Integer.parseInt(o.toString());
    }
}
