# 水煮鱼 Skills

本仓库包含受控 AI 开发工作流 CDF，以及其它 AI Coding Agent Skills。

## CDF：Controlled Development Flow

CDF 是 CDF Suite 中唯一面向用户的入口，负责完整的受控开发路径：

```text
Requirement / PRD / Development Request
    -> Requirement Gate
    -> Requirement Understanding
    -> Repository Evidence Inspection
    -> Risk Classification
    -> Development Plan
    -> cdf-scope/v1 Scope Lock
    -> Human Approval
    -> Execute Now | Save as Task
```

CDF 让小改动保持轻量，同时对高风险、敏感、跨域或架构级工作施加更严格的控制。所有开发路径——包括“把这个 PRD 拆成任务”——都必须先完成仓库检查、风险分级、计划、Scope Lock 和审批，才能进入实现或任务编译。S/M/L/XL 风险模型保持不变。

| 用户动作 | 结果 |
|---|---|
| **Execute Now** | 只实施已批准范围，并只报告实际执行过的验证 |
| **Save as Task** | 编译并验证可恢复的 `_cdtask` 文档，返回路径后停止；该批准只授权持久化 |

任务编译是 CDF 内部 component，不存在顶层任务 Skill、独立安装目标或独立调用入口。

### 合同要点

- Development Plan 按固定顺序使用这些规范标题：`Requirement Understanding`、`Evidence Summary`、`Risk Gate Result`、`Scope Lock`、`Technical Approach`、`Implementation Plan`、`Risks`、`Rollback Plan`、`Acceptance Criteria`、`Verification Strategy` 和 `Next Action`。
- 唯一的 `cdf-scope/v1` 区块是范围的唯一规范授权源，其中的 `acceptance_criteria` 字段是验收标准的唯一规范源。Development Plan 的 `Acceptance Criteria` 只是逐项、同序、逐字投影。
- 部分批准时，`Partial Approval Result` 只是已批准项与未批准项的审计投影；它不复制完整 Scope Lock，也不产生第二个授权源。
- 保存前，CDF 会执行 drift preflight，并记录当前 `Workspace`、`Source-Branch`、`Source-Commit`、`Source-Worktree-State` 和相关的 `Source-Worktree-Changes`。Material drift 必须返回规划并重新审批。
- Scope Lock 与 Approval Record 的 SHA-256 使用确定性序列化：UTF-8 编码、LF 换行、排除 Markdown 围栏分隔符、内容行不得有尾随空白，并且恰好包含一个尾随 LF。

已保存任务必须通过 CDF 恢复：

```text
$cdf continue task <path>
```

CDF 会验证 task contract 和必需区块、完整性摘要、当前仓库状态、假设、停止条件及 material drift。验证成功后，显式 continue 请求会创建本回合的 `Resume Authorization Record`；只有此后才能执行已保存工作。仅检查、审阅、总结或验证任务不授权执行。

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
