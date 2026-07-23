<!-- Editorial content for index.qmd. -->

::: {.hero style="--hero-image: url('content/images/home-hero.png');"}
::: {.hero-copy}
<p class="eyebrow"><strong>Cancer Data Science Laboratory · University of Trieste</strong></p>

<h1>We use data and artificial intelligence to understand how cancer changes.</h1>

Cancer is not a static disease. Our laboratory studies how tumours develop, adapt and respond to treatment, creating new ways to interpret complex biomedical data.

<div class="hero-actions">
<a href="research.html" class="button button-primary">Explore our research</a>
<a href="join.html" class="button button-secondary">Join the lab</a>
<button type="button" class="button button-contact" data-contact-open aria-haspopup="dialog">Contact us</button>
<button type="button" class="button button-visit" data-visit-open aria-haspopup="dialog">Visit us</button>
</div>
:::
:::

<dialog class="contact-dialog" id="contact-dialog" aria-labelledby="contact-dialog-title">
<div class="contact-dialog-inner">
<button type="button" class="contact-dialog-close" data-contact-close aria-label="Close contact options">×</button>
<p class="eyebrow">Get in touch</p>
<h2 id="contact-dialog-title">Who would you like to contact?</h2>
<div class="contact-options">
<a href="mailto:cdslab@units.onmicrosoft.com" class="contact-option">
<span>WHOLE LABORATORY</span>
<strong>Email the Cancer Data Science Laboratory</strong>
<small>cdslab@units.onmicrosoft.com</small>
</a>
<a href="mailto:gcaravagna@units.it" class="contact-option">
<span>PRINCIPAL INVESTIGATOR</span>
<strong>Email Giulio Caravagna</strong>
<small>gcaravagna@units.it</small>
</a>
<a href="https://app.reclaim.ai/m/giulio-caravagna" class="contact-option" target="_blank" rel="noopener">
<span>PRINCIPAL INVESTIGATOR</span>
<strong>Book a meeting with Giulio</strong>
<small>Open the Reclaim booking page ↗</small>
</a>
</div>
</div>
</dialog>

<dialog class="contact-dialog visit-dialog" id="visit-dialog" aria-labelledby="visit-dialog-title">
<div class="contact-dialog-inner">
<button type="button" class="contact-dialog-close" data-visit-close aria-label="Close location information">×</button>
<p class="eyebrow">Visit the laboratory</p>
<h2 id="visit-dialog-title">Find us in Trieste.</h2>
<address class="visit-address">
<strong>Cancer Data Science Laboratory</strong><br>
Department of Mathematics, Informatics and Geosciences<br>
University of Trieste<br>
Via D. Economo 12/3, 34123 Trieste, Italy
</address>
<div class="visit-map">
<iframe src="https://maps-api-ssl.google.com/maps?hl=en-US&amp;ll=45.64469,13.758148&amp;output=embed&amp;q=45.64442,13.758257&amp;z=18" title="Map showing the Cancer Data Science Laboratory in Via D. Economo, Trieste" loading="lazy" allowfullscreen></iframe>
</div>
<a class="visit-directions" href="https://www.google.com/maps?q=45.64442,13.758257" target="_blank" rel="noopener">Open directions in Google Maps ↗</a>
</div>
</dialog>

<script>
document.addEventListener("DOMContentLoaded", () => {
  const configureDialog = (dialogId, openSelector, closeSelector) => {
    const dialog = document.getElementById(dialogId);
    const openButton = document.querySelector(openSelector);
    const closeButton = dialog?.querySelector(closeSelector);

    openButton?.addEventListener("click", () => dialog?.showModal());
    closeButton?.addEventListener("click", () => dialog?.close());
    dialog?.addEventListener("click", (event) => {
      if (event.target === dialog) dialog.close();
    });
  };

  configureDialog("contact-dialog", "[data-contact-open]", "[data-contact-close]");
  configureDialog("visit-dialog", "[data-visit-open]", "[data-visit-close]");
});
</script>

::: {.signal-strip}
::: {.signal-item}
**COMPUTATIONAL ONCOLOGY**

Methods designed around real biological and clinical problems.
:::
::: {.signal-item}
**INTERDISCIPLINARY BY DESIGN**

Computer science, statistics, physics, biology and medicine.
:::
::: {.signal-item}
**OPEN RESEARCH**

Reproducible software, data and collaborative science.
:::
:::

::: {.section-wrap .funders-section}
## Funded by

Our research is made possible by the generous support of several institutions.

<div class="funders-grid">
<a class="funder-card" href="projects.html" aria-label="View projects funded by Fondazione AIRC">
<img class="funder-logo funder-airc" src="assets/funder-airc.png" alt="Fondazione AIRC per la ricerca sul cancro">
</a>
<a class="funder-card" href="projects.html" aria-label="View projects funded by the Ministry of University and Research">
<img class="funder-logo funder-mur" src="assets/funder-mur.png" alt="Ministero dell'Università e della Ricerca">
</a>
<a class="funder-card funder-card-wide" href="projects.html" aria-label="View projects funded by the European Union – NextGenerationEU">
<img class="funder-logo funder-nextgen" src="content/images/funder-nextgenerationeu.png" alt="Funded by the European Union – NextGenerationEU">
</a>
</div>
:::

::: {.section-wrap .people-teaser}
::: {.people-copy}
<p class="eyebrow">Different backgrounds, one shared problem</p>

## A computational lab with biological and clinical reach.

Our group brings together researchers trained in computer science, data science, physics, biology and medicine. We are based in Trieste and collaborate internationally.

[Meet the team](people.qmd){.text-link}
:::

::: {.people-image}
<img src="assets/team-editorial-v2.png" alt="Members of the Caravagna Lab collaborating around computational models and biological data.">
:::
:::

::: {.join-banner}
<p class="eyebrow">Work with us</p>

## Bring your perspective to cancer data science.

We welcome enquiries from prospective PhD students, postdoctoral researchers, thesis students and collaborators.

[See opportunities](join.qmd){.button .button-light} [Contact Giulio](mailto:gcaravagna@units.it){.button .button-outline-light}
:::
