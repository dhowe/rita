#!/usr/bin/env node
/**
 * Generates JS-module-format dict files for js/ and java/ from the canonical
 * shared/rita_dict.json. Run after updating shared/rita_dict.json.
 *
 *   node scripts/gen-dicts.js
 */

import { mkdirSync, readFileSync, writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { join, dirname } from 'path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const data = JSON.parse(readFileSync(join(root, 'shared', 'rita_dict.json'), 'utf8'));

// Serialize with 2-space indent and inline leaf arrays, e.g.
//   "a": ["ey1", "dt"],
// (JSON.stringify(_, null, 2) would expand every leaf array to 4 lines,
// ballooning the file ~4x and producing a huge no-op diff.)
const serialize = (obj) => {
  const keys = Object.keys(obj);
  const lines = keys.map((key, i) => {
    const val = obj[key];
    const encoded = Array.isArray(val)
      ? `[${val.map((x) => JSON.stringify(x)).join(', ')}]`
      : JSON.stringify(val);
    return `  ${JSON.stringify(key)}: ${encoded}${i < keys.length - 1 ? ',' : ''}`;
  });
  return `{\n${lines.join('\n')}\n}`;
};
const body = serialize(data);

// Java reads shared/rita_dict.json directly (staged into its build by Gradle),
// so only the JS module is generated here.
const targets = [
  {
    path: join(root, 'js', 'src', 'rita_dict.js'),
    content: `\n/** @type {object} */\nexport default ${body};\n`,
  },
];

for (const { path, content } of targets) {
  writeFileSync(path, content, 'utf8');
  console.log(`Written: ${path}`);
}

// Python ships the dictionary as package data (python/rita/data/), because an
// installed wheel cannot reach the mono-repo's shared/ directory. In a source
// checkout rita.dictdata still prefers shared/ when present, so this copy is
// what makes the wheel self-contained.
const pyDataDir = join(root, 'python', 'rita', 'data');
mkdirSync(pyDataDir, { recursive: true });
const pyDataPath = join(pyDataDir, 'rita_dict.json');
writeFileSync(pyDataPath, JSON.stringify(data) + '\n', 'utf8');
console.log(`Written: ${pyDataPath}`);
