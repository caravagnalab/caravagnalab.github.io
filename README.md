# Caravagna Lab website

The laboratory website is a Quarto project. Editorial content lives in Markdown;
running one build regenerates the data-driven pages and the static website.

## Preview

```bash
quarto preview
```

## Build

```bash
quarto render
```

The generated static site is written to `_site/`.

## Editorial structure

- `index.qmd`, `research.qmd`, `publications.qmd`, `software.qmd`, `join.qmd`:
  page copy written in Quarto Markdown.
- `team/*.md`: one record per current member, visitor or alumnus. `people.qmd`
  is generated at build time.
- `content/projects/*.md`: one funded-project record. `projects.qmd` is generated.
- `content/papers/*.md`: the reusable pool of example papers shown on projects.
  `assets/papers.json` is generated.
- `content/talks/*.md`: one scientific talk or outreach record. `talks.qmd` is generated.
- `content/opportunities/*.md`: the role cards shown on Join us.
- `software-packages.md`: one package website URL per line. Software metadata is
  refreshed when the site builds.
- `publication-sources.md`: the Scholar profile used to refresh publication
  metadata, with the committed JSON cache as fallback.

Do not edit `people.qmd`, `projects.qmd`, `talks.qmd`,
`includes/join-opportunities.html` or generated JSON files directly: the next
build will replace them.

## Publishing

`.github/workflows/publish.yml` renders the site and deploys `_site` to GitHub
Pages on every push to `master`. In the repository settings, choose **GitHub
Actions** as the Pages source.
