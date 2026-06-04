"""
Loading and pre-filter helpers for the document scoring pipeline example.

The goal of this file is to keep the earliest stage of the pipeline easy to
read:
1. load the job description
2. load resumes
3. apply simple hard filters before semantic scoring
"""

from __future__ import annotations

from pathlib import Path


def split_csv(value: str) -> list[str]:
    """Return a clean list from a comma-separated string."""

    if not value:
        return []

    parts = [part.strip() for part in value.split(",")]
    return [part for part in parts if part]


def parse_labeled_text(path: Path) -> dict:
    """
    Parse a small text file with `Label: value` lines.

    The `Summary:` field may span multiple lines. Everything after `Summary:`
    is treated as summary text.
    """

    fields: dict[str, str] = {}
    summary_lines: list[str] = []
    in_summary = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if in_summary:
            summary_lines.append(line)
            continue

        if line.startswith("Summary:"):
            in_summary = True
            summary_text = line.removeprefix("Summary:").strip()
            if summary_text:
                summary_lines.append(summary_text)
            continue

        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()

    fields["Summary"] = " ".join(summary_lines)
    return fields


def load_job_description(path: Path) -> dict:
    """Load the job description into a small, readable dict."""

    raw = parse_labeled_text(path)

    return {
        "title": raw.get("Title", ""),
        "country": raw.get("Country", ""),
        "minimum_years_experience": int(raw.get("Minimum Years Experience", "0")),
        "required_skills": split_csv(raw.get("Required Skills", "")),
        "preferred_skills": split_csv(raw.get("Preferred Skills", "")),
        "required_certifications": split_csv(raw.get("Required Certifications", "")),
        "summary": raw.get("Summary", ""),
        "text": " ".join(
            [
                raw.get("Title", ""),
                raw.get("Required Skills", ""),
                raw.get("Preferred Skills", ""),
                raw.get("Required Certifications", ""),
                raw.get("Summary", ""),
            ]
        ).strip(),
    }


def load_resumes(folder: Path) -> list[dict]:
    """Load every resume text file from the sample data folder."""

    resumes: list[dict] = []

    for path in sorted(folder.glob("*.txt")):
        raw = parse_labeled_text(path)

        resume = {
            "resume_id": path.stem,
            "name": raw.get("Name", path.stem.replace("-", " ").title()),
            "country": raw.get("Country", ""),
            "years_experience": int(raw.get("Years Experience", "0")),
            "skills": split_csv(raw.get("Skills", "")),
            "certifications": split_csv(raw.get("Certifications", "")),
            "summary": raw.get("Summary", ""),
            "file_path": str(path),
        }

        resume["text"] = " ".join(
            [
                resume["name"],
                " ".join(resume["skills"]),
                " ".join(resume["certifications"]),
                resume["summary"],
            ]
        ).strip()

        resumes.append(resume)

    return resumes


def count_required_skill_hits(resume: dict, job: dict) -> int:
    """Count how many required job skills appear exactly in the resume skills."""

    resume_skills = {skill.lower() for skill in resume["skills"]}
    job_skills = [skill.lower() for skill in job["required_skills"]]

    return sum(1 for skill in job_skills if skill in resume_skills)


def build_pre_filter_report(resume: dict, job: dict) -> dict:
    """Return a small report showing which hard checks passed or failed."""

    skill_hits = count_required_skill_hits(resume, job)
    same_country = resume["country"].lower() == job["country"].lower()
    enough_years = resume["years_experience"] >= job["minimum_years_experience"]
    has_core_skill = skill_hits >= 1

    passed = same_country and enough_years and has_core_skill

    reasons: list[str] = []
    if not same_country:
        reasons.append("country mismatch")
    if not enough_years:
        reasons.append("not enough years of experience")
    if not has_core_skill:
        reasons.append("missing core required skill")

    return {
        "resume": resume,
        "passed": passed,
        "required_skill_hits": skill_hits,
        "reasons": reasons,
    }


def run_pre_filters(resumes: list[dict], job: dict) -> tuple[list[dict], list[dict]]:
    """Split the resumes into passed and rejected groups."""

    passed: list[dict] = []
    rejected_reports: list[dict] = []

    for resume in resumes:
        report = build_pre_filter_report(resume, job)
        if report["passed"]:
            passed.append(resume)
        else:
            rejected_reports.append(report)

    return passed, rejected_reports
