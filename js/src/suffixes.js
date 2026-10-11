
import { createRequire } from 'module';

// EOL for serialization
const EOL = '\n';

// Lazy node loader — no-ops in non-Node envs
function nodeRequire(mod) {
  try { return createRequire(import.meta.url)(mod); } catch { return {}; }
}

export default class SuffixArray {

  static SILENT = true; // set to false to enable logging
  static XOVER_WINDOW = 8;
  static SEQ_START_TOKEN = '<s>';
  static SEQ_END_TOKEN = '</s>';
  static USE_COMPRESSION = true;

  /**
   * Returns a random float in [0,1) from the shared seeded RNG (RiTa.randomizer)
   * when available, so RiTa.randomSeed() makes selection reproducible. Falls
   * back to Math.random() for standalone use without a loaded RiTa.
   */
  static random() {
    return SuffixArray.RiTa ? SuffixArray.RiTa.randomizer.random() : Math.random();
  }

  static __props__ = ['startToken', 'endToken', 'xoverWindow', 'compressed', 'length', 'decoder', 'encoder'];
  static __dict__ = [ ...SuffixArray.__props__, 'input', 'seqmap', 'data', 'xovers' ];

  constructor(s, opts = {}) { // pre-tokenized input

    // fields
    this.length = 0;
    this.input = [];
    this.seqmap = [];
    this.data = [];
    this.xovers = [];

    this.decoder = null;
    this.encoder = null;
    this._startIndexes = null;
    this._startIndexDist = null;

    // opts
    this.startToken = opts.startToken ?? SuffixArray.SEQ_START_TOKEN;
    this.endToken = opts.endToken ?? SuffixArray.SEQ_END_TOKEN;
    this.xoverWindow = opts.xoverWindow ?? SuffixArray.XOVER_WINDOW; // mv to subclass?
    this.compressed = opts.compressed ?? SuffixArray.USE_COMPRESSION;

    if (typeof s !== 'undefined') {
      if (!Array.isArray(s)) {
        throw Error('Expected array of tokens');
      }
      let input = this.compressed ? this.compressTokens(s) : s;
      this.build(input);
    }
  }

  compressTokens(input) {
    if (!input || !input.length) return input;

    let words = new Set(); // set of all words
    for (let i = 0; i < input.length; i++) {
      words.add(input[i]);
    }

    // words are sorted lexicographically
    this.decoder = Array.from(words).sort();

    // create mapping: word -> sorted-position
    this.encoder = {}; // perf: loop 
    for (let i = 0; i < this.decoder.length; i++) {
      this.encoder[this.decoder[i]] = i;
    }

    // compress input based on mapping table
    let compressed = []; // perf: loop 
    for (let i = 0; i < input.length; i++) {
      compressed.push(this.encoder[input[i]]);
    }

    return compressed;
  }

  toFileSync(path) {
    const fs = nodeRequire('fs');
    fs.writeFileSync(path, this.toRawString());
  }

  static fromFileSync(path) {
    const fs = nodeRequire('fs');
    const { EOL: eol = EOL } = nodeRequire('os');
    let data = fs.readFileSync(path, 'utf8');
    let lines = data.split(eol);
    return SuffixArray.fromRawLines(lines);
  }

  async toFileStream(path) {
    const { default: fs } = await import('fs');
    const { EOL: eol } = await import('os');
    return new Promise((resolve, reject) => {
      const outputStream = fs.createWriteStream(path);
      let records = [this.headerRecord(), ...this.dataRecords()];
      records.forEach(r => outputStream.write(r + eol));
      outputStream.end();
      outputStream.on("finish", resolve).on('error', reject);
    });
  }

  static async fromFileStream(path) {
    const { default: fs } = await import('fs');
    const { default: readline } = await import('readline');
    return new Promise((resolve, reject) => {
      const records = [];
      readline.createInterface({
        input: fs.createReadStream(path)
      }).on('line', function (line) {
        records.push(line);
      }).on('close', function () {
        resolve(SuffixArray.fromRawLines(records));
      }).on('error', reject);
    });
  }

