# rita — Python port of RiTa

RiTa is a library for natural language and generative writing: syllables,
phonemes and stresses, parts of speech, conjugation, pluralization, stemming,
letter-to-sound mapping, rhyming and alliteration, plus n-gram generation and
the RiScript scripting language.

This is the Python port of [RiTa](https://rednoise.org/rita), which is written
in JavaScript and Java. The API mirrors the JavaScript one, so JS docs apply.

## Install

```sh
pip install rita-py
```

## Usage

```python
from rita import RiTa

RiTa.tokenize("I'm sure he'll be interested")
# ["I'm", "sure", "he'll", "be", "interested"]

RiTa.syllables("elephant")       # "eh/l-ah/f-ah-n-t"
RiTa.phones("elephant")          # "eh-l-ah-f-ah-n-t"
RiTa.rhymes("cat")               # ["bat", "begat", "brat", "chat", ...]
RiTa.pos("The dog ran")          # ["dt", "nn", "vbd"]

# Generation
markov = RiTa.RiMarkov(2)
markov.add_text("the big dog and the big cat and the small dog")
markov.generate1()               # "the big cat and the big cat and the small dog"

# RiScript
RiTa.evaluate("the [big | small] [dog | cat]")   # "the small dog"
```

## Notes

- Pure Python, no runtime dependencies. Python 3.10+.
- The canonical dictionary (`rita_dict.json`) is bundled with the package.
- Licensed under GPL-3.0, same as the JavaScript and Java implementations.

## Development

The build is managed with [uv](https://docs.astral.sh/uv/):

```sh
uv sync              # create .venv and install dev dependencies
uv run pytest -q     # run the test suite
```

The test suite under `tests/` is auto-generated from the JavaScript tests in
`../js/test/` by `../scripts/js-to-py-tests.js` — regenerate rather than editing
`test_*.py` by hand. Some tests read fixture files from `../js/test/`, so keep
that checkout present when running the suite.
