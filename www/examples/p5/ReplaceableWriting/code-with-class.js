
let txt = "Last Wednesday we decided to visit the zoo. We arrived the next morning after we breakfasted, cashed in our passes and entered. We walked toward the first exhibits. I looked up at a giraffe as it stared back at me. I stepped nervously to the next area. One of the lions gazed at me as he lazed in the shade while the others napped. One of my friends first knocked then banged on the tempered glass in front of the monkey's cage. They howled and screamed at us as we hurried to another exhibit where we stopped and gawked at plumed birds. After we rested, we headed for the petting zoo where we petted wooly sheep who only glanced at us but the goats butted each other and nipped our clothes when we ventured too near their closed pen. Later, our tired group nudged their way through the crowded paths and exited the turnstiled gate. Our car bumped, jerked and swayed as we dozed during the relaxed ride home.";
let paused = false, words = [];

function setup() {
  createCanvas(600, 400);
  loadFont('Chaparral.otf', nextWord);
}

function draw() {
  background(250);
  for (let i = 0; words && i < words.length; i++) {
    words[i].draw();
  }
}

//  replace a random word in the paragraph every 2 sec
function nextWord() {

  if (words.length) {

    // loop from a random spot
    let r = floor(random(0, words.length));
    for (let i = r; i < words.length + r; i++) {

      let idx = i % words.length
      let word = words[idx].text;

      // only words of 3 or more chars
      if (word.length < 3) continue;

      let fpos = RiTa.tagger.allTags(word.toLowerCase())[0];
      if (fpos != null) {
        let syns = RiTa.rhymes(word, { pos: fpos });

        // only words with >1 rhymes
        if (syns.length < 2) continue;

        // pick a random rhyme
        let randIdx = floor(random(0, syns.length));
        let next = syns[randIdx];

        if (/A-Z/.test(word[0])) {
          next = RiTa.capitalize(next); // keep capitals
        }

        selected = idx;
        words[idx].text = next; // make a substitution
        console.log("replace(" + idx + "): " + word + " -> " + next);
        words[idx].hilite();
        break;
      }
    }
    txt = RiTa.untokenize(words.map(w => w.text));
  }
  else { // first time
    textSize(16);
    textLeading(20);
  }

  createWords(words, txt, 50, 30, 500, 20);
  setTimeout(nextWord, 2000); // 2 sec
}


function createWords(words, txt, tx, ty, tw, lead) {
  let strs = RiTa.tokenize(txt);
  if (!words[0]) words[0] = new Word(strs[0]);
  words[0].position(tx, ty);
  let spcw = textWidth(' ');
  for (let i = 1; i < strs.length; i++) {
    let x = words[i - 1].x + textWidth(strs[i - 1]);
    if (!RiTa.isPunct(strs[i])) x += spcw;
    let y = words[i - 1].y;
    if (i < strs.length - 1) {
      let nw = textWidth(strs[i]);
      if (RiTa.isPunct(strs[i + 1])) nw += textWidth(strs[i + 1]);
      if (x > (tx + tw) - nw) {
        y += lead;
        x = tx;
      }
    }
    if (!words[i]) words[i] = new Word(strs[i]);
    words[i].position(x, y);
  }
}

class Word {
  constructor(s) {//, tx, ty) {
    /* this.x = tx;
    this.y = ty; */
    this.text = s;
    this.w = textWidth(s);
    this.d = textDescent();
    this.h = textAscent() + this.d;
    this.oc = colors[floor(random(colors.length))];
    this.c = [this.oc[0], this.oc[1], this.oc[2], this.oc[3]];
  }
  position(x, y) {
    this.x = x;
    this.y = y;
  }
  contains(mx, my) {
    return mx >= this.x && mx <= this.x + w &&
      my <= this.y + this.d && my >= this.y - this.h;
  }
  hilite() {
    this.c = [200, 0, 0, 100];//this.oc[3];
    console.log('hi:' + this.text, this.c);
    this.ts = millis();
  }
  draw() {
    noStroke();
    fill(this.c[0], this.c[1], this.c[2], this.c[3]);
    rect(this.x, this.y + this.d, this.w, -this.h);
    fill(0);
    text(this.text, this.x, this.y);
    //if (this.c[3] > 0) this.c[3]--;// = lerp(this.c[3], 0, (millis() - this.ts) / 100000.0));
  }

}

const colors = [
  [172, 180, 200, 70],
  [192, 178, 194, 100],
  [186, 180, 187, 70],
  [211, 219, 231, 150],
  [249, 238, 243, 255], //pink
  [199, 198, 206, 100]
];