// https://observablehq.com/@shadoof/sifther@2329
import define1 from "./4e36c4335cde0fd3@826.js";

export default function define(runtime, observer) {
  const main = runtime.module();
  const fileAttachments = new Map([["Andale Mono.ttf",new URL("./files/16b2c31c23d138eaf98e2ba30741cd1d39ea471d40c837b23f27b8a36d561a8511c7977dc852fd93074089d0a1ab62328ef78a55d02e5bdcd2b8c00da2bf686d",import.meta.url)]]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], function(md){return(
md`# sifther
*experimenting with Observable for language-art text manipulation<br />
and thus, at the same time, offering some writers and language artists<br />
an initial introduction to (Observable) Javascript.*
`
)});
  main.variable(observer("index")).define("index", ["html"], function(html){return(
html`
<div class='sifther'>
  <div class='mono overlaid index07 text'></div>
  <div class='mono overlaid index07 text visible'></div>
</div>
`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`
*The cell above is a live view of* **sifther**’s *most recent version. Web-published version at [shadoof.github.io/sifther](https://shadoof.github.io/sifther) or perhaps even install it as a screensaver for Mac using [WebViewScreenSaver](https://github.com/liquidx/webviewscreensaver).*

This notebook – intended also as an initial personal trial of Observable itself – emerges from the idea for a poem-sized piece that will explore the effects of the animated, ambient, replacement of textual linguistic elements at various levels and defined in terms of a variety of characteristics, for now:
* words distinguished by ‘subliteral’ differences, e.g. ‘interiority/inferiority’
* synonyms, antonyms and associated words with the same syntactic role, e.g. ‘embarrasses/impresses/frightens/attracts’
* pronouns and/or possessive pronouns.

My plan is to start with simple sketches, easy to write and read, and then move the results into new Observable cells of increasing complexity.

And I will need to test the exportability of the work as embedded code or stand-alone web apps as I go. (This is a concern that I have for use of this platform.)

I anticpate that the cell for final export/embedding will be named \`index\` (as in the conventional \`index.html\`). Thus, as I work toward the notebook-final \`index\` I will name appropriate sketch cells ‘index’ followed by a two-digit version number: ‘00’ intended to correspond with ‘0.0’-style versioning. Thus ‘10’ could be version 1.0 and thus (possibly) a ‘release.’`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`---

### \`index00\``
)});
  main.variable(observer("index00")).define("index00", ["html","text00"], function(html,text00){return(
html`
<style>
  .mono00 {font: 24px AndaleMono;}
</style>

<body>
  &nbsp;<br />

  <div class='mono00'>
    ${text00}
  </div>

  &nbsp;<br />
</body>
`
)});
  main.variable(observer("text00")).define("text00", function()
{
  let getRandomElemLocal = function(array) {
    return array[(array.length * Math.random()) | 0];
  };
  let possessive = [
    "my",
    "your",
    "his",
    "her",
    "their",
    "our",
    "your",
    "their"
  ];
  let noun = ["inferiority", "interiority"];
  let verb = ["embarrasses", "impresses", "frightens", "attracts"];
  let pronoun = ["me", "you", "him", "her", "them", "us", "you", "them"];
  let textArray = new Array();
  textArray[0] = getRandomElemLocal(possessive);
  textArray[1] = getRandomElemLocal(noun);
  textArray[2] = getRandomElemLocal(verb);
  textArray[3] = getRandomElemLocal(pronoun);
  return textArray.join(" ");
}
);
  main.variable(observer()).define(["md"], function(md){return(
md`So, if you \`run\` the above \`text00\` cell, \`index00\` reacts. The next thing to do is probably to animate this with periodic, automated \`run\`ning of the cell that will assemble the phrase in \`index01\`.`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`---

### \`index01\``
)});
  main.variable(observer("index01")).define("index01", ["html","text01"], function(html,text01){return(
html`
&nbsp;<br />

<div class='regular'>
  ${text01}
</div>

&nbsp;<br />
`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`**Note:** This snippet of html does not need the \`<style>\` node from \`index00\` to be copied into the \`01\` cell. In fact, it seems that an html \`<style>\` node can be placed at the end of the notebook with other general-use bits of code that are powering it. CSS for a \`.regular\` class (used above) is in just such a \`<style>\` cell.<br />
(And we never really needed the \`<body>\` tags in \`index00\`.)`
)});
  main.variable(observer("text01")).define("text01", ["randomWord","possessives","nouns","verbs","pronouns"], function(randomWord,possessives,nouns,verbs,pronouns){return(
`${randomWord(possessives)} ${randomWord(nouns)} ${randomWord(
  verbs
)} ${randomWord(pronouns)}`
)});
  main.variable(observer()).define(["md","caret"], function(md,caret){return(
md`Gosh. That’s considerably more elegant and abbreviated, isn’t it?

* I moved the function definition in \`index00\` to a **Functions** section of the notebook, and
* some constant declarations/definitions to a **Constants** section of the notebook (and named them a little better), and 
* I made use of Javascript’s marvellous and new-to-me ‘Template literals’ (also called ‘Template strings.’ Not only do these allow you to place expression evaluations into string literals, they are much more flexible with respect to the inclusion of linebreaks. Try editing the code above by typing \`<return>\` after \`\${randomWord(nouns)}\` then hitting ${caret()} or \`<shift-return>\` and see what happens to \`text01\`. Sadly: this will not propagate to html.

Having learned a bit more for now, automated animation will await \`index02\`.`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`---

### \`index02\``
)});
  main.variable(observer("index02")).define("index02", ["html","text02"], function(html,text02){return(
html`
&nbsp;<br />

<div class='mono'>
  ${text02}
</div>

&nbsp;<br />
`
)});
  main.variable(observer("text02")).define("text02", ["Promises","assembleText"], async function*(Promises,assembleText)
{
  while (true) {
    yield await Promises.tick(4000).then(assembleText);
    // what was spelt out in text01 has been moved to a function
  }
}
);
  main.variable(observer()).define(["md"], function(md){return(
md`\`Promises.tick([milliseconds])\` made this pretty easy, along with the \`yield\` keyword. This is refreshing every four seconds. The next step in \`index03\` will be to work on the cosmetics. We’ll attempt CSS fades.`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`---

### \`index03\``
)});
  main.variable(observer("index03")).define("index03", ["html"], function(html){return(
html`
&nbsp;<br />

<div id='text03' class='mono text'></div>

&nbsp;<br />
`
)});
  main.variable(observer("ticker03")).define("ticker03", ["Promises","fader"], async function*(Promises,fader)
{
  let seconds = 5;
  while (true) {
    yield await Promises.tick(seconds * 1000).then(fader);
  }
}
);
  main.variable(observer()).define(["md"], function(md){return(
md`The following cell fades the text in and out and reassembles the text whenever it is faded out.`
)});
  main.variable(observer("fader")).define("fader", ["assembleText","md"], function(assembleText,md){return(
() => {
  let theElem = document.getElementById('text03');
  // yield theElem.classList.contains('visible');
  if (!theElem.classList.contains('visible'))
    theElem.innerHTML = assembleText();
  theElem.classList.toggle('visible');
  return md`\`fader\` promises ticking away ...`; // purely cosmetic in the notebook
}
)});
  main.variable(observer()).define(["md"], function(md){return(
md`---

### \`index04\``
)});
  main.variable(observer("index04")).define("index04", ["html"], function(html){return(
html`
<div class='sifther'>
  <div class='mono overlaid allSyntagms text'></div>
  <div class='mono overlaid allSyntagms text visible'></div>
</div>
`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`We’re going to implement crossfades next, and we’re also adding a new \`buildText()\` method which, by default has word-padding (to the right) set to \`true\`. Padding words with spaces to the right is used to enhance the visual effect of ‘subliteral’ crossfades in particular (in the sense of making them more difficult to notice). You could try adding \`false\` to the end of the list of arguments that is passed to \`buildText()\` in the cell below to see how this works.`
)});
  main.variable(observer("ticker04")).define("ticker04", ["Promises","crossfader","buildText","assembled"], async function*(Promises,crossfader,buildText,assembled)
{
  let seconds = 5;
  while (true) {
    yield await Promises.tick(seconds * 1000).then(
      crossfader(buildText(assembled, [...assembled.keys()]), 'allSyntagms')
    );
  }
}
);
  main.variable(observer("crossfader")).define("crossfader", function(){return(
(theText, classSelector = 'singleSyntagm') => {
  let theElems = document.getElementsByClassName(classSelector);
  for (let i = 0; i < theElems.length; i++) {
    if (!theElems[i].classList.contains('visible')) {
      theElems[i].innerHTML = theText;
    }
    theElems[i].classList.toggle('visible');
  }
}
)});
  main.variable(observer()).define(["md"], function(md){return(
md`---

### \`index05\``
)});
  main.variable(observer("index05")).define("index05", ["html"], function(html){return(
html`
<div class='sifther'>
  <div class='mono overlaid singleSyntagm text'></div>
  <div class='mono overlaid singleSyntagm text visible'></div>
</div>
`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`This version only replaces and crossfades one of the four syntagms within each period, over the number of seconds that is set in the following cell (7 at the time of writing). This is getting close to what we’re going for in this piece: the animation of changes in linguistic ‘difference’ at various structural levels, which then produce disproportional effects on what is grasped as one reads. This includes changes that are hardly noticable, or only noticed _after_ a ‘meaning’ has been grasped.

But soon we must introduce methods and data structures that will allow us to deploy more ‘subliterally’ differentiated word pairs (as in the ‘interiority/inferiority’ pair). The arrays from which we assemble readable text must be able to contain ‘word pair’ objects which are handled with nuance: in particular, they should follow a rule such as: \`never replace a word in a pair unless both words in the pairing have been displayed in succession\`.`
)});
  main.variable(observer("ticker05")).define("ticker05", ["Promises","crossfader","buildText","assembled05","randInt"], async function*(Promises,crossfader,buildText,assembled05,randInt)
{
  let seconds = 7;
  while (true) {
    yield await Promises.tick(seconds * 1000).then(
      crossfader(buildText(assembled05, [randInt(4)]))
    );
  }
}
);
  main.define("initial assembled05", ["randomWord","possessives","nouns","verbs","pronouns"], function(randomWord,possessives,nouns,verbs,pronouns){return(
[
  randomWord(possessives),
  randomWord(nouns),
  randomWord(verbs),
  randomWord(pronouns)
]
)});
  main.variable(observer("mutable assembled05")).define("mutable assembled05", ["Mutable", "initial assembled05"], (M, _) => new M(_));
  main.variable(observer("assembled05")).define("assembled05", ["mutable assembled05"], _ => _.generator);
  main.variable(observer()).define(["md"], function(md){return(
md`We will need a new \`mutable\` for the assembled array that underlies each one of our subsequently versioned displays. Otherwise – if, say, there was only one mutable ‘assembled’ array – they would all be altering this \`mutable\` in a manner that would have indeterminate results.

\`assembled05\` is an array of currently displayed words in the relevant \`div\` of \`index05\` and this is passed to \`buildText()\` so that any of its elements can be altered at will: by default: just one.`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`---

### \`index06\``
)});
  main.variable(observer("index06")).define("index06", ["html"], function(html){return(
html`
<div class='sifther'>
  <div class='mono overlaid index06 text'></div>
  <div class='mono overlaid index06 text visible'></div>
</div>
`
)});
  main.variable(observer("ticker06")).define("ticker06", ["Promises","crossfader","buildText","assembled06","randInt","syntagms06"], async function*(Promises,crossfader,buildText,assembled06,randInt,syntagms06)
{
  let seconds = 7;
  while (true) {
    yield await Promises.tick(seconds * 1000).then(
      crossfader(buildText(assembled06, [randInt(4)], syntagms06), 'index06')
    );
  }
}
);
  main.variable(observer()).define(["md"], function(md){return(
md`For this version, \`buildText()\` was developed so that it could be passed a different array of syntagms. Here, we are passing \`syntagms06\` which contains an array with significantly more verbs. \`syntagms06\` contains at least one verb associated with each of the nine affects.`
)});
  main.variable(observer("syntagms06")).define("syntagms06", ["possessives","maxLength","nouns","verbsAllAffects","pronouns"], function(possessives,maxLength,nouns,verbsAllAffects,pronouns){return(
[
  { words: possessives, pad: maxLength(possessives) },
  { words: nouns, pad: maxLength(nouns) },
  { words: verbsAllAffects, pad: maxLength(verbsAllAffects) },
  { words: pronouns, pad: maxLength(pronouns) }
]
)});
  main.define("initial assembled06", ["randomWord","possessives","nouns","verbs","pronouns"], function(randomWord,possessives,nouns,verbs,pronouns){return(
[
  randomWord(possessives),
  randomWord(nouns),
  randomWord(verbs),
  randomWord(pronouns)
]
)});
  main.variable(observer("mutable assembled06")).define("mutable assembled06", ["Mutable", "initial assembled06"], (M, _) => new M(_));
  main.variable(observer("assembled06")).define("assembled06", ["mutable assembled06"], _ => _.generator);
  main.variable(observer()).define(["md"], function(md){return(
md`---

### \`index07\``
)});
  main.variable(observer("index07")).define("index07", ["html"], function(html){return(
html`
<div class='sifther'>
  <div class='mono overlaid index07 text'></div>
  <div class='mono overlaid index07 text visible'></div>
</div>
`
)});
  main.variable(observer("ticker07")).define("ticker07", ["Promises","crossfader","buildText","assembled07","randInt","syntagms07"], async function*(Promises,crossfader,buildText,assembled07,randInt,syntagms07)
{
  let seconds = 7;
  while (true) {
    yield await Promises.tick(seconds * 1000).then(
      crossfader(buildText(assembled07, [randInt(4)], syntagms07), 'index07')
    );
  }
}
);
  main.variable(observer()).define(["md"], function(md){return(
md`For this version, \`buildText()\` and the functions it calls are developed so that its array of syntagms can include an array of word pairs. The members of such arrays are actually objects rather than strings. Each object consists of a \`.pair\` with an array of the pair’s two strings, and also a \`.display\` boolean indicating whether one or other word still needs to be displayed during a phase in which the pair has been picked. Here, we are passing the mutable \`syntagms07\` array including \`nounPairs\`. Actually, \`syntagms07\` is defined to contain _part_ of \`nounPairs\` sliced from its larger array (that we’ll use in \`index08\`. We can probably build up to a live-configurable version of the piece, one that can be controlled, for example, by changing the number and range of word pairs that are included as potential syntagms.`
)});
  main.variable(observer("syntagms07")).define("syntagms07", ["possessives","maxLength","nounPairs","verbsAllAffects","pronouns"], function(possessives,maxLength,nounPairs,verbsAllAffects,pronouns){return(
[
  { words: possessives, pad: maxLength(possessives) },
  // { words: nounPairs, pad: maxLength(nounPairs) },
  { words: nounPairs.slice(0, 3), pad: maxLength(nounPairs.slice(0, 3)) },
  { words: verbsAllAffects, pad: maxLength(verbsAllAffects) },
  { words: pronouns, pad: maxLength(pronouns) }
]
)});
  main.define("initial assembled07", ["randomWord","possessives","randWord","nounPairs","verbs","pronouns"], function(randomWord,possessives,randWord,nounPairs,verbs,pronouns){return(
[
  randomWord(possessives),
  randWord(nounPairs.slice(0, 3)),
  randomWord(verbs),
  randomWord(pronouns)
]
)});
  main.variable(observer("mutable assembled07")).define("mutable assembled07", ["Mutable", "initial assembled07"], (M, _) => new M(_));
  main.variable(observer("assembled07")).define("assembled07", ["mutable assembled07"], _ => _.generator);
  main.variable(observer()).define(["md"], function(md){return(
md`---

### \`index08\``
)});
  main.variable(observer("index08")).define("index08", ["html"], function(html){return(
html`
<div class='sifther'>
  <div class='mono overlaid index08 text'></div>
  <div class='mono overlaid index08 text visible'></div>
</div>
`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`\`index08\`, which uses all of the \`nounPairs\` array, is the last version of _sifther_ as such. Further development and derivatives from this work will be pursued in a fork, or in a distinctly named duplicate. \`index08\` will not be the website-published version of _sifther_. I’m happiest, at this stage, with \`index07\`.

I’m also coming to the determination that this version of the notebook is in is a reasonable position to serve as basic material for a soon-forthcoming (as of late 2020) digital language art workshop.`
)});
  main.variable(observer("ticker08")).define("ticker08", ["Promises","crossfader","buildText","assembled08","randInt","syntagms08"], async function*(Promises,crossfader,buildText,assembled08,randInt,syntagms08)
{
  let seconds = 9;
  while (true) {
    yield await Promises.tick(seconds * 1000).then(
      crossfader(buildText(assembled08, [randInt(4)], syntagms08), 'index08')
    );
  }
}
);
  main.variable(observer("syntagms08")).define("syntagms08", ["possessives","maxLength","nounPairs","verbsAllAffects","pronouns"], function(possessives,maxLength,nounPairs,verbsAllAffects,pronouns){return(
[
  { words: possessives, pad: maxLength(possessives) },
  { words: nounPairs, pad: maxLength(nounPairs) },
  { words: verbsAllAffects, pad: maxLength(verbsAllAffects) },
  { words: pronouns, pad: maxLength(pronouns) }
]
)});
  main.define("initial assembled08", ["randomWord","possessives","randWord","nounPairs","verbs","pronouns"], function(randomWord,possessives,randWord,nounPairs,verbs,pronouns){return(
[
  randomWord(possessives),
  randWord(nounPairs),
  randomWord(verbs),
  randomWord(pronouns)
]
)});
  main.variable(observer("mutable assembled08")).define("mutable assembled08", ["Mutable", "initial assembled08"], (M, _) => new M(_));
  main.variable(observer("assembled08")).define("assembled08", ["mutable assembled08"], _ => _.generator);
  main.variable(observer()).define(["md"], function(md){return(
md`---

### \`index10\``
)});
  main.variable(observer("index10")).define("index10", ["html"], function(html){return(
html`
<div class='sifther10'>
  <div class='mono w0 text'></div>
  <div class='mono w0 text visible'>their</div>
  <div class='mono w1 text'></div>
  <div class='mono w1 text visible'>inferiority</div>
  <div class='mono w2 text'></div>
  <div class='mono w2 text visible'>confuses</div>
  <div class='mono w3 text'></div>
  <div class='mono w3 text visible'>her</div>
</div>
`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`Skipping \`09\` and making  an \`index10\`, with some new code because the earlier web-publishable version, \`07\`, does not make enough of an impression when the display is a 1080p tablet. One line of text – even when only four words in extent – cannot be large enough when set out as a line for the tablet display. This version will stack the words of the text and will perform the crossfade transition only on the randomly selected word in each phase.

The standalone web-published version is here: [https://shadoof.github.io/sifther](https://shadoof.github.io/sifther).`
)});
  main.variable(observer("sifther10")).define("sifther10", ["Promises","randInt","assembled10","randWord","syntagms07","crossfader"], async function*(Promises,randInt,assembled10,randWord,syntagms07,crossfader)
{
  let seconds = 9;
  while (true) {
    // let indexes = shuffle([0, 1, 2, 3]); // ...Array(4).keys()
    // for (let i of indexes) {
    yield await Promises.tick(seconds * 1000).then(() => {
      let i = randInt(4);
      assembled10[i] = randWord(syntagms07[i].words, assembled10[i]);
      crossfader(assembled10[i], 'w' + i);
    });
    // }
  }
}
);
  main.define("initial assembled10", ["randWord","possessives","nounPairs","verbs","pronouns"], function(randWord,possessives,nounPairs,verbs,pronouns){return(
[
  randWord(possessives),
  randWord(nounPairs.slice(0, 3)),
  randWord(verbs),
  randWord(pronouns)
]
)});
  main.variable(observer("mutable assembled10")).define("mutable assembled10", ["Mutable", "initial assembled10"], (M, _) => new M(_));
  main.variable(observer("assembled10")).define("assembled10", ["mutable assembled10"], _ => _.generator);
  main.variable(observer()).define(["md"], function(md){return(
md`---

### Constants`
)});
  main.variable(observer("nouns")).define("nouns", function(){return(
["inferiority", "interiority" ]
)});
  main.variable(observer("nounPairs")).define("nounPairs", function(){return(
[
  { pair: ["inferiority", "interiority"], display: true },
  { pair: ["rationality", "nationality"], display: true },
  { pair: ["nationalism", "rationalism"], display: true },
  { pair: ["impunity", "impurity"], display: true },
  { pair: ["oath", "path"], display: true },
  { pair: ["premise", "promise"], display: true },
  { pair: ["sheen", "sneer"], display: true }
]
)});
  main.variable(observer("possessives")).define("possessives", function(){return(
["my", "your", "his", "her", "their", "our", "your", "their"]
)});
  main.variable(observer("pronouns")).define("pronouns", function(){return(
["me", "you", "him", "her", "them", "us", "you", "them"]
)});
  main.variable(observer("verbsAllAffects")).define("verbsAllAffects", function(){return(
[
  "delights",
  "excites",
  "impresses",
  "embarrasses",
  "shames",
  "distresses",
  "disgusts",
  "frightens",
  "enrages",
  "attracts",
  "confuses"
]
)});
  main.variable(observer("verbs")).define("verbs", function(){return(
["embarrasses", "impresses", "frightens", "attracts", "confuses"]
)});
  main.variable(observer()).define(["md"], function(md){return(
md`Above are the verbs that were in mind during initial development of the sketch.`
)});
  main.variable(observer("postiveAffect")).define("postiveAffect", function(){return(
["delights", "excites"]
)});
  main.variable(observer("neutralAffect")).define("neutralAffect", function(){return(
["surprises"]
)});
  main.variable(observer("negativeAffect")).define("negativeAffect", function(){return(
["shames", "distresses", "disgusts", "frightens", "enrages"]
)});
  main.variable(observer()).define(["md"], function(md){return(
md`### Mutables`
)});
  main.define("initial assembled", ["randomWord","possessives","nouns","verbs","pronouns"], function(randomWord,possessives,nouns,verbs,pronouns){return(
[
  randomWord(possessives),
  randomWord(nouns),
  randomWord(verbs),
  randomWord(pronouns)
]
)});
  main.variable(observer("mutable assembled")).define("mutable assembled", ["Mutable", "initial assembled"], (M, _) => new M(_));
  main.variable(observer("assembled")).define("assembled", ["mutable assembled"], _ => _.generator);
  main.variable(observer()).define(["md"], function(md){return(
md`### Functions`
)});
  main.variable(observer("assembleText")).define("assembleText", ["randomWord","possessives","nouns","verbs","pronouns"], function(randomWord,possessives,nouns,verbs,pronouns){return(
() =>
  `${randomWord(possessives)} ${randomWord(nouns)} ${randomWord(
    verbs
  )} ${randomWord(pronouns)}`
)});
  main.variable(observer("buildText")).define("buildText", ["possessives","maxLength","nouns","verbs","pronouns","randWord"], function(possessives,maxLength,nouns,verbs,pronouns,randWord){return(
(
  currentAssembly,
  whichChange = [...Array(4).keys()],
  syntagms = [
    { words: possessives, pad: maxLength(possessives) },
    { words: nouns, pad: maxLength(nouns) },
    { words: verbs, pad: maxLength(verbs) },
    { words: pronouns, pad: maxLength(pronouns) }
  ],
  pad = true
) => {
  let theText = '';
  for (let i = 0; i < currentAssembly.length; i++) {
    let word;
    if (whichChange.includes(i)) {
      // passing the current word to randWord avoids immediate repetition
      currentAssembly[i] = randWord(syntagms[i].words, currentAssembly[i]);
    }
    if (pad) {
      // when padding: add an extra space between the two large words:
      let cosmeticSpace = pad && i == 1 ? ' ' : ''; // HARD CODING HERE
      word = currentAssembly[i].padEnd(syntagms[i].pad) + cosmeticSpace;
    } else word = currentAssembly[i];
    theText += word + ' ';
  }
  return theText;
}
)});
  main.variable(observer("randomWord")).define("randomWord", ["randInt"], function(randInt){return(
function randomWord(wordArray, currentWord) {
  // only works with flat arrays of words
  let safetyCounter = 0,
    word;
  do {
    word = wordArray[randInt(wordArray.length)];
  } while (
    currentWord != undefined &&
    word == currentWord &&
    safetyCounter++ < 100
  );
  return word;
}
)});
  main.variable(observer("randInt")).define("randInt", function(){return(
maxPlusOne => (maxPlusOne * Math.random()) | 0
)});
  main.variable(observer("rpad")).define("rpad", ["maxLength"], function(maxLength){return(
strings => {
  let padded = []; // make this 'pure' - doesn't alter the strings array
  for (let s of strings) {
    padded.push(s.padEnd(maxLength(strings), ' '));
  }
  return padded;
}
)});
  main.variable(observer("maxLength")).define("maxLength", function(){return(
function maxLength(strings) {
  let allStrings = [];
  strings.forEach(object => {
    if (typeof object == 'string') allStrings.push(object);
    else allStrings = allStrings.concat([...object.pair]);
  });
  return allStrings.sort(function(a, b) {
    return b.length - a.length;
  })[0].length;
}
)});
  main.define("initial lastWord", function(){return(
"placeholder"
)});
  main.variable(observer("mutable lastWord")).define("mutable lastWord", ["Mutable", "initial lastWord"], (M, _) => new M(_));
  main.variable(observer("lastWord")).define("lastWord", ["mutable lastWord"], _ => _.generator);
  main.variable(observer()).define(function()
{
  // let seconds = 3;
  // while (true) {
  //   let temp = randWord(nounPairs, lastWord);
  //   yield Promises.tick(seconds * 1000).then(
  //     () => (mutable lastWord = randWord(nounPairs, lastWord))
  //   );
  // }
}
);
  main.variable(observer()).define(["randWord","nounPairs"], function(randWord,nounPairs)
{
  return randWord(nounPairs, "nationalism");
}
);
  main.variable(observer("randWord")).define("randWord", ["randInt","pairIndex"], function(randInt,pairIndex){return(
function randWord(wordArray, currentWord) {
  let wordObject,
    pickedWordObject,
    safetyCounter = 0;
  // first, don't pick the same string:
  do {
    wordObject = wordArray[randInt(wordArray.length)];
    // console.log(`wordObject ${wordObject}, currentWord ${currentWord}`);
  } while (typeof wordObject == 'string' && wordObject == currentWord);
  let wordArrayIndex = pairIndex(currentWord, wordArray);
  // if we have picked a different string and
  // the currentWord is not from a pair, return it
  if (typeof wordObject == 'string' && wordArrayIndex == -1) {
    // console.log(`returning a string: ${wordObject}`);
    return wordObject;
  } else {
    if (wordArrayIndex == -1) {
      // currentWord comes from another pair
      // console.log(`currentWord ${currentWord} comes from another wordObject`);
      // and so we reset here:
      wordObject.display = true; // [true, true];
      let pairIndex = randInt(2);
      // wordObject.display[pairIndex] = false;
      // console.log(`new pair, return either one ${wordObject.pair[pairIndex]}`);
      return wordObject.pair[pairIndex];
    } else {
      // console.log(`currentWord ${currentWord} comes from picked pair`);
      wordObject = wordArray[wordArrayIndex];
      if (wordObject.display == false) {
        //  && wordObject.display[1] == false
        // console.log(`both members of the pair have been displayed`);
        return randWord(wordArray, wordObject);
      }
      let mateIndex = (wordObject.pair.indexOf(currentWord) + 1) % 2;
      wordObject.display = false; // mateIndex
      // console.log(`display other word in pair: done`);
      return wordObject.pair[mateIndex];
    }
  }
}
)});
  main.variable(observer("pairIndex")).define("pairIndex", function(){return(
function pairIndex(item, arr) {
  let index = -1;
  for (let i = 0; i < arr.length; i++) {
    if (typeof arr[i] != 'string') {
      let j = arr[i].pair.indexOf(item);
      if (j != -1) {
        // console.log(`found ${item} at ${i} in wordArray`);
        index = i;
      }
    }
  }
  return index;
}
)});
  main.variable(observer()).define(["shuffle"], function(shuffle)
{
  return shuffle([...Array(4).keys()]);
}
);
  main.variable(observer("shuffle")).define("shuffle", ["randInt"], function(randInt){return(
(arr) => {
  for (let i = arr.length - 1; i >= 0; i--) {
    let randomIndex = randInt(i + 1); // Math.floor(Math.random() * (i + 1));
    let itemAtIndex = arr[randomIndex];
    arr[randomIndex] = arr[i];
    arr[i] = itemAtIndex;
  }
  return arr;
}
)});
  main.variable(observer()).define(["md"], function(md){return(
md`### Files`
)});
  main.variable(observer("andaleMono")).define("andaleMono", ["FileAttachment"], function(FileAttachment){return(
FileAttachment("Andale Mono.ttf")
)});
  main.variable(observer()).define(["md"], function(md){return(
md`This is obviously not how it would normally be done in a web app. Files can also be loaded from your local system. Here the font file is ‘attached’ to the notebook and then referenced in the \`<style\`> cell below to ensure that everyone reading this notebook online sees the correct monospaced font, Andale Mono. You can see that the syntax for the reference in the \`<style\`> cell is a little trickly.`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`### Imports`
)});
  const child1 = runtime.module(define1);
  main.import("caret", child1);
  main.variable(observer("css")).define("css", ["html","andaleMono"], async function(html,andaleMono){return(
html`
<style>

  @font-face {
    font-family: 'AndaleMono';
    src: url('${await andaleMono.url()}');
  }

  .sifther {
    min-height: 90px;
    padding-top: 30px;
  }

  .sifther10 {
    position: relative;
    min-height: 220px;
  }

  .mono {
    font-family: 'AndaleMono', monospace;
    font-size: 32px;
    white-space: pre;
   }

  .overlaid {
    position: absolute;
  }

  .regular {font: 36px 'Minion Pro';}

  .text {
    color: rgba(0,0,0,0);
    transition: color 1.5s ease-in-out;
  }

  .text.visible {
    color: rgba(0,0,0,255);
      /* starts readable */
  }

  .w0 {
    position: absolute;
    top: 20px;
    left: 120px;
  }

  .w1 {
    position: absolute;
    top: 60px;
    left: 120px;
  }

  .w2 {
    position: absolute;
    top: 100px;
    left: 120px;
  }

  .w3 {
    position: absolute;
    top: 140px;
    left: 120px;
  }

</style>
`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`---

### Resources`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`*Since this notebook will be used in a workshop, I’m adding this section of external code, code-editing, and hosting resources orginally suggested to me by the people who recommended Observable in the first place.*
* [JSFiddle](https://jsfiddle.net/), [Codepen](https://codepen.io/) - lightweight online code editors
* [Glitch](https://glitch.com/) - similar, but more powerful, geared toward web app development 
* [GitHub Pages](https://pages.github.com/) - a potential hosting option for students already familiar with coding and using GitHub.
`
)});
  return main;
}
