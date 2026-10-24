"""
rita/tagger.py — Part-of-speech tagger
Python port of ritajs/src/tagger.js
"""
import re
import json
import os

# ── Constants ────────────────────────────────────────────────────────────────

ADJS  = ['jj', 'jjr', 'jjs']
ADVS  = ['rb', 'rbr', 'rbs', 'rp']
NOUNS = ['nn', 'nns', 'nnp', 'nnps']
VERBS = ['vb', 'vbd', 'vbg', 'vbn', 'vbp', 'vbz']

EX_BE = ["is", "are", "was", "were", "isn't", "aren't", "wasn't", "weren't"]

HYPHENATEDS = {
    "well-being":    "nn",
    "knee-length":   "jj",
    "king-size":     "jj",
    "ho-hum":        "uh",
    "roly-poly":     "jj",
    "nitty-gritty":  "nn",
    "topsy-turvy":   "jj",
}
VERB_PREFIX = ["de","over","re","dis","un","mis","out","pre","post","co","fore",
               "inter","sub","trans","under"]
NOUN_PREFIX = ["anti","auto","de","dis","un","non","co","over","under","up",
               "down","hyper","mono","bi","uni","di","semi","omni","mega","mini",
               "macro","micro","counter","ex","mal","neo","out","poly","pseudo",
               "super","sub","sur","tele","tri","ultra","vice"]
ARTICLES = ['the', 'a', 'an', 'some']

_ONLY_PUNCT = re.compile(r'^[\W_]+$', re.UNICODE)

# ── Dict cache ───────────────────────────────────────────────────────────────

_dict_cache = None

def _get_dict():
    global _dict_cache
    if _dict_cache is None:
        p = os.path.join(os.path.dirname(__file__), '..', '..', 'shared', 'rita_dict.json')
        with open(p) as f:
            _dict_cache = json.load(f)
    return _dict_cache

def _pos_arr(word):
    e = _get_dict().get(word) or _get_dict().get(word.lower())
    if e is None:
        return None
    return e[1].split() if len(e) > 1 else None

# ── Tagger ───────────────────────────────────────────────────────────────────

