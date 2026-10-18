package rita;

import java.util.Map;
import java.util.Set;

/**
 * RiScript engine — stub for the {@code riscript} package. Methods throw until ported.
 */
public class RiScript {

    /** Registered transform functions, keyed by name. */
    public final Map<String, Object> transforms = new java.util.HashMap<>();

    public String evaluate(String script, Map<String, Object> context) {
        throw RiTa.notPorted("riscript.evaluate");
    }

    public String evaluate(String script, Map<String, Object> context, Map<String, Object> options) {
        throw RiTa.notPorted("riscript.evaluate");
    }

    public void addTransform(String name, Object definition) {
        throw RiTa.notPorted("riscript.addTransform");
    }

    public void removeTransform(String name) {
        transforms.remove(name);
    }

    public Set<String> getTransforms() {
        return transforms.keySet();
    }
}
