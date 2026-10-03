#!/usr/bin/env python3
"""
scan.py — Collect project discovery information for the acquire-codebase-knowledge skill.
Run from the project root directory.

Usage: python3 scan.py [OPTIONS]

Options:
  --output FILE   Write output to FILE instead of stdout
  --help          Show this message and exit

Exit codes:
  0  Success
  1  Usage error
"""

import sys
import argparse
from pathlib import Path
from dependencies.scanner import CodebaseScanner
from dependencies.constants import TREE_MAX_DEPTH


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Scan the current directory (project root) and output discovery information "
        "for the acquire-codebase-knowledge skill.",
        add_help=True,
    )
    parser.add_argument(
        "--output", type=str, help="Write output to FILE instead of stdout"
    )
    return parser.parse_args()


def print_section(title: str, content: list[str] | str, output_file=None) -> None:
    """Print a section with title and content."""
    lines = [f"\n=== {title} ==="]

    if isinstance(content, list):
        lines.extend(content if content else ["None found."])
    elif isinstance(content, str):
        lines.append(content)

    text = "\n".join(lines) + "\n"

    if output_file:
        output_file.write(text)
    else:
        print(text, end="")


def main():
    """Main entry point."""
    args = parse_args()

    output_file = None
    if args.output:
        output_dir = Path(args.output).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = open(args.output, "w", encoding="utf-8")
        print(f"Writing output to: {args.output}", file=sys.stderr)

    try:
        scanner = CodebaseScanner(Path.cwd())

        # Directory tree
        print_section(
            f"DIRECTORY TREE (max depth {TREE_MAX_DEPTH}, source files only)",
            scanner.get_directory_tree(),
            output_file,
        )

        # Stack detection
        manifests = scanner.find_manifest_files()
        if manifests:
            manifest_content = [""]
            for manifest in manifests:
                manifest_path = Path(manifest)
                manifest_content.append(f"--- {manifest} ---")
                if manifest == "bun.lockb":
                    manifest_content.append(
                        "[Binary lockfile — see package.json for dependency details.]"
                    )
                else:
                    manifest_content.append(scanner.read_file_preview(manifest_path))
            print_section(
                "STACK DETECTION (manifest files)", manifest_content, output_file
            )
        else:
            print_section(
                "STACK DETECTION (manifest files)",
                ["No recognized manifest files found in project root."],
                output_file,
            )

        # Entry points
        entries = scanner.find_entry_points()
        if entries:
            entry_content = [f"Found: {e}" for e in entries]
            print_section("ENTRY POINTS", entry_content, output_file)
        else:
            print_section(
                "ENTRY POINTS",
                [
                    "No common entry points found. Check 'main' or 'scripts.start' in manifest files above."
                ],
                output_file,
            )

        # Linting config
        lint = scanner.find_lint_config()
        if lint:
            lint_content = [f"Found: {n}" for n in lint]
            print_section("LINTING AND FORMATTING CONFIG", lint_content, output_file)
        else:
            print_section(
                "LINTING AND FORMATTING CONFIG",
                ["No linting or formatting config files found in project root."],
                output_file,
            )

        # Environment templates
        envs = scanner.find_env_templates()
        if envs:
            env_content = []
            for filename, filepath in envs:
                env_content.append(f"--- {filename} ---")
                env_content.append(scanner.read_file_preview(filepath))
            print_section("ENVIRONMENT VARIABLE TEMPLATES", env_content, output_file)
        else:
            print_section(
                "ENVIRONMENT VARIABLE TEMPLATES",
                [
                    "No .env.example or .env.template found. Identify required environment variables by searching the code and config for environment variable reads."
                ],
                output_file,
            )

        # Single pass for Code Metrics and TODOs
        metrics, todos = scanner.analyze_codebase()

        # TODOs
        if todos:
            print_section(
                "TODO / FIXME / HACK (production code only, test dirs excluded)",
                todos,
                output_file,
            )
        else:
            print_section(
                "TODO / FIXME / HACK (production code only, test dirs excluded)",
                ["None found."],
                output_file,
            )

        # Git info
        if scanner.is_git_repo():
            commits = scanner.get_git_commits()
            if commits:
                print_section("GIT RECENT COMMITS (last 20)", commits, output_file)
            else:
                print_section(
                    "GIT RECENT COMMITS (last 20)", ["No commits found."], output_file
                )

            churn = scanner.get_git_churn()
            if churn:
                print_section(
                    "HIGH-CHURN FILES (last 90 days, top 20)", churn, output_file
                )
            else:
                print_section(
                    "HIGH-CHURN FILES (last 90 days, top 20)",
                    ["None found."],
                    output_file,
                )
        else:
            print_section(
                "GIT RECENT COMMITS (last 20)",
                ["Not a git repository or no commits yet."],
                output_file,
            )
            print_section(
                "HIGH-CHURN FILES (last 90 days, top 20)",
                ["Not a git repository."],
                output_file,
            )

        # Monorepo detection
        monorepo = scanner.detect_monorepo()
        if monorepo:
            print_section("MONOREPO SIGNALS", monorepo, output_file)
        else:
            print_section(
                "MONOREPO SIGNALS", ["No monorepo signals detected."], output_file
            )

        # Code metrics
        metrics_output = [
            f"Total files scanned: {metrics['total_files']}",
            f"Total lines of code: {metrics['total_lines']}",
            "",
        ]
        if metrics["by_language"]:
            metrics_output.append("Files by language:")
            for lang, count in sorted(
                metrics["by_language"].items(), key=lambda x: x[1], reverse=True
            ):
                metrics_output.append(f"  {lang}: {count}")
        if metrics["largest_files"]:
            metrics_output.append("")
            metrics_output.append("Top 10 largest files:")
            metrics_output.extend(metrics["largest_files"])
        print_section("CODE METRICS", metrics_output, output_file)

        # CI/CD Detection
        ci_cd = scanner.detect_ci_cd_pipelines()
        if ci_cd:
            print_section("CI/CD PIPELINES", ci_cd, output_file)
        else:
            print_section(
                "CI/CD PIPELINES", ["No CI/CD pipelines detected."], output_file
            )

        # Container Detection
        containers = scanner.detect_containers()
        if containers:
            print_section("CONTAINERS & ORCHESTRATION", containers, output_file)
        else:
            print_section(
                "CONTAINERS & ORCHESTRATION",
                ["No containerization configs detected."],
                output_file,
            )

        # Security Configs
        security = scanner.detect_security_configs()
        if security:
            print_section("SECURITY & COMPLIANCE", security, output_file)
        else:
            print_section(
                "SECURITY & COMPLIANCE", ["No security configs detected."], output_file
            )

        # Performance Markers
        performance = scanner.detect_performance_markers()
        if performance:
            print_section("PERFORMANCE & TESTING", performance, output_file)
        else:
            print_section(
                "PERFORMANCE & TESTING",
                ["No performance testing configs detected."],
                output_file,
            )

        # Final message
        final_msg = "\n=== SCAN COMPLETE ===\n"
        if output_file:
            output_file.write(final_msg)
        else:
            print(final_msg, end="")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    finally:
        if output_file:
            output_file.close()


if __name__ == "__main__":
    sys.exit(main())
