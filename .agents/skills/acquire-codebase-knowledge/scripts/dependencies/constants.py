"""
Constants and configurations for the CodebaseScanner.
"""

TREE_LIMIT = 200
TREE_MAX_DEPTH = 3
TODO_LIMIT = 60
MANIFEST_PREVIEW_LINES = 80
RECENT_COMMITS_LIMIT = 20
CHURN_LIMIT = 20

EXCLUDE_DIRS = {
    "node_modules",
    ".git",
    "dist",
    "build",
    "out",
    ".next",
    ".nuxt",
    "__pycache__",
    ".venv",
    "venv",
    ".tox",
    "target",
    "vendor",
    "coverage",
    ".nyc_output",
    "generated",
    ".cache",
    ".turbo",
    ".yarn",
    ".pnp",
    "bin",
    "obj",
}

MANIFESTS = [
    # JavaScript/Node.js
    "package.json",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "bun.lockb",
    "deno.json",
    "deno.jsonc",
    # Python
    "requirements.txt",
    "Pipfile",
    "Pipfile.lock",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "poetry.lock",
    "pdm.lock",
    "uv.lock",
    # Go
    "go.mod",
    "go.sum",
    # Rust
    "Cargo.toml",
    "Cargo.lock",
    # Java/Kotlin
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "settings.gradle.kts",
    "gradle.properties",
    # PHP/Composer
    "composer.json",
    "composer.lock",
    # Ruby
    "Gemfile",
    "Gemfile.lock",
    "*.gemspec",
    # Elixir
    "mix.exs",
    "mix.lock",
    # Dart/Flutter
    "pubspec.yaml",
    "pubspec.lock",
    # .NET/C#
    "*.csproj",
    "*.sln",
    "*.slnx",
    "global.json",
    "packages.config",
    # Swift
    "Package.swift",
    "Package.resolved",
    # Scala
    "build.sbt",
    "scala-cli.yml",
    # Haskell
    "*.cabal",
    "stack.yaml",
    "cabal.project",
    "cabal.project.local",
    # OCaml
    "dune-project",
    "opam",
    "opam.lock",
    # Nim
    "*.nimble",
    "nim.cfg",
    # Crystal
    "shard.yml",
    "shard.lock",
    # R
    "DESCRIPTION",
    "renv.lock",
    # Julia
    "Project.toml",
    "Manifest.toml",
    # Build systems
    "CMakeLists.txt",
    "Makefile",
    "GNUmakefile",
    "SConstruct",
    "build.xml",
    "BUILD",
    "BUILD.bazel",
    "WORKSPACE",
    "bazel.lock",
    "justfile",
    ".justfile",
    "Taskfile.yml",
    "tox.ini",
    "Vagrantfile",
]

ENTRY_CANDIDATES = [
    # JavaScript/Node.js/TypeScript
    "src/index.ts",
    "src/index.js",
    "src/index.mjs",
    "src/main.ts",
    "src/main.js",
    "src/main.py",
    "src/app.ts",
    "src/app.js",
    "src/server.ts",
    "src/server.js",
    "index.ts",
    "index.js",
    "app.ts",
    "app.js",
    "lib/index.ts",
    "lib/index.js",
    # Go
    "main.go",
    "cmd/main.go",
    "cmd/*/main.go",
    # Python
    "main.py",
    "app.py",
    "server.py",
    "run.py",
    "cli.py",
    "src/main.py",
    "src/__main__.py",
    # .NET/C#
    "Program.cs",
    "src/Program.cs",
    "Main.cs",
    # Java
    "Main.java",
    "Application.java",
    "App.java",
    "src/main/java/Main.java",
    # Kotlin
    "Main.kt",
    "Application.kt",
    "App.kt",
    # Rust
    "src/main.rs",
    "src/lib.rs",
    # Swift
    "main.swift",
    "Package.swift",
    "Sources/main.swift",
    # Ruby
    "app.rb",
    "main.rb",
    "lib/app.rb",
    # PHP
    "index.php",
    "app.php",
    "public/index.php",
    # Go
    "cmd/*/main.go",
    # Scala
    "src/main/scala/Main.scala",
    # Haskell
    "Main.hs",
    "app/Main.hs",
    # Clojure
    "src/core.clj",
    "-main.clj",
    # Elixir
    "lib/application.ex",
    "mix.exs",
]

