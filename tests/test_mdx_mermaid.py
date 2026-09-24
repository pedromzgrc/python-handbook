import markdown
import pytest
from mdx_mermaid import MermaidExtension, makeExtension

def test_mermaid_extension_basic():
    text = """Some text before.

```mermaid
graph TD;
    A-->B;
```

Some text after."""

    md = markdown.Markdown(extensions=[MermaidExtension()])
    html = md.convert(text)

    assert '<div class="mermaid">' in html
    assert 'graph TD;' in html
    assert 'A-->B;' in html
    assert '<p>Some text before.</p>' in html
    assert '<p>Some text after.</p>' in html

def test_mermaid_extension_empty():
    text = "```mermaid\n\n```"
    md = markdown.Markdown(extensions=[MermaidExtension()])
    html = md.convert(text)
    assert '<div class="mermaid">' in html
    assert '</div>' in html

def test_mermaid_extension_multiple():
    text = """```mermaid
graph TD;
    A-->B;
```

Some intermediate text.

```mermaid
graph TD;
    C-->D;
```"""
    md = markdown.Markdown(extensions=[MermaidExtension()])
    html = md.convert(text)
    assert html.count('<div class="mermaid">') == 2
    assert 'A-->B;' in html
    assert 'C-->D;' in html

def test_makeExtension():
    ext = makeExtension()
    assert isinstance(ext, MermaidExtension)
