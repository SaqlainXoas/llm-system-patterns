"""
Run the scaled document scoring example.

This version keeps the same scoring idea as the plain example, but changes the
execution style:
- work in batches
- cache embeddings
- keep only a small shortlist in memory
- clean up batch data between passes
"""

from __future__ import annotations

import gc
import sys
from pathlib import Path

from batching import batched
from cache import TextEmbeddingCache


EXAMPLE_DIR = Path(__file__).resolve().parent
PLAIN_EXAMPLE_DIR = EXAMPLE_DIR.parent / "document-scoring-pipeline"
sys.path.insert(0, str(PLAIN_EXAMPLE_DIR))

from filters import load_job_description, load_resumes, run_pre_filters  # noqa: E402
from retrieval import (  # noqa: E402
    SimpleEmbeddingModel,
    build_query_text,
    cosine_similarity,
    keyword_score,
    rerank_candidates,
)
from scorer import score_shortlist  # noqa: E402


JOB_FILE = PLAIN_EXAMPLE_DIR / "sample_data" / "job_description.txt"
RESUMES_DIR = PLAIN_EXAMPLE_DIR / "sample_data" / "resumes"


def print_heading(title: str) -> None:
    """Print a simple stage heading."""

    print(f"\n{title}")
    print("-" * len(title))


def score_batch(batch: list[dict], job: dict, embedder: SimpleEmbeddingModel, cache: TextEmbeddingCache, query_vector) -> list[dict]:
    """Score one batch of resumes and return candidate rows."""

    rows: list[dict] = []

    for resume in batch:
        resume_vector = cache.get_or_create(resume["text"], embedder.embed)
        semantic = cosine_similarity(query_vector, resume_vector)
        rows.append(
            {
                "resume": resume,
                "keyword_score": keyword_score(job, resume),
                "semantic_score": semantic,
            }
        )

    rows.sort(key=lambda row: (row["keyword_score"], row["semantic_score"]), reverse=True)
    return rows


def main() -> None:
    """Run the scaled batch-processing version of the example."""

    job = load_job_description(JOB_FILE)
    resumes = load_resumes(RESUMES_DIR)
    passed_resumes, rejected_reports = run_pre_filters(resumes, job)

    embedder = SimpleEmbeddingModel()
    cache = TextEmbeddingCache()

    query_text = build_query_text(job)

    print_heading("1. Loaded and pre-filtered data")
    print(f"Total resumes: {len(resumes)}")
    print(f"Passed pre-filter: {len(passed_resumes)}")
    print(f"Rejected: {len(rejected_reports)}")

    candidate_buffer: list[dict] = []
    resume_batches = batched(passed_resumes, batch_size=2)

    print_heading("2. Batch scoring")
    for batch_number, batch in enumerate(resume_batches, start=1):
        print(f"Processing batch {batch_number} with {len(batch)} resumes")

        query_vector = cache.get_or_create(query_text, embedder.embed)
        batch_rows = score_batch(batch, job, embedder, cache, query_vector)
        candidate_buffer.extend(batch_rows[:2])
        candidate_buffer.sort(
            key=lambda row: (row["keyword_score"], row["semantic_score"]),
            reverse=True,
        )
        candidate_buffer = candidate_buffer[:5]

        print(f"Shortlist kept after batch {batch_number}: {len(candidate_buffer)}")

        del batch_rows
        gc.collect()

    print_heading("3. Cache statistics")
    print(cache.stats())

    reranked_rows = rerank_candidates(candidate_buffer, job)

    print_heading("4. Reranked shortlist")
    for row in reranked_rows:
        print(
            f"- {row['resume']['name']}: "
            f"keyword={row['keyword_score']}, "
            f"semantic={row['semantic_score']:.3f}, "
            f"rerank={row['rerank_score']:.3f}"
        )

    final_rows = score_shortlist(job, reranked_rows, top_k=3)

    print_heading("5. Final top candidates")
    for row in final_rows:
        print(f"- {row['resume']['name']}: final_score={row['final_score']}")
        for evidence_line in row["evidence"]:
            print(f"  * {evidence_line}")


if __name__ == "__main__":
    main()
