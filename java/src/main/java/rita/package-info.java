/**
 * RiTa — tools for generative natural language.
 *
 * <p>The entry point is {@link rita.RiTa}, which exposes the full API as static
 * methods plus the model classes {@code RiMarkov}, {@code RiGrammar},
 * {@code BackoffModel}, {@code SuffixArray}, {@code Stemmer} and {@code Model}.
 *
 * <pre>{@code
 * import rita.*;
 *
 * String[] tokens = RiTa.tokenize("How now, brown cow?");
 * String text = RiTa.evaluate("i {have|own} a {blue|green} {bird|fish}");
 * }</pre>
 */
package rita;
