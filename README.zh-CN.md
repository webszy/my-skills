# 水煮鱼 Skill

本合集包含持续演进的 Controlled Development Flow Suite，用于受控的规划与任务化流程，同时也收录其它 AI Coding Agent Skills。

当前已可用的 CDF Suite 路径是：

```text
Requirement
  → CDF 评估
  → CDP 规划 + Scope Lock
  → Human Plan Approval（由 CDP 执行）
  → CDF 交接前置条件检查
  → 选用 CDTask 时生成任务定义
  → 可交接的 Task Definition，或 Approved Plan Package
```

CDTask 是可选的：当已批准的工作无需任务拆解时，Approved Plan Package 就是终态输出。执行不在当前套件范围内。

# cdf

`cdf` 是控制平面 Skill，负责评估请求是否进入受控流程、按契约字段路由各组件的返回结果，并执行保护已批准范围的交接前置条件。它不持有持久状态，在交接处停止；执行、验证和 Review 都不在 v0.1 范围内。

查看完整说明：[skills/cdf/README.zh-CN.md](skills/cdf/README.zh-CN.md)

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -a claude-code -g -y
```

# cdp

`cdp` 是 `controlled-development-planning` 的简称，提供基于证据、风险感知的 standalone 与 CDF-managed 开发规划工作流，并在两种上下文下都负责人工审批门禁。

查看完整说明：[skills/cdp/README.zh-CN.md](skills/cdp/README.zh-CN.md)

合集元数据：[skill.json](skill.json)

Skill 元数据：[skills/cdp/skill.json](skills/cdp/skill.json)

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a codex -a claude-code -g -y
```

# cdtask

`cdtask` 将稳定需求、已批准的 standalone CDP 交接包或 CDF-managed approved Plan，转化为边界清晰、依赖明确、可验证的任务定义与执行方交接信息。它可以按需持久化一份可恢复的任务文档，但不执行、不调度、不 Review。

查看完整说明：[skills/cdtask/README.zh-CN.md](skills/cdtask/README.zh-CN.md)

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
