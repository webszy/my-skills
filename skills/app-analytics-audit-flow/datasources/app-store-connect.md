# App Store Connect

## Role

Store analytics and revenue source for App Store acquisition, conversion, sales, subscriptions, refunds, proceeds, territory, and source type.

## Use When

Use App Store Connect when diagnosing store conversion, country performance, download quality, subscription/store revenue, refunds, and version-level changes.

## Key Reports

| Priority | Report | Dimensions | Metrics | Purpose | Notes |
|---|---|---|---|---|---|
| P0 | App Analytics / Acquisition | Date, source type | Impressions, product page views, downloads | Store acquisition baseline | Source type is store source only |
| P0 | Territory | Territory | Views, downloads, conversion | Country store performance | Compare with revenue quality |
| P0 | Product page views | Date, source, territory | Views | Store demand | Pair with conversion rate |
| P0 | First-time downloads | Date, territory, source | Downloads | New acquisition | Not Firebase first_open |
| P1 | Redownloads | Date, territory | Downloads | Returning install behavior | Separate from first-time |
| P1 | Conversion rate | Source, territory | Conversion | Store listing quality | Watch metadata changes |
| P0 | Sales and Trends | Date, product, country | Sales, proceeds, refunds | Revenue basis | Separate customer sales/proceeds |
| P0 | Subscription daily reports | Date, product, event | Starts, renewals, cancels | Subscription lifecycle | Align with RevenueCat if used |
| P1 | App version | Version | Downloads, usage if available | Release comparison | Availability varies |

## Key Metrics

- Product page views: store listing views.
- First-time downloads: new app downloads in ASC.
- Redownloads: repeat downloads.
- Customer sales: gross customer-paid basis.
- Developer proceeds: net proceeds basis.
- Refunds: revenue reversal.

## Common Pitfalls

- ASC downloads and Firebase `first_open` are different.
- Customer sales and developer proceeds are different.
- Source Type is not paid campaign attribution.
- Country downloads do not equal country revenue quality.

## Required Questions

- What countries and source types matter?
- Were metadata, price, screenshots, or app version changed?
- Do reports include refunds and proceeds?
- Are subscription reports needed?

## Output Checklist

- Acquisition by source type.
- Territory report.
- Product page views.
- First-time downloads and redownloads.
- Conversion rate.
- Sales, proceeds, refunds.
- Subscription daily reports.
- App version report if available.
