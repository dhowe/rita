#!/bin/sh

set -e

start=`date +%s`

# paths
tmp="/tmp"
pub="./pub"
rita4j="../rita4j"
ritajs="../ritajs"
pom="$rita4j/pom.xml"
pkg="$ritajs/package.json"
artifacts="./artifacts"
jsdist="$ritajs/dist"
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
        ;;
    esac
done

if [ "$nopub" = true ] ; then         # build website
    echo "\n... publish disabled (use -p)"
fi

if [ -z $version ] ; then
    ./scripts/check-env.sh || check_err $? "env check failed"
    pushd $ritajs >/dev/null
    version=`npx npe version`
    popd >/dev/null
else
    ./scripts/bump-vers.sh $version || check_err $? "bump-vers.sh failed"
fi

[ -z $version ] && check_err 1 "No version found or supplied"

if [ "$nowww" = false ] ; then         # build website
    ./scripts/build-site.sh || check_err $? "build-site.sh failed"
fi

[ "$nojs" = true ] && [ "$nojava" = true ] && check_err 1 "nothing to do"

if [ "$nojs" = false ] ; then         # build.test JavaScript
    
    echo "... building with yarn"
    yarn --cwd  $ritajs build >/dev/null || check_err $? "yarn build failed"
    
    echo "... testing with yarn"
    yarn --cwd  $ritajs test.prod >/dev/null || check_err $? "yarn tests failed"
    
    echo "... packaging with npm"
    rm -rf $ritajs/rita-*.tgz
    pushd $ritajs >/dev/null
    npm pack --quiet >/dev/null || check_err $? "npm pack failed"
    popd >/dev/null
fi

#echo "... cleaning $artifacts"
[[ -d $artifacts ]] || mkdir $artifacts
rm -f $artifacts/*.* >/dev/null

publive=false
if [ "$nojs" = false ] ; then  # publish js to npm/unpkg
    
    if [ "$nopub" = false ] ; then
        echo
        read -p "publish $version to npm/github/maven? " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]] ; then
            publive=true
            echo "... git-tag js $version"
            pushd $ritajs >/dev/null
            git tag -a v$version -m "Release $version"
            git push -q origin --tags
            NPM_TAR=rita-$version.tgz
            echo "... deploying to npm"
            npm publish $NPM_TAR --quiet || check_err $? "npm publish failed"
            popd >/dev/null
            mv $ritajs/*.tgz $artifacts
        else
            echo Exiting 1
            exit 1;
        fi
    fi
    
    # clean previous versions
    compgen -G $artifacts/*.js >/dev/null && mv $artifacts/*.js $tmp
    compgen -G $artifacts/*.tgz >/dev/null && mv $artifacts/*.tgz $tmp
    
    # copy new versions to artifacts
    compgen -G $jsdist/*.js >/dev/null && cp $jsdist/*.js $artifacts
    compgen -G $ritajs/*.tgz >/dev/null && mv $ritajs/*.tgz $artifacts
    
    # copy new web js to pub/examples/lib
    compgen -G $jsdist/rita*.js >/dev/null && cp $jsdist/rita*.js $pubdist
fi

if [ "$nojava" = false ] ; then       # publish java to github packages
    if [ "$nopub" = false ] ; then
        #echo
        #read -p "publish java $version to github? " -n 1 -r
        #echo
        #if [[ $REPLY =~ ^[Yy]$ ]] ; then
        if [ "$publive" = true ] ; then
            pushd $rita4j >/dev/null
            echo "... git-tag java $version"
            git tag -a v$version -m "Release $version"
            git push -q origin --tags
            echo "... deploying to github packages"
            mvn -q -T1C clean deploy || check_err $? "maven publish failed [github]"
            popd >/dev/null
        fi
        #echo
        #read -p "publish java $version to maven central? " -n 1 -r
        #echo
        #if [[ $REPLY =~ ^[Yy]$ ]] ; then
        if [ "$publive" = true ] ; then
            pushd $rita4j >/dev/null
            echo "... deploying to maven central"
            mvn -q -T1C -Pcentral clean deploy || check_err $? "maven publish failed [central]"
            popd >/dev/null
        fi
    else
        pushd $rita4j >/dev/null
        echo "... creating maven packages"
        mvn -q -T1C clean package || check_err $? "maven build failed"
        popd >/dev/null
    fi
    # remove previous versions
    rm -rf $artifacts/rita-*.jar $artifacts/rita-*.pom $artifacts/rita-*.asc 2>/dev/null
    compgen -G $rita4j/target/rita-$version* >/dev/null && cp \
    $rita4j/target/rita-$version* $artifacts
fi

# create processing library
if [ "$noproc" = false ] && [ "$nojava" = false ] ; then
    ./scripts/build-plib.sh $version || check_err $? "build-plib.sh failed"
    cp "$artifacts/rita-$version-plib.zip" "$pub/rita.zip"
    cp "$artifacts/rita.txt" "$pub/rita.txt"
fi

if [ "$zipart" = true ] ; then  # skip artifact zip
    echo "... zipping artifacts"
    zipfile=rita-$version-all.zip
    rm -f rita-$version-all.zip 2>/dev/null
    pushd $artifacts >/dev/null
    zip ../$zipfile ./* >/dev/null
    popd >/dev/null
fi

if [ "$nopub" = false ] ; then
    echo "... updating https://rednoise.org/rita "
    ssh $RED "cd bin && ./update-rita-web.sh" >/dev/null

    echo "... tagging ritaweb"
    git add .
    git tag -a v$version -m "Release $version"
    git commit -q -m "Release $version"
    git push -q
fi


echo "... cleaning up"
#rm -rf $ritajs/*.tgz

runtime=$((`date +%s`-start))

echo "... done in ${runtime}s\n"

