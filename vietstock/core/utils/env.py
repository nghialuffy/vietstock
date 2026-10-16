from __future__ import annotations

import logging
import os
import platform
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def get_vietstock_directory() -> Path:
    """
    Determine .vietstock directory based on environment.
    Reuses logic from core.config.ggcolab

    Returns:
        Path: Path to .vietstock directory
    """
    try:
        from vietstock.core.config.ggcolab import (
            get_vietstock_directory as ggcolab_get_vietstock_dir,
        )

        return ggcolab_get_vietstock_dir()
    except ImportError:
        # Fallback if ggcolab not loaded yet
        return Path.home() / ".vietstock"


def get_platform():
    """Get the name of the running operating system"""
    PLATFORM = platform.system()
    return PLATFORM


def get_hosting_service():
    """Identify cloud service or development environment currently running"""
    hosting_service = "Local or Unknown"
    try:
        if "google.colab" in sys.modules:
            hosting_service = "Google Colab"
        elif "CODESPACE_NAME" in os.environ:
            hosting_service = "Github Codespace"
        elif "REPLIT_USER" in os.environ:
            hosting_service = "Replit"
        elif "KAGGLE_CONTAINER_NAME" in os.environ:
            hosting_service = "Kaggle"
        elif "SPACE_HOST" in os.environ and ".hf.space" in os.environ["SPACE_HOST"]:
            hosting_service = "Hugging Face Spaces"
    except Exception:
        pass
    return hosting_service


def get_package_path(package="vietstock"):
    """Get the path of any Python package"""
    from importlib.util import find_spec

    spec = find_spec(package)
    if spec and spec.origin:
        package_path = spec.origin  # Path to the package's main file
    elif spec and spec.submodule_search_locations:
        package_path = spec.submodule_search_locations[0]  # Path to the package directory
    else:
        package_path = None
    return package_path


def get_username():
    """
    Get the current username of the system.
    """
    try:
        username = os.getlogin()
        return username
    except OSError as e:
        print(f"Error: {e}")
        return None


def get_cwd():
    """Return current working directory"""
    try:
        cwd = os.getcwd()
        return cwd
    except OSError as e:
        print(f"Error: {e}")
        return None


def get_path_delimiter():
    """
    Detect the running OS and return the appropriate file path delimiter.
    """
    return "\\" if os.name == "nt" else "/"


def detect_venv() -> dict:
    """
    Detect the current virtual environment and return its info.
    Centralized environment detection for vietstock ecosystem.

    Returns:
        dict: Contains 'path' (venv path or None), 'is_active' (bool),
              'type' (str: 'venv', 'conda', 'system'), 'python_exe' (str)
    """
    venv_path = None
    is_active = False
    venv_type = "system"
    python_exe = sys.executable

    # Check VIRTUAL_ENV environment variable (most reliable)
    if "VIRTUAL_ENV" in os.environ:
        venv_path = os.environ["VIRTUAL_ENV"]
        is_active = True
        if "conda" in venv_path.lower():
            venv_type = "conda"
        else:
            venv_type = "venv"
        # Get python executable for this venv
        if os.name == "nt":
            python_exe = os.path.join(venv_path, "Scripts", "python.exe")
        else:
            python_exe = os.path.join(venv_path, "bin", "python")
    # Check sys.prefix vs sys.base_prefix (for venv)
    elif hasattr(sys, "base_prefix") and sys.prefix != sys.base_prefix:
        venv_path = sys.prefix
        is_active = True
        venv_type = "venv"
        python_exe = sys.executable
    # Check for conda environment
    elif "CONDA_PREFIX" in os.environ:
        venv_path = os.environ["CONDA_PREFIX"]
        is_active = True
        venv_type = "conda"
        if os.name == "nt":
            python_exe = os.path.join(venv_path, "python.exe")
        else:
            python_exe = os.path.join(venv_path, "bin", "python")
    else:
        python_exe = sys.executable

    return {
        "path": venv_path,
        "is_active": is_active,
        "type": venv_type,
        "python_exe": python_exe,
    }


def get_python_executable() -> str:
    """
    Get the path to the Python executable for current environment.

    Returns:
        str: Path to Python executable
    """
    venv_info = detect_venv()
    return venv_info["python_exe"]


def get_python_version_string() -> str:
    """
    Get Python version string for current environment.

    Returns:
        str: Python version (e.g., "3.11.4" or "3.14")
    """
    return f"{sys.version_info.major}.{sys.version_info.minor}"


def is_venv_active() -> bool:
    """
    Check if running in an active virtual environment.

    Returns:
        bool: True if in venv or conda environment
    """
    return detect_venv().get("is_active", False)


def get_venv_type() -> str:
    """
    Get type of current virtual environment.

    Returns:
        str: 'venv', 'conda', or 'system'
    """
    return detect_venv().get("type", "system")
