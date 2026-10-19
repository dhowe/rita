package rita;

import java.util.ArrayList;
import java.util.List;

/**
 * Stemmer — port of {@code js/src/stemmer.js} (the Snowball English stemmer).
 *
 * <p>Structure mirrors the JS: a {@code SnowballStemmer} primitive-operation base, an {@code Among}
 * table entry, the {@code a_N} among tables, and the {@code r_*} step functions. JS drives this via
 * a single shared {@code Stemmer.impl} plus module-level {@code I_p1/I_p2/B_Y_found}; here each call
 * runs a fresh {@link Engine} holding that state, which is behaviourally identical and avoids
 * shared-state hazards.
 */
public final class Stemmer {

    private Stemmer() {
    }

    /** JS {@code Stemmer.stem} — single word, or tokenize/stem/untokenize for multi-word input. */
    public static String stem(String input) {
        if (input == null) {
            throw new RuntimeException("Expects string");
        }
        if (!input.contains(" ")) {
            return stemEnglish(input);
        }
        String[] words = RiTa.tokenize(input);
        String[] stems = stemAll(words);
        return RiTa.untokenize(stems);
    }

    /** JS {@code Stemmer.stemAll}. */
    public static String[] stemAll(String[] input) {
        String[] out = new String[input.length];
        for (int i = 0; i < input.length; i++) {
            out[i] = stemEnglish(input[i]);
        }
        return out;
    }

    /** JS {@code Stemmer.stemEnglish}. */
    public static String stemEnglish(String word) {
        Engine e = new Engine();
        e.setCurrent(word);
        int v1 = e.cursor;
        if (!e.rException1()) {
            e.cursor = v1;
            int c = e.cursor + 3;
            if (0 <= c && c <= e.limit) {
                e.cursor = v1;
                e.rPrelude();
                e.cursor = v1;
                e.rMarkRegions();
                e.limitBackward = v1;
                e.cursor = e.limit;
                e.rStep1a();
                e.cursor = e.limit;
                if (!e.rException2()) {
                    Runnable[] habr = {e::rStep1b, e::rStep1c, e::rStep2, e::rStep3, e::rStep4, e::rStep5};
                    for (Runnable step : habr) {
                        e.cursor = e.limit;
                        step.run();
                    }
                }
                e.cursor = e.limitBackward;
                e.rPostlude();
            }
        }
        return e.getCurrent();
    }

    // ---- Among ----------------------------------------------------------------------

    static final class Among {
        final int sSize;
        final int[] s;
        final int substringI;
        final int result;

        Among(String s, int substringI, int result) {
            this.sSize = s.length();
            this.s = new int[s.length()];
            for (int i = 0; i < s.length(); i++) {
                this.s[i] = s.charAt(i);
            }
            this.substringI = substringI;
            this.result = result;
        }
    }

    // ---- grouping tables ------------------------------------------------------------

    static final int[] G_V = {17, 65, 16, 1};
    static final int[] G_V_WXY = {1, 17, 65, 208, 1};
    static final int[] G_VALID_LI = {55, 141, 2};

    // ---- among tables ---------------------------------------------------------------

