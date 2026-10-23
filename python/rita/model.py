"""
SuffixGram — Python port of js/src/model.js.

Base class for models that build on a SuffixArray (e.g. BackoffModel).
Handles token/sentence/text ingestion, options, and serialization.
"""

import math

from rita.suffixes import SuffixArray


class SuffixGram:

    SILENT = False
    RiTa = None  # back-reference for default tokenizer/untokenizer

    defaults = {
        'debug': False,
        'ready': False,
        'suffixes': False,
        'compressed': False,
        'startToken': SuffixArray.SEQ_START_TOKEN,
        'endToken': SuffixArray.SEQ_END_TOKEN,
        'tokenize': None,
        'untokenize': None,
    }

    # NOTE: JS declares a vestigial `static __dict__` list that is never used by
    # toJSON (which is `Object.assign({}, this)`). We must NOT define it as a class
    # attribute here because `__dict__` would shadow the instance `__dict__`
    # descriptor and break `self.__dict__` (name mangling does not apply to dunders).

    options = list(defaults.keys())

    def __init__(self, input=None, opts=None):
        if SuffixGram.RiTa is not None:
            if SuffixGram.defaults['tokenize'] is None:
                SuffixGram.defaults['tokenize'] = SuffixGram.RiTa.tokenize
            if SuffixGram.defaults['untokenize'] is None:
                SuffixGram.defaults['untokenize'] = SuffixGram.RiTa.untokenize

        # JS-facing fields are camelCase attributes (this.startToken, etc.).
        self.startToken = None
        self.endToken = None
        self.tokenize = None
        self.untokenize = None
        self.tokens = []
        self.tokenCount = 0
        self.suffixes = None
        self.ready = False
        self.debug = False
        self.compressed = False

        # only an options object
        if SuffixGram.is_object(input) and opts is None:
            opts = input
            input = None

        # initialize with options or default values
        for key in SuffixGram.options:
            setattr(self, key, SuffixGram.defaults[key])
            if opts is not None and opts.get(key) is not None:
                setattr(self, key, opts[key])

        if input is None:
            if opts is not None and opts.get('text') is not None:
                if not isinstance(opts['text'], str):
                    raise Exception('String required for `text` option, got ' +
                                    type(opts['text']).__name__)
                input = opts['text']
            elif opts is not None and opts.get('tokens') is not None:
                if not isinstance(opts['tokens'], list):
                    raise Exception('Array of tokens required for `tokens` option')
                input = opts['tokens']
            elif opts is not None and opts.get('sentences') is not None:
                if not isinstance(opts['sentences'], list):
                    raise Exception('Array of sentences required for `sentences` option')
                input = self._tokenize_sentences(opts['sentences'])

        if input is not None:
            if isinstance(input, list):
                self.add_tokens(input)
            elif isinstance(input, str):
                self.add_text(input)
            else:
                raise Exception('String or array required')
            self.build()

    def to_json(self):
        # JS: Object.assign({}, this) then JSON.stringify — function-valued props
        # (tokenize/untokenize) are dropped by stringify, so skip callables here.
        result = {}
        for k, v in self.__dict__.items():
            if callable(v):
                continue
            if isinstance(v, SuffixArray):
                v = v.to_json()
            result[k] = v
        return result

    def __eq__(self, other):
        # JS `expect(a).to.eql(b)` is deep structural equality. Compare the
        # serialised form (which embeds the suffix array records).
        if not isinstance(other, SuffixGram):
            return NotImplemented
        return self.to_json() == other.to_json()

    def __ne__(self, other):
        eq = self.__eq__(other)
        return eq if eq is NotImplemented else not eq

    def __getitem__(self, key):
        # JS `model[key]` is property access; option keys are camelCase attrs.
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def build(self, opts=None):
        raise Exception('Model.build() not implemented')

    def size(self):
        if not self.ready:
            self.build()
        return self.tokenCount

    def to_string(self, opts=None):
        if not self.ready:
            self.build()
        return self.suffixes.to_string(opts)

    def __str__(self):
        return self.to_string()

    def add_text(self, raw_text):
        if not isinstance(raw_text, str):
            raise Exception('String required: if adding an array see add_tokens() or add_sentences()')
        if len(raw_text) == 0:
            return self
        return self.add_sentences(SuffixGram.RiTa.sentences(raw_text))

    def add_sentences(self, sentences):
        toks = self._tokenize_sentences(sentences)
        return self.add_tokens(toks)

    def add_tokens(self, tokens):
        self.ready = False
        if isinstance(tokens, list) and len(tokens) > 0 and isinstance(tokens[0], str):
            self.tokens = (self.tokens or []) + (tokens or [])
        elif isinstance(tokens, list) and len(tokens) == 0:
            pass
        else:
            raise Exception('Array of individual tokens required, got ' +
                            type(tokens).__name__)
        return self

    # ── privates ────────────────────────────────────────────────────────────

    def _validate_options(self, opts, valid_keys, ignorable_keys=None):
        ignorable_keys = ignorable_keys or []
        if opts is not None and not SuffixGram.is_object(opts):
            raise Exception('Options must be an object')
        for key in (opts or {}):
            if key not in valid_keys and key not in ignorable_keys:
                raise Exception('Invalid option key: ' + str(key))

    def _tokenize_sentences(self, sentences):
        toks = []
        for s in sentences:
            toks.append(self.startToken)
            toks.extend(self.tokenize(s))
            toks.append(self.endToken)
        return toks

    # ── statics ─────────────────────────────────────────────────────────────

    @staticmethod
    def clean_dist(dist, indent, nosort=False):
        entries = list(dist.items())
        if not nosort:
            entries.sort(key=lambda kv: -kv[1])
        truncated = False
        if len(entries) > 10:
            entries = entries[:15]
            truncated = True
        out = ''
        for i, (k, v) in enumerate(entries):
            out += ' ' * (indent + 2) + str(k) + ': ' + ('%.2f' % v) + ','
            if i < len(entries) - 1:
                out += '\n'
        return (out + '\n' + ' ' * (indent + 2) + '...') if truncated else out

    @staticmethod
    def is_object(obj):
        return isinstance(obj, dict)

    @staticmethod
    def random():
        if SuffixGram.RiTa is not None:
            return SuffixGram.RiTa.randomizer.random()
        import random as _random
        return _random.random()
