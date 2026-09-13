import re
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

class MermaidPreprocessor(Preprocessor):
    MERMAID_RE = re.compile(r'^```mermaid\s*\n(.*?)\n```', re.DOTALL | re.MULTILINE)

    def run(self, lines):
        text = '\n'.join(lines)
        def replace_mermaid(match):
            return f'<div class="mermaid">\n{match.group(1)}\n</div>'
        text = self.MERMAID_RE.sub(replace_mermaid, text)
        return text.split('\n')

class MermaidExtension(Extension):
    def extendMarkdown(self, md):
        # Register before fenced_code (which has priority 25)
        md.preprocessors.register(MermaidPreprocessor(md), 'mermaid', 105)

def makeExtension(**kwargs):
    return MermaidExtension(**kwargs)
