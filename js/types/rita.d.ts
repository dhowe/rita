export class RiTa {
    static grammar(rules?: object, context?: object): any;
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

    static randomizer: { seed(n: number): void; random(...args: any[]): number; pselect<T>(arr: T[]): T; pselectIndex(arr: number[]): number; pselect2(arr: number[]): number; ndist(weights: number[], temp?: number): number[]; randomOrdering<T>(arr: T[]): T[]; };
    static RiMarkov: typeof RiMarkov;
    static BackoffModel: typeof BackoffModel;
    static SuffixArray: typeof SuffixArray;

    static VERSION: string;
    static SILENT: boolean;
    static SILENCE_LTS: boolean;
    static SPLIT_CONTRACTIONS: boolean;

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

export class BackoffModel {
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

export class SuffixArray {
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
