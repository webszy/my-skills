# Skills For Webszy

This collection includes CDF, a controlled AI development workflow, alongside other AI coding-agent skills.

## CDF Suite

The CDF Suite has one user-facing Skill: **CDF**.

CDF analyzes the requirement and repository evidence, classifies risk, builds and locks a development plan, requires human approval, then either executes the approved work or compiles it into a resumable task.

```text
Requirement / PRD / Development Request
    -> CDF
    -> Requirement Understanding
    -> Evidence Inspection
    -> Risk Classification
    -> Development Plan
    -> Scope Lock
    -> Human Approval
    -> Execute Now | Save as Task
```

CDTask is an internal CDF component used only after an approved plan is saved as a task. It is not installed or invoked separately.

Read the guides:

- [CDF Skill](skills/cdf/SKILL.md)
- [CDF README](skills/cdf/README.md)

Install for Codex:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -g -y
```

Install for Claude Code:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a claude-code -g -y
```

Install for both:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -a claude-code -g -y
```

### Version Semantics

- **CDF Suite maturity:** v0.1
- **Skill package version:** 1.1.0

These are separate version systems: maturity describes the CDF architecture, while the package version describes the distributable release. This refactor keeps the existing package version.

Repository metadata: [skill.json](skill.json)

## app-analytics-audit-flow

`app-analytics-audit-flow` is a code-first Skill for mobile app growth, monetization, subscription, attribution, store, and stability analysis.

Read the full guide: [skills/app-analytics-audit-flow/README.md](skills/app-analytics-audit-flow/README.md)

Skill metadata: [skills/app-analytics-audit-flow/skill.json](skills/app-analytics-audit-flow/skill.json)

```bash
npx skills add https://github.com/webszy/my-skills --skill app-analytics-audit-flow -a codex -a claude-code -g -y
```
