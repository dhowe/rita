#!/bin/bash

set -e
echo not used && exit1

rita_js="../rita2js"

pushd $rita_js >/dev/null
version=`npx npe version`
popd >/dev/null

zipfile="rita-$version-all.zip"
path="~/git/RiTaWeb/pub/download"

[ ! -f $zipfile ] && echo $'\n'"FATAL: $zipfile not found" && exit 1;

scp $zipfile $RED:$path
ssh $RED "cd $path && unzip $zipfile"

