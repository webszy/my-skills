# 本机 Skills 清单与安装命令

> 盘点日期：2026-08-22
> 汇总 `~/.agents`、`~/.codex`、`~/.claude` 中实际安装的 Skills，跨目录按 Skill 名去重；同一仓库的大型 Skill 集合可折叠为一条安装记录。
> 不包含 Codex 自带 Skills、OpenAI 插件 Skills、缓存/临时市场镜像，并排除指定 Skill。

## 一、理论与方法论类

适用于学习方法、开发工作流、Skill 发现以及内容创作方法。

| Skill 名 | 安装命令 | 简单说明 |
|---|---|---|
| `cdf` | `npx skills add webszy/my-skills --skill cdf` | Controlled development flow that inspects requirements and repository evidence, classifies risk, locks scope, obtains approval, then executes or saves a resumable task. |
| `find-skills` | `npx skills add vercel-labs/skills --skill find-skills` | Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can…                                                                         |
| `karpathy-guidelines` | `npx skills add forrestchang/andrej-karpathy-skills --skill karpathy-guidelines` | Behavioral guidelines to reduce common LLM coding mistakes. Use when writing, reviewing, or refactoring code to avoid overcomplication, make…                                                                         |
| `sigma` | `npx skills add sanyuan0704/sanyuan-skills --skill sigma` | Personalized 1-on-1 AI tutor using Bloom's 2-Sigma mastery learning. Guides users through any topic with Socratic questioning, adaptive paci…                                                                         |
| `chapter-writing` | `npx skills add danjdewhurst/story-skills --skill chapter-writing` | This skill should be used when the user asks to "write a chapter", "next chapter", "chapter outline", "draft chapter", "continue the story",…                                                                         |
| `character-management` | `npx skills add danjdewhurst/story-skills --skill character-management` | This skill should be used when the user asks to "create a character", "update a character", "add a character", "build a family tree", "chara…                                                                         |
| `plot-structure` | `npx skills add danjdewhurst/story-skills --skill plot-structure` | This skill should be used when the user asks to "create a plot arc", "story structure", "add a plot point", "story timeline", "track foresha…                                                                         |
| `story-init` | `npx skills add danjdewhurst/story-skills --skill story-init` | This skill should be used when the user asks to "start a new story", "initialize a story project", "create a story", "new book", "set up a s…                                                                         |
| `worldbuilding` | `npx skills add danjdewhurst/story-skills --skill worldbuilding` | This skill should be used when the user asks to "create a location", "add a location", "magic system", "political system", "build the world"…                                                                         |

## 二、编程语言与应用开发类

适用于编程语言、前端框架、Swift/iOS 和 UI 应用开发。

