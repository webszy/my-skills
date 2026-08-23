# CDF：Controlled Development Flow

CDF 是唯一面向用户的受控开发 Skill。它理解开发需求、检查仓库证据、判断风险、锁定实现计划、获得明确人工批准，然后执行已批准工作，或将其保存为可恢复任务。

> Small changes should be fast. Risky changes should be controlled.

## 何时使用 CDF

通过 `$cdf`、`/cdf`、`cdf:`、`controlled-development-flow`，或明确要求受控开发流程来调用 CDF。

适用场景：

- 新功能、修复、重构、配置改动或其它开发需求；
- 需要结合仓库证据进行规划的 PRD、规格或需求；
- 将已批准开发工作拆分并保存为任务；
- 恢复此前由 CDF 保存的任务。

纯信息请求不会进入开发流程。把 PRD 转成任务也不能跳过完整的分析和审批路径。

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

需求分析和规划都是 CDF 内部阶段，不再通过独立 Skill 交接。只有在 **Save as Task** 获批后，CDF 才会加载 `components/cdtask/`。

## 控制门禁

### 先检查证据，再制定计划

CDF 会确认指定目标真实存在，并检查足够且最小范围内的代码、配置、测试、文档、schema、生成产物和调用点。重要结论会区分事实、推断和假设；证据缺口或冲突必须显式暴露，不能静默猜测。

CDF 还会记录可用的 workspace、branch、commit，以及相关 tracked/untracked worktree 状态，用于后续漂移检查。

### 风险分级

风险根据影响、爆炸半径、可逆性、不确定性、敏感性和协作要求综合确定：

| 等级 | 典型边界 |
|---|---|
| **S** | 单个局部的文案、样式或静态改动，没有共享或行为影响 |
| **M** | 边界明确的局部行为、小型共享组件改动、有限配置或有限既有集成使用 |
| **L** | 跨域行为、持久化数据、计费、认证、安全、隐私、具有重要业务含义的分析、重要外部契约或非平凡回滚 |
| **XL** | 架构、新子系统/服务、迁移、重大数据流重构、分阶段发布或多系统协作 |

风险信号提供证据并可能设定风险下限，但不自动等于最终等级。Level S 和 M 必须通过 Reverse Check。未解决的证据缺口采用最低合理安全等级；会改变含义、范围、验收或安全性的冲突必须 `BLOCKED`。

### Scope Lock

每个可审批计划都包含一个规范 `cdf-scope/v1` 区块，并具备八个字段：

- `in_scope`
- `out_of_scope`
- `non_goals`
- `assumptions`
- `stop_conditions`
- `will_change`
- `will_not_change`
- `acceptance_criteria`

所有字段都必须存在；确实没有内容时可以使用空数组。批准后，规范区块成为不可变数据。执行和任务编译都不得改写、重排、扩大、弱化、格式归一化或静默增加范围。

### 人工审批

所有风险等级都需要批准。有效批准必须同时明确获批的计划、Scope Lock、阶段或子集，以及一个授权动作：

1. **Execute Now**
2. **Save as Task**

当范围或动作仍有歧义时，`ok`、`继续`、`可以` 或 `looks good` 不构成有效授权。CDF 支持完整、带条件和部分批准；条件必须先写入修订后的 Scope Lock，部分批准中未获批内容必须保持明确排除。

对于分阶段的 Level XL 工作，每个阶段都有独立的 Development Plan 边界、规范 Scope Lock、Approval Record 和授权动作；批准不会自动延续到下一阶段。

## 获批后的结果

### Execute Now

明确批准 **Execute Now** 后，CDF 会：

- 重新检查仓库漂移、假设、停止条件、受保护区域和已批准阶段边界；
- 只实施规范 Scope Lock 中已批准的范围；
- 不做无关 cleanup、refactor、dependency 增加或大范围格式化；
- 只报告实际执行过的验证，包括失败和未验证标准。

如果新证据改变范围、风险、实现含义、验收或回滚，必须停止执行，返回规划并重新审批。

### Save as Task

明确批准 **Save as Task** 后，CDF 会创建唯一的内部 tasking contract：

```text
Contract-Version: cdf-cdtask/v1
Handoff-Type: approved-tasking
Approval-State: approved
```

内部任务 compiler 会：

- 原样保留规范 Scope Lock 和 Approval Record；
- 在不增加产品或技术决策的前提下生成稳定、依赖感知的任务；
- 执行 Scope Guard；
- 默认保存到 `<Workspace>/_cdtask/YYYY-MM-DD-<short-slug>.md`；
- 保存 Scope Lock 和 Approval Record 的 SHA-256 摘要；
- 最终回读验证、返回绝对路径并停止。

如果任务编译需要新范围、接口、依赖、架构决策、改变验收标准，或无法安全分离部分批准的剩余内容，它必须 `BLOCKED` 并返回 CDF 规划，重新获得批准。

当用户要的是任务拆分时，**Save as Task** 生成可持久化任务定义；**Execute Now** 表示实施底层已批准开发工作，不会返回未保存的任务列表。

CDTask 是内部 component，不单独安装或调用。

## 恢复已保存任务

```text
$cdf continue task <path>
```

实施前，CDF 会：

1. 验证 `cdf-cdtask/v1` 和全部必需区块；
2. 重新计算 Scope Lock 与 Approval Record 的 SHA-256；
3. 比较 workspace、branch、commit、相关已提交和未提交 worktree 状态、当前代码和依赖；
4. 重新检查假设、停止条件、阶段边界、部分批准排除项、验收标准和验证义务；
5. 判断已批准的实现含义是否仍然有效。

缺失、旧版或无法识别的 contract 会在不修改代码的情况下被拒绝。Material drift 或失效假设必须返回规划并重新审批；可证明无实质影响的漂移信号可以记录后继续。

验证通过后，明确的 `continue task <path>` 会授权本回合执行该已保存的批准范围。仅要求检查、总结或验证任务，不构成实施授权。

## 边界

CDF 不会：

- 在有效批准前修改代码或保存任务；
- 从确认语或沉默中推断批准；
- 扩大批准范围或顺手清理相邻代码；
- 把计划中的验证描述为已经完成；
- 充当 runtime、scheduler、worker 分配系统或自动实现 Review 系统。

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

恢复任务：

```text
$cdf continue task <path>
```

## 参考资料

- [Requirement Gate](references/requirement-gate.md)
- [Risk Classification](references/risk-classification.md)
- [Coding Discipline](references/karpathy-guidelines.md)
- [Boundary Cases](references/boundary-cases.md)
- [Internal Task Handoff](references/task-handoff.md)
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
- **Skill package version：** 1.1.0

两者是不同的版本体系。Suite maturity 表示 CDF 架构，package version 表示可分发版本。

只有 `cdf` 是 Skill 入口。内部任务 compiler 使用 `COMPONENT.md`，不使用 `SKILL.md`。
