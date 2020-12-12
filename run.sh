#!/bin/sh
rm -rf ./ref
java -classpath ./bin:./lib/core3.5.3.jar docgen.MakeDocs
cp -r static ref/
ls -l ref
