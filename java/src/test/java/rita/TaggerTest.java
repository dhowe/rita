package rita;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

/**
 * Ported from <code>js/test/tagger-tests.js</code>.
 *
 * <p>Mapping notes:
 * <ul>
 *   <li>{@code expect(x).eql(y)} -> {@code assertArrayEquals} (arrays) / {@code assertEquals} (lists, strings).</li>
 *   <li>{@code expect(!x).true} -> {@code assertFalse(x)}; {@code expect(x).true} -> {@code assertTrue(x)}.</li>
 *   <li>{@code expect(list).to.include(y)} -> {@code assertTrue(list.contains(y))}.</li>
 *   <li>JS blocks disabled with {@code 0 && expect(...)} are omitted (the JS call never executes).</li>
 *   <li>JS bad-input assertions passing numbers/arrays ({@code isAdverb(42)}, {@code isNoun(["rabbit"])})
 *       test JS runtime type coercion; they do not compile in Java and are documented as comments.</li>
 * </ul>
 */
class TaggerTest {

    @Test
    void shouldCallPosArray() {
        assertArrayEquals(new String[0], RiTa.pos(new String[0]));
        assertArrayEquals(new String[]{"nn"}, RiTa.pos(new String[]{"deal"}));
        assertArrayEquals(new String[]{"jj"}, RiTa.pos(new String[]{"freed"}));
        assertArrayEquals(new String[]{"dt"}, RiTa.pos(new String[]{"the"}));
        assertArrayEquals(new String[]{"dt"}, RiTa.pos(new String[]{"a"}));
        assertArrayEquals(new String[]{"dt", "jj", "nn"}, RiTa.pos("the top seed".split(" ")));
        assertArrayEquals(new String[]{"in", "jj", "nn"}, RiTa.pos("by illegal means".split(" ")));
        assertArrayEquals(new String[]{"prp", "vbz", "prp"}, RiTa.pos("He outnumbers us".split(" ")));
        assertArrayEquals(new String[]{"prp", "vbp", "prp"}, RiTa.pos("I outnumber you".split(" ")));
        assertArrayEquals(new String[]{"nns", "vbp"}, RiTa.pos("Elephants dance".split(" ")));
        assertArrayEquals(new String[]{"dt", "nn", "vbz"}, RiTa.pos("the boy dances".split(" ")));
        assertArrayEquals(new String[]{"nnp", "vbz"}, RiTa.pos("Dave dances".split(" ")));
    }

    @Test
    void shouldCallSimplePosArray() {
        assertArrayEquals(new String[0], RiTa.pos(new String[0], Map.of("simple", true)));
        assertArrayEquals(new String[]{"a"}, RiTa.pos(new String[]{"freed"}, Map.of("simple", true)));
        assertArrayEquals(new String[]{"-"}, RiTa.pos(new String[]{"the"}, Map.of("simple", true)));
        assertArrayEquals(new String[]{"-"}, RiTa.pos(new String[]{"a"}, Map.of("simple", true)));
        assertArrayEquals(new String[]{"-", "a", "n"}, RiTa.pos("the top seed".split(" "), Map.of("simple", true)));
        assertArrayEquals(new String[]{"-", "a", "n"}, RiTa.pos("by illegal means".split(" "), Map.of("simple", true)));
        assertArrayEquals(new String[]{"-", "v", "-"}, RiTa.pos("He outnumbers us".split(" "), Map.of("simple", true)));
        assertArrayEquals(new String[]{"-", "v", "-"}, RiTa.pos("I outnumber you".split(" "), Map.of("simple", true)));
        assertArrayEquals(new String[]{"n", "v"}, RiTa.pos("Elephants dance".split(" "), Map.of("simple", true)));
        assertArrayEquals(new String[]{"-", "n", "v"}, RiTa.pos("the boy dances".split(" "), Map.of("simple", true)));
    }

    @Test
    void shouldCallPosInlineArraySimple() {
        String result;
        String answer;
        String txt;

        assertEquals("", RiTa.posInline(new String[0], Map.of("simple", true)));
        assertEquals("asdfaasd/n", RiTa.posInline(new String[]{"asdfaasd"}, Map.of("simple", true)));

        result = RiTa.posInline(new String[]{"clothes"}, Map.of("simple", true));
        answer = "clothes/n";
        assertEquals(answer, result);

        result = RiTa.posInline(new String[]{"teeth"}, Map.of("simple", true));
        answer = "teeth/n";
        assertEquals(answer, result);

        result = RiTa.posInline("There is a cat".split(" "), Map.of("simple", true));
        answer = "There/- is/v a/- cat/n";
        assertEquals(answer, result);

        result = RiTa.posInline(RiTa.tokenize("The boy, dressed in red, ate an apple."), Map.of("simple", true));
        answer = "The/- boy/n , dressed/v in/- red/a , ate/v an/- apple/n .";
        assertEquals(answer, result);

        txt = "The dog ran faster than the other dog. But the other dog was prettier.";
        result = RiTa.posInline(RiTa.tokenize(txt), Map.of("simple", true));
        answer = "The/- dog/n ran/v faster/r than/- the/- other/a dog/n . But/- the/- other/a dog/n was/v prettier/a .";
        assertEquals(answer, result);
    }

    @Test
    void shouldHandleInflectedVerbs() {
        assertArrayEquals(new String[]{"vbz"}, RiTa.pos("disbelieves"));
        assertArrayEquals(new String[]{"v"}, RiTa.pos("disbelieves", Map.of("simple", 1)));

        assertArrayEquals(new String[]{"nns"}, RiTa.pos("fates"));
        assertArrayEquals(new String[]{"n"}, RiTa.pos("fates", Map.of("simple", 1)));

        assertArrayEquals(new String[]{"vbz"}, RiTa.pos("hates"));
        assertArrayEquals(new String[]{"v"}, RiTa.pos("hates", Map.of("simple", 1)));

        assertArrayEquals(new String[]{"vbd"}, RiTa.pos("hated"));
        assertArrayEquals(new String[]{"v"}, RiTa.pos("hated", Map.of("simple", 1)));

        assertArrayEquals(new String[]{"vbg"}, RiTa.pos("hating"));
        assertArrayEquals(new String[]{"v"}, RiTa.pos("hating", Map.of("simple", 1)));

        assertArrayEquals(new String[]{"prp", "vbd", "dt", "nn"}, RiTa.pos("He rode the horse"));
        assertArrayEquals(new String[]{"prp", "vbz", "vbn", "dt", "nn"}, RiTa.pos("He has ridden the horse"));

        assertArrayEquals(new String[]{"prp", "vbd", "dt", "nn"}, RiTa.pos("He rowed the boat"));
        assertArrayEquals(new String[]{"prp", "vbz", "vbn", "dt", "nn"}, RiTa.pos("He has rowed the boat"));
    }

