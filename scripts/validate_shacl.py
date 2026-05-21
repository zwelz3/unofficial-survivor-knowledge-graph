#!/usr/bin/env python3
"""
validate_shacl.py

Runs SHACL validation against the generated RDF dataset using the
shapes defined in shapes/survivor-shapes.ttl.
"""

import sys
from pathlib import Path

try:
    from rdflib import Graph
    from pyshacl import validate
except ImportError:
    print("Install: pip install rdflib pyshacl --break-system-packages")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent

def main():
    shapes_path = ROOT / "shapes" / "survivor-shapes.ttl"
    trig_path = ROOT / "output" / "survivor.trig"

    if not trig_path.exists():
        print("No output/survivor.trig found. Run 'make expand' first.")
        sys.exit(1)

    data_graph = Graph()
    data_graph.parse(str(trig_path), format="trig")
    print(f"Loaded {len(data_graph)} triples from {trig_path}")

    shapes_graph = Graph()
    shapes_graph.parse(str(shapes_path), format="turtle")
    print(f"Loaded {len(shapes_graph)} shape triples")

    conforms, results_graph, results_text = validate(
        data_graph,
        shacl_graph=shapes_graph,
        inference="none",
        abort_on_first=False,
    )

    print(f"\nConforms: {conforms}")
    if not conforms:
        print("\nValidation issues:")
        print(results_text[:3000])
    else:
        print("All SHACL shapes pass.")

    return 0 if conforms else 1


if __name__ == "__main__":
    sys.exit(main())
