import { expect } from 'chai';
import { RiTa } from './index.js';

const { BackoffModel, SuffixArray, RiMarkov } = RiTa;

// Shared sample texts (used across Markov, Markov.B, Markov.B2)
let sample = "One reason people lie is to achieve personal power. Achieving personal power is helpful for one who pretends to be more confident than he really is. For example, one of my friends threw a party at his house last month. He asked me to come to his party and bring a date. However, I did not have a girlfriend. One of my other friends, who had a date to go to the party with, asked me about my date. I did not want to be embarrassed, so I claimed that I had a lot of work to do. I said I could easily find a date even better than his if I wanted to. I also told him that his date was ugly. I achieved power to help me feel confident; however, I embarrassed my friend and his date. Although this lie helped me at the time, since then it has made me look down on myself.";
let sample2 = "One reason people lie is to achieve personal power. Achieving personal power is helpful for one who pretends to be more confident than he really is. For example, one of my friends threw a party at his house last month. He asked me to come to his party and bring a date. However, I did not have a girlfriend. One of my other friends, who had a date to go to the party with, asked me about my date. I did not want to be embarrassed, so I claimed that I had a lot of work to do. I said I could easily find a date even better than his if I wanted to. I also told him that his date was ugly. I achieved power to help me feel confident; however, I embarrassed my friend and his date. Although this lie helped me at the time, since then it has made me look down on myself. After all, I did occasionally want to be embarrassed.";
let exampleTokens = [
  SuffixArray.SEQ_START_TOKEN,
  'The', 'brown',
  'fox', 'jumps',
  'over', 'the',
  'lazy', 'dog',
  '.', SuffixArray.SEQ_END_TOKEN,
  SuffixArray.SEQ_START_TOKEN,
  'The', 'brown',
  'dog', 'wept',
  'over', 'the',
  'treat', '.',
  SuffixArray.SEQ_END_TOKEN,
];

