# Firebase / GA4

## Role

Product analytics for app behavior, events, screens, funnels, paths, retention, cohorts, audiences, and key events.

## Use When

Use Firebase / GA4 when diagnosing user behavior, activation, feature usage, screen paths, retention, and event instrumentation.

## Key Reports

| Priority | Report | Dimensions | Metrics | Purpose | Notes |
|---|---|---|---|---|---|
| P0 | Analytics dashboard | Date, country, version | Users, sessions, events, revenue | Operating baseline | Treat as overview only |
| P0 | Events | Event name, parameter | Event count, users | Identify available custom events | Required before funnel design |
| P0 | Pages and screens | Screen, country, version | Views, users | Screen inventory | Screen name is not business truth |
| P0 | Funnel exploration | Confirmed steps | Conversion, elapsed time | Measure validated flows | Use only code-confirmed paths |
| P0 | Path exploration | Previous/next screen | Users, events | Analyze result, paywall, ad paths | Use around ambiguous pages |
| P1 | Retention | Cohort, country, source | Retention | Repeat behavior | Align with install date |
| P1 | Cohorts | Cohort date, segment | Retention, revenue | Segment quality | Watch date basis |
| P1 | Audiences | Audience | Users, events | Segment analysis | Use after events are reliable |
| P1 | Conversions / key events | Key event | Count, users | Success tracking | Requires correct event definition |
| P2 | DebugView | Device, event | Live events | Validate new tracking | Use during instrumentation QA |

## Key Metrics

- `first_open`: first Firebase open, not store download.
- `screen_view`: screen exposure, not success.
- Event count: occurrences, not users.
- Users: unique users per reporting scope.
- Revenue: Firebase-reported revenue, not necessarily total revenue.

## Common Pitfalls

- Do not infer business meaning from screen name.
- `screen_view` does not equal success.
- `first_open` does not equal App Store downloads.
- Firebase revenue may exclude AdMob, store, or subscription revenue.
- Automatic screen views may lack business semantics.
- Without custom events, many conclusions are approximate.

## Required Questions

- Are custom events implemented?
- Are screen names manual or automatic?
- Which event defines true success?
- Are purchase, ad, permission, and paywall events tracked?
- Are event parameters stable across versions?

## Output Checklist

- Dashboard overview.
- Events export.
- Pages and screens.
- Validated funnels.
- Path exploration for result, paywall, and ad wrapper screens.
- Retention/cohort reports.
- Conversion/key event settings.
