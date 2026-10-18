package rita;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.LinkedHashMap;
import java.util.Map;
import org.junit.jupiter.api.Test;

/**
 * Ported from <code>js/test/conjugator-tests.js</code>.
 *
 * <p>Mapping notes:
 * <ul>
 *   <li>{@code expect(x).eq(y)} -> {@code assertEquals}; {@code .to.throw()} (with parens) ->
 *       {@code assertThrows}.</li>
 *   <li>JS {@code .to.throw} <em>without</em> parens is a no-op property access (chai asserts
 *       nothing); those calls are kept for fidelity but carry no assertion.</li>
 *   <li>JS option objects -> {@code Map.of(...)}; JS truthy values kept verbatim (e.g.
 *       {@code person: RiTa.THIRD}).</li>
 *   <li>The {@code NOLEX} branch of the unconjugate test is dead in the JS suite (the symbol is
 *       undefined when a lexicon is present) and is omitted.</li>
 * </ul>
 */
class ConjugatorTest {

    private static final boolean HAS_LEX = true;

    @Test
    void shouldCallPastPart() {
        assertEquals("penned", RiTa.pastPart("pen")); // rita #150
        assertEquals("red", RiTa.pastPart("red"));

        assertEquals("slept", RiTa.pastPart("sleep"));
        assertEquals("withheld", RiTa.pastPart("withhold"));

        assertEquals("cut", RiTa.pastPart("cut"));
        assertEquals("gone", RiTa.pastPart("go"));
        assertEquals("swum", RiTa.pastPart("swim"));
        assertEquals("would", RiTa.pastPart("would"));
        assertEquals("might", RiTa.pastPart("might"));
        assertEquals("run", RiTa.pastPart("run"));
        assertEquals("spoken", RiTa.pastPart("speak"));
        assertEquals("broken", RiTa.pastPart("break"));
        assertEquals("pled", RiTa.pastPart("plead"));
        assertEquals("", RiTa.pastPart(""));

        // or shined
        assertEquals("shrunk", RiTa.pastPart("shrink"));

        // or shrunken
        assertEquals("stunk", RiTa.pastPart("stink"));
        assertEquals("studied", RiTa.pastPart("study"));

        // words with wrong 'vb' tag — https://github.com/dhowe/rita/issues/177
        assertEquals("bitten", RiTa.pastPart("bite"));
        assertEquals("broken", RiTa.pastPart("break"));
        assertEquals("called", RiTa.pastPart("call"));
        assertEquals("committed", RiTa.pastPart("commit"));
        assertEquals("computerized", RiTa.pastPart("computerize"));
        assertEquals("concerned", RiTa.pastPart("concern"));
        assertEquals("discriminated", RiTa.pastPart("discriminate"));
        assertEquals("ended", RiTa.pastPart("end"));
        assertEquals("expected", RiTa.pastPart("expect"));
        assertEquals("finished", RiTa.pastPart("finish"));
        assertEquals("gained", RiTa.pastPart("gain"));
        assertEquals("gotten", RiTa.pastPart("get"));
        assertEquals("increased", RiTa.pastPart("increase"));
        assertEquals("involved", RiTa.pastPart("involve"));
        assertEquals("launched", RiTa.pastPart("launch"));
        assertEquals("led", RiTa.pastPart("lead"));
        assertEquals("lived", RiTa.pastPart("live"));
        assertEquals("outpaced", RiTa.pastPart("outpace"));
        assertEquals("overseen", RiTa.pastPart("oversee"));
        assertEquals("oversold", RiTa.pastPart("oversell"));
        assertEquals("paled", RiTa.pastPart("pale"));
        assertEquals("prepaid", RiTa.pastPart("prepay"));
        assertEquals("pressured", RiTa.pastPart("pressure"));
        assertEquals("proliferated", RiTa.pastPart("proliferate"));
        assertEquals("remade", RiTa.pastPart("remake"));
        assertEquals("reopened", RiTa.pastPart("reopen"));
        assertEquals("reported", RiTa.pastPart("report"));
        assertEquals("resold", RiTa.pastPart("resell"));
        assertEquals("settled", RiTa.pastPart("settle"));

        assertEquals("bitten", RiTa.pastPart("bite"));
        assertEquals("broken", RiTa.pastPart("break"));
        assertEquals("built", RiTa.pastPart("build"));
        assertEquals("entered", RiTa.pastPart("enter"));
        assertEquals("owned", RiTa.pastPart("own"));
        assertEquals("planned", RiTa.pastPart("plan"));
        assertEquals("rented", RiTa.pastPart("rent"));
        assertEquals("repurchased", RiTa.pastPart("repurchase"));
        assertEquals("roasted", RiTa.pastPart("roast"));

        assertEquals("started", RiTa.pastPart("start"));
        assertEquals("busted", RiTa.pastPart("bust"));
        assertEquals("hearted", RiTa.pastPart("heart"));
        assertEquals("closeted", RiTa.pastPart("closet"));
        assertEquals("borne", RiTa.pastPart("bear"));

        if (HAS_LEX) {
            // is already past part
            assertEquals("hopped", RiTa.pastPart("hopped"));
            assertEquals("hated", RiTa.pastPart("hated"));
            assertEquals("created", RiTa.pastPart("created"));
            assertEquals("committed", RiTa.pastPart("committed"));
            assertEquals("submitted", RiTa.pastPart("submitted"));
            assertEquals("come", RiTa.pastPart("come"));
            assertEquals("forgotten", RiTa.pastPart("forgotten"));
            assertEquals("arisen", RiTa.pastPart("arisen"));
            assertEquals("eaten", RiTa.pastPart("eaten"));
            assertEquals("chosen", RiTa.pastPart("chosen"));
            assertEquals("frozen", RiTa.pastPart("frozen"));
            assertEquals("stolen", RiTa.pastPart("stolen"));
            assertEquals("worn", RiTa.pastPart("worn"));
            assertEquals("broken", RiTa.pastPart("broken"));
            assertEquals("written", RiTa.pastPart("written"));
            assertEquals("ridden", RiTa.pastPart("ridden"));
            assertEquals("drawn", RiTa.pastPart("drawn"));
            assertEquals("known", RiTa.pastPart("known"));
            assertEquals("grown", RiTa.pastPart("grown"));
            assertEquals("done", RiTa.pastPart("done"));
            assertEquals("gone", RiTa.pastPart("gone"));

            assertEquals("awoken", RiTa.pastPart("awake"));
            assertEquals("become", RiTa.pastPart("become"));
            assertEquals("drunk", RiTa.pastPart("drink"));
            assertEquals("run", RiTa.pastPart("run"));
            assertEquals("shone", RiTa.pastPart("shine"));

            assertEquals("grown", RiTa.pastPart("grown"));
            assertEquals("heard", RiTa.pastPart("heard"));
        }
    }

