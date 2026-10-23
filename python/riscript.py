"""
riscript.py — RiScript interpreter in Python (hand-rolled recursive descent)

Grammar (v3, simplified):
  script  : expr* EOF
  expr    : atom+
  atom    : choice | assign | symbol | silent | pgate | entity | text
  choice  : '[' gate? orExpr elseExpr? ']' transform*
  assign  : Symbol '=' expr
  symbol  : Symbol transform*
  silent  : '{' gate? (Symbol ('=' expr)?)  '}'
  orExpr  : wexpr ('|' wexpr)*
  elseExpr: '||' wexpr
  wexpr   : (expr | Weight)*
  pgate   : PendingGate
  entity  : Entity
  gate    : Gate
  transform: Transform
  text    : Raw | '#' | '&' | '.' | '=' | '(' | ')'
"""

import re
import html
import random
import hashlib

# ── Token types ─────────────────────────────────────────────────────────────

TK_GATE        = 'GATE'
TK_ENTITY      = 'ENTITY'
TK_WEIGHT      = 'WEIGHT'
TK_PENDING     = 'PENDING'
TK_ELSE        = 'ELSE'
TK_OC          = 'OC'
TK_CC          = 'CC'
TK_OS          = 'OS'
TK_CS          = 'CS'
TK_OR          = 'OR'
TK_EQ          = 'EQ'
TK_SYMBOL      = 'SYMBOL'
TK_TRANSFORM   = 'TRANSFORM'
TK_RAW         = 'RAW'
TK_EOF         = 'EOF'

# ── Lexer ────────────────────────────────────────────────────────────────────

# Order matters — longer/more-specific patterns first
_TOKEN_PATTERNS = [
    (TK_GATE,      r'@\s*\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}'),
    (TK_ENTITY,    r'&(?:[a-zA-Z][a-zA-Z0-9]*|#[0-9]+|#x[0-9a-fA-F]+);'),
    (TK_WEIGHT,    r'\s*\^-?\d+\^\s*'),
    (TK_PENDING,   r'@@[0-9]{9,11}'),
    (TK_ELSE,      r'\s*\|\|\s*'),
    (TK_OC,        r'\[\s*'),
    (TK_CC,        r'\s*\]'),
    (TK_OS,        r'\{\s*'),
    (TK_CS,        r'\s*\}'),
    (TK_OR,        r'\s*\|\s*'),
    (TK_EQ,        r'\s*=\s*'),
    (TK_SYMBOL,    r'(?:\$|#[A-Za-z_0-9])[A-Za-z_0-9]*(?:\(\))?'),
    (TK_TRANSFORM, r'\.[A-Za-z_][A-Za-z_0-9]*(?:\(\))?'),
    (TK_RAW,       r'[^|$#&{}\[\]^~@.=()\s\\]+|[ \t]+'),
]

_MASTER_RE = re.compile('|'.join(f'(?P<{name}>{pat})' for name, pat in _TOKEN_PATTERNS))

class Token:
    """A single lexical token produced by the tokenizer."""
    __slots__ = ('type', 'value', 'pos')
    def __init__(self, type_, value, pos=0):
        self.type  = type_
        self.value = value
        self.pos   = pos
    def __repr__(self):
        return f'Token({self.type}, {self.value!r})'

_BACKSLASH_ENTITY_MAP = {
    '{': '&lcub;', '}': '&rcub;', '[': '&lsqb;', ']': '&rsqb;',
    '$': '&dollar;', '#': '&num;', '|': '&vert;', '\\': '&bsol;',
    '^': '&#94;', '~': '&#126;', '@': '&commat;', '=': '&equals;'
}

def tokenize(text):
    """Convert a RiScript string into a list of Tokens, handling backslash escapes."""
    tokens = []
    pos = 0
    while pos < len(text):
        # handle backslash escape: \X -> entity for special chars, else RAW(X)
        if text[pos] == '\\' and pos + 1 < len(text):
            next_ch = text[pos + 1]
            entity = _BACKSLASH_ENTITY_MAP.get(next_ch, next_ch)
            tokens.append(Token(TK_RAW, entity, pos))
            pos += 2
            continue
        m = _MASTER_RE.match(text, pos)
        if m:
            typ = m.lastgroup
            tokens.append(Token(typ, m.group(), pos))
            pos = m.end()
        else:
            # catch-all: single char as RAW
            tokens.append(Token(TK_RAW, text[pos], pos))
            pos += 1
    tokens.append(Token(TK_EOF, '', pos))
    return tokens

# ── Parser ───────────────────────────────────────────────────────────────────

class ParseError(Exception):
    """Raised when the parser encounters an unexpected token or structure."""
    pass

