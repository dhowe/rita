# RiTa — mono-repo

This repository contains all RiTa implementations and documentation

```
rita4/
  js/        JavaScript/TypeScript implementation
  java/      Java implementation (gradle)
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


## Docs / Website (`docs/`)

The `docs/` folder is a static website — no build step required. To preview locally use 'Go Live' in vscode or python:

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

GitHub Actions workflows are path-scoped and trigger when their subtree (or `shared/`) changes:

| Workflow | Trigger paths | Node/JDK/Python versions |
|---|---|---|
| `.github/workflows/js.yml` | `js/**`, `shared/**` | Node 18, 20, 22 |
| `.github/workflows/java.yml` | `java/**`, `shared/**` | JDK 11 · ubuntu + macOS |

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
