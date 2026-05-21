# Instructions: Survivor Knowledge Graph Pipeline

This document explains how to use the research, extraction, and ontology-building pipeline to progressively fill the knowledge graph with verified data for every episode of every season.

## Overview

The pipeline has six stages, each building on the last:

1. **Deep research** on each episode and season (LLM-assisted)
2. **Store** raw research as markdown with PROV-O provenance
3. **Extract** entities, relationships, attributes, and values from markdown
4. **Map** extracted data to RDF concepts (classes, properties)
5. **Store** structured data in JSON files for each episode/season
6. **Generate ontology considerations** that feed back into ontology refinement

## Prerequisites

```bash
make install         # rdflib, pyld, pyshacl, pytest
make generate        # create data/ tree if not already present
```

## Stage 1: Deep Research

For each episode (or season as a whole), perform deep research using Claude's extended search. The research should cover:

- Episode title and air date
- Challenge names, types (reward/immunity/combined), descriptions
- Challenge winners (individual or tribe)
- Reward descriptions and recipients
- Tribal Council votes (who voted for whom, vote count)
- Idol and advantage plays (who played, for whom, votes negated)
- Advantages found (type, finder, description)
- Twists (tribe swaps, medevacs, quits, mutinies, rock draws, fire-making)
- Tribe membership at start of episode
- Notable quotes (speaker, context)
- Alliances formed, broken, or shifted
- Any other significant events

### Running research

```bash
# Research a specific season
python scripts/research_episode.py --season 1

# Research a specific episode
python scripts/research_episode.py --season 1 --episode 5

# Dry run (show gaps without researching)
python scripts/research_episode.py --season 1 --dry-run

# Research all seasons with detected gaps
python scripts/research_episode.py --all --dry-run
```

The script identifies gaps in the existing JSON data and constructs targeted prompts. In its current form, it creates stub markdown files; the actual LLM research call should be integrated via the Anthropic API.

## Stage 2: Store Raw Research

Research output is stored as markdown in `research/raw/`:

```
research/
  raw/
    s01.md              # Season 1 overview research
    s01-e01.md          # Season 1 Episode 1 research
    s01-e02.md
    ...
  provenance/
    s01.jsonld           # PROV-O record for S01 research
    s01-e01.jsonld
    ...
```

Provenance records use the PROV-O vocabulary via `context/provenance.jsonld`. Each record tracks:

- The research activity (who, when, what query)
- Sources consulted (Survivor Wiki, Wikipedia, True Dork Times)
- Target season/episode
- Path to the raw markdown
- Confidence level (to be assessed after extraction)

## Stage 3: Extract Entities

The extraction script reads raw markdown and produces structured data:

```bash
# Extract from a specific file
python scripts/extract_entities.py --file research/raw/s01-e01.md

# Extract for a whole season
python scripts/extract_entities.py --season 1

# Extract everything
python scripts/extract_entities.py --all
```

The baseline extractor uses regex patterns. For production quality, integrate LLM-based extraction that understands context (e.g., distinguishing a contestant named "Amber" from the word "amber" as a color).

### What gets extracted

- **Entities**: Contestants, Tribes, Challenges, Advantages, Alliances
- **Relationships**: voted-for, member-of, winner-of, played-idol-for, allied-with
- **Attributes**: placement, days lasted, tribe color, challenge type
- **Values**: vote counts, air dates, viewership numbers

## Stage 4: Map to RDF Concepts

Each extracted entity type maps to an OWL class:

| Extracted Type | OWL Class | Notes |
|---|---|---|
| Contestant | `surv:Contestant` | Subclass of `foaf:Person` |
| Tribe | `surv:Tribe` | Season-specific instances |
| Challenge | `surv:Challenge` | Types: reward, immunity, combined |
| Vote | `surv:Vote` | Links voter to voted-for |
| IdolPlay | `surv:IdolPlay` | Links player, recipient, votes negated |
| Advantage | `surv:Advantage` | Found/earned/purchased items |
| Alliance | `surv:Alliance` | Named or unnamed groupings |
| Quote | `surv:Quote` | Speaker + context + text |

Relationships map to OWL object properties; attributes to datatype properties. The extraction script outputs these mappings alongside the ontology considerations file.

## Stage 5: Update Episode/Season JSON

Extracted data is merged into the existing JSON files:

```
data/season-01-borneo/
  season.json          # Updated with boot order, detailed tribes
  e01.json             # Updated with challenges, votes, quotes
  e02.json
  ...
```

After updating, the `data_completeness` field advances from `"stub"` through `"season-level"` to `"detailed"` and finally `"verified"` (after manual QA).

## Stage 6: Ontology Considerations

For each season (and aggregated across all seasons), the pipeline generates an "ontology considerations" markdown file:

```
docs/ontology-considerations/
  s01-considerations.md
  s07-considerations.md
  ...
  aggregate-considerations.md
```

These files recommend new classes, properties, and constraints based on what the data actually contains. They feed into ontology refinement: review the recommendations, update `ontology/survivor.ttl` and `shapes/survivor-shapes.ttl`, then re-validate.

## Regenerating RDF

After updating JSON files:

```bash
make expand          # Re-expand all JSON-LD to RDF
make validate        # Re-validate SHACL
make test            # Re-run all tests
```

## Quality gates

Before marking a season as `"verified"`:

1. All episode files have non-null `episode_title` and `air_date`
2. All Tribal Councils have `person_eliminated` and `vote_count_summary`
3. Boot order matches the number of contestants minus the winner
4. SHACL validation passes
5. At least two independent sources corroborate key facts (winner, FTC vote)

## Authoritative sources (priority order)

1. **survivor.fandom.com** (most comprehensive; episode-level detail)
2. **en.wikipedia.org** (reliable season-level tables and vote counts)
3. **truedorktimes.com** (best challenge stats and per-contestant analytics)
4. **insidesurvivor.com** (strongest editorial commentary, New Era)
5. **CBS/Paramount official recaps** (authoritative but less detailed)
