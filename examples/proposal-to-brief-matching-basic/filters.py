import json


def load_brief(path):
    """Load one project brief from JSON."""
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def load_proposals(path):
    """Load proposal rows from JSON."""
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def pre_filter_proposals(brief, proposals):
    """Keep only proposals that pass the hard checks before embeddings."""
    kept_rows = []

    for proposal in proposals:
        if proposal["region"] != brief["region"]:
            continue

        text = proposal["text"].lower()
        passed_required_terms = True

        for term in brief["required_terms"]:
            if term.lower() not in text:
                passed_required_terms = False
                break

        if not passed_required_terms:
            continue

        kept_rows.append(proposal)

    return kept_rows
