# Requirement Gate

## Table of Contents
- Purpose
- When to read this file
- Ask Classification
- Definition Card
- Gap List and Minimal Questions
- Suggested Defaults / Fast Path
- Post-clarification outcomes
- High-Risk Areas
- Requirement Gate vs Level S / L / XL
- Clarification Response Template
- Requirement Spec Output
- Implementation Brief Output
- Acceptance Criteria Patterns
- Examples

## Purpose

Use this file when a request is vague, underspecified, or high-risk. The goal is to reach executable clarity before the CDF workflow chooses a risk level.

Requirement Gate is an entrance check, not a replacement for Target Existence Check, Requirement Understanding, Requirement Decomposition, Risk Classification, Evidence-Based Thinking, Approval, Verification, or Traceability.

## When to read this file

Read this file when:

- The user request is unclear.
- The request could mean more than one task type.
- The request lacks acceptance criteria.
- The request touches a high-risk area.
- The request asks for a spec, PRD, implementation brief, diagnosis, decision memo, or research brief.

## Ask Classification

Classify the request lightly before asking questions:

1. Delivery
   - The user wants a concrete deliverable, feature, page, API, component, document, or Codex prompt.
   - Clarify goal, scope, inputs, deliverable, and acceptance criteria.
2. Diagnosis
   - The user wants to find a cause for a symptom.
   - Clarify symptom, data, reproduction path, impact range, and existing evidence.
3. Decision
   - The user wants to choose between options.
   - Clarify options, constraints, evaluation metrics, and tradeoff criteria.
4. Research
   - The user wants exploration or synthesis.
   - Clarify research scope, source requirements, output format, and confidence expectations.

## Definition Card

When the requirement is unclear, summarize the current understanding with a compact definition card before asking questions.

Fields:

- One-line Definition:
  - What to do + for whom or which system + why.
- Goal:
  - Expected outcome or changed state.
- Actor / System:
  - User, role, module, service, page, workflow, or external system affected.
- Scope:
  - In scope.
  - Out of scope.
- Current Behavior:
  - What happens now.
- Expected Behavior:
  - What should happen.
- Inputs:
  - Existing files, screenshots, APIs, data, examples, designs, logs, metrics, or user-provided facts.
- Constraints:
  - Technical, business, security, compatibility, cost, performance, or timeline constraints.
- Acceptance:
  - Verifiable completion criteria.
- Risk Signals:
  - Money, data, auth, permissions, production config, reports, third-party API, migration, architecture, etc.

Keep the card short. Do not turn simple tasks into PRDs.

## Gap List and Minimal Questions

When the requirement is unclear:

- List the gaps before asking questions.
- Include only gaps that affect implementation direction, risk level, interfaces, data, state, or acceptance.
- Ask at most 5 questions per round.
- Prefer multiple choice, either/or, and fill-in questions.
- Make questions quick to answer.
- Avoid broad questions like "What do you want?"
- Include a recommended default when a safe default exists.
- If the user replies "use your recommendation", "按你的建议来", or "按默认方案", treat the recommended defaults as explicit assumptions and continue.
- Do not chase perfect requirements indefinitely. The goal is executable clarity, not a complete PRD.

Example question format:

```md
## Questions

1. What is the main goal?
   - A. Fix an existing bug
   - B. Add a new feature
   - C. Improve an existing experience
   - D. Refactor internal implementation
   - Recommended: B

2. What should this task include?
   - A. Frontend display only
   - B. Frontend interaction + local state
   - C. Frontend and backend API changes
   - D. Database / jobs / permissions or other backend changes
   - Recommended: A

3. Which acceptance style fits best?
   - A. UI displays correctly
   - B. User can complete a specific flow
   - C. A metric improves
   - D. Tests / logs / data checks pass
   - Recommended: B
```

## Suggested Defaults / Fast Path

When information is missing but a safe, common, reversible default can move the work forward, provide suggested defaults.

Suggested defaults must be:

- Safe.
- Reversible.
- Narrow in scope.
- Not high-risk.
- Not a hidden data model change.
- Not a hidden payment, subscription, permission, or production configuration change.
- Enough to move the task to prototype, validation, or a small implementation step.

Use this format:

```md
## Suggested Defaults

If you want to move quickly, I suggest these defaults:

- Scope: V1 only, covering ...
- Data: No database changes; use existing fields ...
- API: No new API; reuse ...
- UI: Follow the existing design system ...
- Acceptance: Treat ... as done when ...

If you reply "use the defaults", I will treat these as explicit assumptions and continue into CDF risk classification.
```

Defaults are not silent assumptions. State them. Do not use defaults to bypass high-risk confirmation.

## Post-clarification outcomes

After clarification:

- Delivery: if the task is an implementation request, continue into the CDF workflow. If the user only wants a deliverable such as a spec or brief, stop after producing that artifact.
- Diagnosis: return a diagnosis summary, likely causes, evidence gaps, and recommended next checks. Only continue into implementation if the user turns it into a fix request.
- Decision: return a recommendation or decision memo. Only continue into implementation if the chosen option becomes an implementation task.
- Research: return a research brief or synthesis. Only continue into implementation if the user converts the result into a build request.

## High-Risk Areas

Use this list as the single source of truth for high-risk checks:

