---
name: hubspot-app-quality
description: Evaluate and improve HubSpot app quality against official marketplace listing and certification requirements. Use when reviewing an app before submission, preparing for certification, auditing an existing listing, or building a new app with quality goals in mind. Covers security, reliability, usability, documentation, and marketplace readiness.
---

# HubSpot App Quality

## Overview

Evaluate HubSpot apps against the official three-tier quality framework: minimum listing requirements, legal compliance, and certification standards. Use this skill to audit an app at any stage — pre-submission, post-listing, or pre-certification — and produce actionable remediation steps.

## When to Use

- Reviewing an app before marketplace submission
- Preparing an existing listed app for certification
- Auditing app quality after receiving Ecosystem Quality team feedback
- Building a new app and want to target certification from the start
- Comparing current app state against HubSpot's quality bar

## Non-Negotiable Rules

1. Always check current HubSpot docs before evaluating.
   - Run `mcp__HubSpotDev__search-docs` with queries like "app listing requirements", "certification requirements" to get the latest criteria.
   - Requirements change — never rely solely on cached knowledge.

2. Evaluate against all three tiers in order.
   - Minimum requirements first, then legal, then listing, then certification.
   - An app that fails minimum requirements should not be evaluated for certification.

3. Be specific about gaps.
   - Do not say "improve documentation." Say which doc is missing, what it should contain, and where it should link.

4. Separate blocking issues from improvements.
   - Blocking = will cause rejection.
   - Improvement = increases quality score but won't block submission.

## Quality Evaluation Workflow

### Step 1 — Gather App Context

Collect these inputs before evaluating:

- App ID and portal ID
- Distribution mode: private (static), private (OAuth), or marketplace (OAuth)
- Current state: not yet listed, listed, or seeking certification
- Feature surface: UI extensions, webhooks, workflow actions, API integrations, serverless functions
- Requested OAuth scopes

### Step 2 — Evaluate Minimum Requirements

Run through the minimum requirements checklist (see `references/minimum-requirements.md`):

- Single app ID with OAuth authorization
- 3+ active installs from unaffiliated accounts (last 30 days)
- Scope minimalism — only request what's used
- No restricted industry usage
- Functional independence — app works on its own

### Step 3 — Evaluate Legal Requirements

- Acceptable Use Policy compliance
- Branding and trademark guideline adherence
- Terms of Service and Privacy Policy present and accessible

### Step 4 — Evaluate Listing Requirements

Run through listing quality checklist (see `references/listing-requirements.md`):

- Complete marketplace listing info
- Live, functional URLs for docs, support, legal pages
- Clear setup documentation with step-by-step instructions
- Accurate pricing matching external website
- Data flow disclosure in "Shared data" table
- Support contact methods

### Step 5 — Evaluate Certification Readiness (if applicable)

Only if the app is listed and targeting certification. Evaluate across seven dimensions (see `references/certification-requirements.md`):

1. Security and privacy
2. Reliability and performance
3. Usability and accessibility
4. Value indicators
5. Documentation quality
6. Customer engagement
7. Good standing

### Step 6 — Produce Quality Report

Output a structured report with:

1. **Current tier**: Which tier the app currently meets
2. **Target tier**: What the user is aiming for
3. **Blocking issues**: Must fix before submission/certification
4. **Improvements**: Recommended but not blocking
5. **Action items**: Ordered by priority, with specific guidance

## Quick Reference: Key Thresholds

| Metric | Listing | Certification |
|---|---|---|
| Active installs | 3+ | 60+ |
| API success rate | — | 95%+ |
| Rate limit | — | 100 req/10s/account |
| Time listed | — | 6+ months |
| Certification validity | — | 2 years (rolling) |
| Review timeline | 10 business days | 10 business days initial |

## References

- For minimum listing requirements, read `references/minimum-requirements.md`.
- For listing quality criteria, read `references/listing-requirements.md`.
- For certification standards, read `references/certification-requirements.md`.
