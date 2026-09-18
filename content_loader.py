"""Parses the numbered chapter .py files in units/ into structured content
the Flask app can render, so the cheat sheet content lives in one place:
the Python files themselves.
"""
import re
from pathlib import Path

CONTENT_DIR = Path(__file__).parent / "units"
CHAPTER_FILE_PATTERN = re.compile(r"^(\d+)_(.+)\.py$")
CHAPTER_TITLE_PATTERN = re.compile(r"^#\s*Chapter\s*\d+:\s*(.+)$")
MODULE_HEADER_PATTERN = re.compile(r"^#\s*---\s*(.+?)\s*---\s*$")
THEORY_PATTERN = re.compile(r"^#\s*Theory:\s*(.+)$")


def _slugify(name: str) -> str:
    return name.lower().replace(" ", "-")


def _parse_modules(body_lines):
    """Splits a chapter's lines into modules based on '# --- Title ---'
    headers, separating the first theory comment line from the code."""
    modules = []
    current_title = None
    current_lines = []

    def flush():
        if current_title is None:
            return
        lines = current_lines
        theory = ""
        code_lines = lines
        if lines:
            match = THEORY_PATTERN.match(lines[0].strip())
            if match:
                theory = match.group(1)
                code_lines = lines[1:]
        while code_lines and not code_lines[0].strip():
            code_lines = code_lines[1:]
        while code_lines and not code_lines[-1].strip():
            code_lines = code_lines[:-1]
        modules.append(
            {
                "title": current_title,
                "slug": _slugify(current_title),
                "theory": theory,
                "code": "\n".join(code_lines),
            }
        )

    for line in body_lines:
        header_match = MODULE_HEADER_PATTERN.match(line.strip())
        if header_match:
            flush()
            current_title = header_match.group(1)
            current_lines = []
        else:
            current_lines.append(line)
    flush()
    return modules


def load_units():
    """Reads every NN_name.py file in units/ and returns a list of unit
    dicts, ordered by their numeric prefix."""
    units = []
    for path in sorted(CONTENT_DIR.glob("*.py")):
        match = CHAPTER_FILE_PATTERN.match(path.name)
        if not match:
            continue
        number, name = match.groups()
        lines = path.read_text().splitlines()

        title = name.replace("_", " ").title()
        if lines:
            title_match = CHAPTER_TITLE_PATTERN.match(lines[0].strip())
            if title_match:
                title = title_match.group(1)

        units.append(
            {
                "number": int(number),
                "slug": name.replace("_", "-"),
                "title": title,
                "filename": path.name,
                "modules": _parse_modules(lines[1:]),
            }
        )
    units.sort(key=lambda unit: unit["number"])
    return units
