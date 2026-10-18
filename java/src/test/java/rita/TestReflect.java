package rita;

import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Test-only reflection + option-map helpers that mirror JS dynamic property access
 * ({@code obj[key]}, {@code Object.keys(obj)}) and object-literal options.
 */
final class TestReflect {

    private TestReflect() {
    }

    /** Reads a (possibly private, inherited) field by name — mirrors JS {@code obj[f]}. */
    static Object fieldOf(Object o, String name) {
        for (Class<?> c = o.getClass(); c != null; c = c.getSuperclass()) {
            try {
                Field f = c.getDeclaredField(name);
                f.setAccessible(true);
                return f.get(o);
            } catch (NoSuchFieldException ignored) {
                // keep walking up the hierarchy
            } catch (IllegalAccessException e) {
                throw new RuntimeException(e);
            }
        }
        return null;
    }

    /** Non-static field names, sorted — mirrors {@code Object.keys(obj).sort()}. */
    static List<String> keysOf(Object o) {
        List<String> keys = new ArrayList<>();
        for (Class<?> c = o.getClass(); c != null; c = c.getSuperclass()) {
            for (Field f : c.getDeclaredFields()) {
                if (!Modifier.isStatic(f.getModifiers())) {
                    keys.add(f.getName());
                }
            }
        }
        Collections.sort(keys);
        return keys;
    }

    /** Builds a {@code Map<String,Object>} from alternating key/value pairs. */
    static Map<String, Object> opts(Object... kv) {
        Map<String, Object> m = new LinkedHashMap<>();
        for (int i = 0; i + 1 < kv.length; i += 2) {
            m.put((String) kv[i], kv[i + 1]);
        }
        return m;
    }

    /** JS {@code { ...base, ...extra }} — base with extra overrides. */
    static Map<String, Object> merge(Map<String, Object> base, Object... extra) {
        Map<String, Object> m = new LinkedHashMap<>(base);
        for (int i = 0; i + 1 < extra.length; i += 2) {
            m.put((String) extra[i], extra[i + 1]);
        }
        return m;
    }
}
