#!/usr/bin/env python3
"""Per-block assertion parity checker for the JS -> Java test port.

Usage: python3 parity.sh <js-test-file> <java-test-file>

Segments each file into test blocks (JS: it/it.skip/0&&it; Java: @Test methods)
by brace depth, counts assertion calls inside each, and prints OK/DIFF per block.
"""
import re
import sys


def strip_comment(line):
    # Remove line comments that are not inside a string (heuristic: // not preceded by :).
    out = []
    i = 0
    in_s = None
    while i < len(line):
        ch = line[i]
        if in_s:
            if ch == "\\" and i + 1 < len(line):
                out.append(line[i:i + 2])
                i += 2
                continue
            if ch == in_s:
                in_s = None
            out.append(ch)
        else:
            if ch in "\"'`":
                in_s = ch
                out.append(ch)
            elif ch == "/" and i + 1 < len(line) and line[i + 1] == "/":
                break
            else:
                out.append(ch)
        i += 1
    return "".join(out)


def depth_delta(s):
    # Net brace change, ignoring braces inside strings.
    d = 0
    in_s = None
    i = 0
    while i < len(s):
        ch = s[i]
        if in_s:
            if ch == "\\":
                i += 2
                continue
            if ch == in_s:
                in_s = None
        else:
            if ch in "\"'`":
                in_s = ch
            elif ch == "{":
                d += 1
            elif ch == "}":
                d -= 1
        i += 1
    return d


JS_ASSERT = re.compile(
    r"expect\(|assert\.[a-zA-Z]+\(|"
    r"[^a-zA-Z_.]ok\(|[^a-zA-Z_.]eq\(|[^a-zA-Z_.]eql\(|[^a-zA-Z_.]def\(")
JAVA_ASSERT = re.compile(r"assert[A-Za-z]*\(")


def js_blocks(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        m = re.match(r"^ *0 && (it|it\.skip)\(", raw)
        disabled = bool(m)
        started = re.match(r"^ *(it|it\.skip)\(", raw) or disabled
        if started:
            count = 0
            depth = 0
            # consume from the it( line; track depth from the first {
            j = i
            entered = False
            while j < n:
                line = strip_comment(lines[j])
                if not entered:
                    if "{" in line:
                        depth += depth_delta(line)
                        entered = True
                else:
                    depth += depth_delta(line)
                    count += len(JS_ASSERT.findall(line))
                if entered and depth <= 0:
                    break
                j += 1
            blocks.append((disabled, count))
            i = j + 1
            continue
        i += 1
    return blocks


def java_blocks(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        if re.match(r"^    @Test\b", lines[i]):
            count = 0
            depth = 0
            entered = False
            j = i
            while j < n:
                line = strip_comment(lines[j])
                if not entered:
                    if "{" in line:
                        depth += depth_delta(line)
                        entered = True
                else:
                    depth += depth_delta(line)
                    count += len(JAVA_ASSERT.findall(line))
                if entered and depth <= 0:
                    break
                j += 1
            blocks.append(count)
            i = j + 1
            continue
        i += 1
    return blocks


def main():
    js = js_blocks(sys.argv[1])
    java = java_blocks(sys.argv[2])
    # JS blocks that are disabled (0 &&) have no Java counterpart -> drop them.
    js_active = [c for (dis, c) in js if not dis]
    ok = diff = 0
    for k in range(max(len(js_active), len(java))):
        a = js_active[k] if k < len(js_active) else None
        b = java[k] if k < len(java) else None
        if a == b:
            ok += 1
            print(f"OK   js={a} java={b}")
        else:
            diff += 1
            print(f"DIFF js={a} java={b}")
    print(f"-- {ok} OK, {diff} DIFF  (js blocks={len(js_active)}, java blocks={len(java)})")
    return 0 if diff == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
