# Macademia

A local Hugo theme for an academic portfolio site. Dark wabi-sabi tea-room palette: warm brown bg, washi-paper ink, single matcha accent, paper-grain noise overlay. EB Garamond + IBM Plex Mono.

Requires Hugo `>= 0.160.1` (extended).

## Quick start

In `config.toml`:

```toml
theme = "macademia"

[params]
  description = "..."
  date_format = "2006-01-02"
  avatar = "img/avatar.jpg"

  [params.fonts]
    body = "\"EB Garamond\", Georgia, Cambria, \"Times New Roman\", serif"
    google_stylesheets = [
      "https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=IBM+Plex+Mono:wght@400;500&display=swap"
    ]
```

Run `hugo server` for local dev, `hugo --minify` for prod build.

## Section model

Every top-level content section under `content/` must be declared under `[params.macademia.sections.<section>]` with a `class`. The class controls how the section list and its single pages render.

| class          | List page renders                                                          | Single page renders                                          |
| -------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------ |
| `post`         | Magazine list of `page-card` items (date · author · tags)                  | Prose article with `page-meta` + featured image              |
| `publications` | Compact `publication-row` list (year · title · authors · venue · actions)  | (typically disabled — see *Disabling single pages* below)    |
| `project-tags` | Project grid built from configured tags; cards link to canonical tag pages  | Not used for leaf pages                                      |
| `page`         | Just the prose; no child enumeration                                       | Standard prose article                                       |

Sections not declared in config default to `class = "post"` and are **hidden from the nav if they have no child pages** (controlled by `params.macademia.navigation.hide_empty_sections`, default `true`). Always declare a section's class — even `class = "page"` — if you want it in the nav without children.

```toml
[params.macademia.sections.posts]
  class = "post"
  name  = "Posts"

[params.macademia.sections.projects]
  class = "project-tags"
  name  = "Projects"

[params.macademia.projects]
  tags = ["visual-system-patterning", "spinal-motor-neuron-development", "collaborations"]
  featured = ["visual-system-patterning", "spinal-motor-neuron-development"]

[params.macademia.projects.labels]
  visual-system-patterning = "Visual System Patterning"
  spinal-motor-neuron-development = "Spinal Motor Neuron Development"
  collaborations = "Collaborations"

[params.macademia.projects.summaries]
  visual-system-patterning = "Spatial and temporal patterning mechanisms..."

[params.macademia.sections.publications]
  class = "publications"
  name  = "Publications"

[params.macademia.sections.about]
  class = "page"
  name  = "About"
```

## Homepage

The homepage hero pulls from `[params.macademia.home]` plus the `about` section's `summary`:

```toml
[params.macademia.home]
  eyebrow                = "Developmental biology / Neurobiology / ..."
  avatar_alt             = "Portrait of Yen-Chung Chen"
  summary_section        = "about"          # page whose .Params.summary fills the hero copy
  publications_section   = "publications"
  publications_title     = "Featured Publications"
  publications_link_label= "All publications"
  publications_count     = 4
  project_section        = "projects"
  project_title          = "Projects"
  project_link_label     = "All projects"
  posts_section          = "posts"
  posts_title            = "Recent Posts"
  posts_link_label       = "All posts"
  posts_count            = 4
```

The featured-publications list filters child pages where `featured: true`. The project list shows `params.macademia.projects.featured`, falling back to all configured project tags.

## Profile / social links

Render via `partial "profile-links.html"`. Configure under `[[params.macademia.profile.links]]`:

```toml
[[params.macademia.profile.links]]
  key    = "github"
  icon   = "github"               # matches an SVG in profile-icon.html
  name   = "GitHub"
  handle = "chenyenchung"
  url    = "https://github.com/chenyenchung"
  enabled = true
```

`params.macademia.profile.show_on_sections` (default `["about"]`) decides which list pages also append the chip row beneath their heading.

Available icons (in `partials/profile-icon.html`): `mail`, `scholar`, `github`, `bluesky`, `twitter`, `mastodon`, `orcid`. Unknown icon → ALL-CAPS letter fallback.

## Publications

Frontmatter (`content/publications/<slug>/index.md`):

```yaml
---
title: "Paper title"
slug: "2024_dm"
date: "2024-05-01"
summary: "2024 Developmental Cell"     # short label, used in card and search
authors:
  - "First Author"
  - "Yen-Chung Chen"                    # bolded automatically wherever it appears
  - "Last Author"
doi: "10.xxx/xxx"
doi_url: "https://doi.org/10.xxx/xxx"   # required: title links here (resolves to journal)
journal: "Developmental Cell"
journal_short: "Dev Cell"               # preferred for the row meta line
year: 2024
tags:                                    # ordinary tags; configured project tags render as projects
  - "visual-system-patterning"
featured: true                           # controls homepage featured list
image: "/publications/2024_dm.jpg"       # optional, currently unused on the row
fulltext: "/publications/2024_dm.pdf"    # optional → "Full text ↗" pill
behind_the_scene: "post-slug"            # optional → "Behind the Scene →" pill
---
```

