import Stemmer from './stemmer.js';
import Tokenizer from './tokenizer.js';
import Conjugator from './conjugator.js';
import Lexicon from './lexicon.js';
import Tagger from './tagger.js';
import Inflector from './inflector.js';
import Analyzer from './analyzer.js';
import Concorder from './concorder.js';
import RandGen from './randgen.js';
import RiMarkov from './markov.js';
import SuffixArray  from './suffixes.js';

import SuffixGram from './model.js';
import BackoffModel from './backoff.js';

import { RiScript, RiGrammar } from 'riscript';

/** @module rita */

/**
 * @class RiTa
 * @memberof module:rita  
 */
class RiTa {

  /**
   * Create a RiTa grammar instance
   * @param {object} [rules] - the rules of the grammar
   * @param {object} [context] - the context of the grammar
   * @param {object} [options] - options for the grammar
   * @returns {RiGrammar} - a new RiGrammar instance
   */
  static grammar(rules, context, options) {
    return new RiGrammar(rules, context, { ...options, RiTa });
  }

  /**
   * Add a transform function to the RiScript parser
   * @param {string} name - the name of the transform
   * @param {function} definition - the transform function
   */
  static addTransform(name, definition) {
    RiTa.riscript.addTransform(name, definition);
  }

  /**
   * Remove a transform function from the RiScript parser
   * @param {string} name - the name of the transform to remove
   */
  static removeTransform(name) {
    RiTa.riscript.removeTransform(name);
  }

  /**
   * Returns the names of all current transform functions
   * @returns {string[]} the names of all transforms
   */
  static getTransforms() {
    return RiTa.riscript.getTransforms();
  }

  /**
   * Adds the appropriate article ('a' or 'an') to the word, according to its phonemes (useful as a transform function)
   * @param {string} word - the word to transform
   * @returns {string} - the word with an article, e.g., 'honor' -> 'an honor'
   */
  static articlize(word) {
    // @ts-ignore
    return RiScript.articlize(word, RiTa);
  }

  /**
   * Evaluates the input script via the RiScript parser
   * @param {string} script - the script to evaluate
   * @param {object} [context] - the context to evaluate the script ing
   * @param {object} [options] - options for the evaluation
   * @param {boolean} [options.trace] - whether to trace the evaluation
   * @returns {string} the result of the evaluation
   */
  static evaluate(script, context, options) {
    return RiTa.riscript.evaluate(script, context, { ...options });
  }

  /**
   * Creates a new RiMarkov object
   * @param {number} n - an int representing the n-factor of the markov chain 
   * @param {object} [options] - options for the markov chain
   * @param {string|string[]} [options.text] - a text string, or array of sentences, to add to the model (same as via model.addText()
   * @param {number} [options.maxLengthMatch] - # of words allowed in result to match a sequence in the input, default=∞
   * @param {number} [options.maxAttempts=999] - max attempts before to complete one ore more generations before erroring, default=999
   * @param {function} [options.tokenize] - custom tokenizer with tokenize() method, defaults to RiTa.tokenize()
   * @param {function} [options.untokenize] - custom untokenizer with untokenize() method, defaults to RiTa.untokenize()
   * @param {boolean} [options.disableInputChecks=false] - if true, allow result to be present in the input, default
   * @param {boolean} [options.trace] - output trace info to the console
   * @returns {RiMarkov}
   */
  static markov(n, options) {
    return new RiMarkov(n, options);
  }

  /**
   * Return a list of occurrences of the key word in the Key-Word-In-Context (KWIC) model.
   * @overload
   * @param {string} keyword 
   * @param {object} [options]  
   * @param {number} [options.numWords] - the number of words to include in the context
   * @param {string} [options.text] - the text as input for the KWIC model
   * @param {string[]} [options.words] - the array of words to be used as input for the KWIC model
   * @returns {string[]} all the occurrences of the keyword in the model, each with no more 
   * than 'numWords' words of context on either side
   * @overload
   * @param {string} keyword
   * @param {number} text - the number of words to include in the context
   * @returns {string[]} all the occurrences of the keyword in the model, each with no more 
   * than 'numWords' words of context on either side
   */
  static kwic(keyword, options) {
    return RiTa.concorder.kwic(keyword, options);
  }

  /**
   * Creates a concordance, a list of words with their frequency of occurence, from the given text and options.
   * @param {string} text - the text from which to create the concordance
   * @param {object} [options] - options for the concordance
   * @param {boolean} [options.ignoreCase=false] - whether to ignore case when creating the concordance
   * @param {boolean} [options.ignoreStopWords=false] - whether to ignore stop words like
   *  'the', 'and', 'a', 'of', etc, as specified in RiTa.STOP_WORDS
   * @param {boolean} [options.ignorePunctuation=false] - whether to ignore punctuation when creating the concordance
   * @param {string[]} [options.wordsToIgnore=null] - words to ignore when creating the concordance (alternate stop-words)
   * @returns {object} the concordance, an object with words as keys and frequencies as values
   */
  static concordance(text, options) {
    return RiTa.concorder.concordance(text, options);
  }

  /**
   * Returns a random ordering of the input array or a random ordering of integers from 1 to k
   * @overload
   * @param {object[]} array - the array to shuffle
   * @returns {object[]} the input array in a random order
   * @overload
   * @param {number} k - the number of integers to return
   * @returns {number[]} an array of arrays of integers from 1 to k in random order 
   */
  static randomOrdering(arrayOrInt) {
    return RiTa.randomizer.randomOrdering(arrayOrInt);
  }

