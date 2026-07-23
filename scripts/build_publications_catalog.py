#!/usr/bin/env python3
"""Build a publication catalogue from Giulio Caravagna's public Scholar profile."""

from datetime import date
from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import SequenceMatcher
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from html import unescape
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "scholar-publications.json"
SOURCES_FILE = ROOT / "content" / "outputs" / "publications" / "sources.md"


def publication_profile() -> str:
    for raw in SOURCES_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#") and line.startswith("http"):
            return line
    raise ValueError(f"No publication profile URL found in {SOURCES_FILE}")


PROFILE = publication_profile()
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CaravagnaLab-Publications/1.0)",
    "Accept-Language": "en-GB,en;q=0.9",
}
METADATA_VERSION = 3


class ScholarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []
        self.item = None
        self.capture = None
        self.buffer = []
        self.gray = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        classes = set(values.get("class", "").split())
        if tag == "tr" and "gsc_a_tr" in classes:
            self.item = {"title": "", "authors": "", "venue": "", "year": 0, "citations": 0, "url": ""}
            self.gray = []
        if not self.item:
            return
        if tag == "a" and "gsc_a_at" in classes:
            self.capture, self.buffer = "title", []
            self.item["url"] = urljoin("https://scholar.google.com", values.get("href", ""))
        elif tag == "div" and "gs_gray" in classes:
            self.capture, self.buffer = "gray", []
        elif tag == "a" and "gsc_a_ac" in classes:
            self.capture, self.buffer = "citations", []
        elif tag == "span" and "gsc_a_hc" in classes:
            self.capture, self.buffer = "year", []

    def handle_data(self, data):
        if self.capture:
            self.buffer.append(data)

    def handle_endtag(self, tag):
        if not self.item:
            return
        if (tag == "a" and self.capture in {"title", "citations"}) or (tag == "div" and self.capture == "gray") or (tag == "span" and self.capture == "year"):
            value = " ".join("".join(self.buffer).split())
            if self.capture == "gray":
                self.gray.append(value)
            elif self.capture in {"year", "citations"}:
                self.item[self.capture] = int(value) if value.isdigit() else 0
            else:
                self.item[self.capture] = value
            self.capture, self.buffer = None, []
        if tag == "tr":
            if self.item.get("title"):
                self.item["authors"] = self.gray[0] if self.gray else "Authors not available"
                self.item["venue"] = self.gray[1] if len(self.gray) > 1 else "Venue not available"
                self.items.append(self.item)
            self.item = None


def fetch(offset=0):
    request = Request(f"{PROFILE}&cstart={offset}", headers=HEADERS)
    with urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", errors="replace")


def fetch_url(url, *, json_response=False):
    request = Request(url, headers=HEADERS)
    with urlopen(request, timeout=20) as response:
        text = response.read().decode("utf-8", errors="replace")
    return json.loads(text) if json_response else text


def normalized(value):
    value = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def scholar_authors(url):
    try:
        html = fetch_url(url)
        match = re.search(
            r'<div class="gsc_oci_field">Authors</div><div class="gsc_oci_value">(.*?)</div>',
            html,
            flags=re.DOTALL,
        )
        if match:
            return " ".join(unescape(re.sub(r"<[^>]+>", " ", match.group(1))).split())
    except (HTTPError, URLError, TimeoutError):
        pass
    return ""


def enrich(publication):
    crossref_checked = False
    try:
        endpoint = (
            "https://api.crossref.org/works?"
            f"query.title={quote(publication['title'])}&rows=5"
            "&select=DOI,title,author,published,container-title,type"
        )
        results = fetch_url(endpoint, json_response=True).get("message", {}).get("items", [])
        crossref_checked = True
        target = normalized(publication["title"])
        candidates = []
        for work in results:
            title = (work.get("title") or [""])[0]
            score = SequenceMatcher(None, target, normalized(title)).ratio()
            years = (work.get("published") or {}).get("date-parts", [[0]])
            work_year = years[0][0] if years and years[0] else 0
            if score >= 0.9 and (not publication["year"] or not work_year or abs(publication["year"] - work_year) <= 1):
                candidates.append((score, work))
        if candidates:
            work = max(candidates, key=lambda item: item[0])[1]
            authors = [
                " ".join(filter(None, [entry.get("given", ""), entry.get("family", "")]))
                for entry in work.get("author", [])
            ]
            return {
                **publication,
                "authors": ", ".join(filter(None, authors)) or publication["authors"],
                "authorsDetailed": bool(authors) or publication.get("authorsDetailed", False),
                "doi": work.get("DOI", ""),
                "metadataSource": "Crossref",
                "metadataVersion": METADATA_VERSION,
                "doiChecked": True,
            }
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError):
        pass
    authors = scholar_authors(publication["url"])
    return {
        **publication,
        "authors": authors or publication["authors"],
        "authorsDetailed": bool(authors) or publication.get("authorsDetailed", False),
        "doi": "",
        "metadataSource": "Google Scholar",
        "metadataVersion": METADATA_VERSION,
        "doiChecked": crossref_checked,
    }


def main():
    previous = {}
    if OUTPUT.exists():
        try:
            previous = json.loads(OUTPUT.read_text())
        except json.JSONDecodeError:
            pass
    try:
        publications = []
        try:
            for offset in range(0, 1000, 100):
                parser = ScholarParser()
                parser.feed(fetch(offset))
                publications.extend(parser.items)
                if len(parser.items) < 100:
                    break
        except (HTTPError, URLError, TimeoutError):
            publications = previous.get("publications", [])
        if not publications:
            raise ValueError("Scholar returned no publication rows")
        publications = [publication for publication in publications if publication.get("year", 0) > 0]
        for publication in publications:
            if publication.get("authors") and "..." not in publication["authors"]:
                publication["authorsDetailed"] = True
        cached = {
            normalized(item.get("title")): item
            for item in previous.get("publications", [])
            if item.get("metadataVersion") == METADATA_VERSION and item.get("authorsDetailed") and item.get("doiChecked")
        }
        pending = []
        enriched = []
        for publication in publications:
            old = cached.get(normalized(publication["title"]))
            if old:
                enriched.append({
                    **publication,
                    "authors": old.get("authors") or publication["authors"],
                    "authorsDetailed": old.get("authorsDetailed", False),
                    "doi": old.get("doi", ""),
                    "metadataSource": old.get("metadataSource", ""),
                    "metadataVersion": old.get("metadataVersion", METADATA_VERSION),
                    "doiChecked": old.get("doiChecked", False),
                })
            else:
                pending.append(publication)
        if pending:
            # Keep concurrency deliberately low: both bibliographic services
            # throttle bursts, while the cache makes this cost incremental.
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = {executor.submit(enrich, publication): publication for publication in pending}
                for future in as_completed(futures):
                    enriched.append(future.result())
        order = {normalized(item["title"]): index for index, item in enumerate(publications)}
        enriched.sort(key=lambda item: order[normalized(item["title"])])
        payload = {
            "generated": date.today().isoformat(),
            "profile": PROFILE,
            "publications": enriched,
        }
        OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
        detailed = sum(item.get("authorsDetailed", False) for item in enriched)
        dois = sum(bool(item.get("doi")) for item in enriched)
        print(f"Scholar catalogue: {len(enriched)} publications · {detailed} full author lists · {dois} DOIs")
    except (HTTPError, URLError, TimeoutError, ValueError) as error:
        if previous.get("publications"):
            print(f"Scholar unavailable; retaining {len(previous['publications'])} cached publications: {error}")
        else:
            raise


if __name__ == "__main__":
    main()
