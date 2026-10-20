StringDict tagDict;

String tagName(String tag) {
  if (tagDict == null) {
    tagDict = new StringDict();
    tagDict.set("n", "Noun");
    tagDict.set("v", "Verb");
    tagDict.set("r", "Adverb");
    tagDict.set("a", "Adjective");
  }
  return tag == null ? null : tagDict.get(tag);
}

void addSyllables(String sylls, Bubble[] bubbles) {
  String[] syllables = sylls.split("/");
  for (int i = 0, past = 0; i < syllables.length; i++) {
    String[] phs = syllables[i].split("-");
    for (int j = 1; j < phs.length; j++) {
      bubbles[past+j].adjustDistance(-20 * j);
    }
    past += phs.length;
  }
}

void addStresses(String stresses, String syllables, Bubble[] bubbles) {
  String[] stress = stresses.split("/");
  String[] syllable = syllables.split("/");
  for (int i = 0, past = 0; i < stress.length; i++) {
    String[] phs = syllable[i].split("-");

    // if the syllable is stressed, grow its bubbles
    if (Integer.parseInt(stress[i]) == 1) {
      for (int j = 0; j < phs.length; j++) {
        bubbles[past+j].grow();
      }
    }

    past += phs.length;
  }
}

color phonemeColor(String phoneme) {
  int idx = java.util.Arrays.asList(RiTa.PHONES).indexOf(phoneme);
  return idx > -1 ? colors[idx] : 0;
}

color[] colorGradient() {
  colorMode(HSB, 1, 1, 1, 1);
  color[] tmp = new color[RiTa.PHONES.length];
  for (int i = 0; i < tmp.length; i++) {
    float h = map(i, 0, tmp.length, .2, .8);
    tmp[i] = color(h, .9, .9, .6);
  }
  colorMode(RGB, 255, 255, 255, 255);
  return tmp;
}
