"""Markdown processing module for converting Markdown to HTML."""

from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound


class MarkdownProcessor:
    """Processes Markdown content and converts it to HTML."""

    def __init__(self):
        """Initialize the Markdown processor with plugins."""
        self.md = MarkdownIt("commonmark", {
            "highlight": self._highlight_code,
            "typographer": True,
            "linkify": True
        })

        # Add plugins for enhanced Markdown support
        self.md.use(front_matter_plugin)
        self.md.use(deflist_plugin)
        self.md.use(tasklists_plugin)

    def _highlight_code(self, code: str, lang: str = None, attrs: str = None, **_) -> str:
        """Highlight code blocks using Pygments."""
        if not lang:
            try:
                lexer = guess_lexer(code)
            except ClassNotFound:
                return f"<pre><code>{self._escape_html(code)}</code></pre>"
        else:
            try:
                lexer = get_lexer_by_name(lang)
            except ClassNotFound:
                return f"<pre><code>{self._escape_html(code)}</code></pre>"

        formatter = HtmlFormatter(style="default", full=False)
        highlighted = highlight(code, lexer, formatter)
        return f"<pre>{highlighted}</pre>"

    @staticmethod
    def _escape_html(text: str) -> str:
        """Escape HTML special characters."""
        return (text
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#39;"))

    def process(self, markdown_text: str) -> str:
        """Convert Markdown text to HTML.

        Args:
            markdown_text: Raw Markdown content

        Returns:
            HTML string
        """
        try:
            html = self.md.render(markdown_text)
            return html
        except Exception as e:
            return f"<p><strong>Error processing Markdown:</strong> {str(e)}</p>"

    def get_styled_html(self, markdown_text: str) -> str:
        """Get complete HTML with embedded styles.

        Args:
            markdown_text: Raw Markdown content

        Returns:
            Complete HTML document string
        """
        content = self.process(markdown_text)

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #fff;
            padding: 20px;
            max-width: 900px;
            margin: 0 auto;
        }}

        h1, h2, h3, h4, h5, h6 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }}

        h1 {{ font-size: 2em; padding-bottom: 0.3em; }}
        h2 {{ font-size: 1.5em; padding-bottom: 0.3em; }}
        h3 {{ font-size: 1.25em; }}
        h4 {{ font-size: 1em; }}
        h5 {{ font-size: 0.875em; }}
        h6 {{ font-size: 0.85em; color: #6a737d; }}

        p {{
            margin-bottom: 16px;
        }}

        a {{
            color: #0366d6;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        code {{
            background-color: #e8e8e8;
            border-radius: 3px;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 85%;
            padding: 0.2em 0.4em;
        }}

        pre {{
            background-color: #e8e8e8;
            border-radius: 6px;
            padding: 16px;
            overflow-x: auto;
            margin-bottom: 16px;
        }}

        pre code {{
            background-color: transparent;
            padding: 0;
            color: #24292e;
        }}

        .highlight {{
            background-color: #f6f8fa;
        }}

        blockquote {{
            border-left: 4px solid #ddd;
            color: #666;
            padding: 0 15px;
            margin: 0 0 16px 0;
        }}

        ul, ol {{
            margin-bottom: 16px;
            padding-left: 2em;
        }}

        li {{
            margin-bottom: 8px;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 16px;
        }}

        table th, table td {{
            border: 1px solid #ddd;
            padding: 8px 13px;
            text-align: left;
        }}

        table tr:nth-child(2n) {{
            background-color: #f6f8fa;
        }}

        img {{
            max-width: 100%;
            height: auto;
            margin: 16px 0;
        }}

        hr {{
            background-color: #e1e4e8;
            border: 0;
            height: 2px;
            margin: 24px 0;
        }}

        .task-list-item {{
            list-style-type: none;
        }}

        .task-list-item-checkbox {{
            margin-right: 8px;
        }}
    </style>
</head>
<body>
    {content}
</body>
</html>"""
        return html
