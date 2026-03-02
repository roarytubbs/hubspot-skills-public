---
name: hubspot-app-rapid-iteration
description: Rapid workflow for building HubSpot apps iteratively with the HubSpot MCP server and CLI on developer platform 2025.2. Use when creating new HubSpot projects, adding app features (cards, settings, webhooks, workflow actions), validating and uploading builds, debugging build or serverless logs, setting up config profiles, deciding auth or distribution mode, or planning 2025.1 to 2025.2 migration constraints.
---

# HubSpot App Rapid Iteration

## Overview

Build HubSpot app features quickly by enforcing a docs-first, small-slice iteration loop.
Use HubSpot MCP tools first, then fall back to CLI only when needed.

## Non-Negotiable Rules

1. Use official HubSpot docs before implementation.
- Run `mcp__HubSpotDev__search-docs`, then `mcp__HubSpotDev__fetch-doc` on selected pages before planning or coding technical changes.

2. Prefer HubSpot MCP project tools over manual CLI for HubSpot-specific operations.
- Use manual `hs` commands only when MCP tools cannot complete the task.

3. Keep each iteration to one feature slice.
- Add one feature, validate, upload, inspect logs, patch, then move to the next slice.

4. Gate production-impacting actions.
- Require explicit user confirmation before production uploads or deploys.

5. Enforce secure defaults.
- Keep secrets off the client.
- Validate request signatures for external backends called via `hubspot.fetch()`.
- Apply least-privilege scopes.

## Workflow Selection

Choose app mode early:

- `private + static`: fastest path for single-account/internal builds.
- `private + oauth`: allowlisted multi-account installs.
- `marketplace + oauth`: public distribution path and listing readiness.

Choose release track early:

- `dev`: local and test-account iteration.
- `qa`: staging or pre-prod validation.
- `prod`: explicit user-approved promotion only.

## Fast Iteration Loop

1. Capture constraints.
- Confirm feature, auth/distribution mode, target account/profile, and done criteria.

2. Retrieve authoritative docs.
- Search and fetch docs specific to the feature before implementation.

3. Scaffold or extend project.
- Create project or add exactly one new feature component.

4. Implement the smallest useful change.
- Keep UIDs stable.
- Keep config explicit.

5. Validate before upload.
- Run project validation/lint where available.

6. Upload to non-prod profile.
- Use profile-bound uploads/dev sessions when profiles are present.

7. Inspect build and function logs.
- Read recent build status first.
- Pull detailed logs for failed or warning builds.
- Pull serverless logs when endpoint/app functions are involved.

8. Patch once and re-verify.
- Apply minimal fixes and re-run validation/upload.

9. Report concise outcomes.
- Summarize changed files, commands/actions, verification status, and remaining risks.

## Pre-Upload Checks

Check these before each upload:

- Confirm `platformVersion` target (prefer current stable unless migration constraints apply).
- Confirm `app-hsmeta.json` has intentional `distribution`, `auth.type`, and scoped permissions.
- Confirm `permittedUrls.fetch` includes all external endpoints used by UI extensions.
- Confirm profile variables are complete when profiles exist.
- Confirm no client-side secrets or sensitive token leakage in logs.

## Serverless and Migration Guardrails

- Treat 2025.1 and 2025.2 behavior differences as first-order constraints.
- If migrating private apps with serverless core logic from 2025.1, avoid forced migration until an equivalent path exists.
- If serverless behavior is mostly proxy logic, move core backend logic to external hosting and call via `hubspot.fetch()` with signature validation.

## References

Use these references to keep this file lean:

- For concrete feature-by-feature loops, read `references/workflows.md`.
- For release and marketplace gates, read `references/release-checklist.md`.