class Tagger:

    def __init__(self):
        self._tokenizer = None    # lazy
        self._conjugator = None   # lazy
        self._inflector = None    # lazy
        self.SILENT = False

    # ── lazy deps ────────────────────────────────────────────────────────────

    def _get_tokenizer(self):
        if self._tokenizer is None:
            from rita.tokenizer import Tokenizer
            self._tokenizer = Tokenizer()
        return self._tokenizer

    def _get_conjugator(self):
        if self._conjugator is None:
            from rita.conjugator import Conjugator, IRREG_VERBS_LEX, IRREG_VERBS_NOLEX, _IRREG_PAST_PART
            self._conjugator = Conjugator()
            self._conj_IRREG_LEX = IRREG_VERBS_LEX
            self._conj_IRREG_NOLEX = IRREG_VERBS_NOLEX
            self._conj_IRREG_PAST_PART = _IRREG_PAST_PART
        return self._conjugator

    def _get_inflector(self):
        if self._inflector is None:
            from rita.inflector import Inflector
            self._inflector = Inflector()
        return self._inflector

    # ── public API ───────────────────────────────────────────────────────────

    def is_verb(self, word=None, opts=None):
        if not word or not isinstance(word, str):
            return False
        conj = self._get_conjugator()
        if self._is_nolex_irregular_verb(word):
            return True
        # IRREG_VERBS_LEX_VB = base forms in IRREG_VERBS_LEX
        if word in self._conj_IRREG_LEX:
            return True
        if word in self._conj_IRREG_NOLEX:
            return True
        pos = self.all_tags(word, opts or {})
        return any(p in VERBS for p in pos)

    def is_noun(self, word=None):
        if not word or not isinstance(word, str):
            return False
        pos = self.all_tags(word, {'noGuessing': True})
        return any(p in NOUNS for p in pos)

    def is_adverb(self, word=None):
        if not word or not isinstance(word, str):
            return False
        pos = self.all_tags(word)
        return any(p in ADVS for p in pos)

    def is_adjective(self, word=None):
        if not word or not isinstance(word, str):
            return False
        pos = self.all_tags(word)
        return any(p in ADJS for p in pos)

    def has_tag(self, choices=None, tag=None):
        if not isinstance(choices, list):
            return False
        return tag in ''.join(choices)

    def inline_tags(self, words=None, tags=None, delimiter='/'):
        if not words:
            return ''
        if tags is None:
            tags = []
        if len(words) != len(tags):
            raise ValueError(f'Tagger: invalid state: words({len(words)})={words} tags({len(tags)})={tags}')
        delimiter = delimiter or '/'
        parts = []
        for i, w in enumerate(words):
            if _is_punct(w):
                parts.append(w)
            else:
                parts.append(w + delimiter + tags[i])
        return ' '.join(parts)

    def all_tags(self, word, opts=None):
        """Return list of all possible POS tags for word."""
        if not isinstance(opts, dict):
            opts = {}
        no_guessing    = opts.get('noGuessing', False)
        no_derivations = opts.get('noDerivations', False)
        if word and isinstance(word, str) and len(word):
            pos_data = _pos_arr(word)
            if pos_data and len(pos_data) > 0:
                return pos_data
            if '-' in word and opts.get('noGuessingOnHyphenated'):
                return []
            if not no_derivations:
                return self._derive_pos_data(word, no_guessing)
        return []

    def tag(self, input_=None, opts=None):
        """Tag a word or list of words. Returns list of tags, or inline string."""
        if opts is None:
            opts = {}
        inline = opts.get('inline', False)
        simple = opts.get('simple', False)

        if input_ is None or (hasattr(input_, '__len__') and len(input_) == 0):
            return '' if inline else []

        if isinstance(input_, list):
            words = input_
        else:
            s = input_.strip()
            if not s:
                return '' if inline else []
            words = self._get_tokenizer().tokenize(input_)

        result   = [None] * len(words)
        choices2d = [None] * len(words)

        for i, word in enumerate(words):
            if not word:
                continue
            if _is_punct(word):
                result[i] = word
            elif len(word) == 1:
                result[i] = self._handle_single_letter(word)
            else:
                all_t = self.all_tags(word, {'noGuessingOnHyphenated': True})
                choices2d[i] = all_t
                result[i] = all_t[0] if all_t else '__HYPH__'

        tags = self._apply_context(words, result, choices2d)

        if simple:
            for i in range(len(tags)):
                t = tags[i]
                if t in NOUNS:       tags[i] = 'n'
                elif t in VERBS:     tags[i] = 'v'
                elif t in ADJS:      tags[i] = 'a'
                elif t in ADVS:      tags[i] = 'r'
                else:                tags[i] = '-'

        if inline:
            return self.inline_tags(words, tags)
        return tags

    # camelCase aliases (JS API parity)
    allTags    = all_tags
    hasTag     = has_tag
    inlineTags = inline_tags

    # ── internals ────────────────────────────────────────────────────────────

    def _is_nolex_irregular_verb(self, stem):
        conj = self._get_conjugator()
        return stem in self._conj_IRREG_NOLEX.values()

    def _check_plural_noun_or_verb(self, stem, result):
        pos = _pos_arr(stem)
        if pos:
            if 'nn' in pos:
                result.append('nns')
            if 'vb' in pos:
                result.append('vbz')
        if 'vbz' not in result:
            if self._is_nolex_irregular_verb(stem):
                result.append('vbz')

    def _derive_pos_data(self, word, no_guessing=False):
        if word == 'the' or word == 'a':
            return ['dt']

        lex_posarr = _pos_arr

        if word.endswith("ress"):
            pos = lex_posarr(word[:-3])
            if pos and 'vb' in pos:
                return ['nn']
            pos = lex_posarr(word[:-4])
            if pos and 'vb' in pos:
                return ['nn']

        if word.endswith("or"):
            pos = lex_posarr(word[:-2])
            if pos and 'vb' in pos:
                return ['nn']
            pos = lex_posarr(word[:-2] + "e")
            if pos and 'vb' in pos:
                return ['nn']

        if word.endswith("er"):
            pos = lex_posarr(word[:-2])
            if pos and 'vb' in pos:
                return ['nn']
            pos = lex_posarr(word[:-1])
            if pos and 'vb' in pos:
                return ['nn']
            if len(word) >= 4 and word[-3] == word[-4]:
                pos = lex_posarr(word[:-3])
                if pos and 'vb' in pos:
                    return ['nn']

        if word.endswith('ies'):
            check = word[:-3] + 'y'
            pos = lex_posarr(check)
            if pos and 'vb' in pos:
                return ['vbz']
        elif word.endswith('s'):
            result = []
            self._check_plural_noun_or_verb(word[:-1], result)
            if word.endswith('es'):
                self._check_plural_noun_or_verb(word[:-2], result)
                infl = self._get_inflector()
                self._check_plural_noun_or_verb(infl.singularize(word), result)
            if result:
                return result

        if word.endswith('ed'):
            pos = (lex_posarr(word[:-1]) or
                   lex_posarr(word[:-2]) or
                   lex_posarr(word[:-3]))
            if pos and 'vb' in pos:
                return ['vbd', 'vbn']

        if word.endswith('ing'):
            stem = word[:-3]
            if stem:
                pos = lex_posarr(stem)
                if pos and 'vb' in pos:
                    return ['vbg', 'nn']
                pos = lex_posarr(stem + 'e')
                if pos and 'vb' in pos:
                    return ['vbg', 'nn']
                if len(word) >= 5 and word[-4] == word[-5]:
                    pos = lex_posarr(stem[:-1])
                    if pos and 'vb' in pos:
                        return ['vbg', 'nn']

        if word.endswith('ly'):
            stem = word[:-2]
            if stem:
                pos = lex_posarr(stem)
                if pos and 'jj' in pos:
                    return ['rb']
                if stem and stem[-1] == 'i':
                    pos = lex_posarr(stem[:-1] + 'y')
                    if pos and 'jj' in pos:
                        return ['rb']

        if self._is_likely_plural(word):
            return ['nns']

        conj = self._get_conjugator()
        if word in self._conj_IRREG_PAST_PART:
            return ['vbd']

        if no_guessing:
            return []
        if word.endswith('ly'):
            return ['rb']
        if word.endswith('s'):
            return ['nns']
        return ['nn']

    def _is_likely_plural(self, word):
        return self._lex_has('n', self._get_inflector().singularize(word))

    def _handle_single_letter(self, c):
        if c in ('a', 'A'):
            return 'dt'
        if '0' <= c <= '9':
            return 'cd'
        return 'prp' if c == 'I' else c

    def _apply_context(self, words, result, choices):
        for i in range(len(words)):
            word = words[i]
            tag  = result[i]
            if not word:
                continue
            if tag is None:
                tag = ''
                if not self.SILENT:
                    import sys
                    print(f'\n[WARN] Unexpected state in _apply_context for idx={i}', words, file=sys.stderr)

            # transform 1a: DT, {VBD|VBP|VB} → DT, NN
            if i > 0 and result[i-1] == 'dt':
                if tag.startswith('vb'):
                    tag = 'nn'
                    if re.match(r'^.*[^s]s$', word):
                        if word not in MASS_NOUNS:
                            tag = 'nns'
                elif tag.startswith('rb'):
                    tag = 'jj' + tag[2:] if len(tag) > 2 else 'jj'

            # transform 2: noun → cd if all digits
            if tag.startswith('n') and _is_num(word):
                tag = 'cd'

            # transform 3: noun → vbn if word ends 'ed' and follows nn/prp
            if (i > 0 and tag.startswith('n') and word.endswith('ed') and
                    result[i-1] and re.match(r'^(nn|prp)$', result[i-1])):
                if not word.endswith('eed'):
                    tag = 'vbn'

            # transform 4: anything ending 'ly' → rb
            if word.endswith('ly'):
                tag = 'rb'

            # transform 5: nn/nns + ends 'al' (len>4) → jj
            if (len(word) > 4 and tag.startswith('nn') and
                    word.endswith('al') and word != 'mammal'):
                tag = 'jj'

            # transform 6: nn after modal → vb
            if i > 0 and tag.startswith('nn') and result[i-1] and result[i-1].startswith('md'):
                tag = 'vb'

            # transform 7: vbd after vbz → vbn
            if tag == 'vbd' and i > 0 and result[i-1] and re.match(r'^(vbz)$', result[i-1]):
                tag = 'vbn'

            # transform 8: nn + ends 'ing' + choices has vbg → vbg
            if tag.startswith('nn') and word.endswith('ing'):
                if self.has_tag(choices[i], 'vbg'):
                    tag = 'vbg'

            # transform 9: nns + choices has vbz + follows nn/prp/nnp → vbz
            if (i > 0 and tag == 'nns' and self.has_tag(choices[i], 'vbz') and
                    result[i-1] and re.match(r'^(nn|prp|nnp)$', result[i-1])):
                tag = 'vbz'

            # transform 10: nn starts capital → nnp
            if tag.startswith('nn') and word and word[0].isupper():
                infl = self._get_inflector()
                sing = infl.singularize(word.lower())
                if len(words) == 1 or i > 0 or (i == 0 and not self._lex_has('nn', sing)):
                    tag = 'nnps' if tag.endswith('s') else 'nnp'

            # transform 11: nns + choices has vbz + followed by rb → vbz
            if (i < len(result)-1 and tag == 'nns' and
                    result[i+1] and result[i+1].startswith('rb') and
                    self.has_tag(choices[i], 'vbz')):
                tag = 'vbz'

            # transform 12: nns preceded by nn/prp/cc/nnp → vbz if sing is vb
            if tag == 'nns':
                if i > 0 and result[i-1] in ('nn', 'prp', 'cc', 'nnp'):
                    infl = self._get_inflector()
                    if self._lex_has('vb', infl.singularize(word)):
                        tag = 'vbz'
                elif len(words) == 1 and choices[i] is not None and len(choices[i]) < 2:
                    infl = self._get_inflector()
                    sing = infl.singularize(word.lower())
                    if not self._lex_has('nn', sing) and self._lex_has('vb', sing):
                        tag = 'vbz'

            # transform 13: vb/potential-vb after nns/nnps/prp → vbp
            if tag == 'vb' or (tag == 'nn' and self.has_tag(choices[i], 'vb')):
                if i > 0 and result[i-1] and re.match(r'^(nns|nnps|prp)$', result[i-1]):
                    tag = 'vbp'

            # sequential adjectives: nn before another nn with all jj between → jj
            if tag == 'nn' and 'nn' in result[i+1:]:
                idx = result[i+1:].index('nn')
                all_jj = all(result[i+1+k] == 'jj' for k in range(idx))
                if all_jj and 'jj' in self.all_tags(word):
                    tag = 'jj'

            # issue#148: "there"
            if word.lower() == 'there':
                if i+1 < len(words) and words[i+1] in EX_BE:
                    tag = 'ex'
                if i > 0 and result[i-1] == 'in':
                    tag = 'nn'

            # hyphenated words #HWF
            if '-' in word:
                if result[i] != '__HYPH__':
                    continue  # word is in dict, keep original tag
                if word == '--':
                    result[i] = tag
                    continue
                if word in HYPHENATEDS:
                    result[i] = HYPHENATEDS[word]
                    continue
                tag = self._tag_compound_word(word, tag, result, words, i)

            result[i] = tag
        return result

    def _tag_compound_word(self, word, tag, result, context, i):
        parts = word.split('-')
        first_part = parts[0]
        last_part  = parts[-1]
        first_all  = self.all_tags(first_part)
        last_all   = self.all_tags(last_part)

        if (len(parts) == 2 and first_part in VERB_PREFIX and
                any(re.match(r'^vb', t) for t in last_all)):
            tag = next(t for t in last_all if re.match(r'^vb', t))
        elif (len(parts) == 2 and first_part in NOUN_PREFIX and
              any(re.match(r'^nn', t) for t in last_all)):
            tag = next(t for t in last_all if re.match(r'^nn', t))
        elif any(re.match(r'^cd', t) for t in first_all):
            all_cd = all(any(re.match(r'^cd', t) for t in self.all_tags(parts[z]))
                         for z in range(1, len(parts)))
            tag = 'cd' if all_cd else 'jj'
        elif (any(t.startswith('jj') for t in first_all) and len(parts) == 2 and
              any(t.startswith('nn') for t in last_all)):
            tag = 'jj'
        elif (any(t == 'vb' for t in first_all) and
              not any(t.startswith('jj') for t in first_all)):
            if (len(parts) == 2 and any(t == 'in' for t in last_all)):
                tag = 'nn'
            elif (len(parts) == 2 and
                  any(re.match(r'^(vb[gdp])', t) for t in last_all) and
                  not any(re.match(r'^vb$', t) for t in last_all)):
                tag = 'jj'
            elif len(parts) == 2 and any(t.startswith('jj') for t in last_all):
                tag = 'jj'
            else:
                tag = 'nn'
        elif ((any(re.match(r'^(jj[rs]?)', t) for t in last_all) and
               not any(t.startswith('nn') for t in last_all)) or
              any(re.match(r'^vb[dgn]', t) for t in last_all)):
            tag = 'jj'
        elif any(re.match(r'^[n]', t) for t in last_all):
            if any(re.match(r'^(in|rb)', t) for t in first_all):
                tag = 'jj'
            else:
                last_noun_is_major = all(
                    any(re.match(r'^([jn]|dt|in)', t) for t in self.all_tags(parts[z]))
                    for z in range(len(parts)-1)
                )
                tag = 'nn' if last_noun_is_major else 'jj'
        elif any(t.startswith('n') for t in first_all):
            infl = self._get_inflector()
            tag = 'nns' if infl.is_plural(parts[0]) else 'nn'
        else:
            tag = 'nn'

        # adjust by context
        if i+1 < len(result) and result[i+1] and result[i+1].startswith('n') and tag.startswith('n'):
            tag = 'jj'
        elif tag == 'jj' and i+1 < len(result) and result[i+1] and result[i+1].startswith('v'):
            tag = 'rb'
        elif i+1 < len(result) and result[i+1] and result[i+1].startswith('v') and tag == 'jj':
            tag = 'rb'
        elif tag == 'jj' and i > 0 and context[i-1] and context[i-1].lower().strip() in ARTICLES:
            nxt = result[i+1] if i+1 < len(result) else None
            if (not context[i+1] if i+1 < len(context) else True) or \
               (nxt and re.match(r'^(v|cc|in|md|w)', nxt)) or \
               (i+1 < len(context) and _is_punct(context[i+1])):
                tag = 'nn'
        return tag

    def _lex_has(self, pos, word):
        if not isinstance(word, str):
            return False
        tags = _pos_arr(word)
        if not tags:
            return False
        for t in tags:
            if pos == t:
                return True
            if (pos == 'n' and t in NOUNS or
                pos == 'v' and t in VERBS or
                pos == 'r' and t in ADVS  or
                pos == 'a' and t in ADJS):
                return True
        return False


