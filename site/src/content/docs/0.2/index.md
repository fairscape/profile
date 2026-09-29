---
title: Fairscape Release RO-Crate Profile v0.2
description: Structural and semantic constraints that an RO-Crate must satisfy to be considered a Fairscape release.
template: doc
slug: "0.2"
tableOfContents:
  minHeadingLevel: 2
  maxHeadingLevel: 3
---

**Profile URI:** `https://w3id.org/fairscape/profile/0.2`
**Status:** Current · supersedes [v0.1](/profile/0.1/)

This document specifies the **Fairscape Release RO-Crate Profile**: the structural and semantic constraints that an RO-Crate must satisfy to be considered a Fairscape release. The profile is identified by the URI `https://w3id.org/fairscape/profile/0.2` and is published as a W3C PROF-conformant Profile Crate.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Overview

A Fairscape Release Crate is an [RO-Crate 1.2](https://www.researchobject.org/ro-crate/specification/1.2/) packaging a versioned, AI-ready research dataset together with provenance, schema, and machine-learning-readiness metadata. The profile constrains and extends:

- **[RO-Crate 1.2](https://w3id.org/ro/crate/1.2)** — base packaging and metadata layout.
- **[EVI Ontology](https://w3id.org/EVI)** — domain classes (`Dataset`, `Software`, `MLModel`, `Computation`, `Annotation`, `Experiment`, …) and properties.
- **[PROV-O](http://www.w3.org/ns/prov)** — `prov:used`, `prov:wasGeneratedBy`, `prov:wasAttributedTo`, etc.
- **[Schema.org](https://schema.org/)** — core types (`Person`, `Organization`, `Dataset`) and properties (`author`, `license`, `keywords`, `hasPart`, …).
- **[Croissant / Croissant-RAI 1.0](http://mlcommons.org/croissant/1.0)** — machine-learning crosswalk emitted alongside each release.

The constituent artifacts of this profile are described in the [Profile Crate](/profile/0.2/ro-crate-metadata.json) (W3C PROF manifest) and in the Turtle profile manifest [`profile.ttl`](/profile/0.2/profile.ttl).

### 1.1 Changes from v0.1

- **SHACL shapes** ([`fairscape-shapes.ttl`](/profile/0.2/fairscape-shapes.ttl)) are now a normative validation artifact. They add graph-level rules the Pydantic models cannot express. For example, a `generatedBy` edge **MUST** point at a Computation, Experiment or Activity. See [§5](#5-validation-rules).
- A crate conforms only if the shapes report no **Violation** (§2, condition 6).
- The EVI vocabulary is regenerated from the current `fairscape_models`.

---

## 2. Conformance

A crate conforms to this profile if and only if all of the following are true:

1. The crate's `ro-crate-metadata.json` parses as valid JSON-LD per RO-Crate 1.2.
2. The **Root Data Entity** carries a `dct:conformsTo` (`conformsTo` in JSON-LD shorthand) property whose value (or one element thereof) is `{"@id": "https://w3id.org/fairscape/profile/0.2"}`.
3. The Root Data Entity's `@type` list **MUST** include `"Dataset"` and `"https://w3id.org/EVI#ROCrate"`.
4. The Metadata Descriptor (the entity with `@id: ro-crate-metadata.json`) carries a `conformsTo` of `{"@id": "https://w3id.org/ro/crate/1.2"}`.
5. Every required property listed in §4 below is present on its respective entity.
6. Validating the crate's graph against the profile's [SHACL shapes](/profile/0.2/fairscape-shapes.ttl) yields no result of severity `sh:Violation`. Results of severity `sh:Warning` are advisory and do not affect conformance.

Conditions 1–5 are checked by the Pydantic models in [`fairscape_models`](https://github.com/fairscape/fairscape_models) (`ROCrateV1_2.model_validate`), and condition 6 by `fairscape_models.validation.shacl.validate_shacl`, which needs the `[shacl]` extra (`pip install 'fairscape-models[shacl]'`). Any SHACL engine gives the same results for condition 6. See [Validation rules](/profile/0.2/validation/).

### 2.1 Example conformance signal

```json
{
  "@graph": [
    {
      "@id": "ro-crate-metadata.json",
      "@type": "CreativeWork",
      "conformsTo": { "@id": "https://w3id.org/ro/crate/1.2" },
      "about": { "@id": "ark:99999/my-release" }
    },
    {
      "@id": "ark:99999/my-release",
      "@type": ["Dataset", "https://w3id.org/EVI#ROCrate"],
      "conformsTo": { "@id": "https://w3id.org/fairscape/profile/0.2" },
      "name": "…",
      "…": "…"
    }
  ]
}
```

---

## 3. Release file manifest

A conforming Fairscape release **MAY** be distributed as a directory or zip archive whose root contains the files listed below. The presence of each is normative as indicated.

| File | Cardinality | Purpose |
|---|---|---|
| `ro-crate-metadata.json` | **MUST** | RO-Crate JSON-LD manifest (base RO-Crate 1.2 requirement). |
| `ro-crate-preview.html` | **MAY** | Human-readable preview. |
| `ro-crate-datasheet.html` | **MUST** | Datasheet-for-Datasets rendering of the release. |
| `ro-crate-prov-graph.json` | **SHOULD** | Evidence graph (EVI). |
| `ro-crate-prov-graph.html` | **SHOULD** | HTML visualization of the evidence graph. |
| `ro-crate-croissant.json` | **SHOULD** | Croissant / Croissant-RAI 1.0 export of dataset entities. |
| `ro-crate-merkle-tree.json` | **MAY** | SHA-256 Merkle tree for content integrity. |
| `ro-crate-linkml.yaml` | **MAY** | LinkML schema derived from the crate's per-entity `dataSchema` declarations. |

These cardinalities describe what `fairscape-cli` emits today and what consumers of a release can rely on. v0.2 does not enforce file presence in code; conformance to §2 is the binding requirement.

---

## 4. Required entity properties

Every property's required/optional status below is sourced directly from the [Pydantic models](https://github.com/fairscape/fairscape_models) — `is_required()` on each `FieldInfo` is the authoritative source. Each section lists the JSON-LD keys (aliases) as they appear in `ro-crate-metadata.json`. All entities additionally carry `@id` and `@type`, which are always required.

### 4.1 ROCrateMetadataElem (Root Data Entity)

The Root Data Entity has many optional Croissant-RAI and Datasheet-for-Datasets descriptors; only the required ones are listed here. The full schema is in [`schemas/ROCrateV1_2.json`](/profile/0.2/schemas/).

**Required:**
- `@type` — list including `"Dataset"` and `"https://w3id.org/EVI#ROCrate"`
- `conformsTo` — value must include `{"@id": "https://w3id.org/fairscape/profile/0.2"}`
- `name`, `description`, `keywords`, `version`, `hasPart`, `author`, `license`

**Optional:** `publisher`, `funder`, `identifier`, `rai:*`, `d4d:*`, `evi:*Count`, … See [`schemas/ROCrateV1_2.json`](/profile/0.2/schemas/) for the complete list with descriptions.

### 4.2 Dataset

- **Required:** `name`, `author`, `description`, `keywords`, `datePublished`, `format`
- **Optional:** `version`, `contentUrl`, `dataSchema`, `generatedBy`, `derivedFrom`, `usedByComputation`, `md5`, `sha256`, `prov:*`, …

### 4.3 Software

- **Required:** `name`, `author`, `description`, `format`
- **Optional:** `version`, `contentUrl`, `usedByComputation`, `md5`, `sha256`, `dateModified`, `prov:*`, …

### 4.4 MLModel

- **Required:** `name`, `author`, `description`, `format`
- **Optional:** `version`, `modelTask`, `modelArchitecture`, `trainedOn`, `contentUrl`, `usedByComputation`, `md5`, `sha256`, `prov:*`, …

### 4.5 Computation

- **Required:** `name`, `description`, `runBy`, `dateCreated`
- **Optional:** `command`, `usedSoftware`, `usedMLModel`, `usedDataset`, `generated`, `prov:used`, `prov:wasAssociatedWith`, …

### 4.6 Annotation

- **Required:** `name`, `description`, `createdBy`, `dateCreated`
- **Optional:** `usedDataset`, `generated`, `prov:used`, `prov:wasAssociatedWith`, …

### 4.7 Experiment

- **Required:** `name`, `description`, `experimentType`, `runBy`, `datePerformed`
- **Optional:** `protocol`, `usedInstrument`, `usedSample`, `usedTreatment`, `usedStain`, …

### 4.8 Schema

- **Required:** `name`, `description`, `properties`
- **Optional:** `type`, `required`, `separator`, `header`, `examples`, `additionalProperties`, …

### 4.9 Sample

- **Required:** `name`, `author`, `description`, `keywords`
- **Optional:** `contentUrl`, `cellLineReference`, `isPartOf`

### 4.10 Instrument

- **Required:** `name`, `manufacturer`, `model`, `description`
- **Optional:** `usedByExperiment`, `associatedPublication`, `contentUrl`, …

### 4.11 Patient

- **Required:** `name`, `sdPublisher`, `gender`
- **Optional:** `diagnosis`, `drug`, `healthCondition`, `birthDate`, `deathDate`

### 4.12 ModelCard

- **Required:** `name`, `author`, `description`, `version`, `keywords`
- **Optional:** `modelType`, `framework`, `modelFormat`, `trainingDataset`, `parameters`, `inputSize`, `hasBias`, `intendedUseCase`, `baseModel`, `license`, …

---

## 5. Validation rules

The SHACL shapes have two layers. The full, generated listing is on the [Validation rules](/profile/0.2/validation/) page.

**Per-class structure.** There is one node shape per entity type (`evi:Dataset`, `evi:Software`, `evi:Computation`, …), generated from the same Pydantic models as §4 and the [JSON Schemas](/profile/0.2/schemas/). They check cardinality, datatypes, and minimum lengths.

**Graph rules.** These are hand-authored and check how entities link to each other:

| Rule | Severity |
|---|---|
| Reference edges point at a node of the right type (table below) | Violation |
| Every `Dataset` names an `author` (a string or an `@id` reference) | Violation |
| `ark:` references resolve to a node described in the crate | Warning |
| ARK identifiers are well-formed (`ark:NNNNN/name`, no spaces or commas) | Warning |

Reference edge typing:

| Edge (on any entity) | Target **MUST** be |
|---|---|
| `generatedBy` | an Activity: `Computation`, `Experiment`, or `prov:Activity` |
| `generated`, `derivedFrom` | **not** an Activity: the data entity, never the process |
| `usedSoftware` | `Software` |
| `usedDataset`, `trainedOn` | `Dataset` |
| `usedMLModel` | `MLModel` |
| `usedInstrument` | `Instrument` |
| `usedSample` | `Sample` |
| `usedByComputation` | `Computation` |
| `usedByExperiment` | `Experiment` |
| `dataSchema` | `Schema` |

Edge typing applies only when the target is described (has an `@type`) in the same crate. References into sibling crates of a multi-crate release are not type-checked; they surface through the `ark:` reference warning instead. Each edge is matched under both its `schema:` and `evi:` expansions, since both occur depending on a crate's `@context`.

---

## 6. References

- W3C Profiles Vocabulary (PROF): <https://www.w3.org/TR/dx-prof/>
- RO-Crate 1.2: <https://www.researchobject.org/ro-crate/specification/1.2/>
- SHACL: <https://www.w3.org/TR/shacl/>
- RO-Crate 1.2 Profiles section: <https://www.researchobject.org/ro-crate/specification/1.2/profiles.html>
- EVI Ontology: <https://w3id.org/EVI>
- Croissant 1.0 / Croissant-RAI: <http://mlcommons.org/croissant/>
- PROV-O: <https://www.w3.org/TR/prov-o/>
- RFC 2119: <https://www.rfc-editor.org/rfc/rfc2119>
