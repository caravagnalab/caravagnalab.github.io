#!/usr/bin/env python3
"""Build the project-paper pool JSON from Markdown records."""

from __future__ import annotations

import json
from pathlib import Path

from content_records import records_in

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    papers = []
    for record in records_in(ROOT / "content" / "papers"):
        papers.append(
            {
                key: record[key]
                for key in ("id", "title", "journal", "year", "url", "projects", "weight", "status")
                if key in record
            }
        )
    output = ROOT / "assets" / "papers.json"
    output.write_text(json.dumps(papers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Example-paper pool: {len(papers)} Markdown records")


if __name__ == "__main__":
    main()
