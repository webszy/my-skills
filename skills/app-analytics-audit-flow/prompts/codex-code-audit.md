# Codex Prompt: App Analytics Code Audit

You are an app analytics code-audit assistant.

Your task is to scan the current mobile app project and produce a factual Markdown audit report for analytics planning.

Do not modify code.
Do not submit diffs.
Do not refactor.
Do not run builds unless explicitly asked.
Do not expose secrets, API keys, tokens, certificates, private keys, ad unit IDs, bundle identifiers, or other sensitive values.
If sensitive configuration exists, only state that sensitive configuration exists.

Every important finding must include:

- File path
- Class / file / module name
- Method / function name if available
- Line number if available
- Code summary
- Confidence level: confirmed / likely / uncertain

Do not guess business meaning when code does not prove it.
If something cannot be confirmed from code, write: `Cannot confirm from code; needs human confirmation`.

## Table of Contents

1. Project Context
2. Screen and Page Meaning Audit
3. Launch Path Audit
4. Core Feature Path Audit
5. Permission Flow Audit
6. Ad Trigger Audit
7. Paywall / Purchase Audit
8. Entitlement / Pro / VIP Audit
9. Analytics Event Audit
10. Remote Config / A/B Capability Audit
11. Version / Release Audit
12. Analytics Report Plan
13. Final Markdown Output Structure
14. Output Requirements

---

## 1. Project Context

Scan the app project to prepare an analytics and monetization report plan.

The final goal is to help product, growth, and engineering teams decide which Firebase / GA4, AdMob, App Store Connect, Adjust, AppsFlyer, RevenueCat, or other analytics reports should be exported.

Your code audit should identify:

- Real app launch path
- First-time user path
- Returning user path
- Screen / page meanings
- Core feature paths
- Conditional paths
- Permission flows
- Result pages
- Completion pages
- Ad trigger rules
- Paywall trigger rules
- Pro / VIP / subscription entitlement logic
- Analytics events
- Remote Config / A/B testing capabilities
- Reports that should be built after the audit

---

## 2. Screen and Page Meaning Audit

Scan all ViewController / Activity / Fragment / Route / Page / Screen classes.

Output a table:

| Screen / Class | Business meaning | First-time required | Core-flow required | Previous screens | Next screens | File path | Method / evidence | Confidence | Notes |
|---|---|---:|---:|---|---|---|---|---|---|

Pay special attention to:

- Launch / splash pages
- Onboarding pages
- Language selection pages
- Permission pages
- Default home page
- Tab pages
- Core feature entry pages
- Loading pages
- Result pages
- Empty result pages
- Completion pages
- Paywall pages
- Discount pages
- Settings pages
- History pages
- Ad wrapper pages
- SDK internal screens

For each important screen, answer:

1. What does this page really do?
2. Is it required for first-time users?
3. Is it required for the core feature flow?
4. Is it a conditional page?
5. Is it a feature branch page?
6. Is it a result container page?
7. Does seeing this page mean the user succeeded?
8. Does seeing this page only mean the user entered a container or loading state?
9. Is it a product screen or an SDK/internal screen?
10. Should it be used in a Firebase funnel?

---

## 3. Launch Path Audit

Scan app entry files such as:

- AppDelegate
- SceneDelegate
- RootViewController
- MainActivity
- MainTabBarController
- Router
- Navigator
- Launch / Splash / Begin page
- Navigation coordinator

Output:

| Step | Screen / event | Trigger condition | First-time user | Returning user | Failure / skip path | File path | Method | Confidence |
|---:|---|---|---:|---:|---|---|---|---|

Answer:

1. What is the first business screen after app launch?
2. Is there a splash / begin / launch page?
3. Is onboarding shown?
4. Is onboarding shown only once?
5. Is a language page shown?
6. Is the language page shown only once?
7. What is the default home / tab after onboarding?
8. Is an App Open Ad shown during launch?
9. Is a paywall or discount page shown during launch?
10. What page represents successful arrival at the app home state?

---

## 4. Core Feature Path Audit

Identify the app's core features.

Do not force multiple features into one funnel.

For each core feature, output:

| Feature | Step | Screen / event | User action | Success condition | Failure / rejection path | File path | Method | Confidence |
|---|---:|---|---|---|---|---|---|---|

