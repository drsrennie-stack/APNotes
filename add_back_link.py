#!/usr/bin/env python3
"""Inject a 'Back to Concept Notes' link into every unit HTML file.
Preserves ?course= URL parameter so students stay in course context.
Idempotent: skips files that already have the link.
"""
import os
import re
import sys

OUTPUTS_DIR = os.path.dirname(os.path.abspath(__file__))

# Files to process (skip index.html itself, skip ap-topic-map.html as legacy)
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
    "foundations-notes.html",  # redirect/landing page
]

# CSS rule to inject before </style>
BACK_LINK_CSS = """
  .back-to-hub { display:inline-flex; align-items:center; gap:6px; font-family:'DM Sans',sans-serif; font-size:13px; font-weight:600; color:var(--terra-dark); text-decoration:none; padding:6px 10px 6px 8px; margin:0 0 14px -8px; border-radius:4px; transition:background-color 150ms ease, color 150ms ease; }
  .back-to-hub:hover, .back-to-hub:focus-visible { background:var(--navy-tint); color:var(--navy); text-decoration:none; outline:none; }
  .back-to-hub:focus-visible { outline:2px solid var(--gold); outline-offset:2px; }
  .back-to-hub .arrow-glyph { font-size:14px; line-height:1; }
  @media print { .back-to-hub { display:none; } }
"""

# HTML to insert at the top of the wrap container
BACK_LINK_HTML = '<a href="index.html" class="back-to-hub" id="back-to-hub-link" aria-label="Back to Concept Notes library"><span class="arrow-glyph" aria-hidden="true">&larr;</span><span>Back to Concept Notes</span></a>\n  '

# JS to insert before </body>
BACK_LINK_JS = """
<script>
/* Preserve ?course= parameter on the back-to-hub link */
(function () {
  var match = /[?&]course=([^&]+)/.exec(window.location.search);
  if (match) {
    var link = document.getElementById('back-to-hub-link');
    if (link) link.setAttribute('href', 'index.html?course=' + encodeURIComponent(match[1]));
  }
})();
</script>
"""

MARKER = 'id="back-to-hub-link"'


def process_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if MARKER in content:
        return f"SKIP (already has back link): {os.path.basename(path)}"

    original = content

    # 1) Inject CSS before </style>
    if "</style>" in content:
        content = content.replace("</style>", BACK_LINK_CSS + "</style>", 1)
    else:
        return f"FAIL (no </style>): {os.path.basename(path)}"

    # 2) Inject HTML after the wrap div opening tag.
    # Try .page-wrap first, then .wrap as fallback.
    page_wrap_pattern = re.compile(r'(<div class="page-wrap"[^>]*>\s*)', re.IGNORECASE)
    wrap_pattern = re.compile(r'(<div class="wrap"[^>]*>\s*)', re.IGNORECASE)

    if page_wrap_pattern.search(content):
        content = page_wrap_pattern.sub(lambda m: m.group(1) + BACK_LINK_HTML, content, count=1)
    elif wrap_pattern.search(content):
        content = wrap_pattern.sub(lambda m: m.group(1) + BACK_LINK_HTML, content, count=1)
    else:
        return f"FAIL (no wrap div): {os.path.basename(path)}"

    # 3) Inject JS before </body>
    if "</body>" in content:
        content = content.replace("</body>", BACK_LINK_JS + "</body>", 1)
    else:
        return f"FAIL (no </body>): {os.path.basename(path)}"

    if content == original:
        return f"NO-OP: {os.path.basename(path)}"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"OK: {os.path.basename(path)}"


def main():
    results = []
    for name in UNIT_FILES:
        path = os.path.join(OUTPUTS_DIR, name)
        if not os.path.exists(path):
            results.append(f"MISSING: {name}")
            continue
        results.append(process_file(path))

    print("\n".join(results))


if __name__ == "__main__":
    main()
