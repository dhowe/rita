#!/usr/bin/env node
// js-to-py-tests.js — transpile the JS test suite to pytest
//
// Parses each js/test/*-tests.js with acorn and emits a Python pytest file that
// mirrors every describe/it/expect. chai assertions map to Python asserts;
// JS idioms map to their Python equivalents. Nothing is hand-written: rerun this
// after editing JS tests to regenerate the Python.
//
// Usage: node scripts/js-to-py-tests.js [file.js ...]
//   (no args => all js/test/*-tests.js)
//
// Output: python/tests/test_<name>.py
//
// This script was generated via a local AI model

const fs = require('fs');
const path = require('path');

// Repo root is derived from this script's location so the generator works from any
// checkout (and on any machine) rather than from a hardcoded absolute path.
const REPO_ROOT = path.resolve(__dirname, '..');
const JS_DIR = path.join(REPO_ROOT, 'js');

// acorn is a devDependency of js/; resolve it from there so `npm install` in js/ is
// what makes this script runnable.
let acorn;
try {
  acorn = require(require.resolve('acorn', { paths: [JS_DIR] }));
} catch (e) {
  console.error("Cannot find 'acorn' — run `npm install` in js/ first.");
  process.exit(1);
}

const JS_TEST_DIR = path.join(JS_DIR, 'test');
const OUT_DIR = path.join(REPO_ROOT, 'python', 'tests');

const argv = process.argv.slice(2);
const files = argv.length ? argv : fs.readdirSync(JS_TEST_DIR).filter(f => /-tests?\.js$/.test(f) && !f.includes('dist'));

// ---------------------------------------------------------------------------
// Small AST helpers
// ---------------------------------------------------------------------------

const isNode = (n, t) => n && n.type === t;
const id = (n) => n && n.type === 'Identifier' ? n.name : null;

function strLit(n) {
  if (n && n.type === 'Literal' && typeof n.value === 'string') return n.value;
  return null;
}

// ---------------------------------------------------------------------------
// Expression translation
// ---------------------------------------------------------------------------

// Translate a JS expression node to a Python expression string.
function T(node) {
  if (node === null || node === undefined) return 'None';
  switch (node.type) {
    case 'Literal':
      if (node.regex) return `_re_compile(${JSON.stringify(node.regex.pattern)})`;
      if (node.value === null) return 'None';
      if (typeof node.value === 'boolean') return node.value ? 'True' : 'False';
      if (typeof node.value === 'number') return String(node.value);
      if (typeof node.value === 'string') return pyStr(node.value);
      return String(node.value);

    case 'Identifier':
      return mapIdent(node.name);

    case 'TemplateLiteral':
      return template(node);

    case 'StringLiteral':
      return pyStr(node.value);

    case 'ArrayPattern':
      return '[' + node.elements.map(e => e ? T(e) : '_').join(', ') + ']';

    case 'ObjectPattern':
      return '{' + node.properties.map(p => (id(p.key) || id(p.value)) + ': ' + (id(p.value) || id(p.key))).join(', ') + '}';

    case 'ArrayExpression':
      return '[' + node.elements.map(e => e.type === 'SpreadElement' ? '*' + T(e.argument) : T(e)).join(', ') + ']';

    case 'ObjectExpression':
      return 'JsDict({' + node.properties.map(p => {
        if (p.type === 'SpreadElement') return '**' + T(p.argument);
        const key = p.key.type === 'Identifier' ? pyStr(p.key.name) :
                    p.key.type === 'Literal' ? (typeof p.key.value === 'string' ? pyStr(p.key.value) : String(p.key.value)) :
                    '[' + T(p.key) + ']';
        return key + ': ' + T(p.value);
      }).join(', ') + '})';

    case 'MemberExpression':
      return member(node);

    case 'CallExpression':
      return call(node);

    case 'NewExpression': {
      // new URL('./x.json', import.meta.url) => path relative to this test file
      if (node.callee.type === 'Identifier' && node.callee.name === 'URL' && node.arguments.length >= 2) {
        return '_url(' + T(node.arguments[0]) + ')';
      }
      return T(node.callee) + '(' + node.arguments.map(T).join(', ') + ')';
    }

    case 'BinaryExpression':
      return binary(node);

    case 'LogicalExpression': {
      const op = node.operator === '&&' ? ' and ' : node.operator === '||' ? ' or ' : ' ';
      return paren(T(node.left)) + op + paren(T(node.right));
    }

    case 'UnaryExpression': {
      if (node.operator === '!') return 'not ' + paren(T(node.argument));
      if (node.operator === 'typeof') return '_typeof(lambda: ' + T(node.argument) + ')';
      if (node.operator === 'void') return 'None';
      if (node.operator === '-') return '-' + paren(T(node.argument));
      if (node.operator === '+') return 'float(' + T(node.argument) + ')';
      if (node.operator === '+') return paren(T(node.argument));
      if (node.operator === '~') return '~' + paren(T(node.argument));
      return T(node.argument);
    }

    case 'UpdateExpression': {
      // x++ / ++x / x-- handled as statements above; as an expression, rare.
      const v = T(node.argument);
      const delta = node.operator === '++' ? ' + 1' : ' - 1';
      return v + delta;
    }

    case 'AssignmentExpression': {
      const op = node.operator === '=' ? '=' : node.operator;
      // Array/object destructuring assignment: ([a, b] = expr) => a, b = expr
      if ((node.left.type === 'ArrayPattern' || node.left.type === 'ObjectPattern') && node.operator === '=') {
        return node.left.elements ? node.left.elements.map(e => T(e)).join(', ') + ' = ' + T(node.right)
                                  : node.left.properties.map(p => (id(p.key) || id(p.value))).join(', ') + ' = ' + T(node.right);
      }
      // list.length = n  =>  del list[n:]
      if (node.left.type === 'MemberExpression' && !node.left.computed &&
          node.left.property.name === 'length') {
        return 'del ' + T(node.left.object) + '[' + T(node.right) + ':]';
      }
      // Assignment as an *expression* (e.g. inside call args) needs a walrus in
      // Python; statement-level assignments are rewritten to plain `x = y` by
      // exprStatement before reaching here.
      if (node.left.type === 'Identifier') {
        const name = mapName(node.left.name);
        if (op === '=') return '(' + name + ' := ' + T(node.right) + ')';
        return '(' + name + ' := ' + name + ' ' + op.slice(0, -1) + ' ' + T(node.right) + ')';
      }
      return T(node.left) + ' ' + op + ' ' + T(node.right);
    }

    case 'ConditionalExpression':
      return paren(T(node.consequent)) + ' if ' + paren(T(node.test)) + ' else ' + paren(T(node.alternate));

    case 'SequenceExpression':
      return node.expressions.map(T).join(', ');

    case 'ArrowFunctionExpression':
    case 'FunctionExpression':
      return functionExpr(node);

    case 'SpreadElement':
      return '*' + T(node.argument);

    case 'AwaitExpression':
      // RiTa.search etc. are promise-based in JS but synchronous in Python.
      return T(node.argument);

    case 'MetaProperty':
      return '__file__';

    case 'ChainExpression':
      return T(node.expression);

    case 'TaggedTemplateExpression':
      return T(node.tag) + '(' + template(node.quasi) + ')';

    case 'ThisExpression':
      return 'self';

    default:
      return `__UNTRANSLATED_${node.type}__()`;
  }
}

function paren(s) { return '(' + s + ')'; }

function pyStr(s) {
  // Prefer double quotes; escape backslashes and double quotes.
  return JSON.stringify(s);
}

