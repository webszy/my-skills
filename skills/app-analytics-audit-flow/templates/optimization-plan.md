# Optimization Plan Template

## Priority Table

| Priority | Area | Problem | Recommendation | Expected impact | Risk | Rollback |
|---|---|---|---|---|---|---|
| P0 | Tracking | Core success is not tracked | Add completion event and result_state | Enables valid funnel | Requires release | Disable analysis until event exists |
| P1 | Ads | Interstitial appears before value | Move trigger after value or add cooldown | Better completion/retention | Revenue dip | Remote Config rollback |
| P2 | Paywall | Package source unknown | Add paywall_source/package params | Better paywall diagnosis | Low | Keep existing paywall |

## P0

Fix blockers to trustworthy analysis or high-impact revenue/user-flow issues.

## P1

Run experiments for likely improvements with moderate risk.

## P2

Add supporting diagnostics and longer-term refinements.

## Experiment Design

| Experiment | Hypothesis | Eligible users | Variant | Primary metric | Guardrails | Stop condition |
|---|---|---|---|---|---|---|

## Remote Config Plan

| Config | Current | Variant | Segment | Rollout | Rollback |
|---|---|---|---|---|---|

## Release Plan

- Tracking-only release.
- Monetization config release.
- UX flow release.
- SDK update release.
- Post-release monitoring window.
