
let txt, word, keywords = [
  "Gregor", "Samsa", "family", "being",
  "clerk", "room", "violin", "window"
];

function preload() {

  txt = loadStrings('../../data/kafka.txt');
}

function setup() {

  createCanvas(800, 500);
  textFont('Times New Roman', 16);

  RiTa.concordance(txt.join('\n')); // create concordance
  word = RiTa.random(keywords); // pick a word to start

  createButtons();
}

function draw() {

  // get kwic lines for the word
  let kwic = RiTa.kwic(word, 6);
  let tw = textWidth(word) / 2;

  background(250);
  let num = min(10, kwic.length);
  for (let i = 0; i < num; i++) {

    // get the parts, stripping line-breaks
    let parts = kwic[i].split(word)
      .map(p => p.replace(/\n/g,' '));
    
    let x = width / 2, y = i * 24 + 90;
    if (y > height - 20) return;

    fill(0);
    textAlign(RIGHT); // context-before-word
    text(parts[0], x - tw, y);

    fill(200, 0, 0);
    textAlign(CENTER);
    text(word, x, y);  // the word itself

    fill(0);
    textAlign(LEFT); // context-after-word
    text(parts[1], x + tw, y);
  }
  noLoop();
}

function createButtons() {

  // create array of buttons
  let buttons = [], buttonsW = 0, gap = 10;
  for (let i = 0; i < keywords.length; i++) {
    let button = createButton(keywords[i]);
    console.log(button.elt.textContent);
    button.class("button");
    button.style('color', keywords[i] === word ? 'rgb(200,0,0)' : 'black');
    buttonsW += button.width;
    buttons.push(button);
  }

  // center and position each button
  let totalW = (keywords.length * gap) + buttonsW;
  let sofar = 0, startX = width / 2 - totalW / 2;
  for (let i = 0; i < buttons.length; i++) {
    buttons[i].position(startX + sofar, 30);
    sofar += buttons[i].width + gap;
  }

  // add handler function for each
  buttons.forEach((b, i) => b.mouseClicked(() => {
    word = b.elt.textContent;
    buttons.forEach(but => but.style('color', 'black'));
    b.style('color', 'rgb(200,0,0)'); // make clicked button red
    loop();
  }));
}

    



