"""
rita/lexicon.py — Lexicon
Python port of ritajs/src/lexicon.js
"""
import json
import os
import re as _re
import random as _random

from rita.util import Util

_STRESS = '1'
_SYLLABLE_BOUNDARY = '/'
_PHONE_BOUNDARY = '-'
_VOWELS = 'aeiou'
_MASS_NOUNS = [
    'absinthe', 'acceptance', 'acclaim', 'acrimony', 'admiration', 'adobe',
    'adrenaline', 'adversity', 'advice', 'aesthetics', 'aggression', 'agility',
    'agony', 'agriculture', 'air', 'alchemy', 'alcohol', 'alertness', 'algebra',
    'altruism', 'ambiguity', 'ambivalence', 'ammunition', 'anarchy', 'anger',
    'anguish', 'anxiety', 'apathy', 'appeal', 'apprehension', 'archery',
    'architecture', 'aristocracy', 'armor', 'arrogance', 'art', 'aspiration',
    'astronomy', 'athleticism', 'atmosphere', 'audacity', 'austerity', 'authority',
    'autonomy', 'awareness', 'awe', 'balance', 'bankruptcy', 'beauty', 'beef',
    'beer', 'betrayal', 'biochemistry', 'biology', 'bitterness', 'blood',
    'bravery', 'bread', 'Buddhism', 'bureaucracy', 'butter', 'capitalism',
    'caution', 'camaraderie', 'cash', 'certainty', 'chaos', 'charity', 'chemistry',
    'chess', 'chocolate', 'Christianity', 'citizenship', 'civility', 'clarity',
    'clothing', 'coexistence', 'coffee', 'collaboration', 'comfort', 'commerce',
    'compassion', 'complexity', 'compromise', 'confidence', 'consciousness',
    'conservation', 'courage', 'creativity', 'crime', 'criticism', 'culture',
    'curiosity', 'darkness', 'decency', 'democracy', 'depression', 'desire',
    'despair', 'determination', 'dignity', 'diplomacy', 'discipline', 'discrimination',
    'diversity', 'doubt', 'dust', 'economics', 'education', 'electricity',
    'empathy', 'endurance', 'energy', 'engineering', 'enthusiasm', 'equality',
    'equity', 'ethics', 'evil', 'excellence', 'existence', 'faith', 'fame',
    'fascism', 'fear', 'fiction', 'flour', 'food', 'forgiveness', 'freedom',
    'friendship', 'frustration', 'furniture', 'gasoline', 'geography', 'geometry',
    'gold', 'grace', 'gravity', 'grief', 'growth', 'guilt', 'happiness', 'hate',
    'hatred', 'history', 'honor', 'hope', 'hospitality', 'humanity', 'humility',
    'hunger', 'ice', 'ideology', 'ignorance', 'imagination', 'inequality',
    'injustice', 'innovation', 'integrity', 'intelligence', 'iron', 'jealousy',
    'journalism', 'joy', 'justice', 'kindness', 'knowledge', 'labor', 'language',
    'law', 'leadership', 'liberty', 'light', 'literature', 'love', 'loyalty',
    'madness', 'mathematics', 'mercy', 'milk', 'modesty', 'morality', 'music',
    'nationalism', 'nature', 'nobility', 'nostalgia', 'oil', 'optimism', 'order',
    'pain', 'passion', 'peace', 'philosophy', 'physics', 'pity', 'poetry',
    'politics', 'poverty', 'power', 'pride', 'prosperity', 'psychology', 'racism',
    'reality', 'religion', 'resilience', 'respect', 'revenge', 'rice', 'righteousness',
    'romance', 'sand', 'science', 'secrecy', 'serenity', 'silver', 'slavery',
    'socialism', 'society', 'solidarity', 'sorrow', 'spirituality', 'steel',
    'strength', 'stubbornness', 'success', 'sugar', 'sustainability', 'technology',
    'time', 'tobacco', 'tolerance', 'tradition', 'trust', 'truth', 'tyranny',
    'uncertainty', 'unity', 'valor', 'violence', 'virtue', 'water', 'wealth',
    'wisdom', 'wood', 'wool', 'youth',
]


