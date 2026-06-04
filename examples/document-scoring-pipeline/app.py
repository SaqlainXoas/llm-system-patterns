"""
Run the plain-Python document scoring pipeline example.

This script is intentionally small and readable. It shows the full multi-stage
shape without hiding the stages inside a framework.
"""

from __future__ import annotations

from pathlib import Path

from filters import load_job_description, load_resumes, run_pre_filters
from prompts import build_judge_context, build_judge_prompt
from retrieval import SimpleEmbeddingModel, rerank_candidates, retrieve_hybrid_candidates
from scorer import score_shortlist


EXAMPLE_DIR = Path(__file__).resolve().parent
SAMPLE_DATA_DIR = EXAMPLE_DIR / "sample_data"
JOB_FILE = SAMPLE_DATA_DIR / "job_description.txt"
RESUMES_DIR = SAMPLE_DATA_DIR / "resumes"


def print_heading(title: str) -> None:
    """Print a simple stage heading."""

    print(f"\n{title}")
    print("-" * len(title))


def main() -> None:
    """Run every stage of the example and print the results."""

    job = load_job_description(JOB_FILE)
    resumes = load_resumes(RESUMES_DIR)
    embedder = SimpleEmbeddingModel()

    print_heading("1. Loaded data")
    print(f"Job: {job['title']}")
    print(f"Total resumes: {len(resumes)}")

    passed_resumes, rejected_reports = run_pre_filters(resumes, job)

    print_heading("2. Pre-filter results")
    print(f"Passed resumes: {len(passed_resumes)}")
    print(f"Rejected resumes: {len(rejected_reports)}")
    for report in rejected_reports:
        print(f"- {report['resume']['name']}: {', '.join(report['reasons'])}")

    candidate_rows = retrieve_hybrid_candidates(
        resumes=passed_resumes,
        job=job,
        embedder=embedder,
        keyword_top_k=5,
        semantic_top_k=5,
    )

    print_heading("3. Hybrid retrieval shortlist")
    for row in sorted(candidate_rows, key=lambda item: item["semantic_score"], reverse=True):
        resume = row["resume"]
        print(
            f"- {resume['name']}: "
            f"keyword={row['keyword_score']}, "
            f"semantic={row['semantic_score']:.3f}"
        )

    reranked_rows = rerank_candidates(candidate_rows, job)

    print_heading("4. Reranked candidates")
    for row in reranked_rows:
        resume = row["resume"]
        print(
            f"- {resume['name']}: "
            f"rerank={row['rerank_score']:.3f}, "
            f"semantic={row['semantic_score']:.3f}"
        )

    final_rows = score_shortlist(job, reranked_rows, top_k=3)

    print_heading("5. Final scored shortlist")
    for row in final_rows:
        print(f"- {row['resume']['name']}: final_score={row['final_score']}")
        for evidence_line in row["evidence"]:
            print(f"  * {evidence_line}")

    best_row = final_rows[0]
    context = build_judge_context(job, best_row)
    prompt = build_judge_prompt(job, best_row)

    print_heading("6. Final validation context")
    print(context)

    print_heading("7. Example grounded prompt")
    print(prompt)


if __name__ == "__main__":
    main()
