# Example: Photo Recovery Case

## Context

- App type: Photo Recovery / Photo Cleanup utility app.
- Data sources: Firebase, AdMob, App Store Connect.
- Initial mistake: a screen-name-based funnel was built as:

`first_open -> BeginViewController -> GuideViewController -> PRLanguageSelectionViewController -> PRSwipViewController -> PRPhotoPEController -> PRRecoveryViewController -> PRPhotoListController -> PRSwipeDeleteViewController`

## Code Audit Findings

| Finding | Correct meaning | Rule learned |
|---|---|---|
| `PRPhotoListController` | Photo/video recovery list; scan result container | Result container is not automatically success |
| `PRPhotoPEController` | Album permission denial prompt / Face ID full-scan prompt | Page name is not business truth |
| `PRSwipeDeleteViewController` | Swipe cleanup/delete branch | Branch feature is not recovery main path |
| `PRSwipViewController` | First default main screen | Launch path must be code-confirmed |
| `PRRecoveryViewController` | Recovery entry; Start Recovery begins flow | Use user action as funnel step |
| `PRRecoveryCompleteController` | Deeper completion after asset selection and restore/save | Low arrival may be normal |
| Interstitial in `viewDidLoad` | Auto triggers on several pages including result list | Ad interruption needs separate path |
| Firebase custom events | Mostly ad revenue events; scan/permission/recovery/purchase source missing | Missing events limit conclusions |

## Invalid Funnel

| Invalid funnel | Why invalid | Correct replacement |
|---|---|---|
| first_open -> Begin -> Guide -> Language -> Swip -> PhotoPE -> Recovery -> PhotoList -> SwipeDelete | Mixes launch, permission prompt, recovery, result container, and cleanup branch | Split into launch, recovery, cleanup, permission, paywall, and ad paths |

## Correct Funnel Split

| Funnel | Example steps | Notes |
|---|---|---|
| First launch | first_open -> launch/begin -> onboarding/language if required -> `PRSwipViewController` | Confirm required screens from code |
| Recovery feature | `PRRecoveryViewController` -> Start Recovery -> permission allow -> `PRPhotoListController` -> asset select -> restore/save -> `PRRecoveryCompleteController` | List view is not final success |
| Swipe cleanup | `PRSwipViewController` -> `PRSwipeDeleteViewController` -> delete action -> delete result | Separate branch |
| Permission path | permission prompt -> allow/deny -> recovery continuation or denial prompt | Analyze separately |
| Photo list previous path | previous screen -> `PRPhotoListController` | Check entry sources |
| Photo list next path | `PRPhotoListController` -> asset selection / exit / ad / paywall | Shows continuation |
| Purchase source path | previous screen -> paywall -> close/purchase -> next path | Requires source tracking |
| Interstitial path | trigger page -> ad show -> ad close -> return path | Check result-list impact |

## Firebase Reports to Re-export

- Events list with parameters.
- Pages and screens.
- First launch funnel to default home screen.
- Recovery feature funnel.
- Swipe cleanup funnel.
- Permission path exploration.
- `PRPhotoListController` previous path.
- `PRPhotoListController` next path.
- Paywall previous and next path.
- Interstitial wrapper previous and next path.

## AdMob / ASC Reports Still Useful

- AdMob ad unit summary.
- AdMob date + ad unit.
- AdMob country + ad unit.
- AdMob ad format and mediation source.
- ASC source type.
- ASC territory.
- ASC product page views, first-time downloads, redownloads, conversion rate.
- ASC sales, refunds, and proceeds.

## Rules Learned

- Do not build funnels from controller names alone.
- Result list pages need result-state and completion events.
- Permission prompts and feature screens must be separated.
- Cleanup and recovery are separate business goals.
- Ad triggers inside result pages can affect continuation.
- Missing custom events can make Firebase funnels approximate only.
