# Workflow 02: Report Planning

## Goal

Turn confirmed code-audit findings into a report request plan. Request only reports that answer real business-path questions.

## Planning Principles

- Start from the confirmed core success action.
- Build funnels from reachable code paths, not screen names.
- Split multi-feature apps into separate funnels.
- Mark invalid funnel assumptions explicitly.
- Explain the purpose of every requested report.
- Separate required reports from optional reports.
- Re-request old reports when dimensions, date ranges, filters, or metric basis do not match the audit.

## From Success Action to Funnel

1. Identify the feature entry.
2. Identify required user actions.
3. Identify permission gates.
4. Identify loading/result/container states.
5. Identify true completion.
6. Exclude conditional and branch-only pages.
7. Add previous-path and next-path reports for ambiguous pages.

## Branch Splitting

Create separate report groups for onboarding, each core feature, permission recovery, paywall source, ad interruption, result exploration, settings/history, and secondary tools.

## Firebase / GA4

Required first:
- Dashboard overview.
- Events list.
- Pages and screens.
- First launch funnel.
- Core feature funnel.
- Path exploration around result pages, paywalls, and ad wrappers.
- Retention / cohorts.

Optional:
- Audiences.
- Conversions / key events.
- DebugView checks for new event validation.

## AdMob / Ad Monetization

Required first:
- Ad unit summary.
- Date + ad unit.
- Country + ad unit.
- Ad format summary.
- Country + ad format.
- Mediation source.

Metrics: requests, matched requests, impressions, clicks, CTR, eCPM, fill/show rate, match rate, estimated revenue.

## App Store Connect / Google Play

Required first:
- Source type / acquisition source.
- Territory / country.
- Product page views.
- First-time downloads.
- Redownloads.
- Conversion rate.
- Sales, refunds, proceeds, subscription events.
- App version if available.

## Adjust / AppsFlyer

Required first:
- Media source / network.
- Campaign / adgroup / adset / creative.
- Country.
- Cost, installs, sessions, events.
- Ad revenue, IAP revenue, cohort revenue.
- Retention, ROAS, fraud/rejected installs if available.

## RevenueCat / IAP

Required first:
- Paywall views if available.
- Trial starts.
- Initial purchases.
- Renewals.
- Cancellations.
- Refunds.
- Active subscriptions.
- Package performance.
- Entitlements.
- Cohorts, MRR, LTV if available.

## Crashlytics / Sentry

Required first:
- Crash-free users.
- Crash-free sessions.
- Fatal and non-fatal issues.
- Affected users.
- Version, device, OS.
- Trends around core flows and release windows.

## Re-export Rules

Ask for a new export when:
- The date range does not match other sources.
- Daily rows do not sum to totals.
- Dimensions omit required platform, country, campaign, ad unit, or version fields.
- Revenue currency or basis is unclear.
- Old reports mix cohort and activity dates.
- The report cannot distinguish source path, package, ad position, or result state needed by the audit.

## Report Checklist Output

| Priority | Platform | Report name | Report type | Configuration | Date range | Purpose | Notes |
|---|---|---|---|---|---|---|---|
