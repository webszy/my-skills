# cdp

`cdp` 是 `controlled-development-planning` 的简称：一个面向 AI Coding Agent 的风险分级开发工作流 Skill，会在实现前先澄清模糊需求。

可以用 `cdp`、`$cdp`、`cdp:` 或 `controlled-development-planning` 显式调用。

它帮助 Agent 避免两类常见问题：

- 对简单改动过度规划。
- 对高风险改动执行过快。
- 根据模糊提示词实现错误方向。

核心原则：

> 小改动要快，风险改动要可控。

快速流程：先运行 Requirement Gate，必要时先澄清需求；如果用户接受建议默认值，就把它们当作显式假设继续；然后定位目标，向用户展示需求理解和影响面拆解，运行决策树进行初始分级，检查代码证据，再运行同一棵决策树进行最终分级，然后使用对应工作流。如果示例、决策树和分类条件冲突，采用最高风险等级。

决策树：架构或分阶段发布是 Level XL；数据、金钱、报表、认证、任务、生产配置、缓存失效、事件/Webhook、第三方集成、CDN/静态资源投递、本地化/i18n 行为、无障碍/合规行为或类似高风险运行时区域默认是 Level L，除非证据证明只是纯本地展示/样式/文案改动；范围明确的交互、小 API 或本地状态改动是 Level M；纯文案、样式、静态单组件调整只有在所有低风险条件成立时才是 Level S。

## 需求闸门

CDP 在选择工作流等级前，会先判断需求是否达到可执行清晰度。

如果用户请求模糊、不完整、有歧义，或者缺少验收标准，CDP 会先输出需求定义卡、缺口清单、最少追问和建议默认值，而不是直接进入代码实现。

这个闸门的目标不是把所有任务都变成 PRD，而是防止 Coding Agent 根据模糊提示词实现错误方向，减少返工和失控修改。

## 兼容性

`cdp` 遵循 Codex 和 Claude Code 使用的 Agent Skills `SKILL.md` 格式：

- Skill 目录：`skills/cdp/`
- Skill 入口：`skills/cdp/SKILL.md`
- Skill 名称：`cdp`
- Skill 元数据：`skills/cdp/skill.json`
- Codex UI 元数据：`skills/cdp/agents/openai.yaml`

目录名和 `SKILL.md` frontmatter 中的 `name` 保持一致。这能兼容 Agent Skills 规范，也能让短名称调用更稳定。

## 内置参考

`cdp` 内置了 `references/karpathy-guidelines.md`，作为 MIT 协议的编码 Agent 行为参考：先思考再编码、保持简单、做外科手术式修改，并定义可验证的成功标准。

对于 Level M、Level L 和 Level XL 任务，Agent 必须先读取这份参考，再输出计划、设计或开始实现。对于 Level S 任务，读取这份参考是可选的，以保持简单改动足够轻量；仅在当前任务已有失败尝试，或通过 Level S Reverse Check 后仍需要额外最小改动约束时读取。共享代码、多模块影响、设计 token/基础组件、生成代码、公共配置或高风险路径重叠都必须触发重新分级，而不是继续停留在 Level S。

这份参考已经随 `cdp` 打包，用户不需要额外安装 `karpathy-guidelines`。

如果安装后的环境中缺少 `references/karpathy-guidelines.md`，Agent 不应阻塞流程，而应继续以 cdp 规则作为事实来源，并说明这份辅助参考不可用。

## 目标存在性校验

修改已有目标前，Agent 必须先确认用户要求修改的目标确实存在于代码库中。

例如，用户要求修改一个按钮时，Agent 应先定位这个按钮。如果按钮不存在，或无法唯一确认是哪一个按钮，Agent 应暂停并询问用户：是要新增按钮、修改另一个按钮，还是修正需求描述。

对于新模块、新服务、顶层工作流或架构设计，Agent 仍要先快速搜索是否已有相同名称或相同目的的模块、路由、包或工作流，避免重复建设。若存在相似目标，应优先视为扩展已有目标，除非用户明确确认要新建。

这条规则适用于所有工作流等级，包括简单的 Level S 改动。它用于避免 Agent 猜测目标，或在用户要求“修改已有目标”时静默创建新目标。

## 需求理解

目标存在性校验之后，Agent 应先复述用户想要什么，再进入计划、分级或修改。

这部分必须对用户可见，不能只放在 Agent 内部思考中。它应识别用户意图、当前行为、预期行为、可见变化，以及是否存在隐藏业务变化。对于简单的 Level S 任务，可以保持很短：

