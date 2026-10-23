"""
rita/stemmer.py — Snowball/Porter2 English stemmer
Python port of ritajs/src/stemmer.js
"""

# ── SnowballStemmer base ─────────────────────────────────────────────────────

class _SnowballStemmer:
    def __init__(self):
        self.bra = 0
        self.ket = 0
        self.limit = 0
        self.cursor = 0
        self.limit_backward = 0
        self.current = ""

    def set_current(self, word):
        self.current = word
        self.cursor = 0
        self.limit = len(word)
        self.limit_backward = 0
        self.bra = self.cursor
        self.ket = self.limit

    def get_current(self):
        result = self.current
        self.current = ""
        return result

    def in_grouping(self, s, mn, mx):
        if self.cursor < self.limit:
            ch = ord(self.current[self.cursor])
            if mn <= ch <= mx:
                ch -= mn
                if s[ch >> 3] & (0x1 << (ch & 0x7)):
                    self.cursor += 1
                    return True
        return False

    def in_grouping_b(self, s, mn, mx):
        if self.cursor > self.limit_backward:
            ch = ord(self.current[self.cursor - 1])
            if mn <= ch <= mx:
                ch -= mn
                if s[ch >> 3] & (0x1 << (ch & 0x7)):
                    self.cursor -= 1
                    return True
        return False

    def out_grouping(self, s, mn, mx):
        if self.cursor < self.limit:
            ch = ord(self.current[self.cursor])
            if ch > mx or ch < mn:
                self.cursor += 1
                return True
            ch -= mn
            if not (s[ch >> 3] & (0x1 << (ch & 0x7))):
                self.cursor += 1
                return True
        return False

    def out_grouping_b(self, s, mn, mx):
        if self.cursor > self.limit_backward:
            ch = ord(self.current[self.cursor - 1])
            if ch > mx or ch < mn:
                self.cursor -= 1
                return True
            ch -= mn
            if not (s[ch >> 3] & (0x1 << (ch & 0x7))):
                self.cursor -= 1
                return True
        return False

    def eq_s(self, s_size, s):
        if self.limit - self.cursor < s_size:
            return False
        for i in range(s_size):
            if ord(self.current[self.cursor + i]) != ord(s[i]):
                return False
        self.cursor += s_size
        return True

    def eq_s_b(self, s_size, s):
        if self.cursor - self.limit_backward < s_size:
            return False
        for i in range(s_size):
            if ord(self.current[self.cursor - s_size + i]) != ord(s[i]):
                return False
        self.cursor -= s_size
        return True

    def find_among(self, v, v_size):
        i, j = 0, v_size
        c, l = self.cursor, self.limit
        common_i = common_j = 0
        first_key_inspected = False
        while True:
            k = i + ((j - i) >> 1)
            diff = 0
            common = common_i if common_i < common_j else common_j
            w = v[k]
            for i2 in range(common, w.s_size):
                if c + common == l:
                    diff = -1
                    break
                diff = ord(self.current[c + common]) - w.s[i2]
                if diff:
                    break
                common += 1
            if diff < 0:
                j = k
                common_j = common
            else:
                i = k
                common_i = common
            if j - i <= 1:
                if i > 0 or j == i or first_key_inspected:
                    break
                first_key_inspected = True
        while True:
            w = v[i]
            if common_i >= w.s_size:
                self.cursor = c + w.s_size
                if not w.method:
                    return w.result
                res = w.method()
                self.cursor = c + w.s_size
                if res:
                    return w.result
            i = w.substring_i
            if i < 0:
                return 0

    def find_among_b(self, v, v_size):
        i, j = 0, v_size
        c, lb = self.cursor, self.limit_backward
        common_i = common_j = 0
        first_key_inspected = False
        while True:
            k = i + ((j - i) >> 1)
            diff = 0
            common = common_i if common_i < common_j else common_j
            w = v[k]
            for i2 in range(w.s_size - 1 - common, -1, -1):
                if c - common == lb:
                    diff = -1
                    break
                diff = ord(self.current[c - 1 - common]) - w.s[i2]
                if diff:
                    break
                common += 1
            if diff < 0:
                j = k
                common_j = common
            else:
                i = k
                common_i = common
            if j - i <= 1:
                if i > 0 or j == i or first_key_inspected:
                    break
                first_key_inspected = True
        while True:
            w = v[i]
            if common_i >= w.s_size:
                self.cursor = c - w.s_size
                if not w.method:
                    return w.result
                res = w.method()
                self.cursor = c - w.s_size
                if res:
                    return w.result
            i = w.substring_i
            if i < 0:
                return 0

    def replace_s(self, c_bra, c_ket, s):
        adjustment = len(s) - (c_ket - c_bra)
        self.current = self.current[:c_bra] + s + self.current[c_ket:]
        self.limit += adjustment
        if self.cursor >= c_ket:
            self.cursor += adjustment
        elif self.cursor > c_bra:
            self.cursor = c_bra
        return adjustment

    def slice_check(self):
        if (self.bra < 0 or self.bra > self.ket or
                self.ket > self.limit or self.limit > len(self.current)):
            raise Exception("faulty slice operation")

    def slice_from(self, s):
        self.slice_check()
        self.replace_s(self.bra, self.ket, s)

    def slice_del(self):
        self.slice_from("")

    def insert(self, c_bra, c_ket, s):
        adjustment = self.replace_s(c_bra, c_ket, s)
        if c_bra <= self.bra:
            self.bra += adjustment
        if c_bra <= self.ket:
            self.ket += adjustment

    def slice_to(self):
        self.slice_check()
        return self.current[self.bra:self.ket]

    def eq_v_b(self, s):
        return self.eq_s_b(len(s), s)