class Parser:
    """Recursive-descent parser that converts a Token list into an AST."""
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos    = 0

    def peek(self):
        return self.tokens[self.pos]

    def peek_type(self):
        return self.tokens[self.pos].type

    def consume(self, expected_type=None):
        """Advance and return the current token, optionally asserting its type."""
        tok = self.tokens[self.pos]
        if expected_type and tok.type != expected_type:
            raise ParseError(f'Expected {expected_type} got {tok.type!r} ({tok.value!r})')
        self.pos += 1
        return tok

    def at(self, *types):
        return self.tokens[self.pos].type in types

    # ── parse_script ────────────────────────────────────────────────────────

    def parse_script(self):
        exprs = []
        while not self.at(TK_EOF):
            if self.at(TK_OR, TK_ELSE):
                raise ParseError(f'Unexpected {self.peek_type()!r} at top level')
            exprs.append(self.parse_expr())
        return ('script', exprs)

    def parse_expr(self):
        atoms = []
        while not self.at(TK_EOF, TK_OR, TK_ELSE, TK_CC, TK_CS, TK_WEIGHT):
            prev_pos = self.pos
            atoms.append(self.parse_atom())
            if self.pos == prev_pos:  # safety: didn't advance
                raise ParseError(f'Parser stuck at token {self.peek_type()!r}')
        return ('expr', atoms)

    def parse_atom(self):
        t = self.peek_type()

        # choice
        if t == TK_OC:
            return self.parse_choice()

        # silent block
        if t == TK_OS:
            return self.parse_silent()

        # pending gate
        if t == TK_PENDING:
            tok = self.consume()
            return ('pgate', tok.value)

        # entity
        if t == TK_ENTITY:
            tok = self.consume()
            return ('entity', tok.value)

        # symbol or assign
        if t == TK_SYMBOL:
            return self.parse_symbol_or_assign()

        # text
        return self.parse_text()

    def parse_symbol_or_assign(self):
        sym_tok = self.consume(TK_SYMBOL)
        sym = sym_tok.value
        # peek for assignment (EQ)
        if self.at(TK_EQ):
            self.consume(TK_EQ)
            rhs = self.parse_expr()
            return ('assign', sym, rhs)
        # otherwise symbol with optional transforms
        transforms = self._collect_transforms()
        return ('symbol', sym, transforms)

    def parse_choice(self):
        self.consume(TK_OC)
        gate = None
        if self.at(TK_GATE):
            gate = self.consume(TK_GATE).value
        or_expr  = self.parse_or_expr()
        else_expr = None
        if self.at(TK_ELSE):
            self.consume(TK_ELSE)
            else_expr = self.parse_or_expr()
        self.consume(TK_CC)
        transforms = self._collect_transforms()
        return ('choice', gate, or_expr, else_expr, transforms)

    def parse_or_expr(self):
        branches = [self.parse_wexpr()]
        while self.at(TK_OR):
            self.consume(TK_OR)
            branches.append(self.parse_wexpr())
        return branches

    def parse_wexpr(self):
        items = []
        while not self.at(TK_EOF, TK_OR, TK_ELSE, TK_CC):
            if self.at(TK_WEIGHT):
                items.append(('weight', self.consume(TK_WEIGHT).value))
            else:
                items.append(self.parse_expr())
        return items

    def parse_silent(self):
        self.consume(TK_OS)
        gate = None
        if self.at(TK_GATE):
            gate = self.consume(TK_GATE).value
        node = None
        if self.at(TK_SYMBOL):
            sym_tok = self.consume(TK_SYMBOL)
            sym = sym_tok.value
            if self.at(TK_EQ):
                self.consume(TK_EQ)
                rhs = self.parse_expr()
                node = ('assign', sym, rhs)
            else:
                node = ('symbol', sym, [])
        self.consume(TK_CS)
        return ('silent', gate, node)

    def parse_text(self):
        tok = self.consume()
        if tok.type == TK_EOF:
            raise ParseError('Unexpected EOF in text')
        return ('text', tok.value)

    def _collect_transforms(self):
        txs = []
        while self.at(TK_TRANSFORM):
            txs.append(self.consume(TK_TRANSFORM).value)
        return txs

def parse(text):
    """Tokenize and parse a RiScript string, returning an AST."""
    tokens = tokenize(text)
    p = Parser(tokens)
    return p.parse_script()

# ── Default transforms ───────────────────────────────────────────────────────

def _pluralize(s):
    """Pluralize a word using comprehensive rules (RiTa-compatible)."""
    if not s:
        return s
    s = s.strip()
    word = s.lower()
    
    # Check for irregular plurals first
    # ox -> oxen
    if word == 'ox':
        return 'oxen'
    
    # child -> children
    if word == 'child':
        return 'children'
    
    # mouse -> mice
    if word == 'mouse':
        return 'mice'
    
    # tooth -> teeth
    if word == 'tooth':
        return 'teeth'
    
    # foot -> feet
    if word == 'foot':
        return 'feet'
    
    # goose -> geese
    if word == 'goose':
        return 'geese'
    
    # man -> men
    if word == 'man':
        return 'men'
    
    # woman -> women
    if word == 'woman':
        return 'women'
    
    # person -> people
    if word == 'person':
        return 'people'
    
    # criterion -> criteria
    if word == 'criterion':
        return 'criteria'
    
    # formula -> formulas (also formulae)
    if word == 'formula':
        return 'formulas'
    
    # appendix -> appendixes or appendices
    if word == 'appendix':
        return 'appendixes'
    
    # matrix -> matrices
    if word == 'matrix':
        return 'matrices'
    
    # index -> indices
    if word == 'index':
        return 'indices'
    
    # syllabus -> syllabi
    if word == 'syllabus':
        return 'syllabi'
    
    # cactus -> cacti
    if word == 'cactus':
        return 'cacti'
    
    # fungus -> fungi
    if word == 'fungus':
        return 'fungi'
    
    # nucleus -> nuclei
    if word == 'nucleus':
        return 'nuclei'
    
    # stimulus -> stimuli
    if word == 'stimulus':
        return 'stimuli'
    
    # analysis -> analyses
    if word == 'analysis':
        return 'analyses'
    
    # basis -> bases
    if word == 'basis':
        return 'bases'
    
    # crisis -> crises
    if word == 'crisis':
        return 'crises'
    
    # thesis -> theses
    if word == 'thesis':
        return 'theses'
    
    # hypothesis -> hypotheses
    if word == 'hypothesis':
        return 'hypotheses'
    
    # diagnosis -> diagnoses
    if word == 'diagnosis':
        return 'diagnoses'
    
    # axis -> axes
    if word == 'axis':
        return 'axes'
    
    # phenomenon -> phenomena
    if word == 'phenomenon':
        return 'phenomena'
    
    # datum -> data
    if word == 'datum':
        return 'data'
    
    # alumnus -> alumni
    if word == 'alumnus':
        return 'alumni'
    
    # genus -> genera
    if word == 'genus':
        return 'genera'
    
    # curriculum -> curricula
    if word == 'curriculum':
        return 'curricula'
    
    # bacterium -> bacteria
    if word == 'bacterium':
        return 'bacteria'
    
    # symposium -> symposia
    if word == 'symposium':
        return 'symposia'
    
    # memorandum -> memoranda
    if word == 'memorandum':
        return 'memoranda'
    
    # octopus -> octopi or octopuses
    if word == 'octopus':
        return 'octopuses'
    
    # radius -> radii
    if word == 'radius':
        return 'radii'
    
    # vertebra -> vertebrae
    if word == 'vertebra':
        return 'vertebrae'
    
    # larva -> larvae
    if word == 'larva':
        return 'larvae'
    
    # adder -> adders (regular)
    # Apply regular plural rules
    if re.search(r'(?:s|x|z|ch|sh)$', s, re.I):
        return s + 'es'
    if re.search(r'[^aeiou]y$', s, re.I):
        return s[:-1] + 'ies'
    return s + 's'

def _articlize(s):
    if not s:
        return s
    return ('an ' if re.match(r'[aeiouAEIOU]', s) else 'a ') + s

def _capitalize(s):
    if not s:
        return s
    return s[0].upper() + s[1:]

def _quotify(s):
    return '\u201c' + s + '\u201d'

def _identity(s):
    return s

