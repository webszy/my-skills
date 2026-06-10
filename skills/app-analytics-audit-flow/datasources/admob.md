# AdMob

## Role

Ad monetization reporting for ad units, formats, countries, mediation, requests, matches, impressions, clicks, CTR, eCPM, fill/show rate, match rate, and estimated revenue.

## Use When

Use AdMob when analyzing ad revenue, placement quality, ad format mix, country performance, mediation source quality, or potential misclick issues.

## Key Reports

| Priority | Report | Dimensions | Metrics | Purpose | Notes |
|---|---|---|---|---|---|
| P0 | Ad unit summary | Ad unit | Revenue, impressions, eCPM, CTR | Identify revenue drivers | Map to code placement |
| P0 | Date + ad unit | Date, ad unit | Revenue, requests, impressions | Trend by placement | Needed for release/config changes |
| P0 | Country + ad unit | Country, ad unit | Revenue, eCPM, CTR | Country quality | Compare with app paths |
| P0 | Ad format | Format | Revenue, impressions, CTR | Format mix | Separate interstitial/rewarded/banner/native |
| P1 | Country + ad format | Country, format | eCPM, fill, show rate | Geo-format diagnosis | Useful for country rules |
| P1 | Mediation source | Network, ad unit | Revenue, eCPM, fill | Mediation quality | Watch waterfall/bidding changes |

## Key Metrics

- Requests and matched requests show demand availability.
- Impressions show actual exposure.
- CTR may indicate engagement or misclick risk.
- eCPM shows revenue per thousand impressions.
- Fill/show rate and match rate diagnose supply and display issues.
- Estimated revenue is ad-platform revenue, not store revenue.

## Common Pitfalls

- Abnormal CTR may be accidental clicks.
- High eCPM does not mean unlimited scale.
- AdMob revenue must be separated from Firebase revenue.
- SDK pages do not represent ad placements.
- Always map ad units and formats to code trigger positions.

## Required Questions

- Which ad units correspond to which code placements?
- Are App Open, Interstitial, Rewarded, Native, and Banner separated?
- Did ad cooldown, mediation, or placement change recently?
- Are reports broken down by country and date?

## Output Checklist

- Ad unit summary.
- Date + ad unit.
- Country + ad unit.
- Ad format.
- Country + ad format.
- Mediation source.
