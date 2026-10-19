#!/usr/bin/env node
/**
 * Extracts the Letter-to-Sound state-machine rules from js/src/rita_lts.js and
 * writes them to shared/rita_lts.json so the Java (and any other) implementation
 * can load them as a shared resource without duplicating the 13k-line table.
 *
 *   node scripts/gen-lts.js
 *
 * The output is a JSON array of rule strings, e.g. ["T 13100", "I 0 a", "S 4 r 2 1", ...],
 * exactly the contents of LetterToSound.RULES in the JS source.
 */

import { writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { join, dirname } from 'path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');

const mod = await import(join(root, 'js', 'src', 'rita_lts.js'));
const RULES = mod.default?.RULES || mod.LetterToSound?.RULES || mod.RULES;
if (!Array.isArray(RULES)) {
  throw new Error('Could not locate LetterToSound.RULES in js/src/rita_lts.js');
}

const out = join(root, 'shared', 'rita_lts.json');
writeFileSync(out, JSON.stringify(RULES) + '\n');
console.log(`Wrote ${RULES.length} LTS rules to ${out}`);
