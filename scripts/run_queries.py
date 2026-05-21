#!/usr/bin/env python3
"""
run_queries.py

Executes SPARQL queries from queries/analytical.sparql against the
RDF dataset and outputs results as formatted tables.

Usage:
    python scripts/run_queries.py              # run all queries
    python scripts/run_queries.py --query Q4   # run specific query
    python scripts/run_queries.py --json       # output as JSON
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from rdflib import Dataset, URIRef
    from pyld import jsonld
except ImportError:
    print("Install: pip install rdflib pyld --break-system-packages")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CONTEXT_DIR = ROOT / "context"
QUERY_FILE = ROOT / "queries" / "analytical.sparql"


def load_dataset() -> Dataset:
    """Load the full RDF dataset from JSON-LD source files."""
    ds = Dataset()
    
    for sd in sorted(DATA.iterdir()):
        if not sd.is_dir():
            continue
        
        season_file = sd / "season.json"
        if not season_file.exists():
            continue
        
        with open(season_file) as f:
            doc = json.load(f)
        
        sn = doc.get("season_number", 0)
        
        # Load season context
        with open(CONTEXT_DIR / "season.jsonld") as f:
            ctx = json.load(f)["@context"]
        
        doc_copy = dict(doc)
        doc_copy["@context"] = ctx
        
        try:
            nquads = jsonld.to_rdf(doc_copy, {"format": "application/n-quads"})
            g = ds.graph(URIRef(f"https://survivor-kg.github.io/graph/season/{sn}"))
            g.parse(data=nquads, format="nquads")
        except Exception:
            pass
        
        # Load episodes
        with open(CONTEXT_DIR / "episode.jsonld") as f:
            ep_ctx = json.load(f)["@context"]
        
        for ef in sorted(sd.glob("e*.json")):
            with open(ef) as f:
                ep_doc = json.load(f)
            ep_num = ep_doc.get("episode_number", 0)
            ep_doc_copy = dict(ep_doc)
            ep_doc_copy["@context"] = ep_ctx
            try:
                nq = jsonld.to_rdf(ep_doc_copy, {"format": "application/n-quads"})
                eg = ds.graph(URIRef(
                    f"https://survivor-kg.github.io/graph/season/{sn}/episode/{ep_num}"
                ))
                eg.parse(data=nq, format="nquads")
            except Exception:
                pass
    
    return ds


def parse_queries(filepath: Path) -> dict:
    """Parse the SPARQL query file into named queries."""
    content = filepath.read_text()
    queries = {}
    
    # Split on --- separator
    blocks = content.split("\n---\n")
    
    for block in blocks:
        # Find query name (## Q\d+: ...)
        name_match = re.search(r"## (Q\d+): (.+)", block)
        if not name_match:
            continue
        
        qid = name_match.group(1)
        qdesc = name_match.group(2).strip()
        
        # Extract the SPARQL query (starts with SELECT/ASK/CONSTRUCT)
        sparql_match = re.search(
            r"((?:PREFIX[^\n]+\n)*\s*SELECT.+?)(?:\n\n|\n#|\Z)",
            block, re.DOTALL
        )
        if not sparql_match:
            continue
        
        sparql = sparql_match.group(1).strip()
        
        # Add common prefixes if missing
        prefixes = """PREFIX surv: <https://survivor-kg.github.io/ontology/survivor#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX schema: <https://schema.org/>
"""
        if "PREFIX" not in sparql:
            sparql = prefixes + sparql
        
        queries[qid] = {"description": qdesc, "sparql": sparql}
    
    return queries


def run_query(ds: Dataset, qid: str, qdata: dict, as_json: bool = False):
    """Execute a single SPARQL query and print results."""
    print(f"\n{'='*60}")
    print(f"  {qid}: {qdata['description']}")
    print(f"{'='*60}")
    
    try:
        results = list(ds.query(qdata["sparql"]))
    except Exception as e:
        print(f"  Error: {e}")
        return
    
    if not results:
        print("  (no results)")
        return
    
    if as_json:
        rows = []
        for row in results:
            rows.append([str(v) if v else None for v in row])
        print(json.dumps(rows, indent=2))
    else:
        # Format as table
        for row in results[:25]:
            values = [str(v) if v else "?" for v in row]
            print(f"  {' | '.join(values)}")
        if len(results) > 25:
            print(f"  ... ({len(results)} total rows)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", help="Run specific query (e.g., Q4)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--list", action="store_true", help="List queries")
    args = parser.parse_args()
    
    queries = parse_queries(QUERY_FILE)
    
    if args.list:
        for qid, qdata in sorted(queries.items()):
            print(f"  {qid}: {qdata['description']}")
        return
    
    print("Loading RDF dataset...")
    ds = load_dataset()
    n_graphs = sum(1 for _ in ds.graphs())
    print(f"Loaded {n_graphs} graphs")
    
    if args.query:
        if args.query in queries:
            run_query(ds, args.query, queries[args.query], args.json)
        else:
            print(f"Query {args.query} not found. Available: {list(queries.keys())}")
    else:
        for qid, qdata in sorted(queries.items()):
            run_query(ds, qid, qdata, args.json)


if __name__ == "__main__":
    main()
