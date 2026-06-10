# Code-first Principles

## Core Rule

Analyze code before building reports. Reports should answer questions created by real app paths, not guessed page names.

## Principles

- Page names are not business truth.
- SDK pages are not product pages.
- A result container is not necessarily success.
- Permission pages are not always part of the main flow.
- Multi-feature apps must be split into separate funnels.
- Purchase pages must be analyzed by source path and next path.
- Ad pages must be analyzed by trigger point, display, close, reward, and return path.
- Uncertainty must be marked.

## Required Evidence

Important claims should cite file path, class/module, function/method when available, line number when available, code summary, and confidence level.

## Forbidden Shortcuts

- Do not create a funnel from screen names alone.
- Do not merge unrelated branches for cleaner charts.
- Do not infer completion from a page view unless code confirms completion.
- Do not expose secrets, tokens, certificates, ad unit IDs, bundle identifiers, or private keys.
