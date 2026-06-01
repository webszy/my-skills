# cdf

`cdf` is short for `controlled-development-flow`: a risk-based development workflow Skill for AI Coding Agents.

It helps agents avoid two common failure modes:

- Over-planning simple changes.
- Rushing risky changes.

Core principle:

> Small changes should be fast. Risky changes should be controlled.

## Compatibility

`cdf` follows the Agent Skills `SKILL.md` format used by Codex and Claude Code:

- Skill folder: `skills/cdf/`
- Skill entrypoint: `skills/cdf/SKILL.md`
- Skill name: `cdf`
- Skill metadata: `skills/cdf/skill.json`
- Codex UI metadata: `skills/cdf/agents/openai.yaml`

The folder name and `SKILL.md` frontmatter `name` match intentionally. This keeps the skill compatible with the Agent Skills specification and makes the short invocation stable.

## Bundled References

`cdf` includes `references/karpathy-guidelines.md` as a bundled MIT-licensed reference for coding-agent guardrails: think before coding, keep changes simple, make surgical edits, and define verifiable success criteria.

For Level M, Level L, and Level XL tasks, the agent must read this reference before producing a plan, design, or implementation. For Level S tasks, reading it is optional so simple changes stay lightweight.

The reference is included so users do not need to install `karpathy-guidelines` separately.

## Target Existence Check

Before editing an existing target, the agent must verify that the requested target exists in the codebase.

For example, if the user asks to modify a button, the agent should first locate that button. If the button does not exist or cannot be uniquely identified, the agent should pause and ask whether the user wants to create a new button, modify a different button, or correct the request.

For new modules, services, top-level workflows, or architecture, the agent should enter the design workflow, but still search first for existing similar modules or workflows to avoid duplication.

This rule applies to every workflow level, including simple Level S changes. It prevents the agent from guessing or silently creating missing targets.

## Evidence-Based Thinking

After locating the target, the agent must think from concrete code evidence before producing a plan.

For Level M, Level L, and Level XL tasks, the plan or design should be grounded in actual files, symbols, fields, schemas, APIs, configuration keys, call sites, or search results. The agent should explicitly include confirmed evidence and open assumptions before planning.

If the evidence is insufficient, the agent should continue inspecting or pause and ask the user instead of outputting a generic plan.

## Workflow Levels

### Level S: Direct Edit

For simple UI, copy, and style changes.

Examples:

- Button color.
- Text wording.
- Spacing.
- Icon size.
- Static UI adjustment.

Agent behavior:

- Edit directly.
- Do not ask for confirmation.
- Do not create a long plan.
- Provide a brief summary, verification performed, and relevant manual checks after editing.

### Level M: Brief Plan Then Edit

For normal scoped feature changes.

Examples:

- Add a filter.
- Change form behavior.
- Add a validation rule.
- Modify a small API call.
- Adjust one page interaction.

Agent behavior:

- Give a short plan.
- Proceed if the requirement is clear.
- Ask only if ambiguous.
- Provide verification performed and relevant manual checks after editing.

### Level L: Approval Required

For high-risk changes.

Examples:

- Database schema.
- Payment, billing, subscription, or IAP logic.
- Reports, revenue, cost, ROI, or business metric logic.
- Authentication or permissions.
- Cron jobs, sync tasks, queues, retries, or idempotency.
- Production or deployment configuration.

Agent behavior:

- Do not edit immediately.
- Explain requirement understanding.
- Define change scope and affected modules.
- Propose an implementation plan.
- Explain risks and test plan.
- Wait for approval.

### Level XL: Design Required

For architecture or module-level changes.

Examples:

- New module or backend service.
- Major refactor.
- Full report pipeline.
- Permission system.
- App Store Connect API integration.
- Advertising statistics pipeline.

Agent behavior:

- Create a design first.
- Break implementation into phases.
- Wait for approval.
- Avoid large uncontrolled edits.

## Installation

Install for Codex:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -g -y
```

Install for Claude Code:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a claude-code -g -y
```

Install for both:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -a claude-code -g -y
```
