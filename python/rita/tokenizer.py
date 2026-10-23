"""
rita/tokenizer.py — Tokenizer for RiTa

Python port of ritajs/src/tokenizer.js
"""

import re


# ---------------------------------------------------------------------------
# Default stop words (mirrors RiTa.STOP_WORDS in ritajs/src/rita.js)
# ---------------------------------------------------------------------------
_STOP_WORDS = {
    "and", "a", "of", "in", "i", "you", "is", "to", "that", "it", "for", "on",
    "have", "with", "this", "be", "not", "are", "as", "was", "but", "or", "from",
    "my", "at", "if", "they", "your", "all", "he", "by", "one", "me", "what", "so",
    "can", "will", "do", "an", "about", "we", "just", "would", "there", "no", "like",
    "out", "his", "has", "up", "more", "who", "when", "don't", "some", "had", "them",
    "any", "their", "it's", "only", "which", "i'm", "been", "other", "were", "how",
    "then", "now", "her", "than", "she", "well", "also", "us", "very", "because",
    "am", "here", "could", "even", "him", "into", "our", "much", "too", "did",
    "should", "over", "want", "these", "may", "where", "most", "many", "those",
    "does", "why", "please", "off", "going", "its", "i've", "down", "that's",
    "can't", "you're", "didn't", "another", "around", "must", "few", "doesn't",
    "the", "every", "yes", "each", "maybe", "i'll", "away", "doing", "oh", "else",
    "isn't", "he's", "there's", "hi", "won't", "ok", "they're", "yeah", "mine",
    "we're", "what's", "shall", "she's", "hello", "okay", "here's", "less",
    "said", "under",
}

# ---------------------------------------------------------------------------
# Compiled regex constants (mirrors JS consts at bottom of tokenizer.js)
# ---------------------------------------------------------------------------

_UNTAG_RE = [
    re.compile(r'^ *<[a-z][a-z0-9=\'"#;:&\s\-\+\/\.\?]*\/> *$', re.I),   # <br/>
    re.compile(r'^ *<([a-z][a-z0-9=\'"#;:&\s\-\+\/\.\?]*[a-z0-9=\'"#;:&\s\-\+\.\?]|[a-z])> *$', re.I),  # <a>
    re.compile(r'^ *<\/[a-z][a-z0-9=\'"#;:&\s\-\+\/\.\?]*> *$', re.I),   # </a>
    re.compile(r'^ *<!DOCTYPE[^>]*> *$', re.I),
    re.compile(r'^ *<!--[^->]*--> *$'),
]

_LT_RE         = re.compile(r'^ *< *$')
_GT_RE         = re.compile(r'^ *> *$')
_TAGSTART_RE   = re.compile(r'^ *[!\-\/] *$')
_TAGEND_RE     = re.compile(r'^ *[\-\/] *$')
_NOSP_AF_RE    = re.compile(r'^[\^\*\$\/\u2044#\-@\u00b0\u2012\u2013\u2014]+$')
_LB_RE         = re.compile(r'^[\[\(\{\u27e8]+$')
_RB_RE         = re.compile(r'^[\)\]\}\u27e9]+$')
_QUOTE_RE      = re.compile(r'^["\u201c\u201d\u2019\u2018`\'\u00ab\u00bb]+$')
_DOMAIN_RE     = re.compile(r'^(com|org|edu|net|xyz|gov|int|eu|hk|tw|cn|de|ch|fr)$')
_SQUOTE_RE     = re.compile(r'^[\u2019\u2018`\']+$')
_ALPHA_RE      = re.compile(r"^[A-Za-z'']+$")
_WS_RE         = re.compile(r' +')
_APOS_RE       = re.compile(r'^[\u2019\']+$')
_NL_RE         = re.compile(r'(\r?\n)+')
_WWW_RE        = re.compile(r'^(www[0-9]?|WWW[0-9]?)$')
_NOSP_BF_RE    = re.compile(r'^[,\.\;\:\?\!\)"\u201c\u201d\u2019\u2018`\'%\u2026\u2103\^\*\u00b0\/\u2044\u2012\u2013\u2014\-@]+$')
_LINEBREAK_RE  = re.compile(r'\r?\n')
_URL_RE        = re.compile(r'((http[s]?):(\/\/))?([-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b)([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)')
_EMAIL_RE      = re.compile(r'^\w+([\.\-]?\w+)*@\w+([\.\-]?\w+)*(\.\w{2,3})+$')
_TAG_RE        = re.compile(r'(<\/?[a-z][a-z0-9=\'"#;:&\s\-\+\/\.\?]*\/?>|<!DOCTYPE[^>]*>|<!--[^>-]*-->)', re.I)
_UNDER_RE      = re.compile(r'([0-9a-zA-Z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u00FF]|[\.,])_([0-9a-zA-Z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u00FF])')

