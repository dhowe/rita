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

    /** JS {@code ONLY_PUNCT} — matches a string of only punctuation characters. */
    private static final java.util.regex.Pattern ONLY_PUNCT =
        java.util.regex.Pattern.compile("^[\\p{IsPunctuation}|+,<>^$\ufffd`]*$");

    /** JS {@code IS_LETTER} — matches one or more ASCII/latin letters. */
    private static final java.util.regex.Pattern IS_LETTER =
        java.util.regex.Pattern.compile("^[a-z\\u00C0-\\u00ff]+$");

    public static final String[] PHONES = {"aa", "ae", "ah", "ao", "aw", "ay", "b", "ch", "d", "dh", "eh", "er", "ey", "f", "g", "hh", "ih", "iy", "jh", "k", "l", "m", "n", "ng", "ow", "oy", "p", "r", "s", "sh", "t", "th", "uh", "uw", "v", "w", "y", "z", "zh"};
    public static final String[] ABRV = {"Adm.", "Capt.", "Cmdr.", "Col.", "Dr.", "Gen.", "Gov.", "Lt.", "Maj.", "Messrs.", "Mr.", "Mrs.", "Ms.", "Prof.", "Rep.", "Reps.", "Rev.", "Sen.", "Sens.", "Sgt.", "Sr.", "St.", "A.k.a.", "C.f.", "I.e.", "E.g.", "Vs.", "V.", "Jan.", "Feb.", "Mar.", "Apr.", "Mar.", "Jun.", "Jul.", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."};
    public static List<String> QUESTIONS = new java.util.ArrayList<>(List.of("was", "what", "when", "where", "which", "why", "who", "will", "would", "who", "how", "if", "is", "could", "might", "does", "are", "have"));
    public static List<String> STOP_WORDS = new java.util.ArrayList<>(List.of("and", "a", "of", "in", "i", "you", "is", "to", "that", "it", "for", "on", "have", "with", "this", "be", "not", "are", "as", "was", "but", "or", "from", "my", "at", "if", "they", "your", "all", "he", "by", "one", "me", "what", "so", "can", "will", "do", "an", "about", "we", "just", "would", "there", "no", "like", "out", "his", "has", "up", "more", "who", "when", "don't", "some", "had", "them", "any", "their", "it's", "only", "which", "i'm", "been", "other", "were", "how", "then", "now", "her", "than", "she", "well", "also", "us", "very", "because", "am", "here", "could", "even", "him", "into", "our", "much", "too", "did", "should", "over", "want", "these", "may", "where", "most", "many", "those", "does", "why", "please", "off", "going", "its", "i've", "down", "that's", "can't", "you're", "didn't", "another", "around", "must", "few", "doesn't", "the", "every", "yes", "each", "maybe", "i'll", "away", "doing", "oh", "else", "isn't", "he's", "there's", "hi", "won't", "ok", "they're", "yeah", "mine", "we're", "what's", "shall", "she's", "hello", "okay", "here's", "less", "didn't", "said", "over", "this", "that", "just", "then", "under", "some"));
    public static List<String> MASS_NOUNS = new java.util.ArrayList<>(List.of("abalone", "asbestos", "barracks", "bathos", "breeches", "beef", "britches", "chaos", "chinese", "cognoscenti", "clippers", "corps", "cosmos", "crossroads", "diabetes", "ethos", "gallows", "graffiti", "herpes", "innings", "lens", "means", "measles", "mews", "mumps", "news", "pasta", "pathos", "pincers", "pliers", "proceedings", "rabies", "rhinoceros", "sassafras", "scissors", "series", "shears", "species", "tuna", "acoustics", "aesthetics", "aquatics", "basics", "ceramics", "classics", "cosmetics", "dialectics", "deer", "dynamics", "ethics", "harmonics", "heroics", "mechanics", "metrics", "ooze", "optics", "physics", "polemics", "pyrotechnics", "statistics", "tactics", "tropics", "bengalese", "bengali", "bonsai", "booze", "cellulose", "mess", "moose", "burmese", "chinese", "colossus", "congolese", "discus", "electrolysis", "emphasis", "expertise", "flu", "fructose", "gauze", "glucose", "grease", "guyanese", "haze", "incense", "japanese", "lebanese", "malaise", "mayonnaise", "maltese", "music", "money", "menopause", "merchandise", "olympics", "overuse", "paradise", "poise", "potash", "portuguese", "prose", "recompense", "remorse", "repose", "senegalese", "siamese", "singhalese", "sleaze", "sioux", "sudanese", "suspense", "swiss", "taiwanese", "vietnamese", "unease", "aircraft", "anise", "antifreeze", "applause", "archdiocese", "apparatus", "asparagus", "bellows", "bison", "bluefish", "bourgeois", "bream", "brill", "butterfingers", "cargo", "carp", "catfish", "chassis", "clone", "clones", "clothes", "chub", "cod", "codfish", "coley", "contretemps", "crawfish", "crayfish", "cuttlefish", "dice", "dogfish", "doings", "dory", "downstairs", "eldest", "earnings", "economics", "electronics", "firstborn", "fish", "flatfish", "flounder", "fowl", "fry", "fries", "works", "goldfish", "golf", "grand", "grief", "haddock", "hake", "halibut", "headquarters", "herring", "hertz", "honey", "horsepower", "goods", "hovercraft", "ironworks", "kilohertz", "ling", "shrimp", "swine", "lungfish", "mackerel", "macaroni", "megahertz", "moorfowl", "moorgame", "mullet", "myrrh", "nepalese", "offspring", "pants", "patois", "pekinese", "perch", "pickerel", "pike", "potpourri", "precis", "quid", "rand", "rendezvous", "roach", "salmon", "samurai", "seychelles", "shad", "sheep", "shellfish", "smelt", "spaghetti", "spacecraft", "starfish", "stockfish", "sunfish", "superficies", "sweepstakes", "smallpox", "swordfish", "tennis", "tobacco", "triceps", "trout", "tunafish", "turbot", "trousers", "turf", "dibs", "undersigned", "waterfowl", "waterworks", "waxworks", "wildfowl", "woodworm", "yen", "aries", "pisces", "forceps", "jeans", "mathematics", "odds", "politics", "remains", "aids", "wildlife", "shall", "would", "may", "might", "ought", "should", "acne", "admiration", "advice", "air", "anger", "anticipation", "assistance", "awareness", "bacon", "baggage", "blood", "bravery", "chess", "clay", "clothing", "coal", "compliance", "comprehension", "confusion", "consciousness", "cream", "darkness", "diligence", "dust", "education", "empathy", "enthusiasm", "envy", "equality", "equipment", "evidence", "feedback", "fitness", "flattery", "foliage", "fun", "furniture", "garbage", "gold", "gossip", "grammar", "gratitude", "gravel", "guilt", "happiness", "hardware", "hate", "hay", "health", "heat", "help", "hesitation", "homework", "honesty", "honor", "honour", "hospitality", "hostility", "humanity", "humility", "ice", "immortality", "independence", "information", "integrity", "intimidation", "jargon", "jealousy", "jewelry", "justice", "knowledge", "literacy", "logic", "luck", "lumber", "luggage", "mail", "management", "milk", "morale", "mud", "nonsense", "oppression", "optimism", "oxygen", "participation", "pay", "peace", "perseverance", "pessimism", "pneumonia", "poetry", "police", "pride", "privacy", "propaganda", "public", "punctuation", "recovery", "rice", "rust", "satisfaction", "schnapps", "shame", "slang", "software", "stamina", "starvation", "steam", "steel", "stuff", "support", "sweat", "thunder", "timber", "toil", "traffic", "tongs", "training", "trash", "valor", "vehemence", "violence", "warmth", "waste", "weather", "wheat", "wisdom", "work", "accommodation", "advertising", "aid", "art", "bread", "business", "butter", "calm", "cash", "cheese", "childhood", "clothing ", "coffee", "content", "corruption", "courage", "currency", "damage", "danger", "determination", "electricity", "employment", "energy", "entertainment", "failure", "fame", "fire", "flour", "food", "freedom", "friendship", "fuel", "genetics", "hair", "harm", "hospitality ", "housework", "humour", "imagination", "importance", "innocence", "intelligence", "juice", "kindness", "labour", "lack", "laughter", "leisure", "literature", "litter", "love", "magic", "metal", "motherhood", "motivation", "nature", "nutrition", "obesity", "oil", "old age", "paper", "patience", "permission", "pollution", "poverty", "power", "production", "progress", "pronunciation", "publicity", "quality", "quantity", "racism", "rain", "relaxation", "research", "respect", "room (space)", "rubbish", "safety", "salt", "sand", "seafood", "shopping", "silence", "smoke", "snow", "soup", "speed", "spelling", "stress ", "sugar", "sunshine", "tea", "time", "tolerance", "trade", "transportation", "travel", "trust", "understanding", "unemployment", "usage", "vision", "water", "wealth", "weight", "welfare", "width", "wood", "yoga", "youth", "homecare", "childcare", "fanfare", "healthcare", "medicare"));

    // Set mirrors (rebuilt lazily when the source list changes, mirroring JS createSetMirror).
    public static final Set<String> STOP_WORDS_SET = new MirrorSet(() -> STOP_WORDS);
    public static final Set<String> MASS_NOUNS_SET = new MirrorSet(() -> MASS_NOUNS);
    public static final Set<String> QUESTIONS_SET = new MirrorSet(() -> QUESTIONS);

    /**
     * A live view over a mutable list, mirroring the JS {@code createSetMirror} getter: the
     * backing set is rebuilt whenever the source list is reassigned or its length changes.
     */
    static final class MirrorSet extends java.util.AbstractSet<String> {
        private final java.util.function.Supplier<List<String>> getArray;
        private List<String> ref;
        private int len;
        private Set<String> set;

        MirrorSet(java.util.function.Supplier<List<String>> getArray) {
            this.getArray = getArray;
            this.ref = getArray.get();
            this.len = ref.size();
            this.set = new java.util.LinkedHashSet<>(ref);
        }

        private Set<String> sync() {
            List<String> arr = getArray.get();
            if (arr != ref || arr.size() != len) {
                ref = arr;
                len = arr.size();
                set = new java.util.LinkedHashSet<>(arr);
            }
            return set;
        }

        @Override
        public java.util.Iterator<String> iterator() {
            return sync().iterator();
        }

        @Override
        public int size() {
            return sync().size();
        }

        @Override
        public boolean contains(Object o) {
            return sync().contains(o);
        }
    }

    // ---- static methods -------------------------------------------------------------

    public static RiGrammar grammar() {
        return new RiGrammar();
    }

    public static RiGrammar grammar(Object rules) {
        return new RiGrammar(rules);
    }

    public static RiGrammar grammar(Object rules, Map<String, Object> context) {
        return new RiGrammar(rules, context);
    }

    public static void addTransform(String name, Object definition) {
        riscript.addTransform(name, definition);
    }

    public static void removeTransform(String name) {
        riscript.removeTransform(name);
    }

    public static Set<String> getTransforms() {
        return riscript.getTransforms();
    }

    public static String articlize(String word) {
        if (word == null || word.isEmpty()) {
            return "";
        }
        String first = word.split("\\s+")[0];
        // JS: phones(first,{silent:true}) → "an " iff the first phone char is a vowel, else "a ".
        String ph = phones(first, Map.of("silent", true));
        boolean vowel = ph != null && !ph.isEmpty() && VOWELS.indexOf(ph.charAt(0)) >= 0;
        return (vowel ? "an " : "a ") + word;
    }

    public static String evaluate(String script) {
        return riscript.evaluate(script);
    }

    /** JS {@code evaluate(script, context)} — context may be a Map or a falsy scalar (e.g. 0). */
    public static String evaluate(String script, Object context) {
        return riscript.evaluate(script, context);
    }

    public static String evaluate(String script, Object context, Map<String, Object> options) {
        return riscript.evaluate(script, context, options);
    }

    public static RiMarkov markov(int n) {
        return new RiMarkov(n);
    }

    public static RiMarkov markov(int n, Map<String, Object> options) {
        return new RiMarkov(n, options);
    }

    public static List<String> kwic(String keyword, Map<String, Object> options) {
        return concorder.kwic(keyword, options);
    }

    /** JS {@code kwic("cat")} — keyword with no options. */
    public static List<String> kwic(String keyword) {
        return concorder.kwic(keyword, (Object) null);
    }

    /** JS {@code kwic("cat", 4)} — number of context words. */
    public static List<String> kwic(String keyword, int numWords) {
        return concorder.kwic(keyword, (Object) numWords);
    }

    public static Map<String, Integer> concordance(String text, Map<String, Object> options) {
        return concorder.concordance((Object) text, options);
    }

    /** JS {@code concordance(text)} — text with no options. */
    public static Map<String, Integer> concordance(String text) {
        return concorder.concordance((Object) text, null);
    }

    /** JS {@code concordance()} — undefined text throws. */
    public static Map<String, Integer> concordance() {
        return concorder.concordance((Object) null, null);
    }

    public static int[] randomOrdering(int k) {
        return randomizer.randomOrdering(k);
    }

    public static <T> List<T> randomOrdering(List<T> array) {
        return randomizer.randomOrdering(array);
    }

    public static void randomSeed(int seed) {
        randomizer.seed(seed);
    }

    public static boolean isQuestion(String sentence) {
        String[] toks = tokenize(sentence);
        return toks.length > 0 && QUESTIONS_SET.contains(toks[0].toLowerCase());
    }

    public static boolean isVowel(String charOrWord) {
        return charOrWord != null && charOrWord.length() == 1
            && VOWELS.contains(charOrWord.toLowerCase());
    }

    public static boolean isConsonant(String charOrWord) {
        return charOrWord != null && charOrWord.length() == 1
            && !VOWELS.contains(charOrWord.toLowerCase())
            && IS_LETTER.matcher(charOrWord.toLowerCase()).matches();
    }

    public static String capitalize(String string) {
        return string == null || string.isEmpty() ? "" : string.substring(0, 1).toUpperCase() + string.substring(1);
    }

    public static String randomWord(Object pattern, Map<String, Object> options) {
        return lexicon.randomWord(pattern, options);
    }

    /** JS {@code randomWord("^a")} — a pattern string with no options. */
    public static String randomWord(String pattern) {
        return lexicon.randomWord(pattern, null);
    }

    /** JS {@code randomWord({ pos: "nn" })} — options only. */
    public static String randomWord(Map<String, Object> options) {
        return lexicon.randomWord(null, options);
    }

    public static String randomWord() {
        return lexicon.randomWord(null, null);
    }

    public static List<String> rhymes(String word, Map<String, Object> options) {
        return lexicon.rhymesSync(word, options);
    }

    public static List<String> rhymes(String word, int limit) {
        Map<String, Object> opts = new java.util.LinkedHashMap<>();
        opts.put("limit", limit);
        return lexicon.rhymesSync(word, opts);
    }

    public static boolean isRhyme(String word1, String word2) {
        return lexicon.isRhyme(word1, word2);
    }

    public static List<String> alliterations(String word, Map<String, Object> options) {
        return lexicon.alliterationsSync(word, options);
    }

    public static boolean hasWord(String word, Map<String, Object> options) {
        return lexicon.hasWord(word, options);
    }

    public static boolean hasWord(String word) {
        return lexicon.hasWord(word, Map.of());
    }

    public static boolean isAbbrev(String input, Map<String, Object> options) {
        if (input == null) {
            return false;
        }
        if (options != null && truthy(options.get("caseSensitive"))) {
            String trimmed = input.trim();
            for (String a : ABRV) {
                if (a.equals(trimmed)) {
                    return true;
                }
            }
            return false;
        }
        String check = input.trim().toLowerCase();
        for (String a : ABRV) {
            if (a.toLowerCase().equals(check)) {
                return true;
            }
        }
        return false;
    }

    public static boolean isAbbrev(String input) {
        return isAbbrev(input, Map.of());
    }

    public static boolean isAlliteration(String word1, String word2) {
        return lexicon.isAlliteration(word1, word2);
    }

    public static List<String> spellsLike(String word, Map<String, Object> options) {
        return lexicon.spellsLikeSync(word, options);
    }

    public static List<String> soundsLike(String word, Map<String, Object> options) {
        return lexicon.soundsLikeSync(word, options);
    }

    public static String[] pos(String word, Map<String, Object> options) {
        if (options != null && options.containsKey("inline")) {
            throw new RuntimeException("Use RiTa.posInline() instead");
        }
        return (String[]) tagger.tag(word, options);
    }

    public static String[] pos(String word) {
        return (String[]) tagger.tag(word, Map.of());
    }

    public static String[] pos(String[] words) {
        return (String[]) tagger.tag(words, Map.of());
    }

    public static String[] pos(String[] words, Map<String, Object> options) {
        if (options != null && options.containsKey("inline")) {
            throw new RuntimeException("Use RiTa.posInline() instead");
        }
        return (String[]) tagger.tag(words, options);
    }

    public static boolean isNoun(String word) {
        return tagger.isNoun(word);
    }

    /** JS {@code isNoun()} — undefined is not a noun. */
    public static boolean isNoun() {
        return false;
    }

    public static boolean isAdjective(String word) {
        return tagger.isAdjective(word);
    }

    public static boolean isAdjective() {
        return false;
    }

    public static boolean isAdverb(String word) {
        return tagger.isAdverb(word);
    }

    public static boolean isAdverb() {
        return false;
    }

    public static boolean isVerb(String word) {
        return tagger.isVerb(word, Map.of());
    }

    public static boolean isVerb() {
        return false;
    }

    public static boolean isPunct(String text) {
        return text != null && !text.isEmpty() && ONLY_PUNCT.matcher(text).matches();
    }

    public static String posInline(String sentence, Map<String, Object> options) {
        Map<String, Object> opts = new java.util.LinkedHashMap<>(options == null ? Map.of() : options);
        opts.put("inline", true);
        return (String) tagger.tag(sentence, opts);
    }

    public static String posInline(String sentence) {
        return (String) tagger.tag(sentence, Map.of("inline", true));
    }

    public static String posInline(String[] words) {
        return (String) tagger.tag(words, Map.of("inline", true));
    }

    public static String posInline(String[] words, Map<String, Object> options) {
        Map<String, Object> opts = new java.util.LinkedHashMap<>(options == null ? Map.of() : options);
        opts.put("inline", true);
        return (String) tagger.tag(words, opts);
    }

    public static String singularize(String word) {
        return inflector.singularize(word);
    }

    public static String singularize(String word, Map<String, Object> options) {
        return inflector.singularize(word, options);
    }

    /** JS {@code RiTa.singularize()} — undefined input yields the empty string. */
    public static String singularize() {
        return "";
    }

    public static String pluralize(String word) {
        return inflector.pluralize(word);
    }

    public static String pluralize(String word, Map<String, Object> options) {
        return inflector.pluralize(word, options);
    }

    /** JS {@code RiTa.pluralize()} — undefined input yields the empty string. */
    public static String pluralize() {
        return "";
    }

    public static List<String> search(Object pattern, Map<String, Object> options) {
        return lexicon.searchSync(pattern, options);
    }

    /** JS {@code search("phant")} — a pattern string with no options. */
    public static List<String> search(String pattern) {
        return lexicon.searchSync(pattern, null);
    }

    public static List<String> search(Map<String, Object> options) {
        return lexicon.searchSync(null, options);
    }

    public static List<String> search() {
        return lexicon.searchSync(null, null);
    }

    public static String[] tokens(String text, Map<String, Object> options) {
        return tokenizer.tokens(text, options);
    }

    public static String[] tokens(String text) {
        return tokenizer.tokens(text, Map.of());
    }

    public static String[] tokenize(String input, Map<String, Object> options) {
        return tokenizer.tokenize(input, options);
    }

    public static String[] tokenize(String input) {
        return tokenizer.tokenize(input, Map.of());
    }

    public static String untokenize(String[] input, String delim) {
        return tokenizer.untokenize(input, delim);
    }

    public static String untokenize(String[] input) {
        return tokenizer.untokenize(input, " ");
    }

    public static String[] sentences(String text, String pattern) {
        return tokenizer.sentences(text, pattern);
    }

    public static String[] sentences(String text) {
        return tokenizer.sentences(text, null);
    }

    public static boolean isStopWord(String word) {
        return STOP_WORDS_SET.contains(word.toLowerCase());
    }

    public static String stem(String word) {
        return rita.Stemmer.stem(word);
    }

    public static boolean findStem(String word) {
        throw notPorted("findStem");
    }

    public static String presentPart(String verbWord) {
        return conjugator.presentPart(verbWord);
    }

    public static String pastPart(String verbWord) {
        return conjugator.pastPart(verbWord);
    }

    public static String conjugate(String verbWord, Map<String, Object> options) {
        return conjugator.conjugate(verbWord, options);
    }

    /** JS {@code conjugate(verbWord, "1SPr")} — string-form options. */
    public static String conjugate(String verbWord, String args) {
        return conjugator.conjugate(verbWord, args);
    }

    public static String conjugate(String verbWord) {
        return conjugator.conjugate(verbWord, (Map<String, Object>) null);
    }

    /** JS {@code conjugate()} — undefined input throws. */
    public static String conjugate() {
        return conjugator.conjugate();
    }

    public static String stresses(String input, Map<String, Object> options) {
        return analyzer.analyze(input, options).stresses;
    }

    public static String stresses(String input) {
        return analyzer.analyze(input, Map.of()).stresses;
    }

    public static String syllables(String input, Map<String, Object> options) {
        Analysis result = analyzer.analyze(input, options);
        if (options != null && truthy(options.get("ipaPhones"))) {
            return Analyzer.syllablesToIpa(result.syllables, result.stresses, true);
        }
        return result.syllables;
    }

    public static String syllables(String input) {
        return analyzer.analyze(input, Map.of()).syllables;
    }

    public static String phones(String input, Map<String, Object> options) {
        Analysis result = analyzer.analyze(input, options);
        if (options != null && truthy(options.get("ipaPhones"))) {
            return Analyzer.syllablesToIpa(result.syllables, result.stresses);
        }
        return result.phones;
    }

    public static String phones(String input) {
        return analyzer.analyze(input, Map.of()).phones;
    }

    public static Analysis analyze(String input, Map<String, Object> options) {
        Analysis result = analyzer.analyze(input, options);
        if (options != null && truthy(options.get("ipaPhones"))) {
            result.phones = Analyzer.syllablesToIpa(result.syllables, result.stresses);
        }
        return result;
    }

    public static Analysis analyze(String input) {
        return analyzer.analyze(input, Map.of());
    }

    public static List<String> spellsLikeSync(String word, Map<String, Object> options) {
        return lexicon.spellsLikeSync(word, options);
    }

    public static List<String> soundsLikeSync(String word, Map<String, Object> options) {
        return lexicon.soundsLikeSync(word, options);
    }

    public static List<String> rhymesSync(String word, Map<String, Object> options) {
        return lexicon.rhymesSync(word, options);
    }

    public static List<String> searchSync(Object pattern, Map<String, Object> options) {
        return lexicon.searchSync(pattern, options);
    }

    public static List<String> alliterationsSync(String word, Map<String, Object> options) {
        return lexicon.alliterationsSync(word, options);
    }

    public static int randi(int param1) {
        return (int) Math.floor(randomizer.random(param1));
    }

    /** JS {@code randi()} — no args returns 0. */
    public static int randi() {
        return (int) Math.floor(randomizer.random());
    }

    public static int randi(int param1, int param2) {
        return (int) Math.floor(randomizer.random(param1, param2));
    }

    public static double random() {
        return randomizer.random();
    }

    public static double random(int param1) {
        return randomizer.random(param1);
    }

    public static double random(int param1, int param2) {
        return randomizer.random(param1, param2);
    }

    /** JS {@code random(array)} — a random element of the list. */
    public static <T> T random(List<T> array) {
        return randomizer.random(array);
    }

    /**
     * Stemming utilities, exposed as {@code RiTa.Stemmer} for parity with the JS API.
     */
    public static final class Stemmer {

        private Stemmer() {
        }

        public static String[] stemAll(String[] words) {
            return rita.Stemmer.stemAll(words);
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

    /** JS truthiness for option values. */
    static boolean truthy(Object o) {
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
