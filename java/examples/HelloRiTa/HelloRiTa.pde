// HelloRita — minimal RiTa example for Processing
//
// Requires the RiTa library (Sketch > Import Library... > RiTa).

import rita.*;

void setup() {
  size(600, 240);

  // Tokenize and inspect parts of speech
  String[] words = RiTa.tokenize("How now, brown cow?");
  String[] tags = RiTa.pos("How now, brown cow?");

  // Rhyme lookup
  String[] rhymes = RiTa.rhymes("cow", 10);

  // RiScript expansion — run several times for a different result each time
  String line = RiTa.evaluate("i {have|own} a {blue|green|brown} {bird|fish|cow}");

  // Markov chain seeded with a couplet
  RiMarkov m = RiTa.markov(2);
  m.addText("how now brown cow; see you later alligator");
  String generated = m.generate();

  println(words);
  println(tags);
  println(rhymes);
  println(line);
  println(generated);
}

void draw() {
  background(255);
  fill(0);
  text(RiTa.evaluate("the {quick|slow|brown|blue} {fox|cow|bird|fish}"), 20, height / 2);
}