    @Test
    void shouldCallPresentPart() {
        assertEquals("", RiTa.presentPart(""));
        assertEquals("sleeping", RiTa.presentPart("sleep"));
        assertEquals("withholding", RiTa.presentPart("withhold"));

        assertEquals("cutting", RiTa.presentPart("cut"));
        assertEquals("going", RiTa.presentPart("go"));
        assertEquals("running", RiTa.presentPart("run"));
        assertEquals("speaking", RiTa.presentPart("speak"));
        assertEquals("breaking", RiTa.presentPart("break"));
        assertEquals("becoming", RiTa.presentPart("become"));
        assertEquals("pleading", RiTa.presentPart("plead"));
        assertEquals("awaking", RiTa.presentPart("awake"));
        assertEquals("studying", RiTa.presentPart("study"));

        assertEquals("lying", RiTa.presentPart("lie"));
        assertEquals("swimming", RiTa.presentPart("swim"));
        assertEquals("running", RiTa.presentPart("run"));
        assertEquals("digging", RiTa.presentPart("dig"));
        assertEquals("setting", RiTa.presentPart("set"));
        assertEquals("speaking", RiTa.presentPart("speak"));
        assertEquals("bringing", RiTa.presentPart("bring"));
        assertEquals("speaking", RiTa.presentPart("speak"));

        assertEquals("studying", RiTa.presentPart("study ")); // trim
        assertEquals("studying", RiTa.presentPart(" study")); // trim

        assertEquals("hoeing", RiTa.presentPart("hoe"));
        assertEquals("shoeing", RiTa.presentPart("shoe"));

        if (HAS_LEX) {
            assertEquals("awoken", RiTa.pastPart("awake"));
            assertEquals("become", RiTa.pastPart("become"));
            assertEquals("drunk", RiTa.pastPart("drink"));
            assertEquals("run", RiTa.pastPart("run"));
            assertEquals("shone", RiTa.pastPart("shine"));
        }
    }

    @Test
    void shouldConjugateVbds() {
        assertEquals("went", RiTa.conjugate("go", Map.of(
            "number", RiTa.SINGULAR,
            "person", RiTa.FIRST,
            "tense", RiTa.PAST)));
        assertEquals("ran", RiTa.conjugate("run", Map.of(
            "number", RiTa.SINGULAR,
            "person", RiTa.FIRST,
            "tense", RiTa.PAST)));
    }

