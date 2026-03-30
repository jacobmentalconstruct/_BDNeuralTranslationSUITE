"""content_fts.py — shared Cold Artifact FTS5 lookup helper.

Ownership: core/content_fts.py

Provides a tiny shared read helper over ``content_fts`` so ingest-time
candidate selection and inference-time retrieval can reuse the same SQL
shape without duplicating it.
"""

from __future__ import annotations

import sqlite3
from typing import List, NamedTuple


class ContentFtsHit(NamedTuple):
    occurrence_id: str
    hunk_id: str
    score: float
    origin_id: str
    node_kind: str
    content_snippet: str


def search_content_fts(
    conn: sqlite3.Connection,
    query: str,
    top_k: int = 10,
) -> List[ContentFtsHit]:
    """Return up to ``top_k`` occurrence hits ranked by FTS5 BM25."""
    rows = conn.execute(
        """SELECT o.occurrence_id, o.hunk_id, fts.rank,
                  o.origin_id, c.node_kind, c.content
           FROM content_fts fts
           JOIN content_nodes c ON c.rowid = fts.rowid
           JOIN occurrence_nodes o ON o.hunk_id = c.hunk_id
           WHERE content_fts MATCH ?
           ORDER BY fts.rank
           LIMIT ?""",
        (query, top_k),
    ).fetchall()

    return [
        ContentFtsHit(
            occurrence_id=row[0],
            hunk_id=row[1],
            score=float(row[2]),
            origin_id=row[3],
            node_kind=row[4],
            content_snippet=row[5][:120],
        )
        for row in rows
    ]
