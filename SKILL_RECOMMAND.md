# Webszy Skills 清单与安装命令

> 盘点日期：2026-08-21  
> 仅保留非 OpenAI GitHub 仓库来源的独立 Skills；不包含 Codex 内置 Skills、OpenAI 仓库 Skills 或插件。

| Skill 名 | 安装命令 | 简单说明 |
|---|---|---|
| `remotion-best-practices` | `npx skills add remotion-dev/skills --skill remotion-best-practices` | Remotion 视频项目最佳实践。 |
| `frontend-design` | `npx skills add anthropics/skills --skill frontend-design` | 前端界面设计与实现指导。 |
| `ui-ux-pro-max` | `npx skills add nextlevelbuilder/ui-ux-pro-max-skill --skill ui-ux-pro-max` | UI/UX 设计辅助与视觉规范。 |
| `react-best-practices` | `npx skills add 0xbigboss/claude-code --skill react-best-practices` | React 开发最佳实践。 |
| `code-review-expert` | `npx skills add sanyuan0704/sanyuan-skills --skill code-review-expert` | 专业代码审查流程。 |
| `sigma` | `npx skills add sanyuan0704/sanyuan-skills --skill sigma` | 通用工程工作流 Skill。 |
| `skill-forge` | `npx skills add sanyuan0704/sanyuan-skills --skill skill-forge` | 创建和打磨 Agent Skills。 |
| `karpathy-guidelines` | `npx skills add forrestchang/andrej-karpathy-skills --skill karpathy-guidelines` | Karpathy 风格的简洁编码指导。 |
| `vue` | `npx skills add antfu/skills --skill vue` | Vue 项目开发指导。 |
| `uni-app` | `npx skills add uni-helper/skills --skill uni-app` | uni-app 项目开发指导。 |
| `responsive-web-design` | `npx skills add aj-geddes/useful-ai-prompts --skill responsive-web-design` | 响应式 Web 设计实践。 |
| `design-taste-frontend` | `npx skills add leonxlnx/taste-skill --skill design-taste-frontend` | 前端视觉设计与品味指导。 |
| `cdf` | `npx skills add webszy/my-skills --skill cdf` | 来自 webszy/my-skills 的工作流。 |
| `cdtask` | `npx skills add webszy/my-skills --skill cdtask` | 来自 webszy/my-skills 的任务工作流。 |

## 安装说明

- 官方推荐在 Codex 中使用 `$skill-installer <skill-name>` 安装精选 Skill。
- 表中的 `npx skills add ... --skill ...` 用于从对应 GitHub 仓库安装单个 Skill。
- 同名 Skill 如果已经存在，请先确认目标目录，避免覆盖自己的修改。
- 安装后若未出现，重启 Codex。

## 核对来源

- [OpenAI 官方：Build skills](https://learn.chatgpt.com/docs/build-skills)