    @Test
    void shouldCallPos() {
        String[] result;
        String[] answer;
        String[] resultArr;
        String[] answerArr;
        String txt;

        assertArrayEquals(new String[0], RiTa.pos(""));
        assertArrayEquals(new String[]{","}, RiTa.pos(","));
        assertArrayEquals(new String[0], RiTa.pos(" "));

        assertArrayEquals(new String[]{"jj"}, RiTa.pos("freed"));
        assertArrayEquals(new String[]{"nn"}, RiTa.pos("biped"));
        assertArrayEquals(new String[]{"nn"}, RiTa.pos("greed"));
        assertArrayEquals(new String[]{"nn"}, RiTa.pos("creed"));
        assertArrayEquals(new String[]{"nn"}, RiTa.pos("weed"));

        // https://github.com/dhowe/rita/issues/177
        assertArrayEquals(new String[]{"vbd"}, RiTa.pos("broke"));
        assertArrayEquals(new String[]{"v"}, RiTa.pos("broke", Map.of("simple", 1)));
        assertArrayEquals(new String[]{"vbn"}, RiTa.pos("committed"));
        assertArrayEquals(new String[]{"v"}, RiTa.pos("committed", Map.of("simple", 1)));
        assertArrayEquals(new String[]{"vbd"}, RiTa.pos("outpaced"));
        assertArrayEquals(new String[]{"v"}, RiTa.pos("outpaced", Map.of("simple", 1)));
        assertArrayEquals(new String[]{"vbd"}, RiTa.pos("concerned"));
        assertArrayEquals(new String[]{"v"}, RiTa.pos("concerned", Map.of("simple", 1)));
        assertArrayEquals(new String[]{"vbn"}, RiTa.pos("committed"));
        assertArrayEquals(new String[]{"v"}, RiTa.pos("committed", Map.of("simple", 1)));

        assertArrayEquals(new String[]{"dt", "jj", "nn"}, RiTa.pos("the top seed"));
        assertArrayEquals(new String[]{"in", "jj", "nn"}, RiTa.pos("by illegal means"));
        assertArrayEquals(new String[]{"nnp", "nnp", "vbd", "rb"}, RiTa.pos("Joannie Smith ran away"));

        result = RiTa.pos("mammal");
        answer = new String[]{"nn"};
        assertArrayEquals(answer, result);

        result = RiTa.pos("asfaasd");
        answer = new String[]{"nn"};
        assertArrayEquals(answer, result);

        result = RiTa.pos("innings");
        answer = new String[]{"nns"};
        assertArrayEquals(answer, result);

        result = RiTa.pos("clothes");
        answer = new String[]{"nns"};
        assertArrayEquals(answer, result);

        result = RiTa.pos("clothes");
        answer = new String[]{"nns"};
        assertArrayEquals(answer, result);

        result = RiTa.pos("teeth");
        answer = new String[]{"nns"};
        assertArrayEquals(answer, result);

        result = RiTa.pos("memories");
        answer = new String[]{"nns"};
        assertArrayEquals(answer, result);

        assertArrayEquals(new String[]{"vbz"}, RiTa.pos("flunks"), "Failed: flunks");
        assertArrayEquals(new String[]{"vbz"}, RiTa.pos("outnumbers"), "Failed: outnumbers");
        assertArrayEquals(new String[]{"prp", "vbz", "prp"}, RiTa.pos("He outnumbers us"));
        assertArrayEquals(new String[]{"prp", "vbp", "prp"}, RiTa.pos("I outnumber you"));

        resultArr = RiTa.pos("Elephants dance");
        answerArr = new String[]{"nns", "vbp"};
        assertArrayEquals(answerArr, resultArr);

        result = RiTa.pos("the boy dances");
        answer = new String[]{"dt", "nn", "vbz"};
        assertArrayEquals(answer, result);

        result = RiTa.pos("he dances");
        answer = new String[]{"prp", "vbz"};
        assertArrayEquals(answer, result);

        resultArr = RiTa.pos("Dave dances");
        answerArr = new String[]{"nnp", "vbz"};
        assertArrayEquals(answerArr, resultArr);

        result = RiTa.pos("running");
        answer = new String[]{"vbg"};
        assertArrayEquals(answer, result);

        result = RiTa.pos("asserting");
        answer = new String[]{"vbg"};
        assertArrayEquals(answer, result);

        result = RiTa.pos("assenting");
        answer = new String[]{"vbg"};
        assertArrayEquals(answer, result);

        result = RiTa.pos("Dave");
        answer = new String[]{"nnp"};
        assertArrayEquals(answer, result);

        result = RiTa.pos("They feed the cat");
        answer = new String[]{"prp", "vbp", "dt", "nn"};
        assertArrayEquals(answer, result);

        result = RiTa.pos("There is a cat.");
        answer = new String[]{"ex", "vbz", "dt", "nn", "."};
        assertArrayEquals(answer, result);

        result = RiTa.pos("The boy, dressed in red, ate an apple.");
        answer = new String[]{"dt", "nn", ",", "vbn", "in", "jj", ",", "vbd", "dt", "nn", "."};
        assertArrayEquals(answer, result);

        txt = "The dog ran faster than the other dog.  But the other dog was prettier.";
        result = RiTa.pos(txt);
        answer = new String[]{"dt", "nn", "vbd", "rbr", "in", "dt", "jj", "nn", ".", "cc", "dt", "jj", "nn", "vbd", "jjr", "."};
        assertArrayEquals(answer, result);

        // Tests for verb conjugation
        assertArrayEquals(new String[]{"vbz"}, RiTa.pos("is"));
        assertArrayEquals(new String[]{"vbp"}, RiTa.pos("am"));
        assertArrayEquals(new String[]{"vb"}, RiTa.pos("be"));

        result = RiTa.pos("There is a cat.");
        answer = new String[]{"ex", "vbz", "dt", "nn", "."};
        assertArrayEquals(answer, result);

        result = RiTa.pos("There was a cat.");
        answer = new String[]{"ex", "vbd", "dt", "nn", "."};
        assertArrayEquals(answer, result);

        result = RiTa.pos("I am a cat.");
        answer = new String[]{"prp", "vbp", "dt", "nn", "."};
        assertArrayEquals(answer, result);

        result = RiTa.pos("I was a cat.");
        answer = new String[]{"prp", "vbd", "dt", "nn", "."};
        assertArrayEquals(answer, result);

        assertArrayEquals(new String[]{"vb"}, RiTa.pos("flunk"));
        assertArrayEquals(new String[]{"prp", "vbz", "dt", "nn"}, RiTa.pos("He flunks the test"));

        assertArrayEquals(new String[]{"prp"}, RiTa.pos("he"));
        assertArrayEquals(new String[]{"vb"}, RiTa.pos("outnumber"));
        assertArrayEquals(new String[]{"prp", "vbd", "prp"}, RiTa.pos("I outnumbered you"), "I outnumbered you");
        assertArrayEquals(new String[]{"prp", "vbd", "prp"}, RiTa.pos("She outnumbered us"), "She outnumbered us");
        assertArrayEquals(new String[]{"prp", "vbp", "vbg", "prp"}, RiTa.pos("I am outnumbering you"), "I am outnumbering you");
        assertArrayEquals(new String[]{"prp", "vbp", "vbd", "prp"}, RiTa.pos("I have outnumbered you"), "I have outnumbered you"); // ?

        String[] checks = {"emphasis", "stress", "discus", "colossus", "fibrosis", "digitalis", "pettiness", "mess", "cleanliness", "orderliness", "bronchitis", "preparedness", "highness"};
        for (String check : checks) {
            assertArrayEquals(new String[]{"nn"}, RiTa.pos(check));
        }

        // sequential adjectives
        assertArrayEquals(new String[]{"dt", "jj", "jj", "nn"}, RiTa.pos("a light blue sky"));

        // vbg will not be wrongly tagged as nn
        assertArrayEquals(new String[]{"prp", "vbz", "vbg", "in", "prp"}, RiTa.pos("He is running toward me"));
        assertArrayEquals(new String[]{"prp", "vbz", "vbg", "dt", "nn"}, RiTa.pos("She is riding a bike"));
        assertArrayEquals(new String[]{"prp", "vbz", "rb", ",", "vbg", "in", "dt", "nns"}, RiTa.pos("he stands still, thinking about the words"));
        assertArrayEquals(new String[]{"prp", "vbd", "in", "in", "dt", "nn", "vbg"}, RiTa.pos("She walked out of the room smoking"));
        assertArrayEquals(new String[]{"prp", "vbd", "vbg", "prp$", "nn", "nn"}, RiTa.pos("He kept saying his adventure story"));
        assertArrayEquals(new String[]{"vbg", "vbz", "prp$", "nn"}, RiTa.pos("Drinking is his hobby"));
        assertArrayEquals(new String[]{"dt", "nn", "vbg", "in", "dt", "nn", "vbz", "dt", "nn"}, RiTa.pos("The kid playing at the corner is the boss"));
        assertArrayEquals(new String[]{"prp", "vbz", "dt", "nn", "in", "dt", "vbg", "nn"}, RiTa.pos("She is the leader of the reading group"));
        assertArrayEquals(new String[]{"prp", "vbp", "vbg"}, RiTa.pos("I love working"));
        assertArrayEquals(new String[]{"prp", "vbd", "vbg", "in", "vbg", "dt", "nn"}, RiTa.pos("I was thinking about buying a car"));

        // #179
        assertArrayEquals(new String[]{"nn"}, RiTa.pos("lancer"));
        assertArrayEquals(new String[]{"nn"}, RiTa.pos("dancer"));
        assertArrayEquals(new String[]{"nn"}, RiTa.pos("builder"));
        assertArrayEquals(new String[]{"nn"}, RiTa.pos("programmer"));
        assertArrayEquals(new String[]{"nn"}, RiTa.pos("mixer"));
        assertArrayEquals(new String[]{"prp", "vbz", "dt", "nn"}, RiTa.pos("He is a dancer"));
        assertArrayEquals(new String[]{"prp", "vbz", "dt", "nn", "nn"}, RiTa.pos("She is a body bulider"));
        assertArrayEquals(new String[]{"prp", "vbp", "dt", "nn"}, RiTa.pos("I am a programmer"));

        // rita#148
        assertArrayEquals(new String[]{"prp", "vbp", "vbn", "rb", "in", "nn"}, RiTa.pos("I have gone alone in there"));
        assertArrayEquals(new String[]{"prp", "vbd", "cc", "vbd", "in", "in", "nn"}, RiTa.pos("We stopped and went on from there"));
        assertArrayEquals(new String[]{"prp", "vbz", "rb"}, RiTa.pos("She lives there"));
        assertArrayEquals(new String[]{"prp", "vbd", "vbg", "rb"}, RiTa.pos("He was standing there"));
        assertArrayEquals(new String[]{"ex", "vbp", "jj", "nns", "to", "vb", "dt", "nn"}, RiTa.pos("There are good reasons to save the world"));
        assertArrayEquals(new String[]{"ex", "vbz", "dt", "nn"}, RiTa.pos("There is a pig"));
        assertArrayEquals(new String[]{"ex", "vbz", "dt", "nn", "in", "vbz", "jj", "vbg"}, RiTa.pos("There isn't a world that is worth saving"));
    }

