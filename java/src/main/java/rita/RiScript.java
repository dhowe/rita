package rita;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * RiScript engine — a hand-rolled tokenizer, recursive-descent parser and
 * AST-walking evaluator, ported from the Python reference ({@code python/riscript.py}).
 *
 * <p>No ANTLR and no external grammar: the lexer mirrors {@code _TOKEN_PATTERNS}, the
 * parser mirrors the {@code Parser} class, and the evaluator mirrors {@code EvalVisitor}.
 */
public class RiScript {

    /** A transform function: takes the current value, returns the transformed value. */
    public interface Transform {
        Object apply(Object value);
    }

    /** A nullary thunk used for dynamic symbol bindings (re-evaluated on each access). */
    interface Thunk {
        Object get();
    }

    /** Random integer in {@code [0,k)}. */
    interface Rand {
        int apply(int k);
    }

    /** Registered transform functions, keyed by name (defaults plus user-added). */
    public final Map<String, Object> transforms = new LinkedHashMap<>();

    public RiScript() {
        transforms.put("quotify", (Transform) v -> quotify(str(v)));
        transforms.put("pluralize", (Transform) v -> RiTa.pluralize(str(v)));
        transforms.put("articlize", (Transform) v -> RiTa.articlize(str(v)));
        transforms.put("capitalize", (Transform) v -> capitalize(str(v)));
        transforms.put("uppercase", (Transform) v -> str(v).toUpperCase());
        transforms.put("norepeat", (Transform) v -> v);
        transforms.put("art", transforms.get("articlize"));
        transforms.put("nr", transforms.get("norepeat"));
        transforms.put("cap", transforms.get("capitalize"));
        transforms.put("ucf", transforms.get("capitalize"));
        transforms.put("uc", transforms.get("uppercase"));
        transforms.put("qq", transforms.get("quotify"));
        transforms.put("s", transforms.get("pluralize"));
    }

    // ── public API ──────────────────────────────────────────────────────────────

    public String evaluate(String script) {
        return evaluate(script, null, null);
    }

    public String evaluate(String script, Object context) {
        return evaluate(script, context, null);
    }

    /**
     * Evaluate a RiScript string. {@code context} may be a {@link Map} or any falsy
     * scalar (e.g. {@code 0}), which is treated as an empty context — mirroring the
     * JS {@code context || {}} idiom.
     */
    public String evaluate(String script, Object context, Map<String, Object> options) {
        if (script == null) {
            throw new IllegalArgumentException("evaluate() expects a string, got null");
        }
        EvalVisitor v = new EvalVisitor(asMap(context), transforms);
        v.randi = RiScript::randi;
        return evalPasses(script, v, options, true);
    }

    /** Low-level evaluate with a pre-built visitor (used by {@link RiGrammar}). */
    String evaluateWithVisitor(String script, EvalVisitor visitor, Map<String, Object> options) {
        return evalPasses(script, visitor, options, false);
    }

    public void addTransform(String name, Object definition) {
        transforms.put(name, definition);
    }

    public void removeTransform(String name) {
        transforms.remove(name);
    }

    public Set<String> getTransforms() {
        return transforms.keySet();
    }

    // ── evaluation loop ─────────────────────────────────────────────────────────

    private String evalPasses(String script, EvalVisitor visitor, Map<String, Object> options,
        boolean stripUnresolved) {
        Map<String, Object> opts = options == null ? Map.of() : options;
        boolean onepass = truthy(opts.get("onepass"));
        boolean silent = truthy(opts.get("silent"));

        boolean endsWithNewline = script.endsWith("\n");
        String expr = preParse(script);
        if (expr == null || expr.isEmpty()) {
            return "";
        }
        String last = null;
        for (int i = 0; i < 10; i++) {
            if (expr.equals(last)) {
                break;
            }
            last = expr;
            Object r = visitor.evaluate(expr);
            expr = r == null ? "" : (r instanceof String ? (String) r : String.valueOf(r));
            if (onepass || !isParseable(expr)) {
                break;
            }
        }
        if (stripUnresolved && !silent) {
            expr = STRIP_UNRESOLVED.matcher(expr).replaceAll("");
        }
        String result = postParse(expr);
        if (!endsWithNewline) {
            result = stripTrailingNewlines(result);
        } else if (!result.endsWith("\n")) {
            result = result + "\n";
        }
        return result;
    }

    // ── transforms ──────────────────────────────────────────────────────────────

    static String quotify(String s) {
        return "“" + (s == null ? "" : s) + "”";
    }

    static String capitalize(String s) {
        if (s == null || s.isEmpty()) {
            return "";
        }
        return Character.toUpperCase(s.charAt(0)) + s.substring(1);
    }

    // ── helpers ─────────────────────────────────────────────────────────────────

    static int randi(int k) {
        return k > 1 ? (int) (Math.random() * k) : 0;
    }

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

    static String str(Object o) {
        return o == null ? "" : String.valueOf(o);
    }

    @SuppressWarnings("unchecked")
    static Map<String, Object> asMap(Object o) {
        if (o instanceof Map) {
            return (Map<String, Object>) o;
        }
        return new HashMap<>();
    }

    static boolean isCallable(Object o) {
        return o instanceof Transform || o instanceof java.util.function.Function || o instanceof Thunk;
    }

    @SuppressWarnings("unchecked")
    static Object callFn(Object fn, Object arg) {
        if (fn instanceof Transform) {
            return ((Transform) fn).apply(arg);
        }
        if (fn instanceof java.util.function.Function) {
            return ((java.util.function.Function<Object, Object>) fn).apply(arg);
        }
        if (fn instanceof Thunk) {
            return ((Thunk) fn).get();
        }
        throw new IllegalArgumentException("not callable: " + fn);
    }

