# site/ — Fairscape Profile spec site

The rendered specification at <https://fairscape.github.io/profile/> is built from this folder. The profile artifacts themselves live in [`../profile/`](../profile/) and are exposed to the site via the symlink `site/public/0.1 → ../../profile/0.1`, so every file under `profile/0.1/` serves at `/profile/0.1/<path>` without duplication.

Built with [Astro](https://astro.build) + [Starlight](https://starlight.astro.build). Themed to match the Fairscape web client palette (`#005f73` primary, `#ee9b00` accent, Inter).

## Local development

```bash
cd site
npm install
npm run dev          # http://localhost:4321/profile/
npm run build        # output to ./dist
npm run preview
```

## Layout

```
site/
  src/
    content/
      docs/
        index.mdx                       # /profile/ landing
        0.1/
          index.md                      # /profile/0.1/ (the spec)
          croissant-mapping.md          # /profile/0.1/croissant-mapping/
          schemas/index.md              # /profile/0.1/schemas/
    styles/fairscape.css                # palette + font overrides (Starlight CSS vars)
    assets/fairscape-mark.svg
  public/
    0.1 -> ../../profile/0.1            # symlink to canonical artifacts
  astro.config.mjs                      # site / base / sidebar
```

## Adding a new profile version

1. Drop the new artifacts in `../profile/<version>/`.
2. Add a content folder `src/content/docs/<version>/` with markdown pages (set `slug: "<version>"` in frontmatter — Astro otherwise strips the dot).
3. Update the sidebar in `astro.config.mjs`.
4. Update the symlink: `ln -sfn ../../profile/<version> public/<version>`.

## Deployment

`.github/workflows/deploy.yml` (at the repo root) builds on every push to `main` and publishes to GitHub Pages. After the first push, set **Settings → Pages → Source = GitHub Actions** once.

## Why Starlight (not mkdocs)?

mkdocs-material is great for prose docs but boxes you in on layout and component injection. Starlight gives you the same out-of-the-box doc UX (sidebar, Pagefind search, dark mode, edit-on-GitHub) while letting you drop arbitrary Astro/React components into MDX pages — useful as the spec grows interactive bits (live RO-Crate validators, profile diffs, etc.).