    @Test
    void shouldCallPosInline() {
        String result;
        String answer;
        String txt;

        assertEquals("", RiTa.posInline(""));
        assertEquals("", RiTa.posInline(" "));
        assertEquals("asdfaasd/nn", RiTa.posInline("asdfaasd"));

        result = RiTa.posInline("clothes");
        answer = "clothes/nns";
        assertEquals(answer, result);

        result = RiTa.posInline("teeth");
        answer = "teeth/nns";
        assertEquals(answer, result);

        result = RiTa.posInline("There is a cat.");
        answer = "There/ex is/vbz a/dt cat/nn .";
        assertEquals(answer, result);

        result = RiTa.posInline("The boy, dressed in red, ate an apple.");
        answer = "The/dt boy/nn , dressed/vbn in/in red/jj , ate/vbd an/dt apple/nn .";
        assertEquals(answer, result);

        txt = "The dog ran faster than the other dog.  But the other dog was prettier.";
        result = RiTa.posInline(txt);
        answer = "The/dt dog/nn ran/vbd faster/rbr than/in the/dt other/jj dog/nn . But/cc the/dt other/jj dog/nn was/vbd prettier/jjr .";
        assertEquals(answer, result);

        // https://github.com/dhowe/rita/issues/177
        // 'bit': as a vbd
        txt = "The mosquito bit me.";
        result = RiTa.posInline(txt);
        answer = "The/dt mosquito/nn bit/vbd me/prp .";
        assertEquals(answer, result);
        // 'bit': as an nn
        txt = "Give the duck a bit of bread.";
        result = RiTa.posInline(txt);
        answer = "Give/vb the/dt duck/nn a/dt bit/nn of/in bread/nn .";
        assertEquals(answer, result);

        txt = "The show has ended.";
        result = RiTa.posInline(txt);
        answer = "The/dt show/nn has/vbz ended/vbn .";
        assertEquals(answer, result);

        // 'remade': as a vbd
        txt = "She remade this video.";
        result = RiTa.posInline(txt);
        answer = "She/prp remade/vbd this/dt video/nn .";
        assertEquals(answer, result);
        // 'remade': as a vbn -- disabled in JS via `0 &&`
        RiTa.posInline("They will be remade into something else.");

        // 'sold': as a vbd -- disabled in JS via `0 &&`
        RiTa.posInline("She sold her apartment.");
        // 'sold': as a vbn
        txt = "Her apartment was sold.";
        result = RiTa.posInline(txt);
        answer = "Her/prp$ apartment/nn was/vbd sold/vbn .";
        assertEquals(answer, result);

        // 'resold': as a vbd
        txt = "She resold her apartment.";
        result = RiTa.posInline(txt);
        answer = "She/prp resold/vbd her/prp$ apartment/nn .";
        assertEquals(answer, result);
        // 'resold': as a vbn -- disabled in JS via `0 &&`
        RiTa.posInline("Her apartment was resold.");

        // 'led': as a vbd
        txt = "He led a team of crows into battle.";
        result = RiTa.posInline(txt);
        answer = "He/prp led/vbd a/dt team/nn of/in crows/nns into/in battle/nn .";
        assertEquals(answer, result);
        // 'led': as a vbn
        txt = "He led a team of crows into battle.";
        result = RiTa.posInline(txt);
        answer = "He/prp led/vbd a/dt team/nn of/in crows/nns into/in battle/nn .";
        assertEquals(answer, result);
    }