  static initFromMeta(meta) {
    let sa = new SuffixArray();
    SuffixArray.__props__.forEach(p => sa[p] = meta[p]);
    sa.input = new Array(meta.length);
    sa.seqmap = new Array(meta.length);
    sa.data = new Array(meta.length);
    sa.xovers = new Array(meta.length);
    return sa;
  }

  static fromJSON(json) {
    //let t = Date.now();
    let records = typeof json === 'string' ? JSON.parse(json) : json;
    let meta = records.shift();
    let sa = SuffixArray.initFromMeta(meta);
    for (let i = 0; i < records.length; i++) {
      let { input, data, xover, seqmap } = records[i];
      sa.input[i] = input;
      sa.data[i] = data;
      sa.xovers[i] = xover;
      sa.seqmap[i] = seqmap;
    }
    return sa;
  }

  static fromRawString(str) {
    return SuffixArray.fromRawLines(str.split(EOL));
  }

  static fromRecords(meta, records) {
    let sa = SuffixArray.initFromMeta(meta);
    if (records.length !== sa.length) throw Error('Invalid records');
    for (let i = 0; i < records.length; i++) {
      let [input, data, xover, seqmap] = records[i];
      //console.log(i+')', input, data, xover, seqmap);
      sa.input[i] = input;
      sa.data[i] = data;
      sa.xovers[i] = xover;
      sa.seqmap[i] = seqmap;
    }
    return sa
  }

