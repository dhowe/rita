<a href="https://www.npmjs.com/package/rita"><img src="https://img.shields.io/npm/v/rita.svg" alt="npm version"></a> ![Maven Central](https://img.shields.io/maven-central/v/org.rednoise/rita) <a href="http://www.gnu.org/licenses/gpl-3.0.en.html"><img src="https://img.shields.io/badge/license-GPL-orange.svg" alt="npm version"></a>

## RiTa: tools for generative natural language

RiTa is implemented in Java and JavaScript, with a common [API](https://github.com/dhowe/rita4j/blob/master/README.md#api) for both, and is free/libre/open-source via the GPL license.

### Features in v2.0

* Smart lexicon search for words matching part-of-speech, syllable, stress and rhyme patterns
* Fast, heuristic algorithms for inflection, conjugation, stemming, tokenization, and more
* Letter-to-sound engine for feature analysis of arbitrary words (with/without lexicon)
* Integration of the [RiScript](https://observablehq.com/@dhowe/riscript) scripting language, designed for writers
* Powerful new options for generation via grammars and Markov chains

###

This repo contains the website, documentation, and examples for RiTa. For the code, see

* the [JavaScript](https://github.com/dhowe/ritajs) repo, or use it with [npm](https://www.npmjs.com/package/rita) or [unpkg](https://unpkg.com/browse/rita/dist/)
* the [Java](https://github.com/dhowe/rita4j) repo, or add it to your project via [maven](https://search.maven.org/artifact/org.rednoise/rita) 

Note: Version 2.0 contains breaking changes! Please check the [release notes](https://rednoise.org/rita/#whats-new-wrapper)...

## API

   <table cellspacing="0" cellpadding="0" style="vertical-align: top;">
   <tr>
    <th colspan=2 style="vertical-align: top;text-align: left; padding-left: 12px">RiTa
    </th>
    <th colspan=1 style="vertical-align: top;text-align: left;">RiMarkov</th>
    <th colspan=1 style="vertical-align: top;text-align: left;">RiGrammar</th>
   </tr>
   <tr>
    <td style="vertical-align: top; padding-top: 15px">
      <a href="https://rednoise.org/rita/reference/RiTa/addTransform/index.html">RiTa.addTransform()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/alliterations/index.html">RiTa.alliterations()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/analyze/index.html">RiTa.analyze()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/concordance/index.html">RiTa.concordance()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/conjugate/index.html">RiTa.conjugate()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/evaluate/index.html">RiTa.evaluate()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/grammar/index.html">RiTa.grammar()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/hasWord/index.html">RiTa.hasWord()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/isAbbrev/index.html">RiTa.isAbbrev()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/isAdjective/index.html">RiTa.isAdjective()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/isAdverb/index.html">RiTa.isAdverb()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/isAlliteration/index.html">RiTa.isAlliteration()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/isNoun/index.html">RiTa.isNoun()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/isPunct/index.html">RiTa.isPunct()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/isQuestion/index.html">RiTa.isQuestion()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/isStopWord/index.html">RiTa.isStopWord()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/isRhyme/index.html">RiTa.isRhyme()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/isVerb/index.html">RiTa.isVerb()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/kwic/index.html">RiTa.kwic()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/markov/index.html">RiTa.markov()</a><br/>
    </td>
    <td style="vertical-align: top; padding-top: 15px">
      <a href="https://rednoise.org/rita/reference/RiTa/pastPart/index.html">RiTa.pastPart()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/phones/index.html">RiTa.phones()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/pos/index.html">RiTa.pos()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/posInline/index.html">RiTa.posInline()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/presentPart/index.html">RiTa.presentPart()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/pluralize/index.html">RiTa.pluralize()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/randomOrdering/index.html">RiTa.randomOrdering()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/randomSeed/index.html">RiTa.randomSeed()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/randomWord/index.html">RiTa.randomWord()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/rhymes/index.html">RiTa.rhymes()</a><br/>
      <!--a href="./RiTa/scripting/index.html">RiTa.scripting()</a><br/-->
      <a href="https://rednoise.org/rita/reference/RiTa/search/index.html">RiTa.search()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/sentences/index.html">RiTa.sentences()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/singularize/index.html">RiTa.singularize()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/soundsLike/index.html">RiTa.soundsLike()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/spellsLike/index.html">RiTa.spellsLike()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/stem/index.html">RiTa.stem()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/stresses/index.html">RiTa.stresses()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/syllables/index.html">RiTa.syllables()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/tokenize/index.html">RiTa.tokenize()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiTa/untokenize/index.html">RiTa.untokenize()</a><br/>
      <!--a href="./RiTa/VERSION/index.html">RiTa.VERSION</a><br/-->
    </td>
    <td style="vertical-align: top !important; padding-top: 15px; min-width: 125px">
      <a href="https://rednoise.org/rita/reference/RiMarkov/addText/index.html">addText()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiMarkov/completions/index.html">completions()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiMarkov/generate/index.html">generate()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiMarkov/probability/index.html">probability()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiMarkov/probabilities/index.html">probabilities()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiMarkov/size/index.html">size()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiMarkov/toString/index.html">toString()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiMarkov/toJSON/index.html">toJSON()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiMarkov/fromJSON/index.html">fromJSON()</a><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
    </td>
    <td style="vertical-align: top !important; padding-top: 15px; min-width: 125px">
      <a href="https://rednoise.org/rita/reference/RiGrammar/addRule/index.html">addRule()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiGrammar/addRules/index.html">addRules()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiGrammar/expand/index.html">expand()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiGrammar/removeRule/index.html">removeRule()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiGrammar/toJSON/index.html">toJSON()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiGrammar/toString/index.html">toString()</a><br/>
      <a href="https://rednoise.org/rita/reference/RiGrammar/fromJSON/index.html">fromJSON()</a><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
    </td>
 </tr>
</table>

## RiScript

RiScript is a writer-focused scripting language integrated with RiTa. It enables simple generative primitives within plain text for dynamic expansion at runtime. RiScript primitives can be used as part of any [RiTa grammar](https://rednoise.org/rita/reference/RiTa/grammar/) or executed directly using [RiTa.evaluate()](https://rednoise.org/rita/reference/RiTa/evaluate/). 
For documentation, see [this interactive notebook](https://observablehq.com/@dhowe/riscript).

<br>


## Developers
The website in this repo is generated via the `./scripts/make-site.sh` script, which requires `entr` and `ant`

### Static pages
The best way to make updates to static pages is to do the following:
```
$ git clone git@github.com:dhowe/rita.git
$ cd rita
$ sh ./scripts/watch-site.sh
```
* then make your changes in /rita/www 
* then refresh and check /rita/pub/index.html in the browser

When ready, create a PR with only the files you have changed (in `www` and `pub`).


### Reference pages
To make updates to the reference pages, follow the instructions above,<br> but instead make updates to the JSON files in `/rita/docgen/data`.

<br>


## Contributors

### Code Contributors

This project exists only because of the people who contribute. Thank you!
<a href="https://github.com/dhowe/RiTa/graphs/contributors"><img src="https://opencollective.com/RiTa/contributors.svg?width=890&button=false" /></a>

### Financial Contributors
<a href="https://opencollective.com/rita/donate" target="_blank">
  <img src="https://opencollective.com/rita/contribute/button@2x.png?color=blue" width=300 />
</a>