DEFAULT_TRANSFORMS = {
    'quotify':    _quotify,
    'pluralize':  _pluralize,
    'articlize':  _articlize,
    'capitalize': _capitalize,
    'ucf':        _capitalize,
    'cap':        _capitalize,
    'uc':         str.upper,
    'lc':         str.lower,
    'art':        _articlize,
    'qq':         _quotify,
    's':          _pluralize,
    'nr':         _identity,
    'norepeat':   _identity,
    'toUpperCase': str.upper,
    'toLowerCase': str.lower,
}

# ── Pre/post parse ───────────────────────────────────────────────────────────

_COMMENT_RE        = re.compile(r'(?:^|\r?\n)\s*//[^\r\n]*|/\*.*?\*/', re.DOTALL | re.MULTILINE)
_INLINE_ASSIGN_RE  = re.compile(r'^([$#][A-Za-z_0-9]+)\s*=(.+)$', re.MULTILINE)
_CONTINUATION_RE   = re.compile(r'~\n')
_WEIGHT_PAREN_RE   = re.compile(r'\(\s*(\d+)\s*\)')
_MD_LINK_RE        = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

def _pre_parse(text):
    if not text:
        return text
    # normalize Windows-style line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # escape markdown links [text](url) -> entity form  (BEFORE comment stripping, URLs may contain //)
    text = _MD_LINK_RE.sub(lambda m: f'&lsqb;{m.group(1)}&rsqb;&lpar;{m.group(2)}&rpar;', text)
    # strip comments (consume preceding \n for line comments to avoid blank lines)
    text = _COMMENT_RE.sub('', text)
    # clean up blank lines left by comment removal
    text = re.sub(r'\n{2,}', '\n', text).lstrip('\n')
    # line continuation: ~\n and also \<newline> (JS backslash-continuation)
    text = _CONTINUATION_RE.sub('', text)
    text = re.sub(r'\\\n', '', text)
    # (N) -> ^N^
    text = _WEIGHT_PAREN_RE.sub(r'^\1^', text)
    # wrap bare top-level assignments: $foo=bar -> {$foo=bar}
    # Track bracket depth so multiline values like $foo=[cat\ndog] stay together.
    depth = 0
    segments = []
    current = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == '\\' and i + 1 < len(text):
            # escaped char — pass through as-is, don't count brackets
            current.append(ch)
            current.append(text[i + 1])
            i += 2
            continue
        if ch == '[':
            depth += 1
            current.append(ch)
        elif ch == ']':
            depth -= 1
            current.append(ch)
        elif ch == '\n' and depth == 0:
            segments.append(''.join(current))
            current = []
        else:
            current.append(ch)
        i += 1
    segments.append(''.join(current))

    result = []
    for seg in segments:
        m = _INLINE_ASSIGN_RE.match(seg.strip())
        if m:
            result.append(('{' + seg.strip() + '}', True))
        else:
            result.append((seg, False))

    out = []
    for i, (seg, is_assign) in enumerate(result):
        out.append(seg)
        if i < len(result) - 1:
            # suppress \n only after an assignment segment (assignments consume their newline)
            if not is_assign:
                out.append('\n')
    return ''.join(out)

_ENTITY_MAP = {
    'lpar': '(', 'rpar': ')', 'lsqb': '[', 'rsqb': ']',
    'nbsp': '\u00a0', 'amp': '&', 'apos': "'", 'quot': '"',
    'lbrack': '[', 'rbrack': ']',
    'lt': '<', 'gt': '>', 'lbrace': '{', 'rbrace': '}', 'lcub': '{', 'rcub': '}',
    'dollar': '$', 'vert': '|', 'num': '#', 'period': '.', 'bsol': '\\',
    'equals': '=', 'commat': '@', 'sol': '/', 'semi': ';', 'colon': ':',
}

def _decode_entities(text):
    def _replace(m):
        name = m.group(1)
        if name.startswith('#x'):
            return chr(int(name[2:], 16))
        if name.startswith('#'):
            return chr(int(name[1:]))
        return _ENTITY_MAP.get(name, m.group(0))
    return re.sub(r'&([a-zA-Z][a-zA-Z0-9]*|#[0-9]+|#x[0-9a-fA-F]+);', _replace, text)

_UNICODE_WHITESPACE_RE = re.compile(r'[\u00a0\u2000-\u200b\u2028\u2029\u3000]+')

def _post_parse(text):
    if not text:
        return text
    # any unresolved pending gates become empty string
    text = re.sub(r'@@\d{9,11}', '', text)
    text = _decode_entities(text)
    # normalize Unicode whitespace (e.g. &nbsp; -> \u00a0) to regular space
    text = _UNICODE_WHITESPACE_RE.sub(' ', text)
    return text

# ── JSOL parser (JSON-ish with unquoted keys and @ operators) ────────────────

def parse_jsol(text):
    """Parse JSOL: JSON with unquoted keys, @operators -> $operators, regex literals."""
    text = text.strip()
    # remove outer braces if present
    if text.startswith('{') and text.endswith('}'):
        text = text[1:-1].strip()
    # quote bare keys: $word() or $word or @word or word -> "...":
    text = re.sub(r'([$@]?[A-Za-z_][A-Za-z_0-9]*(?:\(\))?)\s*:', r'"\1":', text)
    # single quotes -> double quotes (for JSON compat)
    text = re.sub(r"'([^']*)'", r'"\1"', text)
    # regex literals: /pattern/flags -> {"$regex": "pattern"}
    text = re.sub(r'/([^/]+)/[gimy]*', r'{"$regex": "\1"}', text)
    import json
    return json.loads('{' + text + '}')

# ── Gate evaluation (mingo-style) ────────────────────────────────────────────

