import { expect } from 'chai';
import { readFileSync } from 'fs';
import { RiTa } from './index.js';

/**
 * RandGen (Mersenne Twister) golden-vector tests.
 *
 * The expected values are generated from js/src/randgen.js by
 * scripts/gen-randgen-fixtures.js and stored in shared/randgen-fixtures.json, so this
 * suite and the Java RandGenTest assert byte-identical output for the same seeds.
 */

const fixtures = JSON.parse(
  readFileSync(new URL('../../shared/randgen-fixtures.json', import.meta.url))
);

const R = RiTa.randomizer;

describe('RandGen', function () {
  this.timeout(10000);

  it('Should reproduce the seeded sequences', function () {
    for (const { seed, values } of fixtures.sequences) {
      R.seed(seed);
      const got = values.map(() => R.random());
      expect(got, 'seed ' + seed).to.eql(values);
    }
  });

  it('Should be reproducible across reseeds', function () {
    R.seed(42);
    const first = Array.from({ length: 10 }, () => R.random());
    R.seed(42);
    const second = Array.from({ length: 10 }, () => R.random());
    expect(first).to.eql(second);
  });

  it('Should differ across seeds', function () {
    R.seed(1);
    const a = Array.from({ length: 10 }, () => R.random());
    R.seed(2);
    const b = Array.from({ length: 10 }, () => R.random());
    expect(a).to.not.eql(b);
  });

  it('Should return floats in [0, 1)', function () {
    R.seed(7);
    for (let i = 0; i < 1000; i++) {
      const v = R.random();
      expect(v).to.be.at.least(0);
      expect(v).to.be.below(1);
    }
  });

  it('Should call pselect', function () {
    expect(function () {
      R.pselect();
    }).to.throw();
    R.seed(1);
    expect(R.pselect([1])).to.equal(0);
    expect(fixtures.pselect.expected).to.eql(
      replay(fixtures.pselect.seed, () => R.pselect(fixtures.pselect.probs))
    );
  });

  it('Should call pselectIndex', function () {
    expect(function () {
      R.pselectIndex();
    }).to.throw();
    R.seed(1);
    expect(R.pselectIndex([1])).to.equal(0);
    expect(fixtures.pselectIndex.expected).to.eql(
      replay(fixtures.pselectIndex.seed, () => R.pselectIndex(fixtures.pselectIndex.probs))
    );
  });

  it('Should call pselect2', function () {
    expect(fixtures.pselect2.expected).to.eql(
      replay(fixtures.pselect2.seed, () => R.pselect2(fixtures.pselect2.weights))
    );
  });

  it('Should call pselectObj', function () {
    expect(function () {
      R.pselectObj();
    }).to.throw();
    expect(fixtures.pselectObj.expected).to.eql(
      replay(fixtures.pselectObj.seed, () => R.pselectObj(fixtures.pselectObj.dist))
    );
  });

  it('Should call ndist', function () {
    expect(() => R.ndist([1, 2, 6, -2.5, 0])).to.throw;
    expect(R.ndist([1, 2, 6, 0])).to.eql(fixtures.ndist.expected);
    expect(R.ndist([1, 2, 3], 0.5)).to.eql(fixtures.ndistTemp.expected);
    expect(R.ndist([1, 2, 3], 1)).to.eql(fixtures.ndistTemp1.expected);
    // sums to 1
    const d = R.ndist([3, 7, 11]);
    expect(d.reduce((a, b) => a + b, 0)).to.be.closeTo(1, 1e-12);
  });

  it('Should call shuffle', function () {
    expect(fixtures.shuffle.expected).to.eql(once(fixtures.shuffle.seed, () => R.shuffle(fixtures.shuffle.input)));
    // is a permutation
    const out = [...fixtures.shuffle.expected].sort((a, b) => a - b);
    expect(out).to.eql(fixtures.shuffle.input);
  });

  it('Should call randomOrdering', function () {
    expect(R.randomOrdering(1)).to.eql([0]);
    expect(R.randomOrdering(['a'])).to.eql(['a']);
    expect(fixtures.randomOrdering.expected).to.eql(
      once(fixtures.randomOrdering.seed, () => R.randomOrdering(fixtures.randomOrdering.k))
    );
    const ro = R.randomOrdering(5);
    expect([...ro].sort((a, b) => a - b)).to.eql([0, 1, 2, 3, 4]);
    expect(function () {
      R.randomOrdering('x');
    }).to.throw();
  });

  it('Should call random with ranges', function () {
    expect(fixtures.random1.expected).to.eql(
      replay(fixtures.random1.seed, () => R.random(fixtures.random1.k))
    );
    expect(fixtures.random2.expected).to.eql(
      replay(fixtures.random2.seed, () => R.random(fixtures.random2.min, fixtures.random2.max))
    );
    expect(fixtures.randomArray.expected).to.eql(
      once(fixtures.randomArray.seed, () => R.random(fixtures.randomArray.array))
    );
  });

  it('Should call randomBias', function () {
    const b = fixtures.randomBias;
    expect(b.expected).to.eql(
      replay(b.seed, () => R.randomBias(b.min, b.max, b.bias, b.influence))
    );
  });

  it('Should honor RiTa.randomSeed', function () {
    RiTa.randomSeed(42);
    const viaRiTa = Array.from({ length: 10 }, () => RiTa.random());
    const expected = fixtures.sequences.find((s) => s.seed === 42).values;
    expect(viaRiTa).to.eql(expected);
  });

  it('Should call randi', function () {
    RiTa.randomSeed(42);
    expect(RiTa.randi(10)).to.equal(3); // floor(0.3745... * 10)
    expect(RiTa.randi(5, 15)).to.equal(12); // floor(0.7965... * 10 + 5)
  });
});

// Seeds, then applies fn 5 times (each call draws from the stream), matching the generator.
function replay(seed, fn) {
  R.seed(seed);
  return Array.from({ length: 5 }, () => fn());
}

// Seeds once and applies fn a single time, for operations that consume the whole stream.
function once(seed, fn) {
  R.seed(seed);
  return fn();
}
