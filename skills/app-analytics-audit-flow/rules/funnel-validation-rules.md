# Funnel Validation Rules

## Valid Funnel Requirements

- Each funnel must map to one business goal.
- Funnel steps must be truly sequential and reachable.
- Conditional pages cannot be forced into the main funnel.
- Branch features must be separated.
- SDK screens and ad SDK screens must be separated from product screens.

## Interpretation Rules

- Low completion-page arrival is not automatically abnormal; the page may represent a deeper success state.
- Result pages must distinguish empty result, non-empty result, and completed action.
- Paywalls require previous path and next path.
- Ad wrappers require trigger, SDK display, close/reward, and return path.

## Invalid Funnel Checklist

| Check | Invalid if true | Fix |
|---|---|---|
| Screen-name-only | Steps are chosen by class/page names only | Audit navigation and actions |
| Mixed branches | Steps combine unrelated features | Split funnels |
| Conditional page | Optional page is treated as required | Move to branch/path report |
| SDK screen | SDK/internal page is a product step | Exclude or label separately |
| Result container | Result view is treated as success | Find true completion |
| Paywall unknown | Source and next path are missing | Use path exploration |
| Ad unknown | Trigger/return path missing | Use ad interruption path |
