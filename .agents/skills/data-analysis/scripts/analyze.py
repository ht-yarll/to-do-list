#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path


# Important: Run environment validation BEFORE importing pandas
try:
    from dependencies.env_check import validate_environment
    from dependencies.errors import DependencyError

    validate_environment()
except DependencyError as e:
    print(str(e), file=sys.stderr)
    sys.exit(1)
except ImportError:
    # If the env_check itself fails (which it shouldn't), catch it
    pass

import pandas as pd
from dependencies import load_csv, load_json, load_excel, FormatError, DataLoadError


def get_format(file_path: Path, explicit_format: str) -> str:
    """Infers the format from extension if not explicitly provided."""
    if explicit_format:
        return explicit_format.lower()

    ext = file_path.suffix.lower()
    if ext == ".csv":
        return "csv"
    elif ext in (".json", ".jsonl"):
        return "json"
    elif ext in (".xls", ".xlsx"):
        return "excel"
    else:
        raise FormatError(
            f"Cannot infer format for extension '{ext}'. Please use --format."
        )


def print_summary(
    df: pd.DataFrame, file_path: Path, fmt: str, sample_size: int
) -> None:
    """Prints the standardized data summary for the agent."""
    print("=" * 40)
    print("STANDARDIZED DATA SUMMARY")
    print("=" * 40)
    print(f"File Path : {file_path}")
    print(f"Format    : {fmt.upper()}")
    print(f"Shape     : {df.shape[0]} rows, {df.shape[1]} columns")
    print("-" * 40)
    print("SCHEMA & DATA TYPES")
    print("-" * 40)

    # Create schema summary
    schema_info = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].count()
        schema_info.append(f"  - {col}: {dtype} (Non-Null: {non_null})")
    print("\n".join(schema_info))

    print("-" * 40)
    print(f"SAMPLE DATA (Top {sample_size} rows)")
    print("-" * 40)
    print(df.head(sample_size).to_string())
    print("=" * 40)


def main():
    parser = argparse.ArgumentParser(
        description="Extract Standardized Data Summary from tabular files."
    )
    parser.add_argument(
        "--file", type=str, required=True, help="Path to the data file."
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["csv", "json", "excel"],
        help="Force file format.",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=5,
        help="Number of rows to preview (default 5).",
    )

    args = parser.parse_args()
    file_path = Path(args.file)

    if not file_path.exists() or not file_path.is_file():
        print(f"Error: File '{file_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        fmt = get_format(file_path, args.format)

        if fmt == "csv":
            df = load_csv(file_path)
        elif fmt == "json":
            df = load_json(file_path)
        elif fmt == "excel":
            df = load_excel(file_path)
        else:
            raise FormatError(f"Unsupported format '{fmt}'.")

        print_summary(df, file_path, fmt, args.sample_size)

    except (FormatError, DataLoadError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
