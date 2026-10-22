package rita;

import java.util.Map;
import java.util.regex.Pattern;

/**
 * Word inflector — port of {@code js/src/inflector.js}.
 *
 * <p>The singular/plural rule sets and the isPlural test regexes live in {@link InflectorData},
 * generated from the JS source.
 */
public class Inflector {

    private static final int PLUR = 1;
    private static final int SING = 2;

    /** Compiled isPlural test regexes (raw patterns, unanchored search). */
    private static final Pattern[] IS_PLURAL = compileAll(InflectorData.IS_PLURAL_RULES);

    public String singularize(String word) {
        return singularize(word, Map.of());
    }

    public String singularize(String word, Map<String, Object> options) {
        return adjustNumber(word, SING);
    }

    /** JS {@code singularize()} — undefined input yields the empty string. */
    public String singularize() {
        return "";
    }

    public String pluralize(String word) {
        return pluralize(word, Map.of());
    }

    public String pluralize(String word, Map<String, Object> options) {
        if (isPlural(word, options)) {
            return word;
        }
        return adjustNumber(word, PLUR);
    }

    /** JS {@code pluralize()} — undefined input yields the empty string. */
    public String pluralize() {
        return "";
    }

    public boolean isPlural(String word) {
        return isPlural(word, Map.of());
    }

    /** JS {@code isPlural(word, opts)}. */
    public boolean isPlural(String word, Map<String, Object> options) {
        if (word == null || word.isEmpty()) {
            return false;
        }
        word = word.toLowerCase();

        if (RiTa.lexicon.isMassNoun(word)) {
            return true;
        }

        for (Pattern rule : IS_PLURAL) {
            if (rule.matcher(word).find()) {
                return true;
            }
        }

        // A general modal form? (for example, ends in 'ness')
        if (find(word, "([a-z]+ness)$")) {
            // JS checks !RiTa.MODAL_EXCEPTIONS.includes(word); MODAL_EXCEPTIONS is undefined and
            // this branch is unreachable because isMassNoun already returns true for any -ness word.
            return true;
        }

        String sing = singularize(word, options);

        // Is the singularized form different?
        if (!sing.equals(word)) {
            if (word.endsWith("ae") && word.equals(sing + "e")) {
                return true;
            }
            // Is it in the lexicon as 'nn' (with noGuessing)?
            if (RiTa.tagger.allTagsList(sing, Map.of("noGuessing", true)).contains("nn")) {
                return true;
            }
        }

        return false;
    }

    /** JS {@code isPlural()} — undefined input is not plural. */
    public boolean isPlural() {
        return false;
    }

    // ---- internals --------------------------------------------------------------------

    private String adjustNumber(String word, int type) {
        if (word == null) {
            return "";
        }
        word = word.trim();
        if (word.isEmpty()) {
            return "";
        }

        String check = word.toLowerCase();
        if (RiTa.lexicon.isMassNoun(check)) {
            return word;
        }

        RE[] rules = (type == SING) ? InflectorData.SING_RULES : InflectorData.PLUR_RULES;
        for (RE rule : rules) {
            if (rule.applies(check)) {
                return rule.fire(word);
            }
        }
        return word;
    }

    private static Pattern[] compileAll(String[] regexes) {
        Pattern[] out = new Pattern[regexes.length];
        for (int i = 0; i < regexes.length; i++) {
            out[i] = Pattern.compile(regexes[i]);
        }
        return out;
    }

    private static boolean find(String word, String regex) {
        return Pattern.compile(regex).matcher(word).find();
    }
}
