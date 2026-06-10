# RevenueCat

## Role

Subscription and IAP analytics for paywalls, trials, purchases, renewals, cancellations, refunds, active subscriptions, MRR, LTV, cohorts, package performance, and entitlements.

## Use When

Use RevenueCat when diagnosing subscription conversion, entitlement behavior, package performance, renewal quality, cancellation/refund issues, and paywall source problems.

## Key Reports

| Priority | Report | Dimensions | Metrics | Purpose | Notes |
|---|---|---|---|---|---|
| P0 | Paywall views | Paywall, source | Views | Exposure | If available and instrumented |
| P0 | Trial starts | Package, country | Trials | Trial conversion | Not paid conversion |
| P0 | Initial purchases | Package, source | Purchases, revenue | Paid conversion | Needs source tracking |
| P0 | Renewals | Product, cohort | Renewals, revenue | Retention revenue | Check period basis |
| P0 | Cancellations | Product, cohort | Cancels | Churn | Pair with renewals |
| P0 | Refunds | Product, country | Refunds | Revenue quality | Align with ASC |
| P0 | Active subscriptions | Product, entitlement | Active subs | Current subscriber base | Not daily revenue |
| P1 | MRR / LTV | Cohort, product | MRR, LTV | Long-term value | Basis check required |
| P1 | Package performance | Package, paywall | Conversion | Package optimization | Needs source/package params |
| P0 | Entitlements | Entitlement | Active/inactive | Access logic | Compare with code |

## Key Metrics

- Trial start is not paid conversion.
- Initial purchase indicates first paid action.
- Renewal indicates subscription continuation.
- Active entitlement indicates access state, not daily revenue.
- Refunds and proceeds require store reconciliation.

## Common Pitfalls

- RevenueCat, ASC, and Firebase purchase revenue can differ.
- Trial start does not equal paid conversion.
- Active entitlement is not same-day revenue.
- Package source missing from events weakens paywall analysis.

## Required Questions

- Are paywall views tracked?
- Are paywall source and package parameters available?
- Which entitlements unlock which features?
- Are refunds and cancellations available?
- Do RevenueCat totals reconcile with store reports?

## Output Checklist

- Paywall views if available.
- Trials, purchases, renewals, cancellations, refunds.
- Active subscriptions.
- MRR, LTV, cohorts.
- Package performance.
- Entitlements.
