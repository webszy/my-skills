# Monetization Rules

## Revenue Basis

Always separate:

- Firebase revenue.
- AdMob revenue.
- AppLovin MAX / mediation revenue.
- Store customer sales.
- Developer proceeds.
- RevenueCat revenue.
- Subscription revenue.
- IAP revenue.
- Refunds and net revenue.

## Ad Metrics

- `requests`: ad load opportunities.
- `matched requests`: demand matches.
- `impressions`: displayed ads.
- `clicks`: user clicks.
- `CTR`: clicks / impressions; high CTR may indicate misclicks.
- `eCPM`: revenue per thousand impressions; high eCPM may not scale.
- `fill rate` / `show rate`: ad availability/display quality.
- `match rate`: matched requests / requests.

## Subscription / IAP Metrics

- New subscription: first subscription start.
- Trial start: trial entry, not paid conversion.
- Renewal: recurring paid continuation.
- Cancellation: future renewal stop.
- Refund: revenue reversal.
- Developer proceeds: net platform proceeds.
- Customer sales: gross customer-paid basis.

## Business Metrics

- ARPU: revenue per user.
- ARPDAU: revenue per daily active user.
- LTV: lifetime value over a defined window.
- ROAS: revenue / ad spend, with matched date and currency basis.

## Risk Rules

- High CTR can be a misclick problem.
- High eCPM can collapse under scale.
- Ad revenue gains must be checked against activation, retention, reviews, crashes, and subscription conversion.
