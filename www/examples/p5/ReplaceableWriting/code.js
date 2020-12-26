
let txt = "Last Wednesday we decided to visit the zoo. We arrived the next morning after we breakfasted, cashed in our passes and entered. We walked toward the first exhibits. I looked up at a giraffe as it stared back at me. I stepped nervously to the next area. One of the lions gazed at me as he lazed in the shade while the others napped. One of my friends first knocked then banged on the tempered glass in front of the monkey's cage. They howled and screamed at us as we hurried to another exhibit where we stopped and gawked at plumed birds. After we rested, we headed for the petting zoo where we petted wooly sheep who only glanced at us but the goats butted each other and nipped our clothes when we ventured too near their closed pen. Later, our tired group nudged their way through the crowded paths and exited the turnstiled gate. Our car bumped, jerked and swayed as we dozed during the relaxed ride home.";
let words = [], wx = [], wy = [], selected, salpha, spc;

// TODO: highlight word first, then change it, then fade

function setup() {

  createCanvas(600, 400);
  noStroke();
  loadFont('Chaparral.otf', nextWord);
}


function draw() {
  background(250);
  for (let i = 0; words && i < words.length; i++) {
    if (i == selected) {
      fill(100,0,0,salpha);
      rect(wx[i], wy[i]+textDescent(), 
        textWidth(words[i]), -(textDescent()+textAscent()));
    }
    fill(0);
    text(words[i], wx[i], wy[i]);
  }
  salpha-=.5;
}

//  replace a random word in the paragraph every 2 sec
function nextWord() {
  
  if (words.length) {
  
    // loop from a random spot
    let r = floor(random(0, words.length));
    for (let i = r; i < words.length + r; i++) {

      let idx = i % words.length
      let word = words[idx];

      // only words of 3 or more chars
      if (word.length < 3) continue;

      let fpos = RiTa.tagger.allTags(word.toLowerCase())[0];
      let syns = RiTa.rhymes(word, { pos: fpos });

      // only words with >1 rhymes
      if (syns.length < 2) continue;

      // pick a random rhyme
      let randIdx = floor(random(0, syns.length));
      let next = syns[randIdx];

      if (/[A-Z]/.test(word[0])) {
        next = RiTa.capitalize(next); // keep capitals
      }

      salpha = 50;
      selected = idx;

      words[idx] = next; // make a substitution
      console.log("replace(" + idx + "): " + word + " -> " + next);
      break;
    }
    txt = RiTa.untokenize(words);
  }
  else { // first time
    textSize(16);
    textLeading(20);
    spc = textWidth(' ');
  }

  layout(50, 30, 500, 20);
  setTimeout(nextWord, 2000); // 2 sec
}

function layout(tx, ty, tw, lead) {

  words = RiTa.tokenize(txt);
  wx[0] = tx; wy[0] = ty;
  for (let i = 1; i < words.length; i++) {
    let x = wx[i - 1] + textWidth(words[i - 1]);
    if (!RiTa.isPunctuation(words[i])) x += spc;
    let y = wy[i - 1];
    if (i < words.length - 1) {
      let nw = textWidth(words[i]);
      if (RiTa.isPunctuation(words[i + 1])) nw += textWidth(words[i + 1]);
      if (x > (tx + tw) - nw) {
        y += lead;
        x = tx;
      }
    }
    wx[i] = x;
    wy[i] = y;
  }
}