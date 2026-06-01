# cdf

`cdf` 是 `controlled-development-flow` 的简称：一个面向 AI Coding Agent 的风险分级开发工作流 Skill。

它帮助 Agent 避免两类常见问题：

- 对简单改动过度规划。
- 对高风险改动执行过快。

核心原则：

> 小改动要快，风险改动要可控。

## 兼容性

`cdf` 遵循 Codex 和 Claude Code 使用的 Agent Skills `SKILL.md` 格式：

- Skill 目录：`skills/cdf/`
- Skill 入口：`skills/cdf/SKILL.md`
- Skill 名称：`cdf`
- Skill 元数据：`skills/cdf/skill.json`
- Codex UI 元数据：`skills/cdf/agents/openai.yaml`

目录名和 `SKILL.md` frontmatter 中的 `name` 保持一致。这能兼容 Agent Skills 规范，也能让短名称调用更稳定。

## 目标存在性校验

修改前，Agent 必须先确认用户要求修改的目标确实存在于代码库中。

例如，用户要求修改一个按钮时，Agent 应先定位这个按钮。如果按钮不存在，或无法唯一确认是哪一个按钮，Agent 应暂停并询问用户：是要新增按钮、修改另一个按钮，还是修正需求描述。

这条规则适用于所有工作流等级，包括简单的 Level S 改动。它用于避免 Agent 猜测目标，或在用户要求“修改已有目标”时静默创建新目标。

## 工作流等级

### Level S：直接修改

用于简单 UI、文案和样式改动。

示例：

- 按钮颜色。
- 文案措辞。
- 间距。
- 图标尺寸。
- 静态 UI 调整。

Agent 行为：

- 直接修改。
- 不请求确认。
- 不输出长计划。
- 修改后提供简短总结和测试步骤。

### Level M：简短计划后修改

用于普通、范围明确的小功能改动。

示例：

- 添加筛选器。
- 修改表单行为。
- 添加校验规则。
- 修改小范围 API 调用。
- 调整单个页面交互。

Agent 行为：

- 先给简短计划。
- 需求清晰时直接继续执行。
- 仅在需求有歧义时提问。
- 修改后提供测试步骤。

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
- 定义修改范围和受影响模块。
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
- 将实现拆成阶段。
- 等待确认。
- 避免一次性大范围失控修改。

## 安装

安装到 Codex：

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -g -y
```

安装到 Claude Code：

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a claude-code -g -y
```

同时安装到 Codex 和 Claude Code：

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -a claude-code -g -y
```
