# Requirement Gate

Read this reference when a development request is ambiguous, underspecified, or sensitive enough that a wrong assumption could change the implementation, risk level, scope, or acceptance criteria. The gate belongs to the requirement-understanding stage of [CDF](../SKILL.md); it does not replace repository inspection, risk classification, planning, Scope Lock, approval, or verification.

## Contents

- Ask classification
- Definition card
- Gaps and minimal questions
- Suggested defaults
- Evidence gaps and conflicts
- Risk-sensitive clarification
- Outputs and acceptance criteria

## Ask classification

Classify the request lightly before deciding what must be clarified:

1. **Delivery** — create or change a feature, page, API, component, configuration, document, or other concrete deliverable.
2. **Diagnosis** — find the cause of a symptom or discrepancy.
3. **Decision** — choose among options using stated constraints and tradeoffs.
4. **Research** — explore or synthesize a topic before deciding whether to build anything.

Do not force every request into implementation. Diagnosis, decision, and research requests may end with their requested artifact. If they become development requests, return to the full CDF flow before changing code or saving an implementation task.

## Definition card

When meaning is unclear, restate the current understanding in a compact card:

- **One-line definition:** what changes, for whom or which system, and why.
- **Goal:** the observable outcome or changed state.
- **Actor / system:** the affected user, role, module, service, page, or workflow.
- **Scope:** known inclusions and exclusions.
- **Current behavior:** what happens now, with its evidence source when known.
- **Expected behavior:** what should happen instead.
- **Inputs:** relevant files, designs, examples, logs, APIs, data, or user-provided facts.
- **Constraints:** technical, business, security, compatibility, cost, performance, or timeline constraints.
- **Acceptance:** how completion can be verified.
- **Risk signals:** possible sensitivity, blast radius, irreversibility, uncertainty, or coordination needs.

Keep the card proportional to the request. A clear one-line copy change does not need a miniature PRD.

## Gaps and minimal questions

Before asking, list only gaps that can materially affect one or more of:

- requirement meaning;
- implementation direction or interface shape;
- data, state, permissions, or external behavior;
- risk classification;
- Scope Lock boundaries;
- acceptance or verification.

Ask no more than five questions in one round. Prefer either/or, multiple-choice, or short fill-in questions. When a safe recommendation exists, include it and explain the consequence briefly. Avoid open-ended prompts such as “What do you want?”

Do not seek perfect requirements indefinitely. The target is executable clarity backed by enough evidence to plan safely.

Example:

```markdown
## Questions

1. Which outcome is required?
   - A. Display the new value only
   - B. Let the user edit and persist it
   - Recommended: A, if persistence is not part of this request

2. What is the acceptance boundary?
   - A. This page only
   - B. Every consumer of the shared component
   - Recommended: A, implemented locally when repository evidence permits
```

## Suggested defaults

A suggested default must be:

- safe and reversible;
- narrow in scope;
- explicit rather than silently assumed;
- compatible with available repository evidence;
- free of hidden data-model, payment, permission, production-configuration, or external-contract changes.

Use defaults to accelerate a bounded decision, not to bypass a material ambiguity or approval. If the user says “use your recommendation,” “use the defaults,” or “按你的建议来,” record the stated defaults as explicit assumptions. Evidence inspection may still disprove them.

```markdown
## Suggested defaults

- Scope: V1 covers ... only.
- Data: Reuse existing fields; no persistence change.
- Interface: Reuse the current component/API contract.
- Acceptance: The change is complete when ...

Reply “use the defaults” to adopt these as assumptions for evidence inspection and planning.
```

## Evidence gaps and conflicts

Requirement clarification establishes intent; repository evidence establishes what the system actually does. Keep the two separate.

An **Evidence Gap** exists when a claim needed for planning cannot be verified from available sources. An **Evidence Conflict** exists when credible sources disagree in a way that changes behavior, scope, risk, or acceptance.

- Name the missing or conflicting claim.
- Record which sources were inspected.
- Explain which decision the gap or conflict prevents.
- Ask for the smallest authoritative input or propose a bounded inspection step.
- Do not silently choose the source that best fits the initial interpretation.
- Remain blocked when the uncertainty could materially change the plan or approval boundary.

An unavailable source is not automatically blocking. It is blocking only when the unverified claim is material and no safe bounded alternative exists.

## Risk-sensitive clarification

