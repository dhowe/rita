package rita;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * A tiny, dependency-free JSON reader — just enough to load the canonical dictionary
 * ({@code rita/rita_dict.json}) and the LTS rules without pulling a shaded JSON jar into the
 * Processing library. Supports the subset the data files use: objects, arrays, strings, numbers,
 * booleans and null.
 *
 * <p>Not a general-purpose parser: supports the standard string escapes (including {@code \\u}
 * hex escapes) but no incremental streaming. It exists solely to read RiTa's own data files,
 * which are well-formed and simple.
 */
final class Json {

    private Json() {
    }

    /** Parses a JSON document into Maps (LinkedHashMap, order-preserving), Lists, Strings, Doubles, Booleans, or null. */
    static Object parse(String text) {
        return new Reader(text).parseValue();
    }

    /** Convenience: parse an object whose values are all strings (or nested). */
    @SuppressWarnings("unchecked")
    static Map<String, Object> parseObject(String text) {
        return (Map<String, Object>) parse(text);
    }

    /** Serialises Maps/Lists/Strings/Numbers/Booleans/null to JSON. A SuffixArray is
     *  embedded via its own {@code toJSON()} (raw, not quoted). */
    static String write(Object value) {
        StringBuilder sb = new StringBuilder();
        writeValue(value, sb);
        return sb.toString();
    }

    @SuppressWarnings("unchecked")
    private static void writeValue(Object v, StringBuilder sb) {
        if (v == null) {
            sb.append("null");
        }
        else if (v instanceof Map) {
            sb.append('{');
            boolean first = true;
            for (Map.Entry<String, Object> e : ((Map<String, Object>) v).entrySet()) {
                if (!first) {
                    sb.append(',');
                }
                first = false;
                sb.append(quote(e.getKey())).append(':');
                writeValue(e.getValue(), sb);
            }
            sb.append('}');
        }
        else if (v instanceof List) {
            sb.append('[');
            List<Object> list = (List<Object>) v;
            for (int i = 0; i < list.size(); i++) {
                if (i > 0) {
                    sb.append(',');
                }
                writeValue(list.get(i), sb);
            }
            sb.append(']');
        }
        else if (v instanceof SuffixArray) {
            sb.append(((SuffixArray) v).toJSON());
        }
        else if (v instanceof String) {
            sb.append(quote((String) v));
        }
        else if (v instanceof Boolean) {
            sb.append(v.toString());
        }
        else if (v instanceof Number) {
            double d = ((Number) v).doubleValue();
            if (d == Math.floor(d) && !Double.isInfinite(d) && v instanceof Integer) {
                sb.append(v.toString());
            }
            else {
                sb.append(v.toString());
            }
        }
        else {
            sb.append(quote(String.valueOf(v)));
        }
    }

    private static String quote(String s) {
        StringBuilder sb = new StringBuilder("\"");
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '"':
                    sb.append("\\\"");
                    break;
                case '\\':
                    sb.append("\\\\");
                    break;
                case '\n':
                    sb.append("\\n");
                    break;
                case '\r':
                    sb.append("\\r");
                    break;
                case '\t':
                    sb.append("\\t");
                    break;
                default:
                    sb.append(c);
            }
        }
        return sb.append('"').toString();
    }

    private static final class Reader {
        private final String s;
        private int i;

        Reader(String s) {
            this.s = s;
        }

        private void ws() {
            while (i < s.length()) {
                char c = s.charAt(i);
                if (c == ' ' || c == '\t' || c == '\n' || c == '\r') {
                    i++;
                } else {
                    break;
                }
            }
        }

        Object parseValue() {
            ws();
            char c = peek();
            switch (c) {
                case '{':
                    return parseObj();
                case '[':
                    return parseArr();
                case '"':
                    return parseStr();
                case 't':
                    expect("true");
                    return Boolean.TRUE;
                case 'f':
                    expect("false");
                    return Boolean.FALSE;
                case 'n':
                    expect("null");
                    return null;
                default:
                    return parseNum();
            }
        }

        private Map<String, Object> parseObj() {
            Map<String, Object> m = new LinkedHashMap<>();
            i++; // {
            ws();
            if (peek() == '}') {
                i++;
                return m;
            }
            while (true) {
                ws();
                String key = parseStr();
                ws();
                if (s.charAt(i) != ':') {
                    throw err("expected ':'");
                }
                i++;
                m.put(key, parseValue());
                ws();
                char c = s.charAt(i++);
                if (c == '}') {
                    break;
                }
                if (c != ',') {
                    throw err("expected ',' or '}'");
                }
            }
            return m;
        }

        private List<Object> parseArr() {
            List<Object> a = new ArrayList<>();
            i++; // [
            ws();
            if (peek() == ']') {
                i++;
                return a;
            }
            while (true) {
                a.add(parseValue());
                ws();
                char c = s.charAt(i++);
                if (c == ']') {
                    break;
                }
                if (c != ',') {
                    throw err("expected ',' or ']'");
                }
            }
            return a;
        }

        private String parseStr() {
            if (s.charAt(i) != '"') {
                throw err("expected string");
            }
            i++;
            StringBuilder sb = new StringBuilder();
            while (true) {
                char c = s.charAt(i++);
                if (c == '"') {
                    break;
                }
                if (c == '\\') {
                    char e = s.charAt(i++);
                    switch (e) {
                        case '"':
                            sb.append('"');
                            break;
                        case '\\':
                            sb.append('\\');
                            break;
                        case '/':
                            sb.append('/');
                            break;
                        case 'b':
                            sb.append('\b');
                            break;
                        case 'f':
                            sb.append('\f');
                            break;
                        case 'n':
                            sb.append('\n');
                            break;
                        case 'r':
                            sb.append('\r');
                            break;
                        case 't':
                            sb.append('\t');
                            break;
                        case 'u':
                            sb.append((char) Integer.parseInt(s.substring(i, i + 4), 16));
                            i += 4;
                            break;
                        default:
                            throw err("bad escape \\" + e);
                    }
                } else {
                    sb.append(c);
                }
            }
            return sb.toString();
        }

        private Double parseNum() {
            int start = i;
            while (i < s.length() && "+-0123456789.eE".indexOf(s.charAt(i)) >= 0) {
                i++;
            }
            return Double.valueOf(s.substring(start, i));
        }

        private char peek() {
            return s.charAt(i);
        }

        private void expect(String lit) {
            if (!s.startsWith(lit, i)) {
                throw err("expected " + lit);
            }
            i += lit.length();
        }

        private RuntimeException err(String msg) {
            return new RuntimeException("JSON parse error at " + i + ": " + msg);
        }
    }
}
