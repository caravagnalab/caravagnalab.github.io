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

All editable website content lives below `content/`, grouped like the navigation:

```text
content/
├── home/
│   └── index.md
├── research/
│   ├── overview/page.md
│   └── projects/
│       ├── page.md
│       ├── items/*.md
│       └── example-papers/*.md
├── outputs/
│   ├── publications/
│   │   ├── page.md
│   │   └── sources.md
│   └── software/
│       ├── page.md
│       └── packages.md
├── talks-outreach/
│   ├── page.md
│   └── items/*.md
├── team/
│   ├── page.md
│   └── profiles/*.md
└── join/
    ├── page.md
    └── opportunities/*.md
```

The root `.qmd` files are thin technical wrappers or generated pages that
preserve stable public URLs such as `/research.html`. They are not editorial
sources.

Do not edit `people.qmd`, `projects.qmd`, `talks.qmd`,
`includes/join-opportunities.html` or generated JSON files directly: the next
build will replace them.

## Local workflow

1. Edit files only inside `content/`.
2. Run `quarto preview` while working.
3. Run `quarto render` before committing.
4. Review and commit the local changes.
5. Push only when the revision is ready to publish.

## Publishing

`.github/workflows/publish.yml` renders the site and deploys `_site` to GitHub
Pages on every push to `master`. In the repository settings, choose **GitHub
Actions** as the Pages source.