def _eval_gate(condition_obj, context):
    """Evaluate a mingo-style query object against context dict."""
    import json

    def _normalize_keys(obj):
        """Recursively convert @op to $op in dict keys."""
        if isinstance(obj, dict):
            result = {}
            for k, v in obj.items():
                norm_key = k.replace('@', '$')
                norm_val = _normalize_keys(v)
                result[norm_key] = norm_val
            return result
        elif isinstance(obj, list):
            return [_normalize_keys(item) for item in obj]
        else:
            return obj

    condition_obj = _normalize_keys(condition_obj)

    def _test_value(doc_val, cond):
        if isinstance(cond, dict):
            if not cond:
                return False  # empty condition = always false
            for op, operand in cond.items():
                if op == '$eq':
                    if str(doc_val) != str(operand): return False
                elif op == '$ne':
                    if str(doc_val) == str(operand): return False
                elif op == '$gt':
                    try:
                        if float(doc_val) <= float(operand): return False
                    except (TypeError, ValueError): return False
                elif op == '$gte':
                    try:
                        if float(doc_val) < float(operand): return False
                    except (TypeError, ValueError): return False
                elif op == '$lt':
                    try:
                        if float(doc_val) >= float(operand): return False
                    except (TypeError, ValueError): return False
                elif op == '$lte':
                    try:
                        if float(doc_val) > float(operand): return False
                    except (TypeError, ValueError): return False
                elif op == '$in':
                    if doc_val not in operand: return False
                elif op == '$nin':
                    if doc_val in operand: return False
                elif op == '$exists':
                    if operand and doc_val is None: return False
                    if not operand and doc_val is not None: return False
                elif op == '$regex':
                    if not re.search(operand, str(doc_val)): return False
                else:
                    return False  # unknown op
            return True
        else:
            return str(doc_val) == str(cond)

    def _test(doc, cond_obj):
        for key, cond in cond_obj.items():
            if key == '$or':
                if not any(_test(doc, c) for c in cond): return False
            elif key == '$and':
                if not all(_test(doc, c) for c in cond): return False
            elif key == '$nor':
                if any(_test(doc, c) for c in cond): return False
            else:
                # Strip $ prefix from key to match context keys
                lookup_key = key.lstrip('$')
                doc_val = doc.get(lookup_key)
                if not _test_value(doc_val, cond): return False
        return True

    return _test(context, condition_obj)

_MINGO_OPS = {'$gt','$lt','$gte','$lte','$ne','$eq','$exists','$in','$nin','$or','$and','$nor','$regex',
              '@gt','@lt','@gte','@lte','@ne','@eq','@exists','@in','@nin','@or','@and','@nor','@regex'}

def _get_operands(condition_obj):
    """Get all variable-reference keys ($a, $b, etc.) from a condition object."""
    keys = set()
    stack = [condition_obj]
    while stack:
        obj = stack.pop()
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k not in _MINGO_OPS:
                    keys.add(k)  # includes $a, $b style refs and plain keys
                if isinstance(v, (dict, list)):
                    stack.append(v)
        elif isinstance(obj, list):
            for item in obj:
                stack.append(item)
    # Strip $ prefix to match JS behavior
    return [k.lstrip('$') for k in keys]

# ── Evaluator ────────────────────────────────────────────────────────────────

_SPECIAL_RE = re.compile(r'[|$#{}\[\]^~]|@@\d{9,11}|@\s*\{')

def _is_parseable(s):
    if s is None: return False
    if isinstance(s, (dict, list)): return False
    if callable(s): return True
    if isinstance(s, (int, float)): s = str(s)
    if isinstance(s, str):
        return bool(_SPECIAL_RE.search(s))
    return True

def _string_hash(text):
    """JS-compatible 32-bit string hash (same as Java String.hashCode)."""
    h = 0
    for ch in text:
        h = (31 * h + ord(ch)) & 0xFFFFFFFF
    # convert to signed 32-bit
    if h >= 0x80000000:
        h -= 0x100000000
    return h

