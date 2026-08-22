# CDTask Persistence Contracts

Read this file only when CDTask will write a task document. Use the contract that matches the input route selected in `../SKILL.md`.

The persistence decision, path convention, and overwrite rules stay in `../SKILL.md`. This file defines what a saved document must contain.

## Table of Contents
- Save Verification
- CDP Deferred Task File
- Manual Task File
- CDF-Managed Task File

## Save Verification

After saving, read the file back and verify:

- frontmatter metadata and contract version;
- workspace and source traceability;
- canonical Scope Lock, verbatim;
- Approval Record;
- the required sections for the selected route;
- tasks and dependency data;
- Scope Guard and Task Readiness Gate;
- destination-specific resume or return rules.

Do not claim success if verification fails.

## CDP Deferred Task File

```yaml
---
task_contract: cdp-cdtask/v1
status: ready_for_resume
source: cdp
approval_state: scope-approved-execution-deferred
risk_level: <Level S | Level M | Level L | Level XL>
workspace: <absolute path>
source_branch: <branch or Unavailable>
source_commit: <commit or Unavailable>
created_at: <ISO-8601 timestamp>
---
```

Required sections:

1. Resume Contract;
2. Approval Record;
3. planning evidence and approved design;
4. canonical Scope Lock, verbatim;
5. dependency order and task breakdown;
6. risks, acceptance criteria, verification, and rollback;
7. handoff paths, Scope Guard, Codex Handoff Rules, and Task Readiness Gate.

## Manual Task File

```yaml
---
task_contract: cdtask/v1
status: ready_for_review
source: manual
approval_state: not-approved-by-cdp
risk_level: Unclassified
workspace: <absolute path>
source_branch: <branch or Unavailable>
source_commit: <commit or Unavailable>
created_at: <ISO-8601 timestamp>
---
```

The document must state that it requires user review or CDP planning before any execution authorization.

## CDF-Managed Task File

```yaml
---
task_contract: cdf-cdtask/v1
status: tasking_ready
source: cdf
approval_state: plan-approved
execution_owner: cdf
risk_level: <Level S | Level M | Level L | Level XL>
workspace: <absolute path>
source_branch: <branch or Unavailable>
source_commit: <commit or Unavailable>
created_at: <ISO-8601 timestamp>
---
```

Required sections:

1. CDF Continuation Contract and Approval Record;
2. planning evidence and approved design;
3. canonical Scope Lock, verbatim;
4. dependency graph/data and stable-ID tasks;
5. risks, acceptance criteria, verification, and rollback;
6. Scope Guard, Execution Contract, Task Readiness Gate, and Save Verification.

Managed persistence occurs only when requested by CDF or the user.
