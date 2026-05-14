---
title: "Fairscape ↔ Croissant 1.0 / RAI 1.0 mapping"
description: "How a Fairscape Release Crate is projected into the Croissant 1.0 format and its Responsible AI extension."
template: doc
slug: "0.1/croissant-mapping"
---


This page documents how a Fairscape Release Crate is projected into the [Croissant 1.0](http://mlcommons.org/croissant/1.0) format and its [Responsible AI extension](http://mlcommons.org/croissant/RAI/1.0). The mapping is implemented in [`fairscape_models/conversion/mapping/croissant.py`](https://github.com/fairscape/fairscape_models/blob/main/fairscape_models/conversion/mapping/croissant.py) and emitted by `fairscape-cli` as `ro-crate-croissant.json` alongside every release.

## Top-level

| Fairscape (Root) | Croissant |
|---|---|
| `@id` | `@id` |
| `name` | `name` |
| `description` | `description` |
| `keywords` | `keywords` |
| `license` | `license` |
| `author` | `creator` |
| `version` | `version` |
| `datePublished` | `datePublished` |
| `citation` | `citation` |

The Croissant root carries `dct:conformsTo: http://mlcommons.org/croissant/RAI/1.0`.

## Dataset entities

Each Fairscape `Dataset` becomes a Croissant `FileObject` or `FileSet` depending on whether `hasPart` references concrete files. The `dataSchema` link drives Croissant `RecordSet` generation.

## RAI fields

Every `rai:*` property on the Fairscape Root passes through unchanged to the Croissant root (both use the `http://mlcommons.org/croissant/RAI/` namespace). This includes `dataLimitations`, `dataBiases`, `dataCollection`, `dataAnnotationProtocol`, `personalSensitiveInformation`, and the full RAI vocabulary.

## See also

- [Croissant 1.0 specification](https://docs.mlcommons.org/croissant/docs/croissant-spec.html)
- [`fairscape_models/fairscape_models/conversion/mapping/croissant.py`](https://github.com/fairscape/fairscape_models/blob/main/fairscape_models/conversion/mapping/croissant.py) — implementation
