"""Simple in-memory cache helpers for the scaled document scoring example."""

from __future__ import annotations

import hashlib
from collections import Counter


class TextEmbeddingCache:
    """Cache embeddings by text hash so repeated work stays cheap."""

    def __init__(self) -> None:
        self._store: dict[str, Counter[str]] = {}
        self.hits = 0
        self.misses = 0

    def get_or_create(self, text: str, build_embedding) -> Counter[str]:
        """Return a cached embedding or compute it once."""

        cache_key = hashlib.sha256(text.encode("utf-8")).hexdigest()

        if cache_key in self._store:
            self.hits += 1
            return self._store[cache_key]

        self.misses += 1
        embedding = build_embedding(text)
        self._store[cache_key] = embedding
        return embedding

    def stats(self) -> dict[str, int]:
        """Return simple cache hit and miss counts."""

        return {
            "cached_items": len(self._store),
            "hits": self.hits,
            "misses": self.misses,
        }
