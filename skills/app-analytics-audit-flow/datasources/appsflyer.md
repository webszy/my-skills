# AppsFlyer

## Role

Attribution and marketing analytics for aggregate performance, raw installs/events, cohorts, retention, ad revenue, cost, ROI/ROAS, media source, campaign, adset, ad, geo, and Protect360.

## Use When

Use AppsFlyer for user acquisition quality, paid vs organic split, campaign performance, cohort revenue, retention, ROAS, and fraud diagnostics.

## Key Reports

| Priority | Report | Dimensions | Metrics | Purpose | Notes |
|---|---|---|---|---|---|
| P0 | Aggregate performance | Media source, campaign, geo | Installs, events, revenue | UA summary | Separate organic/non-organic |
| P0 | Raw installs | Install rows | Installs | Attribution QA | Avoid exposing sensitive fields |
| P0 | Raw in-app events | Event rows | Events, revenue | Event forwarding QA | Confirm event names |
| P0 | Cohort | Install date, campaign | Revenue, retention, ROAS | LTV quality | Do not mix with activity reports |
| P1 | Retention | Media source, cohort | Retention | User quality | Align date basis |
| P0 | Ad revenue | Source, campaign, country | Ad revenue | Monetization by UA | Requires forwarding |
| P0 | Cost | Source, campaign | Cost, CPI | Spend basis | Currency check required |
| P0 | ROI / ROAS | Source, campaign, cohort | ROAS | Profitability | Verify revenue basis |
| P1 | Protect360 | Source, campaign | Fraud signals | Traffic risk | If available |

## Key Metrics

- Media source, campaign, adset, ad, and geo describe acquisition.
- Raw data is for QA; aggregate data is for summary.
- Cohort revenue differs from activity revenue.
- ROAS requires aligned cost and revenue.

## Common Pitfalls

- Raw and aggregate data have different grain and basis.
- Cohort and activity reports cannot be mixed casually.
- Organic and non-organic should be separated.
- Paid events and ad revenue events must be confirmed as forwarded.

## Required Questions

- Are ad revenue and IAP revenue forwarded?
- Which campaign hierarchy is available?
- Is cost connected?
- Are Protect360 or fraud reports available?
- Are reports cohort-based or activity-based?

## Output Checklist

- Aggregate performance.
- Raw installs.
- Raw in-app events.
- Cohort.
- Retention.
- Ad revenue.
- Cost.
- ROI/ROAS.
- Protect360 if available.