Field semantics:
- **Title link**: always external. Uses `doi_url`. If absent, the title renders unlinked.
- **`fulltext`** (preferred) / `full_text` (legacy): static asset path or external URL → "Full text ↗" pill.
- **`behind_the_scene`** (preferred) / `bts` (legacy): `posts/`-relative slug, absolute path, or external URL → "Behind the Scene →" pill.
- **No DOI button**: The title is the journal link; a separate DOI button would be redundant.
- **Author bolding**: `partials/publication-card.html` wraps the literal string `"Yen-Chung Chen"` in `<strong class="self-author">`. To rebrand, change that string in the partial.

### Disabling single publication pages

By default, every publication file would emit `/publications/<slug>/index.html`. To suppress those (e.g. when publications are auto-generated from a script and have no body content worth a detail page), put a cascade on the section landing:

```yaml
# content/publications/_index.md
---
title: Publications
summary: Peer-reviewed work, most recent first.
cascade:
  - target:
      kind: page
    build:
      render: link
      list: always
---
```

`target.kind: page` scopes the cascade to leaf pages only (the section's own `_index.md` still renders). `render: link` keeps publication leaf pages from emitting detail HTML, while `list: always` keeps them enumerable from section lists, the search index, and tag pages.

## Search

- **Index source**: `layouts/index.json` emits `/index.json` at build time. It iterates `.Site.Pages` plus, for each allowed section, `.Site.GetPage(section).Pages` — this second pass is what catches publications when single rendering is disabled.
- **Allowed sections**: `params.macademia.search.sections` (defaults to `["about", "posts", "projects", "awards", "talks", "courses", "publications"]`).
- **Per-page exclusion**: set `private: true` or `exclude_search: true` in frontmatter.
- **Permalinks**: for unrendered publications, the search result links to `doi_url` (fallback `fulltext`, `full_text`, then RelPermalink).
- **Client**: `static/js/search.js` fetches the index, scores by term hits in title/summary/authors/tags/body, sorts by score then date, caps at 30. UI lives at `/search/` (a `search.md` page picks up `layouts/search/single.html`).
- **Search box visibility**: toggle with `params.macademia.search.enabled = false`.

## Tweakable knobs

```toml
[params.macademia.theme]
  custom_css = ["css/extra.css"]   # extra stylesheets layered after site.css

[params.macademia.navigation]
  hide_empty_sections = true       # (default) hide nav items whose section has 0 leaf pages

[params.macademia.labels]
  slides = "Slides"                # button label on talk/post pages
```

## Layout & partial map

```
layouts/
  _default/
    baseof.html      # html shell, font/preconnect, header + footer + JS
    list.html        # branches by section class (post, publications, project-tags, page)
    single.html      # branches by section class
    taxonomy.html    # /tags/<tag>/ index
    terms.html       # /tags/ overview
  index.html         # homepage hero + featured pubs + projects + recent posts
  index.json         # search index emitter
  search/single.html # /search/ form + results
  partials/
    site-header.html       # sticky nav with hanko brand mark
    site-footer.html       # mono caps copyright + footer.links
    profile-links.html     # round social chip row
    profile-icon.html      # icon-key → SVG
    page-card.html         # standard list item (post / talk / project)
    page-meta.html         # date · authors · tags row
    publication-card.html  # compact publication row
    publication-links.html # Full text + Behind the Scene pills
    project-badges.html    # project tag badges (resolves configured tags to labels)
    project-card.html      # project cards for configured project tags
    macademia/
      brush.html             # matcha brushstroke SVG
      hanko.html             # square-seal mark used in nav
      section-divider.html   # caps label · hairline · matcha link
      section-config.html    # lookup helper for section class/name
      section-name.html      # section display name
      project-is-tag.html        # tests whether a tag is a configured project
      project-label.html         # display label for a project tag
      project-summary.html       # summary for a project tag
      project-tags.html          # configured project tag list
      project-tags-from-page.html # configured project tags present on a page
      project-url.html           # canonical /tags/<tag>/ URL
```

CSS lives at `static/css/site.css` (single file, no preprocessor). Palette tokens are CSS variables on `:root` — to tweak the theme without touching template logic, override them via a `custom_css` file rather than editing `site.css`.

## Footer

```toml
copyright = "&copy; Yen-Chung Chen 2015 - {year}"   # {year} is replaced with the build year

[[params.macademia.footer.links]]
  name = "Privacy"
  url  = "/privacy/"
```

## Adding a new section

1. Create `content/<section>/_index.md` (and child pages as needed).
2. Add `[params.macademia.sections.<section>]` with the right `class` and `name`.
3. Add a `[[menu.main]]` entry pointing to `/<section>/`.
4. (Optional) add the section to `params.macademia.search.sections` if you want it indexed.