    @Test
    void shouldCallPosSimple() {
        assertArrayEquals(new String[]{"n"}, RiTa.pos("biped", Map.of("simple", true)));
        assertArrayEquals(new String[]{"n"}, RiTa.pos("greed", Map.of("simple", true)));
        assertArrayEquals(new String[]{"n"}, RiTa.pos("creed", Map.of("simple", true)));
        assertArrayEquals(new String[]{"n"}, RiTa.pos("weed", Map.of("simple", true)));
        assertArrayEquals(new String[]{"v"}, RiTa.pos("is", Map.of("simple", true)));
        assertArrayEquals(new String[]{"v"}, RiTa.pos("am", Map.of("simple", true)));
        assertArrayEquals(new String[]{"v"}, RiTa.pos("be", Map.of("simple", true)));
        assertArrayEquals(new String[]{"a"}, RiTa.pos("freed", Map.of("simple", true)));
        assertArrayEquals(new String[]{"-", "a", "n"}, RiTa.pos("the top seed", Map.of("simple", true)));
        assertArrayEquals(new String[0], RiTa.pos("", Map.of("simple", true)));
    }

    @Test
    void shouldCallPosInlineSimple() {
        String result;
        String answer;
        String txt;

        assertEquals("", RiTa.posInline("", Map.of("simple", true)));
        assertEquals("asdfaasd/n", RiTa.posInline("asdfaasd", Map.of("simple", true)));

        result = RiTa.posInline("clothes", Map.of("simple", true));
        answer = "clothes/n";
        assertEquals(answer, result);

        result = RiTa.posInline("clothes", Map.of("simple", true));
        answer = "clothes/n";
        assertEquals(answer, result);

        result = RiTa.posInline("teeth", Map.of("simple", true));
        answer = "teeth/n";
        assertEquals(answer, result);

        result = RiTa.posInline("There is a cat.", Map.of("simple", true));
        answer = "There/- is/v a/- cat/n .";
        assertEquals(answer, result);

        result = RiTa.posInline("The boy, dressed in red, ate an apple.", Map.of("simple", true));
        answer = "The/- boy/n , dressed/v in/- red/a , ate/v an/- apple/n .";
        assertEquals(answer, result);

        txt = "The dog ran faster than the other dog.  But the other dog was prettier.";
        result = RiTa.posInline(txt, Map.of("simple", true));
        answer = "The/- dog/n ran/v faster/r than/- the/- other/a dog/n . But/- the/- other/a dog/n was/v prettier/a .";
        assertEquals(answer, result);

        result = RiTa.posInline("teeth", Map.of("simple", true));
        answer = "teeth/n";
        assertEquals(answer, result);

        result = RiTa.posInline("There is a cat.", Map.of("simple", true));
        answer = "There/- is/v a/- cat/n .";
        assertEquals(answer, result);

        result = RiTa.posInline("The boy, dressed in red, ate an apple.", Map.of("simple", true));
        answer = "The/- boy/n , dressed/v in/- red/a , ate/v an/- apple/n .";
        assertEquals(answer, result);

        txt = "The dog ran faster than the other dog.  But the other dog was prettier.";
        result = RiTa.posInline(txt, Map.of("simple", true));
        answer = "The/- dog/n ran/v faster/r than/- the/- other/a dog/n . But/- the/- other/a dog/n was/v prettier/a .";
        assertEquals(answer, result);
    }

    @Test
    void shouldCallIsAdverb() {
        // bad inputs
        assertFalse(RiTa.isAdverb(""));
        assertFalse(RiTa.isAdverb());
        // JS: expect(!RiTa.isAdverb(42)).true — not portable to a typed language.
        // JS: expect(!RiTa.isAdverb(["lively"])).true — ditto.

        assertFalse(RiTa.isAdverb("swim"));
        assertFalse(RiTa.isAdverb("walk"));
        assertFalse(RiTa.isAdverb("walker"));
        assertFalse(RiTa.isAdverb("beautiful"));
        assertFalse(RiTa.isAdverb("dance"));
        assertFalse(RiTa.isAdverb("dancing"));
        assertFalse(RiTa.isAdverb("dancer"));

        // verb
        assertFalse(RiTa.isAdverb("wash"));
        assertFalse(RiTa.isAdverb("walk"));
        assertFalse(RiTa.isAdverb("play"));
        assertFalse(RiTa.isAdverb("throw"));
        assertFalse(RiTa.isAdverb("drink"));
        assertFalse(RiTa.isAdverb("eat"));
        assertFalse(RiTa.isAdverb("chew"));

        // adj
        assertFalse(RiTa.isAdverb("wet"));
        assertFalse(RiTa.isAdverb("dry"));
        assertFalse(RiTa.isAdverb("furry"));
        assertFalse(RiTa.isAdverb("sad"));
        assertFalse(RiTa.isAdverb("happy"));

        // n
        assertFalse(RiTa.isAdverb("dogs"));
        assertFalse(RiTa.isAdverb("wind"));
        assertFalse(RiTa.isAdverb("dolls"));
        assertFalse(RiTa.isAdverb("frogs"));
        assertFalse(RiTa.isAdverb("ducks"));
        assertFalse(RiTa.isAdverb("flowers"));
        assertFalse(RiTa.isAdverb("fish"));

        // adv
        assertTrue(RiTa.isAdverb("truthfully"));
        assertTrue(RiTa.isAdverb("kindly"));
        assertTrue(RiTa.isAdverb("bravely"));
        assertTrue(RiTa.isAdverb("doggedly"));
        assertTrue(RiTa.isAdverb("sleepily"));
        assertTrue(RiTa.isAdverb("scarily"));
        assertTrue(RiTa.isAdverb("excitedly"));
        assertTrue(RiTa.isAdverb("energetically"));
        assertTrue(RiTa.isAdverb("hard")); // +adj
    }