  /**
   * Sets the seed for the RiTa random number generator
   * @param {number} seed - the seed to set 
   */
  static randomSeed(seed) {
    RiTa.randomizer.seed(seed);
  }

  /**
   * Returns true if the sentence is a question, else false
   * @param {string} sentence 
   * @returns {boolean} - true if the sentence is a question, else false
   */
  static isQuestion(sentence) {
    return RiTa.QUESTIONS_SET.has
      (RiTa.tokenize(sentence)[0].toLowerCase());
  }

  /**
   * Returns true if the character is a vowel, else false
   * @param {string} char 
   * @returns {boolean} - true if the character is a vowel, else false
   */
  static isVowel(char) {
    return !!(char && char.length === 1 && RiTa.VOWELS.includes(char.toLowerCase()));
  }

  /**
   * Returns true if the character is a consonant, else false
   * @param {string} char 
   * @returns {boolean} - true if the character is a consonant, else false
   */
  static isConsonant(char) {
    return !!(char && char.length === 1 && !RiTa.VOWELS.includes(char.toLowerCase())
      && IS_LETTER.test(char.toLowerCase()));
  }

  /**
   * Capitalizes the first letter of the input string, leaving others unchanged
   * @param {string} string - the string to capitalize
   * @returns {string} the capitalized string
   */
  static capitalize(string) {
    return string ? string[0].toUpperCase() + string.substring(1) : '';
  }

  /**
   * Return a random word from the lexicon matching the specified criteria 
   * (length, syllable-count, phonemic pattern, stress pattern, part-of-speech, etc.).
   * @param {(string|RegExp)} [pattern] - the pattern to match
   * @param {object} [options] 
   * @param {number} [options.minLength=4] - the minimum length of the word
   * @param {number} [options.maxLength=-1] - the maximum length of the word
   * @param {number} [options.numSyllables=null] - the number of syllables in the word 
   * @param {number} [options.limit=10] - the maximum number of results to retur   
   * @param {string} [options.pos=null] - the part-of-speech of the word to return,
   *  either from the Penn tag set or the simplified tag set [a, r, v, n]
   * @param {RegExp} [options.pattern=null] - the spelling or phonemic pattern to match
   * @param {string} [options.type=null] - the type of regex or string pattern to match, 
   * options are 'stresses' or 'phones' or 'letters' (the default)
   * @returns {string} a random word matching the criteria in the options object 
   */
  static randomWord(pattern, options) {
    return RiTa.lexicon.randomWord(pattern, options);
  }

  /**
   * Returns words that rhyme with the given word. Two words are considered as rhyming if
   * their final stressed vowel and all following phonemes are identical.
   * @param {string} word 
   * @param {object} [options]
   * @param {number} [options.minLength=4] - the minimum length of the words
   * @param {number} [options.maxLength] - the maximum length of the words
   * @param {number} [options.numSyllables] - the number of syllables in the words 
   * @param {number} [options.limit=10] - the maximum number of results to return (pass -1 to return all matches)
   * @param {boolean} [options.shuffle=false] - whether to shuffle the results before returning them
   * @param {string} [options.pos] - the part-of-speech of the words to return, either from the Penn tag set
   *  or the simplified tag set [a, r, v, n]
   * @returns {Promise<string[]>} an array of rhymes that match criteria in the options object 
   */
  static async rhymes(word, options) {
    return await RiTa.lexicon.rhymes(word, options);
  }

  /**
   * Returns words that rhyme with the given word. Two words are considered as rhyming if
   * their final stressed vowel and all following phonemes are identical.
   * @param {string} word1 - the first word to compare
   * @param {string} word2 - the second word to compare
   * @returns {boolean}  true if the two words rhyme, else false
   */
  static isRhyme(word1, word2) {
    return RiTa.lexicon.isRhyme(word1, word2);
  }


  /**
   * Finds alliterations by comparing the phonemes of the input string to those
   *  of each word in the lexicon via a minimum-edit-distance metric.
   * @param {string} word 
   * @param {object} [options]
   * @param {number} [options.minLength=4] - the minimum length of the words
   * @param {number} [options.maxLength] - the maximum length of the words
   * @param {number} [options.numSyllables] - the number of syllables in the words 
   * @param {number} [options.limit=10] - the maximum number of results to return (pass -1 to return all matches)
   * @param {boolean} [options.shuffle=false] - whether to shuffle the results before returning them
   * @param {string} [options.pos] - the part-of-speech of the words to return, either from the Penn tag set
   *  or the simplified tag set [a, r, v, n]
   * @returns {Promise<string[]>} an array of alliterations matching criteria in the options object 
   */
  static async alliterations(word, options) {
    return await RiTa.lexicon.alliterations(word, options);
  }

  /**
   * Returns true if the word is in the lexicon, else false
   * @param {string} word - the word to check
   * @param {object} [options] - options for the search
   * @param {boolean} [options.noDerivations=false] - whether to ignore derivations and only search for raw words
   * @returns {boolean} true if the word is in the lexicon, else false
   */
  static hasWord(word, options) {
    return RiTa.lexicon.hasWord(word, options);
  }

