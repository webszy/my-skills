# Workflow 03: Data Validation

## Goal

Validate uploaded CSVs, screenshots, and platform reports before analysis.

## Required Checks

### Date Range

Confirm start date, end date, timezone, install-date vs activity-date basis, and whether all sources share a comparable period.

### Missing Dates

Check whether daily rows cover every date. Missing dates should be marked as data gaps, not assumed zero.

### Totals vs Details

Compare total rows with daily or dimensional rows. If totals do not reconcile, mark the report as partially usable or needing re-export.

### Duplicate Rows

Check duplicate combinations of date, country, campaign, ad unit, package, event, version, or other dimensions.

### Encoding and Delimiters

Check UTF-8, delimiter type, decimal separators, thousands separators, currency symbols, and spreadsheet auto-formatting issues.

### Metric Definitions

Confirm whether metrics are users, events, sessions, installs, downloads, impressions, requests, matches, revenue, proceeds, or customer sales.

### Revenue Basis

Separate Firebase revenue, AdMob revenue, store customer sales, developer proceeds, RevenueCat revenue, subscription revenue, IAP revenue, ad revenue, refunds, and net revenue.

### Download Basis

Do not mix Firebase `first_open`, App Store first-time downloads, redownloads, Google Play acquisitions, MMP installs, and SKAdNetwork installs without a reconciliation note.

## Common Cross-source Conflicts

- Firebase `first_open` is not App Store downloads.
- Firebase revenue is not necessarily total revenue.
- AdMob estimated revenue is not store proceeds.
- RevenueCat revenue may not equal ASC proceeds.
- MMP attribution is not store source type.
- Cohort reports and activity reports answer different questions.

## Status Rules

- `usable`: Matches scope, date range, dimensions, and metric basis.
- `partially usable`: Useful for a subset but has gaps or missing dimensions.
- `needs re-export`: Cannot answer the intended question safely.
- `missing`: Required report was not provided.
- `not applicable`: Source or report is irrelevant to the app.

## Data Inventory Table

| Source | Report | Date range | Dimensions | Metrics | Status | Notes |
|---|---|---|---|---|---|---|

## User-facing Validation Summary

Use this structure:

1. Reports received.
2. Reports usable for analysis.
3. Reports partially usable and limitations.
4. Reports needing re-export.
5. Missing required reports.
6. Metric basis conflicts.
7. Confidence level for next-step analysis.
