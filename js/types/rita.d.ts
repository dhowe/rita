import { RiGrammar, RiScript } from 'riscript';

export class RiTa {
    static grammar(rules?: object, context?: object): RiGrammar;
    static addTransform(name: string, definition: ((...args: any[]) => string) | object): void;
    static removeTransform(name: string): void;
    static getTransforms(): string[];
    static articlize(word: string): string;
    static evaluate(script: string, context?: object, options?: {
        trace?: boolean;
    }): string;
    static markov(n: number, options?: MarkovOptions): RiMarkov;
    static markov(text: string, options?: MarkovOptions): RiMarkov;
    static markov(options?: MarkovOptions): RiMarkov;
    static kwic(keyword: string, options?: {
        numWords?: number;
        text?: string;
        words?: string[];
    }): string[];
    static kwic(keyword: string, numWords: number): string[];
    static concordance(text: string, options?: {
        ignoreCase?: boolean;
        ignoreStopWords?: boolean;
        ignorePunctuation?: boolean;
        wordsToIgnore?: string[];
    }): Record<string, number>;
    static randomOrdering(array: object[]): object[];
    static randomOrdering(k: number): number[];
    static randomSeed(seed: number): void;
    static isQuestion(sentence: string): boolean;
    static isVowel(char: string): boolean;
    static isConsonant(char: string): boolean;
    static capitalize(string: string): string;
    static randomWord(pattern?: string | RegExp, options?: {
        minLength?: number;
        maxLength?: number;
        numSyllables?: number;
        limit?: number;
        pos?: string;
        pattern?: RegExp;
        type?: string;
    }): string;
    static rhymes(word: string, options?: {
        minLength?: number;
        maxLength?: number;
        numSyllables?: number;
        limit?: number;
        shuffle?: boolean;
        pos?: string;
    }): Promise<string[]>;
    static isRhyme(word1: string, word2: string): boolean;
    static alliterations(word: string, options?: {
        minLength?: number;
        maxLength?: number;
        numSyllables?: number;
        limit?: number;
        shuffle?: boolean;
        pos?: string;
    }): Promise<string[]>;
    static hasWord(word: string, options?: {
        noDerivations?: boolean;
    }): boolean;
    static isAbbrev(input: string, options?: {
        caseSensitive?: boolean;
    }): boolean;
    static isAlliteration(word1: string, word2: string): boolean;
    static spellsLike(word: string, options?: {
        minLength?: number;
        maxLength?: number;
        numSyllables?: number;
        limit?: number;
        shuffle?: boolean;
        pos?: string;
    }): Promise<string[]>;
    static soundsLike(word: string, options?: {
        minLength?: number;
        maxLength?: number;
        numSyllables?: number;
        limit?: number;
        shuffle?: boolean;
        matchSpelling?: boolean;
        pos?: string;
    }): Promise<string[]>;
    static pos(word: string | string[], options?: {
        simple?: boolean;
    }): string | string[];
    static isNoun(word: string): boolean;
    static isAdjective(word: string): boolean;
    static isAdverb(word: string): boolean;
    static isVerb(word: string): boolean;
    static isPunct(text: string): boolean;
    static posInline(sentence: string, options?: {
        simple?: boolean;
    }): string;
    static singularize(word: string): string;
    static pluralize(word: string): string;
    static search(pattern?: string | RegExp, options?: {
        minLength?: number;
        maxLength?: number;
        numSyllables?: number;
        limit?: number;
        shuffle?: boolean;
        pos?: string;
        type?: string;
    }): Promise<string[]>;
    static tokens(text: string, options?: {
        caseSensitive?: boolean;
        ignoreStopWords?: boolean;
        splitContractions?: boolean;
        includePunct?: boolean;
        sort?: boolean;
    }): string[];
    static tokenize(input: string, options?: {
        regex?: RegExp;
        splitHyphens?: boolean;
        splitContractions?: boolean;
    }): string[];
    static untokenize(input: string[], delim?: string): string;
    static sentences(text: string, pattern?: string | RegExp): string[];
    static isStopWord(word: string): boolean;
    static stem(word: string): string;
    static presentPart(verbWord: string): string;
    static pastPart(verbWord: string): string;
    static conjugate(verbWord: string, options?: {
        tense?: number;
        person?: number;
        number?: number;
        form?: number;
        passive?: boolean;
        progressive?: boolean;
        perfect?: boolean;
        interrogative?: boolean;
    }): string;
    static stresses(input: string, options?: object): string;
    static syllables(input: string, options?: {
        ipaPhones?: boolean;
    }): string;
    static phones(input: string, options?: {
        ipaPhones?: boolean;
    }): string;
    static analyze(input: string, options?: {
        simple?: boolean;
        ipaPhones?: boolean;
    }): object;
    static spellsLikeSync(word: string, options?: {
        minLength?: number;
        maxLength?: number;
        numSyllables?: number;
        limit?: number;
        pos?: string;
        shuffle?: boolean;
    }): string[];
    static soundsLikeSync(word: string, options?: {
        minLength?: number;
        maxLength?: number;
        numSyllables?: number;
        limit?: number;
        matchSpelling?: boolean;
        shuffle?: boolean;
        pos?: string;
    }): string[];
    static rhymesSync(word: string, options?: {
        minLength?: number;
        maxLength?: number;
        numSyllables?: number;
        limit?: number;
        shuffle?: boolean;
        pos?: string;
    }): string[];
    static searchSync(pattern?: string | RegExp, options?: {
        minLength?: number;
        maxLength?: number;
        numSyllables?: number;
        limit?: number;
        shuffle?: boolean;
        pos?: string;
        type?: string;
    }): string[];
    static alliterationsSync(word: string, options?: {
        minLength?: number;
        maxLength?: number;
        numSyllables?: number;
        limit?: number;
        shuffle?: boolean;
        pos?: string;
    }): string[];
    static randi(param1: number, param2?: number): number;
    static random(param1?: number | object[], param2?: number): number | object;

