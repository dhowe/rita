package rita;

import java.util.regex.Pattern;

/**
 * A regex + truncation rule — port of the {@code RE} class in {@code js/src/util.js}.
 *
 * <p>Used by the inflector to express singularize/pluralize rules as
 * {@code RE(pattern, offset, suffix)}: if {@link #applies(String)} matches, the word is truncated
 * by {@code offset} characters and {@code suffix} is appended.
 */
public class RE {

    public final String raw;
    public final Pattern regex;
    public final int offset;
    public final String suffix;

    public RE(String regex, int offset, String suffix) {
        this.raw = regex;
        this.regex = Pattern.compile(regex);
        this.offset = offset;
        this.suffix = (suffix == null) ? "" : suffix;
    }

    /** JS {@code this.regex.test(word)} — an unanchored search. */
    public boolean applies(String word) {
        return regex.matcher(word).find();
    }

    /** JS {@code truncate(word) + suffix}. */
    public String fire(String word) {
        return truncate(word) + suffix;
    }

    /** JS {@code word.substr(0, word.length - offset)} (clamps to "" when offset >= length). */
    public String truncate(String word) {
        if (offset == 0) {
            return word;
        }
        int end = word.length() - offset;
        return end <= 0 ? "" : word.substring(0, end);
    }

    @Override
    public String toString() {
        return "/" + raw + "/";
    }
}
