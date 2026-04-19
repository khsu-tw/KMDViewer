"""Main application window for KMDViewer."""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QToolBar,
    QFileDialog, QMessageBox, QTextEdit, QSplitter, QStatusBar,
    QLabel, QProgressBar, QDialog, QFormLayout, QComboBox,
    QSpinBox, QDialogButtonBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QKeySequence
from PyQt5.QtWidgets import QApplication
import logging
from pathlib import Path

from src.core.markdown_processor import MarkdownProcessor
from src.core.file_manager import FileManager
from src.ui.preview_viewer import PreviewViewer

# 初始化 logger
logger = logging.getLogger(__name__)

# 使用 reportlab PDF 导出器（推薦，穩定且無系統依賴）
try:
    # 優先使用 reportlab 版本 (純 Python，無需 Pango)
    from src.core.pdf_exporter_alt import PDFExporterAlt as PDFExporter
    logger.info("使用 reportlab PDF 導出器（推薦：穩定、無系統依賴）")
except ImportError:
    # 降級到 weasyprint (需要系統庫)
    try:
        from src.core.pdf_exporter import PDFExporter
        logger.info("使用 weasyprint PDF 導出器（可能有版本兼容性問題）")
    except ImportError:
        # 最後降級到無 PDF 功能
        logger.warning("PDF 導出庫不可用，PDF 功能將被禁用")
        PDFExporter = None


