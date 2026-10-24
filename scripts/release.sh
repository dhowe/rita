#!/usr/bin/env bash
#
# release.sh — cut a RiTa release from the mono-repo.
#
# Usage:  scripts/release.sh <version> [all|java|js|python]... [--dry-run]
#
#   scripts/release.sh 4.1.0            # all ports: tag, GitHub release, npm, PyPI
#   scripts/release.sh 4.1.0 java       # Java/Processing only (no npm publish)
#   scripts/release.sh 4.1.0 js         # npm only
#   scripts/release.sh 4.1.0 python     # PyPI (rita-py) only
#   scripts/release.sh 4.1.0 --dry-run  # print what would happen, touch nothing
#
# What it does, in order:
#   1. Validate the tree (clean, on main, tools present, version sane)
#   2. Write the version into every place it lives (see "Version sources" below)
#   3. Build + test the selected ports
#   4. Commit "release: X", tag vX, push main + tag   (git first: reversible)
#   5. Publish to npm            (only for all/js)     (irreversible, so after git)
#   6. Create the GitHub release with the Processing artifacts
#
# PyPI publishing is not done here: pushing the vX.Y.Z tag triggers
# .github/workflows/python-publish.yml, which builds and publishes rita-py via
# PyPI trusted publishing (OIDC). So a python/all release just needs the tag.
#
# Version sources (all bumped together, nothing is generated into git):
#   java/gradle.properties              version=X        -> drives library.properties
#                                                        (version=404 / prettyVersion=4.0.4
#                                                         are expanded at build time)
#   java/src/main/java/rita/RiTa.java   VERSION = "X"
#   js/package.json                     "version": "X"   -> npm version also fixes
#   js/package-lock.json                                 package-lock for us
#   js/src/rita.js                      injected from package.json by tsup at build
#   python/pyproject.toml               version = "X"    -> published to PyPI as rita-py
#
# Notes:
#   * The Java port cannot carry a prerelease version: build.gradle.kts derives the
#     Processing Manager revision by splitting on '.', so 4.1.0-beta.1 would fail to
#     build. Prereleases are therefore npm-only (java excluded).
#   * Processing Manager polls .../releases/latest/download/rita.txt, so every GitHub
#     release carries the Processing artifacts. For a js-only release the Java version
#     is unchanged, so the attached zip is the current Java build — a warning is shown.
#   * Requires: git, gh (authenticated), node/npm (js), uv (python), JDK 17+ for java.

set -euo pipefail

# ---------------------------------------------------------------------------
# Args
# ---------------------------------------------------------------------------

usage() {
  cat <<'EOF'
release.sh — cut a RiTa release from the mono-repo.

Usage:  scripts/release.sh <version> [all|java|js|python]... [--dry-run]

  scripts/release.sh 4.1.0            # all ports: tag, GitHub release, npm, PyPI
  scripts/release.sh 4.1.0 java       # Java/Processing only (no npm publish)
  scripts/release.sh 4.1.0 js         # npm only
  scripts/release.sh 4.1.0 python     # PyPI (rita-py) only
  scripts/release.sh 4.1.0 --dry-run  # print what would happen, touch nothing

Order: validate -> write version -> build+test -> commit "release: X" + tag vX +
       push -> npm publish (all/js) -> GitHub release with the Processing
       artifacts (rita.zip / rita.txt / rita.pdex). PyPI publish (all/python)
       runs automatically from the tag via .github/workflows/python-publish.yml.

Prereleases (X.Y.Z-beta.N) are npm-only; java requires a plain X.Y.Z because
the Processing Manager revision is derived by splitting the version on '.'.
EOF
}

VERSION=""
DRY_RUN=0
TARGETS=()

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    -h|--help) usage; exit 0 ;;
    all|java|js|python) TARGETS+=("$arg") ;;
    -*) echo "release.sh: unknown option '$arg'" >&2; usage; exit 1 ;;
    *) if [[ -n "$VERSION" ]]; then echo "release.sh: version given twice" >&2; usage; exit 1; fi; VERSION="$arg" ;;
  esac
done

[[ -n "$VERSION" ]] || { usage; exit 1; }

