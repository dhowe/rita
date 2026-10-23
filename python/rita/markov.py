"""
rita/markov.py — Markov chain text generation
Python port of ritajs/src/markov.js
"""

import re
import json

_MULTI_SP_RE = re.compile(r' +')


# ── Default parent object ────────────────────────────────────────────────────

class _Parent:
    """Provides rita functions (tokenize, untokenize, sentences, random, randomizer) to RiMarkov."""
    _tokenizer = None
    _randgen = None
    SILENT = False

    def _get_tokenizer(self):
        if not self._tokenizer:
            from rita.tokenizer import Tokenizer
            self._tokenizer = Tokenizer()
        return self._tokenizer

    def _get_randgen(self):
        if not self._randgen:
            from rita.randgen import RandGen
            self._randgen = RandGen()
        return self._randgen

    def tokenize(self, text):
        return self._get_tokenizer().tokenize(text)

    def untokenize(self, arr):
        return self._get_tokenizer().untokenize(arr)

    def sentences(self, text):
        return self._get_tokenizer().sentences(text)

    def random(self, arr=None):
        rg = self._get_randgen()
        return rg.random() if arr is None else rg.random(arr)

    @property
    def randomizer(self):
        return self._get_randgen()


_default_parent = _Parent()


# ── Node ─────────────────────────────────────────────────────────────────────

class Node:

    def __init__(self, parent, word, count=0):
        self.children = {}
        self.parent = parent
        self.token = word
        self.count = count
        self._num_children = -1   # cache; -1 = invalid
        self.marked = False
        self.hidden = False

    def child(self, word):
        lookup = word.token if hasattr(word, 'token') else word
        return self.children.get(lookup)

    def pselect(self, filter_fn=None):
        rand = RiMarkov.parent.randomizer
        children = self.child_nodes(filter_fn=filter_fn)
        if not children:
            raise RuntimeError(
                f'No eligible child for "{self.token}" '
                f'children=[{", ".join(n.token for n in self.child_nodes())}]'
            )
        weights = [n.count for n in children]
        pdist = rand.ndist(weights)
        idx = rand.pselect(pdist)
        return children[idx]

    def is_leaf(self, ignore_hidden=False):
        return self.child_count(ignore_hidden) < 1

    def is_root(self):
        return self.parent is None

    def child_nodes(self, sort=False, filter_fn=None):
        kids = list(self.children.values())
        if filter_fn:
            kids = [k for k in kids if filter_fn(k)]
        if sort:
            kids.sort(key=lambda n: (-n.count, _DescKey(n.token)))
        return kids

    def child_count(self, ignore_hidden=False):
        if self._num_children == -1:
            if ignore_hidden:
                kids = self.child_nodes(filter_fn=lambda t: not t.hidden)
            else:
                kids = self.child_nodes()
            self._num_children = sum(c.count for c in kids)
        return self._num_children

    def node_prob(self, exclude_meta=False):
        if not self.parent:
            raise RuntimeError('no parent')
        return self.count / self.parent.child_count(exclude_meta)

    def add_child(self, word, count=None):
        self._num_children = -1  # invalidate cache
        lookup = word.token if hasattr(word, 'token') else word
        node = self.children.get(lookup)
        if not node:
            node = Node(self, lookup)
            self.children[lookup] = node
        node.count += count if count is not None else 1
        return node

    def __str__(self):
        if not self.parent:
            return 'Root'
        return f"'{self.token}' [{self.count},p={self.node_prob():.3f}]"

    def as_tree(self, sort=False, show_hidden=False):
        s = self.token + ' '
        if self.parent:
            s += f'({self.count})->'
        s += '{'
        if self.child_count(True):
            return _stringulate(self, s, 1, sort, not show_hidden)
        return s + '}'


# ── RiMarkov ─────────────────────────────────────────────────────────────────