  /**
   * Returns true if the word is an abbreviation, else false
   * @param {string} input - the word to check
   * @param {object} [options] - options for the search
   * @param {boolean} [options.caseSensitive=false] - whether to ignore case when checking for abbreviations
   * @returns {boolean} true if the word is an abbreviation, else false
   */
  static isAbbrev(input, options) {
    if (typeof input === 'string') {
      if (options?.caseSensitive) return RiTa.ABRV.includes(input.trim());
      let check = input.trim().toLowerCase();
      return RiTa.ABRV.some(a => a.toLowerCase() === check);
    }
    return false;
  }

  /**
   * Returns true if the two words are an alliteration (if their first stressed consonants match). 
   * Note: returns true if wordA.equals(wordB) and false if either (or both) are null.
   * @param {string} word1 - the first word to compare
   * @param {string} word2 - the second word to compare
   * @returns {boolean}  true if the two words are an alliteration, else false
   */
  static isAlliteration(word1, word2) {
    return RiTa.lexicon.isAlliteration(word1, word2);
  }

  /**
   * Compares the letters of the input word (using a version of the Levenstein min-edit distance algorithm) 
   * to each word in the lexicon, returning the set of closest matches that also match the criteria in the options object.
   * @param {string} word - the word to match
   * @param {object} [options] - options for the search
   * @param {number} [options.minLength=4] - the minimum length of the words
   * @param {number} [options.maxLength] - the maximum length of the words
   * @param {number} [options.numSyllables] - the number of syllables in the words 
   * @param {number} [options.limit=10] - the maximum number of results to return  (pass -1 to return all matches) 
   * @param {boolean} [options.shuffle=false] - whether to shuffle the results before returning them
   * @param {string} [options.pos] - the part-of-speech of the words to return, either from the Penn tag set or the simplified tag set [a, r, v, n]
   * @returns {Promise<string[]>} an array of words matching the spelling pattern and criteria in the options object 
   */
  static async spellsLike(word, options) {
    return await RiTa.lexicon.spellsLike(word, options);
  }

  /**
   * Compares the phonemes of the input pattern (using a version of the Levenstein min-edit distance algorithm)
   *  to each word in the lexicon, returning the set of closest matches that also match the criteria in the options object.
   * @param {string} word - the word to match
   * @param {object} [options] - options for the search
   * @param {number} [options.minLength=4] - the minimum length of the words
   * @param {number} [options.maxLength] - the maximum length of the words
   * @param {number} [options.numSyllables] - the number of syllables in the words 
   * @param {number} [options.limit=10] - the maximum number of results to return (pass -1 to return all matches)
   * @param {boolean} [options.shuffle=false] - whether to shuffle the results before returning them
   * @param {boolean} [options.matchSpelling=false] if true will also attempt to match spelling by returning an intersection with RiTa.spellsLike()
   * @param {string} [options.pos] - the part-of-speech of the words to return, either from the Penn tag set
   *  or the simplified tag set [a, r, v, n]
   * @returns {Promise<string[]>} an array of words matching the phonemic pattern and criteria in the options object 
   */
  static async soundsLike(word, options) {
    return await RiTa.lexicon.soundsLike(word, options);
  }

  /**
   * Generates part-of-speech tags for each word in the input with tags 
   * from the Penn tag set or the simplified tag set [a, r, v, n].
   * @param {(string|string[])} word - the word or words to tag
   * @param {object} [options] - options for the tagging
   * @param {boolean} [options.simple] - use simple tags (noun=n,verb=v,adverb=a,adjective=r)
   * @returns {string|string[]} - an array of part-of-speech tags for each word in the input
   */
  static pos(word, options) {
    if (options && 'inline' in options) {
      throw Error('Use RiTa.posInline() instead');
    }
    return RiTa.tagger.tag(word, options);
  }

  /**
   * Returns true if the word has a noun form. That is, if any of its possible
   *  parts of speech are any variant of a noun in the Penn tag set(e.g. nn, nns, nnp, nnps).
   * @param {string} word - the word to check
   * @returns {string} - true if the word is a noun, else false
   */
  static isNoun(word) {
    return RiTa.tagger.isNoun(word);
  }

  /**
   * Returns true if word has an adjective form. That is, if any of its possible parts of speech
   *  are any variant of an adjective in the Penn tag set (e.g. jj, jjr, jjs).
   * @param {string} word - the word to check
   * @returns {string} - true if the word is an adjective, else false
   */
  static isAdjective(word) {
    return RiTa.tagger.isAdjective(word);
  }

  /**
   * Returns true if the word has an adverb form. That is, if any of its possible parts of speech 
   * are any variant of an adverb in the Penn tag set (e.g. rb, rbr, rbs).
   * @param {string} word - the word to check
   * @returns {string} - true if the word is an adverb, else false
   */
  static isAdverb(word) {
    return RiTa.tagger.isAdverb(word);
  }

  /**
   * Returns true for if word has a verb form. That is, if any of its possible 
   * parts of speech are any variant of a verb in the Penn tag set (e.g. vb, vbg, vbd, vbp, vbz).
   * @param {string} word - the word to check
   * @returns {string} - true if the word is a verb, else false
   */
  static isVerb(word) {
    return RiTa.tagger.isVerb(word);
  }

  /**
   * Returns true if every character of 'text' is a punctuation character.
   * @param {string} text 
   * @returns {boolean} true if every character of 'text' is punctuation, else false
   */
  static isPunct(text) {
    return !!(text && text.length && ONLY_PUNCT.test(text));
  }


