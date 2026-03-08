# copilot-guide — Copilot Instructions

This repository is a comprehensive reference guide documenting every GitHub Copilot customization and agentic feature. Its single artifact is `README.md`.

## What this repo is

- **Content type:** Markdown documentation only — no source code, no build step, no tests
- **Audience:** Developers who want to understand and use Copilot's customization and agentic features
- **Goal:** Accurate, concise, and up-to-date descriptions of each feature with concrete examples

## Contribution conventions

- Keep all content inside `README.md` — do not split into separate pages
- Use the existing section structure: Customization → Agentic → Platform → Community → Best Practices → Quick Reference → Further Reading
- Every feature section must include:
  - A one-line summary
  - A `> **When you need it:**` callout explaining the motivation
  - A `📁 Location:` line (where applicable)
  - A concrete code or config example (preferably inside a `<details>` block if it is long)
  - A two-column summary table at the end of the section
- Use `<details markdown>` / `<summary>` blocks to keep examples collapsible and the page scannable (the `markdown` attribute is required for MkDocs rendering on GitHub Pages)
- Feature names in prose should match their heading exactly (e.g. "Custom Instructions", "Copilot Coding Agent")
- Link every external reference (docs, blog posts, repos) — no bare mentions without a URL

## Style rules

- Use `**bold**` for UI labels and key terms on first use in a section
- Use backticks for file paths, CLI commands, and code values
- Prefer concrete names over abstract ones: "RecipeShare" app examples are used throughout; keep new examples consistent with that project
- Do not add emojis to prose; the ASCII-art diagram at the top and the section header emojis are intentional — don't add more
- Keep the Quick Reference table in sync when adding or removing features

## What not to change

- Do not reorder the top-level sections
- Do not remove or rename existing feature entries
- Do not convert `<details markdown>` examples to inline code blocks — keeping them collapsible is intentional
- Do not modify these structural HTML wrappers — they control GitHub Pages rendering:
  - `<div align="center">` ... `</div>` (top header)
  - `<div class="ascii-glance" markdown>` ... `</div>` (At a Glance code block)
  - `<div class="svg-glance">` ... `</div>` (SVG placeholder for Pages)
  - `<div class="readme-toc" markdown>` ... `</div>` (Table of Contents)
  - `<p class="gh-pages-link">` ... `</p>` (Pages link, hidden on site)

## Automated updates

This guide is automatically checked for updates by an agentic workflow (`.github/workflows/check-copilot-updates.md`). It runs daily, checks official Copilot changelogs and community projects, and opens a PR if the guide needs updating. The GitHub Pages site at https://nishanil.github.io/copilot-guide/ is rebuilt automatically whenever `README.md` changes on `main`.