class RiMarkov:

    parent = _default_parent

    def __init__(self, n=None, options=None):
        if options is None:
            options = {}

        self.n = n
        self.root = Node(None, 'ROOT')
        self.trace = options.get('trace', False)
        self.mlm = options.get('maxLengthMatch')
        self.max_attempts = options.get('maxAttempts', 999)
        self.tokenize = options.get('tokenize') or RiMarkov.parent.tokenize
        self.untokenize = options.get('untokenize') or RiMarkov.parent.untokenize
        self.disable_input_checks = bool(options.get('disableInputChecks', False))
        self.sentence_starts = []   # allows dups for probability
        self.sentence_ends = set()  # no dups

        if n is not None and n < 2:
            raise ValueError('minimum N is 2')
        if self.mlm is not None and n is not None and self.mlm < n:
            raise ValueError('maxLengthMatch must be >= N')

        self.input = None
        if not self.disable_input_checks or self.mlm:
            self.input = []

        if 'text' in options:
            self.add_text(options['text'])

    # ── public API ────────────────────────────────────────────────────────────

    def add_text(self, text, multiplier=1):
        if not isinstance(text, (str, list)):
            raise TypeError(f'text must be str or list, got {type(text).__name__}')

        sents = text if isinstance(text, list) else RiMarkov.parent.sentences(text)

        all_words = []
        for _k in range(multiplier):
            for sent in sents:
                if not sent or not sent.strip():
                    continue
                words = self.tokenize(sent)
                words = [w for w in words if w]   # strip empty tokens
                if words:
                    self.sentence_starts.append(words[0])
                    self.sentence_ends.add(words[-1])
                    all_words.extend(words)
            self.treeify(all_words)

        if self.input is not None:
            self.input.extend(all_words)

        return self

    def generate(self, count=None, options=None):
        if options is None:
            options = {}

        returns_array = False
        if isinstance(count, int):
            if count == 1:
                raise ValueError("For one result, use generate() with no 'count' argument")
            returns_array = True
        elif isinstance(count, dict):
            options = count
            count = 1
        elif count is None:
            count = 1

        num = count
        min_length = options.get('minLength', 5)
        max_length = options.get('maxLength', 35)
        temp = options.get('temperature')

        if temp is not None and temp <= 0:
            raise ValueError('Temperature option must be greater than 0')

        tokens = []
        min_idx = [0]
        sentence_idxs = []
        marked_nodes = []
        tries = [0]

        # ── closures ─────────────────────────────────────────────────────────

        def token_hash():
            return ''.join(n.token for n in tokens)

        def unmark_nodes():
            for n in marked_nodes:
                n.marked = False

        def result_count():
            return sum(1 for t in tokens if self._is_end(t))

        def mark_node(node):
            if node:
                node.marked = token_hash()
                marked_nodes.append(node)

        def not_marked(cn):
            return cn.marked != token_hash()

        def sentence_idx():
            return sentence_idxs[-1] if sentence_idxs else 0

        def validate_sentence(nxt):
            mark_node(nxt)
            sidx = sentence_idx()

            if self.trace:
                others = nxt.parent.child_nodes(filter_fn=lambda t: t is not nxt)
                print(1 + (len(tokens) - sidx), nxt.token,
                      '[' + ','.join(t.token for t in others) + ']')

            sentence = [t.token for t in tokens[sidx:]]
            sentence.append(nxt.token)

            if len(sentence) < min_length:
                fail('too-short (pop: ' + nxt.token + ')')
                return False

            if (not self.disable_input_checks and self.input
                    and _is_sub_array(sentence, self.input)):
                fail('in-input (pop: ' + nxt.token + ')')
                return False

            if (not options.get('allowDuplicates')
                    and _is_sub_array(sentence, [t.token for t in tokens[:sidx]])):
                fail('duplicate (pop: ' + nxt.token + ')')
                return False

            tokens.append(nxt)
            sentence_idxs.append(len(tokens))

            if self.trace:
                flat = self.untokenize(sentence)
                print(f'OK ({result_count()}/{num}) "{flat}" sidxs={sentence_idxs}')

            return True

        def fail(msg, sentence_arg=None, force_backtrack=False):
            tries[0] += 1
            sidx = sentence_idx()
            sentence_str = sentence_arg or self._flatten(tokens[sidx:])

            if tries[0] >= self.max_attempts:
                _throw_error(tries[0], result_count())

            parent = self._path_to(tokens)
            ok_kids = parent.child_nodes(filter_fn=not_marked) if parent else []
            num_children = len(ok_kids)

            if self.trace:
                all_kids = parent.child_nodes() if parent else []
                extra = (' forceBacktrack*' if force_backtrack
                         else f' parent="{parent.token}" goodKids=[{",".join(n.token for n in ok_kids)}]'
                              f' allKids=[{",".join(n.token for n in all_kids)}]')
                print(f'Fail: {msg}\n  -> "{sentence_str}" {tries[0]} tries, '
                      f'{result_count()} successes, numChildren={num_children}{extra}')

            if force_backtrack or num_children == 0:
                backtrack()

        def backtrack():
            for _ in range(99):
                if not tokens:
                    break
                last = tokens.pop()
                mark_node(last)

                if self._is_end(last) and sentence_idxs:
                    sentence_idxs.pop()

                sidx = sentence_idx()
                backtrack_until = max(sidx, min_idx[0])

                if self.trace:
                    print(f'backtrack#{len(tokens)} pop "{last.token}" '
                          f'{len(tokens) - sidx}/{backtrack_until} {self._flatten(tokens)}')

                parent = self._path_to(tokens)
                tc = parent.child_nodes(filter_fn=not_marked) if parent else []

                if len(tokens) <= backtrack_until:
                    if min_idx[0] > 0:   # have seed
                        if len(tokens) <= min_idx[0]:   # back at seed
                            if not tc:
                                raise RuntimeError('back at barren-seed1: case 0')
                            if self.trace:
                                print('case 1')
                            return True
                        else:   # back at sentence-start with seed
                            if not tc:
                                if self.trace:
                                    print('case 2: back at SENT-START')
                                if sentence_idxs:
                                    sentence_idxs.pop()
                            else:
                                if self.trace:
                                    print('case 3')
                    else:
                        if self.trace:
                            print(f'case 4: back at start or 0: {len(tokens)} {sentence_idxs}')
                        if not tokens:
                            sentence_idxs.clear()
                            return select_start()
                    return True

                if tc:
                    if self.trace:
                        sidx = sentence_idx()
                        print(f'{len(tokens) - sidx} {self._flatten(tokens)}\n'
                              f'  ok=[{",".join(n.token for n in tc)}]')
                    return parent

            raise RuntimeError('Invalid state in backtrack() ['
                               + ','.join(t.token for t in tokens) + ']')

        def select_start():
            seed = options.get('seed')
            if seed is not None and len(seed):
                if isinstance(seed, str):
                    seed = self.tokenize(seed)
                node = self._path_to(seed, self.root)
                if not node:
                    raise RuntimeError(f'No valid path for seed: {seed}')
                while not node.is_root():
                    tokens.insert(0, node)
                    node = node.parent
                min_idx[0] = len(tokens)
            elif not tokens or self._is_end(tokens[-1]):
                usable_starts = [ss for ss in self.sentence_starts
                                 if self.root.child(ss) and not_marked(self.root.child(ss))]
                if not usable_starts:
                    raise RuntimeError('No valid sentence-starts remaining')
                start = RiMarkov.parent.random(usable_starts)
                start_tok = self.root.child(start)
                mark_node(start_tok)
                tokens.append(start_tok)
            else:
                raise RuntimeError('Invalid call to selectStart: ' + self._flatten(tokens))

        # ── main generate loop ────────────────────────────────────────────────

        select_start()

        while result_count() < num:
            sidx = sentence_idx()
            if len(tokens) - sidx >= max_length:
                fail('too-long', None, True)
                continue

            parent = self._path_to(tokens)
            nxt = self._select_next(parent, temp, tokens, not_marked)

            if not nxt:
                fail(f'mlm-fail({self.mlm})', self._flatten(tokens), True)
                continue

            if self._is_end(nxt):
                validate_sentence(nxt)
                continue

            tokens.append(nxt)

            if self.trace:
                sidx = sentence_idx()
                parent2 = self._path_to(tokens[:-1])
                ok = parent2.child_nodes(filter_fn=not_marked) if parent2 else []
                print(len(tokens) - sidx, nxt.token,
                      '[' + ','.join(t.token for t in ok if t is not nxt) + ']')

        unmark_nodes()

        result_str = self.untokenize([t.token for t in tokens]).strip()
        return self._split_ends(result_str) if returns_array else result_str

    def to_json(self):
        data = {
            'n': self.n,
            'trace': self.trace,
            'mlm': self.mlm,
            'max_attempts': self.max_attempts,
            'disable_input_checks': self.disable_input_checks,
            'sentence_starts': self.sentence_starts,
            'sentence_ends': list(self.sentence_ends),
            'input': self.input,
            'root': _node_to_dict(self.root),
        }
        return json.dumps(data)

    toJSON = to_json

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        rm = cls.__new__(cls)
        rm.n = data['n']
        rm.trace = data.get('trace', False)
        rm.mlm = data.get('mlm')
        rm.max_attempts = data.get('max_attempts', 999)
        rm.disable_input_checks = data.get('disable_input_checks', False)
        rm.sentence_starts = data.get('sentence_starts', [])
        rm.sentence_ends = set(data.get('sentence_ends', []))
        rm.input = data.get('input')
        rm.tokenize = RiMarkov.parent.tokenize
        rm.untokenize = RiMarkov.parent.untokenize
        rm.root = Node(None, 'ROOT')
        _populate(rm.root, data.get('root', {}))
        return rm

    fromJSON = from_json

    def completions(self, pre, post=None):
        result = []
        if post is not None:
            if len(pre) + len(post) > self.n:
                raise ValueError(
                    f'Sum of pre.length && post.length must be <= N, was {len(pre) + len(post)}'
                )
            tn = self._path_to(pre)
            if not tn:
                if not RiMarkov.parent.SILENT:
                    print(f'Warning: Unable to find nodes in pre: {pre}')
                return None
            for nxt in tn.child_nodes():
                atest = list(pre) + [nxt.token] + list(post)
                if self._path_to(atest):
                    result.append(nxt.token)
        else:
            pr = self.probabilities(pre)
            result = sorted(pr.keys(), key=lambda k: -pr[k])
        return result

    def probabilities(self, path, temperature=None):
        if isinstance(path, str):
            path = self.tokenize(path)
        probs = {}
        parent = self._path_to(path)
        if parent:
            children = parent.child_nodes()
            weights = [n.count for n in children]
            pdist = RiMarkov.parent.randomizer.ndist(weights, temperature)
            for i, c in enumerate(children):
                probs[c.token] = pdist[i]
        return probs

    def probability(self, data):
        p = 0
        if data and len(data):
            if isinstance(data, str):
                tn = self.root.child(data)
            else:
                tn = self._path_to(list(data))
            if tn:
                p = tn.node_prob(True)
        return p

    def to_string(self, root=None, sort=False):
        root = root or self.root
        return root.as_tree(sort).replace('{}', '')

    toString = to_string

    def size(self):
        return self.root.child_count(True)

    # ── internals ─────────────────────────────────────────────────────────────

    def _select_next(self, parent, temp, tokens, filter_fn):
        if not parent:
            raise RuntimeError('no parent: ' + self._flatten(tokens))

        children = parent.child_nodes(filter_fn=filter_fn)
        if not children:
            if self.trace:
                all_c = parent.child_nodes()
                print(f'No children to select, parent={parent.token} '
                      f'children=ok[], all=[{",".join(n.token for n in all_c)}]')
            return None

        # basic case: prob-select from children
        if not self.mlm or self.mlm > len(tokens):
            return parent.pselect(filter_fn=filter_fn)

        def validate_mlms(word_node, toks):
            check = [n.token for n in toks[-self.mlm:]]
            check.append(word_node.token)
            return not _is_sub_array(check, self.input)

        rand = RiMarkov.parent.randomizer
        weights = [n.count for n in children]
        pdist = rand.ndist(weights, temp)
        tries_max = len(children) * 2
        selector = rand.random()
        tried = []
        p_total = 0

        for i in range(tries_max):
            idx = i % len(children)
            p_total += pdist[idx]
            nxt = children[idx]
            if selector < p_total:
                if nxt.token not in tried:
                    tried.append(nxt.token)
                    return nxt if validate_mlms(nxt, tokens) else None

        return None

    def _is_end(self, node):
        if node:
            check = node.token if hasattr(node, 'token') else node
            return check in self.sentence_ends
        return False

    def _path_to(self, path, root=None):
        root = root or self.root
        if isinstance(path, str):
            path = [path]
        if not path or self.n is None or self.n < 2:
            return root
        tokens_arr = [p.token if hasattr(p, 'token') else p for p in path]
        idx = max(0, len(tokens_arr) - (self.n - 1))
        node = root.child(tokens_arr[idx])
        for i in range(idx + 1, len(tokens_arr)):
            if node:
                node = node.child(tokens_arr[i])
        return node   # can be None

    def treeify(self, tokens):
        root = self.root
        for i in range(len(tokens)):
            node = root
            words = list(tokens[i:i + self.n])
            wrap = 0
            for j in range(self.n):
                hidden = False
                if j >= len(words):
                    words.append(tokens[wrap])
                    wrap += 1
                    hidden = True
                node = node.add_child(words[j])
                if hidden:
                    node.hidden = True

    def _split_ends(self, s):
        se = list(self.sentence_ends)
        escaped = [re.escape(w) for w in se]
        pat = '(' + '|'.join(escaped) + ')'
        parts = re.split(pat, s)
        arr = []
        for i, p in enumerate(parts):
            if not p:
                continue
            if i % 2 == 0:
                arr.append(p)
            else:
                if arr:
                    arr[-1] += p
                else:
                    arr.append(p)
        return [a.strip() for a in arr]

    def _flatten(self, nodes):
        if not nodes:
            return ''
        if hasattr(nodes, 'token'):
            return nodes.token
        arr = [n.token if n else '[undef]' for n in nodes]
        sent = self.untokenize(arr)
        return _MULTI_SP_RE.sub(' ', sent)


