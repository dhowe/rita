#!/bin/bash

set -e

# clean
echo
echo ...cleaning pub 
rm -rf pub
mkdir pub

# copy ws
echo ...making website 
cp -rf www/* pub/

# do docs
echo ...generating docs 
cd docgen
error=`./generate-docs.sh --silent`
exitv=$?
#echo exitval=$exitv

# check for errors
if [ $exitv -eq 0 ]; then
  echo ...wrote to ./pub
else
  echo
  echo "Build failed ***"
fi 

cd - >/dev/null


