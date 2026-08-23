# CDF Risk Classification

Read this file before finalizing a CDF risk level. The signal checklist identifies affected surfaces; the six dimensions determine the final level.

## Classification Rule

Assess:

1. **Impact** — cosmetic, behavioral, data, financial, access, operational, or architectural.
2. **Blast radius** — one local target, a bounded shared surface, many flows, or multiple systems.
3. **Reversibility** — trivial revert, bounded rollback, coordinated rollback, or irreversible/migrated state.
4. **Uncertainty** — complete evidence, bounded assumptions, important gaps, or material conflict.
5. **Sensitivity** — ordinary UI/code, business measurement, user data, money, auth, security, privacy, or compliance.
6. **Coordination** — one local change, shared-owner coordination, rollout/operations, or multi-system phases.

Use the highest level justified by the combined dimensions and applicable risk floors. A `HIT` is evidence, not a universal Level L rule.

## Signal Floors and Escalation

| Signal | Bounded case | Higher-risk case |
|---|---|---|
| ESC-01 shared surface | Level M may be valid when usage and regression scope are small, known, and reversible | Level L for broad/global behavior or many materially affected flows |
| ESC-02 conditional behavior | Level M for bounded local state rendering with no entitlement or access meaning | Level L for permission, entitlement, feature-release, or user-specific contract impact |
| ESC-03 persistent data | Normally at least Level L | Level XL for schema migration, backfill, major lifecycle redesign, or hard-to-reverse state |
| ESC-04 money or access | Normally at least Level L | Level XL for subsystem redesign, migration, or coordinated multi-system change |
| ESC-05 analytics or metrics | Level M may be valid for one additive, non-sensitive event using an established contract | Level L for material business meaning, reports, attribution, privacy, revenue/cost logic, or changed metric definitions |
| ESC-06 background/caching/event work | Level M may be valid for bounded cache use with known invalidation and local rollback | Level L for jobs, queues, retries, idempotency, webhooks, consumers, or persistent operational effects; XL for redesign |
| ESC-07 quality/sensitive concerns | Level M may be valid for bounded i18n, accessibility, or observability use with established patterns | Level L for security, privacy, compliance, or broad accessibility/operational impact |
| ESC-08 configuration | Level M may be valid for bounded application configuration with local effect and easy reversal | Level L for deployment, environment, production, or release impact; XL for coordinated platform redesign |
| ESC-09 external/release surface | Level M may be valid for bounded use of an existing stable integration or delivery path | Level L for changed external contracts or meaningful release impact; XL for a new service or major contract redesign |
| ESC-10 architecture | Not a bounded S/M signal | Level XL for a new subsystem/service, architecture decision, migration, major data-flow redesign, phased rollout, or multi-system coordination |
| ESC-11 evidence gap | Floor to the lowest plausible risk supported by what remains unknown | Level L or `BLOCKED` when a bounded plan cannot safely exclude sensitive or cross-cutting impact |
| ESC-12 evidence conflict | Use the higher plausible level while resolving the conflict | `BLOCKED` when the conflict changes implementation meaning, scope, acceptance, ownership, or safety |

Several bounded signals together may produce Level L even when none would do so alone. Consider their interaction, not just each row in isolation.

## Level S Reverse Check

Level S is valid only when every row passes:

| ID | Required condition |
|---|---|
| S-01 | Exactly one identified, non-shared target |
| S-02 | Copy, spacing, color, icon size, or other static presentation only |
| S-03 | No behavior, state, API, data, contract, configuration, or generated-artifact change |
| S-04 | Acceptance and verification are local to the target |
| S-05 | The change is explicit, trivially reversible, and requires no adjacent cleanup |
| S-06 | Evidence is sufficient and consistent; every relevant signal is `CLEAR` |

Record `PASS`, `FAIL`, or `UNKNOWN` with evidence. A `FAIL` requires Level M or higher. An `UNKNOWN` follows the Evidence Gap path.

All six rows must be `PASS` to use the Level S Fast Path. Assess them as reasoning; report only the aggregate result on the fast path's `Reverse Check` line.

## Level M Reverse Check

Level M is valid only when every row passes:

| ID | Required condition |
|---|---|
| M-01 | One bounded feature, flow, shared surface, configuration use, analytics event, or integration use |
| M-02 | Inputs, outputs, callers, state changes, failure behavior, and affected consumers are known |
| M-03 | No persistent-data migration, money/auth/security/privacy/compliance change, architecture decision, or broad contract redesign |
| M-04 | Any shared, configuration, analytics, or external signal is explicitly bounded and covered by regression checks |
| M-05 | Rollback is simple or bounded and verification is specific |
| M-06 | Evidence is sufficient and consistent for the claimed boundary; no higher floor applies |

Record `PASS`, `FAIL`, or `UNKNOWN` with evidence. A `FAIL` requires Level L or XL. An `UNKNOWN` follows the Evidence Gap path.

## Evidence Gap

When evidence is insufficient:

1. name the exact unknown and the decision it affects;
2. inspect the smallest additional source likely to resolve it;
3. ask a focused user question only when repository evidence cannot answer it;
4. if it remains unknown, use the lowest plausible risk as the floor and add an explicit assumption and stop condition;
5. use `BLOCKED` when no safe plan or bounded Scope Lock can be produced.

Never convert missing evidence into an unstated assumption.

## Evidence Conflict

When relevant evidence conflicts:

1. cite the conflicting sources and affected decision;
2. seek an authoritative source or explicit user decision;
3. use the higher plausible risk while investigating;
4. stop as `BLOCKED` if the conflict changes implementation meaning, scope, acceptance, ownership, or safety and remains unresolved.

A separable non-conflicting subset may proceed only through a new plan, its own canonical Scope Lock, and explicit approval.

## Final Record

For Level S the classification is internal reasoning, surfaced only as `Reverse Check: PASS` on the Fast Path Plan. For Level M and above, the Risk Gate Result must contain:

- final level;
- evidence for all six dimensions;
- each mandatory signal's `CLEAR`, `HIT`, or `UNKNOWN` result;
- the M Reverse Check result when applicable;
- evidence gaps or conflicts and their resolution;
- a concise rationale for the final level.

For Level L/XL, include material interactions, rollback difficulty, and coordination requirements.
