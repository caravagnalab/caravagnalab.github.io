#!/usr/bin/env python3
"""Build the software catalogue from package URLs and their public metadata."""

from html.parser import HTMLParser
from pathlib import Path
from datetime import date
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import json
import re

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "content" / "outputs" / "software" / "packages.md"
OUTPUT = ROOT / "assets" / "software-catalog.json"
BUILD_METADATA = ROOT / "assets" / "software-build.json"
ORG = "caravagnalab"
TOOLS_URL = f"https://raw.githubusercontent.com/{ORG}/{ORG}.github.io/master/tools.json"
HEADERS = {"User-Agent": "CaravagnaLab-Quarto-Catalog", "Accept": "application/json, text/html;q=0.9, */*;q=0.8"}


class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = {}
        self.authors = []
        self.icons = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "meta":
            key = values.get("property") or values.get("name")
            if key and values.get("content"):
                key = key.lower()
                content = values["content"].strip()
                self.meta[key] = content
                if key in {"citation_author", "dc.creator"}:
                    self.authors.append(content)
        elif tag == "link" and "icon" in values.get("rel", "").lower() and values.get("href"):
            self.icons.append(values["href"])


def fetch(url, *, as_json=False, limit=None):
    request = Request(url, headers=HEADERS)
    with urlopen(request, timeout=15) as response:
        data = response.read(limit) if limit else response.read()
    text = data.decode("utf-8", errors="replace")
    return json.loads(text) if as_json else text


def fetch_html(url):
    request = Request(url, headers={**HEADERS, "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8"})
    with urlopen(request, timeout=15) as response:
        return response.read().decode("utf-8", errors="replace")


def repository_name(url):
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.hostname == "github.com" and len(parts) >= 2:
        return parts[1]
    if parsed.hostname and parsed.hostname.endswith("github.io") and parts:
        return parts[0]
    raise ValueError(f"Cannot derive repository from {url}")


def first_image(base, parser):
    og_image = parser.meta.get("og:image", "")
    if og_image and "://" not in og_image and og_image.startswith("caravagnalab.github.io/"):
        og_image = f"https://{og_image}"
    candidates = [
        urljoin(base, og_image) if og_image else "",
        urljoin(base.rstrip("/") + "/", "reference/figures/logo.svg"),
        urljoin(base.rstrip("/") + "/", "reference/figures/logo.png"),
        urljoin(base.rstrip("/") + "/", "logo.svg"),
        urljoin(base.rstrip("/") + "/", "logo.png"),
    ]
    candidates.extend(urljoin(base, icon) for icon in parser.icons)
    for candidate in dict.fromkeys(filter(None, candidates)):
        try:
            fetch(candidate, limit=32)
            return candidate
        except (HTTPError, URLError, TimeoutError):
            continue
    return ""


