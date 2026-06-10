# Adjust

## Role

Mobile measurement partner reporting for attribution, campaigns, cost, events, revenue, cohort quality, ROAS, and fraud/rejected installs.

## Use When

Use Adjust when diagnosing paid user acquisition, campaign quality, cost/revenue consistency, post-install event quality, and attribution gaps.

## Key Reports

| Priority | Report | Dimensions | Metrics | Purpose | Notes |
|---|---|---|---|---|---|
| P0 | Campaign performance | Network, campaign, adgroup, creative | Installs, sessions, events | UA quality | Match app event definitions |
| P0 | Country | Country, campaign | Installs, cost, revenue | Geo quality | Compare with app/store country |
| P0 | Cost | Network, campaign | Cost, CPI | Spend basis | Currency must match revenue |
| P0 | Revenue | Source, campaign | Ad revenue, IAP revenue | Monetization quality | Confirm forwarding |
| P0 | Cohort | Install date, campaign | Retention, revenue, ROAS | LTV/ROAS | Use install-date basis |
| P1 | Raw installs | User-level install rows | Installs | Attribution QA | Sensitive fields must not be exposed |
| P1 | Raw events | Event rows | Events, revenue | Event QA | Needed for mapping issues |
| P1 | Fraud / rejected installs | Network, campaign | Rejected installs | Traffic quality | If available |

## Key Metrics

- Installs, sessions, and events measure post-install quality.
- Cost and CPI measure acquisition cost.
- Ad revenue and IAP revenue depend on forwarding setup.
- Cohort ROAS should use install-date cohorts.

## Common Pitfalls

- MMP attribution is not store Source Type.
- Cost and revenue must use the same currency.
- Cohort reports should be read by install date.
- Missing event postbacks can misclassify channel quality.

## Required Questions

- Which networks/campaigns are included?
- Is cost connected?
- Are Firebase/ad/subscription events forwarded?
- Is revenue split into ad and IAP?
- Is fraud reporting enabled?

## Output Checklist

- Campaign performance.
- Country performance.
- Cost and CPI.
- Events and sessions.
- Ad revenue and IAP revenue.
- Cohort retention/revenue/ROAS.
- Raw installs/events if debugging.
- Fraud/rejected installs if available.
