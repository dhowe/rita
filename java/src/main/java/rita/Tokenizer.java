package rita;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Tokenizer — port of {@code js/src/tokenizer.js}.
 *
 * <p>Implements {@code tokenize}, {@code untokenize}, {@code sentences} and {@code tokens} by
 * reproducing the JS sequential-regex pipeline ({@code TOKENIZE_RE}), the tag push/pop handling,
 * and the decision-rule state machine in {@code _nextState}.
 */
public class Tokenizer {

    // ---- regex constants (mirror the JS consts) -------------------------------------

    static final Pattern[] UNTAG_RE = {
        Pattern.compile("^ *<[a-z][a-z0-9='\"#;:&\\s\\-+/.?]*/> *$", Pattern.CASE_INSENSITIVE),
        Pattern.compile("^ *<([a-z][a-z0-9='\"#;:&\\s\\-+/.?]*[a-z0-9='\"#;:&\\s\\-+.?]|[a-z])> *$", Pattern.CASE_INSENSITIVE),
        Pattern.compile("^ *</[a-z][a-z0-9='\"#;:&\\s\\-+/.?]*> *$", Pattern.CASE_INSENSITIVE),
        Pattern.compile("^ *<!DOCTYPE[^>]*> *$", Pattern.CASE_INSENSITIVE),
        Pattern.compile("^ *<!--[^->]*--> *$"),
    };

    static final Pattern LT_RE = Pattern.compile("^ *< *$");
    static final Pattern GT_RE = Pattern.compile("^ *> *$");
    static final Pattern TAGSTART_RE = Pattern.compile("^ *[!\\-/] *$");
    static final Pattern TAGEND_RE = Pattern.compile("^ *[\\-/] *$");
    static final Pattern NOSP_AF_PUNCT_RE = Pattern.compile("^[\\^*$/\u2044#\\-@\u00b0\u2012\u2013\u2014]+$");
    static final Pattern LB_RE = Pattern.compile("^[\\[({\u27e8]+$");
    static final Pattern RB_RE = Pattern.compile("^[)\\]\\}\u27e9]+$");
    static final Pattern QUOTE_RE = Pattern.compile("^[\"\"\u201c\u201d\u2019\u2018`''\u00ab\u00bb]+$");
    static final Pattern DOMAIN_RE = Pattern.compile("^(com|org|edu|net|xyz|gov|int|eu|hk|tw|cn|de|ch|fr)$");
    static final Pattern SQUOTE_RE = Pattern.compile("^[\u2019\u2018`']+$");
    static final Pattern ALPHA_RE = Pattern.compile("^[A-Za-z\u2019']+$");
    static final Pattern WS_RE = Pattern.compile(" +");
    static final Pattern APOS_RE = Pattern.compile("^[\u2019']+$");
    static final Pattern NL_RE = Pattern.compile("(\\r?\\n)+");
    static final Pattern WWW_RE = Pattern.compile("^(www[0-9]?|WWW[0-9]?)$");
    static final Pattern NOSP_BF_PUNCT_RE =
        Pattern.compile("^[,.;:?!)\"\"\u201c\u201d\u2019\u2018`'%\u2026\u2103^*\u00b0/\u2044\u2012\u2013\u2014\\-@]+$");
    static final Pattern LINEBREAK_RE = Pattern.compile("\\r?\\n");
    static final Pattern URL_RE = Pattern.compile(
        "((http[s]?):(//))?([-a-zA-Z0-9@:%._+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b)([-a-zA-Z0-9()@:%_+.~#?&//=]*)");
    static final Pattern EMAIL_RE = Pattern.compile("^\\w+([.-]?\\w+)*@\\w+([.-]?\\w+)*(\\.\\w{2,3})+$");
    static final Pattern ELLIPSIS_RE = Pattern.compile("^(?:\\.\\s*){2,}$");
    static final Pattern ELLIPSIS_ENC_RE = Pattern.compile("^_el([\u2062\u2063]+)_$");
    static final Pattern DASH_RE = Pattern.compile("^[\u2012\u2013\u2014-]+$");
    static final Pattern UNDER_RE = Pattern.compile(
        "([0-9a-zA-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u00FF]|[.,])_([0-9a-zA-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u00FF])");
    static final Pattern TAG_RE = Pattern.compile(
        "(</?[a-z][a-z0-9='\"#;:&\\s\\-+/.?]*/?>|<!DOCTYPE[^>]*>|<!--[^>-]*-->)", Pattern.CASE_INSENSITIVE);
    static final String TAG = "TAG";
    static final Pattern POPTAG_RE = Pattern.compile("_" + TAG + "[0-9]+_");
    static final Pattern SPLITTER = Pattern.compile("(\\S.+?[.!?][\"\u201D]?)(?=\\s+|$)");

