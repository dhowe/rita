import rita.*;
import java.util.*;

String line = "click to (re)generate";
int x = 160, y = 240;
RiMarkov markov;

void setup()
{
  size(500, 500);

  fill(0);
  textFont(createFont("georgia", 16));

  // create a markov model (n=4) from the files
  markov = RiTa.markov(4);
  markov.addText(String.join("\n", loadStrings("wittgenstein.txt")));
  markov.addText(String.join("\n", loadStrings("kafka.txt")));
}

void draw()
{
  background(250);
  text(line, x, y, 400, 400);
}

void mouseReleased()
{
  x = y = 50;
  // v4: generate(Map) returns String[] (one entry per numSentences); join for display
  line = String.join(" ", markov.generate(Map.of("numSentences", 10)));
}