    @Test
    void shouldCallConjugate() {
        Map<String, Object> args;
        String[] s;
        String[] a;
        String c;

        assertEquals("walk", RiTa.conjugate("walk"));
        assertThrows(Exception.class, RiTa::conjugate);
        assertThrows(Exception.class, () -> RiTa.conjugate(""));

        assertEquals("swum", RiTa.pastPart("swim"));

        assertEquals("being", RiTa.conjugate("be", Map.of("form", RiTa.GERUND)));
        assertEquals("were", RiTa.conjugate("are", Map.of(
            "number", RiTa.PLURAL, "person", RiTa.SECOND, "tense", RiTa.PAST)));

        s = new String[]{"swim", "need", "open"};
        a = new String[]{"swims", "needs", "opens"};

        args = Map.of(
            "tense", RiTa.PRESENT,
            "number", RiTa.SINGULAR,
            "person", RiTa.THIRD);

        // JS: expect(() => RiTa.conjugate(args)).to.throw  — no parens, so chai asserts nothing.
        //     Passing the options object as the verb is not typeable in Java; documented only.
        // JS: expect(() => RiTa.conjugate("", args)).to.throw — ditto (no assertion).
        RiTa.conjugate("", args);

        for (int i = 0; i < s.length; i++) {
            c = RiTa.conjugate(s[i], args);
            assertEquals(a[i], c);
        }

        args = Map.of(
            "tense", RiTa.PRESENT,
            "number", RiTa.SINGULAR,
            "person", RiTa.THIRD,
            "passive", true);

        a = new String[]{"is swum", "is needed", "is opened"};
        for (int i = 0; i < s.length; i++) {
            assertEquals(a[i], RiTa.conjugate(s[i], args));
        }

        args = Map.of(
            "number", RiTa.SINGULAR,
            "person", RiTa.FIRST,
            "tense", RiTa.PAST);

        assertEquals("swam", RiTa.conjugate("swim", args));

        s = new String[]{"swim", "need", "open"};
        a = new String[]{"swam", "needed", "opened"};

        assertTrue(a.length == s.length);

        for (int i = 0; i < s.length; i++) {
            c = RiTa.conjugate(s[i], args);
            assertEquals(a[i], c);
        }

        args = Map.of(
            "number", RiTa.PLURAL,
            "person", RiTa.SECOND,
            "tense", RiTa.PAST);

        a = new String[]{"swam", "needed", "opened"};
        assertTrue(a.length == s.length);

        for (int i = 0; i < s.length; i++) {
            assertEquals(a[i], RiTa.conjugate(s[i], args));
        }

        args = Map.of(
            "number", RiTa.PLURAL,
            "person", RiTa.SECOND,
            "tense", RiTa.FUTURE);
        a = new String[]{"will swim", "will need", "will open"};
        assertTrue(a.length == s.length);

        for (int i = 0; i < s.length; i++) {
            assertEquals(a[i], RiTa.conjugate(s[i], args));
        }

        args = Map.of(
            "tense", RiTa.PAST,
            "number", RiTa.SINGULAR,
            "person", RiTa.THIRD);
        a = new String[]{"swam", "needed", "opened"};

        assertTrue(a.length == s.length);

        for (int i = 0; i < s.length; i++) {
            c = RiTa.conjugate(s[i], args);
            assertEquals(a[i], c);
        }

        args = Map.of(
            "tense", RiTa.PAST,
            "number", RiTa.SINGULAR,
            "person", RiTa.THIRD,
            "form", RiTa.INFINITIVE);
        a = new String[]{"to swim", "to need", "to open"};
        assertTrue(a.length == s.length);
        for (int i = 0; i < s.length; i++) {
            c = RiTa.conjugate(s[i], args);
            assertEquals(a[i], c);
        }

        args = Map.of(
            "tense", RiTa.PAST,
            "number", RiTa.SINGULAR,
            "person", RiTa.THIRD,
            "passive", true);

        s = new String[]{"scorch", "burn", "hit"};
        a = new String[]{"was scorched", "was burned", "was hit"};
        assertTrue(a.length == s.length);
        for (int i = 0; i < s.length; i++) {
            c = RiTa.conjugate(s[i], args);
            assertEquals(a[i], c);
        }

        s = new String[]{"swim", "need", "open"};
        args = Map.of(
            "tense", RiTa.PRESENT,
            "number", RiTa.SINGULAR,
            "person", RiTa.THIRD,
            "form", RiTa.INFINITIVE,
            "progressive", true);
        a = new String[]{"to be swimming", "to be needing", "to be opening"};
        assertTrue(a.length == s.length);
        for (int i = 0; i < s.length; i++) {
            c = RiTa.conjugate(s[i], args);
            assertEquals(a[i], c);
        }

        args = Map.of(
            "tense", RiTa.PRESENT,
            "number", RiTa.SINGULAR,
            "person", RiTa.THIRD,
            "form", RiTa.INFINITIVE,
            "perfect", true);

        a = new String[]{"to have swum", "to have needed", "to have opened"};
        assertTrue(a.length == s.length);
        for (int i = 0; i < s.length; i++) {
            c = RiTa.conjugate(s[i], args);
            assertEquals(a[i], c);
        }

        args = Map.of(
            "number", RiTa.PLURAL,
            "person", RiTa.SECOND,
            "tense", RiTa.PAST);
        assertEquals("bartered", RiTa.conjugate("barter", args));
        assertEquals("ran", RiTa.conjugate("run", args));

        args = Map.of(
            "number", RiTa.PLURAL,
            "person", RiTa.SECOND,
            "tense", RiTa.PAST);
        s = new String[]{"compete", "complete", "eject"};
        a = new String[]{"competed", "completed", "ejected"};
        for (int i = 0; i < s.length; i++) {
            assertEquals(a[i], RiTa.conjugate(s[i], args), "failed on " + s[i]);
        }

        args = Map.of(
            "number", RiTa.PLURAL,
            "person", RiTa.SECOND,
            "tense", RiTa.PAST,
            "interrogative", true);
        s = new String[]{"compete", "complete", "eject"};
        a = new String[]{"compete", "complete", "eject"};
        for (int i = 0; i < s.length; i++) {
            assertEquals(a[i], RiTa.conjugate(s[i], args), "failed on " + s[i]);
        }

        // string args
        assertThrows(Exception.class, () -> RiTa.conjugate("walk", "invalid args"));
        assertEquals("walk", RiTa.conjugate("walk", "1SPr"));
        assertEquals("walk", RiTa.conjugate("walk", "1PPr"));
        assertEquals("walk", RiTa.conjugate("walk", "2SPr"));
        assertEquals("walks", RiTa.conjugate("walk", "3SPr"));
        assertEquals("will walk", RiTa.conjugate("walk", "1SFu"));
        assertEquals("walked", RiTa.conjugate("walk", "1SPa"));
        assertEquals("walked", RiTa.conjugate("walk", "2PPa"));
        assertEquals("were", RiTa.conjugate("is", "3PPa"));
        assertEquals("were", RiTa.conjugate("is", "2SPa"));
        assertEquals("was", RiTa.conjugate("is", "3SPa"));
        assertEquals("were", RiTa.conjugate("is", "2PPa"));

        // 4 parameters
        String[] original = {"run", "walk", "swim", "create"};
        // passive
        String[] expected = {"is run", "is walked", "is swum", "is created"};
        for (int i = 0; i < original.length; i++) {
            assertEquals(expected[i], RiTa.conjugate(original[i], Map.of("person", RiTa.THIRD, "passive", true)));
        }
        // progressive
        expected = new String[]{"is running", "is walking", "is swimming", "is creating"};
        for (int i = 0; i < original.length; i++) {
            assertEquals(expected[i], RiTa.conjugate(original[i], Map.of("person", RiTa.THIRD, "progressive", true)));
        }
        // interrogative
        expected = new String[]{"run", "walk", "swim", "create"};
        for (int i = 0; i < original.length; i++) {
            assertEquals(expected[i], RiTa.conjugate(original[i], Map.of("person", RiTa.THIRD, "interrogative", true)));
        }
        // perfect
        expected = new String[]{"has run", "has walked", "has swum", "has created"};
        for (int i = 0; i < original.length; i++) {
            assertEquals(expected[i], RiTa.conjugate(original[i], Map.of("person", RiTa.THIRD, "perfect", true)));
        }
        // gerund passive
        expected = new String[]{"being run", "being walked", "being swum", "being created"};
        for (int i = 0; i < original.length; i++) {
            assertEquals(expected[i], RiTa.conjugate(original[i], Map.of("person", RiTa.THIRD, "passive", true, "form", RiTa.GERUND)));
        }
        // gerund progressive
        expected = new String[]{"being running", "being walking", "being swimming", "being creating"};
        for (int i = 0; i < original.length; i++) {
            assertEquals(expected[i], RiTa.conjugate(original[i], Map.of("person", RiTa.THIRD, "progressive", true, "form", RiTa.GERUND)));
        }
        // gerund interrogative
        expected = new String[]{"running", "walking", "swimming", "creating"};
        for (int i = 0; i < original.length; i++) {
            assertEquals(expected[i], RiTa.conjugate(original[i], Map.of("person", RiTa.THIRD, "interrogative", true, "form", RiTa.GERUND)));
        }
        // gerund perfect
        expected = new String[]{"having run", "having walked", "having swum", "having created"};
        for (int i = 0; i < original.length; i++) {
            assertEquals(expected[i], RiTa.conjugate(original[i], Map.of("person", RiTa.THIRD, "perfect", true, "form", RiTa.GERUND)));
        }
        // infinitive passive
        expected = new String[]{"to be run", "to be walked", "to be swum", "to be created"};
        for (int i = 0; i < original.length; i++) {
            assertEquals(expected[i], RiTa.conjugate(original[i], Map.of("person", RiTa.THIRD, "passive", true, "form", RiTa.INFINITIVE)));
        }
        // infinitive progressive
        expected = new String[]{"to be running", "to be walking", "to be swimming", "to be creating"};
        for (int i = 0; i < original.length; i++) {
            assertEquals(expected[i], RiTa.conjugate(original[i], Map.of("person", RiTa.THIRD, "progressive", true, "form", RiTa.INFINITIVE)));
        }
        // infinitive interrogative
        expected = new String[]{"to run", "to walk", "to swim", "to create"};
        for (int i = 0; i < original.length; i++) {
            assertEquals(expected[i], RiTa.conjugate(original[i], Map.of("person", RiTa.THIRD, "interrogative", true, "form", RiTa.INFINITIVE)));
        }
        // infinitive perfect
        expected = new String[]{"to have run", "to have walked", "to have swum", "to have created"};
        for (int i = 0; i < original.length; i++) {
            assertEquals(expected[i], RiTa.conjugate(original[i], Map.of("person", RiTa.THIRD, "perfect", true, "form", RiTa.INFINITIVE)));
        }
        RiTa.conjugate("swim", "2PPa");

        // deal with non-base form
        assertEquals("walks", RiTa.conjugate("walked", "3SPr"));
        assertEquals("changes", RiTa.conjugate("changed", "3SPr"));
        assertEquals("spends", RiTa.conjugate("spent", "3SPr"));
        assertEquals("eats", RiTa.conjugate("eaten", "3SPr"));
        RiTa.conjugate("swim", "2PPa");
    }

