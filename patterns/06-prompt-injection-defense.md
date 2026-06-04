# Pattern 06: Prompt Injection Defense

![Badge](https://img.shields.io/badge/Pattern-Safety-2563eb) ![Badge](https://img.shields.io/badge/Risk-Prompt%20Injection-0f172a)

## Quick take
Retrieved content is evidence, not authority. If external text can shape your downstream prompt, the pipeline needs explicit trust boundaries.

```mermaid
flowchart LR
  A[External content] --> B[Sanitize and label as evidence]
  B --> C[Policy checks]
  C --> D[Grounded prompt]
```

## Why this matters
Prompt injection problems usually grow when systems blur instruction text and evidence text together. A retrieved document can contain commands, roleplay attempts, or manipulative content that should never become part of the system instruction layer.

The fix is architectural before it is prompt-level: separate instructions from evidence, keep deterministic checks and policy filters ahead of the model, and require grounded outputs that operate only on the provided evidence.

## Where this goes next
This page will grow into trust-boundary patterns, evidence-only prompt design, and practical guardrails for retrieval-heavy systems.

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-05%20Chunking-64748b)](05-chunking-strategies.md)
[![Next](https://img.shields.io/badge/Next-07%20Budgeting-2563eb)](07-cost-latency-budgeting.md)
