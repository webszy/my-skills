---
name: cdf
description: Use when the user invokes cdf, $cdf, cdf:, or controlled-development-flow, or when Codex or Claude needs to clarify vague requirements before implementation, modify code, implement features, fix bugs, refactor modules, change UI or backend behavior, update APIs, adjust data flows, or work in high-risk areas such as database schema, billing, subscriptions, IAP, reports, authentication, permissions, scheduled jobs, queues, production configuration, or architecture design.
---

# cdf: Controlled Development Flow

Use this skill to turn vague or risky requests into clear, scoped, evidence-based, and verifiable implementation work, then choose the lightest safe workflow based on task risk.

Core principle:

> Small changes should be fast. Risky changes should be controlled.

## Requirement Gate

Read `references/requirement-gate.md` when the request is vague, underspecified, high-risk, or asks for a spec, PRD, diagnosis, decision memo, or research brief.

That reference contains the full gate: ask classification, definition card, gap list, suggested defaults, clarification response templates, spec and implementation brief outputs, acceptance patterns, examples, and the single authoritative high-risk list.

If the requirement is unclear, output the clarification response from that reference and stop before target existence check or risk classification.

## Quick Decision Flow

1. Run Requirement Gate.
2. If the requirement is unclear, output a clarification response and stop before implementation.
3. If the user accepts suggested defaults, treat those defaults as explicit assumptions and continue.
4. Locate the target or search for existing similar targets.
5. Show concise Requirement Understanding and Requirement Decomposition to the user.
6. Make an initial risk classification.
7. Inspect code evidence appropriate to the risk.
8. Finalize or upgrade the risk level; the stricter rule always wins.
9. Use the matching workflow.

If the task is urgent or described as a hotfix, keep the analysis compact, but do not bypass Level L or Level XL approval gates for high-risk areas.

## Classification Decision Tree

Use this same decision tree twice:

- Initial classification: run it after target check, requirement understanding, and decomposition, using only known information. If evidence is missing for a branch, keep the branch tentative and inspect before downgrading.
- Final classification: run it again after evidence inspection, using confirmed evidence. The final result controls the workflow.

This decision tree and Classification Rules are the same source of truth. If they appear to differ, use the highest risk level indicated by either section and update the reasoning instead of choosing the lower level.

Choose the first matching branch:

1. If the task requires a new service, new module, major refactor, major data-flow redesign, architecture design, or phased rollout, classify as Level XL.
2. Else if it touches any High-Risk Areas item in `references/requirement-gate.md`, classify as Level L unless the item itself requires Level XL.
3. Else if a High-Risk Areas item is mentioned only because of local display/style/copy, classify as Level L unless evidence proves no runtime, workflow, compliance, or business impact.
4. Else if it changes a scoped interaction, form behavior, validation, local state, small API call, loading state, empty state, filter, or one page flow, classify as Level M.
5. Else if it is copy, style, spacing, icon size, static UI, or a single-component visual tweak and all Level S conditions are true, classify as Level S.
6. If evidence points to multiple branches, use the highest risk branch. If evidence is insufficient for final classification, continue inspecting or ask the user; do not downgrade by assumption.

## Bundled References

For Requirement Gate details, read `references/requirement-gate.md` when the request is vague, underspecified, high-risk, or asks for a spec, PRD, diagnosis, decision memo, research brief, or implementation brief.

For Level M, Level L, and Level XL tasks, read `references/karpathy-guidelines.md` before producing a plan, design, or implementation. Use it to prevent generic planning, overbuilding, scope creep, unrelated edits, and weak verification.

For Level S tasks, do not read this reference by default. After the target check/search, read it for Level S only if at least one objective signal is true:

- The target file, component, symbol, style token, or copy key is shared by two or more modules, routes, packages, or features.
- The target symbol or copy key has more than five references or call sites.
- The change touches more than one file, package, or module.
- The change affects shared UI primitives, design tokens, shared styles, generated code, or common configuration.
- A previous attempt in the current task failed, produced the wrong target, or required rework.
- The located target path or symbol name overlaps a Level L or Level XL risk area; in that case, reclassify before continuing.

This reference is bundled with cdf, so it does not require the user to install `karpathy-guidelines` separately. Treat it as supporting guidance; cdf remains responsible for risk classification, approval gates, and final execution flow.

If `references/karpathy-guidelines.md` is unavailable, do not block the workflow. Continue using the cdf rules as the source of truth, and mention that the supporting reference was unavailable.

## Target Existence Check

Before editing a task that modifies an existing target, first verify that the target exists in the codebase.

Locate the relevant component, function, route, API, configuration, asset, or copy before deciding how to change it. This applies to every risk level, including Level S.

