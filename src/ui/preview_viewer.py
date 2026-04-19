"""Preview viewer widget for displaying rendered HTML."""

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import pyqtSignal, QUrl, Qt
from PyQt5.QtGui import QIcon


class PreviewViewer(QWebEngineView):
    """Web view widget for displaying rendered Markdown as HTML."""

    content_updated = pyqtSignal()

    def __init__(self, parent=None):
        """Initialize the preview viewer.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the web view."""
        # Enable JavaScript and other features
        settings = self.settings()
        settings.setAttribute(settings.JavascriptEnabled, True)
        settings.setAttribute(settings.LocalContentCanAccessFileUrls, True)

    def display_html(self, html_content: str):
        """Display HTML content in the viewer.

        Args:
            html_content: HTML string to display
        """
        self.setHtml(html_content)
        self.content_updated.emit()

    def display_file(self, file_path: str):
        """Display HTML file in the viewer.

        Args:
            file_path: Path to HTML file
        """
        try:
            file_url = QUrl.fromLocalFile(file_path)
            self.load(file_url)
            self.content_updated.emit()
        except Exception as e:
            error_html = f"<p><strong>Error loading file:</strong> {str(e)}</p>"
            self.display_html(error_html)

    def clear(self):
        """Clear the viewer content."""
        self.setHtml("")