# ── Among ────────────────────────────────────────────────────────────────────

class _Among:
    def __init__(self, s, substring_i, result, method=None):
        self.s_size = len(s)
        self.s = [ord(c) for c in s]
        self.substring_i = substring_i
        self.result = result
        self.method = method


# ── Data tables ──────────────────────────────────────────────────────────────

_g_v     = [17, 65, 16, 1]
_g_v_WXY = [1, 17, 65, 208, 1]
_g_valid_LI = [55, 141, 2]

# ── Module-level state (mirrors JS module globals) ────────────────────────────
_impl = _SnowballStemmer()
_B_Y_found = False
_I_p1 = 0
_I_p2 = 0


# ── Porter2 rule functions ────────────────────────────────────────────────────

def _r_prelude():
    global _B_Y_found
    v_1 = _impl.cursor
    _B_Y_found = False
    _impl.bra = _impl.cursor
    if _impl.eq_s(1, "'"):
        _impl.ket = _impl.cursor
        _impl.slice_del()
    _impl.cursor = v_1
    _impl.bra = v_1
    if _impl.eq_s(1, "y"):
        _impl.ket = _impl.cursor
        _impl.slice_from("Y")
        _B_Y_found = True
    _impl.cursor = v_1
    while True:
        v_2 = _impl.cursor
        if _impl.in_grouping(_g_v, 97, 121):
            _impl.bra = _impl.cursor
            if _impl.eq_s(1, "y"):
                _impl.ket = _impl.cursor
                _impl.cursor = v_2
                _impl.slice_from("Y")
                _B_Y_found = True
                continue
        if v_2 >= _impl.limit:
            _impl.cursor = v_1
            return
        _impl.cursor = v_2 + 1


def _habr1():
    while not _impl.in_grouping(_g_v, 97, 121):
        if _impl.cursor >= _impl.limit:
            return True
        _impl.cursor += 1
    while not _impl.out_grouping(_g_v, 97, 121):
        if _impl.cursor >= _impl.limit:
            return True
        _impl.cursor += 1
    return False


def _r_mark_regions():
    global _I_p1, _I_p2
    v_1 = _impl.cursor
    _I_p1 = _impl.limit
    _I_p2 = _I_p1
    if not _impl.find_among(_a_0, 3):
        _impl.cursor = v_1
        if _habr1():
            _impl.cursor = v_1
            return
    _I_p1 = _impl.cursor
    if not _habr1():
        _I_p2 = _impl.cursor


def _r_shortv():
    v_1 = _impl.limit - _impl.cursor
    if not (_impl.out_grouping_b(_g_v_WXY, 89, 121) and
            _impl.in_grouping_b(_g_v, 97, 121) and
            _impl.out_grouping_b(_g_v, 97, 121)):
        _impl.cursor = _impl.limit - v_1
        if (not _impl.out_grouping_b(_g_v, 97, 121) or
                not _impl.in_grouping_b(_g_v, 97, 121) or
                _impl.cursor > _impl.limit_backward):
            return False
    return True


def _r_R1():
    return _I_p1 <= _impl.cursor


