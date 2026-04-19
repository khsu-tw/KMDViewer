"""PDF export module for converting HTML to PDF."""

from pathlib import Path
from weasyprint import HTML, CSS
from io import BytesIO
import logging

logger = logging.getLogger(__name__)


class PDFExporter:
    """Exports HTML content to PDF files."""

    # Default page settings
    DEFAULT_SETTINGS = {
        "page_size": "A4",
        "margin_top": "20mm",
        "margin_right": "20mm",
        "margin_bottom": "20mm",
        "margin_left": "20mm",
    }

    def __init__(self, settings: dict = None):
        """Initialize PDF exporter with settings.

        Args:
            settings: Dictionary with page settings (page_size, margins, etc.)
        """
        self.settings = {**self.DEFAULT_SETTINGS, **(settings or {})}

    def export_to_file(self, html_content: str, output_path: str) -> tuple[bool, str]:
        """Export HTML content to a PDF file.

        Args:
            html_content: HTML string to export
            output_path: Path where PDF will be saved

        Returns:
            tuple[bool, str]: (成功與否, 錯誤訊息)
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Create CSS for page settings
            css_string = self._generate_css()

            # Convert HTML to PDF
            html_obj = HTML(string=html_content)
            css_obj = CSS(string=css_string)

            html_obj.write_pdf(
                output_path,
                stylesheets=[css_obj]
            )

            logger.info(f"PDF exported successfully to {output_path}")
            return True, ""

        except Exception as e:
            error_msg = f"PDF 導出失敗: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return False, error_msg

    def export_to_bytes(self, html_content: str) -> bytes:
        """Export HTML content to PDF bytes.

        Args:
            html_content: HTML string to export

        Returns:
            PDF content as bytes
        """
        try:
            css_string = self._generate_css()
            html_obj = HTML(string=html_content)
            css_obj = CSS(string=css_string)

            pdf_bytes = html_obj.write_pdf(stylesheets=[css_obj])
            return pdf_bytes

        except Exception as e:
            logger.error(f"Failed to export PDF to bytes: {str(e)}")
            return b""

    def _generate_css(self) -> str:
        """Generate CSS for page settings.

        Returns:
            CSS string for page configuration
        """
        margins = (
            f"margin-top: {self.settings['margin_top']}; "
            f"margin-right: {self.settings['margin_right']}; "
            f"margin-bottom: {self.settings['margin_bottom']}; "
            f"margin-left: {self.settings['margin_left']}"
        )

        size = self.settings.get("page_size", "A4")

        css = f"""
        @page {{
            size: {size};
            {margins};
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}

        a {{
            color: #0366d6;
        }}

        code {{
            background-color: rgba(27, 31, 35, 0.05);
            border-radius: 3px;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 85%;
            padding: 0.2em 0.4em;
        }}

        pre {{
            background-color: #f6f8fa;
            border-radius: 6px;
            padding: 16px;
            overflow-x: auto;
            margin-bottom: 16px;
        }}

        blockquote {{
            border-left: 4px solid #ddd;
            color: #666;
            padding: 0 15px;
            margin: 0 0 16px 0;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 16px;
        }}

        table th, table td {{
            border: 1px solid #ddd;
            padding: 8px 13px;
        }}

        table tr:nth-child(2n) {{
            background-color: #f6f8fa;
        }}

        img {{
            max-width: 100%;
            height: auto;
            margin: 16px 0;
        }}
        """
        return css

    def update_settings(self, **kwargs):
        """Update exporter settings.

        Args:
            **kwargs: Settings to update (page_size, margin_top, etc.)
        """
        self.settings.update(kwargs)