# ── module-level helpers ──────────────────────────────────────────────────────

class _DescKey:
    """Sort key for locale-aware case-insensitive descending string order.
    Produces descending casefold order, with uppercase before lowercase tiebreaking.
    This matches the behaviour of JS localeCompare in Node.js for typical ASCII strings.
    """
    __slots__ = ('cf', 'orig')

    def __init__(self, s):
        self.cf = s.casefold()
        self.orig = s

    def __eq__(self, o):
        return self.cf == o.cf and self.orig == o.orig

    def __lt__(self, o):
        if self.cf != o.cf:
            return self.cf > o.cf   # reversed: higher casefold → smaller key (comes first)
        return self.orig < o.orig   # same casefold: uppercase (lower ord) before lowercase

    def __le__(self, o): return self == o or self < o
    def __gt__(self, o): return o < self
    def __ge__(self, o): return self == o or self > o


def _node_to_dict(node):
    return {
        'token': node.token,
        'count': node.count,
        'hidden': node.hidden,
        'children': {k: _node_to_dict(v) for k, v in node.children.items()},
    }


def _populate(obj_node, json_node):
    if not json_node:
        return
    for child_data in json_node.get('children', {}).values():
        new_node = obj_node.add_child(child_data['token'], child_data['count'])
        new_node.hidden = child_data.get('hidden', False)
        _populate(new_node, child_data)


