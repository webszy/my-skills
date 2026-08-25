# CDF：Controlled Development Flow

CDF 是唯一面向用户的受控开发 Skill。它理解开发需求、检查仓库证据、判断风险、锁定范围、获得明确人工批准，然后执行已批准工作，或将其保存为可恢复任务。

> Small changes should be fast. Risky changes should be controlled.

## 何时使用 CDF

通过 `$cdf`、`/cdf`、`cdf:`、`controlled-development-flow`，或明确要求受控开发流程来调用 CDF。

适用场景：

- 新功能、修复、重构、配置改动或其它开发需求；
- 需要结合仓库证据进行规划的 PRD、规格或需求；
- 将已批准开发工作拆分并保存为任务；
- 恢复此前由 CDF 保存的任务。

纯信息请求不会进入开发流程。把 PRD 转成任务也不能跳过完整的分析和审批路径。

CDF 是唯一用户入口。任务编译是 CDF 内部 component，不存在顶层任务 Skill、独立安装或独立调用入口。

## 工作流

```text
Requirement / PRD / Development Request
    -> Requirement Gate
    -> Requirement Understanding
    -> Evidence Inspection
    -> Risk Classification
    -> Development Plan
    -> cdf-scope/v1 Scope Lock
    -> Human Approval
    -> Execute Now | Save as Task
```

需求分析和规划都是 CDF 内部阶段。只有在 **Save as Task** 获批后，CDF 才会进入内部任务 compiler。

## 控制门禁

### 证据与仓库可追溯性

CDF 会确认指定目标真实存在，并检查足够且最小范围内的代码、配置、测试、文档、schema、生成产物和调用点。重要结论会区分事实、推断和假设；证据缺口或冲突必须显式暴露，不能静默猜测。

可用时，CDF 会记录：

```text
Workspace: <absolute path>
Source-Branch: <branch>
Source-Commit: <commit>
Source-Worktree-State: <clean | dirty | Unavailable>
Source-Worktree-Changes: <[] | [Unavailable] | [' M src/foo.ts', '?? src/new-file.ts']>
```

`Source-Worktree-Changes` 统一使用 flow-style YAML 数组，只记录与已批准、受影响或受保护区域有关的 tracked/untracked 路径。Dirty 条目必须加引号，完整保留 Git `XY` 两个字符及前导空格；没有相关改动时使用 `[]`，状态不可用时使用 `[Unavailable]` 并记录原因。Dirty 状态是证据与漂移信号，但不会自动证明风险或漂移具有实质影响。

### 风险分级

S/M/L/XL 风险模型保持不变。风险根据影响、爆炸半径、可逆性、不确定性、敏感性和协作要求综合确定：

| 等级 | 典型边界 |
|---|---|
| **S** | 单个局部的文案、样式或静态改动，没有共享或行为影响 |
| **M** | 边界明确的局部行为、小型共享组件改动、有限配置或有限既有集成使用 |
| **L** | 跨域行为、持久化数据、计费、认证、安全、隐私、具有重要业务含义的分析、重要外部契约或非平凡回滚 |
| **XL** | 架构、新子系统/服务、迁移、重大数据流重构、分阶段发布或多系统协作 |

风险信号提供证据并可能设定风险下限，但不自动等于最终等级。CDF 先执行 `SKILL.md` 中的紧凑 S Reverse Check；明确属于 Level S 时不加载完整风险参考。任一 S 条件失败、未知或出现可能的非 S 类别时，才加载 `risk-classification.md` 及完整 signal record。未解决的 `UNKNOWN` 禁止采用低于最低合理风险的等级。CDF 无法生成安全且边界明确的计划，或冲突证据会改变含义、范围、验收或安全性时，必须停止为 `BLOCKED`。

规划深度随等级变化。Level S 使用下面的快速路径；Level M、L 和 XL 使用完整 Development Plan。

### Level S 快速路径

已确认的 Level S 改动通过四行内容获批，不产生规范 Scope Lock，也不产生十一个规范章节：

```markdown
## Fast-Path Plan (Level S)
- Change: <the single target and the exact change>
- Will Not Change: <protected boundary>
- Verify: <observable check>
- Reverse Check: PASS (S-01..S-06)

Approve and execute? Or save as task?
```