LINT_FILES = [
    ".eslintrc",
    ".eslintrc.json",
    ".eslintrc.js",
    ".eslintrc.cjs",
    ".eslintrc.yml",
    ".eslintrc.yaml",
    "eslint.config.js",
    "eslint.config.mjs",
    "eslint.config.cjs",
    ".prettierrc",
    ".prettierrc.json",
    ".prettierrc.js",
    ".prettierrc.yml",
    "prettier.config.js",
    "prettier.config.mjs",
    ".editorconfig",
    "tsconfig.json",
    "tsconfig.base.json",
    "tsconfig.build.json",
    ".golangci.yml",
    ".golangci.yaml",
    "setup.cfg",
    ".flake8",
    ".pylintrc",
    "mypy.ini",
    ".rubocop.yml",
    "phpcs.xml",
    "phpstan.neon",
    "biome.json",
    "biome.jsonc",
]

ENV_TEMPLATES = [
    ".env.example",
    ".env.template",
    ".env.sample",
    ".env.defaults",
    ".env.local.example",
]

SOURCE_EXTS = {
    "ts", "tsx", "js", "jsx", "mjs", "cjs", "py", "go", "java", "kt", "rb", "php",
    "rs", "cs", "cpp", "c", "h", "ex", "exs", "swift", "scala", "clj", "cljs", "lua",
    "vim", "hs", "ml", "nim", "cr", "r", "jl", "groovy", "gradle", "xml", "json"
}

MONOREPO_FILES = [
    "pnpm-workspace.yaml",
    "lerna.json",
    "nx.json",
    "rush.json",
    "turbo.json",
    "moon.yml",
]

MONOREPO_DIRS = ["packages", "apps", "libs", "services", "modules"]

CI_CD_CONFIGS = {
    ".github/workflows": "GitHub Actions",
    ".gitlab-ci.yml": "GitLab CI",
    "Jenkinsfile": "Jenkins",
    ".circleci/config.yml": "CircleCI",
    ".travis.yml": "Travis CI",
    "azure-pipelines.yml": "Azure Pipelines",
    "appveyor.yml": "AppVeyor",
    ".drone.yml": "Drone CI",
    ".woodpecker.yml": "Woodpecker CI",
    "bitbucket-pipelines.yml": "Bitbucket Pipelines",
}

CONTAINER_FILES = [
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    ".dockerignore",
    "Dockerfile.*",
    "k8s",
    "kustomization.yaml",
    "Chart.yaml",
    "Vagrantfile",
    "podman-compose.yml",
]

SECURITY_CONFIGS = [
    ".snyk",
    "security.txt",
    "SECURITY.md",
    ".dependabot.yml",
    ".whitesource",
    "sbom.json",
    "sbom.spdx",
    ".bandit.yaml",
]

PERFORMANCE_MARKERS = [
    "benchmark",
    "bench",
    "perf.data",
    ".prof",
    "k6.js",
    "locustfile.py",
    "jmeter.jmx",
]

LANG_MAP = {
    "ts": "TypeScript",
    "tsx": "TypeScript/React",
    "js": "JavaScript",
    "jsx": "JavaScript/React",
    "py": "Python",
    "go": "Go",
    "java": "Java",
    "kt": "Kotlin",
    "rs": "Rust",
    "cs": "C#",
    "rb": "Ruby",
    "php": "PHP",
    "swift": "Swift",
    "scala": "Scala",
    "ex": "Elixir",
    "cpp": "C++",
    "c": "C",
    "h": "C Header",
    "clj": "Clojure",
    "lua": "Lua",
    "hs": "Haskell",
}