def clean_description(value):
    value = re.sub(r"<?doi:\s*10\.\d{4,9}/[^>\s]+>?", "", value or "", flags=re.IGNORECASE)
    value = re.sub(r"\s*-\s*caravagnalab/[\w.-]+\s*$", "", value, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", value).strip()


def derived_topics(*values):
    text = " ".join(value or "" for value in values).lower()
    vocabulary = {
        "bayesian-inference": ("bayesian", "variational inference"),
        "cancer-evolution": ("cancer evolution", "tumour evolution", "tumor evolution", "evolutionary"),
        "copy-number-variations": ("copy number", "cna "),
        "differential-expression": ("differential expression",),
        "gene-therapy": ("gene therapy", "insertional mutagenesis"),
        "machine-learning": ("machine learning", "artificial intelligence"),
        "mutational-signatures": ("mutational signature",),
        "phylogenetic-trees": ("phylogen", "clone tree", "mutation tree"),
        "simulation": ("simulation", "agent-based"),
        "single-cell": ("single-cell", "single cell"),
        "subclonal-deconvolution": ("subclonal", "subclone", "clonal deconvolution"),
        "survival-analysis": ("survival", "prognosis"),
        "timing-analysis": ("timing", "pseudo-time", "pseudo-timing"),
    }
    topics = [topic for topic, needles in vocabulary.items() if any(needle in text for needle in needles)]
    return topics or ["research-software"]


def direct_dropbox(value):
    if not value:
        return ""
    return value.replace("https://www.dropbox.com/", "https://dl.dropboxusercontent.com/").replace("dl=0", "dl=1")


def short_author(authors):
    if not authors:
        return ""
    family = authors[0].split(",", 1)[0].strip()
    if " " in family and "," not in authors[0]:
        family = family.split()[-1]
    return f"{family} et al."


def doi_from_url(url):
    parsed = urlparse(url)
    if "doi.org" in (parsed.hostname or ""):
        return parsed.path.lstrip("/")
    match = re.search(r"/articles/(10\.\d{4,9}/[^?#]+|s\d{5}-\d{3}-\d{4,}-\w)", parsed.path)
    if match:
        value = match.group(1)
        return value if value.startswith("10.") else f"10.1038/{value}"
    match = re.search(r"/content/(10\.\d{4,9}/[^?#]+)", parsed.path)
    if match:
        return re.sub(r"v\d+(?:\.full)?$", "", match.group(1))
    query_match = re.search(r"(?:^|[?&])id=(10\.\d{4,9}/[^&]+)", url)
    return query_match.group(1) if query_match else ""


def doi_from_page(text):
    match = re.search(r"10\.\d{4,9}/[A-Z0-9._;()/:+-]+", text or "", flags=re.IGNORECASE)
    if not match:
        return ""
    doi = match.group(0).replace("--", "-")
    doi = re.sub(r"(?:-red)?\.(?:svg|png)$", "", doi, flags=re.IGNORECASE)
    return doi.rstrip(".,;)")


def paper_metadata(config, previous):
    if not config or not config.get("url"):
        return previous or {}
    parser = MetadataParser()
    try:
        parser.feed(fetch_html(config["url"]))
    except (HTTPError, URLError, TimeoutError):
        parser = None
    meta = parser.meta if parser else {}
    authors = parser.authors if parser else []
    title = meta.get("citation_title") or meta.get("dc.title") or (previous or {}).get("title", "")
    journal = meta.get("citation_journal_title") or meta.get("prism.publicationname") or (previous or {}).get("journal", "")
    year_value = meta.get("dc.date") or meta.get("citation_publication_date") or meta.get("citation_date") or (previous or {}).get("year", "")
    doi = doi_from_url(config["url"])
    if doi and (not title or not journal or not authors):
        try:
            crossref = fetch(f"https://api.crossref.org/works/{doi}", as_json=True)["message"]
            title = title or (crossref.get("title") or [""])[0]
            journal = journal or (crossref.get("container-title") or [""])[0]
            authors = authors or [author.get("family", "") for author in crossref.get("author", [])]
            date_parts = (crossref.get("published") or crossref.get("issued") or {}).get("date-parts", [[]])
            if not year_value and date_parts and date_parts[0]:
                year_value = str(date_parts[0][0])
        except (HTTPError, URLError, TimeoutError, KeyError):
            pass
    year_match = re.search(r"\b(19|20)\d{2}\b", str(year_value))
    return {
        "url": config["url"],
        "logo": direct_dropbox(config.get("logo", "")),
        "author": short_author(authors) or (previous or {}).get("author", ""),
        "title": clean_description(title),
        "journal": clean_description(journal),
        "year": year_match.group(0) if year_match else str(year_value),
    }


def build_entry(configured_url, previous, tools, live_repositories):
    name = repository_name(configured_url)
    old_entry = previous.get(name.lower(), {})
    old_repo = old_entry.get("repo", {})
    live_repo = live_repositories.get(name.lower(), {})
    repo_source = {**old_repo, **live_repo}
    site_url = configured_url
    parser = MetadataParser()
    site_html = ""
    try:
        site_html = fetch(site_url)
        parser.feed(site_html)
        description = clean_description(parser.meta.get("description") or parser.meta.get("og:description"))
        logo = first_image(site_url, parser)
    except (HTTPError, URLError, TimeoutError):
        description = ""
        logo = ""
    old_site = previous.get(name.lower(), {}).get("site", {})
    configured_paper = dict(tools.get(name.lower()) or {})
    site_doi = doi_from_page(site_html)
    if site_doi:
        configured_paper["url"] = f"https://doi.org/{site_doi}"
        # The package DOI is authoritative; journal artwork is assigned only
        # after the resolved journal has been verified.
        configured_paper["logo"] = ""
    paper = paper_metadata(configured_paper, old_entry.get("paper"))
    if len(description) < 60:
        description = repo_source.get("description") or old_site.get("description") or description
    if len(description) < 60 and paper.get("title"):
        description = f"Software implementing the methods described in “{paper['title']}”."
    topics = repo_source.get("topics") or derived_topics(
        description, repo_source.get("description"), paper.get("title")
    )
    return {
        "configuredUrl": configured_url,
        "site": {
            "url": site_url,
            "description": description or old_site.get("description") or old_repo.get("description") or "",
            "logo": logo or old_site.get("logo") or "",
        },
        "paper": paper,
        "repo": {
            **repo_source,
            "name": repo_source.get("name") or name,
            "html_url": repo_source.get("html_url") or f"https://github.com/{ORG}/{name}",
            "homepage": repo_source.get("homepage") or (site_url if urlparse(site_url).hostname != "github.com" else ""),
            "default_branch": repo_source.get("default_branch") or "main",
            "description": repo_source.get("description") or description,
            "topics": topics,
            "stargazers_count": repo_source.get("stargazers_count") or 0,
            "open_issues_count": repo_source.get("open_issues_count") or 0,
            "forks_count": repo_source.get("forks_count") or 0,
            "language": repo_source.get("language"),
            "license": repo_source.get("license"),
            "pushed_at": repo_source.get("pushed_at") or "1970-01-01T00:00:00Z",
        },
    }


def main():
    urls = [line.strip() for line in CONFIG.read_text().splitlines() if re.match(r"^https?://", line.strip())]
    previous_entries = []
    if OUTPUT.exists():
        try:
            previous_entries = json.loads(OUTPUT.read_text())
        except json.JSONDecodeError:
            pass
    previous = {entry.get("repo", {}).get("name", "").lower(): entry for entry in previous_entries}
    try:
        raw_tools = fetch(TOOLS_URL, as_json=True)
        tools = {name.lower(): value for name, value in raw_tools.items()}
    except (HTTPError, URLError, TimeoutError):
        tools = {}
    try:
        repositories = fetch(f"https://api.github.com/orgs/{ORG}/repos?per_page=100&type=public", as_json=True)
        live_repositories = {repo["name"].lower(): repo for repo in repositories}
    except (HTTPError, URLError, TimeoutError):
        live_repositories = {}
    entries = []
    for url in urls:
        try:
            entries.append(build_entry(url, previous, tools, live_repositories))
        except (HTTPError, URLError, TimeoutError, ValueError) as error:
            name = repository_name(url).lower()
            if name in previous:
                entries.append(previous[name])
            else:
                print(f"Skipping {url}: {error}")
    journal_logos = {
        entry["paper"].get("journal", "").lower(): entry["paper"].get("logo", "")
        for entry in previous_entries
        if entry.get("paper", {}).get("journal") and entry.get("paper", {}).get("logo")
    }
    journal_logos.update({
        entry["paper"].get("journal", "").lower(): entry["paper"].get("logo", "")
        for entry in entries
        if entry.get("paper", {}).get("journal") and entry.get("paper", {}).get("logo")
    })
    for entry in entries:
        paper = entry.get("paper", {})
        if paper.get("journal") and not paper.get("logo"):
            paper["logo"] = journal_logos.get(paper["journal"].lower(), "")
    OUTPUT.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n")
    BUILD_METADATA.write_text(json.dumps({"generated": date.today().isoformat()}, indent=2) + "\n")
    print(f"Software catalogue: {len(entries)} packages")


if __name__ == "__main__":
    main()
