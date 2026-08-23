# 水煮鱼 Skill

本合集包含受控 AI 开发工作流 CDF，以及其它 AI Coding Agent Skills。

## CDF Suite

CDF Suite 现在只有一个面向用户的 Skill：**CDF**。

CDF 会分析需求与仓库证据、判断风险、生成并锁定开发计划、要求人工批准，然后执行已批准的工作，或将其编译为可恢复任务。

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

CDTask 是 CDF 的内部 component，仅在已批准计划选择保存为任务后使用。它不单独安装，也不单独调用。

查看说明：

- [CDF Skill](skills/cdf/SKILL.md)
- [CDF 中文 README](skills/cdf/README.zh-CN.md)

安装到 Codex：

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -g -y
```

安装到 Claude Code：

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a claude-code -g -y
```

同时安装：

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -a claude-code -g -y
```

### 版本语义

- **CDF Suite maturity：** v0.1
- **Skill package version：** 1.1.0

两者是不同的版本体系：maturity 表示 CDF 架构成熟度，package version 表示可分发版本。本次重构保持现有 package version。

合集元数据：[skill.json](skill.json)

## app-analytics-audit-flow

`app-analytics-audit-flow` 是一个 code-first 的移动 App 增长、变现、订阅、归因、商店和稳定性分析 Skill。

查看完整说明：[skills/app-analytics-audit-flow/README.md](skills/app-analytics-audit-flow/README.md)

Skill 元数据：[skills/app-analytics-audit-flow/skill.json](skills/app-analytics-audit-flow/skill.json)

```bash
npx skills add https://github.com/webszy/my-skills --skill app-analytics-audit-flow -a codex -a claude-code -g -y
```