class PDFExportDialog(QDialog):
    """Dialog for PDF export settings."""

    def __init__(self, parent=None):
        """Initialize the dialog.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.settings = {}
        self._setup_ui()

    def _setup_ui(self):
        """Setup the dialog UI."""
        self.setWindowTitle("Export to PDF")
        self.setModal(True)
        self.setMinimumWidth(400)

        layout = QFormLayout()

        # Page size
        self.page_size = QComboBox()
        self.page_size.addItems(["A4", "Letter", "A3", "Legal"])
        layout.addRow("Page Size:", self.page_size)

        # Margins
        self.margin_top = QSpinBox()
        self.margin_top.setValue(20)
        self.margin_top.setSuffix(" mm")
        layout.addRow("Top Margin:", self.margin_top)

        self.margin_right = QSpinBox()
        self.margin_right.setValue(20)
        self.margin_right.setSuffix(" mm")
        layout.addRow("Right Margin:", self.margin_right)

        self.margin_bottom = QSpinBox()
        self.margin_bottom.setValue(20)
        self.margin_bottom.setSuffix(" mm")
        layout.addRow("Bottom Margin:", self.margin_bottom)

        self.margin_left = QSpinBox()
        self.margin_left.setValue(20)
        self.margin_left.setSuffix(" mm")
        layout.addRow("Left Margin:", self.margin_left)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)

        self.setLayout(layout)

    def get_settings(self) -> dict:
        """Get the selected settings.

        Returns:
            Dictionary with PDF settings
        """
        return {
            "page_size": self.page_size.currentText(),
            "margin_top": f"{self.margin_top.value()}mm",
            "margin_right": f"{self.margin_right.value()}mm",
            "margin_bottom": f"{self.margin_bottom.value()}mm",
            "margin_left": f"{self.margin_left.value()}mm",
        }


class MainWindow(QMainWindow):
    """Main application window for KMDViewer."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.setWindowTitle("KMDViewer")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize core modules
        self.markdown_processor = MarkdownProcessor()
        self.pdf_exporter = PDFExporter() if PDFExporter is not None else None
        self.file_manager = FileManager()

        self.current_file: str = None
        self.current_content: str = None

        self._setup_ui()
        self._create_menus()
        self._create_toolbar()
        self._setup_connections()
        self._load_recent_files()

        logger.info("KMDViewer started")

    def _setup_ui(self):
        """Setup the user interface."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()

        # Splitter for editor and preview
        splitter = QSplitter(Qt.Horizontal)

        # Editor
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Enter or paste Markdown here...")
        editor_font = QFont("Courier", 10)
        self.editor.setFont(editor_font)
        splitter.addWidget(self.editor)

        # Preview
        self.preview = PreviewViewer()
        splitter.addWidget(self.preview)

        # Set initial splitter sizes
        splitter.setSizes([400, 800])

        main_layout.addWidget(splitter)

        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

        central_widget.setLayout(main_layout)

    def _create_menus(self):
        """Create application menus."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        open_action = file_menu.addAction("&Open File")
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_file)

        file_menu.addSeparator()

        recent_menu = file_menu.addMenu("&Recent Files")
        self.recent_files_actions = []
        for i in range(5):
            action = recent_menu.addAction("")
            action.triggered.connect(lambda checked, idx=i: self.open_recent_file(idx))
            self.recent_files_actions.append(action)

        file_menu.addSeparator()

        export_pdf = file_menu.addAction("&Export as PDF")
        export_pdf.setShortcut("Ctrl+E")
        export_pdf.triggered.connect(self.export_pdf)

        file_menu.addSeparator()

        exit_action = file_menu.addAction("E&xit")
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")

        clear_action = edit_menu.addAction("&Clear")
        clear_action.setShortcut("Ctrl+Shift+C")
        clear_action.triggered.connect(self.clear_editor)

        # View menu
        view_menu = menubar.addMenu("&View")

        refresh_action = view_menu.addAction("&Refresh Preview")
        refresh_action.setShortcut(QKeySequence.Refresh)
        refresh_action.triggered.connect(self.refresh_preview)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = help_menu.addAction("&About")
        about_action.triggered.connect(self.show_about)

    def _create_toolbar(self):
        """Create application toolbar."""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # Open file
        open_action = toolbar.addAction("Open")
        open_action.triggered.connect(self.open_file)

        # Clear
        clear_action = toolbar.addAction("Clear")
        clear_action.triggered.connect(self.clear_editor)

        toolbar.addSeparator()

        # Refresh
        refresh_action = toolbar.addAction("Refresh")
        refresh_action.triggered.connect(self.refresh_preview)

        # Export PDF
        export_action = toolbar.addAction("Export PDF")
        export_action.triggered.connect(self.export_pdf)

    def _setup_connections(self):
        """Setup signal-slot connections."""
        self.editor.textChanged.connect(self.on_text_changed)

    def _load_recent_files(self):
        """Load and display recent files."""
        recent_files = self.file_manager.get_recent_files(5)
        for i, action in enumerate(self.recent_files_actions):
            if i < len(recent_files):
                file_path = recent_files[i]
                file_name = Path(file_path).name
                action.setText(file_name)
                action.setData(file_path)
                action.setVisible(True)
            else:
                action.setVisible(False)

    def open_file(self):
        """Open a Markdown file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Markdown File",
            "",
            "Markdown Files (*.md *.markdown);;All Files (*)"
        )

        if file_path:
            self._load_file(file_path)

    def open_recent_file(self, index: int):
        """Open a recent file.

        Args:
            index: Index of recent file
        """
        if index < len(self.recent_files_actions):
            file_path = self.recent_files_actions[index].data()
            if file_path:
                self._load_file(file_path)

    def _load_file(self, file_path: str):
        """Load content from a file.

        Args:
            file_path: Path to the file
        """
        content = self.file_manager.open_file(file_path)
        if content is not None:
            self.current_file = file_path
            self.current_content = content
            self.editor.setText(content)
            self.statusBar.showMessage(f"Opened: {Path(file_path).name}")
            self.refresh_preview()
            self._load_recent_files()
        else:
            QMessageBox.critical(self, "Error", f"Failed to open file: {file_path}")

    def on_text_changed(self):
        """Handle text changes in editor."""
        # Auto-refresh preview
        self.refresh_preview()

    def refresh_preview(self):
        """Refresh the preview with current editor content."""
        content = self.editor.toPlainText()
        if content:
            html = self.markdown_processor.get_styled_html(content)
            self.preview.display_html(html)
            self.statusBar.showMessage("Preview updated")
        else:
            self.preview.clear()
            self.statusBar.showMessage("Ready")

    def clear_editor(self):
        """Clear the editor content."""
        reply = QMessageBox.question(
            self,
            "Clear Editor",
            "Are you sure you want to clear the editor?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.editor.clear()
            self.preview.clear()
            self.current_file = None
            self.current_content = None
            self.statusBar.showMessage("Editor cleared")

    def export_pdf(self):
        """Export current content as PDF."""
        if not self.editor.toPlainText().strip():
            QMessageBox.warning(self, "Empty Content", "There's no content to export.")
            return

        if self.pdf_exporter is None:
            QMessageBox.critical(
                self,
                "PDF Export Not Available",
                "PDF export libraries are not installed.\n\n"
                "Install with: pip install reportlab\n"
                "Or install full dependencies: pip install -r requirements.txt"
            )
            return

        # Show export dialog
        dialog = PDFExportDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            settings = dialog.get_settings()

            # 設定預設文件路徑（與當前 md 檔案同路徑同名）
            default_path = "document.pdf"
            if self.current_file:
                # 取得當前文件的完整路徑並改為 .pdf 副檔名
                current_path = Path(self.current_file)
                default_path = str(current_path.parent / (current_path.stem + ".pdf"))

            # Get save path
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export to PDF",
                default_path,
                "PDF Files (*.pdf)"
            )

            if file_path:
                self.pdf_exporter.update_settings(**settings)

                # Get current HTML
                content = self.editor.toPlainText()
                html = self.markdown_processor.get_styled_html(content)

                # Export
                success, error_msg = self.pdf_exporter.export_to_file(html, file_path)
                if success:
                    QMessageBox.information(
                        self,
                        "Export Successful",
                        f"PDF exported successfully to:\n{file_path}"
                    )
                    self.statusBar.showMessage(f"PDF exported: {Path(file_path).name}")
                else:
                    # 顯示詳細的錯誤訊息
                    error_details = error_msg if error_msg else "Unknown error occurred"
                    QMessageBox.critical(
                        self,
                        "Export Failed",
                        f"Failed to export PDF.\n\nError details:\n{error_details}"
                    )
                    self.statusBar.showMessage("PDF export failed")

    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About KMDViewer",
            "KMDViewer v1.0\n\n"
            "A Markdown Viewer with PDF export capability.\n\n"
            "Features:\n"
            "• Open and view Markdown files\n"
            "• Real-time preview\n"
            "• Export to PDF\n\n"
            "© 2026 by Hsu, Kai-Chun\n\n"
            "Licensed under the MIT License"
        )

    def closeEvent(self, event):
        """Handle window close event."""
        if self.editor.toPlainText() and self.current_file is None:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you want to exit?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                event.ignore()
                return

        event.accept()
        logger.info("KMDViewer closed")
