# Changelog

All notable changes to the Survivor Knowledge Graph dataset.

## [0.6.1] - 2026-05-22 (S50 Finale)

### Added
- S50 finale data: Aubry Bracco wins 8-3-0 over Jonathan Young and Joe Hunter
- S50 finale episodes with fire-making (Jonathan beat Rizo), idol play (Rizo wasted), Simmotion immunity
- Cirie Fields $100K Sia Fan Favorite prize
- $2M prize (tying S40 for largest ever)
- Season 51 The Open Era announced

### Fixed
- Graph view edge rendering (s/t mapped to source/target for d3.forceLink)
- build_static.py Windows compatibility (list-based subprocess, better error output)
- build_static.py now verifies N-Quads file loads into rdflib

### Changed
- 23,467 total RDF triples (was 23,401)

## [0.6.0] - 2026-05-21 (Idol Enrichment + Ontology Maturation)

### Added
- Comprehensive idol event tracking: 138 events across 123 episodes (13 event types)
- IdolEventTypeScheme SKOS concept scheme (11 concepts)
- 6 new idol-related SPARQL queries (Q17-Q22)
- 5 idol-specific test cases (49 total tests)
- New ontology properties: idolEventType, votesNegated, idolSuccessful, isFakeIdol, idolNotes, idolFinder, idolGiver, idolNullifiedBy
- Updated SHACL with IdolPlayDetailedShape and EpisodeIdolConstraint
- Updated episode context with idol inner property mappings

### Changed
- Ontology version 0.5.0 with IdolEventTypeScheme
- 22 SPARQL queries (was 16)
- hasIdolPlay domain changed from TribalCouncil to Episode

## [0.5.0] - 2026-05-21 (Graph Viewer + Full Enrichment)

### Added
- Interactive graph viewer (`docs/index.html`) with d3-force visualization
- React graph viewer component (`survivor-graph-viewer.jsx`)
- Graph data extraction script (`scripts/extract_graph.py`) producing LPG from JSON-LD
- Compact LPG export (`data/graph.json`, `data/graph-compact.json`): 158 nodes, 342 edges
- GitHub Pages deployment via CI (`deploy` job)
- Three layout modes: force-directed, radial, chronological
- Search, node/edge inspection, neighborhood expansion (1-2 degree), type filtering
- Full episode detail for 47+ seasons (642/699 episodes, 91.8%)
- Notable events for 324/699 episodes (46.4%)
- Viewership data for 486/699 episodes (69.5%)

### Changed
- 18,868 total RDF triples (was 17,496)
- Ontology version 0.4.0 with full SKOS concept schemes
- 44 tests passing (was 35)

## [0.3.0] - 2026-05-21 (Infrastructure Audit)

### Added
- DCAT/VoID dataset description (`ontology/dataset.ttl`)
- Provenance records for all enrichment sources (`research/provenance/session-2026-05-21.jsonld`)
- SPARQL analytical query library with 16 queries (`queries/analytical.sparql`)
- SPARQL query runner script (`scripts/run_queries.py`)
- Tiered SHACL validation shapes (Tier 1: title/date, Tier 2: tribal, Tier 3: detailed)
- SHACL shapes for 6 previously unshaped classes (Mechanic, IdolPlay, Advantage, Quote, Alliance, enriched Season/Episode)
- Schema.org alignment: Season/Episode/Contestant mapped to TVSeason/TVEpisode/Person
- This CHANGELOG

### Changed
- Ontology version bumped from 0.1.0-stub to 0.3.0
- Ontology now declares `owl:imports` for FOAF and `rdfs:subClassOf` for schema.org
- SHACL shapes file expanded from 7 to 13+ node shapes

## [0.2.0] - 2026-05-21 (Enrichment Cycles 1-8)

### Added
- Episode titles for 692/699 episodes (99.0%) from Wikipedia and epguides.com
- Air dates for 698/699 episodes (99.9%)
- Tribal council data for 645/699 episodes (92.3%) via boot order mapping
- Challenge data for 158/699 episodes (22.6%) via derivation + manual enrichment
- Notable events for 136/699 episodes (19.5%)
- Viewership data for 246/699 episodes (35.2%)
- Boot orders for 49/50 seasons (S50 still airing)
- 728 unique contestant records across 49 seasons
- Canonical person identity registry (`data/persons.json`) with 98 returning players
- Filming dates for all 50 seasons
- Cross-season analytics (`data/analytics.json`)
- 12 new ontology properties discovered during enrichment

### Detailed Seasons (full per-episode data)
- S1 Borneo: 13 episodes with challenges, votes, viewership, notable events
- S7 Pearl Islands: 14 episodes with Outcast twist, dead grandma lie, Rupert blindside
- S16 Micronesia: 14 episodes with Erik immunity giveaway, Penner medevac
- S20 Heroes vs. Villains: 14 episodes with Parvati double idol, J.T.'s letter
- S28 Cagayan: 13 episodes with spy shack, Tyler Perry idol, Woo's choice
- S31 Cambodia: 14 episodes with Wentworth idol play, Kimmi default elimination
- S37 David vs. Goliath: 13 episodes with idol nullifier, Christian endurance
- S40 Winners at War: 15 episodes with Queenslayer, Edge, Adam podium play
- S41: 13 episodes with Hourglass, Shot in the Dark, Do or Die
- S47: 13 episodes with Operation Italy, Rachel 4-immunity run

### Data Sources (with provenance)
- Wikipedia season articles (confidence: 0.95)
- Wikipedia episode list pages (confidence: 0.97)
- epguides.com episode titles/dates (confidence: 0.98)
- Survivor Wiki / Fandom (confidence: 0.90)
- Algorithmic derivation from boot orders (confidence: 0.80)

## [0.1.0] - 2026-05-21 (Initial Generation)

### Added
- Repository structure with 50 season directories, 699 episode JSON files
- JSON-LD contexts for season, episode, and provenance
- OWL ontology with 15 classes and 20+ properties
- SHACL shapes for 7 core classes
- RDF expansion pipeline (JSON-LD to TriG/N-Quads via rdflib + pyld)
- pytest suite with 26 tests
- GitHub Actions CI workflow
- Makefile for automation
- Documentation: README, instructions, 5-phase roadmap
