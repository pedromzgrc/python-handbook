import pytest
from pathlib import Path
import content_loader
from content_loader import _slugify, _parse_modules, load_units

def test_slugify():
    assert _slugify("Hello World") == "hello-world"
    assert _slugify("Test") == "test"
    assert _slugify("A B C") == "a-b-c"
    assert _slugify("") == ""

def test_parse_modules_basic():
    body_lines = [
        "# --- Module 1 ---",
        "# Theory: This is the theory.",
        "def func1():",
        "    pass",
        "",
        "# --- Module 2 ---",
        "# Theory: Another theory",
        "def func2():",
        "    return 1",
    ]
    modules = _parse_modules(body_lines)
    assert len(modules) == 2

    assert modules[0]["title"] == "Module 1"
    assert modules[0]["slug"] == "module-1"
    assert modules[0]["theory"] == "This is the theory."
    assert modules[0]["code"] == "def func1():\n    pass"

    assert modules[1]["title"] == "Module 2"
    assert modules[1]["slug"] == "module-2"
    assert modules[1]["theory"] == "Another theory"
    assert modules[1]["code"] == "def func2():\n    return 1"

def test_parse_modules_no_theory():
    body_lines = [
        "# --- Just Code ---",
        "print('hello')"
    ]
    modules = _parse_modules(body_lines)
    assert len(modules) == 1
    assert modules[0]["title"] == "Just Code"
    assert modules[0]["theory"] == ""
    assert modules[0]["code"] == "print('hello')"

def test_parse_modules_empty():
    assert _parse_modules([]) == []

def test_parse_modules_extra_newlines():
    body_lines = [
        "# --- Mod ---",
        "# Theory: xyz",
        "",
        "",
        "x = 1",
        "",
        ""
    ]
    modules = _parse_modules(body_lines)
    assert len(modules) == 1
    assert modules[0]["code"] == "x = 1"

def test_parse_modules_ignore_pre_header_content():
    body = [
        "This is some extra stuff before the first header",
        "# that should just be ignored",
        "# --- The Real Module ---",
        "# Theory: It works.",
        "x = 1"
    ]
    modules = _parse_modules(body)
    assert len(modules) == 1
    assert modules[0]["title"] == "The Real Module"
    assert modules[0]["theory"] == "It works."
    assert modules[0]["code"] == "x = 1"

def test_parse_modules_empty_header_only():
    body = [
        "# --- Empty Module ---"
    ]
    modules = _parse_modules(body)
    assert len(modules) == 1
    assert modules[0]["title"] == "Empty Module"
    assert modules[0]["theory"] == ""
    assert modules[0]["code"] == ""

@pytest.fixture(autouse=True)
def clear_lru_cache():
    """Clear the LRU cache on load_units before each test."""
    load_units.cache_clear()
    yield

def test_load_units_empty_dir(monkeypatch, tmp_path):
    monkeypatch.setattr(content_loader, "CONTENT_DIR", tmp_path)
    assert load_units() == []

def test_load_units_success(monkeypatch, tmp_path):
    monkeypatch.setattr(content_loader, "CONTENT_DIR", tmp_path)

    # Valid file with default title (from filename)
    file1 = tmp_path / "01_intro_basics.py"
    file1.write_text("# Chapter 1: Intro Basics\n# --- Hello --- \n# Theory: World\nprint('hello')\n")

    # Valid file with custom chapter title
    file2 = tmp_path / "02_advanced.py"
    file2.write_text("# Chapter 2: The Advanced Stuff\n# --- Concept --- \n# Theory: Wow\npass\n")

    # Invalid files that should be ignored
    file3 = tmp_path / "invalid_name.py"
    file3.write_text("print('no')")

    file4 = tmp_path / "03_bad_ext.txt"
    file4.write_text("print('no')")

    units = load_units()

    assert len(units) == 2

    # Verify unit 1
    assert units[0]["number"] == 1
    assert units[0]["slug"] == "intro-basics"
    assert units[0]["title"] == "Intro Basics"
    assert units[0]["filename"] == "01_intro_basics.py"
    assert len(units[0]["modules"]) == 1
    assert units[0]["modules"][0]["title"] == "Hello"

    # Verify unit 2
    assert units[1]["number"] == 2
    assert units[1]["slug"] == "advanced"
    assert units[1]["title"] == "The Advanced Stuff"
    assert units[1]["filename"] == "02_advanced.py"
    assert len(units[1]["modules"]) == 1
    assert units[1]["modules"][0]["title"] == "Concept"

def test_load_units_ordering(monkeypatch, tmp_path):
    monkeypatch.setattr(content_loader, "CONTENT_DIR", tmp_path)

    # Create them out of order
    (tmp_path / "10_ten.py").write_text("")
    (tmp_path / "02_two.py").write_text("")
    (tmp_path / "05_five.py").write_text("")

    units = load_units()

    assert len(units) == 3
    assert units[0]["number"] == 2
    assert units[1]["number"] == 5
    assert units[2]["number"] == 10
