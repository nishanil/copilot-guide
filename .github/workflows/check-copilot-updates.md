---
name: "Check Copilot Updates"
description: "Daily check for new GitHub Copilot features and updates. Opens a PR if the guide needs updating."
on:
  schedule: daily
  workflow_dispatch:
tools:
  bash: ["curl", "gh"]
  edit:
  web-fetch:
mcp-servers:
  tavily:
    command: npx
    args: ["-y", "@tavily/mcp-server"]
    env:
      TAVILY_API_KEY: "${{ secrets.TAVILY_API_KEY }}"
    allowed: ["search", "search_news"]
network:
  allowed:
    - defaults
    - "*.tavily.com"
safe-outputs:
  create-pull-request:
    labels: [automated-update, copilot-updates]
    title-prefix: "[bot] "
---

# Check for GitHub Copilot Updates

You are a documentation maintainer for a GitHub Copilot reference guide. Your job is to check for recent updates to GitHub Copilot and determine if the guide (`README.md`) needs updating.

## Step 1 — Gather recent Copilot updates

Use the Tavily `search_news` and `search` tools to find the latest GitHub Copilot announcements, changelog entries, and new features from the past 7 days. Focus on:

- The [GitHub Changelog for Copilot](https://github.blog/changelog/label/copilot/)
- The [GitHub Copilot CLI changelog](https://github.com/github/copilot-cli/blob/main/changelog.md)
- The [GitHub Blog — Copilot](https://github.blog/ai-and-ml/github-copilot/)
- New or updated official documentation at docs.github.com/en/copilot

Also use `web-fetch` to read those pages directly for the latest entries.

Look for:
- New features or capabilities (new slash commands, new agent modes, new integrations)
- Significant changes to existing features (renames, deprecations, GA announcements)
- New customization options (instructions, agents, skills, MCP, hooks, plugins)
- New platform features (memory, spaces, SDK updates)
- Notable community projects built on Copilot

## Step 2 — Compare against the current guide

Read the current `README.md` and compare the features documented there against what you found in Step 1.

Identify:
- **Missing features** — new capabilities not yet documented
- **Outdated information** — features that have been renamed, deprecated, or significantly changed
- **Missing links** — new official docs or blog posts not in the Further Reading section

If there is nothing new or everything is already up to date, stop here and report that no updates are needed.

## Step 3 — Update the guide

If updates are needed, edit `README.md` following these conventions:

- Keep all content inside `README.md` — do not split into separate pages
- Use the existing section structure: Customization → Agentic → Platform → Community → Best Practices → Quick Reference → Further Reading
- Every new feature section must include:
  - A one-line summary
  - A `> **When you need it:**` callout
  - A concrete code or config example (preferably inside a `<details>` block if long)
  - A two-column summary table at the end
- Use `<details>` / `<summary>` blocks to keep examples collapsible
- Use "RecipeShare" app examples to stay consistent with the existing guide
- Keep the Quick Reference table in sync when adding or removing features
- Keep the At a Glance ASCII diagram in sync
- Keep the Table of Contents in sync
- Add relevant docs/blog links to the Further Reading section
- Do not reorder top-level sections
- Do not remove or rename existing feature entries

## Step 4 — Open a pull request

Create a pull request with your changes. The PR title should summarize what was updated (e.g., "Add /plan command and model marketplace documentation"). The PR body should list:

1. What new features or changes were found
2. What sections of the guide were updated
3. Links to the source announcements
