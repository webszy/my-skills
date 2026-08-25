# Internal CDTask Persistence Contract

Read this reference before choosing a destination or writing a task document. It applies only to an approved `cdf-cdtask/v1` handoff selected by CDF's **Save as Task** path.

The component boundary, compilation workflow, and blocking semantics remain in [COMPONENT.md](../COMPONENT.md).

CDF owns the drift preflight immediately before **Save as Task**. It supplies the latest traceability metadata plus `Save-Drift-Preflight` and `Save-Drift-Notes`. CDTask persists that result and validates its shape; it does not reinspect the repository, reclassify drift, or replan.

## Destination Rules

Use `Requested-Task-Path` when CDF supplies it. If CDF supplies no path, use:

```text
<Workspace>/_cdtask/YYYY-MM-DD-<short-slug>.md
```

- Derive the date at save time. Use `Task-Title` when CDF supplies it; otherwise derive a filesystem-safe slug mechanically from the first approved `in_scope` entry, using `task` if that entry has no usable characters.
- Resolve a relative CDF-supplied path against the absolute `Workspace`.
- If `Workspace` is `Unavailable`, require CDF to supply an absolute destination; do not guess a workspace.
- Create only the required parent directory and task document.
- Do not modify implementation files or unrelated documents.
- Never silently overwrite an existing file.
- For a default-path collision, append a numeric suffix such as `-2` and preserve the existing file.
- For an explicit-path collision, return `BLOCKED` with `persistence-failure` unless CDF supplies a newly confirmed destination or explicit replacement authority.

## Saved Document Frontmatter

Use this frontmatter:

```yaml
---
task_contract: cdf-cdtask/v1
handoff_type: approved-tasking
status: tasking_ready
source: cdf
approval_state: approved
risk_level: <Level S | Level M | Level L | Level XL>
workspace: <absolute path or Unavailable>
source_branch: <branch or Unavailable>
source_commit: <commit or Unavailable>
source_worktree_state: <clean | dirty | Unavailable>
source_worktree_changes: []
save_drift_preflight: <matched | non-material-drift>
save_drift_notes: <none | concise evidence-backed explanation>
scope_lock_sha256: <64 lowercase hexadecimal characters>
approval_record_sha256: <64 lowercase hexadecimal characters>
created_at: <ISO-8601 timestamp>
---
```

`tasking_ready` is a task-definition state. It does not mean assigned, running, executed, reviewed, or verified, and it does not grant execution authority.

Both digest fields must contain lowercase 64-character values produced by actual hashing commands over the exact canonical payloads after the authoritative pre-save text comparison. If either digest cannot be computed, return `BLOCKED` with `persistence-failure`; do not save a document that cannot establish its later resume baseline. A fabricated digest is never permitted.

`source_worktree_changes` must always be one flow-style YAML array:

- use `[]` when no relevant changes exist, including a clean worktree;
- for relevant dirty paths, use a stable YAML sequence of quoted `git status --short` entries such as `[' M src/foo.ts', '?? src/new-file.ts']`, preserving both `XY` characters including a leading space;
- use `[Unavailable]` only when relevant status evidence cannot be obtained.

Record only paths related to approved work, affected areas, or protected areas. Preserve repository-relative paths and sort deterministically by path, then status. Do not copy every unrelated dirty path from a large repository. `source_worktree_state: dirty` is a drift signal, not an automatic material-drift decision, and may legitimately accompany `source_worktree_changes: []` when all dirty paths are unrelated.

## Required Document Sections

Persist the sections below in this order. Copy approved planning material verbatim. Do not split, rename, summarize, or regenerate approved Development Plan content.

