#!/usr/bin/env bash
# Usage: parity.sh <js-test-file> <java-test-file>
# Counts assertions per test block and compares.
JS="$1"; JAVA="$2"
paste \
  <(awk '
      { line=$0 }
      /^ *0 && it\(/{ dis=1; next }
      /^  it\(/{ dis=0; c=0; next }
      /^  \}\);?$/{ if (!dis) print c; next }
      { if (dis) next
        sub(/\/\/.*$/, "", line)
        n=gsub(/expect\(|[^a-zA-Z_.]eql\(|assert\.[a-zA-Z]+\(/, "x", line); c+=n }
    ' "$JS") \
  <(awk '
      /^    @Test/{ if (intest) print c; c=0; intest=1; next }
      /^    (private|public|protected|static).*\(/ { if (intest) print c; c=0; intest=0; next }
      { if (intest) { line=$0; sub(/\/\/.*$/, "", line); n=gsub(/assert[A-Za-z]*\(/, "x", line); c+=n } }
      END { if (intest) print c }
    ' "$JAVA") |
  awk '{print ($1==$2?"OK  ":"DIFF") " js=" $1 " java=" $2}'