    static final Pattern SPECIAL_RE = Pattern.compile("[@|\\$#{}\\[\\]^~]|@@\\d{9,11}");
    static final Pattern STRIP_UNRESOLVED = Pattern.compile(
        "(?<!&)(?:[$#])[A-Za-z_][A-Za-z_0-9]*(?:\\(\\))?(?:\\.[A-Za-z_][A-Za-z_0-9]*(?:\\(\\))?)*");

    static boolean isParseable(Object s) {
        if (s == null) {
            return false;
        }
        if (s instanceof Map || s instanceof List) {
            return false;
        }
        if (isCallable(s)) {
            return true;
        }
        if (s instanceof Number) {
            return SPECIAL_RE.matcher(String.valueOf(s)).find();
        }
        if (s instanceof String) {
            return SPECIAL_RE.matcher((String) s).find();
        }
        return true;
    }

    static int stringHash(String text) {
        int h = 0;
        for (int i = 0; i < text.length(); i++) {
            h = 31 * h + text.charAt(i);
        }
        return h;
    }

    static String stripTrailingNewlines(String s) {
        int end = s.length();
        while (end > 0 && s.charAt(end - 1) == '\n') {
            end--;
        }
        return s.substring(0, end);
    }

    // ── pre / post parse ────────────────────────────────────────────────────────

    static final Pattern MD_LINK = Pattern.compile("\\[([^\\]]+)\\]\\(([^)]+)\\)");
    static final Pattern COMMENT = Pattern.compile("(?:^|\\n)[ \\t]*//[^\\n]*|/\\*.*?\\*/",
        Pattern.DOTALL | Pattern.MULTILINE);
    static final Pattern WEIGHT_PAREN = Pattern.compile("\\(\\s*(\\d+)\\s*\\)");
    static final Pattern INLINE_ASSIGN = Pattern.compile("^([$#][A-Za-z_0-9]+)\\s*=(.+)$",
        Pattern.MULTILINE);
    static final Pattern UNICODE_WS = Pattern.compile("[\\u00a0\\u2000-\\u200b\\u2028\\u2029\\u3000]+");
    static final Pattern ENTITY_RE = Pattern.compile("&([a-zA-Z][a-zA-Z0-9]*|#[0-9]+|#x[0-9a-fA-F]+);");

    static final Map<String, String> ENTITY_MAP = new HashMap<>();
    static {
        String[][] pairs = {
            {"lpar", "("}, {"rpar", ")"}, {"lsqb", "["}, {"rsqb", "]"}, {"nbsp", "\u00a0"},
            {"amp", "&"}, {"apos", "'"}, {"quot", "\""}, {"lbrack", "["}, {"rbrack", "]"},
            {"lt", "<"}, {"gt", ">"}, {"lbrace", "{"}, {"rbrace", "}"}, {"lcub", "{"}, {"rcub", "}"},
            {"dollar", "$"}, {"vert", "|"}, {"num", "#"}, {"period", "."}, {"bsol", "\\"},
            {"equals", "="}, {"commat", "@"}, {"sol", "/"}, {"semi", ";"}, {"colon", ":"},
            {"circ", "^"}, {"tilde", "~"}
        };
        for (String[] p : pairs) {
            ENTITY_MAP.put(p[0], p[1]);
        }
    }

    static String preParse(String text) {
        if (text == null || text.isEmpty()) {
            return text;
        }
        text = text.replace("\r\n", "\n").replace("\r", "\n");
        text = MD_LINK.matcher(text).replaceAll("&lsqb;$1&rsqb;&lpar;$2&rpar;");
        text = COMMENT.matcher(text).replaceAll("");
        text = text.replaceAll("\n{2,}", "\n");
        text = stripLeadingNewlines(text);
        text = text.replace("~\n", "");
        text = text.replace("\\\n", "");
        text = WEIGHT_PAREN.matcher(text).replaceAll("^$1^");

        // Wrap bare top-level assignments in {..}, tracking bracket depth so that
        // multi-line values (e.g. $foo=[cat\ndog]) stay together.
        List<String> segments = new ArrayList<>();
        List<String> current = new ArrayList<>();
        int depth = 0;
        int i = 0;
        while (i < text.length()) {
            char ch = text.charAt(i);
            if (ch == '\\' && i + 1 < text.length()) {
                current.add(String.valueOf(ch));
                current.add(String.valueOf(text.charAt(i + 1)));
                i += 2;
                continue;
            }
            if (ch == '[') {
                depth++;
                current.add(String.valueOf(ch));
            } else if (ch == ']') {
                depth--;
                current.add(String.valueOf(ch));
            } else if (ch == '\n' && depth == 0) {
                segments.add(String.join("", current));
                current = new ArrayList<>();
            } else {
                current.add(String.valueOf(ch));
            }
            i++;
        }
        segments.add(String.join("", current));

        List<String> result = new ArrayList<>();
        List<Boolean> isAssigns = new ArrayList<>();
        for (String seg : segments) {
            String stripped = seg.strip();
            boolean isAssign = INLINE_ASSIGN.matcher(stripped).lookingAt();
            result.add(isAssign ? "{" + stripped + "}" : seg);
            isAssigns.add(isAssign);
        }
        // Assign segments consume their trailing newline; other segments keep theirs.
        StringBuilder out = new StringBuilder();
        for (int k = 0; k < result.size(); k++) {
            out.append(result.get(k));
            if (k < result.size() - 1 && !isAssigns.get(k)) {
                out.append('\n');
            }
        }
        return out.toString();
    }

