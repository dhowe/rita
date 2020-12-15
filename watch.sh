#!/bin/sh

find data src/docgen css static -name '*.*' | entr ./make-ref.sh
