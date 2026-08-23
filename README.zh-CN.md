# 水煮鱼 Skills

本仓库包含受控 AI 开发工作流 CDF，以及其它 AI Coding Agent Skills。

## CDF：Controlled Development Flow

CDF 是 CDF Suite 中唯一面向用户的 Skill，负责完整的受控开发路径：

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

CDF 让小改动保持轻量，同时对高风险、敏感、跨域或架构级工作施加更严格的控制。所有开发路径——包括“把这个 PRD 拆成任务”——都必须先完成仓库检查、计划、Scope Lock 和审批，才能进入实现或任务编译。

| 用户动作 | 结果 |
|---|---|
| **Execute Now** | 只实施已批准范围，并只报告实际执行过的验证 |
| **Save as Task** | 将已批准计划编译为可恢复的 `_cdtask` 文档，验证保存结果、返回路径并停止 |

CDTask 是 CDF 内部的 post-approval component，不是独立 Skill、安装目标或用户入口。

已保存任务必须通过 CDF 恢复：

```text
$cdf continue task <path>
```

继续前，CDF 会验证 task contract、Scope Lock 与 Approval Record 完整性、当前仓库状态、假设、停止条件和 material drift。

CDF 配置为显式调用。常用形式包括 `$cdf`、`/cdf`、`cdf:` 和 `controlled-development-flow`。

完整文档：

- [CDF 运行规则](skills/cdf/SKILL.md)
- [CDF English Guide](skills/cdf/README.md)
- [CDF 中文指南](skills/cdf/README.zh-CN.md)

### 安装

Codex：

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -g -y
```

Claude Code：

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

两者是不同的版本体系。Suite maturity 表示 CDF 架构成熟度，package version 表示可分发版本。

合集元数据：[skill.json](skill.json)

## app-analytics-audit-flow

`app-analytics-audit-flow` 是一个 code-first 的移动 App 增长、变现、订阅、归因、商店和稳定性分析 Skill。

- [使用指南](skills/app-analytics-audit-flow/README.md)
- [Skill 元数据](skills/app-analytics-audit-flow/skill.json)

```bash
npx skills add https://github.com/webszy/my-skills --skill app-analytics-audit-flow -a codex -a claude-code -g -y
```
