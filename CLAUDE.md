# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo-based static site for Kraken Brewing, a Brisbane-based homebrew and craft beer blog. The site documents brewing recipes, notes, and experiments, and is deployed via Netlify with Decap CMS (formerly Netlify CMS) for content management.

## Hugo Structure

- **Working Directory**: All Hugo commands must be run from the `KrakenBrewing/` subdirectory
- **Theme**: `beautifulhugo` v5.2.1, vendored (copied, not a submodule) in `themes/beautifulhugo/`. Never edit files there; override in `layouts/` instead so theme upgrades stay a straight copy. To upgrade, replace the folder with a newer release (minus `exampleSite/` and `images/`) and run the checks.
- **Config**: Site configuration in `KrakenBrewing/config.toml`
- **Content**:
  - Blog posts in `content/post/` (markdown files with YAML frontmatter)
  - Static pages in `content/page/`
- **Static Assets**: Images and other static files in `static/img/`. Resize photos to at most 1600px and strip EXIF (phone photos carry GPS) before adding them, e.g. `convert in.jpg -auto-orient -resize '1600x1600>' -strip -quality 82 out.jpg`
- **Custom Layouts**: `layouts/_partials/head_custom.html` holds everything site-specific in `<head>`: Google Analytics, AdSense, the Search Console verification tag, the Netlify Identity widget (needed for CMS invite/recovery links) and the `og:image` tag from `share_img`
- **Footer**: `layouts/_partials/footer.html` overrides the theme footer to drop the theme credit and show `since`–build year
- **Headers**: `static/_headers` sets Netlify security headers
- **Build output**: `public/` is git-ignored; Netlify rebuilds it on every deploy

## Common Commands

All commands should be run from the `KrakenBrewing/` directory:

```bash
# Development server (run from KrakenBrewing/)
cd KrakenBrewing
hugo server -D

# Build site for production
cd KrakenBrewing
hugo

# Create new blog post
cd KrakenBrewing
hugo new post/YYYY-MM-DD-post-title.md

# Create new page
cd KrakenBrewing
hugo new page/page-name.md
```

## Checks

`.github/workflows/site-checks.yml` runs on every push to `master` and every PR (including Netlify CMS editorial-workflow PRs):

```bash
cd KrakenBrewing
hugo --panicOnWarning -d /tmp/site   # any Hugo warning fails the build
cd ..
python3 tests/check_site.py /tmp/site  # needs pyyaml
```

`tests/check_site.py` validates post front matter, filenames and image alt text, finds broken local links/images in the built site, and asserts the footer author links, Google Analytics, Search Console tag, Netlify Identity widget, Disqus comments, og:image, JSON-LD author, RSS feed and `_headers` are present.

## Content Management

### Decap CMS
- CMS configuration: `static/admin/config.yml`; the page loading Decap is `static/admin/index.html`
- Backend: Git Gateway with editorial workflow enabled
- Media storage: `/KrakenBrewing/static/img/`
- Post naming convention: `{{year}}-{{month}}-{{day}}-{{slug}}.md`

### Post Frontmatter Structure
```yaml
---
title: "Post Title"
date: YYYY-MM-DD
description: "One or two sentences for search results and link previews"
share_img: /img/photo.jpg   # optional; picture for social link previews
tags: ["Tag1", "Tag2"]
---
```

## Deployment

- Platform: Netlify
- Deploy URL: https://krakenbrewing.netlify.app
- Deploy status badge in README.md
- Source branch: `master`
- Build command: `hugo` (run from KrakenBrewing directory)
- Publish directory: `KrakenBrewing/public/`

## Site Configuration Notes

- Main sections: `["post", "posts"]`
- Comments: Disqus on every post (`comments = true` in config.toml; set `comments: false` in a post to turn them off)
- Analytics: Google Analytics (G-0XPCRBQFPW)
- Features enabled: word count, related posts, RSS (`/index.xml`)
- Features disabled: reading time, commit info, social share links, dark mode (`colorScheme = "light"`)
- Author info configured for Luke Ryan (footer links: GitHub, LinkedIn, Instagram; no email or portfolio link)
