(() => {
  const slots = [...document.querySelectorAll("[data-project-papers]")];
  if (!slots.length) return;

  const randomScore = (paper) => Math.pow(Math.random(), 1 / (paper.weight || 1));

  const makePaper = (paper) => {
    const link = document.createElement("a");
    link.className = "project-paper";
    link.href = paper.url;
    link.target = "_blank";
    link.rel = "noopener";

    const meta = document.createElement("span");
    meta.className = "project-paper-meta";
    meta.textContent = [paper.journal, paper.year, paper.status].filter(Boolean).join(" · ");

    const title = document.createElement("span");
    title.className = "project-paper-title";
    title.textContent = paper.title;

    const arrow = document.createElement("span");
    arrow.className = "project-paper-arrow";
    arrow.setAttribute("aria-hidden", "true");
    arrow.textContent = "↗";

    link.append(meta, title, arrow);
    return link;
  };

  const loadPaperPool = () => new Promise((resolve, reject) => {
    const request = new XMLHttpRequest();
    request.open("GET", "assets/papers.json");
    request.responseType = "json";
    request.onload = () => {
      if (request.status < 200 || request.status >= 300) {
        reject(new Error("Paper pool unavailable"));
        return;
      }
      resolve(request.response);
    };
    request.onerror = () => reject(new Error("Paper pool unavailable"));
    request.send();
  });

  loadPaperPool()
    .then((papers) => {
      const used = new Set();
      const orderedSlots = [...slots].sort((a, b) => {
        const count = (slot) => papers.filter((paper) => paper.projects.includes(slot.dataset.projectPapers)).length;
        return count(a) - count(b);
      });

      orderedSlots.forEach((slot) => {
        const candidates = papers
          .filter((paper) => paper.projects.includes(slot.dataset.projectPapers) && !used.has(paper.id))
          .map((paper) => ({ paper, score: randomScore(paper) }))
          .sort((a, b) => b.score - a.score)
          .slice(0, 2)
          .map(({ paper }) => paper);

        candidates.forEach((paper) => {
          used.add(paper.id);
          slot.append(makePaper(paper));
        });
      });
    })
    .catch(() => slots.forEach((slot) => slot.remove()));
})();