Answer for each feature:

1. Where does the user enter the feature?
2. Is permission required?
3. What happens if permission is denied?
4. Is there a loading / scanning / processing page?
5. Which page shows the result?
6. Which event or page represents user-visible success?
7. Which event or page represents actual completion?
8. Can the result page be empty?
9. Can users enter the result page from history?
10. Do multiple features share the same result page?
11. Should the result page be treated as success, partial success, or only a container?

Also explicitly list:

| Invalid funnel assumption | Why invalid | Correct replacement | Evidence |
|---|---|---|---|

---

## 5. Permission Flow Audit

Scan all permission-related code:

- Photos
- Camera
- Microphone
- Location
- Notification
- Contacts
- Files
- Health
- Tracking / ATT
- Other system permissions

Output:

| Permission | Requested where | Trigger timing | Allow path | Deny path | Prompt page | File path | Method | Confidence |
|---|---|---|---|---|---|---|---|---|

Answer:

1. Which permissions are requested during onboarding?
2. Which permissions are requested only when using a feature?
3. Does permission denial block the core flow?
4. Where is the permission-denied page?
5. Is permission status logged to analytics?
6. Should permission pages be included in the main funnel or analyzed separately?

---

## 6. Ad Trigger Audit

Scan ad-related code:

- AdMob
- GoogleMobileAds
- AppLovin MAX
- ironSource
- TopOn
- TradPlus
- Meta Audience Network
- Pangle
- Unity Ads
- Vungle
- App Open Ad
- Interstitial
- Rewarded
- Native
- Banner
- Ad manager
- Ad wrapper screen
- Ad frequency control
- Remote Config ad settings

### 6.1 App Open Ad

Output:

| Trigger scenario | Shows ad? | Trigger condition | Frequency control | Excluded screens | Fallback | File path | Method | Confidence |
|---|---:|---|---|---|---|---|---|---|

Answer:

1. Is App Open Ad shown on first launch?
2. Is it shown on cold start?
3. Is it shown when returning from background?
4. Can it be shown after returning from permission settings, payment, Safari, or App Store?
5. Is there a cooldown?
6. Is there a session limit?
7. Are paywall, permission, result, or core-flow pages excluded?
8. Does App Open Ad compete with Interstitial?
9. What happens when App Open Ad fails?

### 6.2 Interstitial Ad

Output:

| Trigger screen | Trigger action | Auto trigger | Blocks core flow | Close callback path | Frequency control | File path | Method | Confidence |
|---|---|---:|---:|---|---|---|---|---|

Answer:

1. Where is interstitial shown automatically?
2. Where is it shown after user actions?
3. Is it shown before the user sees value?
4. Is it shown immediately after entering a result page?
5. Is it shown before save / restore / delete / export?
6. Is there a cooldown?
7. Does it share logic with App Open Ad?
8. Could it reduce core flow completion?

### 6.3 Rewarded Ad

Output:

| Entry screen | Trigger action | Unlocked benefit | Success callback | Failure path | Requires real reward callback | File path | Method | Confidence |
|---|---|---|---|---|---:|---|---|---|

Answer:

1. Is Rewarded Ad implemented?
2. Where is it used?
3. Does it unlock one operation or a broader entitlement?
4. What exactly is unlocked?
5. Is the unlock triggered by the reward callback or only by ad close?
6. What happens if rewarded ad fails?
7. Is rewarded ad a good value-exchange placement?

### 6.4 Native / Banner Ads

Output:

| Ad placement | Screen | Position description | Near primary button | Dynamic layout shift | Misclick risk | File path | Confidence |
|---|---|---|---:|---:|---:|---|---|

Answer:

1. Where is each native or banner ad shown?
2. Is it near Continue / Start / Save / Recover / Delete / Export buttons?
3. Does ad loading change layout height or button position?
4. Could it cause accidental clicks?
5. Should this placement be analyzed with a separate report?

---

## 7. Paywall / Purchase Audit

Scan:

- BuyViewController
- Paywall
- Subscription
- StoreKit
- RevenueCat
- Adapty
- Qonversion
- Purchase manager
- Premium
- Pro
- VIP
- Discount
- Trial
- Restore purchase

