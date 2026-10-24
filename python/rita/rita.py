"""
rita/rita.py — Top-level RiTa facade
Python port of ritajs/src/rita.js
"""
import re
import math
import sys
import os

# ── Lazy import for RiScript (lives at project root) ─────────────────────────
_root = os.path.dirname(os.path.dirname(__file__))
if _root not in sys.path:
    sys.path.insert(0, _root)

from rita.randgen import RandGen
from rita.stemmer import Stemmer
from rita.tagger import Tagger
from rita.analyzer import Analyzer
from rita.tokenizer import Tokenizer
from rita.inflector import Inflector
from rita.lexicon import Lexicon
from rita.conjugator import Conjugator
from rita.concorder import Concorder
from rita.markov import RiMarkov
from rita.util import Util


# ── Only-punctuation regex (mirrors JS ONLY_PUNCT) ───────────────────────────
_ONLY_PUNCT = re.compile(
    r'^[\u0021-\u002F\u003A-\u0040\u005B-\u0060\u007B-\u007E'
    r'\u00A1-\u00BF\u2010-\u2027\u2030-\u205E\u2060-\u2FFF'
    r'\+\-<>\^\$\ufffd`\u2018\u2019\u201C\u201D\u00AB\u00BB\u27E8\u27E9%]*$'
)
_IS_LETTER = re.compile(r'^[a-z\u00C0-\u00ff]+$', re.I)


