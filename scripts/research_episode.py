#!/usr/bin/env python3
"""
research_episode.py

Deep-research pipeline for individual episodes and seasons.

Usage:
    python scripts/research_episode.py --season 1
    python scripts/research_episode.py --season 1 --episode 5
    python scripts/research_episode.py --all

This script is a framework; the actual research is performed by an
LLM agent (Claude) via the Anthropic API. The script orchestrates:

1. Loading existing episode/season JSON to identify gaps
2. Constructing research prompts with the right scope
3. Storing raw research output as markdown in research/raw/
4. Recording provenance metadata as JSON-LD in research/provenance/
5. Triggering entity extraction (extract_entities.py)
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RAW_DIR = ROOT / "research" / "raw"
PROV_DIR = ROOT / "research" / "provenance"


def find_season_dir(season_num: int) -> Path | None:
    for d in DATA_DIR.iterdir():
        if d.name.startswith(f"season-{season_num:02d}-"):
            return d
    return None


def assess_gaps(season_dir: Path, episode_num: int | None = None) -> dict:
    """Identify what data is missing for a season or episode."""
    gaps = {"season_level": [], "episodes": {}}

    season_file = season_dir / "season.json"
    with open(season_file) as f:
        season = json.load(f)

    # season-level gaps
    if not season.get("boot_order"):
        gaps["season_level"].append("boot_order")
    if season.get("data_completeness") in ("stub", "season-level"):
        gaps["season_level"].append("detailed_data")
    for tribe in season.get("tribes", []):
        if not tribe.get("members"):
            gaps["season_level"].append(f"tribe_members:{tribe['tribe_name']}")

    # episode-level gaps
    ep_files = sorted(season_dir.glob("e*.json"))
    for ef in ep_files:
        with open(ef) as f:
            ep = json.load(f)
        en = ep["episode_number"]
        if episode_num and en != episode_num:
            continue
        ep_gaps = []
        if ep.get("data_completeness") == "stub":
            ep_gaps.append("all_fields")
        if not ep.get("challenges"):
            ep_gaps.append("challenges")
        if not ep.get("tribal_councils"):
            ep_gaps.append("tribal_councils")
        if not ep.get("episode_title"):
            ep_gaps.append("episode_title")
        if ep_gaps:
            gaps["episodes"][en] = ep_gaps

    return gaps


def build_research_prompt(season_num: int, episode_num: int | None,
                          gaps: dict) -> str:
    """Construct the research prompt for the LLM agent."""
    if episode_num:
        return (
            f"Research Survivor Season {season_num}, Episode {episode_num}. "
            f"Find: episode title, air date, challenge names and descriptions, "
            f"challenge winners, reward details, tribal council votes (who voted "
            f"for whom), idol plays, advantages found, twists, tribe membership, "
            f"notable quotes, and any other significant events. "
            f"Missing data: {gaps.get('episodes', {}).get(episode_num, ['unknown'])}"
        )
    return (
        f"Research Survivor Season {season_num} comprehensively. "
        f"Find: full boot order, all tribe members, filming dates, "
        f"key twists and mechanics, and season-level notable facts. "
        f"Missing data: {gaps.get('season_level', ['unknown'])}"
    )


def create_provenance_record(season_num: int, episode_num: int | None,
                             prompt: str, output_path: str) -> dict:
    """Create a PROV-O JSON-LD record for a research activity."""
    now = datetime.now(timezone.utc).isoformat()
    activity_id = f"survprov:research/s{season_num}"
    if episode_num:
        activity_id += f"/e{episode_num}"
    activity_id += f"/{now[:10]}"

    return {
        "@context": "../../context/provenance.jsonld",
        "id": activity_id,
        "type": "ResearchActivity",
        "started_at": now,
        "ended_at": None,
        "was_associated_with": {
            "id": "survprov:agent/claude-deep-research",
            "type": "SoftwareAgent",
            "name": "Claude Deep Research"
        },
        "research_query": prompt,
        "target_season": f"surv:season/{season_num}",
        "target_episode": (
            f"surv:season/{season_num}/episode/{episode_num}"
            if episode_num else None
        ),
        "raw_markdown_path": output_path,
        "confidence": None,
        "used": [
            {"source_name": "Survivor Wiki (Fandom)",
             "source_url": "https://survivor.fandom.com/"},
            {"source_name": "Wikipedia",
             "source_url": "https://en.wikipedia.org/wiki/Survivor_(American_TV_series)"},
            {"source_name": "True Dork Times",
             "source_url": "https://truedorktimes.com/survivor/"}
        ]
    }


def main():
    parser = argparse.ArgumentParser(
        description="Research pipeline for Survivor episodes"
    )
    parser.add_argument("--season", type=int, help="Season number (1-50)")
    parser.add_argument("--episode", type=int, help="Episode number")
    parser.add_argument("--all", action="store_true",
                        help="Research all seasons with gaps")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be researched")
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROV_DIR.mkdir(parents=True, exist_ok=True)

    if args.all:
        targets = list(range(1, 51))
    elif args.season:
        targets = [args.season]
    else:
        parser.print_help()
        return

    for sn in targets:
        sd = find_season_dir(sn)
        if not sd:
            print(f"  [!] Season {sn} directory not found")
            continue

        gaps = assess_gaps(sd, args.episode)
        if not gaps["season_level"] and not gaps["episodes"]:
            print(f"  [=] S{sn:02d}: no gaps detected, skipping")
            continue

        prompt = build_research_prompt(sn, args.episode, gaps)

        if args.dry_run:
            print(f"  [?] S{sn:02d}: would research")
            print(f"      Gaps: {json.dumps(gaps, indent=2)[:200]}")
            print(f"      Prompt: {prompt[:120]}...")
            continue

        # Placeholder: actual LLM call goes here
        md_filename = f"s{sn:02d}"
        if args.episode:
            md_filename += f"-e{args.episode:02d}"
        md_filename += ".md"
        md_path = RAW_DIR / md_filename

        md_path.write_text(
            f"# Survivor Season {sn}"
            + (f" Episode {args.episode}" if args.episode else "")
            + "\n\n"
            + f"Research prompt: {prompt}\n\n"
            + "## TODO: Replace with actual deep research output\n"
        )

        prov = create_provenance_record(
            sn, args.episode, prompt, str(md_path.relative_to(ROOT))
        )
        prov_path = PROV_DIR / md_filename.replace(".md", ".jsonld")
        with open(prov_path, "w") as f:
            json.dump(prov, f, indent=2)

        print(f"  [+] S{sn:02d}: research stub created at {md_path.name}")


if __name__ == "__main__":
    main()
