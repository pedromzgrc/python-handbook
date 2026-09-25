"""Flask app that turns the numbered chapter .py files in this project
into a browsable cheat sheet: a sidebar lists every unit, and clicking one
renders its modules as Markdown (theory + fenced code snippets)."""
import html
import markdown
import bleach
from flask import Flask, abort, render_template

from content_loader import load_units
from interview_loader import load_categories

app = Flask(__name__)

MARKDOWN_EXTENSIONS = ["fenced_code", "codehilite", "tables", "attr_list", "mdx_mermaid"]
MARKDOWN_EXTENSION_CONFIGS = {"codehilite": {"guess_lang": False, "linenums": True}}

ALLOWED_TAGS = [
    "h1", "h2", "h3", "h4", "h5", "h6",
    "p", "a", "strong", "em", "code", "pre", "blockquote",
    "ul", "ol", "li",
    "table", "thead", "tbody", "tr", "th", "td",
    "div", "span", "br", "hr", "img"
]

ALLOWED_ATTRIBUTES = {
    "*": ["id", "class"],
    "a": ["href", "title"],
    "img": ["src", "alt", "title"],
}


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
    html_content = markdown.markdown(
        document,
        extensions=MARKDOWN_EXTENSIONS,
        extension_configs=MARKDOWN_EXTENSION_CONFIGS,
    )
    return bleach.clean(
        html_content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
    )


def _render_solution_body(exercise):
    """Builds the HTML that goes inside the <details> solution wrapper.
    Most exercises have a single @solution and render as one code block,
    same as before. An exercise that defines more than one @solution:<label>
    (e.g. "Junior" vs "Senior" — same optimal approach, different coding
    style) renders as CSS-only tabs instead: radio inputs + labels toggle
    which .tab-panel is visible via :checked, no JS involved."""
    solutions = [s for s in exercise["solutions"] if s["code"]]

    if len(solutions) <= 1:
        parts = []
        if exercise["code"]:
            parts.append(f"```python\n{exercise['code']}\n```")
        if exercise["explanation"]:
            parts.append(f"**Explanation:** {exercise['explanation']}")
        return _render_markdown("\n\n".join(parts)) if parts else ""

    inputs_and_labels = []
    panels = []
    for index, solution in enumerate(solutions):
        input_id = html.escape(f"tab-{exercise['slug']}-{solution['slug']}")
        code_html = _render_markdown(f"```python\n{solution['code']}\n```")
        checked = " checked" if index == 0 else ""
        esc_exercise_slug = html.escape(exercise["slug"])
        esc_label = html.escape(solution["label"])
        inputs_and_labels.append(
            f'<input type="radio" name="tabs-{esc_exercise_slug}" id="{input_id}" '
            f'class="tab-input"{checked}>'
            f'<label for="{input_id}" class="tab-label">{esc_label}</label>'
        )
        panels.append(f'<div class="tab-panel">{code_html}</div>')

    tabs_html = (
        '<div class="solution-tabs">'
        + "".join(inputs_and_labels)
        + '<div class="tab-panels">'
        + "".join(panels)
        + "</div></div>"
    )
    if exercise["explanation"]:
        tabs_html += _render_markdown(f"**Explanation:** {exercise['explanation']}")
    return tabs_html


def render_category_markdown(category):
    """Builds the HTML for a category's exercises: problem statement and
    hint are always visible; the solution (or solutions, if tabbed) and
    explanation are rendered separately and wrapped in a <details> element
    so they stay hidden (native HTML, no JS) until the reader clicks "Show
    solution"."""
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

        solution_body = _render_solution_body(exercise)
        if solution_body:
            block += (
                '<details class="solution-toggle">'
                "<summary>"
                '<span class="show-label">Show solution</span>'
                '<span class="hide-label">Hide solution</span>'
                "</summary>"
                f'<div class="solution-body">{solution_body}</div>'
                "</details>"
            )
        blocks.append(block)
    return "\n".join(blocks)


_UNITS = load_units()
_CATEGORIES = load_categories()


@app.route("/")
def index():
    return render_template("index.html", units=_UNITS, categories=_CATEGORIES)


@app.route("/unit/<slug>")
def unit_detail(slug):
    unit = next((u for u in _UNITS if u["slug"] == slug), None)
    if unit is None:
        abort(404)
    content_html = render_unit_markdown(unit)
    return render_template(
        "unit.html",
        units=_UNITS,
        categories=_CATEGORIES,
        unit=unit,
        content_html=content_html,
    )


@app.route("/interview/<slug>")
def category_detail(slug):
    category = next((c for c in _CATEGORIES if c["slug"] == slug), None)
    if category is None:
        abort(404)
    content_html = render_category_markdown(category) if category["exercises"] else ""
    return render_template(
        "category.html",
        units=_UNITS,
        categories=_CATEGORIES,
        category=category,
        content_html=content_html,
    )


if __name__ == "__main__":
    # Port 5000 is taken by macOS's AirPlay Receiver (Control Center), so
    # this runs on 5001 instead to avoid clashing with it.
    app.run(debug=False, port=5001)
