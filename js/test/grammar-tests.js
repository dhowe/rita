import { expect } from 'chai';

import { RiTa } from './index.js';

describe('Grammar', () => {

  const T = { trace: 1 };

  it('Should call RiTa.grammar() for a blank grammar', function () {
    const rg = RiTa.grammar();
    expect(rg).to.be.an.instanceof(RiTa.RiGrammar);
  });

  it('Should call RiGrammar.fromJSON(rules)', function () {
    const rules = {
      start: "Meet $person.name. $person.pronoun.cap() drives $person.car.art().",
      "#person": "$sam | $lucy"
    }
    const rg = RiTa.RiGrammar.fromJSON(JSON.stringify(rules));
    expect(rg).to.be.an.instanceof(RiTa.RiGrammar);
  });

  it('Should allow constructions from object or string', function () {
    const rules = {
      start: "Meet $person.name. $person.pronoun.cap() drives $person.car.art().",
      "#person": "$sam | $lucy"
    }
    const rg1 = RiTa.grammar(rules);
    const rg2 = RiTa.grammar(JSON.stringify(rules));
    const rg3 = RiTa.RiGrammar.fromJSON(JSON.stringify(rules));
    expect(rg1.toJSON()).to.deep.equal(rg2.toJSON());
    expect(rg1.toJSON()).to.deep.equal(rg3.toJSON());
  });

  // see tests in RiScript/test/grammar-tests.js
  it('Should call RiTa.grammar().expand()', function () {
    const context = {
      lucy: {
        name: 'Lucy',
        pronoun: 'she',
        car: 'Acura'
      },
      sam: {
        name: 'Sam',
        pronoun: 'he',
        car: 'Subaru'
      }
    }
    const rules = {
      start: "Meet $person.name. $person.pronoun.cap() drives $person.car.art().",
      "#person": "$sam | $lucy"
    }
    let result = RiTa.grammar(rules, context).expand();
    expect(result).to.be.oneOf([
      'Meet Lucy. She drives an Acura.',
      'Meet Sam. He drives a Subaru.',
    ]);
  });

  /*LTR*/0 && it('Should reference context from transforms', function () {
    const context = {
      characters: [{
        name: 'Lucy',
        pronoun: 'she',
        car: 'Acura'
      },
      {
        name: 'Sam',
        pronoun: 'he',
        car: 'Subaru'
      }],
      chooseChar: function () {
        console.log('chooseChar:', typeof this);
        return "OK";//RiTa.random(this.context.characters);
      }
    }
    const rules = {
      start: "$person=$chooseChar() $sentence",
      sentence: "$Meet $person.name. $person.pronoun.cap() drives $person.car.art().",
      "#person": "$sam | $lucy"
    }
    let result = RiTa.grammar(rules, context).expand();
    expect(result).to.be.oneOf([
      'Meet Lucy. She drives an Acura.',
      'Meet Sam. He drives a Subaru.',
    ]);
  });
});
