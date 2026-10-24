"""
rita/analyzer.py — Phonetic analyzer
Python port of ritajs/src/analyzer.js
"""
import json
import os

from rita.util import Util

_SP = ' '
_E  = ''


class Features(dict):
    """Feature map returned by analyze()/analyze_word().

    A dict subclass so it compares equal to a plain dict (eql) while also
    supporting JS-style attribute access (data.phones).
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


class Analyzer:

    def __init__(self):
        self._cache = {}
        self._cacheRef = None     # identity of lexicon.data the cache was built from
        self._lts = None          # lazy LetterToSound
        self._tokenizer = None    # lazy
        self._tagger = None       # lazy
        self.rita = None
        self._dict_cache = None

    def _silent_lts(self, opts=None):
        return bool(
            (self.rita and self.rita.SILENCE_LTS)
            or (opts and opts.get('silent'))
        )

    # ── lazy deps ────────────────────────────────────────────────────────────

    def _get_lts(self):
        if self._lts is None:
            from rita.rita_lts import LetterToSound
            self._lts = LetterToSound(self.rita)
        return self._lts

    def _get_tokenizer(self):
        if self._tokenizer is None:
            from rita.tokenizer import Tokenizer
            self._tokenizer = Tokenizer()
        return self._tokenizer

    def _get_tagger(self):
        if self._tagger is None:
            from rita.tagger import Tagger
            self._tagger = Tagger()
        return self._tagger

    def _get_dict(self):
        # JS reads through the lexicon (lex.rawPhones), so a swapped
        # RiTa.lexicon.data must be visible here too.
        from rita.rita import RiTa
        return RiTa.lexicon.data

    # ── dict helpers ─────────────────────────────────────────────────────────

    def _lookup_raw(self, word):
        if not word:
            return None
        d = self._get_dict()
        return d.get(word.lower())

    def raw_phones(self, word, opts=None):
        """Return raw phone string (with syllable breaks as spaces) from dict,
        or compute via LTS if noLts is not set."""
        no_lts = opts.get('noLts', False) if opts else False
        rdata = self._lookup_raw(word)
        if rdata and len(rdata) > 0:
            return rdata[0]  # phones string from dict
        if not no_lts:
            phones = self.compute_phones(word, opts)
            return Util.syllables_from_phones(phones) if phones else None
        return None

    def dict_size(self):
        return len(self._get_dict())

    # ── public API ───────────────────────────────────────────────────────────

    _DIGIT_WORDS = ['zero','one','two','three','four','five','six','seven','eight','nine']

    def compute_phones(self, word=None, opts=None):
        """Run the LTS engine; returns list of phone strings or None."""
        if word is None:
            return None
        if word and len(word) == 1 and word.isdigit():
            word = self._DIGIT_WORDS[int(word)]
            # use dict phones for digit-words (LTS gives wrong results)
            rdata = self._lookup_raw(word)
            if rdata and len(rdata) > 0:
                # dict format: 'w-ah1-n' or 'w-ah1 n' — split on space/dash
                raw = rdata[0].replace(' ', '-')
                return [p.rstrip('12') if p[-1:].isdigit() else p
                        for p in raw.split('-') if p]
        result = self._get_lts().build_phones(word, opts)
        return result  # list of phoneme strings, or None

    def phones_to_stress(self, phones=None):
        """Convert a syllabified phone string to a stress pattern string."""
        if not phones:
            return None
        stress = _E
        syls = phones.split(_SP)
        for j, syl in enumerate(syls):
            if not syl:
                continue
            stress += '1' if '1' in syl else '0'
            if j < len(syls) - 1:
                stress += '/'
        return stress

    def analyze_word(self, word, opts=None):
        """Return dict with phones, stresses, syllables for a single word."""
        if opts is None:
            opts = {}

        # convert single digit to its word equivalent
        if word and len(word) == 1 and word.isdigit():
            word = self._DIGIT_WORDS[int(word)]

        # invalidate the cache if the lexicon data was swapped out
        from rita.rita import RiTa
        data = RiTa.lexicon.data
        if self._cacheRef is not data:
            self._cache = {}
            self._cacheRef = data

        caching = getattr(RiTa, 'CACHING', True)
        result = self._cache.get(word) if caching else None
        if result is not None:
            return result

        slash = '/'
        delim = '-'
        phones = word
        syllables = word
        stresses = word

        raw_phones = self._raw_phones_word(word, opts) if not word.startswith('-') else None
        raw_phones = raw_phones or self._compute_raw_phones(word, opts)

        if raw_phones:
            if isinstance(raw_phones, str):
                sp = raw_phones.replace('1', _E).replace(_SP, delim) + _SP
                phones = 'dh-ah ' if sp == 'dh ' else sp
                ss = raw_phones.replace(_SP, slash).replace('1', _E) + _SP
                syllables = 'dh-ah ' if ss == 'dh ' else ss
                stresses = self.phones_to_stress(raw_phones)
            else:
                # hyphenated word — list of raw phone strings
                ps, syls, strs = [], [], []
                for p in raw_phones:
                    sp = p.replace('1', _E).replace(_SP, delim)
                    ps.append('dh-ah ' if sp == 'dh ' else sp)
                    ss = p.replace(_SP, slash).replace('1', _E)
                    syls.append('dh-ah ' if ss == 'dh ' else ss)
                    strs.append(self.phones_to_stress(p))
                phones = '-'.join(ps)
                syllables = '/'.join(syls)
                stresses = '-'.join(strs)

        result = Features({
            'phones':    phones.strip(),
            'stresses':  stresses.strip() if stresses else stresses,
            'syllables': syllables.strip(),
        })
        if caching:
            self._cache[word] = result
        return result

    def analyze(self, text, opts=None):
        """Analyze a full text string; returns feature dict."""
        if opts is None:
            opts = {}
        if not text or not text.strip():
            return Features({'tokens': '', 'pos': '', 'stresses': '', 'phones': '', 'syllables': ''})

        words = self._get_tokenizer().tokenize(text)
        tagger = self._get_tagger()
        tags = tagger.tag(words, opts)

        features = Features({
            'phones':    _E,
            'stresses':  _E,
            'syllables': _E,
            'pos':       ' '.join(tags),
            'tokens':    ' '.join(words),
        })

        for word in words:
            r = self.analyze_word(word, opts)
            features['phones']    += _SP + r['phones']
            features['stresses']  += _SP + r['stresses']
            features['syllables'] += _SP + r['syllables']

        for k in features:
            features[k] = features[k].strip()

        if opts.get('ipaPhones'):
            features['phones'] = self.syllables_to_ipa(
                features['syllables'], features['stresses']
            )

        return features

    _ARPABET_TO_IPA = {
        'aa': 'ɑ', 'ae': 'æ', 'ah': 'ʌ', 'ao': 'ɔ', 'aw': 'aʊ',
        'ax': 'ə', 'ay': 'aɪ', 'eh': 'ɛ', 'er': 'ɜr', 'ey': 'eɪ',
        'ih': 'ɪ', 'ix': 'ɨ', 'iy': 'i', 'ow': 'oʊ', 'oy': 'ɔɪ',
        'uh': 'ʊ', 'uw': 'u', 'b': 'b', 'ch': 'tʃ', 'd': 'd',
        'dh': 'ð', 'dx': 'ɾ', 'el': 'l̩', 'em': 'm̩', 'en': 'n̩',
        'f': 'f', 'g': 'ɡ', 'hh': 'h', 'jh': 'dʒ', 'k': 'k',
        'l': 'l', 'm': 'm', 'n': 'n', 'ng': 'ŋ', 'p': 'p',
        'q': 'ʔ', 'r': 'ɹ', 's': 's', 'sh': 'ʃ', 't': 't',
        'th': 'θ', 'v': 'v', 'w': 'w', 'wh': 'ʍ', 'y': 'j',
        'z': 'z', 'zh': 'ʒ',
    }

    @classmethod
    def syllables_to_ipa(cls, syllables, stresses, keep_boundaries=False):
        syllable_words = syllables.split(' ')
        stress_words = stresses.split(' ')
        ipa_words = []
        stress_index = 0
        for word in syllable_words:
            if len(word) == 1 and not (word.isalpha() or word in '-/'):
                stress_index += 1
                continue
            syllable_list = word.split('/')
            stress_list = (stress_words[stress_index] if stress_index < len(stress_words) else '0').split('/')
            stress_index += 1
            monosyllable = len(syllable_list) == 1
            ipa_syllables = []
            for index, syllable in enumerate(syllable_list):
                stressed = index < len(stress_list) and stress_list[index] == '1'
                parts = []
                for phone in syllable.split('-'):
                    if phone == 'ah':
                        parts.append('ʌ' if stressed else 'ə')
                    elif phone == 'er':
                        parts.append('ɜr' if stressed else 'ər')
                    else:
                        ipa = cls._ARPABET_TO_IPA.get(phone, phone)
                        if stressed and phone in ('aa', 'iy', 'ao', 'uw'):
                            ipa += 'ː'
                        parts.append(ipa)
                value = ''.join(parts)
                if stressed and not monosyllable:
                    value = 'ˈ' + value
                ipa_syllables.append(value)
            ipa_words.append('/'.join(ipa_syllables) if keep_boundaries else ''.join(ipa_syllables))
        return ' '.join(ipa_words)

    # ── phone helpers ─────────────────────────────────────────────────────────

    def _compute_raw_phones(self, word, opts=None):
        if '-' in word:
            return self._compute_phones_hyph(word, opts)
        return self._compute_phones_word(word, opts)

    def _compute_phones_hyph(self, word, opts=None):
        raw_phones = []
        for part in word.split('-'):
            p = self._compute_phones_word(part, opts, is_part=True)
            if p and len(p) > 0:
                raw_phones.append(p)
        return raw_phones if raw_phones else None

    def _compute_phones_word(self, word, opts=None, is_part=False):
        raw_phones = None
        if is_part:
            raw_phones = self._raw_phones_word(word, {'noLts': True})

        # singular plural: if ends in 's', try singular + '-z'
        if not raw_phones and word.endswith('s'):
            from rita.inflector import Inflector
            sing = Inflector().singularize(word)
            raw_phones = self._raw_phones_word(sing, {'noLts': True})
            if raw_phones:
                raw_phones += '-z'

        silent = self._silent_lts(opts)

        if not raw_phones:
            lts_phones = self.compute_phones(word, opts)
            if lts_phones and len(lts_phones) > 0:
                if not silent and self.dict_size() > 0:
                    print(f"[RiTa] Used LTS-rules for '{word}'")
                # lts returns a list; join with '-' for syllabification
                raw_phones = Util.syllables_from_phones('-'.join(lts_phones))

        return raw_phones

    def _raw_phones_word(self, word, opts=None):
        """Look up phones in dict only (no LTS fallback)."""
        rdata = self._lookup_raw(word)
        if rdata and len(rdata) > 0:
            return rdata[0]
        return None

    # ── convenience methods (mirror RiTa top-level API) ─────────────────────

    def phones(self, text, opts=None):
        """Return space-separated phone strings for each token."""
        if not text or not text.strip():
            return ''
        features = self.analyze(text, opts)
        return features['phones']

    def syllables(self, text, opts=None):
        """Return space-separated syllable strings for each token."""
        if not text or not text.strip():
            return ''
        features = self.analyze(text, opts)
        if opts and opts.get('ipaPhones'):
            return self.syllables_to_ipa(
                features['syllables'], features['stresses'], keep_boundaries=True
            )
        return features['syllables']

    def stresses(self, text, opts=None):
        """Return space-separated stress patterns for each token."""
        if not text or not text.strip():
            return ''
        return self.analyze(text, opts)['stresses']
