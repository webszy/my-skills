# npx skills installation

Use this reference when preparing the risk-based development workflow Skill for installation with `npx skills`.

## Repository layout

Keep the skill at:

```text
skills/cdf/
  SKILL.md
  agents/openai.yaml
  references/install.md
```

Do not add extra documentation inside the skill folder unless it is required by the agent at runtime.

## Install from GitHub

After pushing the repository to GitHub, install the skill for Codex with:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -g -y
```

Install for Claude Code with:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a claude-code -g -y
```

Install for both with:

```bash
npx skills add https://github.com/webszy/my-skills --skill cdf -a codex -a claude-code -g -y
```

## Validation checklist

- `SKILL.md` exists at the skill root.
- `SKILL.md` frontmatter contains only `name` and `description`.
- The skill folder name matches the frontmatter `name`.
- `agents/openai.yaml` has quoted string values.
- No generated or placeholder files remain in the skill folder.
- The workflow describes Level S, Level M, Level L, and Level XL behavior.
