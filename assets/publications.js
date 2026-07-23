(() => {
  const list = document.querySelector("#publications-list");
  const count = document.querySelector("#publications-count");
  const updated = document.querySelector("#publications-updated");
  const buttons = [...document.querySelectorAll("[data-publication-sort]")];
  const roleButtons = [...document.querySelectorAll("[data-publication-role]")];
  const typeButtons = [...document.querySelectorAll("[data-publication-type]")];
  const yearFilter = document.querySelector("#publication-year-filter");
  if (!list || !count) return;

  let publications = [];
  let sortBy = "year";
  let selectedYear = "all";
  let selectedRole = "all";
  let selectedType = "all";
  const request = (url) => fetch(url).then((response) => {
    if (!response.ok) throw new Error(`Request failed: ${response.status}`);
    return response.json();
  });
  const element = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  };
  const formattedDate = (value) => new Intl.DateTimeFormat("en-GB", {
    day: "numeric", month: "long", year: "numeric"
  }).format(new Date(`${value}T12:00:00`));
  const appendHighlightedPi = (node, value) => {
    const pattern = /(?:Giulio|Gulio|G\.?)\s+Caravagna|Caravagna\s*,\s*(?:Giulio|Gulio|G\.?)/gi;
    let cursor = 0;
    for (const match of value.matchAll(pattern)) {
      node.append(document.createTextNode(value.slice(cursor, match.index)));
      node.append(element("strong", "publication-pi", match[0]));
      cursor = match.index + match[0].length;
    }
    node.append(document.createTextNode(value.slice(cursor)));
  };
  const isPi = (value) => /^(?:Giulio|Gulio|G\.?)\s+Caravagna$|^Caravagna\s+(?:Giulio|Gulio|G\.?)$/i
    .test((value || "").replace(/\./g, ".").trim());
  const piRole = (paper) => {
    if (!paper.authorsDetailed) return { first: false, last: false };
    const authors = (paper.authors || "").split(",").map((author) => author.trim()).filter(Boolean);
    return {
      first: authors.length > 0 && isPi(authors[0]),
      last: authors.length > 0 && isPi(authors[authors.length - 1])
    };
  };
  const isPreprint = (paper) => {
    const venue = (paper.venue || "").toLowerCase();
    return /biorxiv|medrxiv|arxiv|research square|ssrn|preprint/.test(venue)
      || !venue || venue === "venue not available";
  };

  const render = () => {
    const byYear = selectedYear === "all" ? publications : publications.filter((paper) =>
      selectedYear === "before-2020" ? paper.year > 0 && paper.year < 2020 : String(paper.year || 0) === selectedYear);
    const visible = selectedRole === "all"
      ? byYear
      : byYear.filter((paper) => piRole(paper)[selectedRole]);
    const typed = selectedType === "preprint" ? visible.filter(isPreprint) : visible;
    const sorted = [...typed].sort((a, b) => sortBy === "citations"
      ? b.citations - a.citations || b.year - a.year || a.title.localeCompare(b.title)
      : b.year - a.year || b.citations - a.citations || a.title.localeCompare(b.title));
    list.replaceChildren(...sorted.map((paper) => {
      const article = element("article", "publication-row");
      const main = element("div", "publication-main");
      const title = element("a", "publication-title", paper.title);
      title.href = paper.url;
      title.target = "_blank";
      title.rel = "noopener";
      const authors = element("p", `publication-authors${paper.authorsDetailed ? "" : " is-incomplete"}`);
      appendHighlightedPi(authors, paper.authors || "Authors not available");
      if (!paper.authorsDetailed) authors.append(document.createTextNode(" · Full list pending metadata refresh"));
      main.append(title, authors, element("p", "publication-venue", paper.venue || "Venue not available"));
      const doi = element(paper.doi ? "a" : "span", `publication-doi${paper.doi ? "" : " is-missing"}`,
        paper.doi ? `DOI ${paper.doi}` : "DOI not available");
      if (paper.doi) {
        doi.href = `https://doi.org/${paper.doi}`;
        doi.target = "_blank";
        doi.rel = "noopener";
      }
      main.append(doi);
      const metrics = element("div", "publication-metrics");
      metrics.append(
        element("span", "publication-year", paper.year || "Year n/a"),
        element("span", "publication-citations", `${paper.citations || 0} citations`)
      );
      if (isPreprint(paper)) {
        const preprint = element("span", "publication-preprint");
        preprint.append(element("i", "bi bi-file-earmark-text"), document.createTextNode(" Preprint"));
        metrics.append(preprint);
      }
      article.append(main, metrics);
      return article;
    }));
    count.textContent = typed.length === publications.length
      ? publications.length
      : `${typed.length} of ${publications.length}`;
    buttons.forEach((button) => button.classList.toggle("is-active", button.dataset.publicationSort === sortBy));
    roleButtons.forEach((button) => button.classList.toggle("is-active", button.dataset.publicationRole === selectedRole));
    typeButtons.forEach((button) => button.classList.toggle("is-active", button.dataset.publicationType === selectedType));
  };

  buttons.forEach((button) => button.addEventListener("click", () => {
    sortBy = button.dataset.publicationSort;
    render();
  }));
  yearFilter?.addEventListener("change", () => {
    selectedYear = yearFilter.value;
    render();
  });
  roleButtons.forEach((button) => button.addEventListener("click", () => {
    selectedRole = button.dataset.publicationRole;
    render();
  }));
  typeButtons.forEach((button) => button.addEventListener("click", () => {
    selectedType = button.dataset.publicationType;
    render();
  }));

  request("assets/scholar-publications.json")
    .then((data) => {
      publications = data.publications || [];
      if (yearFilter) {
        const years = [...new Set(publications.map((paper) => paper.year).filter((year) => year >= 2020))].sort((a, b) => b - a);
        yearFilter.append(...years.map((year) => {
          const option = document.createElement("option");
          option.value = String(year);
          option.textContent = String(year);
          return option;
        }));
        if (publications.some((paper) => paper.year > 0 && paper.year < 2020)) {
          const option = document.createElement("option");
          option.value = "before-2020";
          option.textContent = "Before 2020";
          yearFilter.append(option);
        }
      }
      if (updated && data.generated) updated.textContent = `Updated ${formattedDate(data.generated)}`;
      render();
    })
    .catch(() => {
      list.replaceChildren(element("p", "publications-error", "Publication data are temporarily unavailable."));
    });
})();