  /**
   * Tags the input string with part-of-speech tags, either from the Penn tag set or the simplified tag set [a, r, v, n].
   * @param {string} sentence - the sentence to tag
   * @param {object} [options] - options for the tagging
   * @param {boolean} [options.simple=false] - use the simplified tag set [a, r, v, n]
   * @returns {string} the tagged sentence
   */
  static posInline(sentence, options) {
    return RiTa.tagger.tag(sentence, { ...options, inline: true });
  }

  /**
   * Return the singular form of the input word
   * @param {string} word - the word to singularize
   * @returns {string} the singular form of the input word
   */
  static singularize(word) {
    return RiTa.inflector.singularize(word);
  }

  /**
   * Return the plural form of the input word
   * @param {string} word - the word to pluralize
   * @returns {string} the plural form of the input word
   */
  static pluralize(word) {
    return RiTa.inflector.pluralize(word);
  }

  /**
   * Searches for words in the lexicon matching the given criteria, either by length, syllable-count, 
   * spelling, phonemes, stresses, part-of-speech, etc. If no regex or options are supplied, the full set of words is returned.
   * @param {(string|RegExp)} [pattern] - the pattern to match
   * @param {object} [options] - options for the search
   * @param {number} [options.minLength=4] - the minimum length of the words
   * @param {number} [options.maxLength] - the maximum length of the words
   * @param {number} [options.numSyllables] - the number of syllables in the words 
   * @param {number} [options.limit=10] - the maximum number of results to return (pass -1 to return all matches)
   * @param {boolean} [options.shuffle=false] - whether to shuffle the results before returning them
   * @param {string} [options.pos] - the part-of-speech of the words to return, either from the Penn tag set
   *  or the simplified tag set [a, r, v, n]
   * @param {string} [options.type] - the type of regex or string pattern to match, options are 'stresses'
   *  or 'phones' or 'letters' (the default)
   * @returns {Promise<string[]>} an array of words matching the criteria in both the pattern and the options object 
   */
  static async search(pattern, options) {
    return await RiTa.lexicon.search(pattern, options);
  }

  /**
    * Returns an array containing all unique alphabetical words (tokens) in the text.
    * Punctuation and case are ignored unless specified otherwise.
    * @param {string} text - The text from which to extract the tokens
    * @param {object} [options] - The options
    * @param {boolean} [options.caseSensitive=false] - Whether to pay attention to case
    * @param {boolean} [options.ignoreStopWords=false] - Whether to ignore words such as 'the', 'and', 'a', 'of', etc,
    *  as specified in RiTa.STOP_WORDS
    * @param {boolean} [options.splitContractions=false] - Whether to convert contractions
    *  (e.g., "I'd" or "she'll") into multiple individual tokens
    * @param {boolean} [options.includePunct=false] - Whether to include punctuation in the results
    * @param {boolean} [options.sort=false] - Whether to sort the tokens before returning them
    * @returns {string[]} Array of tokens
    */
  static tokens(text, options = {
    caseSensitive: false,
    ignoreStopWords: false,
    splitContractions: false,
    includePunct: false,
    sort: false
  }) {
    return RiTa.tokenizer.tokens(text, options);
  }


  /**
   * Tokenizes an input string into words, according to the Penn Treebank conventions
   * @param {string} input - The text to tokenize
   * @param {object} [options] - The options
   * @param {RegExp} [options.regex=null] - An optional custom regex to split on
   * @param {boolean} [options.splitHyphens=false] - Whether to split hyphenated words 
   * (e.g., "mother-in-law") into multiple individual tokens
   * @param {boolean} [options.splitContractions=false] - Whether to split contractions 
   * (e.g., "I'd" or "she'll") into multiple individual tokens
   * @returns {string[]} Array of tokens
   */
  static tokenize(input, options) {
    return RiTa.tokenizer.tokenize(input, options);
  }

  /**
   * Joins an array (of words and punctuation) into a sentence, according to 
   * the Penn Treebank conventions. The inverse of RiTa.tokenize().
   * @param {string[]} input - The array of words to join
   * @param {string} [delim=' '] - The delimiter to use between words, or a space by default
   * @returns {string} The joined sentence
   */
  static untokenize(input, delim = ' ') {
    return RiTa.tokenizer.untokenize(input, delim);
  }

  /**
   * Split the input text into sentences following using Penn Treebank conventions and the specified options.
   * @param {string} text - The text to split
   * @param {(string|RegExp)} [pattern] - An optional custom regex to split on
   * @returns {string[]} An array of sentences
   */
  static sentences(text, pattern) {
    return RiTa.tokenizer.sentences(text, pattern);
  }

  /**
   * Returns true if the word is a 'stop word', a commonly used word that is often ignored in text processing. 
   * To use your own list, set RiTa.STOP_WORDS to a new array of (lowercase) words.
   * @param {string} word - the word to check
   * @returns {boolean} true if the word is a stop word, else false
   */
  static isStopWord(word) {
    return RiTa.STOP_WORDS_SET.has(word.toLowerCase());
  }

  /**
   * Extracts base roots from a word according to the Pling stemming algorithm.
   * @param {string} word - the word to stem 
   * @returns {string} the base root of the word
   */
  static stem(word) {
    return Stemmer.stem(word);
  }

  /**
   * Returns the present participle of the input word (e.g., "walking" for "walk").
   * @param {string} verbWord - the word to get the present participle of
   * @returns {string} the present participle of the input word
   */
  static presentPart(verbWord) {
    return RiTa.conjugator.presentPart(verbWord);
  }

