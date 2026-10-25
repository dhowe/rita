#!/bin/sh

# rebuilds website on change to data files or templates
# Usage: ./scripts/watch-docs.sh
# NOTE: requires entr to be installed

find ./docs/docgen -name '*' | entr ./scripts/gen-docs.sh $@
