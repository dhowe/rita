let word, features, hues;
let bubbles = [], maxWordLen = 12;

function setup() {

  createCanvas(600, 300);
  colorPalette();
  noStroke();

  // initialize bubbles
  for (let i = 0; i < maxWordLen; i++) {
    bubbles[i] = new Bubble();
  }

  selectWord();
}

function draw() {

  background(255);

  fill(56, 66, 90);
  textSize(36);
  textAlign(LEFT);
  textStyle(NORMAL);
  text(word, 80, 50);

  textSize(18);
  text(ipaPhones(word), 80, 80);

  textSize(14);
  textStyle(ITALIC);
  text(tags[features.pos], 80, 105);

  bubbles.forEach((b, i) => b.draw(i));
}

function selectWord() {

  word = RiTa.randomWord({ maxLength: maxWordLen });
  features = RiTa.analyze(word, { simple: true });
  updateBubbles();
}

function updateBubbles() {

  bubbles.forEach(b => b.reset());

  let phones = features.phones.split('-');
  bubbles.forEach((b, i) => {
    if (i < phones.length) b.update(phones, i);
  });

  addStressesAndSyllables();
  setTimeout(selectWord, 4000);
}

function ipaPhones(aWord) {
  let raw = RiTa.lexicon.rawPhones(aWord);
  return "/" + arpaToIPA(raw) + "/";
}

class Bubble {

  constructor() {
    this.gspd = 0; // grow speed
    this.rad = 40; // radius
    this.t = 0; // timer
    this.gravity = 0.5;
    this.ypos = 150;
    this.speed = 0;
  }

  reset() {
    this.ph = '';
    this.t = 0;
    this.gspd = 0;
    this.speed = 0;
  }

  update(phones, i) {
    this.c = phoneColor(phones[i]);
    this.ph = phones[i];
    this.ypos = 150;
    this.xpos = i * 40 + 100;
    this.rad = 40;
  }

  adjustDistance(dis) {
    this.xpos += dis;
  }

  grow() {
    this.rad = 41;
    this.gspd = 0.5;
  }

  draw(i) {

    if (this.ph.length < 1) return;

    fill(this.c);
    ellipse(this.xpos, this.ypos, this.rad + this.gspd, this.rad + this.gspd);

    fill(255);
    textSize(18);
    textAlign(CENTER, CENTER);
    text(this.ph, this.xpos, this.ypos - 1);

    if (this.gspd < 10) this.gspd *= 1.1;

    if (++this.t > 100 + 2 * i) {
      this.speed += this.gravity;
      this.ypos += this.speed;
    }
  }
}

function addStressesAndSyllables() {

  // Split stresses & syllables
  let stresses = features.stresses.split('/'),
    syllables = features.syllables.split('/');

  if (stresses.length !== syllables.length) {
    console.error("invalid state");
  }

  // Initialize vars for distance adjustment
  let totalMergeWidth = 0;

  // Record the previous phoneme count
  for (let i = 0, past = 0; i < syllables.length; i++) {
    let phs = syllables[i].split('-');
    let adjustUnit = 10, gapWidth = 8;

    // Add stress(es) first
    if (stresses[i] === '1') {
      for (let j = 0; j < phs.length; j++) {
        let b = bubbles[past + j];
        if (!b) console.error("null bubble(1): " + (past + j), word, features);
        b && b.grow();
      }
      adjustUnit *= 0.7;
      gapWidth += 5;
    }
    if (i + 1 < syllables.length && stresses[i + 1] === '1') {
      gapWidth += 5;
    }
    // Now adjust the distance
    for (let j = 0; j < phs.length; j++) {
      let b = bubbles[past + j];
      if (!b) console.error("null bubble(2): " + (past + j), word, features);
      b && b.adjustDistance(-(adjustUnit * j + totalMergeWidth));
    }

    totalMergeWidth += adjustUnit * (phs.length - 1) - gapWidth;
    past += phs.length;
  }
}

function addSyllables() {

  // Split each syllable
  let syllable = features.syllables.split('/');

  // Record the past phonemes number
  for (let i = 0, past = 0; i < syllable.length; i++) {
    let phs = syllable[i].split('-');

    for (let j = 1; j < phs.length; j++) {
      bubbles[past + j].adjustDistance(-10 * j);
    }

    past += phs.length;
  }
}


function addStresses() {

  // Split stresses & syllables
  const stress = features.stresses.split('/'),
    syllables = features.syllables.split('/');

  // Record the previous phoneme count
  for (let i = 0, past = 0; i < stress.length; i++) {
    let phs = syllables[i].split('-');

    // if the syllable is stressed, grow its bubbles
    if (stress[i] == RiTa.STRESS) {
      for (let j = 0; j < phs.length; j++) {
        bubbles[past + j].grow();
      }
    }
    past += phs.length;
  }
}

function phoneColor(phoneme) {
  let idx = RiTa.PHONES.indexOf(phoneme);
  return idx > -1 ? hues[idx] : 0;
}

function colorPalette() {

  colorMode(HSB, 1, 1, 1, 1);
  hues = [];
  let apl = RiTa.PHONES.length;
  for (let i = 0; i < apl; i++) {
    let h = map(i, 0, apl, .2, .8);
    hues[i] = color(h, .9, .9, .6);
  }
  colorMode(RGB, 255, 255, 255, 255);
}

const tags = {
  'n': 'noun',
  'v': 'verb',
  'r': 'adverb',
  'a': 'adjective'
};
