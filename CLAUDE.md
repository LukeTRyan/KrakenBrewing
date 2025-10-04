# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo-based static site for Kraken Brewing, a Brisbane-based homebrew and craft beer blog. The site documents brewing recipes, notes, and experiments, and is deployed via Netlify with Netlify CMS for content management.

## Hugo Structure

- **Working Directory**: All Hugo commands must be run from the `KrakenBrewing/` subdirectory
- **Theme**: Uses the `beautifulhugo` theme located in `themes/beautifulhugo/`
- **Config**: Site configuration in `KrakenBrewing/config.toml`
- **Content**:
  - Blog posts in `content/post/` (markdown files with YAML frontmatter)
  - Static pages in `content/page/`
- **Static Assets**: Images and other static files in `static/img/`
- **Custom Layouts**: Override theme templates in `layouts/partials/`
  - `footer_custom.html` - Custom footer
  - `head_custom.html` - Custom head section with analytics/scripts

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

## Content Management

### Netlify CMS
- CMS configuration: `static/admin/config.yml`
- Backend: Git Gateway with editorial workflow enabled
- Media storage: `/KrakenBrewing/static/img/`
- Post naming convention: `{{year}}-{{month}}-{{day}}-{{slug}}.md`

### Post Frontmatter Structure
```yaml
---
title: "Post Title"
date: YYYY-MM-DD
tags: ["Tag1", "Tag2"]
comments: true
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
- Comments: Disqus integration enabled (disqusShortname in config.toml)
- Analytics: Google Analytics (G-0XPCRBQFPW)
- Features enabled: word count, social share, related posts
- Features disabled: reading time, RSS, commit info
- Author info configured for Luke Ryan