# "all" subsumes the rest; no targets means "all".
if [[ ${#TARGETS[@]} -eq 0 ]] || printf '%s\n' "${TARGETS[@]}" | grep -qx all; then
  TARGETS=(java js python)
fi
# De-duplicate while preserving order.
UNIQUE_TARGETS=()
for t in "${TARGETS[@]}"; do
  printf '%s\n' "${UNIQUE_TARGETS[@]:-}" | grep -qx "$t" || UNIQUE_TARGETS+=("$t")
done
TARGETS=("${UNIQUE_TARGETS[@]}")

DO_JAVA=0; DO_JS=0; DO_PYTHON=0
printf '%s\n' "${TARGETS[@]}" | grep -qx java && DO_JAVA=1
printf '%s\n' "${TARGETS[@]}" | grep -qx js && DO_JS=1
printf '%s\n' "${TARGETS[@]}" | grep -qx python && DO_PYTHON=1

TAG="v$VERSION"
if [[ "$VERSION" == *-* ]]; then NPM_DIST_TAG="beta"; PRERELEASE=1; else NPM_DIST_TAG="latest"; PRERELEASE=0; fi

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

say()  { printf '\n\033[1m== %s\033[0m\n' "$*"; }
info() { printf '   %s\n' "$*"; }
warn() { printf '   \033[33m! %s\033[0m\n' "$*"; }
die()  { printf '\n\033[31mrelease.sh: %s\033[0m\n\n' "$*" >&2; exit 1; }

# Run a command, or just announce it under --dry-run.
run() {
  if [[ $DRY_RUN -eq 1 ]]; then
    printf '   \033[36m[dry-run]\033[0m %s\n' "$*"
  else
    printf '   $ %s\n' "$*"
    "$@"
  fi
}

# Portable in-place edit: apply a sed program, then assert it changed something.
#   edit <file> <sed-program> <expected-substring-after>
edit() {
  local file="$1" program="$2" expect="$3"
  if [[ $DRY_RUN -eq 1 ]]; then
    printf '   \033[36m[dry-run]\033[0m edit %s\n' "$file"
    return 0
  fi
  sed -E "$program" "$file" > "$file.tmp" && mv "$file.tmp" "$file"
  grep -qF "$expect" "$file" || die "edit of $file did not produce '$expect'"
}

# ---------------------------------------------------------------------------
# 1. Validate
# ---------------------------------------------------------------------------

say "1/6 Validating"

command -v git >/dev/null || die "git not found"
command -v gh  >/dev/null || die "gh not found — needed for the GitHub release"
if [[ $DO_JS -eq 1 ]]; then command -v npm >/dev/null || die "npm not found"; fi
if [[ $DO_PYTHON -eq 1 ]]; then command -v uv >/dev/null || die "uv not found — needed for the python port"; fi

if [[ $DRY_RUN -eq 0 ]]; then
  gh auth status >/dev/null 2>&1 || die "gh is not authenticated — run 'gh auth login'"
fi

# Version must be plain X.Y.Z for java, and may carry a prerelease for js only.
if [[ $VERSION =~ ^([0-9]+)\.([0-9]+)\.([0-9]+)$ ]]; then
  MAJOR="${BASH_REMATCH[1]}"; MINOR="${BASH_REMATCH[2]}"; PATCH="${BASH_REMATCH[3]}"
elif [[ $VERSION =~ ^([0-9]+)\.([0-9]+)\.([0-9]+)-[0-9A-Za-z.-]+$ ]]; then
  MAJOR="${BASH_REMATCH[1]}"; MINOR="${BASH_REMATCH[2]}"; PATCH="${BASH_REMATCH[3]}"
  if [[ $DO_JAVA -eq 1 ]]; then
    die "prerelease '$VERSION' cannot be used for java: build.gradle.kts derives the
     Processing Manager revision by splitting the version on '.', so 4.1.0-beta.1
     fails to compile. Release java as a plain X.Y.Z, or use 'js' only."
  fi
  warn "prerelease version — npm dist-tag will be '$NPM_DIST_TAG'"
else
  die "'$VERSION' is not a valid version (expected X.Y.Z or X.Y.Z-pre.N)"
fi

# Processing Manager's revision is major*100 + minor*10 + patch, so patch must stay < 10
# or two releases collide (4.0.10 and 4.1.0 would both be 410).
if [[ $DO_JAVA -eq 1 && $PATCH -ge 10 ]]; then
  die "patch $PATCH is >= 10: the Processing Manager revision (major*100+minor*10+patch)
     would collide with the next minor. Use 4.$((MINOR + 1)).0 instead."
fi

REVISION=$((MAJOR * 100 + MINOR * 10 + PATCH))

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
[[ "$BRANCH" == "main" ]] || die "on branch '$BRANCH', but releases must be cut from main"

if [[ -n "$(git status --porcelain)" ]]; then
  git status --short
  die "working tree is not clean — commit or stash first"
fi

if git rev-parse -q --verify "refs/tags/$TAG" >/dev/null || \
   git ls-remote --exit-code --tags origin "refs/tags/$TAG" >/dev/null 2>&1; then
  die "tag $TAG already exists — pick a different version"
fi

CURRENT_JAVA="$(sed -nE 's/^version=//p' java/gradle.properties)"
CURRENT_JS="$(node -p "require('./js/package.json').version")"
CURRENT_PY="$(sed -nE 's/^version = "([^"]*)"/\1/p' python/pyproject.toml)"

info "version      $VERSION  (Processing Manager revision $REVISION)"
info "targets      ${TARGETS[*]}"
info "java         $CURRENT_JAVA -> $([[ $DO_JAVA -eq 1 ]] && echo "$VERSION" || echo "$CURRENT_JAVA (unchanged)")"
info "js           $CURRENT_JS -> $([[ $DO_JS -eq 1 ]] && echo "$VERSION" || echo "$CURRENT_JS (unchanged)")"
info "python       $CURRENT_PY -> $([[ $DO_PYTHON -eq 1 ]] && echo "$VERSION" || echo "$CURRENT_PY (unchanged)")"
info "branch       $BRANCH"
info "dry-run      $([[ $DRY_RUN -eq 1 ]] && echo yes || echo no)"

# ---------------------------------------------------------------------------
# 2. Write the version everywhere it lives
# ---------------------------------------------------------------------------

say "2/6 Setting version"

if [[ $DO_JAVA -eq 1 ]]; then
  edit java/gradle.properties "s/^version=.*/version=$VERSION/" "version=$VERSION"
  edit java/src/main/java/rita/RiTa.java \
       "s/(public static final String VERSION = \")[^\"]*(\")/\1$VERSION\2/" \
       "VERSION = \"$VERSION\""
  info "java/gradle.properties, java/src/main/java/rita/RiTa.java"
  info "java/library.properties is expanded from gradle.properties at build time"
fi

if [[ $DO_JS -eq 1 ]]; then
  # npm version rewrites package.json + package-lock.json in one go, and is the only
  # sanctioned way to touch the lockfile's own version fields.
  if [[ $DRY_RUN -eq 1 ]]; then
    printf '   \033[36m[dry-run]\033[0m npm version %s --no-git-tag-version (in js/)\n' "$VERSION"
  else
    (cd js && npm version "$VERSION" --no-git-tag-version --allow-same-version >/dev/null)
  fi
  info "js/package.json + js/package-lock.json"
  info "js/src/rita.js gets its version injected from package.json by tsup"
fi

if [[ $DO_PYTHON -eq 1 ]]; then
  edit python/pyproject.toml "s/^version = \"[^\"]*\"/version = \"$VERSION\"/" "version = \"$VERSION\""
  info "python/pyproject.toml (published to PyPI as rita-py)"
fi

# ---------------------------------------------------------------------------
# 3. Build + test
# ---------------------------------------------------------------------------

say "3/6 Building and testing"

JAVA_DIST="$ROOT/java/build/distributions"

# The Processing artifacts are attached to every release (see header note), so the Java
# build runs even for a js-only release.
if [[ $DRY_RUN -eq 1 ]]; then
  printf '   \033[36m[dry-run]\033[0m ./gradlew clean build (in java/)\n'
else
  (cd java && ./gradlew clean build --no-daemon -q)
  for f in rita.zip rita.txt rita.pdex; do
    [[ -f "$JAVA_DIST/$f" ]] || die "build did not produce $f"
  done
  # The build's own checkLibraryVersion task already compares these, but verify here too.
  grep -q "^version=$REVISION$" "$JAVA_DIST/rita.txt" || die "rita.txt version != $REVISION"
  grep -q "^prettyVersion=$VERSION$" "$JAVA_DIST/rita.txt" || die "rita.txt prettyVersion != $VERSION"
  info "java: rita.zip / rita.txt / rita.pdex built, metadata verified"
fi

if [[ $DO_JS -eq 1 ]]; then
  if [[ $DRY_RUN -eq 1 ]]; then
    printf '   \033[36m[dry-run]\033[0m npm run build && npm test (in js/)\n'
  else
    (cd js && npm run build >/dev/null && npm test >/dev/null 2>&1)
    # tsup injects the version into the bundles; confirm it took.
    if [[ -f js/dist/rita.min.js ]]; then
      grep -qF "\"$VERSION\"" js/dist/rita.min.js || die "js/dist/rita.min.js does not carry $VERSION"
    fi
    info "js: dist/ built, tests pass, bundles carry $VERSION"
  fi
fi

if [[ $DO_PYTHON -eq 1 ]]; then
  if [[ $DRY_RUN -eq 1 ]]; then
    printf '   \033[36m[dry-run]\033[0m uv sync --frozen && uv run python -m pytest -q && uv build (in python/)\n'
  else
    # 'python -m pytest' rather than the 'pytest' shim: the shim's shebang holds the
    # absolute path of the venv it was built in, so it breaks if the checkout moves.
    (cd python && uv sync --frozen >/dev/null && uv run python -m pytest -q >/dev/null && uv build >/dev/null)
    ls python/dist/rita_py-"$VERSION"-py3-none-any.whl >/dev/null 2>&1 \
      || die "python build did not produce rita_py-$VERSION wheel"
    info "python: tests pass, rita_py-$VERSION wheel built (published from the tag by CI)"
  fi
fi

# ---------------------------------------------------------------------------
# 4. Commit + tag + push
#
# Git first: it is the source of truth and reversible, so a later npm failure can be
# unwound by deleting the tag. npm (irreversible) and the GitHub release come after.
# ---------------------------------------------------------------------------

say "4/6 Commit, tag, push"

STAGED=()
[[ $DO_JAVA -eq 1 ]] && STAGED+=(java/gradle.properties java/src/main/java/rita/RiTa.java)
[[ $DO_JS -eq 1 ]] && STAGED+=(js/package.json js/package-lock.json)
[[ $DO_PYTHON -eq 1 ]] && STAGED+=(python/pyproject.toml)

run git add -- "${STAGED[@]}"
run git commit -m "release: $VERSION"
run git tag "$TAG"
run git push origin main
run git push origin "$TAG"

# ---------------------------------------------------------------------------
# 5. npm publish
# ---------------------------------------------------------------------------

if [[ $DO_JS -eq 1 ]]; then
  say "5/6 Publishing to npm (dist-tag: $NPM_DIST_TAG)"
  # npm publish resolves package.json from the *current* directory and ignores --prefix,
  # so it must run inside js/ rather than via `npm --prefix js publish`.
  if [[ $DRY_RUN -eq 1 ]]; then
    printf '   \033[36m[dry-run]\033[0m (cd js && npm publish --tag %s)\n' "$NPM_DIST_TAG"
  else
    (cd js && npm publish --tag "$NPM_DIST_TAG")
  fi
else
  say "5/6 Skipping npm publish (${TARGETS[*]} only)"
fi

# ---------------------------------------------------------------------------
# 6. GitHub release
# ---------------------------------------------------------------------------

say "6/6 GitHub release"

ASSETS=("$JAVA_DIST/rita.zip" "$JAVA_DIST/rita.txt" "$JAVA_DIST/rita.pdex")
GH_ARGS=(release create "$TAG" --verify-tag --title "RiTa $VERSION" --generate-notes)
[[ $PRERELEASE -eq 1 ]] && GH_ARGS+=(--prerelease)
GH_ARGS+=("${ASSETS[@]}")

run gh "${GH_ARGS[@]}"

if [[ $DO_JAVA -eq 0 && $DO_JS -eq 1 ]]; then
  warn "js-only release: the attached Processing artifacts are still Java $CURRENT_JAVA."
  warn "They keep .../releases/latest/download/rita.txt valid for Processing Manager."
fi

say "Done — RiTa $VERSION"
printf '   release   https://github.com/dhowe/rita/releases/tag/%s\n' "$TAG"
printf '   artifacts https://github.com/dhowe/rita/releases/latest/download/rita.{zip,txt,pdex}\n'
[[ $DO_JS -eq 1 ]] && printf '   npm       https://www.npmjs.com/package/rita (%s)\n' "$NPM_DIST_TAG"
[[ $DO_PYTHON -eq 1 ]] && printf '   pypi      https://pypi.org/project/rita-py/ (published by python-publish.yml on tag %s)\n' "$TAG"
[[ $DRY_RUN -eq 1 ]] && printf '\n   (dry run — nothing was written, pushed, or published)\n'
