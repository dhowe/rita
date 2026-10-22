import rita.*;

HashMap args;
float buttonX = 150;
String[] kwic, buttons = {
  "Gregor", "Samsa", "family", "being", 
  "clerk", "room", "violin", "window"
};
String txt, over, word = buttons[7];

void setup() {
  size(800, 500);

  textFont(createFont("times", 16));

  args = new HashMap();
  args.put("ignorePunctuation", true);
  args.put("ignoreStopWords", true);
  args.put("numWords", 6);

  String[] strs = loadStrings("kafka.txt");
  RiTa.concordance(String.join("\n", strs), args);
}

void draw() {

  kwic = RiTa.kwic(word, 6);

  background(255);
  drawButtons();

  float tw = textWidth(word) / 2f;
  int num = min(10, kwic.length); // keep the display within the canvas

  for (int i = 0; i < num; i++) {

    // split on the literal keyword (not a regex) and strip stray line-breaks
    String[] parts = kwic[i].split(java.util.regex.Pattern.quote(word));
    String before = parts.length > 0 ? parts[0].replace("\n", " ") : "";
    String after = parts.length > 1 ? parts[1].replace("\n", " ") : "";
    float x = width / 2f, y = i * 24 + 90;

    if (y > height - 20) return;

    fill(0);
    textAlign(RIGHT);
    text(before, x - tw, y);

    fill(200, 0, 0);
    textAlign(CENTER);
    text(word, x, y);

    fill(0);
    textAlign(LEFT);
    text(after, x + tw, y);
  }
}

void drawButtons() {

  float posX = buttonX;
  for (int i = 0; i < buttons.length; i++) {
    stroke(200);
    boolean on = word.equals(buttons[i]);
    float tw = textWidth(buttons[i]);
    fill(!on && buttons[i].equals(over) ? 235 : 255);
    rect(posX-5, 44, tw+10, -20, 7);
    fill((on ? 255 : 0), 0, 0);
    text(buttons[i], posX, 40);
    posX += tw + 20;
  }
}

void mouseReleased() {

  float posX = buttonX, tw;
  for (int i = 0; i < buttons.length; i++) {
    tw = textWidth(buttons[i]);
    if (inside(mouseX, mouseY, posX, tw)) {
      word = buttons[i];
      kwic = null;
      break;
    }
    posX += tw + 20;
  }
}

void mouseMoved() {
  over = null;
  float posX = buttonX, tw;
  for (int i = 0; i < buttons.length; i++) {
    tw = textWidth(buttons[i]);
    if (inside(mouseX, mouseY, posX, tw)) {
      over = buttons[i];
      break;
    }
    posX += tw + 20;
  }
}

boolean inside(float mx, float my, float posX, float tw) {
  return (mx >= posX-5 && mx <= posX + tw+5 
    && my >= 25 && my <= 44);
}
