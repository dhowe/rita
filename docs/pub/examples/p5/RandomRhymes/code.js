/* 
 * This is a very bare-bones example. For better results, you will want to pre and post-process the text. 
 * For more info on using rita's unbounded n-grams, see https://observablehq.com/@dhowe/tut-rita-ngrams
 */

let lines, markov, txt1, txt2;
let x = 160, y = 240;

async function setup() {

  createCanvas(500, 500);
  textFont('helvetica', 16);
  textLeading(21);
  textAlign(LEFT);

  lines = ["click to (re)generate"];

  txt1 = await loadStrings('wittgenstein.txt');
  txt2 = await loadStrings('kafka.txt');
  
  // create a markov model w' n=4
  markov = RiTa.markov(4);

  // load text into the model
  markov.addText(txt1.join(' '));
  markov.addText(txt2.join(' '));

  drawText();
}

function drawText() {
  background(50, 30, 40);
  fill(220);
  text(lines.join(' '), x, y, 420, 440);
}

function mouseClicked() {
  lines = markov.generate({ numSentences: 10 });
  x = y = 40;
  drawText();
}

  
 