  /**
   * Returns the past participle of the input word (e.g., "walked" for "walk").
   * @param {string} verbWord 
   * @returns {string} the past participle of the input word
   */
  static pastPart(verbWord) {
    return RiTa.conjugator.pastPart(verbWord);
  }

  /**
   * Conjugates the 'verb' according to the specified options (tense, person, number, etc.)
   * @param {string} verbWord 
   * @param {object} [options]
   * @param {number} [options.tense] - the tense of the verb, either RiTa.PAST, RiTa.PRESENT, or RiTa.FUTURE
   * @param {number} [options.person] - the person of the verb, either RiTa.FIRST, RiTa.SECOND, or RiTa.THIRD
   * @param {number} [options.number] - the number of the verb, either RiTa.SINGULAR or RiTa.PLURAL
   * @param {number} [options.form] - the form of the verb, either RiTa.INFINITIVE or RiTa.GERUND
   * @param {boolean} [options.passive] - whether the verb should be passive
   * @param {boolean} [options.progressive] - whether the verb should be progressive
   * @param {boolean} [options.perfect] - whether the verb should be perfect
   * @param {boolean} [options.interrogative] - whether the verb should be in interrogative form
   * @returns {string} the conjugated verb
   */
  static conjugate(verbWord, options) {
    return RiTa.conjugator.conjugate(verbWord, options);
  }

  /**
   * Analyzes the input and returns a new string containing the stresses for each syllable of the input text .
   * @param {string} input - the text to analyze
   * @param {object} [options] - options for the analysis
   * @returns {string} a string containing the stresses for each syllable of the input text
   */
  static stresses(input, options) {
    return RiTa.analyzer.analyze(input, options).stresses;
  }

  /**
   * Analyzes the input and returns a new string containing the syllables of the input text.
   * @param {string} input - the text to analyze
   * @param {object} [options] - options for the analysis
   * @returns {string} a string containing the syllables of the input text
   */
  static syllables(input, options) {
    const result = RiTa.analyzer.analyze(input, options);
    if (options && options.ipaPhones) {
      return Analyzer.syllablesToIpa(result.syllables, result.stresses, true);
    }
    return result.syllables;
  }

  /**
   * Analyzes the input and returns a new string containing the phonemes of the input text.
   * @param {string} input - the text to analyze
   * @param {object} [options] - options for the analysis
   * @returns {string} a string containing the phones of the input text
   */
  static phones(input, options) {
    const result = RiTa.analyzer.analyze(input, options);
    if (options && options.ipaPhones) {
      return Analyzer.syllablesToIpa(result.syllables, result.stresses);
    }
    return result.phones;
  }

  /**
   * Analyzes the input to compute a set of features for the input,
   * including phonemes, syllables, stresses, and part-of-speech tags.
   * @param {string} input - the text to analyze
   * @param {object} [options] - options for the analysis
   * @param {boolean} [options.simple=false] - whether to use the simplified tag set [a, r, v, n]
   * @param {boolean} [options.ipaPhones=false] - whether to return phones in IPA format instead of Arpabet
   * @returns {object} an object containing the features of the input text (phones, syllables, stresses, pos), or the features inline
   */
  static analyze(input, options) {
    const result = RiTa.analyzer.analyze(input, options);
    if (options && options.ipaPhones) {
        result.phones = Analyzer.syllablesToIpa(result.syllables, result.stresses);
    }
    return result;
  }

  ////////////////////////////// lex-sync ////////////////////////////

  /**
   * A synchronous version of RiTa.spellsLike(). It compares the letters of the input word 
   * (using a version of the Levenstein min-edit distance algorithm) to each word in the lexicon,
   *  returning the set of closest matches that also match the criteria in the options object.
   * @param {string} word - the word to match
   * @param {object} [options] - options for the search
   * @param {number} [options.minLength=4] - the minimum length of the words
   * @param {number} [options.maxLength] - the maximum length of the words
   * @param {number} [options.numSyllables] - the number of syllables in the words
   * @param {number} [options.limit=10] - the maximum number of results to return (pass -1 to return all matches)
   * @param {string} [options.pos] - the part-of-speech of the words to return, either from the Penn tag set
   * or the simplified tag set [a, r, v, n]
   * @param {boolean} [options.shuffle=false] - whether to shuffle the results before returning them
   * @return {string[]} an array of words matching the spelling pattern and criteria in the options object
   */
  static spellsLikeSync(word, options) {
    return RiTa.lexicon.spellsLikeSync(word, options);
  }

  /**
   * A synchronous version of RiTa.lexicon.soundsLike(). It compares the phonemes of the input pattern (using a version of the Levenstein min-edit distance algorithm)
   *  to each word in the lexicon, returning the set of closest matches that also match the criteria in the options object.
   * @param {string} word - the word to match
   * @param {object} [options] - options for the search
   * @param {number} [options.minLength=4] - the minimum length of the words
   * @param {number} [options.maxLength] - the maximum length of the words
   * @param {number} [options.numSyllables] - the number of syllables in the words 
   * @param {number} [options.limit=10] - the maximum number of results to return (pass -1 to return all matches)
   * @param {boolean} [options.matchSpelling=false] if true will also attempt to match spelling by returning an intersection with RiTa.spellsLike()
   * @param {boolean} [options.shuffle=false] - whether to shuffle the results before returning them
   * @param {string} [options.pos] - the part-of-speech of the words to return, either from the Penn tag set
   *  or the simplified tag set [a, r, v, n]
   * @return {string[]} an array of words matching the phonemic pattern and criteria in the options object 
   */
  static soundsLikeSync(word, options) {
    return RiTa.lexicon.soundsLikeSync(word, options);
  }

