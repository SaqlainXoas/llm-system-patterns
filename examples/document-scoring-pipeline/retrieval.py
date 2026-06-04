"""
Retrieval and reranking helpers for the document scoring pipeline example.

This file keeps the semantic stage runnable without API keys by using a tiny
local embedding stand-in. The structure mirrors a real pipeline even though the
math is intentionally simple.
"""

from __future__ import annotations

import math
import re
from collections import Counter


TOKEN_RE = re.compile(r"[a-z0-9\+\#\.]+")


def tokenize(text: str) -> list[str]:
    """Return lowercase tokens for simple local similarity scoring."""

    return TOKEN_RE.findall(text.lower())


class SimpleEmbeddingModel:
    """
    Small local stand-in for a real embedding model.

    In a production system, this class is the place you would swap in Gemini
    embeddings or another hosted provider. For this repo, the local version
    keeps the example runnable and easy to inspect.
    """

    def embed(self, text: str) -> Counter[str]:
        """Convert text into a token-count vector."""

        return Counter(tokenize(text))


def cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    """Compute cosine similarity between two token-count vectors."""

    shared_tokens = set(left) & set(right)
    dot_product = sum(left[token] * right[token] for token in shared_tokens)

    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))

    if left_norm == 0 or right_norm == 0:
        return 0.0

    return dot_product / (left_norm * right_norm)


def build_query_text(job: dict) -> str:
    """Build one text block that represents the job requirements."""

    return " ".join(
        [
            job["title"],
            " ".join(job["required_skills"]),
            " ".join(job["preferred_skills"]),
            " ".join(job["required_certifications"]),
            job["summary"],
        ]
    ).strip()


def keyword_score(job: dict, resume: dict) -> int:
    """Score exact lexical matches for skills and certifications."""

    resume_skills = {skill.lower() for skill in resume["skills"]}
    resume_certs = {cert.lower() for cert in resume["certifications"]}

    score = 0

    for skill in job["required_skills"]:
        if skill.lower() in resume_skills:
            score += 3

    for skill in job["preferred_skills"]:
        if skill.lower() in resume_skills:
            score += 1

    for cert in job["required_certifications"]:
        if cert.lower() in resume_certs:
            score += 2

    return score


def semantic_score(job: dict, resume: dict, embedder: SimpleEmbeddingModel) -> float:
    """Return a local semantic similarity score."""

    query_vector = embedder.embed(build_query_text(job))
    resume_vector = embedder.embed(resume["text"])
    return cosine_similarity(query_vector, resume_vector)


def retrieve_hybrid_candidates(
    resumes: list[dict],
    job: dict,
    embedder: SimpleEmbeddingModel,
    keyword_top_k: int = 5,
    semantic_top_k: int = 5,
) -> list[dict]:
    """
    Build one merged candidate set from keyword retrieval and semantic retrieval.

    Each returned row keeps both scores so later stages remain easy to inspect.
    """

    rows: list[dict] = []
    for resume in resumes:
        rows.append(
            {
                "resume": resume,
                "keyword_score": keyword_score(job, resume),
                "semantic_score": semantic_score(job, resume, embedder),
            }
        )

    keyword_rows = sorted(rows, key=lambda row: row["keyword_score"], reverse=True)[:keyword_top_k]
    semantic_rows = sorted(rows, key=lambda row: row["semantic_score"], reverse=True)[:semantic_top_k]

    merged_by_resume_id: dict[str, dict] = {}
    for row in keyword_rows + semantic_rows:
        merged_by_resume_id[row["resume"]["resume_id"]] = row

    return list(merged_by_resume_id.values())


def rerank_candidates(candidate_rows: list[dict], job: dict) -> list[dict]:
    """
    Apply a simple rerank score on the merged candidate set.

    This is a lightweight stand-in for a real reranker or cross-encoder.
    """

    reranked_rows: list[dict] = []

    for row in candidate_rows:
        resume = row["resume"]
        required_skill_hits = sum(
            1
            for skill in job["required_skills"]
            if skill.lower() in {value.lower() for value in resume["skills"]}
        )
        experience_bonus = min(resume["years_experience"] / 10.0, 1.0)

        rerank_score = (
            row["semantic_score"] * 0.60
            + row["keyword_score"] * 0.25
            + required_skill_hits * 0.10
            + experience_bonus * 0.05
        )

        reranked_row = dict(row)
        reranked_row["rerank_score"] = rerank_score
        reranked_rows.append(reranked_row)

    reranked_rows.sort(key=lambda row: row["rerank_score"], reverse=True)
    return reranked_rows
