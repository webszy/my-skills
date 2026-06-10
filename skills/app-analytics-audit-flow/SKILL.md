---
name: app-analytics-audit-flow
description: Code-first audit workflow for mobile app analytics, growth, advertising monetization, attribution, subscription, store, and stability analysis. Use when the user wants to analyze, audit, optimize, or build reports for a mobile app using Firebase, GA4, AdMob, App Store Connect, Google Play Console, Adjust, AppsFlyer, RevenueCat, Adapty, Crashlytics, Sentry, CSV exports, funnels, retention, paywalls, ads, onboarding, or app growth data.
---

# App Analytics Audit Flow

Use this skill to plan and analyze mobile app growth, monetization, subscription, attribution, store, and stability data from a code-first basis.

Core rule:

> Audit the real app paths from code before building reports or interpreting funnels.

## First Response

When the user asks to analyze or optimize a mobile app with analytics data, do not start by asking for Firebase screenshots or generic funnel exports.

First determine:

- App category and business model.
- Current optimization goal.
- Available data sources.
- Whether source code can be scanned.
- The likely core success action.
- Recent release, price, metadata, ad strategy, Remote Config, or UA budget changes.

If code can be scanned, provide or adapt `prompts/codex-code-audit.md` before requesting final reports.

If code is unavailable, ask for real app flow descriptions, screenshots, or recordings; mark funnels as provisional until code or implementation evidence is available.

## Workflow

1. Clarify the app goal and available data sources.
2. Audit code or parse an existing code-audit report.
3. Identify confirmed business paths and invalid assumptions.
4. Define the true core success action.
5. Plan required reports from confirmed paths.
6. Validate uploaded CSVs, screenshots, or platform exports.
7. Analyze acquisition, activation, retention, monetization, subscription, country/channel quality, stability, and release effects.
8. Output P0/P1/P2 optimization, experiment, event tracking, and next data collection plans.

Use the staged procedures in `workflows/` for detailed execution.

## Non-negotiable Rules

- Do not build funnels from screen names alone.
- Do not treat SDK pages as product pages.
- Do not treat result container pages as completion unless code confirms completion.
- Do not force conditional pages or feature branches into the main funnel.
- Do not mix Firebase revenue, AdMob revenue, store revenue, and subscription revenue without checking metric basis.
- Do not treat App Store downloads and Firebase `first_open` as the same metric.
- Do not output secrets, API keys, tokens, certificates, private keys, ad unit IDs, or bundle identifiers from source code.
- Mark any code-unconfirmed conclusion as uncertain or needing human confirmation.

## Module Map

- `workflows/01-code-audit.md`: Use for code audit scope, evidence tables, uncertainty rules, and path discovery.
- `workflows/02-report-planning.md`: Use to turn confirmed app paths into Firebase, ad, store, attribution, subscription, and stability report requests.
- `workflows/03-data-validation.md`: Use when the user uploads CSVs, screenshots, or platform exports.
- `workflows/04-analysis.md`: Use for final business analysis structure, chart/table choices, and risk notes.
- `workflows/05-optimization.md`: Use for P0/P1/P2 recommendations, experiments, Remote Config plans, rollback, and release planning.

- `prompts/codex-code-audit.md`: Reusable prompt for scanning app code and producing a factual audit report.
- `prompts/codex-report-planning.md`: Reusable prompt for producing a report checklist from a code-audit result.
- `prompts/codex-event-tracking-review.md`: Reusable prompt for reviewing existing and missing analytics events.
- `prompts/codex-remote-config-review.md`: Reusable prompt for reviewing Remote Config, feature flags, and A/B capability.

- `datasources/firebase.md`: Firebase / GA4 report guidance.
- `datasources/admob.md`: AdMob report guidance.
- `datasources/app-store-connect.md`: App Store Connect report guidance.
- `datasources/google-play-console.md`: Google Play Console report guidance.
- `datasources/adjust.md`: Adjust report guidance.
- `datasources/appsflyer.md`: AppsFlyer report guidance.
- `datasources/revenuecat.md`: RevenueCat report guidance.
- `datasources/applovin-max.md`: AppLovin MAX report guidance.
- `datasources/crashlytics.md`: Crashlytics stability guidance.

- `templates/`: Reusable output templates for data inventory, report checklists, funnel plans, final analysis, optimization plans, and event tracking plans.
- `rules/`: Code-first, funnel validation, monetization, and risk checklist rules.
- `examples/`: A photo recovery case and a sample final report shape.

## Output Shape

For analysis work, prefer concise tables for:

- Data inventory.
- Code audit findings.
- Screen meaning map.
- Valid and invalid funnels.
- Report checklist.
- Metric definitions and revenue basis.
- Optimization priorities.
- Event tracking and A/B test plans.

When enough data is available, structure the final result as:

1. Data inventory and confidence level.
2. Business goal and core success action.
3. Operating summary.
4. Acquisition.
5. Activation and core funnel.
6. Retention.
7. Ad monetization.
8. Subscription / IAP.
9. Country / channel quality.
10. Stability, if relevant.
11. Data risks and missing instrumentation.
12. P0 / P1 / P2 optimization plan.
13. A/B test plan.
14. Event tracking plan.
15. Next data collection plan.
