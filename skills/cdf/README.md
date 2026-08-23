# CDF: Controlled Development Flow

CDF is a controlled AI development workflow. It analyzes the requirement and repository evidence, classifies risk, builds and locks a development plan, requires human approval, then either executes the approved work or compiles it into a resumable task.

> Small changes should be fast. Risky changes should be controlled.

## Architecture

CDF is the only user-facing controlled-development Skill:

```text
Requirement / PRD / Development Request
    -> Requirement Understanding
    -> Evidence Inspection
    -> Risk Classification
    -> Development Plan
    -> cdf-scope/v1 Scope Lock
    -> Human Approval
    -> Execute Now | Save as Task
```

Planning, approval, and approved execution all belong to CDF. Saving a task enters an internal post-approval compiler under `components/cdtask/`; that component is not installed or invoked separately.

## Risk and Planning

CDF classifies risk from impact, blast radius, reversibility, uncertainty, sensitivity, and coordination needs:

| Level | Typical work |
|---|---|
| **S** | One local cosmetic or static change with no shared or behavioral impact |
| **M** | Bounded local behavior, small shared-component work, bounded configuration, or bounded external-integration usage |
| **L** | Cross-cutting behavior, persistent data, billing, auth, security, privacy, materially meaningful analytics, meaningful external contracts, or non-trivial rollback |
| **XL** | Architecture, a new subsystem/service, migration, major data-flow redesign, phased rollout, or multi-system coordination |

A signal informs the classification and may establish a floor; it is not automatically the final risk. Plans stay compact for small changes and become more detailed as risk, uncertainty, or coordination grows.

## Scope and Approval

Every plan contains a canonical `cdf-scope/v1` block with all eight fields:

- `in_scope`
- `out_of_scope`
- `non_goals`
- `assumptions`
- `stop_conditions`
- `will_change`
- `will_not_change`
- `acceptance_criteria`

Fields may be empty arrays when there is no meaningful content. After approval the block is immutable: it may not be paraphrased, widened, weakened, or normalized during execution or task compilation.

Approval must identify both the approved Scope Lock (or subset/phase) and one action:

1. **Execute Now** — implement only the approved scope and report checks actually run.
2. **Save as Task** — compile and persist a resumable task, then stop.

Acknowledgements such as `ok` or `continue` are not enough when the action or approved boundary is unclear. Full, conditional, and partial approvals are supported; unapproved partial items remain explicitly excluded.

## Saved Tasks and Resume

The internal compiler accepts only an approved CDF handoff using `cdf-cdtask/v1`. It preserves the canonical Scope Lock verbatim, creates dependency-aware tasks, runs a Scope Guard, saves under `_cdtask/` by default, and verifies the saved file by reading it back.

Resume through CDF:

```text
$cdf continue task <path>
```

CDF validates the task contract, Scope Lock, Approval Record, assumptions, stop conditions, current code, and repository drift. Material drift returns to planning and renewed approval; a stale task is never executed blindly.

## Usage

```text
Use $cdf to analyze this development request, inspect the repository,
classify risk, lock the plan, obtain approval, then execute it or save it
as a resumable task.
```

The complete operating rules are in [SKILL.md](SKILL.md).

## Installation

Codex:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -g -y
```

Claude Code:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a claude-code -g -y
```

Both:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -a claude-code -g -y
```

## Version Semantics

- **CDF Suite maturity:** v0.1
- **Skill package version:** 1.1.0

These are separate version systems. The maturity label describes the architecture; the package version describes this distributable Skill release.

## Internal Layout

```text
skills/cdf/
|-- SKILL.md
|-- README.md
|-- README.zh-CN.md
|-- skill.json
|-- agents/openai.yaml
|-- references/
`-- components/cdtask/
```

Only `cdf` is a Skill entrypoint. The task compiler uses `COMPONENT.md`, not `SKILL.md`.
