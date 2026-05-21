# Roadmap Phase 2: Deep Research Pipeline

**Goal**: Systematically research every episode of every season, producing raw markdown with full provenance tracking. Start with Tier A/B seasons; work outward.

## 2.1 Integrate LLM research agent

- [ ] Add Anthropic API integration to `research_episode.py`
- [ ] Use Claude's deep research mode for episode-level queries
- [ ] Implement rate limiting and cost tracking
- [ ] Add retry logic with query refinement for thin results

### Research query templates

**Season-level query**:
```
Research Survivor Season {N} ({subtitle}). Provide:
1. Complete boot order with day eliminated
2. Full tribe rosters (initial + any swaps/merges)
3. All filming and air dates
4. All twists, advantages, and idols introduced
5. Key alliances and their arc
6. Fan reception and notable controversies
```

**Episode-level query**:
```
Research Survivor Season {N} Episode {E} ("{title}").
Provide: challenge names and descriptions, challenge winners,
reward details, Tribal Council votes (who voted for whom),
idol/advantage plays, twists, tribe membership at episode start,
notable quotes with speaker attribution, and key strategic moves.
```

## 2.2 Provenance chain

Every research output produces two artifacts:

1. `research/raw/sNN-eEE.md` (the markdown)
2. `research/provenance/sNN-eEE.jsonld` (the PROV-O record)

The provenance record links:
- `prov:wasGeneratedBy` -> the research activity
- `prov:wasAssociatedWith` -> the LLM agent
- `prov:used` -> the source URLs consulted
- `survprov:confidence` -> assessed after extraction (0.0-1.0)

## 2.3 Batching strategy

Research is expensive. Batch by season, not by episode:

1. Research the full season first (boot order, tribes, mechanics)
2. Research each episode in order (context builds incrementally)
3. Cross-validate: episode-level eliminations must match boot order

Parallelism: up to 5 seasons in parallel (API rate limits permitting).

## 2.4 Source triangulation

For contested facts (e.g., exact vote tallies, who found an idol), require at least two independent sources. The provenance record supports multiple `prov:used` entries with per-source confidence.

Priority sources:
1. Survivor Wiki episode pages (most complete)
2. Wikipedia season articles (reliable vote tables)
3. True Dork Times calendar pages (challenge stats)
4. CBS episode recaps (authoritative but surface-level)

## Completion criteria

Phase 2 is complete when:
- Raw research markdown exists for all Tier A+B seasons (every episode)
- Provenance records exist for all research outputs
- Season-level research exists for all 50 seasons
- A sample audit of 10 random episodes shows >90% fact accuracy