    static final Among[] A0 = {new Among("arsen", -1, -1), new Among("commun", -1, -1), new Among("gener", -1, -1)};
    static final Among[] A1 = {new Among("'", -1, 1), new Among("'s'", 0, 1), new Among("'s", -1, 1)};
    static final Among[] A2 = {new Among("ied", -1, 2), new Among("s", -1, 3), new Among("ies", 1, 2),
        new Among("sses", 1, 1), new Among("ss", 1, -1), new Among("us", 1, -1)};
    static final Among[] A3 = {new Among("", -1, 3), new Among("bb", 0, 2), new Among("dd", 0, 2),
        new Among("ff", 0, 2), new Among("gg", 0, 2), new Among("bl", 0, 1), new Among("mm", 0, 2),
        new Among("nn", 0, 2), new Among("pp", 0, 2), new Among("rr", 0, 2), new Among("at", 0, 1),
        new Among("tt", 0, 2), new Among("iz", 0, 1)};
    static final Among[] A4 = {new Among("ed", -1, 2), new Among("eed", 0, 1), new Among("ing", -1, 2),
        new Among("edly", -1, 2), new Among("eedly", 3, 1), new Among("ingly", -1, 2)};
    static final Among[] A5 = {new Among("anci", -1, 3), new Among("enci", -1, 2), new Among("ogi", -1, 13),
        new Among("li", -1, 16), new Among("bli", 3, 12), new Among("abli", 4, 4), new Among("alli", 3, 8),
        new Among("fulli", 3, 14), new Among("lessli", 3, 15), new Among("ousli", 3, 10),
        new Among("entli", 3, 5), new Among("aliti", -1, 8), new Among("biliti", -1, 12),
        new Among("iviti", -1, 11), new Among("tional", -1, 1), new Among("ational", 14, 7),
        new Among("alism", -1, 8), new Among("ation", -1, 7), new Among("ization", 17, 6),
        new Among("izer", -1, 6), new Among("ator", -1, 7), new Among("iveness", -1, 11),
        new Among("fulness", -1, 9), new Among("ousness", -1, 10)};
    static final Among[] A6 = {new Among("icate", -1, 4), new Among("ative", -1, 6), new Among("alize", -1, 3),
        new Among("iciti", -1, 4), new Among("ical", -1, 4), new Among("tional", -1, 1),
        new Among("ational", 5, 2), new Among("ful", -1, 5), new Among("ness", -1, 5)};
    static final Among[] A7 = {new Among("ic", -1, 1), new Among("ance", -1, 1), new Among("ence", -1, 1),
        new Among("able", -1, 1), new Among("ible", -1, 1), new Among("ate", -1, 1), new Among("ive", -1, 1),
        new Among("ize", -1, 1), new Among("iti", -1, 1), new Among("al", -1, 1), new Among("ism", -1, 1),
        new Among("ion", -1, 2), new Among("er", -1, 1), new Among("ous", -1, 1), new Among("ant", -1, 1),
        new Among("ent", -1, 1), new Among("ment", 15, 1), new Among("ement", 16, 1)};
    static final Among[] A8 = {new Among("e", -1, 1), new Among("l", -1, 2)};
    static final Among[] A9 = {new Among("succeed", -1, -1), new Among("proceed", -1, -1),
        new Among("exceed", -1, -1), new Among("canning", -1, -1), new Among("inning", -1, -1),
        new Among("earring", -1, -1), new Among("herring", -1, -1), new Among("outing", -1, -1)};
    static final Among[] A10 = {new Among("andes", -1, -1), new Among("atlas", -1, -1), new Among("bias", -1, -1),
        new Among("cosmos", -1, -1), new Among("dying", -1, 3), new Among("early", -1, 9),
        new Among("gently", -1, 7), new Among("howe", -1, -1), new Among("idly", -1, 6),
        new Among("lying", -1, 4), new Among("news", -1, -1), new Among("only", -1, 10),
        new Among("singly", -1, 11), new Among("skies", -1, 2), new Among("skis", -1, 1), new Among("sky", -1, -1),
        new Among("tying", -1, 5), new Among("ugly", -1, 8)};

    // ---- engine (Snowball primitives + English steps) -------------------------------

    static final class Engine {
        int bra;
        int ket;
        int limit;
        int cursor;
        int limitBackward;
        String current;

        int i_p1;
        int i_p2;
        boolean bYFound;

        void setCurrent(String word) {
            current = word;
            cursor = 0;
            limit = word.length();
            limitBackward = 0;
            bra = cursor;
            ket = limit;
        }

        String getCurrent() {
            String result = current;
            current = null;
            return result;
        }