    @Test
    void shouldCallIsNoun() {
        assertTrue(RiTa.isNoun("thieves"), "thieves");
        assertTrue(RiTa.isNoun("calves"));

        assertFalse(RiTa.isNoun("scarily"));
        assertTrue(RiTa.isNoun("boxes"));
        assertTrue(RiTa.isNoun("swim"));
        assertTrue(RiTa.isNoun("walk"));
        assertTrue(RiTa.isNoun("walker"));
        assertTrue(RiTa.isNoun("dance"));
        assertTrue(RiTa.isNoun("dancer"));
        assertTrue(RiTa.isNoun("cats"));
        assertTrue(RiTa.isNoun("teeth"));
        assertTrue(RiTa.isNoun("apples"));
        assertTrue(RiTa.isNoun("buses"));
        assertTrue(RiTa.isNoun("prognoses"));
        assertTrue(RiTa.isNoun("oxen"));
        assertTrue(RiTa.isNoun("theses"));
        assertTrue(RiTa.isNoun("stimuli"));
        assertTrue(RiTa.isNoun("crises"));

        // verb
        assertTrue(RiTa.isNoun("wash"));
        assertTrue(RiTa.isNoun("walk"));
        assertTrue(RiTa.isNoun("play"));
        assertTrue(RiTa.isNoun("throw"));
        assertTrue(RiTa.isNoun("duck"));
        assertTrue(RiTa.isNoun("dog"));
        assertTrue(RiTa.isNoun("drink"));
        assertFalse(RiTa.isNoun("abates"));

        assertFalse(RiTa.isNoun("eat"));
        assertFalse(RiTa.isNoun("chew"));
        assertFalse(RiTa.isNoun("moved"));
        assertFalse(RiTa.isNoun("went"));
        assertFalse(RiTa.isNoun("spent"));

        // adj
        assertFalse(RiTa.isNoun("hard"));
        assertFalse(RiTa.isNoun("dry"));
        assertFalse(RiTa.isNoun("furry"));
        assertFalse(RiTa.isNoun("sad"));
        assertFalse(RiTa.isNoun("happy"));
        assertFalse(RiTa.isNoun("beautiful"));

        // n
        assertTrue(RiTa.isNoun("dogs"));
        assertTrue(RiTa.isNoun("wind"));
        assertTrue(RiTa.isNoun("dolls"));
        assertTrue(RiTa.isNoun("frogs"));
        assertTrue(RiTa.isNoun("ducks"));
        assertTrue(RiTa.isNoun("flower"));
        assertTrue(RiTa.isNoun("fish"));
        assertTrue(RiTa.isNoun("wet")); // +v/adj
        assertTrue(RiTa.isNoun("ducks")); // +v
        assertTrue(RiTa.isNoun("flowers")); // +v

        // adv
        assertFalse(RiTa.isNoun("truthfully"));
        assertFalse(RiTa.isNoun("kindly"));
        assertFalse(RiTa.isNoun("bravely"));
        assertFalse(RiTa.isNoun("scarily"));
        assertFalse(RiTa.isNoun("sleepily"));
        assertFalse(RiTa.isNoun("excitedly"));
        assertFalse(RiTa.isNoun("energetically"));

        // bad input
        assertFalse(RiTa.isNoun(""));
        assertFalse(RiTa.isNoun());
        // JS: expect(!RiTa.isNoun(42)).true — not portable.
        // JS: expect(!RiTa.isNoun(["rabbit"])).true — ditto.

        // verbs (esp. past particle)
        assertFalse(RiTa.isNoun("heard"), "heard: " + RiTa.tagger.allTags("heard"));
        assertFalse(RiTa.isNoun("deterred"));
    }

    @Test
    void shouldCallIsVerb() {
        assertEquals(true, RiTa.isVerb("abandons"));

        // verbs
        assertTrue(RiTa.isVerb("dance"));
        assertTrue(RiTa.isVerb("swim"));
        assertTrue(RiTa.isVerb("walk"));

        assertTrue(RiTa.isVerb("dances"));
        assertTrue(RiTa.isVerb("swims"));
        assertTrue(RiTa.isVerb("walks"));
        assertTrue(RiTa.isVerb("costs"));

        // inflections
        assertTrue(RiTa.isVerb("danced"));
        assertTrue(RiTa.isVerb("swam"));
        assertTrue(RiTa.isVerb("walked"));
        assertTrue(RiTa.isVerb("costed"));
        assertTrue(RiTa.isVerb("satisfies"));
        assertTrue(RiTa.isVerb("falsifies"));
        assertTrue(RiTa.isVerb("beautifies"));
        assertTrue(RiTa.isVerb("repossesses"));

        assertFalse(RiTa.isVerb("dancer"));
        assertFalse(RiTa.isVerb("walker"));
        assertFalse(RiTa.isVerb("beautiful"));

        assertTrue(RiTa.isVerb("eat"), "eat");
        assertTrue(RiTa.isVerb("chew"));

        assertTrue(RiTa.isVerb("throw")); // +n
        assertTrue(RiTa.isVerb("walk")); // +n
        assertTrue(RiTa.isVerb("wash")); // +n
        assertTrue(RiTa.isVerb("drink")); // +n

        assertTrue(RiTa.isVerb("fish")); // +n

        assertTrue(RiTa.isVerb("wind")); // +n
        assertTrue(RiTa.isVerb("wet")); // +adj
        assertTrue(RiTa.isVerb("dry")); // +adj

        // adj
        assertFalse(RiTa.isVerb("hard"));
        assertFalse(RiTa.isVerb("furry"));
        assertFalse(RiTa.isVerb("sad"));
        assertFalse(RiTa.isVerb("happy"));

        // n
        assertFalse(RiTa.isVerb("dolls"));
        assertFalse(RiTa.isVerb("frogs"));
        assertTrue(RiTa.isVerb("flowers"));
        assertTrue(RiTa.isVerb("ducks"));

        // adv
        assertFalse(RiTa.isVerb("truthfully"));
        assertFalse(RiTa.isVerb("kindly"));
        assertFalse(RiTa.isVerb("bravely"));
        assertFalse(RiTa.isVerb("scarily"));
        assertFalse(RiTa.isVerb("sleepily"));
        assertFalse(RiTa.isVerb("excitedly"));
        assertFalse(RiTa.isVerb("energetically"));

        // inflections
        assertTrue(RiTa.isVerb("hates"));
        assertTrue(RiTa.isVerb("hated"));
        assertTrue(RiTa.isVerb("hating"));
        assertTrue(RiTa.isVerb("dancing"));
        assertTrue(RiTa.isVerb("flowers"));

        // irregular inflections (SYNC:)
        assertTrue(RiTa.isVerb("hates"));
        assertTrue(RiTa.isVerb("hated"));
        assertTrue(RiTa.isVerb("ridden"));
        assertTrue(RiTa.isVerb("rode"));

        assertTrue(RiTa.isVerb("abetted"));
        assertTrue(RiTa.isVerb("abetting"));
        assertTrue(RiTa.isVerb("abutted"));
        assertTrue(RiTa.isVerb("abutting"));
        assertTrue(RiTa.isVerb("abuts"));
        assertTrue(RiTa.isVerb("abut"));

        assertTrue(RiTa.isVerb("misdeal"));
        assertTrue(RiTa.isVerb("misdeals"));
        assertTrue(RiTa.isVerb("misdealt"));

        // bad inputs
        assertFalse(RiTa.isVerb(""));
        assertFalse(RiTa.isVerb());
        // JS: expect(!RiTa.isVerb(42)).true — not portable.
        // JS: expect(!RiTa.isVerb(["work"])).true — ditto.
    }

