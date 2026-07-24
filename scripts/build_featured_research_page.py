#!/usr/bin/env python3
"""Build Featured Research from rows checked `featured` in the control sheet."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "content" / "outputs" / "publications-control.json"
OUTPUT = ROOT / "featured-research.qmd"
PUBLICATIONS_FEATURED = ROOT / "content" / "outputs" / "publications" / "featured.md"


def truthy(value: object) -> bool:
    return value is True or str(value).strip().casefold() in {"true", "yes", "1"}


def load_featured() -> list[dict]:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    values = payload["values"]
    headers = values[0]
    papers = []
    for values_row in values[1:]:
        padded = values_row + [""] * (len(headers) - len(values_row))
        row = dict(zip(headers, padded))
        if row.get("doi") and truthy(row.get("featured")):
            papers.append(row)
    return papers


def card(paper: dict) -> str:
    doi = str(paper["doi"])
    url = f"https://doi.org/{html.escape(doi)}"
    return (
        '<article class="highlight-paper">'
        f'<p class="highlight-journal">{html.escape(str(paper.get("journal") or "Journal unavailable"))}</p>'
        f'<span class="highlight-year">{html.escape(str(paper.get("year") or ""))}</span>'
        f'<h3><a href="{url}" target="_blank" rel="noopener">'
        f'{html.escape(str(paper.get("title") or "Untitled publication"))}</a></h3>'
        f'<p class="highlight-doi">{html.escape(doi)}</p>'
        '</article>'
    )


def main() -> None:
    papers = load_featured()
    cards = "".join(card(paper) for paper in papers)
    OUTPUT.write_text(
        f'''---
title: "Featured Research"
description: "Selected research from the Cancer Data Science Laboratory"
page-layout: full
title-block-banner: false
---

<!-- Generated from rows checked `featured` in content/outputs/publications-control.json. -->
::: {{.featured-research-page .highlights-doi-page}}
<header class="featured-intro">
<p class="eyebrow">Signature works</p>
<h1>Computational ideas behind major cancer discoveries.</h1>
<p>A selection of studies chosen by the laboratory. Their order follows the publication control sheet.</p>
</header>

<section class="highlight-category highlight-category-2 highlight-category-single">
<div class="highlight-grid">{cards}</div>
</section>

<section class="featured-all">
<p class="eyebrow">Complete record</p>
<h2>Explore every publication.</h2>
<a class="button button-dark" href="publications.html">View all publications</a>
</section>
:::
''',
        encoding="utf-8",
    )
    PUBLICATIONS_FEATURED.write_text(
        f'''<!-- Generated from rows checked `featured` in the publication control sheet. -->
<section class="publications-featured">
<div class="publications-featured-heading">
<div>
<p class="eyebrow">Featured</p>
<h2>Signature works.</h2>
</div>
<p>Research selected by the laboratory.</p>
</div>
<div class="highlight-grid">{cards}</div>
</section>
''',
        encoding="utf-8",
    )
    print(f"Featured research: {len(papers)} papers in spreadsheet order")


if __name__ == "__main__":
    main()
