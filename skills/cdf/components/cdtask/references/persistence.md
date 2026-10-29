# Persistence and Integrity — cdf-cdtask/v2

Load only before approved save, read-back or saved-task integrity validation. CDTask receives the approved frozen package and CDF's drift conclusion; it does not plan or grant approval. The read-only standard-library [validator](../../../scripts/validate_cdf.py) implements the wire profile and hash functions. Run `--describe` for authoritative mechanical field names.

## Destination

Use the requested path, resolving relative paths against absolute Workspace. Otherwise use `<Workspace>/_cdtask/YYYY-MM-DD-<slug>.md`, with the actual local save date and a title/first-scope-derived safe slug. If workspace is unavailable, require an explicit absolute destination. Create only necessary parents and the task document. For default collisions append `-2`, etc.; explicit collisions require a distinct destination or explicit replacement authority. Never silently overwrite an old task or its history.

## Markdown envelope

Use UTF-8 without BOM, LF line endings and a final LF. Frontmatter begins/ends with `---`. Each field occupies one line `key: <JSON value>`; this is a narrow YAML 1.2 profile, not a general YAML parser. Strings are double-quoted JSON strings, booleans are JSON booleans, arrays are JSON arrays. No aliases, comments, duplicate keys or non-finite numbers. Unsupported input fails clearly; never silently normalize approved content.

Required metadata (also available through `--describe`):

```yaml
task_contract: "cdf-cdtask/v2"
handoff_type: "approved-tasking"
status: "tasking_ready"
source: "cdf"
approval_state: "approved"
risk_level: "Level M"
workspace: "/absolute/workspace"
source_branch: "main"
source_commit: "<actual commit or Unavailable>"
source_worktree_state: "clean"
source_worktree_changes: []
save_drift_preflight: "matched"
save_drift_notes: "none"
scope_lock_sha256: "<computed SHA-256>"
approval_record_sha256: "<computed SHA-256>"
definition_sha256: "<computed SHA-256>"
created_at: "<ISO-8601 with timezone>"
approval_basis: "summary"
phase_scoped: false
```

Risk supports S/M/L/XL. Traceability supports explicit `Unavailable` with its reason in Evidence Summary. Scope and approval records remain authoritative, not metadata labels. `tasking_ready` means definition readiness only.

After a document title, these `##` sections occur exactly in order:

1. CDF Resume Contract
2. Approval Summary — only for `approval_basis: "summary"`
3. Development Plan — the eleven headings in [Task Handoff](../../../references/task-handoff.md)
4. Approved Phase Boundary — only when `phase_scoped: true`, required for XL
5. Approval Record
6. Partial Approval Result — only for partial approval
7. Dependency Graph
8. Task Definitions
9. Acceptance Mapping
10. Scope Guard
11. Future CDF Execution Constraints
12. Compilation Gate Result
13. Save Verification

JSON sections use exactly one `json` fence and no additional prose outside it. Approval Summary uses one `text` fence, longer than any embedded fence, preserving exact displayed text and action question. Headings inside fences are quoted data, never section boundaries. Full-plan approval preserves that displayed plan directly without an invented summary. Do not add a second canonical scope block.

CDF Resume Contract is exactly:

```json
{"resume_path": "CDF only", "execution_authorized": false, "progress_created_by_save": false}
```

Approval Record is a JSON object with `user_statement` (exact), `context` (timestamp/turn), `action: "Save as Task"`, `type` (`full`, `conditional`, `partial`), `approved_items` (exact canonical in_scope array), `conditions` (canonical assumptions/stop conditions), `unapproved_items` (verbatim remainder protected by canonical exclusions). These fields preserve the existing approval meaning; no field can manufacture approval provenance.

Approved Phase Boundary is JSON `{phase, scope, ends_at, explicitly_deferred}`: scope exactly matches canonical in_scope and all deferred items are protected. Partial Approval Result is JSON `{approved_items, unapproved_items}` exactly projecting the Approval Record, not another Scope Lock.

Task/graph/mapping/guard sections follow [Task Templates](task-templates.md). Save Verification is JSON `{ "status": "verified", "verified_at": "<actual read-back time>" }` only after the provisional read-back described below. All sections, including receipts and traceability, are immutable after save succeeds.

