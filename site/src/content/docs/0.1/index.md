---
title: Fairscape Release RO-Crate Profile v0.1
description: Structural and semantic constraints that an RO-Crate must satisfy to be considered a Fairscape release.
template: doc
slug: "0.1"
tableOfContents:
  minHeadingLevel: 2
  maxHeadingLevel: 3
---

**Profile URI:** `https://w3id.org/fairscape/profile/0.1`
**Status:** Stable

This document specifies the **Fairscape Release RO-Crate Profile**: the structural and semantic constraints that an RO-Crate must satisfy to be considered a Fairscape release. The profile is identified by the URI `https://w3id.org/fairscape/profile/0.1` and is published as a W3C PROF-conformant Profile Crate.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).

---

## 1. Overview

A Fairscape Release Crate is an [RO-Crate 1.2](https://www.researchobject.org/ro-crate/specification/1.2/) packaging a versioned, AI-ready research dataset together with provenance, schema, and machine-learning-readiness metadata. The profile constrains and extends:

- **[RO-Crate 1.2](https://w3id.org/ro/crate/1.2)** — base packaging and metadata layout.
- **[EVI Ontology](https://w3id.org/EVI)** — domain classes (`Dataset`, `Software`, `MLModel`, `Computation`, `Annotation`, `Experiment`, …) and properties.
- **[PROV-O](http://www.w3.org/ns/prov)** — `prov:used`, `prov:wasGeneratedBy`, `prov:wasAttributedTo`, etc.
- **[Schema.org](https://schema.org/)** — core types (`Person`, `Organization`, `Dataset`) and properties (`author`, `license`, `keywords`, `hasPart`, …).
- **[Croissant / Croissant-RAI 1.0](http://mlcommons.org/croissant/1.0)** — machine-learning crosswalk emitted alongside each release.

The constituent artifacts of this profile are described in the [Profile Crate](/profile/0.1/ro-crate-metadata.json) (W3C PROF manifest) and in the Turtle profile manifest at [`fairscape_models/profiles/profile.ttl`](https://github.com/fairscape/fairscape_models/blob/main/profiles/profile.ttl).

---

## 2. Conformance

A crate conforms to this profile if and only if all of the following are true:

1. The crate's `ro-crate-metadata.json` parses as valid JSON-LD per RO-Crate 1.2.
2. The **Root Data Entity** carries a `dct:conformsTo` (`conformsTo` in JSON-LD shorthand) property whose value (or one element thereof) is `{"@id": "https://w3id.org/fairscape/profile/0.1"}`.
3. The Root Data Entity's `@type` list **MUST** include `"Dataset"` and `"https://w3id.org/EVI#ROCrate"`.
4. The Metadata Descriptor (the entity with `@id: ro-crate-metadata.json`) carries a `conformsTo` of `{"@id": "https://w3id.org/ro/crate/1.2"}`.
5. Every required property listed in §4 below is present on its respective entity.

Conformance can be checked by the `fairscape-cli rocrate validate` command, which today performs Pydantic-based structural validation. The validator entry point is pinned at [`rocrate_commands.py:1290`](https://github.com/fairscape/fairscape-cli/blob/8c8e6bcf929dcb72b2ef7cfde6f650704cdd0b51/src/fairscape_cli/commands/rocrate_commands.py#L1290) (permalink to the v0.1 reference commit). Install instructions: <https://fairscape.github.io/fairscape-cli/setup/>.

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
      "conformsTo": { "@id": "https://w3id.org/fairscape/profile/0.1" },
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

These cardinalities describe what `fairscape-cli` emits today and what consumers of a release can rely on. v0.1 does not enforce file presence in code; conformance to §2 is the binding requirement.

---

## 4. Required entity properties

Every property's required/optional status below is sourced directly from the [Pydantic models](https://github.com/fairscape/fairscape_models) — `is_required()` on each `FieldInfo` is the authoritative source. Each section lists the JSON-LD keys (aliases) as they appear in `ro-crate-metadata.json`. All entities additionally carry `@id` and `@type`, which are always required.

### 4.1 ROCrateMetadataElem (Root Data Entity)

The Root Data Entity has many optional Croissant-RAI and Datasheet-for-Datasets descriptors; only the required ones are listed here. The full schema is in [`schemas/ROCrateV1_2.json`](/profile/0.1/schemas/).

**Required:**
- `@type` — list including `"Dataset"` and `"https://w3id.org/EVI#ROCrate"`
- `conformsTo` — value must include `{"@id": "https://w3id.org/fairscape/profile/0.1"}`
- `name`, `description`, `keywords`, `version`, `hasPart`, `author`, `license`

**Optional:** `publisher`, `funder`, `identifier`, `rai:*`, `d4d:*`, `evi:*Count`, … See [`schemas/ROCrateV1_2.json`](/profile/0.1/schemas/) for the complete list with descriptions.

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

## 5. References

- W3C Profiles Vocabulary (PROF): <https://www.w3.org/TR/dx-prof/>
- RO-Crate 1.2: <https://www.researchobject.org/ro-crate/specification/1.2/>
- RO-Crate 1.2 Profiles section: <https://www.researchobject.org/ro-crate/specification/1.2/profiles.html>
- EVI Ontology: <https://w3id.org/EVI>
- Croissant 1.0 / Croissant-RAI: <http://mlcommons.org/croissant/>
- PROV-O: <https://www.w3.org/TR/prov-o/>
- RFC 2119: <https://www.rfc-editor.org/rfc/rfc2119>