class EvalVisitor:
    """AST-walking evaluator for RiScript.

    Maintains context (variable bindings, transforms, pending gates) across
    multiple evaluation passes of the same script.
    """

    def __init__(self, context=None, transforms=None):
        self.context      = dict(context or {})
        self.transforms   = dict(DEFAULT_TRANSFORMS)
        if transforms:
            self.transforms.update(transforms)
        self.dynamics     = {}   # ident -> callable
        self.statics      = {}   # ident -> value
        self.choices      = {}   # hash -> last chosen value (norepeat)
        self.pending_gates = {}  # key -> {gate_text, deferred_node, operands}
        self.is_no_repeat = False
        self._obj_store   = {}   # placeholder -> object (for non-string values)
        self._force_gate  = False
        self.randi        = lambda k: random.randint(0, k - 1) if k > 1 else 0

    # ── public ──────────────────────────────────────────────────────────────

    def evaluate(self, text):
        """Parse and evaluate a RiScript string, returning the result."""
        tree = parse(text)
        return self._visit_script(tree)

    # ── visitors ────────────────────────────────────────────────────────────

    def _pack_obj(self, obj):
        """Store a non-string object and return a safe placeholder string."""
        key = f'\x00obj{len(self._obj_store)}\x00'
        self._obj_store[key] = obj
        return key

    def _unpack_obj(self, s):
        """If s is a single object placeholder, return the original object; else return s."""
        if isinstance(s, str) and s in self._obj_store:
            return self._obj_store[s]
        return s

    def _visit_script(self, node):
        _, exprs = node
        parts = [self._visit_expr(e) for e in exprs]
        # If single non-string result, return it directly (preserves dict/int)
        non_none = [p for p in parts if p is not None]
        if len(non_none) == 1 and not isinstance(non_none[0], str):
            return non_none[0]
        result = ''
        for p in parts:
            if p is None:
                pass
            elif isinstance(p, str):
                result += p
            else:
                result += self._pack_obj(p)
        return result

    def _visit_expr(self, node):
        _, atoms = node
        results = [self._visit_atom(a) for a in atoms]
        results = ['' if r is None else r for r in results]

        if len(results) == 1:
            return results[0]

        # $+choice -> symbol ref: look at the atom nodes, not just results
        combined = []
        i = 0
        while i < len(atoms):
            r = results[i]
            a = atoms[i]
            is_bare_sigil = (a[0] == 'symbol' and not re.sub(r'\(\)$', '', a[1]).lstrip('$#'))
            if is_bare_sigil and i + 1 < len(atoms):
                sigil = re.sub(r'\(\)$', '', a[1])  # '$' or '#'
                nxt = results[i + 1]
                if isinstance(nxt, str) and nxt and re.match(r'[A-Za-z_0-9]', nxt):
                    combined.append(sigil + nxt)
                    i += 2
                    continue
            combined.append(r)
            i += 1

        if len(combined) == 1:
            return combined[0]

        # "not [quite|] far enough" -> collapse double spaces
        for i in range(1, len(combined) - 1):
            if combined[i] == '' and \
               isinstance(combined[i-1], str) and combined[i-1].endswith(' ') and \
               isinstance(combined[i+1], str) and combined[i+1].startswith(' '):
                combined[i+1] = combined[i+1][1:]

        return ''.join(str(c) for c in combined)

    def _visit_atom(self, node):
        kind = node[0]
        if kind == 'choice':
            return self._visit_choice(node)
        if kind == 'assign':
            return self._visit_assign(node)
        if kind == 'symbol':
            return self._visit_symbol(node)
        if kind == 'silent':
            return self._visit_silent(node)
        if kind == 'pgate':
            return self._visit_pgate(node)
        if kind == 'entity':
            return node[1]  # keep entity text; decoded in _post_parse
        if kind == 'text':
            return node[1]
        raise ParseError(f'Unknown atom kind: {kind}')

    def _visit_symbol(self, node, silent=False):
        _, sym, txs = node
        sym_clean = re.sub(r'\(\)$', '', sym)
        is_func_call = sym.endswith('()')
        ident = sym_clean.lstrip('$#')
        is_static = sym_clean.startswith('#')

        # bare $ or # — sigil with no ident
        # if followed by a choice in the same expr, _visit_expr will combine them
        # standalone bare $ -> '' (unresolved dynamic with empty name)
        if not ident:
            if txs:
                return self._apply_transforms('', txs)
            return ''  # bare $ or # alone

        self.is_no_repeat = self._has_no_repeat(txs)

        result, is_st, is_user, resolved = self._check_context(ident)

        # validate norepeat on statics/user vars
        if self.is_no_repeat and (is_st or is_user):
            kind_str = 'static' if is_st else 'non-dynamic'
            raise RuntimeError(f"Attempt to call norepeat() on {kind_str} symbol '{sym}'")

        # validate: #foo can't reference a dynamic
        if is_static and not is_st and ident in self.dynamics:
            raise RuntimeError(f"Attempt to access dynamic symbol '{ident}' as static '#'")

        # call functions / resolve callables
        depth = 0
        while callable(result):
            try:
                result = result('')  # call with empty string (transform on nothing)
            except TypeError:
                try:
                    result = result()  # 0-arg function
                except TypeError:
                    result = str(result)
                    break
            resolved = not _is_parseable(result)
            depth += 1
            if depth > 10: raise RuntimeError('Max recursion depth')

        # unpack object store placeholders
        if isinstance(result, str):
            result = self._unpack_obj(result)

        # unresolved — nothing found in context/dynamics/statics/transforms
        if result is None:
            if silent:
                if txs:
                    return self._restore_transforms(sym_clean, txs)
                return sym_clean  # preserve in silent mode
            # defer — preserve for next pass
            if txs:
                return self._restore_transforms(sym_clean, txs)
            return sym_clean

        # still has parseable script
        if isinstance(result, str) and not resolved:
            if is_st:
                # static value is parseable — evaluate it now and cache for consistency
                # Use a minimal sub-visitor that shares state, and get the raw result
                # (not stringified) so dict/object values can be stored directly
                evaluated = EvalVisitor(self.context, self.transforms)
                evaluated.dynamics = self.dynamics
                evaluated.statics = self.statics
                evaluated.choices = self.choices
                # Parse and visit the parseable string, returning raw value (may be dict)
                try:
                    sub_tree = parse(result)
                    raw_val = evaluated._visit_script(sub_tree)
                except Exception:
                    raw_val = result
                if raw_val is None or (isinstance(raw_val, str) and _is_parseable(raw_val)):
                    return result  # still unresolved, defer
                if isinstance(raw_val, str):
                    raw_val = self._unpack_obj(raw_val)
                self.statics[ident] = raw_val
                result = raw_val
                # fall through to apply transforms below
                if txs:
                    result = self._apply_transforms(result, txs)
                self.is_no_repeat = False
                return result
            if txs:
                return self._restore_transforms(result, txs)
            return result  # defer — return the parseable value for next pass

        # store untransformed result for statics
        if is_st:
            self.statics[ident] = result

        # apply transforms
        if txs:
            result = self._apply_transforms(result, txs)
        elif isinstance(result, str) and len(result) == 0 and len(sym_clean) == 1:
            # bare $ without transform
            return sym_clean

        self.is_no_repeat = False
        return result

    def _visit_assign(self, node, silent=False):
        _, sym, rhs_node = node
        sym_clean = sym.rstrip('()')
        ident = sym_clean.lstrip('$#')
        is_static = sym_clean.startswith('#')

        if is_static:
            if ident in self.statics and not _is_parseable(self.statics[ident]):
                return self.statics[ident]
            val = self._visit_expr(rhs_node)
            self.statics[ident] = val
            return val
        else:
            # dynamic — store as lambda, return current evaluation
            val = self._visit_expr(rhs_node)
            rhs = rhs_node  # capture
            self.dynamics[ident] = lambda: self._visit_expr(rhs)
            # if val is a non-string object (dict/object), cache it directly
            if not isinstance(val, (str, type(None))):
                _cached = val
                self.dynamics[ident] = lambda: _cached
            return val  # return as-is; _visit_script/_pack_obj handles non-strings

    def _visit_silent(self, node):
        _, gate, inner = node
        if gate:
            decision = self._eval_gate_text(gate)
            if decision == 'defer':
                # treat as accept for now (simplified)
                pass
        if inner:
            _, kind2 = inner[0], inner
            if inner[0] == 'assign':
                self._visit_assign(inner, silent=True)
            else:
                self._visit_symbol(inner, silent=True)
        return ''

    def _visit_choice(self, node):
        _, gate_text, or_expr, else_expr, txs = node
        original = self._node_to_text(node)
        choice_key = str(_string_hash(original))

        if self._has_no_repeat(txs):
            raise RuntimeError(f'noRepeat() not allowed on choice (use a $variable instead): {original}')

        decision = 'accept'
        if gate_text:
            decision = self._eval_gate_text(gate_text)
            if decision == 'defer':
                key = str(abs(_string_hash(gate_text + original))).zfill(10)
                self.pending_gates[key] = {
                    'gate_text': gate_text,
                    'node': node,
                    'operands': self._get_gate_operands(gate_text),
                }
                return f'@@{key}'

        branches = or_expr if decision != 'reject' else (else_expr if else_expr else [])
        if not branches:
            return ''

        options = self._parse_options(branches)
        if not options:
            return ''

        excluded = []
        value = None
        restored = False
        while value is None:
            option = self._choose(options, excluded)
            if option == '':
                value = ''
            else:
                value = self._visit_expr(option) if isinstance(option, tuple) else option

            if isinstance(value, str):
                value = value.strip()

            # if still parseable, restore transforms and defer
            if _is_parseable(value):
                if txs:
                    value = self._restore_transforms(value, txs)
                restored = True
                break

            if txs:
                value = self._apply_transforms(value, txs)

            # norepeat check
            if self.is_no_repeat and value == self.choices.get(choice_key):
                excluded.append(value)
                value = None
                continue

        if not restored:
            self.choices[choice_key] = value

        return value

    def _visit_pgate(self, node):
        _, raw = node
        key = raw.replace('@@', '')
        lookup = self.pending_gates.get(key)
        if not lookup:
            raise RuntimeError(f'No pending gate: {raw!r}')

        def _op_unresolved(op):
            ident = op.lstrip('$#').rstrip('()')
            result, _, _, resolved = self._check_context(ident)
            while callable(result):
                result = result()
            # still parseable string = unresolved; None or scalar = resolved
            return isinstance(result, str) and _is_parseable(result)

        still_unresolved = any(_op_unresolved(op) for op in lookup['operands'])
        if still_unresolved:
            return raw  # still defer

        self._force_gate = True
        result = self._visit_choice(lookup['node'])
        self._force_gate = False
        return result

    # ── gate helpers ─────────────────────────────────────────────────────────

    def _eval_gate_text(self, gate_text):
        raw = gate_text.lstrip('@').strip()
        try:
            cond = parse_jsol(raw)
        except Exception as e:
            raise RuntimeError(f'Invalid gate: "{gate_text}"\n{e}')

        operands = _get_operands(cond)
        if not operands and not any(k in cond for k in ('$or', '$and', '$nor')):
            raise RuntimeError(f'Empty gate (no operands): "{gate_text}"')
        resolved_ops = {}
        unresolved = []

        for sym in operands:
            ident = sym.lstrip('$#').rstrip('()')  # strip sigil for lookup
            result, _, _, resolved = self._check_context(ident)
            depth = 0
            while callable(result):
                result = result()
                resolved = not _is_parseable(result)
                depth += 1
                if depth > 10: raise RuntimeError('Max recursion depth')
            if not self._force_gate and (result is None or (isinstance(result, str) and _is_parseable(result))):
                # not yet defined or still a parseable expression — defer
                unresolved.append(sym)
            else:
                resolved_ops[sym] = result

        if unresolved:
            return 'defer'

        if _eval_gate(cond, resolved_ops):
            return 'accept'
        # try casting to numbers
        casted = {}
        made_cast = False
        for k, v in resolved_ops.items():
            try:
                casted[k] = float(v)
                made_cast = True
            except (TypeError, ValueError):
                casted[k] = v
        if made_cast and _eval_gate(cond, casted):
            return 'accept'
        return 'reject'

    def _get_gate_operands(self, gate_text):
        raw = gate_text.lstrip('@').strip()
        try:
            cond = parse_jsol(raw)
            return _get_operands(cond)
        except Exception:
            return []

    # ── context lookup ────────────────────────────────────────────────────────

    def _check_context(self, ident):
        """Look up ident in dynamics → statics → user context → transforms.

        Returns (result, is_static, is_user, resolved).
        """
        if not ident:
            return ('', False, False, True)

        result = self.dynamics.get(ident)
        is_static = is_user = False

        if result is None:
            result = self.statics.get(ident)
            if result is not None:
                is_static = True

        if result is None:
            result = self.context.get(ident)
            if result is not None:
                is_user = True

        if result is None:
            result = self.transforms.get(ident)

        resolved = not _is_parseable(result)
        return (result, is_static, is_user, resolved)

    # ── transform helpers ─────────────────────────────────────────────────────

    def _has_no_repeat(self, txs):
        """Return True if any transform in txs is a norepeat variant."""
        return any(tx.lstrip('.').rstrip('()') in ('nr', 'norepeat') for tx in (txs or []))

    def _apply_transforms(self, value, txs):
        for tx_image in txs:
            value = self._apply_transform(value, tx_image)
        return value

    def _apply_transform(self, target, image):
        tx = image.lstrip('.').rstrip('()')

        def _call(fn, val):
            """Call fn with val, falling back to 0-arg if needed."""
            try:
                return fn(val)
            except TypeError:
                try:
                    return fn()
                except TypeError:
                    return val

        # context function
        fn = self.context.get(tx)
        if callable(fn):
            return _call(fn, target)

        # registered transform
        fn = self.transforms.get(tx)
        if callable(fn):
            return _call(fn, target)

        # dynamics/statics
        fn = self.dynamics.get(tx)
        if callable(fn):
            return _call(fn, target)
        fn = self.statics.get(tx)
        if callable(fn):
            return _call(fn, target)

        # object property/method
        if target is not None and isinstance(target, dict):
            if tx in target:
                v = target[tx]
                return v() if callable(v) else v

        # object attribute/method (class instances)
        if target is not None and not isinstance(target, (str, int, float, bool)):
            attr = getattr(target, tx, None)
            if attr is not None:
                return attr() if callable(attr) else attr

        # string method
        if isinstance(target, str):
            method = getattr(str, tx, None)
            if callable(method):
                return method(target)

        # unresolved — if silent mode, preserve as text; if empty target, return empty
        if target == '':
            return ''
        return str(target) + image

    def _restore_transforms(self, value, txs):
        if isinstance(value, str):
            choice_re = re.compile(r'^\[.*\]$', re.DOTALL)
            sym_re = re.compile(r'[$#][A-Za-z_0-9]')
            if not choice_re.match(value) and not sym_re.search(value):
                value = '[' + value + ']'
            for tx in txs:
                value += tx
        return value

    # ── option parsing ────────────────────────────────────────────────────────

    def _parse_options(self, branches):
        """Expand weighted branches into a flat options list.

        Each branch may contain a weight token (``^N^``) that repeats the
        corresponding option N times to produce a weighted distribution.
        """
        options = []
        for branch in branches:
            weight = 1
            expr_items = []
            for item in branch:
                if isinstance(item, tuple) and item[0] == 'weight':
                    try:
                        weight = int(item[1].strip().strip('^'))
                    except ValueError:
                        pass
                else:
                    expr_items.append(item)

            # rebuild a single expr node from the collected items
            if not expr_items:
                opt = ('expr', [])
            elif len(expr_items) == 1:
                opt = expr_items[0]
            else:
                opt = ('expr', [('text', self._visit_expr(e)) if isinstance(e, tuple) else e
                                for e in expr_items])

            options.extend([opt] * weight)

        return options

    def _choose(self, options, excluded):
        valid = [o for o in options if o not in excluded]
        if not valid:
            raise RuntimeError('No valid options (all excluded)')
        return valid[self.randi(len(valid))]

    def _node_to_text(self, node):
        """Rough text representation of a node for hashing."""
        return repr(node)

