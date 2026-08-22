---
name: google-analytics-integration
description: Integrate or repair Google Analytics 4 in an existing web project by detecting its stack, consulting current Google documentation, and adding minimal framework-appropriate tagging and event tracking. Use when the user asks to add GA4, Google Analytics, Google tag, gtag.js, page-view tracking, or GA4 business events to a repository.
---

# Google Analytics Integration

Integrate GA4 into the repository that is actually present. Inspect first, use current Google documentation as the source of truth, and make the smallest change that fits the project's architecture.

## Success Criteria

- The integration matches the detected framework, rendering mode, router, and environment-variable conventions.
- The Google tag loads once when a valid configured Measurement ID is available and remains inert when it is absent.
- Page views are correct for the routing model and are not counted twice.
- Any event wrapper is safe when GA is unavailable and matches the project's language and style.
- Only reliable, existing product actions receive business events; no personal data is sent.
- The final response reports evidence, changes, configuration, verification, and the next required input.

## Non-negotiable Rules

- Never guess the framework, router, rendering mode, package manager, build system, environment-variable prefix, or Measurement ID.
- Do not edit code until repository analysis and an integration design have been presented.
- Use only current official Google documentation for GA4 integration decisions. Do not rely on memory when documentation can be checked.
- Prefer the Google tag (`gtag.js`). Use Google Tag Manager only when the project already uses GTM or the user's requirements make GTM necessary.
- Do not introduce an analytics package when the existing stack can integrate the Google tag directly.
- Never hardcode a real Measurement ID in source code. A Measurement ID is not a secret, but it is deployment-specific configuration.
- Respect repository instructions, consent management, Content Security Policy, tests, formatting, and existing analytics behavior. Do not broaden the task into a privacy or analytics redesign without approval.

## Workflow

### 1. Analyze the Repository

Read applicable repository instructions first. Use the repository's preferred code-intelligence tools when available, and cite file paths for important conclusions.

Inspect, without modifying files:

- manifests and lockfiles to identify the package manager and installed versions;
- framework and build configuration for Nuxt, Next.js, React, Vue, Astro, Angular, vanilla HTML/JS, or another stack;
- application entry points, document/head templates, layouts, and deployment configuration;
- routing configuration and navigation hooks;
- SSR, SSG, hydration, client-only, or mixed rendering behavior;
- TypeScript or JavaScript conventions and existing shared utilities;
- existing GA, Google tag, GTM, Firebase Analytics, consent, cookie, or other analytics code;
- environment files and examples to determine public/client variable naming and access patterns;
- existing lint, typecheck, test, and build commands.

Do not infer a framework from directory names alone. Confirm it from dependencies and configuration. If the repository is a monorepo, identify the exact application in scope before designing the integration.

### 2. Research Current Google Guidance

Consult the official documentation relevant to the detected stack and behavior. Start with these official sources and follow their current linked guidance when needed:

- Google tag: <https://developers.google.com/tag-platform/gtagjs>
- Configure the Google tag: <https://developers.google.com/tag-platform/gtagjs/configure>
- GA4 events: <https://developers.google.com/analytics/devguides/collection/ga4/events>
- Single-page applications: <https://developers.google.com/analytics/devguides/collection/ga4/single-page-applications>
- Recommended events: <https://developers.google.com/analytics/devguides/collection/ga4/reference/events>
- DebugView: <https://support.google.com/analytics/answer/7201382>

Record the official pages that support the chosen approach. Treat repository-specific framework documentation as implementation context, not as a replacement for Google's GA4 guidance.

Choose the method using these constraints:

- Reuse a correctly installed Google tag or GTM container instead of adding a second loader.
- With an existing GTM setup, implement through its established data-layer conventions unless the user explicitly requests a migration.
- Without GTM, use the Google tag through the stack's supported head/script mechanism.
- For client-side routing, determine whether automatic page measurement already covers history changes. If manual page views are necessary, configure one authoritative path and prevent automatic/manual duplicates.
- For SSR or SSG, render or initialize through the framework-supported boundary and guard all browser globals.

### 3. Present the Integration Design

Before editing code, present an `## Analysis` section containing:

1. the detected stack, package manager, build system, router, rendering mode, analytics state, and environment convention, with repository evidence;
2. the selected Google tag or GTM method;
3. the exact files expected to change;
4. the environment-variable name and development behavior;
5. the official Google documentation supporting the design;
6. proposed events, separated into events safe to implement now and suggestions requiring product confirmation.