    static randomizer: RandGen;
    static RiGrammar: typeof RiGrammar;
    static Stemmer: typeof Stemmer;
    static Model: typeof SuffixGram;
    static RiMarkov: typeof RiMarkov;
    static BackoffModel: typeof BackoffModel;
    static SuffixArray: typeof SuffixArray;

    static tagger: Tagger;
    static analyzer: Analyzer;
    static concorder: Concorder;
    static tokenizer: Tokenizer;
    static inflector: Inflector;
    static lexicon: Lexicon;
    static conjugator: Conjugator;
    static riscript: RiScript;

    static VERSION: string;
    static SILENT: boolean;
    static SILENCE_LTS: boolean;
    static SPLIT_CONTRACTIONS: boolean;
    static CACHING: boolean;

    static STRESS: string;
    static NOSTRESS: string;
    static PHONE_BOUNDARY: string;
    static WORD_BOUNDARY: string;
    static SYLLABLE_BOUNDARY: string;
    static SENTENCE_BOUNDARY: string;
    static VOWELS: string;
    static PHONES: string[];
    static ABRV: string[];
    static QUESTIONS: string[];
    static STOP_WORDS: string[];
    static MASS_NOUNS: string[];

    /** Lazily rebuilt mirror of STOP_WORDS */
    static readonly STOP_WORDS_SET: ReadonlySet<string>;
    /** Lazily rebuilt mirror of MASS_NOUNS */
    static readonly MASS_NOUNS_SET: ReadonlySet<string>;
    /** Lazily rebuilt mirror of QUESTIONS */
    static readonly QUESTIONS_SET: ReadonlySet<string>;

    static INFINITIVE: number;
    static FIRST: number;
    static SECOND: number;
    static THIRD: number;
    static PAST: number;
    static PRESENT: number;
    static FUTURE: number;
    static SINGULAR: number;
    static PLURAL: number;
    static NORMAL: number;
    static GERUND: number;
}

export interface MarkovOptions {
    n?: number;
    text?: string;
    sentences?: string[];
    trace?: boolean;
    maxLengthMatch?: number;
    maxAttempts?: number;
    tokenize?: (sentence: string) => string[];
    untokenize?: (tokens: string[]) => string;
}

export interface GenerateOptions {
    n?: number;
    prompt?: string[];
    numSentences?: number;
    /** minimum tokens before a stop condition is honoured */
    minLength?: number;
    /** also accepted as minTokens */
    minTokens?: number;
    /** maximum tokens to generate */
    maxLength?: number;
    /** also accepted as maxTokens */
    maxTokens?: number;
    /** sampling temperature */
    temp?: number;
    /** also accepted as temperature */
    temperature?: number;
    /** max run of consecutive tokens that may appear verbatim in training data */
    maxLengthMatch?: number;
    /** stop token string or predicate */
    generateUntil?: string | ((token: string, soFar: string[]) => boolean);
    allowDuplicates?: boolean;
}

// Not exported: reachable as RiTa.BackoffModel.
declare class BackoffModel {
    static SILENT: number;
    static fromJSON(json: string): BackoffModel;
    constructor(input?: string | string[], opts?: MarkovOptions);
    addText(text: string): BackoffModel;
    addSentences(sentences: string[]): BackoffModel;
    addTokens(tokens: string[]): BackoffModel;
    build(opts?: object): BackoffModel;
    size(): number;
    toJSON(): object;
    toString(opts?: object): string;
    suffixes: SuffixArray;
    startToken: string;
    endToken: string;
    ready: boolean;
}