快速路径要求 S Reverse Check 的每一行都通过且没有 `UNKNOWN`。在该等级上，信号记录和 Reverse Check 属于内部推理步骤，只以聚合的 `Reverse Check` 一行对外报告。批准依然必须显式：用户要同时说明获批的改动和授权动作。

一旦证据显示存在第二个目标、行为影响、共享消费方，或任何此前被假定为 `CLEAR` 的信号，CDF 必须离开快速路径并产出完整 Development Plan。选择 **Save as Task** 同样要求提升为完整计划，因为任务 contract 携带规范 Scope Lock；风险等级仍保持 `Level S`。

### Development Plan 合同

Level M、L 和 XL 的每个可审批完整 Development Plan，以及为 **Save as Task** 提升的 Level S 计划，都按以下顺序使用规范标题：

1. `Requirement Understanding`
2. `Evidence Summary`
3. `Risk Gate Result`
4. `Scope Lock`
5. `Technical Approach`
6. `Implementation Plan`
7. `Risks`
8. `Rollback Plan`
9. `Acceptance Criteria`
10. `Verification Strategy`
11. `Next Action`

Handoff 或已保存任务会直接携带这些标题，不得重命名、合并、拆分或重新生成。Level S 改用快速路径，只有在为 **Save as Task** 提升为完整计划时才采用这些标题。Level S 或 M 的 `Rollback Plan` 可以很简洁，或在确实不适用时使用 `None`；Level L 和 XL 则必须包含 [SKILL.md](SKILL.md) 规定的额外细节。

### Scope Lock 与验收授权源

每个可审批完整计划都包含且只包含一个规范 `cdf-scope/v1` 区块，包括为 **Save as Task** 提升的 Level S 计划，并按以下顺序具备八个字段：

- `in_scope`
- `out_of_scope`
- `non_goals`
- `assumptions`
- `stop_conditions`
- `will_change`
- `will_not_change`
- `acceptance_criteria`

所有字段都必须存在，且顺序固定，因为完整性验证以第一个和最后一个字段界定 payload 边界。批准前，`in_scope` 和 `acceptance_criteria` 必须各有至少一个非空条目；其它数组确实没有内容时可以为空。部分或条件批准若没有任何获批 `in_scope` 条目，必须返回 `BLOCKED`。批准后，规范区块成为不可变数据。执行和任务编译都不得改写、重排、扩大、弱化、格式归一化、重新缩进或静默增加范围。

唯一的 `cdf-scope/v1` 区块是范围的唯一规范授权源，其中的 `acceptance_criteria` 字段是验收标准的唯一规范源。Development Plan 的 `Acceptance Criteria` 只是可读投影：必须逐项、同序、逐字重复全部规范标准，不得增加、删除、弱化、扩大、重新解释、合并或拆分。Task-level 标准只能逐字引用适用的规范条目。任何新增或改变的标准都是范围变更，必须重新规划并审批。

### 人工审批

所有风险等级都需要批准。有效批准必须同时明确获批的计划、Scope Lock、阶段或子集，以及一个授权动作：

1. **Execute Now**
2. **Save as Task**

当范围或动作仍有歧义时，`ok`、`continue`、`可以` 或 `looks good` 不构成有效授权。CDF 支持完整、带条件和部分批准；条件必须先写入修订后的 Scope Lock。

部分批准时，计划中唯一的规范 Scope Lock 必须修订为仅包含可安全分离的获批子集；未批准项保持逐字不变，并通过规范排除项加以保护。CDF 还会生成稳定的 `Partial Approval Result`，只包含批准类型、逐字的已批准项、逐字的未批准项和规范版本标记。该结果只是审计投影：它不复制完整 Scope Lock，也不产生第二个授权源。

Approval Record 记录已批准边界和所选动作。对于 **Save as Task**，该记录只授权持久化，明确不授权批准回合或未来恢复时修改代码。保存后，其内容始终保持不变。

对于分阶段的 Level XL 工作，每个已批准阶段都有自己的 Development Plan 边界、规范 Scope Lock、Approval Record 和所选动作；一个阶段的批准绝不授权后续阶段。已批准的阶段边界会显式记录：

