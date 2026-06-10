# Data Inventory Template

Use this template before analysis to classify every provided or missing report.

| Source | Report | Date range | Dimensions | Metrics | Status | Notes |
|---|---|---|---|---|---|---|
| Firebase | Events | YYYY-MM-DD to YYYY-MM-DD | Event name, country, version | Event count, users | usable / partially usable / needs re-export / missing / not applicable |  |
| AdMob | Ad unit summary | YYYY-MM-DD to YYYY-MM-DD | Ad unit, country | Revenue, impressions, eCPM, CTR | usable / partially usable / needs re-export / missing / not applicable |  |
| App Store Connect | Acquisition | YYYY-MM-DD to YYYY-MM-DD | Source type, territory | Views, downloads, conversion | usable / partially usable / needs re-export / missing / not applicable |  |

## Status Values

- `usable`: report can support the intended analysis.
- `partially usable`: report answers only part of the question or has gaps.
- `needs re-export`: date range, dimensions, metrics, or basis are incompatible.
- `missing`: required report not provided.
- `not applicable`: source/report does not apply to this app.
