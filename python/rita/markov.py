"""
rita/markov.py — Markov chain text generation.
Python port of js/src/markov.js.

RiMarkov is a thin delegation wrapper over BackoffModel (which is built on a
SuffixArray). Method names follow Python conventions (snake_case) with camelCase
aliases for JS API parity; option dict keys remain camelCase.
"""

import json
import math

from rita.model import SuffixGram
from rita.backoff import BackoffModel
from rita.util import JsDict


class RiMarkov:

    # Back-reference to RiTa (wired in rita.py); kept for compatibility.
    parent = None

    def __init__(self, input=None, opts=None):
        self.n = -1
        if isinstance(input, (int, float)) and not isinstance(input, bool):
            # v3.x compatibility: RiMarkov(n, opts)
            self.n = input
            if opts is not None:
                input = opts.get('text') or opts.get('tokens')
            else:
                input = None
        elif SuffixGram.is_object(input) and opts is None:
            opts = input
            input = opts.get('text') or opts.get('tokens')

        if opts is not None and opts.get('n') is not None and math.isfinite(opts['n']):
            self.n = opts['n']

        # save generation-relevant opts as per-instance defaults
        self.opts = JsDict()
        if opts:
            for key in BackoffModel.generationDefaults:
                if opts.get(key) is not None:
                    self.opts[key] = opts[key]

        self.model = BackoffModel(input, opts)

    # ── generation ──────────────────────────────────────────────────────────

    def stream(self, n, prompt=None, opts=None):
        prompt = [] if prompt is None else prompt
        opts = {} if opts is None else opts
        prompt, opts = self._resolve_args(n, prompt, opts)
        opts = {**self.opts, **opts}
        if not self.model.ready:
            self.model.build()
        yield from self.model.stream_tokens(self.n, prompt, opts)

    def generate(self, n=None, prompt=None, opts=None):
        prompt = [] if prompt is None else prompt
        opts = {} if opts is None else opts
        prompt, opts = self._resolve_args(n, prompt, opts)
        opts = {**self.opts, **opts}
        if not self.model.ready:
            self.model.build()
        num_sentences = opts.get('numSentences', 1)
        result = self.model.generate_sentences(self.n, prompt, {**opts, 'numSentences': num_sentences})
        return result[0] if num_sentences == 1 else result

    def generate1(self, n=None, prompt=None, opts=None):
        prompt = [] if prompt is None else prompt
        opts = {} if opts is None else opts
        return self.generate(n, prompt, {**opts, 'numSentences': 1})

    # ── input ───────────────────────────────────────────────────────────────

    def add_text(self, *args):
        return self.model.add_text(*args)

    def add_sentences(self, *args):
        return self.model.add_sentences(*args)

    def add_tokens(self, *args):
        return self.model.add_tokens(*args)

    # ── queries ─────────────────────────────────────────────────────────────

    def completions(self, pre, post=None, opts=None):
        opts = opts or {}
        if not isinstance(pre, list):
            raise Exception('Array required for pre')
        allow_special = opts.get('allowSpecial', False)
        if not self.model.ready:
            self.model.build()

        # single-array form: next-token distribution ordered by probability
        if post is None:
            dist = self.model.suffixes.pdist(pre)
            if not dist:
                return []
            items = sorted(dist.items(), key=lambda kv: -kv[1])
            return [t for t, _ in items
                    if allow_special or (t != self.model.startToken and t != self.model.endToken)]

        # two-array form: words w completing [...pre, w, ...post]
        if not isinstance(post, list):
            raise Exception('Array required for post')
        if len(pre) + len(post) >= (self.n if self.n and self.n > 0 else 3):
            raise Exception('pre.length + post.length must be less than n (%s)'
                            % (self.n if self.n and self.n > 0 else 3))
        dist = self.model.suffixes.pdist(pre)
        if not dist:
            return []
        result = []
        for w in dist:
            if not allow_special and (w == self.model.startToken or w == self.model.endToken):
                continue
            if self.model.suffixes.has_prefix(list(pre) + [w] + list(post)):
                result.append(w)
        return result

    def probability(self, prompt=None, next=None):
        raise Exception('probability() is deprecated. Use probabilities() to get the full '
                        'distribution, or compute probability of a sequence with '
                        'completions() and pdist().')

    def probabilities(self, tokens=None, opts=None):
        opts = opts or {}
        if not self.model.ready:
            self.model.build()
        if tokens is None:
            tokens = [self.model.startToken]
        if not isinstance(tokens, list):
            raise Exception('tokens[] required')
        dist = self.model.suffixes.pdist(tokens, {'temp': opts.get('temp') or 0})
        if not dist:
            return {}
        allow_special = opts.get('allowSpecial', False)
        return {t: p for t, p in dist.items()
                if allow_special or (t != self.model.startToken and t != self.model.endToken)}

    # ── misc ────────────────────────────────────────────────────────────────

    def size(self):
        return self.model.size()

    def to_string(self, opts=None):
        return self.model.to_string(opts)

    def __str__(self):
        return self.to_string()

    def to_json(self):
        if not self.model.ready:
            self.model.build()
        data = {'n': self.n or -1}
        data.update(self.model.to_json())
        return json.dumps(data)

    @staticmethod
    def from_json(json_data):
        if not isinstance(json_data, str):
            raise Exception('String required for from_json()')
        rm = RiMarkov()
        parsed = json.loads(json_data)
        n = parsed.pop('n', -1)
        rm.model = BackoffModel.from_json(parsed)
        rm.n = n
        return rm

    # ── internals ───────────────────────────────────────────────────────────

    def _resolve_args(self, n, prompt, opts):
        if SuffixGram.is_object(n):
            opts = dict(n)
            prompt = opts.pop('prompt', [])
            n = opts.pop('n', None)
        elif isinstance(n, list):
            opts = prompt if prompt is not None else {}
            prompt = n
            n = opts.get('n') if isinstance(opts, dict) else None
        elif SuffixGram.is_object(prompt):
            opts = dict(prompt)
            prompt = opts.pop('prompt', [])

        if not isinstance(prompt, list):
            raise Exception('Array required for prompt')

        self.n = n if n is not None else (opts.get('n') if isinstance(opts, dict) else None) or self.n
        if self.n < 1:
            raise Exception('n must be specified before calling generate() or stream()')

        return prompt, (opts if isinstance(opts, dict) else {})

    # ── camelCase aliases (JS API parity) ───────────────────────────────────
    addText = add_text
    addSentences = add_sentences
    addTokens = add_tokens
    generateSentences = generate
    toJSON = to_json
    toString = to_string
    fromJSON = from_json