        // ---- primitives -------------------------------------------------------------

        boolean inGrouping(int[] s, int min, int max) {
            if (cursor < limit) {
                int ch = current.charAt(cursor);
                if (ch <= max && ch >= min) {
                    ch -= min;
                    if ((s[ch >> 3] & (0X1 << (ch & 0X7))) != 0) {
                        cursor++;
                        return true;
                    }
                }
            }
            return false;
        }

        boolean inGroupingB(int[] s, int min, int max) {
            if (cursor > limitBackward) {
                int ch = current.charAt(cursor - 1);
                if (ch <= max && ch >= min) {
                    ch -= min;
                    if ((s[ch >> 3] & (0X1 << (ch & 0X7))) != 0) {
                        cursor--;
                        return true;
                    }
                }
            }
            return false;
        }

        boolean outGrouping(int[] s, int min, int max) {
            if (cursor < limit) {
                int ch = current.charAt(cursor);
                if (ch > max || ch < min) {
                    cursor++;
                    return true;
                }
                ch -= min;
                if ((s[ch >> 3] & (0X1 << (ch & 0X7))) == 0) {
                    cursor++;
                    return true;
                }
            }
            return false;
        }

        boolean outGroupingB(int[] s, int min, int max) {
            if (cursor > limitBackward) {
                int ch = current.charAt(cursor - 1);
                if (ch > max || ch < min) {
                    cursor--;
                    return true;
                }
                ch -= min;
                if ((s[ch >> 3] & (0X1 << (ch & 0X7))) == 0) {
                    cursor--;
                    return true;
                }
            }
            return false;
        }

        boolean eqS(int sSize, String s) {
            if (limit - cursor < sSize) {
                return false;
            }
            for (int i = 0; i < sSize; i++) {
                if (current.charAt(cursor + i) != s.charAt(i)) {
                    return false;
                }
            }
            cursor += sSize;
            return true;
        }

        boolean eqSB(int sSize, String s) {
            if (cursor - limitBackward < sSize) {
                return false;
            }
            for (int i = 0; i < sSize; i++) {
                if (current.charAt(cursor - sSize + i) != s.charAt(i)) {
                    return false;
                }
            }
            cursor -= sSize;
            return true;
        }

        int findAmong(Among[] v) {
            int i = 0, j = v.length, c = cursor, l = limit, commonI = 0, commonJ = 0;
            boolean firstKeyInspected = false;
            while (true) {
                int k = i + ((j - i) >> 1), diff = 0, common = commonI < commonJ ? commonI : commonJ;
                Among w = v[k];
                for (int i2 = common; i2 < w.sSize; i2++) {
                    if (c + common == l) {
                        diff = -1;
                        break;
                    }
                    diff = current.charAt(c + common) - w.s[i2];
                    if (diff != 0) {
                        break;
                    }
                    common++;
                }
                if (diff < 0) {
                    j = k;
                    commonJ = common;
                } else {
                    i = k;
                    commonI = common;
                }
                if (j - i <= 1) {
                    if (i > 0 || j == i || firstKeyInspected) {
                        break;
                    }
                    firstKeyInspected = true;
                }
            }
            while (true) {
                Among w = v[i];
                if (commonI >= w.sSize) {
                    cursor = c + w.sSize;
                    if (w.result != 0) {
                        return w.result;
                    }
                }
                i = w.substringI;
                if (i < 0) {
                    return 0;
                }
            }
        }

