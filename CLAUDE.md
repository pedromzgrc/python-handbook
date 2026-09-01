# Python Interview Prep — Project Guide

A Flask app that turns plain `.py` files into a browsable cheat sheet.
There are two independent content types, each with its own numbered
file series, its own loader module, and its own comment-based format
that the loader parses. **The `.py` files are the source of truth** —
the loader modules just parse them, and the Flask app just renders
whatever the loader returns. To add content, edit/create a `.py` file;
never hand-write HTML for content.

## Running the app

```
source .venv/bin/activate
python3 app.py
```

Then open **http://127.0.0.1:5001** (not 5000 — macOS's AirPlay
Receiver/Control Center squats on port 5000 by default, so `app.py`
runs on 5001 to avoid the conflict; see the comment above `app.run()`).

Dependencies (Flask, Markdown, Pygments) live in `.venv/`, pinned in
`requirements.txt`.

## Content type 1: Chapters (the numbered root files)

Files: `01_basics.py`, `02_control_flow.py`, ... `08_fetching_data.py`
Loader: `content_loader.py` → `load_units()`
Route: `/unit/<slug>`

Format:

```python
# Chapter N: Title

# --- Module Name ---
# Theory: one short sentence explaining the concept. Only this first
# comment line becomes prose — everything else in the block (more
# comments, blank lines, code) becomes the code snippet verbatim.
some_code = "here"
print(some_code)
```

- First line of the file: `# Chapter N: Title` — sets the unit's title.
- Each module starts with `# --- Module Name ---`.
- Only the **first** comment line after the header is pulled out as
  the prose explanation (stripping a leading `Theory:` if present).
  Everything else — more comment lines, blank lines, actual code — is
  kept as-is and becomes the fenced code block. This means multi-line
  explanations are allowed, but line 2 onward will visually appear as
  a comment sitting above the code, not as a second paragraph. Keep
  the essential point in line 1.
- A new chapter file needs a numeric prefix one higher than the last
  (`09_...py`) — `content_loader.py` globs `*.py` in the project root
  and orders by that prefix. It also needs an entry point in the
  sidebar automatically (the sidebar just iterates `load_units()`), so
  no template changes are needed to add a chapter or a module.

## Content type 2: Interview questions (interview_questions/)

Files: `interview_questions/01_arrays_and_hashing.py` ...
`interview_questions/18_bit_manipulation_and_maths_and_geometry.py`
(one file per category, all 18 category files already exist — most
currently hold zero exercises)
Loader: `interview_loader.py` → `load_categories()`
Route: `/interview/<slug>`

Format:

```python
# Category: Arrays and Hashing

# --- Exercise Title ---
# Difficulty: Easy
# @problem
# The problem statement, verbatim from the prompt given. Can span
# multiple comment lines/paragraphs (blank "#" lines become paragraph
# breaks).
# @hint
# A conceptual nudge — name the technique to use (e.g. "try a sliding
# window", "use an auxiliary dictionary to count occurrences") without
# giving away the full solution.
# @solution

def solution_function(...):
    ...

# @explanation
# Walks through why the solution works, referencing the actual
# variable/function names used above.
```

