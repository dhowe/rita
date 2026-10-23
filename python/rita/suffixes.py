"""
SuffixArray — Python port of js/src/suffixes.js.

A compressed suffix array over a token sequence, used by BackoffModel/RiMarkov
for n-gram lookup, prefix/suffix search, and probability distributions.

Method names follow Python conventions (snake_case); option dict keys remain
camelCase to match the JS-origin test suite (consistent with the rest of the port).
"""

import json
import math

EOL = '\n'


class _Undefined:
    """Mimics JS `undefined`: never equal to a real value, never ordered.

    JS returns `undefined` for out-of-range array reads and for `encoder[unknown]`.
    Comparisons against `undefined` are always false (`x < undefined`, `undefined < x`,
    `x === undefined` are all false), while `undefined === undefined` is true. This
    singleton reproduces that so encoded-unknown tokens never match any real token.
    """
    _singleton = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super().__new__(cls)
        return cls._singleton

    def __eq__(self, other):
        return isinstance(other, _Undefined)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return False

    def __gt__(self, other):
        return False

    def __le__(self, other):
        return False

    def __ge__(self, other):
        return False

    def __hash__(self):
        return 0

    def __repr__(self):
        return 'undefined'


# Sentinel for out-of-range array reads / unknown tokens (JS returns undefined there).
_UNSET = _Undefined()


def _rawcmp(a, b):
    if a == b:
        return 0
    return -1 if a < b else 1


def _softmax(logits, temp=1):
    if temp == 0:
        return _normalize(dict(enumerate(logits)))
    temp = max(temp, 0.000001)
    scaled = [math.exp(v / temp) for v in logits]
    total = sum(scaled)
    return [v / total for v in scaled]


def _normalize(dist):
    total = sum(dist.values())
    if total == 0:
        return {k: 0 for k in dist}
    return {k: v / total for k, v in dist.items()}


