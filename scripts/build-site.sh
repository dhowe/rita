#!/bin/bash

set -e

dest="./pub"
ritajs="../ritajs"

# clean
[[ -d $dest ]] || mkdir $dest

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


