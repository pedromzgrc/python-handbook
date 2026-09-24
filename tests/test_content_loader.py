import pytest
from content_loader import _parse_modules

def test_parse_modules_basic():
    body = [
        "# --- First Module ---",
        "# Theory: This is the theory.",
        "",
        "print('Hello World')",
        ""
    ]
    modules = _parse_modules(body)
    assert len(modules) == 1
    assert modules[0]["title"] == "First Module"
    assert modules[0]["slug"] == "first-module"
    assert modules[0]["theory"] == "This is the theory."
    assert modules[0]["code"] == "print('Hello World')"

def test_parse_modules_no_theory():
    body = [
        "# --- No Theory Module ---",
        "print('Just code')",
    ]
    modules = _parse_modules(body)
    assert len(modules) == 1
    assert modules[0]["title"] == "No Theory Module"
    assert modules[0]["slug"] == "no-theory-module"
    assert modules[0]["theory"] == ""
    assert modules[0]["code"] == "print('Just code')"

def test_parse_modules_multiple():
    body = [
        "# --- Module One ---",
        "# Theory: Theory one.",
        "code_one()",
        "# --- Module Two ---",
        "code_two()",
    ]
    modules = _parse_modules(body)
    assert len(modules) == 2
    assert modules[0]["title"] == "Module One"
    assert modules[0]["theory"] == "Theory one."
    assert modules[0]["code"] == "code_one()"

    assert modules[1]["title"] == "Module Two"
    assert modules[1]["theory"] == ""
    assert modules[1]["code"] == "code_two()"

def test_parse_modules_whitespace_trimming():
    body = [
        "# --- Whitespace Module ---",
        "# Theory: Should trim blank lines.",
        "   ",
        "",
        "print('code here')",
        "   ",
        ""
    ]
    modules = _parse_modules(body)
    assert len(modules) == 1
    assert modules[0]["theory"] == "Should trim blank lines."
    assert modules[0]["code"] == "print('code here')"

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

def test_parse_modules_empty():
    body = [
        "# --- Empty Module ---"
    ]
    modules = _parse_modules(body)
    assert len(modules) == 1
    assert modules[0]["title"] == "Empty Module"
    assert modules[0]["theory"] == ""
    assert modules[0]["code"] == ""