Use risk signals to decide what evidence and clarification are required. A signal is not the final risk level, and a signal hit does not automatically imply Level L.

Relevant signals include:

- shared components, UI primitives, design tokens, global state, or shared configuration;
- conditional rendering, feature gates, entitlements, permissions, authentication, or authorization;
- persistent data, schemas, migrations, deletion, backfills, caches, queues, retries, or idempotency;
- billing, subscriptions, pricing, revenue, cost, or materially interpreted analytics;
- user data, privacy, security, accessibility, localization, or compliance behavior;
- external APIs, webhooks, public contracts, asset delivery, release packaging, or production configuration;
- architecture, a new subsystem, cross-module data flow, phased rollout, or multi-system coordination;
- material evidence gaps or conflicts.

Classify risk from the combined evidence:

- **Impact:** what user or business behavior can change?
- **Blast radius:** how many paths, consumers, environments, or systems are affected?
- **Reversibility:** how safely and quickly can the change be undone?
- **Uncertainty:** how much of the relevant behavior is verified?
- **Sensitivity:** does it touch money, data, identity, security, privacy, or material reporting?
- **Coordination:** does safe delivery require migration, rollout, or multiple owners/systems?

A bounded shared component use, a small configuration change, or an analytics event may remain Level M when evidence shows limited impact and straightforward rollback. Cross-cutting behavior, persistent data, sensitive logic, material external contracts, or non-trivial rollback generally supports Level L. Architecture, new subsystems, migrations, major data-flow redesign, phased rollout, or multi-system coordination generally supports Level XL.

See [Boundary Cases](boundary-cases.md) for examples near these control boundaries.

## Relationship to CDF levels

- **Level S:** a clear, isolated, cosmetic or static local change with no behavioral or shared impact.
- **Level M:** bounded local behavior, a small shared-component change with verified consumers, bounded configuration, or bounded external-integration usage.
- **Level L:** cross-cutting behavior, persistent data, billing, identity, security, privacy, materially interpreted analytics, meaningful external contracts, or non-trivial rollback.
- **Level XL:** architecture, a new subsystem or service, migration, major data-flow redesign, phased rollout, or multi-system coordination.

Use the gate even for a small request when its meaning is unclear. Do not use defaults to make an incompletely understood sensitive request appear low risk.

## Post-clarification outcomes

- **Delivery:** continue to evidence inspection, risk classification, planning, `cdf-scope/v1`, and approval.
- **Diagnosis:** return evidence-backed findings and next checks. Continue to a fix only when the user authorizes a development request.
- **Decision:** return the decision or recommendation. Treat implementation of the selected option as a development request.
- **Research:** return the requested synthesis. Treat any resulting build request as a new development request.

A request to “turn this PRD into tasks” is still a delivery request. It must pass repository inspection, planning, canonical Scope Lock, and approval before CDF may enter its internal task-compiler component. See [Task Handoff](task-handoff.md).

## Requirement outputs

When the user asks for a requirement artifact, use only the sections that help resolve the actual request:

```markdown
# Requirement Spec

## Background and Goal
...

## Actor / Affected System
...

## Current and Expected Behavior
...

## In Scope
- ...

## Out of Scope
- ...

## Functional Requirements
- ...

## Non-functional Requirements
- Performance:
- Security and privacy:
- Compatibility:
- Reliability and observability:
- Accessibility:

## Data / API / State Impact
...

## Constraints and Edge Cases
- ...

## Acceptance Criteria
- ...

## Open Questions
- ...
```

This artifact records requirement meaning; it is not an approval record, Scope Lock, or execution authorization.

## Acceptance criteria

Criteria captured at the Requirement Gate clarify intent; they are not yet an approved authority. When CDF produces an approval-ready Development Plan, place the agreed wording in `cdf-scope/v1.acceptance_criteria`. That array is then the sole canonical acceptance source, and the plan's `### Acceptance Criteria` section must repeat it item for item, in the same order and exact wording.

Use observable checklist criteria for ordinary work:

```markdown
- [ ] The affected page displays ...
- [ ] Existing ... behavior remains unchanged.
```

Use Given / When / Then when state, permissions, flows, or API behavior make the precondition important:

```markdown
- Given ...
  When ...
  Then ...
```

Acceptance criteria must distinguish planned verification from completed verification. During planning, describe checks that should be run; after execution, report only checks actually run and their results.
