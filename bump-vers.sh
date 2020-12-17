#!/bin/bash

function help {
    echo "Usage: $(basename $0) [ <version> | major | minor | patch | prerelease]"
}

if [ -z "$1" ] || [ "$1" = "help" ]; then
    help
    exit
fi

rita_java=../RiTa2
rita_js=../rita2js
version=$1

############################# JS ################################
pushd $rita_js >/dev/null
changes=$(git status --porcelain)
if [ -z "${changes}" ]; then
    npx npe version $version
    git add .
    git commit -m "bump to ${version}"
    git push
    head package.json
    #git tag -a "${output}" -m "${version}"
    #git push origin --tags
    #npm publish ./
else
    echo "Uncommitted changes in JS repo"
fi
popd >/dev/null

############################# JAVA ################################
pushd $rita_java >/dev/null
changes=$(git status --porcelain)
if [ -z "${changes}" ]; then
    mvn versions:set -DnewVersion=$version
    git add .
    git commit -m "bump to ${version}"
    head pom.xml
else
    echo "Uncommitted changes in Java repo"
fi
popd >/dev/null


