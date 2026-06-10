# Funnel Plan Template

## Funnel Table

| Funnel name | Business goal | Steps | Required? | Exclusions | Success definition | Notes |
|---|---|---|---:|---|---|---|
| First launch | Reach usable home state | first_open -> launch -> onboarding -> home | Yes | SDK screens, optional branches | Home/default tab reached | Confirm from code |
| Core feature | Complete primary task | Entry -> permission -> processing -> result -> completion | Yes | Secondary feature branches | Actual completion event/page | Result container may not be success |

## Valid Funnels

List only code-confirmed, continuous paths tied to one business goal.

## Invalid Funnels

| Invalid funnel | Why invalid | Correct replacement | Evidence |
|---|---|---|---|

## Path Exploration Plan

- Result page previous path.
- Result page next path.
- Paywall previous path.
- Paywall next path.
- Ad wrapper previous path.
- Ad wrapper next path.

## Specialized Funnels

- Permission funnel: prompt view -> allow/deny -> recovery path.
- Paywall source path: previous page -> paywall -> close/purchase -> next page.
- Ad interruption path: trigger -> ad show -> close/reward -> return path.
