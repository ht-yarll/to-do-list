import importlib.util
import shutil
from .errors import DependencyError

REQUIRED_PACKAGES = {"pandas": "pandas", "openpyxl": "openpyxl"}


def detect_package_manager() -> str:
    """Detects which package manager is available."""
    if shutil.which("uv"):
        return "uv add"
    if shutil.which("poetry"):
        return "poetry add"
    return "pip install"


def validate_environment() -> None:
    """
    Validates that required packages are installed.
    Raises DependencyError if any are missing.
    """
    missing = []
    for module_name, package_name in REQUIRED_PACKAGES.items():
        if importlib.util.find_spec(module_name) is None:
            missing.append(package_name)

    if missing:
        pm_cmd = detect_package_manager()
        missing_str = " ".join(missing)
        error_msg = (
            f"Missing required dependencies: {', '.join(missing)}.\n"
            f"Detected package manager. Please run:\n"
            f"    {pm_cmd} {missing_str}\n"
        )
        raise DependencyError(error_msg)
