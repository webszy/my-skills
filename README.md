# Webszy Skills

This repository contains CDF, a controlled AI development workflow, alongside other AI coding-agent skills.

## CDF: Controlled Development Flow

CDF is the only user-facing Skill in the CDF Suite. It owns the complete controlled-development path:

```text
Requirement / PRD / Development Request
    -> Requirement Understanding
    -> Repository Evidence Inspection
    -> Risk Classification
    -> Development Plan
    -> cdf-scope/v1 Scope Lock
    -> Human Approval
    -> Execute Now | Save as Task
```

CDF keeps small changes lightweight while applying stronger controls to risky, sensitive, cross-cutting, or architectural work. Every development path—including “turn this PRD into tasks”—must complete repository inspection, planning, Scope Lock, and approval before implementation or task compilation.

| User action | Result |
|---|---|
| **Execute Now** | Implement only the approved scope and report verification actually performed |
| **Save as Task** | Compile the approved plan into a resumable `_cdtask` document, verify the saved artifact, return its path, and stop |

CDTask is an internal post-approval CDF component. It is not a separate Skill, installation target, or user entry point.

Resume a saved task through CDF:

```text
$cdf continue task <path>
```

CDF validates the task contract, Scope Lock and Approval Record integrity, current repository state, assumptions, stop conditions, and material drift before continuing.

CDF is configured for explicit invocation. Common forms include `$cdf`, `/cdf`, `cdf:`, and `controlled-development-flow`.

Read the full documentation:

- [CDF operating rules](skills/cdf/SKILL.md)
- [CDF guide](skills/cdf/README.md)
- [CDF 中文指南](skills/cdf/README.zh-CN.md)

### Installation

Codex:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -g -y
```

Claude Code:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a claude-code -g -y
```

Both:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -a claude-code -g -y
```

### Version Semantics

- **CDF Suite maturity:** v0.1
- **Skill package version:** 1.1.0

These are separate version systems. Suite maturity describes the CDF architecture; package version describes the distributable release.

Repository metadata: [skill.json](skill.json)

## app-analytics-audit-flow

`app-analytics-audit-flow` is a code-first Skill for mobile app growth, monetization, subscription, attribution, store, and stability analysis.

- [Guide](skills/app-analytics-audit-flow/README.md)
- [Skill metadata](skills/app-analytics-audit-flow/skill.json)

```bash
npx skills add https://github.com/webszy/my-skills --skill app-analytics-audit-flow -a codex -a claude-code -g -y
```
