# CDF Risk Classification

Read this file when the compact Level S Reverse Check in [SKILL.md](../SKILL.md#4-risk-gate) does not definitively pass. A confirmed Level S fast path does not load this reference. The signal checklist identifies affected surfaces; the six dimensions determine the final level.

## Classification Rule

Assess:

1. **Impact** — cosmetic, behavioral, data, financial, access, operational, or architectural.
2. **Blast radius** — one local target, a bounded shared surface, many flows, or multiple systems.
3. **Reversibility** — trivial revert, bounded rollback, coordinated rollback, or irreversible/migrated state.
4. **Uncertainty** — complete evidence, bounded assumptions, important gaps, or material conflict.
5. **Sensitivity** — ordinary UI/code, business measurement, user data, money, auth, security, privacy, or compliance.
6. **Coordination** — one local change, shared-owner coordination, rollout/operations, or multi-system phases.

Use the highest level justified by the combined dimensions and applicable risk floors. A `HIT` is evidence, not a universal Level L rule.

## Mandatory Signal Record

Record `CLEAR`, `HIT`, or `UNKNOWN` with evidence for every row:

| ID | Signal |
|---|---|
| ESC-01 | Shared components, primitives, tokens, styles, or global state |
| ESC-02 | Conditional rendering, feature gates, entitlements, permissions, or user-specific behavior |
| ESC-03 | Persistent data writes/deletes, schema, migration, backfill, or user data |
| ESC-04 | Billing, payments, subscriptions, pricing, authentication, or authorization |
| ESC-05 | Reports, analytics, telemetry, revenue/cost/ROI, or business metrics |
| ESC-06 | Cache, jobs, sync, queues, retries, idempotency, events, webhooks, or consumers |
| ESC-07 | Internationalization, accessibility, compliance, security, privacy, or observability |
| ESC-08 | Application, deployment, environment, or production configuration |
| ESC-09 | Third-party APIs, external contracts, static delivery, or release packaging |
| ESC-10 | Architecture, new module/service, major redesign, migration coordination, or phased rollout |
| ESC-11 | Evidence is insufficient to bound a higher plausible risk |
| ESC-12 | Evidence materially conflicts about scope, behavior, ownership, risk, or impact |

Signals are evidence and may impose a floor; use the highest level supported by the combined record and dimensions.

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

## Level S Boundary

The compact S Reverse Check in [SKILL.md](../SKILL.md#4-risk-gate) is the sole Level S authority. If this file was loaded because any S row failed, was unknown, or exposed a plausible non-S category, do not return to the fast path by silently clearing that evidence. Resolve the evidence and re-run the authoritative S check, or classify at Level M or above.

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

For a Level S fast path, classification is internal reasoning surfaced only as `Reverse Check: PASS`. When Level S is promoted to a full plan for `Save as Task`, its Risk Gate Result records `Final Level: S`, the six dimensions, a compact all-clear signal summary, `Reverse Check: S`, and a concise rationale. For Level M and above, the Risk Gate Result must contain:

- final level;
- evidence for all six dimensions;
- each mandatory signal's `CLEAR`, `HIT`, or `UNKNOWN` result;
- the M Reverse Check result when applicable;
- evidence gaps or conflicts and their resolution;
- a concise rationale for the final level.

For Level L/XL, include material interactions, rollback difficulty, and coordination requirements.
