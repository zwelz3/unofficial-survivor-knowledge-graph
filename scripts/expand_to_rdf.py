#!/usr/bin/env python3
"""
expand_to_rdf.py

Reads the generated JSON data tree, expands each file via its JSON-LD
context into RDF triples, and stores them in an rdflib Dataset where
each season and episode occupies a named graph.

Named graph URIs follow the pattern:
  - Season:  https://survivor-kg.github.io/graph/season/{num}
  - Episode: https://survivor-kg.github.io/graph/season/{num}/episode/{ep}

The Dataset can be serialized to TriG (default), N-Quads, or individual
Turtle files per graph.
"""

import json
import sys
from pathlib import Path

try:
    from rdflib import Dataset, Graph, URIRef, Namespace
    from pyld import jsonld
except ImportError:
    print("Install dependencies:  pip install rdflib pyld --break-system-packages")
    sys.exit(1)

# ── configuration ────────────────────────────────────────────────────
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CONTEXT_DIR = Path(__file__).resolve().parent.parent / "context"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

SURV = Namespace("https://survivor-kg.github.io/ontology/survivor#")
GRAPH_BASE = "https://survivor-kg.github.io/graph"


def load_context(name: str) -> dict:
    """Load a JSON-LD context file and return its @context dict."""
    path = CONTEXT_DIR / name
    with open(path) as f:
        doc = json.load(f)
    return doc.get("@context", doc)


def resolve_context_in_doc(doc: dict, context_filename: str) -> dict:
    """Replace the relative @context path with the actual context dict.
    
    Also strips underscore-prefixed metadata keys (e.g., _provenance)
    which are data-about-data and should not expand into RDF triples.
    """
    ctx = load_context(context_filename)
    doc_copy = {k: v for k, v in doc.items() if not k.startswith("_")}
    doc_copy["@context"] = ctx
    return doc_copy


def json_to_nquads(doc: dict) -> str:
    """Expand a JSON-LD document to N-Quads using pyld."""
    return jsonld.to_rdf(doc, {"format": "application/n-quads"})


def ingest_season(ds: Dataset, season_dir: Path) -> int:
    """Ingest season.json and all e*.json from a season directory."""
    triple_count = 0

    # ── season graph ─────────────────────────────────────────────────
    season_file = season_dir / "season.json"
    if not season_file.exists():
        return 0

    with open(season_file) as f:
        season_doc = json.load(f)

    season_num = season_doc.get("season_number", 0)
    season_graph_uri = URIRef(f"{GRAPH_BASE}/season/{season_num}")

    resolved = resolve_context_in_doc(season_doc, "season.jsonld")

    try:
        nquads = json_to_nquads(resolved)
        g = ds.graph(season_graph_uri)
        g.parse(data=nquads, format="nquads")
        triple_count += len(g)
    except Exception as e:
        print(f"  [!] Season {season_num} expansion error: {e}")

    # ── episode graphs ───────────────────────────────────────────────
    ep_files = sorted(season_dir.glob("e*.json"))
    for ep_file in ep_files:
        with open(ep_file) as f:
            ep_doc = json.load(f)

        ep_num = ep_doc.get("episode_number", 0)
        ep_graph_uri = URIRef(
            f"{GRAPH_BASE}/season/{season_num}/episode/{ep_num}"
        )

        resolved_ep = resolve_context_in_doc(ep_doc, "episode.jsonld")

        try:
            nquads_ep = json_to_nquads(resolved_ep)
            eg = ds.graph(ep_graph_uri)
            eg.parse(data=nquads_ep, format="nquads")
            triple_count += len(eg)
        except Exception as e:
            print(f"  [!] S{season_num}E{ep_num} expansion error: {e}")

    return triple_count


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    ds = Dataset()
    ds.bind("surv", SURV)
    ds.bind("schema", "https://schema.org/")
    ds.bind("prov", "http://www.w3.org/ns/prov#")
    ds.bind("foaf", "http://xmlns.com/foaf/0.1/")
    ds.bind("dct", "http://purl.org/dc/terms/")

    total_triples = 0
    season_dirs = sorted(DATA_DIR.iterdir())

    for sd in season_dirs:
        if not sd.is_dir():
            continue
        count = ingest_season(ds, sd)
        print(f"  [+] {sd.name}: {count} triples")
        total_triples += count

    # ── serialize ────────────────────────────────────────────────────
    trig_path = OUTPUT_DIR / "survivor.trig"
    ds.serialize(destination=str(trig_path), format="trig")
    print(f"\nSerialized {total_triples} triples to {trig_path}")

    nq_path = OUTPUT_DIR / "survivor.nq"
    ds.serialize(destination=str(nq_path), format="nquads")
    print(f"Serialized to {nq_path}")

    # ── per-season turtle ────────────────────────────────────────────
    turtle_dir = OUTPUT_DIR / "turtle"
    turtle_dir.mkdir(exist_ok=True)
    for ctx in ds.contexts():
        ctx_id = str(ctx.identifier)
        if ctx_id == "urn:x-rdflib:default":
            continue
        slug = ctx_id.replace(GRAPH_BASE + "/", "").replace("/", "-")
        ttl_path = turtle_dir / f"{slug}.ttl"
        ctx.serialize(destination=str(ttl_path), format="turtle")

    print(f"Per-graph Turtle files in {turtle_dir}/")

    # ── summary stats ────────────────────────────────────────────────
    n_graphs = sum(1 for c in ds.contexts()
                   if str(c.identifier) != "urn:x-rdflib:default")
    print(f"\nDataset summary: {n_graphs} named graphs, "
          f"{total_triples} total triples")


if __name__ == "__main__":
    main()
