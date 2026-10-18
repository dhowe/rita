# RiTa — mono-repo

This repository contains all RiTa implementations and documentation

```
rita4/
  js/        JavaScript/TypeScript implementation
  java/      Java implementation (gradle)
  python/    Python implementation
  docs/      Website and API reference
  shared/    Shared data (rita_dict.json — canonical dictionary)
  scripts/   Maintenance scripts
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

**Requirements:** Python 3.10+

```sh
cd python
python -m venv .venv && source .venv/bin/activate   # optional virtualenv
pip install pytest
pytest -q            # run all tests
```

No package installation is required to run tests directly from the repo.

---

## Docs / Website (`docs/`)

The `docs/` folder is a static website — no build step required. To preview locally:

```sh
cd docs
python3 -m http.server 8080
# open http://localhost:8080
```

Reference pages are in `docs/reference/` and tutorials in `docs/tutorials/`. Both are hand-authored HTML.

---

## Shared dictionary (`shared/`)

`shared/rita_dict.json` is the source for the RiTa lexicon. All three implementations use it:

- **Python** — loaded at runtime via a `__file__`-relative path in each module
- **JS / Java** — use JS-module wrappers (`js/src/rita_dict.js`, `java/src/main/resources/rita/rita_dict.js`)

To regenerate the JS/Java wrappers after editing `shared/rita_dict.json`:

```sh
node scripts/gen-dicts.js
```

---

## CI

GitHub Actions workflows are path-scoped and trigger when their subtree (or `shared/`) changes:

| Workflow | Trigger paths | Node/JDK/Python versions |
|---|---|---|
| `.github/workflows/js.yml` | `js/**`, `shared/**` | Node 18, 20, 22 |
| `.github/workflows/java.yml` | `java/**`, `shared/**` | JDK 11 · ubuntu + macOS |
| `.github/workflows/python.yml` | `python/**`, `shared/**` | 3.10, 3.11, 3.12, 3.13 |
