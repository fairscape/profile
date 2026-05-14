# Fairscape RO-Crate Profile

This repository is the canonical home of the **Fairscape Release RO-Crate Profile** — the structural and semantic constraints that an RO-Crate must satisfy to be considered a Fairscape release.

The rendered specification lives at **<https://fairscape.github.io/profile/>**.

## What's a Fairscape Release Crate?

A Fairscape Release Crate is an [RO-Crate 1.2](https://www.researchobject.org/ro-crate/specification/1.2/) packaging a versioned, AI-ready research dataset together with provenance, schema, and machine-learning-readiness metadata. The profile constrains and extends:

- **[RO-Crate 1.2](https://w3id.org/ro/crate/1.2)** — base packaging and metadata layout
- **[EVI Ontology](https://w3id.org/EVI)** — `Dataset`, `Software`, `MLModel`, `Computation`, `Annotation`, `Experiment`, …
- **[PROV-O](http://www.w3.org/ns/prov)** — `prov:used`, `prov:wasGeneratedBy`, `prov:wasAttributedTo`
- **[Schema.org](https://schema.org/)** — `Person`, `Organization`, `Dataset`, `author`, `license`, …
- **[Croissant / Croissant-RAI 1.0](http://mlcommons.org/croissant/1.0)** — ML crosswalk emitted alongside each release

## Published versions

| Version | Profile URI | Specification | Status |
|---|---|---|---|
| 0.1 | `https://w3id.org/fairscape/profile/0.1` | [v0.1 spec](https://fairscape.github.io/profile/0.1/) | Current |

Profile URIs are **immutable**. Future revisions will be published under a new URI (e.g. `…/0.2`, `…/1.0`); a crate's `dct:conformsTo` value pins the exact revision it was authored against.

## How conformance is signaled

A Fairscape release crate declares conformance by setting `dct:conformsTo` on its Root Data Entity:

```json
{
  "@id": "ark:99999/my-release",
  "@type": ["Dataset", "https://w3id.org/EVI#ROCrate"],
  "conformsTo": { "@id": "https://w3id.org/fairscape/profile/0.1" }
}
```

Conformance is checkable via `fairscape-cli rocrate validate` (Pydantic-based structural validation).

## Profile artifacts

Each version lives under `profile/<version>/`. The contents follow the [W3C Profiles Vocabulary (PROF)](https://www.w3.org/TR/dx-prof/) resource roles:

| Artifact | Path | PROF role | Format |
|---|---|---|---|
| Profile Crate manifest | [`profile/0.1/ro-crate-metadata.json`](profile/0.1/ro-crate-metadata.json) | — | JSON-LD |
| W3C PROF manifest | [`profile/0.1/profile.ttl`](profile/0.1/profile.ttl) | — | Turtle |
| EVI ontology (classes/properties) | [`profile/0.1/evi-vocabulary.ttl`](profile/0.1/evi-vocabulary.ttl) | `role:vocabulary` | Turtle |
| Per-class JSON Schemas | [`profile/0.1/schemas/`](profile/0.1/schemas/) | `role:schema` | JSON Schema |
| Canonical conforming crate | [`profile/0.1/examples/release/`](profile/0.1/examples/release/) | `role:example` | JSON-LD |
| Validator | [fairscape/fairscape-cli](https://github.com/fairscape/fairscape-cli#validate) | `role:validation` | Python |

Each artifact resolves at `https://fairscape.github.io/profile/0.1/<artifact>` — the same path declared inside `profile.ttl` and the Profile Crate manifest.

## Repository layout

```
profile/                  # the canonical profile artifacts (source of truth)
  0.1/
    ro-crate-metadata.json
    profile.ttl
    evi-vocabulary.ttl
    schemas/
    examples/release/
site/                     # Astro + Starlight source for the rendered spec site
README.md                 # you are here
```

The `site/` folder is the documentation generator — see [`site/README.md`](site/README.md) if you're working on the rendered spec, otherwise ignore it.

## Versioning policy

- Backwards-incompatible changes (relaxing or tightening any **MUST**) → **MAJOR** bump, new URI.
- Additive changes (new **MAY** properties, new supporting files) → **MINOR** bump, new URI.
- The profile URI is the version pin. Never mutate a published version in place.

## Related Fairscape projects

- [fairscape-cli](https://github.com/fairscape/fairscape-cli) — builds and validates release crates
- [fairscape_models](https://github.com/fairscape/fairscape_models) — Pydantic models (authoritative source for required/optional fields)
- [fairscape_server](https://github.com/fairscape/fairscape_server) — API server
- [fairscape_web_client](https://github.com/fairscape/fairscape_web_client) — web UI

## License

Profile content is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