    @Test
    void shouldCallToString() {
        assertEquals("  ---------------------\n  Passive = false\n  Perfect = false\n  Progressive = false\n  ---------------------\n  Number = 8\n  Person = 2\n  Tense = 4\n  ---------------------\n",
            RiTa.conjugator.toString());
    }

    @Test
    void shouldAcceptStems() {
        Map<String, Object> plurPast2 = Map.of("number", RiTa.PLURAL, "person", RiTa.SECOND, "tense", RiTa.PAST);
        Map<String, Object> plurPres2 = Map.of("number", RiTa.PLURAL, "person", RiTa.SECOND, "tense", RiTa.PRESENT);
        Map<String, Object> singPres3 = Map.of("number", RiTa.SINGULAR, "person", RiTa.THIRD, "tense", RiTa.PRESENT);

        // https://github.com/dhowe/rita/issues/116
        String stem = RiTa.stem("walking");
        assertEquals("walked", RiTa.conjugate(stem, plurPast2), stem + " => walked");
        assertEquals("walk", RiTa.conjugate(stem, plurPres2), stem + " => walk");
        assertEquals("walks", RiTa.conjugate(stem, singPres3), stem + " => walks");

        stem = RiTa.stem("writing");
        assertEquals("wrote", RiTa.conjugate(stem, plurPast2), stem + " => wrote");
        assertEquals("write", RiTa.conjugate(stem, plurPres2), stem + " => write");
        assertEquals("writes", RiTa.conjugate(stem, singPres3), stem + " => writes");

        stem = RiTa.stem("asked");
        assertEquals("asked", RiTa.conjugate(stem, plurPast2), stem + " => asked");
        assertEquals("ask", RiTa.conjugate(stem, plurPres2), stem + " => ask");
        assertEquals("asks", RiTa.conjugate(stem, singPres3), stem + " => asks");

        stem = RiTa.stem("changed");
        assertEquals("changed", RiTa.conjugate(stem, plurPast2), stem + " => changed");
        assertEquals("change", RiTa.conjugate(stem, plurPres2), stem + " => change");
        assertEquals("changes", RiTa.conjugate(stem, singPres3), stem + " => changes");

        stem = RiTa.stem("admired");
        assertEquals("admired", RiTa.conjugate(stem, plurPast2), stem + " => admired");
        assertEquals("admire", RiTa.conjugate(stem, plurPres2), stem + " => admire");
        assertEquals("admires", RiTa.conjugate(stem, singPres3), stem + " => admires");

        stem = RiTa.stem("cured");
        assertEquals("cured", RiTa.conjugate(stem, plurPast2), stem + " => cured");
        assertEquals("cure", RiTa.conjugate(stem, plurPres2), stem + " => cure");
        assertEquals("cures", RiTa.conjugate(stem, singPres3), stem + " => cures");

        stem = RiTa.stem("studies");
        assertEquals("studied", RiTa.conjugate(stem, plurPast2), stem + " => studied");
        assertEquals("study", RiTa.conjugate(stem, plurPres2), stem + " => study");
        assertEquals("studies", RiTa.conjugate(stem, singPres3), stem + " => studies");
    }

