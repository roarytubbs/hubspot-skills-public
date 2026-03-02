# HubSpot Skills (Public)

Reusable Codex/agent skills for HubSpot app development workflows.

## Included Skills

- `hubspot-app-rapid-iteration`: docs-first, one-slice-at-a-time workflow for building and shipping HubSpot app features.
- `hubspot-dev-onboarding`: interview-driven onboarding flow that generates a `preference.md` for collaboration style and guardrails.

## Repository Layout

```text
skills/
  hubspot-app-rapid-iteration/
  hubspot-dev-onboarding/
```

Each skill folder includes a `SKILL.md` plus any supporting `references/`, `scripts/`, or `agents/` assets.

## Usage

1. Copy one or both skill folders into your local Codex skills directory.
2. Reference them by name in prompts (for example, `$hubspot-app-rapid-iteration`).
3. Follow each skill's `SKILL.md` workflow and constraints.

## Notes

- This repo is curated for public sharing and excludes local machine artifacts.
- The workflows assume access to HubSpot developer tooling (MCP and/or CLI).
