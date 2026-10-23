"""
BackoffModel — Python port of js/src/backoff.js.

Extends SuffixGram with n-gram generation via per-position backtracking,
streaming generation, and generation-path enumeration.

Method names follow Python conventions (snake_case) with camelCase aliases for
JS API parity; option dict keys remain camelCase (as in the JS source/tests).
"""

import json
import math

from rita.model import SuffixGram
from rita.suffixes import SuffixArray
from rita.util import JsDict


class _JsGenerator:
    """Wraps a Python generator to mimic the JS iterator protocol.

    JS `gen.next()` returns `{done, value}` and the generator body runs lazily
    (so a throw inside the generator only surfaces on the first `next()`).
    Supports `for x in gen` (yields values) and `gen.next()` (returns a dict).
    """

    def __init__(self, gen):
        self._gen = gen

    def __iter__(self):
        return self._gen

    def __next__(self):
        return next(self._gen)

    def next(self):
        try:
            return JsDict({'done': False, 'value': next(self._gen)})
        except StopIteration:
            return JsDict({'done': True, 'value': None})


class BackoffModel(SuffixGram):

    generationDefaults = {
        'debug': False, 'minLength': 5, 'maxLength': 999,
        'maxAttempts': 999, 'maxBacktracks': 9999, 'forceOriginal': False,
        'maxLengthMatch': math.inf, 'temp': 1, 'topK': 20, 'depth': 50,
        'allowSpecial': False, 'sortByProb': False,
    }

    generationAliases = {
        'dbug': 'debug', 'minTokens': 'minLength', 'maxTokens': 'maxLength',
        'temperature': 'temp', 'mlm': 'maxLengthMatch',
    }

    generationIgnorable = ['numSentences', 'generateUntil', 'allowDuplicates',
                           'prompt', 'n', 'trace']

    def __init__(self, input=None, opts=None):
        super().__init__(input, opts)

    @staticmethod
    def from_json(json_data):
        obj = json.loads(json_data) if isinstance(json_data, str) else json_data
        model = BackoffModel()
        for k, v in obj.items():
            setattr(model, k, v)
        # restore suffixes as a proper SuffixArray instance
        if getattr(model, 'suffixes', None) and not isinstance(model.suffixes, SuffixArray):
            model.suffixes = SuffixArray.from_json(model.suffixes)
        return model

    def generate_sentences(self, n, prompt, opts=None):
        return self._backtracking_generate(n, prompt, opts or {})

    def generation_paths(self, n, prompt, options=None):
        options = options or {}
        opts = BackoffModel.resolve_opts(n, options, ['numSentences'])
        tree = self.build_tree(n, prompt, opts, opts['depth'])

        paths = []
        BackoffModel.collect_paths(
            tree, [JsDict({'token': t, 'prob': 1}) for t in prompt], paths)

        if opts.get('sortByProb'):
            def joint(path):
                p = 1
                for nd in path[len(prompt):]:
                    p *= nd['prob']
                return p
            paths.sort(key=joint, reverse=True)

        raw = []
        for tokens in paths:
            p = 1
            for nd in tokens[len(prompt):]:
                p *= nd['prob']
            raw.append(p)
        total = sum(raw)

        result = []
        for i, tokens in enumerate(paths):
            result.append(JsDict({
                'tokens': tokens,
                'prob': (raw[i] / total) if total else 0,
                'inInput': self.suffixes.has_prefix([t['token'] for t in tokens]),
            }))
        return result

    def path_generator(self, n, prompt, options=None):
        # JS generators are lazy and .next() returns {done, value}. Wrap the
        # underlying generator so both `for x in gen` and `gen.next()` work.
        return _JsGenerator(self._path_gen(n, prompt, options))

    def _path_gen(self, n, prompt, options=None):
        options = options or {}
        opts = BackoffModel.resolve_opts(n, options)
        prompt_nodes = [JsDict({'token': t, 'prob': 1}) for t in prompt]

        tree = self.build_tree(n, prompt, opts)
        if len(tree) == 0:
            if opts.get('forceOriginal'):
                raise Exception('forceOriginal: no original completions found for prompt [' +
                                ' '.join(prompt) + ']')
            return

        def walk(nodes, current_path):
            for node in nodes:
                if node['isEnd']:
                    continue
                path = current_path + [JsDict({'token': node['token'], 'prob': node['prob']})]
                kids = node['children']
                if len(kids) == 0 or all(c['isEnd'] for c in kids):
                    prob = 1
                    for nd in path[len(prompt):]:
                        prob *= nd['prob']
                    yield JsDict({'tokens': path, 'prob': prob})
                else:
                    yield from walk(kids, path)

        yield from walk(tree, prompt_nodes)

    def stream_tokens(self, n, prompt, options=None):
        options = options or {}
        opts = BackoffModel.resolve_opts(n, options, ['generateUntil', 'numSentences'])

        minLength = opts['minLength']
        maxLength = opts['maxLength']
        maxLengthMatch = opts['maxLengthMatch']
        temp = opts['temp']
        allowSpecial = opts['allowSpecial']
        debug = opts['debug']

        if opts.get('forceOriginal'):
            raise Exception('`forceOriginal` invalid for stream_tokens')

        generate_until = opts.get('generateUntil', self.endToken)
        if callable(generate_until):
            is_until = generate_until
        else:
            is_until = lambda token, *a: token == generate_until

        def is_special(token):
            return token.startswith('<') and token.endswith('>')

        sa_opts = {'temp': temp, 'n': n}
        context = list(prompt)
        generated = 0
        while generated < maxLength:

            query = context[-(n - 1):] if n - 1 > 0 else context
            if len(context) > n - 1:
                dist = self.suffixes.pdist(context, sa_opts) or self.suffixes.pdist(query, sa_opts)
            else:
                dist = self.suffixes.pdist(query, sa_opts)

            while (not dist or len(dist) == 0) and len(query) > 1:
                query = query[1:]
                dist = self.suffixes.pdist(query, sa_opts)
            if not dist:
                break

            chosen_token = None
            weight_sum = 0
            check_length = math.isfinite(maxLengthMatch)
            total_so_far = len(prompt) + generated

            for token, prob in dist.items():
                if is_special(token):
                    if total_so_far < minLength:
                        continue
                elif check_length:
                    non_special = [t for t in context if not is_special(t)]
                    seq = non_special[-maxLengthMatch:] + [token]
                    hp = self.suffixes.has_prefix(seq)
                    if debug:
                        print('[MLM] token="%s" seq.len=%d mlm=%d seqGtMlm=%s hasPrefix=%s seq=[%s]'
                              % (token, len(seq), maxLengthMatch, len(seq) > maxLengthMatch, hp,
                                 ','.join(seq)))
                    if len(seq) > maxLengthMatch and hp:
                        if debug:
                            print('[FAIL] skipping token "%s" due to maxLengthMatch constraint: sequence [%s] found in training data'
                                  % (token, ', '.join(seq)))
                        continue
                weight_sum += prob
                if SuffixGram.random() * weight_sum < prob:
                    chosen_token = token

            if chosen_token is None:
                break
            token = chosen_token

            if (not is_special(token)) and is_until(token, context[len(prompt):]) and total_so_far + 1 >= minLength:
                yield token
                break

            if is_special(token):
                if is_until(token, context[len(prompt):]) and total_so_far + 1 >= minLength:
                    if allowSpecial:
                        yield token
                    break
                if allowSpecial:
                    yield token
                context.append(token)
                generated += 1
                continue

            yield token
            context.append(token)
            generated += 1

    # ── privates ────────────────────────────────────────────────────────────

    def _backtracking_generate(self, n, prompt, opts=None):
        opts = opts or {}
        resolved = BackoffModel.resolve_opts(n, opts)

        numSentences = opts.get('numSentences', 2)
        maxBacktracks = resolved['maxBacktracks']
        perMax = resolved['maxLength']
        perMin = resolved['minLength']
        mlm = resolved['maxLengthMatch']
        maxAttempts = resolved['maxAttempts']
        temp = resolved['temp']
        endToken = self.endToken
        startToken = self.startToken
        debug = resolved['debug']

        def is_special(token):
            return token.startswith('<') and token.endswith('>')

        sa_opts = {'temp': temp, 'n': n}

        non_empty_prompt = [t for t in (prompt or []) if t and len(t) > 0]
        valid_prompt = [t for t in non_empty_prompt if len(t.strip()) > 0]
        if len(non_empty_prompt) > 0 and len(valid_prompt) == 0:
            raise Exception('prompt contains only whitespace tokens')

        def random_starter():
            if len(valid_prompt) > 0:
                return list(valid_prompt)
            return [SuffixGram.RiTa.randomizer.pselect_obj(self.suffixes.start_index_dist())]

        if len(valid_prompt) > 0:
            dist = self.suffixes.pdist(valid_prompt, {'n': n})
            if not dist or len(dist) == 0:
                raise Exception('generate() failed: prompt [%s] not found in model'
                                % ', '.join(valid_prompt))
            if numSentences == 1:
                start_dist = self.suffixes.start_index_dist()
                if not start_dist.get(valid_prompt[0]):
                    raise Exception("generate() failed: prompt token '%s' is not a sentence start"
                                    % valid_prompt[0])

        def split_into_sentences(context, sentence_starts):
            sentences = []
            bounds = [0] + sentence_starts[1:]
            for i in range(len(bounds) - 1):
                sl = [t for t in context[bounds[i]:bounds[i + 1]]
                      if t != startToken and t != endToken]
                sentences.append(self.untokenize(sl))
            return sentences

        def weighted_select(candidates):
            chosen = candidates[-1][0]
            weight_sum = 0
            for token, prob in candidates:
                weight_sum += prob
                if SuffixGram.random() * weight_sum < prob:
                    chosen = token
            return chosen

        attempts = 0
        while True:
            attempts += 1
            if attempts > maxAttempts:
                break

            context = list(random_starter())
            if debug:
                print('[GEN] attempt %d/%d seed=[%s] n=%d numSentences=%d'
                      % (attempts, maxAttempts, ' '.join(context), n, numSentences))
            floor = len(context)
            choice_points = []
            sentence_starts = [0]

            state = {'ends_seen': 0, 'backtracks': 0}
            gave_up = False

            def backtrack(reason):
                if len(context) <= floor:
                    return False
                popped_idx = len(context) - 1
                popped = context[popped_idx]
                context.pop()
                cp = choice_points[popped_idx] if popped_idx < len(choice_points) else None
                if cp and cp['isSentenceEnd']:
                    state['ends_seen'] -= 1
                    sentence_starts.pop()
                if cp:
                    cp['isSentenceEnd'] = False
                state['backtracks'] += 1
                if debug:
                    print('[BACKTRACK] %d/%d popped="%s" (%s)'
                          % (state['backtracks'], maxBacktracks, popped, reason))
                return True

            while state['ends_seen'] < numSentences:
                if state['backtracks'] > maxBacktracks:
                    gave_up = True
                    break

                pos = len(context)
                cur_start = sentence_starts[-1]
                tokens_in_sentence = pos - cur_start

                query = context[-(n - 1):] if n - 1 > 0 else context
                dist = self.suffixes.pdist(query, sa_opts)
                tried = choice_points[pos]['triedTokens'] if pos < len(choice_points) and choice_points[pos] else set()

                if not dist or len(dist) == 0:
                    if debug:
                        print('[FAIL] no distribution for query [%s] at pos=%d'
                              % (','.join(query), pos))
                    if not backtrack('no distribution'):
                        gave_up = True
                        break
                    continue

                candidates = []
                for token, prob in dist.items():
                    if token in tried:
                        continue
                    if token == endToken:
                        if tokens_in_sentence < perMin:
                            continue
                    elif math.isfinite(mlm) and not is_special(token):
                        non_special = [t for t in context if not is_special(t)]
                        seq = non_special[-mlm:] + [token]
                        if len(seq) > mlm and self.suffixes.has_prefix(seq):
                            if debug:
                                print('[MLM] skipping token="%s" seq=[%s] found in training data'
                                      % (token, ','.join(seq)))
                            continue
                    candidates.append([token, prob])

                if len(candidates) == 0:
                    if not backtrack('all candidates filtered'):
                        gave_up = True
                        break
                    continue

                token = weighted_select(candidates)
                if debug:
                    print('[GEN] pos=%d sentLen=%d chose="%s" of %d candidates'
                          % (pos, tokens_in_sentence, token, len(candidates)))

                tried.add(token)
                if pos < len(choice_points):
                    choice_points[pos] = {'triedTokens': tried, 'isSentenceEnd': False}
                else:
                    while len(choice_points) <= pos:
                        choice_points.append(None)
                    choice_points[pos] = {'triedTokens': tried, 'isSentenceEnd': False}

                if token == endToken:
                    sent_len = tokens_in_sentence
                    if sent_len < perMin or sent_len > perMax:
                        if debug:
                            print('[FAIL] skipping endToken: sentence length %d outside [%d,%d]'
                                  % (sent_len, perMin, perMax))
                        continue
                    context.append(token)
                    choice_points[pos]['isSentenceEnd'] = True
                    state['ends_seen'] += 1
                    sentence_starts.append(len(context))
                    continue

                context.append(token)

            if not gave_up and state['ends_seen'] == numSentences:
                return split_into_sentences(context, sentence_starts)

        raise Exception('backoff failed after %d attempts' % maxAttempts)

    def build(self, opts=None):
        opts = opts or {}
        self.tokenCount = 0
        if self.tokens and len(self.tokens) > 0:
            self.suffixes = SuffixArray(self.tokens, opts)
            self.tokenCount = len(self.tokens)
            self.tokens = None
            self.ready = True
        return self

    def pselect(self, dist):
        if not isinstance(dist, dict):
            raise Exception('object required')
        cutoff = 0
        point = SuffixGram.random()
        keys = list(dist.keys())
        for i in range(len(keys) - 1):
            tok = keys[i]
            cutoff += dist[tok]
            if point < cutoff:
                return tok
        return keys[-1]

    @staticmethod
    def resolve_opts(n, options, ignorable_keys=None):
        ignorable_keys = ignorable_keys or []
        if options is not None and not SuffixGram.is_object(options):
            raise Exception('Options must be an object')
        resolved = JsDict(options or {})

        aliases = BackoffModel.generationAliases
        for key in list(resolved.keys()):
            if key in aliases:
                canonical = aliases[key]
                resolved.setdefault(canonical, resolved[key])
                del resolved[key]
        for o, default in BackoffModel.generationDefaults.items():
            if resolved.get(o) is None:
                resolved[o] = default
        allowed = BackoffModel.generationIgnorable + list(ignorable_keys)
        for key in resolved:
            if key not in BackoffModel.generationDefaults and key not in allowed:
                raise Exception('Invalid option key: ' + str(key))
        if math.isfinite(resolved['maxLengthMatch']) and resolved['maxLengthMatch'] < n:
            raise Exception('maxLengthMatch (%s) must be >= n (%s)'
                            % (resolved['maxLengthMatch'], n))
        if math.isfinite(n) and n > 1:
            resolved['n'] = n
        return resolved

    def build_tree(self, n, prompt=None, opts=None, depth=None, tokens_so_far=0):
        prompt = prompt if prompt is not None else []
        opts = opts if opts is not None else {}
        if depth is None:
            depth = opts.get('depth')
        if depth == 0:
            return []
        topK = opts.get('topK')
        temp = opts.get('temp')
        minLength = opts.get('minLength')
        maxLength = opts.get('maxLength')
        maxLengthMatch = opts.get('maxLengthMatch')
        forceOriginal = opts.get('forceOriginal')
        if not self.ready:
            self.build()
        sa_opts = {'temp': temp, 'n': n}
        query = prompt[-(n - 1):] if n - 1 > 0 else prompt
        dist = self.suffixes.pdist(query, sa_opts)
        if (not dist or len(dist) == 0) and len(query) > 1:
            dist = self.suffixes.pdist(query[1:], sa_opts)
        if not dist:
            return []

        entries = sorted(dist.items(), key=lambda kv: -kv[1])[:topK]
        entry_total = sum(p for _, p in entries)
        entries = [(t, p / entry_total) for t, p in entries]

        result = []
        for token, prob in entries:
            is_end = token == self.endToken or token == self.startToken
            if is_end and tokens_so_far < minLength:
                continue
            if (not is_end) and tokens_so_far >= maxLength:
                continue
            if (not is_end) and math.isfinite(maxLengthMatch):
                seq = prompt[-maxLengthMatch:] + [token]
                if len(seq) > maxLengthMatch and self.suffixes.has_prefix(seq):
                    continue
            if is_end and forceOriginal and self.suffixes.has_prefix(prompt):
                continue

            if is_end or depth <= 1:
                children = []
            else:
                children = self.build_tree(n, prompt + [token], opts, depth - 1, tokens_so_far + 1)

            if (not is_end) and len(children) == 0:
                continue

            result.append(JsDict({'token': token, 'prob': prob, 'isEnd': is_end, 'children': children}))
        return result

    @staticmethod
    def collect_paths(nodes, current_path, accumulator, prompt_length=None):
        if prompt_length is None:
            prompt_length = len(current_path)
        for node in nodes:
            if node['isEnd']:
                continue
            path = current_path + [JsDict({'token': node['token'], 'prob': node['prob']})]
            kids = node['children']
            if len(kids) == 0 or all(c['isEnd'] for c in kids):
                accumulator.append(path)
            else:
                BackoffModel.collect_paths(kids, path, accumulator, prompt_length)

    # ── camelCase aliases (JS API parity) ───────────────────────────────────
    generateSentences = generate_sentences
    generationPaths = generation_paths
    pathGenerator = path_generator
    streamTokens = stream_tokens
    buildTree = build_tree
    collectPaths = collect_paths
    resolveOpts = resolve_opts
    fromJSON = from_json
    toJSON = SuffixGram.to_json
    toString = SuffixGram.to_string
