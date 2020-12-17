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

# check version and git status
./check-env.sh || check_err $? "env check failed"
pushd $RITA_JS >/dev/null
VERSION=`npx npe version`
popd >/dev/null

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
#mkdir -p ./dist/download

if [ "$DO_JS" = true ] ; then
    cp $RITA_JS/dist/*.js  ./dist/download
    mv $RITA_JS/*.tgz  ./dist/download
    echo
    read -p "publish v$VERSION to npm? " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]] ; then
        echo "... git-tagging js v$VERSION"
        pushd $RITA_JS >/dev/null
        git tag -a v$VERSION -m "Release v$VERSION"
        git push origin --tags
        popd >/dev/null
        NPM_TAR=dist/download/rita-v$VERSION.tgz
        echo "... publishing $NPM_TAR to npm"
        npm publish $NPM_TAR || check_err $? "npm publish failed"
    fi
fi

if [ "$DO_JAVA" = true ] ; then
    echo
    read -p "deploy java v$VERSION to github? " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]] ; then
        pushd $RITA_JAVA >/dev/null
        echo "... git-tagging java v$VERSION"
        git tag -a v$VERSION -m "Release v$VERSION"
        git push origin --tags
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
