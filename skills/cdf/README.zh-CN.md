# CDF：Controlled Development Flow

CDF 是受控开发流程的唯一用户入口：理解需求、检查仓库证据、分级风险、规划并锁定范围，获得明确人工批准后执行或保存任务。CDTask 只是内部编译组件，不是独立 Skill、服务或运行平台。

**小修改保持快速，高风险修改保持受控。**

- Skill Package Version：**1.3.0**
- CDF Suite Maturity：**v0.1**，与包版本是不同概念
- 合同：`cdf-scope/v1`、`cdf-cdtask/v2`、`cdf-execution-progress/v2`

## 使用方式

显式调用 `$cdf`、`/cdf`、`cdf:`、`controlled-development-flow`，或明确要求受控开发流程。保留 Codex 的显式调用策略，引用均相对 skill 目录解析，支持 Codex 与 Claude Code。

```text
$cdf 分析这个功能，然后询问我是否批准执行。
$cdf 先生成任务拆分草案，不执行、不保存。
$cdf 批准已展示的方案并保存为任务。
$cdf continue task <path>
$cdf validate task <path> without executing it
```

授权必须对应具体展示的方案及动作。已明确选择执行／保存时，只确认该动作，不再提供重复二选一。范围或动作不明确时，“ok／可以／继续”和沉默仍不能构成授权。只读草案不标记已批准，不创建正式任务、进度或执行授权。

## 流程

```text
需求 → Requirement Gate → 仓库证据 → 风险 → 计划 → Scope Lock → 人工批准
  Execute Now → 范围内实施
  Save as Task → 内部编译 → 持久化／回读验证 → 停止
    → 本回合明确恢复请求 + 完整性／历史进度／漂移检查 → 范围内实施
→ 任务局部验证 → 产品最终验收 → Completion Evidence Gate
→ 最终范围内评审（以及原流程确实要求的审批）→ Completed
```

S 级使用四行快速计划；M／L／XL 默认简述需求理解、技术方案、实施与验证、风险。内部保留完整分析，保存时使用固定十一节 Development Plan；格式展开不得引入隐藏义务。

如果仅在单个调用点使用共享组件已经支持的静态样式参数，且不修改组件定义、公共接口、全局 token、行为及其他消费者，并能独立验证／回滚，通过全部 S Reverse Check 后可以是 S。共享定义／接口修改至少重新评估 M，跨页面或全局影响可能达到 L。不能只根据文件数判断风险。

## v1.3.0 修复

- **局部验证与最终验收分离**：产品 AC 仍由不可变规范 Scope Lock 唯一定义；`contributes_to` 表示贡献，`task_verification` 引用已批准的局部检查。API 局部 verified 后可推进前端，完整登录 AC 仍需集成验证。
- **保存时完整性基线**：保存时即计算范围、审批和完整定义 SHA-256。完整定义只排除自身摘要的 frontmatter 行；最终回读、首次执行及每次恢复重新计算。缺失／不匹配时不能补摘要洗白。自包含摘要只能提供有限完整性检查，不是授权签名。
- **合法返工**：v2 进度日志支持受控 `verified → in_progress → verified`，记录原因和范围证据、保留历史、使旧证据及下游检查失效。新范围或决策必须停止并重新规划审批。
- **最终评审可追溯**：结项检查全部产品 AC、实际检查、diff／范围证据、门禁 PASS，再记录最终评审结果、证据、源码快照、时间、未解决问题及适用审批。评审后相关修改使受影响验证／评审失效。不凭空增加人工审批。
- **旧版本保护**：旧 v1 任务和 sidecar 保留只读，经明确核对、重新审批后另存新任务；不得覆盖原 Approval Record／历史、直接升级版本号或自动执行。

任务仍为 Markdown。v2 的 YAML frontmatter 使用 JSON 值，结构化区块使用 JSON 围栏，运行进度使用 JSON 兼容 YAML，让校验器只依赖 Python 标准库。Scope 的 v1 字段及语义不变，v2 任务使用明确的窄序列化格式。格式应在批准前确定，不得为了通过解析／摘要而重写已批准 payload。

## 校验与复测

在仓库根目录执行：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/cdf/tests -p 'test_*.py' -v
python3 skills/cdf/scripts/validate_cdf.py --describe
python3 skills/cdf/scripts/validate_cdf.py <task.md>
python3 skills/cdf/scripts/validate_cdf.py <task.md> --progress <task.md.progress.yaml> --snapshot <实际当前源码摘要>
```

CLI 只读；退出 0 只表示机械校验有效，不代表产品语义通过、人工批准或执行授权。退出 1 返回 JSON 错误，并始终列出尚需语义审核的事项。`--draft-hashes` 只用于刚获批且尚未正式保存的候选文件，不能修补已有任务基线；`--previous-progress` 可对照保留的旧进度检查历史未被改写。

[校验记录](tests/validation-results.md) 区分已执行脚本测试与未执行的 Agent 行为用例。合成 fixture 只证明协议机械规则，不证明真实人工授权、登录功能、视觉效果或 Agent 在实际宿主中的遵循情况。

CDF 回复第一行使用从 metadata 读取的 `当前流程：cdf v<version>`；披露当前 Agent 实际动作和无关改动，包括已撤回改动，没有／无法确认时如实说明。S 级默认可简化为 `Changed`、`Verified`、`Scope`、`Remaining Issues`，内部完整证据不能省略，失败和缺口不能隐藏。

## 按路线加载参考

- [SKILL.md](SKILL.md)：入口、控制门、S 风险检查、审批。
- [需求门](references/requirement-gate.md)、[风险分级](references/risk-classification.md)、[开发纪律](references/karpathy-guidelines.md)：按规划需要加载。
- [Task Handoff](references/task-handoff.md)、[CDTask](components/cdtask/COMPONENT.md)、[任务模板](components/cdtask/references/task-templates.md)、[持久化](components/cdtask/references/persistence.md)：保存路线。
- [恢复与兼容](references/resume.md)、[执行进度](references/execution-progress.md)：已保存任务的检查／执行。
- [完成证据门](references/completion-evidence-gate.md)：评估完成时。
- [边界案例](references/boundary-cases.md)：风险、审批及范围边界。

## 安装

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -a claude-code -g -y
```

单宿主只保留 `-a codex` 或 `-a claude-code` 即可，无需独立安装 CDTask。
