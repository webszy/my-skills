# CDF：Controlled Development Flow

CDF 是一个受控的 AI 开发工作流。它会分析需求与仓库证据、判断风险、生成并锁定开发计划、要求人工批准，然后执行已批准的工作，或将其编译为可恢复任务。

> Small changes should be fast. Risky changes should be controlled.

## 架构

CDF 是唯一面向用户的受控开发 Skill：

```text
Requirement / PRD / Development Request
    -> Requirement Understanding
    -> Evidence Inspection
    -> Risk Classification
    -> Development Plan
    -> cdf-scope/v1 Scope Lock
    -> Human Approval
    -> Execute Now | Save as Task
```

规划、审批和获批后的执行都属于 CDF。保存任务时，CDF 会进入 `components/cdtask/` 下的内部 post-approval compiler；该 component 不单独安装，也不单独调用。

## 风险与计划

CDF 根据影响、爆炸半径、可逆性、不确定性、敏感性和协作要求综合判断风险：

| 等级 | 典型工作 |
|---|---|
| **S** | 单个局部的文案、样式或静态改动，没有共享或行为影响 |
| **M** | 边界明确的局部行为、小型共享组件改动、有限配置或有限外部集成使用 |
| **L** | 跨域行为、持久化数据、计费、认证、安全、隐私、具有重要业务含义的分析、重要外部契约或非平凡回滚 |
| **XL** | 架构、新子系统/服务、迁移、重大数据流重构、分阶段发布或多系统协作 |

风险信号用于提供证据并可能设定风险下限，但不自动等于最终等级。小改动保持精简；风险、不确定性或协调成本越高，计划越详细。

## Scope Lock 与审批

每个计划都包含一个规范 `cdf-scope/v1` 区块，并具备八个字段：

- `in_scope`
- `out_of_scope`
- `non_goals`
- `assumptions`
- `stop_conditions`
- `will_change`
- `will_not_change`
- `acceptance_criteria`

没有实际内容的字段可以使用空数组。批准后，该区块是不可变数据：执行和任务编译期间都不得改写、扩大、弱化或格式归一化。

有效批准必须同时明确获批的 Scope Lock（或子集/阶段）以及一个动作：

1. **Execute Now** — 只实施获批范围，并只报告实际运行过的检查。
2. **Save as Task** — 编译并保存可恢复任务，然后停止。

当动作或批准边界不清楚时，`ok`、`继续` 等确认语不足以构成授权。CDF 支持完整、带条件和部分批准；部分批准中未获批的内容必须继续明确排除。

## 保存与恢复任务

内部 compiler 只接受已批准的 `cdf-cdtask/v1` CDF 交接。它会原样保留规范 Scope Lock、生成依赖感知任务、执行 Scope Guard、默认保存到 `_cdtask/`，并回读验证文件。

任务必须通过 CDF 恢复：

```text
$cdf continue task <path>
```

CDF 会验证 task contract、Scope Lock、Approval Record、假设、停止条件、当前代码和仓库漂移。Material drift 必须返回规划并重新审批；不能盲目执行旧任务。

## 使用方式

```text
使用 $cdf 分析这个开发需求、检查仓库、判断风险、锁定计划并获得批准，
然后执行它或保存为可恢复任务。
```

完整运行规则见 [SKILL.md](SKILL.md)。

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

两者是不同的版本体系。maturity 表示架构成熟度，package version 表示当前可分发 Skill 包版本。

## 内部目录

```text
skills/cdf/
|-- SKILL.md
|-- README.md
|-- README.zh-CN.md
|-- skill.json
|-- agents/openai.yaml
|-- references/
`-- components/cdtask/
```

只有 `cdf` 是 Skill 入口。内部任务 compiler 使用 `COMPONENT.md`，不使用 `SKILL.md`。