```text
Understanding: Change the submit button color only. No behavior change.
```

## 需求拆解

风险分级之前，Agent 应把需求拆成可能影响的区域：

- UI / 样式
- 前端交互
- 状态管理
- API 请求/响应
- 后端逻辑
- 数据库结构
- 权限/认证
- 定时任务
- 缓存失效
- 事件、Webhook 和消息消费者
- 账单/订阅/IAP
- 报表/指标
- 第三方 API 集成
- CDN/静态资源
- 本地化/i18n
- 无障碍/合规
- 生产配置
- 测试

这部分必须在任何计划、审批请求或修改前对用户可见。这一步的目的不是写长文档，而是避免漏掉隐藏风险。对于 Level M，必须包含在极简计划里。

## 风险分级

Agent 只能在需求闸门通过、需求理解和需求拆解之后，对任务进行 Level S、Level M、Level L 或 Level XL 的初始分级。

风险等级采用可检查规则：

- Level S 必须同时满足：单一非共享目标、仅本地静态展示、不改变行为/数据/契约/配置、证据充分且一致，并完整通过 Level S Reverse Check。
- Level M 必须同时满足：单一且有边界的可逆功能流、输入/输出/失败行为明确、不涉及共享或全局表面、不含高风险信号、证据充分且一致，并完整通过 Level M Reverse Check。
- Level L 只要出现任一共享组件/主题/全局状态、条件渲染/权限、缓存、埋点、i18n、配置、任务/事件、持久化数据写入、计费、认证授权或生产配置等信号就成立。
- Level XL 适用于新模块/服务、架构或重大数据流重设计、协调迁移，或需要审批控制的分阶段交付。

在最终判定 S/M 前，Agent 必须按顺序完整运行下面两类 Checklist。这些是实际工作门禁，不是仅供参考的清单；最终分级时每一行都必须填写状态和证据。

### 强制升级 Checklist

每一行使用 `CLEAR`、`HIT` 或 `UNKNOWN`。

| ID | 检查项 | 结果 | 证据 |
|---|---|---|---|
| ESC-01 | 共享组件/基础组件、主题/token/共享样式或全局状态 | `CLEAR / HIT / UNKNOWN` | 已检查来源 |
| ESC-02 | 条件渲染、功能开关、权益、权限或用户特定行为 | `CLEAR / HIT / UNKNOWN` | 已检查来源 |
| ESC-03 | 持久化数据写入/删除、schema、迁移、回填或用户数据 | `CLEAR / HIT / UNKNOWN` | 已检查来源 |
| ESC-04 | 计费/支付/订阅/定价、认证或授权 | `CLEAR / HIT / UNKNOWN` | 已检查来源 |
| ESC-05 | 报表、分析、遥测、埋点、收入/成本/ROI 或业务指标 | `CLEAR / HIT / UNKNOWN` | 已检查来源 |
| ESC-06 | 缓存、定时/同步任务、队列/重试/幂等、事件/webhook/consumer | `CLEAR / HIT / UNKNOWN` | 已检查来源 |
| ESC-07 | i18n、无障碍、合规、安全、隐私或可观测性敏感行为 | `CLEAR / HIT / UNKNOWN` | 已检查来源 |
| ESC-08 | 应用、部署、环境或生产配置 | `CLEAR / HIT / UNKNOWN` | 已检查来源 |
| ESC-09 | 第三方 API、外部契约、CDN/静态资源交付或发布打包 | `CLEAR / HIT / UNKNOWN` | 已检查来源 |
| ESC-10 | 架构/新模块/服务、重大重设计/重构、协调迁移或分阶段发布 | `CLEAR / HIT / UNKNOWN` | 已检查来源 |
| ESC-11 | 证据不足，无法排除更高风险 | `CLEAR / HIT / UNKNOWN` | 明确缺口 |
| ESC-12 | 关于范围、行为、归属、风险或影响的证据发生实质冲突 | `CLEAR / HIT / UNKNOWN` | 冲突来源 |

任一 `HIT` 至少升级到 Level L；ESC-10 涉及架构、新模块/服务、重大重设计、协调迁移或分阶段交付时使用 Level XL。任一 `UNKNOWN` 都禁止最终判定 S/M，并进入 Evidence Gap Handling。证据实质冲突时进入 Evidence Conflict Handling；冲突影响计划含义时保持 `BLOCKED`。

### Level S Reverse Check

