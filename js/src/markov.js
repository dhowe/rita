import SuffixGram from './model.js';
import BackoffModel from './backoff.js';

export default class RiMarkov {

  static RiTa = undefined;

  /**
   * Creates an instance of RiMarkov.
   * @param {*} input
   * @param {*} [opts]
   * @memberof RiMarkov
   */
  constructor(input, opts) {
    this.n = -1;
    if (typeof input === 'number') {
      // for compatibility with v3.x constructor
      this.n = input;
      input = opts ? opts?.text || opts?.tokens : undefined;
    }
    else if (SuffixGram.isObject(input) && typeof opts === 'undefined') {
      opts = input;
      input = opts?.text || opts?.tokens;
    }

    if (isFinite(opts?.n)) this.n = opts.n;

    // save any generation-relevant opts for use as per-instance defaults
    this.opts = {};
    if (opts) {
      for (const key of Object.keys(BackoffModel.generationDefaults)) {
        if (typeof opts[key] !== 'undefined') this.opts[key] = opts[key];
      }
    }

    this.model = new BackoffModel(input, opts);
  }

  /**
   * Stream tokens one-by-one from the model, yielding each token as it is sampled.
   * Delegates to {@link BackoffModel#streamTokens}.
   *
   * @param {number}   n       - n-gram order
   * @param {string[]} prompt  - initial context tokens
   * @param {Object}   [opts]
   * @param {number}   [opts.minTokens]      - minimum tokens before a stop condition is honoured
   * @param {number}   [opts.maxLength]      - hard cap on tokens yielded
   * @param {number}   [opts.temp]           - sampling temperature
   * @param {string|function} [opts.generateUntil] - stop token or predicate `(token, tokensSoFar) => boolean`
   * @yields {string} one token at a time
   */
  * stream(n, prompt = [], opts = {}) {

    ({ prompt, opts } = this._resolveArgs(n, prompt, opts));
    opts = { ...this.opts, ...opts }; // apply instance defaults

    if (!this.model.ready) this.model.build(); // ensure model is built before generating

    yield* this.model.streamTokens(this.n, prompt, opts);
  }

  /**
   * Generate one or more sentences from the model.
   *
   * Supports several call signatures:
   *   generate(n, prompt, opts)   — explicit n-gram order, prompt array, options
   *   generate(n, opts)           — n-gram order + options (empty prompt)
   *   generate(prompt, opts)      — prompt array + options (n via opts.n or constructor)
   *   generate(opts)              — all parameters in opts.n / opts.prompt
   *
   * @param {number|string[]|Object} n      - n-gram order, or prompt array, or opts object
   * @param {string[]|Object}        prompt - prompt tokens, or opts object
   * @param {Object}                 [opts]
   * @param {number}  [opts.n]            - n-gram order (alternative to positional arg)
   * @param {string[]}[opts.prompt]       - prompt tokens (alternative to positional arg)
   * @param {number}  [opts.numSentences] - number of sentences to generate (default: 1)
   * @param {number}  [opts.minTokens]    - minimum tokens per sentence
   * @param {number}  [opts.maxLength]    - maximum tokens per sentence
   * @param {number}  [opts.temp]         - sampling temperature
   * @returns {string|string[]} a single string when numSentences=1, otherwise an array of strings
   */
  generate(n, prompt = [], opts = {}) {

    ({ prompt, opts } = this._resolveArgs(n, prompt, opts));
    opts = { ...this.opts, ...opts }; // apply instance defaults

    if (!this.model.ready) this.model.build();

    const numSentences = opts.numSentences ?? 1;
    const result = this.model.generateSentences(this.n, prompt, { ...opts, numSentences });

    // return a plain string for the single-sentence case
    return (numSentences === 1) ? result[0] : result;
  }

  /*
   * For API consistency only; delegates to generate() with numSentences=1.
   */
  generate1(n, prompt = [], opts = {}) {
    return this.generate(n, prompt, { ...opts, numSentences: 1 });
  }

  addText(...args) {
    return this.model.addText(...args);
  }

  addSentences(...args) {
    return this.model.addSentences(...args);
  }

  addTokens(...args) {
    return this.model.addTokens(...args);
  }

