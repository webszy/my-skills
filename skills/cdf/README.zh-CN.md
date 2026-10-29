# CDF：Controlled Development Flow

CDF 是唯一面向用户的受控开发 Skill。它理解开发需求、检查仓库证据、判断风险、锁定范围、获得明确人工批准，然后执行已批准工作，或将其保存为可恢复任务。

> Small changes should be fast. Risky changes should be controlled.

CDF 流程运行时，每次对外回复的第一行显示 `当前流程：cdf v<version>`，版本读取该 skill 的 `skill.json`（当前为 `1.2.1`）。进度、审批、保存和恢复消息均适用；这行提示不增加 task 文件的固定章节。

每次回复还会简要列出 **当前 Agent 已做** 和 **与当前需求无关的代码改动**：说明实际工作、额外动作及原因，以及无关改动的文件、授权证据和保留或撤回状态；确认没有时明确写“无”，归属不明时写“无法确认”并说明证据缺口。最终报告累计覆盖当前需求，并区分已有或其他 Agent 的修改。完成报告复用动作证据和 `out_of_scope_changes`；披露不代表获得额外范围授权。

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

规划深度随等级变化。Level S 使用下面的快速路径。M／L／XL 仍需完成完整分析，但默认只展示精简审批摘要；固定 11 章节用于内部 handoff 和已保存 task 文件。

### 精简审批展示

使用用户的语言，每段通常一到三条简短内容：

- **需求理解（Requirement Understanding）**：目标、范围和重要排除项。
- **技术方案（Technical Approach）**：采用什么方案、哪些决策需要批准。
- **实施步骤（Implementation Plan）**：简短步骤、可观察的验收结果及检查方式。
- **风险（Risks）**：重要风险、假设或条件、回滚影响。

最后用一句话选择：批准并执行，或批准并保存为 task。重要条件和 XL 阶段边界必须展示；证据清单、风险检查表、规范 YAML、原始审批及进度记录默认不在聊天中展开，用户要求时再展示。授权只覆盖已展示的含义，内部范围不能增加隐藏义务。批准后用一句话确认即可。

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

一旦证据显示第二个目标、行为影响、共享消费方或其它信号，CDF 必须离开快速路径，重新判断风险并展示精简摘要。批准 **Save as Task** 后，CDF 将 S 级快速计划映射为完整文档计划和规范范围，含义不变，风险仍为 `Level S`。仅展开文档格式不需要再次批准。

### Development Plan 合同

所有风险等级在 **Save as Task** 获批后，均由 CDF 将已批准的规划内容整理为以下 11 个文档章节，再进行内部 handoff。这不是默认的聊天审批格式：

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

CDF 将整理后的计划与批准摘要核对，冻结后交给 compiler 原样保存。文件还会保留实际展示过的摘要作为审批证据。格式展开不产生新授权，也不触发二次审批；若发现新增范围、决策、验收或验证义务，则展示更新后的精简摘要并重新审批。**Execute Now** 直接使用已批准的规划记录，不要求展开 11 章节。S／M 的回滚说明可以很短或在确实不适用时写 `None`；L／XL 仍保留 [SKILL.md](SKILL.md) 要求的完整细节。

### Scope Lock 与验收授权源

M／L／XL 在审批前准备一个内部规范 `cdf-scope/v1` 区块。每个已保存计划均包含一个该区块，包括由已批准快速计划机械映射的 S 级任务。以下八个字段用于内部约束和 task 文件，不要求在聊天审批时展示：

- `in_scope`
- `out_of_scope`
- `non_goals`
- `assumptions`
- `stop_conditions`
- `will_change`
- `will_not_change`
- `acceptance_criteria`

所有字段必须存在且顺序固定，`in_scope` 和 `acceptance_criteria` 各至少有一个非空条目，其它数组可为空。部分或条件批准没有任何已批准项时必须 `BLOCKED`。批准后，或完成已批准 S 级任务的机械映射后，区块不可变；执行和编译不得改写或增加范围。每项重要义务都必须在审批摘要中展示，内部内容本身不构成授权。

唯一的 `cdf-scope/v1` 区块是范围的唯一规范授权源，其中的 `acceptance_criteria` 字段是验收标准的唯一规范源。Development Plan 的 `Acceptance Criteria` 只是可读投影：必须逐项、同序、逐字重复全部规范标准，不得增加、删除、弱化、扩大、重新解释、合并或拆分。Task-level 标准只能逐字引用适用的规范条目。任何新增或改变的标准都是范围变更，必须重新规划并审批。

### 人工审批

所有风险等级都需要批准。有效批准必须明确已展示的精简计划（用户要求时为完整计划）、阶段或子集，以及一个授权动作：

