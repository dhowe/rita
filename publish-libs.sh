#!/bin/sh

### port Java examples

set -e

start=`date +%s`

# paths
tmp="/tmp"
pub="./pub"
rita_java="../RiTa2"
rita_js="../rita2js"
pom="$rita_java/pom.xml"
pkg="$rita_js/package.json"
artifacts="./artifacts"
download="$pub/download"
jsdist="$rita_js/dist"
pubdist="$pub/dist"

# options
nojs=false
nojava=false
noproc=false
nowww=false
nopub=true

check_err() {
    local exit_code=$1
    shift
    [[ $exit_code ]] && ((exit_code != 0)) && {
        printf '\nFATAL: %s\n' "$@" >&2
        exit "$exit_code"
    }
}

while getopts "v:p" option; do
    case ${option} in
        v) version=$OPTARG
            echo "\n... using version: $version"
        ;;
        p) nopub=false
            echo "... publish enabled *"
        ;;
    esac
done

if [ "$nopub" = true ] ; then         # build website
    echo "... publish disabled (use -p)"    
fi

if [ -z $version ] ; then
    ./check-env.sh || check_err $? "env check failed"
    pushd $rita_js >/dev/null
    version=`npx npe version`
    popd >/dev/null
else
    ./bump-vers.sh $version || check_err $? "bump-vers.sh failed"
fi

[ -z $version ] && check_err 1 "No version found or supplied"

if [ "$nowww" = false ] ; then         # build website
    ./build-site.sh || check_err $? "build-site.sh failed"
fi

[ "$nojs" = true ] && [ "$nojava" = true ] && check_err 1 "nothing to do"

if [ "$nojs" = false ] ; then         # build.test JavaScript
    
    echo "... building with yarn"
    yarn --cwd  $rita_js build >/dev/null || check_err $? "yarn build failed"
    
    echo "... testing with yarn"
    yarn --cwd  $rita_js test.prod >/dev/null || check_err $? "yarn tests failed"
    
    echo "... packaging with npm"
    rm -rf $rita_js/rita-*.tgz
    pushd $rita_js >/dev/null
    npm pack --quiet >/dev/null || check_err $? "npm pack failed"
    popd >/dev/null
fi

echo "... cleaning $artifacts"
[[ -d $artifacts ]] || mkdir $artifacts
rm -f $artifacts/*.* >/dev/null


if [ "$nojs" = false ] ; then  # publish js to npm/unpkg
    
    if [ "$nopub" = false ] ; then
        echo
        read -p "publish v$version to npm? " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]] ; then
            echo "... git-tag js v$version"
            pushd $rita_js >/dev/null
            git tag -a v$version -m "Release v$version"
            git push -q origin --tags
            NPM_TAR=rita-$version.tgz
            echo "... deploying to npm"
            npm publish $NPM_TAR --quiet || check_err $? "npm publish failed"
            popd >/dev/null
            mv $rita_js/*.tgz  $artifacts
        fi
    fi
    
    # clean previous versions
    compgen -G $artifacts/*.js >/dev/null && mv $artifacts/*.js $tmp
    compgen -G $artifacts/*.tgz >/dev/null && mv $artifacts/*.tgz $tmp
    
    # copy new versions to artifacts
    compgen -G $jsdist/*.js >/dev/null && cp $jsdist/*.js $artifacts
    compgen -G $rita_js/*.tgz >/dev/null && mv $rita_js/*.tgz $artifacts
    
    # copy new web js to pub/examples/lib
    compgen -G $jsdist/rita-web*.js >/dev/null && \
    cp $jsdist/rita-web*.js $pubdist
fi

if [ "$nojava" = false ] ; then       # publish java to github packages
    if [ "$nopub" = false ] ; then
        echo
        read -p "publish java v$version to github? " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]] ; then
            pushd $rita_java >/dev/null
            echo "... git-tag java v$version"
            git tag -a v$version -m "Release v$version"
            git push -q origin --tags
            echo "... deploying to github packages"
            mvn -q -T1C clean deploy || check_err $? "maven publish failed"
            popd >/dev/null
        fi
    else
        pushd $rita_java >/dev/null
        echo "... creating maven packages"
        mvn -q -T1C clean package || check_err $? "maven build failed"
        popd >/dev/null
    fi
    # remove previous versions
    rm -rf $artifacts/rita-*.jar $artifacts/rita-*.pom $artifacts/rita-*.asc 2>/dev/null
    compgen -G $rita_java/target/rita-$version* >/dev/null && cp \
    $rita_java/target/rita-$version* $artifacts
fi

# create processing library
if [ "$noproc" = false ] ; then
    ./build-plib.sh $version || check_err $? "build-plib.sh failed"
    cp "$artifacts/rita-$version-plib.zip" $download
fi

if [ "$zipart" = true ] ; then  # skip artifact zip
    echo "... zipping artifacts"
    zipfile=rita-$version-all.zip
    rm -f rita-$version-all.zip 2>/dev/null
    pushd $artifacts >/dev/null
    zip ../$zipfile ./* >/dev/null
    popd >/dev/null
fi


echo "... cleaning up"
#rm -rf $rita_js/*.tgz

runtime=$((`date +%s`-start))

echo "... done in ${runtime}s\n"

ls -l pub/download