    static String stripLeadingNewlines(String s) {
        int start = 0;
        while (start < s.length() && s.charAt(start) == '\n') {
            start++;
        }
        return s.substring(start);
    }

    static String decodeEntities(String text) {
        Matcher m = ENTITY_RE.matcher(text);
        StringBuilder sb = new StringBuilder();
        while (m.find()) {
            String name = m.group(1);
            String rep;
            if (name.startsWith("#x")) {
                rep = new String(Character.toChars(Integer.parseInt(name.substring(2), 16)));
            } else if (name.startsWith("#")) {
                rep = new String(Character.toChars(Integer.parseInt(name.substring(1))));
            } else {
                rep = ENTITY_MAP.getOrDefault(name, m.group(0));
            }
            m.appendReplacement(sb, Matcher.quoteReplacement(rep));
        }
        m.appendTail(sb);
        return sb.toString();
    }

    static String postParse(String text) {
        if (text == null || text.isEmpty()) {
            return text;
        }
        text = text.replaceAll("@@\\d{9,11}", "");
        text = decodeEntities(text);
        text = UNICODE_WS.matcher(text).replaceAll(" ");
        return text;
    }

    // ── JSOL parser (JSON-ish with unquoted keys / @ operators) ─────────────────

    static Object parseJsol(String text) {
        text = text.strip();
        if (text.startsWith("{") && text.endsWith("}")) {
            text = text.substring(1, text.length() - 1).strip();
        }
        text = text.replaceAll("([$@]?[A-Za-z_][A-Za-z_0-9]*(?:\\(\\))?)\\s*:", "\"$1\":");
        text = text.replaceAll("'([^']*)'", "\"$1\"");
        text = text.replaceAll("/([^/]+)/[gimy]*", "\\{\"\\$regex\": \"$1\"\\}");
        return Json.parse("{" + text + "}");
    }

    // ── gate evaluation (mingo-style) ───────────────────────────────────────────

    @SuppressWarnings("unchecked")
    static boolean evalGate(Object conditionObj, Map<String, Object> context) {
        Object cond = normalizeKeys(conditionObj);
        return gateTest(context, (Map<String, Object>) cond);
    }

    @SuppressWarnings("unchecked")
    static Object normalizeKeys(Object obj) {
        if (obj instanceof Map) {
            Map<String, Object> out = new LinkedHashMap<>();
            for (Map.Entry<String, Object> e : ((Map<String, Object>) obj).entrySet()) {
                out.put(e.getKey().replace("@", "$"), normalizeKeys(e.getValue()));
            }
            return out;
        }
        if (obj instanceof List) {
            List<Object> out = new ArrayList<>();
            for (Object item : (List<Object>) obj) {
                out.add(normalizeKeys(item));
            }
            return out;
        }
        return obj;
    }

    @SuppressWarnings("unchecked")
    static boolean gateTest(Map<String, Object> doc, Map<String, Object> cond) {
        for (Map.Entry<String, Object> e : cond.entrySet()) {
            String key = e.getKey();
            Object c = e.getValue();
            if (key.equals("$or")) {
                boolean any = false;
                for (Object sub : (List<Object>) c) {
                    if (gateTest(doc, (Map<String, Object>) sub)) {
                        any = true;
                        break;
                    }
                }
                if (!any) {
                    return false;
                }
            } else if (key.equals("$and")) {
                for (Object sub : (List<Object>) c) {
                    if (!gateTest(doc, (Map<String, Object>) sub)) {
                        return false;
                    }
                }
            } else if (key.equals("$nor")) {
                for (Object sub : (List<Object>) c) {
                    if (gateTest(doc, (Map<String, Object>) sub)) {
                        return false;
                    }
                }
            } else {
                String lookup = key.startsWith("$") ? key.substring(1) : key;
                Object docVal = doc.get(lookup);
                if (!testValue(docVal, c)) {
                    return false;
                }
            }
        }
        return true;
    }

    @SuppressWarnings("unchecked")
    static boolean testValue(Object docVal, Object cond) {
        if (cond instanceof Map) {
            Map<String, Object> m = (Map<String, Object>) cond;
            if (m.isEmpty()) {
                return false;
            }
            for (Map.Entry<String, Object> e : m.entrySet()) {
                String op = e.getKey();
                Object operand = e.getValue();
                switch (op) {
                    case "$eq":
                        if (!str(docVal).equals(str(operand))) {
                            return false;
                        }
                        break;
                    case "$ne":
                        if (str(docVal).equals(str(operand))) {
                            return false;
                        }
                        break;
                    case "$gt":
                        if (!cmp(docVal, operand, (a, b) -> a > b)) {
                            return false;
                        }
                        break;
                    case "$gte":
                        if (!cmp(docVal, operand, (a, b) -> a >= b)) {
                            return false;
                        }
                        break;
                    case "$lt":
                        if (!cmp(docVal, operand, (a, b) -> a < b)) {
                            return false;
                        }
                        break;
                    case "$lte":
                        if (!cmp(docVal, operand, (a, b) -> a <= b)) {
                            return false;
                        }
                        break;
                    case "$in":
                        if (!(operand instanceof List) || !((List<Object>) operand).contains(docVal)) {
                            return false;
                        }
                        break;
                    case "$nin":
                        if (operand instanceof List && ((List<Object>) operand).contains(docVal)) {
                            return false;
                        }
                        break;
                    case "$exists":
                        if (truthy(operand) && docVal == null) {
                            return false;
                        }
                        if (!truthy(operand) && docVal != null) {
                            return false;
                        }
                        break;
                    case "$regex":
                        if (!Pattern.compile(str(operand)).matcher(str(docVal)).find()) {
                            return false;
                        }
                        break;
                    default:
                        return false;
                }
            }
            return true;
        }
        return str(docVal).equals(str(cond));
    }