```markdown
## Approved Phase Boundary
- Phase: <identifier and short name>
- Phase Scope: <what this phase delivers, matching canonical in_scope>
- Ends At: <the observable state that completes this phase>
- Explicitly Deferred: <later-phase work that this approval does not authorize>
```

## 获批后的结果

### Execute Now

明确批准 **Execute Now** 后，CDF 会：

- 重新检查仓库漂移、假设、停止条件、受保护区域和已批准阶段边界；
- 只实施规范 Scope Lock 中已批准的范围；
- 不做无关 cleanup、refactor、dependency 增加或大范围格式化；
- 只报告实际执行过的验证，包括失败和未验证标准。

如果新证据改变范围、风险、实现含义、验收、验证或回滚，必须停止执行，返回规划并重新审批。

### Save as Task

持久化前，CDF 会对已批准的规划证据执行 drift preflight，重新检查 workspace、branch、commit、worktree 状态和相关 `Source-Worktree-Changes`：

- Material drift 会停止保存，并返回更新后的规划、风险评估、必要时修订的 Scope Lock 和重新审批；
- 可证明无实质影响的漂移会被记录，handoff 使用最新的可追溯性元数据。

只有 preflight 通过后，CDF 才会创建内部 tasking handoff：

```text
Contract-Version: cdf-cdtask/v1
Handoff-Type: approved-tasking
Approval-State: approved
```

内部任务 compiler 会：

- 原样保留规范 Scope Lock 和 Approval Record；
- 对照 `cdf-scope/v1.acceptance_criteria` 验证 `Acceptance Criteria` 投影；
- 在不增加产品或技术决策的前提下生成稳定、依赖感知的任务；
- 保留部分批准的审计投影，但不复制 Scope Lock；
- 执行 Scope Guard；
- 默认保存到 `<Workspace>/_cdtask/YYYY-MM-DD-<short-slug>.md`；
- 回读验证时逐行比对两个规范 payload，并重新计算必需摘要，随后返回绝对路径并停止。

如果任务编译需要新范围、接口、依赖、架构决策、改变验收标准、不充分的 Scope Lock，或无法安全分离部分批准的剩余内容，它必须 `BLOCKED` 并返回 CDF 规划，重新获得批准。

已批准的 Level S 快速路径没有规范 Scope Lock，因此不能直接 handoff。CDF 必须先把它提升为完整 Development Plan 并获得该计划的批准；风险等级仍保持 `Level S`。

当用户要的是任务拆分时，**Save as Task** 生成可持久化任务定义；**Execute Now** 表示实施底层已批准开发工作，不会返回未保存的任务列表。

### 完整性验证

规范 Scope Lock 和 Approval Record 必须在持久化和恢复过程中保持不变。CDF 通过比对文本来验证这一点，而不是依赖记忆中的某个值。

payload 边界是固定的：Scope Lock 从 `Scope-Lock-Version: cdf-scope/v1` 开始，到最后一个 `acceptance_criteria` 条目结束；Approval Record 从 `## Approval Record` 开始，到最后一个字段结束；两者都排除 Markdown 围栏分隔符。八个 Scope Lock 字段必须保持规范顺序，因为边界依赖该顺序。

Payload 字节统一使用 UTF-8、LF 换行，排除 Markdown 围栏分隔符，payload 行不得有尾随空白，并且最后一行后恰好保留一个尾随 LF。

比对是逐行进行的：行数相同、顺序相同、字符（含缩进）相同。任何差异都是不匹配，CDF 会报告它，而不是改写已批准内容来强行通过。边界有歧义、规范区块重复，或 payload 行存在尾随空白，同样直接拒绝。

对于持久化任务，CDF 在权威的逐行比对通过后，必须为两个精确规范 payload 分别计算并保存 SHA-256 摘要。摘要是跨会话恢复使用的持久基线，恢复时必须重新计算并匹配。任一摘要无法计算时，不得把任务报告为可恢复。旧任务若记录 `Unavailable`，执行前必须重新审批并完成可验证的重新保存。

## 恢复已保存任务

```text
$cdf continue task <path>
```