## Exact digest definitions

All hashes are SHA-256 over actual bytes, stored as 64 lowercase hex characters. Do not claim to have computed a hash without executing hashing code.

| Field | Exact bytes |
|---|---|
| scope_lock_sha256 | The sole Scope Lock fence payload, starting at `Scope-Lock-Version: cdf-scope/v1`, eight ordered arrays, exactly one trailing LF; no fences or trailing whitespace |
| approval_record_sha256 | Literal `## Approval Record` plus LF, then the exact JSON fence payload with exactly one trailing LF; no fence delimiters |
| definition_sha256 | **All saved document bytes**, excluding only the complete `definition_sha256: ...` line in top-level frontmatter, including that line's LF |

The definition hash includes all other metadata and digests, approval basis, plan, scope, approval, partial/phase boundaries, task definitions, graph, acceptance mapping, constraints, compilation result and final save receipt. There is no mutable appendix or other exclusion. The digest cannot include itself. v2 Approval Record serialization is new; never apply it to v1 payloads.

Runtime `task_document_sha256` additionally hashes the entire final task file, including its definition digest. It is a binding check established at execution, **not** a replacement for the definition baseline already established at save.

Self-contained hashes detect accidental or one-sided tampering. Anyone able to replace content **and** hashes can forge consistency. SHA-256 is not an authorization signature, cannot independently prove human approval, and cannot replace trusted conversation evidence or pre-save text comparison.

## Save transaction

1. Require valid Save approval and semantic Scope Guard. Compare frozen approved plan, displayed basis, Scope Lock and Approval Record against the draft verbatim. Reject mismatch, ambiguity, duplicate canonical scope or unsupported wire format; do not repair approval text.
2. In a private temporary draft, assemble the complete document, temporarily using digest placeholders and a provisional save receipt. Compute and fill scope/approval hashes. Write/read the provisional bytes and compare all immutable material and mappings against the handoff. Do not report ready.
3. After that actual read-back succeeds, set Save Verification to verified with its actual timestamp. This still is an unsaved candidate. `python3 <skill>/scripts/validate_cdf.py <draft> --draft-hashes` computes all three candidate hashes without treating any existing baseline as valid. Fill the digest fields in the draft; because the full hash includes the other two digests, compute again after filling scope/approval values. Fill `definition_sha256` last.
4. Validate the completed candidate normally; write final bytes to the resolved destination without clobbering an existing task. Reopen **that exact destination**, compare its complete bytes with the candidate, recompute all three hashes with the normal validator, and compare the approved payloads again. Recheck all semantic invariants and source traceability.
5. Report READY and the absolute path only after final read-back succeeds. Any failure is `BLOCKED: persistence-failure`; preserve the failed artifact for diagnosis but do not treat it as resumable. Do not modify the final receipt after hashing. A post-save edit invalidates the definition.

`--draft-hashes` is a calculation tool for newly approved, unsaved candidates. It never writes, approves, migrates or repairs an existing task. On first Execute Saved Task and every resume, use **normal validation** against persisted hashes. A missing/mismatched digest stops execution; never run the draft-hash route to bless current contents.

## Validator CLI

```bash
python3 <skill>/scripts/validate_cdf.py <task.md>
python3 <skill>/scripts/validate_cdf.py <task.md> --progress <task.md.progress.yaml> --snapshot <current-content-sha256>
python3 <skill>/scripts/validate_cdf.py <task.md> --progress <current> --previous-progress <prior>
python3 <skill>/scripts/validate_cdf.py --describe
```

Exit 0 means mechanical structure/integrity checks succeeded (or hashes were calculated in explicit draft mode); exit 1 returns machine-readable `errors[{code,message}]`. Neither result declares semantic PASS, authorizes execution or proves source evidence true. `review_required` always lists remaining approval/scope/drift/evidence checks. No validator command writes any file. Use the same normal validator on save read-back, first execution and resume. v1 returns `legacy-reapproval`; follow [compatibility](../../../references/resume.md#legacy-and-version-policy), not hash repair.