1. **Title**
2. **CDF Resume Contract**
3. **Development Plan** — verbatim, including its sole canonical `cdf-scope/v1` block
4. **Approved Phase Boundary**, when applicable
5. **Approval Record** — verbatim and immutable
6. **Partial Approval Result**, when applicable, in the stable format below
7. **Dependency Graph**
8. **Dependency Data**
9. **Task Definitions**
10. **Scope Guard**
11. **Future CDF Execution Constraints**
12. **Compilation Gate Result**
13. **Save Verification**

The persisted Development Plan must retain these approved headings in this order:

```markdown
## Development Plan

### Requirement Understanding
### Evidence Summary
### Risk Gate Result
### Scope Lock
### Technical Approach
### Implementation Plan
### Risks
### Rollback Plan
### Acceptance Criteria
### Verification Strategy
### Next Action
```

Its `### Scope Lock` section contains the only complete canonical Scope Lock in the saved document. Do not create a second Canonical Scope Lock section. For Level S or M, preserve a concise reversible action or genuine `None` under `### Rollback Plan`; do not expand it into filler.

Canonical `in_scope` and `acceptance_criteria` must each contain at least one non-empty entry. `cdf-scope/v1.acceptance_criteria` is the sole canonical acceptance source. The plan's `### Acceptance Criteria` must contain an item-for-item, same-order, verbatim projection of that array. Task-level criteria may contain only applicable canonical entries quoted verbatim and retained in canonical order. Any empty required array, addition, deletion, weakening, broadening, reinterpretation, merge, split, or need for a new criterion is `BLOCKED` and returns to CDF for refreshed planning and renewed approval.

