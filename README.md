# Webszy Skills

This repository contains CDF, a controlled AI development workflow, alongside other AI coding-agent skills.

## CDF: Controlled Development Flow

CDF is the only user-facing entry point in the CDF Suite. It owns the complete controlled-development path:

```text
Requirement / PRD / Development Request
    -> Requirement Gate
    -> Requirement Understanding
    -> Repository Evidence Inspection
    -> Risk Classification
    -> Development Plan
    -> cdf-scope/v1 Scope Lock
    -> Human Approval
    -> Execute Now | Save as Task
```

CDF keeps small changes lightweight while applying stronger controls to risky, sensitive, cross-cutting, or architectural work. Every development path—including “turn this PRD into tasks”—must complete repository inspection, risk classification, planning, Scope Lock, and approval before implementation or task compilation. The S/M/L/XL risk model is unchanged.

| User action | Result |
|---|---|
| **Execute Now** | Implement only the approved scope and report verification actually performed |
| **Save as Task** | Compile and verify a resumable `_cdtask` document, return its path, and stop; this approval authorizes persistence only |

Task compilation is an internal CDF component. There is no top-level tasking Skill, separate installation target, or independent invocation.

### Contract essentials

- The Development Plan uses these canonical headings in order: `Requirement Understanding`, `Evidence Summary`, `Risk Gate Result`, `Scope Lock`, `Technical Approach`, `Implementation Plan`, `Risks`, `Rollback Plan`, `Acceptance Criteria`, `Verification Strategy`, and `Next Action`.
- The single `cdf-scope/v1` block is the sole canonical scope authority, and its `acceptance_criteria` field is the sole canonical acceptance source. Approval-ready `in_scope` and `acceptance_criteria` arrays must both be non-empty. The Development Plan’s `Acceptance Criteria` section is only an item-for-item, same-order, verbatim projection.
- For partial approval, `Partial Approval Result` is an audit projection of approved and unapproved items. It does not copy the complete Scope Lock or create a second authority source.
- Before saving, CDF performs a drift preflight and records current `Workspace`, `Source-Branch`, `Source-Commit`, `Source-Worktree-State`, and relevant `Source-Worktree-Changes`. Material drift returns to planning and renewed approval.
- Scope Lock and Approval Record SHA-256 values use deterministic serialization: UTF-8, LF line endings, no Markdown fence delimiters, no trailing whitespace on content lines, and exactly one trailing LF.

Resume a saved task through CDF:

```text
$cdf continue task <path>
```

CDF validates the task contract and required sections, integrity digests, current repository state, assumptions, stop conditions, and material drift. After validation succeeds, the explicit continue request creates a current-turn `Resume Authorization Record`; only then may saved work execute. Before the first code change, CDF creates or validates the separate `cdf-execution-progress/v1` sidecar, skips only still-applicable `verified` tasks, and inspects interrupted work before continuing. Inspecting, reviewing, summarizing, or validating a task authorizes neither execution nor progress mutation.

CDF is configured for explicit invocation. Common forms include `$cdf`, `/cdf`, `cdf:`, and `controlled-development-flow`.

Read the full documentation:

- [CDF operating rules](skills/cdf/SKILL.md)
- [CDF guide](skills/cdf/README.md)
- [CDF 中文指南](skills/cdf/README.zh-CN.md)

### Installation

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

### Version Semantics

- **CDF Suite maturity:** v0.1
- **Skill package version:** 1.2.0

These are separate version systems. Suite maturity describes the CDF architecture; package version describes the distributable release.

Repository metadata: [skill.json](skill.json)

## app-analytics-audit-flow

`app-analytics-audit-flow` is a code-first Skill for mobile app growth, monetization, subscription, attribution, store, and stability analysis.

- [Guide](skills/app-analytics-audit-flow/README.md)
- [Skill metadata](skills/app-analytics-audit-flow/skill.json)

```bash
npx skills add https://github.com/webszy/my-skills --skill app-analytics-audit-flow -a codex -a claude-code -g -y
```