仅当全部升级项都是 `CLEAR` 时运行。每一行都为 `PASS` 才能使用 Level S。

| ID | Level S 必须满足 | 结果 | 证据 |
|---|---|---|---|
| S-01 | 只有一个已定位且非共享的目标 | `PASS / FAIL / UNKNOWN` | 目标/使用证据 |
| S-02 | 仅涉及文案、间距、颜色、图标尺寸或静态展示 | `PASS / FAIL / UNKNOWN` | 行为证据 |
| S-03 | 不改变行为/状态/API/数据/契约/配置/生成产物 | `PASS / FAIL / UNKNOWN` | 已检查来源 |
| S-04 | 验收与验证可在该目标局部完成 | `PASS / FAIL / UNKNOWN` | 验证证据 |
| S-05 | 范围明确、可逆，且不需要相邻清理或重构 | `PASS / FAIL / UNKNOWN` | 范围证据 |
| S-06 | 证据充分且一致，并且升级清单全部 `CLEAR` | `PASS / FAIL / UNKNOWN` | 证据摘要 |

任一 `FAIL` 都使 Level S 不成立；如果没有命中升级信号，继续评估 Level M，不要自动跳到 Level L。任一 `UNKNOWN` 进入 Evidence Gap Handling。

### Level M Reverse Check

仅当全部升级项都是 `CLEAR` 时运行。每一行都为 `PASS` 才能使用 Level M。

| ID | Level M 必须满足 | 结果 | 证据 |
|---|---|---|---|
| M-01 | 只有一个边界清晰的功能或用户流 | `PASS / FAIL / UNKNOWN` | 流程边界 |
| M-02 | 模块、输入、输出、状态变化和失败行为均已确认 | `PASS / FAIL / UNKNOWN` | 已检查来源 |
| M-03 | 不涉及共享/全局表面或公共/共享契约 | `PASS / FAIL / UNKNOWN` | 使用/契约证据 |
| M-04 | 不需要迁移、发布协调、契约重设计、新模块/服务或架构决策 | `PASS / FAIL / UNKNOWN` | 依赖/设计证据 |
| M-05 | 改动可逆且验证策略明确 | `PASS / FAIL / UNKNOWN` | 回退/测试证据 |
| M-06 | 证据充分且一致，并且升级清单全部 `CLEAR` | `PASS / FAIL / UNKNOWN` | 证据摘要 |

任一 `FAIL` 都使 Level M 不成立；应采用证据支持的最高 L/XL 规则，或在无法确定时继续澄清。任一 `UNKNOWN` 进入 Evidence Gap Handling。

用户可见计划包含精简的 `Risk Gate Result`：升级清单结果、反向检查结果、证据引用和最终风险等级。这样可以证明门禁已实际运行，同时不暴露私有思维链，也不让小改动计划变得冗长。

初始风险分级应和需求理解、需求拆解一起对用户可见。

## 基于证据的思考

完成初始风险分级后，Agent 应基于具体代码证据进行思考，再输出计划。

对于 Level M、Level L 和 Level XL 任务，计划或设计必须建立在实际文件、符号、字段、schema、API、配置项、调用点或搜索结果之上。Agent 应在计划前明确列出已确认的证据和仍未确认的假设，并识别影响工作流等级的风险边界。

完成证据检查后，Agent 应最终确认或升级风险等级。如果证据显示存在更高风险区域，应立即重新分级，并切换到更严格的工作流。

如果证据不足，Agent 应记录缺失项，继续安全的只读检查，或提出最少的定向问题。无法排除高风险时采用临时 Level L 控制；缺口影响范围、行为、风险或审批含义时，managed planning 必须进入 BLOCKED。

如果证据冲突，Agent 应列出冲突结论及来源，采用各可信来源支持的最高风险等级，请求权威决策，并在冲突解决前将计划标记为 BLOCKED。不得为了方便选择低风险解释。

Level S 应保持简洁，但仍需要足够的文件或搜索证据来定位准确目标，避免改错文案、样式来源或组件。

## Scope Lock 契约

每个可审批或可交接计划都必须包含内部 `Scope-Lock-Version: cdp-scope/v1`，并具备 `in_scope`、`out_of_scope`、`non_goals`、`assumptions`、`stop_conditions`、`will_change`、`will_not_change` 和高层 `acceptance_criteria` 八个数组字段。

该区块是唯一范围事实源。CDF 和 CDTask 必须原样复制，不得改写、弱化、遗漏或扩大。任何必要扩展都必须返回 CDP 重新规划并再次审批。