    // ---- TOKENIZE_RE: sequential (pattern, replacement) pairs -----------------------

    static final class Rule {
        final Pattern p;
        final String repl;
        final Function<String, String> fn;
        final boolean global;

        Rule(String regex, int flags, String repl) {
            this(regex, flags, repl, true);
        }

        Rule(String regex, int flags, String repl, boolean global) {
            this.p = Pattern.compile(regex, flags);
            this.repl = repl;
            this.fn = null;
            this.global = global;
        }

        Rule(String regex, int flags, Function<String, String> fn) {
            this.p = Pattern.compile(regex, flags);
            this.repl = null;
            this.fn = fn;
            this.global = true;
        }
    }

    static final Rule[] TOKENIZE_RE = {
        // save abbreviations --------
        new Rule("\\b([Ee])[.]([Gg])[.]", 0, "_$1$2_"),
        new Rule("\\b([Ii])[.]([Ee])[.]", 0, "_$1$2_"),
        new Rule("\\b([Aa])[.]([Mm])[.]", 0, "_$1$2_"),
        new Rule("\\b([Pp])[.]([Mm])[.]", 0, "_$1$2_"),
        new Rule("\\b(Cap)[.]", 0, "_Cap_"),
        new Rule("\\b([Cc])[.]", 0, "_$1_"),
        new Rule("\\b([Ee][Tt])[\\s]([Aa][Ll])[.]", 0, "_$1zzz$2_", false),
        new Rule("\\b(etc|ETC)[.]", 0, "_$1_"),
        new Rule("\\b([Pp])[.]([Ss])[.]", 0, "_$1$2dot_"),
        new Rule("\\b([Pp])[.]([Ss])", 0, "_$1$2_"),
        new Rule("\\b([Pp])([Hh])[.]([Dd])", 0, "_$1$2$3_"),
        new Rule("\\b([Rr])[.]([Ii])[.]([Pp])", 0, "_$1$2$3_"),
        new Rule("\\b([Vv])([Ss]?)[.]", 0, "_$1$2_"),
        new Rule("\\b([Mm])([Rr]|[Ss]|[Xx])\\.", 0, "_$1$2_"),
        new Rule("\\b([Dd])([Rr])[.]", 0, "_$1$2_"),
        new Rule("\\b([Pp])([Ff])[.]", 0, "_$1$2_"),
        new Rule("\\b([Ii])([Nn])([Dd]|[Cc])[.]", 0, "_$1$2$3_"),
        new Rule("\\b([Cc])([Oo])[.][,][\\s]([Ll])([Tt])([Dd])[.]", 0, "_$1$2dcs$3$4$5_"),
        new Rule("\\b([Cc])([Oo])[.][\\s]([Ll])([Tt])([Dd])[.]", 0, "_$1$2ds$3$4$5_"),
        new Rule("\\b([Cc])([Oo])[.][,]([Ll])([Tt])([Dd])[.]", 0, "_$1$2dc$3$4$5_"),
        new Rule("\\b([Cc])([Oo])([Rr]?)([Pp]?)[.]", 0, "_$1$2$3$4_"),
        new Rule("\\b([Ll])([Tt])([Dd])[.]", 0, "_$1$2$3_"),
        new Rule("\\b(prof|Prof|PROF)\\.", 0, "_$1_"),
        new Rule("\\b([\\w.]+)@(\\w+\\.\\w+)", 0, "$1__AT__$2"),
        new Rule("\\b((http[s]?):(//))([-a-zA-Z0-9@:%._+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b)([-a-zA-Z0-9()@:%_+.~#?&//=]*)",
            0, "$2COLON$3$4$5"),
        // decimal #
        new Rule("([-]?[0-9]+)\\.([0-9]+)", 0, "$1DECIMALDOT$2_"),
        new Rule("([-]?[0-9]+)\\.([0-9]+)e([-]?[0-9]+)", 0, "_$1DECIMALDOT$2POWERE$3_"),
        new Rule("([0-9]{1,3}),([0-9]{3})", 0, "$1_DECIMALCOMMA_$2"),
        new Rule("([A-Za-z0-9])\\.([A-Za-z0-9])", 0, "$1_DECIMALDOT_$2"),
        // escape sequences of line breaks
        new Rule("\\r\\n", 0, " _CARRIAGERETURNLINEFEED_ "),
        new Rule("\\n\\r", 0, " _LINEFEEDCARRIAGERETURN_ "),
        new Rule("\\n", 0, " _LINEFEED_ "),
        new Rule("\\r", 0, " _CARRIAGERETURN_ "),
        // collapse 2+ periods into one encoded token
        new Rule("\\.(?:\\s*\\.)+", 0, (Function<String, String>) m ->
            " _el" + m.replace(".", "\u2062").replaceAll("\\s+", "\u2063") + "_ "),
        new Rule("([?!\"\u201C.,;:@#$%&])", 0, " $1 "),
        new Rule("\u2026", 0, " \u2026 "),
        new Rule("\\s+", 0, " "),
        new Rule(",([^0-9])", 0, " , $1"),
        new Rule("([^.])([.])([\\])}>\"'\u2019]*)\\s*$", 0, "$1 $2$3 "),
        new Rule("([\\[\\](){}<>\u27e8\u27e9])", 0, " $1 "),
        new Rule("--", 0, " -- "),
        new Rule("\u2012", 0, " \u2012 "),
        new Rule("\u2013", 0, " \u2013 "),
        new Rule("\u2014", 0, " \u2014 "),
        new Rule("$", 0, " "),
        new Rule("^", 0, " "),
        new Rule("([^'])' | '", 0, "$1 ' "),
        new Rule(" \u2018", 0, " \u2018 "),
        new Rule("'([SMD]) ", 0, " '$1 "),
        new Rule(" ([A-Z]) \\.", 0, " $1. "),
        new Rule("^\\s+", 0, ""),
        new Rule("\\^", 0, " ^ "),
        new Rule("\u00b0", 0, " \u00b0 "),
        // pop ------------------
        new Rule("_([Ee])([Gg])_", 0, "$1.$2."),
        new Rule("_([Ii])([Ee])_", 0, "$1.$2."),
        new Rule("_([Aa])([Mm])_", 0, "$1.$2."),
        new Rule("_([Pp])([Mm])_", 0, "$1.$2."),
        new Rule("_Cap_", 0, "Cap."),
        new Rule("_([Cc])_", 0, "$1."),
        new Rule("_([Ee][Tt])zzz([Aa][Ll])_", 0, "$1_$2.", false),
        new Rule("_(etc|ETC)_", 0, "$1."),
        new Rule("_([Pp])([Ss])dot_", 0, "$1.$2."),
        new Rule("_([Pp])([Ss])_", 0, "$1.$2"),
        new Rule("_([Pp])([Hh])([Dd])_", 0, "$1$2.$3"),
        new Rule("_([Rr])([Ii])([Pp])_", 0, "$1.$2.$3"),
        new Rule("_([Vv])([Ss]?)_", 0, "$1$2."),
        new Rule("_([Mm])([Rr]|[Ss]|[Xx])_", 0, "$1$2."),
        new Rule("_([Dd])([Rr])_", 0, "$1$2."),
        new Rule("_([Pp])([Ff])_", 0, "$1$2."),
        new Rule("_([Ii])([Nn])([Dd]|[Cc])_", 0, "$1$2$3."),
        new Rule("_([Cc])([Oo])([Rr]?)([Pp]?)_", 0, "$1$2$3$4."),
        new Rule("_([Cc])([Oo])dc([Ll])([Tt])([Dd])_", 0, "$1$2.,$3$4$5."),
        new Rule("_([Ll])([Tt])([Dd])_", 0, "$1$2$3."),
        new Rule("_([Cc])([Oo])dcs([Ll])([Tt])([Dd])_", 0, "$1$2.,_$3$4$5."),
        new Rule("_([Cc])([Oo])ds([Ll])([Tt])([Dd])_", 0, "$1$2._$3$4$5."),
        new Rule("_(prof|PROF|Prof)_", 0, "$1."),
        new Rule("([-]?[0-9]+)DECIMALDOT([0-9]+)_", 0, "$1.$2"),
        new Rule("_([-]?[0-9]+)\\DECIMALDOT([0-9]+)POWERE([-]?[0-9]+)_", 0, "$1.$2e$3"),
        new Rule("_DECIMALCOMMA_", 0, ","),
        new Rule("_DECIMALDOT_", 0, "."),
        new Rule("__AT__", 0, "@"),
        new Rule("((http[s]?)COLON(//))([-a-zA-Z0-9@:%._+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b)([-a-zA-Z0-9()@:%_+.~#?&//=]*)",
            0, "$2:$3$4$5"),
        new Rule("_LINEFEED_", 0, "\n"),
        new Rule("_CARRIAGERETURN_", 0, "\r"),
        new Rule("_CARRIAGERETURNLINEFEED_", 0, "\r\n"),
        new Rule("_LINEFEEDCARRIAGERETURN_", 0, "\n\r"),
    };