    interface Cmp {
        boolean test(double a, double b);
    }

    static boolean cmp(Object a, Object b, Cmp op) {
        try {
            return op.test(Double.parseDouble(str(a)), Double.parseDouble(str(b)));
        } catch (NumberFormatException e) {
            return false;
        }
    }

    static final Set<String> MINGO_OPS = Set.of(
        "$gt", "$lt", "$gte", "$lte", "$ne", "$eq", "$exists", "$in", "$nin", "$or", "$and", "$nor",
        "$regex", "@gt", "@lt", "@gte", "@lte", "@ne", "@eq", "@exists", "@in", "@nin", "@or",
        "@and", "@nor", "@regex");

    @SuppressWarnings("unchecked")
    static List<String> getOperands(Object conditionObj) {
        Set<String> keys = new java.util.LinkedHashSet<>();
        List<Object> stack = new ArrayList<>();
        stack.add(conditionObj);
        while (!stack.isEmpty()) {
            Object obj = stack.remove(stack.size() - 1);
            if (obj instanceof Map) {
                for (Map.Entry<String, Object> e : ((Map<String, Object>) obj).entrySet()) {
                    if (!MINGO_OPS.contains(e.getKey())) {
                        keys.add(e.getKey());
                    }
                    if (e.getValue() instanceof Map || e.getValue() instanceof List) {
                        stack.add(e.getValue());
                    }
                }
            } else if (obj instanceof List) {
                stack.addAll((List<Object>) obj);
            }
        }
        List<String> out = new ArrayList<>();
        for (String k : keys) {
            out.add(k.startsWith("$") ? k.substring(1) : k);
        }
        return out;
    }

    // ── AST node ────────────────────────────────────────────────────────────────

    static final class Node {
        final String kind;
        final List<Object> args;

        Node(String kind, List<Object> args) {
            this.kind = kind;
            this.args = args;
        }

        Object get(int i) {
            return args.get(i);
        }

        String str(int i) {
            return (String) args.get(i);
        }

        @SuppressWarnings("unchecked")
        List<Node> nodes(int i) {
            return (List<Node>) args.get(i);
        }

        @SuppressWarnings("unchecked")
        List<String> strings(int i) {
            return (List<String>) args.get(i);
        }
    }

    // ── Tokenizer ───────────────────────────────────────────────────────────────

    static final class Token {
        final String type;
        final String value;
        final int pos;

        Token(String type, String value, int pos) {
            this.type = type;
            this.value = value;
            this.pos = pos;
        }
    }

    static final class Pattern2 {
        final String type;
        final Pattern pattern;

        Pattern2(String type, String regex) {
            this.type = type;
            this.pattern = Pattern.compile(regex);
        }
    }

    static final List<Pattern2> TOKEN_PATTERNS = List.of(
        new Pattern2("GATE", "@\\s*\\{(?:[^{}]|\\{(?:[^{}]|\\{[^{}]*\\})*\\})*\\}"),
        new Pattern2("ENTITY", "&(?:[a-zA-Z][a-zA-Z0-9]*|#[0-9]+|#x[0-9a-fA-F]+);"),
        new Pattern2("WEIGHT", "\\s*\\^-?\\d+\\^\\s*"),
        new Pattern2("PENDING", "@@[0-9]{9,11}"),
        new Pattern2("ELSE", "\\s*\\|\\|\\s*"),
        new Pattern2("OC", "\\[\\s*"),
        new Pattern2("CC", "\\s*\\]"),
        new Pattern2("OS", "\\{\\s*"),
        new Pattern2("CS", "\\s*\\}"),
        new Pattern2("OR", "\\s*\\|\\s*"),
        new Pattern2("EQ", "\\s*=\\s*"),
        new Pattern2("SYMBOL", "(?:\\$|#[A-Za-z_0-9])[A-Za-z_0-9]*(?:\\(\\))?"),
        new Pattern2("TRANSFORM", "\\.[A-Za-z_][A-Za-z_0-9]*(?:\\(\\))?"),
        new Pattern2("RAW", "[^|$#&{}\\[\\]^~@.=()\\s\\\\]+|[ \\t]+"));

    static final Map<Character, String> BACKSLASH_ENTITY = new HashMap<>();
    static {
        String[][] pairs = {
            {"{", "&lcub;"}, {"}", "&rcub;"}, {"[", "&lsqb;"}, {"]", "&rsqb;"},
            {"$", "&dollar;"}, {"#", "&num;"}, {"|", "&vert;"}, {"\\", "&bsol;"},
            {"^", "&#94;"}, {"~", "&#126;"}, {"@", "&commat;"}, {"=", "&equals;"},
            {"(", "&lpar;"}, {")", "&rpar;"}, {".", "&period;"}, {"/", "&sol;"},
            {"&", "&amp;"}
        };
        for (String[] p : pairs) {
            BACKSLASH_ENTITY.put(p[0].charAt(0), p[1]);
        }
    }

    static List<Token> tokenize(String text) {
        List<Token> tokens = new ArrayList<>();
        int pos = 0;
        while (pos < text.length()) {
            if (text.charAt(pos) == '\\' && pos + 1 < text.length()) {
                char next = text.charAt(pos + 1);
                String entity = BACKSLASH_ENTITY.getOrDefault(next, String.valueOf(next));
                tokens.add(new Token("RAW", entity, pos));
                pos += 2;
                continue;
            }
            boolean matched = false;
            for (Pattern2 p : TOKEN_PATTERNS) {
                Matcher m = p.pattern.matcher(text);
                if (m.find(pos) && m.start() == pos) {
                    tokens.add(new Token(p.type, m.group(), pos));
                    pos = m.end();
                    matched = true;
                    break;
                }
            }
            if (!matched) {
                tokens.add(new Token("RAW", String.valueOf(text.charAt(pos)), pos));
                pos += 1;
            }
        }
        tokens.add(new Token("EOF", "", pos));
        return tokens;
    }