## 工作流等级

### Level S：轻量计划与决策

用于简单 UI、文案和样式改动。

示例：

- 按钮颜色。
- 文案措辞。
- 间距。
- 图标尺寸。
- 静态 UI 调整。

Agent 行为：

- 输出精简 Development Plan 和 Scope Lock。
- 推荐 `Execute Now`，然后等待用户明确选择 Next Action。
- 不输出长计划。
- 修改后提供简短总结、已执行的验证和相关人工检查项。

### Level M：简短计划与决策

用于普通、范围明确的小功能改动。

示例：

- 添加筛选器。
- 修改表单行为。
- 添加校验规则。
- 修改小范围 API 调用。
- 调整单个页面交互。

Agent 行为：

- 先给基于证据的极简计划。
- 包含规范化 Scope Lock 并推荐 Next Action。
- 在实现或保存 task 前等待用户明确选择 Next Action。
- 修改后提供已执行的验证和相关人工检查项。

Level M 极简格式：

```md
I’ll treat this as Level M.

Understanding:
- ...

Requirement Decomposition:
- ...

Evidence:
- ...

Risk Gate Result:
- Escalation Checklist: All rows: CLEAR
- Reverse Check: Level M — PASS
- Evidence: ...
- Final Risk Level: Level M

Plan:
1. ...
2. ...

Recommendation: Execute Now because this is scoped and passed the Level M Reverse Check. Awaiting explicit user choice.
```

### Level L：需要确认

用于高风险改动。

示例：

- 数据库结构。
- 支付、账单、订阅或 IAP 逻辑。
- 报表、收入、成本、ROI 或业务指标逻辑。
- 认证或权限。
- 定时任务、同步任务、队列、重试或幂等逻辑。
- 生产或部署配置。

Agent 行为：

- 不立即修改。
- 说明需求理解。
- 使用 `Will Change` 和 `Will Not Change` 定义修改范围、受影响模块，并给出独立验收标准。
- 提出实现计划。
- 说明风险和测试计划。
- 等待确认后再执行。

### Level XL：需要设计

用于架构级或模块级改动。

示例：

- 新模块或新后端服务。
- 大型重构。
- 完整报表流水线。
- 权限系统。
- App Store Connect API 集成。
- 广告统计流水线。

Agent 行为：

- 先产出设计。
- 将实现拆成有明确边界的阶段。
- 延期保存为本地 task 时，必须保留已批准的设计、数据/API/状态流、验收标准和当前阶段边界。
- 对大型或高风险设计，默认按阶段确认。
- 如果实现中发现设计假设失效，或某个阶段发生实质变化，应暂停并更新设计，重新确认后继续。
- 避免一次性大范围失控修改。

## 执行中的重新分级

如果实现过程中发现比原分级更高风险的区域，Agent 应立即停止继续编辑，说明触发升级的新证据，并从更严格工作流的必需审批模板重新进入。Level S 或 M 发现高风险逻辑时必须升级为 Level L。Level L 如果需要架构、新服务、分阶段发布或重大数据流重设计，必须升级为 Level XL。

如果已有部分编辑造成语法错误、导入损坏、格式化失败，或仅由半完成编辑导致构建/测试失败，Agent 可以先做最小修复或回退以恢复工作区一致性，再等待更严格审批。该修复不能扩大范围。

## 审批与验证

对于 Level L 和 Level XL，有效批准必须同时明确“动作”和获批的 Scope Lock、阶段、任务或子集。`Approve and implement`、`批准并实施`、`同意按此范围执行` 等属于明确批准；单独的 `ok`、`继续`、`可以`、`嗯`、`Proceed` 或 `go ahead` 无效，Agent 必须使用简短的上下文追问模板再次确认。

CDP 支持完整批准、带条件批准和部分批准。条件必须写入 Scope Lock；部分批准必须生成正向字段只包含获批工作的子集 Scope Lock，并把其余内容明确标记为未批准。任何扩大范围的条件都必须重新规划并再次审批。

完整批准或带条件批准生效后，CDP 必须回显 Locked Scope Summary，至少包含 `in_scope`、`will_not_change`、`non_goals`、批准类型和授权动作，并原样复制已批准内容。

部分批准使用独立结果，让用户一眼看清边界：

````md
## Partial Approval Result

Approval Type: partial
Authorized Action: <Execute Now | Save as CDTask | Return Approved Plan Package to CDF>

