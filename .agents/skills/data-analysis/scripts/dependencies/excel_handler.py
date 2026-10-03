import pandas as pd
from pathlib import Path
from .errors import DataLoadError


def load_excel(file_path: Path) -> pd.DataFrame:
    """
    Loads an Excel file into a pandas DataFrame.
    Automatically handles .xls and .xlsx extensions.
    """
    try:
        # Uses openpyxl for xlsx and xlrd for xls (if available, pandas handles engine selection)
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        raise DataLoadError(f"Failed to load Excel file '{file_path}': {str(e)}")