    static final Rule[] CONTRACTS_RE = {
        new Rule("\\b([Cc])an['\u2019]t", 0, "$1an not"),
        new Rule("\\b([Dd])idn['\u2019]t", 0, "$1id not"),
        new Rule("\\b([CcWw])ouldn['\u2019]t", 0, "$1ould not"),
        new Rule("\\b([Ss])houldn['\u2019]t", 0, "$1hould not"),
        new Rule("\\b([Ii])t['\u2019]s", 0, "$1t is"),
        new Rule("\\b([tT]hat)['\u2019]s", 0, "$1 is"),
        new Rule("\\b(she|he|you|they|i)['\u2019]d", Pattern.CASE_INSENSITIVE, "$1 had"),
        new Rule("\\b(she|he|you|they|i)['\u2019]ll", Pattern.CASE_INSENSITIVE, "$1 will"),
        new Rule("n['\u2019]t ", 0, " not "),
        new Rule("['\u2019]ve ", 0, " have "),
        new Rule("['\u2019]re ", 0, " are "),
    };

    // ---- public API -----------------------------------------------------------------

    public String[] tokens(String text, Map<String, Object> options) {
        Map<String, Object> opts = (options == null) ? Map.of() : options;
        String[] words = tokenize(text, opts);
        LinkedHashSet<String> map = new LinkedHashSet<>();
        for (String w : words) {
            if (!truthy(opts.get("caseSensitive"))) {
                w = w.toLowerCase();
            }
            if (truthy(opts.get("includePunct")) || ALPHA_RE.matcher(w).find()) {
                map.add(w);
            }
        }
        List<String> tokens = new ArrayList<>(map);
        if (truthy(opts.get("ignoreStopWords"))) {
            tokens.removeIf(t -> RiTa.isStopWord(t));
        }
        if (truthy(opts.get("sort"))) {
            tokens.sort(null);
        }
        return tokens.toArray(new String[0]);
    }

