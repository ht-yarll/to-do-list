---
name: data_analysis
description: Guide for reading, previewing, and analyzing data from CSV, JSON, and Excel files. Use this skill when users want to query tabular datasets, check data standardization, or explore data contents. This skill provides a lightweight standard summary of the file so you can answer user questions.
---

# Data Analysis Skill

## Overview

This skill helps you extract a standardized data summary (schema, data types, sample rows) from CSV, JSON, and Excel files. By running the provided Python script, you can quickly understand the shape and content of a dataset without writing custom pandas scripts from scratch.

## When to Use This Skill

Use this skill when users:
- Ask about the contents of a specific CSV, JSON, or Excel file.
- Need to know if a column is standardized (e.g., for BigQuery).
- Want to compare a dataset with previous results.
- Request a quick summary or preview of tabular data.

## General Workflow

### Step 1: Run the Analyze Script

Run the `analyze.py` script against the target file. The script will automatically infer the file format based on its extension.

```bash
python3 scripts/analyze.py --file /path/to/data.csv
```

Optional arguments:
- `--format`: Explicitly specify the format (`csv`, `json`, `excel`) if the file extension is missing or non-standard.
- `--sample-size`: Number of sample rows to print (default is 5).

```bash
python3 scripts/analyze.py --file /path/to/data.txt --format csv --sample-size 10
```

### Step 2: Handle Missing Dependencies (Environment Validation)

The script relies on `pandas` and `openpyxl`. If these libraries are missing from the current environment, the script will **fail fast** and output an error message indicating the missing libraries and the detected package manager (e.g., `uv`, `poetry`, `pip`).

**If you encounter this error:**
1. Do not prompt the user via an interactive script.
2. Ask the user for permission to install the missing libraries using the detected package manager.
3. Once approved, run the installation command (e.g., `uv add pandas openpyxl`).
4. Re-run the `analyze.py` script.

### Step 3: Read the Standardized Data Summary

If successful, the script will output a standardized summary containing:
- **File Metadata:** Path, inferred format, file size.
- **Data Shape:** Number of rows and columns.
- **Schema & Types:** Column names, their data types, and non-null counts.
- **Sample Data:** The first few rows of the dataset.

### Step 4: Answer the User's Query

Using the output from Step 3, formulate your answer to the user's original question. **Do not** attempt to modify the `analyze.py` script to answer natural language questions directly. Your job as the Agent is to perform the reasoning using the extracted data summary.

### Troubleshooting "Bad Data"
If a CSV file fails to load due to encoding or separator issues, the script attempts to use dynamic CSV sniffing. If it still fails, consider writing a custom script in the workspace or asking the user for the correct encoding/separator.