        int findAmongB(Among[] v) {
            int i = 0, j = v.length, c = cursor, lb = limitBackward, commonI = 0, commonJ = 0;
            boolean firstKeyInspected = false;
            while (true) {
                int k = i + ((j - i) >> 1), diff = 0, common = commonI < commonJ ? commonI : commonJ;
                Among w = v[k];
                for (int i2 = w.sSize - 1 - common; i2 >= 0; i2--) {
                    if (c - common == lb) {
                        diff = -1;
                        break;
                    }
                    diff = current.charAt(c - 1 - common) - w.s[i2];
                    if (diff != 0) {
                        break;
                    }
                    common++;
                }
                if (diff < 0) {
                    j = k;
                    commonJ = common;
                } else {
                    i = k;
                    commonI = common;
                }
                if (j - i <= 1) {
                    if (i > 0 || j == i || firstKeyInspected) {
                        break;
                    }
                    firstKeyInspected = true;
                }
            }
            while (true) {
                Among w = v[i];
                if (commonI >= w.sSize) {
                    cursor = c - w.sSize;
                    if (w.result != 0) {
                        return w.result;
                    }
                }
                i = w.substringI;
                if (i < 0) {
                    return 0;
                }
            }
        }

        int replaceS(int cBra, int cKet, String s) {
            int adjustment = s.length() - (cKet - cBra);
            String left = current.substring(0, cBra);
            String right = current.substring(cKet);
            current = left + s + right;
            limit += adjustment;
            if (cursor >= cKet) {
                cursor += adjustment;
            } else if (cursor > cBra) {
                cursor = cBra;
            }
            return adjustment;
        }

        void sliceCheck() {
            if (bra < 0 || bra > ket || ket > limit || limit > current.length()) {
                throw new RuntimeException("faulty slice operation");
            }
        }

        void sliceFrom(String s) {
            sliceCheck();
            replaceS(bra, ket, s);
        }

        void sliceDel() {
            sliceFrom("");
        }

        void insert(int cBra, int cKet, String s) {
            int adjustment = replaceS(cBra, cKet, s);
            if (cBra <= bra) {
                bra += adjustment;
            }
            if (cBra <= ket) {
                ket += adjustment;
            }
        }

        // ---- steps ------------------------------------------------------------------

        void rPrelude() {
            int v1 = cursor;
            bYFound = false;
            bra = cursor;
            if (eqS(1, "'")) {
                ket = cursor;
                sliceDel();
            }
            cursor = v1;
            bra = v1;
            if (eqS(1, "y")) {
                ket = cursor;
                sliceFrom("Y");
                bYFound = true;
            }
            cursor = v1;
            while (true) {
                int v2 = cursor;
                if (inGrouping(G_V, 97, 121)) {
                    bra = cursor;
                    if (eqS(1, "y")) {
                        ket = cursor;
                        cursor = v2;
                        sliceFrom("Y");
                        bYFound = true;
                        continue;
                    }
                }
                if (v2 >= limit) {
                    cursor = v1;
                    return;
                }
                cursor = v2 + 1;
            }
        }

        void rMarkRegions() {
            int v1 = cursor;
            i_p1 = limit;
            i_p2 = i_p1;
            if (findAmong(A0) == 0) {
                cursor = v1;
                if (habr1()) {
                    cursor = v1;
                    return;
                }
            }
            i_p1 = cursor;
            if (!habr1()) {
                i_p2 = cursor;
            }
        }

        boolean habr1() {
            while (!inGrouping(G_V, 97, 121)) {
                if (cursor >= limit) {
                    return true;
                }
                cursor++;
            }
            while (!outGrouping(G_V, 97, 121)) {
                if (cursor >= limit) {
                    return true;
                }
                cursor++;
            }
            return false;
        }

        boolean rShortv() {
            int v1 = limit - cursor;
            if (!(outGroupingB(G_V_WXY, 89, 121) && inGroupingB(G_V, 97, 121)
                && outGroupingB(G_V, 97, 121))) {
                cursor = limit - v1;
                if (!outGroupingB(G_V, 97, 121) || !inGroupingB(G_V, 97, 121)
                    || cursor > limitBackward) {
                    return false;
                }
            }
            return true;
        }

        boolean rR1() {
            return i_p1 <= cursor;
        }

        boolean rR2() {
            return i_p2 <= cursor;
        }

