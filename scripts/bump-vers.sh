#!/bin/bash


function help {
    echo "Usage: $(basename $0) [ <version> | major | minor | patch | prerelease]"
}

if [ -z "$1" ] || [ "$1" = "help" ]; then
    help; exit 1
fi

rita4j=../rita4j
ritajs=../ritajs
version=$1

# need to update java version via mvn
# pushd $rita4j >/dev/null
# sed -e "s/__VERSION__/$version/" "./src/main/java/rita/RiTa.java" > /tmp/RiTa.java
# mv -- /tmp/RiTa.java ./src/main/java/rita/RiTa.java
# grep VERSION /tmp/RiTa.java
# popd >/dev/null
# exit

############################# ERRORS ################################
check_err() {
    local exit_code=$1
    shift
    [[ $exit_code ]] &&               # do nothing if no error code passed
    ((exit_code != 0)) && {         # do nothing if error code is 0
        printf '\nFATAL: %s\n' "$@" >&2
        exit "$exit_code"
    }
}

############################# JS ################################
pushd $ritajs >/dev/null
changes=$(git status --porcelain)
if [ -z "${changes}" ]; then
    echo "... bump package.js version"
    npx npe version $version >/dev/null || check_err $? "npe failed [1]"
    git add package.json &> /dev/null || check_err $? "git add failed [1]"
    git commit -q -m "bump to ${version}" &> /dev/null
    git push -q || check_err $? "git push failed [1]"
    #head package.json
    #git tag -a "${output}" -m "${version}"
    #git push origin --tags
    #npm publish ./
else
    echo "Uncommitted changes in JS repo"
fi
popd >/dev/null

############################# JAVA ################################
pushd $rita4j >/dev/null
changes=$(git status --porcelain)
if [ -z "${changes}" ]; then
    #echo "... bump source version"
    #sed -i "s/__VERSION__/$version/" "./src/main/java/rita/RiTa.java"
    echo "... bump pom.xml version"
    mvn versions:set -DnewVersion=$version  >/dev/null || check_err $? "git commit failed [2]"
    git add pom.xml &> /dev/null || check_err $? "git add failed[2]"
    git commit -q -m "bump to ${version}" &> /dev/null
    git push -q || check_err $? "git push failed [2]"
else
    echo "Uncommitted changes in Java repo"
fi
popd >/dev/null

./scripts/check-env.sh