实施前，CDF 会：

1. 验证 `task_contract: cdf-cdtask/v1` 和全部必需区块；
2. 按固定边界提取规范 Scope Lock 和 Approval Record，并要求重新计算的摘要与持久化基线一致；
3. 执行**代码证据 Diff**：将当前 branch、commit 以及任务 write scopes 和 protected areas 涉及文件的内容，与任务文件中保存的 `Source-Branch`、`Source-Commit` 和 `Source-Worktree-Changes` 进行比对。

缺失、旧版或无法识别的 contract 会在不修改代码的情况下被拒绝。

**Fast-Resume Path** — 如果自 `Source-Commit` 以来没有任何提交触及任务 write scopes 或 protected areas 的文件，且 worktree 在这些路径上也没有相关未提交改动，直接进入以下 Resume Authorization Record。

**Full-Replan Path** — 如果有提交或未提交的改动触及了任务 write scopes 或 protected areas 的文件，返回 CDF 规划。以保存任务中的 `Requirement Understanding`、`Evidence Summary`、`Risk Gate Result`、`Scope Lock`、`Technical Approach` 和 `Implementation Plan` 作为起点，只重新检查变动的文件，更新 Evidence Summary，重新评估风险，必要时修订 Development Plan 和 Scope Lock，获得新审批后再执行。

Fast-Resume Path 通过后，或 Full-Replan Path 重新获得审批后，显式 `$cdf continue task <path>` 请求会创建如下本回合 `Resume Authorization Record`：

```markdown
## Resume Authorization Record
- User Request: <verbatim current continue request>
- Task Path: <resolved absolute path>
- Authorized Action: Execute Saved Approved Scope
- Scope Source: persisted cdf-scope/v1
- Authorization Context: <timestamp when available, otherwise current conversation turn>
- Code Changes Authorized In This Turn: Yes
```

只有此后，CDF 才能按依赖顺序执行已保存的批准范围。首次修改代码前，CDF 会按 `cdf-execution-progress/v1` 创建或验证 `<saved-task-path>.progress.yaml`。Sidecar 只记录 `pending`、`in_progress`、`verified` 或 `blocked`；恢复时只跳过证据仍适用的 `verified` 任务，并在继续前检查中断任务。该记录和 sidecar 都不修改已保存任务或其 Approval Record。仅检查、审阅、总结或验证任务既不创建 Resume Authorization Record，也不授权实施或修改进度。

## 边界

CDF 不会：

- 在有效批准前修改代码或保存任务；
- 从确认语或沉默中推断批准；
- 扩大批准范围或顺手清理相邻代码；
- 把保存时的持久化批准当成未来执行授权；
- 把计划中的验证描述为已经完成；
- 充当后台 runtime、scheduler、worker 分配系统或自动实现 Review 系统；进度 sidecar 只是执行日志。

完整规则以 [SKILL.md](SKILL.md) 为准。

## 使用示例

新开发需求：

```text
$cdf 分析这个开发需求、检查仓库、判断风险、锁定计划并获得批准，
然后执行它或保存为可恢复任务。
```

PRD 转任务：

```text
$cdf 检查这个 PRD 和仓库，生成可审批计划，然后将获批工作保存为依赖感知任务。
```

验证后恢复并执行：

```text
$cdf continue task <path>
```

只检查、不执行：

```text
$cdf validate task <path> without executing it
```

## 参考资料

- [Requirement Gate](references/requirement-gate.md)
- [Risk Classification](references/risk-classification.md)
- [Coding Discipline](references/karpathy-guidelines.md)
- [Boundary Cases](references/boundary-cases.md)
- [Internal Task Handoff](references/task-handoff.md)
- [Saved-Task Execution Progress](references/execution-progress.md)
- [Internal Task Compiler](components/cdtask/COMPONENT.md)

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

## 版本语义

- **CDF Suite maturity：** v0.1
- **Skill package version：** 1.2.0

两者是不同的版本体系。Suite maturity 表示 CDF 架构，package version 表示可分发版本。

只有 `cdf` 是 Skill 入口。内部任务 compiler 使用 `COMPONENT.md`，不使用 `SKILL.md`。