    @Test
    void shouldCallIsAdjective() {
        assertFalse(RiTa.isAdjective("swim"));
        assertFalse(RiTa.isAdjective("walk"));
        assertFalse(RiTa.isAdjective("walker"));
        assertTrue(RiTa.isAdjective("beautiful"));
        assertFalse(RiTa.isAdjective("dance"));
        assertFalse(RiTa.isAdjective("dancing"));
        assertFalse(RiTa.isAdjective("dancer"));

        // verb
        assertFalse(RiTa.isAdjective("wash"));
        assertFalse(RiTa.isAdjective("walk"));
        assertFalse(RiTa.isAdjective("play"));
        assertFalse(RiTa.isAdjective("throw"));
        assertFalse(RiTa.isAdjective("drink"));
        assertFalse(RiTa.isAdjective("eat"));
        assertFalse(RiTa.isAdjective("chew"));

        // adj
        assertTrue(RiTa.isAdjective("hard"));
        assertTrue(RiTa.isAdjective("wet"));
        assertTrue(RiTa.isAdjective("dry"));
        assertTrue(RiTa.isAdjective("furry"));
        assertTrue(RiTa.isAdjective("sad"));
        assertTrue(RiTa.isAdjective("happy"));
        assertTrue(RiTa.isAdjective("kindly")); // +adv

        // n
        assertFalse(RiTa.isAdjective("dogs"));
        assertFalse(RiTa.isAdjective("wind"));
        assertFalse(RiTa.isAdjective("dolls"));
        assertFalse(RiTa.isAdjective("frogs"));
        assertFalse(RiTa.isAdjective("ducks"));
        assertFalse(RiTa.isAdjective("flowers"));
        assertFalse(RiTa.isAdjective("fish"));

        // adv
        assertFalse(RiTa.isAdjective("truthfully"));
        assertFalse(RiTa.isAdjective("bravely"));
        assertFalse(RiTa.isAdjective("scarily"));
        assertFalse(RiTa.isAdjective("sleepily"));
        assertFalse(RiTa.isAdjective("excitedly"));
        assertFalse(RiTa.isAdjective("energetically"));

        // bad inputs
        assertFalse(RiTa.isAdjective(""));
        assertFalse(RiTa.isAdjective());
        // JS: expect(!RiTa.isAdjective(42)).true — not portable.
        // JS: expect(!RiTa.isAdjective(["happy"])).true — ditto.
    }

    @Test
    void shouldCallAllTags() {
        assertEquals(List.of("nn"), RiTa.tagger.allTags("monkey"));
        assertEquals(List.of("nns"), RiTa.tagger.allTags("monkeys"));
        assertEquals(List.of(), RiTa.tagger.allTags(""));
        assertEquals(List.of(), RiTa.tagger.allTags(new String[]{"monkey"}));
        assertEquals(List.of(), RiTa.tagger.allTags("hates", Map.of("noDerivations", true)));
        assertEquals(List.of("vbz"), RiTa.tagger.allTags("satisfies"));
        assertEquals(List.of("vbz"), RiTa.tagger.allTags("falsifies"));
        assertTrue(RiTa.tagger.allTags("hates").contains("vbz"));
        assertTrue(RiTa.tagger.allTags("hates").contains("nns"));
        assertTrue(RiTa.tagger.allTags("cakes").contains("nns"));
        assertTrue(RiTa.tagger.allTags("repossesses").contains("vbz"));
        assertTrue(RiTa.tagger.allTags("thieves").contains("nns"));
        assertTrue(RiTa.tagger.allTags("thieves").contains("vbz"));
        assertTrue(RiTa.tagger.allTags("hated").contains("vbd"));
        assertTrue(RiTa.tagger.allTags("hated").contains("vbn"));
        assertTrue(RiTa.tagger.allTags("owed").contains("vbd"));
        assertTrue(RiTa.tagger.allTags("owed").contains("vbn"));
        assertTrue(RiTa.tagger.allTags("assenting").contains("vbg"));
        assertTrue(RiTa.tagger.allTags("hating").contains("vbg"));
        assertTrue(RiTa.tagger.allTags("feet").contains("nns"));
        assertTrue(RiTa.tagger.allTags("men").contains("nns"));
        // given up
        assertTrue(RiTa.tagger.allTags("ashdj").contains("nn"));
        assertTrue(RiTa.tagger.allTags("kahsdly").contains("rb"));
        assertTrue(RiTa.tagger.allTags("asdkasws").contains("nns"));

        // https://github.com/dhowe/rita/issues/177
        assertEquals(List.of("vbd", "nn", "rb"), RiTa.tagger.allTags("bit"));
        assertEquals(List.of("vbd", "jj", "rb"), RiTa.tagger.allTags("broke"));
        assertEquals(List.of("vbd", "vbn"), RiTa.tagger.allTags("called"));
        assertEquals(List.of("vbn", "jj", "vbd"), RiTa.tagger.allTags("committed"));
        assertEquals(List.of("jj", "vbd", "vbn"), RiTa.tagger.allTags("computerized"));
        assertEquals(List.of("vbd", "jj", "vbn"), RiTa.tagger.allTags("concerned"));
        assertEquals(List.of("vbd", "vbn", "jj"), RiTa.tagger.allTags("discriminated"));
        assertEquals(List.of("vbd", "jj", "vbn"), RiTa.tagger.allTags("ended"));
        assertEquals(List.of("vbn", "vbd", "jj"), RiTa.tagger.allTags("expected"));
        assertEquals(List.of("vbd", "jj", "vbn"), RiTa.tagger.allTags("finished"));
        assertEquals(List.of("vbd", "vbn"), RiTa.tagger.allTags("gained"));

        assertEquals(List.of("vbd", "vbn"), RiTa.tagger.allTags("got"));
        assertEquals(List.of("vbn", "jj", "vbd"), RiTa.tagger.allTags("increased"));
        assertEquals(List.of("vbn", "vbd", "jj"), RiTa.tagger.allTags("involved"));
        assertEquals(List.of("vbn", "vbd"), RiTa.tagger.allTags("launched"));
        assertEquals(List.of("vbd", "vbn"), RiTa.tagger.allTags("led"));
        assertEquals(List.of("vbd", "vbn"), RiTa.tagger.allTags("lived"));
        assertEquals(List.of("vbd"), RiTa.tagger.allTags("oversaw"));
        assertEquals(List.of("vbd", "vbn"), RiTa.tagger.allTags("paled"));
        assertEquals(List.of("jj", "vbd", "vbn"), RiTa.tagger.allTags("prepaid"));
        assertEquals(List.of("vbn", "jj", "vbd"), RiTa.tagger.allTags("pressured"));
        assertEquals(List.of("vbn", "vbd"), RiTa.tagger.allTags("proliferated"));
        assertEquals(List.of("vbd", "vbn"), RiTa.tagger.allTags("remade"));
        assertEquals(List.of("vbd", "vbn"), RiTa.tagger.allTags("reopened"));
        assertEquals(List.of("vbd", "jj", "vbn"), RiTa.tagger.allTags("reported"));
        assertEquals(List.of("vbd", "vbn"), RiTa.tagger.allTags("resold"));
        assertEquals(List.of("vbd", "vbn", "jj"), RiTa.tagger.allTags("settled"));
        assertEquals(List.of("vbd", "jj", "vbn"), RiTa.tagger.allTags("started"));
    }

