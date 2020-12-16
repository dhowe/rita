#!/bin/bash

[ ! -f /bin/docgen/MakeDocs.class ] && echo "...compiling" && ant build
java -classpath ./bin:./lib/core3.5.3.jar docgen.MakeDocs "$@"
