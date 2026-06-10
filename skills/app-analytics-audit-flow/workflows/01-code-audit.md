# Workflow 01: Code Audit

## Goal

Produce a factual map of the app's real business paths before requesting or interpreting analytics reports.

## Inputs

- App source code or a prior code-audit report.
- App category, business model, and optimization goal.
- Known analytics, ad, attribution, subscription, store, or stability SDKs.

## Outputs

- Screen meaning map.
- Launch path.
- Core feature paths.
- Permission paths.
- Ad trigger rules.
- Paywall trigger rules.
- Entitlement map.
- Analytics event inventory.
- Remote Config / feature flag capability map.
- Version / release context.
- Uncertainty list.

## Audit Scope

Scan app entry points, routers, navigation coordinators, screens, feature controllers, permission managers, ad managers, purchase managers, entitlement logic, analytics wrappers, config services, and version files.

## Screen Meaning Audit

Do not infer business meaning from a class or route name alone. For each screen, identify previous screens, next screens, user actions, completion conditions, and whether the screen is a product screen, SDK screen, wrapper screen, branch screen, loading state, result container, or true completion page.

| Screen / Class | Business meaning | First-time required | Core-flow required | Previous screens | Next screens | File path | Method / evidence | Confidence | Notes |
|---|---|---:|---:|---|---|---|---|---|---|

## Launch Path Audit

Trace cold start, first-time user, returning user, onboarding, language selection, home/tab selection, app open ads, launch paywalls, and fallback paths.

| Step | Screen / event | Trigger condition | First-time user | Returning user | Failure / skip path | File path | Method | Confidence |
|---:|---|---|---:|---:|---|---|---|---|

## Core Feature Path Audit

Separate each feature. Do not merge unrelated branches into one funnel.

| Feature | Step | Screen / event | User action | Success condition | Failure / rejection path | File path | Method | Confidence |
|---|---:|---|---|---|---|---|---|---|

## Permission Path Audit

Identify where permissions are requested, whether they are onboarding requirements or feature-time requirements, and whether denial blocks the core flow.

| Permission | Requested where | Trigger timing | Allow path | Deny path | Prompt page | File path | Method | Confidence |
|---|---|---|---|---|---|---|---|---|

## Ad Trigger Audit

Audit App Open, Interstitial, Rewarded, Native, Banner, mediation wrappers, cooldowns, excluded screens, callback paths, and layout shift risk.

| Ad type | Trigger screen | Trigger action | Blocks core flow | Close / reward callback | Frequency control | File path | Method | Confidence |
|---|---|---|---:|---|---|---|---|---|

## Paywall Trigger Audit

Audit source screens, auto popups, user-triggered paywalls, discount pages, close paths, purchase success paths, and whether the original action continues.

| Entry screen | Trigger action | Paywall screen | Auto popup | Close path | Purchase success path | Continues original action | File path | Method | Confidence |
|---|---|---|---:|---|---|---:|---|---|---|

## Pro / VIP Entitlement Audit

Map free user restrictions, Pro/VIP benefits, ad removal, usage limits, rewarded-ad unlocks, package claims, and restore behavior.

| Entitlement | Free user | Pro user | Unlockable by ad | Has usage limit | Code location | Confidence |
|---|---|---|---:|---:|---|---|

## Analytics Event Audit

List existing events and missing events. Check `source`, `ad_type`, `ad_position`, `package`, `result_state`, `is_new_user`, country, version, and custom screen naming.

| Event name | Trigger screen | Trigger timing | Parameters | File path | Method | Useful for funnel? | Confidence |
|---|---|---|---|---|---|---|---|

## Remote Config Audit

Identify ad switches, paywall switches, frequency controls, country rules, version rules, user segment rules, experiment assignment, review-state config, default values, and no-release adjustability.

| Config key | Default value | Controls | Remote configurable | No-release change? | File path | Confidence |
|---|---|---|---:|---:|---|---|

## Version / Release Audit

Find app version, build number, relevant release files, and whether recent ad, paywall, analytics, or core-flow changes can be mapped to releases.

| Item | Finding | File path | Confidence |
|---|---|---|---|

## Uncertainty Rules

- Use `confirmed` only when code directly proves the finding.
- Use `likely` when navigation or naming strongly suggests it but code evidence is incomplete.
- Use `uncertain` when evidence is weak or indirect.
- Write `Cannot confirm from code; needs human confirmation` when code cannot prove the business meaning.
- Do not output secrets, tokens, certificates, ad unit IDs, bundle identifiers, or private keys.

## Hard Rules

- Do not guess business meaning from page names.
- Do not treat SDK pages as product pages.
- Do not force branch pages into the main funnel.
- Do not treat result containers as success unless completion is confirmed.
- Do not include permission pages in main funnels unless code proves they are required.
