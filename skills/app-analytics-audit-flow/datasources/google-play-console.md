# Google Play Console

## Role

Google Play store analytics, Android acquisition, conversion, retention, vitals, crashes, ANR, revenue, subscriptions, and refunds.

## Use When

Use Google Play Console for Android store funnel, source/country/device analysis, store listing conversion, Android vitals, and Play revenue/subscription checks.

## Key Reports

| Priority | Report | Dimensions | Metrics | Purpose | Notes |
|---|---|---|---|---|---|
| P0 | Store listing visitors | Date, country, source | Visitors | Store demand | Compare with acquisitions |
| P0 | Acquisitions | Date, country, source, device | Acquisitions | Install baseline | Different from Firebase/MMP |
| P0 | Conversion rate | Country, source | Conversion | Store listing quality | Separate from UA quality |
| P1 | Retention | Cohort, country | Retention | Repeat usage | Availability varies |
| P0 | Android vitals | Version, device, OS | Crashes, ANR | Store health impact | Can affect store performance |
| P0 | Revenue | Product, country | Revenue, refunds | Monetization | Separate gross/net if possible |
| P0 | Subscriptions | Product, event | Starts, renewals, cancels | Subscription lifecycle | Align with IAP platform |

## Key Metrics

- Store listing visitors and acquisitions describe store behavior.
- Conversion rate describes store listing effectiveness.
- Android vitals includes crash/ANR quality signals.
- Revenue and refunds need currency and basis checks.

## Common Pitfalls

- Play Console metrics differ from Firebase and MMP metrics.
- Android vitals can affect store performance.
- Store listing conversion must be separated from UA quality.

## Required Questions

- Which countries, sources, and devices are important?
- Were listing assets, price, or version changed?
- Are vitals above bad-behavior thresholds?
- Are revenue, subscription, and refund reports included?

## Output Checklist

- Visitors, acquisitions, and conversion rate.
- Country/device/source breakdowns.
- Android vitals.
- Revenue/subscription/refund reports.