        void rStep1a() {
            int amongVar, v1 = limit - cursor;
            ket = cursor;
            amongVar = findAmongB(A1);
            if (amongVar != 0) {
                bra = cursor;
                if (amongVar == 1) {
                    sliceDel();
                }
            } else {
                cursor = limit - v1;
            }
            ket = cursor;
            amongVar = findAmongB(A2);
            if (amongVar != 0) {
                bra = cursor;
                switch (amongVar) {
                    case 1:
                        sliceFrom("ss");
                        break;
                    case 2:
                        int c = cursor - 2;
                        if (limitBackward > c || c > limit) {
                            sliceFrom("ie");
                            break;
                        }
                        cursor = c;
                        sliceFrom("i");
                        break;
                    case 3:
                        do {
                            if (cursor <= limitBackward) {
                                return;
                            }
                            cursor--;
                        } while (!inGroupingB(G_V, 97, 121));
                        sliceDel();
                        break;
                    default:
                        break;
                }
            }
        }

        void rStep1b() {
            int amongVar, v1, v3, v4;
            ket = cursor;
            amongVar = findAmongB(A4);
            if (amongVar != 0) {
                bra = cursor;
                switch (amongVar) {
                    case 1:
                        if (rR1()) {
                            sliceFrom("ee");
                        }
                        break;
                    case 2:
                        v1 = limit - cursor;
                        while (!inGroupingB(G_V, 97, 121)) {
                            if (cursor <= limitBackward) {
                                return;
                            }
                            cursor--;
                        }
                        cursor = limit - v1;
                        sliceDel();
                        v3 = limit - cursor;
                        amongVar = findAmongB(A3);
                        if (amongVar != 0) {
                            cursor = limit - v3;
                            switch (amongVar) {
                                case 1: {
                                    int c = cursor;
                                    insert(cursor, cursor, "e");
                                    cursor = c;
                                    break;
                                }
                                case 2:
                                    ket = cursor;
                                    if (cursor > limitBackward) {
                                        cursor--;
                                        bra = cursor;
                                        sliceDel();
                                    }
                                    break;
                                case 3:
                                    if (cursor == i_p1) {
                                        v4 = limit - cursor;
                                        if (rShortv()) {
                                            cursor = limit - v4;
                                            int c = cursor;
                                            insert(cursor, cursor, "e");
                                            cursor = c;
                                        }
                                    }
                                    break;
                                default:
                                    break;
                            }
                        }
                        break;
                    default:
                        break;
                }
            }
        }

        void rStep1c() {
            int v1 = limit - cursor;
            ket = cursor;
            if (!eqSB(1, "y")) {
                cursor = limit - v1;
                if (!eqSB(1, "Y")) {
                    return;
                }
            }
            bra = cursor;
            if (outGroupingB(G_V, 97, 121) && cursor > limitBackward) {
                sliceFrom("i");
            }
        }

        void rStep2() {
            int amongVar;
            ket = cursor;
            amongVar = findAmongB(A5);
            if (amongVar != 0) {
                bra = cursor;
                if (rR1()) {
                    switch (amongVar) {
                        case 1:
                            sliceFrom("tion");
                            break;
                        case 2:
                            sliceFrom("ence");
                            break;
                        case 3:
                            sliceFrom("ance");
                            break;
                        case 4:
                            sliceFrom("able");
                            break;
                        case 5:
                            sliceFrom("ent");
                            break;
                        case 6:
                            sliceFrom("ize");
                            break;
                        case 7:
                            sliceFrom("ate");
                            break;
                        case 8:
                            sliceFrom("al");
                            break;
                        case 9:
                            sliceFrom("ful");
                            break;
                        case 10:
                            sliceFrom("ous");
                            break;
                        case 11:
                            sliceFrom("ive");
                            break;
                        case 12:
                            sliceFrom("ble");
                            break;
                        case 13:
                            if (eqSB(1, "l")) {
                                sliceFrom("og");
                            }
                            break;
                        case 14:
                            sliceFrom("ful");
                            break;
                        case 15:
                            sliceFrom("less");
                            break;
                        case 16:
                            if (inGroupingB(G_VALID_LI, 99, 116)) {
                                sliceDel();
                            }
                            break;
                        default:
                            break;
                    }
                }
            }
        }