    // ── Parser ──────────────────────────────────────────────────────────────────

    static final class ParseError extends RuntimeException {
        ParseError(String msg) {
            super(msg);
        }
    }

    static final class Parser {
        final List<Token> tokens;
        int pos = 0;

        Parser(List<Token> tokens) {
            this.tokens = tokens;
        }

        Token peek() {
            return tokens.get(pos);
        }

        String peekType() {
            return tokens.get(pos).type;
        }

        Token consume(String expected) {
            Token t = tokens.get(pos);
            if (expected != null && !t.type.equals(expected)) {
                throw new ParseError("Expected " + expected + " got " + t.type + " (" + t.value + ")");
            }
            pos++;
            return t;
        }

        boolean at(String... types) {
            String t = peekType();
            for (String ty : types) {
                if (ty.equals(t)) {
                    return true;
                }
            }
            return false;
        }

        Node parseScript() {
            List<Node> exprs = new ArrayList<>();
            while (!at("EOF")) {
                if (at("OR", "ELSE")) {
                    throw new ParseError("Unexpected " + peekType() + " at top level");
                }
                exprs.add(parseExpr());
            }
            return new Node("script", new ArrayList<>(List.of(exprs)));
        }

        Node parseExpr() {
            List<Node> atoms = new ArrayList<>();
            while (!at("EOF", "OR", "ELSE", "CC", "CS", "WEIGHT")) {
                int prev = pos;
                atoms.add(parseAtom());
                if (pos == prev) {
                    throw new ParseError("Parser stuck at token " + peekType());
                }
            }
            return new Node("expr", new ArrayList<>(List.of(atoms)));
        }

        Node parseAtom() {
            String t = peekType();
            if (t.equals("OC")) {
                return parseChoice();
            }
            if (t.equals("OS")) {
                return parseSilent();
            }
            if (t.equals("PENDING")) {
                return new Node("pgate", new ArrayList<>(List.of(consume(null).value)));
            }
            if (t.equals("ENTITY")) {
                return new Node("entity", new ArrayList<>(List.of(consume(null).value)));
            }
            if (t.equals("SYMBOL")) {
                return parseSymbolOrAssign();
            }
            return parseText();
        }

        Node parseSymbolOrAssign() {
            String sym = consume("SYMBOL").value;
            if (at("EQ")) {
                consume("EQ");
                Node rhs = parseExpr();
                return new Node("assign", new ArrayList<>(List.of(sym, rhs)));
            }
            List<String> txs = collectTransforms();
            return new Node("symbol", new ArrayList<>(List.of(sym, txs)));
        }

        Node parseChoice() {
            consume("OC");
            String gate = null;
            if (at("GATE")) {
                gate = consume(null).value;
            }
            List<List<Object>> orExpr = parseOrExpr();
            List<List<Object>> elseExpr = null;
            if (at("ELSE")) {
                consume("ELSE");
                elseExpr = parseOrExpr();
            }
            consume("CC");
            List<String> txs = collectTransforms();
            return new Node("choice",
                new ArrayList<>(Arrays.asList(gate, orExpr, elseExpr, txs)));
        }

        List<List<Object>> parseOrExpr() {
            List<List<Object>> branches = new ArrayList<>();
            branches.add(parseWexpr());
            while (at("OR")) {
                consume("OR");
                branches.add(parseWexpr());
            }
            return branches;
        }

        List<Object> parseWexpr() {
            List<Object> items = new ArrayList<>();
            while (!at("EOF", "OR", "ELSE", "CC")) {
                if (at("WEIGHT")) {
                    items.add(new Node("weight", new ArrayList<>(List.of(consume(null).value))));
                } else {
                    items.add(parseExpr());
                }
            }
            return items;
        }

        Node parseSilent() {
            consume("OS");
            String gate = null;
            if (at("GATE")) {
                gate = consume(null).value;
            }
            Node node = null;
            if (at("SYMBOL")) {
                String sym = consume("SYMBOL").value;
                if (at("EQ")) {
                    consume("EQ");
                    Node rhs = parseExpr();
                    node = new Node("assign", new ArrayList<>(List.of(sym, rhs)));
                } else {
                    node = new Node("symbol", new ArrayList<>(List.of(sym, new ArrayList<String>())));
                }
            }
            consume("CS");
            return new Node("silent", new ArrayList<>(Arrays.asList(gate, node)));
        }

        Node parseText() {
            Token t = consume(null);
            if (t.type.equals("EOF")) {
                throw new ParseError("Unexpected EOF in text");
            }
            return new Node("text", new ArrayList<>(List.of(t.value)));
        }

        List<String> collectTransforms() {
            List<String> txs = new ArrayList<>();
            while (at("TRANSFORM")) {
                txs.add(consume(null).value);
            }
            return txs;
        }
    }

    static Node parse(String text) {
        return new Parser(tokenize(text)).parseScript();
    }

    // ── Evaluator ───────────────────────────────────────────────────────────────

    final class EvalVisitor {
        final Map<String, Object> context;
        final Map<String, Object> transforms;
        final Map<String, Object> dynamics = new HashMap<>();
        final Map<String, Object> statics = new HashMap<>();
        final Map<String, Object> choices = new HashMap<>();
        final Map<String, Object> pendingGates = new HashMap<>();
        Rand randi = RiScript::randi;
        boolean isNoRepeat = false;
        boolean forceGate = false;

