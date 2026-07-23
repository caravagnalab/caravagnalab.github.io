(() => {
  const organisation = "caravagnalab";
  const grid = document.querySelector("#github-software-grid");
  const status = document.querySelector("#software-status");
  const count = document.querySelector("#software-count");
  const filters = document.querySelector("#software-filters");
  const buildDate = document.querySelector("#software-build-date");
  if (!grid || !status || !count || !filters) return;

  const request = (url, json = false) => new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    if (json) xhr.setRequestHeader("Accept", "application/vnd.github+json");
    xhr.onload = () => {
      if (xhr.status < 200 || xhr.status >= 300) {
        reject(new Error(`Request failed: ${xhr.status}`));
        return;
      }
      try {
        resolve(json ? JSON.parse(xhr.responseText) : xhr.responseText);
      } catch (error) {
        reject(error);
      }
    };
    xhr.onerror = () => reject(new Error("Network request failed"));
    xhr.send();
  });

  const formatDate = (value) => new Intl.DateTimeFormat("en", { month: "short", year: "numeric" }).format(new Date(value));
  const formatBuildDate = (value) => new Intl.DateTimeFormat("en-GB", {
    day: "numeric", month: "long", year: "numeric"
  }).format(new Date(`${value}T12:00:00`));

  if (buildDate) {
    request("assets/software-build.json", true)
      .then(({ generated }) => {
        if (!generated) return;
        buildDate.dateTime = generated;
        buildDate.textContent = formatBuildDate(generated);
      })
      .catch(() => {});
  }

  const element = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  };

  const badge = (label, value, href) => {
    const node = href ? element("a", "repo-badge") : element("span", "repo-badge");
    const kind = label === "★" ? "stars" : label.toLowerCase().replace(/\W+/g, "-");
    node.classList.add(`repo-badge-${kind}`);
    if (href) {
      node.href = href;
      node.target = "_blank";
      node.rel = "noopener";
    }
    node.append(element("span", "repo-badge-label", label), document.createTextNode(` ${value}`));
    return node;
  };

  const parseCff = (text, repo) => {
    const preferredAt = text.search(/^preferred-citation:/m);
    const source = preferredAt >= 0 ? text.slice(preferredAt) : text;
    const field = (name) => {
      const match = source.match(new RegExp(`^\\s{0,6}${name}:\\s*["']?(.+?)["']?\\s*$`, "m"));
      return match ? match[1].replace(/["']$/, "").trim() : "";
    };
    const title = field("title");
    const doi = field("doi").replace(/^https?:\/\/(dx\.)?doi\.org\//, "");
    const journal = field("journal");
    const year = field("year");
    if (!title) return null;
    return {
      title,
      meta: [journal, year].filter(Boolean).join(" · "),
      url: doi ? `https://doi.org/${doi}` : `${repo.html_url}/blob/${repo.default_branch}/CITATION.cff`
    };
  };

  const cleanMarkdown = (text) => text
    .replace(/\[\s*\]\s*\([^)]*\)/g, "")
    .replace(/!\[[^\]]*\]\([^)]*\)/g, "")
    .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1")
    .replace(/[*_`>#]/g, "")
    .replace(/^[-+]\s*/, "")
    .trim();

  const parseReadmeCitation = (text, repo) => {
    const heading = text.match(/^#{2,6}\s+(?:citation|how to cite|cite this[^\n]*)\s*$/im);
    if (!heading) return null;
    const tail = text.slice(heading.index + heading[0].length);
    const section = tail.split(/^#{1,6}\s+/m)[0];
    const lines = section.split("\n").map(cleanMarkdown).filter((line) => line.length > 35 && !/install|support|copyright/i.test(line));
    if (!lines.length) return null;
    const doiMatch = section.match(/10\.\d{4,9}\/[-._;()/:A-Z0-9]+/i);
    return {
      title: lines[0].replace(/\.$/, ""),
      meta: "Reference paper",
      url: doiMatch ? `https://doi.org/${doiMatch[0].replace(/[).,;]+$/, "")}` : `${repo.html_url}#citation`
    };
  };

  const getCitation = async (repo, configuredUrl) => {
    const raw = `https://raw.githubusercontent.com/${organisation}/${repo.name}/${repo.default_branch}`;
    let paper = null;
    try {
      paper = parseCff(await request(`${raw}/CITATION.cff`), repo);
    } catch (_) {
      for (const file of ["README.md", "README.Rmd"]) {
        try {
          paper = parseReadmeCitation(await request(`${raw}/${file}`), repo);
          if (paper) break;
        } catch (_) {}
      }
    }
    if (paper && configuredUrl) paper.url = configuredUrl;
    if (!paper && configuredUrl) paper = { title: "Reference paper", meta: "Publication", url: configuredUrl };
    return paper;
  };

  const loadLogo = (repo, site, frame) => {
    const raw = `https://raw.githubusercontent.com/${organisation}/${repo.name}/${repo.default_branch}`;
    const homepage = (repo.homepage || "").replace(/\/$/, "");
    const published = `https://${organisation}.github.io/${repo.name}`;
    const candidates = [
      site.logo,
      homepage && `${homepage}/reference/figures/logo.svg`, homepage && `${homepage}/reference/figures/logo.png`,
      homepage && `${homepage}/logo.svg`, homepage && `${homepage}/logo.png`,
      `${published}/reference/figures/logo.svg`, `${published}/reference/figures/logo.png`,
      `${published}/logo.svg`, `${published}/logo.png`,
      `${raw}/logo.svg`, `${raw}/logo.png`, `${raw}/man/figures/logo.svg`,
      `${raw}/man/figures/logo.png`, `${raw}/pkgdown/logo.svg`, `${raw}/pkgdown/logo.png`,
      `${raw}/inst/figures/logo.svg`, `${raw}/inst/figures/logo.png`,
      `${raw}/docs/reference/figures/logo.svg`, `${raw}/docs/reference/figures/logo.png`,
      `${raw}/docs/logo.svg`, `${raw}/docs/logo.png`,
      `https://opengraph.githubassets.com/${encodeURIComponent(repo.updated_at)}/${organisation}/${repo.name}`
    ].filter(Boolean);
    const image = element("img", "software-logo");
    image.alt = `${repo.name} logo`;
    image.loading = "lazy";
    const fallback = repo.name.slice(0, 2).toUpperCase();
    let index = 0;
    let timer;
    const tryCandidate = () => {
      clearTimeout(timer);
      if (index >= candidates.length) {
        frame.classList.remove("has-image");
        frame.replaceChildren(document.createTextNode(fallback));
        return;
      }
      image.src = candidates[index];
      timer = setTimeout(() => {
        if (!frame.classList.contains("has-image")) {
          index += 1;
          tryCandidate();
        }
      }, 1400);
    };
    image.onload = () => {
      clearTimeout(timer);
      frame.classList.add("has-image");
    };
    image.onerror = () => {
      clearTimeout(timer);
      index += 1;
      tryCandidate();
    };
    frame.replaceChildren(image);
    tryCandidate();
  };

  const makeCard = ({ repo, site, paper }) => {
    const card = element("article", "github-software-card");
    card.dataset.tags = repo.topics.join(" ").toLowerCase();
    const top = element("div", "software-card-top");
    const logo = element("a", "software-logo-frame", repo.name.slice(0, 2).toUpperCase());
    logo.href = site.url || repo.html_url;
    logo.target = "_blank";
    logo.rel = "noopener";
    logo.title = `${repo.name} ${site.url ? "documentation" : "repository"}`;
    loadLogo(repo, site, logo);

    const identity = element("div", "software-identity");
    const name = element("a", "software-name", repo.name);
    name.href = repo.html_url;
    name.target = "_blank";
    name.rel = "noopener";
    identity.append(name);
    if (repo.topics.length) identity.append(element("p", "software-topics", repo.topics.slice(0, 3).join(" · ")));
    top.append(logo, identity);

    const description = element("p", "software-description", site.description || repo.description || "Description maintained by the package website.");
    const metrics = element("div", "software-metrics");
    metrics.append(
      badge("★", repo.stargazers_count, `${repo.html_url}/stargazers`),
      badge("Issues", repo.open_issues_count, `${repo.html_url}/issues`),
      badge("Forks", repo.forks_count, `${repo.html_url}/forks`)
    );
    metrics.append(badge(
      "License",
      repo.license?.spdx_id && repo.license.spdx_id !== "NOASSERTION" ? repo.license.spdx_id : "Not declared"
    ));
    metrics.append(badge("Updated", formatDate(repo.pushed_at)));

    const citation = element("div", "software-citation is-loading", "Looking for the reference paper…");
    const renderPaper = (reference) => {
      citation.classList.remove("is-loading");
      if (!reference) {
        reference = { title: "To appear", meta: "Reference paper" };
      }
      const meta = reference.author
        ? [reference.author, reference.journal, reference.year].filter(Boolean).join(" · ")
        : (reference.meta || "Reference paper");
      const label = element("span", "software-citation-label", meta);
      const link = element(reference.url ? "a" : "span", "software-citation-title", reference.title || "Reference paper");
      if (reference.url) {
        link.href = reference.url;
        link.target = "_blank";
        link.rel = "noopener";
      }
      if (reference.logo) {
        const journalLogo = element("img", "software-journal-logo");
        journalLogo.src = reference.logo;
        journalLogo.alt = reference.journal ? `${reference.journal} logo` : "Journal logo";
        journalLogo.onerror = () => journalLogo.remove();
        citation.replaceChildren(journalLogo, label, link);
      } else {
        citation.replaceChildren(label, link);
      }
    };
    if (paper?.url) {
      renderPaper(paper);
    } else {
      getCitation(repo, "").then(renderPaper);
    }

    const footer = element("div", "software-card-footer");
    const repository = element("a", "software-repo-link is-repository");
    repository.href = repo.html_url;
    repository.target = "_blank";
    repository.rel = "noopener";
    repository.append(element("i", "bi bi-github"), document.createTextNode("Repository"));
    footer.append(repository);
    if (site.url) {
      const documentation = element("a", "software-repo-link is-documentation");
      documentation.href = site.url;
      documentation.target = "_blank";
      documentation.rel = "noopener";
      documentation.append(element("i", "bi bi-globe2"), document.createTextNode("Website"));
      footer.append(documentation);
    }

    card.append(top, description, metrics, citation, footer);
    return card;
  };

  const buildFilters = (items) => {
    const topics = [...new Set(items.flatMap(({ repo }) => repo.topics))].sort((a, b) => a.localeCompare(b));
    const all = element("button", "software-filter is-active", "All");
    all.type = "button";
    all.dataset.topic = "";
    filters.append(all, ...topics.map((topic) => {
      const button = element("button", "software-filter", topic);
      button.type = "button";
      button.dataset.topic = topic.toLowerCase();
      return button;
    }));
    filters.addEventListener("click", (event) => {
      const button = event.target.closest(".software-filter");
      if (!button) return;
      filters.querySelectorAll(".software-filter").forEach((item) => item.classList.toggle("is-active", item === button));
      const topic = button.dataset.topic;
      let visible = 0;
      grid.querySelectorAll(".github-software-card").forEach((card) => {
        const show = !topic || card.dataset.tags.split(" ").includes(topic);
        card.hidden = !show;
        if (show) visible += 1;
      });
      count.textContent = visible;
    });
  };

  request("assets/software-catalog.json", true)
    .then(async (items) => {
      try {
        const repositories = await request(`https://api.github.com/orgs/${organisation}/repos?per_page=100&type=public`, true);
        const live = new Map(repositories.map((repo) => [repo.name.toLowerCase(), repo]));
        return items.map((item) => ({ ...item, repo: live.get(item.repo.name.toLowerCase()) || item.repo }));
      } catch (_) {
        return items;
      }
    })
    .then((items) => items.filter((item) => item?.repo)
      .sort((a, b) => b.repo.stargazers_count - a.repo.stargazers_count || a.repo.name.localeCompare(b.repo.name)))
    .then((items) => {
      count.textContent = items.length;
      status.remove();
      grid.replaceChildren(...items.map(makeCard));
      buildFilters(items);
    })
    .catch(() => {
      count.textContent = "—";
      status.textContent = "GitHub is temporarily unavailable. Browse the laboratory organisation directly.";
      status.classList.add("is-error");
    });
})();