def _throw_error(tries, oks):
    msg = f'Failed after {tries} tries'
    if oks:
        msg += f' and {oks} successes'
    msg += ', you may need to adjust options or add more text'
    raise RuntimeError(msg)


def _is_sub_array(find, arr):
    if not arr:
        return False
    find_len = len(find)
    arr_len = len(arr)
    for i in range(find_len - 1, arr_len):
        match = True
        for j in range(find_len):
            if find[find_len - j - 1] != arr[i - j]:
                match = False
                break
        if match:
            return True
    return False


def _stringulate(mn, s, depth, sort, ignore_hidden=False):
    indent = '\n' + '  ' * depth
    end_indent = '\n' + '  ' * (depth - 1)
    kids = mn.child_nodes(sort=True, filter_fn=lambda t: not t.hidden)
    if not kids:
        return s
    for node in kids:
        if node and node.token:
            s += indent + "'" + _encode(node.token) + "'"
            if not node.is_root():
                s += f' [{node.count},p={node.node_prob():.3f}]'
            if not node.is_leaf(ignore_hidden):
                s += '  {'
            if mn.child_count(ignore_hidden):
                s = _stringulate(node, s, depth + 1, sort)
            else:
                s += '}'
    return s + end_indent + '}'


def _encode(tok):
    tok = tok.replace('\r\n', '\\r\\n')
    tok = tok.replace('\n', '\\n')
    tok = tok.replace('\r', '\\r')
    tok = tok.replace('\t', '\\t')
    return tok
