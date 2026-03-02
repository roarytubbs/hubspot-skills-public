# Release Checklist

## Pre-Release Technical Gates

1. Confirm auth and distribution mode match target release.
- `private + static` for single-account internal installs.
- `private + oauth` for allowlisted multi-account installs.
- `marketplace + oauth` for public distribution.

2. Confirm scopes are least-privilege.
- Remove unused required scopes.
- Move context-specific scopes to optional/conditional where appropriate.

3. Confirm environment and profile correctness.
- Ensure all profile variables resolve.
- Avoid uploading without explicit profile when profiles are configured.

4. Confirm UI extension data-fetch safety.
- Keep external endpoints in `permittedUrls.fetch`.
- Enforce backend signature validation.
- Avoid storing secrets in client code.

5. Confirm rate-limit resilience.
- Add retry/backoff for transient errors.
- Add throttling and caching for high-volume flows.

## Build and Deployment Gates

1. Run validation/lint checks.
2. Upload and verify successful build.
3. Review build warnings, not only failures.
4. If auto-deploy is disabled, perform controlled deploy after successful build verification.

## Observability Gates

1. Confirm API and extension logs are available for the target account.
2. Verify no sensitive fields are logged.
3. Verify error handling returns actionable diagnostics without leaking secrets.

## Marketplace Readiness Gates

1. Confirm OAuth-only install flow for public listing path.
2. Confirm verified domain for trust and install UX.
3. Confirm installation and reconnect flows work for new accounts.
4. Confirm setup docs and support links are current.
5. Confirm listing/certification constraints are satisfied for current submission stage.

## Final Promotion Gate

Require explicit user approval before:
- production upload
- production deploy
- auth/distribution changes that alter install behavior
