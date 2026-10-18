package rita;

import java.util.Map;

/**
 * Tokenizer — stub for {@code js/src/tokenizer.js}. Methods throw until ported.
 */
public class Tokenizer {

    public String[] tokens(String text, Map<String, Object> options) {
        throw RiTa.notPorted("tokenizer.tokens");
    }

    public String[] tokenize(String input, Map<String, Object> options) {
        throw RiTa.notPorted("tokenizer.tokenize");
    }

    public String untokenize(String[] input, String delim) {
        throw RiTa.notPorted("tokenizer.untokenize");
    }

    public String[] sentences(String text, String pattern) {
        throw RiTa.notPorted("tokenizer.sentences");
    }
}
