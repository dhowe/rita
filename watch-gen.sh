#!/bin/sh

find data src/docgen css static -name '*.*' | entr ./generate-docs.sh
