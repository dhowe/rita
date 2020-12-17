#!/bin/sh

find ./docgen ./www  -name '*' | entr ./build-www.sh
