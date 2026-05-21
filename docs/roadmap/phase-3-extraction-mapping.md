# Roadmap Phase 3: Entity Extraction and Data Mapping

**Goal**: Transform raw research markdown into structured JSON data by extracting entities, relationships, and attributes; then map them to the ontology's RDF classes and properties.

## 3.1 LLM-based entity extraction

The baseline regex extractor in `extract_entities.py` catches ~30% of entities. Full extraction requires LLM processing:

- [ ] Add Anthropic API call to `extract_entities.py`
- [ ] Use structured output (JSON mode) for reliable parsing
- [ ] Extraction prompt includes the ontology class list so the LLM maps entities directly

### Extraction output format

```json
{
  "entities": [
    {"name": "Richard Hatch", "type": "Contestant", "attributes": {"placement": 1}},
    {"name": "Tagi", "type": "Tribe", "attributes": {"color": "orange"}}
  ],
  "relationships": [
    {"subject": "Richard Hatch", "predicate": "votedFor", "object": "Rudy Boesch"},
    {"subject": "Tagi", "predicate": "hasMember", "object": "Richard Hatch"}
  ],
  "values": [
    {"entity": "S01E13", "attribute": "viewershipMillions", "value": 51.7}
  ]
}
```

## 3.2 Relationship type mapping

| Extracted Predicate | RDF Property | Domain | Range |
|---|---|---|---|
| votedFor | surv:votedFor | surv:Vote | surv:Contestant |
| eliminated | surv:personEliminated | surv:TribalCouncil | surv:Contestant |
| wonChallenge | surv:challengeWinner | surv:Challenge | surv:Contestant |
| foundIdol | surv:advantageFinder | surv:Advantage | surv:Contestant |
| playedIdolFor | surv:idolPlayedFor | surv:IdolPlay | surv:Contestant |
| memberOf | surv:hasMember (inverse) | surv:Tribe | surv:Contestant |
| alliedWith | surv:alliedWith | surv:Contestant | surv:Contestant |
| saidQuote | surv:quoteSpeaker (inverse) | surv:Quote | surv:Contestant |

## 3.3 Merge into JSON files

After extraction, update episode/season JSON files:

- Challenges: add to `challenges[]` with name, type, description, winners
- Votes: add to `tribal_councils[].votes[]` with voter, voted_for
- Idols: add to `idol_plays[]` with player, played_for, votes_negated
- Quotes: add to `notable_quotes[]` with text, speaker, context
- Twists: add to `twists[]` with name, description, type
- Update `data_completeness` and `research_status` fields

## 3.4 Validation after merge

After each episode update:

1. Re-expand JSON-LD to RDF
2. Run SHACL validation
3. Cross-check: eliminated contestant in episode N should not appear in episode N+1 tribe states
4. Cross-check: vote counts must sum correctly

## 3.5 Generate ontology considerations

For each processed season, generate `docs/ontology-considerations/sNN-considerations.md` covering:

- New entity types observed (not yet in ontology)
- New relationship types observed
- Recommended cardinality constraints
- Enum value candidates (challenge types, elimination methods)
- Notes on ambiguous or context-dependent relationships

## Completion criteria

Phase 3 is complete when:
- All Tier A+B season episodes have extracted and merged data
- `data_completeness` is at least `"detailed"` for those episodes
- SHACL validation passes after merge
- Ontology considerations files exist for all processed seasons
