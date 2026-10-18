package rita;

import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Entry point for the RiTa API — currently a signature-only stub so the ported test suite
 * compiles and fails on behaviour rather than compilation. Methods throw
 * {@link UnsupportedOperationException}; constants and component singletons are real so
 * tests that read them (e.g. {@code RiTa.THIRD}, {@code RiTa.STOP_WORDS}) behave correctly.
 *
 * <p>Signatures mirror <code>js/src/rita.js</code>. JS async methods (rhymes, search, …) are
 * synchronous here, returning the resolved value directly, since Java tests have no
 * {@code await}.
 */
public final class RiTa {

    private RiTa() {
    }

    // ---- component singletons (mirror js/src/rita.js) -------------------------------
    public static final RandGen randomizer = new RandGen();
    public static final Tagger tagger = new Tagger();
    public static final Analyzer analyzer = new Analyzer();
    public static final Concorder concorder = new Concorder();
    public static final Tokenizer tokenizer = new Tokenizer();
    public static final Inflector inflector = new Inflector();
    public static final Lexicon lexicon = new Lexicon();
    public static final Conjugator conjugator = new Conjugator();
    public static final RiScript riscript = new RiScript();
    public static final Util Util = new Util();

    // ---- constants ------------------------------------------------------------------
    public static final String VERSION = "4.0.3";
    public static boolean SILENT = false;
    public static boolean SILENCE_LTS = false;
    public static boolean CACHING = true;
    public static boolean SPLIT_CONTRACTIONS = false;

    public static final int FIRST = 1;
    public static final int SECOND = 2;
    public static final int THIRD = 3;
    public static final int PAST = 4;
    public static final int PRESENT = 5;
    public static final int FUTURE = 6;
    public static final int SINGULAR = 7;
    public static final int PLURAL = 8;
    public static final int NORMAL = 9;
    public static final int INFINITIVE = 1;
    public static final int GERUND = 2;
    public static final String STRESS = "1";
    public static final String NOSTRESS = "0";
    public static final String PHONE_BOUNDARY = "-";
    public static final String WORD_BOUNDARY = " ";
    public static final String SYLLABLE_BOUNDARY = "/";
    public static final String SENTENCE_BOUNDARY = "|";
    public static final String VOWELS = "aeiou";