When applicable, persist the partial-approval projection defined in [Human Approval](../../../SKILL.md#6-human-approval) exactly as received.

Do not copy another complete Scope Lock into this projection. Approved Items must quote canonical `in_scope` entries verbatim. Unapproved Items must be preserved verbatim, protected by canonical exclusions, and have no positive task, write scope, acceptance mapping, or verification obligation. Unsafe separation is `BLOCKED` with `partial-separation` and returns to CDF planning and renewed approval.

The CDF Resume Contract must state:

```markdown
## CDF Resume Contract
- Resume Path: CDF only
- Task Contract: cdf-cdtask/v1
- Canonical Scope Lock: cdf-scope/v1
- Saved Definition State: tasking_ready
- Execution Authorized by This Document: No
- Saved Approval Meaning: approved scope and Save as Task persistence authorization only
- Source Workspace: <absolute path or Unavailable>
- Source Branch: <branch or Unavailable>
- Source Commit: <commit or Unavailable>
- Source Worktree State: <clean | dirty | Unavailable>
- Source Worktree Changes: <[] | [Unavailable] | stable YAML array of relevant git status entries>
- Save Drift Preflight: <matched | non-material-drift>
- Save Drift Notes: <none | concise evidence-backed explanation>
- Scope Lock SHA-256: <64 lowercase hexadecimal characters>
- Approval Record SHA-256: <64 lowercase hexadecimal characters>
- Execution Progress Path: <resolved absolute saved-task path>.progress.yaml
- Execution Progress Created By Save: No
```

The Source Worktree Changes line is a readable projection of the frontmatter array and must preserve the same entries and order. The saved Approval Record is immutable historical evidence. It does not authorize future execution and must never be edited during resume.

The Compilation Gate Result must state the pre-save result and must not claim that implementation was reviewed or verified:

```markdown
## Compilation Gate Result
- Compilation Status: READY
- Task Count: <number>
- Scope Guard: passed
- Canonical Scope Lock Before Save: matched approved handoff
```

## Canonical Integrity Verification

Apply [Integrity Verification](../../../SKILL.md#integrity-verification) when validating the handoff, before save, during read-back, and during a later CDF resume. Compare payloads line for line while the handoff is available; that comparison is authoritative. Persist and later recompute both required digests as the durable cross-session baseline.

Use only the deterministic payload-byte representation defined there: UTF-8, LF line endings, excluded Markdown fences, no trailing whitespace on payload lines, and exactly one trailing LF. Do not introduce a persistence-specific serialization variant.

Reject non-LF payloads, trailing whitespace on payload lines, missing or ambiguous boundaries, a reordered Scope Lock, duplicate canonical Scope Lock blocks, unavailable digests, or digest mismatches. Never normalize or repair an approved payload inside CDTask. Mirror the computed lowercase 64-character digests in the CDF Resume Contract.

## Read-Back Verification

Write the document initially with this provisional final section:

```markdown
## Save Verification
- Status: pending-read-back
```

Reopen the exact destination and verify all of the following:

- the file exists at the resolved absolute path;
- frontmatter parses and every required metadata value matches the approved handoff;
- `task_contract`, `handoff_type`, `approval_state`, and definition `status` have the exact supported values;
- workspace, branch, commit, worktree state, the legal path-scoped worktree changes array, save-drift preflight result and notes, risk, and timestamp traceability are present and match the handoff;
- every required and applicable section is present;
- the Development Plan and all canonical headings are copied verbatim in the required order, with no regenerated parallel planning sections;
- the plan contains exactly one canonical Scope Lock payload, and it matches the handoff payload line for line;
- the plan's Acceptance Criteria is an item-for-item, same-order, verbatim projection of canonical `cdf-scope/v1.acceptance_criteria`;
- the persisted Approval Record matches the received Approval Record line for line;
- each digest field holds an actually computed digest and recomputing the exact payload produces the same value;
- the stable Partial Approval Result, when applicable, contains only the verbatim Approved/Unapproved projections and `Scope-Lock-Version: cdf-scope/v1`, without a second complete Scope Lock;
- partial-approval exclusions are preserved as protections and have no corresponding positive task, acceptance mapping, or verification obligation;
- task IDs are unique and every dependency resolves;
- the dependency graph is acyclic and matches Dependency Data and task fields;
- every task maps only to approved scope and at least one applicable canonical acceptance entry quoted verbatim and in canonical order;
- Scope Guard is fully checked;
- Future CDF Execution Constraints and CDF-only resume rules are present;
- the document contains no claim that planned implementation verification was performed;
- the document does not grant execution authorization.

Only after this pass succeeds, replace the provisional section with:

```markdown
## Save Verification
- [x] Frontmatter and traceability match the approved handoff.
- [x] Required sections are present.
- [x] Verbatim Development Plan headings, sole canonical Scope Lock, and acceptance projection match.
- [x] Immutable Approval Record and stable partial-approval projection are preserved.
- [x] Required Scope Lock and Approval Record digests recompute and match.
- [x] Source worktree changes and save-drift preflight metadata match.
- [x] Task IDs and dependency data are internally consistent.
- [x] Scope Guard and CDF-only resume constraints are present.
- [x] The document grants no execution authority.
- Verified At: <ISO-8601 timestamp>
```

Writing this section is the only change made after the read-back pass, so it cannot invalidate the checks above. Confirm every item is checked and `Verified At` is populated, then return the absolute path and verified result to CDF and stop.

If any read-back check fails, do not report `READY`, do not treat the file as resumable, and do not continue into execution. Return `BLOCKED` with `Blocked-Reason-Class: persistence-failure`, the affected path, and a concise mismatch or I/O reason.

## Resume Validation Performed by CDF

The saved document is input to a later CDF continuation, never directly to CDTask or an executor. Follow [Resume a Saved Task](../../../SKILL.md#resume-a-saved-task), [Integrity Verification](../../../SKILL.md#integrity-verification), and [Repository Drift](../../../SKILL.md#repository-drift) as the sole validation and authorization authorities.

Only after validation and explicit current authorization may CDF enter [Execution Progress](../../../references/execution-progress.md), creating or updating the separate sidecar at the recorded path. Never append authorization or runtime status to this saved task, and never edit its canonical Scope Lock or Approval Record. A request only to inspect, review, summarize, or validate the task authorizes no code change or progress mutation.
