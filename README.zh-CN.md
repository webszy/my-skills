# 水煮鱼 Skill

本合集包含持续演进的 Controlled Development Flow Suite，用于受控的规划与任务化流程，同时也收录其它 AI Coding Agent Skills。

当前已可用的 CDF Suite 路径是：

```text
Requirement → CDF → CDP → CDF → CDTask → CDF → READY_TO_EXECUTE
```

# cdf

`cdf` 是负责生命周期状态转换的控制平面 Skill，编排 managed planning-to-tasking 流程。当前集成在 execution runtime 之前停止。

查看完整说明：[skills/cdf/SKILL.md](skills/cdf/SKILL.md)

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -a claude-code -g -y
```

# cdp

`cdp` 是 `controlled-development-planning` 的简称，提供基于证据、风险感知的 standalone 与 CDF-managed 开发规划工作流。

查看完整说明：[skills/cdp/README.zh-CN.md](skills/cdp/README.zh-CN.md)

合集元数据：[skill.json](skill.json)

Skill 元数据：[skills/cdp/skill.json](skills/cdp/skill.json)

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a codex -a claude-code -g -y
```

# cdtask

`cdtask` 将稳定需求、已批准的 standalone CDP 交接包或 CDF-managed approved Plan，转化为边界清晰、依赖明确、可验证的执行单元。它可以按需持久化任务，但自身不实现或调度代码。

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
