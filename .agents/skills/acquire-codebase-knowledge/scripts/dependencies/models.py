from typing import TypedDict

class CodeMetrics(TypedDict):
    """Metrics collected during codebase analysis."""
    total_files: int
    by_extension: dict[str, int]
    by_language: dict[str, int]
    total_lines: int
    largest_files: list[str]
