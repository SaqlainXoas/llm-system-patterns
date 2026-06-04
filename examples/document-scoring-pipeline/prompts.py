"""
Prompt helpers for the document scoring pipeline example.

The runnable code uses deterministic scoring so the example works without API
keys. These helpers still show what a grounded LLM validation prompt can look
like once you plug in a hosted model.
"""

from __future__ import annotations


def build_judge_context(job: dict, scored_row: dict) -> dict:
    """Build a small context object for a final LLM validation step."""

    resume = scored_row["resume"]

    return {
        "job_title": job["title"],
        "job_summary": job["summary"],
        "required_skills": job["required_skills"],
        "preferred_skills": job["preferred_skills"],
        "candidate_name": resume["name"],
        "candidate_skills": resume["skills"],
        "candidate_certifications": resume["certifications"],
        "candidate_summary": resume["summary"],
        "pipeline_scores": {
            "keyword": scored_row["keyword_score"],
            "semantic": round(scored_row["semantic_score"], 3),
            "rerank": round(scored_row["rerank_score"], 3),
            "final": scored_row["final_score"],
        },
    }


def build_judge_prompt(job: dict, scored_row: dict) -> str:
    """Return a grounded prompt template for a real LLM validation call."""

    context = build_judge_context(job, scored_row)

    return f"""
Role:
You are validating whether a shortlisted candidate matches the job.

Task:
Use only the provided evidence. Confirm the strengths, gaps, and final fit.

Job title:
{context["job_title"]}

Required skills:
{", ".join(context["required_skills"])}

Preferred skills:
{", ".join(context["preferred_skills"])}

Candidate:
{context["candidate_name"]}

Candidate skills:
{", ".join(context["candidate_skills"])}

Candidate certifications:
{", ".join(context["candidate_certifications"])}

Candidate summary:
{context["candidate_summary"]}

Pipeline scores:
{context["pipeline_scores"]}

Output:
- final fit summary
- strengths
- gaps
- confidence note
""".strip()