    public String[] tokens(String text) {
        return tokens(text, Map.of());
    }

    public String[] tokenize(String input, Map<String, Object> opts) {
        if (input == null) {
            return new String[0];
        }
        Map<String, Object> o = (opts == null) ? Map.of() : opts;

        Object regexOpt = o.get("regex");
        if (regexOpt instanceof Pattern) {
            return ((Pattern) regexOpt).split(input);
        }

        List<String> tags = new ArrayList<>();
        String text = pushTags(input.trim(), tags);

        for (Rule rule : TOKENIZE_RE) {
            text = apply(text, rule);
        }

        if (truthy(o.get("splitHyphens"))) {
            text = text.replaceAll("([a-zA-Z]+)-([a-zA-Z]+)", "$1 - $2");
        }

        if (RiTa.SPLIT_CONTRACTIONS || truthy(o.get("splitContractions"))) {
            for (Rule rule : CONTRACTS_RE) {
                text = apply(text, rule);
            }
        }

        String[] result = text.trim().split(WS_RE.pattern());
        return popTags(result, tags);
    }

    public String[] tokenize(String input) {
        return tokenize(input, Map.of());
    }

    public String untokenize(String[] input, String delim) {
        if (input == null) {
            return "";
        }
        String d = (delim == null) ? " " : delim;
        List<String> tokens = preProcessTags(input);

        State state = new State();
        state.withinQuote = !tokens.isEmpty() && QUOTE_RE.matcher(tokens.get(0)).find();

        String result = tokens.isEmpty() ? "" : (tokens.get(0) == null ? "" : tokens.get(0));
        for (int i = 1; i < tokens.size(); i++) {
            String curr = tokens.get(i);
            if (curr == null || curr.isEmpty()) {
                continue;
            }
            String prev = tokens.get(i - 1);
            String next = (i + 1 < tokens.size()) ? tokens.get(i + 1) : null;
            Object[] ns = nextState(prev, curr, next, i == tokens.size() - 1, state);
            boolean space = (Boolean) ns[0];
            boolean trailing = (Boolean) ns[1];
            state = (State) ns[2];
            result += (space ? d : "") + curr + (trailing ? d : "");
        }
        return result.trim();
    }