If the task appears to create a new module, service, top-level workflow, or architecture, do not rely on the wording alone. Perform a quick search for any existing module, service, workflow, route, package, or architecture with the same name or purpose before entering the new-target path. If a similar target exists, treat the request as modifying or extending that target unless the user confirms otherwise. Do not finalize risk at this step; continue through visible requirement understanding, visible decomposition, and evidence inspection before final classification.

If the requested target does not exist, cannot be located, or cannot be uniquely identified:

- Pause before editing.
- Tell the user what was searched.
- Explain what could not be found or why the match is ambiguous.
- Ask whether the intended action is to create a new target, modify a different target, or correct the request.

Do not silently create a missing target when the user asked to modify an existing one.

## Requirement Understanding

After target existence check, restate the actionable request before planning, classifying, or editing. Keep it visible and concise; simple Level S tasks may use one line.

## Requirement Decomposition

Before risk classification, break the request into the relevant impact areas. Show only what matters, and use the High-Risk Areas list in `references/requirement-gate.md` when deciding whether anything escalates.

## Initial Risk Classification

Perform an initial classification into Level S, Level M, Level L, or Level XL only after target existence check, requirement understanding, and requirement decomposition.

Use risk first, not file count.

If decomposition reveals any high-risk area, initially classify as Level L or Level XL even when the visible change looks small.

The initial classification must be visible to the user together with requirement understanding and decomposition.

## Evidence-Based Thinking

After the initial risk classification, think from concrete code evidence before producing a plan.

For Level M, Level L, and Level XL tasks, do not output a modification plan or design until you have inspected relevant files or search results and can name concrete evidence, such as:

- Route, page, component, or module files that were found.
- Existing symbols, functions, props, fields, schemas, API types, or configuration keys.
- Current data source and rendering path.
- Relevant call sites or references.
- Confirmed constraints from the codebase.

Before planning, separate:

- Confirmed facts from files or search results.
- Assumptions that still need validation.
- Risk boundaries that affect the workflow level.

If evidence is insufficient, continue inspecting or pause and ask the user. Do not produce a generic plan based only on the user request.

For Level S tasks, this thinking may stay brief and usually does not need to be shown as a plan, but the agent must still inspect enough code or search results to locate the exact target and avoid inventing targets, style sources, copy locations, or facts.

## Final Risk Classification

After evidence inspection, finalize or upgrade the risk level before planning or editing.

If evidence reveals a higher-risk area than the initial classification, reclassify immediately and switch to the stricter workflow.

Examples:

- A visible UI field that depends on payment, IAP, ROI, report, permission, or database logic must upgrade to Level L.
- A scoped change that requires a new service, new module, major data-flow redesign, or phased rollout must upgrade to Level XL.
- If evidence is insufficient to decide whether the task is high-risk, keep inspecting or pause and ask the user.

## Risk Levels

The levels below are the outcomes of Final Risk Classification. When examples, the decision tree, and classification conditions disagree, use the highest risk level.

## Shared Approval Sections

All pre-edit user-visible outputs must include Requirement Understanding and Requirement Decomposition. Level L and Level XL approval outputs also need Confirmed Evidence, Open Assumptions, Risks, and Test Plan / Test Strategy.

### Level S: Direct Edit

Use Level S for simple, low-risk changes:

- Text, copy, labels, placeholders, and empty-state wording.
- Button colors, spacing, icon sizes, and simple CSS.
- Static UI adjustments.
- Simple display or hide logic with no business impact.
- Single-component visual tweaks.

Rules:

- Show concise Requirement Understanding, Requirement Decomposition, and Risk Classification before editing.
- Edit directly.
- Do not ask for confirmation.
- Do not create a long plan.
- Keep the change minimal.
- Do not refactor surrounding code.
- Do not introduce new dependencies.
- Summarize changed files, verification performed, and relevant manual checks after editing.

### Level M: Brief Plan Then Edit

Use Level M for normal scoped changes:

- Add or modify a form field.
- Change a page interaction.
- Add a filter.
- Modify a small API call.
- Change validation or local state behavior.
- Add a simple loading or empty state.
- Adjust one page flow.
- Touch a small number of files without data, money, security, or production-risk impact.

Rules:

- After target, requirement, decomposition, classification, and evidence checks, provide a short evidence-backed plan first.
- Include Requirement Understanding and Requirement Decomposition in the visible compact plan.
- If the requirement is clear and low-risk, proceed without waiting for confirmation.
- Ask only when the requirement is ambiguous.
- Before classifying a task as Level M, confirm that it does not touch any Level L high-risk area. If it does, upgrade it to Level L, produce the full Level L approval template using the evidence already gathered, and wait for approval before editing.
- Keep changes focused.
- Do not modify unrelated files.
- Summarize changed files, behavior, verification performed, and relevant manual checks after editing.

