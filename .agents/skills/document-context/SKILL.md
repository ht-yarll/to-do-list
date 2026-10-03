---
name: document-context
description: Create and maintain project knowledge documents using the Open Knowledge Format (OKF) conventions.
---

# Document Context Skill

Use this skill when the user asks to capture, update, or organize project knowledge for future agent sessions.

This skill maintains a lightweight project knowledge base in `docs/knowledge` using the Open Knowledge Format (OKF) pattern: markdown files with YAML frontmatter, readable by humans and parseable by agents.

## Source Material

- Use `OKF-TEMPLATE.md` as the starting template for new knowledge documents.
- Align with the OKF v0.1 conventions from the official Google Cloud / GoogleCloudPlatform references:
  - https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/
  - https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md

## Output Location

- Save knowledge documents under `docs/knowledge`.
- Create `docs/knowledge` if it does not exist.
- Use lowercase, hyphenated filenames that describe the concept, decision, or session context, for example `dataset-extractor-context.md`.
- Treat each non-reserved markdown file as one OKF concept document.

## OKF Requirements

Every knowledge document must:

- Be a UTF-8 markdown file.
- Start with YAML frontmatter delimited by `---`.
- Include a non-empty `type` field in frontmatter.
- Prefer these frontmatter fields when applicable: `title`, `description`, `resource`, `tags`, and `timestamp`.
- Use standard markdown links for references to source files, ADRs, docs, issues, or external references.

## Content Guidance

Capture knowledge that will help a future agent or maintainer understand the project without rediscovering context. Good candidates include:

- Session context and user intent.
- Domain terminology and canonical names.
- Architectural decisions and guardrails.
- Known issues, constraints, tradeoffs, and rejected approaches.
- Source-code landmarks and ownership boundaries.
- References to related ADRs, docs, tests, or source files.

Prefer concise, factual notes over broad summaries. Include concrete examples when they prevent ambiguity.

## Tags

- Keep tags short, lowercase, and hyphenated.
- Reuse existing tags whenever possible.
- Maintain `docs/knowledge/tags.md` as a local tag reference when adding or changing tags.
- The tag reference is a project convention for consistency; it is not required by OKF itself.

## Workflow

1. Inspect existing `docs/knowledge` documents and `docs/knowledge/tags.md` before creating a new document.
2. Decide whether to update an existing concept document or create a new one.
3. Fill `OKF-TEMPLATE.md` with the current context, decisions, issues, consequences, and references.
4. Link related knowledge documents with normal markdown links.
5. Update `docs/knowledge/tags.md` if new tags are introduced or tag meanings change.
6. Keep changes focused on knowledge that was actually learned or decided in the current session.