function template(node) {
  let out = "f\"";
  for (let i = 0; i < node.quasis.length; i++) {
    const raw = node.quasis[i].value.cooked || '';
    out += raw.replace(/\\/g, '\\\\').replace(/"/g, '\\"')
              .replace(/\n/g, '\\n').replace(/\t/g, '\\t')
              .replace(/\{/g, '{{').replace(/\}/g, '}}');
    if (i < node.expressions.length) out += '{' + T(node.expressions[i]) + '}';
  }
  return out + '"';
}

function mapIdent(name) {
  const map = {
    'undefined': 'None', 'null': 'None', 'NaN': 'float("nan")', 'Infinity': 'float("inf")',
    'JSON': 'json', 'Math': 'math', 'Object': 'obj', 'Array': 'arr', 'String': 'str',
    'Number': 'float', 'Boolean': 'bool', 'console': 'console', 'process': 'process',
    'RiTa': 'RiTa', 'expect': 'expect', 'true': 'True', 'false': 'False',
    'Set': 'set', 'Map': 'dict', 'RegExp': 're.compile', 'Error': 'Exception',
    'URL': 'URL',
  };
  if (map[name]) return map[name];
  if (RENAME[name]) return RENAME[name];
  if (SHADOWS.has(name)) return name + '_';
  return mapName(name);
}

// Python reserved words that can be JS identifiers — suffix with _ so they are
// valid names, applied consistently to declarations and references.
const PY_RESERVED = new Set(['def', 'class', 'import', 'from', 'global', 'lambda', 'assert',
  'del', 'pass', 'break', 'continue', 'return', 'yield', 'raise', 'in', 'is', 'and', 'or',
  'not', 'if', 'elif', 'else', 'for', 'while', 'try', 'except', 'finally', 'with', 'as',
  'nonlocal', 'None', 'True', 'False', 'str']);
function mapName(name) {
  return PY_RESERVED.has(name) ? name + '_' : name;
}

// Python builtins that a JS local may shadow. Renaming them globally would
// break the `len(...)`/`list(...)` calls the generator itself emits, so we
// rename only inside the scope where the shadowing declaration appears.
const PY_BUILTINS = new Set(['len', 'list', 'set', 'map', 'sum', 'id', 'next', 'min', 'max',
  'open', 'iter', 'type', 'input', 'range', 'hash', 'round', 'sorted', 'reversed', 'zip',
  'abs', 'all', 'any', 'int', 'float', 'bool', 'dict', 'bytes', 'filter', 'format']);
let SHADOWS = new Set();
function shadowName(name) {
  if (PY_BUILTINS.has(name)) { SHADOWS.add(name); return name + '_'; }
  return mapName(name);
}
// Reference/assignment-target name: honors a shadowing declaration seen earlier.
function refName(name) {
  return SHADOWS.has(name) ? name + '_' : mapName(name);
}

// Convert a JS camelCase method name to its Python snake_case equivalent, so
// generated tests call the Python API by its idiomatic names (the port keeps
// camelCase only for option-dict keys and data attributes, not methods).
function camelToSnake(name) {
  return name
    .replace(/([A-Z]+)([A-Z][a-z])/g, '$1_$2')
    .replace(/([a-z0-9])([A-Z][a-z])/g, '$1_$2')
    .replace(/([a-z])([A-Z])/g, '$1_$2')
    .toLowerCase();
}

// Member expression: handle .length and method-ish property reads.
function member(node) {
  const obj = node.object;
  // import.meta.url / import.meta.filename => just __file__
  if (obj.type === 'MetaProperty') return '__file__';
  // Number.isInteger / isFinite / isNaN as predicate *values* (e.g. satisfy(...)).
  if (!node.computed && obj.type === 'Identifier' && obj.name === 'Number' &&
      node.property.type === 'Identifier') {
    if (node.property.name === 'isInteger') return '_is_integer';
    if (node.property.name === 'isFinite') return '_is_finite';
    if (node.property.name === 'isNaN') return '_is_nan';
  }
  if (node.computed) {
    // x[Symbol.iterator] => x.__iter__ (JS iterable protocol check).
    const prop = node.property;
    if (prop.type === 'MemberExpression' && !prop.computed &&
        prop.object.type === 'Identifier' && prop.object.name === 'Symbol' &&
        prop.property.type === 'Identifier' && prop.property.name === 'iterator') {
      return T(obj) + '.__iter__';
    }
    // results[i = 0] => results[(i := 0)] — assignment inside an index needs a walrus.
    if (node.property.type === 'AssignmentExpression') {
      return T(obj) + '[(' + T(node.property.left) + ' := ' + T(node.property.right) + ')]';
    }
    return T(obj) + '[' + T(node.property) + ']';
  }
  if (node.property.type === 'Identifier') {
    if (node.property.name === 'length') return 'len(' + T(obj) + ')';
    // JS Map/Set `.size` => Python len() of the underlying dict/set.
    if (node.property.name === 'size') return 'len(' + T(obj) + ')';
    // JS `SuffixArray.__dict__` is a static list of field names; Python's
    // __dict__ is a class mapping, so map to the equivalent _FIELDS list.
    if (node.property.name === '__dict__' && obj.type === 'Identifier' &&
        obj.name === 'SuffixArray') {
      return 'SuffixArray._FIELDS';
    }
  }
  return T(obj) + '.' + node.property.name;
}

// Call expression: dispatch on the callee to map JS methods to Python.
function call(node) {
  const callee = node.callee;
  if (callee.type === 'MemberExpression' && !callee.computed && callee.property.type === 'Identifier') {
    const obj = callee.object;
    const m = callee.property.name;
    const args = node.arguments;
    return memberCall(obj, m, args);
  }
  // expect(...) handled by the statement/assertion layer; here just pass through.
  if (callee.type === 'Identifier' && callee.name === 'expect') {
    return 'expect(' + node.arguments.map(T).join(', ') + ')';
  }
  if (callee.type === 'Identifier' && callee.name === 'parseInt') return 'int(' + args.map(T).join(', ') + ')';
  if (callee.type === 'Identifier' && callee.name === 'parseFloat') return 'float(' + args.map(T).join(', ') + ')';
  if (callee.type === 'Identifier' && callee.name === 'String') return 'str(' + args.map(T).join(', ') + ')';
  return T(callee) + '(' + node.arguments.map(T).join(', ') + ')';
}

function memberCall(obj, m, args) {
  const O = () => T(obj);
  const A = (i) => args[i] !== undefined ? T(args[i]) : null;
  // JSON.parse / JSON.stringify
  if (m === 'parse' && obj.type === 'Identifier' && obj.name === 'JSON') {
    return 'json.loads(' + T(args[0]) + ', object_hook=JsDict)';
  }
  if (m === 'stringify' && obj.type === 'Identifier' && obj.name === 'JSON') {
    return 'json.dumps(' + T(args[0]) + ')';
  }
  // Date.now() -> int(time.time() * 1000)
  if (m === 'now' && obj.type === 'Identifier' && obj.name === 'Date') {
    return 'int(time.time() * 1000)';
  }
  // Object.keys/values/entries(x) -> list(x.keys()) etc. (static call, arg is the target)
  if ((obj.type === 'Identifier' && obj.name === 'Object') &&
      (m === 'keys' || m === 'values' || m === 'entries')) {
    const arg = T(args[0]);
    if (m === 'keys') return 'list(' + arg + '.keys())';
    if (m === 'values') return 'list(' + arg + '.values())';
    return 'list(' + arg + '.items())';
  }
  // Number.isInteger(x) as a predicate expression
  if (m === 'isInteger' && obj.type === 'Identifier' && obj.name === 'Number') {
    return 'isinstance(' + T(args[0]) + ', int)';
  }
  if (m === 'isFinite' && obj.type === 'Identifier' && obj.name === 'Number') {
    return 'isinstance(' + T(args[0]) + ', (int, float))';
  }
  if (m === 'isNaN' && obj.type === 'Identifier' && obj.name === 'Number') {
    return 'isinstance(' + T(args[0]) + ', float) && ' + T(args[0]) + ' != ' + T(args[0]);
  }
  // Array.from({length: N}, fn) => [fn() for _ in range(N)]
  if (m === 'from' && obj.type === 'Identifier' && obj.name === 'Array' &&
      args[0] && args[0].type === 'ObjectExpression' &&
      args[0].properties.some(p => p.key && (p.key.name === 'length'))) {
    const lenProp = args[0].properties.find(p => p.key && p.key.name === 'length');
    const fn = args[1];
    return '[' + (fn ? bodyOf(fn) : 'None') + ' for _ in range(' + T(lenProp.value) + ')]';
  }
  if (m === 'from' && obj.type === 'Identifier' && obj.name === 'Array') {
    return 'list(' + T(args[0]) + ')';
  }
  if (m === 'isArray' && obj.type === 'Identifier' && obj.name === 'Array') {
    return 'isinstance(' + T(args[0]) + ', list)';
  }
  switch (m) {
    case 'map': return mapCall(obj, args[0]);
    case 'forEach': return forEachCall(obj, args[0]);
    case 'filter': return '[' + T(args[0].body) + ' for ' + paramOfNoDefault(args[0]) + ' in ' + O() + ']';
    case 'join': return A(0) + '.join(' + O() + ')';
    case 'split': {
      if (args.length === 0 || (args[0].type === 'Literal' && args[0].value === '')) {
        return 'list(' + O() + ')';
      }
      // "x".split(/ /) -> re.split(' ', "x"); JS split(regex) splits on pattern.
      if (args[0].type === 'Literal' && args[0].regex) {
        return 're.split(' + JSON.stringify(args[0].regex.pattern) + ', ' + O() + ')';
      }
      return O() + '.split(' + A(0) + ')';
    }
    case 'sort': return sortCall(obj, args[0]);
    case 'reduce': return reduceCall(obj, args);
    case 'includes': return A(0) + ' in ' + O();
    case 'indexOf': return '_indexof(' + O() + ', ' + A(0) + ')';
    case 'push': return O() + '.append(' + A(0) + ')';
    case 'pop': return O() + '.pop()';
    case 'slice': return O() + '[' + (A(0) || '') + (args.length > 1 ? ':' + A(1) : '') + ']';
    case 'substring':
    case 'substr': return O() + '[' + (A(0) || '') + (args.length > 1 ? ':' + A(1) : '') + ']';
    case 'concat': return O() + ' + ' + args.map(T).join(' + ');
    case 'toLowerCase': return O() + '.lower()';
    case 'toUpperCase': return O() + '.upper()';
    case 'trim': return O() + '.strip()';
    case 'startsWith': return O() + '.startswith(_jsstr(' + A(0) + '))';
    case 'endsWith': return O() + '.endswith(_jsstr(' + A(0) + '))';
    case 'flat': return '[item for sublist in ' + O() + ' for item in sublist]';
    case 'match': {
      // str.match(/re/g) -> re.findall(pattern, str); without /g -> re.search(...)
      if (args[0] && args[0].type === 'Literal' && args[0].regex) {
        const rx = args[0].regex;
        const pat = JSON.stringify(rx.pattern);
        if (rx.flags && rx.flags.includes('g')) return 're.findall(' + pat + ', ' + O() + ')';
        return 're.search(' + pat + ', ' + O() + ')';
      }
      return O() + '.match(' + A(0) + ')';
    }
    case 'charAt': return O() + '[' + A(0) + ']';
    case 'charCodeAt': return 'ord(' + O() + '[' + A(0) + '])';
    case 'replace': {
      // str.replace(/re/, x) -> re.sub(pattern, x, str, count=1); JS replaces
      // the first match only.  A string pattern keeps str.replace semantics.
      if (args[0] && args[0].type === 'Literal' && args[0].regex) {
        return 're.sub(' + JSON.stringify(args[0].regex.pattern) + ', ' + A(1) + ', ' + O() + ', count=1)';
      }
      return O() + '.replace(' + A(0) + ', ' + A(1) + ', 1)';
    }
    case 'replaceAll': {
      if (args[0] && args[0].type === 'Literal' && args[0].regex) {
        return 're.sub(' + JSON.stringify(args[0].regex.pattern) + ', ' + A(1) + ', ' + O() + ')';
      }
      return O() + '.replace(' + A(0) + ', ' + A(1) + ')';
    }
    case 'repeat': return O() + ' * ' + A(0);
    case 'keys': return 'list(' + O() + '.keys())';
    case 'values': return 'list(' + O() + '.values())';
    case 'find': {
      if (!isNode(args[0], 'ArrowFunctionExpression') && !isNode(args[0], 'FunctionExpression')) {
        return O() + '.find(' + args.map(T).join(', ') + ')';
      }
      // find returns the matching *element*, not the predicate result.
      return 'next((' + paramOfNoDefault(args[0]) + ' for ' + paramOfNoDefault(args[0]) + ' in ' + O() + ' if ' + bodyOf(args[0]) + '), None)';
    }
    case 'some': {
      if (!isNode(args[0], 'ArrowFunctionExpression') && !isNode(args[0], 'FunctionExpression')) {
        return O() + '.some(' + args.map(T).join(', ') + ')';
      }
      return 'any(' + bodyOf(args[0]) + ' for ' + paramOfNoDefault(args[0]) + ' in ' + O() + ')';
    }
    case 'every': {
      if (!isNode(args[0], 'ArrowFunctionExpression') && !isNode(args[0], 'FunctionExpression')) {
        return O() + '.every(' + args.map(T).join(', ') + ')';
      }
      return 'all(' + bodyOf(args[0]) + ' for ' + paramOfNoDefault(args[0]) + ' in ' + O() + ')';
    }
    case 'hasOwnProperty': return '_has_own(' + O() + ', ' + A(0) + ')';
    case 'toFixed': return 'format(' + O() + ', ".%df" % ' + A(0) + ')';
    case 'toString': return 'str(' + O() + ')';
    case 'test': return O() + '.search(' + A(0) + ') is not None';
    case 'exec': return O() + '.search(' + A(0) + ')';
    case 'add': return O() + '.add(' + A(0) + ')';
    case 'has': return A(0) + ' in ' + O();
    case 'delete': return 'del ' + O() + '[' + A(0) + ']';
    case 'get': return O() + '.get(' + A(0) + (args.length > 1 ? ', ' + A(1) : '') + ')';
    case 'set': return O() + '[' + A(0) + '] = ' + A(1);
    default:
      // JS camelCase method -> Python snake_case (idiomatic API).
      return O() + '.' + camelToSnake(m) + '(' + args.map(T).join(', ') + ')';
  }
}

function mapCall(obj, fn) {
  if (isNode(fn, 'ArrowFunctionExpression') && fn.body.type !== 'BlockStatement') {
    return '[' + T(fn.body) + ' for ' + paramOfNoDefault(fn) + ' in ' + T(obj) + ']';
  }
  return 'list(map(' + asFunc(fn) + ', ' + T(obj) + '))';
}

function forEachCall(obj, fn) {
  // Used as a statement; returns a for-loop string (handled in S()).
  return forEachStatement(obj, fn);
}

// obj.forEach(fn) as a statement => for <param> in <obj>:\n<body>
function forEachStatement(obj, fn, I) {
  const ind = I || '';
  let body;
  if (fn.body.type === 'BlockStatement') {
    body = fn.body.body.map(s => S(s, ind + '    ')).join('\n');
  } else {
    body = exprAsStatement(fn.body, ind + '    ');
  }
  // Destructuring param: forEach(({a, b}) => ...) => for __it in obj: a = __it.a; ...
  const p = fn.params && fn.params[0];
  if (p && p.type === 'ObjectPattern') {
    const unpack = p.properties.map(pr => {
      const key = id(pr.key) || id(pr.value);
      return ind + '    ' + key + ' = __it[' + pyStr(key) + ']';
    }).join('\n');
    return ind + 'for __it in ' + T(obj) + ':\n' + unpack + '\n' + body;
  }
  if (p && p.type === 'ArrayPattern') {
    const names = p.elements.map(e => e ? T(e) : '_').join(', ');
    return ind + 'for ' + names + ' in ' + T(obj) + ':\n' + body;
  }
  // forEach((element, index) => ...) => for <index>, <element> in enumerate(obj):
  if (fn.params && fn.params.length === 2) {
    const el = mapName(id(fn.params[0])) || T(fn.params[0]);
    const ix = mapName(id(fn.params[1])) || T(fn.params[1]);
    return ind + 'for ' + ix + ', ' + el + ' in enumerate(' + T(obj) + '):\n' + (body || ind + '    pass');
  }
  return ind + 'for ' + paramOfNoDefault(fn) + ' in ' + T(obj) + ':\n' + (body || ind + '    pass');
}

// An expression used as a statement (arrow body, etc.), emitted with correct indent.
function exprAsStatement(b, ind) {
  if ((b.type === 'CallExpression' || b.type === 'MemberExpression') && chainHasExpect(b)) {
    return translateExpect(b, ind);
  }
  if (b.type === 'CallExpression' && b.callee.type === 'MemberExpression' &&
      b.callee.property.name === 'forEach') {
    return forEachStatement(b.callee.object, b.arguments[0], ind);
  }
  return ind + T(b);
}

function sortCall(obj, cmp) {
  if (!cmp) return 'sorted(' + T(obj) + ')';
  // (a,b)=>a-b  => numeric sort
  if (isNode(cmp, 'ArrowFunctionExpression') && cmp.body.type === 'BinaryExpression' && cmp.body.operator === '-') {
    return 'sorted(' + T(obj) + ')';
  }
  return 'sorted(' + T(obj) + ', key=cmp_to_key(' + asFunc(cmp) + '))';
}

function reduceCall(obj, args) {
  const fn = args[0], init = args[1];
  // `sum(obj)` shortcut is only valid when the body is exactly `acc + item`
  // (both operands are the reduce params). If either side is a member access
  // (e.g. (s, p) => s + p.prob), it must fall through to functools.reduce.
  if (isNode(fn, 'ArrowFunctionExpression') && fn.body.type === 'BinaryExpression' && fn.body.operator === '+') {
    const names = (fn.params || []).map(p => id(p));
    const l = fn.body.left, r = fn.body.right;
    const isParam = (n) => n.type === 'Identifier' && names.includes(n.name);
    if (isParam(l) && isParam(r)) {
      return 'sum(' + T(obj) + (init ? ', start=' + T(init) : '') + ')';
    }
  }
  return 'functools.reduce(' + asFunc(fn) + ', ' + T(obj) + (init ? ', ' + T(init) : '') + ')';
}

function paramOf(fn) {
  if (!fn) return '*args';
  if (fn.params && fn.params.length) {
    // JS functions accept fewer args than declared (missing -> undefined) AND
    // ignore extra args. Mirror both: give simple identifier params a None
    // default and append *args so extra call-site args are absorbed. (If any
    // param is a pattern, leave all as-is to avoid "non-default after default".)
    const allIdent = fn.params.every(p => p.type === 'Identifier');
    const base = allIdent
      ? fn.params.map(p => mapName(id(p)) + '=None').join(', ')
      : fn.params.map(p => mapName(id(p)) || T(p)).join(', ');
    return base + ', *args';
  }
  return '*args';
}

// For list comprehensions / for-of / forEach the loop variable must NOT carry a
// default (Python forbids `x=None` in a comprehension target).
function paramOfNoDefault(fn) {
  if (!fn) return '_';
  if (fn.params && fn.params.length) return fn.params.map(p => mapName(id(p)) || T(p)).join(', ');
  return '_';
}
function bodyOf(fn) {
  if (!fn) return 'None';
  if (fn.body.type !== 'BlockStatement') return T(fn.body);
  // single-return block
  const r = fn.body.body.find(s => s.type === 'ReturnStatement');
  return r ? T(r.argument) : 'None';
}
function blockOf(fn) {
  if (!fn) return '';
  if (fn.body.type !== 'BlockStatement') {
    const b = fn.body;
    // An expect chain in expression position is a statement, not a return value.
    if ((b.type === 'CallExpression' || b.type === 'MemberExpression') && chainHasExpect(b)) {
      return translateExpect(b, '');
    }
    if (b.type === 'AssignmentExpression' || b.type === 'UpdateExpression' ||
        (b.type === 'CallExpression' && b.callee.type === 'MemberExpression' &&
         ['push', 'add', 'set', 'delete', 'pop'].includes(b.callee.property.name))) {
      return T(b);
    }
    return 'return ' + T(b);
  }
  return fn.body.body.map(s => S(s, '')).join('\n');
}

// A function value used in expression position. Multi-statement bodies can't be
// lambdas in Python, so they are hoisted to a named def and referenced by name.
let HOIST = [];
let HOIST_N = 0;
let MODULE_FNS = [];
let MODULE_VARS = [];
let MODULE_HOOKS = [];
// Names of hoisted helpers that pytest would mis-collect (start with 'test');
// mapped to a safe name, applied consistently via mapIdent.
const RENAME = {};
// Test method names used in the current class, to avoid duplicate defs
// (mocha allows duplicate it() descriptions; Python would silently shadow).
let USED_NAMES = new Set();
// Set while translating the body of an inlined throw-assertion, where a JS
// `return` has no enclosing function and must not become a Python return.
let STRIP_RETURN = false;

function functionExpr(node) {
  if (node.body.type !== 'BlockStatement') {
    return 'lambda ' + paramOf(node) + ': ' + T(node.body);
  }
  const stmts = node.body.body;
  if (stmts.length === 1 && stmts[0].type === 'ReturnStatement') {
    return 'lambda ' + paramOf(node) + ': ' + T(stmts[0].argument);
  }
  const name = '_fn_' + (++HOIST_N);
  const prevStrip = STRIP_RETURN;
  STRIP_RETURN = false;
  let body;
  try {
    body = bodyBlock(node.body, '');
  } finally {
    STRIP_RETURN = prevStrip;
  }
  HOIST.push('def ' + name + '(' + paramOf(node) + '):\n' + body);
  return name;
}

function asFunc(fn) {
  if (!fn) return 'None';
  if (isNode(fn, 'ArrowFunctionExpression') && fn.body.type !== 'BlockStatement') {
    return 'lambda ' + paramOf(fn) + ': ' + T(fn.body);
  }
  // Block body: multi-statement bodies (e.g. `s => { let t = ...; return t }`)
  // can't be a lambda — delegate to functionExpr, which hoists them to a def.
  if (fn.body && fn.body.type === 'BlockStatement') {
    const stmts = fn.body.body;
    if (stmts.length === 1 && stmts[0].type === 'ReturnStatement') {
      return 'lambda ' + paramOf(fn) + ': ' + T(stmts[0].argument);
    }
    return functionExpr(fn);
  }
  return 'lambda ' + paramOf(fn) + ': ' + bodyOf(fn);
}

function binary(node) {
  const opMap = { '===': '==', '!==': '!=', '==': '==', '!=': '!=', '>': '>', '<': '<', '>=': '>=', '<=': '<=', '+': '+', '-': '-', '*': '*', '/': '/', '%': '%', '&': '&', '|': '|', '^': '^', '<<': '<<', '>>': '>>' };
  let op = opMap[node.operator] || node.operator;
  let left = T(node.left), right = T(node.right);
  if (node.operator === 'in') return paren(left) + ' in ' + paren(right);
  if (node.operator === 'instanceof') return 'isinstance(' + left + ', ' + right + ')';
  if (node.operator === '+' && (isStringish(node.left) || isStringish(node.right))) {
    return '_jsstr(' + left + ') + _jsstr(' + right + ')';
  }
  return paren(left) + ' ' + op + ' ' + paren(right);
}

function isStringish(node) {
  if (node.type === 'Literal') return typeof node.value === 'string';
  if (node.type === 'TemplateLiteral') return true;
  return node.type === 'BinaryExpression' && node.operator === '+' &&
    (isStringish(node.left) || isStringish(node.right));
}

// ---------------------------------------------------------------------------
// Statement translation
// ---------------------------------------------------------------------------

function S(node, ind) {
  const I = ind || '';
  if (!node) return I + 'pass';
  switch (node.type) {
    case 'ExpressionStatement': {
      const e = node.expression;
      // x++ / ++x / x-- / --x as a statement must assign, not just compute.
      if (e.type === 'UpdateExpression') {
        const v = T(e.argument);
        const op = e.operator === '++' ? ' += 1' : ' -= 1';
        return I + v + op;
      }
      // mocha this.timeout()/this.slow() are ignored; this.skip() -> pytest.skip()
      if (e.type === 'CallExpression' && e.callee.type === 'MemberExpression' &&
          e.callee.object.type === 'ThisExpression') {
        const m = e.callee.property.name;
        if (m === 'timeout' || m === 'slow') return I + '# mocha this.' + m + ' — ignored\n' + I + 'pass';
        if (m === 'skip') return I + 'pytest.skip("mocha this.skip")';
      }
      return exprStatement(e, I);
    }
    case 'VariableDeclaration':
      return node.declarations.map(d => varDecl(d, I)).join('\n');
    case 'BlockStatement':
      return node.body.map(s => S(s, I + '    ')).join('\n') || I + 'pass';
    case 'IfStatement':
      return ifStatement(node, I);
    case 'ForStatement':
      return forStatement(node, I);
    case 'ForOfStatement': {
      const pattern = node.left.type === 'VariableDeclaration' ? node.left.declarations[0].id : node.left;
      if (pattern && pattern.type === 'ObjectPattern') {
        const assigns = pattern.properties.map(p => {
          const k = id(p.key), v = id(p.value) || k;
          return I + '    ' + v + ' = __it[' + JSON.stringify(k) + ']\n';
        }).join('');
        return I + 'for __it in ' + T(node.right) + ':\n' + assigns + bodyBlock(node.body, I);
      }
      const lhs = node.left.type === 'VariableDeclaration' ? id(node.left.declarations[0].id) : T(node.left);
      return I + 'for ' + lhs + ' in ' + T(node.right) + ':\n' + bodyBlock(node.body, I);
    }
    case 'ReturnStatement':
      // Inside an inlined throw-assertion body there is no function to return
      // from; evaluating the expression is what matters (and returning would
      // trip pytest's PytestReturnNotNoneWarning).
      if (STRIP_RETURN) {
        if (!node.argument) return I + 'pass';
        const v = T(node.argument);
        return I + (isCallLike(node.argument) ? v : '_ = ' + v);
      }
      return node.argument ? I + 'return ' + T(node.argument) : I + 'return';
    case 'ThrowStatement':
      return I + 'raise Exception(' + T(node.argument) + ')';
    case 'TryStatement':
      return tryStatement(node, I);
    case 'FunctionDeclaration':
      return I + 'def ' + (RENAME[id(node.id)] || mapName(id(node.id))) + '(' + (node.params && node.params.length ? paramOf(node) : '') + '):\n' + bodyBlock(node.body, I);
    case 'WhileStatement':
      return I + 'while ' + T(node.test) + ':\n' + bodyBlock(node.body, I);

    case 'BreakStatement':
      return I + 'break';
    case 'ContinueStatement':
      return I + 'continue';
    case 'EmptyStatement':
      return '';
    case 'SwitchStatement':
      return switchStatement(node, I);
    default:
      return I + '# UNTRANSLATED ' + node.type + '\n' + I + 'pass';
  }
}

function bodyBlock(block, I) {
  if (block.type === 'BlockStatement') {
    const inner = block.body.map(s => S(s, I + '    ')).join('\n');
    return inner || I + '    pass';
  }
  return S(block, I + '    ');
}

function varDecl(d, I) {
  // Destructuring declarations.
  if (d.id.type === 'ArrayPattern') {
    const els = d.id.elements.map(e => e ? T(e) : '_');
    // Trailing star absorbs extra elements (JS arrays may be longer than the pattern).
    if (!d.id.elements[d.id.elements.length - 1] ||
        d.id.elements[d.id.elements.length - 1].type !== 'RestElement') {
      els.push('*_');
    }
    return I + els.join(', ') + ' = ' + T(d.init);
  }
  if (d.id.type === 'ObjectPattern') {
    // const { A, B } = obj  =>  A = obj.A; B = obj.B
    const src = T(d.init);
    return d.id.properties.map(p => {
      const key = id(p.key) || id(p.value);
      return I + key + ' = ' + src + '.' + key;
    }).join('\n');
  }
  const name = d.id.type === 'Identifier' ? shadowName(d.id.name) : T(d.id);
  if (!d.init) return I + name + ' = None';
  // JS object literals are read both as maps (d['k']) and objects (d.k). Wrap the
  // initializer in JsDict so attribute access works; it is still a dict subclass
  // so `== {...}` equality assertions and json.dumps keep working.
  if (d.init.type === 'ObjectExpression') {
    return I + name + ' = JsDict(' + T(d.init) + ')';
  }
  if (isNode(d.init, 'FunctionExpression') || isNode(d.init, 'ArrowFunctionExpression')) {
    const fn = d.init;
    if (fn.body.type === 'BlockStatement') {
      return I + 'def ' + name + '(' + paramOf(fn) + '):\n' + bodyBlock(fn.body, I);
    }
    return I + name + ' = lambda ' + paramOf(fn) + ': ' + T(fn.body);
  }
  return I + name + ' = ' + T(d.init);
}

function ifStatement(node, I) {
  let out = I + 'if ' + T(node.test) + ':\n' + bodyBlock(node.consequent, I);
  let alt = node.alternate;
  while (alt) {
    if (alt.type === 'IfStatement') {
      out += '\n' + I + 'elif ' + T(alt.test) + ':\n' + bodyBlock(alt.consequent, I);
      alt = alt.alternate;
    } else {
      out += '\n' + I + 'else:\n' + bodyBlock(alt, I);
      alt = null;
    }
  }
  return out;
}

function forStatement(node, I) {
  // C-style: for (let i=0; i<N; i++)  =>  for i in range(N)
  if (node.init && node.test && node.update) {
    const initLines = node.init.type === 'VariableDeclaration'
      ? node.init.declarations.map(d => varDecl(d, I)).join('\n')
      : I + S(node.init, '').trim();
    const loopVar = node.init.type === 'VariableDeclaration' ? id(node.init.declarations[0].id) : null;
    const rng = rangeExpr(node.test, loopVar, node.init, node.update);
    if (rng) {
      return initLines + '\n' + I + 'for ' + (loopVar || '_') + ' in ' + rng + ':\n' + bodyBlock(node.body, I);
    }
    // fall back to while
    return initLines + '\n' + I + 'while ' + T(node.test) + ':\n' + bodyBlock(node.body, I) + '\n' + I + '    ' + T(node.update);
  }
  if (node.test) return I + 'while ' + T(node.test) + ':\n' + bodyBlock(node.body, I);
  return I + 'while True:\n' + bodyBlock(node.body, I);
}

function rangeExpr(test, loopVar, init, update) {
  if (test.type === 'BinaryExpression' && (test.operator === '<' || test.operator === '<=')) {
    const right = T(test.right);
    const start = init.type === 'VariableDeclaration' &&
      init.declarations[0].init ? T(init.declarations[0].init) : '0';
    let step;
    if (update.type === 'UpdateExpression' && update.argument.type === 'Identifier' &&
        id(update.argument) === loopVar) {
      step = update.operator === '++' ? '1' : '-1';
    } else if (update.type === 'AssignmentExpression' &&
        update.left.type === 'Identifier' && id(update.left) === loopVar &&
        update.operator === '+=') {
      step = T(update.right);
    } else {
      return null;
    }
    const stop = test.operator === '<=' ? right + ' + 1' : right;
    return 'range(' + start + ', ' + stop + ', ' + step + ')';
  }
  return null;
}

function tryStatement(node, I) {
  let out = I + 'try:\n' + bodyBlock(node.block, I);
  if (node.handler) {
    const name = node.handler.param ? id(node.handler.param) : 'e';
    out += '\n' + I + 'except Exception as ' + name + ':\n' + bodyBlock(node.handler.body, I);
  }
  if (node.finalizer) out += '\n' + I + 'finally:\n' + bodyBlock(node.finalizer, I);
  return out;
}

function switchStatement(node, I) {
  let out = I + 'match ' + T(node.discriminant) + ':\n';
  for (const c of node.cases) {
    if (c.test) out += I + '    case ' + T(c.test) + ':\n';
    else out += I + '    case _:\n';
    const body = c.consequent.filter(s => s.type !== 'BreakStatement');
    out += (body.map(s => S(s, I + '        ')).join('\n') || I + '        pass') + '\n';
  }
  return out;
}

// Expression used as a statement: detect describe/it/forEach/assertion.
function exprStatement(expr, I) {
  if (expr.type === 'CallExpression') {
    const name = id(expr.callee);
    if (name === 'describe') return describeCall(expr, I);
    if (name === 'it') return itCall(expr, I);
    if (name === 'expect') return assertion(expr, I);
    // mocha hooks: before/beforeEach/after/afterEach(fn) — run the body inline.
    if (['before', 'beforeEach', 'after', 'afterEach'].includes(name)) {
      const fn = expr.arguments[0];
      const body = fn && fn.body ? (fn.body.type === 'BlockStatement' ? fn.body.body.map(s => S(s, I)).join('\n') : I + T(fn.body)) : I + 'pass';
      return I + '# mocha ' + name + ' hook\n' + body;
    }
    // it.skip(...) — disabled test
    if (expr.callee.type === 'MemberExpression' && id(expr.callee.object) === 'it' &&
        expr.callee.property.name === 'skip') {
      const nm = strLit(expr.arguments[0]) || 'skipped';
      const mname = uniqueName('test_' + nm.replace(/[^A-Za-z0-9]+/g, '_').replace(/^_+|_+$/g, '').toLowerCase());
      return I + '@pytest.mark.skip(reason="it.skip in JS")\n' + I + 'def ' + mname + '(self):\n' + I + '    pass';
    }
    // it(...).timeout(n) / .slow(n) — the chain is a MemberExpression callee.
    if (expr.callee.type === 'MemberExpression' && expr.callee.object.type === 'CallExpression' &&
        id(expr.callee.object.callee) === 'it') {
      return itCall(expr.callee.object, I) + '\n' + I + '# mocha .' + expr.callee.property.name + '(' + expr.arguments.map(T).join(', ') + ')';
    }
    // forEach as statement
    if (expr.callee.type === 'MemberExpression' && expr.callee.property.name === 'forEach') {
      return forEachStatement(expr.callee.object, expr.arguments[0], I);
    }
    return I + T(expr);
  }
  // Plain assignment as a statement: keep `x = y` (not a walrus).
  if (expr.type === 'AssignmentExpression' && expr.left.type === 'Identifier') {
    const op = expr.operator === '=' ? '=' : expr.operator;
    const target = refName(expr.left.name);
    if (op === '=') return I + target + ' = ' + T(expr.right);
    return I + target + ' ' + op + ' ' + T(expr.right);
  }
  // 0 && it(...) — disabled in JS
  if (expr.type === 'LogicalExpression' && expr.operator === '&&' &&
      expr.right.type === 'CallExpression' && id(expr.right.callee) === 'it') {
    const lit = expr.left;
    if (lit.type === 'Literal' && !lit.value) {
      return I + '@pytest.mark.skip(reason="disabled in JS")  # /*LTR*/\n' + itCall(expr.right, I);
    }
  }
  return I + T(expr);
}

function indentBody(body, I) {
  return body.split('\n').map(l => (l.trim() ? I + '    ' + l.trim() : '')).join('\n');
}

// describe('X', () => { its })  =>  class TestX:
function describeCall(expr, I) {
  const name = strLit(expr.arguments[0]) || 'Suite';
  const fn = expr.arguments[1];
  const cls = 'Test' + name.replace(/[^A-Za-z0-9]/g, '');
  USED_NAMES = new Set();
  // Pre-scan for hoisted helpers so calls that appear before the declaration
  // (JS hoists them) get the renamed reference.
  if (fn && fn.body && fn.body.type === 'BlockStatement') {
    for (const s of fn.body.body) {
      if (s.type === 'FunctionDeclaration') {
        const nm = id(s.id);
        if (/^test/.test(nm)) RENAME[nm] = '_' + nm;
      }
    }
  }
  let body = '';
  if (fn && fn.body && fn.body.type === 'BlockStatement') {
    body = fn.body.body.map(s => describeOrIt(s, '    ')).join('\n');
  }
  return I + 'class ' + cls + ':\n' + (body || I + '    pass');
}

// Function declarations inside a describe body are hoisted to JS describe scope;
// in Python they must be module-level defs (a class method would break plain calls).
function describeOrIt(node, I) {
  if (node.type === 'FunctionDeclaration') {
    const nm = id(node.id);
    if (/^test/.test(nm)) RENAME[nm] = '_' + nm;
    MODULE_FNS.push(S(node, ''));
    return I + '# (helper hoisted to module scope)';
  }
  // describe-scope `let/const` are shared across all it() blocks in JS; in
  // Python each it() is a separate method, so hoist them to module scope.
  if (node.type === 'VariableDeclaration') {
    const decl = S(node, '');
    MODULE_VARS.push(decl);
    return I + '# (var hoisted to module scope)';
  }
  if (node.type === 'ExpressionStatement') {
    const e = node.expression;
    if (e.type === 'CallExpression') {
      const name = id(e.callee);
      if (name === 'it') return itCall(e, I);
      if (name === 'describe') return describeCall(e, I);
      // Suite-level mocha hooks run before any test; in JS their assignments are
      // visible to every it() (describe scope). In Python a class-body statement is
      // NOT visible to methods, so hoist the hook body to module scope.
      if (['before', 'beforeEach', 'after', 'afterEach'].includes(name)) {
        const fn = e.arguments[0];
        const body = fn && fn.body ? (fn.body.type === 'BlockStatement' ? fn.body.body.map(s => S(s, '')).join('\n') : T(fn.body)) : 'pass';
        MODULE_HOOKS.push('# mocha ' + name + ' hook\n' + body);
        return I + '# (mocha ' + name + ' hook hoisted to module scope)';
      }
      if (e.callee.type === 'MemberExpression' && e.callee.object.type === 'CallExpression' &&
          id(e.callee.object.callee) === 'it') return exprStatement(e, I);
    }
  }
  return S(node, I);
}

function uniqueName(base) {
  let n = base;
  let i = 2;
  while (USED_NAMES.has(n)) { n = base + '_' + i; i++; }
  USED_NAMES.add(n);
  return n;
}

function itCall(expr, I) {
  const name = strLit(expr.arguments[0]) || 'test';
  const fn = expr.arguments[1];
  const mname = uniqueName('test_' + name.replace(/[^A-Za-z0-9]+/g, '_').replace(/^_+|_+$/g, '').toLowerCase());
  const prevShadows = SHADOWS;
  SHADOWS = new Set();
  let body = '';
  if (fn && fn.body) {
    if (fn.body.type === 'BlockStatement') {
      body = fn.body.body.map(s => S(s, '        ')).join('\n');
    } else {
      body = '        ' + T(fn.body);
    }
  }
  return I + 'def ' + mname + '(self):\n' + (body || '        pass');
}

// ---------------------------------------------------------------------------
// chai assertion translation
// ---------------------------------------------------------------------------

function assertion(expectCall, I) {
  const subject = expectCall.arguments[0];
  const msg = expectCall.arguments[1];
  const msgStr = msg ? ', ' + T(msg) : '';
  // Walk the chain: expect(x).to.be.deep.equal(y)
  let chain = [];
  let cur = expectCall;
  // expectCall is the base; the chain is built by callers wrapping it.
  // We rely on the caller having passed the full member chain via `fullChain`.
  return I + '# assertion base\n' + I + 'assert ' + T(subject) + msgStr;
}

// The real entry: given the outermost expression of an expect chain, translate.
function translateExpect(node, I) {
  const { base, parts } = flattenChain(node);
  const subject = base.arguments[0];
  const msg = base.arguments[1];
  const msgStr = msg ? ', ' + T(msg) : '';
  return emitAssertion(subject, parts, msgStr, I);
}

function flattenChain(node) {
  const parts = [];
  let cur = node;
  while (cur) {
    if (cur.type === 'CallExpression' && cur.callee.type === 'MemberExpression') {
      parts.push({ name: cur.callee.property.name, args: cur.arguments });
      cur = cur.callee.object;
    } else if (cur.type === 'MemberExpression') {
      parts.push({ name: cur.property.name, args: null });
      cur = cur.object;
    } else if (cur.type === 'CallExpression' && id(cur.callee) === 'expect') {
      return { base: cur, parts: parts.reverse() };
    } else {
      break;
    }
  }
  return { base: node, parts: [] };
}

const NOISE = new Set(['to', 'be', 'been', 'is', 'that', 'which', 'and', 'has', 'have', 'with', 'of', 'at', 'a', 'an', 'the', 'then', 'once', 'but', 'does', 'still', 'itself', 'deep']);

function emitAssertion(subject, parts, msgStr, I) {
  const names = parts.map(p => p.name);
  const argsOf = (n) => { const p = parts.find(p => p.name === n); return p && p.args ? p.args : []; };
  const neg = names.includes('not');
  const lengthMode = names.includes('length') && !argsOf('length').length;
  const subj = lengthMode ? 'len(' + T(subject) + ')' : T(subject);

  // A length comparison that follows a bare `.length` (e.g. ...have.length.above(0)).
  // Returns a comparison expression against `len(subject)`, or null if none.
  const lengthCmp = (subjExpr) => {
    if (names.includes('above') || names.includes('greaterThan') || names.includes('gt')) {
      const n = names.includes('above') ? 'above' : names.includes('gt') ? 'gt' : 'greaterThan';
      return subjExpr + ' > ' + T(argsOf(n)[0]);
    }
    if (names.includes('below') || names.includes('lessThan') || names.includes('lt')) {
      const n = names.includes('below') ? 'below' : names.includes('lt') ? 'lt' : 'lessThan';
      return subjExpr + ' < ' + T(argsOf(n)[0]);
    }
    if (names.includes('least') || names.includes('atLeast')) {
      const n = names.includes('least') ? 'least' : 'atLeast';
      return subjExpr + ' >= ' + T(argsOf(n)[0]);
    }
    if (names.includes('most') || names.includes('atMost')) {
      const n = names.includes('most') ? 'most' : 'atMost';
      return subjExpr + ' <= ' + T(argsOf(n)[0]);
    }
    if (names.includes('equal') || names.includes('equals') || names.includes('eq') || names.includes('eql')) {
      const n = names.find(n => ['equal', 'equals', 'eq', 'eql'].includes(n));
      return subjExpr + ' == ' + T(argsOf(n)[0]);
    }
    return null;
  };

  const wrap = (cond) => {
    const c = neg ? 'not (' + cond + ')' : '(' + cond + ')';
    return I + 'assert ' + c + msgStr;
  };

  // throw: subject is a function/arrow; inline its body under pytest.raises.
  // `.to.not.throw()` must run the body WITHOUT expecting an exception.
  if (names.includes('throw') || names.includes('throws')) {
    const p = parts.find(p => p.name === 'throw' || p.name === 'throws');
    const matchArg = p.args && p.args[0] ? ', match=' + T(p.args[0]) : '';
    const body = functionBody(subject);
    const indented = body.split('\n').map(l => (l.trim() ? I + '    ' + l.trim() : '')).join('\n');
    if (neg) {
      return I + 'try:\n' + indented + '\n' + I + 'except Exception as _e:\n' + I + '    raise AssertionError("expected no throw, got: " + str(_e))' + msgStr;
    }
    return I + 'with pytest.raises(Exception' + matchArg + '):\n' + indented;
  }

  if (names.includes('instanceof') || names.includes('instanceOf')) {
    const t = argsOf('instanceof')[0] || argsOf('instanceOf')[0];
    return wrap('isinstance(' + subj + ', ' + T(t) + ')');
  }
  if (names.includes('a') || names.includes('an')) {
    const p = parts.find(p => p.name === 'a' || p.name === 'an');
    if (p && p.args && p.args[0] && p.args[0].type === 'Literal') {
      const tmap = { string: 'str', number: '(int, float)', boolean: 'bool', array: 'list', object: 'dict', function: 'types.FunctionType', undefined: 'type(None)' };
      const t = tmap[p.args[0].value] || 'object';
      // Chained type + length check, e.g. .to.be.a('string').and.have.length.above(0).
      if (lengthMode) {
        const lc = lengthCmp('len(' + T(subject) + ')');
        if (lc) return wrap('isinstance(' + T(subject) + ', ' + t + ') and ' + lc);
      }
      return wrap('isinstance(' + subj + ', ' + t + ')');
    }
  }
  if (names.includes('satisfy')) {
    const pred = T(argsOf('satisfy')[0]);
    return wrap('(' + pred + ')(' + subj + ')');
  }
  if (names.includes('oneOf')) {
    return wrap(T(subject) + ' in ' + T(argsOf('oneOf')[0]));
  }
  if (names.includes('members')) {
    const subset = names.includes('include') || names.includes('includes') || names.includes('contain');
    if (subset) return wrap('set(' + T(argsOf('members')[0]) + ') <= set(' + subj + ')');
    return wrap('set(' + subj + ') == set(' + T(argsOf('members')[0]) + ')');
  }
  if (names.includes('include') || names.includes('includes') || names.includes('contain') || names.includes('contains')) {
    const n = names.find(n => ['include', 'includes', 'contain', 'contains'].includes(n));
    const p = parts.find(p => p.name === n);
    return wrap(T(p.args[0]) + ' in ' + subj);
  }
  if (names.includes('match')) {
    return wrap(T(argsOf('match')[0]) + '.search(' + subj + ') is not None');
  }
  if (names.includes('above') || names.includes('greaterThan') || names.includes('gt')) {
    const n = names.includes('above') ? 'above' : names.includes('gt') ? 'gt' : 'greaterThan';
    return wrap(subj + ' > ' + T(argsOf(n)[0]));
  }
  if (names.includes('below') || names.includes('lessThan') || names.includes('lt')) {
    const n = names.includes('below') ? 'below' : names.includes('lt') ? 'lt' : 'lessThan';
    return wrap(subj + ' < ' + T(argsOf(n)[0]));
  }
  if (names.includes('least') || names.includes('atLeast')) {
    const n = names.includes('least') ? 'least' : 'atLeast';
    return wrap(subj + ' >= ' + T(argsOf(n)[0]));
  }
  if (names.includes('most') || names.includes('atMost')) {
    const n = names.includes('most') ? 'most' : 'atMost';
    return wrap(subj + ' <= ' + T(argsOf(n)[0]));
  }
  if (names.includes('within')) {
    const [lo, hi] = argsOf('within');
    return wrap(T(lo) + ' <= ' + subj + ' <= ' + T(hi));
  }
  if (names.includes('closeTo')) {
    const [v, d] = argsOf('closeTo');
    return wrap('abs(' + subj + ' - ' + T(v) + ') <= ' + T(d));
  }
  if (names.includes('lengthOf')) {
    return wrap('len(' + T(subject) + ') == ' + T(argsOf('lengthOf')[0]));
  }
  if (names.includes('equal') || names.includes('equals') || names.includes('eq') || names.includes('eql') || names.includes('deepEqual')) {
    const n = names.find(n => ['equal', 'equals', 'eq', 'eql', 'deepEqual'].includes(n));
    const p = parts.find(p => p.name === n);
    return wrap(subj + ' == ' + T(p.args[0]));
  }
  if (names.includes('true')) return wrap('(' + subj + ') is True');
  if (names.includes('false')) return wrap('(' + subj + ') is False');
  if (names.includes('null')) return wrap('(' + subj + ') is None');
  if (names.includes('undefined')) return wrap('(' + subj + ') is None');
  if (names.includes('ok')) return wrap('(' + subj + ')');
  if (names.includes('empty')) return wrap('len(' + subj + ') == 0');
  if (names.includes('NaN')) return wrap('isinstance(' + subj + ', float) and ' + subj + ' != ' + subj);
  if (names.includes('property') || names.includes('ownProperty')) {
    const n = names.includes('property') ? 'property' : 'ownProperty';
    return wrap('_hasprop(' + subj + ', ' + T(argsOf(n)[0]) + ')');
  }
  if (names.includes('keys')) {
    return wrap('set(' + T(argsOf('keys')[0]) + ') <= set(' + subj + '.keys())');
  }
  // bare expect(x) truthiness
  if (names.filter(n => !NOISE.has(n)).length === 0) return wrap(subj);

  return I + 'raise NotImplementedError("untranslated chai: ' + names.filter(n => !NOISE.has(n)).join('.') + '")';
}

function functionBody(fn) {
  if (!fn) return 'pass';
  if (fn.type === 'ArrowFunctionExpression' || fn.type === 'FunctionExpression') {
    const prev = STRIP_RETURN;
    STRIP_RETURN = true;
    let out;
    try {
      if (fn.body.type !== 'BlockStatement') return T(fn.body);
      out = fn.body.body.map(s => S(s, '')).join('\n');
    } finally {
      STRIP_RETURN = prev;
    }
    return out;
  }
  return T(fn);
}

function isCallLike(node) {
  return node && (node.type === 'CallExpression' || node.type === 'NewExpression' ||
    node.type === 'AwaitExpression' || node.type === 'YieldExpression' ||
    node.type === 'UpdateExpression');
}

// Override exprStatement's expect handling to use translateExpect.
const _origExprStatement = exprStatement;
exprStatement = function (expr, I) {
  if (expr.type === 'CallExpression' && id(expr.callee) === 'expect') {
    return translateExpect(expr, I);
  }
  if (expr.type === 'CallExpression' && expr.callee.type === 'MemberExpression') {
    // could be expect(...).to... chain rooted differently — handled below
  }
  return _origExprStatement(expr, I);
};

// The chain root is `expect(...)` wrapped in member/call expressions, so the
// ExpressionStatement.expression is the outermost node, not the expect call.
// Re-route: if expression is a member/call chain that contains expect, use translateExpect.
const _origS = S;
S = function (node, ind) {
  if (node && node.type === 'ExpressionStatement') {
    const e = node.expression;
    if (e && (e.type === 'CallExpression' || e.type === 'MemberExpression') && chainHasExpect(e)) {
      return translateExpect(e, ind || '');
    }
  }
  return _origS(node, ind);
};

function chainHasExpect(node) {
  let cur = node;
  while (cur) {
    if (cur.type === 'CallExpression' && id(cur.callee) === 'expect') return true;
    if (cur.type === 'CallExpression' && cur.callee && cur.callee.type === 'MemberExpression') cur = cur.callee.object;
    else if (cur.type === 'MemberExpression') cur = cur.object;
    else break;
  }
  return false;
}

// ---------------------------------------------------------------------------
// File driver
// ---------------------------------------------------------------------------

function transpile(file) {
  HOIST = [];
  HOIST_N = 0;
  MODULE_FNS = [];
  MODULE_VARS = [];
  MODULE_HOOKS = [];
  for (const k of Object.keys(RENAME)) delete RENAME[k];
  const src = fs.readFileSync(path.join(JS_TEST_DIR, file), 'utf8');
  const ast = acorn.parse(src, { ecmaVersion: 'latest', sourceType: 'module', locations: true });

  const header = [
    '# AUTO-GENERATED from js/test/' + file + ' by scripts/js-to-py-tests.js — do not edit by hand.',
    '# Mirrors the JS suite 1:1 (describe/it/expect).',
    'import json',
    'import math',
    'import os',
    'import re',
    'import time',
    'import types',
    'import functools',
    'from functools import cmp_to_key',
    'import pytest',
    '',
    '_JS_TEST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "js", "test")',
    '',
    'from rita import RiTa',
    'from rita.util import JsDict',
    '',
    '# --- JS compatibility shims -------------------------------------------',
    'console = type("console", (), {"log": staticmethod(print), "warn": staticmethod(print), "error": staticmethod(print)})',
    'obj = type("obj", (), {"keys": staticmethod(lambda d: list(d.keys())), "values": staticmethod(lambda d: list(d.values()))})',
    'arr = type("arr", (), {"isArray": staticmethod(lambda x: isinstance(x, list)), "from": staticmethod(_arr_from)}) if False else None',
    'def _arr_from(x, fn=None):',
    '    if isinstance(x, dict) and "length" in x:',
    '        return [fn() if fn else None for _ in range(x["length"])]',
    '    return list(x)',
    'arr = type("arr", (), {"isArray": staticmethod(lambda x: isinstance(x, list)), "from": staticmethod(_arr_from)})',
    'def _typeof(fn):',
    '    try: x = fn()',
    '    except NameError: return "undefined"',
    '    except AttributeError: return "undefined"',
    '    if x is None: return "undefined"',
    '    if isinstance(x, bool): return "boolean"',
    '    if isinstance(x, str): return "string"',
    '    if isinstance(x, (int, float)): return "number"',
    '    if callable(x): return "function"',
    '    return "object"',
    'def _indexof(a, x):',
    '    try: return a.index(x)',
    '    except ValueError: return -1',
    'def _re_compile(p):',
    '    return re.compile(p)',
    'def readFileSync(p):',
    '    return open(p).read()',
    'def existsSync(p):',
    '    return os.path.exists(p)',
    'def _is_integer(x):',
    '    return isinstance(x, int) and not isinstance(x, bool)',
    'def _is_finite(x):',
    '    return isinstance(x, (int, float)) and x == x and x not in (float("inf"), float("-inf"))',
    'def _is_nan(x):',
    '    return isinstance(x, float) and x != x',
    'def _url(rel):',
    '    if rel.startswith("./"):',
    '        rel = rel[2:]',
    '    return os.path.normpath(os.path.join(_JS_TEST_DIR, rel))',
    'def expect(*a, **k):',
    '    return a[0]',
    'def _jsstr(x):',
    '    # JS String(x): arrays coerce to comma-joined, others to str().',
    '    if isinstance(x, list):',
    '        return ",".join(_jsstr(e) for e in x)',
    '    if x is None:',
    '        return "None"',
    '    if x is True:',
    '        return "true"',
    '    if x is False:',
    '        return "false"',
    '    return str(x)',
    'def _hasprop(x, k):',
    '    # JS expect(obj).to.have.property(k): key membership for dicts, attr for objects.',
    '    if isinstance(x, dict):',
    '        return k in x',
    '    return hasattr(x, k)',
    'def _has_own(x, k):',
    '    # JS obj.hasOwnProperty(k): key membership for dicts, attr for objects.',
    '    if isinstance(x, dict):',
    '        return k in x',
    '    return hasattr(x, k)',
    '',
  ].join('\n');

  let body = '';
  // Local test-helper imports (e.g. ./arpabet-ipa.js re-exports analyzer
  // utilities). Map the named bindings onto their Python equivalents.
  const HELPER_IMPORTS = {
    './arpabet-ipa.js': {
      arpabetToIpa: 'from rita.analyzer import Analyzer\narpabetToIpa = Analyzer.arpabet_to_ipa',
      phonesToIpa: 'from rita.analyzer import Analyzer\nphonesToIpa = Analyzer.phones_to_ipa',
      syllablesToIpa: 'from rita.analyzer import Analyzer\nsyllablesToIpa = Analyzer.syllables_to_ipa',
    },
  };
  for (const node of ast.body) {
    if (node.type === 'ImportDeclaration') {
      const spec = node.source && node.source.value;
      if (spec && HELPER_IMPORTS[spec]) {
        for (const s of node.specifiers || []) {
          const name = s.imported ? s.imported.name : s.local.name;
          if (HELPER_IMPORTS[spec][name]) body += HELPER_IMPORTS[spec][name] + '\n';
        }
      }
      continue;
    }
    if (node.type === 'ExpressionStatement' && node.expression.type === 'CallExpression' && id(node.expression.callee) === 'describe') {
      body += describeCall(node.expression, '') + '\n\n';
    } else if (node.type === 'VariableDeclaration') {
      body += node.declarations.map(d => varDecl(d, '')).join('\n') + '\n\n';
    } else if (node.type === 'FunctionDeclaration') {
      body += S(node, '') + '\n\n';
    } else if (node.type === 'ExpressionStatement') {
      const e = node.expression;
      if (e.type === 'CallExpression' && id(e.callee) === 'describe') {
        body += describeCall(e, '') + '\n\n';
      } else if ((e.type === 'CallExpression' || e.type === 'MemberExpression') && chainHasExpect(e)) {
        body += translateExpect(e, '') + '\n\n';
      } else {
        body += exprStatement(e, '') + '\n\n';
      }
    } else {
      body += S(node, '') + '\n\n';
    }
  }

  const hoisted = (MODULE_VARS.length ? MODULE_VARS.join('\n') + '\n\n' : '') + (MODULE_HOOKS.length ? MODULE_HOOKS.join('\n') + '\n\n' : '') + (MODULE_FNS.length ? MODULE_FNS.join('\n\n') + '\n\n' : '') + (HOIST.length ? HOIST.join('\n\n') + '\n\n' : '');
  // body first so module-level `let` (e.g. `sample`) is defined before any
  // describe-scope var (e.g. `sample3 = sample + ...`) that references it.
  const out = header + '\n' + body + hoisted;
  const base = file.replace(/\.js$/, '').replace(/-tests?$/, '');
  const outFile = path.join(OUT_DIR, 'test_' + base + '.py');
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.writeFileSync(outFile, out);
  return outFile;
}

for (const f of files) {
  try {
    const out = transpile(f);
    console.log('wrote', out);
  } catch (e) {
    console.error('FAILED', f, e.message);
  }
}
