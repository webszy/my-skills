# Workflow 05: Optimization

## Goal

Produce a prioritized optimization plan grounded in code paths, validated data, and measurable risk.

## Priority Rules

- **P0**: High confidence, high impact, low or controlled risk, or fixes data/UX issues blocking diagnosis.
- **P1**: Meaningful impact with moderate uncertainty, requires experiment or release coordination.
- **P2**: Lower impact, longer-term, or dependent on better instrumentation.

## Optimization Areas

### Ad Strategy

Tune ad unit placement, format mix, mediation source, country rules, ad loading, cooldown, and trigger timing. Do not optimize CTR without checking misclick risk and user path impact.

### First Launch

Reduce unnecessary steps before the first business screen. Separate language, onboarding, permissions, app open ads, and launch paywalls in analysis.

### Interstitial Frequency

Check whether interstitials appear before value, inside core flows, immediately on result pages, or before save/export/restore. Prefer cooldowns, excluded screens, and post-value triggers.

### Rewarded Value Exchange

Use rewarded ads where the benefit is explicit, callback-based, and tied to one clear unlock or quota extension.

### Paywall Timing

Move paywalls toward moments with demonstrated intent or value exposure. Track source and next path. Avoid blocking essential understanding before value is visible unless testing proves it works.

### Subscription Entitlements

Align paywall claims with code entitlements. Clarify ad removal, batch operations, quality/export limits, quotas, and rewarded bypasses.

### Onboarding

Shorten mandatory onboarding, separate education from permissions, and measure onboarding start, completion, skip, and downstream feature entry.

### Permissions

Request permissions at feature-time when possible. Track prompt view, allow, deny, settings open, and recovery success.

### Event Tracking

Add P0 events for core success, permission, paywall source, ad trigger/show/close, purchase result, and result state. Add P1/P2 events for deeper branch and segmentation analysis.

### A/B Testing

Define one hypothesis per test, one primary metric, guardrail metrics, eligibility rules, duration, rollback condition, and reporting dimensions.

### Remote Config

Prefer Remote Config for ad switches, cooldowns, paywall frequency, country/version/user segment rules, review state, and experiment assignment when code already supports it.

### Risk and Rollback

Every optimization should include user-experience risk, revenue risk, data-quality risk, review risk, misclick risk, and rollback path.

### Version Plan

Separate no-release config changes, tracking-only releases, UX releases, monetization releases, and SDK upgrades.

## Output Table

| Priority | Area | Problem | Recommendation | Expected impact | Risk | Rollback |
|---|---|---|---|---|---|---|