- Database schema, migrations, destructive data changes, or data backfills.
- Payment, billing, subscription, IAP, paywall, or pricing logic.
- Revenue, cost, ROI, reports, analytics, or business metric logic.
- Authentication, authorization, permissions, or user data.
- Scheduled tasks, cron jobs, sync jobs, queues, retries, or idempotency.
- Cache invalidation, events, webhooks, or message consumers.
- Third-party API integrations.
- CDN delivery, static asset delivery, or release packaging.
- Production configuration, deployment configuration, or environment variables.
- Architecture changes, new modules, major refactors, major data-flow redesign, or phased rollout.
- Localization, i18n, accessibility, or compliance behavior.
- Security, privacy, or observability-sensitive behavior.

## Requirement Gate vs Level S / L / XL

- Level S should stay fast when the request is already clear, low-risk, and easy to verify.
- If a request is vague, use Requirement Gate first, even for Level S.
- If a request touches any High-Risk Areas item and is incomplete, clarify before Level L or Level XL.
- If a request is clear and high-risk, continue into Level L.
- If a request is clear and architecture-level, cross-module, or phased, continue into Level XL.
- Do not use defaults to bypass high-risk confirmation.

## Clarification Response Template

Use the user's language. If the user writes in Chinese, respond in Chinese. If the user writes in English, respond in English.

English template:

```md
I need to clarify the requirement before choosing a CDF workflow level.

## Ask Type
- Delivery / Diagnosis / Decision / Research

## Current Understanding
- ...

## Definition Card
- One-line Definition:
- Goal:
- Actor / System:
- Scope:
  - In:
  - Out:
- Current Behavior:
- Expected Behavior:
- Inputs:
- Constraints:
- Acceptance:
- Risk Signals:

## Missing / Ambiguous
- ...

## Questions
1. ...
2. ...
3. ...

## Suggested Defaults
- ...
```

Chinese template:

```md
在进入 CDF 风险分级和实现前，我需要先把需求澄清一下。

## 需求类型
- 交付型 / 诊断型 / 决策型 / 研究型

## 我目前理解的需求
- ...

## 需求定义卡
- 一句话定义：
- 目标：
- 使用者 / 影响系统：
- 范围：
  - 本次包含：
  - 本次不包含：
- 当前行为：
- 期望行为：
- 输入信息：
- 约束：
- 验收标准：
- 风险信号：

## 还不清楚的关键点
- ...

## 需要你确认的问题
1. ...
2. ...
3. ...

## 如果你想快速推进，我建议默认这样定
- ...
```

## Requirement Spec Output

When the user explicitly asks to organize requirements, output a requirement document, generate a spec or PRD, create development instructions for Codex, or turn an idea into a task, cdf may output a structured Requirement Spec.

Template:

```md
# Requirement Spec

## 1. Background
...

## 2. Goal
...

## 3. Ask Type
- Delivery / Diagnosis / Decision / Research

## 4. Target User / Actor / System
...

## 5. Scope

### In Scope
- ...

### Out of Scope
- ...

## 6. Current Behavior
...

## 7. Expected Behavior
...

## 8. User Flow / System Flow
...

## 9. Functional Requirements
- ...

## 10. Non-functional Requirements
- Performance:
- Security:
- Compatibility:
- Reliability:
- Accessibility:
- Observability:

## 11. Data / API / State Impact
- ...

## 12. Constraints
- ...

## 13. Edge Cases
- ...

## 14. Acceptance Criteria
- ...

## 15. Open Questions
- ...

## 16. Implementation Notes
- ...
```

## Implementation Brief Output

When the user asks to generate a Codex prompt, hand work to a coding agent, or produce implementation instructions, output an Implementation Brief only after the requirement has passed Requirement Gate.

Template:

```md
# Implementation Brief

## Task
...

## Context
...

## Ask Type
- Delivery / Diagnosis / Decision / Research

## Confirmed Requirements
- ...

## Assumptions
- ...

## Files / Modules Likely Involved
- ...

## Scope

### In Scope
- ...

### Out of Scope
- ...

## Constraints
- ...

## Risk Level
- Level S / M / L / XL
- Reason:

## Acceptance Criteria
- ...

## Suggested Steps
1. ...

## Do Not Do
- ...

## Verification
- ...

## Remaining Questions
- ...
```

## Acceptance Criteria Patterns

For normal tasks, use checklist acceptance criteria:

```md
- [ ] ...
- [ ] ...
- [ ] ...
```

For behavior-heavy tasks, use Given / When / Then:

```md
- Given ...
- When ...
- Then ...
```

Use checklist criteria for simple tasks. Use Given / When / Then for flow, permission, state, and API behavior. Do not force Gherkin onto every task.

## Examples

### Example 1: Clear Level S

```md
User:
Change the submit button text from "Send" to "Submit".

Agent:
Understanding: Change only the submit button label. No behavior change.
Risk: Level S.
Proceed with direct edit.
```

### Example 2: Unclear optimization request

```md
User:
Optimize the login page.

Agent:
This is unclear. It could mean UI style, loading speed, validation behavior, auth flow, conversion tracking, or copy.
```

### Example 3: High-risk vague request

```md
User:
Improve subscription conversion.

Agent:
This touches money / subscription / metrics. Requirement Gate must clarify:
- target metric.
- funnel step.
- current data.
- experiment scope.
- pricing / paywall constraints.
- acceptance criteria.

Do not directly modify paywall or pricing logic.
```

### Example 4: User accepts defaults

```md
User:
按你的默认方案来。

Agent:
Treat suggested defaults as explicit assumptions, restate them, then continue into the CDF workflow.
```