def _r_R2():
    return _I_p2 <= _impl.cursor


def _r_Step_1a():
    v_1 = _impl.limit - _impl.cursor
    _impl.ket = _impl.cursor
    among_var = _impl.find_among_b(_a_1, 3)
    if among_var:
        _impl.bra = _impl.cursor
        if among_var == 1:
            _impl.slice_del()
    else:
        _impl.cursor = _impl.limit - v_1
    _impl.ket = _impl.cursor
    among_var = _impl.find_among_b(_a_2, 6)
    if among_var:
        _impl.bra = _impl.cursor
        if among_var == 1:
            _impl.slice_from("ss")
        elif among_var == 2:
            c = _impl.cursor - 2
            if _impl.limit_backward > c or c > _impl.limit:
                _impl.slice_from("ie")
            else:
                _impl.cursor = c
                _impl.slice_from("i")
        elif among_var == 3:
            while True:
                if _impl.cursor <= _impl.limit_backward:
                    return
                _impl.cursor -= 1
                if _impl.in_grouping_b(_g_v, 97, 121):
                    break
            _impl.slice_del()


def _r_Step_1b():
    _impl.ket = _impl.cursor
    among_var = _impl.find_among_b(_a_4, 6)
    if among_var:
        _impl.bra = _impl.cursor
        if among_var == 1:
            if _r_R1():
                _impl.slice_from("ee")
        elif among_var == 2:
            v_1 = _impl.limit - _impl.cursor
            while not _impl.in_grouping_b(_g_v, 97, 121):
                if _impl.cursor <= _impl.limit_backward:
                    return
                _impl.cursor -= 1
            _impl.cursor = _impl.limit - v_1
            _impl.slice_del()
            v_3 = _impl.limit - _impl.cursor
            among_var2 = _impl.find_among_b(_a_3, 13)
            if among_var2:
                _impl.cursor = _impl.limit - v_3
                if among_var2 == 1:
                    c = _impl.cursor
                    _impl.insert(_impl.cursor, _impl.cursor, "e")
                    _impl.cursor = c
                elif among_var2 == 2:
                    _impl.ket = _impl.cursor
                    if _impl.cursor > _impl.limit_backward:
                        _impl.cursor -= 1
                        _impl.bra = _impl.cursor
                        _impl.slice_del()
                elif among_var2 == 3:
                    if _impl.cursor == _I_p1:
                        v_4 = _impl.limit - _impl.cursor
                        if _r_shortv():
                            _impl.cursor = _impl.limit - v_4
                            c = _impl.cursor
                            _impl.insert(_impl.cursor, _impl.cursor, "e")
                            _impl.cursor = c


def _r_Step_1c():
    v_1 = _impl.limit - _impl.cursor
    _impl.ket = _impl.cursor
    if not _impl.eq_s_b(1, "y"):
        _impl.cursor = _impl.limit - v_1
        if not _impl.eq_s_b(1, "Y"):
            return
    _impl.bra = _impl.cursor
    if (_impl.out_grouping_b(_g_v, 97, 121) and
            _impl.cursor > _impl.limit_backward):
        _impl.slice_from("i")


def _r_Step_2():
    _impl.ket = _impl.cursor
    among_var = _impl.find_among_b(_a_5, 24)
    if among_var:
        _impl.bra = _impl.cursor
        if _r_R1():
            _step2_map = {
                1: "tion", 2: "ence", 3: "ance", 4: "able", 5: "ent",
                6: "ize", 7: "ate", 8: "al", 9: "ful", 10: "ous",
                11: "ive", 12: "ble", 14: "ful", 15: "less",
            }
            if among_var in _step2_map:
                _impl.slice_from(_step2_map[among_var])
            elif among_var == 13:
                if _impl.eq_s_b(1, "l"):
                    _impl.slice_from("og")
            elif among_var == 16:
                if _impl.in_grouping_b(_g_valid_LI, 99, 116):
                    _impl.slice_del()


def _r_Step_3():
    _impl.ket = _impl.cursor
    among_var = _impl.find_among_b(_a_6, 9)
    if among_var:
        _impl.bra = _impl.cursor
        if _r_R1():
            _step3_map = {1: "tion", 2: "ate", 3: "al", 4: "ic"}
            if among_var in _step3_map:
                _impl.slice_from(_step3_map[among_var])
            elif among_var == 5:
                _impl.slice_del()
            elif among_var == 6:
                if _r_R2():
                    _impl.slice_del()


