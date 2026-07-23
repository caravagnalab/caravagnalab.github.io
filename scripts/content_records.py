"""Small helpers shared by Markdown-backed content builders."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path


def read_record(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^\+\+\+\n(.*?)\n\+\+\+\n?(.*)$", text, re.S)
    if not match:
        raise ValueError(f"{path}: expected TOML front matter delimited by +++")
    record = tomllib.loads(match.group(1))
    record["body"] = match.group(2).strip()
    record["source"] = path.name
    return record


def records_in(directory: Path) -> list[dict]:
    return sorted(
        (read_record(path) for path in directory.glob("*.md")),
        key=lambda item: (item.get("order", 999), item.get("title", item["source"])),
    )
