#!/bin/sh
rm -rf ./ref
java -classpath ./bin:./lib/core3.5.3.jar docgen.MakeDocs
cp static/* ref/
cp -r ref/* ../RiTaWeb/reference/
ls -l ref