def _r_Step_4():
    _impl.ket = _impl.cursor
    among_var = _impl.find_among_b(_a_7, 18)
    if among_var:
        _impl.bra = _impl.cursor
        if _r_R2():
            if among_var == 1:
                _impl.slice_del()
            elif among_var == 2:
                v_1 = _impl.limit - _impl.cursor
                if not _impl.eq_s_b(1, "s"):
                    _impl.cursor = _impl.limit - v_1
                    if not _impl.eq_s_b(1, "t"):
                        return
                _impl.slice_del()


def _r_Step_5():
    _impl.ket = _impl.cursor
    among_var = _impl.find_among_b(_a_8, 2)
    if among_var:
        _impl.bra = _impl.cursor
        if among_var == 1:
            v_1 = _impl.limit - _impl.cursor
            if not _r_R2():
                _impl.cursor = _impl.limit - v_1
                if not _r_R1() or _r_shortv():
                    return
                _impl.cursor = _impl.limit - v_1
            _impl.slice_del()
        elif among_var == 2:
            if not _r_R2() or not _impl.eq_s_b(1, "l"):
                return
            _impl.slice_del()


def _r_exception2():
    _impl.ket = _impl.cursor
    if _impl.find_among_b(_a_9, 8):
        _impl.bra = _impl.cursor
        return _impl.cursor <= _impl.limit_backward
    return False


def _r_exception1():
    _impl.bra = _impl.cursor
    among_var = _impl.find_among(_a_10, 18)
    if among_var:
        _impl.ket = _impl.cursor
        if _impl.cursor >= _impl.limit:
            _exc1_map = {
                1: "ski", 2: "sky", 3: "die", 4: "lie", 5: "tie",
                6: "idl", 7: "gentl", 8: "ugli", 9: "earli",
                10: "onli", 11: "singl",
            }
            if among_var in _exc1_map:
                _impl.slice_from(_exc1_map[among_var])
            return True
    return False


def _r_postlude():
    if _B_Y_found:
        while True:
            v_1 = _impl.cursor
            _impl.bra = v_1
            if _impl.eq_s(1, "Y"):
                _impl.ket = _impl.cursor
                _impl.cursor = v_1
                _impl.slice_from("y")
                continue
            _impl.cursor = v_1
            if _impl.cursor >= _impl.limit:
                return
            _impl.cursor += 1


# ── Among tables (defined after functions so methods can reference them) ─────

