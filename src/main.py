"""Main entry point for KMDViewer application."""

import sys
import logging
from pathlib import Path
from PyQt5.QtWidgets import QApplication

from src.ui.main_window import MainWindow

# Configure logging - output to both file and console
def setup_logging():
    """設定日誌輸出到檔案和控制台"""
    log_dir = Path.home() / '.kmdviewer'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'kmdviewer.log'

    # 創建 logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.info(f"日誌檔案位置: {log_file}")
    except Exception as e:
        logger.warning(f"無法創建日誌檔案: {e}")

setup_logging()


def main():
    """Run the KMDViewer application."""
    app = QApplication(sys.argv)

    # Set application metadata
    app.setApplicationName("KMDViewer")
    app.setApplicationVersion("1.0")

    # Create and show main window
    window = MainWindow()
    window.show()

    # Run the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
