#!/bin/sh

set -e

RITA_JAVA=../RiTa2
RITA_JS=../rita2js

POM=$RITA_JAVA/pom.xml
PKG=$RITA_JS/package.json

DO_CHECK=true
DO_BUILD=true

echo "\n... checking environment"
if [ "$DO_CHECK" = true ] ; then

  if [[ ! -f $POM ]] ; then
    echo FATAL: expected java repo at $RITA_JAVA
    exit
  fi

  if [[ ! -f $PKG ]] ; then
    echo FATAL: expected js repo at $RITA_JS
    exit
  fi

  pushd $RITA_JAVA >/dev/null
  JAVAVER=`mvn help:evaluate -Dexpression=project.version -q -DforceStdout`
  popd >/dev/null

fi

pushd $RITA_JS >/dev/null
VERSION=$(node -p -e "require('$PKG').version")
popd >/dev/null

if [ "$DO_CHECK" = true ] ; then
  if [ "$JAVAVER" != "$VERSION" ]; then
    echo "FATAL: version mismatch $JAVAVER != $VERSION"
    exit
  fi
fi


echo "... found version $VERSION"

if [ "$DO_BUILD" = true ] ; then

  # build.test JavaScript
  pushd $RITA_JS >/dev/null
  echo "... building js"
  yarn build >/dev/null
  echo "... testing js"
  yarn test.prod >/dev/null
  popd >/dev/null

  # build.test Java
  echo "... packaging java"
  pushd $RITA_JAVA >/dev/null
  mvn clean package >/dev/null
  popd >/dev/null
fi


# build.test Java
echo "... moving resources"
mkdir -p dist/download
cp $RITA_JAVA/target/*.jar dist/download
cp $RITA_JS/dist/*.js  dist/download

echo "... finished\n"
ls -l dist/download
