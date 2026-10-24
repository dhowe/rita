<a href="https://www.npmjs.com/package/rita"><img src="https://img.shields.io/npm/v/rita.svg" alt="npm version"></a> <a href="http://www.gnu.org/licenses/gpl-3.0.en.html"><img src="https://img.shields.io/badge/license-GPL-orange.svg" alt="npm version"></a> <img src="https://img.shields.io/badge/%E2%99%A8_ai--free-100%25-green" alt="100% ai-free">


## RiTa: tools for generative natural language

This repository contains all RiTa implementations and documentation

```
rita/
  js/        JavaScript implementation
  java/      Java implementation (gradle)
  python/    Python implementation (uv)
  docs/      Website and API reference
  shared/    Shared data (rita_dict.json)
  scripts/   Various maintenance scripts
```

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

**Requirements:** JDK 11+ (Gradle wrapper included)

```sh
cd java
./gradlew build                # compile, test, and assemble rita.jar + rita.zip
./gradlew test                 # run tests only
./gradlew processingLibrary    # build/distributions/rita.zip (Processing library)
./gradlew javadoc              # reference docs (also bundled into rita.zip)
```

The artifact is `org.rednoise:rita`. The canonical dictionary is read directly from
`shared/rita_dict.json` (staged into the build by `gradlew processResources`), so there
is no generated copy to keep in sync.

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

The `docs/` folder is a static website — no build required. To preview locally use 'Go Live' in vscode or python:

```sh
cd docs
python3 -m http.server 8080
# open http://localhost:8080
```

Reference pages are in `docs/reference/` and tutorials in `docs/tutorials/`. Both are hand-authored HTML.

---

## Shared dictionary (`shared/`)

`shared/rita_dict.json` is the source for the RiTa lexicon. All three implementations use it:

- **JS / Java** — use JS-module wrappers (`js/src/rita_dict.js`, `java/src/main/resources/rita/rita_dict.js`)

To regenerate the JS/Java wrappers after editing `shared/rita_dict.json`:

```sh
node scripts/gen-dicts.js
```

---

## CI

GitHub Actions workflows trigger when their subtree (or `shared/`) changes:

| Workflow | Trigger paths | Node/JDK/Python versions |
|---|---|---|
| `.github/workflows/js.yml` | `js/**`, `shared/**` | Node 18, 20, 22 |
| `.github/workflows/java.yml` | `java/**`, `shared/**` | JDK 11 · ubuntu + macOS |
| `.github/workflows/python.yml` | `python/**`, `shared/**` | Python 3.10–3.13 (uv) |

---

## Releasing

`scripts/release.sh` does an end-to-end release, writing the various versions into the places 
they live, builds and tests, publishes to npm (for `all`/`js`), commits + tags + pushes, and
creates the GitHub release with the Processing artifacts.

```sh
scripts/release.sh 4.1.0            # both ports: tag, GitHub release, npm
scripts/release.sh 4.1.0 java       # Java/Processing only (no npm publish)
scripts/release.sh 4.1.0 js         # npm only
scripts/release.sh 4.1.0 --dry-run  # print what would happen, touch nothing
```

The version lives in exactly these files (everything else is derived at build time):

| File | Field | Notes |
|---|---|---|
| `java/gradle.properties` | `version=X` | drives `library.properties` (`version=410`, `prettyVersion=4.1.0`) |
| `java/src/main/java/rita/RiTa.java` | `VERSION = "X"` | |
| `js/package.json` | `"version": "X"` | `npm version` also fixes `package-lock.json` |
| `js/src/rita.js` | injected by tsup | from `package.json` at build time |

Checks: the tree must be clean and on `main`; the tag must not already exist; the patch
must stay `< 10` for Java (the Processing Manager revision is `major*100 + minor*10 +
patch`, so `4.0.10` would collide with `4.1.0`); prereleases (`X.Y.Z-beta.N`) are npm-only
because the Java revision can't be derived from a dotted prerelease.