If a material ambiguity would change the files, privacy behavior, page-view semantics, or event meaning, ask a focused question before editing. Otherwise proceed with the stated design.

### 4. Implement the Minimal Integration

Follow the project's existing style and framework primitives.

- Add the loader exactly once.
- Read the Measurement ID through the project's client-visible environment convention. For example, the semantic setting may be `GA_MEASUREMENT_ID`, while a framework may require a public prefix or runtime-config mapping. Use the detected convention, not a universal name.
- Gracefully no-op when the value is absent or malformed. Do not emit noisy errors for an intentionally unconfigured development environment.
- Keep analytics disabled in development by default unless the repository already has a deliberate development or debug opt-in.
- Avoid accessing `window`, `document`, or `dataLayer` during server execution.
- Preserve an existing consent default and update flow. Do not cause tags to run before the project's consent policy allows them.
- Update an existing environment example when appropriate, but do not create or modify a committed file containing a real ID.
- Do not add unrelated refactors, formatting changes, dependencies, or analytics providers.

For page views, verify the exact behavior of the chosen setup. Do not combine an automatic initial `page_view`, enhanced-measurement history tracking, and a router listener unless the documented configuration explicitly prevents duplicates.

### 5. Add a Tracking API When Appropriate

Create a small `trackEvent(eventName, parameters)` abstraction when the project has multiple call sites, uses TypeScript, or benefits from centralizing browser and availability guards. Reuse a compatible existing analytics abstraction instead of creating another one.

The abstraction must:

- be a safe no-op during SSR, development-disabled mode, missing configuration, blocked consent, or unavailable GA;
- preserve useful TypeScript types when the project uses TypeScript;
- pass event parameters without adding implicit personal or sensitive data;
- remain provider-specific unless the repository already has a provider-neutral analytics interface.

Do not build a speculative analytics framework for a single call site.

### 6. Select Business Events from Existing Behavior

Understand the product from routes, UI actions, and success callbacks before proposing events. Prefer Google's recommended event names and required parameters when semantics match.

Examples are prompts, not a checklist:

- SaaS: `sign_up`, `login`, `purchase`, or a clearly defined subscription success event.
- Search/report products: events for submitted searches, completed results, or generated reports when those milestones are distinguishable in code.
- E-commerce: `view_item`, `add_to_cart`, `begin_checkout`, and `purchase` with the documented parameters.

Only wire an event where existing code proves the action completed. Do not infer success from a button click when an asynchronous operation can fail. Do not send names, email addresses, free-form user text, stable user identifiers, or other PII. Keep unimplemented event ideas in the report as suggestions.

### 7. Validate

After implementation, follow repository instructions and run the smallest relevant existing checks when execution is permitted:

- formatting or lint checks for changed files;
- TypeScript/type checks when applicable;
- focused tests, then the existing build if proportionate to the change.

If repository or user instructions prohibit running commands after modification, do not run them; provide the exact commands and manual steps for the user instead.

Also explain how to verify behavior:

1. configure a test Measurement ID in the identified local environment file;
2. start the app using its documented command;
3. confirm the Google tag request and GA collection request in browser developer tools;
4. navigate through client-side routes and confirm one page view per intended navigation;
5. trigger each implemented event and inspect its parameters;
6. use GA4 Realtime and DebugView, allowing for product latency and consent/ad-blocking effects;
7. repeat without the ID and confirm the app has no runtime errors and sends no GA requests.

Do not claim that an event reached GA solely because the local wrapper was called.

### 8. Request the Measurement ID Last

Do not ask for a Measurement ID at the beginning. Ask only after repository analysis is complete, the integration code is prepared, and the correct environment location is known.

If the ID is still missing, use this exact request under `## Next step`:

> Please provide your Google Analytics Measurement ID (G-XXXXXXXX). I will configure it in the environment settings.

Do not insert a guessed or placeholder ID into active runtime configuration.

## Final Output

Always use these headings:

## Analysis

Summarize the detected stack, repository evidence, selected method, event decisions, and official-documentation rationale.

## Changes

List every modified file and its purpose. If no code was changed, say why.

## Configuration

Give the exact environment-variable name, file or deployment setting, expected format, and development behavior. Do not expose unrelated environment values.

## Verification

Report checks actually run separately from checks not run, then provide GA network, Realtime, and DebugView verification steps.

## Next step

Request the missing Measurement ID only when the integration is ready, using the required sentence above. If it is already configured, state the next concrete verification action instead.
