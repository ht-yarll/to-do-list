import os
import subprocess
import json
import contextlib
from collections import Counter
from pathlib import Path

from .constants import (
    EXCLUDE_DIRS,
    MANIFESTS,
    ENTRY_CANDIDATES,
    LINT_FILES,
    ENV_TEMPLATES,
    SOURCE_EXTS,
    MONOREPO_FILES,
    MONOREPO_DIRS,
    CI_CD_CONFIGS,
    CONTAINER_FILES,
    SECURITY_CONFIGS,
    PERFORMANCE_MARKERS,
    LANG_MAP,
    TREE_MAX_DEPTH,
    TREE_LIMIT,
    TODO_LIMIT,
    MANIFEST_PREVIEW_LINES,
    RECENT_COMMITS_LIMIT,
    CHURN_LIMIT,
)
from .models import CodeMetrics

class CodebaseScanner:
    """Orchestrates codebase analysis and data collection."""
    
    def __init__(self, root_dir: Path | str):
        self.root_dir = Path(root_dir).resolve()

    def _should_exclude(self, path: Path) -> bool:
        """Check if a path should be excluded from scanning."""
        return any(part in EXCLUDE_DIRS for part in path.parts)

    def get_directory_tree(self, max_depth: int = TREE_MAX_DEPTH) -> list[str]:
        """Get directory tree up to max_depth."""
        files: list[str] = []

        def walk(path: Path, depth: int):
            if depth > max_depth or self._should_exclude(path):
                return
            try:
                for item in sorted(path.iterdir()):
                    if self._should_exclude(item):
                        continue
                    try:
                        rel_path = item.relative_to(self.root_dir)
                    except ValueError:
                        continue
                    files.append(str(rel_path))
                    if item.is_dir():
                        walk(item, depth + 1)
            except OSError:
                pass

        walk(self.root_dir, 0)
        return files[:TREE_LIMIT]

    def find_manifest_files(self) -> list[str]:
        """Find manifest files matching patterns."""
        found: set[str] = set()
        for pattern in MANIFESTS:
            if "*" in pattern:
                for path in self.root_dir.glob(pattern):
                    if path.is_file() and not self._should_exclude(path):
                        found.add(path.name)
            else:
                path = self.root_dir / pattern
                if path.is_file():
                    found.add(pattern)
        return sorted(list(found))

    def read_file_preview(self, filepath: Path, max_lines: int = MANIFEST_PREVIEW_LINES) -> str:
        """Read file with line limit safely."""
        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                lines = [next(f) for _ in range(max_lines + 1)]
                
            if not lines:
                return "None found."

            preview = "".join(lines[:max_lines])
            if len(lines) > max_lines:
                preview += f"\n[TRUNCATED] Showing first {max_lines} lines."
            return preview
        except StopIteration:
            return "".join(lines) if 'lines' in locals() else "None found."
        except OSError as e:
            return f"[Error reading file: {e}]"

    def find_entry_points(self) -> list[str]:
        """Find entry point candidates."""
        return [c for c in ENTRY_CANDIDATES if (self.root_dir / c).exists()]

    def find_lint_config(self) -> list[str]:
        """Find linting and formatting config files."""
        return [f for f in LINT_FILES if (self.root_dir / f).exists()]

    def find_env_templates(self) -> list[tuple[str, Path]]:
        """Find environment variable templates."""
        found = []
        for filename in ENV_TEMPLATES:
            path = self.root_dir / filename
            if path.exists():
                found.append((filename, path))
        return found

    def analyze_codebase(self) -> tuple[CodeMetrics, list[str]]:
        """Single-pass codebase analysis for metrics and TODOs."""
        metrics: CodeMetrics = {
            "total_files": 0,
            "by_extension": {},
            "by_language": {},
            "total_lines": 0,
            "largest_files": [],
        }
        todos: list[str] = []
        patterns = ["TODO", "FIXME", "HACK"]
        test_dirs = {"test", "tests", "__tests__", "spec", "__mocks__", "fixtures"}
        file_sizes: list[tuple[Path, int]] = []

        try:
            for root, dirs, files in os.walk(self.root_dir):
                # Filter directories in-place
                dirs[:] = [
                    d for d in dirs 
                    if d not in EXCLUDE_DIRS and d not in test_dirs
                ]

                for file in files:
                    filepath = Path(root) / file
                    ext = filepath.suffix.lstrip(".")

                    if not ext or ext in {"pyc", "o", "a", "so"}:
                        continue

                    try:
                        size = filepath.stat().st_size
                        rel_path = filepath.relative_to(self.root_dir)
                        file_sizes.append((rel_path, size))

                        metrics["total_files"] += 1
                        metrics["by_extension"][ext] = metrics["by_extension"].get(ext, 0) + 1
                        
                        lang = LANG_MAP.get(ext, "Other")
                        metrics["by_language"][lang] = metrics["by_language"].get(lang, 0) + 1

                        # Source files processing (lines and TODOs)
                        if ext in SOURCE_EXTS and size < 1_000_000:
                            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                                for line_num, line in enumerate(f, 1):
                                    metrics["total_lines"] += 1
                                    if len(todos) < TODO_LIMIT and any(p in line for p in patterns):
                                        todos.append(f"{rel_path}:{line_num}: {line.strip()}")
                    except OSError:
                        pass
                        
        except OSError:
            pass

        # Calculate top 10 largest
        file_sizes.sort(key=lambda x: x[1], reverse=True)
        metrics["largest_files"] = [f"{str(f)}: {s / 1024:.1f}KB" for f, s in file_sizes[:10]]

        return metrics, todos

    def detect_monorepo(self) -> list[str]:
        """Detect monorepo signals securely."""
        signals = []

        for filename in MONOREPO_FILES:
            if (self.root_dir / filename).exists():
                signals.append(f"Monorepo tool detected: {filename}")

        for dirname in MONOREPO_DIRS:
            if (self.root_dir / dirname).is_dir():
                signals.append(f"Sub-package directory found: {dirname}/")

        # Safely parse package.json
        pkg_json = self.root_dir / "package.json"
        if pkg_json.exists():
            with contextlib.suppress(OSError, json.JSONDecodeError):
                with open(pkg_json, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "workspaces" in data:
                        signals.append("package.json has 'workspaces' field (npm/yarn workspaces monorepo)")

        # Safely parse pyproject.toml (simple string check since tomli might not be installed)
        pyproject = self.root_dir / "pyproject.toml"
        if pyproject.exists():
            with contextlib.suppress(OSError):
                with open(pyproject, "r", encoding="utf-8") as f:
                    content = f.read()
                    suspects = ["[tool.uv.workspaces]", "workspaces = ", "packages = "]
                    if any(suspect in content for suspect in suspects):
                        signals.append("pyproject.toml has 'workspaces' field (monorepo)")

        return signals

    def is_git_repo(self) -> bool:
        """Check if current directory is a git repository."""
        try:
            subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                cwd=self.root_dir,
                timeout=2,
                check=True
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def get_git_commits(self) -> list[str]:
        """Get recent git commits."""
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "-n", str(RECENT_COMMITS_LIMIT)],
                capture_output=True,
                text=True,
                cwd=self.root_dir,
                timeout=5,
                check=True
            )
            return result.stdout.strip().split("\n") if result.stdout.strip() else []
        except (subprocess.SubprocessError, FileNotFoundError):
            return []

    def get_git_churn(self) -> list[str]:
        """Get high-churn files from last 90 days."""
        try:
            result = subprocess.run(
                ["git", "log", "--since=90 days ago", "--name-only", "--pretty=format:"],
                capture_output=True,
                text=True,
                cwd=self.root_dir,
                timeout=10,
                check=True
            )
            files = [f.strip() for f in result.stdout.split("\n") if f.strip()]
            counts = Counter(files)
            churn = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            return [f"{count:4d} {filename}" for filename, count in churn[:CHURN_LIMIT]]
        except (subprocess.SubprocessError, FileNotFoundError):
            return []

    def detect_ci_cd_pipelines(self) -> list[str]:
        """Detect CI/CD pipeline configurations."""
        pipelines = []
        for config_path, pipeline_name in CI_CD_CONFIGS.items():
            path = self.root_dir / config_path
            if path.is_file():
                pipelines.append(f"CI/CD: {pipeline_name}")
            elif path.is_dir():
                with contextlib.suppress(OSError):
                    if list(path.glob("*.yml")) or list(path.glob("*.yaml")):
                        pipelines.append(f"CI/CD: {pipeline_name}")
        return pipelines

    def detect_containers(self) -> list[str]:
        """Detect containerization and orchestration configs."""
        containers = []
        for config in CONTAINER_FILES:
            path = self.root_dir / config
            if path.is_file():
                if "Dockerfile" in config:
                    containers.append("Container: Docker found")
                elif "docker-compose" in config:
                    containers.append("Orchestration: Docker Compose found")
                elif config.endswith(".yaml") or config.endswith(".yml"):
                    containers.append(f"Container/Orchestration: {config}")
            elif path.is_dir():
                if config in ["k8s", "kubernetes"]:
                    containers.append("Orchestration: Kubernetes configs found")
                with contextlib.suppress(OSError):
                    if list(path.glob("*.yml")) or list(path.glob("*.yaml")):
                        containers.append(f"Container/Orchestration: {config}/ directory found")
        return containers

    def detect_security_configs(self) -> list[str]:
        """Detect security and compliance configurations."""
        security = []
        for config in SECURITY_CONFIGS:
            if (self.root_dir / config).exists():
                config_name = config.replace(".yml", "").replace(".yaml", "").lstrip(".")
                security.append(f"Security: {config_name}")
        return security

    def detect_performance_markers(self) -> list[str]:
        """Detect performance testing and profiling markers."""
        performance = []
        for marker in PERFORMANCE_MARKERS:
            path = self.root_dir / marker
            if path.exists():
                if path.is_dir():
                    performance.append(f"Performance: {marker}/ directory found")
                else:
                    performance.append(f"Performance: {marker} found")
        return performance
