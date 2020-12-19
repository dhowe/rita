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

if [ -z "$1" ] || [ "$1" = "help" ]; then
   help; exit 1
fi

version=$1  #${1:-XXX}
rita_java="../RiTa2"
zipfile="rita-$version-plib.zip"
plibs="$HOME/Documents/Processing/libraries/"
tmp="/tmp/rita"
lib="$tmp/library"
dest="./artifacts"
openproc=false

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
cp -r $rita_java/examples/processing $tmp/examples

echo "... copying source, javadocs"
cp -r $dest/rita-$version-sources.jar  $tmp/source.jar
cp -r $dest/rita-$version-javadoc.jar  $tmp/javadoc.jar

echo "... compiling rita.jar with deps"
(cd $rita_java && mvn -q compile assembly:single) || check_err $? "maven compile failed"
cp -r $rita_java/target/rita-$version-jar-with-dependencies.jar  $lib/rita.jar

echo "... zipping processing library"
rm -f $dest/$zipfile 2>/dev/null 
(cd $tmp/.. && zip -q -r - rita) > $dest/$zipfile

echo "... moving to libraries"
rm -rf $plibs/rita 2>/dev/null
mv $tmp $plibs

#temp stuff
#open $plibs/rita
#echo && ls -l $tmp $lib
if [ "$openproc" = true ] ; then
  killall Processing
  sleep 1
  open $rita_java/examples/
fi

exit 0;


