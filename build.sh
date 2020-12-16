#!/bin/bash

# clean
rm -rf dist/*

# copy ws
cp -r www/* dist/

# do docs
docgen/generate-docs.sh


