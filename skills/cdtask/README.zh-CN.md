# CDTask：Controlled Development Task

## 快速理解

CDTask 是 CDF Suite 的任务定义与交接层。它把已批准的计划转化为可验证任务，且不改变已批准的含义和范围。

> Small changes should be fast. Risky changes should be controlled.

CDTask 是可选的。它生成任务定义和文本形式的交接信息，可按需持久化一份可恢复的任务文档。它不是任务引擎、调度器、执行器、Runtime 或 Review 系统。

## 在 CDF Suite 中的位置

```text
Requirement
 ↓
CDF 评估
 ↓
CDP 规划 + Scope Lock
 ↓
Human Plan Approval（由 CDP 执行）
 ↓
CDTask：校验 → 拆解 → 守护范围 → 准备交接
 ↓
执行，在 CDF v0.1 范围之外
```

| Skill | 角色 | 与 CDTask 的关系 |
|---|---|---|
| `cdf` | 控制平面与返回路由 | 发送已批准的 managed 包，接收任务定义就绪状态 |
| `cdp` | 风险感知规划、Scope Lock 和审批材料 | 发送可选的已批准延迟执行包 |
| `cdtask` | 将已批准计划转化为可验证任务定义 | 保持含义不变并准备对外交接 |

## 核心职责与边界

CDTask 负责：

- 校验输入就绪度与审批元数据；
- 复制并执行规范 Scope Lock；
- 定义依赖关系与任务边界；
- 保留验收标准与受保护区域；
- 准备与执行方无关的交接信息；
- 按需持久化可恢复的任务文档；
- 对 managed 任务化返回 `READY`、`NOT_READY` 或 `BLOCKED`。

CDTask 不负责：

- 需求分析或技术重新规划；
- 计划审批；
- 扩大范围；
- 实现或修改代码；
- 执行、调度或并行工作决策；
- Runtime 或生命周期控制；
- 实现验证或 Review。

`READY` 的含义是任务定义已可返回 CDF，等待另行授权的交接。它不代表 CDTask 执行或验证了任何工作。

## 何时使用 CDTask

当已批准工作需要持久化或后续恢复、需要显式拆解、规模较大或分阶段或多人参与、或需要把规划与实施分离时，使用 CDTask。

不要为每个改动都创建 CDTask，也不要用它来发现需求、决定产品问题、批准计划，或修补语义不完整的计划。

## 输入路由

任务化前必须且只能选择一条路由。

| 路由 | 要求契约 | 审批状态 | 生命周期归属 |
|---|---|---|---|
| CDF-managed | `cdf-cdtask/v1` | `plan-approved` | CDF |
| CDP 延迟交接 | `cdp-cdtask/v1` | `scope-approved-execution-deferred` | 经 CDP 恢复后的外部调用方 |
| 手动需求 | 持久化时为 `cdtask/v1` | `not-approved-by-cdp` | 用户 / 外部调用方 |

元数据缺失、无效或自相矛盾时判为 `BLOCKED`。CDTask 绝不推断批准。

手动输入未经 CDP 批准：必须先与用户确认目标、范围、非目标、验收标准和约束，持久化输出也要相应标注。需要大量分析或产品决策的需求应改走 CDP。

以上都是 CDF v0.1 的内部 Skill 交接格式，不是公开 Runtime Protocol。

## 工作流程

```text
输入路由校验
  → 需求就绪度检查
  → 规范 Scope Lock 校验
  → 依赖分析
  → 任务拆解
  → Scope Guard
  → 交接规则 / Execution Contract
  → Task Readiness Gate
  → 按需持久化
  → 返回生命周期归属方
```

规范 `cdp-scope/v1` 区块从收到的包中逐字复制，绝不推导、重建、摘要、规范化或改写。可以另外添加可读投影，但投影不能取代或改变规范区块；任何与规范区块矛盾的投影判为 `BLOCKED`。

## 任务规则

- 每个任务只有一个主要产出。
- 依赖关系和完成标准必须明确。
- 写入范围必须具体，不得编造路径。
- 验证方式与风险等级匹配。
- 受保护区域复制进 `Must Not Change`。
- 任何任务都不得悄悄吞并其它任务或未批准的产出。

