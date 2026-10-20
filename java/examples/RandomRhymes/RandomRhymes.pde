import rita.*;

String syns="", word = "";
int last = -9999;

void setup()
{
  size(300, 300);
  fill(255);
  textFont(createFont("Georgia", 36));
}

void draw()
{
  background(100, 0, 100);

  textAlign(RIGHT);
  textSize(36);
  text(word, 280, 40);

  textSize(14);
  textLeading(17);
  textAlign(LEFT);
  text(syns, 30, 73);
  
  int now = millis();
  if (now - last > 2000) {
    last = now;
    nextWord();
  }
}

void nextWord() { // every 2 sec

  String[] tmp = {};
  while (tmp.length < 3) {

    word = RiTa.randomWord();
    tmp = RiTa.rhymes(word);
  }

  text(word, 280, 40); // max of 13 words
  syns = String.join("\n", subset(tmp, 0, min(tmp.length, 13)));
}
