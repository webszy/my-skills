# CDP：Controlled Development Planning

## 快速理解

CDP 将不清晰的开发需求转化为基于证据、感知风险的计划，并通过 Scope Lock 锁定范围，形成明确的人工决策点。

> Small changes should be fast. Risky changes should be controlled.

CDP 负责规划和推荐下一步，不是 Runtime Controller、调度器或自动 Review 系统。

## 在 CDF Suite 中的位置

```text
CDF — 控制平面、返回路由、交接前置条件
 ↓
CDP — 需求分析、证据、风险、Scope Lock、计划
 ↓
Human Plan Approval — 两种上下文下均由 CDP 执行
 ↓
standalone：  Execute Now | Save as CDTask
cdf-managed： Return Approved Plan Package to CDF
```

- **CDF** 以 managed 模式调用 CDP，按契约字段路由返回结果，并执行交接前置条件检查。它不运行审批门禁。
- **CDP** 负责规划、风险决策、Scope Lock、审批材料，以及人工审批门禁本身 —— 展示计划、判断回复是否构成有效批准、必要时追问。
- **CDTask** 按需将已批准计划转化为可验证任务定义。

规范 Scope Lock 必须在全部交接中原样复制。`cdf-managed` 模式下，CDP 不调用 CDTask，也不实现代码。

## 核心职责与边界

CDP 负责：

- 需求理解与拆解；
- 证据检查与冲突处理；
- S/M/L/XL 风险分级；
- Development Plan 与验证策略；
- 规范 `cdp-scope/v1` Scope Lock；
- 完整、带条件和部分审批材料；
- Next Action 推荐。

CDP 不负责：

- CDF 生命周期编排；
- CDTask 任务拆解；
- 调度或 Runtime 管理；
- 审批前自动实现或持久化；
- 实现 Review。

## 工作流程

```text
Requirement Gate
  → 理解并拆解需求
  → 检查证据
  → 运行升级信号 Checklist
  → 符合条件时运行 S 或 M Reverse Check
  → 确定最终风险等级
  → 创建 Development Plan 与 Scope Lock
  → 获得明确批准
  → 请求用户选择 Next Action
```

对于模糊、不完整、高风险或规格类需求，使用 [Requirement Gate](references/requirement-gate.md)。规划对现有目标的修改前，必须确认该目标确实存在。

## 风险控制

CDP 使用可检查规则，而不是根据表面观感或 diff 大小判断风险。

| 等级 | 判定条件 | 规划控制 |
|---|---|---|
| **S** | 单个局部静态目标；升级清单全部 `CLEAR`；S Reverse Check 全部 `PASS` | 精简计划、有效批准与明确动作选择 |
| **M** | 单个边界明确且影响已知的流程；升级清单全部 `CLEAR`；M Reverse Check 全部 `PASS` | 基于证据的简短计划、有效批准与明确动作选择 |
| **L** | 命中共享、条件、持久化、敏感、生产、集成或证据风险信号 | 详细计划与有效批准 |
| **XL** | 架构、新子系统、重大数据流、迁移或分阶段发布 | 设计、阶段边界与有效批准 |

风险等级只决定规划深度，不决定审批要求。任何等级在实现、持久化或交接前都必须获得有效批准并生成 Approval Record。

最终判为 S 或 M 前，必须逐项检查以下强制升级类别：

- 共享组件、主题系统、设计 token 和全局状态；
- 条件渲染、feature flag、角色、权限和 entitlement；
- 持久化数据、schema、迁移、支付、计费、认证和访问控制；
- 报表、分析、埋点、缓存、任务、队列、定时器和事件；
- 国际化、无障碍、合规、安全、隐私和可观测性；
- 配置、部署、生产设置、第三方契约和发布交付；
- 架构、模块、服务、迁移和分阶段发布；
- 证据不足或证据冲突。

每一行都必须记录 `CLEAR`、`HIT` 或 `UNKNOWN` 以及证据。任一 `HIT` 至少升级为 Level L；架构类信号通常升级为 XL。任一 `UNKNOWN` 都禁止判为 S/M。证据冲突改变计划含义时必须 `BLOCKED`。

完整可执行 Checklist 与输出格式见 [SKILL.md](SKILL.md)。这些是必须实际运行的门禁，不是参考清单。

## Scope Lock 与审批

