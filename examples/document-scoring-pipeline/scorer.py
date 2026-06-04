"""
Final scoring helpers for the document scoring pipeline example.

The last stage stays intentionally readable:
- score the shortlist against explicit criteria
- attach evidence
- keep the final result easy to explain
"""

from __future__ import annotations


def score_resume(job: dict, candidate_row: dict) -> dict:
    """Return one final scoring record for a shortlisted resume."""

    resume = candidate_row["resume"]
    resume_skills = {skill.lower() for skill in resume["skills"]}
    resume_certs = {cert.lower() for cert in resume["certifications"]}

    required_skill_hits = [
        skill for skill in job["required_skills"] if skill.lower() in resume_skills
    ]
    preferred_skill_hits = [
        skill for skill in job["preferred_skills"] if skill.lower() in resume_skills
    ]
    required_cert_hits = [
        cert for cert in job["required_certifications"] if cert.lower() in resume_certs
    ]

    score = 0
    score += len(required_skill_hits) * 20
    score += len(preferred_skill_hits) * 8
    score += len(required_cert_hits) * 10
    score += min(resume["years_experience"], 10) * 2
    score += round(candidate_row["semantic_score"] * 15)

    evidence = []
    if required_skill_hits:
        evidence.append(f"Required skills matched: {', '.join(required_skill_hits)}")
    if preferred_skill_hits:
        evidence.append(f"Preferred skills matched: {', '.join(preferred_skill_hits)}")
    if required_cert_hits:
        evidence.append(f"Required certifications matched: {', '.join(required_cert_hits)}")
    evidence.append(f"Years of experience: {resume['years_experience']}")
    evidence.append(f"Semantic score: {candidate_row['semantic_score']:.3f}")

    return {
        "resume": resume,
        "final_score": score,
        "keyword_score": candidate_row["keyword_score"],
        "semantic_score": candidate_row["semantic_score"],
        "rerank_score": candidate_row["rerank_score"],
        "evidence": evidence,
    }


def score_shortlist(job: dict, reranked_rows: list[dict], top_k: int = 3) -> list[dict]:
    """Score the reranked shortlist and return the best final candidates."""

    scored_rows = [score_resume(job, row) for row in reranked_rows]
    scored_rows.sort(key=lambda row: row["final_score"], reverse=True)
    return scored_rows[:top_k]
