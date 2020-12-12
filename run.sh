#!/bin/sh
rm -rf ./ref
java -classpath ./bin:./lib/core3.5.3.jar docgen.MakeDocs
cp data/POS.html data/RiScript.html ref/
ls -l ref