Output:

| Entry screen | Trigger action | Paywall screen | Auto popup | Close path | Purchase success path | Continues original action | File path | Method | Confidence |
|---|---|---|---:|---|---|---:|---|---|---|

Answer:

1. Where is the paywall shown?
2. Is it auto-shown or user-triggered?
3. Is it shown on first launch?
4. Is it shown before the core feature?
5. Is it shown after the user sees a result?
6. Is it shown before save / restore / delete / export?
7. When is the discount page shown?
8. How is the discount page related to the main paywall?
9. What happens when the paywall is closed?
10. Is there a rewarded-ad free continuation path after closing?
11. What happens after purchase success?
12. Is the original action continued after purchase?
13. What packages exist?
14. Which package is default selected or highlighted?
15. Is there a free trial?
16. Are product prices hardcoded or fetched from StoreKit / server / RevenueCat?
17. Is paywall source logged?

---

## 8. Entitlement / Pro / VIP Audit

Scan:

- isPro
- isVip
- isSubscribed
- premium
- subscription
- entitlement
- hideAd
- freeUse
- limit
- quota
- trial
- restore

Output:

| Entitlement | Free user | Pro user | Unlockable by ad | Has usage limit | Code location | Confidence |
|---|---|---|---:|---:|---|---|

Answer:

1. Does Pro remove ads?
2. Does Pro unlock batch operations?
3. Does Pro unlock high-quality save or export?
4. Does Pro unlock unlimited use?
5. Does Pro unlock cloud / premium / advanced features?
6. What are free user restrictions?
7. Are there daily, per-session, or lifetime limits?
8. Can rewarded ads bypass Pro restrictions?
9. Do paywall claims match code entitlements?

---

## 9. Analytics Event Audit

Scan:

- Firebase Analytics
- GA4
- Analytics.logEvent
- logEvent
- setScreenName
- screen_view
- purchase event
- ad event
- Adjust event tracking
- AppsFlyer event tracking
- RevenueCat event forwarding
- Custom tracking service

Output existing events:

| Event name | Trigger screen | Trigger timing | Parameters | File path | Method | Useful for funnel? | Confidence |
|---|---|---|---|---|---|---|---|

Check whether these events exist:

- first_open
- screen_view
- app_open
- onboarding_start
- onboarding_complete
- permission_view
- permission_allow
- permission_deny
- core_feature_entry_click
- scan_start
- scan_success
- scan_empty
- scan_fail
- result_view
- list_view
- item_select
- restore_click
- restore_success
- save_click
- save_success
- delete_click
- delete_success
- paywall_view
- paywall_close
- package_click
- purchase_click
- purchase_success
- purchase_fail
- ad_trigger
- ad_show
- ad_close
- ad_reward_complete

Also check:

1. Do ad events include `ad_type`?
2. Do ad events include `ad_position`?
3. Do paywall events include `source`?
4. Do purchase events include `package`?
5. Do core feature events include `source`?
6. Can result events distinguish empty result from non-empty result?
7. Are screen views automatic or manually named?
8. Is there custom screen naming that differs from class names?
9. Are Adjust / AppsFlyer / MMP events consistent with Firebase events?

Output missing event recommendations:

| Suggested event | Suggested location | Trigger timing | Suggested parameters | Purpose | Priority |
|---|---|---|---|---|---|

---

## 10. Remote Config / A/B Capability Audit

Scan:

- Firebase Remote Config
- Local config
- Server config
- Feature flags
- Ad switches
- Paywall switches
- Frequency controls
- Country rules
- Version rules
- User segment rules
- Experiment assignment

Output:

| Config key | Default value | Controls | Remote configurable | No-release change? | File path | Confidence |
|---|---|---|---:|---:|---|---|

Answer:

1. Can App Open Ad be remotely disabled?
2. Can Interstitial be remotely disabled?
3. Can Rewarded be remotely disabled?
4. Can Native / Banner be remotely disabled?
5. Can ad cooldown be changed remotely?
6. Can paywall frequency be changed remotely?
7. Can logic be changed by country?
8. Can logic be changed by app version?
9. Can logic be changed by new vs returning user?
10. Is there A/B test assignment?
11. Which optimizations can be done without release?
12. Which optimizations require a new release?

