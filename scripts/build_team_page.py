#!/usr/bin/env python3
"""Build people.qmd from one Markdown record per active lab member."""

from __future__ import annotations

import html
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PEOPLE_DIR = ROOT / "content" / "team" / "profiles"
OUTPUT = ROOT / "people.qmd"

def read_record(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^\+\+\+\n(.*?)\n\+\+\+\n?(.*)$", text, re.S)
    if not match:
        raise ValueError(f"{path}: expected TOML front matter delimited by +++")
    data = tomllib.loads(match.group(1))
    data["background"] = match.group(2).strip()
    data["source"] = path.name
    return data


def inline_md(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    return escaped


def markdown_fragment(text: str) -> str:
    if not text:
        return ""
    chunks: list[str] = []
    list_open = False
    for raw in text.splitlines():
        line = raw.strip()
        if line in {
            "**Training**",
            "**Current positions**",
            "**Background**",
        }:
            continue
        if line.startswith("- "):
            if not list_open:
                chunks.append("<ul>")
                list_open = True
            chunks.append(f"<li>{inline_md(line[2:])}</li>")
        else:
            if list_open:
                chunks.append("</ul>")
                list_open = False
            if line:
                chunks.append(f"<p>{inline_md(line)}</p>")
    if list_open:
        chunks.append("</ul>")
    return "".join(chunks)


def card(person: dict) -> str:
    featured = " team-card-pi" if person.get("featured") else ""
    text_only = " team-card-text" if not person.get("photo") else ""
    links = []
    if person.get("email"):
        links.append(
            f'<a href="mailto:{html.escape(person["email"])}">'
            '<i class="bi bi-envelope"></i> Email</a>'
        )
    if person.get("meeting"):
        links.append(
            f'<a href="{html.escape(person["meeting"])}" target="_blank" rel="noopener">'
            '<i class="bi bi-calendar3"></i> Meet Giulio</a>'
        )
    if person.get("thesis_title") and person.get("thesis_url"):
        thesis_title = html.escape(person["thesis_title"])
        links.append(
            f'<a class="team-thesis" href="{html.escape(person["thesis_url"])}" '
            f'target="_blank" rel="noopener" title="{thesis_title}" '
            f'aria-label="PhD thesis: {thesis_title}">'
            '<i class="bi bi-mortarboard"></i> PhD thesis</a>'
        )
    links_html = f'<div class="team-links">{"".join(links)}</div>' if links else ""
    details = []
    interests = person.get("research_interests", [])
    if interests and person["category"] not in {"visiting", "alumni"}:
        interests_html = "<ul>" + "".join(
            f"<li>{inline_md(interest)}</li>" for interest in interests
        ) + "</ul>"
        details.append(
            '<details class="team-background"><summary>Research interests</summary>'
            f'<div class="team-background-content">{interests_html}</div></details>'
        )
    for field, label in (("positions", "Positions"), ("training", "Training")):
        entries = person.get(field, [])
        if entries:
            entries_html = "<ul>" + "".join(
                f"<li>{inline_md(entry)}</li>" for entry in entries
            ) + "</ul>"
            details.append(
                f'<details class="team-background"><summary>{label}</summary>'
                f'<div class="team-background-content">{entries_html}</div></details>'
            )
    if person["background"] and person["category"] not in {"visiting", "alumni"}:
        details.append(
            '<details class="team-background"><summary>Background</summary>'
            f'<div class="team-background-content">{markdown_fragment(person["background"])}</div>'
            "</details>"
        )
    photo = (
        f'<img src="{html.escape(person["photo"])}" alt="{html.escape(person["name"])}">'
        if person.get("photo")
        else f'<div class="team-photo-placeholder" aria-hidden="true">'
        f'{"".join(part[0] for part in person["name"].split()[:2])}</div>'
    )
    summary = (
        f'<p>{html.escape(person["summary"])}</p>'
        if person["category"] in {"visiting", "alumni"}
        else ""
    )
    role = (
        f'<span>{html.escape(person["role"])}</span>'
        if person.get("role")
        else ""
    )
    return (
        f'<article class="team-card{featured}{text_only}" data-profile="{html.escape(person["source"])}">'
        f"{photo}"
        "<div>"
        f"{role}"
        f'<h3>{html.escape(person["display_name"])}</h3>'
        f"{summary}"
        f'{links_html}{"".join(details)}'
        "</div></article>"
    )


def main() -> None:
    page = read_record(ROOT / "content" / "team" / "page.md")
    records = sorted(
        (read_record(path) for path in PEOPLE_DIR.glob("*.md")),
        key=lambda item: (item["order"], item["name"]),
    )
    page_header = page["background"].replace("[[hero_image]]", page["hero_image"])
    parts = [
        f"""---
title: "{page["page_title"]}"
description: "{page["page_description"]}"
page-layout: full
title-block-banner: false
---

<!-- Generated by scripts/build_team_page.py. Edit content/team/. -->
::: {{.team-page}}
{page_header}
"""
    ]
    for section in page["sections"]:
        key = section["category"]
        eyebrow = section["eyebrow"]
        title = section["title"]
        tinted = section.get("tinted", False)
        members = [person for person in records if person["category"] == key]
        if not members:
            continue
        section_class = "team-section team-section-tinted" if tinted else "team-section"
        if key == "leadership":
            grid_class = "team-grid team-grid-featured"
        elif key in {"visiting", "alumni"}:
            grid_class = "team-grid team-grid-compact"
        else:
            grid_class = "team-grid"
        parts.append(
            f'<section class="{section_class}">'
            f'<div class="team-section-title"><p class="eyebrow">{eyebrow}</p>'
            f"<h2>{title}</h2></div>"
            f'<div class="{grid_class}">'
            + "\n".join(card(person) for person in members)
            + "</div></section>"
        )
    parts.append(":::")
    OUTPUT.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    missing = [person["name"] for person in records if not person.get("email")]
    print(
        f"Team page: {len(records)} profiles · "
        f"{len(records) - len(missing)} emails · {len(missing)} email placeholders"
    )


if __name__ == "__main__":
    main()
