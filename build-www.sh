#!/bin/bash

set -e

# clean
echo
echo ...cleaning dist 
rm -rf dist
mkdir dist

# copy ws
echo ...making website 
cp -rf www/* dist/

# do docs
echo ...generating docs 
cd docgen
error=`./generate-docs.sh --silent`
exitv=$?
#echo exitval=$exitv

# check for errors
if [ $exitv -eq 0 ]; then
  echo
  echo wrote site to ./dist
else
  echo
  echo "Build failed ***"
fi 

cd - >/dev/null


