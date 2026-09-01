"""Parses the interview-question category files (interview_questions/) into
structured content: each category (e.g. "Arrays and Hashing") holds a list
of exercises, each with a problem statement, a hint, a solution, and an
explanation.

Exercise blocks look like this:

    # --- Two Sum ---
    # Difficulty: Easy
    # @problem
    # Given an array of integers nums and an integer target, return
    # indices of the two numbers that add up to target.
    # @hint
    # Try using a hash map to record each number you've seen and its
    # index, so you can look up a complement in one step.
    # @solution

    def two_sum(nums, target):
        ...

    # @explanation
    # We use a hash map to store numbers we've already seen along with
    # their indices...

Every "#"-prefixed comment line is routed into whichever section
("problem", "hint", "solution", or "explanation") was last opened by an
"@" marker; non-comment lines are always solution code regardless of the
current marker. Every exercise needs its own "@solution" marker — without
it, code right after "@problem" or "@hint" would be swallowed into that
section's text instead of becoming the code block. "@hint" is optional. A
category file with no "# --- Title ---" blocks simply has no exercises
yet.
"""
import re
from pathlib import Path

CONTENT_DIR = Path(__file__).parent / "interview_questions"
CATEGORY_FILE_PATTERN = re.compile(r"^(\d+)_(.+)\.py$")
CATEGORY_TITLE_PATTERN = re.compile(r"^#\s*Category:\s*(.+)$")
EXERCISE_HEADER_PATTERN = re.compile(r"^#\s*---\s*(.+?)\s*---\s*$")
DIFFICULTY_PATTERN = re.compile(r"^#\s*Difficulty:\s*(.+)$")
SECTION_MARKER_PATTERN = re.compile(r"^#\s*@(problem|hint|solution|explanation)\s*$")


def _slugify(name: str) -> str:
    return name.lower().replace(" ", "-")


def _prose(lines):
    """Turns a block of '#'-prefixed comment lines into Markdown text,
    keeping blank comment lines as paragraph breaks."""
    text_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped in ("#", ""):
            text_lines.append("")
        elif stripped.startswith("#"):
            text_lines.append(stripped[1:].strip())
        else:
            text_lines.append(stripped)
    return "\n".join(text_lines).strip()


def _trim_blank_lines(lines):
    while lines and not lines[0].strip():
        lines = lines[1:]
    while lines and not lines[-1].strip():
        lines = lines[:-1]
    return lines


def _parse_exercises(body_lines):
    exercises = []
    current_title = None
    current_lines = []

    def flush():
        if current_title is None:
            return
        sections = {"problem": [], "hint": [], "solution": [], "explanation": []}
        section = "solution"
        difficulty = ""
        for line in current_lines:
            stripped = line.strip()
            difficulty_match = DIFFICULTY_PATTERN.match(stripped)
            if difficulty_match:
                difficulty = difficulty_match.group(1).strip()
                continue
            marker = SECTION_MARKER_PATTERN.match(stripped)
            if marker:
                section = marker.group(1)
                continue
            sections[section].append(line)

        exercises.append(
            {
                "title": current_title,
                "slug": _slugify(current_title),
                "difficulty": difficulty,
                "problem": _prose(sections["problem"]),
                "hint": _prose(sections["hint"]),
                "code": "\n".join(_trim_blank_lines(sections["solution"])),
                "explanation": _prose(sections["explanation"]),
            }
        )

    for line in body_lines:
        header_match = EXERCISE_HEADER_PATTERN.match(line.strip())
        if header_match:
            flush()
            current_title = header_match.group(1)
            current_lines = []
        else:
            current_lines.append(line)
    flush()
    return exercises


def load_categories():
    """Reads every NN_name.py file in interview_questions/ and returns a
    list of category dicts, ordered by their numeric prefix."""
    categories = []
    for path in sorted(CONTENT_DIR.glob("*.py")):
        match = CATEGORY_FILE_PATTERN.match(path.name)
        if not match:
            continue
        number, name = match.groups()
        lines = path.read_text().splitlines()

        title = name.replace("_", " ").title()
        if lines:
            title_match = CATEGORY_TITLE_PATTERN.match(lines[0].strip())
            if title_match:
                title = title_match.group(1)

        categories.append(
            {
                "number": int(number),
                "slug": name.replace("_", "-"),
                "title": title,
                "filename": path.name,
                "exercises": _parse_exercises(lines[1:]),
            }
        )
    categories.sort(key=lambda category: category["number"])
    return categories


def get_category(slug):
    for category in load_categories():
        if category["slug"] == slug:
            return category
    return None