### Approved Scope
- <从获批子集 Scope Lock 的 `in_scope` 原样复制>

### Unapproved / Remaining
Status: NOT APPROVED — MUST NOT BE IMPLEMENTED / 未批准，不得实施
- <从 Approval Record 的剩余项原样复制>

### Approved-Subset Scope Lock

```yaml
Scope-Lock-Version: cdp-scope/v1
in_scope: [...]
out_of_scope: [...]
non_goals: [...]
assumptions: [...]
stop_conditions: [...]
will_change: [...]
will_not_change: [...]
acceptance_criteria: [...]
```
````

已批准范围、剩余项和完整子集 Scope Lock 都必须原样复制。如果无法在不新增假设或改写语义的前提下隔离子集，CDP 必须追问或重新规划，不得交接。

每个 standalone Development Plan 都提供两个明确选项；Level L 和 Level XL 只有在高风险范围审批门禁通过后才能使用：

- `Execute Now`（`Approve and implement` / `同意并修改`）：授权修改当前展示的 Scope Lock 或当前获批阶段内的代码。
- `Save as CDTask`（`Approve and save as local task` / `同意并保存为本地 task`）：批准 Scope Lock、延期实施，并把 `cdp-cdtask/v1` 交接包交给 `cdtask`。

延期保存选项不授权当前回合修改实现文件。CDTask 会校验交接包和 Scope Lock、生成依赖感知的任务拆分、运行 Task Readiness Gate，并以 `status: ready_for_resume` 保存。用户指定路径时优先使用；否则默认保存到当前工作区的 `_cdtask/YYYY-MM-DD-<slug>.md`。

CDP 会在生成交接包或创建本地文件之前检查 CDTask 是否可用。如果 CDTask 不可用，CDP 不创建 `_cdtask`、不保存降级文档，也不自动安装，只输出：

```bash
npx skills add https://github.com/webszy/my-skills --skill cdtask -a codex -a claude-code -g -y
```

安装完成后，用户需要再次选择 `Approve and save as local task` / `同意并保存为本地 task`。

保存后的 task 支持两条路径：

- Path A：用户明确请求 `Continue local task: <path>` 或 `继续执行本地 task：<path>`。CDP 会重新检查目标、代码证据、风险、分支和 commit；没有实质变化时，该请求授权执行已保存范围。
- Path B：用户明确把 task 交给外部 coding agent。该 Agent 只能实现 Task Breakdown，并遵守 Scope Guard 和 Handoff Rules。CDP 不会自动把外部执行视为完成；需要 CDP 管理收尾时，应把结果带回 CDP 验证或关闭。

文档处于 ready 状态本身不代表获得实施授权。如果存在实质漂移，则必须重新输出审批请求。

如果用户在审批请求后回复的是新需求，而不是明确批准，上一版审批请求应视为过期。Agent 应合并新需求，重新执行分级和证据检查，并为修订后的方案重新请求确认。

验证应匹配变更风险区域。例如 schema 改动需要 schema 或 migration 验证，账单/报表改动需要计算路径检查，认证改动需要允许和拒绝路径检查。验证失败时，只有仍在已批准范围内的修复可以继续；扩大范围必须重新请求确认。

对于 Level L 和 Level XL，最终回复应包含结构化的 Traceability 字段。在 git 工作区中，Agent 应主动查询当前分支和最新 commit；如果溯源信息不可用，应说明原因。

## 边界案例

完整双语对话见 [边界案例](references/boundary-cases.md)，其中覆盖三个控制边界：

1. 看似只改一行颜色，但实际影响共享 Button、全局主题 token 和条件状态；ESC-01、ESC-02 命中，因此最终必须从 S 升到 L。
2. Level L 计划之后用户只回复 `ok，继续`，既没有指定动作，也没有明确范围；CDP 必须再次显示简短的明确授权选项，不实施也不准备任务交接。
3. 权限证据冲突时采用临时 Level L 并保持 `BLOCKED`；用户移除冲突范围后，CDP 必须先展示重新分级的新计划和子集 Scope Lock。只有后续明确批准才能授权展示最终部分批准结果，并把可独立成立的文案子集交给 CDTask。

这些是决策模式，不是产品默认值。如果看似可分离的子集仍依赖未解决证据，继续保持 `BLOCKED`。

## 安装

安装到 Codex：

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a codex -g -y
```

安装到 Claude Code：

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a claude-code -g -y
```

同时安装到 Codex 和 Claude Code：

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a codex -a claude-code -g -y
```