  static fromRawLines(lines) {
    if (!lines || !Array.isArray(lines) || !lines.length) {
      throw Error('No lines to process');
    }
    let header = JSON.parse(lines.shift());
    let sa = SuffixArray.initFromMeta(header);
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (line.length > 0) {
        let [input, data, xover, seqmap] = line.split(',').map(e => parseInt(e));
        sa.input[i] = input;
        sa.data[i] = data;
        sa.xovers[i] = xover;
        sa.seqmap[i] = seqmap;
      }
    }
    return sa;
  }

  toRawString() {
    let header = this.headerRecord();
    let data = this.dataRecords().map(r => r.join(','));
    return header + EOL + data.join(EOL);
  }

  // returns an array of records, once for each input token
  dataRecords() {
    return this.data.map((d, i) => [this.input[i], d, this.xovers[i], this.seqmap[i]]);
  }

  headerRecord() {
    let header = {};
    SuffixArray.__props__.forEach(p => header[p] = this[p]);
    return JSON.stringify(header);
  }

  toJSON() {
    // return json array of records, once for each input token
    let meta = {}, records = new Array(this.length);

    SuffixArray.__props__.forEach(e => meta[e] = this[e]);

    for (let i = 0; i < this.length; i++) {
      let record = {
        input: this.input[i],
        data: this.data[i],
        xover: this.xovers[i],
        seqmap: this.seqmap[i]
      };
      records[i] = record;
    }
    records.unshift(meta);

    return records;
  }

  /**
   * Binary search that returns indices [min, max] so that the interval 
   * this.input[s..r] contains all suffixes starting with the tokens
   */
  find(query, opts) {
    if (!Array.isArray(query) || query.length === 0) { // empty query
      query = [this.startToken];
    }
    query = this._encode(query);
    let start = this.binsearch(query, true, opts);
    let end = this.binsearch(query, false, opts);
    return (start === null || end === null) ? [0, 0] : [start, end + 1];
  }

  /**
    * Returns a normalised probability distribution (summing to 1) for a mapping of tokens to counts
    * If temperature is provided this is basically the softmax, otherwise it is simple normalisation
    * 
    * Temperature parameter: range is between 0 and +Infinity (excluding both).
    * Lower values move the highest-weighted output toward a probability of 1.0.
    * Higher values tend toward evening out all the probabilities (all tokens equally likely).
    */
  static normaliseDist(mapping, temp = 0) { // TODO: move to utils, grab from RiTa-Markov

    if (Object.keys(mapping).length === 0) return {}; // empty

    let total = 0, tdist = {};
    if (temp === 0) {
      // normalize counts as probabilities (sum to 1)
      total = Object.values(mapping).reduce((a, b) => a + b, 0);
      Object.keys(mapping).forEach(tok => {
        if (mapping[tok] < 0) throw Error('Negative count');
        tdist[tok] = mapping[tok] / total
      });
    }
    else {
      // normalize counts via softmax with temperature
      temp = Math.max(temp, 0.01); // avoid NaN result
      for (const [token, count] of Object.entries(mapping)) {
        if (count < 0) throw Error('Negative count');
        let pr = Math.exp(count / temp);
        tdist[token] = pr;
        total += pr;
      }
      Object.keys(tdist).forEach(tok => tdist[tok] /= total);
    }
    return tdist;
  }

  /**
   * Returns the array of `len` tokens at this.data[`index`] or the rest of the input if `len` is not provided
   * @returns {Array<string>}
   * @throws {Error} Index out of range
   */
  tokensFor(index, len) { // 
    if (typeof index === 'undefined' || index < 0 || index > this.data.length) {
      throw Error('Index out of range: ' + index);
    }
    let toks;
    if (typeof len === 'undefined') {
      toks = this.input.slice(this.data[index]);
    }
    else {
      toks = this.input.slice(this.data[index], this.data[index] + len);
    }

    return this._decode(toks);
  }

  ///////////////////////////// PUBLIC API /////////////////////////////

  /**
   * Returns a 2d array of tokens at this.data.slice(min ,max)
   * @param {number} min
   * @param {number} max
   * @returns {Array<Array<string>>}
   * @throws {Error} Index out of range
   */
  tokensForRange(min, max) {
    if (min < 0 || min >= this.data.length) {
      throw Error('Index out of range');
    }
    if (typeof max === 'undefined') {
      max = this.data.length - 1;
    }
    let lines = [];
    for (let i = min; i < max; i++) {
      let tokArr = this._decode(this.input.slice(this.data[i]));
      //console.log(i, tokArr);
      lines.push(tokArr);
    }
    return lines;
  }

  prefixIndexes(query) {
    let low = 0, high = this.data.length - 1;
    while (low <= high) {
      const mid = Math.floor((low + high) / 2);
      if (this.isSubArray(mid, query)) return mid;
      if (this.lt(mid, query)) {
        low = mid + 1;
      } else {
        high = mid - 1;
      }
    }
    return -1;
  }

  hasPrefix(query) {
    query = this._encode(query);
    if (!query || !query.length) return false;
    let low = 0, high = this.data.length - 1;
    while (low <= high) {
      const mid = Math.floor((low + high) / 2);
      if (this.isSubArray(mid, query)) return true;
      if (this.lt(mid, query)) {
        low = mid + 1;
      } else {
        high = mid - 1;
      }
    }
    return false;
  }

  hasSuffix(query) {
    query = this._encode(query);
    let low = 0, high = this.data.length - 1;
    while (low <= high) {
      const mid = Math.floor((low + high) / 2);
      if (this.arrayEquals(mid, query)) return true;
      if (this.lt(mid, query)) {
        low = mid + 1;
      } else {
        high = mid - 1;
      }
    }
    return false;
  }

  /**
   * Return a probability distribution for possible next tokens given the pattern
   */
  pdist(query = [], opts) {

    // if no query, or query is just start token, return start token dist
    if (!query.length || (query.length === 1 && query[0] === this.startToken)) {
      return normalize(this.startIndexDist());
    }

    // compute raw distribution for next token given the query pattern
    const [min, max] = this.find(query, opts);
    let probDist = this.distFromIndexes(min, max, query.length);
    if (!probDist) return undefined;

    // get normalised distribution with temperature via softmax
    let logits = Object.values(probDist);
    let tokens = Object.keys(probDist);
    let ndist = softmax(logits, opts?.temp);

    // create mapping of tokens to normalised probability
    let result = {};
    tokens.forEach((t, i) => result[t] = ndist[i]);

    return result;
  }

  distFromIndexes(min, max, queryLength) {
    //if (opts?.debug) console.log('  distFromIndexes', min, max, queryLength);
    if (max > min) {

      let probs = {};
      for (let i = min; i < max; i++) {
        let idx = this.data[i] + queryLength;
        let next = this._encode(this.input[idx]);
        if (typeof next !== 'undefined') {// && (!exclude || !exclude.includes(next))) { // save
          probs[next] = probs[next] ? probs[next] + 1 : 1;
        }
      }
      return probs;
    }
  }

  toString(opts) {
    let s = EOL + '[' + EOL;
    let xovers = opts?.xovers ?? false;
    let tokensPer = opts?.maxLength ?? 20;
    if (tokensPer < 1) tokensPer = Number.MAX_SAFE_INTEGER;
    this.data.forEach((idx, i) => {
      let tokens = this._decode(this.input.slice(idx, idx + tokensPer));
      let truncated = this.input.length - idx > tokensPer;
      if (truncated) tokens.push('...');
      let m = '  ' + i + ': [' + tokens.join(',') + "],";
      if (xovers && this.xovers[i] > 1) {
        let query = tokens.slice(0, this.xovers[i]);
        let choices = this.pdist(query, opts);
        if (Object.keys(choices).length > 1) {
          m += ` (${this.xovers[i]}) q={${query}} idx=${i} len=`
            + `${this.xovers[i]} numOpts=${Object.keys(choices).length}`
            + ` next=${JSON.stringify(choices).replace(/"/g, '')}`;
        }
      }
      s += m + EOL;  // add
    });

    return s + ']' + EOL;
  }

  /**
   * Returns true if the model does not contain the given sequence of tokens, else false
   * @param {Array} sequence - The sequence to check
   * @returns {boolean} - True if the sequence is unique in the model
   */
  isUnique(sequence) {
    if (!sequence || !sequence.length || typeof sequence[0] !== 'string') {
      throw Error('Invalid sequence(' + typeof sequence + '): ' + JSON.stringify(sequence));
    }
    //console.log(this.suffixes.toString(), 'isUnique', sequence);
    return !this.hasPrefix(sequence);
  }

  /**
   * Returns true if the model does not contain the sequence of tokens specified by the given indexes, else false
   * @param {Number} startIdx - The start index of the sequence
   * @param {Number} endIdx - The end index of the sequence
   * @returns {boolean} - True if the sequence is unique in the model
   */
  isUniqueAt(startIdx, endIdx) {
    let sequence = this.input.slice(startIdx, endIdx);
    return !this.hasPrefix(sequence);
  }

  /**
   * Returns a randomly selected sequence start (a token directly following a start token)
   * @returns {string} a random sequence start
   */
  randSeqStart() {
    let indexes = this.startIndexes();
    let start = indexes[Math.floor(SuffixArray.random() * indexes.length)];
    return this._decode(start);
  }

  build(s) {

    if (!SuffixArray.SILENT) console.log('Received ' + s.length + ' tokens');

    let ts = Date.now();
    const len = s.length;
    const data = new Array(len);
    const ranks = new Array(len);
    const tmp = new Array(len);
    const starts = new Array(len);
    const xovers = new Array(len);

    let startIndex = this.compressed ?
      this.encoder[this.startToken] : this.startToken;

    for (let i = 0; i < len; i++) {
      data[i] = i;
      tmp[i] = 0;
      ranks[i] = s[i];
      //starts[i] = (s[i] === this.startToken) ? 1 : 0;
      starts[i] = (s[i] === startIndex) ? 1 : 0;
    }

    let gap;
    const cmp = (x, y) => {
      if (ranks[x] !== ranks[y]) {
        return rawcmp(ranks[x], ranks[y]);
      }
      x += gap;
      y += gap;
      return x < len && y < len ?
        rawcmp(ranks[x], ranks[y]) : rawcmp(y, x);
    }

    for (gap = 1; tmp[len - 1] < len - 1; gap <<= 1) {
      data.sort(cmp);

      for (let i = 1; i < len; i++) {
        tmp[i] = tmp[i - 1] +
          (cmp(data[i - 1], data[i]) === -1 ? 1 : 0);
      }

      //console.log('gap1:', gap, tmp[len - 1], '<?', len - 1);
      let finalPass = (tmp[len - 1] >= len - 1);
      for (let i = 0; i < len; i++) {
        ranks[data[i]] = tmp[i];
        if (finalPass) { // OPT:
          let aStart = data[i], aEnd = data[i] + this.xoverWindow;
          let bStart = data[i + 1], bEnd = data[i + 1] + this.xoverWindow;
          xovers[i] = SuffixArray.arrayCompareSlices(s, aStart, aEnd, bStart, bEnd);
        }
      }
    }
    xovers[len - 1] = -1;   // last token
    //console.log('xo',xovers);

    if (!SuffixArray.SILENT) console.log('Processed ' +
      s.length + ' tokens in ' + (Date.now() - ts) + 'ms');

    this.input = s;
    this.data = data;
    this.xovers = xovers;
    this.seqmap = starts;
    this.length = s.length;
    //console.log(this.input.length, this.data.length, this.xovers.length, this.seqmap.length);
  }

  createDist(arr, normalise = false) {
    let dist = {};
    for (let i = 0; i < arr.length; i++) {
      dist[arr[i]] = dist[arr[i]] || 0;
      dist[arr[i]]++;
    }
    return normalise ? SuffixArray.normaliseDist(dist) : dist;
  }

  startIndexDist() {
    if (!this._startIndexDist) {
      let indexes = this._decode(this.startIndexes())
      this._startIndexDist = this.createDist(indexes, true);
    }
    return this._startIndexDist;
  }

  startIndexes() {
    if (this._startIndexes === null) {
      let indexes = this.seqmap.reduce((a, e, i) => {
        if (e === 1) a.push(i); return a;
      }, []);
      this._startIndexes = indexes.map(idx => this.input[idx + 1]);
    }
    return this._startIndexes;
  }

  binsearch(query, isFirst, opts) {
    let data = this.data; // opts?.reverse ? this.atad : this.data;
    let low = 0, high = data.length - 1;

    let result = -1;
    while (low <= high) {
      const mid = Math.floor((low + high) / 2);
      if (this.isSubArray(mid, query)) {
        result = mid;
        if (isFirst) {
          high = mid - 1;
        } else {
          low = mid + 1;
        }
      } else if (this.lt(mid, query)) {
        low = mid + 1;
      } else {
        high = mid - 1;
      }
    }
    return result === -1 ? null : result;
  }

  lt2(dataIdx, startIdx, endIdx, query) {
    const position = this.data[dataIdx];
    const queryLen = endIdx - startIdx;
    for (let i = 0; i < queryLen; i++) {
      if (position + i >= this.input.length) {
        return true;
      }
      const eleA = this.input[position + i];
      const eleB = this.input[startIdx + i];
      if (eleA !== eleB) return eleA < eleB;
      //if (query[i] !== c) return c < query[i];
    }

    return false;
  }


  lt(idx, query) {
    const position = this.data[idx];

    for (let i = 0; i < query.length; i++) {
      if (position + i >= this.input.length) {
        return true;
      }
      const c = this.input[position + i];
      if (query[i] !== c) return c < query[i];
    }

    return false;
  }

  /**
   * Returns true if the query is a subarray of the input at data[index]
   * @param {*} index 
   * @param {*} query 
   * @returns true if query is a subarray of the input at data[index], false otherwise
   */
  isSubArray(index, query) {
    const position = this.data[index];
    for (let i = 0; i < query.length; i++) {
      const c = this.input[position + i];
      if (query[i] !== c) return false;
    }
    return true;
  }

  /**
   * Returns true if the query is a subarray of the input at data[index]
   * @param {*} dataIndex 
   * @param {*} startIdx 
   * @param {*} endIdx 
   * @returns true if query is a subarray of the input at data[index], false otherwise
   */
  isSubArray2(dataIndex, startIdx, endIdx) {
    const position = this.data[dataIndex];
    let queryLen = endIdx - startIdx;
    for (let i = 0; i < queryLen; i++) {
      const eleA = this.input[position + i];
      const eleB = this.input[startIdx + i];
      if (eleA !== eleB) return false;
    }
    return true;
  }

  /**
   * Returns true if the query matches the array at data[index], element by element
   * @param {*} index 
   * @param {*} query 
   * @returns true if equal, false otherwise
   */
  arrayEquals(index, query) {
    const tokens = this.input.slice(this.data[index]);
    if (tokens.length !== query.length) return false;
    for (let i = 0; i < tokens.length; i++) {
      if (tokens[i] !== query[i]) return false;
    }
    return true;
  }

  /**
   * Compares two slices of an array, element-by-element, returning the index of the first non-equal token
   * Note: the index is relative to the start of the slice
   * @param {Array} arr - the array to compare
   * @param {Number} aStart - start index of slice a
   * @param {Number} aEnd - end index of slice a, exclusive
   * @param {Number} bStart - start index of slice b
   * @param {Number} bEnd - end index of slice b, exclusive
   * @returns the index of the first non-equal token from two slices, or -1 if they are equal
   */
  static arrayCompareSlices(arr, aStart, aEnd, bStart, bEnd) { // ?
    let lenA = Math.min(arr.length, aEnd - aStart);
    let lenB = Math.min(arr.length, bEnd - bStart);
    let len = Math.min(lenA, lenB);
    if (lenA !== lenB) return len;
    for (let i = 0; i < len; i++) {
      if (arr[aStart + i] !== arr[bStart + i]) return i;
    }
    return -1;
  }

  /**
   * Compares two arrays, element-by-element, returning the index of the first non-equal token
   * @param {Array} a 
   * @param {Array} b 
   * @returns the index of the first non-equal token from two arrays or -1 if they are equal
   */
  static arrayCompare(a, b) {
    if (!a || !b) return -1;
    let len = Math.min(a.length, b.length);
    if (a.length !== b.length) return len;
    for (let i = 0; i < len; i++) {
      if (a[i] !== b[i]) return i;
    }
    return -1;
  }

  /*
   * encodes a sequence to numeric data
   */
  _encode(arg) {
    if (!this.compressed) return arg;
    return Array.isArray(arg) ? arg.map(t => this.encoder[t]) : this.decoder[arg];
  }

  /*
   * translates a numeric entry back to its human-readable form
   */
  _decode(arg) {
    if (!this.compressed) return arg;
    return Array.isArray(arg) ? arg.map(t => this.decoder[t]) : this.decoder[arg];
  }

} // end

function rawcmp(a, b) {
  return a === b ? 0 : (a < b ? -1 : 1);
}

function softmax(logits, temp = 1) {
  if (temp === 0) return normalize(Object.fromEntries(logits.map((v, i) => [i, v])));
  temp = Math.max(temp, 0.000001); // avoid negative temperature
  const scaled = logits.map(v => Math.exp(v / temp));
  const sum = scaled.reduce((a, b) => a + b, 0);
  return scaled.map(v => v / sum);
}

function normalize(dist) {
  const total = Object.values(dist).reduce((sum, p) => sum + p, 0);
  return Object.fromEntries(Object.entries(dist).map(([k, v]) => [k, v / total]));
}