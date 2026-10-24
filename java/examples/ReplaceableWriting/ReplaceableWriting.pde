
import rita.*;
import java.util.*;

int last = -9999;

String txt = "Last Wednesday we decided to visit the zoo. We arrived the next morning after we breakfasted, cashed in our passes and entered. We walked toward the first exhibits. I looked up at a giraffe as it stared back at me. I stepped nervously to the next area. One of the lions gazed at me as he lazed in the shade while the others napped. One of my friends first knocked then banged on the tempered glass in front of the monkey cage. They howled and screamed at us as we hurried to another exhibit where we stopped and gawked at plumed birds. After we rested, we headed for the petting zoo where we petted wooly sheep who only glanced at us but the goats butted each other and nipped our clothes when we ventured too near their closed pen. Later, our tired group nudged their way through the crowded paths and exited the turnstiled gate. Our car bumped, jerked and swayed as we dozed during the relaxed ride home.";

void setup() {

  size(600, 480);
  noStroke();
  textSize(17.5);
  textLeading(24);
}

void draw() {
  background(20, 30, 55);
  fill(250, 240, 230);
  text(txt, 50, 30, 500, height);

  int now = millis();
  if (now - last > 2000) {
    last = now;
    nextWord();
  }
}

void nextWord() { // replaces a random word in the text

  String[] words = RiTa.tokenize(txt); // split into words

  // loop from a random spot
  int r = floor(random(0, words.length));
  for (int i = r; i < words.length + r; i++) {

    int idx = i % words.length;
    String word = words[idx].toLowerCase();
    if (word.length() < 3) continue; // len >= 3

    // get the first sense of the word
    String pos = RiTa.tagger.allTags(word)[0];

    // find related words
    Map opts = Map.of("pos", pos);
    String[] rhymes = RiTa.rhymes(word, opts);
    String[] sounds = RiTa.soundsLike(word, opts);
    String[] spells = RiTa.spellsLike(word, opts);
    String[] similars = merge(rhymes, sounds, spells);

    // only words with 2 or more similars
    if (similars.length < 2) continue;

    // pick a random similar
    String next = RiTa.random(similars);

    if (next.contains(word) || word.contains(next)) {
      continue;  // skip substrings
    }

    if (Character.isUpperCase(words[idx].charAt(0))) {
      next = RiTa.capitalize(next); // keep capitals
    }

    println("replace("+pos+"): " + word + " -> " + next);
    words[idx] = next;  // do replacement
    break;
  }

  // recombine for display
  txt = RiTa.untokenize(words);
}

String[] merge(String[]... arrays) {
  String[] dest = null;
  int length = 0, destPos = 0;
  for (String[] array : arrays) {
    length += array.length;
  }
  for (String[] array : arrays) {
    if (dest == null) {
      dest = Arrays.copyOf(array, length);
    } else {
      System.arraycopy(array, 0, dest, destPos, array.length);
    }
    destPos += array.length;
  }
  return dest;
}