#!/bin/bash

set -e

tmp="/tmp"
dest="./pub"
ritajs="../ritajs"

# move aside rita.txt and rita.zip if we have them
compgen -G $dest/rita.txt >/dev/null && mv $dest/rita.txt $tmp
compgen -G $dest/rita.zip >/dev/null && mv $dest/rita.zip $tmp

# clean
rm -rf $dest
mkdir $dest && mkdir $dest/dist

# move aside rita.txt and rita.zip if we have them
compgen -G $tmp/rita.txt >/dev/null && mv $tmp/rita.txt $dest
compgen -G $tmp/rita.zip >/dev/null && mv $tmp/rita.zip $dest

# copy ws
echo ... making website 
cp -r www/* $dest

# if we have built js move it into website (for examples)
compgen -G $ritajs/dist/rita*.js >/dev/null && cp $ritajs/dist/rita*.js $dest/dist/

# do docs
echo ... generating docs 
pushd docgen >/dev/null
error=`./generate-docs.sh --silent`
exitv=$?

# check for errors
if [ $exitv -eq 0 ]; then
  echo ... wrote www to $dest
else
  echo
  echo "Site build failed ***"
  exit $exitv;
fi 

popd >/dev/null

exit 0;


