#!/bin/sh

set -e

RITA_JAVA=../RiTa2
RITA_JS=../rita2js

POM=$RITA_JAVA/pom.xml
PKG=$RITA_JS/package.json

echo "\n... checking environment"

check_err() {
    local exit_code=$1
    shift
    [[ $exit_code ]] &&
    ((exit_code != 0)) && {
        printf '\nFATAL: %s\n' "$@" >&2
        exit "$exit_code"
    }
}

[[ ! -f $POM ]] && check_err 1 "expected java repo at $RITA_JAVA"
[[ ! -f $PKG ]] && check_err 1 "expected js repo at $RITA_JS"

pushd $RITA_JS >/dev/null
VERSION=`npx npe version`
STATUS=`git status -s`
[[ $STATUS ]] && check_err 1 "uncommitted changes in $RITA_JS: $STATUS"
popd >/dev/null

pushd $RITA_JAVA >/dev/null
JAVAVER=`grep version $POM | grep -v -e '<?xml|~'| head -n 1 | sed 's/[[:space:]]//g' \
| sed -E 's/<.{0,1}version>//g' | awk '{print $1}'`
STATUS=`git status -s`
[[ $STATUS ]] && check_err 1 "uncommitted changes in $RITA_JAVA: $STATUS"
popd >/dev/null

if [ "$JAVAVER" != "$VERSION" ]; then # check versions are same
    check_err 1 "version mismatch JAVA:$JAVAVER JS:$VERSION"
fi

echo "... valid -> v$VERSION"
exit 0;
