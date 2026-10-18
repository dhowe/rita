package rita;

import java.util.Map;

/**
 * Word inflector — stub for {@code js/src/inflector.js}. Methods throw until ported.
 */
public class Inflector {

    public String singularize(String word) {
        throw RiTa.notPorted("inflector.singularize");
    }

    public String pluralize(String word) {
        throw RiTa.notPorted("inflector.pluralize");
    }

    public boolean isPlural(String word, Map<String, Object> options) {
        throw RiTa.notPorted("inflector.isPlural");
    }

    public boolean isPlural(String word) {
        throw RiTa.notPorted("inflector.isPlural");
    }

    /** JS {@code isPlural()} — undefined input is not plural. */
    public boolean isPlural() {
        throw RiTa.notPorted("inflector.isPlural");
    }
}