class Lexicon:

    def __init__(self, data=None):
        self._data = data          # custom dict; None = lazy-load default
        self._dict_cache = None
        self._words = None         # cached list of dict keys
        self._syl_index = None     # dict: num_syllables -> [word, ...]
        self._pos_index = None     # dict: pos_tag -> [word, ...]
        self._plural_cache = {}    # word -> plural form
        self._conjug_cache = {}    # (word, pos) -> conjugated form
        self._analyzer = None
        self._tagger = None
        self._inflector = None
        self._conjugator = None
        self._randgen = None

    # ── lazy deps ─────────────────────────────────────────────────────────────

    def _get_dict(self):
        if self._data is not None:
            return self._data
        if self._dict_cache is None:
            p = os.path.join(os.path.dirname(__file__), '..', '..', 'shared', 'rita_dict.json')
            with open(p) as f:
                self._dict_cache = json.load(f)
        return self._dict_cache

    def _get_words(self):
        if self._words is None:
            self._words = list(self._get_dict().keys())
        return self._words

    def _get_syl_index(self):
        if self._syl_index is None:
            idx = {}
            for word, data in self._get_dict().items():
                if data:
                    n = data[0].count(' ') + 1
                    idx.setdefault(n, []).append(word)
            self._syl_index = idx
        return self._syl_index

    def _get_pos_index(self):
        if self._pos_index is None:
            idx = {}
            for word, data in self._get_dict().items():
                if data and len(data) > 1:
                    for tag in data[1].split(' '):
                        idx.setdefault(tag, []).append(word)
            self._pos_index = idx
        return self._pos_index

    def _get_analyzer(self):
        if self._analyzer is None:
            from rita.analyzer import Analyzer
            self._analyzer = Analyzer()
        return self._analyzer

    def _get_tagger(self):
        if self._tagger is None:
            from rita.tagger import Tagger
            self._tagger = Tagger()
        return self._tagger

    def _get_inflector(self):
        if self._inflector is None:
            from rita.inflector import Inflector
            self._inflector = Inflector()
        return self._inflector

    def _get_conjugator(self):
        if self._conjugator is None:
            from rita.conjugator import Conjugator
            self._conjugator = Conjugator()
        return self._conjugator

    def _get_randgen(self):
        if self._randgen is None:
            from rita.randgen import RandGen
            self._randgen = RandGen()
        return self._randgen

    # ── public API ────────────────────────────────────────────────────────────

    def size(self):
        return len(self._get_dict())

    def has_word(self, word, opts=None):
        if not word or not len(word):
            return False
        opts = opts or {}
        token = word.lower()
        d = self._get_dict()
        exists = token in d
        no_derivations = opts.get('noDerivations', False)
        if no_derivations or exists:
            return exists

        # 1) plural form of a noun?
        sing = self._get_inflector().singularize(token)
        if sing in d:
            tags = self._all_tags(sing)
            if 'nn' in tags:
                return True

        # 2) conjugated form of a verb?
        vlemma = self._get_conjugator().unconjugate(token, opts)
        if vlemma and vlemma in d:
            tags = self._all_tags(vlemma)
            if 'vb' in tags:
                return True

        return False

    def random_word(self, pattern=None, opts=None):
        d = self._get_dict()

        # no arguments
        if pattern is None and opts is None:
            return _random.choice(self._get_words())

        # single dict argument = opts
        if isinstance(pattern, dict) and opts is None:
            opts = pattern
            pattern = None

        opts = opts or {}
        opts['limit'] = 1
        opts['shuffle'] = True
        opts['strictPos'] = True
        opts.setdefault('minLength', 4)

        result = self.search_sync(pattern, opts)

        # relax pos constraints if nothing found
        if len(result) < 1 and 'pos' in opts:
            opts['strictPos'] = False
            result = self.search_sync(pattern, opts)

        if len(result) < 1:
            for k in ('strictPos', 'shuffle', 'targetPos'):
                opts.pop(k, None)
            raise ValueError(f"No words matching constraints: {opts}")

        return result[0]

    def search_sync(self, pattern=None, opts=None):
        d = self._get_dict()

        if pattern is None and not opts:
            return list(self._get_words())

        regex, opts = self._parse_regex(pattern, opts or {})
        self._parse_args(opts)

        num_syl = opts.get('numSyllables', 0)
        target_pos = opts.get('targetPos')
        if num_syl:
            words = list(self._get_syl_index().get(num_syl, []))
        elif target_pos:
            words = list(self._get_pos_index().get(target_pos, []))
        else:
            words = list(self._get_words())

        limit = opts.get('limit', 10)

        # Fast path: rejection sampling avoids a full O(n) shuffle when we
        # only need a small number of results.
        if opts.get('shuffle') and 0 < limit <= 3 and len(words) > limit * 10:
            result = []
            seen = set()
            attempts = min(300, len(words))
            indices = _random.sample(range(len(words)), attempts)
            for i in indices:
                word = words[i]
                data = d.get(word)
                if not self._check_criteria(word, data, opts):
                    continue
                if opts.get('targetPos'):
                    word = self._match_pos(word, data, opts, opts.get('strictPos', False))
                    if not word:
                        continue
                    data = d.get(word) if word in d else None
                if word in seen:
                    continue
                if regex is None or self._regex_match(word, data, regex, opts.get('type')):
                    seen.add(word)
                    result.append(word)
                    if len(result) == limit:
                        return result
            if result:
                return result
            # fall through to full scan if rejection sampling came up empty

        if opts.get('shuffle'):
            _random.shuffle(words)

        result = []
        seen = set()

        for word in words:
            data = d.get(word)
            if not self._check_criteria(word, data, opts):
                continue

            if opts.get('targetPos'):
                word = self._match_pos(word, data, opts, opts.get('strictPos', False))
                if not word:
                    continue
                if word not in d:
                    data = None
                else:
                    data = d.get(word)

            if word in seen:
                continue
            if regex is None or self._regex_match(word, data, regex, opts.get('type')):
                seen.add(word)
                result.append(word)
                if len(result) == limit:
                    break

        return result

    # alias: async in JS, sync in Python
    search = search_sync

    def rhymes_sync(self, the_word, opts=None):
        opts = opts or {}
        self._parse_args(opts)

        if not the_word or len(the_word) < 2:
            return []

        d = self._get_dict()
        phone = self._last_stressed_phone_to_end(the_word)
        if not phone:
            return []

        num_syl = opts.get('numSyllables', 0)
        target_pos = opts.get('targetPos')
        if num_syl:
            words = list(self._get_syl_index().get(num_syl, []))
        elif target_pos:
            words = list(self._get_pos_index().get(target_pos, []))
        else:
            words = list(self._get_words())
        if opts.get('shuffle'):
            _random.shuffle(words)

        if opts.get('shuffle'):
            _random.shuffle(words)

        result = []
        limit = opts.get('limit', 10)

        for word in words:
            data = d.get(word)
            if word == the_word or not self._check_criteria(word, data, opts):
                continue

            if opts.get('targetPos'):
                word = self._match_pos(word, data, opts, opts.get('strictPos', False))
                if not word:
                    continue
                data = d.get(word)

            phones = data[0] if data else self.raw_phones(word)
            if phones and phones.endswith(phone):
                result.append(word)

            if len(result) == limit:
                break

        return result

    rhymes = rhymes_sync

    def alliterations_sync(self, the_word, opts=None):
        opts = opts or {}
        self._parse_args(opts)

        if not the_word or not isinstance(the_word, str) or len(the_word) < 2:
            return []

        # only consonant inputs
        if the_word[0].lower() in _VOWELS:
            if not opts.get('silent'):
                import warnings
                warnings.warn(f'Expects a word starting with a consonant, got: {the_word}')
            return []

        d = self._get_dict()
        fss = self._first_stressed_syl(the_word)
        if not fss:
            return []

        phone = self._first_phone(fss)
        if not phone:
            if not opts.get('silent'):
                import warnings
                warnings.warn(f'Failed parsing first phone in "{the_word}"')
            return []

        num_syl = opts.get('numSyllables', 0)
        target_pos = opts.get('targetPos')
        if num_syl:
            words = list(self._get_syl_index().get(num_syl, []))
        elif target_pos:
            words = list(self._get_pos_index().get(target_pos, []))
        else:
            words = list(self._get_words())
        if opts.get('shuffle'):
            _random.shuffle(words)

        if opts.get('shuffle'):
            _random.shuffle(words)

        result = []
        limit = opts.get('limit', 10)

        for word in words:
            data = d.get(word)
            if word == the_word or not self._check_criteria(word, data, opts):
                continue

            if opts.get('targetPos'):
                word = self._match_pos(word, data, opts)
                if not word:
                    continue
                data = d.get(word)

            c2 = self._first_phone(self._first_stressed_syl(word))
            if phone == c2:
                result.append(word)

            if len(result) == limit:
                break

        return result

    alliterations = alliterations_sync

    def spells_like_sync(self, word, opts=None):
        if not word or not len(word):
            return []
        opts = opts or {}
        opts['type'] = 'letter'
        return self._by_type_sync(word, opts)

    spells_like = spells_like_sync

    def sounds_like_sync(self, word, opts=None):
        if not word or not len(word):
            return []
        opts = opts or {}
        if opts.get('matchSpelling'):
            return self._by_sound_and_letter_sync(word, opts)
        opts['type'] = 'sound'
        return self._by_type_sync(word, opts)

    sounds_like = sounds_like_sync

    def is_rhyme(self, word1, word2):
        if not word1 or not word2 or word1.upper() == word2.upper():
            return False
        if self.raw_phones(word1) == self.raw_phones(word2):
            return False
        p1 = self._last_stressed_vowel_phoneme_to_end(word1)
        p2 = self._last_stressed_vowel_phoneme_to_end(word2)
        return bool(p1 and p2 and p1 == p2)

    def is_alliteration(self, word1, word2):
        if not word1 or not word2 or not len(word1):
            return False
        c1 = self._first_phone(self._first_stressed_syl(word1))
        c2 = self._first_phone(self._first_stressed_syl(word2))
        return bool(c1 and c2 and c1[0] not in _VOWELS and c1 == c2)

    def raw_phones(self, word, opts=None):
        no_lts = opts.get('noLts', False) if opts else False
        rdata = self._lookup_raw(word)
        if rdata and len(rdata):
            return rdata[0]
        if not no_lts:
            phones = self._get_analyzer().compute_phones(word)
            if phones:
                return Util.syllables_from_phones('-'.join(phones))
        return None

    def min_edit_dist(self, source, target):
        """Minimum edit distance between two strings or lists."""
        m, n = len(source), len(target)
        matrix = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            matrix[i][0] = i
        for j in range(n + 1):
            matrix[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if source[i - 1] == target[j - 1] else 1
                matrix[i][j] = min(
                    matrix[i - 1][j] + 1,
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j - 1] + cost,
                )
        return matrix[m][n]

    def is_mass_noun(self, w):
        return (w.endswith('ness') or w.endswith('ism')
                or w in _MASS_NOUNS)

    # ── private helpers ───────────────────────────────────────────────────────

    def _by_type_sync(self, the_word, opts):
        self._parse_args(opts)
        d = self._get_dict()
        inp = the_word.lower()
        match_sound = opts.get('type') == 'sound'
        variations = {inp, inp + 's', inp + 'es'}

        phones_a = self._to_phone_array(self.raw_phones(inp)) if match_sound else inp
        if phones_a is None:
            return []

        min_val = float('inf')
        target_pos = opts.get('targetPos')
        if target_pos:
            words = list(self._get_pos_index().get(target_pos, []))
        else:
            words = list(self._get_words())
        if opts.get('shuffle'):
            _random.shuffle(words)

        result = []
        seen = set()
        limit = opts.get('limit', 10)
        min_distance = opts.get('minDistance', 1)

        for word in words:
            data = d.get(word)
            if word in variations:
                continue
            if not self._check_criteria(word, data, opts):
                continue

            if opts.get('targetPos'):
                word = self._match_pos(word, data, opts)
                if not word:
                    continue
                data = d.get(word)

            if word in seen:
                continue
            seen.add(word)

            if match_sound:
                phones = data[0] if data else self.raw_phones(word)
                phones_b = self._to_phone_array(phones) if phones else word
            else:
                phones_b = word

            # Skip if length difference already exceeds current best (MED lower bound)
            if abs(len(phones_a) - len(phones_b)) > min_val:
                continue

            med = self.min_edit_dist(phones_a, phones_b)

            if med >= min_distance and med < min_val:
                min_val = med
                result = [word]
            elif med == min_val and len(result) < limit:
                result.append(word)

        return result[:limit]

    def _by_sound_and_letter_sync(self, word, opts):
        by_sound = self._by_type_sync(word, {**opts, 'type': 'sound'})
        by_letter = self._by_type_sync(word, {**opts, 'type': 'letter'})
        if not by_sound or not by_letter:
            return []
        limit = opts.get('limit', 10)
        return self._intersect(by_sound, by_letter)[:limit]

    def _match_pos(self, word, rdata, opts, strict=False):
        if not rdata or len(rdata) < 2:
            return None
        pos_arr = rdata[1].split(' ')
        target_pos = opts.get('targetPos')
        if not target_pos:
            return word

        orig_pos = opts.get('pos', '')
        conjugate = opts.get('conjugate', False)

        # Check if pos matches: accept targetPos ('vb') OR exact original pos ('vbd')
        pos_match = target_pos in pos_arr
        exact_match = conjugate and orig_pos in pos_arr

        if not pos_match and not exact_match:
            return None
        if strict and target_pos != pos_arr[0] and (not exact_match or orig_pos != pos_arr[0]):
            return None

        result = word
        if opts.get('pluralize'):
            if word.endswith('ness') or word.endswith('ism'):
                return None
            result = self._plural_cache.get(word)
            if result is None:
                result = self._get_inflector().pluralize(word)
                self._plural_cache[word] = result
            if not self._is_noun(result):
                return None
        elif conjugate and pos_match:  # only reconjugate base verb forms
            key = (word, orig_pos)
            result = self._conjug_cache.get(key)
            if result is None:
                result = self._reconjugate(word, orig_pos)
                self._conjug_cache[key] = result
        # if exact_match (already the right verb form), return word as-is

        if result != word:
            if opts.get('numSyllables'):
                syls = self._get_analyzer().analyze_word(result, {'silent': True})['syllables']
                num = len(syls.split(_SYLLABLE_BOUNDARY))
                if num != opts['numSyllables']:
                    return None
            min_len = opts.get('minLength', 3)
            max_len = opts.get('maxLength', float('inf'))
            if len(result) < min_len or len(result) > max_len:
                return None

        return result

    def _check_criteria(self, word, rdata, opts):
        min_len = opts.get('minLength', 3)
        max_len = opts.get('maxLength', float('inf'))
        if len(word) > max_len or len(word) < min_len:
            return False
        num_syl = opts.get('numSyllables', 0)
        if num_syl and rdata:
            if num_syl != rdata[0].count(' ') + 1:
                return False
        return True

    def _parse_args(self, opts):
        opts['limit'] = int(opts.get('limit', 10))
        opts['minDistance'] = int(opts.get('minDistance', 1))
        opts['numSyllables'] = int(opts.get('numSyllables', 0))
        opts['maxLength'] = opts.get('maxLength', float('inf'))
        opts['minLength'] = int(opts.get('minLength', 3))

        if opts['limit'] < 1:
            opts['limit'] = float('inf')

        tpos = opts.get('pos', False)
        if tpos and len(tpos):
            opts['pluralize'] = (tpos == 'nns')
            opts['conjugate'] = (tpos[0] == 'v' and len(tpos) > 2)
            if tpos[0] == 'n':
                tpos = 'nn'
            elif tpos[0] == 'v':
                tpos = 'vb'
            elif tpos == 'r':
                tpos = 'rb'
            elif tpos == 'a':
                tpos = 'jj'

        opts['targetPos'] = tpos

    def _parse_regex(self, pattern, opts):
        """Normalize pattern to a compiled re.Pattern (or None) and return (regex, opts)."""
        opts = opts or {}

        if isinstance(pattern, str):
            if opts.get('type') in ('stresses', 'stress'):
                if _re.match(r'^\^?[01]+\$?$', pattern):
                    # insert slashes: 010 -> 0/1/0
                    pattern = _re.sub(r'([01])(?=[01])', r'\1/', pattern)
            regex = _re.compile(pattern)
        elif hasattr(pattern, 'match'):  # compiled regex
            regex = pattern
        elif isinstance(pattern, dict) or pattern is None:
            if pattern and not opts:
                opts = pattern
            regex_raw = opts.get('regex')
            if isinstance(regex_raw, str):
                if opts.get('type') in ('stresses', 'stress'):
                    if _re.match(r'^\^?[01]+\$?$', regex_raw):
                        regex_raw = _re.sub(r'([01])(?=[01])', r'\1/', regex_raw)
                regex = _re.compile(regex_raw)
            elif regex_raw is not None and hasattr(regex_raw, 'match'):
                regex = regex_raw
            else:
                regex = None
        else:
            regex = None

        return regex, opts

    def _regex_match(self, word, data, regex, type_):
        if type_ == 'stresses':
            phones = data[0] if data else self.raw_phones(word)
            stresses = self._get_analyzer().phones_to_stress(phones)
            return bool(stresses and regex.search(stresses))
        elif type_ == 'phones':
            phones = data[0] if data else self.raw_phones(word)
            if phones:
                phones = phones.replace('1', '').replace(' ', '-')
                return bool(regex.search(phones))
            return False
        else:
            return bool(regex.search(word))

    def _reconjugate(self, word, pos):
        from rita.conjugator import PAST, PRESENT, SINGULAR, FIRST, THIRD
        c = self._get_conjugator()
        pos = pos.lower()
        if pos == 'vbd':
            return c.conjugate(word, {'number': SINGULAR, 'person': FIRST, 'tense': PAST})
        elif pos == 'vbg':
            return c.present_part(word)
        elif pos == 'vbn':
            return c.past_part(word)
        elif pos == 'vbp':
            return word
        elif pos == 'vbz':
            return c.conjugate(word, {'number': SINGULAR, 'person': THIRD, 'tense': PRESENT})
        else:
            raise ValueError(f'Unexpected pos: {pos}')

    def _to_phone_array(self, raw):
        if not raw:
            return None
        return raw.replace('1', '').replace(' ', '-').split('-')

    def _first_phone(self, raw_phones):
        if raw_phones and len(raw_phones):
            parts = raw_phones.split(_PHONE_BOUNDARY)
            if parts:
                return parts[0]

    def _intersect(self, a1, a2):
        s2 = set(a2)
        return [x for x in a1 if x in s2]

    def _last_stressed_phone_to_end(self, word):
        raw = self.raw_phones(word)
        if raw:
            idx = raw.rfind(_STRESS)
            if idx >= 0:
                idx -= 1
                c = raw[idx] if idx >= 0 else ''
                while c not in ('-', ' '):
                    idx -= 1
                    if idx < 0:
                        return raw  # single-stressed syllable
                    c = raw[idx]
            return raw[idx + 1:]
        return None

    def _last_stressed_vowel_phoneme_to_end(self, word):
        raw = self._last_stressed_phone_to_end(word)
        if raw:
            syllables = raw.split(' ')
            last_syl = syllables[-1]
            last_syl = _re.sub(r'[^a-z\-1 ]', '', last_syl)
            idx = -1
            for i, c in enumerate(last_syl):
                if c in _VOWELS:
                    idx = i
                    break
            return last_syl[idx:]
        return None

    def _first_stressed_syl(self, word):
        raw = self.raw_phones(word)
        if raw:
            idx = raw.find(_STRESS)
            if idx >= 0:
                idx -= 1
                c = raw[idx] if idx >= 0 else ''
                while c != ' ':
                    idx -= 1
                    if idx < 0:
                        idx = 0
                        break
                    c = raw[idx]
                first_to_end = raw if idx == 0 else raw[idx:].strip()
                sp = first_to_end.find(' ')
                return first_to_end if sp < 0 else first_to_end[:sp]
        return None

    def _pos_data(self, word):
        rdata = self._lookup_raw(word)
        if rdata and len(rdata) == 2:
            return rdata[1]
        return None

    def _pos_arr(self, word):
        rdata = self._lookup_raw(word)
        if rdata and len(rdata) == 2:
            return rdata[1].split(' ')
        return []

    def _lookup_raw(self, word):
        if not word:
            return None
        return self._get_dict().get(word.lower())

    def _all_tags(self, word):
        rdata = self._lookup_raw(word)
        if rdata and len(rdata) == 2:
            return rdata[1].split(' ')
        return []

    def _is_noun(self, word):
        tags = self._all_tags(word)
        if 'nn' in tags or 'nns' in tags:
            return True
        # word may not be in dict (e.g. a freshly pluralized form); check singular
        sing = self._get_inflector().singularize(word)
        if sing != word:
            tags = self._all_tags(sing)
            return 'nn' in tags or 'nns' in tags
        return False
