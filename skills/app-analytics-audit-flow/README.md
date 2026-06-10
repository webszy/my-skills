# App Analytics Audit Flow

`app-analytics-audit-flow` is a code-first Skill for mobile app growth, monetization, subscription, attribution, store, and stability analysis.

Its core rule:

> Audit the real app paths from code before building reports or interpreting funnels.

## Use Cases

Use this Skill for:

- Firebase / GA4 app analytics and funnel planning.
- AdMob, AppLovin MAX, or mediation revenue analysis.
- App Store Connect or Google Play Console acquisition and revenue checks.
- Adjust / AppsFlyer attribution and ROAS analysis.
- RevenueCat / IAP subscription conversion analysis.
- Crashlytics / Sentry stability impact analysis.
- CSV report validation and final optimization planning.

## Workflow

1. **Code audit**: Identify launch paths, feature paths, permissions, ads, paywalls, entitlements, events, Remote Config, and version context.
2. **Report planning**: Convert confirmed app paths into required reports and reject invalid funnels.
3. **Data validation**: Check dates, dimensions, metric definitions, revenue basis, duplicates, totals, and missing reports.
4. **Data analysis**: Analyze acquisition, activation, retention, monetization, subscription, country/channel quality, stability, and release impact.
5. **Optimization plan**: Produce P0/P1/P2 actions, experiments, Remote Config changes, tracking fixes, and release recommendations.

## Supported Data Sources

- Product analytics: Firebase, GA4, Amplitude, Mixpanel, PostHog.
- Attribution / UA: Adjust, AppsFlyer, Branch, Singular, Kochava.
- Ad monetization: AdMob, AppLovin MAX, ironSource, TopOn, TradPlus.
- Store analytics: App Store Connect, Google Play Console.
- Subscription / IAP: RevenueCat, Adapty, Qonversion, App Store, Google Play.
- Stability: Crashlytics, Sentry, Bugly, Firebase Performance.

## Examples

Firebase + AdMob + App Store Connect:
1. Run the code audit prompt.
2. Build Firebase launch/core/paywall/ad path reports from confirmed paths.
3. Request AdMob ad unit, country, format, and mediation reports.
4. Request App Store source type, territory, conversion, sales, refund, and subscription reports.

AppsFlyer + MAX + RevenueCat:
1. Confirm install cohort, campaign, ad placement, paywall source, and entitlement logic from code.
2. Request AppsFlyer aggregate, raw installs/events, cohort, retention, cost, ad revenue, and ROAS reports.
3. Request MAX ad unit, placement, country, network, eCPM, fill, show rate, revenue, and ARPDAU reports.
4. Request RevenueCat trials, purchases, renewals, cancellations, refunds, active subscriptions, package, cohorts, and entitlements.

Reports without code:
1. Ask for real app flow descriptions, screenshots, or recordings.
2. Mark funnels as provisional.
3. Validate existing reports.
4. Recommend code audit before final optimization decisions.

## File Structure

- `SKILL.md`: Main routing rules and top-level workflow.
- `workflows/`: Stage-by-stage procedures.
- `prompts/`: Reusable Codex prompts.
- `datasources/`: Platform-specific report guidance.
- `templates/`: Output templates.
- `rules/`: Validation, monetization, and risk rules.
- `examples/`: Reusable examples and report shapes.

## Extension Ideas

- Add datasource modules for Amplitude, Mixpanel, Branch, Singular, Adapty, and Sentry.
- Add scripts for CSV inventory generation and metric consistency checks.
- Add app-category examples for VPN, utility, AI photo, cleaner, scanner, fitness, and education apps.
