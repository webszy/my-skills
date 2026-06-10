# Event Tracking Plan Template

## Event Table

| Event | Trigger | Parameters | Platform | Priority | Purpose |
|---|---|---|---|---|---|
| onboarding_complete | User completes onboarding | source, screen, is_new_user, app_version | Firebase / MMP | P0 | Launch funnel |
| core_feature_start | User starts primary feature | source, screen, feature, is_new_user | Firebase / MMP | P0 | Activation |
| core_feature_result | Result screen is shown | feature, result_state, source | Firebase | P0 | Result quality |
| paywall_view | Paywall shown | paywall_source, package, screen | Firebase / RevenueCat | P0 | Paywall source |
| ad_show | Ad is shown | ad_type, ad_position, screen | Firebase / MMP | P0 | Ad interruption |

## Recommended Parameters

- `source`
- `screen`
- `feature`
- `result_state`
- `ad_type`
- `ad_position`
- `paywall_source`
- `package`
- `is_new_user`
- `country`
- `app_version`

## Priority Guidance

- P0: required to validate core success, revenue, permission, ad, paywall, or purchase paths.
- P1: useful for segmentation and experiment interpretation.
- P2: useful for long-term diagnostics.
