# Workflow 04: Analysis

## Goal

Convert validated data and code-audit findings into a business diagnosis and optimization-ready report.

## Analysis Areas

### Operating Summary

Summarize app category, business model, core success action, main revenue sources, data coverage, confidence level, and biggest constraints.

### Acquisition

Analyze source type, campaign/channel quality, country mix, cost, installs/downloads, conversion rate, organic vs paid, and store listing behavior.

### Activation / Core Funnel

Analyze launch path, onboarding completion, permission allow/deny, core feature entry, result view, true completion, paywall exposure, and ad interruption.

### Retention

Analyze cohort retention, returning users, feature repeat usage, subscription retention, and whether ad or paywall strategy may affect return behavior.

### Ad Monetization

Analyze ad revenue by date, ad unit, placement, format, country, network, eCPM, CTR, requests, fill, match, show rate, and code trigger location.

### Subscription / IAP

Analyze paywall views, package performance, trial starts, purchases, renewals, cancellations, refunds, active subscriptions, LTV, and entitlement behavior.

### Country / Channel Quality

Compare country/channel acquisition, activation, retention, monetization, refund, crash, and ROAS. Separate volume, quality, and profitability.

### Version / Release Impact

Compare metrics before and after releases, metadata changes, price changes, SDK changes, ad strategy changes, and event tracking changes.

### Remote Config Impact

Map metric changes to config changes where available. Separate no-release config effects from code-release effects.

### Stability

Analyze crash-free users/sessions, fatal/non-fatal issues, affected users, version/device/OS concentration, and whether crashes hit high-value flows.

## Data Risk Notes

Always state incompatible metrics, missing events, missing dimensions, short date ranges, unreconciled revenue bases, attribution gaps, and unverified funnels.

## Tables and Charts

Prefer:
- Data inventory table.
- Funnel conversion table.
- Revenue basis table.
- Country/channel quality table.
- Ad unit performance table.
- Paywall package table.
- Version comparison table.
- P0/P1/P2 priority table.
- Line charts for daily trends.
- Bar tables for country/ad unit/channel rankings.
- Funnel charts only for validated sequential paths.

## Report Structure

Use Markdown for most work. Use HTML only when the user asks for a deliverable dashboard or presentation-style report.

Recommended sections:
1. Executive summary
2. Data inventory
3. Business goal
4. Revenue basis
5. Acquisition
6. Activation / core funnel
7. Retention
8. Ad monetization
9. Subscription / IAP
10. Country / channel quality
11. Stability
12. Data risks
13. Optimization priorities
14. A/B tests
15. Event tracking plan
16. Next data collection