  /**
   * Synchronous version of RiTa.rhymes(). Returns words that rhyme with the given word. 
   * Two words are considered as rhyming if their final stressed vowel and all following phonemes are identical.
   * @param {string} word - the word to match
   * @param {object} [options] - options for the search
   * @param {number} [options.minLength=4] - the minimum length of the words
   * @param {number} [options.maxLength] - the maximum length of the words
   * @param {number} [options.numSyllables] - the number of syllables in the words
   * @param {number} [options.limit=10] - the maximum number of results to return (pass -1 to return all matches)
   * @param {boolean} [options.shuffle=false] - whether to shuffle the results before returning them
   * @param {string} [options.pos] - the part-of-speech of the words to return, either from the Penn tag set  
   * or the simplified tag set [a, r, v, n]
   * @return {string[]} an array of rhymes that match criteria in the options object
   */
  static rhymesSync(word, options) {
    return RiTa.lexicon.rhymesSync(word, options);
  }

  /**
   * A synchronous version of RiTa.search(). Searches for words in the lexicon matching
   *  the given criteria, either by length, syllable-count, spelling, phonemes, stresses, 
   * part-of-speech, etc.
   * @param {(string|RegExp)} [pattern] - the pattern to match
   * @param {object} [options] - options for the search
   * @param {number} [options.minLength=4] - the minimum length of the words
   * @param {number} [options.maxLength] - the maximum length of the words
   * @param {number} [options.numSyllables] - the number of syllables in the words
   * @param {number} [options.limit=10] - the maximum number of results to return (pass -1 to return all matches)
   * @param {boolean} [options.shuffle=false] - whether to shuffle the results before returning them
   * @param {string} [options.pos] - the part-of-speech of the words to return, either from the Penn tag set
   * or the simplified tag set [a, r, v, n]
   * @param {string} [options.type] - the type of regex or string pattern to match, options are 'stresses' or 'phones' or 'letters' (the default)
   * @return {string[]} an array of words matching the criteria in both the pattern and the options object
   */
  static searchSync(pattern, options) {
    return RiTa.lexicon.searchSync(pattern, options);
  }

  /**
   * A synchronous version of RiTa.alliterations(). Finds alliterations by comparing the phonemes
   * of the input string to those of each word in the lexicon via a minimum-edit-distance metric.
   * @param {string} word - the word to match
   * @param {object} [options] - options for the search
   * @param {number} [options.minLength=4] - the minimum length of the words
   * @param {number} [options.maxLength] - the maximum length of the words
   * @param {number} [options.numSyllables] - the number of syllables in the words
   * @param {number} [options.limit=10] - the maximum number of results to return (pass -1 to return all matches)
   * @param {boolean} [options.shuffle=false] - whether to shuffle the results before returning them
   * @param {string} [options.pos] - the part-of-speech of the words to return, either from the Penn tag set
   *  or the simplified tag set [a, r, v, n]
   * @return {string[]} an array of alliterations matching criteria in the options object
   */
  static alliterationsSync(word, options) {
    return RiTa.lexicon.alliterationsSync(word, options);
  }

  ////////////////////////////// niapa /////////////////////////////

  /**
   * Returns a random integer from a range
   * The version of random() with one parameter returns a random integer from 0 up to but not including the number. 
   * The version of random() with two parameters returns a random integer from the first number up to but not including the second.
   * @param {number} param1 - the first parameter
   * @param {number} [param2] - the second optional parameter
   * @returns {number} a random integer from the range
   */
  static randi(param1, param2) {
    return Math.floor(RiTa.random(...arguments)); // keep args
  }

  /**
   * Returns a random number or a random element from an array.
   * The version of random() with no parameters returns a random number from 0 up to but not including 1.
   * The version of random() with one parameter works one of two ways. If the argument passed is a number, random() returns a random number from 0 up to but not including the number. 
   * If the argument passed is an array, random() returns a random element from that array.
   * The version of random() with two parameters returns a random number from the first number up to but not including the second.   
   * @param {number|object[]} [param1] - the minimum value of the random number, or an array of values to choose from
   * @param {number} [param2] - the maximum value of the random number
   * @returns {number|object} a random number or a random element from the array
   */
  static random(param1, param2) {
    return RiTa.randomizer.random(...arguments); // keep args
  }
}

// CLASSES (for testing)
RiTa.RiGrammar = RiGrammar;
RiTa.RiMarkov = RiMarkov;
RiTa.Stemmer = Stemmer;

// INTERNAL Markov classes
RiTa.Model = SuffixGram;
RiTa.BackoffModel = BackoffModel;
RiTa.SuffixArray = SuffixArray;

// COMPONENTS
RiTa.randomizer = new RandGen();
RiTa.tagger = new Tagger(RiTa);
RiTa.analyzer = new Analyzer(RiTa);
RiTa.concorder = new Concorder(RiTa);
RiTa.tokenizer = new Tokenizer(RiTa);
RiTa.inflector = new Inflector(RiTa);
RiTa.lexicon = new Lexicon(RiTa);
RiTa.conjugator = new Conjugator(RiTa);

// BACKREFS
RiMarkov.RiTa = RiTa;
RiTa.Model.RiTa = RiTa;
SuffixArray.RiTa = RiTa;
Stemmer.tokenizer = RiTa.tokenizer;