// Not exported: reachable as RiTa.SuffixArray.
declare class SuffixArray {
    static SEQ_START_TOKEN: string;
    static SEQ_END_TOKEN: string;
    hasPrefix(seq: string[]): boolean;
    pdist(context: string[], opts?: { temp?: number }): Record<string, number> | undefined;
    startIndexDist(): Record<string, number>;
    length: number;
}

// Not exported: reachable as RiTa.RiMarkov (or via RiTa.markov()).
declare class RiMarkov {
    static fromJSON(json: string): RiMarkov;
    /** new RiMarkov(n, opts) */
    constructor(n: number, options?: MarkovOptions);
    /** new RiMarkov(text, opts) */
    constructor(text: string, options?: MarkovOptions);
    /** new RiMarkov(opts) */
    constructor(options?: MarkovOptions);
    /** new RiMarkov() — empty model */
    constructor();
    n: number;
    model: BackoffModel;
    opts: Partial<GenerateOptions>;
    addText(text: string): RiMarkov;
    addSentences(sentences: string[]): RiMarkov;
    addTokens(tokens: string[]): RiMarkov;
    build(opts?: object): RiMarkov;
    /** Generate one sentence (numSentences=1, default) */
    generate(n: number, prompt: string[], opts: GenerateOptions & { numSentences: 1 }): string;
    /** Generate multiple sentences */
    generate(n: number, prompt: string[], opts: GenerateOptions & { numSentences: number }): string[];
    /** Generate with prompt and options */
    generate(n: number, prompt?: string[], opts?: GenerateOptions): string;
    /** Generate with prompt array and options */
    generate(prompt: string[], opts?: GenerateOptions): string;
    /** Generate with options object only */
    generate(opts?: GenerateOptions): string | string[];
    /** Stream tokens one-by-one */
    stream(n: number, prompt?: string[], opts?: GenerateOptions): IterableIterator<string>;
    stream(prompt: string[], opts?: GenerateOptions): IterableIterator<string>;
    stream(opts?: GenerateOptions): IterableIterator<string>;
    toJSON(): string;
    completions(pre: string[], post?: string[], opts?: { allowSpecial?: boolean }): string[];
    probabilities(tokens?: string[], opts?: { temp?: number; allowSpecial?: boolean }): Record<string, number>;
    /** @deprecated — throws. Use probabilities() instead. */
    probability(prompt: string[], next?: string | string[]): never;
    toString(opts?: object): string;
    size(): number;
}

// ---------------------------------------------------------------------------
// Component classes — not part of the runtime export surface; reachable as
// RiTa.<name> (either a class, for Stemmer/Model, or a singleton instance).
// ---------------------------------------------------------------------------

// Not exported: reachable as RiTa.Stemmer.
declare class Stemmer {
    /** Set by rita.js as a backref to RiTa.tokenizer */
    static tokenizer: Tokenizer;
    static stem(input: string): string;
    static stemAll(input: string[]): string[];
    static stemEnglish(word: string): string;
}

// Not exported: reachable as RiTa.Model (the base class of BackoffModel).
declare class SuffixGram {
    static SILENT: boolean;
    static RiTa: typeof RiTa;
    static defaults: {
        debug: boolean;
        ready: boolean;
        suffixes: boolean;
        compressed: boolean;
        startToken: string;
        endToken: string;
        tokenize?: (input: string) => string[];
        untokenize?: (tokens: string[], delim?: string) => string;
    };
    static options: string[];
    constructor(input?: string | string[], opts?: object);
    /** Subclasses implement this; the base class throws. */
    build(): SuffixGram;
    size(): number;
    toString(opts?: object): string;
    toJSON(): object;
    addText(rawText: string): SuffixGram;
    addSentences(sentences: string[]): SuffixGram;
    addTokens(tokens: string[]): SuffixGram;
    tokens: string[];
    tokenCount: number;
    startToken: string;
    endToken: string;
    ready: boolean;
    suffixes: SuffixArray;
    tokenize?: (input: string) => string[];
    untokenize?: (tokens: string[], delim?: string) => string;
}

// Not exported: reachable as RiTa.tagger.
declare class Tagger {
    constructor(parent: typeof RiTa);
    allTags(word: string, opts?: { noGuessing?: boolean }): string[];
    isVerb(word: string, opts?: object): boolean;
    isNoun(word: string): boolean;
    isAdjective(word: string): boolean;
    isAdverb(word: string): boolean;
    isLikelyPlural(word: string): boolean;
    hasTag(choices: string[], tag: string): boolean;
    inlineTags(words: string[], tags: string[], delimiter?: string): string;
}

