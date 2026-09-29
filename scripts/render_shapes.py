#!/usr/bin/env python3
"""Render a profile version's SHACL shapes as a Starlight page.

Usage:
    python scripts/render_shapes.py 0.2

Reads profile/<version>/fairscape-shapes.ttl and writes
site/src/content/docs/<version>/validation.md. Needs rdflib. Re-run it whenever
the shapes file changes; the page is generated, so don't edit it by hand.
"""

import re
import sys
import textwrap
from pathlib import Path

from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import RDF, RDFS

SH = Namespace("http://www.w3.org/ns/shacl#")
FSH = Namespace("https://w3id.org/EVI/shapes#")

ROOT = Path(__file__).resolve().parent.parent

# Graph rules are the hand-authored shapes; they are the ones that set an
# explicit sh:severity. The per-class shapes are generated from fairscape_models.
EDGE_MESSAGE = re.compile(
    r"^(?P<edges>.+?) on \{\?subj\} points to \{\?value\}, described here but not an? (?P<expected>.+?)\.$"
)
NOT_ACTIVITY_MESSAGE = re.compile(r"^(?P<edges>.+?) on \{\?subj\} points to \{\?value\}, which is an Activity")


def curie(g: Graph, node) -> str:
    if isinstance(node, URIRef):
        try:
            return g.namespace_manager.normalizeUri(node)
        except Exception:
            return str(node)
    return str(node)


def first(g: Graph, s, p):
    return next(g.objects(s, p), None)


def sparql(text: str) -> str:
    head, _, rest = text.strip("\n").partition("\n")
    return (head.strip() + ("\n" + textwrap.dedent(rest) if rest else "")).rstrip()


def cell(text) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def value_type(g: Graph, prop) -> str:
    parts = []
    dt = first(g, prop, SH.datatype)
    if dt is not None:
        parts.append(f"`{curie(g, dt)}`")
    cls = first(g, prop, SH["class"])
    if cls is not None:
        parts.append(f"→ `{curie(g, cls)}`")
    nk = first(g, prop, SH.nodeKind)
    if nk is not None:
        parts.append({SH.IRI: "`@id` reference", SH.Literal: "literal"}.get(nk, curie(g, nk)))
    alts = first(g, prop, SH["or"])
    if alts is not None:
        parts.append(" or ".join(value_type(g, a) for a in Collection(g, alts)))
    return ", ".join(p for p in parts if p) or "any"


def extras(g: Graph, prop) -> str:
    out = []
    for pred, label in ((SH.minLength, "min length"), (SH.maxLength, "max length"),
                        (SH.minInclusive, "≥"), (SH.maxInclusive, "≤")):
        v = first(g, prop, pred)
        if v is not None:
            out.append(f"{label} {v}")
    pat = first(g, prop, SH.pattern)
    if pat is not None:
        out.append(f"pattern `{pat}`")
    allowed = first(g, prop, SH["in"])
    if allowed is not None:
        out.append("one of " + ", ".join(f"`{v}`" for v in Collection(g, allowed)))
    return "; ".join(out)