class RiTa:
    """Top-level facade for the RiTa library (mirrors ritajs/src/rita.js)."""

    # ── Numeric constants ─────────────────────────────────────────────────────
    FIRST = 1;   SECOND = 2;   THIRD = 3
    PAST  = 4;   PRESENT = 5;  FUTURE = 6
    SINGULAR = 7; PLURAL = 8;  NORMAL = 9
    INFINITIVE = 1; GERUND = 2

    # ── String constants ──────────────────────────────────────────────────────
    STRESS           = '1'
    NOSTRESS         = '0'
    PHONE_BOUNDARY   = '-'
    WORD_BOUNDARY    = ' '
    SYLLABLE_BOUNDARY= '/'
    SENTENCE_BOUNDARY= '|'
    VOWELS           = 'aeiou'

    # ── Flags ─────────────────────────────────────────────────────────────────
    SILENT            = False
    SILENCE_LTS       = False
    SPLIT_CONTRACTIONS= False

    # ── Lists ─────────────────────────────────────────────────────────────────
    PHONES = [
        'aa','ae','ah','ao','aw','ay','b','ch','d','dh','eh','er','ey',
        'f','g','hh','ih','iy','jh','k','l','m','n','ng','ow','oy','p',
        'r','s','sh','t','th','uh','uw','v','w','y','z','zh'
    ]
    ABRV = [
        "Adm.","Capt.","Cmdr.","Col.","Dr.","Gen.","Gov.","Lt.","Maj.",
        "Messrs.","Mr.","Mrs.","Ms.","Prof.","Rep.","Reps.","Rev.","Sen.",
        "Sens.","Sgt.","Sr.","St.","A.k.a.","C.f.","I.e.","E.g.","Vs.",
        "V.","Jan.","Feb.","Mar.","Apr.","Mar.","Jun.","Jul.","Aug.",
        "Sept.","Oct.","Nov.","Dec."
    ]
    QUESTIONS = [
        "was","what","when","where","which","why","who","will","would",
        "who","how","if","is","could","might","does","are","have"
    ]
    STOP_WORDS = [
        "and","a","of","in","i","you","is","to","that","it","for","on",
        "have","with","this","be","not","are","as","was","but","or","from",
        "my","at","if","they","your","all","he","by","one","me","what","so",
        "can","will","do","an","about","we","just","would","there","no","like",
        "out","his","has","up","more","who","when","don't","some","had","them",
        "any","their","it's","only","which","i'm","been","other","were","how",
        "then","now","her","than","she","well","also","us","very","because",
        "am","here","could","even","him","into","our","much","too","did",
        "should","over","want","these","may","where","most","many","those",
        "does","why","please","off","going","its","i've","down","that's",
        "can't","you're","didn't","another","around","must","few","doesn't",
        "the","every","yes","each","maybe","i'll","away","doing","oh","else",
        "isn't","he's","there's","hi","won't","ok","they're","yeah","mine",
        "we're","what's","shall","she's","hello","okay","here's","less",
        "didn't","said","over","this","that","just","then","under","some"
    ]
    MASS_NOUNS = [
        "abalone","asbestos","barracks","bathos","breeches","beef","britches",
        "chaos","chinese","cognoscenti","clippers","corps","cosmos","crossroads",
        "diabetes","ethos","gallows","graffiti","herpes","innings","lens","means",
        "measles","mews","mumps","news","pasta","pathos","pincers","pliers",
        "proceedings","rabies","rhinoceros","sassafras","scissors","series",
        "shears","species","tuna","acoustics","aesthetics","aquatics","basics",
        "ceramics","classics","cosmetics","dialectics","deer","dynamics","ethics",
        "harmonics","heroics","mechanics","metrics","ooze","optics","physics",
        "polemics","pyrotechnics","statistics","tactics","tropics","bengalese",
        "bengali","bonsai","booze","cellulose","mess","moose","burmese","chinese",
        "colossus","congolese","discus","electrolysis","emphasis","expertise",
        "flu","fructose","gauze","glucose","grease","guyanese","haze","incense",
        "japanese","lebanese","malaise","mayonnaise","maltese","music","money",
        "menopause","merchandise","olympics","overuse","paradise","poise","potash",
        "portuguese","prose","recompense","remorse","repose","senegalese","siamese",
        "singhalese","sleaze","sioux","sudanese","suspense","swiss","taiwanese",
        "vietnamese","unease","aircraft","anise","antifreeze","applause",
        "archdiocese","apparatus","asparagus","bellows","bison","bluefish",
        "bourgeois","bream","brill","butterfingers","cargo","carp","catfish",
        "chassis","clone","clones","clothes","chub","cod","codfish","coley",
        "contretemps","crawfish","crayfish","cuttlefish","dice","dogfish","doings",
        "dory","downstairs","eldest","earnings","economics","electronics",
        "firstborn","fish","flatfish","flounder","fowl","fry","fries","works",
        "goldfish","golf","grand","grief","haddock","hake","halibut","headquarters",
        "herring","hertz","honey","horsepower","goods","hovercraft","ironworks",
        "kilohertz","ling","shrimp","swine","lungfish","mackerel","macaroni",
        "megahertz","moorfowl","moorgame","mullet","myrrh","nepalese","offspring",
        "pants","patois","pekinese","perch","pickerel","pike","potpourri","precis",
        "quid","rand","rendezvous","roach","salmon","samurai","seychelles","shad",
        "sheep","shellfish","smelt","spaghetti","spacecraft","starfish","stockfish",
        "sunfish","superficies","sweepstakes","smallpox","swordfish","tennis",
        "tobacco","triceps","trout","tunafish","turbot","trousers","turf","dibs",
        "undersigned","waterfowl","waterworks","waxworks","wildfowl","woodworm",
        "yen","aries","pisces","forceps","jeans","mathematics","odds","politics",
        "remains","aids","wildlife","shall","would","may","might","ought","should",
        "acne","admiration","advice","air","anger","anticipation","assistance",
        "awareness","bacon","baggage","blood","bravery","chess","clay","clothing",
        "coal","compliance","comprehension","confusion","consciousness","cream",
        "darkness","diligence","dust","education","empathy","enthusiasm","envy",
        "equality","equipment","evidence","feedback","fitness","flattery","foliage",
        "fun","furniture","garbage","gold","gossip","grammar","gratitude","gravel",
        "guilt","happiness","hardware","hate","hay","health","heat","help",
        "hesitation","homework","honesty","honor","honour","hospitality","hostility",
        "humanity","humility","ice","immortality","independence","information",
        "integrity","intimidation","jargon","jealousy","jewelry","justice",
        "knowledge","literacy","logic","luck","lumber","luggage","mail","management",
        "milk","morale","mud","nonsense","oppression","optimism","oxygen",
        "participation","pay","peace","perseverance","pessimism","pneumonia",
        "poetry","police","pride","privacy","propaganda","public","punctuation",
        "recovery","rice","rust","satisfaction","schnapps","shame","slang",
        "software","stamina","starvation","steam","steel","stuff","support",
        "sweat","thunder","timber","toil","traffic","tongs","training","trash",
        "valor","vehemence","violence","warmth","waste","weather","wheat","wisdom",
        "work","accommodation","advertising","aid","art","bread","business","butter",
        "calm","cash","cheese","childhood","coffee","content","corruption","courage",
        "currency","damage","danger","determination","electricity","employment",
        "energy","entertainment","failure","fame","fire","flour","food","freedom",
        "friendship","fuel","genetics","hair","harm","housework","humour",
        "imagination","importance","innocence","intelligence","juice","kindness",
        "labour","lack","laughter","leisure","literature","litter","love","magic",
        "metal","motherhood","motivation","nature","nutrition","obesity","oil",
        "paper","patience","permission","pollution","poverty","power","production",
        "progress","pronunciation","publicity","quality","quantity","racism","rain",
        "relaxation","research","respect","rubbish","safety","salt","sand",
        "seafood","shopping","silence","smoke","snow","soup","speed","spelling",
        "sugar","sunshine","tea","time","tolerance","trade","transportation",
        "travel","trust","understanding","unemployment","usage","vision","water",
        "wealth","weight","welfare","width","wood","yoga","youth","homecare",
        "childcare","fanfare","healthcare","medicare"
    ]

    # ── Component instances (class-level) ─────────────────────────────────────
    randomizer = RandGen()
    tagger     = Tagger()
    analyzer   = Analyzer()
    tokenizer  = Tokenizer()
    inflector  = Inflector()
    lexicon    = Lexicon()
    conjugator = Conjugator()
    stemmer    = Stemmer()
    concorder  = Concorder()
    Util       = Util

    # riscript is set up after class definition (needs RiTa backref)
    riscript = None

    # ── RiScript / Grammar methods ────────────────────────────────────────────

    @classmethod
    def evaluate(cls, script, context=None, opts=None):
        if opts is None:
            opts = {}
        if isinstance(opts, int):
            opts = {}
        return cls.riscript.evaluate(script, context, **opts)

    @classmethod
    def grammar(cls, rules=None, context=None, opts=None):
        from riscript import RiGrammar
        opts = opts or {}
        return RiGrammar(rules, context, **opts)

    @classmethod
    def add_transform(cls, name, fn):
        cls.riscript.add_transform(name, fn)

    @classmethod
    def remove_transform(cls, name):
        cls.riscript.remove_transform(name)

    @classmethod
    def get_transforms(cls):
        from riscript import DEFAULT_TRANSFORMS
        result = dict(DEFAULT_TRANSFORMS)
        result.update(cls.riscript.extra_transforms)
        return result

    # camelCase aliases
    addTransform    = add_transform
    removeTransform = remove_transform
    getTransforms   = get_transforms

    # ── Articlize ─────────────────────────────────────────────────────────────

    @classmethod
    def articlize(cls, word):
        if not word:
            return word
        first_word = word.split()[0] if word.split() else word
        try:
            ph = cls.phones(first_word)
            if ph:
                first_phone = ph.split('-')[0]
                article = 'an ' if first_phone in ('aa','ae','ah','ao','aw','ay','eh','er','ey','ih','iy','ow','oy','uh','uw') else 'a '
                return article + word
        except Exception:
            pass
        import re
        return ('an ' if re.match(r'[aeiouAEIOU]', word) else 'a ') + word

    # ── Random helpers ────────────────────────────────────────────────────────

    @classmethod
    def random(cls, *args):
        return cls.randomizer.random(*args)

    @classmethod
    def randi(cls, *args):
        if not args:
            return 0
        return int(math.floor(cls.random(*args)))

    @classmethod
    def random_seed(cls, seed):
        cls.randomizer.seed(seed)

    @classmethod
    def random_ordering(cls, arg):
        return cls.randomizer.random_ordering(arg)

    # camelCase aliases
    randomSeed     = random_seed
    randomOrdering = random_ordering

    # ── Boolean checks ────────────────────────────────────────────────────────

    @classmethod
    def is_question(cls, sentence):
        if not sentence:
            return False
        tokens = cls.tokenizer.tokenize(sentence)
        if not tokens or not tokens[0]:
            return False
        first = tokens[0].lower()
        return first in cls.QUESTIONS

    @classmethod
    def is_vowel(cls, char):
        if not char or len(char) != 1:
            return False
        return char.lower() in cls.VOWELS

    @classmethod
    def is_consonant(cls, char):
        if not char or len(char) != 1:
            return False
        c = char.lower()
        return c not in cls.VOWELS and bool(_IS_LETTER.match(c))

    @classmethod
    def is_punct(cls, text):
        if not text:
            return False
        return bool(_ONLY_PUNCT.match(text))

    @classmethod
    def is_stop_word(cls, word):
        if not word:
            return False
        return word.lower() in cls.STOP_WORDS

    @classmethod
    def is_abbrev(cls, input_, opts=None):
        if not input_ or not isinstance(input_, str):
            return False
        opts = opts or {}
        case_sensitive = opts.get('caseSensitive', False)
        word = input_.strip()
        if not word:
            return False
        if case_sensitive:
            return word in cls.ABRV
        word_lower = word.lower()
        return any(a.lower() == word_lower for a in cls.ABRV)

    # camelCase aliases
    isQuestion   = is_question
    isVowel      = is_vowel
    isConsonant  = is_consonant
    isPunct      = is_punct
    isStopWord   = is_stop_word
    isAbbrev     = is_abbrev

    # ── String helpers ────────────────────────────────────────────────────────

    @classmethod
    def capitalize(cls, s):
        if not s:
            return s
        return s[0].upper() + s[1:]

    # ── POS / tagger ─────────────────────────────────────────────────────────

    @classmethod
    def pos(cls, word, opts=None):
        return cls.tagger.tag(word, opts)

    @classmethod
    def pos_inline(cls, sentence, opts=None):
        opts = dict(opts or {})
        opts['inline'] = True
        return cls.tagger.tag(sentence, opts)

    @classmethod
    def is_noun(cls, word=None):
        return cls.tagger.is_noun(word)

    @classmethod
    def is_verb(cls, word=None):
        return cls.tagger.is_verb(word)

    @classmethod
    def is_adjective(cls, word=None):
        return cls.tagger.is_adjective(word)

    @classmethod
    def is_adverb(cls, word=None):
        return cls.tagger.is_adverb(word)

    # camelCase aliases
    posInline    = pos_inline
    isNoun       = is_noun
    isVerb       = is_verb
    isAdjective  = is_adjective
    isAdverb     = is_adverb

    # ── Inflector ─────────────────────────────────────────────────────────────

    @classmethod
    def pluralize(cls, word=None, opts=None):
        return cls.inflector.pluralize(word, opts)

    @classmethod
    def singularize(cls, word=None, opts=None):
        return cls.inflector.singularize(word, opts)

    # ── Lexicon ───────────────────────────────────────────────────────────────

    @classmethod
    def random_word(cls, pattern=None, opts=None):
        return cls.lexicon.random_word(pattern, opts)

    @classmethod
    def has_word(cls, word, opts=None):
        return cls.lexicon.has_word(word, opts)

    @classmethod
    def rhymes(cls, word, opts=None):
        return cls.lexicon.rhymes_sync(word, opts)

    @classmethod
    def is_rhyme(cls, word1, word2):
        return cls.lexicon.is_rhyme(word1, word2)

    @classmethod
    def alliterations(cls, word, opts=None):
        return cls.lexicon.alliterations_sync(word, opts)

    @classmethod
    def is_alliteration(cls, word1, word2):
        return cls.lexicon.is_alliteration(word1, word2)

    @classmethod
    def spells_like(cls, word, opts=None):
        return cls.lexicon.spells_like_sync(word, opts)

    @classmethod
    def sounds_like(cls, word, opts=None):
        return cls.lexicon.sounds_like_sync(word, opts)

    @classmethod
    def search(cls, pattern=None, opts=None):
        return cls.lexicon.search_sync(pattern, opts)

    # camelCase aliases
    randomWord      = random_word
    hasWord         = has_word
    isRhyme         = is_rhyme
    isAlliteration  = is_alliteration
    spellsLike      = spells_like
    soundsLike      = sounds_like
    spellsLikeSync  = spells_like
    soundsLikeSync  = sounds_like
    rhymesSync      = rhymes
    searchSync      = search
    alliterationsSync = alliterations

    # ── Stemmer ───────────────────────────────────────────────────────────────

    @classmethod
    def stem(cls, word):
        return Stemmer.stem(word)

    # ── Conjugator ────────────────────────────────────────────────────────────

    @classmethod
    def conjugate(cls, verb, opts=None):
        return cls.conjugator.conjugate(verb, opts)

    @classmethod
    def present_part(cls, verb):
        return cls.conjugator.present_part(verb)

    @classmethod
    def past_part(cls, verb):
        return cls.conjugator.past_part(verb)

    # camelCase aliases
    presentPart = present_part
    pastPart    = past_part

    # ── Analyzer ─────────────────────────────────────────────────────────────

    @classmethod
    def analyze(cls, input_, opts=None):
        return cls.analyzer.analyze(input_, opts)

    @classmethod
    def stresses(cls, input_, opts=None):
        return cls.analyzer.analyze(input_, opts).get('stresses', '')

    @classmethod
    def syllables(cls, input_, opts=None):
        return cls.analyzer.syllables(input_, opts)

    @classmethod
    def phones(cls, input_, opts=None):
        return cls.analyzer.phones(input_, opts)

    # ── Tokenizer ─────────────────────────────────────────────────────────────

    @classmethod
    def tokenize(cls, text, opts=None):
        return cls.tokenizer.tokenize(text, opts)

    @classmethod
    def untokenize(cls, tokens, delim=' '):
        return cls.tokenizer.untokenize(tokens, delim)

    @classmethod
    def sentences(cls, text, pattern=None):
        return cls.tokenizer.sentences(text, pattern)

    @classmethod
    def tokens(cls, text, opts=None):
        return cls.tokenizer.tokens(text, opts)

    # ── Concorder ─────────────────────────────────────────────────────────────

    @classmethod
    def concordance(cls, text, opts=None):
        if text is None:
            raise TypeError('concordance() requires text argument')
        return cls.concorder.concordance(text, opts)

    @classmethod
    def kwic(cls, word, opts=None):
        return cls.concorder.kwic(word, opts)

    # ── Markov ────────────────────────────────────────────────────────────────

    @classmethod
    def markov(cls, n=3, opts=None):
        m = RiMarkov(n, opts)
        m.parent = cls
        return m


