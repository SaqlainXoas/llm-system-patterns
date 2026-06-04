def chunked(rows, size):
    """Yield small batches in the same order they arrived."""
    batch = []

    for row in rows:
        batch.append(row)
        if len(batch) == size:
            yield batch
            batch = []

    if batch:
        yield batch


def build_worker_payload(brief_id, upload_id):
    """Simple payload shape for a Celery or queue worker."""
    return {
        "brief_id": brief_id,
        "upload_id": upload_id,
        "status": "queued",
    }


def keep_rolling_pool(rows, top_k):
    """Trim the working pool so later stages stay bounded."""
    rows.sort(key=lambda row: row["score"], reverse=True)
    return rows[:top_k]