1. **Execute Now**
2. **Save as Task**

当范围或动作仍有歧义时，`ok`、`continue`、`可以` 或 `looks good` 不构成有效授权。CDF 支持完整、带条件和部分批准；条件先写入工作中的 Scope Lock，并通过修订后的精简摘要展示给用户，再取得批准。

部分批准时，规范范围只包含可安全分离的已批准子集，并保护未批准项。聊天中简要说明这个边界；结构化 `Partial Approval Result` 保留在内部并写入 task 文件，只作为审计证据，不产生第二个 Scope Lock。审批及阶段记录也遵循相同展示规则：聊天简述含义，完整记录写入文件，用户要求时再展开。

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
- 要求每条规范验收标准至少映射到一个任务，并有对应的计划检查；
- 在不增加产品或技术决策的前提下生成稳定、依赖感知的任务；
- 保留部分批准的审计投影，但不复制 Scope Lock；
- 执行 Scope Guard；
- 默认保存到 `<Workspace>/_cdtask/YYYY-MM-DD-<short-slug>.md`；
- 回读验证时逐行比对两个规范 payload，并重新计算必需摘要，随后返回绝对路径并停止。

如果任务编译需要新范围、接口、依赖、架构决策、改变验收标准、不充分的 Scope Lock，或无法安全分离部分批准的剩余内容，它必须 `BLOCKED` 并返回 CDF 规划，重新获得批准。

已批准的 Level S 快速路径不能直接 handoff。CDF 先将其映射为完整文档格式，并用原批准语句补全 Approval Record，风险仍为 `Level S`。除非发现新增含义，这种机械展开不要求再次审批。

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
3. 在选择恢复路径前，只读校验已有进度 sidecar；
4. 执行**代码证据 Diff**，覆盖 write scopes、protected areas，以及 API、配置、schema、调用方等只读证据依赖。将已提交和未提交内容与来源版本、Evidence Summary 中的内容基线比对；Git status 条目一致不能证明内容未变；
5. 结合经过校验的进度核对实际改动，区分原有工作、可归因的已批准执行产出、无实质影响的外部漂移，以及实质或无法解释的变化；
6. 重新验证假设、停止条件、共享契约、验收、验证、回滚和阶段边界。

缺失、旧版或无法识别的 contract 会在不修改代码的情况下被拒绝。

**Fast-Resume Path** — 全部检查通过后，已保存计划必须仍有效，且证据未变，或每项差异均可解释为已批准执行产出或无实质影响的漂移。中断任务的正常产出本身不触发重新审批。基线缺失、sidecar 绑定无效或归因未明确不能视为无变化，必须遵循 CDF 的证据缺口及核对规则。

**Full-Replan Path** — 实质漂移必须返回规划，重新检查变化来源及受影响的依赖或假设，必要时修订计划和 Scope Lock，并获得针对新计划及动作的批准。即使 Scope Lock 文本未变，也结束旧任务的恢复路径。**Execute Now** 按 7A 使用新计划和 Approval Record；**Save as Task** 按 7B 保存到不同的新路径并停止，等待用户后续明确继续新任务。两种情况均保留旧任务及 sidecar 绑定，不将新计划的执行写入旧 sidecar，也不把旧运行状态复制到新 sidecar。

只有 Fast-Resume Path 通过后，显式 `$cdf continue task <path>` 请求才会为未变的已保存定义创建如下本回合 `Resume Authorization Record`：

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

结项必须同时满足：全部任务 verified、每条规范验收标准都有任务覆盖及当前有效的成功验证证据、最终范围内审查没有未解决问题。不能仅凭全部任务 verified 就记录 completed。

[Completion Evidence Gate](references/completion-evidence-gate.md) 对 Execute Now 和保存任务的完成申请统一检查验收条件、实际验证结果、Diff Review、范围合规及已知或未验证问题，每次生成结构化 `completion_gate` 报告。`FAIL` 和 `INSUFFICIENT_EVIDENCE` 阻止结项；`PASS` 仅允许进入现有最终 Review，不豁免任何 Human Approval 要求。Agent 输出 `Done` 不会改变任务状态。现有任务契约和生命周期状态保持不变；旧进度 sidecar 仍可读取，但结项必须有当前有效的门禁证据。

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
- [Completion Evidence Gate](references/completion-evidence-gate.md)
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
- **Skill package version：** 1.2.1

两者是不同的版本体系。Suite maturity 表示 CDF 架构，package version 表示可分发版本。

只有 `cdf` 是 Skill 入口。内部任务 compiler 使用 `COMPONENT.md`，不使用 `SKILL.md`。