    @Test
    void shouldAcceptStemPairs() {
        // more random tests
        Map<String, Object> opts = Map.of("number", RiTa.PLURAL, "person", RiTa.SECOND, "tense", RiTa.PAST);
        String[][] pairs = {
            {"accompanying", "accompanied"},
            {"feeling", "felt"},
            {"placating", "placated"},
            {"centralizing", "centralized"},
            {"humanized", "humanized"},
            {"boosted", "boosted"},
            {"wearing", "wore"},
            {"aroused", "aroused"},
            {"rising", "rose"},
            {"raising", "raised"},
            {"vibrating", "vibrated"},
            {"injection", "injected"},
            {"vibration", "vibrated"},
        };
        for (String[] p : pairs) {
            String res = RiTa.conjugate(RiTa.stem(p[0]), opts);
            assertEquals(p[1], res, p[0] + " => " + RiTa.stem(p[0]) + " => " + p[1]);
        }
    }

    @Test
    void shouldCallUnconjugate() {
        assertEquals("trepan", RiTa.conjugator.unconjugate("trepanning"));

        // 3rd person singular (regular)
        assertEquals("play", RiTa.conjugator.unconjugate("plays"));
        assertEquals("take", RiTa.conjugator.unconjugate("takes"));
        assertEquals("get", RiTa.conjugator.unconjugate("gets"));
        assertEquals("come", RiTa.conjugator.unconjugate("comes"));
        assertEquals("go", RiTa.conjugator.unconjugate("goes"));
        assertEquals("teach", RiTa.conjugator.unconjugate("teaches"));
        assertEquals("fix", RiTa.conjugator.unconjugate("fixes"));
        assertEquals("miss", RiTa.conjugator.unconjugate("misses"));
        assertEquals("study", RiTa.conjugator.unconjugate("studies"));
        assertEquals("try", RiTa.conjugator.unconjugate("tries"));
        assertEquals("carry", RiTa.conjugator.unconjugate("carries"));
        assertEquals("wish", RiTa.conjugator.unconjugate("wishes"));
        assertEquals("blitz", RiTa.conjugator.unconjugate("blitzes"));

        // -ed (regular)
        assertEquals("watch", RiTa.conjugator.unconjugate("watched"));
        assertEquals("plant", RiTa.conjugator.unconjugate("planted"));
        assertEquals("water", RiTa.conjugator.unconjugate("watered"));
        assertEquals("pull", RiTa.conjugator.unconjugate("pulled"));
        assertEquals("pick", RiTa.conjugator.unconjugate("picked"));
        assertEquals("like", RiTa.conjugator.unconjugate("liked"));
        assertEquals("move", RiTa.conjugator.unconjugate("moved"));
        assertEquals("taste", RiTa.conjugator.unconjugate("tasted"));
        assertEquals("try", RiTa.conjugator.unconjugate("tried"));
        assertEquals("study", RiTa.conjugator.unconjugate("studied"));
        assertEquals("carry", RiTa.conjugator.unconjugate("carried"));
        assertEquals("dig", RiTa.conjugator.unconjugate("digged"));
        assertEquals("flag", RiTa.conjugator.unconjugate("flagged"));

        // -ing (regular)
        assertEquals("blow", RiTa.conjugator.unconjugate("blowing"));
        assertEquals("rain", RiTa.conjugator.unconjugate("raining"));
        assertEquals("come", RiTa.conjugator.unconjugate("coming"));
        assertEquals("have", RiTa.conjugator.unconjugate("having"));
        assertEquals("run", RiTa.conjugator.unconjugate("running"));
        assertEquals("put", RiTa.conjugator.unconjugate("putting"));
        assertEquals("sit", RiTa.conjugator.unconjugate("sitting"));
        assertEquals("pull", RiTa.conjugator.unconjugate("pulling"));

        // irregular
        assertEquals("have", RiTa.conjugator.unconjugate("has"));
        assertEquals("have", RiTa.conjugator.unconjugate("had"));
        assertEquals("sit", RiTa.conjugator.unconjugate("sat"));
        assertEquals("show", RiTa.conjugator.unconjugate("shown"));
        assertEquals("eat", RiTa.conjugator.unconjugate("ate"));
        assertEquals("go", RiTa.conjugator.unconjugate("went"));
        assertEquals("meet", RiTa.conjugator.unconjugate("met"));

        // for base form verbs, return input
        assertEquals("have", RiTa.conjugator.unconjugate("have"));
        assertEquals("eat", RiTa.conjugator.unconjugate("eat"));
        assertEquals("play", RiTa.conjugator.unconjugate("play"));
        assertEquals("go", RiTa.conjugator.unconjugate("go"));
        assertEquals("do", RiTa.conjugator.unconjugate("do"));

        // not in lexicon
        assertEquals("spoon", RiTa.conjugator.unconjugate("spooning"));
        assertEquals("mepan", RiTa.conjugator.unconjugate("mepanning"));
        assertEquals("muddle", RiTa.conjugator.unconjugate("muddling"));

        // JS `if (typeof NOLEX !== 'undefined')` is false when a lexicon is present — block skipped.

        // words with wrong 'vb' tag — https://github.com/dhowe/rita/issues/177
        assertEquals("bite", RiTa.conjugator.unconjugate("bitten"));
        assertEquals("break", RiTa.conjugator.unconjugate("broken"));
        assertEquals("commit", RiTa.conjugator.unconjugate("committed"));
        assertEquals("computerize", RiTa.conjugator.unconjugate("computerized"));
        assertEquals("concern", RiTa.conjugator.unconjugate("concerned"));
        assertEquals("discriminate", RiTa.conjugator.unconjugate("discriminated"));
        assertEquals("end", RiTa.conjugator.unconjugate("ended"));
        assertEquals("expect", RiTa.conjugator.unconjugate("expected"));
        assertEquals("finish", RiTa.conjugator.unconjugate("finished"));
        assertEquals("gain", RiTa.conjugator.unconjugate("gained"));
        assertEquals("get", RiTa.conjugator.unconjugate("gotten"));
        assertEquals("increase", RiTa.conjugator.unconjugate("increased"));
        assertEquals("involve", RiTa.conjugator.unconjugate("involved"));
        assertEquals("launch", RiTa.conjugator.unconjugate("launched"));
        assertEquals("lead", RiTa.conjugator.unconjugate("led"));
        assertEquals("live", RiTa.conjugator.unconjugate("lived"));
        assertEquals("outpace", RiTa.conjugator.unconjugate("outpaced"));
        assertEquals("oversee", RiTa.conjugator.unconjugate("overseen"));
        assertEquals("pale", RiTa.conjugator.unconjugate("paled"));
        assertEquals("prepay", RiTa.conjugator.unconjugate("prepaid"));
        assertEquals("pressure", RiTa.conjugator.unconjugate("pressured"));
        assertEquals("proliferate", RiTa.conjugator.unconjugate("proliferated"));
        assertEquals("remake", RiTa.conjugator.unconjugate("remade"));
        assertEquals("reopen", RiTa.conjugator.unconjugate("reopened"));
        assertEquals("report", RiTa.conjugator.unconjugate("reported"));
        assertEquals("sell", RiTa.conjugator.unconjugate("sold"));
        assertEquals("resell", RiTa.conjugator.unconjugate("resold"));
        assertEquals("settle", RiTa.conjugator.unconjugate("settled"));
        assertEquals("start", RiTa.conjugator.unconjugate("started"));
        assertEquals("be", RiTa.conjugator.unconjugate("were"));

        assertEquals("bite", RiTa.conjugator.unconjugate("bitten"));
        assertEquals("break", RiTa.conjugator.unconjugate("broken"));
        assertEquals("own", RiTa.conjugator.unconjugate("owned"));
        assertEquals("plan", RiTa.conjugator.unconjugate("planned"));
        assertEquals("rent", RiTa.conjugator.unconjugate("rented"));
        assertEquals("repurchase", RiTa.conjugator.unconjugate("repurchased"));
        assertEquals("roast", RiTa.conjugator.unconjugate("roasted"));

        assertEquals("bust", RiTa.conjugator.unconjugate("busted"));
        assertEquals("grow", RiTa.conjugator.unconjugate("grown"));
        assertEquals("blow", RiTa.conjugator.unconjugate("blown"));
        assertEquals("hear", RiTa.conjugator.unconjugate("heard"));
    }

