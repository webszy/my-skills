# AppLovin MAX

## Role

Ad mediation analytics for ad units, formats, countries, networks, waterfall/bidding, impressions, revenue, eCPM, fill rate, show rate, ARPDAU, and cohort revenue.

## Use When

Use AppLovin MAX when diagnosing mediated ad revenue, network quality, placement performance, waterfall/bidding changes, country performance, and ad strategy impact.

## Key Reports

| Priority | Report | Dimensions | Metrics | Purpose | Notes |
|---|---|---|---|---|---|
| P0 | Ad unit | Ad unit | Revenue, impressions, eCPM | Placement performance | Map to code triggers |
| P0 | Ad format | Format | Revenue, impressions, eCPM | Format mix | Separate interstitial/rewarded/native/banner |
| P0 | Country | Country, ad unit | Revenue, eCPM, fill | Geo quality | Useful for country rules |
| P0 | Network | Network, ad unit | Revenue, eCPM, fill | Network quality | Bidding/waterfall context |
| P1 | Waterfall / bidding | Network, waterfall | Fill, eCPM, revenue | Mediation tuning | Watch user experience |
| P1 | ARPDAU | Date, country | ARPDAU | Revenue quality | Needs active user basis |
| P1 | Cohort revenue | Cohort, source | Revenue | LTV / ROAS | If available |

## Key Metrics

- Impressions and revenue show volume and monetization.
- eCPM shows price, not scale.
- Fill rate and show rate diagnose supply/display.
- ARPDAU needs daily active user denominator.

## Common Pitfalls

- MAX ad unit / placement must match code trigger points.
- High network eCPM does not mean high total revenue.
- Waterfall changes can affect fill and user experience.

## Required Questions

- Which ad units map to which screens/actions?
- Were waterfall, bidding, or network settings changed?
- Are country and date dimensions available?
- Are ARPDAU or cohort reports available?

## Output Checklist

- Ad unit, format, country, and network reports.
- Waterfall/bidding report.
- Impressions, revenue, eCPM, fill, show rate.
- ARPDAU and cohort revenue if available.
