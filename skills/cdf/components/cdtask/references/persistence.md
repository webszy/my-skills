# Internal CDTask Persistence Contract

Read this reference before choosing a destination or writing a task document. It applies only to an approved `cdf-cdtask/v1` handoff selected by CDF's **Save as Task** path.

The component boundary, compilation workflow, and blocking semantics remain in [COMPONENT.md](../COMPONENT.md).

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
scope_lock_sha256: <64 lowercase hexadecimal characters>
approval_record_sha256: <64 lowercase hexadecimal characters>
created_at: <ISO-8601 timestamp>
---
```

`tasking_ready` is a task-definition state. It does not mean assigned, running, executed, reviewed, or verified, and it does not grant execution authority.

## Required Document Sections

Persist the sections below in this order. Copy approved planning material without changing its meaning. Sections marked verbatim must be copied exactly from the handoff.

1. **Title**
2. **CDF Resume Contract**
3. **Requirement Understanding**
4. **Evidence Summary**, including material evidence gaps recorded by CDF
5. **Development Plan**
6. **Approved Phase Boundary**, when applicable
7. **Canonical Scope Lock** — the complete `cdf-scope/v1` payload, byte for byte
8. **Approval Record** — verbatim
9. **Partial Approval Result**, when applicable, including the unapproved remainder verbatim
10. **Acceptance Criteria**
11. **Verification Strategy**
12. **Risks**
13. **Rollback Plan**, when applicable
14. **Dependency Graph**
15. **Dependency Data**
16. **Task Definitions**
17. **Scope Guard**
18. **Future CDF Execution Constraints**
19. **Compilation Gate Result**
20. **Save Verification**

The CDF Resume Contract must state:

```markdown
## CDF Resume Contract
- Resume Path: CDF only
- Task Contract: cdf-cdtask/v1
- Canonical Scope Lock: cdf-scope/v1
- Saved Definition State: tasking_ready
- Execution Authorized by This Document: No
- Source Workspace: <absolute path or Unavailable>
- Source Branch: <branch or Unavailable>
- Source Commit: <commit or Unavailable>
- Source Worktree State: <clean | dirty | Unavailable>
- Scope Lock SHA-256: <64 lowercase hexadecimal characters>
- Approval Record SHA-256: <64 lowercase hexadecimal characters>
```

The Compilation Gate Result must state the pre-save result and must not claim that implementation was reviewed or verified:

```markdown
## Compilation Gate Result
- Compilation Status: READY
- Task Count: <number>
- Scope Guard: passed
- Canonical Scope Lock Before Save: matched approved handoff
```

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
- workspace, branch, commit, worktree state, risk, integrity digests, and timestamp traceability are present;
- every required and applicable section is present;
- the persisted canonical Scope Lock payload is byte-for-byte identical to the handoff payload;
- the persisted Approval Record is identical to the received Approval Record;
- SHA-256 over each persisted canonical payload matches its respective frontmatter digest;
- partial-approval exclusions are preserved and have no corresponding task;
- task IDs are unique and every dependency resolves;
- the dependency graph is acyclic and matches Dependency Data and task fields;
- every task maps only to approved scope and acceptance criteria;
- Scope Guard is fully checked;
- Future CDF Execution Constraints and CDF-only resume rules are present;
- the document contains no claim that planned implementation verification was performed;
- the document does not grant execution authorization.

Only after this first pass succeeds, replace the provisional section with:

```markdown
## Save Verification
- [x] Frontmatter and traceability match the approved handoff.
- [x] Required sections are present.
- [x] Canonical Scope Lock matches byte for byte.
- [x] Approval Record and partial-approval material are preserved.
- [x] Scope Lock and Approval Record SHA-256 digests match.
- [x] Task IDs and dependency data are internally consistent.
- [x] Scope Guard and CDF-only resume constraints are present.
- [x] The document grants no execution authority.
- Verified At: <ISO-8601 timestamp>
```

Reopen the exact destination once more after recording Save Verification. Rerun every read-back check above against the final persisted bytes, including the frontmatter, both SHA-256 recomputations, canonical Scope Lock byte comparison, Approval Record comparison, partial exclusions, task IDs, dependency graph, Scope Guard, resume constraints, and authorization boundary. Also confirm every Save Verification item is checked and `Verified At` is populated. Only then return the absolute path and verified result to CDF and stop.

If any read-back check fails, do not report `READY`, do not treat the file as resumable, and do not continue into execution. Return `BLOCKED` with `Blocked-Reason-Class: persistence-failure`, the affected path, and a concise mismatch or I/O reason.

## Resume Validation Performed by CDF

The saved document is input to a later CDF continuation, never directly to CDTask or an executor. Before any work, CDF must:

1. validate the saved contract and document structure;
2. recompute and validate the persisted Scope Lock and Approval Record SHA-256 values;
3. compare current workspace, branch, commit, relevant worktree state, and repository evidence with the recorded source;
4. re-check assumptions and stop conditions;
5. verify that every task still matches the current code and approved Development Plan;
6. determine whether material drift invalidated risk, scope, acceptance criteria, phase boundaries, or approval;
7. obtain whatever current action authorization CDF requires before implementation.

Material drift or invalid authority returns to CDF planning and renewed approval. The saved document must never be executed blindly.
