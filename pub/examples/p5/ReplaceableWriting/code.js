
let txt = "Last Wednesday we decided to visit the zoo. We arrived the next morning after we breakfasted, cashed in our passes and entered. We walked toward the first exhibits. I looked up at a giraffe as it stared back at me. I stepped nervously to the next area. One of the lions gazed at me as he lazed in the shade while the others napped. One of my friends first knocked then banged on the tempered glass in front of the monkey's cage. They howled and screamed at us as we hurried to another exhibit where we stopped and gawked at plumed birds. After we rested, we headed for the petting zoo where we petted wooly sheep who only glanced at us but the goats butted each other and nipped our clothes when we ventured too near their closed pen. Later, our tired group nudged their way through the crowded paths and exited the turnstiled gate. Our car bumped, jerked and swayed as we dozed during the relaxed ride home.";

function setup() {
  createCanvas(600, 400);
  nextWord();
}

function draw() {
  fill(0);
  textSize(16);
  textLeading(20);
  background(250);
  text(txt, 50, 30, 500, 10000);
}

function mouseClicked() {
  paused = !paused;
  if (!paused) nextWord();
}

//  replace a random word in the paragraph with one
//  with the same (basic) part-of-speech that rhymes
function nextWord() {

  let words = RiTa.tokenize(txt);

  // loop from a random spot
  let count = floor(random(0, words.length));

  for (let i = count; i < words.length; i++) {
    let word = words[i];

    // only words of 3 or more chars
    if (word.length < 4) continue;

    let pos = RiTa.tagger.allTags(word.toLowerCase())[0];

    if (pos != null) {
word = "abated";
      console.log("rhymes: " + word + ",",{pos});

      let rhymes = RiTa.rhymes(word, { pos });

      // only words with >1 rhymes
      if (rhymes.length < 2) continue;

      // pick a random rhyme
      let newStr = RiTa.random(rhymes);

      if (/[A-Z]/.test(word[0])) {
        newStr = RiTa.capitalize(newStr); // keep capitals
      }

      console.log("replace: " + word + " -> " + newStr);

      // and make the substitution
      txt = txt.replace(new RegExp("\\b" + word + "\\b", 'g'), newStr);
      break;
    }
  }
  if (!paused) {
    setTimeout(nextWord, 2000);
  }
}     
