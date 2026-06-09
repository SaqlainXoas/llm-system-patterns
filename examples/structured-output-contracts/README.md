# Structured Output Contracts

![Badge](https://img.shields.io/badge/Example-Structured%20Output-2563eb) ![Badge](https://img.shields.io/badge/Style-Reference%20Script-0f172a) ![Badge](https://img.shields.io/badge/Goal-Validate%20Before%20Use-16a34a) ![Badge](https://img.shields.io/badge/Progress-7%2F7-0f172a)

## Goal
Learn the smallest useful contract flow for structured model output:
1. define the application schema
2. ask the model for structured output
3. validate the response with `Pydantic`
4. convert the typed result into normal application data

## Flow
```mermaid
flowchart LR
  A[Prompt] --> B[Provider structured output]
  B --> C[Validate with Pydantic]
  C --> D[Typed object]
  D --> E[JSON payload]
```

## What this example is
- One small reference script, not a full application shell.
- A schema-first data flow that matches Pattern 14.
- A practical example of the application boundary staying stronger than the model response.

## What this example is not
- Not a framework demo.
- Not a full provider comparison.
- Not a guarantee that every reader can run it unchanged.

## How to run

```bash
pip install google-genai pydantic
export GEMINI_API_KEY=your_key_here
python3 structured_output_ticket.py
```

Adjust the model name or SDK version if the provider docs change.

## Why this shape matters
The same contract pattern works with OpenAI and other providers that support structured output.

What changes is the API call shape. What should stay stable is:
- the schema
- the validation boundary
- the payload your application actually uses

## File walkthrough order
1. `structured_output_ticket.py`

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../../README.md)
[![Cookbook](https://img.shields.io/badge/Cookbook-Examples-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-RAG%20Without%20Frameworks-64748b)](../rag-without-frameworks/README.md)
[![Pattern](https://img.shields.io/badge/Pattern-14%20Structured%20Output%20Contracts-2563eb)](../../patterns/14-structured-output-contracts.md)