_a_0 = [
    _Among("arsen", -1, -1),
    _Among("commun", -1, -1),
    _Among("gener", -1, -1),
]
_a_1 = [
    _Among("'", -1, 1),
    _Among("'s'", 0, 1),
    _Among("'s", -1, 1),
]
_a_2 = [
    _Among("ied", -1, 2),
    _Among("s", -1, 3),
    _Among("ies", 1, 2),
    _Among("sses", 1, 1),
    _Among("ss", 1, -1),
    _Among("us", 1, -1),
]
_a_3 = [
    _Among("", -1, 3),
    _Among("bb", 0, 2),
    _Among("dd", 0, 2),
    _Among("ff", 0, 2),
    _Among("gg", 0, 2),
    _Among("bl", 0, 1),
    _Among("mm", 0, 2),
    _Among("nn", 0, 2),
    _Among("pp", 0, 2),
    _Among("rr", 0, 2),
    _Among("at", 0, 1),
    _Among("tt", 0, 2),
    _Among("iz", 0, 1),
]
_a_4 = [
    _Among("ed", -1, 2),
    _Among("eed", 0, 1),
    _Among("ing", -1, 2),
    _Among("edly", -1, 2),
    _Among("eedly", 3, 1),
    _Among("ingly", -1, 2),
]
_a_5 = [
    _Among("anci", -1, 3),
    _Among("enci", -1, 2),
    _Among("ogi", -1, 13),
    _Among("li", -1, 16),
    _Among("bli", 3, 12),
    _Among("abli", 4, 4),
    _Among("alli", 3, 8),
    _Among("fulli", 3, 14),
    _Among("lessli", 3, 15),
    _Among("ousli", 3, 10),
    _Among("entli", 3, 5),
    _Among("aliti", -1, 8),
    _Among("biliti", -1, 12),
    _Among("iviti", -1, 11),
    _Among("tional", -1, 1),
    _Among("ational", 14, 7),
    _Among("alism", -1, 8),
    _Among("ation", -1, 7),
    _Among("ization", 17, 6),
    _Among("izer", -1, 6),
    _Among("ator", -1, 7),
    _Among("iveness", -1, 11),
    _Among("fulness", -1, 9),
    _Among("ousness", -1, 10),
]
_a_6 = [
    _Among("icate", -1, 4),
    _Among("ative", -1, 6),
    _Among("alize", -1, 3),
    _Among("iciti", -1, 4),
    _Among("ical", -1, 4),
    _Among("tional", -1, 1),
    _Among("ational", 5, 2),
    _Among("ful", -1, 5),
    _Among("ness", -1, 5),
]
_a_7 = [
    _Among("ic", -1, 1),
    _Among("ance", -1, 1),
    _Among("ence", -1, 1),
    _Among("able", -1, 1),
    _Among("ible", -1, 1),
    _Among("ate", -1, 1),
    _Among("ive", -1, 1),
    _Among("ize", -1, 1),
    _Among("iti", -1, 1),
    _Among("al", -1, 1),
    _Among("ism", -1, 1),
    _Among("ion", -1, 2),
    _Among("er", -1, 1),
    _Among("ous", -1, 1),
    _Among("ant", -1, 1),
    _Among("ent", -1, 1),
    _Among("ment", 15, 1),
    _Among("ement", 16, 1),
]
_a_8 = [
    _Among("e", -1, 1),
    _Among("l", -1, 2),
]
_a_9 = [
    _Among("succeed", -1, -1),
    _Among("proceed", -1, -1),
    _Among("exceed", -1, -1),
    _Among("canning", -1, -1),
    _Among("inning", -1, -1),
    _Among("earring", -1, -1),
    _Among("herring", -1, -1),
    _Among("outing", -1, -1),
]
_a_10 = [
    _Among("andes", -1, -1),
    _Among("atlas", -1, -1),
    _Among("bias", -1, -1),
    _Among("cosmos", -1, -1),
    _Among("dying", -1, 3),
    _Among("early", -1, 9),
    _Among("gently", -1, 7),
    _Among("howe", -1, -1),
    _Among("idly", -1, 6),
    _Among("lying", -1, 4),
    _Among("news", -1, -1),
    _Among("only", -1, 10),
    _Among("singly", -1, 11),
    _Among("skies", -1, 2),
    _Among("skis", -1, 1),
    _Among("sky", -1, -1),
    _Among("tying", -1, 5),
    _Among("ugly", -1, 8),
]

_habr = [_r_Step_1b, _r_Step_1c, _r_Step_2, _r_Step_3, _r_Step_4, _r_Step_5]


# ── Stemmer public class ──────────────────────────────────────────────────────

class Stemmer:
    """Porter2/Snowball English stemmer."""

    _tokenizer = None  # lazy-initialised on first multi-word call

    @staticmethod
    def _get_tokenizer():
        if Stemmer._tokenizer is None:
            from rita.tokenizer import Tokenizer
            Stemmer._tokenizer = Tokenizer()
        return Stemmer._tokenizer

    @staticmethod
    def stem(word: str) -> str:
        if not isinstance(word, str):
            raise TypeError("Expects string")
        if " " not in word:
            return Stemmer._stem_english(word)
        tok = Stemmer._get_tokenizer()
        words = tok.tokenize(word)
        stems = Stemmer.stem_all(words)
        return tok.untokenize(stems)

    @staticmethod
    def stem_all(words):
        return [Stemmer._stem_english(w) for w in words]

    @staticmethod
    def _stem_english(word: str) -> str:
        global _B_Y_found, _I_p1, _I_p2
        _impl.set_current(word)
        v_1 = _impl.cursor
        if not _r_exception1():
            _impl.cursor = v_1
            c = _impl.cursor + 3
            if 0 <= c <= _impl.limit:
                _impl.cursor = v_1
                _r_prelude()
                _impl.cursor = v_1
                _r_mark_regions()
                _impl.limit_backward = v_1
                _impl.cursor = _impl.limit
                _r_Step_1a()
                _impl.cursor = _impl.limit
                if not _r_exception2():
                    for fn in _habr:
                        _impl.cursor = _impl.limit
                        fn()
                _impl.cursor = _impl.limit_backward
                _r_postlude()
        return _impl.get_current()