每个可审批计划都必须包含一个规范 `cdp-scope/v1` 区块，并具备八个必填数组：

- `in_scope`
- `out_of_scope`
- `non_goals`
- `assumptions`
- `stop_conditions`
- `will_change`
- `will_not_change`
- `acceptance_criteria`

批准后必须原样复制整个区块，不得改写、重排、遗漏、弱化或扩大。扩大范围必须返回 CDP 重新规划并再次审批。

有效批准必须同时指出授权动作，以及获批的计划、Scope Lock、阶段、任务或子集。单独的 `ok`、`继续`、`可以` 等确认语不构成批准。

CDP 支持：

- **完整批准（Full Approval）** — 批准完整 Scope Lock。
- **带条件批准（Conditional Approval）** — 先把准确条件写入修订后的规范 Scope Lock。
- **部分批准（Partial Approval）** — 只批准明确列出的内容，其余全部显示为 `NOT APPROVED — MUST NOT BE IMPLEMENTED / 未批准，不得实施`。

部分批准必须生成完整的获批子集 Scope Lock，并展示 Partial Approval Result，其中包含 Approved Scope、Unapproved / Remaining 和 Authorized Action。已批准与未批准的措辞都必须原样保留，包括上面那行双语状态文本。

## Execution Context 与交接

### Standalone

计划获批后，由用户选择：

1. `Execute Now`
2. `Save as CDTask`

CDP 不得自动选择。`Save as CDTask` 适合需要持久化、恢复、较大、分阶段或规划与实施分离的工作，并使用 `cdp-cdtask/v1` 与 `Approval-State: scope-approved-execution-deferred`。

### CDF-managed

CDP 将 Approved Plan Package 返回 CDF 后停止。它不实现、不调用 CDTask、不持久化本地任务，也不继续生命周期。

CDF 之后可以使用 `cdf-cdtask/v1` 将已批准计划交给 CDTask。两种契约都只是内部 Skill 交接格式，不是公开 Runtime Protocol。

## 快速开始

可通过 `cdp`、`$cdp`、`cdp:` 或 `controlled-development-planning` 调用：

```text
使用 CDP 检查此需求、判断风险、生成可审批的 Scope Lock 和
Development Plan，然后让我选择下一步动作。
```

计划应包含：

1. Requirement Understanding
2. Evidence
3. Risk Gate Result
4. Scope Lock
5. Change Scope —— `Will Change` 与 `Will Not Change`，逐字取自 Scope Lock
6. Technical Approach
7. Risks
8. Acceptance Criteria
9. Verification Strategy
10. Next Action

所有章节在任何风险等级下都必须存在，变化的是深度而不是有无。`Change Scope` 是规范 Scope Lock 的可读投影，不能取代它 —— CDTask 在所有风险等级下都要求该章节，缺失或与规范区块矛盾时会返回 `BLOCKED`。

## 参考资料

- [Requirement Gate](references/requirement-gate.md) — 需求清晰度与产品风险问题。
- [Karpathy Guidelines](references/karpathy-guidelines.md) — 最小化、基于证据的工程约束。
- [Boundary Cases](references/boundary-cases.md) — 风险升级、模糊审批、证据冲突和部分审批的双语示例。
- [Installation Notes](references/install.md) — 安装和 CDTask 可用性说明。

Level M/L/XL 在输出计划或设计前必须阅读 Karpathy Guidelines。Level S 完成目标检查后通常不需要读取；仅在此前尝试失败或需要额外最小改动约束时使用。辅助资料不可用时，以 CDP 规则为准。

## 兼容性

CDP 使用 Codex 和 Claude Code 支持的 Agent Skills 布局：

- 入口：`skills/cdp/SKILL.md`
- 元数据：`skills/cdp/skill.json`
- Codex UI 元数据：`skills/cdp/agents/openai.yaml`

## 安装

Codex：

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a codex -g -y
```

Claude Code：

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a claude-code -g -y
```

同时安装：

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a codex -a claude-code -g -y
```

## 不可违反的规则

- 不得隐藏证据不足或证据冲突。
- 未完成两类强制 Checklist，不得最终判为 S/M。
- 不得扩大或改写已批准范围。
- 不得接受模糊批准。
- 不得自动进入实现或持久化。
- 不得引入 Runtime、调度或 Review 行为。