class SuffixArray:

    SILENT = True
    XOVER_WINDOW = 8
    SEQ_START_TOKEN = '<s>'
    SEQ_END_TOKEN = '</s>'
    USE_COMPRESSION = True

    # Back-reference to RiTa for the shared seeded RNG (wired in rita.py).
    RiTa = None

    @staticmethod
    def random():
        if SuffixArray.RiTa is not None:
            return SuffixArray.RiTa.randomizer.random()
        import random as _random
        return _random.random()

    def keys(self):
        # JS Object.keys(suffixes) returns the instance's own property names.
        return list(self.__dict__.keys())

    def __eq__(self, other):
        # JS deep-equal of two suffix arrays: compare the serialised records.
        if not isinstance(other, SuffixArray):
            return NotImplemented
        return self.to_json() == other.to_json()

    def __ne__(self, other):
        eq = self.__eq__(other)
        return eq if eq is NotImplemented else not eq

    def __getitem__(self, key):
        # JS `sa[key]` is property access; keys are camelCase, attrs snake_case.
        return getattr(self, self._PROP_ATTR.get(key, key))

    def __setitem__(self, key, value):
        setattr(self, self._PROP_ATTR.get(key, key), value)

    __props__ = ['startToken', 'endToken', 'xoverWindow', 'compressed',
                 'length', 'decoder', 'encoder']

    # JS `static __dict__` — the full list of instance field names (props + data).
    _FIELDS = __props__ + ['input', 'seqmap', 'data', 'xovers']

    # Serialization keys (JS-facing camelCase) -> instance attribute names.
    _PROP_ATTR = {
        'startToken': 'start_token', 'endToken': 'end_token',
        'xoverWindow': 'xover_window', 'compressed': 'compressed',
        'length': 'length', 'decoder': 'decoder', 'encoder': 'encoder',
    }

    def __init__(self, s=None, opts=None):
        opts = opts or {}
        self.length = 0
        self.input = []
        self.seqmap = []
        self.data = []
        self.xovers = []

        self.decoder = None
        self.encoder = None
        self._start_indexes = None
        self._start_index_dist = None

        self.start_token = opts.get('startToken', SuffixArray.SEQ_START_TOKEN)
        self.end_token = opts.get('endToken', SuffixArray.SEQ_END_TOKEN)
        self.xover_window = opts.get('xoverWindow', SuffixArray.XOVER_WINDOW)
        self.compressed = opts.get('compressed', SuffixArray.USE_COMPRESSION)

        if s is not None:
            if not isinstance(s, list):
                raise Exception('Expected array of tokens')
            inp = self.compress_tokens(s) if self.compressed else s
            self.build(inp)

    # camelCase attribute aliases (JS API parity for property reads)
    @property
    def startToken(self):
        return self.start_token

    @property
    def endToken(self):
        return self.end_token

    def compress_tokens(self, input):
        if not input:
            return input
        words = list(dict.fromkeys(input))  # preserve-then-sort semantics below
        self.decoder = sorted(set(input))
        self.encoder = {w: i for i, w in enumerate(self.decoder)}
        return [self.encoder[w] for w in input]

    @staticmethod
    def init_from_meta(meta):
        sa = SuffixArray()
        for p in SuffixArray.__props__:
            setattr(sa, SuffixArray._PROP_ATTR.get(p, p), meta.get(p))
        n = meta['length']
        sa.input = [None] * n
        sa.seqmap = [None] * n
        sa.data = [None] * n
        sa.xovers = [None] * n
        return sa

    @staticmethod
    def from_json(json_data):
        records = json.loads(json_data) if isinstance(json_data, str) else json_data
        records = list(records)
        meta = records.pop(0)
        sa = SuffixArray.init_from_meta(meta)
        for i, rec in enumerate(records):
            sa.input[i] = rec['input']
            sa.data[i] = rec['data']
            sa.xovers[i] = rec['xover']
            sa.seqmap[i] = rec['seqmap']
        return sa

    @staticmethod
    def from_raw_string(s):
        return SuffixArray.from_raw_lines(s.split(EOL))

    @staticmethod
    def from_records(meta, records):
        sa = SuffixArray.init_from_meta(meta)
        if len(records) != sa.length:
            raise Exception('Invalid records')
        for i, rec in enumerate(records):
            inp, data, xover, seqmap = rec
            sa.input[i] = inp
            sa.data[i] = data
            sa.xovers[i] = xover
            sa.seqmap[i] = seqmap
        return sa

    @staticmethod
    def from_raw_lines(lines):
        if not lines:
            raise Exception('No lines to process')
        lines = list(lines)
        header = json.loads(lines.pop(0))
        sa = SuffixArray.init_from_meta(header)
        for i, line in enumerate(lines):
            if len(line) > 0:
                parts = [int(e) for e in line.split(',')]
                sa.input[i], sa.data[i], sa.xovers[i], sa.seqmap[i] = parts
        return sa

    def to_raw_string(self):
        header = self.header_record()
        data = [','.join(str(x) for x in r) for r in self.data_records()]
        return header + EOL + EOL.join(data)

    def data_records(self):
        return [[self.input[i], d, self.xovers[i], self.seqmap[i]]
                for i, d in enumerate(self.data)]

    def header_record(self):
        header = {}
        for p in SuffixArray.__props__:
            header[p] = getattr(self, SuffixArray._PROP_ATTR.get(p, p))
        return json.dumps(header)

    def to_json(self):
        meta = {}
        records = [None] * self.length
        for e in SuffixArray.__props__:
            meta[e] = getattr(self, SuffixArray._PROP_ATTR.get(e, e))
        for i in range(self.length):
            records[i] = {
                'input': self.input[i],
                'data': self.data[i],
                'xover': self.xovers[i],
                'seqmap': self.seqmap[i],
            }
        records.insert(0, meta)
        return records

    def find(self, query=None, opts=None):
        if not query or len(query) == 0:
            query = [self.start_token]
        query = self._encode(query)
        start = self.binsearch(query, True, opts)
        end = self.binsearch(query, False, opts)
        if start is None or end is None:
            return [0, 0]
        return [start, end + 1]

    @staticmethod
    def normalise_dist(mapping, temp=0):
        if len(mapping) == 0:
            return {}
        tdist = {}
        if temp == 0:
            total = sum(mapping.values())
            for tok, v in mapping.items():
                if v < 0:
                    raise Exception('Negative count')
                tdist[tok] = v / total
        else:
            temp = max(temp, 0.01)
            total = 0
            for token, count in mapping.items():
                if count < 0:
                    raise Exception('Negative count')
                pr = math.exp(count / temp)
                tdist[token] = pr
                total += pr
            for tok in list(tdist):
                tdist[tok] /= total
        return tdist

    def tokens_for(self, index, length=None):
        if index is None or index < 0 or index > len(self.data):
            raise Exception('Index out of range: ' + str(index))
        if length is None:
            toks = self.input[self.data[index]:]
        else:
            toks = self.input[self.data[index]:self.data[index] + length]
        return self._decode(toks)

    def tokens_for_range(self, min_idx, max_idx=None):
        if min_idx < 0 or min_idx >= len(self.data):
            raise Exception('Index out of range')
        if max_idx is None:
            max_idx = len(self.data) - 1
        lines = []
        for i in range(min_idx, max_idx):
            lines.append(self._decode(self.input[self.data[i]:]))
        return lines

    def prefix_indexes(self, query):
        low, high = 0, len(self.data) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.is_sub_array(mid, query):
                return mid
            if self.lt(mid, query):
                low = mid + 1
            else:
                high = mid - 1
        return -1

    def has_prefix(self, query):
        query = self._encode(query)
        if not query or not len(query):
            return False
        low, high = 0, len(self.data) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.is_sub_array(mid, query):
                return True
            if self.lt(mid, query):
                low = mid + 1
            else:
                high = mid - 1
        return False

    def has_suffix(self, query):
        query = self._encode(query)
        low, high = 0, len(self.data) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.array_equals(mid, query):
                return True
            if self.lt(mid, query):
                low = mid + 1
            else:
                high = mid - 1
        return False

    def pdist(self, query=None, opts=None):
        if query is None:
            query = []
        if not len(query) or (len(query) == 1 and query[0] == self.start_token):
            return _normalize(self.start_index_dist())
        min_idx, max_idx = self.find(query, opts)
        prob_dist = self.dist_from_indexes(min_idx, max_idx, len(query))
        if not prob_dist:
            return None
        logits = list(prob_dist.values())
        tokens = list(prob_dist.keys())
        temp = (opts or {}).get('temp')
        ndist = _softmax(logits, temp if temp is not None else 1)
        return {t: ndist[i] for i, t in enumerate(tokens)}

    def dist_from_indexes(self, min_idx, max_idx, query_length):
        if max_idx > min_idx:
            probs = {}
            for i in range(min_idx, max_idx):
                idx = self.data[i] + query_length
                if idx >= len(self.input):
                    continue
                nxt = self._encode(self.input[idx])
                if nxt is not None:
                    probs[nxt] = probs.get(nxt, 0) + 1
            return probs
        return None

    def to_string(self, opts=None):
        opts = opts or {}
        s = EOL + '[' + EOL
        xovers = opts.get('xovers', False)
        tokens_per = opts.get('maxLength', 20)
        if tokens_per < 1:
            tokens_per = 2 ** 63
        for i, idx in enumerate(self.data):
            tokens = self._decode(self.input[idx:idx + tokens_per])
            truncated = len(self.input) - idx > tokens_per
            if truncated:
                tokens.append('...')
            m = '  ' + str(i) + ': [' + ','.join(tokens) + '],'
            if xovers and self.xovers[i] > 1:
                query = tokens[:self.xovers[i]]
                choices = self.pdist(query, opts)
                if choices and len(choices) > 1:
                    m += (' (' + str(self.xovers[i]) + ') q={' +
                          ','.join(query) + '} idx=' + str(i) +
                          ' len=' + str(self.xovers[i]) +
                          ' numOpts=' + str(len(choices)) +
                          ' next=' + json.dumps(choices).replace('"', '') + ')')
            s += m + EOL
        return s + ']' + EOL

    def is_unique(self, sequence):
        if not sequence or not len(sequence) or not isinstance(sequence[0], str):
            raise Exception('Invalid sequence(' + str(type(sequence)) + '): ' +
                            json.dumps(sequence))
        return not self.has_prefix(sequence)

    def is_unique_at(self, start_idx, end_idx):
        sequence = self.input[start_idx:end_idx]
        return not self.has_prefix(sequence)

    def rand_seq_start(self):
        indexes = self.start_indexes()
        start = indexes[int(SuffixArray.random() * len(indexes))]
        return self._decode(start)

    def build(self, s):
        if not SuffixArray.SILENT:
            print('Received ' + str(len(s)) + ' tokens')
        length = len(s)
        data = list(range(length))
        ranks = list(s)
        tmp = [0] * length
        starts = [0] * length
        xovers = [0] * length

        start_index = self.encoder[self.start_token] if self.compressed else self.start_token

        for i in range(length):
            data[i] = i
            tmp[i] = 0
            ranks[i] = s[i]
            starts[i] = 1 if s[i] == start_index else 0

        import functools

        state = {'gap': 1}

        def cmp(x, y):
            gap = state['gap']
            if ranks[x] != ranks[y]:
                return _rawcmp(ranks[x], ranks[y])
            x += gap
            y += gap
            if x < length and y < length:
                return _rawcmp(ranks[x], ranks[y])
            return _rawcmp(y, x)

        gap = 1
        while tmp[length - 1] < length - 1:
            state['gap'] = gap
            data.sort(key=functools.cmp_to_key(cmp))
            for i in range(1, length):
                tmp[i] = tmp[i - 1] + (1 if cmp(data[i - 1], data[i]) == -1 else 0)
            final_pass = tmp[length - 1] >= length - 1
            for i in range(length):
                ranks[data[i]] = tmp[i]
                if final_pass:
                    a_start = data[i]
                    a_end = data[i] + self.xover_window
                    b_start = data[i + 1] if i + 1 < length else 0
                    b_end = b_start + self.xover_window
                    xovers[i] = SuffixArray.array_compare_slices(s, a_start, a_end, b_start, b_end)
            gap <<= 1
        xovers[length - 1] = -1

        self.input = s
        self.data = data
        self.xovers = xovers
        self.seqmap = starts
        self.length = length

    def create_dist(self, arr, normalise=False):
        dist = {}
        for x in arr:
            dist[x] = dist.get(x, 0) + 1
        return SuffixArray.normalise_dist(dist) if normalise else dist

    def start_index_dist(self):
        if self._start_index_dist is None:
            indexes = self._decode(self.start_indexes())
            self._start_index_dist = self.create_dist(indexes, True)
        return self._start_index_dist

    def start_indexes(self):
        if self._start_indexes is None:
            indexes = [i for i, e in enumerate(self.seqmap) if e == 1]
            self._start_indexes = [self.input[i + 1] for i in indexes]
        return self._start_indexes

    def binsearch(self, query, is_first, opts=None):
        data = self.data
        low, high = 0, len(data) - 1
        result = -1
        while low <= high:
            mid = (low + high) // 2
            if self.is_sub_array(mid, query):
                result = mid
                if is_first:
                    high = mid - 1
                else:
                    low = mid + 1
            elif self.lt(mid, query):
                low = mid + 1
            else:
                high = mid - 1
        return None if result == -1 else result

    def lt(self, idx, query):
        position = self.data[idx]
        for i in range(len(query)):
            if position + i >= len(self.input):
                return True
            c = self.input[position + i]
            if query[i] != c:
                return c < query[i]
        return False

    def is_sub_array(self, index, query):
        position = self.data[index]
        for i in range(len(query)):
            j = position + i
            c = self.input[j] if 0 <= j < len(self.input) else _UNSET
            if query[i] != c:
                return False
        return True

    def array_equals(self, index, query):
        tokens = self.input[self.data[index]:]
        if len(tokens) != len(query):
            return False
        for i in range(len(tokens)):
            if tokens[i] != query[i]:
                return False
        return True

    @staticmethod
    def array_compare_slices(arr, a_start, a_end, b_start, b_end):
        len_a = min(len(arr), a_end - a_start)
        len_b = min(len(arr), b_end - b_start)
        length = min(len_a, len_b)
        if len_a != len_b:
            return length
        # JS reads arr[i] as undefined when out of range; mirror that so two
        # out-of-range reads compare equal.
        _OOB = object()
        def get(i):
            return arr[i] if 0 <= i < len(arr) else _OOB
        for i in range(length):
            if get(a_start + i) != get(b_start + i):
                return i
        return -1

    @staticmethod
    def array_compare(a, b):
        if not a or not b:
            return -1
        length = min(len(a), len(b))
        if len(a) != len(b):
            return length
        for i in range(length):
            if a[i] != b[i]:
                return i
        return -1

    def _encode(self, arg):
        if not self.compressed:
            return arg
        if isinstance(arg, list):
            # JS maps unknown tokens to `undefined` (encoder[t] -> undefined);
            # mirror that so find/pdist/has_prefix return empty for unknown tokens.
            return [self.encoder.get(t, _UNSET) for t in arg]
        return self.decoder[arg]

    def _decode(self, arg):
        if not self.compressed:
            return arg
        if isinstance(arg, list):
            return [self.decoder[t] for t in arg]
        return self.decoder[arg]
