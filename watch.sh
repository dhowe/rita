#!/bin/sh

find data -name '*.json' | entr ./run.sh
