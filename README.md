# Skills For Webszy

## cdp(controlled-development-planning)
                    /cdp
                     │
                 Orchestrator
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
       CDP         CDTask      Flow State
        │            │
      Plan         Tasks
                     │
                  CDRunner
                     │
               Executor Agent
                     │
                   Diff
                     │
                  CDReview
                     │
              Reviewer Agent
                     │
                Fix / Pass
`cdp` is short for `controlled-development-planning`, which is a risk-based development workflow Skill for AI Coding Agents.

Read the full guide: [skills/cdp/README.md](skills/cdp/README.md)

Repository metadata: [skill.json](skill.json)

Skill metadata: [skills/cdp/skill.json](skills/cdp/skill.json)

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a codex -a claude-code -g -y
```

## cdtask

`cdtask` turns stable requirements, PRDs, technical proposals, or approved CDP handoff packages into scoped, reviewable, dependency-ordered task breakdowns for coding agents. It can save a local task for deferred execution, but it does not implement code itself.

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