# ── Helpers ──────────────────────────────────────────────────────────────────

def _is_punct(text):
    return bool(text and len(text) and re.match(r'^[^\w\s]+$', text))

def _is_num(text):
    try:
        float(text.replace(',', ''))
        return True
    except (ValueError, AttributeError):
        return False


# ── MASS_NOUNS (from rita.js) ────────────────────────────────────────────────

MASS_NOUNS = frozenset([
    "abalone","asbestos","barracks","bathos","breeches","beef","britches","chaos",
    "chinese","cognoscenti","clippers","corps","cosmos","crossroads","diabetes",
    "ethos","gallows","graffiti","herpes","innings","lens","means","measles","mews",
    "mumps","news","pasta","pathos","pincers","pliers","proceedings","rabies",
    "rhinoceros","sassafras","scissors","series","shears","species","tuna",
    "acoustics","aesthetics","aquatics","basics","ceramics","classics","cosmetics",
    "dialectics","deer","dynamics","ethics","harmonics","heroics","mechanics",
    "metrics","ooze","optics","physics","polemics","pyrotechnics","statistics",
    "tactics","tropics","bengalese","bengali","bonsai","booze","cellulose","mess",
    "moose","burmese","chinese","colossus","congolese","discus","electrolysis",
    "emphasis","expertise","flu","fructose","gauze","glucose","grease","guyanese",
    "haze","incense","japanese","lebanese","malaise","mayonnaise","maltese",
    "music","money","menopause","merchandise","olympics","overuse","paradise",
    "poise","potash","portuguese","prose","recompense","remorse","repose",
    "senegalese","siamese","singhalese","sleaze","sioux","sudanese","suspense",
    "swiss","taiwanese","vietnamese","unease","aircraft","anise","antifreeze",
    "applause","archdiocese","apparatus","asparagus","bellows","bison","bluefish",
    "bourgeois","bream","brill","butterfingers","cargo","carp","catfish","chassis",
    "clone","clones","clothes","chub","cod","codfish","coley","contretemps",
    "crawfish","crayfish","cuttlefish","dice","dogfish","doings","dory","downstairs",
    "eldest","earnings","economics","electronics","firstborn","fish","flatfish",
    "flounder","fowl","fry","fries","works","goldfish","golf","grand","grief",
    "haddock","hake","halibut","headquarters","herring","hertz","honey","horsepower",
    "goods","hovercraft","ironworks","kilohertz","ling","shrimp","swine","lungfish",
    "mackerel","macaroni","megahertz","moorfowl","moorgame","mullet","myrrh",
    "nepalese","offspring","pants","patois","pekinese","perch","pickerel","pike",
    "potpourri","precis","quid","rand","rendezvous","roach","salmon","samurai",
    "seychelles","shad","sheep","shellfish","smelt","spaghetti","spacecraft",
    "starfish","stockfish","sunfish","superficies","sweepstakes","smallpox",
    "swordfish","tennis","tobacco","triceps","trout","tunafish","turbot","trousers",
    "turf","dibs","undersigned","waterfowl","waterworks","waxworks","wildfowl",
    "woodworm","yen","aries","pisces","forceps","jeans","mathematics","odds",
    "politics","remains","aids","wildlife","shall","would","may","might","ought",
    "should","acne","admiration","advice","air","anger","anticipation","assistance",
    "awareness","bacon","baggage","blood","bravery","chess","clay","clothing",
    "coal","compliance","comprehension","confusion","consciousness","cream",
    "darkness","diligence","dust","education","empathy","enthusiasm","envy",
    "equality","equipment","evidence","feedback","fitness","flattery","foliage",
    "fun","furniture","garbage","gold","gossip","grammar","gratitude","gravel",
    "guilt","happiness","hardware","hate","hay","health","heat","help","hesitation",
    "homework","honesty","honor","honour","hospitality","hostility","humanity",
    "humility","ice","immortality","independence","information","integrity",
    "intimidation","jargon","jealousy","jewelry","justice","knowledge","literacy",
    "logic","luck","lumber","luggage","mail","management","milk","morale","mud",
    "nonsense","oppression","optimism","oxygen","participation","pay","peace",
    "perseverance","pessimism","pneumonia","poetry","police","pride","privacy",
    "propaganda","public","punctuation","recovery","rice","rust","satisfaction",
    "schnapps","shame","slang","software","stamina","starvation","steam","steel",
    "stuff","support","sweat","thunder","timber","toil","traffic","tongs","training",
    "trash","valor","vehemence","violence","warmth","waste","weather","wheat",
    "wisdom","work","accommodation","advertising","aid","art","bread","business",
    "butter","calm","cash","cheese","childhood","clothing ","coffee","content",
    "corruption","courage","currency","damage","danger","determination",
    "electricity","employment","energy","entertainment","failure","fame","fire",
    "flour","food","freedom","friendship","fuel","genetics","hair","harm",
    "hospitality ","housework","humour","imagination","importance","innocence",
    "intelligence","juice","kindness","labour","lack","laughter","leisure",
    "literature","litter","love","magic","metal","motherhood","motivation","nature",
    "nutrition","obesity","oil","old age","paper","patience","permission",
    "pollution","poverty","power","production","progress","pronunciation",
    "publicity","quality","quantity","racism","rain","relaxation","research",
    "respect","room (space)","rubbish","safety","salt","sand","seafood","shopping",
    "silence","smoke","snow","soup","speed","spelling","stress ","sugar","sunshine",
    "tea","time","tolerance","trade","transportation","travel","trust",
    "understanding","unemployment","usage","vision","water","wealth","weight",
    "welfare","width","wood","yoga","youth","homecare","childcare","fanfare",
    "healthcare","medicare",
])
