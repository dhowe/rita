#!/bin/sh

set -e

RITA_JAVA=../RiTa2
RITA_JS=../rita2js


POM=$RITA_JAVA/pom.xml
PKG=$RITA_JS/package.json

DO_CHECK=true
DO_BUILD=true
DO_JAVA=false

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
if [ "$DO_CHECK" = true ] && [ "$DO_JAVA" = true ] ; then
  [[ ! -f $POM ]] && check_err 1 "expected java repo at $RITA_JAVA"
  [[ ! -f $PKG ]] && check_err 1 "expected js repo at $RITA_JS"
  #JAVAVER=`mvn help:evaluate -Dexpression=project.version -q -DforceStdout` # too slow!
  JAVAVER=`grep version $POM | grep -v -e '<?xml|~'| head -n 1 | sed 's/[[:space:]]//g' \
    | sed -E 's/<.{0,1}version>//g' | awk '{print $1}'`
fi

VERSION=`node -p -e "require('$PKG').version"`

# check versions are same
if [ "$DO_CHECK" = true ] && [ "$DO_JAVA" = true ] && [ "$JAVAVER" != "$VERSION" ]; then 
  check_err 1 "version mismatch JAVA:$JAVAVER JS:$VERSION"
fi

echo "... found v$VERSION"

if [ "$DO_BUILD" = true ] ; then

  # build.test JavaScript
  echo "... building with yarn"
  yarn --cwd  $RITA_JS build >/dev/null || check_err $? "yarn build failed"
fi

echo "... testing with yarn"
yarn --cwd  $RITA_JS test.prod >/dev/null || check_err $? "yarn tests failed"
echo "... packaging with yarn"
yarn --cwd  $RITA_JS pack >/dev/null || check_err $? "yarn pack failed"

if [ "$DO_BUILD" = true ] ; then
  # build.test Java
  if [ "$DO_JAVA" = true ] ; then
    echo "... build/test java with maven"
    pushd $RITA_JAVA >/dev/null
    mvn clean package >/dev/null || check_err $? "maven build failed"
    popd >/dev/null
  fi
fi

echo "... moving jar/js/tgz resources"
mkdir -p dist/download
[ "$DO_JAVA" = true ] && cp $RITA_JAVA/target/*.jar dist/download 
cp $RITA_JS/dist/*.js  dist/download
cp $RITA_JS/*.tgz  dist/download

read -p "publish v$VERSION to npm? " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
  # pull from github and link rita.zip
  NPM_TAR=$RITA_JS/rita-v$VERSION.tgz
  echo "... publishing $NPM_TAR to npm"
  npm publish $NPM_TAR || check_err $? "npm publish failed"
  #ssh $RED "cd ~/git/RiTa && git stash && git pull && ./create-symlinks.sh ${VERSION}"
fi

echo "... cleaning up"
#rm -rf $RITA_JS/*.tgz  

echo "... finished\n"
ls -l dist/download
