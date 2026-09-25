from pathlib import Path
from interview_loader import (
    _slugify,
    _prose,
    _trim_blank_lines,
    _parse_exercises,
    load_categories,
    get_category,
)
import interview_loader

def test_slugify():
    assert _slugify("Arrays and Hashing") == "arrays-and-hashing"
    assert _slugify("Two Sum") == "two-sum"
    assert _slugify("") == ""

def test_prose():
    lines = [
        "# This is a test.",
        "# ",
        "# It spans multiple lines.",
        "",
        "# And handles missing space",
        "#like this."
    ]
    expected = "This is a test.\n\nIt spans multiple lines.\n\nAnd handles missing space\nlike this."
    assert _prose(lines) == expected

def test_trim_blank_lines():
    lines = ["", "  ", "code", "more code", "", "  "]
    assert _trim_blank_lines(lines) == ["code", "more code"]
    assert _trim_blank_lines([]) == []
    assert _trim_blank_lines([""]) == []
    assert _trim_blank_lines(["  ", "  "]) == []

def test_parse_exercises_basic():
    body = [
        "# --- Two Sum ---",
        "# Difficulty: Easy",
        "# @problem",
        "# Problem description.",
        "# @hint",
        "# A helpful hint.",
        "# @solution",
        "def two_sum(nums, target):",
        "    pass",
        "# @explanation",
        "# The explanation."
    ]
    exercises = _parse_exercises(body)
    assert len(exercises) == 1
    ex = exercises[0]
    assert ex["title"] == "Two Sum"
    assert ex["slug"] == "two-sum"
    assert ex["difficulty"] == "Easy"
    assert ex["problem"] == "Problem description."
    assert ex["hint"] == "A helpful hint."
    assert ex["explanation"] == "The explanation."
    assert len(ex["solutions"]) == 1
    assert ex["solutions"][0]["label"] == ""
    assert ex["solutions"][0]["code"] == "def two_sum(nums, target):\n    pass"
    assert ex["code"] == "def two_sum(nums, target):\n    pass"

def test_parse_exercises_multiple_solutions():
    body = [
        "# --- Two Sum ---",
        "# @problem",
        "# Problem description.",
        "# @solution:Junior",
        "def two_sum(nums, target):",
        "    return []",
        "# @solution:Senior",
        "def two_sum(nums, target):",
        "    pass"
    ]
    exercises = _parse_exercises(body)
    assert len(exercises) == 1
    ex = exercises[0]
    assert len(ex["solutions"]) == 2
    assert ex["solutions"][0]["label"] == "Junior"
    assert ex["solutions"][0]["slug"] == "junior"
    assert ex["solutions"][0]["code"] == "def two_sum(nums, target):\n    return []"
    assert ex["solutions"][1]["label"] == "Senior"
    assert ex["solutions"][1]["slug"] == "senior"
    assert ex["solutions"][1]["code"] == "def two_sum(nums, target):\n    pass"

def test_parse_exercises_multiple_exercises():
    body = [
        "# --- First ---",
        "# @problem",
        "# Prob 1",
        "# @solution",
        "code 1",
        "# --- Second ---",
        "# @problem",
        "# Prob 2",
        "# @solution",
        "code 2"
    ]
    exercises = _parse_exercises(body)
    assert len(exercises) == 2
    assert exercises[0]["title"] == "First"
    assert exercises[1]["title"] == "Second"
    assert exercises[0]["code"] == "code 1"
    assert exercises[1]["code"] == "code 2"

def test_load_categories_and_get_category(monkeypatch, tmp_path):
    # Setup temporary directory with test files
    monkeypatch.setattr(interview_loader, "CONTENT_DIR", tmp_path)

    file1 = tmp_path / "01_arrays_and_hashing.py"
    file1.write_text("# Category: Arrays\n# --- First ---\n# @problem\n# Prob 1\n# @solution\ncode 1")

    file2 = tmp_path / "02_two_pointers.py"
    file2.write_text("# Category: Two Pointers\n# --- Second ---\n# @problem\n# Prob 2\n# @solution\ncode 2")

    # Invalid format file that should be skipped
    file3 = tmp_path / "invalid_file.py"
    file3.write_text("some content")

    categories = load_categories()

    assert len(categories) == 2
    assert categories[0]["number"] == 1
    assert categories[0]["slug"] == "arrays-and-hashing"
    assert categories[0]["title"] == "Arrays"
    assert categories[0]["filename"] == "01_arrays_and_hashing.py"
    assert len(categories[0]["exercises"]) == 1

    assert categories[1]["number"] == 2
    assert categories[1]["slug"] == "two-pointers"
    assert categories[1]["title"] == "Two Pointers"
    assert categories[1]["filename"] == "02_two_pointers.py"
    assert len(categories[1]["exercises"]) == 1

    # Test get_category
    assert get_category("arrays-and-hashing") == categories[0]
    assert get_category("two-pointers") == categories[1]
    assert get_category("non-existent") is None
