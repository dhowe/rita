# rita — Python port of RiTa

RiTa is a library for computational language and generative writing, handling syllables,
phonemes and stresses, parts of speech, conjugation, pluralization, stemming,
letter-to-sound mapping, rhyming and alliteration, plus unbounded n-gram generation and
the RiScript scripting language for context-free grammars.

This is the Python port of [RiTa](https://rednoise.org/rita) from the original js - 
see the shared API reference [here](https://rednoise.org/rita/index.html#reference).

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

# RiScript
RiTa.evaluate("the [big | small] [dog | cat]")   # "the small dog"
```

## Notes
- Pure Python, no runtime dependencies. Python 3.10+
- Free/libre and licensed under GPL-3.0

## Development

The build is managed with [uv](https://docs.astral.sh/uv/):

```sh
uv sync              # create .venv and install dev deps
uv run pytest -q     # run the test suite
```