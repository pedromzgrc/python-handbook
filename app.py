"""Flask app that turns the numbered chapter .py files in this project
into a browsable cheat sheet: a sidebar lists every unit, and clicking one
renders its modules as Markdown (theory + fenced code snippets)."""
import markdown
from flask import Flask, abort, render_template

from content_loader import load_units
from interview_loader import load_categories

app = Flask(__name__)

MARKDOWN_EXTENSIONS = ["fenced_code", "codehilite", "tables", "attr_list"]
MARKDOWN_EXTENSION_CONFIGS = {"codehilite": {"guess_lang": False}}


def render_unit_markdown(unit):
    """Builds one Markdown document for a unit's modules and renders it
    to HTML, so both the prose and the code snippets come from Markdown.
    attr_list pins each heading's id to the module slug so the sidebar's
    anchor links land on the right section."""
    parts = []
    for module in unit["modules"]:
        parts.append(f"## {module['title']} {{: #{module['slug']} }}")
        if module["theory"]:
            parts.append(module["theory"])
        if module["code"]:
            parts.append(f"```python\n{module['code']}\n```")
    return _render_markdown("\n\n".join(parts))


def _render_markdown(document):
    return markdown.markdown(
        document,
        extensions=MARKDOWN_EXTENSIONS,
        extension_configs=MARKDOWN_EXTENSION_CONFIGS,
    )


def render_category_markdown(category):
    """Builds the HTML for a category's exercises: problem statement and
    hint are always visible; the solution code and explanation are
    rendered separately and wrapped in a <details> element so they stay
    hidden (native HTML, no JS) until the reader clicks "Show solution"."""
    blocks = []
    for exercise in category["exercises"]:
        prose_parts = [f"## {exercise['title']} {{: #{exercise['slug']} }}"]
        if exercise["difficulty"]:
            prose_parts.append(f"**Difficulty:** {exercise['difficulty']}")
        if exercise["problem"]:
            prose_parts.append(exercise["problem"])
        if exercise["hint"]:
            prose_parts.append(f"> **Hint:** {exercise['hint']}")
        block = _render_markdown("\n\n".join(prose_parts))

        solution_parts = []
        if exercise["code"]:
            solution_parts.append(f"```python\n{exercise['code']}\n```")
        if exercise["explanation"]:
            solution_parts.append(f"**Explanation:** {exercise['explanation']}")
        if solution_parts:
            solution_html = _render_markdown("\n\n".join(solution_parts))
            block += (
                '<details class="solution-toggle">'
                "<summary>"
                '<span class="show-label">Show solution</span>'
                '<span class="hide-label">Hide solution</span>'
                "</summary>"
                f'<div class="solution-body">{solution_html}</div>'
                "</details>"
            )
        blocks.append(block)
    return "\n".join(blocks)


@app.route("/")
def index():
    units = load_units()
    categories = load_categories()
    return render_template("index.html", units=units, categories=categories)


@app.route("/unit/<slug>")
def unit_detail(slug):
    units = load_units()
    categories = load_categories()
    unit = next((u for u in units if u["slug"] == slug), None)
    if unit is None:
        abort(404)
    content_html = render_unit_markdown(unit)
    return render_template(
        "unit.html",
        units=units,
        categories=categories,
        unit=unit,
        content_html=content_html,
    )


@app.route("/interview/<slug>")
def category_detail(slug):
    units = load_units()
    categories = load_categories()
    category = next((c for c in categories if c["slug"] == slug), None)
    if category is None:
        abort(404)
    content_html = render_category_markdown(category) if category["exercises"] else ""
    return render_template(
        "category.html",
        units=units,
        categories=categories,
        category=category,
        content_html=content_html,
    )


if __name__ == "__main__":
    # Port 5000 is taken by macOS's AirPlay Receiver (Control Center), so
    # this runs on 5001 instead to avoid clashing with it.
    app.run(debug=True, port=5001)
