# Roadmap Phase 1: Data Foundation

**Goal**: Establish the structural backbone; every season and episode has a well-formed JSON file with correct metadata, and the JSON-LD-to-RDF pipeline runs cleanly.

## 1.1 Generate and validate the data tree

- [x] Create `generate_data.py` with all 50 seasons
- [x] Produce season.json for each season (winner, FTC vote, tribes, era, mechanics)
- [x] Produce episode stub JSON for every episode (~700 files)
- [x] JSON-LD contexts for season, episode, and provenance
- [x] `expand_to_rdf.py` producing TriG, N-Quads, per-graph Turtle
- [x] pytest suite covering directory structure, field presence, era boundaries

## 1.2 Fill priority season data

Priority seasons (by popularity and research availability):

| Tier | Seasons | Rationale |
|------|---------|-----------|
| A | 1, 7, 16, 20, 28, 40 | Most iconic; highest fan engagement |
| B | 2, 10, 13, 15, 25, 31, 37 | Highly rated; watershed moments |
| C | 41, 42, 43, 44, 45, 46, 47, 48, 49, 50 | New Era; most recent |
| D | 3, 4, 5, 6, 8, 9, 11, 12, 14, 17, 18, 19 | Classic fill |
| E | 21-24, 26, 27, 29, 30, 32-36, 38, 39 | Modern fill |

For each tier, the deliverable is:
- Complete boot order in season.json
- Full tribe rosters (all members named) in season.json
- All mechanics listed with descriptions
- Episode titles for every episode
- Air dates for every episode

## 1.3 Establish identity resolution

Returning players appear across multiple seasons. The data model uses season-specific contestant IDs (`surv:contestant/boston-rob/s4`, `surv:contestant/boston-rob/s8`, etc.) linked by a shared canonical person URI (`surv:person/rob-mariano`).

Deliverables:
- Create `data/contestants.json` as a cross-season identity registry
- Add `original_season` and `canonical_person` fields to contestant records
- Script to validate no orphan contestant references

## 1.4 SHACL and ontology baseline

- [x] `survivor.ttl` ontology with core classes and properties
- [x] `survivor-shapes.ttl` SHACL shapes for Season, Episode, Contestant, Tribe
- [x] `validate_shacl.py` runner
- [ ] Fix any violations surfaced by first validation pass
- [ ] Add SHACL shapes for Challenge, TribalCouncil, Vote, IdolPlay

## Completion criteria

Phase 1 is complete when:
- `make all` runs without errors
- All 50 season.json files pass SHACL validation
- Tier A and B seasons have complete boot orders and tribe rosters
- The RDF dataset has >5,000 triples