        EvalVisitor(Map<String, Object> context, Map<String, Object> transforms) {
            this.context = context;
            this.transforms = transforms;
        }

        Object evaluate(String text) {
            return visitScript(parse(text));
        }

        Object visitScript(Node node) {
            List<Node> exprs = node.nodes(0);
            List<Object> parts = new ArrayList<>();
            for (Node e : exprs) {
                parts.add(visitExpr(e));
            }
            List<Object> nonNone = new ArrayList<>();
            for (Object p : parts) {
                if (p != null) {
                    nonNone.add(p);
                }
            }
            if (nonNone.size() == 1 && !(nonNone.get(0) instanceof String)) {
                return nonNone.get(0);
            }
            StringBuilder sb = new StringBuilder();
            for (Object p : parts) {
                if (p == null) {
                    continue;
                }
                if (p instanceof String) {
                    sb.append(p);
                } else {
                    sb.append(String.valueOf(p));
                }
            }
            return sb.toString();
        }

        Object visitExpr(Node node) {
            List<Node> atoms = node.nodes(0);
            List<Object> results = new ArrayList<>();
            for (Node a : atoms) {
                Object r = visitAtom(a);
                results.add(r == null ? "" : r);
            }
            if (results.size() == 1) {
                return results.get(0);
            }
            // "not [quite|] far enough" -> collapse the doubled space around an empty atom.
            List<Object> combined = new ArrayList<>(results);
            for (int i = 1; i < combined.size() - 1; i++) {
                Object cur = combined.get(i);
                Object prev = combined.get(i - 1);
                Object next = combined.get(i + 1);
                if ("".equals(cur) && prev instanceof String && ((String) prev).endsWith(" ")
                    && next instanceof String && ((String) next).startsWith(" ")) {
                    combined.set(i + 1, ((String) next).substring(1));
                }
            }
            StringBuilder sb = new StringBuilder();
            for (Object c : combined) {
                sb.append(str(c));
            }
            return sb.toString();
        }

        Object visitAtom(Node node) {
            switch (node.kind) {
                case "choice":
                    return visitChoice(node);
                case "assign":
                    return visitAssign(node, false);
                case "symbol":
                    return visitSymbol(node, false);
                case "silent":
                    return visitSilent(node);
                case "pgate":
                    return visitPgate(node);
                case "entity":
                    return node.str(0);
                case "text":
                    return node.str(0);
                default:
                    throw new ParseError("Unknown atom kind: " + node.kind);
            }
        }

        Object visitSymbol(Node node, boolean silent) {
            String sym = node.str(0);
            List<String> txs = node.strings(1);
            String symClean = sym.replaceAll("\\(\\)$", "");
            String ident = symClean.replaceAll("^[\\$#]+", "");
            boolean isStatic = symClean.startsWith("#");

            if (ident.isEmpty()) {
                if (!txs.isEmpty()) {
                    return applyTransforms("", txs);
                }
                return "";
            }

            isNoRepeat = hasNoRepeat(txs);
            Ctx c = checkContext(ident);
            Object result = c.result;

            if (isNoRepeat && (c.isStatic || c.isUser)) {
                throw new RuntimeException("Attempt to call norepeat() on "
                    + (c.isStatic ? "static symbol '" + sym + "'" : "non-dynamic symbol '" + ident + "'"));
            }
            if (isStatic && !c.isStatic && dynamics.containsKey(ident)) {
                throw new RuntimeException("Attempt to access dynamic symbol '" + ident + "' as static '#'");
            }

            int depth = 0;
            while (isCallable(result)) {
                result = callFn(result, "");
                depth++;
                if (depth > 10) {
                    throw new RuntimeException("Max recursion depth");
                }
            }

            if (result == null) {
                if (txs.isEmpty()) {
                    return symClean;
                }
                return restoreTransforms(symClean, txs);
            }

            boolean resolved = !isParseable(result);
            if (result instanceof String && !resolved) {
                if (isStatic) {
                    EvalVisitor sub = new EvalVisitor(context, transforms);
                    sub.dynamics.putAll(dynamics);
                    sub.statics.putAll(statics);
                    sub.choices.putAll(choices);
                    sub.randi = randi;
                    Object raw;
                    try {
                        raw = sub.visitScript(parse((String) result));
                    } catch (Exception e) {
                        raw = result;
                    }
                    if (raw == null || (raw instanceof String && isParseable((String) raw))) {
                        return result;
                    }
                    statics.put(ident, raw);
                    result = raw;
                    if (!txs.isEmpty()) {
                        result = applyTransforms(result, txs);
                    }
                    isNoRepeat = false;
                    return result;
                }
                if (!txs.isEmpty()) {
                    return restoreTransforms((String) result, txs);
                }
                return result;
            }

            if (isStatic) {
                statics.put(ident, result);
            }
            if (!txs.isEmpty()) {
                result = applyTransforms(result, txs);
            } else if (result instanceof String && ((String) result).isEmpty() && symClean.length() == 1) {
                return symClean;
            }
            isNoRepeat = false;
            return result;
        }

        Object visitAssign(Node node, boolean silent) {
            String sym = node.str(0);
            String symClean = sym.replaceAll("[()]+$", "");
            String ident = symClean.replaceAll("^[\\$#]+", "");
            boolean isStatic = symClean.startsWith("#");
            Node rhs = (Node) node.get(1);

            if (isStatic) {
                if (statics.containsKey(ident) && !isParseable(statics.get(ident))) {
                    return statics.get(ident);
                }
                Object val = visitExpr(rhs);
                statics.put(ident, val);
                return val;
            }
            Object val = visitExpr(rhs);
            final Node r = rhs;
            dynamics.put(ident, (Thunk) () -> visitExpr(r));
            return val;
        }

