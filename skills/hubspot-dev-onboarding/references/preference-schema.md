# preference.md schema

Use this structure when creating or updating `preference.md`:

1. YAML frontmatter
- `preferences_version` (number)
- `updated_at_utc` (ISO-8601 timestamp)
- `developer_experience` (`beginner | intermediate | experienced | expert`)
- `hubspot_experience` (`none | beginner | intermediate | advanced`)
- `stack_preset` (`react-card | serverless-function | cms-module | card-plus-serverless | custom`)
- `autonomy_level` (`hands-off | pair-programming | human-in-the-loop`)
- `control_profile` (`autonomous | checkpointed | strict`)
- `planning_style` (`terse | standard | detailed`)
- `testing_rigor` (`smoke | standard | strict`)

2. Markdown body sections
- `# Developer Preferences`
- `## Profile`
- `## Common Use-Case Workflows`
- `## Autonomy`
- `## Control`
- `## Per-Action Gates`
- `## Workflow Preferences`
- `## Gate Rules`

3. Required semantics
- Autonomy and control settings must be explicit and non-ambiguous.
- Per-action gate entries must explicitly include upload/deploy actions.
- For HubSpot development guidance, include MCP docs workflow requirement:
  `search-docs` then `fetch-doc`.
- Gate rules must always require human confirmation for deploy/destructive actions.
- Keep language concise so other agents can parse quickly.
