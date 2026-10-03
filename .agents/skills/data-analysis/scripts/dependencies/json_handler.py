import pandas as pd
from pathlib import Path
from .errors import DataLoadError


def load_json(file_path: Path) -> pd.DataFrame:
    """
    Loads a JSON file into a pandas DataFrame.
    Attempts to read as standard JSON first, and falls back to lines=True
    if it encounters an error (for JSONL formats).
    """
    try:
        try:
            df = pd.read_json(file_path)
            return df
        except ValueError:
            # Fallback for JSON Lines
            df = pd.read_json(file_path, lines=True)
            return df
    except Exception as e:
        raise DataLoadError(f"Failed to load JSON file '{file_path}': {str(e)}")
