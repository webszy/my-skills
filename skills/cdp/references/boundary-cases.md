# CDP Boundary Cases / CDP 边界案例

Use these cases when a low-risk-looking request, approval reply, or evidence record is close to a control boundary. Copy the decision pattern, not the example's product details.

在看似低风险的需求、审批回复或证据记录接近控制边界时使用这些案例。复用判断模式，不要照搬示例中的产品细节。

## Case 1: Small-looking visual change that must upgrade / 看似小改动但必须升级

### User request / 用户需求

> Make the disabled button on the sign-in page a lighter gray. It should be a one-line change.
>
> 把登录页禁用按钮的灰色调浅一点，应该只改一行。

### Evidence and gate result / 证据与门禁结果

- The page uses the shared `ui/Button` primitive. / 页面使用共享基础组件 `ui/Button`。
- The disabled color comes from global theme token `--button-disabled-bg`. / 禁用色来自全局主题 token `--button-disabled-bg`。
- Registration, checkout, and admin pages use the same primitive and token. / 注册、结账和后台页面使用同一组件和 token。
- A disabled-state condition selects the style. / 样式由禁用状态条件选择。

```text
ESC-01 Shared component/theme token: HIT
ESC-02 Conditional behavior: HIT
Level S Reverse Check: Not run after mandatory escalation
Final Risk Level: Level L
```

### Correct behavior / 正确行为

```md
Surface impression before evidence: Level S
Final classification: Level L

The visible change reaches a shared Button primitive, a global theme token,
and conditional state styling. I will prepare an evidence-backed plan and
Scope Lock. No implementation or CDTask handoff may occur before valid approval.
```

### Why / 为什么

A small visual delta does not imply a small blast radius. Any mandatory escalation `HIT` forces at least Level L. / 可见改动很小不代表影响面小；任一强制升级项命中都必须至少升到 Level L。

## Case 2: Ambiguous acknowledgement is not approval / 模糊回复不构成批准

### Context / 上下文

- Execution Context: `standalone`
- Risk: Level L
- The Development Plan and canonical Scope Lock are already displayed. / Development Plan 和规范 Scope Lock 已展示。
- CDP is waiting for the user's Next Action. / CDP 正在等待用户选择 Next Action。

### User reply / 用户回复

> ok，继续

### Approval check / 审批检查

- The reply does not name an authorized action. / 回复没有指定授权动作。
- The reply does not identify the displayed Scope Lock, phase, task, or subset. / 回复没有明确指向已展示的 Scope Lock、阶段、任务或子集。
- Approval result: invalid and ambiguous. / 审批结果：无效且含糊。

### Correct behavior / 正确行为

```md
继续前，我需要你对已锁定范围给出明确授权动作。

请选择：
1. `Execute Now` — 批准按已展示的 Scope Lock 实施。
2. `Save as CDTask` — 仅批准保存和任务交接；本回合不实施。
3. `Request changes` — 修改计划或 Scope Lock。
```

Remain at the approval gate. Do not implement, create a handoff package, or persist a task. / 保持在审批门禁，不实施、不生成交接包、不保存任务。

### Why / 为什么

`ok` and `继续` acknowledge the message but do not prove both action and scope authorization. / `ok` 和 `继续` 只能表示收到，不能同时证明动作和范围都已获授权。

## Case 3: Evidence conflict, BLOCK, then partial approval / 证据冲突、BLOCK 与部分批准

### User request / 用户需求

> Update the admin help copy, and hide the export entry from users without export permission.
>
> 更新管理员帮助文案，并让没有导出权限的用户看不到导出入口。

The displayed candidate plan uses these exact scope items: / 候选计划使用以下原文范围项：

- `更新管理员帮助文案为已确认的新文案。`
- `对没有导出权限的用户隐藏导出入口。`

### Conflicting evidence / 冲突证据

- Frontend condition: `canExport`.
- API documentation: `reports.export`.
- Permission configuration: `report_export`.
- Product note: all managers should see the export entry.

This conflict changes permission behavior and acceptance criteria. ESC-02 and ESC-12 are `HIT`; use provisional Level L controls and remain `BLOCKED`. / 冲突会改变权限行为和验收标准；ESC-02 与 ESC-12 命中，采用临时 Level L 控制并保持 `BLOCKED`。

### Correct blocked response / 正确的阻塞响应

```md
Planning Status: BLOCKED
Provisional Risk: Level L

Evidence Conflict:
- Frontend condition: `canExport`
- API contract: `reports.export`
- Permission configuration: `report_export`
- Product rule: all managers see the export entry

Please identify the authoritative source. I will not finalize the permission
plan or prepare a CDTask handoff while this conflict changes plan meaning.
```

### User narrows the request / 用户缩小范围

> 权限逻辑先不做，只保留帮助文案。

Treat this as a scope revision, not approval of the earlier plan. Re-run evidence and classification for the separable copy-only subset. If it is independently safe, produce a new approved-subset Scope Lock and request an explicit Next Action. If the copy cannot be separated from the permission conflict, remain `BLOCKED`. / 这属于范围修订，不是对旧计划的批准。仅当文案子集可独立成立时才重新分级、生成子集 Scope Lock 并请求明确动作；否则继续 `BLOCKED`。

### Explicit partial approval / 明确的部分批准

> 批准这个子集并 `Save as CDTask`。

```md
## Partial Approval Result

Approval Type: partial
Authorized Action: Save as CDTask

### Approved Scope
- 更新管理员帮助文案为已确认的新文案。

### Unapproved / Remaining
Status: NOT APPROVED — MUST NOT BE IMPLEMENTED / 未批准，不得实施
- 对没有导出权限的用户隐藏导出入口。

### Approved-Subset Scope Lock

Scope-Lock-Version: cdp-scope/v1
in_scope:
  - 更新管理员帮助文案为已确认的新文案。
out_of_scope:
  - 对没有导出权限的用户隐藏导出入口。
non_goals:
  - 更改权限、授权或条件渲染逻辑。
assumptions:
  - 已批准的帮助文案为最终文案。
stop_conditions:
  - 文案修改需要改动权限或条件渲染逻辑。
will_change:
  - 管理员帮助文案。
will_not_change:
  - 导出入口可见性。
  - 权限与授权逻辑。
acceptance_criteria:
  - 管理员帮助区域显示已批准的新文案。
```

### Why / 为什么

The permission item stays visibly unapproved, while the canonical Scope Lock contains only the independently approved positive work plus its protections. CDTask may receive only this approved-subset block and may create no task for the remaining item. / 权限项必须明确保持未批准；规范 Scope Lock 只包含独立获批的正向工作及其保护约束。CDTask 只能接收该子集，不得为剩余项创建任务。
