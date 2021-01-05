#!/bin/sh

set -e

rita4j=../rita4j
ritajs=../ritajs

POM=$rita4j/pom.xml
PKG=$ritajs/package.json

echo "... checking environment"

check_err() {
    local exit_code=$1
    shift
    [[ $exit_code ]] &&
    ((exit_code != 0)) && {
        printf '\nFATAL: %s\n' "$@" >&2
        exit "$exit_code"
    }
}

[[ ! -f $POM ]] && check_err 1 "expected java repo at $rita4j"
[[ ! -f $PKG ]] && check_err 1 "expected js repo at $ritajs"

pushd $ritajs >/dev/null
VERSION=`npx npe version`
STATUS=`git status -s`
[[ $STATUS ]] && check_err 1 "uncommitted changes in $ritajs: $STATUS"
popd >/dev/null

pushd $rita4j >/dev/null
JAVAVER=`grep version $POM | grep -v -e '<?xml|~'| head -n 1 | sed 's/[[:space:]]//g' \
| sed -E 's/<.{0,1}version>//g' | awk '{print $1}'`
STATUS=`git status -s`
[[ $STATUS ]] && check_err 1 "uncommitted changes in $rita4j: $STATUS"
popd >/dev/null

if [ "$JAVAVER" != "$VERSION" ]; then # check versions are same
    check_err 1 "version mismatch JAVA:$JAVAVER JS:$VERSION"
fi

echo "... valid -> v$VERSION"
exit 0;
