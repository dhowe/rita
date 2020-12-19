#!/bin/bash

set -e

dest="./pub"

# clean
echo ... cleaning $dest
rm -rf $dest 2>/dev/null
mkdir $dest

# copy ws
echo ... making website 
cp -rf www/* $dest

# do docs
echo ... generating docs 
pushd docgen >/dev/null
error=`./generate-docs.sh --silent`
exitv=$?
#echo exitval=$exitv

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