    public String untokenize(String[] input) {
        return untokenize(input, " ");
    }

    public String[] sentences(String text, String pattern) {
        if (text == null || text.isEmpty()) {
            return new String[] {text};
        }
        String clean = NL_RE.matcher(text).replaceAll(" ");
        String delim = "___";
        Pattern re = Pattern.compile(delim);
        Pattern splitter = (pattern != null) ? Pattern.compile(pattern) : SPLITTER;

        String escaped = escapeAbbrevs(clean, delim);
        List<String> arr = findAll(escaped, splitter);
        if (arr.isEmpty()) {
            return new String[] {text};
        }
        List<String> out = new ArrayList<>();
        for (String s : arr) {
            out.add(re.matcher(s).replaceAll("."));
        }
        return out.toArray(new String[0]);
    }

    public String[] sentences(String text) {
        return sentences(text, null);
    }

    // ---- internals ------------------------------------------------------------------

    private static String escapeAbbrevs(String text, String delim) {
        for (String abv : RiTa.ABRV) {
            int idx = text.indexOf(abv);
            while (idx > -1) {
                String repl = abv.replaceFirst("\\.", Matcher.quoteReplacement(delim));
                text = text.replaceFirst(Pattern.quote(abv), Matcher.quoteReplacement(repl));
                idx = text.indexOf(abv);
            }
        }
        return text;
    }

    private static List<String> findAll(String text, Pattern p) {
        List<String> out = new ArrayList<>();
        Matcher m = p.matcher(text);
        while (m.find()) {
            out.add(m.group());
        }
        return out;
    }

    private static String apply(String text, Rule rule) {
        Matcher m = rule.p.matcher(text);
        if (rule.fn != null) {
            StringBuilder sb = new StringBuilder();
            while (m.find()) {
                m.appendReplacement(sb, Matcher.quoteReplacement(rule.fn.apply(m.group())));
            }
            m.appendTail(sb);
            return sb.toString();
        }
        return rule.global ? m.replaceAll(rule.repl) : m.replaceFirst(rule.repl);
    }

