class DataAnalysisError(Exception):
    """Base exception class for data analysis script."""

    pass


class DependencyError(DataAnalysisError):
    """Raised when required libraries are missing."""

    pass


class FormatError(DataAnalysisError):
    """Raised when the file format is unsupported or unrecognized."""

    pass


class DataLoadError(DataAnalysisError):
    """Raised when pandas fails to load the data file."""

    pass