---

## 11. Version / Release Audit

Scan:

- Version config
- Build number
- Info.plist
- Gradle version
- Xcode project settings
- Git tags if available
- Changelog if available

Output:

| Item | Finding | File path | Confidence |
|---|---|---|---|

Answer:

1. Current app version.
2. Current build number.
3. Where version/build is configured.
4. Whether recent release dates can be mapped to commits.
5. Whether ad, paywall, analytics, or core flow files changed recently.
6. If release mapping cannot be confirmed, say so.

---

## 12. Analytics Report Plan

Based on the code audit, generate a report plan.

Do not use generic templates blindly.
Generate reports based on real app paths.

Output:

| Priority | Report name | Platform | Report type | Configuration | Date range | Purpose | Notes |
|---|---|---|---|---|---|---|---|

### 12.1 Product Analytics Reports

For Firebase / GA4 / Amplitude / Mixpanel-like tools, recommend:

- Dashboard overview
- Events list
- Pages and screens
- Retention / cohort
- First launch funnel
- Core feature funnel
- Separate branch funnels
- Permission path
- Result page previous path
- Result page next path
- Paywall previous path
- Paywall next path
- Ad wrapper previous / next path
- Completion page previous path

Specify:

- Funnel steps
- Start point
- End point
- Dimensions
- Filters
- Which pages should not be included
- Which assumptions are unverified

### 12.2 Ad Monetization Reports

For AdMob / MAX / ironSource / TopOn-like tools, recommend:

- Ad unit summary
- Date + ad unit
- Country + ad unit
- Ad format summary
- Country + ad format
- Mediation source
- Requests
- Matches
- Impressions
- Clicks
- CTR
- eCPM
- Fill rate
- Match rate
- Estimated revenue

Explain what each report answers.

### 12.3 Store Reports

For App Store Connect / Google Play Console, recommend:

- Source type
- Country / territory
- Product page views
- First-time downloads
- Redownloads
- Conversion rate
- Store search / browse
- Sales and trends
- Subscription events
- Refunds
- Developer proceeds
- App version if available

Explain what each report answers.

### 12.4 Attribution Reports

For Adjust / AppsFlyer-like tools, recommend:

- Media source performance
- Campaign performance
- Adset / creative performance
- Country performance
- Cost
- CPI
- Installs
- Sessions
- Events
- Ad revenue
- IAP revenue
- Cohort revenue
- Retention
- ROAS
- Fraud / rejected installs

Explain what each report answers.

---

## 13. Final Markdown Output Structure

Output the final audit report using this structure:

# App Analytics Code Audit Report

## 1. Executive Summary

Use no more than 10 bullets.

## 2. Screen and Business Path Map

Include the screen meaning table.

## 3. Launch Path

Include first-time and returning user paths.

## 4. Core Feature Paths

Separate features. Do not merge unrelated branches.

## 5. Permission Flows

Show permission request, allow path, deny path.

## 6. Ad Trigger Rules

Separate App Open, Interstitial, Rewarded, Native, Banner.

## 7. Paywall Trigger Rules

Show paywall source, close path, purchase success path.

## 8. Entitlements

Show free vs Pro / VIP behavior.

## 9. Analytics Events

Show existing events, missing events, and suggested events.

## 10. Remote Config and A/B Capabilities

Show what can be adjusted without release.

## 11. Version / Release Notes

Show current version and release mapping limits.

## 12. Valid Funnels

List funnels that should be built.

## 13. Invalid Funnel Assumptions

List funnels or screen sequences that should not be used.

## 14. Report Checklist

List Firebase / Product Analytics, Ad Monetization, Store, Subscription, Attribution, and Stability reports needed.

## 15. Data Analysis Risks

Explain what would be misread if the code audit is ignored.

## 16. Next Steps

Use P0 / P1 / P2.

---

## 14. Output Requirements

- Output Markdown.
- Use tables wherever useful.
- Keep conclusions factual.
- Every important conclusion must have code evidence.
- Do not output secrets.
- Do not output full source files.
- Quote only short code summaries.
- Mark uncertainty clearly.
- Do not propose report funnels that contradict the code path.
- Do not treat screen names as business truth without code evidence.