`DRAFT` 和 `READY` 只是定义态。绝不引入 assigned、running、retrying、completed 等运行态。

依赖只描述约束 —— CDTask 不调度工作、不分配人员、不选择并行执行。仅由任务结构造成的循环判为 `NOT_READY`，在已批准范围内修复；暴露计划矛盾的循环判为 `BLOCKED`。

## Task Readiness Gate

| 状态 | 含义 | 应采取的动作 |
|---|---|---|
| `READY` | 任务定义完整、自洽且在已批准范围内 | 按所选路由返回或持久化 |
| `NOT_READY` | 属于 CDTask 自身的定义缺陷，可在不改变已批准含义的前提下修复 | 修复后重跑该门禁 |
| `BLOCKED` | 审批、范围、需求含义或来源计划的授权缺失或矛盾 | 停止并返回用户、CDP 或 CDF |

每个 `BLOCKED` 返回都携带 `Blocked-Reason-Class` —— `approval`、`scope-lock`、`ambiguity`、`requires-new-scope` 或 `partial-remainder` —— 使 CDF 无需阅读阻塞说明即可路由。

`READY` 的 managed 返回还携带 `Task Count`（必须大于零），以及 `Execution Owner: CDF` 和 `Next Owner: CDF` 两个证明字段。这两个字段是常量：CDTask 交还流程，而不是自己接着走。

## Scope Guard

拆解完成后，CDTask 确认：每个任务都映射到已批准的 `in_scope` 或 `will_change`；没有任务映射到 `out_of_scope`、`non_goals`、`will_not_change` 或未批准的剩余项；Scope Lock 与审批措辞逐字保留；依赖关系没有引入新的产品或架构决策；验收标准被保留而非放宽；停止条件对未来的执行方可见；没有执行任何实现、调度、Runtime 或 Review 动作。

部分批准时，`Approved Items` 必须与获批子集的 `in_scope` 逐字一致，每个未批准项保持原文且明确排除，任何任务、写入范围、说明、验收标准或验证步骤都不得映射到未批准项。

## 持久化

仅在被要求或所选交接路径需要时才持久化。默认路径为：

```text
<Workspace>/_cdtask/YYYY-MM-DD-<short-slug>.md
```

绝不静默覆盖已有任务文档：默认名冲突时加后缀，明确指定的路径需先确认。只创建必需的父目录，不修改任何实现文件。保存后读回文件并按路由对应的文档契约校验；校验不通过时不得声称保存成功。

## 快速开始

典型的 CDF-managed 调用：

```text
将这份已批准的 CDF 计划转化为带依赖关系的任务定义。
逐字保留规范 Scope Lock，并把任务就绪状态返回给 CDF。
```

典型的 standalone 延迟调用：

```text
将这份已批准的 CDP 包转化为可恢复的 CDTask。不要执行它。
```

## 参考资料

- [Task Templates](references/task-templates.md) —— 依赖、任务拆解和交接的输出格式。
- [Persistence](references/persistence.md) —— 各路由的任务文档契约与保存校验。

拆解前阅读 Task Templates，写文件前阅读 Persistence。辅助资料不可用时，以 CDTask 规则为准。

## 安装

Codex：

```bash
npx skills add https://github.com/webszy/my-skills --skill cdtask -a codex -g -y
```

Claude Code：

```bash
npx skills add https://github.com/webszy/my-skills --skill cdtask -a claude-code -g -y
```

同时安装：

```bash
npx skills add https://github.com/webszy/my-skills --skill cdtask -a codex -a claude-code -g -y
```

## 不可违反的规则

- 不得实现或修改代码。
- 不得执行、调度、分配、监控或 Review 工作。
- 不得推断或授予批准。
- 不得重新规划或臆造影响实现的决策。
- 不得扩大已批准范围。
- 不得改写规范 Scope Lock 或 Approval Record。
- 不得为部分批准中未获批的条目创建任务。
- 不得把就绪状态转换成运行态。
