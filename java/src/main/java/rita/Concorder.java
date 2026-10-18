package rita;

import java.util.List;
import java.util.Map;

/**
 * Key-Word-In-Context concordance — stub for {@code js/src/concorder.js}. Methods throw until ported.
 */
public class Concorder {

    public List<String> kwic(String keyword, Map<String, Object> options) {
        throw RiTa.notPorted("concorder.kwic");
    }

    public Map<String, Integer> concordance(String text, Map<String, Object> options) {
        throw RiTa.notPorted("concorder.concordance");
    }
}
