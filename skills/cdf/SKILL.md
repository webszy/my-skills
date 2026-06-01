---
name: cdf
description: cdf, short for controlled-development-flow, is a risk-based development workflow for AI coding agents. Use when Codex or Claude needs to modify code, implement features, fix bugs, refactor modules, change UI or backend behavior, update APIs, adjust data flows, or work in high-risk areas such as database schema, billing, subscriptions, IAP, reports, authentication, permissions, scheduled jobs, queues, production configuration, or architecture design.
---

# cdf: Controlled Development Flow

Use this skill to choose the lightest safe workflow based on task risk.

Core principle:

> Small changes should be fast. Risky changes should be controlled.

## Bundled References

For Level M, Level L, and Level XL tasks, read `references/karpathy-guidelines.md` before producing a plan, design, or implementation. Use it to prevent generic planning, overbuilding, scope creep, unrelated edits, and weak verification.

For Level S tasks, reading this reference is optional; keep simple changes lightweight.

This reference is bundled with cdf, so it does not require the user to install `karpathy-guidelines` separately. Treat it as supporting guidance; cdf remains responsible for risk classification, approval gates, and final execution flow.

## Target Existence Check

Before editing a task that modifies an existing target, first verify that the target exists in the codebase.

Locate the relevant component, function, route, API, configuration, asset, or copy before deciding how to change it. This applies to every risk level, including Level S.

If the task is explicitly to create a new module, service, top-level workflow, or architecture, do not block on an existing-target lookup. However, perform a quick search for any existing module, service, workflow, or architecture with the same name or purpose to avoid duplication before entering the design workflow. Classify it as Level XL when it requires design or phased implementation, then enter the design workflow.

If the requested target does not exist, cannot be located, or cannot be uniquely identified:

- Pause before editing.
- Tell the user what was searched.
- Explain what could not be found or why the match is ambiguous.
- Ask whether the intended action is to create a new target, modify a different target, or correct the request.

Do not silently create a missing target when the user asked to modify an existing one.

## Evidence-Based Thinking

After the target existence check, think from concrete code evidence before producing a plan.

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

For Level S tasks, this thinking may stay brief, but the agent still must not invent targets or facts.

## Risk Levels

Classify the task before editing. Use risk first, not file count.

### Level S: Direct Edit

Use Level S for simple, low-risk changes:

- Text, copy, labels, placeholders, and empty-state wording.
- Button colors, spacing, icon sizes, and simple CSS.
- Static UI adjustments.
- Simple display or hide logic with no business impact.
- Single-component visual tweaks.

Rules:

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

- After target and evidence checks, provide a short evidence-backed plan first.
- If the requirement is clear and low-risk, proceed without waiting for confirmation.
- Ask only when the requirement is ambiguous.
- Before classifying a task as Level M, confirm that it does not touch any Level L high-risk area. If it does, upgrade it to Level L and switch to the Level L workflow immediately; do not continue with Level M's direct-edit path.
- Keep changes focused.
- Do not modify unrelated files.
- Summarize changed files, behavior, verification performed, and relevant manual checks after editing.

### Level L: Approval Required

Use Level L for changes to existing systems that do not require architectural redesign, but touch high-risk areas:

- Database schema or migrations.
- Destructive operations or data migration.
- Payment, billing, subscription, IAP, revenue, cost, or ROI logic.
- Report calculation or business metric logic.
- Authentication or permission logic.
- Scheduled jobs, sync tasks, queues, retries, or idempotency.
- Production configuration, deployment configuration, or environment variables.
- Multi-module changes with unclear risk.

Rules:

- Do not edit code immediately.
- First understand the requirement and inspect the relevant context.
- Identify change scope and what will not change.
- Identify affected modules.
- Propose an implementation plan.
- Explain risks.
- Provide a test plan.
- Wait for explicit user approval before editing.

Required output before editing:

```md
I’ll treat this as a Level L change because it affects high-risk logic.

## Requirement Understanding

...

## Confirmed Evidence

- ...

## Open Assumptions

- ...

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

## Risks

- ...

## Test Plan

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
- Break implementation into phases.
- Wait for explicit approval before implementation.
- Do not mix architecture design and large implementation in one uncontrolled step.

Required output before editing:

```md
I’ll treat this as a Level XL change because it affects architecture/module design.

## Goal

...

## Current Context

...

## Confirmed Evidence

- ...

## Open Assumptions

- ...

## Proposed Design

...

## Data Model / API / State Flow

...

## Implementation Phases

### Phase 1
...

### Phase 2
...

## Risks

...

## Test Strategy

...

Please confirm the design before implementation.
```

## Classification Rules

Classify as Level S only when all are true:

- The change is visual, copy, style, or static UI behavior.
- There is no API change.
- There is no database change.
- There is no business logic change.
- There is no production configuration, data, infrastructure, money, security, scheduled-task, permission, or business-critical runtime impact.

Classify as Level M when the change is scoped and reversible, and it does not affect high-risk data, money, security, reports, production configuration, or scheduled execution.

Before finalizing Level M classification, check the Level L high-risk list. Any overlap forces Level L, even when the change looks small or touches only one API call.

Classify as Level L when any high-risk area is affected, even if the file count is small.

Classify as Level XL when the task requires architecture, a new module, a new service, a major data-flow change, or phased implementation.

## Anti-Overplanning Rule

Do not over-plan Level S tasks.

For simple UI, copy, and style changes, do not output requirement analysis, proposals, design documents, implementation phases, risk matrices, or confirmation requests.

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

Valid approval examples:

- Confirm
- Approved
- Proceed
- Go ahead
- 确认执行
- 开始修改
- 按方案改
- 可以，改吧
- 没问题，执行
- OK
- 好的
- 那就这样吧

If the user's reply semantically means agreement and does not ask a follow-up question, raise a concern, or add a conflicting requirement, treat it as valid approval.

Do not treat vague resignation or non-committal replies such as "whatever", "随便", or "up to you" as approval for Level L or Level XL changes. Ask for explicit confirmation instead.

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

## Final Response Rule

After code changes, include:

```md
Changed:
- ...

Summary:
- ...

Verification:
- ...
```

List the verification that was actually performed. If no test or check was run for a Level S or Level M task, say so explicitly and provide the most relevant manual verification steps.

For Level L and Level XL, perform at least one concrete verification before final response. Prefer the most relevant automated test; if that is not available, run a meaningful static check such as targeted reference search, type/lint/build check, configuration validation, or inspection of affected call sites. Do not leave Level L or Level XL verification empty. Verification must pass before the final response is issued. If verification fails, fix the issues first, or explicitly report the failure and its cause to the user before proceeding.

For Level L and Level XL, also include:

```md
Regression:
- ...

Risks / Manual checks:
- ...
```

## npx skills Packaging

This skill is intended to live inside a repository under:

```text
skills/cdf/
```

For publishing and install command examples, read `references/install.md` only when the user asks about packaging, release, or installation through `npx skills`. If that file is unavailable in the installed environment, use this repository's README installation command as the fallback.
