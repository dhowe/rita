package rita;

import java.util.List;
import java.util.Map;

/**
 * Part-of-speech tagger — stub for {@code js/src/tagger.js}. Methods throw until ported.
 */
public class Tagger {

    /** JS {@code tag(input, opts)} — returns a tag array, or an inline string when {@code inline}. */
    public Object tag(String word, Map<String, Object> options) {
        throw RiTa.notPorted("tagger.tag");
    }

    public String[] tag(String word) {
        throw RiTa.notPorted("tagger.tag");
    }

    public Object tag(String[] words, Map<String, Object> options) {
        throw RiTa.notPorted("tagger.tag");
    }

    public String[] tag(String[] words) {
        throw RiTa.notPorted("tagger.tag");
    }

    /** JS {@code tag()} — undefined input yields an empty tag array. */
    public String[] tag() {
        throw RiTa.notPorted("tagger.tag");
    }

    /** JS {@code inlineTags(words, tags, delimiter)}. */
    public String inlineTags(String[] words, String[] tags, String delimiter) {
        throw RiTa.notPorted("tagger.inlineTags");
    }

    public String inlineTags(String[] words, String[] tags) {
        throw RiTa.notPorted("tagger.inlineTags");
    }

    public String inlineTags(String[] words) {
        throw RiTa.notPorted("tagger.inlineTags");
    }

    /** JS {@code inlineTags()} — undefined words yield the empty string. */
    public String inlineTags() {
        throw RiTa.notPorted("tagger.inlineTags");
    }

    /** All POS tags for a word (JS returns an array of tag strings). */
    public List<String> allTags(String word, Map<String, Object> options) {
        throw RiTa.notPorted("tagger.allTags");
    }

    public List<String> allTags(String word, boolean simple) {
        throw RiTa.notPorted("tagger.allTags");
    }

    public List<String> allTags(String word) {
        throw RiTa.notPorted("tagger.allTags");
    }

    /** JS {@code allTags(array)} — a non-string input yields no tags. */
    public List<String> allTags(String[] words) {
        throw RiTa.notPorted("tagger.allTags");
    }

    /** JS {@code hasTag(choices, tag)} — choices is a tag list, or a non-array (always false). */
    public boolean hasTag(List<String> choices, String tag) {
        throw RiTa.notPorted("tagger.hasTag");
    }

    /** JS {@code hasTag(nonArray, tag)} — a non-array first argument is never tagged. */
    public boolean hasTag(String choices, String tag) {
        throw RiTa.notPorted("tagger.hasTag");
    }

    /** JS {@code hasTag()} — undefined choices are not tagged. */
    public boolean hasTag() {
        throw RiTa.notPorted("tagger.hasTag");
    }
}