For Level M, use a compact format before editing:

```md
I’ll treat this as Level M.

Understanding:
- ...

Requirement Decomposition:
- ...

Evidence:
- ...

Risk:
- ...

Plan:
1. ...
2. ...

I’ll proceed because this is scoped and does not touch high-risk areas.
```

### Level L: Approval Required

Use Level L for changes to existing systems that do not require architectural redesign, but touch high-risk areas:

- Any High-Risk Areas item in `references/requirement-gate.md`, unless the item requires Level XL.
- Multi-module changes with unclear risk.

Rules:

- Do not edit code immediately.
- First understand the requirement and inspect the relevant context.
- Identify change scope and what will not change.
- Treat `Will not change` as required. If the boundary cannot be stated, continue inspecting or ask the user instead of proposing implementation.
- Identify affected modules.
- Propose an implementation plan.
- Explain risks.
- Provide a test plan.
- Wait for explicit user approval before editing.

Required output before editing combines the shared approval block with Level L-specific sections:

```md
I’ll treat this as a Level L change because it affects high-risk logic.

Expand Shared Approval Sections here.

## Change Scope

Will change:
- ...

Will not change:
- ...

## Affected Modules

- ...

## Implementation Plan

1. ...
2. ...
3. ...

Please confirm before I modify the code.
```

### Level XL: Design Required

Use Level XL when the task requires designing from scratch or large-scale restructuring of existing systems:

- New module or backend service.
- Major refactor.
- Full pipeline design.
- Permission, billing, subscription, report, or sync system design.
- App Store Connect API integration.
- Advertising statistics pipeline.
- Cross-service orchestration.
- Large data model design.
- Any task requiring phased implementation.

Rules:

- Do not edit code immediately.
- Create or update a design first.
- Define data models, APIs, state flow, risks, rollout, and test strategy as relevant.
- Break implementation into phases with explicit phase boundaries.
- Wait for explicit approval before implementation. Approval covers only the design and phases described in the approval request.
- For large or risky designs, ask for per-phase approval by default. If the user gives broad approval, complete only the currently described phase before reporting progress and asking whether to continue.
- If evidence during implementation invalidates a design assumption, changes the data flow, expands the affected modules, or makes a phase materially different from the approved design, stop and update the design for approval before continuing.
- Do not mix architecture design and large implementation in one uncontrolled step.

Required output before editing combines the shared approval block with Level XL-specific design sections:

```md
I’ll treat this as a Level XL change because it affects architecture/module design.

## Goal

...

## Current Context

...

Expand Shared Approval Sections here.

## Proposed Design

...

## Data Model / API / State Flow

...

## Implementation Phases

### Phase 1
...

### Phase 2
...

Please confirm the design before implementation.
```

## Classification Rules

Apply these rules during both initial and final classification. Initial classification happens after requirement understanding and requirement decomposition. Final classification happens after evidence inspection.

These rules and the Classification Decision Tree share priority over the examples in Risk Levels. If a task matches a low-risk example but fails any low-risk condition or matches a higher-risk decision-tree branch, use the higher risk level.

Classify as Level S only when all are true:

- The change is visual, copy, style, or static UI behavior.
- It does not touch any High-Risk Areas item in `references/requirement-gate.md`.
- Any mention of a high-risk area is proven to be purely local display/style/copy with no runtime, workflow, compliance, or business impact.

Classify as Level M when the change is scoped and reversible, and it does not touch any High-Risk Areas item.

Before finalizing Level M classification, check High-Risk Areas. Any overlap forces Level L, even when the change looks small or touches only one API call.

Classify as Level L when any High-Risk Areas item is affected, even if the file count is small.

Classify as Level XL when the task requires architecture, a new module, a new service, a major data-flow change, or phased implementation.

## Reclassification During Implementation

If implementation reveals a higher-risk area than originally classified, stop editing immediately.

- Level S or Level M must upgrade to Level L if high-risk logic is discovered.
- Level L must upgrade to Level XL if architecture, a new service, phased rollout, or major data-flow redesign becomes necessary.
- Explain what new evidence caused the upgrade.
- Re-enter the stricter workflow from its required output template using the evidence already gathered; do not merely append a warning to the old plan.
- If edits were already made before the discovery, disclose them, do not continue editing, and do not revert user or unrelated changes unless the user approves or the revert is required to leave the workspace coherent.
- Workspace coherence means the agent's own partial edits should not leave obvious syntax errors, type errors, broken imports, failed formatting caused by the edit, or tests/builds that fail solely because the edit is half-applied. If such breakage is discovered, first make the smallest repair or revert necessary to restore the pre-upgrade baseline, report it, and then wait for the stricter approval. Do not use coherence repair to implement additional scope or continue the high-risk change.
- Wait for the required approval before any further Level L or Level XL edits.

