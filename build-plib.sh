#!/bin/bash

function help {
    echo "Usage: $(basename $0) <version>"
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
   help; #exit 1
fi

version=${1:-XXX}
rita_java="../RiTa2"
zipfile="rita-$version-proc.zip"
tmp="/tmp/rita"
lib="$tmp/library"
dest="./artifacts"

echo "... cleaning $tmp"
rm -rf $tmp 2>/dev/null
mkdir -p $tmp/library

echo "... updating library.properties"
cp -r library.properties  $tmp
sed -i '' "s/##version##/$version/" $tmp/library.properties
sed -i '' "s/##versionnum##/${version//./}/" $tmp/library.properties
cp -r $tmp/library.properties $dest/rita.txt

echo "... copying reference, examples"
cp -r pub/reference pub/examples $tmp 

echo "... copying source, javadocs"
cp -r $dest/rita-$version-sources.jar  $tmp/source.jar
cp -r $dest/rita-$version-javadoc.jar  $tmp/javadoc.jar

echo "... compiling jar with-deps"
pushd $rita_java >/dev/null
mvn -q compile assembly:single || check_err $? "maven compile failed"
cp -r target/rita-$version-jar-with-dependencies.jar  $lib/rita.jar
popd >/dev/null

#echo && ls -l $tmp $lib

echo "... zipping library"
rm -f $dest/$zipfile 2>/dev/null 
(cd $tmp/.. && zip -r - rita) > $dest/$zipfile

ls -l $dest
jar tf $dest/$zipfile

exit 0;


