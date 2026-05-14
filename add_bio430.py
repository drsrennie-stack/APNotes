#!/usr/bin/env python3
"""Update COURSE_MAP in every unit HTML file:
   - Add BIO 430 (A&P I) entry
   - Rename BIO 431 to BIO 431 A&P II
Idempotent: skips files already updated.
"""
import os, re, sys

OUTPUTS_DIR = os.path.dirname(os.path.abspath(__file__))

UNIT_FILES = [
    "intro-notes.html",
    "chemistry-biochemistry-notes.html",
    "cells-notes.html",
    "tissues-notes.html",
    "integumentary-notes.html",
    "skeletal-notes.html",
    "muscular-notes.html",
    "nervous-notes.html",
    "endocrine-notes.html",
    "blood-hematology-notes.html",
    "cardiovascular-notes.html",
    "lymphatic-immune-notes.html",
    "respiratory-notes.html",
    "gi-notes.html",
    "renal-notes.html",
    "reproductive-notes.html",
]

BIO431_OLD = "BIO 431 Human Anatomy & Physiology · American River College"
BIO431_NEW = "BIO 431 Human Anatomy & Physiology II · American River College"

BIO430_ENTRY = "'BIO430':{eyebrow:'BIO 430 Human Anatomy & Physiology I · American River College',view:'combined',depth:'full'},"

# Regex matches the BIO431 entry start; we prepend BIO430 before it.
# Pattern accepts the leading quote, BIO431, optional whitespace, colon.
BIO431_START_RE = re.compile(r"('BIO431'\s*:\s*\{)")


def process_file(path):
    name = os.path.basename(path)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "'BIO430'" in content:
        return f"SKIP (already has BIO430): {name}"

    if BIO431_OLD not in content:
        return f"WARN (BIO431 eyebrow not found verbatim): {name}"

    # 1) Update BIO 431 label to include II
    content_new = content.replace(BIO431_OLD, BIO431_NEW)

    # 2) Insert BIO 430 entry before BIO431 in the COURSE_MAP object
    if not BIO431_START_RE.search(content_new):
        return f"FAIL (could not locate BIO431 key): {name}"

    content_new = BIO431_START_RE.sub(BIO430_ENTRY + r"\1", content_new, count=1)

    if content_new == content:
        return f"NO-OP: {name}"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content_new)

    return f"OK: {name}"


def main():
    out = []
    for n in UNIT_FILES:
        p = os.path.join(OUTPUTS_DIR, n)
        out.append(process_file(p) if os.path.exists(p) else f"MISSING: {n}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
