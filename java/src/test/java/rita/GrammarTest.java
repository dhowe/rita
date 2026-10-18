package rita;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.HashMap;
import java.util.Map;
import org.junit.jupiter.api.Test;

/**
 * Ported from <code>js/test/grammar-tests.js</code>.
 *
 * <p>Mapping: {@code expect(x).to.be.an.instanceof(RiTa.RiGrammar)} -> {@code assertTrue(x instanceof
 * RiGrammar)}; {@code expect(a).to.deep.equal(b)} -> {@code assertEquals(a, b)};
 * {@code expect(result).to.be.oneOf([...])} -> membership assertion. The final JS block is
 * disabled via {@code 0 && it(...)} and is intentionally omitted.
 */
class GrammarTest {

    @Test
    void shouldCallRiTaGrammarForABlankGrammar() {
        RiGrammar rg = RiTa.grammar();
        assertTrue(rg instanceof RiGrammar);
    }

    @Test
    void shouldCallRiGrammarFromJSON() {
        Map<String, Object> rules = rules();
        RiGrammar rg = RiGrammar.fromJSON(toJsonString(rules));
        assertTrue(rg instanceof RiGrammar);
    }

    @Test
    void shouldAllowConstructionsFromObjectOrString() {
        Map<String, Object> rules = rules();
        RiGrammar rg1 = RiTa.grammar(rules);
        RiGrammar rg2 = RiTa.grammar(toJsonString(rules));
        RiGrammar rg3 = RiGrammar.fromJSON(toJsonString(rules));
        assertEquals(rg1.toJSON(), rg2.toJSON());
        assertEquals(rg1.toJSON(), rg3.toJSON());
    }

    @Test
    void shouldCallRiTaGrammarExpand() {
        Map<String, Object> context = new HashMap<>();
        context.put("lucy", person("Lucy", "she", "Acura"));
        context.put("sam", person("Sam", "he", "Subaru"));
        Map<String, Object> rules = rules();
        String result = RiTa.grammar(rules, context).expand();
        assertTrue(result.equals("Meet Lucy. She drives an Acura.")
            || result.equals("Meet Sam. He drives a Subaru."),
            "unexpected expand() result: " + result);
    }

    private static Map<String, Object> person(String name, String pronoun, String car) {
        Map<String, Object> m = new HashMap<>();
        m.put("name", name);
        m.put("pronoun", pronoun);
        m.put("car", car);
        return m;
    }

    private static Map<String, Object> rules() {
        Map<String, Object> rules = new HashMap<>();
        rules.put("start", "Meet $person.name. $person.pronoun.cap() drives $person.car.art().");
        rules.put("#person", "$sam | $lucy");
        return rules;
    }

    /** Minimal JSON serializer for the flat rules map (mirrors JSON.stringify(rules)). */
    private static String toJsonString(Map<String, Object> rules) {
        StringBuilder sb = new StringBuilder("{");
        boolean first = true;
        for (Map.Entry<String, Object> e : rules.entrySet()) {
            if (!first) {
                sb.append(',');
            }
            first = false;
            sb.append(JSONObject.quote(e.getKey())).append(':').append(JSONObject.quote(String.valueOf(e.getValue())));
        }
        return sb.append('}').toString();
    }

    /** Tiny JSON helper to avoid pulling Gson into main sources. */
    private static final class JSONObject {
        static String quote(String s) {
            return "\"" + s.replace("\\", "\\\\").replace("\"", "\\\"") + "\"";
        }
    }
}
