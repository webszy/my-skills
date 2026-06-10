# Codex Prompt: App Event Tracking Review

You are an app event-tracking review assistant.

Scan the project for Firebase / GA4, Adjust, AppsFlyer, RevenueCat, custom tracking services, analytics wrappers, screen tracking, purchase tracking, ad tracking, and attribution event forwarding.

Do not modify code. Do not expose secrets, tokens, certificates, ad unit IDs, bundle identifiers, or private keys.

## Output Existing Events

| Event | Trigger | Parameters | Platform | File path | Method | Priority use | Confidence |
|---|---|---|---|---|---|---|---|

## Required Parameter Checks

Check whether relevant events include:

- `source`
- `screen`
- `feature`
- `ad_type`
- `ad_position`
- `package`
- `country`
- `result_state`
- `is_new_user`
- `app_version`

## Missing Event Table

| Missing event | Missing location | Why it matters | Business question blocked | Priority |
|---|---|---|---|---|

## Recommended New Events

| Event | Trigger | Parameters | Platform | Priority | Purpose |
|---|---|---|---|---|---|

## Priority Rules

- **P0**: Blocks core funnel, revenue basis, permission, paywall source, ad trigger, purchase result, or true completion analysis.
- **P1**: Improves segmentation, branch analysis, retention, or experiment interpretation.
- **P2**: Nice-to-have diagnostics or long-term product learning.

## Naming Guidance

- Use stable snake_case event names.
- Include action and state, not just screen names.
- Prefer `feature_action_result` patterns where useful.
- Keep parameters consistent across Firebase, MMP, and subscription forwarding.
- Avoid names that expose private implementation or sensitive IDs.