_TAG_MARKER = "TAG"


# ---------------------------------------------------------------------------
# TOKENIZE_RE — sequential (pattern, replacement) pairs applied to the text
# ---------------------------------------------------------------------------

# In Python re.sub, backreferences use \1 not $1.
# JS 'g' flag = no re.DOTALL needed; all these are compiled without DOTALL.

_TOKENIZE_RE = [
    # save abbreviations --------
    (re.compile(r'\b([Ee])[.]([Gg])[.]'),           r'_\1\2_'),
    (re.compile(r'\b([Ii])[.]([Ee])[.]'),           r'_\1\2_'),
    (re.compile(r'\b([Aa])[.]([Mm])[.]'),           r'_\1\2_'),
    (re.compile(r'\b([Pp])[.]([Mm])[.]'),           r'_\1\2_'),
    (re.compile(r'\b(Cap)[.]'),                     r'_Cap_'),
    (re.compile(r'\b([Cc])[.]'),                    r'_\1_'),
    (re.compile(r'\b([Ee][Tt])\s([Aa][Ll])[.]'),   r'_\1zzz\2_'),
    (re.compile(r'\b(etc|ETC)[.]'),                 r'_\1_'),
    (re.compile(r'\b([Pp])[.]([Ss])[.]'),           r'_\1\2dot_'),
    (re.compile(r'\b([Pp])[.]([Ss])'),              r'_\1\2_'),
    (re.compile(r'\b([Pp])([Hh])[.]([Dd])'),        r'_\1\2\3_'),
    (re.compile(r'\b([Rr])[.]([Ii])[.]([Pp])'),     r'_\1\2\3_'),
    (re.compile(r'\b([Vv])([Ss]?)[.]'),             r'_\1\2_'),
    (re.compile(r'\b([Mm])([RrSsXx])[.]'),          r'_\1\2_'),
    (re.compile(r'\b([Dd])([Rr])[.]'),              r'_\1\2_'),
    (re.compile(r'\b([Pp])([Ff])[.]'),              r'_\1\2_'),
    (re.compile(r'\b([Ii])([Nn])([DdCc])[.]'),      r'_\1\2\3_'),
    (re.compile(r'\b([Cc])([Oo])[.][,][\s]([Ll])([Tt])([Dd])[.]'), r'_\1\2dcs\3\4\5_'),
    (re.compile(r'\b([Cc])([Oo])[.][\s]([Ll])([Tt])([Dd])[.]'),    r'_\1\2ds\3\4\5_'),
    (re.compile(r'\b([Cc])([Oo])[.][,]([Ll])([Tt])([Dd])[.]'),     r'_\1\2dc\3\4\5_'),
    (re.compile(r'\b([Cc])([Oo])([Rr]?)([Pp]?)[.]'),               r'_\1\2\3\4_'),
    (re.compile(r'\b([Ll])([Tt])([Dd])[.]'),        r'_\1\2\3_'),
    (re.compile(r'\b(prof|Prof|PROF)[.]'),          r'_\1_'),
    (re.compile(r'\b([\w.]+)@(\w+\.\w+)'),          r'\1__AT__\2'),
    # URLs with http(s)
    (re.compile(r'\b((http[s]?):(\/\/))([-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b)([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)'),
                                                    r'\2COLON\3\4\5'),
    # decimal numbers
    (re.compile(r'([\-]?[0-9]+)\.([0-9]+)e([\-]?[0-9]+)'), r'_\1DECIMALDOT\2POWERE\3_'),
    (re.compile(r'([\-]?[0-9]+)\.([0-9]+)'),        r'\1DECIMALDOT\2_'),
    (re.compile(r'([0-9]{1,3}),([0-9]{3})'),        r'\1_DECIMALCOMMA_\2'),
    (re.compile(r'([A-Za-z0-9])[.]([A-Za-z0-9])'),  r'\1_DECIMALDOT_\2'),
    # line breaks
    (re.compile(r'\r\n'),   ' _CARRIAGERETURNLINEFEED_ '),
    (re.compile(r'\n\r'),   ' _LINEFEEDCARRIAGERETURN_ '),
    (re.compile(r'\n'),     ' _LINEFEED_ '),
    (re.compile(r'\r'),     ' _CARRIAGERETURN_ '),
    # punctuation spacing
    (re.compile(r'\.\.\.\s'),                        '_elipsis_ '),
    (re.compile(r'([\?!"\u201C\.,;:@#$%&])'),        r' \1 '),
    (re.compile(r'\u2026'),                          ' \u2026 '),
    (re.compile(r'\s+'),                             ' '),
    (re.compile(r',([^0-9])'),                       r' , \1'),
    (re.compile(r'([^.])([.])([\])}>"\'\u2019]*)\s*$'), r'\1 \2\3 '),
    (re.compile(r'([\[\](){}<>\u27e8\u27e9])'),      r' \1 '),
    (re.compile(r'--'),                              ' -- '),
    (re.compile(r'\u2012'),                          ' \u2012 '),
    (re.compile(r'\u2013'),                          ' \u2013 '),
    (re.compile(r'\u2014'),                          ' \u2014 '),
    (re.compile(r'$'),                               ' '),
    (re.compile(r'^'),                               ' '),
    (re.compile(r"([^'])' | '"),                     r"\1 ' "),
    (re.compile(r' \u2018'),                         ' \u2018 '),
    (re.compile(r"'([SMD]) "),                       r" '\1 "),
    (re.compile(r' ([A-Z]) \.'),                     r' \1. '),
    (re.compile(r'^\s+'),                            ''),
    (re.compile(r'\^'),                              ' ^ '),
    (re.compile(r'\u00b0'),                          ' \u00b0 '),
    (re.compile(r'_elipsis_'),                       ' ... '),
    # pop abbreviations --------
    (re.compile(r'_([Ee])([Gg])_'),                  r'\1.\2.'),
    (re.compile(r'_([Ii])([Ee])_'),                  r'\1.\2.'),
    (re.compile(r'_([Aa])([Mm])_'),                  r'\1.\2.'),
    (re.compile(r'_([Pp])([Mm])_'),                  r'\1.\2.'),
    (re.compile(r'_Cap_'),                           'Cap.'),
    (re.compile(r'_([Cc])_'),                        r'\1.'),
    (re.compile(r'_([Ee][Tt])zzz([Aa][Ll])_'),       r'\1_\2.'),
    (re.compile(r'_(etc|ETC)_'),                     r'\1.'),
    (re.compile(r'_([Pp])([Ss])dot_'),               r'\1.\2.'),
    (re.compile(r'_([Pp])([Ss])_'),                  r'\1.\2'),
    (re.compile(r'_([Pp])([Hh])([Dd])_'),            r'\1\2.\3'),
    (re.compile(r'_([Rr])([Ii])([Pp])_'),            r'\1.\2.\3'),
    (re.compile(r'_([Vv])([Ss]?)_'),                 r'\1\2.'),
    (re.compile(r'_([Mm])([RrSsXx])_'),              r'\1\2.'),
    (re.compile(r'_([Dd])([Rr])_'),                  r'\1\2.'),
    (re.compile(r'_([Pp])([Ff])_'),                  r'\1\2.'),
    (re.compile(r'_([Ii])([Nn])([DdCc])_'),          r'\1\2\3.'),
    (re.compile(r'_([Cc])([Oo])([Rr]?)([Pp]?)_'),    r'\1\2\3\4.'),
    (re.compile(r'_([Cc])([Oo])dc([Ll])([Tt])([Dd])_'),  r'\1\2.,\3\4\5.'),
    (re.compile(r'_([Ll])([Tt])([Dd])_'),            r'\1\2\3.'),
    (re.compile(r'_([Cc])([Oo])dcs([Ll])([Tt])([Dd])_'), r'\1\2.,_\3\4\5.'),
    (re.compile(r'_([Cc])([Oo])ds([Ll])([Tt])([Dd])_'),  r'\1\2._\3\4\5.'),
    (re.compile(r'_(prof|PROF|Prof)_'),              r'\1.'),
    (re.compile(r'([\-]?[0-9]+)DECIMALDOT([0-9]+)_'),     r'\1.\2'),
    (re.compile(r'_([\-]?[0-9]+)DECIMALDOT([0-9]+)POWERE([\-]?[0-9]+)_'), r'\1.\2e\3'),
    (re.compile(r'_DECIMALCOMMA_'),                  ','),
    (re.compile(r'_DECIMALDOT_'),                    '.'),
    (re.compile(r'__AT__'),                          '@'),
    (re.compile(r'((http[s]?)COLON(\/\/))([-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b)([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)'),
                                                    r'\2:\3\4\5'),
    (re.compile(r'_LINEFEED_'),                      '\n'),
    (re.compile(r'_CARRIAGERETURN_'),                '\r'),
    (re.compile(r'_CARRIAGERETURNLINEFEED_'),        '\r\n'),
    (re.compile(r'_LINEFEEDCARRIAGERETURN_'),        '\n\r'),
]