    @Test
    void shouldConjugateVerbs() {
        // words with wrong 'vb' tag — https://github.com/dhowe/rita/issues/177
        Map<String, Object> opt = Map.of(
            "number", RiTa.SINGULAR,
            "person", RiTa.FIRST,
            "tense", RiTa.PAST);
        assertEquals("bit", RiTa.conjugate("bite", opt));
        assertEquals("broke", RiTa.conjugate("break", opt));
        assertEquals("called", RiTa.conjugate("call", opt));
        assertEquals("committed", RiTa.conjugate("commit", opt));
        assertEquals("computerized", RiTa.conjugate("computerize", opt));
        assertEquals("concerned", RiTa.conjugate("concern", opt));
        assertEquals("discriminated", RiTa.conjugate("discriminate", opt));
        assertEquals("ended", RiTa.conjugate("end", opt));
        assertEquals("expected", RiTa.conjugate("expect", opt));
        assertEquals("finished", RiTa.conjugate("finish", opt));
        assertEquals("gained", RiTa.conjugate("gain", opt));
        assertEquals("got", RiTa.conjugate("get", opt));
        assertEquals("increased", RiTa.conjugate("increase", opt));
        assertEquals("involved", RiTa.conjugate("involve", opt));
        assertEquals("launched", RiTa.conjugate("launch", opt));
        assertEquals("led", RiTa.conjugate("lead", opt));
        assertEquals("lived", RiTa.conjugate("live", opt));
        assertEquals("concerned", RiTa.conjugate("concern", opt));
        assertEquals("oversaw", RiTa.conjugate("oversee", opt));
        assertEquals("paled", RiTa.conjugate("pale", opt));
        assertEquals("prepaid", RiTa.conjugate("prepay", opt));
        assertEquals("pressured", RiTa.conjugate("pressure", opt));
        assertEquals("proliferated", RiTa.conjugate("proliferate", opt));
        assertEquals("remade", RiTa.conjugate("remake", opt));
        assertEquals("reopened", RiTa.conjugate("reopen", opt));
        assertEquals("reported", RiTa.conjugate("report", opt));
        assertEquals("resold", RiTa.conjugate("resell", opt));
        assertEquals("settled", RiTa.conjugate("settle", opt));
        assertEquals("started", RiTa.conjugate("start", opt));

        opt = Map.of(
            "tense", RiTa.PRESENT,
            "number", RiTa.SINGULAR,
            "perfect", true);
        assertEquals("have bitten", RiTa.conjugate("bite", opt));
        assertEquals("have broken", RiTa.conjugate("break", opt));
        assertEquals("have built", RiTa.conjugate("build", opt));
        assertEquals("have entered", RiTa.conjugate("enter", opt));
        assertEquals("have owned", RiTa.conjugate("own", opt));
        assertEquals("have planned", RiTa.conjugate("plan", opt));
        assertEquals("have rented", RiTa.conjugate("rent", opt));
        assertEquals("have repurchased", RiTa.conjugate("repurchase", opt));
        assertEquals("have roasted", RiTa.conjugate("roast", opt));
    }

