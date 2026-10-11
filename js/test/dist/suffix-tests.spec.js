import { assert, expect } from "chai";
import { RiTa } from "./index.js";
const { SuffixArray } = RiTa;
const SEQ_START_TOKEN = SuffixArray.SEQ_START_TOKEN;
const SEQ_END_TOKEN = SuffixArray.SEQ_END_TOKEN;
let exampleTokens = [
  SEQ_START_TOKEN,
  "The",
  "brown",
  "fox",
  "jumps",
  "over",
  "the",
  "lazy",
  "dog",
  ".",
  SEQ_END_TOKEN,
  SEQ_START_TOKEN,
  "The",
  "brown",
  "dog",
  "wept",
  "over",
  "the",
  "treat",
  ".",
  SEQ_END_TOKEN
];
let longerTokens = [
  "<s>",
  "Little",
  "humps",
  "of",
  "sand",
  ",",
  "of",
  "water",
  "mixed",
  "with",
  "sand",
  "so",
  "thoroughly",
  "that",
  "granules",
  "of",
  "this",
  "new",
  "matter",
  "have",
  "the",
  "texture",
  "of",
  "firn",
  ",",
  "stick",
  "out",
  "smartly",
  "where",
  "the",
  "surf",
  "used",
  "to",
  "pound",
  "the",
  "shore",
  ",",
  "and",
  "beyond",
  "that",
  "a",
  "great",
  "frozen",
  "slab",
  "opens",
  "out",
  "like",
  "a",
  "cold",
  "hand",
  ",",
  "lined",
  "with",
  "the",
  "details",
  "of",
  "waves",
  ",",
  "crests",
  ",",
  "white",
  "horses",
  "of",
  "snow",
  ",",
  "a",
  "fleeting",
  "image",
  "of",
  "air",
  "in",
  "a",
  "furtive",
  "coupling",
  "of",
  "wind",
  "and",
  "spray",
  ",",
  "an",
  "alphabet",
  "of",
  "meanings",
  "receding",
  "to",
  "the",
  "horizon",
  ",",
  "repeated",
  "to",
  "infinity",
  ",",
  "an",
  "infinity",
  "of",
  "vibrations",
  "and",
  "still-born",
  "interferences",
  ".",
  "</s>",
  "<s>",
  "But",
  "it\u2019s",
  "a",
  "splendid",
  "funeral",
  ";",
  "all",
  "around",
  ",",
  "in",
  "the",
  "strong",
  "wind",
  ",",
  "thousands",
  "of",
  "snowflakes",
  "are",
  "crowding",
  ",",
  "each",
  "one",
  "a",
  "crystal",
  "star",
  "with",
  "its",
  "own",
  "particular",
  "design",
  ".",
  "</s>",
  "<s>",
  "The",
  "path",
  "was",
  "like",
  "those",
  "that",
  "wind",
  "from",
  "the",
  "crest",
  "of",
  "the",
  "Downs",
  "south",
  "to",
  "the",
  "sea",
  ".",
  "</s>",
  "<s>",
  "That",
  "seems",
  "to",
  "even",
  "things",
  ",",
  "for",
  "those",
  "who",
  "regard",
  "it",
  "as",
  "a",
  "balance",
  ",",
  "or",
  "think",
  "the",
  "wind",
  "blows",
  "one",
  "way",
  ".",
  "</s>",
  "<s>",
  "And",
  "they",
  "hadn\u2019t",
  "invented",
  "wind",
  "and",
  "rain",
  ",",
  "so",
  "the",
  "footprints",
  "stayed",
  "where",
  "they",
  "were",
  ".",
  "</s>",
  "<s>",
  "They",
  "hadn\u2019t",
  "invented",
  "wind",
  "and",
  "rain",
  ",",
  "remember",
  ".",
  "</s>",
  "<s>",
  "In",
  "winter",
  ",",
  "when",
  "the",
  "wind",
  "blows",
  "hard",
  "and",
  "there\u2019s",
  "no",
  "one",
  "about",
  "in",
  "these",
  "out-of-the-way",
  "places",
  ",",
  "I",
  "like",
  "to",
  "hear",
  "the",
  "flag",
  "crack",
  "like",
  "a",
  "whip",
  "with",
  "the",
  "fish",
  "swimming",
  "in",
  "the",
  "sky",
  "as",
  "if",
  "it",
  "were",
  "alive",
  ".",
  "</s>",
  "<s>",
  "But",
  "in",
  "high",
  "winter",
  ",",
  "the",
  "flag",
  "thrashes",
  "up",
  "there",
  "with",
  "its",
  "fish",
  "in",
  "the",
  "air",
  ",",
  "trembling",
  "with",
  "cold",
  ",",
  "wind",
  "and",
  "sky",
  ".",
  "</s>",
  "<s>",
  "I",
  "see",
  "the",
  "iron",
  "fences",
  "and",
  "the",
  "shallow",
  "ditches",
  "of",
  "the",
  "countryside",
  "the",
  "mild",
  "wind",
  "has",
  "travelled",
  "over",
  ".",
  "</s>",
  "<s>",
  "I",
  "cannot",
  "join",
  "together",
  "the",
  "mild",
  "wind",
  "and",
  "the",
  "shallow",
  "ditches",
  ",",
  "I",
  "cannot",
  "lay",
  "the",
  "light",
  "across",
  "the",
  "world",
  "and",
  "then",
  "watch",
  "it",
  "slide",
  "away",
  ".",
  "</s>",
  "<s>",
  "In",
  "the",
  "mirror",
  ",",
  "the",
  "wind",
  "from",
  "the",
  "south",
  "spins",
  ",",
  "carrying",
  "leaves",
  "and",
  "feathers",
  ".",
  "</s>",
  "<s>",
  "In",
  "the",
  "wind",
  "from",
  "the",
  "desert",
  "the",
  "needles",
  "bend",
  "and",
  "my",
  "hour",
  "is",
  "past",
  ".",
  "</s>",
  "<s>",
  "Everywhere",
  "the",
  "light",
  "wind",
  "blows",
  ",",
  "the",
  "breeze",
  "that",
  "provokes",
  "the",
  "immense",
  "whiplash",
  "each",
  "time",
  "it",
  "unwinds",
  "in",
  "the",
  "air",
  ".",
  "</s>",
  "<s>",
  "The",
  "light",
  "wind",
  "rises",
  "from",
  "the",
  "meadows",
  "of",
  "the",
  "past",
  ",",
  "and",
  "hurries",
  "closer",
  "to",
  "our",
  "time",
  ".",
  "</s>",
  "<s>",
  "A",
  "great",
  "wind",
  "is",
  "blowing",
  "from",
  "the",
  "centre",
  ".",
  "</s>",
  "<s>",
  "Hearths",
  "that",
  "were",
  "red",
  "yesterday",
  "are",
  "now",
  "dead",
  "ashes",
  ",",
  "and",
  "the",
  "wind",
  "blowing",
  "through",
  "the",
  "burst-open",
  "windows",
  ".",
  "</s>",
  "<s>",
  "A",
  "sudden",
  "icy",
  "wind",
  "struck",
  "me",
  ";",
  "I",
  "felt",
  "my",
  "legs",
  "go",
  "numb",
  ".",
  "</s>",
  "<s>",
  "Secret",
  "the",
  "meeting",
  "in",
  "time",
  "and",
  "place",
  ",",
  "the",
  "time",
  "of",
  "the",
  "off-shore",
  "wind",
  ",",
  "the",
  "place",
  "where",
  "the",
  "loyalty",
  "is",
  "divided",
  ".",
  "</s>",
  "<s>",
  "Green",
  "is",
  "almost",
  "uniformly",
  "spread",
  "over",
  "the",
  "plants",
  ",",
  "the",
  "wind",
  "follows",
  "the",
  "birds",
  ",",
  "no",
  "one",
  "risks",
  "seeing",
  "the",
  "stones",
  "die",
  ".",
  "</s>",
  "<s>",
  "The",
  "wind",
  "roars",
  "up",
  "the",
  "avenue",
  ".",
  "</s>",
  "<s>",
  "The",
  "wind",
  "falls",
  ",",
  "the",
  "rain",
  "slides",
  "silver",
  "down",
  "the",
  "glass",
  ".",
  "</s>",
  "<s>",
  "The",
  "wind",
  "drives",
  "straightly",
  ";",
  "the",
  "flame",
  "stoops",
  "slightly",
  ".",
  "</s>",
  "<s>",
  "At",
  "sunset",
  ",",
  "when",
  "there",
  "was",
  "no",
  "wind",
  ",",
  "and",
  "the",
  "pine-smoke",
  "from",
  "over",
  "by",
  "the",
  "sawmill",
  "hugged",
  "the",
  "earth",
  ",",
  "and",
  "you",
  "couldn\u2019t",
  "see",
  "more",
  "than",
  "a",
  "few",
  "feet",
  "in",
  "front",
  ",",
  "her",
  "sudden",
  "darting",
  "past",
  "you",
  "was",
  "a",
  "bit",
  "of",
  "vivid",
  "color",
  ",",
  "like",
  "a",
  "black",
  "bird",
  "that",
  "flashes",
  "in",
  "light",
  ".",
  "</s>",
  "<s>",
  "In",
  "sad",
  "times",
  ",",
  "hurt",
  "seabirds",
  "come",
  "to",
  "wail",
  "in",
  "ice",
  "white",
  "wind",
  ",",
  "alone",
  ",",
  "and",
  "wail",
  "in",
  "starlight",
  "wells",
  ",",
  "cold",
  "pits",
  "of",
  "evening",
  ",",
  "and",
  "endings",
  ",",
  "flinging",
  "rounds",
  "of",
  "flame",
  "sheeted",
  "balls",
  "of",
  "jagged",
  "bone",
  ",",
  "eaten",
  ",",
  "with",
  "remains",
  "of",
  "torn",
  "flowers",
  ",",
  "overwhelming",
  "after-thoughts",
  ",",
  "binding",
  "loves",
  ",",
  "classic",
  "pains",
  ",",
  "casting",
  "elongated",
  "shadows",
  ",",
  "of",
  "early",
  "blue",
  ".",
  "</s>",
  "<s>",
  "Will",
  "you",
  "come",
  "to",
  "visit",
  "me",
  "in",
  "hospital",
  "?",
  ";",
  "I",
  "stood",
  "up",
  ",",
  "I",
  "sat",
  "down",
  ",",
  "I",
  "stood",
  "up",
  "again",
  ";",
  "the",
  "clock",
  "slowed",
  "down",
  ",",
  "the",
  "post",
  "came",
  "late",
  ",",
  "the",
  "afternoon",
  "turned",
  "cool",
  ";",
  "the",
  "cat",
  "licked",
  "his",
  "coat",
  ",",
  "tore",
  "the",
  "chair",
  "to",
  "shreds",
  ",",
  "slept",
  "in",
  "a",
  "drawer",
  "that",
  "didn\u2019t",
  "close",
  ";",
  "I",
  "entered",
  "a",
  "room",
  ",",
  "I",
  "felt",
  "my",
  "skin",
  "shiver",
  ",",
  "then",
  "dissolve",
  ",",
  "I",
  "lighted",
  "a",
  "candle",
  ",",
  "I",
  "saw",
  "something",
  "move",
  ",",
  "I",
  "recognized",
  "the",
  "shadow",
  "to",
  "be",
  "my",
  "own",
  "hand",
  ",",
  "I",
  "felt",
  "myself",
  "to",
  "be",
  "one",
  "thing",
  ";",
  "the",
  "wind",
  "was",
  "hard",
  ",",
  "the",
  "house",
  "swayed",
  ",",
  "the",
  "angiosperms",
  "prospered",
  ",",
  "the",
  "mammal-like",
  "reptiles",
  "vanished",
  "Is",
  "the",
  "Heaven",
  "to",
  "be",
  "above",
  "?",
  "</s>"
];
SuffixArray.SILENT = true;
describe("Markov.SuffixArray", () => {
  it("SuffixArray.constructor", function() {
    let sa;
    sa = new SuffixArray(["b", "c", "a"]);
    assert.strictEqual(sa.data.length, 3);
    assert.deepStrictEqual(sa.seqmap.filter((e) => e), []);
    assert.deepStrictEqual(sa.data, [2, 0, 1]);
    sa = new SuffixArray(["b", "c", "ab", "a"], { debug: 0 });
    assert.strictEqual(sa.data.length, 4);
    assert.deepStrictEqual(sa.seqmap.filter((e) => e), []);
    assert.deepStrictEqual(sa.data, [3, 2, 0, 1]);
    sa = new SuffixArray(["banana", "ananas"]);
    assert.strictEqual(sa.data.length, 2);
    assert.deepStrictEqual(sa.seqmap.filter((e) => e), []);
    assert.deepStrictEqual(sa.data, [1, 0]);
    sa = new SuffixArray(exampleTokens);
    expect(sa).to.be.an.instanceof(SuffixArray);
    expect(Array.isArray(sa.data)).to.be.true;
    expect(sa.data.length).to.eq(21);
    assert.deepStrictEqual(sa.data, [
      19,
      9,
      20,
      10,
      11,
      0,
      12,
      1,
      13,
      2,
      8,
      14,
      3,
      4,
      7,
      5,
      16,
      6,
      17,
      18,
      15
    ]);
  });
  it("SuffixArray.compressed()", () => {
    let sa = new SuffixArray(exampleTokens);
    expect(sa).to.be.an.instanceof(SuffixArray);
    expect(Array.isArray(sa.data)).to.be.true;
    expect(sa.data.length).to.eq(21);
    assert.deepStrictEqual(sa.data, [
      19,
      9,
      20,
      10,
      11,
      0,
      12,
      1,
      13,
      2,
      8,
      14,
      3,
      4,
      7,
      5,
      16,
      6,
      17,
      18,
      15
    ]);
  });
  it("SuffixArray.arrayCompare()", () => {
    expect(SuffixArray.arrayCompare([], ["a"])).to.equal(0);
    expect(SuffixArray.arrayCompare(["a", "b"], ["a"])).to.equal(1);
    expect(SuffixArray.arrayCompare(["a", "b", "c"], ["a", "b"])).to.equal(2);
    expect(SuffixArray.arrayCompare(["a", "b"], ["a", "b", "c"])).to.equal(2);
    expect(SuffixArray.arrayCompare(["a", "b"], ["a", "b", "c", "d"])).to.equal(2);
    expect(SuffixArray.arrayCompare("The dog ate".split(" "), "The dog ran".split(" "))).to.equal(2);
    expect(SuffixArray.arrayCompare([], [])).to.equal(-1);
    expect(SuffixArray.arrayCompare(["a"], ["a"])).to.equal(-1);
    expect(SuffixArray.arrayCompare("The dog ate".split(" "), "The dog ate".split(" "))).to.equal(-1);
  });
  it("SuffixArray.arrayCompareSlices()", () => {
    let arr = ["a", "b", "c", "d"];
    expect(SuffixArray.arrayCompareSlices(arr, 0, 0, 0, 1)).to.equal(0);
    expect(SuffixArray.arrayCompareSlices(arr, 0, 2, 0, 1)).to.equal(1);
    expect(SuffixArray.arrayCompareSlices(arr, 0, 3, 0, 2)).to.equal(2);
    expect(SuffixArray.arrayCompareSlices(arr, 0, 2, 0, 3)).to.equal(2);
    expect(SuffixArray.arrayCompareSlices(arr, 0, 2, 0, 4)).to.equal(2);
    expect(SuffixArray.arrayCompareSlices(arr, 1, 2, 1, 4)).to.equal(1);
  });
  it("SuffixArray.to/fromJSON()", function() {
    let sa = new SuffixArray(exampleTokens);
    let json = sa.toJSON();
    let sa2 = SuffixArray.fromJSON(json);
    expect(Object.keys(sa).sort()).to.deep.equal(Object.keys(sa2).sort());
    expect(sa2).to.be.an.instanceof(SuffixArray);
    SuffixArray.__dict__.forEach((f) => expect(sa2[f]).to.deep.equal(sa[f], '1. failed on "' + f + '"'));
    let sa3 = SuffixArray.fromJSON(JSON.stringify(sa.toJSON()));
    expect(sa3).to.be.an.instanceof(SuffixArray);
    SuffixArray.__dict__.forEach((f) => expect(sa3[f]).to.deep.equal(sa[f], "2. failed on" + f + '"'));
    expect(Object.keys(sa).sort()).to.deep.equal(Object.keys(sa3).sort());
  });
  it("SuffixArray.randSeqStart()", () => {
    let model = new SuffixArray(exampleTokens);
    let starts = model.seqmap.reduce((a, e, i) => {
      if (e === 1) a.push(i);
      return a;
    }, []);
    let decoded = starts.map((idx) => model._decode(model.input[idx + 1]));
    expect(decoded).to.deep.equal(["The", "The"]);
    expect(model.randSeqStart()).to.equal("The");
  });
  it("SuffixArray.randSeqStart() honors RiTa.randomSeed", () => {
    const toks = [
      SEQ_START_TOKEN,
      "The",
      "dog",
      "ran",
      SEQ_END_TOKEN,
      SEQ_START_TOKEN,
      "A",
      "cat",
      "sat",
      SEQ_END_TOKEN,
      SEQ_START_TOKEN,
      "Some",
      "bird",
      "flew",
      SEQ_END_TOKEN
    ];
    const model = new SuffixArray(toks);
    const draw = (seed) => {
      RiTa.randomSeed(seed);
      return Array.from({ length: 10 }, () => model.randSeqStart());
    };
    try {
      expect(draw(1)).to.eql(draw(1));
      expect(draw(1)).to.not.eql(draw(500));
    } finally {
      RiTa.randomSeed(Date.now());
    }
  });
  it("SuffixArray.find()", () => {
    let sa, min, max, patt, tokens, count;
    sa = new SuffixArray(["b", "c", "ab", "a"]);
    expect(sa.tokensFor(3)).to.deep.equal(["c", "ab", "a"]);
    patt = ["ab"];
    [min, max] = sa.find(patt);
    tokens = sa.tokensForRange(min, max);
    expect(tokens).to.deep.equal([["ab", "a"]]);
    tokens.forEach((t) => t.slice(0, patt.length).forEach((p, i) => expect(p).to.equal(patt[i])));
    patt = ["ab", "a"];
    [min, max] = sa.find(patt);
    tokens = sa.tokensForRange(min, max);
    tokens.forEach((t) => t.slice(0, patt.length).forEach((p, i) => expect(p).to.equal(patt[i])));
    sa = new SuffixArray(["b", "c", "ab", "a", "ab", "a", "c"]);
    patt = ["ab", "a"];
    [min, max] = sa.find(patt);
    tokens = sa.tokensForRange(min, max);
    tokens.forEach((t) => t.slice(0, patt.length).forEach((p, i) => expect(p).to.equal(patt[i])));
    sa = new SuffixArray(exampleTokens, { debug: 0 });
    patt = ["The", "brown"];
    [min, max] = sa.find(patt);
    count = max - min;
    expect(count).equal(2);
    tokens = sa.tokensForRange(min, max);
    tokens.forEach((t) => t.slice(0, patt.length).forEach((p, i) => expect(p).to.equal(patt[i])));
    patt = ["over", "the"];
    [min, max] = sa.find(patt);
    count = max - min;
    expect(count).equal(2);
    tokens = sa.tokensForRange(min, max);
    tokens.forEach((t) => t.slice(0, patt.length).forEach((p, i) => expect(p).to.equal(patt[i])));
    patt = ["The", "brown", "dog"];
    [min, max] = sa.find(patt);
    count = max - min;
    expect(count).equal(1);
    tokens = sa.tokensForRange(min, max);
    tokens.forEach((t) => t.slice(0, patt.length).forEach((p, i) => expect(p).to.equal(patt[i])));
    [min, max] = sa.find([]);
    count = max - min;
    expect(count).equal(2);
    tokens = sa.tokensForRange(min, max);
    tokens.forEach((t) => expect(t[0]).to.equal(SEQ_START_TOKEN) && expect(t[t.length - 1]).to.equal(SEQ_END_TOKEN));
    sa = new SuffixArray(longerTokens);
    [min, max] = sa.find(["wind", "and", "the"]);
    expect(max - min).to.equal(1);
  });
  it("SuffixArray.tokensFor()", () => {
    let sa = new SuffixArray(["b", "c", "ab", "a"]);
    expect(sa.tokensFor(3)).to.deep.equal(["c", "ab", "a"]);
    sa = new SuffixArray(exampleTokens);
    let toks = sa.tokensFor(11);
    expect(toks).to.deep.equal([
      "dog",
      "wept",
      "over",
      "the",
      "treat",
      ".",
      "</s>"
    ]);
  });
  it("SuffixArray.isUnique()", () => {
    let sa = new SuffixArray(exampleTokens);
    expect(sa.isUnique(exampleTokens)).false;
    expect(sa.isUnique(exampleTokens.slice(1))).false;
    expect(sa.isUnique("The clown dog wept over the treat . </s>".split(" "))).to.equal(true);
    expect(sa.isUnique("The brown dog wept over the treat . </s>".split(" "))).to.equal(false);
    expect(sa.isUnique([
      SEQ_START_TOKEN,
      "The",
      "brown",
      "fox",
      "jumps",
      "over",
      "the",
      "treat",
      ".",
      SEQ_END_TOKEN
    ])).to.equal(true);
  });
  it("SuffixArray.pdist()", () => {
    let dist, sa = new SuffixArray(exampleTokens);
    dist = sa.pdist(["The", "brown"]);
    expect(dist).to.deep.equal({ fox: 0.5, dog: 0.5 });
    dist = sa.pdist([SEQ_END_TOKEN]);
    expect(dist).to.deep.equal({ [SEQ_START_TOKEN]: 1 });
    dist = sa.pdist([".", SEQ_END_TOKEN]);
    expect(dist).to.deep.equal({ [SEQ_START_TOKEN]: 1 });
    dist = sa.pdist(["dog", ".", SEQ_END_TOKEN]);
    expect(dist).to.deep.equal({ [SEQ_START_TOKEN]: 1 });
    let inp = [...exampleTokens, SEQ_START_TOKEN, "The", "brown", "dog", "leapt", "over", "the", "fence", ".", SEQ_END_TOKEN, SEQ_START_TOKEN, "The", "brown", "dog", ".", SEQ_END_TOKEN];
    sa = new SuffixArray(inp);
    dist = sa.pdist(["The", "brown"]);
    expect(dist).to.deep.equal({ dog: 0.8807970779778824, fox: 0.11920292202211755 });
    dist = sa.pdist(["The", "brown"], { temp: 0 });
    expect(dist).to.deep.equal({ fox: 0.25, dog: 0.75 });
    dist = sa.pdist(["leapt", "over", "the"]);
    expect(dist).to.deep.equal({ fence: 1 });
  });
  it("SuffixArray.hasSuffix()", () => {
    let res, patt, sa = new SuffixArray(exampleTokens);
    patt = "The,brown,dog,wept,over,the,treat,.,</s>".split(",");
    res = sa.hasSuffix(patt);
    expect(res).equal(true);
    patt = "<s>,The,brown,dog,wept,over,the,treat,.,</s>".split(",");
    res = sa.hasSuffix(patt);
    expect(res).equal(true);
    patt = "<s>,The,brown,dog,wept,over,the,treat,.,".split(",");
    res = sa.hasSuffix(patt);
    expect(res).equal(false);
    patt = "<s>,The,brown,dogs,wept,over,the,treat,.,</s>".split(",");
    res = sa.hasSuffix(patt);
    expect(res).equal(false);
    patt = "The,brown".split(",");
    res = sa.hasSuffix(patt);
    expect(res).equal(false);
  });
  it("SuffixArray.hasPrefix()", () => {
    let res, patt, sa;
    sa = new SuffixArray("<s> The dog ate . </s>".split(" "), { debug: 0 });
    expect(sa.hasPrefix("The dog".split(" "), { debug: 0 })).equal(true);
    expect(sa.hasPrefix("The dog ate . </s>".split(" "))).equal(true);
    expect(sa.hasPrefix("The dog ate .".split(" "))).equal(true);
    expect(sa.hasPrefix("The dog ate".split(" "))).equal(true);
    expect(sa.hasPrefix("The".split(" "))).equal(true);
    expect(sa.hasPrefix("The fox ate . </s>".split(" "))).equal(false);
    expect(sa.hasPrefix("The fox ate .".split(" "))).equal(false);
    expect(sa.hasPrefix("The fox ate".split(" "))).equal(false);
    expect(sa.hasPrefix("The fox".split(" "))).equal(false);
    sa = new SuffixArray(exampleTokens);
    patt = "The,brown,dog,wept,over,the,treat,.,</s>".split(",");
    res = sa.hasPrefix(patt);
    expect(res).equal(true);
    patt = "<s>,The,brown,dog,wept,over,the,treat,.,</s>".split(",");
    res = sa.hasPrefix(patt);
    expect(res).equal(true);
    patt = "The,brown".split(",");
    res = sa.hasPrefix(patt);
    expect(res).equal(true);
    patt = "The,brown,fox,wept".split(",");
    res = sa.hasPrefix(patt);
    expect(res).equal(false);
    patt = "<s>,The,brown,dog,over,the,treat,.,".split(",");
    res = sa.hasPrefix(patt);
    expect(res).equal(false);
    patt = "<s>,The,brown,dogs,wept,over,the,treat,.,</s>".split(",");
    res = sa.hasPrefix(patt);
    expect(res).equal(false);
    patt = "The,brown,cat".split(",");
    res = sa.hasPrefix(patt);
    expect(res).equal(false);
  });
  it("SuffixArray.normaliseDist()", () => {
    expect(SuffixArray.normaliseDist({})).to.deep.equal({});
    expect(SuffixArray.normaliseDist({ fox: 1, dog: 3 })).to.deep.equal({ fox: 0.25, dog: 0.75 });
    let res = SuffixArray.normaliseDist({ fox: 1 + Math.random() * 999, dog: 1 + Math.random() * 999 });
    expect(Object.values(res).reduce((acc, val) => acc + val, 0)).to.be.closeTo(1, 1e-4);
    expect(() => SuffixArray.normaliseDist()).to.throw();
    expect(() => SuffixArray.normaliseDist({ a: -1 })).to.throw();
  });
  it("SuffixArray.normaliseDist(floats)", () => {
    let res = SuffixArray.normaliseDist({ fox: 0.5 });
    expect(res.fox).to.be.closeTo(1, 1e-4);
    res = SuffixArray.normaliseDist({ fox: 0.333333 });
    expect(res.fox).to.be.closeTo(1, 1e-4);
    res = SuffixArray.normaliseDist({ fox: 0.1, dog: 0.3 });
    expect(res.fox).to.be.closeTo(0.25, 1e-4);
    expect(res.dog).to.be.closeTo(0.75, 1e-4);
    res = SuffixArray.normaliseDist({ fox: 0.1 + Math.random() * 0.999, dog: 0.1 + Math.random() * 0.999 });
    expect(Object.values(res).reduce((acc, val) => acc + val, 0)).to.be.closeTo(1, 1e-4);
  });
  it("SuffixArray.toString()", () => {
    let sa, expected;
    sa = new SuffixArray(["b", "c", "a"]);
    assert.deepStrictEqual(sa.data, [2, 0, 1]);
    expected = `
[
  0: [a],
  1: [b,c,a],
  2: [c,a],
]
`;
    assert.strictEqual(sa.toString(), expected);
    assert.strictEqual(sa.toString({ maxTokens: 3 }), expected);
    expected = `
[
  0: [a],
  1: [b,c,a],
  2: [c,a],
]
`;
    assert.strictEqual(sa.toString({ maxTokens: 2 }), expected);
    expected = `
[
  0: [a],
  1: [b,c,a],
  2: [c,a],
]
`;
    assert.strictEqual(sa.toString({ maxTokens: 1 }), expected);
    sa = new SuffixArray(["b", "c", "ab", "a"]);
    expected = `
[
  0: [a],
  1: [ab,a],
  2: [b,c,ab,a],
  3: [c,ab,a],
]
`;
    expect(sa.toString()).to.equal(expected);
    sa = new SuffixArray(["banana", "ananas"]);
    expected = `
[
  0: [ananas],
  1: [banana,ananas],
]
`;
    expect(sa.toString()).to.equal(expected);
  });
});
