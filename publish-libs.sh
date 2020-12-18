#!/bin/sh

set -e

DO_JAVA=true
DO_JS=true

RITA_JAVA=../RiTa2
RITA_JS=../rita2js

POM=$RITA_JAVA/pom.xml
PKG=$RITA_JS/package.json

check_err() {
    local exit_code=$1
    shift
    [[ $exit_code ]] &&         
    ((exit_code != 0)) && {
        printf '\nFATAL: %s\n' "$@" >&2
        exit "$exit_code"
    }
}

[ "$DO_JAVA" = false ] && [ "$DO_JS" = false ] && check_err 1 "DO_JAVA and DO_JS false" #change to skip

while getopts "v:" option; do
    case ${option} in
        v) VERSION=$OPTARG
            echo "\n... using version: $VERSION"
        ;;
    esac
done

if [ -z $VERSION ] ; then
    pushd $RITA_JS >/dev/null
    VERSION=`npx npe version`
    ./check-env.sh || check_err $? "env check failed"
    popd >/dev/null
else 
    ./bump-vers.sh $VERSION || check_err $? "bump-vers.sh failed"
fi

[ -z $VERSION ] && check_err 1 "No version found or supplied"

if [ "$DO_JS" = true ] ; then         # build.test JavaScript
    echo "... building with yarn"
    yarn --cwd  $RITA_JS build >/dev/null || check_err $? "yarn build failed"
    
    echo "... testing with yarn"
    yarn --cwd  $RITA_JS test.prod >/dev/null || check_err $? "yarn tests failed"
    
    echo "... packaging for npm"
    rm -rf $RITA_JS/rita-*.tgz
    pushd $RITA_JS >/dev/null
    npm pack --quiet >/dev/null || check_err $? "npm pack failed"
    popd >/dev/null
fi

ARTIFACTS=./pub/download
[[ -d $ARTIFACTS ]] || mkdir $ARTIFACTS

if [ "$DO_JS" = true ] ; then
    echo
    read -p "publish v$VERSION to npm? " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]] ; then
        echo "... git-tag js v$VERSION"
        pushd $RITA_JS >/dev/null
        git tag -a v$VERSION -m "Release v$VERSION"
        git push -q origin --tags
        NPM_TAR=rita-$VERSION.tgz
        echo "... deploying to npm"
        npm publish $NPM_TAR --quiet || check_err $? "npm publish failed"
        popd >/dev/null
        rm -rf $ARTIFACTS/*.js # remove previous versions
        cp $RITA_JS/dist/*.js  $ARTIFACTS
        mv $RITA_JS/*.tgz  $ARTIFACTS
    fi
fi

if [ "$DO_JAVA" = true ] ; then
    echo
    read -p "publish java v$VERSION to github? " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]] ; then
        pushd $RITA_JAVA >/dev/null
        echo "... git-tag java v$VERSION"
        git tag -a v$VERSION -m "Release v$VERSION"
        git push -q origin --tags
        echo "... deploying to github packages"
        mvn -q clean deploy || check_err $? "maven publish failed"
        popd >/dev/null
        # remove previous versions
        rm -rf $ARTIFACTS/rita-*.jar $ARTIFACTS/rita-*.pom $ARTIFACTS/rita-*.asc
        cp $RITA_JAVA/target/rita-$VERSION* $ARTIFACTS
    fi
fi


echo "... cleaning up"
#rm -rf $RITA_JS/*.tgz

echo "... finished\n"
ls -l $ARTIFACTS
