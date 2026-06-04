# Decision Guide: When to Use a Reranker

This guide will help readers decide whether a reranker meaningfully improves precision or only adds cost and latency.

## Quick Direction

- Use a reranker when retrieval recall is decent but result ordering is weak
- Skip it when candidate sets are already small and high quality