// Not exported: reachable as RiTa.analyzer.
declare class Analyzer {
    constructor(parent: typeof RiTa);
    analyze(text: string, opts?: { simple?: boolean; ipaPhones?: boolean }): object;
    analyzeWord(word: string, opts?: { simple?: boolean; ipaPhones?: boolean }): {
        phones: string;
        stresses: string;
        syllables: string;
    };
    computePhones(word: string, opts?: object): string;
    phonesToStress(phones: string): string | undefined;
}

// Not exported: reachable as RiTa.concorder.
declare class Concorder {
    constructor(parent: typeof RiTa);
    concordance(text: string | string[], options?: {
        ignoreCase?: boolean;
        ignoreStopWords?: boolean;
        ignorePunctuation?: boolean;
        wordsToIgnore?: string[];
    }): Record<string, number>;
    /** opts may be an options object or a number of context words */
    kwic(word: string, opts?: object | number): string[];
    count(word: string): number;
}

// Not exported: reachable as RiTa.tokenizer.
declare class Tokenizer {
    constructor(parent: typeof RiTa);
    tokens(text: string, options?: {
        caseSensitive?: boolean;
        ignoreStopWords?: boolean;
        splitContractions?: boolean;
        includePunct?: boolean;
        sort?: boolean;
    }): string[];
    tokenize(input: string, opts?: {
        regex?: RegExp;
        debug?: boolean;
        splitHyphens?: boolean;
        splitContractions?: boolean;
    }): string[];
    untokenize(tokenArray: string[], delim?: string): string;
    sentences(text: string, regex?: string | RegExp): string[];
}

// Not exported: reachable as RiTa.inflector.
declare class Inflector {
    constructor(parent: typeof RiTa);
    singularize(word: string, opts?: object): string;
    pluralize(word: string, opts?: object): string;
    isPlural(word: string, opts?: object): boolean;
    adjustNumber(word: string, type: number, dbug?: boolean): string;
}

// Not exported: reachable as RiTa.lexicon.
declare class Lexicon {
    constructor(parent: typeof RiTa, custom?: object);
    /** the underlying word -> [phones, pos] map */
    data: Record<string, [string, string]>;
    hasWord(word: string, opts?: { noDerivations?: boolean }): boolean;
    randomWord(pattern?: string | RegExp, opts?: {
        minLength?: number;
        maxLength?: number;
        numSyllables?: number;
        limit?: number;
        pos?: string;
        type?: string;
        shuffle?: boolean;
    }): string;
    searchSync(pattern?: string | RegExp, options?: {
        minLength?: number;
        maxLength?: number;
        numSyllables?: number;
        limit?: number;
        shuffle?: boolean;
        pos?: string;
        type?: string;
    }): string[];
    rhymesSync(theWord: string, opts?: object): string[];
    alliterationsSync(theWord: string, opts?: object): string[];
    spellsLikeSync(word: string, options?: object): string[];
    soundsLikeSync(word: string, opts?: object): string[];
    isAlliteration(word1: string, word2: string): boolean;
    isRhyme(word1: string, word2: string): boolean;
    isMassNoun(word: string): boolean;
    rawPhones(word: string, opts?: object): string;
    minEditDist(source: string, target: string): number;
    size(): number;
}

// Not exported: reachable as RiTa.conjugator.
declare class Conjugator {
    constructor(parent: typeof RiTa);
    conjugate(verb: string, args?: object | string): string;
    unconjugate(word: string, opts?: object): string | undefined;
    presentPart(theVerb: string): string;
    pastPart(theVerb: string): string;
    toString(): string;
}

// Not exported: reachable as RiTa.randomizer.
declare class RandGen {
    constructor();
    seed(num: number): void;
    /** random() -> 0..1, random(k) -> 0..k, random(j,k) -> j..k, random(arr) -> item */
    random(...args: any[]): any;
    randomBias(min: number, max: number, bias: number, influence?: number): number;
    shuffle<T>(arr: T[]): T[];
    randomOrdering(arg: any[] | number): any[];
    /** returns the selected index */
    pselect(probs: number[]): number;
    /** returns the selected key */
    pselectObj(dist: Record<string, number>): string;
    pselectIndex(probs: number[]): number;
    pselect2(weightsArray: number[]): number;
    ndist(weights: number[], temp?: number): number[];
}

export type {
    BackoffModel, SuffixArray, RiMarkov,
    Stemmer, SuffixGram, Tagger, Analyzer, Concorder,
    Tokenizer, Inflector, Lexicon, Conjugator, RandGen,
    RiGrammar, RiScript,
};
