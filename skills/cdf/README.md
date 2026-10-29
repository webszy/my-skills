# CDF: Controlled Development Flow

CDF is the only user-facing entry to the Controlled Development Flow suite. It turns a development request into an evidence-backed, risk-classified, scope-locked plan, then executes or saves only explicitly approved work. CDTask is an internal compiler, never a separate Skill, service or runtime.

**Small changes should be fast. Risky changes should be controlled.**

- Skill Package Version: **1.3.0**
- CDF Suite Maturity: **v0.1** (a separate concept)
- Contracts: `cdf-scope/v1`, `cdf-cdtask/v2`, `cdf-execution-progress/v2`

## Use

Invoke `$cdf`, `/cdf`, `cdf:`, `controlled-development-flow`, or explicitly request the controlled workflow. The package retains explicit invocation policy for Codex and works through relative local references in both Codex and Claude Code.

```text
$cdf Analyze this feature, then ask me to approve execution.
$cdf Draft a task breakdown only; do not execute or save.
$cdf Approve the displayed plan and save as task.
$cdf continue task <path>
$cdf validate task <path> without executing it
```

Approval binds the concrete displayed plan and chosen action. If execution/save was already specified, confirm that action without offering a redundant menu. Ambiguous scope/action cannot be authorized by “ok” or silence. A read-only draft is unapproved and creates neither a formal task nor progress nor execution permission.

## Flow

```text
Requirement -> Requirement Gate -> Repository Evidence -> Risk -> Plan
 -> Canonical Scope Lock -> Human Approval
    Execute Now -> scoped implementation
    Save as Task -> internal compilation -> persistence/read-back -> stop
       -> current explicit resume request + integrity/history/drift validation
       -> scoped implementation
 -> Task Verification -> Product Acceptance -> Completion Evidence Gate
 -> Final Scoped Review (+ only applicable approvals) -> Completed
```

S uses a four-line fast-path plan; M/L/XL expose a concise summary of requirement, technical approach, steps/verification and risks. Full evidence still exists internally. Saved files use the eleven-section Development Plan; mechanical formatting cannot introduce hidden obligations.

The S Reverse Check may accept one call site's existing static shared-component parameter when the definition, public interface, global tokens, behavior and other consumers are unchanged and evidence supports independent verification/rollback. A shared definition or interface edit requires reassessment at least at M; broad/global behavior may be L. File count alone never determines risk.

## v1.3.0 reliability changes

- Product ACs remain immutable canonical scope data. `contributes_to` maps task contribution; approved local `task_verification` checks unblock dependencies without prematurely claiming end-to-end acceptance.
- Save establishes hashes for Scope Lock, Approval Record and the **entire definition**. Only the definition digest's own frontmatter line is excluded. Final read-back and every first execution/resume recompute them. A missing or mismatched baseline cannot be silently regenerated. These hashes are limited integrity checks, not authorization signatures.
- v2 runtime journals controlled `verified -> in_progress -> verified` repair with reason/scope evidence, retained old receipts and downstream invalidation. New scope or decisions stop execution and require replanning.
- Completion requires every canonical product criterion, actual checks/diff/scope evidence, gate PASS, and a recorded final review with evidence, source snapshot, time and outstanding findings. Changes after review invalidate affected checks/review. No new human approval is invented where the host workflow does not require it.
- v1 tasks/sidecars remain historical, read-only artifacts. Migration requires explicit comparison, re-approval and a distinct new task when saving; never replace original approval/history or reinterpret v1 as v2.

Saved documents remain Markdown. v2 uses JSON values in YAML frontmatter, JSON fenced structured sections and JSON-compatible YAML runtime data to keep the validator standard-library-only. Scope keeps its v1 schema, using a documented narrow wire profile for v2 tasks. Choose representation before approval; never normalize approved payloads to force a match.

## Validation

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/cdf/tests -p 'test_*.py' -v
python3 skills/cdf/scripts/validate_cdf.py --describe
python3 skills/cdf/scripts/validate_cdf.py <task.md>
python3 skills/cdf/scripts/validate_cdf.py <task.md> --progress <task.md.progress.yaml> --snapshot <actual-current-sha256>
```

The CLI is read-only. Exit 0 is mechanical validity, never semantic approval or execution permission; exit 1 contains JSON errors. It always lists required semantic review. `--draft-hashes` computes hashes for a newly approved unsaved candidate only, not for repairing saved baselines. `--previous-progress` checks append-only history against a preserved earlier snapshot.

[Validation results](tests/validation-results.md) distinguish executed mechanical tests from unexecuted Agent behavior cases. Synthetic fixture approvals/receipts prove protocol mechanics, not real human approval, login functionality, visual quality or real Agent compliance.

Active CDF replies begin with `当前流程：cdf v<version>` read from skill metadata. They disclose actual Current Agent Actions and unrelated edits (including reverted ones), explicitly None/Unknown as supported. Level S may show `Changed`, `Verified`, `Scope`, `Remaining Issues` while retaining the full internal evidence; failures and gaps must remain visible.

## References loaded by route

- [SKILL.md](SKILL.md): entry, control gates, S risk check and approval.
- [Requirement Gate](references/requirement-gate.md), [Risk Classification](references/risk-classification.md), [Coding Discipline](references/karpathy-guidelines.md): when relevant to planning.
- [Task Handoff](references/task-handoff.md), [CDTask](components/cdtask/COMPONENT.md), [Task Templates](components/cdtask/references/task-templates.md), [Persistence](components/cdtask/references/persistence.md): Save only.
- [Resume / compatibility](references/resume.md), [Execution Progress](references/execution-progress.md): saved-task validation/execution.
- [Completion Evidence Gate](references/completion-evidence-gate.md): completion evaluation.
- [Boundary Cases](references/boundary-cases.md): decisions near risk, approval and scope boundaries.

## Install

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -a claude-code -g -y
```

Use only `-a codex` or `-a claude-code` to install for one host. No separate CDTask installation is needed.