        void rStep3() {
            int amongVar;
            ket = cursor;
            amongVar = findAmongB(A6);
            if (amongVar != 0) {
                bra = cursor;
                if (rR1()) {
                    switch (amongVar) {
                        case 1:
                            sliceFrom("tion");
                            break;
                        case 2:
                            sliceFrom("ate");
                            break;
                        case 3:
                            sliceFrom("al");
                            break;
                        case 4:
                            sliceFrom("ic");
                            break;
                        case 5:
                            sliceDel();
                            break;
                        case 6:
                            if (rR2()) {
                                sliceDel();
                            }
                            break;
                        default:
                            break;
                    }
                }
            }
        }

        void rStep4() {
            int amongVar, v1;
            ket = cursor;
            amongVar = findAmongB(A7);
            if (amongVar != 0) {
                bra = cursor;
                if (rR2()) {
                    switch (amongVar) {
                        case 1:
                            sliceDel();
                            break;
                        case 2:
                            v1 = limit - cursor;
                            if (!eqSB(1, "s")) {
                                cursor = limit - v1;
                                if (!eqSB(1, "t")) {
                                    return;
                                }
                            }
                            sliceDel();
                            break;
                        default:
                            break;
                    }
                }
            }
        }

        void rStep5() {
            int amongVar, v1;
            ket = cursor;
            amongVar = findAmongB(A8);
            if (amongVar != 0) {
                bra = cursor;
                switch (amongVar) {
                    case 1:
                        v1 = limit - cursor;
                        if (!rR2()) {
                            cursor = limit - v1;
                            if (!rR1() || rShortv()) {
                                return;
                            }
                            cursor = limit - v1;
                        }
                        sliceDel();
                        break;
                    case 2:
                        if (!rR2() || !eqSB(1, "l")) {
                            return;
                        }
                        sliceDel();
                        break;
                    default:
                        break;
                }
            }
        }

        boolean rException2() {
            ket = cursor;
            if (findAmongB(A9) != 0) {
                bra = cursor;
                return cursor <= limitBackward;
            }
            return false;
        }

        boolean rException1() {
            int amongVar;
            bra = cursor;
            amongVar = findAmong(A10);
            if (amongVar != 0) {
                ket = cursor;
                if (cursor >= limit) {
                    switch (amongVar) {
                        case 1:
                            sliceFrom("ski");
                            break;
                        case 2:
                            sliceFrom("sky");
                            break;
                        case 3:
                            sliceFrom("die");
                            break;
                        case 4:
                            sliceFrom("lie");
                            break;
                        case 5:
                            sliceFrom("tie");
                            break;
                        case 6:
                            sliceFrom("idl");
                            break;
                        case 7:
                            sliceFrom("gentl");
                            break;
                        case 8:
                            sliceFrom("ugli");
                            break;
                        case 9:
                            sliceFrom("earli");
                            break;
                        case 10:
                            sliceFrom("onli");
                            break;
                        case 11:
                            sliceFrom("singl");
                            break;
                        default:
                            break;
                    }
                    return true;
                }
            }
            return false;
        }

        void rPostlude() {
            if (bYFound) {
                while (true) {
                    int v1 = cursor;
                    bra = v1;
                    if (eqS(1, "Y")) {
                        ket = cursor;
                        cursor = v1;
                        sliceFrom("y");
                        continue;
                    }
                    cursor = v1;
                    if (cursor >= limit) {
                        return;
                    }
                    cursor++;
                }
            }
        }
    }
}
