# Python Handbook — Project Guide

Flask app that renders plain `.py` files as a browsable cheat sheet.
**Content `.py` files are the source of truth** — never hand-write HTML
for content.

## Commands

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

```bash
source .venv/bin/activate && python3 app.py
```

Serves http://127.0.0.1:5001 (not 5000, which macOS AirPlay occupies).
Stop it with `pkill -f "app.py"`. There is no test suite or linter.

## Layout

- `units/NN_*.py` — chapters, parsed by `content_loader.py`, route `/unit/<slug>`.
- `interview_questions/NN_*.py` — one file per category, parsed by
  `interview_loader.py`, route `/interview/<slug>`.
- `app.py` — routes and Markdown→HTML rendering. `mdx_mermaid.py` is a
  local Markdown extension it loads.
- `templates/base.html` — shared shell and sidebar; every route must pass
  both `units` and `categories`.
- `static/style.css` is hand-written; `static/pygments*.css` are generated.

## Content rules

- Files are ordered by numeric prefix and appear in the sidebar automatically.
- The two formats differ; read the loader's docstring and an existing
  file of the same type before editing.
- In interview files, code must follow a `# @solution` (or
  `# @solution:<Label>`) marker, or it is silently absorbed into the prose.
- Heading ids come from each loader's `_slugify()`; keep them in sync with
  the `{: #slug }` ids in `app.py` or sidebar anchors break.
- Write solutions in vanilla Python unless asked otherwise.
- Verify new exercises: `exec()` the parsed code from `load_categories()`
  against test cases, then curl the category page.

## Frontend

- Solution toggles and tabs are CSS-only (`<details>`, radio inputs); keep them JS-free.
- `base.html` holds the site's only JS: CDN-loaded Lucide and Mermaid,
  plus inline dark-mode and copy-button scripts.

Regenerate Pygments CSS:

```bash
python3 -c "from pygments.formatters import HtmlFormatter; print(HtmlFormatter(style='friendly').get_style_defs('.codehilite'))" > static/pygments.css
```

```bash
python3 -c "from pygments.formatters import HtmlFormatter; print(HtmlFormatter(style='monokai').get_style_defs('[data-theme=\"dark\"] .codehilite'))" > static/pygments-dark.css
```