| Skill 名 | 安装命令 | 简单说明 |
|---|---|---|
| `golang-modernize` | `npx skills add samber/cc-skills-golang --skill golang-modernize` | Modernize Golang code to use recent language features, standard library improvements, and idiomatic patterns. Trigger proactively when writi…                                                                         |
| `kotlin-specialist` | `npx skills add jeffallan/claude-skills --skill kotlin-specialist` | Provides idiomatic Kotlin implementation patterns including coroutine concurrency, Flow stream handling, multiplatform architecture, Compose…                                                                         |
| `swift-expert` | `npx skills add jeffallan/claude-skills --skill swift-expert` | Use when building iOS/macOS applications with Swift 5.9+, SwiftUI, or async/await concurrency. Invoke for protocol-oriented programming, Swi…                                                                         |
| `swift-ios-skills（86 个）` | `npx skills add dpearson2699/swift-ios-skills --all` | [iOS 26+、Swift 6.3、SwiftUI 与现代 Apple 框架 Skill 集合](https://github.com/dpearson2699/swift-ios-skills)。远端共 86 个，本机已安装 84 个；缺少 `ios-ettrace-performance`、`ios-memgraph-analysis`。                                         |
| `vue` | `npx skills add antfu/skills --skill vue` | Vue 3 Composition API, script setup macros, reactivity system, and built-in components. Use when writing Vue SFCs, defineProps/defineEmits/d…                                                                         |
| `nuxt` | `npx skills add antfu/skills --skill nuxt` | Nuxt full-stack Vue framework with SSR, auto-imports, and file-based routing. Use when working with Nuxt apps, server routes, useFetch, midd…                                                                         |
| `nuxt-ui` | `npx skills add onmax/nuxt-skills --skill nuxt-ui` | Use when building styled UI with @nuxt/ui v4 components - create forms with validation, implement data tables with sorting, build modal dial…                                                                         |
| `mobile-responsiveness` | `npx skills add hoodini/ai-agents-skills --skill mobile-responsiveness` | Build responsive, mobile-first web applications. Use when implementing responsive layouts, touch interactions, mobile navigation, or optimiz…                                                                         |
| `frontend-design` | `npx skills add anthropics/skills --skill frontend-design` | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typog…                                                                         |
| `design-taste-frontend` | `npx skills add leonxlnx/taste-skill --skill design-taste-frontend` | Anti-slop frontend skill for landing pages, portfolios, and redesigns. The agent reads the brief, infers the right design direction, and shi…                                                                         |
| `ui-ux-pro-max` | `npx skills add nextlevelbuilder/ui-ux-pro-max-skill --skill ui-ux-pro-max` | UI/UX design intelligence. 50 styles, 21 palettes, 50 font pairings, 20 charts, 9 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native…                                                                         |
| `claude-design-card` | `npx skills add geekjourneyx/claude-design-card --skill claude-design-card` | 本地已安装的 claude-design-card Skill。                                                                                                                                                                                      |

## 三、SDK、云平台与外部集成类

适用于云平台 SDK、通信协作平台、联网能力和第三方归因集成。

| Skill 名 | 安装命令 | 简单说明 |
|---|---|---|
| `agent-reach` | `npx skills add https://github.com/panniantong/agent-reach --skill agent-reach` | 联网搜索各种信息。 |
| `agents-sdk` | `npx skills add cloudflare/skills --skill agents-sdk` | Build AI agents on Cloudflare Workers using the Agents SDK. Load when creating stateful agents, durable workflows, real-time WebSocket apps,…                                                                         |
| `cloudflare` | `npx skills add cloudflare/skills --skill cloudflare` | Comprehensive Cloudflare platform skill covering Workers, Pages, storage (KV, D1, R2), AI (Workers AI, Vectorize, Agents SDK), feature flags…                                                                         |
| `cloudflare-email-service` | `npx skills add cloudflare/skills --skill cloudflare-email-service` | Send and receive transactional emails with Cloudflare Email Service (Email Sending + Email Routing). Use when building email sending (Worker…                                                                         |
| `cloudflare-one` | `npx skills add cloudflare/skills --skill cloudflare-one` | Guides Cloudflare One Zero Trust and SASE work across Access, Gateway, WARP, Tunnel, Cloudflare WAN, DLP, CASB, device posture, and identity…                                                                         |
| `cloudflare-one-migrations` | `npx skills add cloudflare/skills --skill cloudflare-one-migrations` | Plans migrations from Zscaler ZIA/ZPA, Palo Alto, legacy VPN, SWG, or SASE stacks to Cloudflare One. Use for migration assessments, policy m…                                                                         |
| `durable-objects` | `npx skills add cloudflare/skills --skill durable-objects` | Create and review Cloudflare Durable Objects. Use when building stateful coordination (chat rooms, multiplayer games, booking systems), impl…                                                                         |
| `turnstile-spin` | `npx skills add cloudflare/skills --skill turnstile-spin` | Set up Cloudflare Turnstile end-to-end in a project — scan the codebase, create the widget via the Cloudflare API, deploy the managed siteve…                                                                         |
| `web-perf` | `npx skills add cloudflare/skills --skill web-perf` | Analyzes web performance using Chrome DevTools MCP. Measures Core Web Vitals (LCP, INP, CLS) and supplementary metrics (FCP, TBT, Speed Inde…                                                                         |
| `workers-best-practices` | `npx skills add cloudflare/skills --skill workers-best-practices` | Reviews and authors Cloudflare Workers code against production best practices. Load when writing new Workers, reviewing Worker code, configu…                                                                         |
| `wrangler` | `npx skills add cloudflare/skills --skill wrangler` | Cloudflare Workers CLI for deploying, developing, and managing Workers, KV, R2, D1, Vectorize, Hyperdrive, Workers AI, Containers, Queues, W…                                                                         |
| `Lark CLI Skills（28 个）` | `npx skills add larksuite/cli --all` | [飞书/Lark 官方 CLI 的 AI Agent Skills 集合](https://github.com/larksuite/cli)，覆盖消息、文档、多维表格、电子表格、日历、邮箱、任务和会议等。远端共 28 个，本机有 27 个 `lark-*` Skill，其中匹配 26 个；缺少 `lark-meeting`、`lark-note`，本机另有远端正式清单未包含的 `lark-whiteboard-cli`。 |

## 统计

- 分类后共 34 条安装记录：理论与方法论类 9 条、编程语言与应用开发类 12 条、SDK/云平台与外部集成类 13 条。
- 其中两个大型仓库的同源 Skill 已分别折叠为一条仓库级记录。
- `swift-ios-skills` 远端共 86 个 Skill，本机覆盖 84 个，缺少 2 个。
- `larksuite/cli` 远端共 28 个 `lark-*` Skill；本机有 27 个，其中匹配 26 个、缺少 2 个，另有 1 个本机旧项。

## 安装说明

- 有明确来源的条目可使用表中 `npx skills add ...` 命令重新安装。
- 同名 Skill 如果已经存在，请先确认目标目录，避免覆盖自己的修改。
- 安装后若未出现，请重启对应 Agent 客户端。
