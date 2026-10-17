
let txt = "Last Wednesday we decided to visit the zoo. We arrived the next morning after we breakfasted, cashed in our passes and entered. We walked toward the first exhibits. I looked up at a giraffe as it stared back at me. I stepped nervously to the next area. One of the lions gazed at me as he lazed in the shade while the others napped. One of my friends first knocked then banged on the tempered glass in front of the monkey cage. They howled and screamed at us as we hurried to another exhibit where we stopped and gawked at plumed birds. After we rested, we headed for the petting zoo where we petted wooly sheep who only glanced at us but the goats butted each other and nipped our clothes when we ventured too near their closed pen. Later, our tired group nudged their way through the crowded paths and exited the turnstiled gate. Our car bumped, jerked and swayed as we dozed during the relaxed ride home.";

function setup() {

  createCanvas(600, 400).parent('#cdiv');
  noStroke();
  textSize(17.5);
  loadFont('../../data/Chaparral.otf', nextWord);
}

// replace one random word in the text
async function nextWord() {

  let words = RiTa.tokenize(txt); // split into words

  // loop from a random spot
  let r = floor(random(0, words.length));
  for (let i = r; i < words.length + r; i++) {

    let idx = i % words.length;
    let word = words[idx].toLowerCase();
    if (word.length < 3) continue; // len >= 3

    // find related words
    let pos = RiTa.tagger.allTags(word)[0];
    let rhymes = await RiTa.rhymes(word, { pos });
    let sounds = await RiTa.soundsLike(word, { pos });
    let spells = await RiTa.spellsLike(word, { pos });
    let similars = [...rhymes, ...sounds, ...spells];

    // only words with 2 or more similars
    if (similars.length < 2) {
      console.log("No sims for "+word);
      continue;
    }

    // pick a random similar
    let next = RiTa.random(similars);

    if (next.includes(word) || word.includes(next)) {
      continue;                     // skip substrings
    }
    
    if (/[A-Z]/.test(words[idx][0])) {
      next = RiTa.capitalize(next); // keep capitals
    }

    console.log("replace(" + idx + "): " + word + " -> " + next);

    words[idx] = next;             // do replacement
    break;
  }

  // recombine into string and display
  txt = RiTa.untokenize(words); 
  background(20, 30, 55);
  fill(250, 240, 230);
  text(txt, 50, 30, 500, height);

  setTimeout(nextWord, 2000);
}