## Anti-Overplanning Rule

Do not over-plan Level S tasks.

For simple UI, copy, and style changes, do not output long requirement analysis, proposals, design documents, implementation phases, risk matrices, or confirmation requests.

Requirement understanding and decomposition may be one concise line when the task is simple.

Anti-overplanning limits the amount of text shown to the user, not the need to inspect the exact target. A Level S edit still requires enough file or search evidence to know where the change belongs.

Make the smallest safe change and provide a short final summary.

This rule applies only to Level S. It does not apply to Level L or Level XL; their planning, risk, and approval outputs are mandatory.

## Minimal Change Rule

Always prefer the smallest change that satisfies the request.

Do not:

- Rewrite unrelated code.
- Refactor without being asked.
- Introduce dependencies unless necessary.
- Change file structure unnecessarily.
- Alter behavior outside the requested scope.
- Rename variables unnecessarily.
- Reformat entire files unnecessarily.
- Change public APIs unless explicitly requested by the user or required by the approved plan.

## Confirmation Rule

For Level L and Level XL tasks, do not modify code until the user gives explicit approval.

Strong approval examples:

- Confirm
- Approved
- Proceed
- Go ahead
- 确认执行
- 开始修改
- 按方案改
- 可以，改吧
- 没问题，执行
- OK, proceed
- 那就这样吧

Treat approval as valid only when the user's reply clearly authorizes code changes for the stated scope and does not ask a follow-up question, raise a concern, add a conflicting requirement, or narrow the scope.

Acknowledgements and vague replies are not approval. This includes "OK" or "好的" when they plausibly mean "I understand", and hedged replies such as "sounds good", "why not", "I guess", "そうですね", or "pourquoi pas". When uncertain, ask for a specific confirmation such as: `Please reply "Approve implementation" or "确认执行" if you want me to modify the code.`

For non-English replies, use the same rule: the reply must clearly authorize the proposed code changes. If cultural or linguistic ambiguity remains, ask for explicit confirmation.

If the user gives partial or conditional approval, execute only the approved subset. Update the scope, risks, and test plan for that subset before editing. If the condition changes high-risk scope, ask for confirmation again.

If the user responds to an approval request with a new requirement instead of clear approval, do not treat it as approval and do not edit. Mark the previous approval request as stale, incorporate the new requirement, and rerun target check, requirement understanding, decomposition, evidence inspection, and final risk classification. Then produce an updated Level L approval request or Level XL design request as needed.

If the new requirement merely narrows the proposed scope, treat it as partial or conditional approval only for the narrowed subset, update the scope, risks, and test plan, and proceed only when the remaining authorization is explicit. If the new requirement expands scope, changes architecture, touches a new high-risk area, or conflicts with the previous plan, request approval again for the revised plan.

Invalid approval examples:

- What do you think?
- Explain more.
- Is this risky?
- Any other plan?
- Continue analyzing.
- Whatever.
- Up to you.
- 你觉得呢？
- 还有别的方案吗？
- 风险大吗？
- 随便。
- 好的。
- そうですね。
- Pourquoi pas.

## Final Response Rule

After code changes, include:

```md
Changed:
- ...

Summary:
- ...

Verification:
- ...

Traceability:
- ...
```

List the verification that was actually performed. If no test or check was run for a Level S or Level M task, say so explicitly and provide the most relevant manual verification steps.

For Level L and Level XL, choose verification that matches the changed risk area. Schema changes need migration/schema validation or targeted persistence checks. Billing, subscription, IAP, revenue, cost, ROI, and report changes need calculation-path or fixture-based checks. Auth and permission changes need authorized and unauthorized path checks. Scheduled jobs, queues, retries, and idempotency changes need job-path or retry/idempotency checks. Production configuration changes need configuration validation or environment reference checks.

If the ideal verification cannot be run, explain why and run the strongest available static or targeted check, such as affected call-site inspection, type/lint/build check, configuration validation, or targeted reference search.

Verification must pass before the final response is issued. If verification fails and the fix is within the approved scope, fix it and re-run the relevant verification. If the fix would expand scope, touch a new high-risk area, or alter the approved design, stop and request approval before editing further. If the failure cannot be fixed in the current turn, report the failure and its cause.

For Level L and Level XL, also include:

```md
Regression:
- ...

Risks / Manual checks:
- ...
```

For Level L and Level XL, `Traceability` is required. If the workspace is a git repository, actively query and include the current branch and latest commit, such as with `git branch --show-current` and `git log -1 --oneline`. If a release version, deployment version, ticket, or timestamp is already available from the workflow, include it too. If git or other traceability data is unavailable, write `Unavailable` with the reason. Do not invent missing traceability data.
