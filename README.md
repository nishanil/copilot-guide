<div align="center">

# 🤖 Understanding GitHub Copilot

**A comprehensive guide to every GitHub Copilot customization and agentic feature.**

What each does · When you'd use it · How they fit together

[![GitHub Copilot](https://img.shields.io/badge/GitHub-Copilot-blue?logo=github)](https://github.com/features/copilot)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/nishanil/copilot-guide/pulls)

</div>

## At a Glance

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  📄 CUSTOMIZATION — files that shape how Copilot behaves            │
│                                                                     │
│  Instructions        Always-on project context & conventions        │
│  Path-specific       Different rules for different parts            │
│  Prompt files        Reusable recipes for repeated tasks            │
│  Skills              Packaged expertise, auto-loaded on demand      │
│  MCP Servers         Connect to external tools, databases, APIs     │
│  Hooks               Automate lifecycle events (format, lint, etc.) │
│  Custom Agents       Named specialists with personas                │
│  Plugins             Bundle all of the above into one package       │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ⚡ AGENTIC — runtime capabilities for delegation & parallelism     │
│                                                                     │
│  Tasks               Spawn child agents in CLI (background/sync)    │
│  Subagents           Spawn child agents in VS Code (auto-parallel)  │
│  Coding Agent        Autonomous cloud agent — issues in, PRs out    │
│  Agentic Workflows   Automate repo tasks via GitHub Actions + AI    │
│  Mission Control     Dashboard to manage coding agents at scale     │
│  Agents Tab          Repo-level UI for agent tasks and tracking     │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🧠 PLATFORM — built-in intelligence & extensibility                │
│                                                                     │
│  Agentic Memory      Per-repo persistent memory across sessions     │
│  Copilot Spaces      Project-specific knowledge containers          │
│  Copilot SDK         Build your own agents as code (Node/Python/Go) │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🌐 COMMUNITY — open-source projects built on Copilot              │
│                                                                     │
│  Squad               Persistent AI team with memory & identity      │
│  awesome-copilot     Curated collection of patterns & resources     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Table of Contents

- [Customization Features](#customization-features)
  - [Custom Instructions](#custom-instructions)
  - [Path-Specific Instructions](#path-specific-instructions)
  - [Prompt Files](#prompt-files)
  - [Skills](#skills)
  - [MCP Servers](#mcp-servers)
  - [Hooks](#hooks)
  - [Custom Agents](#custom-agents)
  - [Plugins](#plugins)
- [Agentic Features](#agentic-features)
  - [Tasks (CLI)](#tasks-cli)
  - [Subagents (VS Code)](#subagents-vs-code)
  - [Copilot Coding Agent](#copilot-coding-agent)
  - [Agentic Workflows](#agentic-workflows)
  - [Mission Control](#mission-control)
  - [Agents Tab](#agents-tab)
- [Platform Features](#platform-features)
  - [Agentic Memory](#agentic-memory)
  - [Copilot Spaces](#copilot-spaces)
  - [Copilot SDK](#copilot-sdk)
- [Community Projects](#community-projects)
  - [Squad](#squad)
  - [awesome-copilot](#awesome-copilot)
- [Best Practices](#best-practices)
- [Quick Reference](#quick-reference)
- [Further Reading](#further-reading)

---

## Customization Features

> Files you add to your repo (or user config) that shape how Copilot behaves.

### Custom Instructions

Always-on project context. Copilot reads this on **every** interaction — chat, completions, code review.

> **When you need it:** Copilot doesn't know your stack, conventions, or preferences.

**📁 Location:** `.github/copilot-instructions.md`

```markdown
# Project: RecipeShare
- Framework: React 19 + Hono backend
- Styling: Tailwind CSS (no CSS modules)
- Language: TypeScript strict mode
- Use `const` over `let`, never `var`
- Tests: Vitest + React Testing Library
- Database: Drizzle ORM with PostgreSQL
```

**Effect:** Every Copilot response now respects these rules. No agent needed. No tools. Just context.

| | |
|---|---|
| **Scope** | Repository-wide, always-on |
| **Applies to** | Chat, completions, code review — everything |
| **Commit it** | Yes — the whole team benefits |

---

### Path-Specific Instructions

Override or refine rules for specific files or folders.

> **When you need it:** Your backend code needs different rules than your frontend. Test files shouldn't be as strict.

**📁 Location:** `.github/instructions/*.instructions.md`

```
.github/
├── copilot-instructions.md              # global
├── instructions/
│   ├── frontend.instructions.md         # applyTo: "src/client/**"
│   ├── backend.instructions.md          # applyTo: "src/server/**"
│   └── tests.instructions.md            # applyTo: "**/*.test.ts"
```

<details>
<summary>Example — <code>backend.instructions.md</code></summary>

```markdown
---
applyTo: "src/server/**"
---
- All API routes return JSON with { data, error } envelope
- Use Zod for request validation
- Every endpoint needs rate limiting middleware
```

</details>

**Effect:** Backend files get global + backend instructions. Frontend files get global + frontend instructions. They don't bleed into each other.

| | |
|---|---|
| **Scope** | Targeted via `applyTo` glob patterns |
| **Merging** | Path-specific merges with global (doesn't replace) |

---

### Prompt Files

Reusable task templates you invoke explicitly via `/` commands in chat.

> **When you need it:** You keep doing the same multi-step tasks — "create a new API endpoint" always involves route + validation + test + migration.

**📁 Location:** `.github/prompts/*.prompt.md`

<details>
<summary>Example — <code>new-endpoint.prompt.md</code></summary>

```markdown
Create a new Hono API endpoint:
1. Add route in src/server/routes/
2. Add Zod schema in src/server/schemas/
3. Add Drizzle migration in drizzle/migrations/
4. Add Vitest integration test
5. Update the OpenAPI spec
```

</details>

**Usage:** Type `/new-endpoint` in Copilot chat → it runs the full recipe.

| | |
|---|---|
| **Scope** | On-demand — invoked explicitly, never auto-loaded |
| **Difference from instructions** | Prompts are manual recipes; instructions are always-on context |

---

### Skills

Modular knowledge packages with a `SKILL.md` that Copilot loads on-demand when relevant.

> **When you need it:** Your deployment or migration process is complex and you want Copilot (including the coding agent) to know how to do it without you explaining every time.

**📁 Location:** `.github/skills/{skill-name}/SKILL.md`

<details>
<summary>Example — <code>drizzle-migrations/SKILL.md</code></summary>

```markdown
---
name: drizzle-migrations
description: Create, review, and apply Drizzle ORM database migrations.
---

# Drizzle Migration Skill

## When to use
When creating or modifying database tables.

## Steps
1. Run `npx drizzle-kit generate` to create migration
2. Review generated SQL in drizzle/migrations/
3. Run `npx drizzle-kit migrate` to apply
4. Update src/server/db/schema.ts with new types

## Gotchas
- Always check for existing data before DROP COLUMN
- Use `default()` for new non-nullable columns on existing tables
```

</details>

**Effect:** When Copilot detects a task related to migrations, it loads this skill automatically. Works across CLI, VS Code, and the coding agent.

| | |
|---|---|
| **Scope** | Auto-loaded when the task domain matches |
| **Difference from prompts** | Skills are auto-detected; prompts are manually invoked |

---

### MCP Servers

[Model Context Protocol](https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/extend-copilot-chat-with-mcp) servers connect Copilot to external tools — databases, APIs, cloud services, issue trackers — so agents can read and write to systems beyond your local files.

> **When you need it:** Your app needs to query PostgreSQL, check GitHub issues, or interact with cloud storage. Without MCP, you'd have to copy-paste data into chat.

**📁 Location:** `.vscode/mcp.json` (VS Code) or `~/.copilot/mcp-config.json` (CLI)

<details>
<summary>Example configuration</summary>

```jsonc
{
  "servers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": { "DATABASE_URL": "${DATABASE_URL}" }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./docs"]
    }
  }
}
```

</details>

| Without MCP | With MCP |
|---|---|
| "Here's my schema, can you write a query?" | Agent reads the schema directly from PostgreSQL |
| "The issue says..." (you paste it) | Agent reads the issue via GitHub MCP server |
| "Upload to cloud storage" (you do it manually) | Agent calls cloud storage API through an MCP server |

| | |
|---|---|
| **Scope** | Available to all agents in the session |
| **Discovery** | VS Code has a built-in MCP server gallery (search `@mcp` in Extensions) |
| **Security** | Servers run locally — your credentials stay on your machine |

---

### Hooks

Custom scripts that run automatically at specific lifecycle events — like pre-commit formatting, post-generation linting, or deployment triggers.

> **When you need it:** You want every code generation to be auto-formatted with Prettier, or every commit to run lint checks, without remembering to do it manually.

<details>
<summary>Example configuration</summary>

```jsonc
// .copilot/hooks.json
{
  "hooks": {
    "post-edit": {
      "command": "npx",
      "args": ["prettier", "--write", "${file}"]
    },
    "pre-commit": {
      "command": "npm",
      "args": ["run", "lint:fix"]
    }
  }
}
```

</details>

| | |
|---|---|
| **Scope** | Runs automatically at lifecycle events — no manual invocation |
| **Difference from skills** | Skills are knowledge Copilot reads; hooks are scripts Copilot runs |

---

### Custom Agents

A named agent with a persona, specific tools, and specialized behavior.

> **When you need it:** You want a dedicated "security reviewer" that always checks for auth issues, SQL injection, etc. — not just general Copilot.

**📁 Location:** `.github/agents/{name}.agent.md`

<details>
<summary>Example — <code>security-reviewer.agent.md</code></summary>

```markdown
---
name: Security Reviewer
description: Reviews code for security vulnerabilities
---
You are a security-focused code reviewer for RecipeShare.

Always check for:
- SQL injection (even with Drizzle ORM — check raw queries)
- XSS in React components (dangerouslySetInnerHTML)
- Auth bypass in API routes (missing middleware)
- File upload validation (type, size, path traversal)
- Rate limiting on auth endpoints
- Secrets in code or config

Output format: list findings as HIGH/MEDIUM/LOW with file:line references.
```

</details>

**Usage:** Select "Security Reviewer" from `/agents` in Copilot. It's a separate selectable agent, not always-on.

| | |
|---|---|
| **Scope** | Explicitly selected by the user — not auto-loaded |
| **Difference from instructions** | Agents are interactive personas; instructions are passive context |

---

### Plugins

Installable packages that bundle agents, skills, hooks, and MCP server configs into a single distributable unit. ([Docs](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating))

> **When you need it:** Your team has built a great set of agents, skills, hooks, and MCP configs. Instead of copying files between repos, you package them as a plugin that anyone can install.

<details>
<summary>Example structure</summary>

```
my-copilot-plugin/
├── plugin.json              # Manifest — what's in the package
├── agents/
│   └── security-reviewer.agent.md
├── skills/
│   └── drizzle-migrations/
│       └── SKILL.md
├── hooks/
│   └── post-edit-prettier.json
└── mcp/
    └── postgres-config.json
```

</details>

```bash
# Install from a GitHub repo
copilot plugin install github:myorg/recipeshare-toolkit

# List installed plugins
copilot plugin list
```

| | |
|---|---|
| **Location** | Installed into `~/.copilot/plugins/` or project-local |
| **Scope** | All bundled agents/skills/hooks/MCP become available |
| **Difference from skills** | A skill is one knowledge file; a plugin is a complete toolkit |

---

## Agentic Features

> Runtime capabilities — how Copilot delegates work, runs in parallel, and operates autonomously.

### Tasks (CLI)

The `task` tool lets an agent (or you in Copilot CLI) spawn a child agent in a **separate context window** to do focused work.

> **When you need it:** You want to run multiple checks in parallel, or delegate focused work without polluting the current context.

```
task(
  agent_type: "general-purpose",
  mode: "background",
  model: "claude-sonnet-4",
  description: "🧪 Security scan",
  prompt: "Check all API routes for missing auth middleware..."
)
```

#### Modes

| Mode | Behavior | Use when |
|------|----------|----------|
| `"sync"` | Blocks until the child agent finishes | You need the result before continuing |
| `"background"` | Runs in parallel, collect later via `read_agent` | Independent work, fan-out |

#### Agent types

| Type | What it does | Model tier |
|------|-------------|-------|
| `explore` | Read-only codebase search and Q&A | Fast/cheap |
| `task` | Run commands (tests, builds, lints) | Fast/cheap |
| `general-purpose` | Full capability — code, edit, reason | Standard |
| `code-review` | Review diffs, only surface real issues | Standard |

#### Parallelism

The key trick: **multiple `task` calls in a single response = true parallel execution.**

```
// All three fire at once:
task(mode: "background", prompt: "Check frontend for XSS...")
task(mode: "background", prompt: "Check backend for auth bypass...")
task(mode: "background", prompt: "Run npm audit...")
```

| | |
|---|---|
| **Where** | Copilot CLI only |
| **Context** | Each child gets its own isolated context window |
| **No file needed** | Runtime tool, not a config file |

---

### Subagents (VS Code)

The VS Code equivalent of the `task` tool. Your agent spawns child agents via `runSubagent` for parallel work.

> **When you need it:** You're in VS Code (not CLI) and want the same parallel delegation that `task` provides.

```
runSubagent(prompt: "Check all React components for XSS patterns...")
runSubagent(prompt: "Check all API routes for missing auth middleware...")
runSubagent(prompt: "Run npm audit and analyze results...")
```

#### Tasks vs Subagents

| | Tasks (`task` tool) | Subagents (`runSubagent`) |
|---|---|---|
| **Platform** | Copilot CLI | VS Code |
| **Parallelism** | `mode: "background"` + `read_agent` polling | Multiple calls in one turn auto-parallelize |
| **Model selection** | Per-spawn `model` param | Uses session model |
| **Agent types** | `explore`, `task`, `general-purpose`, `code-review` | One type — prompt determines behavior |
| **Result collection** | Manual via `read_agent` | Automatic — results return when done |

---

### Copilot Coding Agent

GitHub's autonomous agent that picks up issues, creates branches, and opens PRs — **without a chat session**. It runs on GitHub's cloud infrastructure, not your machine.

> **When you need it:** You have issues in your backlog that you want worked on asynchronously. You assign them; the coding agent works while you sleep and delivers a PR for review.

#### How it works

1. **Assign an issue to `@copilot`** — via label, Mission Control dashboard, or directly in the issue
2. **GitHub's cloud infrastructure** spins up an agent with your repo context
3. **The agent works autonomously** — reads the issue, creates a `copilot/*` branch, makes changes, opens a draft PR
4. **You review the PR** — treat it like any team member's work

#### Prerequisites

- **Copilot coding agent** enabled on the repo (Settings → Copilot → Coding agent)
- **`copilot-setup-steps.yml`** in `.github/` — defines the agent's environment
- **GitHub Actions** enabled

<details>
<summary>Example — <code>copilot-setup-steps.yml</code></summary>

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-node@v4
    with:
      node-version: '22'
  - run: npm ci
  - run: npm run build
```

</details>

> 💡 The coding agent reads your custom instructions and skills — so everything you've configured for interactive Copilot also applies to the autonomous agent.

| | |
|---|---|
| **Where** | GitHub cloud infrastructure |
| **Interaction** | Async only — no chat, results delivered as PRs |
| **Context** | Each agent runs in full isolation — separate branch, separate PR |
| **Cost** | Copilot premium requests |

---

### Mission Control

[Mission Control](https://github.blog/changelog/2025-10-28-a-mission-control-to-assign-steer-and-track-copilot-coding-agent-tasks/) is a centralized dashboard for managing multiple coding agents at scale.

> **When you need it:** You're running multiple coding agents across repos and want a single view to assign, monitor, and steer them.

- See all active coding agents across repos in one view
- Read real-time session logs and code change rationales
- Steer, pause, or restart agents mid-execution
- Assign new tasks to agents directly

Available on **GitHub.com**, **VS Code Insiders**, and **GitHub Mobile**.

#### Local vs Cloud agents

| | Tasks / Subagents | Coding Agent + Mission Control |
|---|---|---|
| **Runs on** | Your machine | GitHub cloud infrastructure |
| **Interaction** | Synchronous — in a chat session | Asynchronous — works while you sleep |
| **Result** | Agent output in terminal/editor | A pull request |
| **Memory** | Session-only | `copilot-instructions.md` + issue context |
| **Scale** | Limited by your machine | Multiple agents across repos |

---

### Agentic Workflows

Markdown-described automations that run inside **GitHub Actions** — agents triage issues, update docs, fix CI failures, and generate PRs, all triggered by repo events.

> **When you need it:** You want your repo to run on autopilot — issues get triaged, docs stay in sync with code, and CI failures get diagnosed automatically.

**How it works:**

1. **Describe the automation** in a markdown workflow file — what you want done on which trigger
2. **GitHub Actions invokes the coding agent** with your instructions and repo context
3. **The agent executes** — reading code, making changes, running tests
4. **Results appear as PRs** — fully reviewable, with diffs, commit history, and CI results

#### Examples of what you can automate

- Auto-triage and label new issues based on content
- Diagnose and suggest fixes for CI/CD failures
- Keep documentation in sync when code changes
- Generate routine dependency update PRs
- Improve test coverage on schedule

#### Key details

| | |
|---|---|
| **Where** | GitHub Actions + Coding Agent |
| **Trigger** | Repo events (push, issue created, schedule, etc.) |
| **Result** | Pull requests — always human-reviewed before merge |
| **Blog post** | [Automate repository tasks with GitHub Agentic Workflows](https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/) |

---

### Agents Tab

A repo-level tab on GitHub.com for launching, tracking, and reviewing agent tasks — the repo-scoped companion to Mission Control.

> **When you need it:** You want to see all agent activity for a specific repo in one place, launch new tasks, and review agent-generated PRs without leaving the repo.

- Launch agent tasks directly from the repo
- Track progress of active agents
- Review agent-generated pull requests
- See history of completed agent work

| | |
|---|---|
| **Where** | GitHub.com — new tab on each repo |
| **Scope** | Single repo (vs Mission Control which is cross-repo) |

---

## Platform Features

> Built-in intelligence and extensibility that power the entire Copilot ecosystem.

### Agentic Memory

Per-repo persistent memory — Copilot remembers context across sessions, automatically learning from your interactions and expiring stale information.

> **When you need it:** You're tired of re-explaining your architecture, conventions, or recent decisions every new session. You want Copilot to remember what it learned last time.

**How it works:**

- Copilot stores learnings from sessions as per-repo "memories"
- Memories are shared across Copilot features (chat, completions, agents, code review)
- Stale or outdated insights auto-expire for safety
- You can view and manage memories

| | |
|---|---|
| **Scope** | Per-repository, persistent across sessions |
| **Difference from instructions** | Instructions are manually authored; memory is auto-learned |
| **Difference from Squad's history.md** | Memory is platform-native and automatic; Squad's is file-based and git-committed |

---

### Copilot Spaces

Project-specific knowledge containers — persistent, shareable collections of context accessible in Codespaces, dev containers, and across Copilot features.

> **When you need it:** You want to package project knowledge (architecture docs, API specs, onboarding guides) into a container that Copilot always has access to, especially for onboarding new team members.

| | |
|---|---|
| **Scope** | Per-project, accessible across Copilot surfaces |
| **Use for** | Onboarding, architecture context, shared team knowledge |
| **Supports** | Role-based access, public sharing, templates |

---

### Copilot SDK

Programmatic access to Copilot's capabilities in **Node.js**, **Python**, **Go**, and **.NET**. Build your own agents as code — with execution loops, tool orchestration, multi-model routing, and context management.

> **When you need it:** You want agents as *code* rather than *prompts*. Or you need to integrate Copilot into custom automation, CI/CD pipelines, or your own developer tools.

```bash
# Install (Node.js example)
npm install @github/copilot-sdk
```

| | |
|---|---|
| **Status** | Technical preview |
| **Languages** | Node.js, Python, Go, .NET |
| **Repository** | [github.com/github/copilot-sdk](https://github.com/github/copilot-sdk) |
| **Difference from agents** | Agents are markdown prompts; SDK is programmatic code |

---

## Community Projects

> Open-source projects built on top of Copilot's features.

### Squad

A persistent team of AI agents with identity, memory, and parallel coordination — all through prompt engineering.

**Repository:** [github.com/bradygaster/squad](https://github.com/bradygaster/squad)

```bash
npx github:bradygaster/squad
```

<details>
<summary>What gets created</summary>

```
.ai-team/                          # Team state (committed to git)
├── team.md                        # Roster — who's on the team
├── decisions.md                   # Shared brain — team decisions
├── routing.md                     # Who handles what
├── agents/
│   ├── stark/
│   │   ├── charter.md            # Lead — identity, expertise
│   │   └── history.md            # What Stark knows about YOUR project
│   ├── parker/charter.md         # Frontend specialist
│   ├── banner/charter.md         # Backend specialist
│   └── romanoff/charter.md       # Tester
├── log/                           # Session history
└── orchestration-log/             # What was spawned and why

.github/agents/squad.agent.md     # The coordinator (~1,771 lines)
```

</details>

**How it works:** You say *"Team, build the login page"* → the coordinator spawns agents in parallel using the `task` tool → each agent works in its own context → decisions are merged via a drop-box pattern → knowledge persists in `history.md` across sessions.

| | Vanilla Custom Agent | Squad |
|---|---|---|
| **Memory** | Fresh every session | `history.md` per agent, `decisions.md` shared |
| **Identity** | Generic | Persistent themed names (MCU, Star Wars, etc.) |
| **Coordination** | Manual | Auto-routes based on `routing.md` |
| **Parallelism** | DIY | Built-in fan-out |
| **Git-native** | Just a markdown file | Full `.ai-team/` folder — clone = get the team |

---

### awesome-copilot

A curated collection of Copilot resources, customizations, and advanced patterns.

**Repository:** [github.com/github/awesome-copilot](https://github.com/github/awesome-copilot)

Includes custom instructions examples, agent patterns, orchestration strategies, MCP configs, community skills, and guides for maximizing agentic workflows. A great starting point for seeing how others use these features in practice.

---

## Best Practices

> Tips for writing effective instructions, prompts, skills, and agents.

### General Principles

- **Be specific, not vague.** "React 19 with Vite and Tailwind CSS" beats "a React app." Name exact frameworks, versions, and tools.
- **Show, don't just tell.** One concrete code example is worth more than a paragraph of description.
- **Set boundaries explicitly.** List files, directories, and configs the AI should *never* touch.
- **Front-load commands.** Put relevant CLI commands near the top — agents act on these first.
- **Only include what can't be inferred.** Don't duplicate what linters or CI already enforce.
- **Version control everything.** Check all customization files into your repo.

### Writing Instructions

- Keep under ~1,000 lines — beyond that, context dilution reduces effectiveness
- Use headings and bullet points, not prose
- Make rules actionable: ✅ `Never use any in TypeScript` — ❌ `Try to use good types`
- Use `applyTo:` globs to scope. Don't put backend rules in a file that applies to frontend

### Writing Prompts

- One prompt = one task. Don't combine unrelated steps
- Include expected inputs and outputs
- Use numbered steps for multi-step workflows
- Specify output format if it matters

### Writing Skills

- Each skill gets its own folder with a lowercased, hyphenated name
- Include YAML frontmatter with `name` and `description`
- Write step-by-step with gotchas and edge cases
- Bundle related scripts in the same folder
- Clearly specify "When to use" so Copilot loads it at the right time

### Writing Agents

Based on [lessons from 2,500+ repositories](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/):

- **Define a specialist, not a generalist.** "You are a security reviewer for a Node.js API" — not "You are a helpful assistant"
- **Cover:** commands/tooling, testing, project structure, code style, git workflow, boundaries
- **Include positive AND negative instructions.** What to do *and* what to never do
- **Show output examples.** Demonstrate what a good response looks like
- **Keep personas focused.** Don't mix frontend and backend concerns — make separate agents

### Authoring Resources

| Resource | Source |
|---|---|
| [How to write a great agents.md — Lessons from 2,500+ repos](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/) | GitHub Blog |
| [Using custom instructions to unlock the power of Copilot](https://docs.github.com/en/copilot/tutorials/use-custom-instructions) | GitHub Docs |
| [Creating agent skills](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-skills) | GitHub Docs |
| [Prompt files vs Instructions vs Agents](https://gist.github.com/burkeholland/435ab18c549ddbefde1846165e8b2e08) | Burke Holland |
| [Mastering GitHub Copilot Customisation](https://onlyutkarsh.com/posts/2026/github-copilot-customization/) | Utkarsh Shigihalli |
| [All About Copilot Custom Instructions](https://www.nathannellans.com/post/all-about-github-copilot-custom-instructions) | Nathan Nellans |

---

## Quick Reference

| Feature | What | Location | When to use |
|---------|------|----------|-------------|
| **Instructions** | Always-on project context | `.github/copilot-instructions.md` | When Copilot doesn't know your stack |
| **Path-specific** | Per-folder/file overrides | `.github/instructions/*.instructions.md` | When parts need different rules |
| **Prompts** | Reusable task recipes | `.github/prompts/*.prompt.md` | When you repeat multi-step tasks |
| **Skills** | Packaged domain knowledge | `.github/skills/{name}/SKILL.md` | When procedures are complex |
| **MCP Servers** | External tool connections | `.vscode/mcp.json` | When agents need databases/APIs |
| **Hooks** | Lifecycle automation | `.copilot/hooks.json` | When you want auto-formatting/linting |
| **Agents** | Named specialist personas | `.github/agents/{name}.agent.md` | When you need dedicated workflow owners |
| **Plugins** | Bundled agent toolkits | `plugin.json` manifest | When sharing agent setups across repos |
| **Tasks** | CLI child agent spawning | *(runtime tool)* | When you need parallelism in CLI |
| **Subagents** | VS Code child agents | *(runtime pattern)* | When you need parallelism in VS Code |
| **Coding Agent** | Autonomous cloud agent | GitHub infrastructure | When you want async issue automation |
| **Agentic Workflows** | AI + GitHub Actions automation | GitHub Actions | When you want automated repo maintenance |
| **Mission Control** | Multi-agent dashboard | GitHub.com / VS Code | When managing agents at scale |
| **Agents Tab** | Repo-level agent UI | GitHub.com | When tracking agent work per repo |
| **Agentic Memory** | Persistent per-repo memory | Built-in | When you want Copilot to remember across sessions |
| **Copilot Spaces** | Project knowledge containers | GitHub.com | When packaging shared context for teams |
| **Copilot SDK** | Programmatic agent building | npm / pip / go | When you need agents as code, not prompts |

### File Structure

```
.github/
├── copilot-instructions.md              # Global instructions
├── copilot-setup-steps.yml              # Coding agent environment
├── instructions/
│   ├── frontend.instructions.md         # Path-specific
│   ├── backend.instructions.md
│   └── tests.instructions.md
├── prompts/
│   ├── new-endpoint.prompt.md           # Reusable recipes
│   └── new-component.prompt.md
├── skills/
│   ├── drizzle-migrations/              # Domain knowledge
│   │   └── SKILL.md
│   └── recipe-image-upload/
│       └── SKILL.md
├── agents/
│   └── security-reviewer.agent.md       # Custom agents
└── workflows/
    └── ...

.vscode/
└── mcp.json                             # MCP server config

.copilot/
└── hooks.json                           # Lifecycle hooks
```

---

## Further Reading

**Official Documentation**
- [Custom Instructions](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions) · [Custom Agents](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli) · [Plugins](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating) · [Comparing CLI Features](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/comparing-cli-features) · [MCP Servers](https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/extend-copilot-chat-with-mcp) · [Coding Agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent)

**VS Code**
- [MCP Servers](https://github.com/microsoft/vscode-docs/blob/main/docs/copilot/customization/mcp-servers.md) · [Subagents](https://code.visualstudio.com/docs/copilot/agents/subagents) · [Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills) · [Prompt Files](https://code.visualstudio.com/docs/copilot/customization/prompt-files)

**Blog Posts & Guides**
- [Maximize Agentic Capabilities](https://github.blog/ai-and-ml/github-copilot/how-to-maximize-github-copilots-agentic-capabilities/) · [Mission Control](https://github.blog/changelog/2025-10-28-a-mission-control-to-assign-steer-and-track-copilot-coding-agent-tasks/) · [Agents vs Skills vs Instructions](https://github.com/orgs/community/discussions/183962) · [Agentic Workflows](https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/)

**Platform**
- [Copilot SDK](https://github.com/github/copilot-sdk) · [Copilot Spaces](https://github.blog/changelog/2025-05-19-copilot-spaces-public-preview/)

**Community**
- [awesome-copilot](https://github.com/github/awesome-copilot) · [Squad](https://github.com/bradygaster/squad)

---

<div align="center">

**Found this useful?** Give it a ⭐ and share it with your team.

**Something missing?** [Open an issue](https://github.com/nishanil/copilot-guide/issues) or submit a PR.

</div>
