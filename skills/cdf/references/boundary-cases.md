# CDF Boundary Cases

Use these cases when a small-looking request, risk signal, approval reply, partial approval, or resumed task sits close to a control boundary. Reuse the decision pattern, not the example's product details.

## Case 1: A signal is evidence, not the final risk

### Request

> Make the disabled sign-in button a lighter gray. It should be a one-line change.

### Variant A: bounded shared use

Evidence shows the page passes a local color override to a shared button. The override is used only on the sign-in page, does not change disabled-state logic, has visual regression coverage, and can be reverted in one file.

```text
Signal: shared component usage
Evidence obligation: inspect the shared contract and known consumers
Risk floor: Level M because a shared contract is involved
Final risk: Level M
```

The shared-component signal prevents a superficial Level S classification, but it does not force Level L. Impact and blast radius remain bounded, uncertainty is low, and rollback is straightforward.

### Variant B: cross-cutting token

Evidence instead shows the color comes from a global token used by sign-in, registration, checkout, and administration flows. The proposed edit changes every consumer and several state variants.

```text
Signals: shared token; conditional state styling
Risk floor: Level M
Final risk: Level L
Reason: verified cross-cutting behavior and broad user-path impact
```

Level L follows from the combined impact and blast radius, not from a rule that any signal hit is automatically Level L.

## Case 2: Bounded analytics or configuration need not be Level L

### Request

> Add the existing `help_opened` event to the local help drawer.

Evidence confirms that the event schema already exists, the call adds no user identifiers, no downstream business metric depends on this occurrence, the change is isolated to one drawer, and disabling the call is trivial.

```text
Signals: analytics; shared event contract
Final risk: Level M
```

If evidence showed that the event drives billing, experiments, executive reporting, consent behavior, or a public data contract, those added impact and sensitivity dimensions could support Level L. Treat a small configuration change the same way: inspect consumers and rollback, then classify the observed impact.

## Case 3: Ambiguous acknowledgement is not action approval

### Context

CDF displayed a Development Plan and canonical Scope Lock, then asked the user to choose **Execute Now** or **Save as Task**.

### Reply

> ok, continue

The reply acknowledges the plan but does not unambiguously select execution or persistence.

### Correct response

```markdown
Before continuing, please choose what the approval authorizes:

1. **Execute Now** — implement only the displayed Scope Lock.
2. **Save as Task** — compile and persist the approved work; do not implement it now.

If neither action is acceptable, describe the required plan or Scope Lock changes instead of approving it.
```

Remain at the approval gate. Do not implement or enter the internal task compiler until both the approved scope and next action are clear. The user need not name an internal contract.

## Case 4: Evidence conflict, block, then partial approval

### Request

> Update the admin help copy, and hide the export entry from users without export permission.

Candidate scope items:

- `Update the admin help copy to the confirmed text.`
- `Hide the export entry from users without export permission.`

Repository sources disagree about the permission identifier and whether managers must always see the entry. This conflict changes behavior and acceptance criteria.

### Blocked result

```markdown
Status: BLOCKED
Provisional risk floor: Level L

Evidence Conflict:
- Frontend condition: `canExport`
- API contract: `reports.export`
- Permission configuration: `report_export`
- Product rule: managers always see the export entry

Please identify the authoritative rule. I cannot finalize the permission plan
or Scope Lock while this conflict changes the intended behavior.
```

The provisional floor preserves safe controls while evidence is unresolved; it is not a claim that a signal alone determines the final risk.

### User narrows the request

> Leave permission behavior out; keep only the help-copy change.

This is a scope revision, not approval of the earlier plan. Reinspect and classify the copy-only subset. If it is independently safe, display a new canonical Scope Lock and request explicit approval.

```yaml
Scope-Lock-Version: cdf-scope/v1
in_scope:
  - Update the admin help copy to the confirmed text.
out_of_scope:
  - Change export-entry visibility.
non_goals: []
assumptions:
  - The confirmed help copy supplied by the user is final.
stop_conditions:
  - The copy change requires permission or conditional-rendering changes.
will_change:
  - Admin help copy.
will_not_change:
  - Export visibility.
  - Permission and authorization behavior.
acceptance_criteria:
  - The admin help area displays the approved text.
```

All eight arrays must exist. Empty arrays are valid; do not invent filler text merely to make a field non-empty.

If the user approves this subset, the Approval Record must identify it as partial approval and keep the permission item visibly unapproved. **Save as Task** may hand off only the approved-subset Scope Lock; no task may be created for the remainder.

The plan above remains the only canonical Scope Lock. Record the partial outcome as a projection without copying that block:

```markdown
## Partial Approval Result

Approval Type: partial

### Approved Items
- Update the admin help copy to the confirmed text.

### Unapproved Items
- Hide the export entry from users without export permission.

### Canonical Approved Scope
Scope-Lock-Version: cdf-scope/v1
```

The approved item exactly matches canonical `in_scope`; the unapproved item remains verbatim and is protected by canonical exclusions. The projection creates no second scope authority.

## Case 5: New scope discovered after approval

### Context

The approved plan changes a local API adapter. During execution or task compilation, evidence shows safe completion also requires a new database column and a public response-field change.

### Correct behavior

Stop. Do not treat these as incidental implementation details. Return to CDF planning to:

1. inspect the data and API impact;
2. reassess risk and rollback;
3. update the Development Plan and canonical Scope Lock;
4. request renewed approval for the revised boundary.

Neither previous approval nor a persisted task authorizes the new data or contract scope.

## Case 6: Resume metadata differs, but drift must be assessed

### Context

A saved task records commit `abc123` plus a stable list of relevant `Source-Worktree-Changes`. The current workspace is at `def456`, and its relevant status list may also differ.

Do not blindly execute the task, but do not declare material drift from the commit mismatch alone. Compare the intervening changes with the task's evidence, assumptions, planned write scope, shared contracts, acceptance criteria, and verification strategy.

- Documentation-only changes outside the task boundary may be non-material.
- A changed target API, renamed module, altered permission rule, invalidated assumption, or conflicting implementation is material.
- When drift is material, return to planning, update the Scope Lock as needed, and obtain renewed approval.
- When drift is demonstrably non-material, record the check and continue inside the existing approved scope.

The saved Approval Record still does not authorize execution. Only an explicit CDF continue request followed by successful contract, integrity, scope, assumption, and drift validation creates the current-turn Resume Authorization Record. Inspecting, reviewing, summarizing, or validating the task creates no such record and authorizes no code changes.

See [Task Handoff](task-handoff.md) for the complete resume and drift rules.
