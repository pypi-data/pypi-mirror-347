import subprocess
from pathlib import Path
from typing import List, Optional

from loguru import logger


class ProjectRootFinder:
    """
    ProjectRootFinder
    TODO git, svn, hg查找均未考虑需要向上查找的情况
    """

    _cache = None

    def __init__(self, start_path: str = None):
        self.start_path = Path(start_path or __file__).parent.resolve()

    def _find_by_git(self) -> Optional[Path]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=self.start_path,
                capture_output=True,
                text=True,
                check=True
            )
            return Path(result.stdout.strip())
        except Exception as e:
            logger.debug(f"Failed to find project root path by git")
        return None

    def _find_by_svn(self) -> Optional[Path]:
        try:
            result = subprocess.run(
                ["svn", "info", "--show-item", "wcroot-abspath", str(self.start_path)],
                cwd=self.start_path,
                capture_output=True,
                text=True,
                check=True
            )
            return Path(result.stdout.strip())
        except Exception:
            logger.debug(f"Failed to find project root path by svn")
        return None

    def _find_by_hg(self) -> Optional[Path]:
        try:
            result = subprocess.run(
                ["hg", "root"],
                cwd=self.start_path,
                capture_output=True,
                text=True,
                check=True
            )
            return Path(result.stdout.strip())
        except Exception as e:
            logger.debug(f"Failed to find project root path by hg")
        return None

    def _find_by_markers(self, markers: List[str] = None) -> Optional[Path]:
        if markers is None:
            markers = [
                "setup.py", "pyproject.toml", "setup.cfg",
                ".git", ".gitignore", "requirements.txt",
                "Pipfile", "poetry.lock", "Makefile",
                ".idea", ".vscode", ".hg"
            ]
        current = self.start_path
        while current != current.parent:
            for marker in markers:
                if (current / marker).exists():
                    return current
            current = current.parent
        return None

    def _find_by_structure(self) -> Optional[Path]:
        current = self.start_path
        while current != current.parent:
            src_dir = current / "src"
            lib_dir = current / "lib"
            if (src_dir.exists() and src_dir.is_dir()) or (lib_dir.exists() and lib_dir.is_dir()):
                py_files = list(current.glob("*.py"))
                if len(py_files) > 0 or (current / "__init__.py").exists():
                    return current
            current = current.parent
        return None

    def find_root(self, search_methods: List[str] = None) -> Path:

        if self._cache:
            return self._cache

        if search_methods is None:
            search_methods = ["git", "svn", "hg", "markers", "structure"]

        for search_method in search_methods:
            try:
                if search_method == "git":
                    result = self._find_by_git()
                elif search_method == "svn":
                    result = self._find_by_svn()
                elif search_method == "hg":
                    result = self._find_by_hg()
                elif search_method == "markers":
                    result = self._find_by_markers()
                elif search_method == "structure":
                    result = self._find_by_structure()
                else:
                    continue
            except Exception as e:
                logger.warning(f"Failed: {e} to find project root by search method: {search_method}")
                continue

            if result:
                self._cache = result
                return result

        raise FileNotFoundError("Unable to locate project root directory")


def get_root_path(start_path: str = None, search_methods: List[str] = None) -> Path:
    """
    Get project root path
    :param start_path: start path
    :param search_methods: search methods
    :return: project root path
    """
    finder = ProjectRootFinder(start_path)
    return finder.find_root(search_methods)
