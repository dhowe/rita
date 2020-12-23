
let txt = "Last Wednesday we decided to visit the zoo. We arrived the next morning after we breakfasted, cashed in our passes and entered. We walked toward the first exhibits. I looked up at a giraffe as it stared back at me. I stepped nervously to the next area. One of the lions gazed at me as he lazed in the shade while the others napped. One of my friends first knocked then banged on the tempered glass in front of the monkey's cage. They howled and screamed at us as we hurried to another exhibit where we stopped and gawked at plumed birds. After we rested, we headed for the petting zoo where we petted wooly sheep who only glanced at us but the goats butted each other and nipped our clothes when we ventured too near their closed pen. Later, our tired group nudged their way through the crowded paths and exited the turnstiled gate. Our car bumped, jerked and swayed as we dozed during the relaxed ride home.";

function setup()
{
  createCanvas(600, 400);   
  setTimeout(nextWord, 2000);
}

function draw() {
  fill(0);
  textSize(16);
  textLeading(20);
  background(250);
  text(text, 50, 30, 500, 10000);
}

//  replace a random word in the paragraph with one
//  from wordnet with the same (basic) part-of-speech 
function nextWord()
{   
  let words = text.split(" ");

  // loop from a random spot
  let count = floor(random(0, words.length));
  for (let i = count; i < words.length; i++) 
  {
    // only words of 3 or more chars
    if (words[i].length() < 3) continue;

    let pos = Tagger.allTags(words[i].toLowerCase())[0];  

    if (pos != null) 
    {
      // get the synset
      let syns = RiTa.rhymes(words[i]);

      // only words with >1 rhymes
      if (syns.length<2) continue;

      // pick a random rhyme
      let randIdx = floor(random(0, syns.length));
      let newStr = syns[randIdx];

      if (Character.isUpperCase(words[i].charAt(0))) {             
        newStr = RiTa.capitalize(newStr); // keep capitals
      }

      //println("replace: "+words[i]+" -> "+newStr);

      // and make a substitution
      text = text.replaceAll("\\b"+words[i]+"\\b", newStr);
      break;
    }
  }
}     
