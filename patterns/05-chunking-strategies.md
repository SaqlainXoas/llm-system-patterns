# Pattern 05: Chunking Strategies

![Badge](https://img.shields.io/badge/Pattern-Chunking-2563eb) ![Badge](https://img.shields.io/badge/Goal-Better%20Context%20Shape-0f172a) ![Badge](https://img.shields.io/badge/Default-Structure%20Aware-16a34a)

## Quick take
Chunking is not just preprocessing. It changes recall, precision, context quality, cost, and what the downstream model is even able to judge correctly.

```mermaid
flowchart LR
  A[Raw document] --> B[Chunking strategy]
  B --> C[Retrieval quality]
  C --> D[RAG or judge quality]
```

## Why this matters
Fixed-size chunks are easy, but they can split meaning at the wrong boundary. Structure-aware chunks are often better for long documents, policy sections, reports, or pages where headings and sections carry real signal. Overlap helps recall, but too much overlap increases noise, duplicate evidence, and cost.

The right chunking strategy depends on the job. Retrieval may benefit from smaller recall-friendly chunks, while final judgment often benefits from larger, more coherent evidence windows. That is why chunking should be treated as a system design choice, not just a loader setting.

## Common methods

| Method | Good when | Watch out for |
|---|---|---|
| `Fixed-size` | you need a fast baseline | can split meaning in the wrong place |
| `Structure-aware` | headings, sections, bullets, and pages carry signal | needs cleaner parsing first |
| `Two-pass` | retrieval needs focus but final judgment needs more context | adds one more stitching step |

`Fixed-size` chunking is the easiest start. `Structure-aware` chunking is usually the better long-document default. `Two-pass` chunking is often the production-minded move when retrieval and final reasoning need different context shapes.

## Rough implementation ideas
If you are using a framework, a text splitter such as LangChain's recursive character splitter is a reasonable baseline. If you are not using a framework, the core logic is still simple:

```python
def chunk_text(text, chunk_size=800, overlap=120):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks
```

For structured documents, a better first version is often:

```python
def chunk_by_sections(section_blocks, max_chars=1200):
    chunks = []
    current = []
    current_len = 0

    for block in section_blocks:
        if current_len + len(block) > max_chars and current:
            chunks.append("\n".join(current))
            current = [block]
            current_len = len(block)
        else:
            current.append(block)
            current_len += len(block)

    if current:
        chunks.append("\n".join(current))

    return chunks
```

## Practical defaults
| Stage | Better chunk shape |
|---|---|
| `Retrieval` | smaller, topic-focused chunks |
| `Final judgment` | larger, stitched evidence windows |
| `Citation or explanation` | enough surrounding text to keep meaning intact |

For retrieval, start with smaller chunks that preserve topical focus. For final judgment or citation, combine neighboring chunks so the model sees enough surrounding context to reason safely.

A practical first pass is:

```text
retrieve on chunks around 600-1000 chars
-> keep overlap modest
-> merge neighboring hits before final LLM use
```

That keeps retrieval sharp without starving the final stage of context.

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-04%20Reranker-64748b)](04-reranker-when-and-why.md)
[![Next](https://img.shields.io/badge/Next-06%20Prompt%20Injection-2563eb)](06-prompt-injection-defense.md)
