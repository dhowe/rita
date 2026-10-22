import { expect } from "chai";
import { RiTa } from "./index.js";
let hasLex = true;
describe("Conjugator", function() {
  it("Should call pastPart", function() {
    expect(RiTa.pastPart("pen")).eq("penned");
    expect(RiTa.pastPart("red")).eq("red");
    expect(RiTa.pastPart("sleep")).eq("slept");
    expect(RiTa.pastPart("withhold")).eq("withheld");
    expect(RiTa.pastPart("cut")).eq("cut");
    expect(RiTa.pastPart("go")).eq("gone");
    expect(RiTa.pastPart("swim")).eq("swum");
    expect(RiTa.pastPart("would")).eq("would");
    expect(RiTa.pastPart("might")).eq("might");
    expect(RiTa.pastPart("run")).eq("run");
    expect(RiTa.pastPart("speak")).eq("spoken");
    expect(RiTa.pastPart("break")).eq("broken");
    expect(RiTa.pastPart("plead")).eq("pled");
    expect(RiTa.pastPart("")).eq("");
    expect(RiTa.pastPart("shrink")).eq("shrunk");
    expect(RiTa.pastPart("stink")).eq("stunk");
    expect(RiTa.pastPart("study")).eq("studied");
    expect(RiTa.pastPart("bite")).eq("bitten");
    expect(RiTa.pastPart("break")).eq("broken");
    expect(RiTa.pastPart("call")).eq("called");
    expect(RiTa.pastPart("commit")).eq("committed");
    expect(RiTa.pastPart("computerize")).eq("computerized");
    expect(RiTa.pastPart("concern")).eq("concerned");
    expect(RiTa.pastPart("discriminate")).eq("discriminated");
    expect(RiTa.pastPart("end")).eq("ended");
    expect(RiTa.pastPart("expect")).eq("expected");
    expect(RiTa.pastPart("finish")).eq("finished");
    expect(RiTa.pastPart("gain")).eq("gained");
    expect(RiTa.pastPart("get")).eq("gotten");
    expect(RiTa.pastPart("increase")).eq("increased");
    expect(RiTa.pastPart("involve")).eq("involved");
    expect(RiTa.pastPart("launch")).eq("launched");
    expect(RiTa.pastPart("lead")).eq("led");
    expect(RiTa.pastPart("live")).eq("lived");
    expect(RiTa.pastPart("outpace")).eq("outpaced");
    expect(RiTa.pastPart("oversee")).eq("overseen");
    expect(RiTa.pastPart("oversell")).eq("oversold");
    expect(RiTa.pastPart("pale")).eq("paled");
    expect(RiTa.pastPart("prepay")).eq("prepaid");
    expect(RiTa.pastPart("pressure")).eq("pressured");
    expect(RiTa.pastPart("proliferate")).eq("proliferated");
    expect(RiTa.pastPart("remake")).eq("remade");
    expect(RiTa.pastPart("reopen")).eq("reopened");
    expect(RiTa.pastPart("report")).eq("reported");
    expect(RiTa.pastPart("resell")).eq("resold");
    expect(RiTa.pastPart("settle")).eq("settled");
    expect(RiTa.pastPart("bite")).eq("bitten");
    expect(RiTa.pastPart("break")).eq("broken");
    expect(RiTa.pastPart("build")).eq("built");
    expect(RiTa.pastPart("enter")).eq("entered");
    expect(RiTa.pastPart("own")).eq("owned");
    expect(RiTa.pastPart("plan")).eq("planned");
    expect(RiTa.pastPart("rent")).eq("rented");
    expect(RiTa.pastPart("repurchase")).eq("repurchased");
    expect(RiTa.pastPart("roast")).eq("roasted");
    expect(RiTa.pastPart("start")).eq("started");
    expect(RiTa.pastPart("bust")).eq("busted");
    expect(RiTa.pastPart("heart")).eq("hearted");
    expect(RiTa.pastPart("closet")).eq("closeted");
    expect(RiTa.pastPart("bear")).eq("borne");
    if (hasLex) {
      expect(RiTa.pastPart("hopped")).eq("hopped");
      expect(RiTa.pastPart("hated")).eq("hated");
      expect(RiTa.pastPart("created")).eq("created");
      expect(RiTa.pastPart("committed")).eq("committed");
      expect(RiTa.pastPart("submitted")).eq("submitted");
      expect(RiTa.pastPart("come")).eq("come");
      expect(RiTa.pastPart("forgotten")).eq("forgotten");
      expect(RiTa.pastPart("arisen")).eq("arisen");
      expect(RiTa.pastPart("eaten")).eq("eaten");
      expect(RiTa.pastPart("chosen")).eq("chosen");
      expect(RiTa.pastPart("frozen")).eq("frozen");
      expect(RiTa.pastPart("stolen")).eq("stolen");
      expect(RiTa.pastPart("worn")).eq("worn");
      expect(RiTa.pastPart("broken")).eq("broken");
      expect(RiTa.pastPart("written")).eq("written");
      expect(RiTa.pastPart("ridden")).eq("ridden");
      expect(RiTa.pastPart("drawn")).eq("drawn");
      expect(RiTa.pastPart("known")).eq("known");
      expect(RiTa.pastPart("grown")).eq("grown");
      expect(RiTa.pastPart("done")).eq("done");
      expect(RiTa.pastPart("gone")).eq("gone");
      expect(RiTa.pastPart("awake")).eq("awoken");
      expect(RiTa.pastPart("become")).eq("become");
      expect(RiTa.pastPart("drink")).eq("drunk");
      expect(RiTa.pastPart("run")).eq("run");
      expect(RiTa.pastPart("shine")).eq("shone");
      expect(RiTa.pastPart("grown")).eq("grown");
      expect(RiTa.pastPart("heard")).eq("heard");
    }
  });
  it("Should call presentPart", function() {
    expect(RiTa.presentPart("")).eq("");
    expect(RiTa.presentPart("sleep")).eq("sleeping");
    expect(RiTa.presentPart("withhold")).eq("withholding");
    expect(RiTa.presentPart("cut")).eq("cutting");
    expect(RiTa.presentPart("go")).eq("going");
    expect(RiTa.presentPart("run")).eq("running");
    expect(RiTa.presentPart("speak")).eq("speaking");
    expect(RiTa.presentPart("break")).eq("breaking");
    expect(RiTa.presentPart("become")).eq("becoming");
    expect(RiTa.presentPart("plead")).eq("pleading");
    expect(RiTa.presentPart("awake")).eq("awaking");
    expect(RiTa.presentPart("study")).eq("studying");
    expect(RiTa.presentPart("lie")).eq("lying");
    expect(RiTa.presentPart("swim")).eq("swimming");
    expect(RiTa.presentPart("run")).eq("running");
    expect(RiTa.presentPart("dig")).eq("digging");
    expect(RiTa.presentPart("set")).eq("setting");
    expect(RiTa.presentPart("speak")).eq("speaking");
    expect(RiTa.presentPart("bring")).eq("bringing");
    expect(RiTa.presentPart("speak")).eq("speaking");
    expect(RiTa.presentPart("study ")).eq("studying");
    expect(RiTa.presentPart(" study")).eq("studying");
    expect(RiTa.presentPart("hoe")).eq("hoeing");
    expect(RiTa.presentPart("shoe")).eq("shoeing");
    if (hasLex) {
      expect(RiTa.pastPart("awake")).eq("awoken");
      expect(RiTa.pastPart("become")).eq("become");
      expect(RiTa.pastPart("drink")).eq("drunk");
      expect(RiTa.pastPart("run")).eq("run");
      expect(RiTa.pastPart("shine")).eq("shone");
    }
  });
  it("Should conjugate VBDs", function() {
    if (!hasLex) this.skip();
    expect(RiTa.conjugate("go", {
      number: RiTa.SINGULAR,
      person: RiTa.FIRST,
      tense: RiTa.PAST
    })).eq("went");
    expect(RiTa.conjugate("run", {
      number: RiTa.SINGULAR,
      person: RiTa.FIRST,
      tense: RiTa.PAST
    })).eq("ran");
  });
  it("Should call conjugate", function() {
    if (!hasLex) this.skip();
    let args, s, a, c;
    expect(RiTa.conjugate("walk")).eq("walk");
    expect(function() {
      RiTa.conjugate();
    }).to.throw();
    expect(function() {
      RiTa.conjugate("");
    }).to.throw();
    expect("swum").eq(RiTa.pastPart("swim"));
    expect(RiTa.conjugate("be", { form: RiTa.GERUND })).eq("being");
    expect(RiTa.conjugate("are", {
      number: RiTa.PLURAL,
      person: RiTa.SECOND,
      tense: RiTa.PAST
    })).eq("were");
    s = ["swim", "need", "open"];
    a = ["swims", "needs", "opens"];
    args = {
      tense: RiTa.PRESENT,
      number: RiTa.SINGULAR,
      person: RiTa.THIRD
    };
    expect(() => RiTa.conjugate(args)).to.throw();
    expect(() => RiTa.conjugate("", args)).to.throw();
    for (let i = 0; i < s.length; i++) {
      let c2 = RiTa.conjugate(s[i], args);
      expect(c2).eq(a[i]);
    }
    args = {
      tense: RiTa.PRESENT,
      number: RiTa.SINGULAR,
      person: RiTa.THIRD,
      passive: true
    };
    a = ["is swum", "is needed", "is opened"];
    for (let i = 0; i < s.length; i++) {
      expect(RiTa.conjugate(s[i], args)).eq(a[i]);
    }
    args = {
      number: RiTa.SINGULAR,
      person: RiTa.FIRST,
      tense: RiTa.PAST
    };
    expect(RiTa.conjugate("swim", args)).eq("swam");
    s = ["swim", "need", "open"];
    a = ["swam", "needed", "opened"];
    expect(a.length === s.length).true;
    for (let i = 0; i < s.length; i++) {
      let c2 = RiTa.conjugate(s[i], args);
      expect(c2).eq(a[i]);
    }
    args = {
      number: RiTa.PLURAL,
      person: RiTa.SECOND,
      tense: RiTa.PAST
    };
    a = ["swam", "needed", "opened"];
    expect(a.length === s.length).true;
    for (let i = 0; i < s.length; i++) {
      expect(RiTa.conjugate(s[i], args)).eq(a[i]);
    }
    args = {
      number: RiTa.PLURAL,
      person: RiTa.SECOND,
      tense: RiTa.FUTURE
    };
    a = ["will swim", "will need", "will open"];
    expect(a.length === s.length).true;
    for (let i = 0; i < s.length; i++) {
      expect(RiTa.conjugate(s[i], args)).eq(a[i]);
    }
    args = {
      tense: RiTa.PAST,
      number: RiTa.SINGULAR,
      person: RiTa.THIRD
    };
    a = ["swam", "needed", "opened"];
    expect(a.length === s.length).true;
    for (let i = 0; i < s.length; i++) {
      c = RiTa.conjugate(s[i], args);
      expect(c).eq(a[i]);
    }
    args = {
      tense: RiTa.PAST,
      number: RiTa.SINGULAR,
      person: RiTa.THIRD,
      form: RiTa.INFINITIVE
    };
    a = ["to swim", "to need", "to open"];
    expect(a.length === s.length).true;
    for (let i = 0; i < s.length; i++) {
      c = RiTa.conjugate(s[i], args);
      expect(c).eq(a[i]);
    }
    args = {
      tense: RiTa.PAST,
      number: RiTa.SINGULAR,
      person: RiTa.THIRD,
      passive: true
    };
    s = ["scorch", "burn", "hit"];
    a = ["was scorched", "was burned", "was hit"];
    expect(a.length === s.length).true;
    for (let i = 0; i < s.length; i++) {
      c = RiTa.conjugate(s[i], args);
      expect(c).eq(a[i]);
    }
    s = ["swim", "need", "open"];
    args = {
      tense: RiTa.PRESENT,
      number: RiTa.SINGULAR,
      person: RiTa.THIRD,
      form: RiTa.INFINITIVE,
      progressive: true
    };
    a = ["to be swimming", "to be needing", "to be opening"];
    expect(a.length === s.length).true;
    for (let i = 0; i < s.length; i++) {
      c = RiTa.conjugate(s[i], args);
      expect(c).eq(a[i]);
    }
    args = {
      tense: RiTa.PRESENT,
      number: RiTa.SINGULAR,
      person: RiTa.THIRD,
      form: RiTa.INFINITIVE,
      perfect: true
    };
    a = ["to have swum", "to have needed", "to have opened"];
    expect(a.length === s.length).true;
    for (let i = 0; i < s.length; i++) {
      c = RiTa.conjugate(s[i], args);
      expect(c).eq(a[i]);
    }
    args = {
      number: RiTa.PLURAL,
      person: RiTa.SECOND,
      tense: RiTa.PAST
    };
    expect(RiTa.conjugate("barter", args)).eq("bartered");
    expect(RiTa.conjugate("run", args)).eq("ran");
    args = {
      number: RiTa.PLURAL,
      person: RiTa.SECOND,
      tense: RiTa.PAST
    };
    s = ["compete", "complete", "eject"];
    a = ["competed", "completed", "ejected"];
    for (let i = 0; i < s.length; i++) {
      expect(RiTa.conjugate(s[i], args)).eq(a[i], "failed on " + s[i]);
    }
    args = {
      number: RiTa.PLURAL,
      person: RiTa.SECOND,
      tense: RiTa.PAST,
      interrogative: true
    };
    s = ["compete", "complete", "eject"];
    a = ["compete", "complete", "eject"];
    for (let i = 0; i < s.length; i++) {
      expect(RiTa.conjugate(s[i], args)).eq(a[i], "failed on " + s[i]);
    }
    expect(function() {
      RiTa.conjugate("walk", "invalid args");
    }).to.throw();
    expect(RiTa.conjugate("walk", "1SPr")).eq("walk");
    expect(RiTa.conjugate("walk", "1PPr")).eq("walk");
    expect(RiTa.conjugate("walk", "2SPr")).eq("walk");
    expect(RiTa.conjugate("walk", "3SPr")).eq("walks");
    expect(RiTa.conjugate("walk", "1SFu")).eq("will walk");
    expect(RiTa.conjugate("walk", "1SPa")).eq("walked");
    expect(RiTa.conjugate("walk", "2PPa")).eq("walked");
    expect(RiTa.conjugate("is", "3PPa")).eq("were");
    expect(RiTa.conjugate("is", "2SPa")).eq("were");
    expect(RiTa.conjugate("is", "3SPa")).eq("was");
    expect(RiTa.conjugate("is", "2PPa")).eq("were");
    let original = ["run", "walk", "swim", "create"];
    let expected = ["is run", "is walked", "is swum", "is created"];
    original.forEach((w, i) => {
      expect(RiTa.conjugate(w, { person: RiTa.THIRD, passive: true })).eq(expected[i]);
    });
    expected = ["is running", "is walking", "is swimming", "is creating"];
    original.forEach((w, i) => {
      expect(RiTa.conjugate(w, { person: RiTa.THIRD, progressive: true })).eq(expected[i]);
    });
    expected = ["run", "walk", "swim", "create"];
    original.forEach((w, i) => {
      expect(RiTa.conjugate(w, { person: RiTa.THIRD, interrogative: true })).eq(expected[i]);
    });
    expected = ["has run", "has walked", "has swum", "has created"];
    original.forEach((w, i) => {
      expect(RiTa.conjugate(w, { person: RiTa.THIRD, perfect: true })).eq(expected[i]);
    });
    expected = ["being run", "being walked", "being swum", "being created"];
    original.forEach((w, i) => {
      expect(RiTa.conjugate(w, { person: RiTa.THIRD, passive: true, form: RiTa.GERUND })).eq(expected[i]);
    });
    expected = ["being running", "being walking", "being swimming", "being creating"];
    original.forEach((w, i) => {
      expect(RiTa.conjugate(w, { person: RiTa.THIRD, progressive: true, form: RiTa.GERUND })).eq(expected[i]);
    });
    expected = ["running", "walking", "swimming", "creating"];
    original.forEach((w, i) => {
      expect(RiTa.conjugate(w, { person: RiTa.THIRD, interrogative: true, form: RiTa.GERUND })).eq(expected[i]);
    });
    expected = ["having run", "having walked", "having swum", "having created"];
    original.forEach((w, i) => {
      expect(RiTa.conjugate(w, { person: RiTa.THIRD, perfect: true, form: RiTa.GERUND })).eq(expected[i]);
    });
    expected = ["to be run", "to be walked", "to be swum", "to be created"];
    original.forEach((w, i) => {
      expect(RiTa.conjugate(w, { person: RiTa.THIRD, passive: true, form: RiTa.INFINITIVE })).eq(expected[i]);
    });
    expected = ["to be running", "to be walking", "to be swimming", "to be creating"];
    original.forEach((w, i) => {
      expect(RiTa.conjugate(w, { person: RiTa.THIRD, progressive: true, form: RiTa.INFINITIVE })).eq(expected[i]);
    });
    expected = ["to run", "to walk", "to swim", "to create"];
    original.forEach((w, i) => {
      expect(RiTa.conjugate(w, { person: RiTa.THIRD, interrogative: true, form: RiTa.INFINITIVE })).eq(expected[i]);
    });
    expected = ["to have run", "to have walked", "to have swum", "to have created"];
    original.forEach((w, i) => {
      expect(RiTa.conjugate(w, { person: RiTa.THIRD, perfect: true, form: RiTa.INFINITIVE })).eq(expected[i]);
    });
    RiTa.conjugate("swim", "2PPa");
    expect(RiTa.conjugate("walked", "3SPr")).eq("walks");
    expect(RiTa.conjugate("changed", "3SPr")).eq("changes");
    expect(RiTa.conjugate("spent", "3SPr")).eq("spends");
    expect(RiTa.conjugate("eaten", "3SPr")).eq("eats");
    RiTa.conjugate("swim", "2PPa");
  });
  it("Should call toString", function() {
    if (!hasLex) this.skip();
    expect(RiTa.conjugator.toString()).eq("  ---------------------\n  Passive = false\n  Perfect = false\n  Progressive = false\n  ---------------------\n  Number = 8\n  Person = 2\n  Tense = 4\n  ---------------------\n");
  });
  it("Should accept stems", function() {
    let plurPast2 = { number: RiTa.PLURAL, person: RiTa.SECOND, tense: RiTa.PAST };
    let plurPres2 = { number: RiTa.PLURAL, person: RiTa.SECOND, tense: RiTa.PRESENT };
    let singPres3 = { number: RiTa.SINGULAR, person: RiTa.THIRD, tense: RiTa.PRESENT };
    let stem = RiTa.stem("walking");
    expect(RiTa.conjugate(stem, plurPast2)).eq("walked", `${stem} => walked`);
    expect(RiTa.conjugate(stem, plurPres2)).eq("walk", `${stem} => walk`);
    expect(RiTa.conjugate(stem, singPres3)).eq("walks", `${stem} => walks`);
    stem = RiTa.stem("writing");
    expect(RiTa.conjugate(stem, plurPast2)).eq("wrote", `${stem} => wrote`);
    expect(RiTa.conjugate(stem, plurPres2)).eq("write", `${stem} => write`);
    expect(RiTa.conjugate(stem, singPres3)).eq("writes", `${stem} => writes`);
    stem = RiTa.stem("asked");
    expect(RiTa.conjugate(stem, plurPast2)).eq("asked", `${stem} => asked`);
    expect(RiTa.conjugate(stem, plurPres2)).eq("ask", `${stem} => ask`);
    expect(RiTa.conjugate(stem, singPres3)).eq("asks", `${stem} => asks`);
    stem = RiTa.stem("changed");
    expect(RiTa.conjugate(stem, plurPast2)).eq("changed", `${stem} => changed`);
    expect(RiTa.conjugate(stem, plurPres2)).eq("change", `${stem} => change`);
    expect(RiTa.conjugate(stem, singPres3)).eq("changes", `${stem} => changes`);
    stem = RiTa.stem("admired");
    expect(RiTa.conjugate(stem, plurPast2)).eq("admired", `${stem} => admired`);
    expect(RiTa.conjugate(stem, plurPres2)).eq("admire", `${stem} => admire`);
    expect(RiTa.conjugate(stem, singPres3)).eq("admires", `${stem} => admires`);
    stem = RiTa.stem("cured");
    expect(RiTa.conjugate(stem, plurPast2)).eq("cured", `${stem} => cured`);
    expect(RiTa.conjugate(stem, plurPres2)).eq("cure", `${stem} => cure`);
    expect(RiTa.conjugate(stem, singPres3)).eq("cures", `${stem} => cures`);
    stem = RiTa.stem("studies");
    expect(RiTa.conjugate(stem, plurPast2)).eq("studied", `${stem} => studied`);
    expect(RiTa.conjugate(stem, plurPres2)).eq("study", `${stem} => study`);
    expect(RiTa.conjugate(stem, singPres3)).eq("studies", `${stem} => studies`);
  });
  it("Should accept stem pairs", function() {
    let opts = { number: RiTa.PLURAL, person: RiTa.SECOND, tense: RiTa.PAST };
    let pairs = [
      ["accompanying", "accompanied"],
      ["feeling", "felt"],
      ["placating", "placated"],
      ["centralizing", "centralized"],
      ["humanized", "humanized"],
      ["boosted", "boosted"],
      ["wearing", "wore"],
      ["aroused", "aroused"],
      ["rising", "rose"],
      ["raising", "raised"],
      ["vibrating", "vibrated"],
      ["injection", "injected"],
      ["vibration", "vibrated"]
    ];
    pairs.forEach((p) => {
      let res = RiTa.conjugate(RiTa.stem(p[0]), opts);
      expect(res).equal(p[1], p[0] + " => " + RiTa.stem(p[0]) + " => " + p[1]);
    });
  });
  it("Should call unconjugate", function() {
    if (!hasLex) this.skip();
    expect(RiTa.conjugator.unconjugate("trepanning")).eq("trepan");
    expect(RiTa.conjugator.unconjugate("plays")).eq("play");
    expect(RiTa.conjugator.unconjugate("takes")).eq("take");
    expect(RiTa.conjugator.unconjugate("gets")).eq("get");
    expect(RiTa.conjugator.unconjugate("comes")).eq("come");
    expect(RiTa.conjugator.unconjugate("goes")).eq("go");
    expect(RiTa.conjugator.unconjugate("teaches")).eq("teach");
    expect(RiTa.conjugator.unconjugate("fixes")).eq("fix");
    expect(RiTa.conjugator.unconjugate("misses")).eq("miss");
    expect(RiTa.conjugator.unconjugate("studies")).eq("study");
    expect(RiTa.conjugator.unconjugate("tries")).eq("try");
    expect(RiTa.conjugator.unconjugate("carries")).eq("carry");
    expect(RiTa.conjugator.unconjugate("wishes")).eq("wish");
    expect(RiTa.conjugator.unconjugate("blitzes")).eq("blitz");
    expect(RiTa.conjugator.unconjugate("watched")).eq("watch");
    expect(RiTa.conjugator.unconjugate("planted")).eq("plant");
    expect(RiTa.conjugator.unconjugate("watered")).eq("water");
    expect(RiTa.conjugator.unconjugate("pulled")).eq("pull");
    expect(RiTa.conjugator.unconjugate("picked")).eq("pick");
    expect(RiTa.conjugator.unconjugate("liked")).eq("like");
    expect(RiTa.conjugator.unconjugate("moved")).eq("move");
    expect(RiTa.conjugator.unconjugate("tasted")).eq("taste");
    expect(RiTa.conjugator.unconjugate("tried")).eq("try");
    expect(RiTa.conjugator.unconjugate("studied")).eq("study");
    expect(RiTa.conjugator.unconjugate("carried")).eq("carry");
    expect(RiTa.conjugator.unconjugate("digged")).eq("dig");
    expect(RiTa.conjugator.unconjugate("flagged")).eq("flag");
    expect(RiTa.conjugator.unconjugate("blowing")).eq("blow");
    expect(RiTa.conjugator.unconjugate("raining")).eq("rain");
    expect(RiTa.conjugator.unconjugate("coming")).eq("come");
    expect(RiTa.conjugator.unconjugate("having")).eq("have");
    expect(RiTa.conjugator.unconjugate("running")).eq("run");
    expect(RiTa.conjugator.unconjugate("putting")).eq("put");
    expect(RiTa.conjugator.unconjugate("sitting")).eq("sit");
    expect(RiTa.conjugator.unconjugate("pulling")).eq("pull");
    expect(RiTa.conjugator.unconjugate("has")).eq("have");
    expect(RiTa.conjugator.unconjugate("had")).eq("have");
    expect(RiTa.conjugator.unconjugate("sat")).eq("sit");
    expect(RiTa.conjugator.unconjugate("shown")).eq("show");
    expect(RiTa.conjugator.unconjugate("ate")).eq("eat");
    expect(RiTa.conjugator.unconjugate("went")).eq("go");
    expect(RiTa.conjugator.unconjugate("met")).eq("meet");
    expect(RiTa.conjugator.unconjugate("have")).eq("have");
    expect(RiTa.conjugator.unconjugate("eat")).eq("eat");
    expect(RiTa.conjugator.unconjugate("play")).eq("play");
    expect(RiTa.conjugator.unconjugate("go")).eq("go");
    expect(RiTa.conjugator.unconjugate("do")).eq("do");
    expect(RiTa.conjugator.unconjugate("spooning")).eq("spoon");
    expect(RiTa.conjugator.unconjugate("mepanning")).eq("mepan");
    expect(RiTa.conjugator.unconjugate("muddling")).eq("muddle");
    if (typeof NOLEX !== "undefined") {
      expect(RiTa.conjugator.unconjugate("gets")).eq("get");
      expect(RiTa.conjugator.unconjugate("comes")).eq("come");
      expect(RiTa.conjugator.unconjugate("goes")).eq("go");
      expect(RiTa.conjugator.unconjugate("teaches")).eq("teach");
      expect(RiTa.conjugator.unconjugate("fixes")).eq("fix");
      expect(RiTa.conjugator.unconjugate("misses")).eq("miss");
      expect(RiTa.conjugator.unconjugate("studies")).eq("study");
      expect(RiTa.conjugator.unconjugate("tries")).eq("try");
      expect(RiTa.conjugator.unconjugate("carries")).eq("carry");
      expect(RiTa.conjugator.unconjugate("wishes")).eq("wish");
      expect(RiTa.conjugator.unconjugate("blitzes")).eq("blitz");
      expect(RiTa.conjugator.unconjugate("watered")).eq("water");
      expect(RiTa.conjugator.unconjugate("pulled")).eq("pull");
      expect(RiTa.conjugator.unconjugate("picked")).eq("pick");
      expect(RiTa.conjugator.unconjugate("liked")).eq("like");
      expect(RiTa.conjugator.unconjugate("moved")).eq("move");
      expect(RiTa.conjugator.unconjugate("tasted")).eq("taste");
      expect(RiTa.conjugator.unconjugate("tried")).eq("try");
      expect(RiTa.conjugator.unconjugate("studied")).eq("study");
      expect(RiTa.conjugator.unconjugate("carried")).eq("carry");
      expect(RiTa.conjugator.unconjugate("digged")).eq("dig");
      expect(RiTa.conjugator.unconjugate("flagged")).eq("flag");
      expect(RiTa.conjugator.unconjugate("raining")).eq("rain");
      expect(RiTa.conjugator.unconjugate("coming")).eq("come");
      expect(RiTa.conjugator.unconjugate("having")).eq("have");
      expect(RiTa.conjugator.unconjugate("running")).eq("run");
      expect(RiTa.conjugator.unconjugate("putting")).eq("put");
      expect(RiTa.conjugator.unconjugate("sitting")).eq("sit");
      expect(RiTa.conjugator.unconjugate("pulling")).eq("pull");
    }
    expect(RiTa.conjugator.unconjugate("bitten")).eq("bite");
    expect(RiTa.conjugator.unconjugate("broken")).eq("break");
    expect(RiTa.conjugator.unconjugate("committed")).eq("commit");
    expect(RiTa.conjugator.unconjugate("computerized")).eq("computerize");
    expect(RiTa.conjugator.unconjugate("concerned")).eq("concern");
    expect(RiTa.conjugator.unconjugate("discriminated")).eq("discriminate");
    expect(RiTa.conjugator.unconjugate("ended")).eq("end");
    expect(RiTa.conjugator.unconjugate("expected")).eq("expect");
    expect(RiTa.conjugator.unconjugate("finished")).eq("finish");
    expect(RiTa.conjugator.unconjugate("gained")).eq("gain");
    expect(RiTa.conjugator.unconjugate("gotten")).eq("get");
    expect(RiTa.conjugator.unconjugate("increased")).eq("increase");
    expect(RiTa.conjugator.unconjugate("involved")).eq("involve");
    expect(RiTa.conjugator.unconjugate("launched")).eq("launch");
    expect(RiTa.conjugator.unconjugate("led")).eq("lead");
    expect(RiTa.conjugator.unconjugate("lived")).eq("live");
    expect(RiTa.conjugator.unconjugate("outpaced")).eq("outpace");
    expect(RiTa.conjugator.unconjugate("overseen")).eq("oversee");
    expect(RiTa.conjugator.unconjugate("paled")).eq("pale");
    expect(RiTa.conjugator.unconjugate("prepaid")).eq("prepay");
    expect(RiTa.conjugator.unconjugate("pressured")).eq("pressure");
    expect(RiTa.conjugator.unconjugate("proliferated")).eq("proliferate");
    expect(RiTa.conjugator.unconjugate("remade")).eq("remake");
    expect(RiTa.conjugator.unconjugate("reopened")).eq("reopen");
    expect(RiTa.conjugator.unconjugate("reported")).eq("report");
    expect(RiTa.conjugator.unconjugate("sold")).eq("sell");
    expect(RiTa.conjugator.unconjugate("resold")).eq("resell");
    expect(RiTa.conjugator.unconjugate("settled")).eq("settle");
    expect(RiTa.conjugator.unconjugate("started")).eq("start");
    expect(RiTa.conjugator.unconjugate("were")).eq("be");
    expect(RiTa.conjugator.unconjugate("bitten")).eq("bite");
    expect(RiTa.conjugator.unconjugate("broken")).eq("break");
    expect(RiTa.conjugator.unconjugate("owned")).eq("own");
    expect(RiTa.conjugator.unconjugate("planned")).eq("plan");
    expect(RiTa.conjugator.unconjugate("rented")).eq("rent");
    expect(RiTa.conjugator.unconjugate("repurchased")).eq("repurchase");
    expect(RiTa.conjugator.unconjugate("roasted")).eq("roast");
    expect(RiTa.conjugator.unconjugate("busted")).eq("bust");
    expect(RiTa.conjugator.unconjugate("grown")).eq("grow");
    expect(RiTa.conjugator.unconjugate("blown")).eq("blow");
    expect(RiTa.conjugator.unconjugate("heard")).eq("hear");
  });
  it("Should conjugate verbs", function() {
    let opt = {
      number: RiTa.SINGULAR,
      person: RiTa.FIRST,
      tense: RiTa.PAST
    };
    expect(RiTa.conjugate("bite", opt)).eq("bit");
    expect(RiTa.conjugate("break", opt)).eq("broke");
    expect(RiTa.conjugate("call", opt)).eq("called");
    expect(RiTa.conjugate("commit", opt)).eq("committed");
    expect(RiTa.conjugate("computerize", opt)).eq("computerized");
    expect(RiTa.conjugate("concern", opt)).eq("concerned");
    expect(RiTa.conjugate("discriminate", opt)).eq("discriminated");
    expect(RiTa.conjugate("end", opt)).eq("ended");
    expect(RiTa.conjugate("expect", opt)).eq("expected");
    expect(RiTa.conjugate("finish", opt)).eq("finished");
    expect(RiTa.conjugate("gain", opt)).eq("gained");
    expect(RiTa.conjugate("get", opt)).eq("got");
    expect(RiTa.conjugate("increase", opt)).eq("increased");
    expect(RiTa.conjugate("involve", opt)).eq("involved");
    expect(RiTa.conjugate("launch", opt)).eq("launched");
    expect(RiTa.conjugate("lead", opt)).eq("led");
    expect(RiTa.conjugate("live", opt)).eq("lived");
    expect(RiTa.conjugate("concern", opt)).eq("concerned");
    expect(RiTa.conjugate("oversee", opt)).eq("oversaw");
    expect(RiTa.conjugate("pale", opt)).eq("paled");
    expect(RiTa.conjugate("prepay", opt)).eq("prepaid");
    expect(RiTa.conjugate("pressure", opt)).eq("pressured");
    expect(RiTa.conjugate("proliferate", opt)).eq("proliferated");
    expect(RiTa.conjugate("remake", opt)).eq("remade");
    expect(RiTa.conjugate("reopen", opt)).eq("reopened");
    expect(RiTa.conjugate("report", opt)).eq("reported");
    expect(RiTa.conjugate("resell", opt)).eq("resold");
    expect(RiTa.conjugate("settle", opt)).eq("settled");
    expect(RiTa.conjugate("start", opt)).eq("started");
    opt = {
      tense: RiTa.PRESENT,
      number: RiTa.SINGULAR,
      perfect: true
    };
    expect(RiTa.conjugate("bite", opt)).eq("have bitten");
    expect(RiTa.conjugate("break", opt)).eq("have broken");
    expect(RiTa.conjugate("build", opt)).eq("have built");
    expect(RiTa.conjugate("enter", opt)).eq("have entered");
    expect(RiTa.conjugate("own", opt)).eq("have owned");
    expect(RiTa.conjugate("plan", opt)).eq("have planned");
    expect(RiTa.conjugate("rent", opt)).eq("have rented");
    expect(RiTa.conjugate("repurchase", opt)).eq("have repurchased");
    expect(RiTa.conjugate("roast", opt)).eq("have roasted");
  });
  it("Should handle stem lookup correctly", function() {
    const conj = RiTa.conjugator;
    ["be", "been", "goes", "running", "walked", "bettering"].forEach((w) => {
      expect(conj._handleStem(w)).eq(w);
    });
    expect(conj._handleStem("alien")).eq("alienate");
    expect(conj._handleStem("bath")).eq("bathe");
    expect(conj._handleStem("central")).eq("centralize");
  });
  it("Should invalidate the stem cache on lexicon swap", function() {
    const conj = RiTa.conjugator;
    const orig = RiTa.lexicon.data;
    try {
      const before = conj._handleStem("alien");
      expect(before).eq("alienate");
      expect(conj._stemCache.size).to.be.above(0);
      RiTa.lexicon.data = { ...orig };
      conj._handleStem("alien");
      expect(conj._stemCacheRef).to.equal(RiTa.lexicon.data);
      expect(conj._stemCache.size).to.equal(1);
      expect(conj._handleStem("alien")).eq(before);
    } finally {
      RiTa.lexicon.data = orig;
    }
  });
});
