#!/bin/sh

find ./docgen ./www  -name '*' | entr ./scripts/build-site.sh $@
