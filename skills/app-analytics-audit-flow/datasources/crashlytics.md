# Crashlytics

## Role

Stability analytics for crash-free users, crash-free sessions, fatal issues, non-fatal issues, affected users, versions, devices, OS, stack traces, and issue trends.

## Use When

Use Crashlytics when diagnosing stability impact on acquisition, activation, monetization, subscription conversion, retention, or release quality.

## Key Reports

| Priority | Report | Dimensions | Metrics | Purpose | Notes |
|---|---|---|---|---|---|
| P0 | Crash-free users | Date, version | Crash-free users | User stability | Different from sessions |
| P0 | Crash-free sessions | Date, version | Crash-free sessions | Session stability | Different from users |
| P0 | Fatal issues | Issue, version, device | Fatal count, affected users | Severe failures | Prioritize core/revenue flows |
| P1 | Non-fatal issues | Issue, version | Non-fatal count | Degraded experience | Can affect conversion |
| P0 | Affected users | Issue, version | Users | Impact scope | Use with flow importance |
| P0 | Version | Version | Crashes, users | Release impact | Compare before/after release |
| P1 | Device / OS | Device, OS | Crashes, users | Compatibility | Useful for segmenting |
| P0 | Stack trace | Issue | Trace | Engineering handoff | Do not paste huge traces |
| P1 | Issue trend | Date, issue | Count | Regression detection | Match releases/config changes |

## Key Metrics

- Crash-free users and sessions are different.
- Fatal and non-fatal issues have different severity.
- Affected users indicate user impact.
- Version/device/OS dimensions help isolate regressions.

## Common Pitfalls

- No crash does not mean no performance problem.
- Crash-free sessions and crash-free users are not interchangeable.
- Version differences are often critical.
- Crashes near high-value flows should be higher priority.

## Required Questions

- Which versions are in scope?
- Did a release or SDK upgrade happen recently?
- Are issues near onboarding, core feature, ads, or purchase flows?
- Are non-fatal and performance issues available?

## Output Checklist

- Crash-free users/sessions.
- Fatal and non-fatal issues.
- Affected users.
- Version, device, OS breakdowns.
- Issue trends and relevant stack traces.
