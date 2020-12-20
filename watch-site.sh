#!/bin/sh

find ./docgen ./www  -name '*' | entr ./build-site.sh
