#!/bin/sh

set -e

RITA_JAVA=../RiTa2
RITA_JS=../rita2js

POM=$RITA_JAVA/pom.xml
PKG=$RITA_JS/package.json

DO_CHECK=true
DO_BUILD=true

check_err() {
  local exit_code=$1
  shift
  [[ $exit_code ]] &&               # do nothing if no error code passed
    ((exit_code != 0)) && {         # do nothing if error code is 0
      printf '\nFATAL: %s\n' "$@" >&2 
      exit "$exit_code"
    }
}

echo "\n... checking environment"
if [ "$DO_CHECK" = true ] ; then
  [[ ! -f $POM ]] && check_err 1 "expected java repo at $RITA_JAVA"
  [[ ! -f $PKG ]] && check_err 1 "expected js repo at $RITA_JS"
  #JAVAVER=`mvn help:evaluate -Dexpression=project.version -q -DforceStdout` # too slow!
  JAVAVER=`grep version $POM | grep -v -e '<?xml|~'| head -n 1 | sed 's/[[:space:]]//g' \
     | sed -E 's/<.{0,1}version>//g' | awk '{print $1}'`
fi

VERSION=`node -p -e "require('$PKG').version"`

# check versions are same
if [ "$DO_CHECK" = true ] && [ "$JAVAVER" != "$VERSION" ]; then 
  check_err 1 "version mismatch JAVA:$JAVAVER JS:$VERSION"
fi

echo "... found v$VERSION"

if [ "$DO_BUILD" = true ] ; then

  # build.test JavaScript
  pushd $RITA_JS >/dev/null
  echo "... building js with yarn"
  yarn build >/dev/null || check_err $? "yarn build failed"
  echo "... testing js with yarn"
  yarn test.prod >/dev/null || check_err $? "yarn tests failed"
  popd >/dev/null

  # build.test Java
  echo "... build/test java with maven"
  pushd $RITA_JAVA >/dev/null
  mvn clean package >/dev/null || check_err $? "maven build failed"
  popd >/dev/null
fi

echo "... moving jar/js resources"
mkdir -p dist/download
cp $RITA_JAVA/target/*.jar dist/download
cp $RITA_JS/dist/*.js  dist/download

echo "... finished\n"
ls -l dist/download
