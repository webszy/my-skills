# Skills For Webszy

This collection includes the evolving Controlled Development Flow suite for controlled planning and tasking workflows, alongside other AI coding agent skills.

The currently available CDF Suite path is:

```text
Requirement → CDF → CDP → CDF → CDTask → CDF → READY_TO_EXECUTE
```

## cdf

`cdf` is the control-plane Skill that owns lifecycle state transitions and orchestrates the managed planning-to-tasking flow. The current integration stops before execution runtime.

Read the full guide: [skills/cdf/SKILL.md](skills/cdf/SKILL.md)

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -a claude-code -g -y
```

## cdp (controlled-development-planning)

`cdp` provides evidence-based, risk-aware planning with standalone and CDF-managed workflows.

Read the full guide: [skills/cdp/README.md](skills/cdp/README.md)

Repository metadata: [skill.json](skill.json)

Skill metadata: [skills/cdp/skill.json](skills/cdp/skill.json)

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a codex -a claude-code -g -y
```

## cdtask

`cdtask` turns stable requirements, approved standalone CDP handoffs, or CDF-managed approved plans into scoped, dependency-aware, verifiable execution units. It can optionally persist tasks, but it does not implement or schedule code itself.

Read the full guide: [skills/cdtask/SKILL.md](skills/cdtask/SKILL.md)

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
