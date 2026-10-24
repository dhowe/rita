<a href="https://www.npmjs.com/package/rita"><img src="https://img.shields.io/npm/v/rita.svg" alt="npm version"></a> <a href="http://www.gnu.org/licenses/gpl-3.0.en.html"><img src="https://img.shields.io/badge/license-GPL-orange.svg" alt="npm version"></a> <img src="https://img.shields.io/badge/%E2%99%A8_ai--free-100%25-green" alt="100% ai-free">


## RiTa: tools for generative natural language

```
rita/
  js/        JavaScript implementation
  java/      Java implementation (gradle)
  python/    Python implementation (uv)
  docs/      Website and API reference
  shared/    Shared data (dict, lts, etc.)
  scripts/   Various maintenance scripts
```

The shared API reference is [here](https://rednoise.org/rita/index.html#reference)

---

## JavaScript (`js/`)

**Requirements:** Node.js 18+, npm

```sh
cd js
npm install          # install dependencies
npm run build        # build dist/ (ESM, CJS, IIFE bundles)
npm test             # run tests against src/
npm run test:dist    # run tests against built dist/
```

The build uses [tsup](https://tsup.egoist.dev/) and outputs to `js/dist/`:
- `dist/rita.js` — ESM
- `dist/rita.cjs` — CommonJS
- `dist/rita.min.js` — IIFE (browser)

---

## Java (`java/`)

**Requirements:** JDK 17+ (Gradle wrapper included)

```sh
cd java
./gradlew build                # compile, test, and assemble rita.{jar,zip,txt,pdex}
./gradlew test                 # run tests only
./gradlew processingLibrary    # build/distributions/rita.zip (Processing library)
./gradlew javadoc              # reference docs (also bundled into rita.zip)
```

The artifact is `org.rednoise:rita`. The dictionary is read directly from
`shared/rita_dict.json` (staged into the build by `gradlew syncSharedData`), so there
is no generated copy to sync.

---

## Python (`python/`)

Install the published package from PyPI (import name `rita`):

```sh
pip install rita-py
```

**Requirements for development:** [uv](https://docs.astral.sh/uv/) (Python 3.10+; 
managed by `python/pyproject.toml` + `python/uv.lock`)

```sh
cd python
uv sync              # create .venv and install the package + dev deps (pytest)
uv run pytest -q     # run the test suite
uv build             # build the sdist + wheel for PyPI (dist/)
```

The package is pure Python with no runtime dependencies. The rita dictionary ships
inside the wheel (`rita/data/rita_dict.json`, staged from `shared/rita_dict.json` by
`node scripts/gen-dicts.js`); in a repo checkout the canonical `shared/rita_dict.json`
is preferred, so both work from any working directory.

To publish a new version to PyPI, bump `version` in `python/pyproject.toml` (alongside
the js/java versions), commit, and push a `vX.Y.Z` tag: `.github/workflows/python-publish.yml`
builds and publishes via PyPI trusted publishing (OIDC — no token in the repo).

The pytest suite under `python/tests/` is **generated** from the JavaScript tests
in `js/test/` by `scripts/js-to-py-tests.js` — do not edit `test_*.py` by hand. To
regenerate after changing `js/test/` (requires `npm install` in `js/` for acorn):

```sh
node scripts/js-to-py-tests.js
```

Some tests read fixture files from `js/test/` (e.g. `harvard-data.json`), so keep the
`js/` checkout present when running the Python suite.

---

## Docs / Website (`docs/`)

The `docs/pub` folder is a static website. `scripts/gen-docs.sh` regenerates the API
reference (`docs/pub/reference/`) and the homepage index from the Java sources; the rest
of the site (tutorials, gallery, examples, assets) is authored in place. To preview
locally, use 'Go Live' in vscode or python:

```sh
cd docs/pub
python3 -m http.server 8080
# open http://localhost:8080
```

---

## Shared dictionary (`shared/`)

`shared/rita_dict.json` is the source for the RiTa lexicon. All three implementations use it:

- **JS** — generated module wrapper, `js/src/rita_dict.js`
- **Java** — loaded from the jar as `/rita/rita_dict.json`, staged from `shared/` by `syncSharedData`
- **Python** — copied to `rita/data/rita_dict.json` for the wheel; a checkout prefers `shared/`

To regenerate the JS wrapper and the Python data copy after editing `shared/rita_dict.json`:

```sh
node scripts/gen-dicts.js
```

`shared/rita_lts.json` is the other shared file (generated from `js/src/rita_lts.js` by
`node scripts/gen-lts.js`) and is staged into the Java jar the same way.

---

## CI

GitHub Actions workflows trigger when their subtree (or `shared/`) changes:

| Workflow | Trigger paths | Node/JDK/Python versions |
|---|---|---|
| `.github/workflows/js.yml` | `js/**`, `shared/**` | Node 18, 20, 22 |
| `.github/workflows/java.yml` | `java/**`, `shared/**` | JDK 17 · ubuntu |
| `.github/workflows/python.yml` | `python/**`, `shared/**` | Python 3.10–3.13 (uv) |

---

## Releasing

`scripts/release.sh` does an end-to-end release, writing the various versions into the places 
they live, builds and tests, publishes to npm (for `all`/`js`), commits + tags + pushes, and
creates the GitHub release with the Processing artifacts.

```sh
scripts/release.sh 4.1.0            # three ports: tag, GitHub release, npm, PyPI (from the tag)
scripts/release.sh 4.1.0 java       # Java/Processing only (no npm publish)
scripts/release.sh 4.1.0 js         # JavaScript/npm only
scripts/release.sh 4.1.0 python     # PyPI (rita-py) only
scripts/release.sh 4.1.0 --dry-run  # print what will happen, touch nothing
```

The version lives in the files below (everything else is derived at build time):

| File | Field | Notes |
|---|---|---|
| `java/gradle.properties` | `version=X` | drives `library.properties` (`version=410`, `prettyVersion=4.1.0`) |
| `java/src/main/java/rita/RiTa.java` | `VERSION = "X"` | |
| `js/package.json` | `"version": "X"` | `npm version` also fixes `package-lock.json` |
| `js/src/rita.js` | injected by tsup | from `package.json` at build time |
| `python/pyproject.toml` | `version = "X"` | written by `release.sh`; hatchling reads it |

Checks: the tree must be clean and on `main`; the tag must not already exist; the patch
must stay `< 10` for Java (the Processing Manager revision is `major*100 + minor*10 +
patch`, so `4.0.10` would collide with `4.1.0`); prereleases (`X.Y.Z-beta.N`) are npm-only
because the Java revision can't be derived from a dotted prerelease.

## Contributors

### Code Contributors

This project exists only because of the people who contribute. Thank you!
<a href="https://github.com/dhowe/rita/graphs/contributors"><img src="https://opencollective.com/rita/contributors.svg?width=890&button=false" /></a>

### Financial Contributors
<a href="https://opencollective.com/rita/donate" target="_blank">
  <img src="https://opencollective.com/rita/contribute/button@2x.png?color=blue" width=300 />
</a>