_CONTRACTS_RE = [
    (re.compile(r"\b([Cc])an['\u2019]t"),           r'\1an not'),
    (re.compile(r"\b([Dd])idn['\u2019]t"),          r'\1id not'),
    (re.compile(r"\b([CcWw])ouldn['\u2019]t"),      r'\1ould not'),
    (re.compile(r"\b([Ss])houldn['\u2019]t"),       r'\1hould not'),
    (re.compile(r"\b([Ii])t['\u2019]s"),            r'\1t is'),
    (re.compile(r"\b([tT]hat)['\u2019]s"),          r'\1 is'),
    (re.compile(r"\b(she|he|you|they|i)['\u2019]d", re.I), r'\1 had'),
    (re.compile(r"\b(she|he|you|they|i)['\u2019]ll", re.I), r'\1 will'),
    (re.compile(r"n['\u2019]t "),                   ' not '),
    (re.compile(r"['\u2019]ve "),                   ' have '),
    (re.compile(r"['\u2019]re "),                   ' are '),
]

_POPTAG_RE = re.compile(r'_' + _TAG_MARKER + r'[0-9]+_')
_SPLITTER  = re.compile(r'(\S.+?[.!?]["\u201D]?)(?=\s+|$)')


# ---------------------------------------------------------------------------
# Tokenizer class
# ---------------------------------------------------------------------------

