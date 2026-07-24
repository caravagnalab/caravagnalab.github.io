<!-- Editorial content for publications.qmd. -->

::: {.hero .outputs-hero style="--hero-image: url('content/images/outputs-hero.png');"}
::: {.hero-copy}
<p class="eyebrow">Outputs · Publications</p>
<h1>Our scientific record.</h1>
<p>A live publication list drawn from Giulio Caravagna’s Google Scholar profile. Citation counts reflect Scholar and may change over time.</p>
<p class="publications-context-note">The laboratory was established in 2020; earlier publications reflect the PI’s PhD and postdoctoral research.</p>
:::
:::

::: {.publications-page}
<div class="publications-topline">
<a class="publications-scholar-link" href="https://scholar.google.com/citations?hl=en&user=iktXWosAAAAJ&view_op=list_works&sortby=pubdate" target="_blank" rel="noopener"><img src="https://scholar.google.com/favicon.ico" alt="" aria-hidden="true"> Google Scholar profile</a>
</div>

<nav class="publications-view-switch" aria-label="Choose publication view">
<span>View</span>
<button class="is-active" type="button" data-publications-view="featured" aria-pressed="true">Featured</button>
<button type="button" data-publications-view="all" aria-pressed="false">All papers</button>
</nav>

<div class="publications-view-panel" data-publications-panel="featured">
{{< include content/outputs/publications/featured.md >}}
</div>

<div class="publications-view-panel" data-publications-panel="all" hidden>
<div class="publications-toolbar">
<p><span id="publications-count">Loading</span> publications · <span id="publications-updated">connecting to Scholar</span></p>
</div>

<div class="publications-sort" aria-label="Sort publications">
<span>Sort by</span>
<button class="publication-sort is-active" type="button" data-publication-sort="year">Year</button>
<button class="publication-sort" type="button" data-publication-sort="citations">Citations</button>
<label class="publication-year-filter">Filter by year
<select id="publication-year-filter" aria-label="Filter publications by year">
<option value="all">All years</option>
</select>
</label>
</div>

<div id="publications-list" class="publications-list" aria-live="polite"></div>
</div>
:::

<script src="assets/publications.js" defer></script>
<script>
document.addEventListener("DOMContentLoaded", () => {
  const buttons = [...document.querySelectorAll("[data-publications-view]")];
  const panels = [...document.querySelectorAll("[data-publications-panel]")];
  const show = (view) => {
    buttons.forEach((button) => {
      const active = button.dataset.publicationsView === view;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    panels.forEach((panel) => {
      panel.hidden = panel.dataset.publicationsPanel !== view;
    });
  };
  buttons.forEach((button) => button.addEventListener("click", () => show(button.dataset.publicationsView)));
  show("featured");
});
</script>
