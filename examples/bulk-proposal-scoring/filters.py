import hashlib
import json


def load_brief(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def load_proposals(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def drop_duplicate_proposals(proposals):
    """Keep the first copy of each proposal text."""
    seen_hashes = set()
    unique_rows = []

    for proposal in proposals:
        text_hash = hashlib.sha256(proposal["text"].encode("utf-8")).hexdigest()
        if text_hash in seen_hashes:
            continue

        seen_hashes.add(text_hash)
        unique_rows.append(proposal)

    return unique_rows


def pre_filter_batch(brief, proposals):
    """Keep only proposals that satisfy the required hard signals."""
    kept_rows = []

    for proposal in proposals:
        if proposal["region"] != brief["region"]:
            continue

        proposal_text = proposal["text"].lower()
        failed_term = False

        for term in brief["required_terms"]:
            if term.lower() not in proposal_text:
                failed_term = True
                break

        if failed_term:
            continue

        kept_rows.append(proposal)

    return kept_rows
