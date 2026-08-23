# Coding Discipline

These guidelines reduce common coding-agent mistakes during CDF planning and approved execution. They are adapted from the [Karpathy Guidelines skill](https://github.com/szkocot/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md), which in turn draws on [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876).

They bias toward deliberate, surgical work. Apply them proportionally: a trivial, well-evidenced change should stay fast.

## Think before changing code

- State implementation-affecting assumptions; do not hide uncertainty.
- Surface materially different interpretations and tradeoffs.
- Prefer the simpler approach when it satisfies the approved acceptance criteria.
- If evidence is missing or contradictory, name the uncertainty and inspect or ask rather than guessing.
- Stop when new evidence would change risk, approved scope, or acceptance criteria.

## Keep the solution minimal

- Implement only behavior authorized by the canonical Scope Lock.
- Do not add speculative features, extensibility, configuration, abstractions, or dependencies.
- Do not add handling for impossible states unless repository evidence shows they are possible.
- Favor the smallest change that meets the approved outcome and existing project conventions.
- If the implementation is substantially larger than the behavior warrants, reconsider the design before continuing.

## Make surgical edits

- Touch only files and lines required by the approved work.
- Do not refactor, reformat, rename, or clean up adjacent code unless it is in scope.
- Match the repository's established style and patterns.
- Remove imports, variables, functions, or files made obsolete by the current change.
- Report unrelated defects or dead code; do not silently fix or delete them.

Every changed line should trace to an approved plan step, an acceptance criterion, or a necessary verification fix.

## Work toward observable goals

Turn each plan step into an outcome with a matching check:

```text
1. <change> -> verify: <observable check>
2. <change> -> verify: <observable check>
```

Examples:

- “Add validation” becomes “cover the rejected inputs, then make those checks pass.”
- “Fix the bug” becomes “reproduce the failure, apply the bounded fix, then verify the reproduction no longer fails.”
- “Refactor” becomes “preserve the specified behavior before and after the approved structural change.”

Run checks in proportion to risk and project capability. Do not claim a check passed unless it actually ran. Distinguish a planned verification strategy from execution evidence.

## Respect control boundaries

- Approval authorizes only the displayed canonical Scope Lock and selected next action.
- Do not infer permission for adjacent cleanup, dependency changes, protected areas, or a broader rollout.
- A task document or passing test does not authorize scope expansion.
- If safe completion requires new modules, interfaces, behavior, acceptance criteria, or broader write scope, stop and return to CDF planning for a revised Scope Lock and renewed approval.

For worked examples, read [Boundary Cases](boundary-cases.md).