class Tokenizer:

    def __init__(self, rita=None):
        self.rita = rita

    # ------------------------------------------------------------------
    def tokens(self, text, options=None):
        """Return unique words from text (deduplicated, optionally filtered)."""
        options = options or {}
        words = self.tokenize(text, options)
        seen = {}
        for w in words:
            key = w if options.get('caseSensitive') else w.lower()
            if options.get('includePunct') or _ALPHA_RE.match(key):
                seen[key] = 1
        result = list(seen.keys())
        if options.get('ignoreStopWords'):
            stop = (self.rita.STOP_WORDS if self.rita and hasattr(self.rita, 'STOP_WORDS')
                    else _STOP_WORDS)
            result = [t for t in result if t.lower() not in stop]
        return sorted(result) if options.get('sort') else result

    # ------------------------------------------------------------------
    def tokenize(self, text, opts=None):
        """Split text into tokens."""
        opts = opts or {}
        if not isinstance(text, str):
            return []
        if opts.get('regex'):
            return text.split(opts['regex'])

        result = text.strip()
        tags_data = self._push_tags(result)
        tags   = tags_data['tags']
        result = tags_data['text']

        for (pattern, replacement) in _TOKENIZE_RE:
            result = pattern.sub(replacement, result)

        if opts.get('splitHyphens'):
            result = re.sub(r'([a-zA-Z]+)-([a-zA-Z]+)', r'\1 - \2', result)

        split_contractions = (
            opts.get('splitContractions') or
            (self.rita and getattr(self.rita, 'SPLIT_CONTRACTIONS', False))
        )
        if split_contractions:
            for (pat, rep) in _CONTRACTS_RE:
                result = pat.sub(rep, result)

        parts = _WS_RE.split(result.strip())
        return self._pop_tags(parts, tags)

    # ------------------------------------------------------------------
    def untokenize(self, arr, delim=' '):
        """Re-join a token list into a string with proper spacing."""
        if not arr or not isinstance(arr, list):
            return ''

        arr = self._pre_process_tags(arr)
        arr = [t for t in arr if t]  # filter empty strings
        if not arr:
            return ''

        next_no_space   = False
        after_quote     = False
        mid_sentence    = False
        within_quote    = bool(arr) and bool(_QUOTE_RE.match(arr[0]))
        result = arr[0] if arr else ''

        for i in range(1, len(arr)):
            if not arr[i]:
                continue
            this_token = arr[i]
            last_token = arr[i - 1]

            this_comma   = (this_token == ',')
            last_comma   = (last_token == ',')
            this_nb_punct = (
                bool(_NOSP_BF_RE.match(this_token)) or
                bool(_UNTAG_RE[2].match(this_token)) or
                bool(_LINEBREAK_RE.match(this_token))
            )
            this_lb    = bool(_LB_RE.match(this_token))
            this_rb    = bool(_RB_RE.match(this_token))
            last_nb_punct = (
                bool(_NOSP_BF_RE.match(last_token)) or
                bool(_LINEBREAK_RE.match(last_token))
            )
            last_na_punct = (
                bool(_NOSP_AF_RE.match(last_token)) or
                bool(_UNTAG_RE[1].match(last_token)) or
                bool(_LINEBREAK_RE.match(last_token))
            )
            last_lb    = bool(_LB_RE.match(last_token))
            last_rb    = bool(_RB_RE.match(last_token))
            last_ends_s = (
                last_token and last_token[-1] == 's' and
                last_token not in ('is', 'Is', 'IS')
            )
            last_is_www = bool(_WWW_RE.match(last_token))
            is_domain   = bool(_DOMAIN_RE.match(this_token))
            is_last     = (i == len(arr) - 1)
            next_is_s   = (
                False if is_last
                else (arr[i + 1] in ('s', 'S'))
            )
            last_quote = bool(_QUOTE_RE.match(last_token))
            this_quote = bool(_QUOTE_RE.match(this_token))
            this_linebreak = bool(_LINEBREAK_RE.match(this_token))

            if (last_token == '.' and is_domain) or next_no_space:
                next_no_space = False
                result += this_token
                continue

            elif this_token == '.' and last_is_www:
                next_no_space = True

            elif this_lb:
                result += delim

            elif last_rb:
                if not this_nb_punct and not this_lb:
                    result += delim

            elif this_quote:
                if within_quote:
                    after_quote  = True
                    within_quote = False
                elif not (
                    (_APOS_RE.match(this_token) and last_ends_s) or
                    (_APOS_RE.match(this_token) and next_is_s)
                ):
                    within_quote = True
                    after_quote  = False
                    result += delim

            elif after_quote and not this_nb_punct:
                result += delim
                after_quote = False

            elif last_quote and this_comma:
                mid_sentence = True

            elif mid_sentence and last_comma:
                result += delim
                mid_sentence = False

            elif (
                (not this_nb_punct and not last_quote and not last_na_punct
                 and not last_lb and not this_rb) or
                (not is_last and this_nb_punct and last_nb_punct and
                 not last_na_punct and not last_quote and not last_lb and
                 not this_rb and not this_linebreak)
            ):
                result += delim

            result += this_token

            if (
                this_nb_punct and not last_nb_punct and not within_quote and
                _SQUOTE_RE.match(this_token) and last_ends_s
            ):
                result += delim

        return result.strip()

    # ------------------------------------------------------------------
    def sentences(self, text, regex=None):
        """Split text into sentences."""
        if not text or not len(text):
            return [text]

        clean   = _NL_RE.sub(' ', text)
        delim   = '___'
        re_delim = re.compile(re.escape(delim), re.IGNORECASE)
        pattern = regex or _SPLITTER

        abrv = self.rita.ABRV if self.rita else _DEFAULT_ABRV

        def escape_abbrevs(s):
            for abv in abrv:
                idx = s.find(abv)
                while idx != -1:
                    s = s.replace(abv, abv.replace('.', delim), 1)
                    idx = s.find(abv)
            return s

        def unescape_abbrevs(arr):
            return [a.replace(delim, '.') for a in arr]

        escaped = escape_abbrevs(clean)
        arr = pattern.findall(escaped)
        return unescape_abbrevs(arr) if arr else [text]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _push_tags(self, text):
        tags, tag_idx = [], 0
        while _TAG_RE.search(text):
            m = _TAG_RE.search(text)
            tags.append(m.group(0))
            text = text[:m.start()] + ' _' + _TAG_MARKER + str(tag_idx) + '_ ' + text[m.end():]
            tag_idx += 1
        return {'tags': tags, 'text': text}

    def _pop_tags(self, result, tags):
        out = []
        for tok in result:
            if _POPTAG_RE.match(tok):
                tok = tags.pop(0) if tags else tok
            elif '_' in tok and not _EMAIL_RE.match(tok) and not _URL_RE.match(tok):
                tok = _UNDER_RE.sub(r'\1 \2', tok)
            out.append(tok)
        return out

    def _pre_process_tags(self, array):
        result = []
        idx = 0
        while idx < len(array):
            token = array[idx]
            if not _LT_RE.match(token):
                result.append(token)
                idx += 1
                continue
            sub = [array[idx]]
            inspect = idx + 1
            while inspect < len(array):
                sub.append(array[inspect])
                if _LT_RE.match(array[inspect]):
                    break
                if _GT_RE.match(array[inspect]):
                    break
                inspect += 1
            if _LT_RE.match(sub[-1]):
                result.extend(sub[:-1])
                idx = inspect
                continue
            if not _GT_RE.match(sub[-1]):
                result.extend(sub)
                idx = inspect + 1
                continue
            joined = ''.join(sub)
            if not _TAG_RE.match(joined):
                result.extend(sub)
                idx = inspect + 1
                continue
            tag = self._tag_subarray_to_string(sub)
            result.append(tag)
            idx = inspect + 1
        return result

    def _tag_subarray_to_string(self, array):
        if not _LT_RE.match(array[0]) or not _GT_RE.match(array[-1]):
            raise ValueError(f"{array} is not a tag")
        start = array[0].strip()
        end   = array[-1].strip()
        inspect = 1
        while inspect < len(array) - 1 and _TAGSTART_RE.match(array[inspect]):
            start += array[inspect].strip()
            inspect += 1
        content_start = inspect
        inspect = len(array) - 2
        while inspect > content_start and _TAGEND_RE.match(array[inspect]):
            end = array[inspect].strip() + end
            inspect -= 1
        content_end = inspect
        inner = self.untokenize(array[content_start:content_end + 1]).strip()
        return start + inner + end


# ---------------------------------------------------------------------------
# Default abbreviation list (used when no RiTa parent is available)
# ---------------------------------------------------------------------------

_DEFAULT_ABRV = [
    'Mr.', 'Mrs.', 'Ms.', 'Dr.', 'Prof.', 'Sr.', 'Jr.', 'Rev.', 'Gen.',
    'Pres.', 'Gov.', 'Lt.', 'Col.', 'Capt.', 'Sgt.', 'Pvt.',
    'Mt.', 'Blvd.', 'Ave.', 'St.', 'Apt.',
    'Jan.', 'Feb.', 'Mar.', 'Apr.', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.',
    'Nov.', 'Dec.',
    'vs.', 'etc.', 'i.e.', 'e.g.', 'Ph.D', 'U.S.A.', 'U.S.',
]
