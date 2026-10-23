"""
rita/concorder.py — Concorder for RiTa
Python port of ritajs/src/concorder.js
"""


class Concorder:
    """Builds word-frequency models and supports keyword-in-context (KWIC) queries."""

    def __init__(self, rita=None):
        self.rita = rita
        self.model = None
        self.words = None
        self.ignore_case = False
        self.ignore_stop_words = False
        self.ignore_punctuation = False
        self.words_to_ignore = []

    # ── Public API ────────────────────────────────────────────────────────────

    def concordance(self, text, options=None):
        options = options or {}
        self.words = (
            text if isinstance(text, list)
            else self.rita.tokenize(text)
        )
        self.ignore_case = options.get('ignoreCase', False)
        self.ignore_stop_words = options.get('ignoreStopWords', False)
        self.ignore_punctuation = options.get('ignorePunctuation', False)
        self.words_to_ignore = options.get('wordsToIgnore', [])

        self._build_model()

        result = {}
        for key, entry in self.model.items():
            result[key] = len(entry['indexes'])
        return result

    def kwic(self, word, opts=None):
        num_words = 6

        if isinstance(opts, dict):
            num_words = opts.get('numWords', 6)
            if opts.get('text'):
                self.concordance(opts['text'], opts)
            elif opts.get('words'):
                self.concordance(opts['words'], opts)
        elif isinstance(opts, int):
            num_words = opts

        if self.model is None:
            raise RuntimeError('Call concordance() first')

        result = []
        entry = self._lookup(word)
        if entry:
            idxs = entry['indexes']
            for i, idx in enumerate(idxs):
                sub = self.words[max(0, idx - num_words):min(len(self.words), idx + num_words + 1)]
                if i < 1 or (idx - idxs[i - 1]) > num_words:
                    result.append(self.rita.untokenize(sub))
        return result

    def count(self, word):
        entry = self._lookup(word)
        return len(entry['indexes']) if entry else 0

    # ── Private ───────────────────────────────────────────────────────────────

    def _build_model(self):
        if not self.words:
            raise RuntimeError('No text in model')
        self.model = {}
        for j, word in enumerate(self.words):
            if self._is_ignorable(word):
                continue
            entry = self._lookup(word)
            if entry is None:
                entry = {'word': word, 'key': self._compare_key(word), 'indexes': []}
                self.model[entry['key']] = entry
            entry['indexes'].append(j)

    def _is_ignorable(self, word):
        if self.ignore_punctuation and self.rita and self.rita.is_punct(word):
            return True
        if self.ignore_stop_words and self.rita and self.rita.is_stop_word(word):
            return True
        for w in self.words_to_ignore:
            if word == w or (self.ignore_case and word.upper() == w.upper()):
                return True
        return False

    def _compare_key(self, word):
        return word.lower() if self.ignore_case else word

    def _lookup(self, word):
        return self.model.get(self._compare_key(word)) if self.model else None
