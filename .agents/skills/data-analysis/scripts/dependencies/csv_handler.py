import csv
import pandas as pd
from pathlib import Path
from .errors import DataLoadError


def detect_csv_params(file_path: Path) -> tuple[str, str]:
    """
    Attempts to sniff the separator and encoding of a CSV file.
    Returns a tuple of (separator, encoding).
    """
    encoding = "utf-8"
    sep = ","

    # Try detecting encoding (basic fallback from utf-8 to latin-1)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            sample_data = f.read(4096)
    except UnicodeDecodeError:
        encoding = "latin-1"
        with open(file_path, "r", encoding="latin-1") as f:
            sample_data = f.read(4096)

    # Sniff separator
    try:
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample_data, delimiters=",;\t|")
        sep = dialect.delimiter
    except csv.Error:
        # Fallback to comma if sniffer fails
        pass

    return sep, encoding


def load_csv(file_path: Path) -> pd.DataFrame:
    """
    Loads a CSV file into a pandas DataFrame using dynamic sniffing.
    """
    sep, encoding = detect_csv_params(file_path)
    try:
        df = pd.read_csv(file_path, sep=sep, encoding=encoding, on_bad_lines="skip")
        return df
    except Exception as e:
        raise DataLoadError(f"Failed to load CSV file '{file_path}': {str(e)}")
