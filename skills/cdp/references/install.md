# npx skills installation

Use this reference when packaging CDP for installation with `npx skills`, or when CDP must tell the user how to install CDTask.

Every command below names the skill it installs. Never copy a command from one section to satisfy the other.

## Repository layout

Keep the skill at:

```text
skills/cdp/
  SKILL.md
  README.md
  README.zh-CN.md
  skill.json
  agents/openai.yaml
  references/requirement-gate.md
  references/install.md
  references/karpathy-guidelines.md
```

Do not add extra documentation inside the skill folder unless it is required by the agent at runtime.

## Install CDP from GitHub

After pushing the repository to GitHub, install CDP for Codex with:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a codex -g -y
```

Install CDP for Claude Code with:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a claude-code -g -y
```

Install CDP for both with:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdp -a codex -a claude-code -g -y
```

## Install CDTask from GitHub

CDP never installs anything itself. When the user selects `Save as CDTask` and CDTask is unavailable, output the command that matches the user's agent, then wait for the user to install it and select the action again.

Both agents:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdtask -a codex -a claude-code -g -y
```

Codex only:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdtask -a codex -g -y
```

Claude Code only:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdtask -a claude-code -g -y
```

Every CDTask command names `--skill cdtask`. A `--skill cdp` command reinstalls CDP and leaves CDTask unavailable.

## Validation checklist

- `SKILL.md` exists at the skill root.
- `SKILL.md` frontmatter contains only `name` and `description`.
- The skill folder name matches the frontmatter `name`.
- `agents/openai.yaml` has quoted string values.
- No generated or placeholder files remain in the skill folder.
- The workflow describes Level S, Level M, Level L, and Level XL behavior.