Key rules for this format (different from chapters — don't mix them up):

- Sections are opened with explicit `# @problem`, `# @hint`,
  `# @solution`, `# @explanation` marker lines (must be exactly that,
  alone on the comment line). Whatever follows a marker — comment
  lines or code lines — belongs to that section until the next marker.
- **`@solution` is not optional.** If you write code right after
  `@problem` or `@hint` with no `@solution` marker in between, that
  code gets silently swallowed into the problem/hint prose instead of
  becoming the code block. Always include it, even directly followed
  by a blank line then the function.
- `@hint` is optional — a category can have exercises with or without
  one. When present, it renders as a blockquote callout above the
  (hidden) solution, so learners can attempt the exercise themselves
  before revealing anything.
- `# Difficulty: Easy|Medium|Hard` is a metadata line, not a section —
  put it right after the exercise header, before `@problem`.
- The solution code block + explanation are rendered inside a native
  `<details>`/`<summary>` element (`solution-toggle` class in
  `style.css`), collapsed by default. This is pure HTML — **no
  JavaScript**, so don't add any when touching this. If you need the
  show/hide label text to change, it's done with CSS attribute
  selectors on `details[open]`, not a script.
- A category file with no `# --- Title ---` blocks (just the
  `# Category:` header) is valid and renders an empty-state message —
  that's the default state for a category with no exercises yet.
- Multiple exercises can live in one category file; just repeat the
  `# --- Title ---` block. They render in file order.

### Adding a new exercise — checklist

1. Pick the right category file under `interview_questions/`.
2. Append a new `# --- Title ---` block using the format above. Copy
   the problem statement text as given.
3. Write the solution in "vanilla" Python by default (basic loops,
   dicts/sets, no niche stdlib helpers like `collections.Counter`)
   unless the person doing the exercise asks for something else —
   this repo is a fundamentals cheat sheet, and prior exercises
   (`is_anagram`, `is_valid_sudoku`) set that precedent.
4. **Verify before considering it done, every time:**
   - Parse-check the fields: run `load_categories()`, find the new
     exercise, print every field, and confirm `hint`/`problem`/`code`/
     `explanation` all contain what you expect (not empty, not each
     other's content bled together — see the `@solution`-is-required
     rule above, this is the most common failure mode).
   - Execute the parsed `code` string directly (`exec()` it into a
     namespace) and run it against a couple of concrete test cases —
     don't just trust that code you typed is correct; prove the
     *parsed* version behaves right.
   - Start the Flask app, `curl` the category page, and grep for: the
     new heading's `id`, the difficulty badge, the blockquote (if a
     hint was added), the `<details class="solution-toggle">` wrapper,
     and that the codehilite block is present.
   - Confirm the sidebar count and the home page's exercise count
     updated, and that nothing else regressed (spot-check one existing
     unit/category route still returns 200).
   - Stop the dev server when done (`pkill -f "app.py"`) — don't leave
     it running across turns.

## Templates & styling

- `templates/base.html` is the shared shell: the sticky red sidebar
  (`position: sticky`, doesn't scroll away) with two nav groups, Units
  and Interview Questions, both iterating whatever the route passed in
  (`units`, `categories`) and expanding the active one's children
  (`unit.modules` / `category.exercises`) inline. Every route must pass
  both `units` and `categories` even if the page only cares about one,
  so the sidebar always has both groups populated.
- Each nav group is itself a `<details class="nav-group">` (VS Code
  folder-style collapse, no JS — see the `.nav-group` / `.sidebar-heading`
  rules in `style.css` for the chevron). Default open/closed state is
  decided in the template: on a unit page only "Units" is open, on a
  category page only "Interview Questions" is open, and on the home
  page both are open. If you add a third nav group, follow the same
  `<details open="...">` pattern rather than introducing JS to track
  expand state.
- `templates/index.html` — home page, one card grid per content type.
- `templates/unit.html` / `templates/category.html` — detail pages,
  basically just `{{ content_html | safe }}` inside `.markdown-body`.
- `static/style.css` — single stylesheet, red/white theme modeled after
  Refactoring Guru's site. `static/pygments.css` is generated, not
  hand-written — regenerate it if you ever change the Pygments style:
  ```
  python3 -c "from pygments.formatters import HtmlFormatter; print(HtmlFormatter(style='friendly').get_style_defs('.codehilite'))" > static/pygments.css
  ```

## General conventions

- Everything renders through the `markdown` library (`fenced_code`,
  `codehilite`, `tables`, `attr_list` extensions) — the loaders only
  extract structured text/code; `app.py` is where Markdown-to-HTML
  conversion happens (see `_render_markdown()`).
- `attr_list` is what lets headings carry a specific `id` (`{: #slug }`
  syntax) so sidebar anchor links land in the right place — if you
  change how slugs are generated, keep the loader's `_slugify()` and
  the heading's `{: #... }` id in sync, or anchors break silently.
- No JavaScript anywhere in this app by design — interactivity (the
  solution toggle) is done with native HTML (`<details>`) and CSS
  only. Keep it that way unless explicitly asked to add JS.
