# Internal Task Handoff

Load only for approved **Save as Task**. CDF is the user entry; [CDTask](../components/cdtask/COMPONENT.md) only compiles and persists. The current internal contract is `cdf-cdtask/v2`; compatibility is defined in [Resume](resume.md#legacy-and-version-policy).

## Entry boundary

Requirement meaning, repository evidence, risk, technical approach, Scope Lock, verification strategy and rollback must be settled before approval. Require an exact displayed Approval Summary or explicitly approved full plan, an Approval Record selecting **Save as Task**, and a current CDF save-drift preflight. Neither a raw PRD nor an unapproved/read-only draft is valid compiler input.

CDF assembles the full plan from already-approved material, checks it against what the user saw, then freezes it before handing it to CDTask. This transcription cannot introduce decisions or verification obligations. For S, mechanically map approved `Change`, `Will Not Change`, `Verify` into the full plan and retain the original approval. Formatting needs no second approval; new meaning does.

## Development Plan

Preserve these eleven headings in this exact order, with nonempty content:

1. Requirement Understanding — outcomes, decomposition, constraints and non-goals.
2. Evidence Summary — facts, sources, inferences, assumptions, gaps; retrievable source revisions/content digests for write targets, protected areas and read-only dependencies. Include dirty/untracked content baselines, not only Git status.
3. Risk Gate Result — level, six dimensions, mandatory signals, reverse check and rationale.
4. Scope Lock — the sole canonical `cdf-scope/v1` block.
5. Technical Approach — the approved implementation direction.
6. Implementation Plan — ordered work, dependency reasons and approved write areas.
7. Risks — actual risks and mitigations.
8. Rollback Plan — specific rollback; `None` only if genuinely inapplicable.
9. Acceptance Criteria — same-order, verbatim projection of the complete canonical array.
10. Verification Strategy — approved local and product checks, not executed results.
11. Next Action — the selected **Save as Task** action.

At L include affected modules and regression/rollback detail; at XL include architecture, data/API/state flow and the explicit approved phase. These requirements document existing decisions, not compiler authority to make new ones.

## Three distinct meanings

- **Product Acceptance Criteria:** `cdf-scope/v1.acceptance_criteria` remains the sole product authority. No compiler addition, deletion, weakening, rewriting, merging or splitting. AC-001, AC-002, etc. are derived one-based indices into that immutable array, not new criteria.
- **Task Verification:** local delivery checks entailed by approved Technical Approach and Verification Strategy. A local task can be verified while final product acceptance is still unverified. No new product commitment, architecture choice or write permission can enter through these checks.
- **Acceptance Contribution Mapping:** each task references at least one canonical AC ID through `contributes_to`. This establishes contribution, not satisfaction. Every AC also has planned product verification and contributing task coverage.

Example: the API task may be verified using its approved response/tests and unblock the form task. The login-form AC passes only after the complete login integration is actually checked. Never use task verification as substitute evidence for that product result.

## Wire format and preservation

The [persistence reference](../components/cdtask/references/persistence.md) defines the v2 Markdown envelope. JSON-compatible YAML metadata and JSON fenced structured sections keep validation standard-library-only. Scope retains its v1 schema and exact text, using eight single-line JSON arrays in fixed order in the v2 wire profile. Choose that representation **before approval**; never reserialize an already-approved block to satisfy a parser. Unsupported representations require explicit review/re-approval if byte preservation cannot be maintained.

The canonical block has a version line then these eight fields:

```yaml
Scope-Lock-Version: cdf-scope/v1
in_scope: ["Approved outcome"]
out_of_scope: []
non_goals: []
assumptions: []
stop_conditions: []
will_change: ["Approved area"]
will_not_change: []
acceptance_criteria: ["Observable product result"]
```

All entries are nonempty strings; `in_scope` and `acceptance_criteria` must be nonempty arrays. Other arrays may be empty. Hard exclusions and partial-approval remainders grant no positive scope. Preserve all approved payloads verbatim; derived mappings cannot replace them.

Verification Strategy is one JSON fenced array of `{id, kind, description}` objects. `kind` is `task` or `product`. IDs are unique; descriptions specify approved checks and expected results. Mechanical IDs and grouping may be assigned during transcription without changing meaning. Any missing local/product verification obligation that requires a new decision returns to planning. Task definitions reference these checks rather than creating free-form new requirements. When one already-approved check establishes both local delivery and product acceptance (for example a saved S task), it may have separate task/product IDs with the same approved check description. These are role mappings, not two new obligations or a requirement to run the same physical check twice; evidence may reference the same actual receipt with the respective check IDs.

The Acceptance Criteria projection is one JSON fenced array exactly equal to the canonical array. Human Approval fields remain semantically the same; their v2 serialization is defined in persistence. Preserve the exact user statement and summary, not a reconstructed approval.

## Preflight and validation

Carry absolute Workspace (or explicit `Unavailable`), branch, commit, worktree state and relevant status entries. Preserve Git XY characters, sort by path then status, and include affected read-only evidence sources. `[]` means no relevant changes; `["Unavailable"]` requires an explanation in Evidence Summary. Dirty alone is not material drift.

CDF compares current evidence with the approved baseline immediately before saving. `matched` requires notes `none`; `non-material-drift` requires concrete notes. Material or unexplained drift returns to CDF planning before compilation. CDTask validates/transcribes these findings; it does not independently replan.

Validate approval provenance, exposed meaning, exact Scope Lock/plan/approval text, partial exclusions, phase boundaries, write scopes, full bidirectional acceptance coverage and approved checks. Mechanical validation cannot determine whether prose introduces hidden scope. Missing or contradictory authority blocks save.

A compiler-owned grouping or missing-field defect may be repaired without changing approved meaning. A new interface, dependency, behavior, write area, product criterion, architecture decision or verification obligation requires a refreshed plan and renewed approval, even if the Scope Lock wording stays unchanged. Preserve the old package as evidence.
