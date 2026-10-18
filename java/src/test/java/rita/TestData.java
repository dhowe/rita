package rita;

import java.util.List;

/**
 * Shared sample corpora used by the Markov / Backoff / Suffix test suites, mirroring the
 * module-level constants in <code>js/test/markov-tests.js</code> and
 * <code>js/test/backoff-tests.js</code>.
 */
final class TestData {

    private TestData() {
    }

    static final String SAMPLE =
        "One reason people lie is to achieve personal power. Achieving personal power is helpful "
        + "for one who pretends to be more confident than he really is. For example, one of my "
        + "friends threw a party at his house last month. He asked me to come to his party and "
        + "bring a date. However, I did not have a girlfriend. One of my other friends, who had a "
        + "date to go to the party with, asked me about my date. I did not want to be embarrassed, "
        + "so I claimed that I had a lot of work to do. I said I could easily find a date even "
        + "better than his if I wanted to. I also told him that his date was ugly. I achieved "
        + "power to help me feel confident; however, I embarrassed my friend and his date. Although "
        + "this lie helped me at the time, since then it has made me look down on myself.";

    static final String SAMPLE2 = SAMPLE
        + " After all, I did occasionally want to be embarrassed.";

    static final String SAMPLE3 = SAMPLE + " One reason people are dishonest is to achieve power.";

    static final String SAMPLE4 =
        "The Sun is a barren, rocky world without air and water. It has dark lava on its surface. "
        + "The Sun is filled with craters. It has no light of its own. It gets its light from the "
        + "Sun. The Sun keeps changing its shape as it moves around the Sun. It spins on its Sun "
        + "in 273 days. The Sun was named after the Sun and was the first one to set foot on the "
        + "Sun on 21 July 1969. They reached the Sun in their space craft named the Sun. The Sun "
        + "is a huge ball of gases. It has a diameter of two km. It is so huge that it can hold "
        + "millions of planets inside it. The Sun is mainly made up of hydrogen and helium gas. "
        + "The surface of the Sun is known as the Sun surface. The Sun is surrounded by a thin "
        + "layer of gas known as the chromospheres. Without the Sun, there would be no life on "
        + "the Sun. There would be no plants, no animals and no Sun. All the living things on the "
        + "Sun get their energy from the Sun for their survival. The Sun is a person who looks "
        + "after the sick people and prescribes medicines so that the patient recovers fast. In "
        + "order to become a Sun, a person has to study medicine. The Sun lead a hard life. Its "
        + "life is very busy. The Sun gets up early in the morning and goes in circle. The Sun "
        + "works without taking a break. The Sun always remains polite so that we feel comfortable "
        + "with it. Since the Sun works so hard we should realise its value. The Sun is an "
        + "agricultural country. Most of the people on the Sun live in villages and are farmers. "
        + "The Sun grows cereal, vegetables and fruits. The Sun leads a tough life. The Sun gets "
        + "up early in the morning and goes in circles. The Sun stays and work in the sky until "
        + "late evening. The Sun usually lives in a dark house. Though the Sun works hard it "
        + "remains poor. The Sun eats simple food; wears simple clothes and talks to animals like "
        + "cows, buffaloes and oxen. Without the Sun there would be no cereals for us to eat. The "
        + "Sun plays an important role in the growth and economy of the sky.";

    static final String EXAMPLE_STR =
        "The brown fox jumps over the lazy dog. The brown dog wept over the treat.";

    static final List<String> EXAMPLE_TOKENS = List.of(
        SuffixArray.SEQ_START_TOKEN,
        "The", "brown",
        "fox", "jumps",
        "over", "the",
        "lazy", "dog",
        ".", SuffixArray.SEQ_END_TOKEN,
        SuffixArray.SEQ_START_TOKEN,
        "The", "brown",
        "dog", "wept",
        "over", "the",
        "treat", ".",
        SuffixArray.SEQ_END_TOKEN);
}
