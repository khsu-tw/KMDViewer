"""File management module for handling Markdown files."""

from pathlib import Path
import json
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class FileManager:
    """Manages file operations for Markdown documents."""

    SUPPORTED_EXTENSIONS = {".md", ".markdown", ".mdown", ".mkdn", ".mdwn", ".mkd", ".mdtext"}
    CONFIG_DIR = Path.home() / ".mdviewer"
    RECENT_FILES_CONFIG = CONFIG_DIR / "recent_files.json"

    def __init__(self):
        """Initialize file manager."""
        self.config_dir = self.CONFIG_DIR
        self.config_dir.mkdir(exist_ok=True)
        self.recent_files: List[str] = self._load_recent_files()

    def open_file(self, file_path: str) -> Optional[str]:
        """Open and read a Markdown file.

        Args:
            file_path: Path to the Markdown file

        Returns:
            File content if successful, None otherwise
        """
        try:
            path = Path(file_path)

            if not path.exists():
                logger.error(f"File not found: {file_path}")
                return None

            if not self._is_supported_format(path):
                logger.error(f"Unsupported file format: {file_path}")
                return None

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            self._add_to_recent_files(str(path.absolute()))
            logger.info(f"File opened successfully: {file_path}")
            return content

        except UnicodeDecodeError:
            logger.error(f"Failed to decode file (not UTF-8): {file_path}")
            return None
        except Exception as e:
            logger.error(f"Error opening file: {str(e)}")
            return None

    def save_file(self, file_path: str, content: str) -> bool:
        """Save content to a Markdown file.

        Args:
            file_path: Path where file will be saved
            content: Content to save

        Returns:
            True if successful, False otherwise
        """
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            self._add_to_recent_files(str(path.absolute()))
            logger.info(f"File saved successfully: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            return False

    def is_markdown_file(self, file_path: str) -> bool:
        """Check if file is a supported Markdown format.

        Args:
            file_path: Path to check

        Returns:
            True if file is a supported Markdown file
        """
        return self._is_supported_format(Path(file_path))

    def get_recent_files(self, limit: int = 10) -> List[str]:
        """Get list of recently opened files.

        Args:
            limit: Maximum number of recent files to return

        Returns:
            List of file paths
        """
        # Filter for files that still exist
        valid_files = [f for f in self.recent_files if Path(f).exists()]
        self.recent_files = valid_files
        self._save_recent_files()
        return valid_files[:limit]

    def clear_recent_files(self):
        """Clear the recent files list."""
        self.recent_files = []
        self._save_recent_files()

    def _is_supported_format(self, path: Path) -> bool:
        """Check if file has a supported Markdown extension.

        Args:
            path: Path to check

        Returns:
            True if extension is supported
        """
        return path.suffix.lower() in self.SUPPORTED_EXTENSIONS

    def _add_to_recent_files(self, file_path: str):
        """Add file to recent files list.

        Args:
            file_path: Absolute path to add
        """
        # Remove duplicates
        self.recent_files = [f for f in self.recent_files if f != file_path]
        # Add to beginning
        self.recent_files.insert(0, file_path)
        # Keep only 20 most recent
        self.recent_files = self.recent_files[:20]
        self._save_recent_files()

    def _load_recent_files(self) -> List[str]:
        """Load recent files from config.

        Returns:
            List of recent file paths
        """
        try:
            if self.RECENT_FILES_CONFIG.exists():
                with open(self.RECENT_FILES_CONFIG, "r") as f:
                    data = json.load(f)
                    return data.get("recent_files", [])
        except Exception as e:
            logger.error(f"Error loading recent files: {str(e)}")

        return []

    def _save_recent_files(self):
        """Save recent files list to config."""
        try:
            with open(self.RECENT_FILES_CONFIG, "w") as f:
                json.dump({"recent_files": self.recent_files}, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving recent files: {str(e)}")