    @Test
    void shouldCallHasTag() {
        assertFalse(RiTa.tagger.hasTag());
        assertFalse(RiTa.tagger.hasTag("nn adj", "nn"));
        assertTrue(RiTa.tagger.hasTag(RiTa.tagger.allTags("monkey"), "nn"));
    }

    @Test
    void shouldCallInlineTags() {
        assertEquals("", RiTa.tagger.inlineTags());
        assertEquals("", RiTa.tagger.inlineTags(new String[0]));
        assertThrows(Exception.class, () -> RiTa.tagger.inlineTags(new String[]{"I", "am", "Pikachu"}, new String[0], "/"));
        assertEquals("I/prp am/vbp happy/jj .",
            RiTa.tagger.inlineTags(new String[]{"I", "am", "happy", "."}, new String[]{"prp", "vbp", "jj", "."}));
        assertEquals("I;prp am;vbp happy;jj .",
            RiTa.tagger.inlineTags(new String[]{"I", "am", "happy", "."}, new String[]{"prp", "vbp", "jj", "."}, ";"));
    }

    @Test
    void shouldCallTag() {
        assertArrayEquals(new String[0], RiTa.tagger.tag(new String[0]));
        assertArrayEquals(new String[0], RiTa.tagger.tag());
        assertEquals("", RiTa.tagger.tag(new String[0], Map.of("inline", true)));
        assertArrayEquals(new String[]{"-", "v", "a", "-"},
            (String[]) RiTa.tagger.tag(new String[]{"I", "am", "happy", "."}, Map.of("simple", true)));
        assertEquals("I/- am/v happy/a .",
            RiTa.tagger.tag(new String[]{"I", "am", "happy", "."}, Map.of("simple", true, "inline", true)));
        assertEquals("I/prp roll/vbp a/dt 9/cd .",
            RiTa.tagger.tag(new String[]{"I", "roll", "a", "9", "."}, Map.of("inline", true)));
        assertEquals("A/dt badguy/nn .",
            RiTa.tagger.tag(new String[]{"A", "badguy", "."}, Map.of("inline", true)));
        assertEquals("A/dt C/C level/jj grade/nn .",
            RiTa.tagger.tag(new String[]{"A", "C", "level", "grade", "."}, Map.of("inline", true)));
        // rule 1
        assertEquals("The/dt run/nn was/vbd great/jj .",
            RiTa.tagger.tag(new String[]{"The", "run", "was", "great", "."}, Map.of("inline", true)));
        assertEquals("They/prp are/vbp the/dt beaten/nn .",
            RiTa.tagger.tag(new String[]{"They", "are", "the", "beaten", "."}, Map.of("inline", true)));
        assertEquals("A/dt diss/nns .",
            RiTa.tagger.tag(new String[]{"A", "diss", "."}, Map.of("inline", true)));
        assertEquals("The/dt soon/jj .",
            RiTa.tagger.tag(new String[]{"The", "soon", "."}, Map.of("inline", true)));
        assertEquals("The/dt sooner/jjr .",
            RiTa.tagger.tag(new String[]{"The", "sooner", "."}, Map.of("inline", true)));
        assertEquals("The/dt soonest/jjs .",
            RiTa.tagger.tag(new String[]{"The", "soonest", "."}, Map.of("inline", true)));
        // rule 2
        assertEquals("It/prp is/vbz 59876/cd .",
            RiTa.tagger.tag(new String[]{"It", "is", "59876", "."}, Map.of("inline", true)));
        // rule 3
        assertEquals("I/prp teabaged/vbn .",
            RiTa.tagger.tag(new String[]{"I", "teabaged", "."}, Map.of("inline", true)));
        assertEquals("Sun/nn teabaged/vbn .",
            RiTa.tagger.tag(new String[]{"Sun", "teabaged", "."}, Map.of("inline", true)));
        assertEquals("The/dt worker/nn proletarianized/vbn .",
            RiTa.tagger.tag(new String[]{"The", "worker", "proletarianized", "."}, Map.of("inline", true)));
        // rule 4
        assertEquals("The/dt fortunately/rb .", // 1-b then 4
            RiTa.tagger.tag(new String[]{"The", "fortunately", "."}, Map.of("inline", true)));
        assertEquals("He/prp is/vbz goodly/rb working/vbg .",
            RiTa.tagger.tag(new String[]{"He", "is", "goodly", "working", "."}, Map.of("inline", true)));
        // rule 5
        assertEquals("It/prp is/vbz nonexistional/jj .",
            RiTa.tagger.tag(new String[]{"It", "is", "nonexistional", "."}, Map.of("inline", true)));
        assertEquals("It/prp is/vbz mammal/nn .",
            RiTa.tagger.tag(new String[]{"It", "is", "mammal", "."}, Map.of("inline", true)));
        assertEquals("It/prp is/vbz onal/nn .",
            RiTa.tagger.tag(new String[]{"It", "is", "onal", "."}, Map.of("inline", true)));
        // rule 6
        assertEquals("We/prp must/md place/vb it/prp .",
            RiTa.tagger.tag(new String[]{"We", "must", "place", "it", "."}, Map.of("inline", true)));
        assertEquals("We/prp must/md teabag/vb him/prp .",
            RiTa.tagger.tag(new String[]{"We", "must", "teabag", "him", "."}, Map.of("inline", true)));
        // rule 7
        assertEquals("He/prp has/vbz played/vbn it/prp .",
            RiTa.tagger.tag(new String[]{"He", "has", "played", "it", "."}, Map.of("inline", true)));
        assertEquals("He/prp gets/vbz played/vbn .",
            RiTa.tagger.tag(new String[]{"He", "gets", "played", "."}, Map.of("inline", true)));
        // rule 8
        assertEquals("The/dt morning/nn .",
            RiTa.tagger.tag(new String[]{"The", "morning", "."}, Map.of("inline", true)));
        assertEquals("They/prp are/vbp fishing/vbg .",
            RiTa.tagger.tag(new String[]{"They", "are", "fishing", "."}, Map.of("inline", true)));
        // rule 9
        assertEquals("He/prp dances/vbz .",
            RiTa.tagger.tag(new String[]{"He", "dances", "."}, Map.of("inline", true)));
        assertEquals("The/dt dog/nn dances/vbz .",
            RiTa.tagger.tag(new String[]{"The", "dog", "dances", "."}, Map.of("inline", true)));
        assertEquals("Dave/nnp dances/vbz .",
            RiTa.tagger.tag(new String[]{"Dave", "dances", "."}, Map.of("inline", true)));
        // rule 10
        assertEquals("Taipei/nnp .",
            RiTa.tagger.tag(new String[]{"Taipei", "."}, Map.of("inline", true)));
        assertEquals("Buddhas/nnps .",
            RiTa.tagger.tag(new String[]{"Buddhas", "."}, Map.of("inline", true)));
        assertEquals("In/in Beijing/nnp .",
            RiTa.tagger.tag(new String[]{"In", "Beijing", "."}, Map.of("inline", true)));
        assertEquals("One/cd of/in the/dt Beats/nnps .",
            RiTa.tagger.tag(new String[]{"One", "of", "the", "Beats", "."}, Map.of("inline", true)));
        assertEquals("Taipei/nnp is/vbz a/dt big/jj city/nn .",
            RiTa.tagger.tag(new String[]{"Taipei", "is", "a", "big", "city", "."}, Map.of("inline", true)));
        assertEquals("Buddhas/nnps in/in this/dt temple/nn have/vbp a/dt history/nn of/in 500/cd years/nns .",
            RiTa.tagger.tag(new String[]{"Buddhas", "in", "this", "temple", "have", "a", "history", "of", "500", "years", "."}, Map.of("inline", true)));
        assertEquals("Balls/nns on/in the/dt floor/nn .",
            RiTa.tagger.tag(new String[]{"Balls", "on", "the", "floor", "."}, Map.of("inline", true)));
        // rule 11
        assertEquals("dances/nns .",
            RiTa.tagger.tag(new String[]{"dances", "."}, Map.of("inline", true)));
        assertEquals("dances/nns and/cc performances/nns .",
            RiTa.tagger.tag(new String[]{"dances", "and", "performances", "."}, Map.of("inline", true)));
        assertEquals("cakes/nns quickly/rb .",
            RiTa.tagger.tag(new String[]{"cakes", "quickly", "."}, Map.of("inline", true)));
        assertEquals("dances/vbz quickly/rb .",
            RiTa.tagger.tag(new String[]{"dances", "quickly", "."}, Map.of("inline", true)));
        // rule 12
        assertEquals("David/nnp cakes/nns .",
            RiTa.tagger.tag(new String[]{"David", "cakes", "."}, Map.of("inline", true)));
        assertEquals("David/nnp laughs/vbz and/cc dances/vbz .",
            RiTa.tagger.tag(new String[]{"David", "laughs", "and", "dances", "."}, Map.of("inline", true)));
        assertEquals("counterattacks/nns .",
            RiTa.tagger.tag(new String[]{"counterattacks", "."}, Map.of("inline", true)));
        // rule 13
        assertEquals("Monkeys/nns run/vbp .",
            RiTa.tagger.tag(new String[]{"Monkeys", "run", "."}, Map.of("inline", true)));
        assertEquals("Monkeys/nns attack/vbp .",
            RiTa.tagger.tag(new String[]{"Monkeys", "attack", "."}, Map.of("inline", true)));
        //
        assertEquals("A/dt light/jj blue/jj sky/nn .",
            RiTa.tagger.tag(new String[]{"A", "light", "blue", "sky", "."}, Map.of("inline", true)));

        // https://github.com/dhowe/rita/issues/177
        assertEquals("It/prp broke/vbd .",
            RiTa.tagger.tag(new String[]{"It", "broke", "."}, Map.of("inline", true)));
        assertEquals("It/prp outpaced/vbd that/in .",
            RiTa.tagger.tag(new String[]{"It", "outpaced", "that", "."}, Map.of("inline", true)));
        assertEquals("She/prp remade/vbd this/dt video/nn .",
            RiTa.tagger.tag(new String[]{"She", "remade", "this", "video", "."}, Map.of("inline", true)));
        assertEquals("She/prp has/vbz remade/vbn this/dt video/nn .",
            RiTa.tagger.tag(new String[]{"She", "has", "remade", "this", "video", "."}, Map.of("inline", true)));
        // two further tag() checks are disabled in JS via `0 &&`
    }

