# App Card Use Cases

Use these presets when onboarding a developer who wants to build CRM app cards quickly.

## High-Value Starter Use Cases

1. Event intake card
- Goal: create/log events directly from contact or company records.
- Typical shape: card UI form + serverless POST endpoint + validation + success toast.

2. Lead qualification card
- Goal: score leads and suggest next best actions.
- Typical shape: card summary + fetch scoring data + action buttons.

3. Renewal health card
- Goal: show account renewal risk and owner tasks.
- Typical shape: health score, risk factors, owner checklist, linked playbook.

4. Support escalation card
- Goal: escalate high-severity issues quickly with full context.
- Typical shape: ticket metadata + SLA state + escalation action endpoint.

5. Meeting follow-up card
- Goal: turn meeting notes into tasks and timeline updates.
- Typical shape: summary box + generated tasks + quick-create actions.

## Recommended "Fast Build" Sequence

1. Scope
- Choose one record type and one primary action.

2. UI card
- Build smallest useful card first (inputs + one action + clear success/failure states).

3. Backend
- Add a serverless function for validation and side effects.

4. Permissions and URLs
- Ensure all external URLs are in app `permittedUrls.fetch`.

5. Test loop
- Run local dev flow, test errors, then validate project config before upload/deploy.