        Object visitSilent(Node node) {
            String gate = (String) node.get(0);
            Node inner = (Node) node.get(1);
            if (gate != null && !gate.isEmpty()) {
                String decision = evalGateText(gate);
                if (decision.equals("reject")) {
                    return "";
                }
            }
            if (inner != null) {
                if (inner.kind.equals("assign")) {
                    visitAssign(inner, true);
                } else {
                    visitSymbol(inner, true);
                }
            }
            return "";
        }

        @SuppressWarnings("unchecked")
        Object visitChoice(Node node) {
            String gate = (String) node.get(0);
            List<List<Object>> orExpr = (List<List<Object>>) node.get(1);
            List<List<Object>> elseExpr = (List<List<Object>>) node.get(2);
            List<String> txs = (List<String>) node.get(3);
            String original = nodeRepr(node);
            String choiceKey = String.valueOf(stringHash(original));

            if (hasNoRepeat(txs)) {
                throw new RuntimeException("noRepeat() not allowed on choice: " + original);
            }

            String decision = "accept";
            if (gate != null && !gate.isEmpty()) {
                decision = evalGateText(gate);
                if (decision.equals("defer")) {
                    String key = String.format("%010d", Math.abs(stringHash(gate + original)));
                    Map<String, Object> entry = new HashMap<>();
                    entry.put("gate_text", gate);
                    entry.put("node", node);
                    entry.put("operands", getGateOperands(gate));
                    pendingGates.put(key, entry);
                    return "@@" + key;
                }
            }

            List<List<Object>> branches = decision.equals("reject")
                ? (elseExpr != null ? elseExpr : List.of())
                : orExpr;
            if (branches.isEmpty()) {
                return "";
            }
            List<Object> options = parseOptions(branches);
            if (options.isEmpty()) {
                return "";
            }

            List<Object> excluded = new ArrayList<>();
            Object value = null;
            boolean restored = false;
            while (value == null) {
                Object option = choose(options, excluded);
                if ("".equals(option)) {
                    value = "";
                } else {
                    value = option instanceof Node ? visitExpr((Node) option) : option;
                }
                if (value instanceof String) {
                    value = ((String) value).trim();
                }
                if (isParseable(value)) {
                    if (!txs.isEmpty()) {
                        value = restoreTransforms((String) value, txs);
                    }
                    restored = true;
                    break;
                }
                if (!txs.isEmpty()) {
                    value = applyTransforms(value, txs);
                }
                if (isNoRepeat && value != null && value.equals(choices.get(choiceKey))) {
                    excluded.add(value);
                    value = null;
                    continue;
                }
            }
            if (!restored) {
                choices.put(choiceKey, value);
            }
            return value;
        }

        @SuppressWarnings("unchecked")
        Object visitPgate(Node node) {
            String raw = node.str(0);
            String key = raw.replace("@@", "");
            Map<String, Object> lookup = (Map<String, Object>) pendingGates.get(key);
            if (lookup == null) {
                throw new RuntimeException("No pending gate: " + raw);
            }
            forceGate = true;
            Object result = visitChoice((Node) lookup.get("node"));
            forceGate = false;
            return result;
        }

        // ── gate helpers ────────────────────────────────────────────────────────

        String evalGateText(String gateText) {
            String raw = gateText.replaceAll("^@+", "").strip();
            Object cond;
            try {
                cond = parseJsol(raw);
            } catch (Exception e) {
                throw new RuntimeException("Invalid gate: \"" + gateText + "\"");
            }
            List<String> operands = getOperands(cond);
            if (operands.isEmpty()) {
                return "accept";
            }
            Map<String, Object> resolvedOps = new HashMap<>();
            List<String> unresolved = new ArrayList<>();
            for (String sym : operands) {
                String ident = sym.replaceAll("^[\\$#]+", "").replaceAll("\\(\\)$", "");
                Ctx c = checkContext(ident);
                Object result = c.result;
                int depth = 0;
                while (isCallable(result)) {
                    result = callFn(result, "");
                    depth++;
                    if (depth > 10) {
                        break;
                    }
                }
                if (!forceGate && (result == null
                    || (result instanceof String && isParseable((String) result)))) {
                    unresolved.add(sym);
                } else {
                    resolvedOps.put(sym, result);
                }
            }
            if (!unresolved.isEmpty()) {
                return "defer";
            }
            if (evalGate(cond, resolvedOps)) {
                return "accept";
            }
            Map<String, Object> casted = new HashMap<>();
            boolean madeCast = false;
            for (Map.Entry<String, Object> e : resolvedOps.entrySet()) {
                try {
                    casted.put(e.getKey(), Double.parseDouble(str(e.getValue())));
                    madeCast = true;
                } catch (NumberFormatException ex) {
                    casted.put(e.getKey(), e.getValue());
                }
            }
            if (madeCast && evalGate(cond, casted)) {
                return "accept";
            }
            return "reject";
        }

        List<String> getGateOperands(String gateText) {
            String raw = gateText.replaceAll("^@+", "").strip();
            try {
                return getOperands(parseJsol(raw));
            } catch (Exception e) {
                return List.of();
            }
        }

        // ── context lookup ──────────────────────────────────────────────────────