def class_table(g: Graph, shape) -> list[str]:
    rows = []
    for prop in g.objects(shape, SH.property):
        path = first(g, prop, SH.path)
        name = first(g, prop, SH.name) or curie(g, path)
        min_c = int(first(g, prop, SH.minCount) or 0)
        max_c = first(g, prop, SH.maxCount)
        card = f"{'1' if min_c else '0'}..{'1' if max_c is not None and int(max_c) == 1 else '*'}"
        desc = first(g, prop, SH.description) or ""
        rows.append((min_c == 0, str(name).lower(), [
            f"`{name}`", f"`{curie(g, path)}`", "**required**" if min_c else "optional",
            card, value_type(g, prop), cell(extras(g, prop)), cell(desc),
        ]))
    rows.sort(key=lambda r: (r[0], r[1]))
    lines = ["| Property | Path | Status | Card. | Value | Constraints | Description |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    lines += ["| " + " | ".join(r[2]) + " |" for r in rows]
    return lines


def rule_section(g: Graph, shape) -> list[str]:
    label = first(g, shape, RDFS.label)
    severity = first(g, shape, SH.severity)
    sev = "Violation — fails conformance" if severity == SH.Violation else "Warning — reported, crate still conforms"
    target = first(g, shape, SH.targetClass)
    scope = f"every `{curie(g, target)}` node" if target is not None else "the whole graph, once"
    out = [f"### {label}", "", f"**Severity:** {sev} · **Applies to:** {scope} · **Shape:** `{curie(g, shape)}`", ""]

    edge_rows, other = [], []
    queries = []
    for c in g.objects(shape, SH.sparql):
        msg = str(first(g, c, SH.message) or "")
        m = EDGE_MESSAGE.match(msg) or NOT_ACTIVITY_MESSAGE.match(msg)
        if m:
            edges = ", ".join(f"`{e.strip()}`" for e in m["edges"].split("/"))
            expected = m.groupdict().get("expected") or "not an Activity — the data entity, never the process"
            edge_rows.append((m["edges"], f"| {edges} | {cell(expected)} |"))
        else:
            other.append(msg)
        queries.append((msg, sparql(str(first(g, c, SH.select) or ""))))
    for p in g.objects(shape, SH.property):
        other.append(str(first(g, p, SH.message) or ""))

    if edge_rows:
        out += ["| Edge | Target, when described in this crate, must be |", "| --- | --- |"]
        out += [r for _, r in sorted(edge_rows)]
        out.append("")
    for msg in sorted(other):
        text = msg.replace("{?subj}", "*X*").replace("{?value}", "*Y*").replace("{?n}", "*N*")
        out.append(f"- {text}")
    if other:
        out.append("")
    if queries:
        out += ["<details>", "<summary>SPARQL</summary>", ""]
        for msg, q in sorted(queries):
            out += ["```sparql", q, "```", ""]
        out += ["</details>", ""]
    return out


def main() -> None:
    version = sys.argv[1] if len(sys.argv) > 1 else "0.2"
    ttl = ROOT / "profile" / version / "fairscape-shapes.ttl"
    dest = ROOT / "site" / "src" / "content" / "docs" / version / "validation.md"

    g = Graph()
    g.parse(ttl)
    g.bind("fsh", FSH, replace=True)

    # Keep the order the shapes are written in.
    text = ttl.read_text()
    def file_order(shape):
        return text.find(f"{curie(g, shape)} a sh:NodeShape")

    shapes = sorted(g.subjects(RDF.type, SH.NodeShape), key=file_order)
    rules = [s for s in shapes if (s, SH.severity, None) in g]
    classes = [s for s in shapes if s not in rules]
    shapes_version = first(g, URIRef(str(FSH)), URIRef("http://www.w3.org/2002/07/owl#versionInfo"))

    out = [
        "---",
        f'title: "Validation rules (v{version})"',
        'description: "The SHACL shapes a Fairscape release crate is checked against: graph rules and per-class structure."',
        "template: doc",
        f'slug: "{version}/validation"',
        "tableOfContents:",
        "  minHeadingLevel: 2",
        "  maxHeadingLevel: 3",
        "---",
        "",
        f"<!-- Generated by scripts/render_shapes.py from profile/{version}/fairscape-shapes.ttl. Do not edit by hand. -->",
        "",
        f"The profile's machine-checkable rules are published as SHACL: [`fairscape-shapes.ttl`](/profile/{version}/fairscape-shapes.ttl) "
        f"(shapes version {shapes_version}). Run them with:",
        "",
        "```bash",
        "pip install 'fairscape-models[shacl]'",
        "```",
        "",
        "```python",
        "from fairscape_models.validation.shacl import validate_shacl",
        "",
        "report = validate_shacl(\"./my-crate\")  # crate dir, metadata file, dict or ROCrateV1_2",
        "report.passes      # True iff there are no Violations; Warnings are advisory",
        "report.results     # severity, shape, message, focusNode, path",
        "```",
        "",
        "Any SHACL engine (e.g. `pyshacl -s fairscape-shapes.ttl ro-crate-metadata.json`) gives the same results.",
        "",
        "## Graph rules",
        "",
        "These rules check how entities link to each other, which the per-entity JSON Schemas cannot express. "
        "A **Violation** is raised only when this file alone proves the defect. When a flagged reference could "
        "legitimately point into a sibling crate of a release, the rule is a **Warning**. Edge rules match both the "
        "`schema:` and `evi:` expansions of each key, and skip targets that have no `@type` in this crate.",
        "",
    ]
    for s in rules:
        out += rule_section(g, s)

    out += [
        "## Per-class structure",
        "",
        "One shape per entity type, generated from the `fairscape_models` Pydantic classes (the same source as the "
        "[JSON Schemas](../schemas/)). All are open shapes: properties not listed are allowed. "
        "Card. is the allowed number of values (`0..1`, `1..1`, `0..*`, `1..*`).",
        "",
    ]
    for s in classes:
        target = first(g, s, SH.targetClass)
        out += [f"### {first(g, s, RDFS.label)}", "",
                f"Applies to every `{curie(g, target)}` node.", ""]
        out += class_table(g, s)
        out.append("")

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(out).rstrip() + "\n")
    print(f"wrote {dest.relative_to(ROOT)} ({len(rules)} graph rules, {len(classes)} class shapes)")


if __name__ == "__main__":
    main()