    @Test
    void shouldHandleHyphenatedWords() {
        String[] pool = {
            "He is my father-in-law.",
            "We have a off-site meeting yesterday.",
            "I know a great place for an off-site.",
            "a state-of-the-art computer",
            "The girls wanted the merry-go-round to go faster.",
            "He ate twenty-one burgers today.",
            "The politician arrived by high-speed railway.",
            "People doing yoga benefit from an increased feeling of well-being.",
            "There is a life-size statue of the dragon in the park.",
            "He has a king-size bed in his room.",
            "I am taking a full-time job now",
            "The cost for the round-trip ticket is 2000 dollars.",
            "The cost is 2000 dollars for the round-trip.",
            "He come back empty-handed",
            "She is left-handed",
            "I like the dress of the long-haired girl in the photo.",
            "His move was breath-taking.",
            "Snakes are cold-blooded.",
            "People liked to wear bell-bottoms in the 80s.",
            "This shop mainly sells corn-fed meat.",
            "I withdraw the application and re-apply for another position.",
            "Our co-manager believe in neo-liberalism.",
            "He did a u-turn.",
            "We are not going to get down to the nitty-gritty analysis of value for money.",
            "The game require co-op with your teammates.",
            "He was a roly-poly little man."
        };

        String[][] answers = {
            {"prp", "vbz", "prp$", "nn", "."},
            {"prp", "vbp", "dt", "jj", "vbg", "nn", "."},
            {"prp", "vbp", "dt", "jj", "nn", "in", "dt", "nn", "."},
            {"dt", "jj", "nn"},
            {"dt", "nns", "vbd", "dt", "nn", "to", "vb", "rbr", "."},
            {"prp", "vbd", "cd", "nns", "nn", "."},
            {"dt", "nn", "vbd", "in", "jj", "nn", "."},
            {"nn", "vbg", "nn", "nn", "in", "dt", "jj", "vbg", "in", "nn", "."},
            {"ex", "vbz", "dt", "jj", "nn", "in", "dt", "nn", "in", "dt", "nn", "."},
            {"prp", "vbz", "dt", "jj", "nn", "in", "prp$", "nn", "."},
            {"prp", "vbp", "vbg", "dt", "jj", "nn", "rb"},
            {"dt", "nn", "in", "dt", "jj", "nn", "vbz", "cd", "nns", "."},
            {"dt", "nn", "vbz", "cd", "nns", "in", "dt", "nn", "."},
            {"prp", "vbp", "rb", "jj"},
            {"prp", "vbz", "jj"},
            {"prp", "vbp", "dt", "nn", "in", "dt", "jj", "nn", "in", "dt", "nn", "."},
            {"prp$", "nn", "vbd", "jj", "."},
            {"nns", "vbp", "jj", "."},
            {"nn", "vbd", "to", "vb", "nn", "in", "dt", "nns", "."},
            {"dt", "nn", "rb", "nns", "jj", "nn", "."},
            {"prp", "vbp", "dt", "nn", "cc", "vb", "in", "dt", "nn", "."},
            {"prp$", "nn", "vbp", "in", "nn", "."},
            {"prp", "vbd", "dt", "nn", "."},
            {"prp", "vbp", "rb", "vbg", "to", "vb", "rb", "to", "dt", "nn", "nn", "in", "nn", "in", "nn", "."},
            {"dt", "nn", "vb", "nn", "in", "prp$", "nns", "."},
            {"prp", "vbd", "dt", "jj", "jj", "nn", "."}
        };

        for (int i = 0; i < answers.length; i++) {
            assertArrayEquals(answers[i], RiTa.pos(pool[i]), "fail at: " + pool[i]);
        }
    }
}