        Ctx checkContext(String ident) {
            Ctx c = new Ctx();
            if (ident == null || ident.isEmpty()) {
                c.result = "";
                c.resolved = true;
                return c;
            }
            Object result = dynamics.get(ident);
            if (result == null) {
                result = statics.get(ident);
                if (result != null) {
                    c.isStatic = true;
                }
            }
            if (result == null) {
                if (context.containsKey(ident)) {
                    result = context.get(ident);
                    c.isUser = true;
                }
            }
            if (result == null) {
                result = transforms.get(ident);
            }
            c.result = result;
            c.resolved = !isParseable(result);
            return c;
        }

        // ── transform helpers ───────────────────────────────────────────────────

        boolean hasNoRepeat(List<String> txs) {
            if (txs == null) {
                return false;
            }
            for (String tx : txs) {
                String name = tx.replaceAll("^\\.+", "").replaceAll("\\(\\)$", "");
                if (name.equals("nr") || name.equals("norepeat")) {
                    return true;
                }
            }
            return false;
        }

        Object applyTransforms(Object value, List<String> txs) {
            for (String tx : txs) {
                value = applyTransform(value, tx);
            }
            return value;
        }

        @SuppressWarnings("unchecked")
        Object applyTransform(Object target, String image) {
            String tx = image.replaceAll("^\\.+", "").replaceAll("\\(\\)$", "");

            Object fn = context.get(tx);
            if (isCallable(fn)) {
                return callFn(fn, target);
            }
            fn = transforms.get(tx);
            if (isCallable(fn)) {
                return callFn(fn, target);
            }
            fn = dynamics.get(tx);
            if (isCallable(fn)) {
                return callFn(fn, target);
            }
            fn = statics.get(tx);
            if (isCallable(fn)) {
                return callFn(fn, target);
            }
            if (target instanceof Map) {
                Map<String, Object> m = (Map<String, Object>) target;
                if (m.containsKey(tx)) {
                    Object v = m.get(tx);
                    return isCallable(v) ? callFn(v, null) : v;
                }
            }
            if (target instanceof String) {
                String s = (String) target;
                switch (tx) {
                    case "toUpperCase":
                        return s.toUpperCase();
                    case "toLowerCase":
                        return s.toLowerCase();
                    case "trim":
                        return s.trim();
                    default:
                        break;
                }
            }
            if ("".equals(target)) {
                return "";
            }
            return str(target) + image;
        }

        Object restoreTransforms(Object value, List<String> txs) {
            if (value instanceof String) {
                String v = (String) value;
                boolean isChoice = v.matches("(?s)^\\[.*\\]$");
                boolean hasSymbol = Pattern.compile("[\\$#][A-Za-z_0-9]").matcher(v).find();
                if (!isChoice && !hasSymbol) {
                    v = "[" + v + "]";
                }
                for (String tx : txs) {
                    v += tx;
                }
                return v;
            }
            return value;
        }

        // ── option parsing ──────────────────────────────────────────────────────

        @SuppressWarnings("unchecked")
        List<Object> parseOptions(List<List<Object>> branches) {
            List<Object> options = new ArrayList<>();
            for (List<Object> branch : branches) {
                int weight = 1;
                List<Object> exprItems = new ArrayList<>();
                for (Object item : branch) {
                    if (item instanceof Node && ((Node) item).kind.equals("weight")) {
                        try {
                            weight = Integer.parseInt(((Node) item).str(0).strip().replace("^", ""));
                        } catch (NumberFormatException e) {
                            // keep weight = 1
                        }
                    } else {
                        exprItems.add(item);
                    }
                }
                Object opt;
                if (exprItems.isEmpty()) {
                    opt = new Node("expr", new ArrayList<>(List.of(new ArrayList<Node>())));
                } else if (exprItems.size() == 1) {
                    opt = exprItems.get(0);
                } else {
                    List<Node> rebuilt = new ArrayList<>();
                    for (Object e : exprItems) {
                        if (e instanceof Node) {
                            Node en = (Node) e;
                            Object evaluated = visitExpr(en);
                            rebuilt.add(new Node("text", new ArrayList<>(List.of(str(evaluated)))));
                        } else {
                            rebuilt.add((Node) e);
                        }
                    }
                    opt = new Node("expr", new ArrayList<>(List.of(rebuilt)));
                }
                for (int w = 0; w < weight; w++) {
                    options.add(opt);
                }
            }
            return options;
        }

        Object choose(List<Object> options, List<Object> excluded) {
            List<Object> valid = new ArrayList<>();
            for (Object o : options) {
                if (!excluded.contains(o)) {
                    valid.add(o);
                }
            }
            if (valid.isEmpty()) {
                throw new RuntimeException("No valid options (all excluded)");
            }
            return valid.get(randi.apply(valid.size()));
        }
    }

    static final class Ctx {
        Object result;
        boolean isStatic;
        boolean isUser;
        boolean resolved;
    }

    /** Deterministic text form of a node, used for choice hashing. */
    @SuppressWarnings("unchecked")
    static String nodeRepr(Object node) {
        if (node instanceof Node) {
            Node n = (Node) node;
            StringBuilder sb = new StringBuilder("(");
            sb.append(n.kind);
            for (Object a : n.args) {
                sb.append(" ").append(nodeRepr(a));
            }
            sb.append(")");
            return sb.toString();
        }
        if (node instanceof List) {
            StringBuilder sb = new StringBuilder("[");
            boolean first = true;
            for (Object o : (List<Object>) node) {
                if (!first) {
                    sb.append(" ");
                }
                first = false;
                sb.append(nodeRepr(o));
            }
            sb.append("]");
            return sb.toString();
        }
        if (node == null) {
            return "None";
        }
        return String.valueOf(node);
    }
}