// MESSAGES
RiTa.SILENT = false;
RiTa.SILENCE_LTS = false;

// Enable the per-word phone cache in Analyzer (parity with the Java impl)
RiTa.CACHING = true;

// CONSTANTS
RiTa.VERSION = '[VI]{{inject}}[/VI]'; // injected by build script
RiTa.FIRST = 1;
RiTa.SECOND = 2;
RiTa.THIRD = 3;
RiTa.PAST = 4;
RiTa.PRESENT = 5;
RiTa.FUTURE = 6;
RiTa.SINGULAR = 7;
RiTa.PLURAL = 8;
RiTa.NORMAL = 9;
RiTa.STRESS = '1';
RiTa.NOSTRESS = '0';
RiTa.PHONE_BOUNDARY = '-';
RiTa.WORD_BOUNDARY = " ";
RiTa.SYLLABLE_BOUNDARY = "/";
RiTa.SENTENCE_BOUNDARY = "|";
RiTa.VOWELS = "aeiou";

// RiTa.MODAL_EXCEPTIONS = ["hardness", "shortness"];
RiTa.PHONES = ['aa', 'ae', 'ah', 'ao', 'aw', 'ay', 'b', 'ch', 'd', 'dh', 'eh', 'er', 'ey', 'f', 'g', 'hh', 'ih', 'iy', 'jh', 'k', 'l', 'm', 'n', 'ng', 'ow', 'oy', 'p', 'r', 's', 'sh', 't', 'th', 'uh', 'uw', 'v', 'w', 'y', 'z', 'zh'];
RiTa.ABRV = ["Adm.", "Capt.", "Cmdr.", "Col.", "Dr.", "Gen.", "Gov.", "Lt.", "Maj.", "Messrs.", "Mr.", "Mrs.", "Ms.", "Prof.", "Rep.", "Reps.", "Rev.", "Sen.", "Sens.", "Sgt.", "Sr.", "St.", "A.k.a.", "C.f.", "I.e.", "E.g.", "Vs.", "V.", "Jan.", "Feb.", "Mar.", "Apr.", "Mar.", "Jun.", "Jul.", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."];
RiTa.QUESTIONS = ["was", "what", "when", "where", "which", "why", "who", "will", "would", "who", "how", "if", "is", "could", "might", "does", "are", "have"];
RiTa.STOP_WORDS = ["and", "a", "of", "in", "i", "you", "is", "to", "that", "it", "for", "on", "have", "with", "this", "be", "not", "are", "as", "was", "but", "or", "from", "my", "at", "if", "they", "your", "all", "he", "by", "one", "me", "what", "so", "can", "will", "do", "an", "about", "we", "just", "would", "there", "no", "like", "out", "his", "has", "up", "more", "who", "when", "don't", "some", "had", "them", "any", "their", "it's", "only", "which", "i'm", "been", "other", "were", "how", "then", "now", "her", "than", "she", "well", "also", "us", "very", "because", "am", "here", "could", "even", "him", "into", "our", "much", "too", "did", "should", "over", "want", "these", "may", "where", "most", "many", "those", "does", "why", "please", "off", "going", "its", "i've", "down", "that's", "can't", "you're", "didn't", "another", "around", "must", "few", "doesn't", "the", "every", "yes", "each", "maybe", "i'll", "away", "doing", "oh", "else", "isn't", "he's", "there's", "hi", "won't", "ok", "they're", "yeah", "mine", "we're", "what's", "shall", "she's", "hello", "okay", "here's", "less", "didn't", "said", "over", "this", "that", "just", "then", "under", "some"];
RiTa.MASS_NOUNS = ["abalone", "asbestos", "barracks", "bathos", "breeches", "beef", "britches", "chaos", "chinese", "cognoscenti", "clippers", "corps", "cosmos", "crossroads", "diabetes", "ethos", "gallows", "graffiti", "herpes", "innings", "lens", "means", "measles", "mews", "mumps", "news", "pasta", "pathos", "pincers", "pliers", "proceedings", "rabies", "rhinoceros", "sassafras", "scissors", "series", "shears", "species", "tuna", "acoustics", "aesthetics", "aquatics", "basics", "ceramics", "classics", "cosmetics", "dialectics", "deer", "dynamics", "ethics", "harmonics", "heroics", "mechanics", "metrics", "ooze", "optics", "physics", "polemics", "pyrotechnics", "statistics", "tactics", "tropics", "bengalese", "bengali", "bonsai", "booze", "cellulose", "mess", "moose", "burmese", "chinese", "colossus", "congolese", "discus", "electrolysis", "emphasis", "expertise", "flu", "fructose", "gauze", "glucose", "grease", "guyanese", "haze", "incense", "japanese", "lebanese", "malaise", "mayonnaise", "maltese", "music", "money", "menopause", "merchandise", "olympics", "overuse", "paradise", "poise", "potash", "portuguese", "prose", "recompense", "remorse", "repose", "senegalese", "siamese", "singhalese", "sleaze", "sioux", "sudanese", "suspense", "swiss", "taiwanese", "vietnamese", "unease", "aircraft", "anise", "antifreeze", "applause", "archdiocese", "apparatus", "asparagus", "bellows", "bison", "bluefish", "bourgeois", "bream", "brill", "butterfingers", "cargo", "carp", "catfish", "chassis", "clone", "clones", "clothes", "chub", "cod", "codfish", "coley", "contretemps", "crawfish", "crayfish", "cuttlefish", "dice", "dogfish", "doings", "dory", "downstairs", "eldest", "earnings", "economics", "electronics", "firstborn", "fish", "flatfish", "flounder", "fowl", "fry", "fries", "works", "goldfish", "golf", "grand", "grief", "haddock", "hake", "halibut", "headquarters", "herring", "hertz", "honey", "horsepower", "goods", "hovercraft", "ironworks", "kilohertz", "ling", "shrimp", "swine", "lungfish", "mackerel", "macaroni", "megahertz", "moorfowl", "moorgame", "mullet", "myrrh", "nepalese", "offspring", "pants", "patois", "pekinese", "perch", "pickerel", "pike", "potpourri", "precis", "quid", "rand", "rendezvous", "roach", "salmon", "samurai", "seychelles", "shad", "sheep", "shellfish", "smelt", "spaghetti", "spacecraft", "starfish", "stockfish", "sunfish", "superficies", "sweepstakes", "smallpox", "swordfish", "tennis", "tobacco", "triceps", "trout", "tunafish", "turbot", "trousers", "turf", "dibs", "undersigned", "waterfowl", "waterworks", "waxworks", "wildfowl", "woodworm", "yen", "aries", "pisces", "forceps", "jeans", "mathematics", "odds", "politics", "remains", "aids", "wildlife", "shall", "would", "may", "might", "ought", "should", "acne", "admiration", "advice", "air", "anger", "anticipation", "assistance", "awareness", "bacon", "baggage", "blood", "bravery", "chess", "clay", "clothing", "coal", "compliance", "comprehension", "confusion", "consciousness", "cream", "darkness", "diligence", "dust", "education", "empathy", "enthusiasm", "envy", "equality", "equipment", "evidence", "feedback", "fitness", "flattery", "foliage", "fun", "furniture", "garbage", "gold", "gossip", "grammar", "gratitude", "gravel", "guilt", "happiness", "hardware", "hate", "hay", "health", "heat", "help", "hesitation", "homework", "honesty", "honor", "honour", "hospitality", "hostility", "humanity", "humility", "ice", "immortality", "independence", "information", "integrity", "intimidation", "jargon", "jealousy", "jewelry", "justice", "knowledge", "literacy", "logic", "luck", "lumber", "luggage", "mail", "management", "milk", "morale", "mud", "nonsense", "oppression", "optimism", "oxygen", "participation", "pay", "peace", "perseverance", "pessimism", "pneumonia", "poetry", "police", "pride", "privacy", "propaganda", "public", "punctuation", "recovery", "rice", "rust", "satisfaction", "schnapps", "shame", "slang", "software", "stamina", "starvation", "steam", "steel", "stuff", "support", "sweat", "thunder", "timber", "toil", "traffic", "tongs", "training", "trash", "valor", "vehemence", "violence", "warmth", "waste", "weather", "wheat", "wisdom", "work", "accommodation", "advertising", "aid", "art", "bread", "business", "butter", "calm", "cash", "cheese", "childhood", "clothing ", "coffee", "content", "corruption", "courage", "currency", "damage", "danger"/*, "data"*/, "determination", "electricity", "employment", "energy", "entertainment", "failure", "fame", "fire", "flour", "food", "freedom", "friendship", "fuel", "genetics", "hair", "harm", "hospitality ", "housework", "humour", "imagination", "importance", "innocence", "intelligence", "juice", "kindness", "labour", "lack", "laughter", "leisure", "literature", "litter", "love", "magic", "metal", "motherhood", "motivation", "nature", "nutrition", "obesity", "oil", "old age", "paper", "patience", "permission", "pollution", "poverty", "power", "production", "progress", "pronunciation", "publicity", "quality", "quantity", "racism", "rain", "relaxation", "research", "respect", "room (space)", "rubbish", "safety", "salt", "sand", "seafood", "shopping", "silence", "smoke", "snow", "soup", "speed", "spelling", "stress ", "sugar", "sunshine", "tea", "time", "tolerance", "trade", "transportation", "travel", "trust", "understanding", "unemployment", "usage", "vision", "water", "wealth", "weight", "welfare", "width", "wood", "yoga", "youth", "homecare", "childcare", "fanfare", "healthcare", "medicare"];

RiTa.INFINITIVE = 1;
RiTa.GERUND = 2;

// For tokenization, Can't -> Can not, etc.
RiTa.SPLIT_CONTRACTIONS = false;

// Fast set mirrors for the word arrays above; each Set is rebuilt
// lazily when its source array changes; reassignment is detected, and
// in-place push/pop/splice is caught by the length check.
function defineSetMirror(name, getArray) {
  let ref = getArray(), len = ref.length, set = new Set(ref);
  Object.defineProperty(RiTa, name, {
    configurable: true, enumerable: false,
    get() {
      const arr = getArray();
      if (arr !== ref || arr.length !== len) {
        ref = arr, len = arr.length, set = new Set(arr);
      }
      return set;
    }
  });
}
defineSetMirror('STOP_WORDS_SET', () => RiTa.STOP_WORDS);
defineSetMirror('MASS_NOUNS_SET', () => RiTa.MASS_NOUNS);
defineSetMirror('QUESTIONS_SET', () => RiTa.QUESTIONS);

const ONLY_PUNCT = /^[\p{P}|+|-|<|>|^|$|\ufffd|`]*$/u;
const IS_LETTER = /^[a-z\u00C0-\u00ff]+$/;

RiTa.riscript = new RiScript({ RiTa });

export { RiTa, RiMarkov };
