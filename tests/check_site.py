#!/usr/bin/env python3
"""Sanity checks for the Kraken Brewing Hugo site.

Usage:
    python3 tests/check_site.py <built-site-dir>

Checks post front matter in KrakenBrewing/content/post, then checks the
built site for broken local links/images and for content every page should
carry (author links, analytics, comments).
"""
import datetime
import html
import json
import os
import re
import sys
from urllib.parse import unquote

import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(REPO, "KrakenBrewing", "content", "post")
BASE_URL = "https://krakenbrewing.netlify.app"
GA_ID = "G-0XPCRBQFPW"
DISQUS_SHORTNAME = "https-krakenbrewing-netlify-app"
FILENAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[A-Za-z0-9&_.-]+\.md$")

errors = []


def fail(msg):
    errors.append(msg)


def check_front_matter():
    for name in sorted(os.listdir(POSTS)):
        if not name.endswith(".md"):
            continue
        path = os.path.join("content/post", name)
        if not FILENAME_RE.match(name):
            fail(f"{path}: filename should be YYYY-MM-DD-slug.md with no spaces")
        text = open(os.path.join(POSTS, name), encoding="utf-8").read()
        m = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
        if not m:
            fail(f"{path}: missing YAML front matter")
            continue
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError as e:
            fail(f"{path}: invalid YAML front matter: {e}")
            continue
        if not isinstance(fm.get("title"), str) or not fm["title"].strip():
            fail(f"{path}: missing title")
        date = fm.get("date")
        if isinstance(date, str):
            try:
                datetime.datetime.fromisoformat(date.replace("Z", "+00:00"))
            except ValueError:
                fail(f"{path}: unparseable date {date!r}")
        elif not isinstance(date, (datetime.date, datetime.datetime)):
            fail(f"{path}: missing date")
        tags = fm.get("tags")
        if not isinstance(tags, list) or not tags or not all(
            isinstance(t, (str, int, float)) and str(t).strip() for t in tags
        ):
            fail(f"{path}: tags should be a non-empty list")
        if fm.get("draft") is True:
            fail(f"{path}: marked draft: true, won't be published")


def local_target(site, page_dir, url):
    """Return the file a local link points at, or None if it isn't local."""
    url = html.unescape(url)
    if url.startswith(BASE_URL):
        url = url[len(BASE_URL):] or "/"
    elif re.match(r"^([a-z][a-z0-9+.-]*:|//|#)", url, re.I):
        return None
    url = unquote(url.split("#")[0].split("?")[0])
    if not url:
        return None
    if url.startswith("/"):
        return os.path.normpath(os.path.join(site, url.lstrip("/")))
    return os.path.normpath(os.path.join(page_dir, url))


def check_built_site(site):
    pages = []
    for d, _, files in os.walk(site):
        for f in files:
            if f.endswith(".html"):
                pages.append(os.path.join(d, f))
    if not pages:
        fail(f"{site}: no HTML pages found; did the build run?")
        return

    broken = {}
    for p in pages:
        text = open(p, encoding="utf-8", errors="replace").read()
        for url in re.findall(r'(?:src|href)="([^"]+)"', text):
            tgt = local_target(site, os.path.dirname(p), url)
            if tgt and not (
                os.path.isfile(tgt) or os.path.isfile(os.path.join(tgt, "index.html"))
            ):
                broken.setdefault(url, os.path.relpath(p, site))
    for url, page in sorted(broken.items()):
        fail(f"broken link/image {url} (first seen in {page})")

    home = open(os.path.join(site, "index.html"), encoding="utf-8").read()
    footer = home[home.rfind("<footer"):]
    for needle in (
        "https://github.com/LukeTRyan",
        "https://www.instagram.com/kraken.brewing/",
        "https://linkedin.com/in/luke-t-ryan",
        "mailto:",
        "Luke Ryan",
    ):
        if needle not in footer:
            fail(f"homepage footer is missing {needle!r} (check [Params.Author] in config.toml)")

    post_dir = os.path.join(site, "post")
    posts = sorted(
        os.path.join(post_dir, d, "index.html")
        for d in os.listdir(post_dir)
        if os.path.isfile(os.path.join(post_dir, d, "index.html"))
    )
    expected = len([n for n in os.listdir(POSTS) if n.endswith(".md")])
    if len(posts) != expected:
        fail(f"built {len(posts)} post pages but content/post has {expected} posts")

    for p in [os.path.join(site, "index.html")] + posts:
        rel = os.path.relpath(p, site)
        text = open(p, encoding="utf-8").read()
        if GA_ID not in text:
            fail(f"{rel}: Google Analytics tag {GA_ID} missing")
        if p == os.path.join(site, "index.html"):
            continue
        if f"disqus_shortname = '{DISQUS_SHORTNAME}'" not in text:
            fail(f"{rel}: Disqus comments missing")
        for block in re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', text, re.S
        ):
            try:
                data = json.loads(block)
            except ValueError as e:
                fail(f"{rel}: invalid JSON-LD: {e}")
                continue
            author = data.get("author") if isinstance(data, dict) else None
            if isinstance(author, dict) and not author.get("name"):
                fail(f"{rel}: JSON-LD author name is empty")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    check_front_matter()
    check_built_site(sys.argv[1])
    if errors:
        print(f"{len(errors)} problem(s) found:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("All site checks passed.")


if __name__ == "__main__":
    main()
