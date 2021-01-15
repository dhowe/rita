[![Build Status](https://travis-ci.org/dhowe/RiTaJS.svg?branch=master)](https://travis-ci.org/dhowe/ritajs) <a href="https://www.npmjs.com/package/rita"><img src="https://img.shields.io/npm/v/rita.svg" alt="npm version"></a> ![Maven Central](https://img.shields.io/maven-central/v/org.rednoise/rita) <a href="http://www.gnu.org/licenses/gpl-3.0.en.html"><img src="https://img.shields.io/badge/license-GPL-orange.svg" alt="npm version"></a> <a href="https://spectrum.chat/rita"><img src="https://img.shields.io/badge/spectrum-chat-%23b14344"/></a>

## RiTa: a toolkit for generative writing and natural language

RiTa is a toolkit for generative writing and natural language. It is implemented in Java and JavaScript, with a common API for both, and it is free/libre/open-source via the GPL license.

###

This repo contains the website, documentation, and examples for RiTa. For the code, see

* the [JavaScript](https://github.com/dhowe/ritajs) repo, or use it with [npm](https://www.npmjs.com/package/rita) or [unpkg](https://unpkg.com/browse/rita/dist/)
* the [Java](https://github.com/dhowe/ritajs) repo, or add it to your project via [maven](https://search.maven.org/artifact/org.rednoise/rita) 

:warning: Version 2.0 contains breaking changes! Please check the [release notes](https://rednoise.org/rita/#whats-new-wrapper)

## API

  <table cellspacing="0" cellpadding="0" style="vertical-align: top;">
   <tr>
    <th colspan=2 style="text-align: left; padding-left: 12px">RiTa
    </th>
    <th colspan=1 style="text-align: left;">RiMarkov</th>
    <th colspan=1 style="text-align: left;">RiGrammar</th>
   </tr>
   <tr>
    <td style="vertical-align: top; padding-top: 15px">
      <a href="./RiTa/addTransform/index.html">RiTa.addTransform()</a><br/>
      <a href="./RiTa/alliterations/index.html">RiTa.alliterations()</a><br/>
      <a href="./RiTa/analyze/index.html">RiTa.analyze()</a><br/>
      <a href="./RiTa/concordance/index.html">RiTa.concordance()</a><br/>
      <a href="./RiTa/conjugate/index.html">RiTa.conjugate()</a><br/>
      <a href="./RiTa/evaluate/index.html">RiTa.evaluate()</a><br/>
      <a href="./RiTa/grammar/index.html">RiTa.grammar()</a><br/>
      <a href="./RiTa/hasWord/index.html">RiTa.hasWord()</a><br/>
      <a href="./RiTa/isAbbreviation/index.html">RiTa.isAbbreviation()</a><br/>
      <a href="./RiTa/isAdjective/index.html">RiTa.isAdjective()</a><br/>
      <a href="./RiTa/isAdverb/index.html">RiTa.isAdverb()</a><br/>
      <a href="./RiTa/isAlliteration/index.html">RiTa.isAlliteration()</a><br/>
      <a href="./RiTa/isNoun/index.html">RiTa.isNoun()</a><br/>
      <a href="./RiTa/isPunctuation/index.html">RiTa.isPunctuation()</a><br/>
      <a href="./RiTa/isQuestion/index.html">RiTa.isQuestion()</a><br/>
      <a href="./RiTa/isStopWord/index.html">RiTa.isStopWord()</a><br/>
      <a href="./RiTa/isRhyme/index.html">RiTa.isRhyme()</a><br/>
      <a href="./RiTa/isVerb/index.html">RiTa.isVerb()</a><br/>
      <a href="./RiTa/kwic/index.html">RiTa.kwic()</a><br/>
      <a href="./RiTa/markov/index.html">RiTa.markov()</a><br/>
    </td>
    <td style="vertical-align: top; padding-top: 15px"><br/>
      <a href="./RiTa/pastParticiple/index.html">RiTa.pastParticiple()</a><br/>
      <a href="./RiTa/phones/index.html">RiTa.phones()</a><br/>
      <a href="./RiTa/pos/index.html">RiTa.pos()</a><br/>
      <a href="./RiTa/posInline/index.html">RiTa.posInline()</a><br/>
      <a href="./RiTa/presentParticiple/index.html">RiTa.presentParticiple()</a><br/>
      <a href="./RiTa/pluralize/index.html">RiTa.pluralize()</a><br/>
      <a href="./RiTa/randomOrdering/index.html">RiTa.randomOrdering()</a><br/>
      <a href="./RiTa/randomSeed/index.html">RiTa.randomSeed()</a><br/>
      <a href="./RiTa/randomWord/index.html">RiTa.randomWord()</a><br/>
      <a href="./RiTa/rhymes/index.html">RiTa.rhymes()</a><br/>
      <a href="./RiTa/search/index.html">RiTa.search()</a><br/>
      <a href="./RiTa/sentences/index.html">RiTa.sentences()</a><br/>
      <a href="./RiTa/singularize/index.html">RiTa.singularize()</a><br/>
      <a href="./RiTa/soundsLike/index.html">RiTa.soundsLike()</a><br/>
      <a href="./RiTa/spellsLike/index.html">RiTa.spellsLike()</a><br/>
      <a href="./RiTa/stem/index.html">RiTa.stem()</a><br/>
      <a href="./RiTa/stresses/index.html">RiTa.stresses()</a><br/>
      <a href="./RiTa/syllables/index.html">RiTa.syllables()</a><br/>
      <a href="./RiTa/tokenize/index.html">RiTa.tokenize()</a><br/>
      <a href="./RiTa/untokenize/index.html">RiTa.untokenize()</a><br/><br/>
      <!--a href="./RiTa/VERSION/index.html">RiTa.VERSION</a><br/-->
    </td>
    <td style="vertical-align: top; padding-top: 15px; min-width: 125px">
      <a href="https://rednoise.org/rita/reference/Markov/addText/index.html">addText()</a><br/>
      <a href="https://rednoise.org/rita/reference/Markov/completions/index.html">completions()</a><br/>
      <a href="https://rednoise.org/rita/reference/Markov/generate/index.html">generate()</a><br/>
      <a href="https://rednoise.org/rita/reference/Markov/probability/index.html">probability()</a><br/>
      <a href="https://rednoise.org/rita/reference/Markov/probabilities/index.html">probabilities()</a><br/>
      <a href="https://rednoise.org/rita/reference/Markov/size/index.html">size()</a><br/>
      <a href="https://rednoise.org/rita/reference/Markov/toString/index.html">toString()</a><br/>
      <a href="https://rednoise.org/rita/reference/Markov/toJSON/index.html">toJSON()</a><br/>
      <a href="https://rednoise.org/rita/reference/Markov/fromJSON/index.html">fromJSON()</a><br/>
    </td>
    <td style="vertical-align: top; padding-top: 15px; min-width: 125px">
      <a href="https://rednoise.org/rita/reference/Grammar/addRule/index.html">addRule()</a><br/>
      <a href="https://rednoise.org/rita/reference/Grammar/addRules/index.html">addRules()</a><br/>
      <a href="https://rednoise.org/rita/reference/Grammar/expand/index.html">expand()</a><br/>
      <a href="https://rednoise.org/rita/reference/Grammar/removeRule/index.html">removeRule()</a><br/>
      <a href="https://rednoise.org/rita/reference/Grammar/toJSON/index.html">toJSON()</a><br/>
      <a href="https://rednoise.org/rita/reference/Grammar/toString/index.html">toString()</a><br/>
      <a href="https://rednoise.org/rita/reference/Grammar/fromJSON/index.html">fromJSON()</a><br/>
    </td>
 </tr>
</table>

## RiScript

RiScript is a writer-focused scripting language integrated with RiTa. It enables simple generative primitives within plain text for dynamic expansion at runtime. RiScript primitives can be used as part of any [RiTa grammar](https://rednoise.org/rita/reference/RiTa/grammar/) or executed directly using [RiTa.evaluate()](https://rednoise.org/rita/reference/RiTa/evaluate/). For full documentation, see [this page](https://rednoise.org/rita/reference/riscript.html).

<br>

## Contributors

### Code Contributors

This project exists only because of the people who contribute. Thank you!
<a href="https://github.com/dhowe/RiTa/graphs/contributors"><img src="https://opencollective.com/RiTa/contributors.svg?width=890&button=false" /></a>

### Financial Contributors
<a href="https://opencollective.com/rita/donate" target="_blank">
  <img src="https://opencollective.com/rita/contribute/button@2x.png?color=blue" width=300 />
</a>

