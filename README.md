# HubSpot Skills (Public)

Reusable agent skills for HubSpot app development workflows.

## Skills Catalog

### `hubspot-app-rapid-iteration`

Overview: A docs-first, small-slice delivery workflow for building HubSpot apps quickly and safely. It emphasizes one-feature-at-a-time implementation, validation before upload, build/log debugging loops, environment/profile discipline, and explicit gating before production-impacting actions.

### `hubspot-dev-onboarding`

Overview: An interview-style onboarding workflow that captures developer collaboration preferences and writes them to `preference.md`. It standardizes autonomy/control settings, per-action safety gates (especially upload/deploy), preferred stack/workflows, and expectations other agents should follow in the workspace.

## Repository Layout

```text
skills/
  hubspot-app-rapid-iteration/
  hubspot-dev-onboarding/
```

Each skill folder includes a `SKILL.md` plus any supporting `references/`, `scripts/`, or `agents/` assets.

## Usage

Before using these skills, install HubSpot developer tooling (CLI + local MCP server), then add the skills to your agent environment:

1. Install the HubSpot CLI: [HubSpot CLI commands (v7)](https://developers.hubspot.com/docs/guides/cms/tools/hubspot-cli/cli-v7)
2. Install and configure the HubSpot Developer MCP server: [Creating apps and CMS content with HubSpot's developer MCP server](https://developers.hubspot.com/docs/developer-tooling/local-development/mcp-server)
3. Install command: `npm install -g @hubspot/cli@latest`
4. MCP setup command: `hs mcp setup`

## Add Skills

1. Copy one or both skill folders into your agent runtime's skills directory.
2. Reference them by name in prompts (for example, `$hubspot-app-rapid-iteration`).
3. Follow each skill's `SKILL.md` workflow and constraints.

## Notes

- This repo is curated for public sharing and excludes local machine artifacts.
- The workflows assume access to HubSpot developer tooling (MCP and/or CLI).
