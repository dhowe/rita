#!/bin/bash
rm -rf www/reference/
java -classpath ./bin:./lib/core3.5.3.jar docgen.MakeDocs
cp static/* www/reference/
ls -l www/reference
