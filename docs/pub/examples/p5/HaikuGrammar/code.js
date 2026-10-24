/*
 * Note that this is a rather bare-bones example. 
 * For a more complete example, see https://observablehq.com/@dhowe/rita-grammars
 * For more advanced grammar and riscript features, see https://observablehq.com/@dhowe/tut-rita-ngrams#advanced
 */

let font, grammar, json;
let lines = ["click to", "generate", "a haiku"];

async function setup() {

  createCanvas(650, 200);
  textAlign(CENTER);
  loadFont('../../data/Resagokr.otf', f => textFont(f, 30));

  json = await loadJSON('../../data/haiku.json');
  grammar = RiTa.grammar(json);
}

function draw() {

  background(230, 240, 255);
  text(lines[0], width / 2, 75);
  text(lines[1], width / 2, 110);
  text(lines[2], width / 2, 145);
}

function mouseReleased() {

  let result = grammar.expand();
  
  // split on % characters in the grammar
  lines = result.split("%");  
}