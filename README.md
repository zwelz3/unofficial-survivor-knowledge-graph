# Survivor Knowledge Graph

![](static/img/banner.png)


A comprehensive RDF knowledge graph covering all 50 seasons of Survivor (US), with 23,000+ triples across 749 named graphs. Includes per-episode challenge results, tribal council votes, idol tracking (233 events), viewership data, and returning player identity resolution. Built on OWL/SKOS/PROV-O with SHACL validation, SPARQL query library, and an interactive d3 graph viewer.

## Dataset coverage (v0.6.0)

| Metric | Coverage |
|---|---|
| Seasons | 50/50 (100%) |
| Episode titles | 692/699 (99.0%) |
| Air dates | 698/699 (99.9%) |
| Viewership | 686/699 (98.1%) |
| Notable events | 674/699 (96.4%) |
| Tribal councils | 665/699 (95.1%) |
| Detailed episodes | 662/699 (94.7%) |
| Challenges (any) | 656/699 (93.8%) |
| Immunity | 638/699 (91.3%) |
| Reward | 532/699 (76.1%) |
| Idol events | 233 events, 14 types, S11-S50 |
| Boot orders | 49/50 (98%) |
| Contestants | 728 unique, 98 returning |
| RDF triples | 23,401 |
| Tests | 49/49 passing |

## Quick start

```bash
pip install rdflib pyld pyshacl pytest

python scripts/build_static.py    # build consolidated outputs in static/
python -m pytest tests/ -v        # run 49 tests
```

## Static distribution

`python scripts/build_static.py` produces a ready-to-use bundle in `static/`:

| File | Description | Size |
|---|---|---|
| `survivor.nq` | Full dataset as N-Quads (23,401 triples, 749 named graphs) | ~5 MB |
| `survivor.ttl` | OWL ontology (v0.5.0, 17 classes, 40+ properties) | ~25 KB |
| `survivor-shapes.ttl` | SHACL validation shapes (26 node shapes) | ~19 KB |
| `graph.json` | LPG export for visualization (seasons, tribes, idols, players) | ~812 KB |
| `index.html` | Interactive dashboard (Chart.js + d3 force graph) | ~267 KB |

These files are also available as build artifacts from the [GitHub Actions CI](../../actions).

## Repository structure

```
context/          JSON-LD contexts (season, episode, provenance)
ontology/         OWL ontology (survivor.ttl) + DCAT dataset (dataset.ttl)
shapes/           SHACL shapes with tiered validation (26 shapes)
data/             50 season dirs, each with season.json + e01..eNN.json
  persons.json    Cross-season identity registry (98 returning players)
  graph.json      LPG export for visualization
queries/          SPARQL analytical query library (22 queries)
scripts/          Data generation, RDF expansion, enrichment, graph extraction, static build
research/         Provenance records (PROV-O JSON-LD, 50 per-season + 699 per-episode)
tests/            pytest suite (49 tests: structure, data, RDF, SPARQL, provenance, idols)
docs/             Dashboard, instructions, roadmap
static/           Built distribution files (N-Quads, ontology, shapes, graph, dashboard)
.github/          CI workflow (test, build artifacts, GitHub Pages deploy)
```

## Ontology

The ontology (v0.5.0) provides 17 OWL classes and 40+ properties aligned with:

- **schema.org**: Season/Episode/Contestant map to TVSeason/TVEpisode/Person (18 alignments)
- **SKOS**: 4 concept schemes (Era, EliminationMethod, ChallengeType, IdolEventType)
- **PROV-O**: Season/Episode/Contestant as prov:Entity subclasses
- **FOAF**: contestant names via foaf:name
- **DCAT/VoID**: dataset-level metadata in ontology/dataset.ttl

SHACL validation includes 26 node shapes with tiered constraints (Tier 1: title/date; Tier 2: elimination; Tier 3: challenges/votes/events) plus idol-specific and era-specific shapes.

## Idol tracking

233 idol events across 14 types, covering the full evolution from S11 Guatemala (first idol, 2005) through S50:

- 108 idol finds, 95 idol plays, 9 idols not played, 8 beware idols
- Fake idols, idol nullifiers, Knowledge Is Power, idol theft
- 6 dedicated SPARQL queries (Q17-Q22)
- IdolEventTypeScheme SKOS vocabulary with 11 concepts

## SPARQL queries

22 analytical queries in `queries/analytical.sparql` across 7 categories: data quality (Q1-Q3), winners/FTC (Q4-Q7), episodes (Q8-Q12), cross-graph joins (Q13-Q14), networks (Q15-Q16), idol analysis (Q17-Q22).

## Dashboard

Interactive dashboard deployed to GitHub Pages with 6 tabs: Overview, Seasons, Players, Idols, Graph Explorer, Data Quality.

The graph explorer supports 8 toggleable node types (seasons, players, tribes, idols, locations, mechanics, winners, episodes) with click-to-inspect, episode drill-down, and d3 force simulation.

```bash
python scripts/build_static.py
cd static && python3 -m http.server 8000
# open http://localhost:8000
```

## Data provenance

All enrichment sources tracked via PROV-O in `research/provenance/`. 12 canonical sources with per-field attribution across 50 season records and 699 episode records. Enrichment chain tracks 8 phases from initial generation (8,266 triples) to current state (23,401 triples).

## Contributing

See [docs/instructions.md](docs/instructions.md) for the research pipeline. See [CHANGELOG.md](CHANGELOG.md) for version history.

## License

Data compiled from public sources. Ontology and tooling: MIT.
