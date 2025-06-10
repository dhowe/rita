#!/bin/sh

# NOTE: requires entr to be installed
# Usage: ./scripts/watch-site.sh [additional arguments for build-site.sh]

find ./docgen ./www  -name '*' | entr ./scripts/build-site.sh $@