    public static final String[] PHONES = {"aa", "ae", "ah", "ao", "aw", "ay", "b", "ch", "d", "dh", "eh", "er", "ey", "f", "g", "hh", "ih", "iy", "jh", "k", "l", "m", "n", "ng", "ow", "oy", "p", "r", "s", "sh", "t", "th", "uh", "uw", "v", "w", "y", "z", "zh"};
    public static final String[] ABRV = {"Adm.", "Capt.", "Cmdr.", "Col.", "Dr.", "Gen.", "Gov.", "Lt.", "Maj.", "Messrs.", "Mr.", "Mrs.", "Ms.", "Prof.", "Rep.", "Reps.", "Rev.", "Sen.", "Sens.", "Sgt.", "Sr.", "St.", "A.k.a.", "C.f.", "I.e.", "E.g.", "Vs.", "V.", "Jan.", "Feb.", "Mar.", "Apr.", "Mar.", "Jun.", "Jul.", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."};
    public static List<String> QUESTIONS = new java.util.ArrayList<>(List.of("was", "what", "when", "where", "which", "why", "who", "will", "would", "who", "how", "if", "is", "could", "might", "does", "are", "have"));
    public static List<String> STOP_WORDS = new java.util.ArrayList<>(List.of("and", "a", "of", "in", "i", "you", "is", "to", "that", "it", "for", "on", "have", "with", "this", "be", "not", "are", "as", "was", "but", "or", "from", "my", "at", "if", "they", "your", "all", "he", "by", "one", "me", "what", "so", "can", "will", "do", "an", "about", "we", "just", "would", "there", "no", "like", "out", "his", "has", "up", "more", "who", "when", "don't", "some", "had", "them", "any", "their", "it's", "only", "which", "i'm", "been", "other", "were", "how", "then", "now", "her", "than", "she", "well", "also", "us", "very", "because", "am", "here", "could", "even", "him", "into", "our", "much", "too", "did", "should", "over", "want", "these", "may", "where", "most", "many", "those", "does", "why", "please", "off", "going", "its", "i've", "down", "that's", "can't", "you're", "didn't", "another", "around", "must", "few", "doesn't", "the", "every", "yes", "each", "maybe", "i'll", "away", "doing", "oh", "else", "isn't", "he's", "there's", "hi", "won't", "ok", "they're", "yeah", "mine", "we're", "what's", "shall", "she's", "hello", "okay", "here's", "less", "said", "under"));
    public static List<String> MASS_NOUNS = new java.util.ArrayList<>(List.of("abalone", "asbestos", "barracks", "bathos", "breeches", "beef", "britches", "chaos", "chinese", "cognoscenti", "clippers", "corps", "cosmos", "crossroads", "diabetes", "ethos", "gallows", "graffiti", "herpes", "innings", "lens", "means", "measles", "mews", "mumps", "news", "pasta", "pathos", "pincers", "pliers", "proceedings", "rabies", "rhinoceros", "sassafras", "scissors", "series", "shears", "species", "tuna"));

    // Set mirrors (rebuilt lazily in the real impl; static here for the stub).
    public static Set<String> STOP_WORDS_SET = new java.util.LinkedHashSet<>(STOP_WORDS);
    public static Set<String> MASS_NOUNS_SET = new java.util.LinkedHashSet<>(MASS_NOUNS);
    public static Set<String> QUESTIONS_SET = new java.util.LinkedHashSet<>(QUESTIONS);

    // ---- static methods -------------------------------------------------------------

    public static RiGrammar grammar() {
        throw notPorted("grammar");
    }

    public static RiGrammar grammar(Object rules) {
        throw notPorted("grammar");
    }

    public static RiGrammar grammar(Object rules, Map<String, Object> context) {
        throw notPorted("grammar");
    }

    public static void addTransform(String name, Object definition) {
        throw notPorted("addTransform");
    }

    public static void removeTransform(String name) {
        throw notPorted("removeTransform");
    }

    public static Set<String> getTransforms() {
        throw notPorted("getTransforms");
    }

    public static String articlize(String word) {
        throw notPorted("articlize");
    }

    public static String evaluate(String script) {
        throw notPorted("evaluate");
    }

    /** JS {@code evaluate(script, context)} — context may be a Map or a falsy scalar (e.g. 0). */
    public static String evaluate(String script, Object context) {
        throw notPorted("evaluate");
    }

    public static String evaluate(String script, Object context, Map<String, Object> options) {
        throw notPorted("evaluate");
    }

    public static RiMarkov markov(int n) {
        throw notPorted("markov");
    }

    public static RiMarkov markov(int n, Map<String, Object> options) {
        throw notPorted("markov");
    }

    public static List<String> kwic(String keyword, Map<String, Object> options) {
        throw notPorted("kwic");
    }

    public static Map<String, Integer> concordance(String text, Map<String, Object> options) {
        throw notPorted("concordance");
    }

    public static int[] randomOrdering(int k) {
        throw notPorted("randomOrdering");
    }

    public static <T> List<T> randomOrdering(List<T> array) {
        throw notPorted("randomOrdering");
    }

    public static void randomSeed(int seed) {
        throw notPorted("randomSeed");
    }

    public static boolean isQuestion(String sentence) {
        throw notPorted("isQuestion");
    }

    public static boolean isVowel(String charOrWord) {
        throw notPorted("isVowel");
    }

    public static boolean isConsonant(String charOrWord) {
        throw notPorted("isConsonant");
    }

    public static String capitalize(String string) {
        return string == null || string.isEmpty() ? "" : string.substring(0, 1).toUpperCase() + string.substring(1);
    }

    public static String randomWord(Object pattern, Map<String, Object> options) {
        throw notPorted("randomWord");
    }

    /** JS {@code randomWord("^a")} — a pattern string with no options. */
    public static String randomWord(String pattern) {
        throw notPorted("randomWord");
    }

    /** JS {@code randomWord({ pos: "nn" })} — options only. */
    public static String randomWord(Map<String, Object> options) {
        throw notPorted("randomWord");
    }

    public static String randomWord() {
        throw notPorted("randomWord");
    }

    public static List<String> rhymes(String word, Map<String, Object> options) {
        throw notPorted("rhymes");
    }

    public static List<String> rhymes(String word, int limit) {
        throw notPorted("rhymes");
    }

    public static boolean isRhyme(String word1, String word2) {
        throw notPorted("isRhyme");
    }

    public static List<String> alliterations(String word, Map<String, Object> options) {
        throw notPorted("alliterations");
    }

    public static boolean hasWord(String word, Map<String, Object> options) {
        throw notPorted("hasWord");
    }

    public static boolean hasWord(String word) {
        throw notPorted("hasWord");
    }

    public static boolean isAbbrev(String input, Map<String, Object> options) {
        throw notPorted("isAbbrev");
    }

    public static boolean isAbbrev(String input) {
        throw notPorted("isAbbrev");
    }

    public static boolean isAlliteration(String word1, String word2) {
        throw notPorted("isAlliteration");
    }

    public static List<String> spellsLike(String word, Map<String, Object> options) {
        throw notPorted("spellsLike");
    }

    public static List<String> soundsLike(String word, Map<String, Object> options) {
        throw notPorted("soundsLike");
    }

    public static String[] pos(String word, Map<String, Object> options) {
        throw notPorted("pos");
    }

    public static String[] pos(String word) {
        throw notPorted("pos");
    }

    public static String[] pos(String[] words) {
        throw notPorted("pos");
    }

    public static String[] pos(String[] words, Map<String, Object> options) {
        throw notPorted("pos");
    }

    public static boolean isNoun(String word) {
        throw notPorted("isNoun");
    }

    /** JS {@code isNoun()} — undefined is not a noun. */
    public static boolean isNoun() {
        throw notPorted("isNoun");
    }

    public static boolean isAdjective(String word) {
        throw notPorted("isAdjective");
    }

    public static boolean isAdjective() {
        throw notPorted("isAdjective");
    }

    public static boolean isAdverb(String word) {
        throw notPorted("isAdverb");
    }

    public static boolean isAdverb() {
        throw notPorted("isAdverb");
    }

    public static boolean isVerb(String word) {
        throw notPorted("isVerb");
    }

    public static boolean isVerb() {
        throw notPorted("isVerb");
    }

    public static boolean isPunct(String text) {
        throw notPorted("isPunct");
    }

    public static String posInline(String sentence, Map<String, Object> options) {
        throw notPorted("posInline");
    }

    public static String posInline(String sentence) {
        throw notPorted("posInline");
    }

    public static String posInline(String[] words) {
        throw notPorted("posInline");
    }

    public static String posInline(String[] words, Map<String, Object> options) {
        throw notPorted("posInline");
    }

    public static String singularize(String word) {
        throw notPorted("singularize");
    }

    public static String singularize(String word, Map<String, Object> options) {
        throw notPorted("singularize");
    }

    /** JS {@code RiTa.singularize()} — undefined input yields the empty string. */
    public static String singularize() {
        throw notPorted("singularize");
    }

    public static String pluralize(String word) {
        throw notPorted("pluralize");
    }

    public static String pluralize(String word, Map<String, Object> options) {
        throw notPorted("pluralize");
    }

    /** JS {@code RiTa.pluralize()} — undefined input yields the empty string. */
    public static String pluralize() {
        throw notPorted("pluralize");
    }

    public static List<String> search(Object pattern, Map<String, Object> options) {
        throw notPorted("search");
    }

    /** JS {@code search("phant")} — a pattern string with no options. */
    public static List<String> search(String pattern) {
        throw notPorted("search");
    }

    public static List<String> search(Map<String, Object> options) {
        throw notPorted("search");
    }

    public static List<String> search() {
        throw notPorted("search");
    }

    public static String[] tokens(String text, Map<String, Object> options) {
        throw notPorted("tokens");
    }

    public static String[] tokens(String text) {
        throw notPorted("tokens");
    }

    public static String[] tokenize(String input, Map<String, Object> options) {
        throw notPorted("tokenize");
    }

    public static String[] tokenize(String input) {
        throw notPorted("tokenize");
    }

    public static String untokenize(String[] input, String delim) {
        throw notPorted("untokenize");
    }

    public static String untokenize(String[] input) {
        throw notPorted("untokenize");
    }

    public static String[] sentences(String text, String pattern) {
        throw notPorted("sentences");
    }

    public static String[] sentences(String text) {
        throw notPorted("sentences");
    }

    public static boolean isStopWord(String word) {
        throw notPorted("isStopWord");
    }

    public static String stem(String word) {
        throw notPorted("stem");
    }

    public static boolean findStem(String word) {
        throw notPorted("findStem");
    }

    public static String presentPart(String verbWord) {
        throw notPorted("presentPart");
    }

    public static String pastPart(String verbWord) {
        throw notPorted("pastPart");
    }

    public static String conjugate(String verbWord, Map<String, Object> options) {
        throw notPorted("conjugate");
    }

    /** JS {@code conjugate(verbWord, "1SPr")} — string-form options. */
    public static String conjugate(String verbWord, String args) {
        throw notPorted("conjugate");
    }

    public static String conjugate(String verbWord) {
        throw notPorted("conjugate");
    }

    /** JS {@code conjugate()} — undefined input throws. */
    public static String conjugate() {
        throw notPorted("conjugate");
    }

    public static String stresses(String input, Map<String, Object> options) {
        throw notPorted("stresses");
    }

    public static String stresses(String input) {
        throw notPorted("stresses");
    }

    public static String syllables(String input, Map<String, Object> options) {
        throw notPorted("syllables");
    }

    public static String syllables(String input) {
        throw notPorted("syllables");
    }

    public static String phones(String input, Map<String, Object> options) {
        throw notPorted("phones");
    }

    public static String phones(String input) {
        throw notPorted("phones");
    }

    public static Analysis analyze(String input, Map<String, Object> options) {
        throw notPorted("analyze");
    }

    public static Analysis analyze(String input) {
        throw notPorted("analyze");
    }

    public static List<String> spellsLikeSync(String word, Map<String, Object> options) {
        throw notPorted("spellsLikeSync");
    }

    public static List<String> soundsLikeSync(String word, Map<String, Object> options) {
        throw notPorted("soundsLikeSync");
    }

    public static List<String> rhymesSync(String word, Map<String, Object> options) {
        throw notPorted("rhymesSync");
    }

    public static List<String> searchSync(Object pattern, Map<String, Object> options) {
        throw notPorted("searchSync");
    }

    public static List<String> alliterationsSync(String word, Map<String, Object> options) {
        throw notPorted("alliterationsSync");
    }

    public static int randi(int param1) {
        throw notPorted("randi");
    }

    public static int randi(int param1, int param2) {
        throw notPorted("randi");
    }

    public static double random() {
        throw notPorted("random");
    }

    public static int random(int param1) {
        throw notPorted("random");
    }

    public static int random(int param1, int param2) {
        throw notPorted("random");
    }

    /**
     * Stemming utilities, exposed as {@code RiTa.Stemmer} for parity with the JS API.
     */
    public static final class Stemmer {

        private Stemmer() {
        }

        public static String[] stemAll(String[] words) {
            throw notPorted("Stemmer.stemAll");
        }
    }

    /**
     * The result of {@link #analyze(String, Map)}: parallel feature strings for the input.
     * Mirrors the JS object, where {@code pos} and {@code tokens} are space-joined strings.
     */
    public static final class Analysis {
        public String tokens;
        public String pos;
        public String stresses;
        public String phones;
        public String syllables;

        /** The features as a map, for equality against a JS-style object literal. */
        public Map<String, String> toMap() {
            Map<String, String> m = new java.util.LinkedHashMap<>();
            m.put("tokens", tokens);
            m.put("pos", pos);
            m.put("stresses", stresses);
            m.put("phones", phones);
            m.put("syllables", syllables);
            return m;
        }
    }

    static UnsupportedOperationException notPorted(String name) {
        return new UnsupportedOperationException("RiTa." + name + " not yet ported from js/src");
    }
}
