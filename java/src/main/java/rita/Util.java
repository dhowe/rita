package rita;

/**
 * Shared helpers — stub for {@code js/src/util.js}. Methods throw until ported.
 */
public class Util {

    public static boolean isString(Object o) {
        return o instanceof String;
    }

    public static boolean isLetter(char c) {
        return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= 0xC0 && c <= 0xFF);
    }
}
