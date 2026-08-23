# Skills For Webszy

This collection includes the evolving Controlled Development Flow suite for controlled planning and tasking workflows, alongside other AI coding agent skills.

The currently available CDF Suite path is:

```text
Requirement
  → CDF assessment
  → CDP planning + Scope Lock
  → Human Plan Approval (run by CDP)
  → CDF handoff preconditions
  → CDTask definition, when selected
  → Handoff-ready Task Definition, or the Approved Plan Package
```

CDTask is optional: when the approved work gains nothing from task decomposition, the Approved Plan Package is the terminal output. Execution is outside the current suite.

## cdf

`cdf` is the control-plane Skill that assesses whether a request enters the controlled flow, routes each component return on contract fields, and enforces the handoff preconditions that protect approved scope. It holds no persistent state and stops at the handoff; execution, verification, and review are outside v0.1.

Read the full guide: [skills/cdf/README.md](skills/cdf/README.md)

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -a claude-code -g -y
```

## cdp (controlled-development-planning)

`cdp` provides evidence-based, risk-aware planning with standalone and CDF-managed workflows. It also owns the human approval gate in both contexts.

Read the full guide: [skills/cdp/README.md](skills/cdp/README.md)

Repository metadata: [skill.json](skill.json)

Skill metadata: [skills/cdp/skill.json](skills/cdp/skill.json)

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a codex -a claude-code -g -y
```

## cdtask

`cdtask` turns stable requirements, approved standalone CDP handoffs, or CDF-managed approved plans into scoped, dependency-aware, verifiable task definitions and executor handoff information. It can optionally persist a resumable task document, but it does not execute, schedule, or review work.

Read the full guide: [skills/cdtask/README.md](skills/cdtask/README.md)

```bash
npx skills add https://github.com/webszy/my-skills --skill cdtask -a codex -a claude-code -g -y
```

## app-analytics-audit-flow

`app-analytics-audit-flow` is a code-first Skill for mobile app growth, monetization, subscription, attribution, store, and stability analysis.

Read the full guide: [skills/app-analytics-audit-flow/README.md](skills/app-analytics-audit-flow/README.md)

Skill metadata: [skills/app-analytics-audit-flow/skill.json](skills/app-analytics-audit-flow/skill.json)

```bash
npx skills add https://github.com/webszy/my-skills --skill app-analytics-audit-flow -a codex -a claude-code -g -y
```