  /*
   * If only one array parameter is provided, this function returns all possible next words, ordered by probability, for the given array.
   *  
   * If two arrays are provided, it returns an unordered array of possible words w that complete the n-gram consisting of: pre[0]...pre[k], w, post[k+1]...post[n].
   * 
   *       result = rm.completions([ "the" ], [ "red", "ball" ]);
   * 
   * The line above will return all the single words that occur between 'the' and 'red ball' in the current model (assuming n > 3), eg [ 'round', 'big', 'bouncy' ]).
   */
  completions(pre, post, opts = {}) {
    if (!Array.isArray(pre)) throw Error('Array required for pre');

    let allowSpecial = opts?.allowSpecial ?? false;

    if (!this.model.ready) this.model.build();

    // single-array form: return next-token distribution (ordered by prob)
    if (typeof post === 'undefined') {
      const dist = this.model.suffixes.pdist(pre);
      if (!dist) return [];
      return Object.entries(dist)
        .sort(([, a], [, b]) => b - a)
        .map(([t]) => t)
        .filter(t => allowSpecial || (t !== this.model.startToken && t !== this.model.endToken));
    }

    // 3-arg form: find all w where [...pre, w, ...post] exists in corpus
    if (!Array.isArray(post)) throw Error('Array required for post');
    if (pre.length + post.length >= (this.n ?? 3)) {
      throw Error(`pre.length + post.length must be less than n (${this.n ?? 3})`);
    }

    // collect every token that follows `pre` and is followed by `post`
    const dist = this.model.suffixes.pdist(pre);
    if (!dist) return [];
    return Object.keys(dist).filter(w => {
      if (!allowSpecial && (w === this.model.startToken || w === this.model.endToken)) {
        return false;
      }
      return this.model.suffixes.hasPrefix([...pre, w, ...post]);
    });
  }

  /**
   * @deprecated
   */
  probability(prompt, next) {
    throw Error('probability() is deprecated. Use probabilities() to get the full distribution,'
      + ' or compute probability of a sequence with completions() and pdist().');
  }

  /**
   * Returns the full set of possible next tokens as an object, given an array of tokens as prompt. 
   * 
   * For example, rm.probabilities(['the', 'cat']) might return { sat: 0.5, jumped: 0.3, meowed: 0.2 }.
   * 
   * If no tokens are provided, returns the distribution of next words following the start token.
   * If `allowSpecial` option is false (default), special start/end tokens will be filtered out of the result. Set `allowSpecial: true` to include them.
   * 
   * @param {string[]} tokens - array of tokens to use as prompt/context
   * @param {Object} [opts]
   * @param {number} [opts.temp] - sampling temperature (default: 0, i.e. no temperature)
   * @param {boolean} [opts.allowSpecial] - whether to include special start/end tokens in the result
   * @returns {Object} an object mapping possible next tokens to their probabilities
   */
  probabilities(tokens, opts = {}) {

    if (!this.model.ready) this.model.build();

    if (typeof tokens === 'undefined') {
      tokens = [this.model.startToken];
    }

    if (!Array.isArray(tokens)) throw Error('tokens[] required');

    const dist = this.model.suffixes.pdist(tokens, { temp: opts?.temp || 0 });
    if (!dist) return {};

    // strip special tokens from result unless allowSpecial
    return Object.fromEntries(Object.entries(dist).filter(([t]) =>
      opts?.allowSpecial || (t !== this.model.startToken && t !== this.model.endToken)));
  }

  /**
   * Return the number of tokens in the model.
   * For character count, see model.suffixes.length
   */
  size() {
    return this.model.size();
  }

  toString(opts) {
    return this.model.toString(opts);
  }

  toJSON() {
    if (!this.model.ready) this.model.build();
    let data = { n: this.n || -1, ...this.model.toJSON() };
    let s = JSON.stringify(data);
    return s;
  }

  static fromJSON(json) {
    if (typeof json !== 'string') throw Error('String required for fromJSON()');
    let rm = new RiMarkov();
    let parsed = JSON.parse(json);
    const { n, ...modelData } = parsed;
    rm.model = BackoffModel.fromJSON(modelData);
    rm.n = n;
    return rm;
  }

  /**
   * Normalise the polymorphic (n, prompt, opts) argument patterns shared by
   * stream() and generate() into a canonical { n, prompt, opts } object.
   *
   * Supported call patterns:
   *   (n, prompt, opts)  — all positional
   *   (n, opts)          — n + options, empty prompt
   *   (prompt, opts)     — prompt array + options, n via opts.n or constructor
   *   (opts)             — everything in opts.n / opts.prompt
   */
  _resolveArgs(n, prompt, opts) {

    if (SuffixGram.isObject(n)) {
      // single-argument form: fn(opts)
      opts = { ...n };
      prompt = opts.prompt ?? [];
      n = opts.n;
      delete opts.n;
      delete opts.prompt;

    } else if (Array.isArray(n)) {
      // two-argument form: fn(prompt, opts?)
      opts = prompt ?? {};
      prompt = n;
      n = opts.n;

    } else if (SuffixGram.isObject(prompt)) {
      // two-argument form: fn(n, opts)
      opts = { ...prompt };
      prompt = opts.prompt ?? [];
      delete opts.prompt;
    }

    if (!Array.isArray(prompt)) throw Error('Array required for prompt');

    this.n = n ?? opts?.n ?? this.n;
    if (this.n < 1) throw Error('n must be specified'
      + ' before calling generate() or stream()');

    return { prompt, opts: opts ?? {} };
  }
}