describe('Markov', function () {

  BackoffModel.SILENT = 1;
  let exampleStr = 'The brown fox jumps over the lazy dog. The brown dog wept over the treat.';

  let sample3 = sample + ' One reason people are dishonest is to achieve power.';
  let sample4 = "The Sun is a barren, rocky world without air and water. It has dark lava on its surface. The Sun is filled with craters. It has no light of its own. It gets its light from the Sun. The Sun keeps changing its shape as it moves around the Sun. It spins on its Sun in 273 days. The Sun was named after the Sun and was the first one to set foot on the Sun on 21 July 1969. They reached the Sun in their space craft named the Sun. The Sun is a huge ball of gases. It has a diameter of two km. It is so huge that it can hold millions of planets inside it. The Sun is mainly made up of hydrogen and helium gas. The surface of the Sun is known as the Sun surface. The Sun is surrounded by a thin layer of gas known as the chromospheres. Without the Sun, there would be no life on the Sun. There would be no plants, no animals and no Sun. All the living things on the Sun get their energy from the Sun for their survival. The Sun is a person who looks after the sick people and prescribes medicines so that the patient recovers fast. In order to become a Sun, a person has to study medicine. The Sun lead a hard life. Its life is very busy. The Sun gets up early in the morning and goes in circle. The Sun works without taking a break. The Sun always remains polite so that we feel comfortable with it. Since the Sun works so hard we should realise its value. The Sun is an agricultural country. Most of the people on the Sun live in villages and are farmers. The Sun grows cereal, vegetables and fruits. The Sun leads a tough life. The Sun gets up early in the morning and goes in circles. The Sun stays and work in the sky until late evening. The Sun usually lives in a dark house. Though the Sun works hard it remains poor. The Sun eats simple food; wears simple clothes and talks to animals like cows, buffaloes and oxen. Without the Sun there would be no cereals for us to eat. The Sun plays an important role in the growth and economy of the sky.";

  let Random;
  before(async () => Random = RiTa.randomizer);

  it('should call RiMarkov', function () {
    let rm = RiTa.markov(3);
    expect(typeof rm).eq('object');
    expect(rm.size()).eq(0);
  });

  it('should call RiTa.markov', function () {
    let rm = RiTa.markov(3);
    expect(typeof rm).eq('object');
    expect(rm.size()).eq(0);

    rm = RiTa.markov(3, { text: "The dog ran away" });
    expect(rm.size()).eq(6); // includes start/end tokens

    rm = RiTa.markov(3, { text: "" });
    expect(rm.size()).eq(0);
    expect(function () { rm.generate() }).to.throw();

    rm = RiTa.markov(3, { text: sample });
    //console.log(rm.generate());

    expect(rm.generate().length).to.be.greaterThan(0);

    rm = RiTa.markov(3, { text: "Too short." });
    expect(function () { rm.generate() }).to.throw();

    expect(function () { rm = RiTa.markov(3, { text: 1 }); }).to.throw();

    expect(function () { RiTa.markov(3, { text: false }) }).to.throw();

    rm = RiTa.markov(3, { sentences: ["Sentence one.", "Sentence two."] });
    expect(rm.size()).eq(10);

    rm = RiTa.markov(3, { sentences: RiTa.sentences(sample) });
    expect(rm.generate().length).to.be.greaterThan(0);
  });

  it('should call Random.pSelect', function () {

    // should throw when options conflict
    expect(function () { Random.pselect() }).to.throw();
    expect(Random.pselect([1])).equal(0);

    //////////////////////////////////////////
    let weights = [1.0, 2, 6, -2.5, 0];
    let expected = [2, 2, 1.75, 1.55];
    let temps = [.5, 1, 2, 10];
    let distrs = [], results = [];
    temps.forEach(t => distrs.push(Random.ndist(weights, t)));
    let i, numTests = 100;
    distrs.forEach(sm => {
      let sum = 0;
      for (let j = 0; j < numTests; j++) {
        sum += Random.pselect(sm);
      }
      results.push(sum / numTests);
    });

    expect(results[i = 0], 'failed #' + i + ' temp=' + temps[i]).to.be.closeTo(expected[i], .1);
    expect(results[i = 1], 'failed #' + i + ' temp=' + temps[i]).to.be.closeTo(expected[i], .2);
    expect(results[i = 2], 'failed #' + i + ' temp=' + temps[i]).to.be.closeTo(expected[i], .4);
    expect(results[i = 3], 'failed #' + i + ' temp=' + temps[i]).to.be.closeTo(expected[i], 1);

    let distr = [[1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4], [0.2, 0.3, 0.4, 0.5]];
    expected = [3, 0.3, 0.3857];
    for (let k = 0; k < 10; k++) {
      let results = [];
      distr.forEach(sm => {
        let sum = 0;
        for (let j = 0; j < 1000; j++) {
          sum += Random.pselect2(sm);
        }
        results.push(sum / 1000);
      });
      expect(results[0]).to.be.closeTo(expected[0], .5);
      expect(results[1]).to.be.closeTo(expected[1], .05);
      expect(results[2]).to.be.closeTo(expected[2], .05);
    }
  });

  // NOTE: markov-a called this 'should call Random.pselectIndex' (lowercase s); name unified to C spelling
  it('should call Random.pSelectIndex', function () {

    // should throw when options conflict
    expect(function () { Random.pselect() }).to.throw();
    expect(Random.pselectIndex([1])).equal(0);

    //////////////////////////////////////////
    let weights = [1.0, 2, 6, -2.5, 0];
    let expected = [2, 2, 1.75, 1.55];
    let temps = [.5, 1, 2, 10];
    let distrs = [], results = [];
    temps.forEach(t => distrs.push(Random.ndist(weights, t)));
    let i, numTests = 100;
    distrs.forEach(sm => {
      let sum = 0;
      for (let j = 0; j < numTests; j++) {
        sum += Random.pselectIndex(sm);
      }
      results.push(sum / numTests);
    });

    expect(results[i = 0], 'failed #' + i + ' temp=' + temps[i]).to.be.closeTo(expected[i], .1);
    expect(results[i = 1], 'failed #' + i + ' temp=' + temps[i]).to.be.closeTo(expected[i], .2);
    expect(results[i = 2], 'failed #' + i + ' temp=' + temps[i]).to.be.closeTo(expected[i], .4);
    expect(results[i = 3], 'failed #' + i + ' temp=' + temps[i]).to.be.closeTo(expected[i], 1);
    //expect(results[i = 4], 'failed #' + i + ' temp=' + temps[i]).to.be.closeTo(expected[i], .75);

    let distr = [[1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4], [0.2, 0.3, 0.4, 0.5]];
    expected = [3, 0.3, 0.3857];
    //should pselect2 return index or return the value (which is what is returned now)
    for (let k = 0; k < 10; k++) {
      let results = [];
      distr.forEach(sm => {
        let sum = 0;
        for (let j = 0; j < 1000; j++) {
          sum += Random.pselect2(sm); // TODO: check diff between pselect, pselect2 and pselectIndex
        }
        results.push(sum / 1000);
      });
      expect(results[0]).to.be.closeTo(expected[0], .5);
      expect(results[1]).to.be.closeTo(expected[1], .05);
      expect(results[2]).to.be.closeTo(expected[2], .05);
    }
  });

  it('should call Random.ndist', function () {
    expect(() => Random.ndist([1.0, 2, 6, -2.5, 0])).to.throw;

    let weights, expected, results;
    weights = [2, 1];
    expected = [.666, .333];
    results = Random.ndist(weights);
    for (let i = 0; i < results.length; i++) {
      expect(results[i]).to.be.closeTo(expected[i], 0.01);
    }
    weights = [7, 1, 2];
    expected = [.7, .1, .2];
    results = Random.ndist(weights);
    for (let i = 0; i < results.length; i++) {
      expect(results[i]).to.be.closeTo(expected[i], 0.01);
    }
  });

  it('should call Random.ndist.temp', function () {
    let weights, expected, results;
    weights = [1.0, 2, 6, -2.5, 0];
    expected = [
      [0, 0, 1, 0, 0],
      [0.0066, 0.018, 0.97, 0.0002, 0.0024],
      [0.064, 0.11, 0.78, 0.011, 0.039],
      [0.19, 0.21, 0.31, 0.13, 0.17],
    ]
    results = [
      Random.ndist(weights, 0.5),
      Random.ndist(weights, 1),
      Random.ndist(weights, 2),
      Random.ndist(weights, 10)
    ];
    for (let i = 0; i < results.length; i++) {
      const result = results[i];
      for (let j = 0; j < result.length; j++) {
        expect(result[j]).to.be.closeTo(expected[i][j], 0.01);
      }
    }
  });

  0 && it('should call createSeed', function () { // no longer used
    let rm, toks;

    rm = new RiMarkov(3);
    rm.addText(sample);
    expect(rm._flatten(rm.createSeed(['I', 'also']))).eq("I also");

    rm = new RiMarkov(4);
    rm.addText(sample);
    expect(rm._flatten(rm.createSeed('I also'))).eq("I also told");
    expect(rm._flatten(rm.createSeed('I also told'))).eq("I also told");
    expect(rm._flatten(rm.createSeed(['I', 'also']))).eq("I also told");
    expect(rm._flatten(rm.createSeed(['I', 'also', 'told']))).eq("I also told");

    rm = new RiMarkov(4);
    rm.addText("The young boy ate it. The young girl gave up.");

    toks = rm.createSeed('The');
    expect(toks.length).eq(rm.n - 1);
    expect(["The young boy", "The young girl"]
      .includes(rm._flatten(toks))).true;

    toks = rm.createSeed('The young');
    expect(toks.length).eq(rm.n - 1);
    expect(["The young boy", "The young girl"]
      .includes(rm._flatten(toks))).true;

    toks = rm.createSeed(['The', 'young']);
    expect(toks.length).eq(rm.n - 1);
    expect(["The young boy", "The young girl"]
      .includes(rm._flatten(toks))).true;

    toks = rm.createSeed('The young boy');
    expect(toks.length).eq(rm.n - 1);
    expect(rm._flatten(toks)).eq('The young boy');

    toks = rm.createSeed('The young girl');
    expect(toks.length).eq(rm.n - 1);
    expect(rm._flatten(toks)).eq('The young girl');
  });

  it('should throw on generate for empty model', function () {
    let rm = new RiMarkov(4, { maxLengthMatch: 6 });
    expect(() => rm.generate(5)).to.throw;
  });

  it('should throw on failed generate', function () {
    let rm = new RiMarkov(4, { maxLengthMatch: 6 });
    rm.addSentences(RiTa.sentences(sample));
    expect(() => rm.generate(5)).to.throw;

    rm = new RiMarkov(4, { maxLengthMatch: 5 });
    rm.addSentences(RiTa.sentences(sample));
    expect(() => rm.generate(5)).to.throw;

    rm = new RiMarkov(4, { maxAttempts: 1 });
    rm.addText("This is a text that is too short.");
    expect(() => rm.generate(5)).to.throw;
  });

  it('should apply custom tokenizers', function () {

    let sents = ['asdfasdf-', 'aqwerqwer+', 'asdfasdf*'];
    let tokenize = (sent) => sent.split("");
    let untokenize = (sents) => sents.join("");

    let rm = new RiMarkov(4, { tokenize, untokenize });
    rm.addSentences(sents);

    expect(rm.size()).eq(sents.reduce((sum, s) => sum + s.length, 0) + (2 * sents.length));
  });

  it('should compute start distrib', function () {

    let sents = ['asdfasdf-', 'asqwerqwer+', 'aqadaqdf*'];
    let tokenize = (sent) => sent.split("");
    let untokenize = (sents) => sents.join("");

    let rm = new RiMarkov(4, { tokenize, untokenize });
    rm.addSentences(sents).build();

    expect(Object.keys(rm.model.suffixes.startIndexDist())).eql(['a']);
  });

  it('RiMarkov.generate.restart', () => {
    let sents = ['asdfasdf-', 'asqwerqwer+', 'aqadaqdf*'];
    let tokenize = (sent) => sent.split("");
    let untokenize = (sents) => sents.join("");

    let rm = new RiMarkov(4, { tokenize, untokenize });
    rm.addSentences(sents).build();

    expect(Object.keys(rm.model.suffixes.startIndexDist())).eql(['a']);

    for (let i = 0; i < 10; i++) {
      let result = rm.generate(2, ['a', 's'], { maxLength: 20 });
      expect(/^as[a-z]+[-+*]$/.test(result)).to.be.true;
    }
  });

  // NOTE: markov-a used n=4 here; C version (n=3) used
  it('should generate non-english sentences', function () {

    let text = '家 安 春 夢 家 安 春 夢 ！ 家 安 春 夢 德 安 春 夢 ？ 家 安 春 夢 安 安 春 夢 。';
    let sentArray = text.match(/[^，；。？！]+[，；。？！]/g);
    let rm = new RiMarkov(3);
    rm.addSentences(sentArray);
    let result = rm.generate({ prompt: ['家'], numSentences: 5 });
    expect(result.length).eq(5);
    expect(/^[^，；。？！]+[，；。？！]$/.test(result[0]), "FAIL: '" + result[0] + "'").is.true;
    result.forEach(r => expect(/^[^，；。？！]+[，；。？！]$/.test(r), "FAIL: '" + r + "'").to.be.true);
  });

  it('should apply custom chinese tokenizers', function () {
    let text = '家安春夢家安春夢！家安春夢德安春夢？家安春夢安安春夢。';
    let sents = text.match(/[^，；。？！]+[，；。？！]/g);

    let tokenize = (sent) => sent.split("");
    let untokenize = (sents) => sents.join("");

    let rm = new RiMarkov(3, { tokenize, untokenize });
    rm.addSentences(sents);
    let result = rm.generate({ prompt: ['家'], numSentences: 5 });

    expect(result.length).eq(5);
    expect(/^[^，；。？！]+[，；。？！]$/.test(result[0]), "FAIL: '" + result[0] + "'").is.true;
    result.forEach(r => expect(/^[^，；。？！]+[，；。？！]$/.test(r), "FAIL: '" + r + "'").to.be.true);
  });

  // NOTE: markov-a used n=4 here; C version (n=5) used
  it('should call generate1', function () {

    let rm;
    rm = new RiMarkov(5);
    rm.addText(sample);

    let sent = rm.generate();
    expect(typeof sent).eq('string');
    expect(sent[0]).eq(sent[0].toUpperCase());
    expect(/[!?.]$/.test(sent)).to.be.true;
  });

  // NOTE: markov-a had extra { disableInputChecks: true }; removed
  it('should call generate2', function () {
    let rm;
    rm = new RiMarkov(4);
    rm.addText(sample);
    let sent = rm.generate({ prompt: ["I"] });
    expect(typeof sent).eq('string');
    expect(sent[0]).eq("I");
    expect(/[!?.]$/.test(sent)).to.be.true;
  });

  it('should call generate3', function () {

    let rm;
    rm = new RiMarkov(4);
    rm.addText(sample);
    let sents = rm.generate({ numSentences: 3 });
    expect(sents.length).eq(3);
    for (let i = 0; i < sents.length; i++) {
      let s = sents[i];
      expect(s[0]).eq(s[0].toUpperCase());
      expect(/[!?.]$/.test(s), "FAIL: bad last char in '" + s + "'").to.be.true;
    }
  });

  it('should call generate4', function () {
    let rm = new RiMarkov(3); // 3 is max for sample, with input checking
    rm.addText(sample);
    // Pass the bounds explicitly: bare generate() defaults maxLength to 999,
    // so asserting <= 35 here was an unfounded guess that failed ~2-4% of runs.
    // (The generator enforces explicit bounds exactly -- see generate.minMaxLength.)
    let s = rm.generate({ minLength: 5, maxLength: 35 });
    expect(s && s[0] === s[0].toUpperCase(), "FAIL: bad first char in '" + s + "'").to.be.true;
    expect(/[!?.]$/.test(s), "FAIL: bad last char in '" + s + "'").to.be.true;
    let num = RiTa.tokenize(s).length;
    expect(num >= 5 && num <= 35, num + ' not within 5-35').to.be.true;
  });

  it('should call generate5', function () { // misc

    let rm = new RiMarkov(3);
    rm.addText(sample2);

    let res = rm.generate({ prompt: ["One", "reason"] });
    //console.log(res);
    expect(res.startsWith("One reason")).to.be.true;
    expect(/^[A-Z][a-z ,I]+[.?!]$/.test(res)).to.be.true;
    expect(/[!?.]$/.test(res)).to.be.true;

    rm = new RiMarkov(3, { trace: 0 });
    rm.addText(sample2);
    res = rm.generate();
    expect(/^[A-Z]/.test(res)).to.be.true;
    expect(/[!?.]$/.test(res)).to.be.true;

    rm = new RiMarkov(3, { trace: 0 });
    rm.addText(sample2);
    res = rm.generate({ maxLength: 20, numSentences: 2 });
    expect(res.length).eq(2);
    res.forEach((r, i) => {
      expect(/^[A-Z]/.test(r)).to.be.true;
      expect(/[!?.]$/.test(r)).to.be.true;
    });
  });

  it('should call generate.minMaxLength', function () {

    let rm = new RiMarkov(3), minLength = 7, maxLength = 20;
    rm.addText(sample);

    let sents = rm.generate(3, { minLength, maxLength, numSentences: 3 });
    expect(sents.length).eq(3);
    for (let i = 0; i < sents.length; i++) {
      let s = sents[i];
      expect(s[0]).eq(s[0].toUpperCase());
      expect(/[!?.]$/.test(s), "FAIL: bad last char in '" + s + "'").to.be.true;
      let num = RiTa.tokenize(s).length;
      expect(num >= minLength && num <= maxLength,
        (num + ' not within ' + minLength + '-' + maxLength)).to.be.true;
    }
  });

  // NOTE: markov-a called this 'should call generate.minMaxLengthDIC'; same body, C name used
  it('should call generate.minMaxLength.combine.with.above', function () {

    let rm = new RiMarkov(4);
    rm.addText(sample);
    for (let i = 0; i < 3; i++) {
      let minLength = (3 + i), maxLength = (10 + i);
      let s = rm.generate({ minLength, maxLength });
      expect(s && s[0] === s[0].toUpperCase(), "FAIL: bad first char in '" + s + "'").to.be.true;
      expect(/[!?.]$/.test(s), "FAIL: bad last char in '" + s + "'").to.be.true;
      let num = RiTa.tokenize(s).length;
      expect(num >= minLength && num <= maxLength,
        (num + ' not within ' + minLength + '-' + maxLength)).to.be.true;
    }
  });

  it('should call generate.prompt', function () {

    let rm = new RiMarkov(4);
    let start = ['One'];
    rm.addText(sample);
    let s = rm.generate({ prompt: start });
    expect(s.startsWith(start)).to.be.true;

    start = ['Achieving'];
    let res = rm.generate({ prompt: start });
    expect(typeof res).eq('string');
    expect(res.startsWith(start)).to.be.true;

    start = ['I'];
    let arr = rm.generate({ prompt: start, numSentences: 2 });
    expect(Array.isArray(arr)).to.be.true;
    expect(arr.length).eq(2);
    expect(arr[0].startsWith(start)).to.be.true;

    // should throw when sentence start is not found
    start = ["Not-exist"];
    expect(function () { rm.generate({ prompt: start }) }).to.throw();
    expect(function () { rm.generate({ prompt: start, numSentences: 1 }) }).to.throw();
    expect(function () { rm.generate({ prompt: start, numSentences: 2 }) }).to.throw();

    start = ["I and she"];
    expect(function () { rm.generate({ prompt: start, numSentences: 2 }) }).to.throw();
    // if startToken is empty string, equal to not have start token
    start = [""];
    expect(rm.generate({ prompt: start, numSentences: 2 }).length).eq(2);
    // if startToken is just space, throw
    start = [" "];
    expect(function () { rm.generate({ prompt: start, numSentences: 2 }) }).to.throw();
  });

  it('should call generate.promptArray', function () {

    let rm = new RiMarkov(4);
    let start = ['One'];
    rm.addText(sample);
    for (let i = 0; i < 5; i++) {
      let s = rm.generate({ prompt: start });
      expect(s.startsWith(start)).to.be.true;
    }

    start = ['Achieving'];
    for (let i = 0; i < 5; i++) {
      let res = rm.generate({ prompt: start });
      expect(typeof res).eq('string');
      expect(res.startsWith(start)).to.be.true;
    }

    start = ['I'];
    for (let i = 0; i < 5; i++) {
      let arr = rm.generate(2, { prompt: start, numSentences: 2 });
      expect(arr.length).eq(2);
      expect(arr[0].startsWith(start)).to.be.true;
    }

    rm = new RiMarkov(4);
    rm.addText(sample);
    start = ['One', 'reason'];
    for (let i = 0; i < 1; i++) {
      let s = rm.generate({ prompt: start });
      expect(s.startsWith(start.join(' '))).to.be.true;
    }

    start = ['Achieving', 'personal'];
    for (let i = 0; i < 5; i++) {
      let res = rm.generate({ prompt: start });
      expect(typeof res).eq('string');
      expect(res.startsWith(start.join(' '))).to.be.true;
    }

    start = ['I', 'also'];
    for (let i = 0; i < 5; i++) {
      let res = rm.generate({ prompt: start });
      expect(typeof res).eq('string');
      expect(res.startsWith(start.join(' '))).to.be.true;
    }
  });

  it.skip('Should call generate.allowDuplicates', function () {
    let rm = RiTa.markov(3, { text: sample3 });
    let res;
    for (let index = 0; index < 10; index++) {
      res = rm.generate({ allowDuplicates: false });
      expect(!sample3.includes(res)).to.be.true;
    }
  });

  it('Should call generate.temp', function () {
    let rm = RiTa.markov(3, { text: sample3 });
    for (let index = 0; index < 1; index++) {
      let res = rm.generate({ temperature: 0 });
      expect(res.length).to.be.greaterThan(0);
      res = rm.generate({ temperature: 1 });
      expect(res.length).to.be.greaterThan(0);
      res = rm.generate({ temperature: 0.1 });
      expect(res.length).to.be.greaterThan(0);
      res = rm.generate({ temperature: 100 });
      expect(res.length).to.be.greaterThan(0);
    }
  });

  it('should generate across sentences', function () {

    let rm = new RiMarkov(3, { trace: 0 });
    rm.addText(sample2);
    expect(rm.n).eq(3);

    let sents = rm.generate({ numSentences: 3 });
    expect(sents.length).eq(3);

    // All within-sentence n-grams must be in the corpus
    for (const sent of sents) {
      let toks = RiTa.tokenize(sent);
      for (let j = 0; j <= toks.length - rm.n; j++) {
        let part = toks.slice(j, j + rm.n);
        let res = RiTa.untokenize(part);
        expect(sample2.includes(res), 'output not found in text: "' + res + '"').to.be.true;
      }
    }

    // Each sentence must start and end at a corpus sentence boundary
    let corpusSents = RiTa.sentences(sample2);
    let validStarts = new Set(corpusSents.map(s => RiTa.tokenize(s)[0]));
    let validEnds = new Set(corpusSents.map(s => { let t = RiTa.tokenize(s); return t[t.length - 1]; }));
    for (const sent of sents) {
      let toks = RiTa.tokenize(sent);
      expect(validStarts.has(toks[0]), 'bad sentence start: "' + toks[0] + '"').to.be.true;
      expect(validEnds.has(toks[toks.length - 1]), 'bad sentence end: "' + toks[toks.length - 1] + '"').to.be.true;
    }
  });

  // NOTE: markov-a had bug: rm.addText(RiTa.sentences(theText)) — array passed to addText; fixed to addText(theText)
  it('should call generate.mlm1', function () {

    let mlms = 8, theText = sample4, rm;

    rm = new RiMarkov(3, { maxLengthMatch: mlms, trace: 0 });
    rm.addText(theText);

    let sents = rm.generate({ numSentences: 2 });
    for (let i = 0; i < sents.length; i++) {
      let sent = sents[i];
      let toks = RiTa.tokenize(sent);
      //console.log(i, sent);

      // All sequences of len=N are (by def.) in the input text
      for (let j = 0; j <= toks.length - rm.n; j++) {
        let part = toks.slice(j, j + rm.n);
        let res = RiTa.untokenize(part);
        expect(theText.indexOf(res) > -1, 'output not found in text: "' + res + '"').to.be.true;
      }

      // All sequences of len=mlms+1 must NOT be in text
      for (let j = 0; j <= toks.length - (mlms + 1); j++) {
        let part = toks.slice(j, j + (mlms + 1));
        let res = RiTa.untokenize(part);
        expect(theText.indexOf(res) < 0, 'Got "' + sent + '"\n\nBut "'
          + res + '" was found in input:\n\n' + sample4 + '\n\n' + rm.input)
          .to.be.true;
      }
    }
  });

  // NOTE: markov-a had rm.generate(3) treating 3 as positional numSentences (wrong); fixed to opts form
  it('should call generate.mlm2', function () {

    let mlms = 9;
    let rm = new RiMarkov(3, { maxLengthMatch: mlms, trace: 0 });
    rm.addText(sample2);
    let sents = rm.generate({ numSentences: 3 });
    for (let i = 0; i < sents.length; i++) {
      let sent = sents[i];
      let toks = RiTa.tokenize(sent);
      for (let j = 0; j <= toks.length - rm.n; j++) {
        let part = toks.slice(j, j + rm.n);
        let res = RiTa.untokenize(part);
        expect(sample2.indexOf(res) > -1, 'output not found in text: "' + res + '"').to.be.true;
      }
      for (let j = 0; j <= toks.length - (mlms + 1); j++) {
        let part = toks.slice(j, j + (mlms + 1));
        let res = RiTa.untokenize(part);
        expect(sample2.indexOf(res) < 0, 'Got "' + sent + '"\n\nBut "'
          + res + '" was found in input:\n\n' + sample + '\n\n' + rm.input).to.be.true;
      }
    }
  });

  // Reproduces annograms issue: tight maxLengthMatch + minLength + numSentences
  it('should call generate with tight maxLengthMatch+minLength (regression: annograms)', function () {
    let rm = new RiMarkov(3, { maxLengthMatch: 6, trace: 0 });
    rm.addText(sample + ' ' + sample4);
    let sents = rm.generate({ numSentences: 4, minLength: 8 });
    expect(sents.length).eq(4);
  });

  it('should call completions', function () {

    let rm = new RiMarkov(4);
    rm.addText((sample));

    let res = rm.completions("people lie is".split(' '));
    expect(res).eql(["to"]);

    res = rm.completions("One reason people lie is".split(' '));
    expect(res).eql(["to"]);

    res = rm.completions("personal power".split(' '));
    expect(res).eql(['.', 'is']);

    res = rm.completions(['to', 'be', 'more']);
    expect(res).eql(['confident']);

    res = rm.completions(["I"]); // testing the sort
    //      console.log(res);

    let expec = ["did", "claimed", "had", "said", "could",
      "wanted", "also", "achieved", "embarrassed"
    ];
    expect(res.sort()).eql(expec.sort());

    res = rm.completions(["XXX"]);
    expect(res).eql([]);

    ///////////////////// ///////////////////// /////////////////////

    rm = new RiMarkov(4);
    rm.addText((sample2));

    res = rm.completions(['I'], ['not']);
    expect(res).eql(["did"]);

    res = rm.completions(['achieve'], ['power']);
    expect(res).eql(["personal"]);

    res = rm.completions(['to', 'achieve'], ['power']);
    expect(res).eql(["personal"]);

    res = rm.completions(['achieve'], ['power']);
    expect(res).eql(["personal"]);

    res = rm.completions(['I', 'did']);
    expect(res).eql(["not", "occasionally"]);

    res = rm.completions(['I', 'did'], ['want']);
    expect(res).eql(["not", "occasionally"]);

    //should throw with bad inputs
    expect(function () {
      rm.completions(['I', 'did', 'not', 'occasionally'], ['want']);
    }).to.throw();

    let tmp = RiTa.SILENT;
    RiTa.SILENT = true;

    // should return undefined if no completions are found
    res = rm.completions(['I', 'non-exist'], ['want']);
    expect(res).eql([]);

    res = rm.completions(['I', 'non-exist'], ['want']);
    expect(res).eql([]);

    RiTa.SILENT = tmp;
  });

  it('should call probabilities', function () {

    let rm = new RiMarkov(3);
    rm.addText((sample));

    let checks = ["reason", "people", "personal", "the", "is", "XXX"];
    let expected = [{
      people: 1.0
    }, {
      lie: 1
    }, {
      power: 1.0
    }, {
      time: 0.5,
      party: 0.5
    }, {
      to: 0.3333333333333333,
      '.': 0.3333333333333333,
      helpful: 0.3333333333333333
    }, {}];

    for (let i = 0; i < checks.length; i++) {
      let res = rm.probabilities([checks[i]]);
      expect(res).eql(expected[i]);
    }
  });

  it('should call probabilities.array', function () {

    let rm = new RiMarkov(4);
    rm.addText(sample2);

    let res = rm.probabilities(["the"]);
    let expec = {
      time: 0.5,
      party: 0.5
    };
    expect(res).eql(expec);

    res = rm.probabilities("people lie is".split(" "));
    expec = {
      to: 1.0
    };
    expect(res).eql(expec);

    res = rm.probabilities(["is"]);
    expec = {
      to: 0.3333333333333333,
      '.': 0.3333333333333333,
      helpful: 0.3333333333333333
    };
    expect(res).eql(expec);

    res = rm.probabilities("personal power".split(' '));
    expec = {
      '.': 0.5,
      is: 0.5
    };
    expect(res).eql(expec);

    res = rm.probabilities(['to', 'be', 'more']);
    expec = {
      confident: 1.0
    };
    expect(res).eql(expec);

    res = rm.probabilities(["XXX"]);
    expec = {};
    expect(res).eql(expec);

    res = rm.probabilities(["personal", "XXX"]);
    expec = {};
    expect(res).eql(expec);

    res = rm.probabilities(['I', 'did']);
    expec = {
      "not": 0.6666666666666666,
      "occasionally": 0.3333333333333333
    };
    expect(res).eql(expec);
  });

  it.skip('should call probability', function () {

    let text, rm;
    text = 'the dog ate the boy the';
    rm = new RiMarkov(3);
    rm.addText(text);
    expect(rm.probability(["the"])).eq(.5);
    expect(rm.probability(["dog"])).eq(1 / 6);
    expect(rm.probability(["cat"])).eq(0);

    text = 'the dog ate the boy that the dog found.';
    rm = new RiMarkov(3);
    rm.addText(text);

    expect(rm.probability(["the"])).eq(.3);
    expect(rm.probability(["dog"])).eq(.2);
    expect(rm.probability(["cat"])).eq(0);

    rm = new RiMarkov(3);
    rm.addText(sample);
    expect(rm.probability(["power"])).eq(0.017045454545454544);

    //bad inputs
    expect(rm.probability(["Non-exist"])).eq(0);
  });

  it.skip('should call probability.array', function () {

    let rm = new RiMarkov(3);
    rm.addText(sample);

    let check = 'personal power is'.split(' ');
    expect(rm.probability(check)).eq(1 / 3);

    check = 'personal powXer is'.split(' ');
    expect(rm.probability(check)).eq(0);

    check = 'someone who pretends'.split(' ');
    expect(rm.probability(check)).eq(1 / 2);

    expect(rm.probability([])).eq(0);
  });

  it('should call addText', function () {
    let rm = new RiMarkov(4);
    let sents = RiTa.sentences(sample);
    let count = 0;
    for (let i = 0; i < sents.length; i++) {
      let words = RiTa.tokenize(sents[i]);
      count += words.length + 2; // add 2 for start and end tokens
    }
    rm.addSentences(sents);

    expect(rm.size()).eq(count);
  });

  it('should call size', function () {

    let rm = new RiMarkov(4);
    expect(rm.size()).eq(0);

    let tokens = RiTa.tokenize(sample);
    let sents = RiTa.sentences(sample);
    rm = new RiMarkov(3);
    rm.addText(sample);
    expect(rm.size()).eq(tokens.length + (2 * sents.length)); // add 2 for start and end tokens

    let rm2 = new RiMarkov(4);
    rm2 = new RiMarkov(3);
    rm2.addSentences(sents);
    expect(rm.size()).eq(rm2.size());
  });

  // NOTE: markov-a used n=4 and positional generate arg; C version (n=3) used
  it('should serialize and deserialize', function () {

    let rm, copy;
    rm = new RiMarkov(3);
    let json = rm.toJSON();
    copy = RiMarkov.fromJSON(json);
    markovEquals(rm, copy);

    rm = new RiMarkov(3);
    rm.addText('I ate the dog.');
    copy = RiMarkov.fromJSON(rm.toJSON());
    markovEquals(rm, copy);

    rm = new RiMarkov(3);
    rm.addText('I ate the dog.');
    copy = RiMarkov.fromJSON(rm.toJSON());
    markovEquals(rm, copy);
    expect(copy.generate()).eql(rm.generate());
  });

  0 && it('Should output log with trace option', function () {
    let rm = new RiMarkov(4, { maxAttempts: 2, trace: true });
    rm.addText("This is a text that is too short.");
    expect(() => rm.generate(5)).to.throw;

    rm = new RiMarkov(3, { trace: true, maxLengthMatch: 10 });
    rm.addText(sample3);
    expect(rm.generate(2).length).eq(2);
  });

  /////////////////////////// helpers ////////////////////////////

  function distribution(res, dump) {
    let dist = {};
    for (var i = 0; i < res.length; i++) {
      if (!dist[res[i]]) dist[res[i]] = 0;
      dist[res[i]]++;
    }
    let keys = Object.keys(dist);
    keys.forEach(k => {
      dist[k] = dist[k] / res.length
      dump && console.log(k, dist[k]);
    });
    dump && console.log();
    return dist;
  }

  function markovEquals(rm, copy) {
    expect(rm.n).eql(copy.n);
    expect(rm.size()).eql(copy.size());
  }

  it('RiMarkov.constructor', () => {

    let lm1 = new BackoffModel();
    expect(lm1).to.be.an.instanceof(BackoffModel);
    expect(typeof lm1 === 'object').true;
    expect(lm1.size()).to.eq(0);

    // input: array of tokens with separator
    lm1 = new BackoffModel(exampleTokens);
    expect(lm1.suffixes).to.be.an.instanceof(SuffixArray);
    expect(lm1.size()).to.eq(21);

    // input: raw string (tokenized by RiTa)
    let lm2 = new BackoffModel(exampleStr);
    expect(lm2.suffixes).to.be.an.instanceof(SuffixArray);
    expect(lm2.size()).to.eq(21);

    expect(() => new BackoffModel(123)).to.throw();
    expect(() => new BackoffModel([RiTa.sentences(exampleStr)])).to.throw(); // 2d
  });

  it('should throw on generate for empty model', function () {
    let rm = new BackoffModel({ maxLengthMatch: 6 });
    expect(() => rm.generate(5)).to.throw;
  });

  it('should throw on failed generate', function () {
    let rm = new BackoffModel({ maxLengthMatch: 6 });
    rm.addText(sample);
    expect(() => rm.generate(5)).to.throw;

    rm = new BackoffModel({ maxLengthMatch: 5 });
    rm.addSentences(RiTa.sentences(sample));
    expect(() => rm.generate(5)).to.throw;

    rm = new BackoffModel({ maxAttempts: 1 });
    rm.addText("This is a text that is too short.");
    expect(() => rm.generate(5)).to.throw;
  });

  it('should call addText with string', function () {
    let rm = new BackoffModel({ maxLengthMatch: 6 });
    rm.addText(sample).build();
    expect(rm.size()).to.be.greaterThan(0);
    expect(rm).to.eql(new BackoffModel(sample, { maxLengthMatch: 6 }));
  });

  it('should call addText with token array', function () {
    let rm = new BackoffModel({ maxLengthMatch: 6 });
    rm.addTokens(exampleTokens).build();
    expect(rm.size()).to.be.greaterThan(0);
    expect(rm).to.eql(new BackoffModel(exampleTokens, { maxLengthMatch: 6 }));
  });

  it('should call addSentences with sentence array', function () {
    let rm = new BackoffModel({ maxLengthMatch: 6 });
    rm.addSentences(RiTa.sentences(sample)).build();
    expect(rm.size()).to.be.greaterThan(0);
    expect(rm).to.eql(new BackoffModel(sample, { maxLengthMatch: 6 }));
  });

  it('should split on custom tokenizers', function () {

    let start = SuffixArray.SEQ_START_TOKEN;
    let end = SuffixArray.SEQ_END_TOKEN;
    let sents = ['asdfasdf-', 'aqwerqwer+', 'asdfasdf*'];
    let chars = sents.reduce((acc, curr) => acc + curr.length, sents.length * 2);

    let tokenize = (sent) => sent.split("");
    let untokenize = (sents) => sents.join("");

    let rm = new BackoffModel({ tokenize, untokenize });
    rm.addSentences(sents).build();

    expect(rm.size()).eq(chars);
    let toks = sents.map(s => [start, ...s.split(""), end]).flat()
    expect(rm.size()).eq(new BackoffModel(toks).size());
  });

  it('RiMarkov.constructor', () => {
    // text form (implicit n)
    const rm = new RiMarkov(exampleStr);
    expect(rm).to.be.an.instanceof(RiMarkov);
    expect(rm.model).to.be.an.instanceof(BackoffModel);
    expect(rm.size()).to.be.above(0);

    // legacy form: new RiMarkov(n, { text })
    const rm2 = new RiMarkov(3, { text: exampleStr });
    expect(rm2.n).to.equal(3);
    expect(rm2.model.size()).to.equal(rm.model.size());

    // opts-only form: new RiMarkov({ text })
    const rm3 = new RiMarkov({ text: exampleStr });
    expect(rm3.model.size()).to.equal(rm.model.size());

    // n stored via opts.n
    const rm4 = new RiMarkov(exampleStr, { n: 4 });
    expect(rm4.n).to.equal(4);
  });

  it('RiMarkov.addText / addSentences / addTokens / size', () => {
    // addText: builds same model as constructor string form
    const rm1 = new RiMarkov(exampleStr);
    const rm2 = new RiMarkov();
    rm2.addText(exampleStr);
    expect(rm2.size()).to.equal(rm1.size());

    // addSentences
    const rm3 = new RiMarkov();
    rm3.addSentences(RiTa.sentences(exampleStr));
    expect(rm3.size()).to.equal(rm1.size());

    // addTokens
    const rm4 = new RiMarkov();
    rm4.addTokens(exampleTokens);
    expect(rm4.size()).to.equal(rm1.size());

    // size() reflects token count
    expect(rm1.size()).to.equal(21);
    expect(new RiMarkov().size()).to.equal(0);

    // addText throws on non-string
    expect(() => rm2.addText(123)).to.throw();
  });

  it('RiMarkov.toJSON / fromJSON', () => {
    const rm = new RiMarkov(exampleStr);
    const json = rm.toJSON();
    expect(json).to.be.a('string');

    // fromJSON returns a proper RiMarkov with a BackoffModel (not a plain Object.assign copy)
    const copy = RiMarkov.fromJSON(json);
    expect(copy).to.be.an.instanceof(RiMarkov);
    expect(copy.size()).to.equal(rm.size());

    // static fromJSON
    const copy2 = RiMarkov.fromJSON(json);
    expect(copy2).to.be.an.instanceof(RiMarkov);
    expect(copy2.size()).to.equal(rm.size());

    // completions survive round-trip
    const orig = rm.completions(['The', 'brown']);
    const after = copy2.completions(['The', 'brown']);
    expect(after).to.deep.equal(orig);
  });

  it('RiMarkov.generate (numSentences)', () => {
    const rm = new RiMarkov(sample);
    rm.n = 3;
    const opts = { minTokens: 3, maxTokens: 20 };

    // numSentences=1 returns a single string (same as default)
    const norm = rm.generate(3, ['I'], opts);
    expect(norm).to.be.a('string').and.have.length.above(0);

    // numSentences=1 returns a single string (same as default)
    const one = rm.generate(3, ['I'], { ...opts, numSentences: 1 });
    expect(one).to.be.a('string').and.have.length.above(0);

    // numSentences=2 returns an array of 2 strings
    const two = rm.generate(3, ['I'], { ...opts, numSentences: 2 });
    expect(two).to.be.an('array').with.lengthOf(2);
    two.forEach(s => expect(s).to.be.a('string').and.have.length.above(0));

    // numSentences=3 returns an array of 3 strings
    const three = rm.generate(3, ['I'], { numSentences: 3 });
    expect(three).to.be.an('array').with.lengthOf(3);
  });

  it('RiMarkov.completions (single array)', () => {
    const rm = new RiMarkov(exampleStr);

    // next tokens after ['The', 'brown'] are 'fox' and 'dog'
    const nexts = rm.completions(['The', 'brown']);
    expect(nexts).to.be.an('array');
    expect(nexts).to.include('fox');
    expect(nexts).to.include('dog');
    // no special tokens in result by default
    nexts.forEach(t => expect(t).to.not.match(/^<.*>$/));
    expect(nexts.length).to.equal(2);

    expect(rm.completions(['brown', 'fox'])).to.deep.equal(['jumps']);

    // unknown context returns empty array
    expect(rm.completions(['never', 'seen'])).to.deep.equal([]);

    // allowSpecial: special tokens appear when at sentence end
    const nextsSpecial = rm.completions(['dog', '.'], undefined, { allowSpecial: true });
    expect(nextsSpecial).to.include(SuffixArray.SEQ_END_TOKEN);

    // allowSpecial: false (default) strips them
    rm.completions(['dog', '.']).forEach(t => expect(t).to.not.match(/^<.*>$/));

    // exact-value checks with sample corpus
    const rm2 = new RiMarkov(sample);
    rm2.n = 4;
    expect(rm2.completions('people lie is'.split(' '))).to.deep.equal(['to']);
    expect(rm2.completions('One reason people lie is'.split(' '))).to.deep.equal(['to']);
    expect(rm2.completions('personal power'.split(' '))).to.deep.equal(['.', 'is']);
    expect(rm2.completions(['to', 'be', 'more'])).to.deep.equal(['confident']);
    const iCompletions = rm2.completions(['I']);
    ['did', 'claimed', 'had', 'said', 'could', 'wanted', 'also', 'achieved', 'embarrassed']
      .forEach(w => expect(iCompletions).to.include(w));
    expect(rm2.completions(['XXX'])).to.deep.equal([]);
  });

  it('RiMarkov.completions (two arrays)', () => {
    const rm = new RiMarkov(exampleStr);
    rm.n = 4;

    // find w s.t. ['The', w, 'fox'] exists: 'brown' should be the answer
    const middle = rm.completions(['The'], ['fox']);
    expect(middle).to.be.an('array');
    expect(middle).to.include('brown');
    // no special tokens by default
    middle.forEach(t => expect(t).to.not.match(/^<.*>$/));

    // allowSpecial: include boundary tokens in results
    expect(rm.completions(['The'], ['fox'], { allowSpecial: true })).to.include('brown');

    // exact-value checks with sample2 corpus
    const rm2 = new RiMarkov(sample2);
    rm2.n = 4;
    expect(rm2.completions(['I'], ['not'])).to.deep.equal(['did']);
    expect(rm2.completions(['achieve'], ['power'])).to.deep.equal(['personal']);
    expect(rm2.completions(['to', 'achieve'], ['power'])).to.deep.equal(['personal']);
    expect(rm2.completions(['I', 'did'])).to.deep.equal(['not', 'occasionally']);
    expect(rm2.completions(['I', 'did'], ['want'])).to.deep.equal(['not', 'occasionally']);

    // throws when pre+post length >= n
    expect(() => rm2.completions(['I', 'did', 'not', 'occasionally'], ['want'])).to.throw();
  });

  it('RiMarkov.generate.restart', () => {
    let sents = ['asdfasdf-', 'asqwerqwer+', 'aqadaqdf*'];
    let tokenize = (sent) => sent.split("");
    let untokenize = (sents) => sents.join("");

    let rm = new RiMarkov(4, { tokenize, untokenize });
    rm.addSentences(sents).build();

    expect(Object.keys(rm.model.suffixes.startIndexDist())).eql(['a']);

    for (let i = 0; i < 10; i++) {
      let result = rm.generate(2, ['a', 's'], { maxTokens: 20 });
      expect(/^as[a-z]+[-+*]$/.test(result)).to.be.true;
    }
  });

  it('RiMarkov.generate', () => {
    const rm = new RiMarkov(exampleStr);
    rm.n = 3;

    // returns a non-empty string
    const text = rm.generate(3, ['The', 'brown'], { minTokens: 2, maxTokens: 10 });
    expect(text).to.be.a('string').and.have.length.above(0);

    // starts with the prompt words
    expect(text.startsWith('The brown')).to.be.true;

    // two-arg form: generate(prompt, opts) — n from constructor
    rm.n = 3;
    const text2 = rm.generate(['The', 'brown'], { minTokens: 2, maxTokens: 10 });
    expect(text2).to.be.a('string').and.have.length.above(0);
    expect(text2.startsWith('The brown')).to.be.true;

    // throws when prompt is not an array
    expect(() => rm.generate(3, 'The brown', {})).to.throw();

    // throws when n is not set
    const rm2 = new RiMarkov(exampleStr);
    expect(() => rm2.generate(undefined, ['The'], {})).to.throw();
  });

  it.skip('RiMarkov.probability', () => {
    const rm = new RiMarkov(exampleStr);

    expect(rm.probability(['xyz'])).to.equal(0);
    expect(rm.probability(['the'])).to.be.above(0).and.be.at.most(1);
    expect(rm.probability(['the'])).to.be.above(rm.probability(['fox']));

    const pSeq1 = rm.probability(['The', 'brown']);
    const pSeq2 = rm.probability(['The', 'brown', 'fox']);
    expect(pSeq1).to.be.above(0);
    expect(pSeq2).to.be.above(0);
    expect(pSeq1).to.be.above(pSeq2);

    expect(rm.probability(['brown', 'fox', 'lazy'])).to.equal(0);
    expect(rm.probability(['The', 'brown'], 'fox')).to.be.closeTo(0.5, 0.01);
    expect(rm.probability(['The', 'brown'], 'dog')).to.be.closeTo(0.5, 0.01);
    expect(rm.probability(['The', 'brown'], ['fox', 'jumps'])).to.be.above(0).and.be.at.most(1);
    expect(rm.probability(['The', 'brown'], 'xyz')).to.equal(0);
    expect(rm.probability([], ['The'])).to.be.above(0);
    expect(() => rm.probability('not-an-array', 'token')).to.throw();

    const rm2 = new RiMarkov('the dog ate the boy the');
    expect(rm2.probability('the')).to.be.closeTo(3 / rm2.model.suffixes.length, 1e-9);
    expect(rm2.probability('dog')).to.be.closeTo(1 / rm2.model.suffixes.length, 1e-9);
    expect(rm2.probability('cat')).to.equal(0);

    const rm3 = new RiMarkov('the dog ate the boy that the dog found.');
    expect(rm3.probability('the')).to.be.closeTo(3 / rm3.model.suffixes.length, 1e-9);
    expect(rm3.probability('dog')).to.be.closeTo(2 / rm3.model.suffixes.length, 1e-9);
    expect(rm3.probability('cat')).to.equal(0);

    const rm4 = new RiMarkov(sample);
    expect(rm4.probability('Non-exist')).to.equal(0);
    expect(rm4.probability([])).to.equal(0);
    expect(rm4.probability('personal power is'.split(' '))).to.be.above(0);
    expect(rm4.probability('personal powXer is'.split(' '))).to.equal(0);
  });

  it('RiMarkov.probabilities', () => {
    const rm = new RiMarkov(exampleStr);

    const dist = rm.probabilities(['The', 'brown']);
    expect(dist).to.have.property('fox');
    expect(dist).to.have.property('dog');
    Object.keys(dist).forEach(t => expect(t).to.not.match(/^<.*>$/));
    expect(Object.values(dist).reduce((s, p) => s + p, 0)).to.be.closeTo(1, 1e-9);
    Object.values(dist).forEach(p => expect(p).to.be.above(0));

    const dist2 = rm.probabilities(['brown', 'fox']);
    expect(Object.keys(dist2)).to.deep.equal(['jumps']);
    expect(dist2['jumps']).to.be.closeTo(1, 1e-9);

    expect(rm.probabilities(['never', 'seen'])).to.deep.equal({});

    expect(rm.probabilities(['dog', '.'], { allowSpecial: true }))
      .to.have.property(SuffixArray.SEQ_END_TOKEN);

    Object.keys(rm.probabilities(['dog', '.']))
      .forEach(t => expect(t).to.not.match(/^<.*>$/));

    const startDist = rm.probabilities();
    expect(Object.keys(startDist).length).to.be.above(0);
    Object.keys(startDist).forEach(t => expect(t).to.not.match(/^<.*>$/));

    expect(() => rm.probabilities('not-an-array')).to.throw();

    const rm2 = new RiMarkov(sample);
    expect(rm2.probabilities(['reason'])).to.deep.equal({ people: 1.0 });
    expect(rm2.probabilities(['people'])).to.deep.equal({ lie: 1 });
    expect(rm2.probabilities(['personal'])).to.deep.equal({ power: 1.0 });
    const theProbs = rm2.probabilities(['the']);
    expect(Object.keys(theProbs).sort()).to.deep.equal(['party', 'time']);
    expect(theProbs['time'] + theProbs['party']).to.be.closeTo(1, 1e-9);
    const isProbs = rm2.probabilities(['is']);
    expect(Object.keys(isProbs).sort()).to.deep.equal(['.', 'helpful', 'to']);
    expect(Object.values(isProbs).reduce((s, p) => s + p, 0)).to.be.closeTo(1, 1e-9);
    expect(rm2.probabilities(['XXX'])).to.deep.equal({});

    const rm3 = new RiMarkov(sample2);
    expect(rm3.probabilities('people lie is'.split(' '))).to.deep.equal({ to: 1.0 });
    const pp = rm3.probabilities('personal power'.split(' '));
    expect(Object.keys(pp).sort()).to.deep.equal(['.', 'is']);
    expect(pp['.'] + pp['is']).to.be.closeTo(1, 1e-9);
    expect(rm3.probabilities(['to', 'be', 'more'])).to.deep.equal({ confident: 1.0 });
    expect(rm3.probabilities(['XXX'])).to.deep.equal({});
    expect(rm3.probabilities(['personal', 'XXX'])).to.deep.equal({});
    const didProbs = rm3.probabilities(['I', 'did']);
    expect(Object.keys(didProbs).sort()).to.deep.equal(['not', 'occasionally']);
    expect(didProbs['not'] + didProbs['occasionally']).to.be.closeTo(1, 1e-9);
    expect(didProbs['not']).to.be.above(didProbs['occasionally']);
  });

  it('RiMarkov.constructor (sentences option)', () => {
    const sents = RiTa.sentences(exampleStr);
    const rm = new RiMarkov({ sentences: sents });
    expect(rm.size()).to.be.above(0);

    const rm2 = new RiMarkov();
    rm2.addSentences(sents);
    expect(rm.size()).to.equal(rm2.size());
  });

  it('RiMarkov.generate (opts-only form)', () => {
    const rm = new RiMarkov(sample);

    const result = rm.generate({ n: 3, prompt: ['I'], minTokens: 3, maxTokens: 20 });
    expect(result).to.be.a('string').and.have.length.above(0);

    const rm2 = new RiMarkov(exampleStr);
    const result2 = rm2.generate({ n: 3, prompt: ['The', 'brown'], minTokens: 2, maxTokens: 10 });
    expect(result2).to.be.a('string').and.have.length.above(0);
    expect(result2.startsWith('The brown')).to.be.true;

    const rm3 = new RiMarkov(exampleStr);
    expect(() => rm3.generate({ prompt: ['The'] })).to.throw();
  });

  it('RiMarkov.toString', () => {
    const rm = new RiMarkov(exampleStr);
    const str = rm.toString();
    expect(str).to.be.a('string').and.have.length.above(0);
  });

  it('RiMarkov.stream', () => {
    const rm = new RiMarkov(exampleStr);
    rm.n = 3;

    const gen = rm.stream(3, ['The', 'brown'], { maxTokens: 10 });
    expect(typeof gen[Symbol.iterator]).to.equal('function');

    const tokens = [...rm.stream(3, ['The', 'brown'], { maxTokens: 10 })];
    expect(tokens.length).to.be.above(0);
    tokens.forEach(t => expect(t).to.be.a('string'));

    const specials = new Set([SuffixArray.SEQ_START_TOKEN, SuffixArray.SEQ_END_TOKEN]);
    tokens.forEach(t => expect(specials.has(t)).to.be.false);

    const capped = [...rm.stream(3, ['The'], { maxTokens: 3 })];
    expect(capped.length).to.be.at.most(3);

    const tokens2 = [...rm.stream(['The', 'brown'], { maxTokens: 10 })];
    expect(tokens2.length).to.be.above(0);

    const tokens3 = [...rm.stream({ n: 3, prompt: ['The', 'brown'], maxTokens: 10 })];
    expect(tokens3.length).to.be.above(0);

    const toStop = [...rm.stream(3, ['The', 'brown'], { maxTokens: 20, generateUntil: '.' })];
    expect(toStop[toStop.length - 1]).to.equal('.');

    const toPred = [...rm.stream(3, ['The', 'brown'], {
      maxTokens: 20,
      generateUntil: (t) => t === '.'
    })];
    expect(toPred[toPred.length - 1]).to.equal('.');

    expect(() => [...rm.stream(3, 'not an array', {})]).to.throw();

    const rm2 = new RiMarkov(exampleStr);
    expect(() => [...rm2.stream({ prompt: ['The'] })]).to.throw();
  });

  it('should be reproducible with RiTa.randomSeed', function () {

    // Regression: Markov sampling used Math.random(), bypassing the seeded
    // Mersenne Twister, so RiTa.randomSeed() had no effect on generate()
    const text = 'The cat sat on the mat. The dog ran in the park. A bird flew '
      + 'over the house. The fish swam in the pond. The horse ran through the '
      + 'field. The mouse hid in the wall. The cat chased the mouse. The dog '
      + 'chased the cat. The bird ate the fish.';

    const gen = (seed) => {
      RiTa.randomSeed(seed);
      const rm = new RiMarkov(2);
      rm.addText(text);
      return rm.generate({ numSentences: 3, maxLength: 12 });
    };

    try {
      const one = gen(1), two = gen(1), other = gen(7);
      expect(one).to.eql(two);              // same seed => same output
      expect(one).to.not.eql(other);        // different seed => different output
    } finally {
      RiTa.randomSeed(Date.now());          // don't leak a fixed seed into other tests
    }
  });

  it('should honor maxBacktracks as a constructor option', function () {

    // Regression: RiMarkov copies instance defaults from generationDefaults,
    // so maxBacktracks was silently dropped when it was missing from that map
    const rm = new RiMarkov(3, { maxBacktracks: 50 });
    expect(rm.opts.maxBacktracks).to.equal(50);

    // and it must be a valid option key (resolveOpts rejects unknown keys)
    expect(() => BackoffModel.resolveOpts(3, { maxBacktracks: 50 })).to.not.throw();
    expect(BackoffModel.resolveOpts(3, { maxBacktracks: 50 }).maxBacktracks).to.equal(50);
  });

  it('should build with verbose enabled', function () {

    // Regression: build() referenced an undeclared `ts`, so build({verbose:true})
    // threw ReferenceError. Nothing exercised the verbose path before this.
    const rm = new RiMarkov(2);
    rm.addText("The quick brown fox jumped over the lazy dog. The lazy dog slept. The dog ran.");

    const log = console.log;
    try {
      console.log = () => { };   // keep the timing line out of the test output
      expect(() => rm.model.build({ verbose: true })).to.not.throw();
    } finally {
      console.log = log;
    }
  });
});