# ── Public API ────────────────────────────────────────────────────────────────

class RiScript:
    """Public API for evaluating RiScript expressions.

    Manages transforms, visitor state, and multi-pass evaluation.
    """

    def __init__(self, transforms=None, rita=None):
        self.extra_transforms = transforms or {}
        self.rita = rita
        self._visitor = None

    def evaluate(self, script, context=None, **opts):
        """Evaluate a RiScript string, running up to 10 passes until fully resolved.

        Args:
            script:  The RiScript source string.
            context: Optional dict of variable bindings and/or custom transforms.
            **opts:  onepass=True to stop after first pass; silent=True to keep
                     unresolved symbol references in the output.
        Returns:
            The evaluated string.
        """
        if not isinstance(script, str):
            raise TypeError(f'evaluate() expects str, got {type(script).__name__}')

        ends_with_newline = script.endswith('\n')
        expr = _pre_parse(script)
        if not expr:
            return ''

        transforms = dict(DEFAULT_TRANSFORMS)
        transforms.update(self.extra_transforms)
        visitor = EvalVisitor(context or {}, transforms)
        if self.rita:
            visitor.randi = lambda k: self.rita.randi(k)
        self._visitor = visitor

        last = None
        for _ in range(10):
            if expr == last:
                break
            last = expr
            expr = visitor.evaluate(expr) or ''
            if opts.get('onepass') or not _is_parseable(expr):
                break

        # strip any unresolved symbols (stuck after all passes)
        if not opts.get('silent'):
            expr = re.sub(r'(?<!&)(?:\$|#)[A-Za-z_][A-Za-z_0-9]*(?:\(\))?(?:\.[A-Za-z_][A-Za-z_0-9]*(?:\(\))?)*', '', expr)

        result = _post_parse(expr)
        if not ends_with_newline:
            result = result.rstrip('\n')
        elif not result.endswith('\n'):
            result = result + '\n'
        return result

    @staticmethod
    def static_evaluate(script, context=None, **opts):
        return RiScript().evaluate(script, context, **opts)

    def add_transform(self, name, fn):
        self.extra_transforms[name] = fn
        return self

    def remove_transform(self, name):
        self.extra_transforms.pop(name, None)
        return self

    def is_parseable(self, s):
        return _is_parseable(s)

    def pre_parse(self, s):
        return _pre_parse(s)

    def parse_jsol(self, s):
        return parse_jsol(s)

    @staticmethod
    def string_hash(s):
        return str(_string_hash(s))

    @staticmethod
    def lex(script, opts=None):
        """Lex a RiScript string into tokens.

        Args:
            script: The RiScript source string to tokenize, OR a dict with 'input' key.
            opts: Optional dict with 'traceLex' to enable tracing.

        Returns:
            If script is a string: List of Token objects.
            If script is a dict: Same dict with 'tokens' key added.
        """
        if isinstance(script, dict):
            # JS-style: pass config object, get it back with tokens added
            script_input = script.get('input', '')
            result = tokenize(script_input)
            script['tokens'] = list(result)
            if script.get('traceLex'):
                for token in result:
                    print(f"{token.type}: '{token.value}'")
            return script
        else:
            result = list(tokenize(script))
            if opts and opts.get('traceLex'):
                for token in result:
                    print(f"{token.type}: '{token.value}'")
            return result

    # RiTa compatibility - add standard RiTa methods
    VERSION = "3.0.0"

    # Question detection - list of question starters
    QUESTIONS = ['what', 'how', 'when', 'where', 'why', 'who', 'which', 'whose', 'whom',
                'do', 'does', 'did', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                'have', 'has', 'had', 'has', 'can', 'could', 'will', 'would', 'shall',
                'should', 'may', 'might', 'must', 'need', 'dare', 'ought', 'used']

    VOWELS = 'aeiou'
    STOP_WORDS = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
                 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                 'could', 'should', 'may', 'might', 'must', 'shall', 'can',
                 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
                 'it', 'we', 'they', 'what', 'which', 'who', 'whom', 'whose']

    @property
    def transforms(self):
        """Return a mutable dict merging DEFAULT_TRANSFORMS + extra_transforms."""
        combined = dict(DEFAULT_TRANSFORMS)
        combined.update(self.extra_transforms)
        return _TransformProxy(self.extra_transforms, combined)

    @staticmethod
    def isQuestion(sentence):
        """Check if sentence is a question"""
        if not sentence:
            return False
        tokens = RiScript.tokenize(sentence)
        if tokens:
            first = tokens[0].lower()
            return first in RiScript.QUESTIONS or first == '?'
        return False

    @staticmethod
    def isAbbrev(input):
        """Check if text is an abbreviation"""
        if not input or not isinstance(input, str):
            return False
        # Simple check: ends with period and has multiple capital letters or is short
        return input.endswith('.') and (len(input) < 10 or any(c.isupper() for c in input[1:-1]))

    @staticmethod
    def isPunct(text):
        """Check if text is punctuation"""
        if not text or not isinstance(text, str):
            return False
        return len(text) == 1 and not text.isalnum()

    @staticmethod
    def isStopWord(word):
        """Check if word is a stop word"""
        if not word or not isinstance(word, str):
            return False
        return word.lower() in RiScript.STOP_WORDS

    @staticmethod
    def addTransform(name, fn):
        """Add a transform function to RiScript"""
        RiScript.transforms[name] = fn

    @staticmethod
    def removeTransform(name):
        """Remove a transform function from RiScript"""
        if name in DEFAULT_TRANSFORMS or name in RiScript.transforms:
            RiScript.transforms.pop(name, None)

    @staticmethod
    def getTransforms():
        """Get list of transform names"""
        return list(DEFAULT_TRANSFORMS.keys())

    def _evaluate(self, input, visitor=None):
        """Low-level evaluate with a pre-configured visitor."""
        if visitor is None:
            visitor = EvalVisitor({}, dict(DEFAULT_TRANSFORMS))
        self._visitor = visitor
        ends_with_newline = input.endswith('\n')
        expr = _pre_parse(input)
        if not expr:
            return ''
        last = None
        for _ in range(10):
            if expr == last:
                break
            last = expr
            expr = visitor.evaluate(expr) or ''
            if not _is_parseable(expr):
                break
        result = _post_parse(expr)
        if not ends_with_newline:
            result = result.rstrip('\n')
        elif not result.endswith('\n'):
            result = result + '\n'
        return result

    @property
    def visitor(self):
        return self._visitor

    class Query:
        """Mingo-style query object for gate evaluation."""
        def __init__(self, riscript_instance, obj):
            if isinstance(obj, str):
                self._cond = parse_jsol(obj)
            else:
                # convert JS-style keys ($op) to @op style for internal use,
                # or just store as-is; _eval_gate already handles both
                self._cond = obj

        def operands(self, riscript_instance, obj=None):
            if obj is None:
                cond = self._cond
            elif isinstance(obj, str):
                cond = parse_jsol(obj)
            else:
                cond = obj
            return _get_operands(cond)

        def test(self, context):
            return _eval_gate(self._cond, context)

    # Expose Visitor class
    Visitor = EvalVisitor

