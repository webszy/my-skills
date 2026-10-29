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

CDF keeps small changes lightweight while applying stronger controls to risky, sensitive, cross-cutting, or architectural work. Every development path—including “turn this PRD into tasks”—must complete repository inspection, risk classification, planning, Scope Lock, and approval before implementation or persistent task compilation. Explicit read-only drafts need no execution/save approval and create neither authority nor runtime progress. The S/M/L/XL model is retained; evidence-backed bounded local use of an existing shared presentation parameter may qualify as S.

| User action | Result |
|---|---|
| **Execute Now** | Implement only the approved scope and report verification actually performed |
| **Save as Task** | Compile and verify a resumable `_cdtask` document, return its path, and stop; this approval authorizes persistence only |

Task compilation is an internal CDF component. There is no top-level tasking Skill, separate installation target, or independent invocation.

### Contract essentials

- Chat approval normally shows a concise `Requirement Understanding`, `Technical Approach`, `Implementation Plan`, and `Risks`, followed by confirmation of the already-selected action; offer execute/save only if unspecified. Level S keeps its four-line fast path. Full contract details are shown only on request.
- The eleven-section Development Plan is the handoff and saved-task file format. After **Save as Task** approval, CDF organizes the approved material into that format and preserves the exact displayed summary as approval evidence. Formatting alone does not require a second approval; hidden obligations are never authorized.
- The single `cdf-scope/v1` block is the sole canonical scope authority, and its `acceptance_criteria` field is the sole canonical acceptance source. Approval-ready `in_scope` and `acceptance_criteria` arrays must both be non-empty. The Development Plan’s `Acceptance Criteria` section is only an item-for-item, same-order, verbatim projection.
- For partial approval, `Partial Approval Result` is an audit projection of approved and unapproved items. It does not copy the complete Scope Lock or create a second authority source.
- Before saving, CDF performs a drift preflight and records current `Workspace`, `Source-Branch`, `Source-Commit`, `Source-Worktree-State`, and relevant `Source-Worktree-Changes`. Material drift returns to planning and renewed approval.
- `cdf-cdtask/v2` stores scope/approval digests and a complete definition SHA-256 at save, verified on final read-back and every execution/resume. Local Task Verification is separate from canonical Product Acceptance. Old v1 tasks remain read-only pending explicit review/re-approval; hashes never prove human approval provenance.

Resume a saved task through CDF:

```text
$cdf continue task <path>
```

CDF validates the task contract and required sections, integrity digests, current repository state, assumptions, stop conditions, and material drift. After validation succeeds, the explicit continue request creates a current-turn `Resume Authorization Record`; only then may saved work execute. Before the first code change, CDF creates or validates the separate `cdf-execution-progress/v2` sidecar, skips only still-applicable `verified` tasks, and inspects interrupted work before continuing. Inspecting, reviewing, summarizing, or validating a task authorizes neither execution nor progress mutation.

Resume checks include read-only evidence dependencies and read-only reconciliation of existing progress, so normal approved execution output does not itself force replanning. Material drift ends the old resume route: newly approved work executes under the new plan or is saved at a new task path. Compilation requires full canonical acceptance coverage. Controlled in-scope reopen preserves history and invalidates downstream checks. Completion requires every product criterion, the evidence gate and a current recorded final review; local verified alone is insufficient.

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
- **Skill package version:** 1.3.0

These are separate version systems. Suite maturity describes the CDF architecture; package version describes the distributable release.

Repository metadata: [skill.json](skill.json)

## app-analytics-audit-flow

`app-analytics-audit-flow` is a code-first Skill for mobile app growth, monetization, subscription, attribution, store, and stability analysis.

- [Guide](skills/app-analytics-audit-flow/README.md)
- [Skill metadata](skills/app-analytics-audit-flow/skill.json)

```bash
npx skills add https://github.com/webszy/my-skills --skill app-analytics-audit-flow -a codex -a claude-code -g -y
```
