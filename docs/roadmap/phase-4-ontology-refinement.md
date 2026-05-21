# Roadmap Phase 4: Ontology Refinement and SHACL Hardening

**Goal**: Synthesize all per-season ontology considerations into a stable, well-documented ontology; update JSON-LD contexts to match; harden SHACL shapes for full data validation.

## 4.1 Aggregate ontology considerations

- [ ] Script to merge all `docs/ontology-considerations/sNN-considerations.md` files
- [ ] Produce `docs/ontology-considerations/aggregate-considerations.md`
- [ ] Identify consensus classes, properties, and constraints across seasons
- [ ] Flag conflicts (e.g., "Alliance" is explicit in some seasons, implicit in others)

## 4.2 Ontology revision

Based on the aggregate, revise `ontology/survivor.ttl`:

### Candidate new classes

| Class | Rationale |
|---|---|
| `surv:StrategicMove` | Blindsides, idol plays, alliance flips are first-class events |
| `surv:Confessional` | On-camera interview (distinct from in-game dialogue) |
| `surv:AllianceShift` | When alliance membership changes |
| `surv:FinalTribalCouncil` | Subclass of TribalCouncil with FTC-specific properties |
| `surv:JuryVote` | Subclass of Vote cast at FTC (different semantics from regular votes) |
| `surv:Medevac` | Subclass of MedicalEvent for evacuations vs. minor injuries |
| `surv:TribeSwap` | Subclass of Twist for tribe reshuffles |
| `surv:Merge` | Subclass of Twist for tribe merges |

### Candidate new properties

| Property | Domain | Range | Notes |
|---|---|---|---|
| `surv:bootPosition` | Contestant | xsd:integer | Ordinal elimination position |
| `surv:votesAgainst` | Contestant | xsd:integer | Total votes received (season) |
| `surv:individualImmunityWins` | Contestant | xsd:integer | Per-season count |
| `surv:idolsFound` | Contestant | xsd:integer | Per-season count |
| `surv:alliedWith` | Contestant | Contestant | Symmetric property |
| `surv:allianceName` | Alliance | xsd:string | e.g., "Tagi Four", "Black Widow Brigade" |
| `surv:screenTime` | Contestant/Episode | xsd:duration | If available |
| `surv:editArchetype` | Contestant | xsd:string | "winner edit", "villain", etc. |

## 4.3 JSON-LD context updates

After ontology revision:

- [ ] Update `context/season.jsonld` with new terms
- [ ] Update `context/episode.jsonld` with new terms
- [ ] Verify all existing JSON files still expand correctly
- [ ] Add `@type` coercion for new enum-like properties

## 4.4 SHACL shape hardening

Extend shapes for the new classes:

- [ ] `surv:StrategicMoveShape` (requires description + at least one involved contestant)
- [ ] `surv:FinalTribalCouncilShape` (requires exactly 2 or 3 finalists)
- [ ] `surv:JuryVoteShape` (voter must be a jury member, not a finalist)
- [ ] `surv:AllianceShape` (requires at least 2 members)

Tighten existing shapes:

- [ ] Episode: if `is_finale`, must have FTC data
- [ ] Season: boot_order length must equal num_castaways minus 1
- [ ] Tribe: merged tribe must have `surv:mergeDay` property
- [ ] Challenge: if type is "immunity", must have at least one winner

## 4.5 Versioning

The ontology uses `owl:versionInfo`. Revision history:

| Version | Changes |
|---|---|
| 0.1.0-stub | Initial stub with core classes |
| 0.2.0 | Add strategic/alliance classes, new properties |
| 0.3.0 | SHACL hardening, context alignment |
| 1.0.0 | Stable release (after all 50 seasons validated) |

## Completion criteria

Phase 4 is complete when:
- `ontology/survivor.ttl` is at version 0.3.0+
- All JSON-LD contexts align with the ontology
- SHACL validation passes on the full dataset (all 50 seasons)
- Ontology is documented with rdfs:comment on every class and property
