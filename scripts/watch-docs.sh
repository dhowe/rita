#!/bin/sh

# rebuilds website on change to data files or templates
# Usage: ./scripts/watch-docs.sh
# NOTE: requires entr to be installed

find ./docs/docgen ./docs/pub/css ./docs/pub/examples ./docs/pub/js ./docs/pub/img ./docs/pub/gallery ./docs/pub/font -name '*' | entr ./scripts/gen-docs.sh $@
