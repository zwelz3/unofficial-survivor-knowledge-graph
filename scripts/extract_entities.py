#!/usr/bin/env python3
"""
extract_entities.py

Reads raw research markdown files and extracts structured entities,
relationships, attributes, and values. Maps them to RDF concepts
(classes, object properties, data properties) and updates the
episode/season JSON files.

Usage:
    python scripts/extract_entities.py --season 1
    python scripts/extract_entities.py --file research/raw/s01.md
    python scripts/extract_entities.py --all
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RAW_DIR = ROOT / "research" / "raw"
PROV_DIR = ROOT / "research" / "provenance"
ONTO_DIR = ROOT / "docs" / "ontology-considerations"


@dataclass
class ExtractedEntity:
    name: str
    entity_type: str  # Contestant, Tribe, Challenge, etc.
    attributes: dict = field(default_factory=dict)
    source_span: str = ""


@dataclass
class ExtractedRelationship:
    subject: str
    predicate: str
    object: str
    relationship_type: str  # object_property or data_property
    source_span: str = ""


@dataclass
class ExtractionResult:
    entities: list[ExtractedEntity] = field(default_factory=list)
    relationships: list[ExtractedRelationship] = field(default_factory=list)
    ontology_notes: list[str] = field(default_factory=list)


# ── pattern-based extraction (baseline; LLM extraction extends) ─────

CONTESTANT_PATTERN = re.compile(
    r"(?:voted out|eliminated|won|found|played)\s+(?:by\s+)?([A-Z][a-z]+ [A-Z][a-z]+)"
)
TRIBE_PATTERN = re.compile(
    r"([A-Z][a-z]+)\s+tribe"
)
CHALLENGE_PATTERN = re.compile(
    r"(?:Reward|Immunity|Combined)\s+Challenge:\s*(.+?)(?:\.|$)", re.MULTILINE
)
VOTE_PATTERN = re.compile(
    r"(\d+)-(\d+)(?:-(\d+))?\s+vote"
)


def extract_from_markdown(text: str) -> ExtractionResult:
    """Run pattern-based extraction on research markdown."""
    result = ExtractionResult()

    # Extract contestant mentions
    seen_names = set()
    for match in CONTESTANT_PATTERN.finditer(text):
        name = match.group(1)
        if name not in seen_names:
            result.entities.append(ExtractedEntity(
                name=name,
                entity_type="Contestant",
                source_span=match.group(0)[:80]
            ))
            seen_names.add(name)

    # Extract tribe mentions
    seen_tribes = set()
    for match in TRIBE_PATTERN.finditer(text):
        tribe = match.group(1)
        if tribe not in seen_tribes and tribe not in ("The", "A", "No"):
            result.entities.append(ExtractedEntity(
                name=tribe,
                entity_type="Tribe",
                source_span=match.group(0)[:80]
            ))
            seen_tribes.add(tribe)

    # Extract challenge mentions
    for match in CHALLENGE_PATTERN.finditer(text):
        result.entities.append(ExtractedEntity(
            name=match.group(1).strip(),
            entity_type="Challenge",
            source_span=match.group(0)[:80]
        ))

    # Note: full extraction requires LLM processing.
    # This baseline catches ~30% of entities; the rest require
    # semantic understanding of context.
    result.ontology_notes.append(
        "Pattern-based extraction is a baseline. "
        "LLM-based extraction will identify implicit relationships "
        "(e.g., alliance membership, strategic moves, emotional arcs) "
        "that regex cannot capture."
    )

    return result


def generate_ontology_considerations(
    season_num: int,
    results: list[ExtractionResult]
) -> str:
    """Generate an ontology considerations markdown file."""
    entity_types = set()
    rel_types = set()
    notes = []

    for r in results:
        for e in r.entities:
            entity_types.add(e.entity_type)
        for rel in r.relationships:
            rel_types.add(rel.predicate)
        notes.extend(r.ontology_notes)

    lines = [
        f"# Ontology Considerations: Season {season_num}",
        "",
        "## Observed Entity Types",
        "",
    ]
    for et in sorted(entity_types):
        lines.append(f"- **{et}**: maps to `surv:{et}`")
    lines.extend([
        "",
        "## Observed Relationship Types",
        "",
    ])
    for rt in sorted(rel_types):
        lines.append(f"- `{rt}`")
    lines.extend([
        "",
        "## Recommended New Classes",
        "",
        "Based on the extracted data, consider adding:",
        "",
        "- `surv:StrategicMove`: captures blindsides, idol plays, "
        "alliance flips as first-class events",
        "- `surv:Confessional`: a contestant's on-camera interview "
        "statement (distinct from in-game quotes)",
        "- `surv:Rivalry`: a sustained adversarial relationship "
        "between two contestants",
        "- `surv:AllianceShift`: an event where alliance membership changes",
        "",
        "## Recommended New Properties",
        "",
        "- `surv:votingConfidence` (xsd:decimal): how predictable "
        "the vote outcome was",
        "- `surv:screenTime` (xsd:duration): approximate screen time "
        "per contestant per episode",
        "- `surv:editType` (xsd:string): winner edit, villain edit, "
        "under-the-radar, etc.",
        "",
        "## Notes from Extraction",
        "",
    ])
    for note in notes:
        lines.append(f"- {note}")

    return "\n".join(lines) + "\n"


def update_episode_json(season_dir: Path, episode_num: int,
                        result: ExtractionResult):
    """Merge extracted entities into the episode JSON file."""
    ep_file = season_dir / f"e{episode_num:02d}.json"
    if not ep_file.exists():
        return

    with open(ep_file) as f:
        doc = json.load(f)

    # Merge notable events from entities
    existing_events = set(doc.get("notable_events", []))
    for entity in result.entities:
        if entity.entity_type == "Challenge":
            doc.setdefault("challenges", []).append({
                "challenge_name": entity.name,
                "challenge_type": None,
                "challenge_description": None,
                "challenge_winners": []
            })

    if result.entities:
        doc["data_completeness"] = "season-level"
        doc["research_status"] = "extracted"

    with open(ep_file, "w") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="Extract entities from research markdown"
    )
    parser.add_argument("--season", type=int)
    parser.add_argument("--file", type=str)
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    ONTO_DIR.mkdir(parents=True, exist_ok=True)

    if args.file:
        md_path = Path(args.file)
        if not md_path.exists():
            print(f"File not found: {md_path}")
            sys.exit(1)
        text = md_path.read_text()
        result = extract_from_markdown(text)
        print(f"Extracted {len(result.entities)} entities, "
              f"{len(result.relationships)} relationships")
        for e in result.entities:
            print(f"  [{e.entity_type}] {e.name}")
        return

    targets = list(range(1, 51)) if args.all else [args.season] if args.season else []
    if not targets:
        parser.print_help()
        return

    for sn in targets:
        md_path = RAW_DIR / f"s{sn:02d}.md"
        if not md_path.exists():
            continue

        text = md_path.read_text()
        result = extract_from_markdown(text)

        # Write ontology considerations
        onto_md = generate_ontology_considerations(sn, [result])
        onto_path = ONTO_DIR / f"s{sn:02d}-considerations.md"
        onto_path.write_text(onto_md)

        print(f"  [+] S{sn:02d}: {len(result.entities)} entities, "
              f"ontology notes -> {onto_path.name}")


if __name__ == "__main__":
    main()
