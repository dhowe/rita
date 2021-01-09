#!/bin/bash

# compile grammar if needed (via ant)
[ ! -f /bin/docgen/MakeDocs.class ] && echo "...compiling" && ant build

# generate the documentation
java -classpath ./bin:./lib/core3.5.3.jar docgen.MakeDocs "$@"
