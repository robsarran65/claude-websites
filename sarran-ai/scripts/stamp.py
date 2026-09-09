#!/usr/bin/env python3
"""Content-hash styles.css and main.js, and point every page at the result.

Run this before committing whenever styles.css or main.js changed:

    python scripts/stamp.py

The hashed file IS the source file - there is no build output and no second
copy to keep in sync. Editing styles.<hash>.css works exactly like editing
styles.css did; this script just renames it when the content no longer matches
the hash in its name, and rewrites the <link>/<script> in all 10 pages.

Why bother: vercel.json serves hashed assets with a one-year immutable cache.
That is only safe because the URL changes whenever the bytes change. It also
gives every page one identical URL, so moving from the home page to a service
page no longer re-downloads the same stylesheet under a different cache key.

Idempotent - running it twice in a row is a no-op.
"""

import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HASH_LEN = 10

# (stem, extension, how the file is referenced in HTML)
TARGETS = [("styles", "css"), ("main", "js")]

# styles.css, styles.a1b2c3d4e5.css - but not some-other-styles.css
def _pattern(stem, ext):
    return re.compile(r'^%s(?:\.[0-9a-f]{%d})?\.%s$' % (re.escape(stem), HASH_LEN, re.escape(ext)))


def find_source(stem, ext):
    """The one file on disk for this target. More than one is an error."""
    pat = _pattern(stem, ext)
    hits = [f for f in os.listdir(ROOT) if pat.match(f)]
    if not hits:
        sys.exit("error: no %s.%s (hashed or not) in %s" % (stem, ext, ROOT))
    if len(hits) > 1:
        sys.exit("error: %d candidates for %s.%s - %s\n"
                 "Delete the stale one; only the current hash should exist."
                 % (len(hits), stem, ext, ", ".join(sorted(hits))))
    return hits[0]


def main():
    pages = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
    changed, refs = [], 0

    for stem, ext in TARGETS:
        current = find_source(stem, ext)
        path = os.path.join(ROOT, current)
        with open(path, "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()[:HASH_LEN]
        wanted = "%s.%s.%s" % (stem, digest, ext)

        if current != wanted:
            os.replace(path, os.path.join(ROOT, wanted))
            changed.append("%s -> %s" % (current, wanted))

        # Rewrite every reference, including any leftover ?v= query string from
        # the hand-bumped scheme this replaces.
        ref = re.compile(r'(?:%s)(?:\.[0-9a-f]{%d})?\.%s(?:\?[^"\']*)?'
                         % (re.escape(stem), HASH_LEN, re.escape(ext)))
        for page in pages:
            p = os.path.join(ROOT, page)
            src = io.open(p, encoding="utf-8").read()
            out, n = ref.subn(wanted, src)
            if n and out != src:
                # newline="" so Windows does not turn every \n into \r\n and
                # rewrite the whole file
                io.open(p, "w", encoding="utf-8", newline="").write(out)
                refs += n

    if changed:
        for line in changed:
            print("  renamed  " + line)
    else:
        print("  hashes already current")
    print("  rewrote %d reference%s across %d pages" % (refs, "" if refs == 1 else "s", len(pages)))

    # Fail loudly rather than shipping a page that points at a missing file.
    missing, unhashed = [], []
    local = re.compile(r'(?:href|src)="(?!https?:|//|mailto:)([^"]+\.(?:css|js))(?:\?[^"]*)?"')
    hashed = re.compile(r'\.[0-9a-f]{%d}\.(?:css|js)$' % HASH_LEN)
    for page in pages:
        src = io.open(os.path.join(ROOT, page), encoding="utf-8").read()
        for m in local.finditer(src):
            target = m.group(1).split("?")[0]
            if not os.path.exists(os.path.join(ROOT, target.lstrip("/"))):
                missing.append("%s -> %s" % (page, target))
            # vercel.json caches *every* .css/.js for a year as immutable, which
            # is only safe while the URL changes with the bytes. An unhashed one
            # would be pinned in browsers for a year with no way to update it.
            if not hashed.search(target):
                unhashed.append("%s -> %s" % (page, target))
    if missing:
        sys.exit("error: dangling references:\n  " + "\n  ".join(missing))
    if unhashed:
        sys.exit("error: unhashed css/js referenced - vercel.json would cache these\n"
                 "immutable for a year:\n  " + "\n  ".join(sorted(set(unhashed))))
    print("  all references resolve, all hashed")


if __name__ == "__main__":
    main()
