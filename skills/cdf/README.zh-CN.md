# CDF：Controlled Development Flow

## 快速理解

CDF 是 CDF Suite 的控制平面。它决定一个开发请求是否进入受控流程，按契约字段路由各组件的返回结果，并拒绝任何缺少完整审批证据的交接。

> Small changes should be fast. Risky changes should be controlled.

CDF v0.1 在交接处结束。它不是 Runtime、调度器、执行器、验证系统或 Review 系统，也不持有持久状态。

## 在 CDF Suite 中的位置

```text
Requirement
 ↓
CDF 评估
 ↓
CDP 规划 + 人工计划审批
 ↓
CDF 交接前置条件检查
 ↓
选用 CDTask 时生成任务定义
 ↓
可交接的 Task Definition，或 Approved Plan Package
```

| Skill | 角色 | 输出 |
|---|---|---|
| `cdf` | 控制平面、返回路由、交接前置条件 | 已批准的流程交接 |
| `cdp` | 基于证据的规划、风险分级、Scope Lock 和人工审批门禁 | Approved Plan Package |
| `cdtask` | 将已批准计划编译为可验证任务 | 可交接的 Task Definition |

CDF 负责协调流程，不取代 CDP 的规划、CDP 的审批门禁，也不取代 CDTask 的任务拆解。

## 核心职责与边界

CDF 负责：

- 流程评估与协调；
- 组件交接与返回路由；
- 交接前置条件与审批证据校验；
- 保护已批准范围。

CDF 不负责：

- 需求分析或技术规划（`cdp`）；
- 人工审批门禁本身，包括展示计划、判断批准措辞和追问（`cdp`）；
- 详细任务拆解（`cdtask`）；
- 实现、执行或调度；
- 实现验证或 Review；
- Runtime 或生命周期状态管理。

CDF 按契约字段路由。它绝不通过阅读计划正文、任务正文或 `Reason` 文本来决定下一步。

## 路由规则

每个决策都是字段比较，而不是对措辞或意图的判断。

| CDP 返回的 `Planning Status` | CDF 动作 |
|---|---|
| `APPROVED` | 进入交接前置条件检查 |
| `NOT_APPROVED` | 报告 `Reason`，不产出交接，本轮按终止结束 |
| `BLOCKED` | 原样报告 `Reason` 并结束本轮 |
| 缺失或无法识别 | 按 blocked 处理，指出缺失字段并结束本轮 |

| CDTask 返回的 `Tasking Status` | CDF 动作 |
|---|---|
| `READY` | 产出终态交接 |
| `NOT_READY` | 退回在已批准范围内修复，然后重新评估 |
| `BLOCKED` | 按 `Blocked-Reason-Class` 路由：approval 和 scope-lock 类缺陷重跑前置条件；`requires-new-scope`、`partial-remainder` 和 `ambiguity` 返回 CDP |

## 交接前置条件

调用 CDTask 前，CDF 通过字段检查确认：

- `Contract-Version: cdp-cdf/v1` 存在且可识别；
- `Planning Status` 为 `APPROVED`；
- 每个证明字段都携带其要求的常量值；
- 存在 Approval Record，且 `Scope Approved: Yes`、`Code Changes Authorized In This Turn: No`；
- 存在规范 `cdp-scope/v1` 区块，八个数组全部有值；
- `Risk Level` 是 Level S、M、L 或 XL 之一；
- `Approval Type` 为 `partial` 时存在 Partial Approval Result；
- `Phase` 和 `Remaining-Phases` 存在或为 `Not applicable`；
- workspace、branch 和 commit 元数据存在，或明确为 `Unavailable`。

任一条件不满足即把包退回 CDP。CDF 绝不修复包、绝不补充缺失字段，也绝不因为"差不多够了"而放行。

批准确认的是方向和范围，不构成对 CDF 的实现或执行授权。

## 证明字段

部分契约字段是常量而非变量。值不对意味着发送方越过了自己的 managed 契约，因此 CDF 会报告并结束本轮，而不是继续：

| 字段 | 契约 | 要求值 |
|---|---|---|
| `Lifecycle Owner` | `cdp-cdf/v1` | `CDF` |
| `Execution by CDP` | `cdp-cdf/v1` | `Not authorized` |
| `Code Changes by CDP` | `cdp-cdf/v1` | `None` |
| `Execution Owner` | `cdf-cdtask/v1` | `CDF` |

`APPROVED` 返回中 `Next Owner` 必须为 `CDF`；`APPROVED` 与 `Human approver` 同时出现意味着审批门禁根本没有关闭。`READY` 返回中 `Task Count` 必须存在且大于零。

## Scope Lock 保护

规范 `cdp-scope/v1` 区块作为不透明载荷，从 CDP 经 CDF 传到 CDTask，全程逐字节复制。CDF 不改写、不重排、不合并、不遗漏、不弱化、不扩大、不重新缩进、不规范化引号、不重新折行，并在交接前读回副本与原文比对。

部分批准时只传递获批子集的规范 Scope Lock。每个未批准项保持明确排除，不为剩余部分准备任何任务，终态报告中必须说明剩余部分未被带入本轮。

## 风险等级与 CDTask 选择

| 风险等级 | 协调深度 | CDTask 默认 |
|---|---|---|
| Level S | 以最小协调透传 CDP 的精简包 | 不选用 |
| Level M | 简短协调摘要 | 不选用 |
| Level L | 完整包，含风险、回滚和验证 | 选用 |
| Level XL | 完整包加阶段追踪 | 选用 |

风险等级不改变审批要求。任何等级在交接前都必须有已完成的 CDP 审批门禁和有效的 Approval Record。

CDTask 是可选的。当已批准工作需要持久化、显式拆解、分阶段、多人协作，或需要把规划与实施分离时才选用；否则 Approved Plan Package 就是终态输出。

若选用了 CDTask 但它不可用，CDF 输出安装命令后停止。它绝不伪造任务定义、绝不写降级文件，也绝不自行安装。

## 快速开始

可通过 `cdf`、`/cdf`、`$cdf`、`cdf:` 或 `controlled-development-flow` 调用：

```text
使用 CDF 评估此需求，获取已批准的 CDP 计划，并准备 CDTask 交接。
```

CDF 在每次交接前后打印 Flow State 区块，便于人工恢复被中断的会话。该区块是可读检查点，不是状态文件。

## 参考资料

- [Flow Contracts](references/flow-contracts.md) —— 四个交接方向的字段定义、状态语义和 Flow State 区块。

组装或校验交接时阅读。该资料不可用时，以 CDF 规则为准。

## 安装

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

## 不可违反的规则

- 不得实现、修改、执行或 Review 代码。
- 不得跳过 CDP，不得在没有有效 Approval Record 的情况下交接。
- 不得判断用户回复是否构成有效批准，该门禁属于 CDP。
- 不得依据计划正文、任务正文或 `Reason` 文本做路由。
- 不得扩大已批准范围，不得补充缺失的契约字段。
- 不得接受携带错误值的证明字段，也不得代为更正。
- 不得声称具备 Runtime、事件系统、公开 schema protocol、CLI、执行器、验证或 Review 能力。
