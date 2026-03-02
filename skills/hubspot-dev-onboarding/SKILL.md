---
name: hubspot-dev-onboarding
description: Interview-style onboarding for HubSpot app development collaboration preferences. Use when a developer wants to define experience level, tech stack, and AI autonomy/control settings, then write or update a local preference.md file that other agents can read on each run.
---

# HubSpot Dev Onboarding

## Overview

Run a short developer interview and persist collaboration preferences to `preference.md` in the active workspace.

## Non-Negotiable Rules

1. Use HubSpot MCP first for HubSpot tasks.
- When `HubSpotDev` MCP is available, use its tools before manual `hs` CLI commands for HubSpot asset/project operations.
- Only fall back to manual CLI if the MCP tool cannot complete the task.

2. Ground technical guidance in HubSpot developer docs.
- Before giving technical implementation guidance, run:
  - `mcp__HubSpotDev__search-docs`
  - then `mcp__HubSpotDev__fetch-doc` on the selected result(s)
- Base recommendations on fetched official docs, not memory-only behavior.

## Workflow

1. Confirm output target.
- Default to `<workspace>/preference.md`.
- Use a different path only if the user asks.

2. Run onboarding interview.
- Ask concise questions for:
  - Developer experience: `beginner | intermediate | experienced | expert`
  - HubSpot experience: `none | beginner | intermediate | advanced`
  - Stack preset: `react-card | serverless-function | cms-module | card-plus-serverless | custom`
  - Tech stack: frameworks, language, testing tools
  - Project focus: CRM card, serverless, CMS module, workflow action, or mixed
  - Common workflows to optimize for (preset-driven use cases)
  - Autonomy level: `hands-off | pair-programming | human-in-the-loop`
  - Control profile: `autonomous | checkpointed | strict`

3. Encode control behavior.
- `hands-off`: execute end-to-end with minimal check-ins; stop before deploy/destructive changes.
- `pair-programming`: show plan first, implement in checkpoints, ask before high-impact actions.
- `human-in-the-loop`: require explicit approval before writes, risky commands, and non-trivial edits.
- Always enforce per-action gates for:
  - `hs project upload`
  - `hs project deploy`
  - `mcp__HubSpotDev__upload-project`
  - `mcp__HubSpotDev__deploy-project`

4. Generate `preference.md`.
- Use the script for deterministic formatting:
  - `python "<path-to-skill>/scripts/generate_preference.py" --interactive --output "<workspace>/preference.md"`
- Non-interactive mode is supported with flags (see script `--help`).

5. Ensure agent consumption.
- If `<workspace>/AGENTS.md` exists, ensure it instructs agents to read `preference.md` at the start of each run.
- If missing, create `<workspace>/AGENTS.md` with that instruction.

## Script

`scripts/generate_preference.py` writes a structured preference file that includes:
- machine-readable frontmatter
- autonomy behavior mapping
- stack presets and common use-case workflows
- per-action gate definitions
- execution guardrails
- testing and communication expectations

Quick start:
- `python "<path-to-skill>/scripts/generate_preference.py" --interactive --output "./preference.md"`
- `python "<path-to-skill>/scripts/generate_preference.py" --developer-experience experienced --hubspot-experience intermediate --tech-stack "TypeScript, React, HubSpot UI Extensions" --project-focus "CRM card + serverless function" --autonomy-level pair-programming --control-profile checkpointed --output "./preference.md"`

## References

- For common CRM card presets and fast-build workflow ideas, read:
  - `references/app-card-use-cases.md`
