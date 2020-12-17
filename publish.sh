#!/bin/sh

DO_JAVA=true
DO_JS=true

RITA_JAVA=../RiTa2
RITA_JS=../rita2js

set -e

POM=$RITA_JAVA/pom.xml
PKG=$RITA_JS/package.json

check_err() {
    local exit_code=$1
    shift
    [[ $exit_code ]] &&               # do nothing if no error code passed
    ((exit_code != 0)) && {         # do nothing if error code is 0
        printf '\nFATAL: %s\n' "$@" >&2
        exit "$exit_code"
    }
}

[ "$DO_JAVA" = false ] && [ "$DO_JS" = false ] && check_err 1 "DO_JAVA and DO_JS false"

echo "\n... checking environment" ###########################################

if [ "$DO_JAVA" = true ] ; then
    
    [[ ! -f $POM ]] && check_err 1 "expected java repo at $RITA_JAVA"
    
    #JAVAVER=`mvn help:evaluate -Dexpression=project.version -q -DforceStdout` # too slow!
    JAVAVER=`grep version $POM | grep -v -e '<?xml|~'| head -n 1 | sed 's/[[:space:]]//g' \
    | sed -E 's/<.{0,1}version>//g' | awk '{print $1}'`
else
    echo "WARN: skipping Java"
fi

if [ "$DO_JS" = true ] ; then
    [[ ! -f $PKG ]] && check_err 1 "expected js repo at $RITA_JS"
    VERSION=`npm view rita version`
    #VERSION=`node -p -e "require('$PKG').version"`
else
    echo "WARN: skipping JavaScript"
fi

# check versions are same
if [ "$DO_JAVA" = true ] && [ "$DO_JS" = true ] && [ "$JAVAVER" != "$VERSION" ]; then
    check_err 1 "version mismatch JAVA:$JAVAVER JS:$VERSION"
fi

# check for git changes             ###########################################
echo "... checking git status"
if [ "$DO_JAVA" = true ] ; then
    pushd $RITA_JS >/dev/null
    STATUS=`git status -s`
    [[ $STATUS ]] && check_err 1 "uncommitted changes in $RITA_JS: $STATUS"
    popd >/dev/null
fi
if [ "$DO_JAVA" = true ] ; then
    pushd $RITA_JAVA >/dev/null
    STATUS=`git status -s`
    [[ $STATUS ]] && check_err 1 "uncommitted changes in $RITA_JAVA: $STATUS"
    popd >/dev/null
fi

[ "$DO_JAVA" = true ] && VERSION=$JAVAVER

echo "... found v$VERSION"         ###########################################
#echo "... cleaning dist/download"
#rm -rf dist/download

if [ "$DO_JS" = true ] ; then         # build.test JavaScript
    echo "... building with yarn"
    yarn --cwd  $RITA_JS build >/dev/null || check_err $? "yarn build failed"
    
    echo "... testing with yarn"
    yarn --cwd  $RITA_JS test.prod >/dev/null || check_err $? "yarn tests failed"
    
    echo "... packaging with yarn"
    rm -rf $RITA_JS/rita-*.tgz
    yarn --cwd  $RITA_JS pack >/dev/null || check_err $? "yarn pack failed"
fi

# if [ "$DO_JAVA" = true ] ; then        # build.test Java
# echo "... build/test java with maven"
# pushd $RITA_JAVA >/dev/null
# mvn clean package >/dev/null || check_err $? "maven build failed"
# popd >/dev/null
# fi

echo "... moving js/tgz resources"      ###########################################
mkdir -p ./dist/download

if [ "$DO_JS" = true ] ; then
    cp $RITA_JS/dist/*.js  ./dist/download
    mv $RITA_JS/*.tgz  ./dist/download
    read -p "publish v$VERSION to npm? " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]] then
        echo "... git-tagging js v$VERSION"
        pushd $RITA_JS >/dev/null
        git tag -a v$VERSION -m "Release v$VERSION"
        git push origin --tags
        popd >/dev/null
        exit
        NPM_TAR=dist/download/rita-v$VERSION.tgz
        echo "... publishing $NPM_TAR to npm"
        npm publish $NPM_TAR || check_err $? "npm publish failed"
        #ssh $RED "cd ~/git/RiTa && git stash && git pull && ./create-symlinks.sh ${VERSION}"
    fi
fi

if [ "$DO_JAVA" = true ] ; then
    read -p "deploy java v$VERSION to github? " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        pushd $RITA_JAVA >/dev/null
        echo "... git-tagging java v$VERSION"
        git tag -a v$VERSION -m "Release v$VERSION"
        git push origin --tags
        popd >/dev/null
        exit
        #mvn clean deploy -Dmaven.test.skip=true
        echo "... deploying to github packages"
        mvn clean deploy || check_err $? "maven publish failed"
        popd >/dev/null
        cp $RITA_JAVA/target/*.jar dist/download
        #ssh $RED "cd ~/git/RiTa && git stash && git pull && ./create-symlinks.sh ${VERSION}"
    fi
fi


echo "... cleaning up"
#rm -rf $RITA_JS/*.tgz

echo "... finished\n"
ls -l dist/download
