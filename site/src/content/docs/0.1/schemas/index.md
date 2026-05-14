---
title: "FAIRSCAPE Schemas (v0.1)"
description: "JSON Schema definitions for all FAIRSCAPE / EVI profile types."
template: doc
slug: "0.1/schemas"
---


JSON Schema definitions for all FAIRSCAPE / EVI profile types. Each link below points to the raw JSON Schema file, which can be referenced directly via `$ref` or used with any JSON Schema validator.

## Base Models

| Schema | Description |
| --- | --- |
| [FairscapeBaseModel](FairscapeBaseModel.json) | Fairscape base model inherited from Pydantic |
| [FairscapeEVIBaseModel](FairscapeEVIBaseModel.json) | EVI-specific base model |
| [Identifier](Identifier.json) | Identifier base type |
| [IdentifierValue](IdentifierValue.json) | Identifier value wrapper |
| [IdentifierPropertyValue](IdentifierPropertyValue.json) | Identifier as a typed property value |
| [Item](Item.json) | Generic item base |
| [Property](Property.json) | Generic property base |

## Core EVI Types

| Schema | Description |
| --- | --- |
| [Activity](Activity.json) | Base class for Activity types (Computation, Annotation, Experiment) |
| [Computation](Computation.json) | A computational step |
| [Annotation](Annotation.json) | An annotation activity |
| [Experiment](Experiment.json) | An experimental activity |
| [DigitalObject](DigitalObject.json) | Base class for DigitalObject types (Dataset, Software, MLModel) |
| [Dataset](Dataset.json) | Dataset digital object |
| [Software](Software.json) | Software digital object |
| [MLModel](MLModel.json) | Machine learning model digital object |
| [Schema](Schema.json) | Schema describing a Dataset's structure |
| [Instrument](Instrument.json) | Instrument used in an Activity |
| [Sample](Sample.json) | Sample / specimen |

## RO-Crate

| Schema | Description |
| --- | --- |
| [ROCrateV1_2](ROCrateV1_2.json) | Full RO-Crate v1.2 metadata document |
| [ROCrateMetadataElem](ROCrateMetadataElem.json) | Metadata element representing the crate as a whole |
| [ROCrateMetadataFileElem](ROCrateMetadataFileElem.json) | Element corresponding to the `ro-crate-metadata.json` file itself |
| [ROCrateDistribution](ROCrateDistribution.json) | Distribution metadata for an RO-Crate |
| [GenericMetadataElem](GenericMetadataElem.json) | Generic metadata element of an RO-Crate |

## ML / LLM Annotations

| Schema | Description |
| --- | --- |
| [AnnotatedComputation](AnnotatedComputation.json) | LLM-generated annotation of a single `evi:Computation` step |
| [AnnotatedEvidenceGraph](AnnotatedEvidenceGraph.json) | Full annotated condensed evidence graph (graph-level LLM output) |
| [CodeAnalysis](CodeAnalysis.json) | Analysis of a software entity used in the computation |
| [DatasetSummary](DatasetSummary.json) | Summary of a dataset's role in the computation |
| [ModelCard](ModelCard.json) | Model Card for ML models as RO-Crate Dataset elements |
| [Split](Split.json) | A named partition or subset of a Dataset |

## Schema.org Types

| Schema | Description |
| --- | --- |
| [BioChemEntity](BioChemEntity.json) | Schema.org BioChemEntity datatype |
| [MedicalCondition](MedicalCondition.json) | Schema.org MedicalCondition datatype |
| [Patient](Patient.json) | Patient record |
| [ContactPoint](ContactPoint.json) | Schema.org ContactPoint for structured contact information |
| [PostalAddress](PostalAddress.json) | Schema.org PostalAddress for structured address information |
| [IRB](IRB.json) | Institutional Review Board with structured contact and address info |
