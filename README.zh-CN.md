# 水煮鱼 Skill

# cdp

`cdp` 是 `controlled-development-planning`的简称。这是一个面向 AI Coding Agent 的风险分级开发工作流 Skill。

查看完整说明：[skills/cdp/README.zh-CN.md](skills/cdp/README.zh-CN.md)

合集元数据：[skill.json](skill.json)

Skill 元数据：[skills/cdp/skill.json](skills/cdp/skill.json)

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a codex -a claude-code -g -y
```

# cdtask

`cdtask` 将稳定的需求文档、PRD、技术方案或已批准的 CDP 交接包，转化为边界清晰、可评审、按依赖排序的 Coding Agent 任务拆分。它可以保存待后续执行的本地 task，但自身不修改代码。

查看完整说明：[skills/cdtask/SKILL.md](skills/cdtask/SKILL.md)

```bash
npx skills add https://github.com/webszy/my-skills --skill cdtask -a codex -a claude-code -g -y
```

# app-analytics-audit-flow

`app-analytics-audit-flow` 是一个 code-first 的移动 App 增长、变现、订阅、归因、商店和稳定性分析 Skill。

查看完整说明：[skills/app-analytics-audit-flow/README.md](skills/app-analytics-audit-flow/README.md)

Skill 元数据：[skills/app-analytics-audit-flow/skill.json](skills/app-analytics-audit-flow/skill.json)

```bash
npx skills add https://github.com/webszy/my-skills --skill app-analytics-audit-flow -a codex -a claude-code -g -y
```