    @Test
    void shouldHandleStemLookupCorrectly() {
        // Regression: _handleStem was rewritten from a regex-scan to a binary-searched
        // verb index + memo cache; these assert the result is unchanged.
        Conjugator conj = RiTa.conjugator;

        // identity cases (base verbs / non-verbs return the word)
        String[] identity = {"be", "been", "goes", "running", "walked", "bettering"};
        for (String w : identity) {
            assertEquals(w, conj._handleStem(w));
        }

        // stem-mapping cases (noun -> verb via longest-prefix match)
        assertEquals("alienate", conj._handleStem("alien"));
        assertEquals("bathe", conj._handleStem("bath"));
        assertEquals("centralize", conj._handleStem("central"));
    }

    @Test
    void shouldInvalidateStemCacheOnLexiconSwap() {
        Conjugator conj = RiTa.conjugator;
        Map<String, Object> orig = RiTa.lexicon.data;
        try {
            String before = conj._handleStem("alien");
            assertEquals("alienate", before);
            assertTrue(conj._stemCache.size() > 0);

            // a new data object identity must reset the memo and its ref
            RiTa.lexicon.data = new LinkedHashMap<>(orig);
            conj._handleStem("alien");
            assertSame(RiTa.lexicon.data, conj._stemCacheRef);
            assertEquals(1, conj._stemCache.size());

            // results stay correct across the swap
            assertEquals(before, conj._handleStem("alien"));
        } finally {
            RiTa.lexicon.data = orig;
        }
    }
}
