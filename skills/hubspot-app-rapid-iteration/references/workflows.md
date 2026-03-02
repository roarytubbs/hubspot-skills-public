# Workflow Recipes

## Recipe 1: New Internal App Fast Path

Goal: ship a working internal feature quickly with low setup overhead.

1. Create a `2025.2` project with `private + static`.
2. Add exactly one feature (`card` or `settings` first).
3. Keep scopes minimal and explicit.
4. Validate project configuration.
5. Upload to a dev/test account.
6. Confirm install and feature rendering.

Definition of done:
- Build succeeds.
- Feature appears in expected HubSpot location.
- No secret/token values exposed in UI code or logs.

## Recipe 2: Add One Feature Iteratively

Goal: expand a stable app by one capability at a time.

1. Fetch docs for the specific feature first.
2. Add one feature component and required config.
3. Preserve existing UIDs unless intentionally creating a new component.
4. Validate and upload.
5. Inspect build output and fix only blocking/warning issues tied to that feature.

Definition of done:
- Feature behaves as specified.
- Existing features continue to work.
- No unrelated refactors bundled in the same iteration.

## Recipe 3: Debug Failed Build

Goal: restore green build quickly and safely.

1. Read recent build status.
2. Inspect detailed build logs for the failed build ID.
3. Classify root cause:
- schema/config error
- dependency or packaging error
- runtime/serverless misconfiguration
4. Apply minimal fix and re-validate.
5. Re-upload and confirm resolution.

Definition of done:
- Current build passes.
- Error root cause and fix are documented in summary output.

## Recipe 4: Multi-Environment with Profiles

Goal: prevent accidental cross-environment changes.

1. Create named config profiles (`qa`, `prod`).
2. Define all required variables in each profile.
3. Use profile-specific uploads/dev commands.
4. Fail fast if profile variables are missing.

Definition of done:
- Environment-specific values resolve correctly.
- Uploads run only with explicit profile selection.

## Recipe 5: 2025.1 to 2025.2 Migration Triage

Goal: choose migration path without breaking core behavior.

1. Check whether legacy serverless functions contain core logic.
2. If core logic is embedded and no equivalent migration path exists, defer migration and continue stable operation.
3. If serverless is mostly proxy behavior, migrate backend logic externally and shift UI extensions to `hubspot.fetch()`.
4. Re-check auth, scopes, and permitted URLs after migration changes.

Definition of done:
- Migration decision is explicit.
- Risks and follow-up tasks are documented.
