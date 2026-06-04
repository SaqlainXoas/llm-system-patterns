"""Small batching helpers for the scaled document scoring example."""

from __future__ import annotations


def batched(items: list, batch_size: int) -> list[list]:
    """Split one list into smaller batches."""

    batches: list[list] = []

    for start in range(0, len(items), batch_size):
        stop = start + batch_size
        batches.append(items[start:stop])

    return batches
