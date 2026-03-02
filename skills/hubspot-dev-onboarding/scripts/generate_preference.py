#!/usr/bin/env python3
"""Generate a local preference.md for agent collaboration behavior."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

EXPERIENCE_LEVELS = ("beginner", "intermediate", "experienced", "expert")
HUBSPOT_EXPERIENCE_LEVELS = ("none", "beginner", "intermediate", "advanced")
AUTONOMY_LEVELS = ("hands-off", "pair-programming", "human-in-the-loop")
CONTROL_PROFILES = ("autonomous", "checkpointed", "strict")
PLANNING_STYLES = ("terse", "standard", "detailed")
TESTING_RIGOR_LEVELS = ("smoke", "standard", "strict")
GATE_POLICIES = ("ask-always", "ask-before-run", "allow")

STACK_PRESETS = {
    "react-card": {
        "tech_stack": "TypeScript, React, HubSpot UI Extensions, Node.js",
        "project_focus": "CRM app card UI extension",
        "use_cases": [
            "Event intake card (create/log event from contact or company record)",
            "Lead qualification card (score + next-best-action)",
            "Renewal health card (open risks, owner tasks, renewal status)",
            "Support escalation card (severity, SLA, assignee + quick actions)",
            "Meeting follow-up card (summary, tasks, timeline actions)",
        ],
    },
    "serverless-function": {
        "tech_stack": "TypeScript or JavaScript, HubSpot serverless functions, Node.js",
        "project_focus": "Serverless app function endpoints for HubSpot app",
        "use_cases": [
            "Inbound webhook processor for external systems",
            "Record enrichment endpoint using third-party APIs",
            "Workflow action backend endpoint with validation",
            "Signed request verification + secure fan-out",
            "Scheduled sync bridge between HubSpot and external DB",
        ],
    },
    "cms-module": {
        "tech_stack": "HubL or React module, CSS, JavaScript, HubSpot CMS",
        "project_focus": "Reusable CMS module development",
        "use_cases": [
            "Event listing module with date/location filters",
            "Speaker spotlight module for landing pages",
            "Pricing/plan comparison module",
            "Campaign hero module with CTA variants",
            "FAQ accordion module with analytics hooks",
        ],
    },
    "card-plus-serverless": {
        "tech_stack": "TypeScript, React card, HubSpot serverless functions, Node.js",
        "project_focus": "CRM card + serverless backend (recommended app pattern)",
        "use_cases": [
            "Event creator card + event API endpoint",
            "Deal risk card + aggregation endpoint",
            "Customer health card + enrichment endpoint",
            "Approval card + workflow-trigger endpoint",
            "NPS feedback card + summary endpoint",
        ],
    },
    "custom": {
        "tech_stack": "TypeScript, React, HubSpot UI Extensions, Node.js",
        "project_focus": "HubSpot app development (custom workflow)",
        "use_cases": [],
    },
}

AUTONOMY_EXPLANATIONS = {
    "hands-off": (
        "Agent drives implementation end-to-end and reports outcomes. "
        "Ask before deploy, production-impacting changes, or destructive operations."
    ),
    "pair-programming": (
        "Agent proposes a plan, then executes in checkpoints with regular syncs. "
        "Ask before high-impact or irreversible actions."
    ),
    "human-in-the-loop": (
        "Agent asks before non-trivial edits, write operations, risky commands, "
        "or architecture-level decisions."
    ),
}

CONTROL_EXPLANATIONS = {
    "autonomous": (
        "Allow autonomous command execution for safe development workflows; "
        "require confirmation for deploy, publish, account-level changes, and destructive commands."
    ),
    "checkpointed": (
        "Require confirmation at logical checkpoints: before major code edits, "
        "before running broad scripts, and before any deploy/publish action."
    ),
    "strict": (
        "Require confirmation before every write, external side effect, and shell command "
        "beyond read-only inspection."
    ),
}


@dataclass
class PreferenceAnswers:
    developer_experience: str
    hubspot_experience: str
    stack_preset: str
    tech_stack: str
    project_focus: str
    common_use_cases: list[str]
    autonomy_level: str
    control_profile: str
    action_gates: list[tuple[str, str]]
    planning_style: str
    testing_rigor: str
    communication_notes: str


def _prompt_choice(question: str, options: Iterable[str], default: str) -> str:
    options = tuple(options)
    print(f"\n{question}")
    for i, option in enumerate(options, start=1):
        marker = " (default)" if option == default else ""
        print(f"  {i}. {option}{marker}")

    while True:
        raw = input("Select option number: ").strip()
        if not raw:
            return default
        if raw.isdigit():
            idx = int(raw)
            if 1 <= idx <= len(options):
                return options[idx - 1]
        if raw in options:
            return raw
        print("Invalid choice. Enter a number or exact option value.")


def _prompt_text(question: str, default: str) -> str:
    raw = input(f"\n{question}\n[{default}] ").strip()
    return raw or default


def _prompt_multi_choice(question: str, options: list[str], default_count: int = 3) -> list[str]:
    print(f"\n{question}")
    for i, option in enumerate(options, start=1):
        marker = " (default)" if i <= default_count else ""
        print(f"  {i}. {option}{marker}")
    print("Enter comma-separated numbers. Press Enter to accept defaults.")

    default_values = options[: min(default_count, len(options))]
    while True:
        raw = input("Selection: ").strip()
        if not raw:
            return default_values

        values: list[str] = []
        ok = True
        for token in raw.split(","):
            token = token.strip()
            if not token:
                continue
            if not token.isdigit():
                ok = False
                break
            idx = int(token)
            if idx < 1 or idx > len(options):
                ok = False
                break
            candidate = options[idx - 1]
            if candidate not in values:
                values.append(candidate)

        if ok and values:
            return values
        print("Invalid selection. Use comma-separated numbers from the list.")


def _parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _parse_gate_values(raw_values: list[str] | None) -> list[tuple[str, str]]:
    parsed: list[tuple[str, str]] = []
    for raw in raw_values or []:
        if "=" not in raw:
            raise SystemExit(f"Invalid --gate value '{raw}'. Use action=policy format.")
        action, policy = raw.split("=", 1)
        action = action.strip()
        policy = policy.strip()
        if not action:
            raise SystemExit(f"Invalid --gate value '{raw}'. Action is empty.")
        if policy not in GATE_POLICIES:
            allowed = ", ".join(GATE_POLICIES)
            raise SystemExit(
                f"Invalid gate policy '{policy}' for action '{action}'. Allowed: {allowed}"
            )
        parsed.append((action, policy))
    return parsed


def _build_action_gates(control_profile: str, custom_gates: list[tuple[str, str]]) -> list[tuple[str, str]]:
    gates: dict[str, str] = {
        "hs project upload": "ask-always",
        "hs project deploy": "ask-always",
        "mcp__HubSpotDev__upload-project": "ask-always",
        "mcp__HubSpotDev__deploy-project": "ask-always",
    }

    if control_profile in ("checkpointed", "strict"):
        gates.update(
            {
                "hs project create": "ask-before-run",
                "mcp__HubSpotDev__create-project": "ask-before-run",
                "mcp__HubSpotDev__create-test-account": "ask-before-run",
                "hs secret add": "ask-before-run",
                "hs secret update": "ask-before-run",
                "hs cms upload": "ask-before-run",
            }
        )

    if control_profile == "strict":
        gates.update(
            {
                "Any write operation (create/update/delete/upload/deploy)": "ask-always",
                "Any non-read shell command": "ask-always",
            }
        )

    for action, policy in custom_gates:
        gates[action] = policy

    return sorted(gates.items(), key=lambda item: item[0].lower())


def _frontmatter(answers: PreferenceAnswers) -> str:
    lines = [
        "---",
        "preferences_version: 1",
        f'updated_at_utc: "{datetime.now(timezone.utc).replace(microsecond=0).isoformat()}"',
        f"developer_experience: {answers.developer_experience}",
        f"hubspot_experience: {answers.hubspot_experience}",
        f"stack_preset: {answers.stack_preset}",
        f"autonomy_level: {answers.autonomy_level}",
        f"control_profile: {answers.control_profile}",
        f"planning_style: {answers.planning_style}",
        f"testing_rigor: {answers.testing_rigor}",
    ]
    if answers.common_use_cases:
        primary = answers.common_use_cases[0].replace('"', "'")
        lines.append(f'primary_use_case: "{primary}"')
    lines.append("---")
    return "\n".join(lines)


def render_preference_markdown(answers: PreferenceAnswers) -> str:
    use_case_lines = [f"- {use_case}" for use_case in answers.common_use_cases] or [
        "- No preset use-cases selected."
    ]
    gate_lines = [f"- `{action}`: `{policy}`" for action, policy in answers.action_gates]

    parts = [
        _frontmatter(answers),
        "",
        "# Developer Preferences",
        "",
        "This file defines how agents should collaborate in this repository.",
        "",
        "## Profile",
        f"- Developer experience: `{answers.developer_experience}`",
        f"- HubSpot experience: `{answers.hubspot_experience}`",
        f"- Stack preset: `{answers.stack_preset}`",
        f"- Tech stack: `{answers.tech_stack}`",
        f"- Project focus: `{answers.project_focus}`",
        "",
        "## Common Use-Case Workflows",
        *use_case_lines,
        "",
        "## Autonomy",
        f"- Level: `{answers.autonomy_level}`",
        f"- Behavior: {AUTONOMY_EXPLANATIONS[answers.autonomy_level]}",
        "",
        "## Control",
        f"- Profile: `{answers.control_profile}`",
        f"- Execution policy: {CONTROL_EXPLANATIONS[answers.control_profile]}",
        "",
        "## Per-Action Gates",
        *gate_lines,
        "",
        "## Workflow Preferences",
        f"- Planning style: `{answers.planning_style}`",
        f"- Testing rigor: `{answers.testing_rigor}`",
        f"- Communication notes: {answers.communication_notes}",
        "",
        "## Gate Rules",
        "- Always ask before deploy, publish, production data changes, or destructive actions.",
        "- For HubSpot operations, use `HubSpotDev` MCP tools first; fall back to manual CLI only if MCP is blocked.",
        "- For technical HubSpot guidance, use `search-docs` then `fetch-doc` from HubSpot MCP before implementation advice.",
        "- Treat external input as untrusted and keep security/performance tradeoffs explicit.",
        "- Keep change summaries concise and include impacted files plus tests run.",
        "",
    ]
    return "\n".join(parts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="preference.md", help="Output markdown file path")
    parser.add_argument("--interactive", action="store_true", help="Run interview prompts")
    parser.add_argument("--developer-experience", choices=EXPERIENCE_LEVELS)
    parser.add_argument("--hubspot-experience", choices=HUBSPOT_EXPERIENCE_LEVELS)
    parser.add_argument("--stack-preset", choices=tuple(STACK_PRESETS.keys()), default="custom")
    parser.add_argument("--tech-stack", help="Comma-separated stack summary")
    parser.add_argument("--project-focus", help="What the developer is building")
    parser.add_argument("--use-cases", help="Comma-separated use-case strings")
    parser.add_argument("--autonomy-level", choices=AUTONOMY_LEVELS)
    parser.add_argument("--control-profile", choices=CONTROL_PROFILES)
    parser.add_argument("--gate", action="append", help="Per-action gate in action=policy format")
    parser.add_argument("--planning-style", choices=PLANNING_STYLES, default="standard")
    parser.add_argument("--testing-rigor", choices=TESTING_RIGOR_LEVELS, default="standard")
    parser.add_argument(
        "--communication-notes",
        default="Prefer concise updates with explicit tradeoffs and next steps.",
    )
    return parser.parse_args()


def gather_answers(args: argparse.Namespace) -> PreferenceAnswers:
    if args.interactive:
        developer_experience = _prompt_choice(
            "Overall software development experience?",
            EXPERIENCE_LEVELS,
            args.developer_experience or "experienced",
        )
        hubspot_experience = _prompt_choice(
            "HubSpot app/platform experience?",
            HUBSPOT_EXPERIENCE_LEVELS,
            args.hubspot_experience or "intermediate",
        )
        stack_preset = _prompt_choice(
            "Choose a stack preset.",
            STACK_PRESETS.keys(),
            args.stack_preset or "react-card",
        )
        preset = STACK_PRESETS[stack_preset]

        tech_stack = _prompt_text(
            "Primary tech stack (frameworks/languages/tools)?",
            args.tech_stack or preset["tech_stack"],
        )
        project_focus = _prompt_text(
            "Current project focus?",
            args.project_focus or preset["project_focus"],
        )
        if preset["use_cases"]:
            common_use_cases = _prompt_multi_choice(
                "Select common workflows to optimize for.",
                preset["use_cases"],
            )
        else:
            custom_use_cases = _prompt_text(
                "Enter common workflows (comma-separated).",
                args.use_cases or "",
            )
            common_use_cases = _parse_csv(custom_use_cases)

        autonomy_level = _prompt_choice(
            "Preferred AI autonomy level?",
            AUTONOMY_LEVELS,
            args.autonomy_level or "pair-programming",
        )
        control_profile = _prompt_choice(
            "Preferred control profile?",
            CONTROL_PROFILES,
            args.control_profile or "checkpointed",
        )
        additional_gates = _prompt_text(
            "Additional actions to always ask before (comma-separated, optional)",
            "",
        )
        custom_gates = [(action, "ask-always") for action in _parse_csv(additional_gates)]
        custom_gates.extend(_parse_gate_values(args.gate))

        planning_style = _prompt_choice(
            "Planning detail preference?",
            PLANNING_STYLES,
            args.planning_style,
        )
        testing_rigor = _prompt_choice(
            "Testing rigor?",
            TESTING_RIGOR_LEVELS,
            args.testing_rigor,
        )
        communication_notes = _prompt_text(
            "Any communication preferences for agents?",
            args.communication_notes,
        )
    else:
        stack_preset = args.stack_preset or "custom"
        preset = STACK_PRESETS[stack_preset]
        tech_stack = args.tech_stack or preset["tech_stack"]
        project_focus = args.project_focus or preset["project_focus"]
        common_use_cases = _parse_csv(args.use_cases) or list(preset["use_cases"][:3])
        custom_gates = _parse_gate_values(args.gate)

        missing = [
            name
            for name, value in (
                ("--developer-experience", args.developer_experience),
                ("--hubspot-experience", args.hubspot_experience),
                ("--autonomy-level", args.autonomy_level),
                ("--control-profile", args.control_profile),
                ("--tech-stack/--stack-preset", tech_stack),
                ("--project-focus/--stack-preset", project_focus),
            )
            if not value
        ]
        if missing:
            missing_csv = ", ".join(missing)
            raise SystemExit(
                f"Missing required arguments for non-interactive mode: {missing_csv}. "
                "Use --interactive or provide all required flags."
            )
        developer_experience = args.developer_experience
        hubspot_experience = args.hubspot_experience
        autonomy_level = args.autonomy_level
        control_profile = args.control_profile
        planning_style = args.planning_style
        testing_rigor = args.testing_rigor
        communication_notes = args.communication_notes

    action_gates = _build_action_gates(control_profile, custom_gates)
    return PreferenceAnswers(
        developer_experience=developer_experience,
        hubspot_experience=hubspot_experience,
        stack_preset=stack_preset,
        tech_stack=tech_stack,
        project_focus=project_focus,
        common_use_cases=common_use_cases,
        autonomy_level=autonomy_level,
        control_profile=control_profile,
        action_gates=action_gates,
        planning_style=planning_style,
        testing_rigor=testing_rigor,
        communication_notes=communication_notes,
    )


def main() -> None:
    args = parse_args()
    answers = gather_answers(args)
    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    content = render_preference_markdown(answers)
    output_path.write_text(content, encoding="utf-8")
    print(f"[ok] Wrote {output_path}")


if __name__ == "__main__":
    main()
