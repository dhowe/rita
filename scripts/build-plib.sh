#!/bin/bash

function help {
    echo; echo "Usage: $(basename $0) <version>"
}

function check_err {
    local exit_code=$1
    shift
    [[ $exit_code ]] && ((exit_code != 0)) && {
        printf '\nFATAL: %s\n' "$@" >&2
        exit "$exit_code"
    }
}

[ "$1" = "help" ] && help && exit 1

openproc=false
version=$1  #${1:-XXX}
ritajava="../rita"
pom="pom.xml"

if [ -z "$version" ]; then
   pushd $ritajava >/dev/null
   version=`grep version $pom | grep -v -e '<?xml|~'| head -n 1 | sed 's/[[:space:]]//g' | sed -E 's/<.{0,1}version>//g' | awk '{print $1}'`
   popd >/dev/null
   echo ... found version $version
fi

dest="./artifacts"
zipfile="rita-$version-plib.zip"
plibs="$HOME/Documents/Processing/libraries/"
tmp="/tmp/rita"
lib="$tmp/library"

echo "... creating library for processing"
rm -rf $tmp 2>/dev/null
mkdir -p $tmp/library

echo "... updating library.properties"
cp -r library.properties  $tmp
sed -i '' "s/##version##/$version/" $tmp/library.properties
sed -i '' "s/##versionnum##/${version//./}/" $tmp/library.properties
cp -r $tmp/library.properties $dest/rita.txt

echo "... copying reference, examples"
cp -r pub/reference $tmp 
cp -r $ritajava/examples/processing $tmp/examples

echo "... copying source, javadocs"
cp -r $dest/rita-$version-sources.jar  $tmp/source.jar || check_err $? "cp sources failed"
cp -r $dest/rita-$version-javadoc.jar  $tmp/javadoc.jar || check_err $? "cp javadocs failed"

echo "... compiling rita.jar with deps"
(cd $ritajava && mvn -q compile assembly:single) || check_err $? "maven compile failed"
cp -r $ritajava/target/rita-$version-jar-with-dependencies.jar  $lib/rita.jar

echo "... zipping processing library"
rm -f $dest/$zipfile 2>/dev/null 
(cd $tmp/.. && zip -q -r - rita) > $dest/$zipfile

echo "... moving to libraries"
rm -rf $plibs/rita 2>/dev/null
mv $tmp $plibs

if [ "$openproc" = true ] ; then
  echo "... (re)starting Processing"
  killall Processing 2>/dev/null
  sleep 3
  open $ritajava/examples/processing/RandomRhymes/RandomRhymes.pde
fi

exit 0;