# ── Wire up back-references after class definition ───────────────────────────

# Give components a reference to RiTa so they can read SPLIT_CONTRACTIONS, etc.
RiTa.tokenizer.rita  = RiTa
RiTa.concorder.rita  = RiTa
RiTa.analyzer.rita   = RiTa

# Set up RiScript with RiTa backref
from riscript import RiScript, RiGrammar  # noqa: E402

def _rita_articlize(word):
    return RiTa.articlize(word)

RiTa.riscript = RiScript(
    transforms={'articlize': _rita_articlize, 'art': _rita_articlize},
    rita=RiTa,
)

# Expose RiScript / RiGrammar as RiTa attributes (JS API parity).
RiTa.RiScript = RiScript
RiTa.RiGrammar = RiGrammar

# Wire Stemmer tokenizer
Stemmer.tokenizer = RiTa.tokenizer

# Wire RiMarkov parent
RiMarkov.parent = RiTa

# Expose RiMarkov as RiTa.RiMarkov (JS API parity: const { RiMarkov } = RiTa)
RiTa.RiMarkov = RiMarkov

# Wire the suffix-array model stack (BackoffModel / SuffixArray / SuffixGram).
# These give RiTa the tokenizer/untokenizer and seeded RNG they need, and expose
# them as RiTa attributes for JS API parity (const { BackoffModel, SuffixArray } = RiTa).
from rita.suffixes import SuffixArray          # noqa: E402
from rita.model import SuffixGram              # noqa: E402
from rita.backoff import BackoffModel          # noqa: E402

SuffixArray.RiTa = RiTa
SuffixGram.RiTa = RiTa
RiTa.SuffixArray = SuffixArray
RiTa.BackoffModel = BackoffModel
