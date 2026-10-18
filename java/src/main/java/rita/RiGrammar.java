package rita;

import java.util.Map;

/**
 * Grammar engine — stub for the {@code riscript} RiGrammar. Methods throw until ported.
 */
public class RiGrammar {

    public RiGrammar() {
        throw RiTa.notPorted("RiGrammar.constructor");
    }

    public RiGrammar(Object rules) {
        throw RiTa.notPorted("RiGrammar.constructor");
    }

    public RiGrammar(Object rules, Map<String, Object> context) {
        throw RiTa.notPorted("RiGrammar.constructor");
    }

    public static RiGrammar fromJSON(String json) {
        throw RiTa.notPorted("RiGrammar.fromJSON");
    }

    /** The grammar's rules as a nested map (mirrors the JS toJSON object). */
    public Map<String, Object> toJSON() {
        throw RiTa.notPorted("RiGrammar.toJSON");
    }

    public String expand() {
        throw RiTa.notPorted("RiGrammar.expand");
    }

    public String expand(Map<String, Object> context) {
        throw RiTa.notPorted("RiGrammar.expand");
    }

    public void addRule(String name, String rule) {
        throw RiTa.notPorted("RiGrammar.addRule");
    }

    public void removeRule(String name) {
        throw RiTa.notPorted("RiGrammar.removeRule");
    }
}
