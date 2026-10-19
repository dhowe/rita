package rita;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Grammar engine — a probabilistic context-free grammar over RiScript rules,
 * ported from the JS {@code RiGrammar} (and the Python reference).
 *
 * <p>Rules are dynamic by default; a {@code #} prefix makes a rule static. Expanding a
 * grammar compiles the rules into inline RiScript assignments and evaluates them.
 */
public class RiGrammar {

    /** The grammar's rules, in insertion order. */
    public final Map<String, Object> rules = new LinkedHashMap<>();

    /** The context (world-state) used during expansion. */
    public final Map<String, Object> context;

    private final RiScript scripting;

    public RiGrammar() {
        this(null, null);
    }

    public RiGrammar(Object rules) {
        this(rules, null);
    }

    public RiGrammar(Object rules, Map<String, Object> context) {
        this.context = context == null ? new LinkedHashMap<>() : context;
        this.scripting = new RiScript();
        if (rules == null) {
            return;
        }
        Object parsed = rules instanceof String ? parseJson((String) rules) : rules;
        if (!(parsed instanceof Map)) {
            throw new IllegalArgumentException("RiGrammar: expecting object, found "
                + (parsed == null ? "null" : parsed.getClass().getSimpleName()));
        }
        setRules(parsed);
    }

    public static RiGrammar fromJSON(String json) {
        return new RiGrammar(parseJson(json), null);
    }

    public static RiGrammar fromJSON(String json, Map<String, Object> context) {
        return new RiGrammar(parseJson(json), context);
    }

    /** Static one-shot expansion: build a grammar from {@code rules} and expand it. */
    public static String expand(Object rules, Map<String, Object> context, Map<String, Object> options) {
        return new RiGrammar(rules, context).expand(options);
    }

    // ── rules ───────────────────────────────────────────────────────────────────

    public RiGrammar addRule(String name, Object def) {
        if (name == null || name.isEmpty()) {
            throw new IllegalArgumentException("expected [string] name");
        }
        if (def == null) {
            throw new IllegalArgumentException("undefined rule def: " + name);
        }
        if (name.startsWith("$")) {
            throw new IllegalArgumentException("Grammar rules are dynamic by default; if you need a static rule, use '"
                + name.substring(1) + "' with a leading #, otherwise just use '" + name.substring(1) + "'.");
        }
        String bare = name.startsWith("#") ? name.substring(1) : name;
        if (!bare.matches("[A-Za-z_0-9]+")) {
            throw new IllegalArgumentException("invalid rule name: \"" + name + "\"");
        }
        rules.put(name, def);
        return this;
    }

    public RiGrammar setRules(Object rules) {
        if (rules == null) {
            throw new IllegalArgumentException("undefined rules");
        }
        Object incoming = rules instanceof String ? parseJson((String) rules) : rules;
        this.rules.clear();
        if (incoming instanceof Map) {
            for (Map.Entry<?, ?> e : ((Map<?, ?>) incoming).entrySet()) {
                addRule(String.valueOf(e.getKey()), e.getValue());
            }
        }
        return this;
    }

    public RiGrammar removeRule(String name) {
        if (name != null && !name.startsWith("$")) {
            rules.remove(name);
        }
        return this;
    }

    /** The rules as a nested map (mirrors the JS {@code toJSON} object). */
    public Map<String, Object> toJSON() {
        return rules;
    }

    public String toJSONString() {
        return Json.write(rules);
    }

    @Override
    public String toString() {
        return toJSONString();
    }

    public boolean equals(RiGrammar other) {
        return other != null && other.toJSONString().equals(this.toJSONString());
    }

    // ── transforms (delegate to the scripting engine) ───────────────────────────

    public RiGrammar addTransform(String name, Object def) {
        scripting.addTransform(name, def);
        return this;
    }

    public RiGrammar removeTransform(String name) {
        scripting.removeTransform(name);
        return this;
    }

    public java.util.Set<String> getTransforms() {
        return scripting.getTransforms();
    }

    // ── expansion ───────────────────────────────────────────────────────────────

    public String expand() {
        return expand(null);
    }

    public String expand(Map<String, Object> options) {
        Map<String, Object> opts = options == null ? Map.of() : options;
        if (opts.containsKey("context")) {
            throw new IllegalArgumentException("pass context to RiTa.grammar() or new RiGrammar() instead");
        }
        String start = opts.get("start") == null ? "start" : String.valueOf(opts.get("start"));
        if (start.startsWith("$")) {
            start = start.substring(1);
        }
        if (start.startsWith("#")) {
            start = start.substring(1);
        }
        if (!rules.containsKey(start) && !rules.containsKey("#" + start)) {
            throw new IllegalArgumentException("Rule: \"" + start + "\" not found in grammar");
        }
        String script = toScript(start);
        RiScript.EvalVisitor visitor = scripting.new EvalVisitor(context, scripting.transforms);
        return scripting.evaluateWithVisitor(script, visitor, opts);
    }

    /** Compile the rules into a self-contained RiScript program ending in {@code $start}. */
    String toScript(String start) {
        List<String> lines = new ArrayList<>();
        for (Map.Entry<String, Object> e : rules.entrySet()) {
            String name = e.getKey();
            String rule = ruleText(e.getValue());
            if (name.startsWith("$")) {
                name = name.substring(1);
            }
            if (!name.startsWith("#")) {
                name = "$" + name;
            }
            if (!needsNoWrap(rule)) {
                rule = "[" + rule + "]";
            }
            lines.add(name + "=" + rule);
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < lines.size(); i++) {
            if (i > 0) {
                sb.append('\n');
            }
            sb.append(lines.get(i));
        }
        sb.append('\n').append('$').append(start);
        return sb.toString();
    }

    /** True if {@code rule} is already a single balanced {@code [...]} choice. */
    static boolean needsNoWrap(String rule) {
        String s = rule.strip();
        if (!s.startsWith("[") || !s.endsWith("]")) {
            return false;
        }
        int depth = 0;
        int closePos = -1;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '[') {
                depth++;
            } else if (c == ']') {
                depth--;
                if (depth == 0) {
                    closePos = i;
                    break;
                }
            }
        }
        return closePos == s.length() - 1;
    }

    private static String ruleText(Object rule) {
        if (rule instanceof List) {
            List<String> parts = new ArrayList<>();
            for (Object o : (List<?>) rule) {
                parts.add(String.valueOf(o));
            }
            return String.join(" | ", parts);
        }
        return String.valueOf(rule);
    }

    private static Object parseJson(String json) {
        try {
            return Json.parse(json);
        } catch (Exception e) {
            throw new IllegalArgumentException(
                "RiGrammar appears to be invalid JSON, please check it at http://jsonlint.com/\n" + json, e);
        }
    }
}
