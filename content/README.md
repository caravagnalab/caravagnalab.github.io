# Website content

Edit files in this directory to update the website. The folders follow the
navigation shown in the header:

- `home/`: landing page.
- `research/overview/`: research overview.
- `research/projects/`: project introduction, project records and example papers.
- `outputs/publications/`: publication-page copy and external publication sources.
- `outputs/software/`: software-page copy and package website list.
- `talks-outreach/`: page copy and individual talks or outreach activities.
- `team/`: team-page copy and one profile per person.
- `join/`: Join-us copy and one record per opportunity.

Files named `page.md` contain section-level copy. Folders named `items`,
`profiles`, `opportunities` or `example-papers` contain one Markdown record per
entry.

Team portraits live in `team/images/`. Every profile that has a portrait
declares it explicitly in its TOML front matter, for example:

```toml
photo = "content/team/images/giulio-caravagna-v2.png"
```

After editing, run:

```bash
quarto render
```

Do not edit the generated root pages `people.qmd`, `projects.qmd` and
`talks.qmd`, the generated include under `includes/`, or JSON files under
`assets/`.
