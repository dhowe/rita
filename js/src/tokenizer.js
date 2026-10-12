/**
 * @class Tokenizer
 * @memberof module:rita
 */
class Tokenizer {

  constructor(parent) {
    this.RiTa = parent;
    this.splitter = /(\S.+?[.!?]["\u201D]?)(?=\s+|$)/g;
  }

  /**
   * Returns an array containing all unique alphabetical words (tokens) in the text.
   * Punctuation and case are ignored unless specified otherwise.
   * @param {string} text - The text from which to extract the tokens
   * @param {object} [options] - The options
   * @param {boolean} [options.caseSensitive=false] - Whether to pay attention to case
   * @param {boolean} [options.ignoreStopWords=false] - Whether to ignore words like 'the', 'and', 'a', 'of', etc, as specified in RiTa.STOP_WORDS
   * @param {boolean} [options.splitContractions=false] - Whether to convert contractions (e.g., "I'd" or "she'll") into multiple individual tokens
   * @param {boolean} [options.includePunct=false] - Whether to include punctuation in the results
   * @param {boolean} [options.sort=false] - Whether to sort the tokens before returning them
   * @returns {string[]} Array of tokens
   */
  tokens(text, options = {
    caseSensitive: false,
    ignoreStopWords: false,
    splitContractions: false,
    includePunct: false,
    sort: false,
  }) {
    let words = this.tokenize(text, options), map = {};
    words.forEach(w => {
      if (!options.caseSensitive) w = w.toLowerCase();
      if (options.includePunct || ALPHA_RE.test(w)) map[w] = 1;
    });
    let tokens = Object.keys(map);
    if (options.ignoreStopWords) tokens = tokens.filter(t => !this.RiTa.isStopWord(t));
    return options.sort ? tokens.sort() : tokens;
  }

  tokenize(input, opts = {
    // regex: null,
    // debug: false,
    // splitHyphens: false,
    // splitContractions: false
  }) {
    if (typeof input !== 'string') return [];

    if (opts.regex) return input.split(opts.regex); // TODO: tests

    let { tags, text } = this._pushTags(input.trim());

    for (let i = 0; i < TOKENIZE_RE.length; i += 2) {
      if (opts.debug) var pre = text;
      text = text.replace(TOKENIZE_RE[i], TOKENIZE_RE[i + 1]);
      if (opts.debug && text !== pre) console.log('HIT' + i, pre + ' -> '
        + text, TOKENIZE_RE[i], TOKENIZE_RE[i + 1]);
    }

    // https://github.com/dhowe/rita/issues/65
    // default behavior is to keep hyphen
    if (opts.splitHyphens) {
      text = text.replace(/([a-zA-Z]+)-([a-zA-Z]+)/g, "$1 - $2");
    }

    if (this.RiTa.SPLIT_CONTRACTIONS || opts.splitContractions) {
      for (let i = 0; i < CONTRACTS_RE.length; i += 2) {
        text = text.replace(CONTRACTS_RE[i], CONTRACTS_RE[i + 1]);
        //if (pre !== text) console.log('splitCon: ' + pre + '->' + text);
      }
    }

    return this._popTags(text.trim().split(WS_RE), tags);
  }

  untokenize(tokenArray, delim = ' ') {

    if (!Array.isArray(tokenArray)) return '';

    let tokens = this._preProcessTags(tokenArray);

    let state = { // state variables for decision rules
      withinQuote: !!(tokens.length && QUOTE_RE.test(tokens[0])),
      afterQuote: false,
      midSentence: false,
      nextNoSpace: false
    };

    let result = tokens[0] || '';
    for (let i = 1; i < tokens.length; i++) {
      if (!tokens[i]) continue;
      const [space, trailing, nextState] = this._nextState
        (tokens[i - 1], tokens[i], tokens[i + 1], i === tokens.length - 1, state);
      result += (space ? delim : '') + tokens[i] + (trailing ? delim : '');
      state = nextState;
    }

    return result.trim();
  }

  /**
   * Split the input text into sentences according to the options
   * @param {string} text - The text to split
   * @param {(string|RegExp)} [regex] - An optional custom regex to split on
   * @returns {string[]} An array of sentences
   */
  sentences(text, regex) {
    if (!text || !text.length) return [text];

    let clean = text.replace(NL_RE, ' ')

    let delim = '___';
    let re = new RegExp(delim, 'g');
    let pattern = regex || this.splitter;

    let unescapeAbbrevs = (arr) => {
      for (let i = 0; i < arr.length; i++) {
        arr[i] = arr[i].replace(re, ".");
      }
      return arr;
    }

    let escapeAbbrevs = (text) => {
      let abbrevs = this.RiTa.ABRV;
      for (let i = 0; i < abbrevs.length; i++) {
        let abv = abbrevs[i];
        let idx = text.indexOf(abv);
        while (idx > -1) {
          text = text.replace(abv, abv.replace('.', delim));
          idx = text.indexOf(abv);
        }
      }
      return text;
    }

    let arr = escapeAbbrevs(clean).match(pattern);
    return arr?.length ? unescapeAbbrevs(arr) : [text];
  }


  /**
   * Decide whether a space (delimiter) should be inserted before `curr` (and optionally after it).
   * Returns [spaceBefore, spaceAfter, nextState]. 
   * @param {string} prev - the preceding token
   * @param {string} curr - the current token being appended
   * @param {string|undefined} next - the token after curr (may be undefined)
   * @param {boolean} isLast - whether curr is the last token
   * @param {{withinQuote:boolean, afterQuote:boolean, midSentence:boolean, nextNoSpace:boolean}} state
   * @returns {[boolean, boolean, object]}
   */
  _nextState(prev, curr, next, isLast, state) {
    let { withinQuote, afterQuote, midSentence, nextNoSpace } = state;

    // derived booleans — computed once per state, used below
    const thisNBPunct = NOSP_BF_PUNCT_RE.test(curr) || UNTAG_RE[2].test(curr) || LINEBREAK_RE.test(curr); // no space before curr
    const lastNBPunct = NOSP_BF_PUNCT_RE.test(prev) || LINEBREAK_RE.test(prev) || ELLIPSIS_RE.test(prev);
    const lastNAPunct = NOSP_AF_PUNCT_RE.test(prev) || UNTAG_RE[1].test(prev) || LINEBREAK_RE.test(prev); // no space after prev
    const thisLBracket = LB_RE.test(curr), thisRBracket = RB_RE.test(curr);
    const lastLB = LB_RE.test(prev), lastRB = RB_RE.test(prev);
    const thisQuote = QUOTE_RE.test(curr), lastQuote = QUOTE_RE.test(prev);
    const thisComma = curr === ',', lastComma = prev === ',';
    const thisLineBreak = LINEBREAK_RE.test(curr);
    const isDomain = DOMAIN_RE.test(curr), lastIsWWW = WWW_RE.test(prev);
    const lastEndWithS = prev[prev.length - 1] === 's' && prev !== 'is' && prev !== 'Is' && prev !== 'IS';
    const nextIsS = next === 's' || next === 'S';

    // ── rules (ordered by priority) - ugly but working

    // URL domain continuation or deferred no-space
    if ((prev === '.' && isDomain) || nextNoSpace) {
      return [false, false, { withinQuote, afterQuote, midSentence, nextNoSpace: false }];
    }

    // www.<domain>  — suppress space before the dot, and before whatever follows
    if (curr === '.' && lastIsWWW) {
      return [false, false, { withinQuote, afterQuote, midSentence, nextNoSpace: true }];
    }

    // left bracket: always space before
    if (thisLBracket) {
      return [true, false, { withinQuote, afterQuote, midSentence, nextNoSpace }];
    }

    // after right bracket: space unless followed by punct or another bracket
    if (lastRB) {
      const space = !thisNBPunct && !thisLBracket;
      return [space, false, { withinQuote, afterQuote, midSentence, nextNoSpace }];
    }

    // trailing space: possessive apostrophe after plural — computed here so quote branch can use it
    const trailingSpace = thisNBPunct && !lastNBPunct && !withinQuote && SQUOTE_RE.test(curr) && lastEndWithS;

    // quote token
    if (thisQuote) {
      if (withinQuote) {
        // closing quote — no space before, mark done
        return [false, false, { withinQuote: false, afterQuote: true, midSentence, nextNoSpace }];
      }
      // possessive apostrophe after plural (dogs') or before 's'
      if ((APOS_RE.test(curr) && lastEndWithS) || (APOS_RE.test(curr) && nextIsS)) {
        return [false, trailingSpace, { withinQuote, afterQuote, midSentence, nextNoSpace }];
      }
      // opening quote — space before
      return [true, false, { withinQuote: true, afterQuote: false, midSentence, nextNoSpace }];
    }

    // first token after a closing quote
    if (afterQuote && !thisNBPunct) {
      return [true, false, { withinQuote, afterQuote: false, midSentence, nextNoSpace }];
    }

    // "word," mid-sentence pattern: "he said," she replied
    if (lastQuote && thisComma) {
      return [false, false, { withinQuote, afterQuote, midSentence: true, nextNoSpace }];
    }
    if (midSentence && lastComma) {
      return [true, false, { withinQuote, afterQuote, midSentence: false, nextNoSpace }];
    }

    // Period-run (ellipsis) and dash tokens: glued to a preceding word, but
    // spaced after punctuation or after a token that already ends in a dot.
    // This must not depend on isLast, otherwise untokenize of a token window
    // differs from untokenize of the same tokens in the full text.
    if (ELLIPSIS_RE.test(curr) || DASH_RE.test(curr)) {
      const glue = !lastNBPunct && !/\.$/.test(prev);
      return [!glue, false, { withinQuote, afterQuote, midSentence, nextNoSpace }];
    }

    // general case
    const generalSpace = (!thisNBPunct && !lastQuote && !lastNAPunct && !lastLB && !thisRBracket)
      || (!isLast && thisNBPunct && lastNBPunct && !lastNAPunct
        && !lastQuote && !lastLB && !thisRBracket && !thisLineBreak);

    return [generalSpace, trailingSpace, { withinQuote, afterQuote, midSentence, nextNoSpace }];
  }

  _pushTags(text) {
    let tags = [], tagIdx = 0;
    while (TAG_RE.test(text)) {
      tags.push(text.match(TAG_RE)[0]);
      text = text.replace(TAG_RE, " _" + TAG + (tagIdx++) + "_ ");
    }
    return { tags, text };
  }

  _popTags(result, tags) {
    for (let i = 0; i < result.length; i++) {
      if (POPTAG_RE.test(result[i])) {
        result[i] = tags.shift();
      }
      // restore the raw period-run spelling captured during tokenize
      if (ELLIPSIS_ENC_RE.test(result[i])) {
        result[i] = result[i].replace(ELLIPSIS_ENC_RE,
          (m, s) => s.replace(/\u2062/g, '.').replace(/\u2063/g, ' '));
      }
      if (result[i].includes('_') && !EMAIL_RE.test(result[i]) && !URL_RE.test(result[i])) {
        result[i] = result[i].replace(UNDER_RE, "$1 $2");
      }
    }
    return result;
  }

  _preProcessTags(array) {
    let result = [], currentIdx = 0;
    while (currentIdx < array.length) {
      let currentToken = array[currentIdx];
      if (!LT_RE.test(currentToken)) {
        result.push(currentToken);
        currentIdx++;
        continue;
      } // if not '<'
      let subArray = [array[currentIdx]];
      let inspectIdx = currentIdx + 1;
      while (inspectIdx < array.length) {
        subArray.push(array[inspectIdx]);
        if (LT_RE.test(array[inspectIdx])) break;
        if (GT_RE.test(array[inspectIdx])) break;
        inspectIdx++;
      }
      if (LT_RE.test(subArray[subArray.length - 1])) {
        result = result.concat(subArray.slice(0, subArray.length - 1));
        currentIdx = inspectIdx;
        continue;
      }
      if (!GT_RE.test(subArray[subArray.length - 1])) {
        result = result.concat(subArray);
        currentIdx = inspectIdx + 1;
        continue;
      }
      if (!TAG_RE.test(subArray.join(''))) {
        result = result.concat(subArray);
        currentIdx = inspectIdx + 1;
        continue;
      }
      let tag = this._tagSubarrayToString(subArray);
      result.push(tag);
      currentIdx = inspectIdx + 1;
    }
    return result;
  }

  _tagSubarrayToString(array) {
    if (!LT_RE.test(array[0]) || !GT_RE.test(array[array.length - 1])) {
      throw Error(array + 'is not a tag');
    }
    let start = array[0].trim();
    let end = array[array.length - 1].trim();

    let inspectIdx = 1;
    while (inspectIdx < array.length - 1 && TAGSTART_RE.test(array[inspectIdx])) {
      start += array[inspectIdx].trim();
      inspectIdx++;
    }

    let contentStartIdx = inspectIdx;
    inspectIdx = array.length - 2;
    while (inspectIdx > contentStartIdx && TAGEND_RE.test(array[inspectIdx])) {
      end = array[inspectIdx].trim() + end;
      inspectIdx--;
    }

    let contentEndIdx = inspectIdx;
    let result = start + this.untokenize
      (array.slice(contentStartIdx, contentEndIdx + 1)).trim() + end;

    return result;
  }
}

const UNTAG_RE = [
  /^ *<[a-z][a-z0-9='"#;:&\s\-+/.?]*\/> *$/i, // empty tags <br/> <img /> etc. -> like a normal word
  /^ *<([a-z][a-z0-9='"#;:&\s\-+/.?]*[a-z0-9='"#;:&\s\-+.?]|[a-z])> *$/i, // opening tags <a>, <p> etc. -> no space after 
  /^ *<\/[a-z][a-z0-9='"#;:&\s\-+/.?]*> *$/i, // closing tags </a> </p> etc. -> no space before
  /^ *<!DOCTYPE[^>]*> *$/i, // <!DOCTYPE> -> like a normal word
  /^ *<!--[^->]*--> *$/i // <!-- --> -> like a normal word
];

const LT_RE = /^ *< *$/;
const GT_RE = /^ *> *$/;
const TAGSTART_RE = /^ *[!\-/] *$/;
const TAGEND_RE = /^ *[-/] *$/
const NOSP_AF_PUNCT_RE = /^[\^*$/\u2044#\-@\u00b0\u2012\u2013\u2014]+$/;
const TAG = "TAG", UNDER_RE = /([0-9a-zA-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u00FF]|[.,])_([0-9a-zA-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u00FF])/g;
const LB_RE = /^[[({\u27e8]+$/, RB_RE = /^[)\]}\u27e9]+$/;
const QUOTE_RE = /^[""\u201c\u201d\u2019\u2018`''\u00ab\u00bb]+$/;
const DOMAIN_RE = /^(com|org|edu|net|xyz|gov|int|eu|hk|tw|cn|de|ch|fr)$/;
const SQUOTE_RE = /^[\u2019\u2018`']+$/, ALPHA_RE = /^[A-Za-z’']+$/, WS_RE = / +/;
const APOS_RE = /^[\u2019']+$/, NL_RE = /(\r?\n)+/g, WWW_RE = /^(www[0-9]?|WWW[0-9]?)$/;
const NOSP_BF_PUNCT_RE = /^[,.;:?!)""\u201c\u201d\u2019\u2018`'%\u2026\u2103^*\u00b0/\u2044\u2012\u2013\u2014\-@]+$/;
const LINEBREAK_RE = /\r?\n/;//[\n\r\036]/;
const URL_RE = /((http[s]?):(\/\/))?([-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b)([-a-zA-Z0-9()@:%_+.~#?&//=]*)/;
const EMAIL_RE = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/;
// period-run tokens: ELLIPSIS_RE matches a decoded token, ELLIPSIS_ENC_RE the encoded placeholder
const ELLIPSIS_RE = /^(?:\.\s*){2,}$/;
const ELLIPSIS_ENC_RE = /^_el([\u2062\u2063]+)_$/;
// dash tokens (em/en/hyphen runs) share the ellipsis spacing rule: glued to a
// preceding word, spaced after punctuation, and never isLast-dependent
const DASH_RE = /^[\u2012\u2013\u2014-]+$/;

const TOKENIZE_RE = [
  // save  --------
  /\b([Ee])[.]([Gg])[.]/g, "_$1$2_", //E.g
  /\b([Ii])[.]([Ee])[.]/g, "_$1$2_", //i.e
  /\b([Aa])[.]([Mm])[.]/g, "_$1$2_", //a.m.
  /\b([Pp])[.]([Mm])[.]/g, "_$1$2_", //p.m.
  /\b(Cap)[.]/g, "_Cap_", //Cap.
  /\b([Cc])[.]/g, "_$1_", //c.
  /\b([Ee][Tt])[\s]([Aa][Ll])[.]/, "_$1zzz$2_", // et al.
  /\b(etc|ETC)[.]/g, "_$1_", //etc.
  /\b([Pp])[.]([Ss])[.]/g, "_$1$2dot_", // p.s.
  /\b([Pp])[.]([Ss])/g, "_$1$2_", // p.s
  /\b([Pp])([Hh])[.]([Dd])/g, "_$1$2$3_", // Ph.D
  /\b([Rr])[.]([Ii])[.]([Pp])/g, "_$1$2$3_", // R.I.P
  /\b([Vv])([Ss]?)[.]/g, "_$1$2_", // vs. and v.
  /\b([Mm])([Rr]|[Ss]|[Xx])\./g, "_$1$2_", // Mr. Ms. and Mx.
  /\b([Dd])([Rr])[.]/g, "_$1$2_", // Dr.
  /\b([Pp])([Ff])[.]/g, "_$1$2_", // Pf.
  /\b([Ii])([Nn])([Dd]|[Cc])[.]/g, "_$1$2$3_", // Ind. and Inc.
  /\b([Cc])([Oo])[.][,][\s]([Ll])([Tt])([Dd])[.]/g, "_$1$2dcs$3$4$5_", // co., ltd.
  /\b([Cc])([Oo])[.][\s]([Ll])([Tt])([Dd])[.]/g, "_$1$2ds$3$4$5_", // co. ltd.
  /\b([Cc])([Oo])[.][,]([Ll])([Tt])([Dd])[.]/g, "_$1$2dc$3$4$5_", // co.,ltd.
  /\b([Cc])([Oo])([Rr]?)([Pp]?)[.]/g, "_$1$2$3$4_", // Corp. and Co.
  /\b([Ll])([Tt])([Dd])[.]/g, "_$1$2$3_", // ltd.
  /\b(prof|Prof|PROF)\./g, "_$1_", //Prof. 
  //   /(\w+([\.-_]?\w+)*)@(\w+([\.-_]?\w+)*)\.(\w{2,3})/g, "$1__AT__$3.$5", //email addresses
  // /^\w+([\.-]?\w+)+@\w+([\.:]?\w+)+(\.[a-zA-Z0-9]{2,3})+$/g, "$1__AT__$2", //email addresses
  /\b([\w.]+)@(\w+\.\w+)/g, "$1__AT__$2",
  /\b((http[s]?):(\/\/))([-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b)([-a-zA-Z0-9()@:%_+.~#?&//=]*)/g, "$2COLON$3$4$5", //urls with http(s)
  //decimal #
  /([-]?[0-9]+)\.([0-9]+)/g, "$1DECIMALDOT$2_", //(-)27.3
  /([-]?[0-9]+)\.([0-9]+)e([-]?[0-9]+)/g, "_$1DECIMALDOT$2POWERE$3_", //(-)1.2e10
  /([0-9]{1,3}),([0-9]{3})/g, "$1_DECIMALCOMMA_$2", // large numbers like 19,700 or 200,000,000.13
  /([A-Za-z0-9])\.([A-Za-z0-9])/g, "$1_DECIMALDOT_$2", //www.example.com

  //escape sequences of line breaks in ASCII
  /\r\n/g, " _CARRIAGERETURNLINEFEED_ ", // CR LF
  /\n\r/g, " _LINEFEEDCARRIAGERETURN_ ", // LF CR
  /\n/g, " _LINEFEED_ ", // LF
  /\r/g, " _CARRIAGERETURN_ ", // CR
  ///\036/g, " _RECORDSEPARATOR_ ", // RS
  //--------------------------
  // collapse any run of 2+ periods (whitespace allowed between) into a single
  // token that preserves its exact original spelling, so ". . .", "...", "..",
  // ". ." etc. all roundtrip verbatim. Dots and spaces are encoded as U+2062 /
  // U+2063 so they survive the punctuation-splitting rules below, and are
  // decoded back to the raw substring in _popTags.
  /\.(?:\s*\.)+/g, m => " _el" + m.replace(/\./g, "\u2062").replace(/\s+/g, "\u2063") + "_ ",
  /([?!"\u201C.,;:@#$%&])/g, " $1 ",
  /\u2026/g, " \u2026 ",
  /\s+/g, ' ',
  /,([^0-9])/g, " , $1",
  /([^.])([.])([\])}>"'\u2019]*)\s*$/g, "$1 $2$3 ",
  /([[\](){}<>\u27e8\u27e9])/g, " $1 ",
  /--/g, " -- ",
  /\u2012/g, " \u2012 ", //" ‒ "
  /\u2013/g, " \u2013 ", // " — "
  /\u2014/g, " \u2014 ",//" – "
  /$/g, ' ',
  /^/g, ' ',
  /([^'])' | '/g, "$1 ' ",
  / \u2018/g, " \u2018 ",
  /'([SMD]) /g, " '$1 ",
  / ([A-Z]) \./g, " $1. ",
  /^\s+/g, '',
  /\^/g, " ^ ",
  /\u00b0/g, " \u00b0 ",

  //pop ------------------
  /_([Ee])([Gg])_/g, "$1.$2.", //Eg
  /_([Ii])([Ee])_/g, "$1.$2.", //ie
  /_([Aa])([Mm])_/g, "$1.$2.", //a.m.
  /_([Pp])([Mm])_/g, "$1.$2.", //p.m.
  /_Cap_/g, "Cap.", //Cap.
  /_([Cc])_/g, "$1.", //c.
  /_([Ee][Tt])zzz([Aa][Ll])_/, "$1_$2.", // et al.
  /_(etc|ETC)_/g, "$1.", //etc.
  /_([Pp])([Ss])dot_/g, "$1.$2.", // p.s.
  /_([Pp])([Ss])_/g, "$1.$2",
  /_([Pp])([Hh])([Dd])_/g, "$1$2.$3", // Ph.D
  /_([Rr])([Ii])([Pp])_/g, "$1.$2.$3", // R.I.P
  /_([Vv])([Ss]?)_/g, "$1$2.", // vs. and v.
  /_([Mm])([Rr]|[Ss]|[Xx])_/g, "$1$2.", // Mr. Ms. and Mx.
  /_([Dd])([Rr])_/g, "$1$2.", // Dr.
  /_([Pp])([Ff])_/g, "$1$2.", // Pf.
  /_([Ii])([Nn])([Dd]|[Cc])_/g, "$1$2$3.", // Ind. and Inc.
  /_([Cc])([Oo])([Rr]?)([Pp]?)_/g, "$1$2$3$4.", // Corp. and Co.
  /_([Cc])([Oo])dc([Ll])([Tt])([Dd])_/g, "$1$2.,$3$4$5.", // co.,ltd.
  /_([Ll])([Tt])([Dd])_/g, "$1$2$3.", // ltd.
  /_([Cc])([Oo])dcs([Ll])([Tt])([Dd])_/g, "$1$2.,_$3$4$5.", // co., ltd.
  /_([Cc])([Oo])ds([Ll])([Tt])([Dd])_/g, "$1$2._$3$4$5.", // co. ltd.
  /_(prof|PROF|Prof)_/g, "$1.", //Prof.
  /([-]?[0-9]+)DECIMALDOT([0-9]+)_/g, "$1.$2", //(-)27.3
  /_([-]?[0-9]+)\DECIMALDOT([0-9]+)POWERE([-]?[0-9]+)_/g, "$1.$2e$3", //(-)1.2e(-)9
  /_DECIMALCOMMA_/g, ",", // large numbers like 200,000,000.13
  /_DECIMALDOT_/g, ".",
  // /(\w+([\.-]?\w+)*)__AT__(\w+([\.-]?\w+)*)\.(\w{2,3})/g, "$1@$3.$5",
  /__AT__/g, "@",
  /((http[s]?)COLON(\/\/))([-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b)([-a-zA-Z0-9()@:%_+.~#?&//=]*)/g, "$2:$3$4$5",
  /_LINEFEED_/g, "\n", // LF
  /_CARRIAGERETURN_/g, "\r", // CR
  /_CARRIAGERETURNLINEFEED_/g, "\r\n", // CR LF
  /_LINEFEEDCARRIAGERETURN_/g, "\n\r", // LF CR
  ///_RECORDSEPARATOR_/g, "\\036", // RS
];

const CONTRACTS_RE = [
  // TODO: 'She'd have wanted' -> 'She would have wanted'

  /\b([Cc])an['\u2019]t/g, "$1an not",
  /\b([Dd])idn['\u2019]t/g, "$1id not",
  /\b([CcWw])ouldn['\u2019]t/g, "$1ould not",
  /\b([Ss])houldn['\u2019]t/g, "$1hould not",
  /\b([Ii])t['\u2019]s/g, "$1t is",
  /\b([tT]hat)['\u2019]s/g, "$1 is",
  /\b(she|he|you|they|i)['\u2019]d/gi, "$1 had", // changed from would, 12/8/23
  /\b(she|he|you|they|i)['\u2019]ll/gi, "$1 will",
  /n['\u2019]t /g, " not ",
  /['\u2019]ve /g, " have ",
  /['\u2019]re /g, " are "
];

const TAG_RE = /(<\/?[a-z][a-z0-9='"#;:&\s\-+/.?]*\/?>|<!DOCTYPE[^>]*>|<!--[^>-]*-->)/i; // html tags (rita#103)
const POPTAG_RE = new RegExp(`_${TAG}[0-9]+_`);

export default Tokenizer;