class _TransformProxy(dict):
    """A dict proxy that writes through to the backing store."""
    def __init__(self, backing, combined):
        super().__init__(combined)
        self._backing = backing

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._backing[key] = value

    def __delitem__(self, key):
        super().pop(key, None)
        self._backing.pop(key, None)

# ── RiGrammar ─────────────────────────────────────────────────────────────────

import json as _json

class RiGrammar:
    """
    A probabilistic context-free grammar for text generation, using RiScript rules.
    Rules are dynamic by default; prefix with '#' to make them static.
    """

    def __init__(self, rules=None, context=None, options=None):
        self.rules = {}
        self.context = context or {}
        self._scripting = RiScript()

        if rules is None:
            return

        if isinstance(rules, str):
            rules = self._parse_json(rules)

        if not isinstance(rules, dict):
            raise ValueError(f'RiGrammar: expecting dict, found {type(rules).__name__}')

        self.set_rules(rules)

    def expand(self, options=None):
        """
        Instance call:  rg.expand()  or  rg.expand({'start': 'rule'})
        Static-style:   RiGrammar.expand(rules_dict, context) -> str
          (Python will pass rules_dict as self; we detect and handle this)
        """
        if not isinstance(self, RiGrammar):
            # called as RiGrammar.expand(rules, context)
            rules = self
            context = options
            return RiGrammar(rules, context)._expand({})
        return self._expand(options or {})

    @staticmethod
    def from_json(json_str, context=None):
        """Create a RiGrammar from a JSON string."""
        if not isinstance(json_str, str):
            raise ValueError('RiGrammar.from_json expects a string')
        return RiGrammar(RiGrammar._parse_json(json_str), context)

    # alias
    fromJSON = from_json

    def add_rule(self, name, definition):
        if not isinstance(name, str) or not name:
            raise ValueError('expected non-empty string name')
        if definition is None:
            raise ValueError(f'undefined rule definition: {name}')
        # convert list rules to pipe-separated string (JS array syntax)
        if isinstance(definition, list):
            definition = ' | '.join(str(v) for v in definition)
        # disallow $-prefixed names (dynamic is the default)
        if name.startswith('$'):
            bare = name[1:]
            raise ValueError(
                f"Grammar rules are dynamic by default; use '{bare}' or '#{bare}' for static"
            )
        if name.startswith('$$'):
            raise ValueError('Invalid rule name: ' + name)
        self.rules[name] = definition
        return self

    # alias
    addRule = add_rule

    def set_rules(self, rules):
        if rules is None:
            raise ValueError('undefined rules')
        if isinstance(rules, str):
            rules = self._parse_json(rules)
        self.rules = {}
        for name, defn in rules.items():
            self.add_rule(name, defn)
        return self

    # alias
    setRules = set_rules

    def remove_rule(self, name):
        if not name:
            return self
        # $-prefixed: do nothing (per JS semantics)
        if name.startswith('$'):
            return self
        self.rules.pop(name, None)
        return self

    # alias
    removeRule = remove_rule

    def to_json(self, indent=2):
        return _json.dumps(self.rules, indent=indent)

    def toJSON(self, indent=2):
        return self.to_json(indent)

    def to_string(self, options=None):
        options = options or {}
        lb = options.get('linebreak')
        indent = options.get('space', 2)
        result = self.to_json(indent=indent)
        if lb:
            result = result.replace('\n', lb)
        return result

    def toString(self, options=None):
        return self.to_string(options)

    def _expand(self, options):
        if 'context' in options:
            raise ValueError('pass context to RiGrammar() constructor instead')

        start = options.get('start', 'start')
        start = start.lstrip('$#')

        # validate start rule exists
        if start not in self.rules and ('#' + start) not in self.rules:
            raise ValueError(f'Rule "{start}" not found in grammar')

        # validate start is a plain rule name (no sigils/spaces)
        if re.search(r'[\s$]', start):
            raise ValueError(f'Invalid start rule: "{start}"')

        script = self._to_script(start)
        visitor = EvalVisitor(self.context, DEFAULT_TRANSFORMS)
        return self._scripting._evaluate(input=script, visitor=visitor)

    def _to_script(self, start='start'):
        """Convert grammar rules to a self-contained RiScript string.

        Each rule becomes an inline assignment (e.g. ``$hero=[knight|mage]``),
        followed by a reference to the start symbol.
        """
        lines = []
        for name, rule in self.rules.items():
            # normalise name: strip leading $, keep # for statics
            if name.startswith('$'):
                name = name[1:]
            if not name.startswith('#'):
                name = '$' + name
            # wrap rule in [...] if not already a single balanced choice
            stripped = rule.strip()
            needs_wrap = True
            if stripped.startswith('[') and stripped.endswith(']'):
                # Check that the opening [ closes at the end (balanced, single choice)
                depth = 0
                top_level_or = False
                for ch in stripped:
                    if ch == '[': depth += 1
                    elif ch == ']':
                        depth -= 1
                        if depth == 0:
                            break
                    elif ch == '|' and depth == 1:
                        pass  # OR inside the choice — that's fine
                # Check: does the first [ close at the very end?
                depth = 0
                close_pos = -1
                for i, ch in enumerate(stripped):
                    if ch == '[': depth += 1
                    elif ch == ']':
                        depth -= 1
                        if depth == 0:
                            close_pos = i
                            break
                # If the first [ closes at the end of the string, it's already wrapped
                needs_wrap = (close_pos != len(stripped) - 1)
            if needs_wrap:
                rule = '[' + rule + ']'
            lines.append(f'{name}={rule}')

        script = '\n'.join(lines) + '\n' + f'${start}'
        return script

    @staticmethod
    def _parse_json(s):
        try:
            return _json.loads(s)
        except Exception:
            raise ValueError(
                'RiGrammar appears to be invalid JSON, please check it at http://jsonlint.com/\n' + s
            )

# Add lex method to RiScript class at the end of the file
# (will be appended via separate edit)
