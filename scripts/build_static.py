#!/usr/bin/env python3
"""
build_static.py

Produces the static distribution bundle in static/:

  static/
    survivor.nq          – Full dataset as N-Quads (all named graphs)
    survivor.ttl          – OWL ontology (single file)
    survivor-shapes.ttl   – SHACL validation shapes (single file)
    graph.json            – LPG export for visualization
    index.html            – Interactive dashboard

Run:  python scripts/build_static.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "static"
OUTPUT = ROOT / "output"
SCRIPTS = ROOT / "scripts"


def run(script_name, label):
    script = SCRIPTS / script_name
    cmd = [sys.executable, str(script)]
    print(f"  [{label}] {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR (stderr): {result.stderr[:500]}")
        print(f"  ERROR (stdout): {result.stdout[:500]}")
        sys.exit(1)
    return result.stdout


def main():
    STATIC.mkdir(exist_ok=True)

    # 1. Expand JSON-LD to RDF (produces output/survivor.nq)
    print("1. Expanding JSON-LD to RDF...")
    out = run("expand_to_rdf.py", "rdf")
    for line in out.strip().split("\n"):
        if "Dataset summary" in line or "Serialized" in line:
            print(f"     {line.strip()}")

    # 2. Copy N-Quads
    nq_src = OUTPUT / "survivor.nq"
    nq_dst = STATIC / "survivor.nq"
    if nq_src.exists():
        shutil.copy2(nq_src, nq_dst)
        size = nq_dst.stat().st_size
        print(f"2. N-Quads:  {nq_dst}  ({size:,} bytes)")
        # Verify the file loads directly into rdflib
        try:
            from rdflib import Dataset as RDFDataset
            ds = RDFDataset()
            ds.parse(str(nq_dst), format="nquads")
            n_graphs = sum(1 for g in ds.graphs()
                          if str(g.identifier) != "urn:x-rdflib:default")
            n_triples = sum(len(g) for g in ds.graphs()
                           if str(g.identifier) != "urn:x-rdflib:default")
            print(f"   Verified: {n_graphs} named graphs, {n_triples} triples load into rdflib")
        except ImportError:
            print("   (rdflib not available for verification; file should still be valid)")
        except Exception as e:
            print(f"   WARNING: verification failed: {e}")
    else:
        print("  ERROR: survivor.nq not found; expand_to_rdf.py may have failed")
        sys.exit(1)

    # 3. Copy ontology
    ont_src = ROOT / "ontology" / "survivor.ttl"
    ont_dst = STATIC / "survivor.ttl"
    shutil.copy2(ont_src, ont_dst)
    print(f"3. Ontology: {ont_dst}  ({ont_dst.stat().st_size:,} bytes)")

    # 4. Copy SHACL shapes
    shp_src = ROOT / "shapes" / "survivor-shapes.ttl"
    shp_dst = STATIC / "survivor-shapes.ttl"
    shutil.copy2(shp_src, shp_dst)
    print(f"4. Shapes:   {shp_dst}  ({shp_dst.stat().st_size:,} bytes)")

    # 5. Extract graph JSON
    print("5. Extracting graph data...")
    run("extract_graph.py", "graph")
    graph_src = ROOT / "data" / "graph.json"
    graph_dst = STATIC / "graph.json"
    shutil.copy2(graph_src, graph_dst)
    print(f"   Graph:    {graph_dst}  ({graph_dst.stat().st_size:,} bytes)")

    # 6. Copy dashboard
    dash_src = ROOT / "docs" / "index.html"
    dash_dst = STATIC / "index.html"
    if dash_src.exists():
        shutil.copy2(dash_src, dash_dst)
        print(f"6. Dashboard:{dash_dst}  ({dash_dst.stat().st_size:,} bytes)")

    # Summary
    print(f"\n{'=' * 50}")
    print(f"Static bundle ready: {STATIC}/")
    total = sum(f.stat().st_size for f in STATIC.iterdir() if f.is_file())
    files = list(STATIC.iterdir())
    for f in sorted(files):
        if f.is_file():
            print(f"  {f.name:<25} {f.stat().st_size:>10,} bytes")
    print(f"  {'TOTAL':<25} {total:>10,} bytes")


if __name__ == "__main__":
    main()