    private static boolean truthy(Object o) {
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

    private String pushTags(String text, List<String> tags) {
        int tagIdx = 0;
        Matcher m = TAG_RE.matcher(text);
        while (m.find()) {
            tags.add(m.group());
            text = text.substring(0, m.start()) + " _" + TAG + (tagIdx++) + "_ " + text.substring(m.end());
            m = TAG_RE.matcher(text);
        }
        return text;
    }

    private String[] popTags(String[] result, List<String> tags) {
        for (int i = 0; i < result.length; i++) {
            if (POPTAG_RE.matcher(result[i]).find()) {
                result[i] = tags.remove(0);
            }
            if (ELLIPSIS_ENC_RE.matcher(result[i]).find()) {
                Matcher m = ELLIPSIS_ENC_RE.matcher(result[i]);
                StringBuffer sb = new StringBuffer();
                while (m.find()) {
                    String s = m.group(1).replace("\u2062", ".").replace("\u2063", " ");
                    m.appendReplacement(sb, Matcher.quoteReplacement(s));
                }
                m.appendTail(sb);
                result[i] = sb.toString();
            }
            if (result[i].contains("_") && !EMAIL_RE.matcher(result[i]).find()
                && !URL_RE.matcher(result[i]).find()) {
                result[i] = UNDER_RE.matcher(result[i]).replaceAll("$1 $2");
            }
        }
        return result;
    }

    private List<String> preProcessTags(String[] array) {
        List<String> result = new ArrayList<>();
        int currentIdx = 0;
        while (currentIdx < array.length) {
            String currentToken = array[currentIdx];
            if (!LT_RE.matcher(currentToken).find()) {
                result.add(currentToken);
                currentIdx++;
                continue;
            }
            List<String> subArray = new ArrayList<>();
            subArray.add(array[currentIdx]);
            int inspectIdx = currentIdx + 1;
            while (inspectIdx < array.length) {
                subArray.add(array[inspectIdx]);
                if (LT_RE.matcher(array[inspectIdx]).find()) {
                    break;
                }
                if (GT_RE.matcher(array[inspectIdx]).find()) {
                    break;
                }
                inspectIdx++;
            }
            String last = subArray.get(subArray.size() - 1);
            if (LT_RE.matcher(last).find()) {
                result.addAll(subArray.subList(0, subArray.size() - 1));
                currentIdx = inspectIdx;
                continue;
            }
            if (!GT_RE.matcher(last).find()) {
                result.addAll(subArray);
                currentIdx = inspectIdx + 1;
                continue;
            }
            if (!TAG_RE.matcher(String.join("", subArray)).find()) {
                result.addAll(subArray);
                currentIdx = inspectIdx + 1;
                continue;
            }
            result.add(tagSubarrayToString(subArray));
            currentIdx = inspectIdx + 1;
        }
        return result;
    }

    private String tagSubarrayToString(List<String> array) {
        if (!LT_RE.matcher(array.get(0)).find() || !GT_RE.matcher(array.get(array.size() - 1)).find()) {
            throw new RuntimeException(array + " is not a tag");
        }
        String start = array.get(0).trim();
        String end = array.get(array.size() - 1).trim();

        int inspectIdx = 1;
        while (inspectIdx < array.size() - 1 && TAGSTART_RE.matcher(array.get(inspectIdx)).find()) {
            start += array.get(inspectIdx).trim();
            inspectIdx++;
        }
        int contentStartIdx = inspectIdx;
        inspectIdx = array.size() - 2;
        while (inspectIdx > contentStartIdx && TAGEND_RE.matcher(array.get(inspectIdx)).find()) {
            end = array.get(inspectIdx).trim() + end;
            inspectIdx--;
        }
        int contentEndIdx = inspectIdx;
        List<String> content = new ArrayList<>(array.subList(contentStartIdx, contentEndIdx + 1));
        return start + untokenize(content.toArray(new String[0])).trim() + end;
    }

    /** Mutable decision-rule state, mirrors the JS state object. */
    private static final class State {
        boolean withinQuote;
        boolean afterQuote;
        boolean midSentence;
        boolean nextNoSpace;
    }

    private Object[] nextState(String prev, String curr, String next, boolean isLast, State state) {
        boolean withinQuote = state.withinQuote;
        boolean afterQuote = state.afterQuote;
        boolean midSentence = state.midSentence;
        boolean nextNoSpace = state.nextNoSpace;

        boolean thisNBPunct = NOSP_BF_PUNCT_RE.matcher(curr).find()
            || UNTAG_RE[2].matcher(curr).find() || LINEBREAK_RE.matcher(curr).find();
        boolean lastNBPunct = NOSP_BF_PUNCT_RE.matcher(prev).find()
            || LINEBREAK_RE.matcher(prev).find() || ELLIPSIS_RE.matcher(prev).find();
        boolean lastNAPunct = NOSP_AF_PUNCT_RE.matcher(prev).find()
            || UNTAG_RE[1].matcher(prev).find() || LINEBREAK_RE.matcher(prev).find();
        boolean thisLBracket = LB_RE.matcher(curr).find();
        boolean thisRBracket = RB_RE.matcher(curr).find();
        boolean lastLB = LB_RE.matcher(prev).find();
        boolean lastRB = RB_RE.matcher(prev).find();
        boolean thisQuote = QUOTE_RE.matcher(curr).find();
        boolean lastQuote = QUOTE_RE.matcher(prev).find();
        boolean thisComma = curr.equals(",");
        boolean lastComma = prev.equals(",");
        boolean thisLineBreak = LINEBREAK_RE.matcher(curr).find();
        boolean isDomain = DOMAIN_RE.matcher(curr).find();
        boolean lastIsWWW = WWW_RE.matcher(prev).find();
        boolean lastEndWithS = prev.length() > 0 && prev.charAt(prev.length() - 1) == 's'
            && !prev.equals("is") && !prev.equals("Is") && !prev.equals("IS");
        boolean nextIsS = "s".equals(next) || "S".equals(next);

        // URL domain continuation or deferred no-space
        if ((prev.equals(".") && isDomain) || nextNoSpace) {
            return new Object[] {false, false, newState(withinQuote, afterQuote, midSentence, false)};
        }

        // www.<domain>
        if (curr.equals(".") && lastIsWWW) {
            return new Object[] {false, false, newState(withinQuote, afterQuote, midSentence, true)};
        }

        // left bracket: always space before
        if (thisLBracket) {
            return new Object[] {true, false, newState(withinQuote, afterQuote, midSentence, nextNoSpace)};
        }

        // after right bracket
        if (lastRB) {
            boolean space = !thisNBPunct && !thisLBracket;
            return new Object[] {space, false, newState(withinQuote, afterQuote, midSentence, nextNoSpace)};
        }

        // trailing space: possessive apostrophe after plural
        boolean trailingSpace = thisNBPunct && !lastNBPunct && !withinQuote
            && SQUOTE_RE.matcher(curr).find() && lastEndWithS;

        // quote token
        if (thisQuote) {
            if (withinQuote) {
                return new Object[] {false, false, newState(false, true, midSentence, nextNoSpace)};
            }
            if ((APOS_RE.matcher(curr).find() && lastEndWithS) || (APOS_RE.matcher(curr).find() && nextIsS)) {
                return new Object[] {false, trailingSpace, newState(withinQuote, afterQuote, midSentence, nextNoSpace)};
            }
            return new Object[] {true, false, newState(true, false, midSentence, nextNoSpace)};
        }

        // first token after a closing quote
        if (afterQuote && !thisNBPunct) {
            return new Object[] {true, false, newState(withinQuote, false, midSentence, nextNoSpace)};
        }

        // "word," mid-sentence pattern
        if (lastQuote && thisComma) {
            return new Object[] {false, false, newState(withinQuote, afterQuote, true, nextNoSpace)};
        }
        if (midSentence && lastComma) {
            return new Object[] {true, false, newState(withinQuote, afterQuote, false, nextNoSpace)};
        }

        // period-run (ellipsis) and dash tokens
        if (ELLIPSIS_RE.matcher(curr).find() || DASH_RE.matcher(curr).find()) {
            boolean glue = !lastNBPunct && !prev.matches(".*\\.$");
            return new Object[] {!glue, false, newState(withinQuote, afterQuote, midSentence, nextNoSpace)};
        }

        // general case
        boolean generalSpace = (!thisNBPunct && !lastQuote && !lastNAPunct && !lastLB && !thisRBracket)
            || (!isLast && thisNBPunct && lastNBPunct && !lastNAPunct
                && !lastQuote && !lastLB && !thisRBracket && !thisLineBreak);

        return new Object[] {generalSpace, trailingSpace, newState(withinQuote, afterQuote, midSentence, nextNoSpace)};
    }

    private static State newState(boolean withinQuote, boolean afterQuote, boolean midSentence, boolean nextNoSpace) {
        State s = new State();
        s.withinQuote = withinQuote;
        s.afterQuote = afterQuote;
        s.midSentence = midSentence;
        s.nextNoSpace = nextNoSpace;
        return s;
    }
}
