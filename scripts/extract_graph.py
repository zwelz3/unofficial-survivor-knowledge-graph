#!/usr/bin/env python3
"""
extract_graph.py

Extracts a labeled property graph (LPG) from the JSON-LD dataset
for visualization. Produces a compact JSON with nodes and edges
at multiple zoom levels:

  - overview:  seasons + returning players + cross-season edges
  - season:    one season's contestants, tribes, episodes
  - episode:   one episode's tribal council detail

Output: data/graph.json
"""

import json, re
from pathlib import Path
from collections import defaultdict

DATA = Path(__file__).resolve().parent.parent / "data"

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def build_graph():
    seasons = []
    all_contestants = {}  # name -> {seasons_played, ...}
    all_tribes = []
    all_edges = []
    season_details = {}  # sn -> season-level subgraph

    for sd in sorted(DATA.iterdir()):
        if not sd.is_dir():
            continue
        sf = sd / "season.json"
        if not sf.exists():
            continue
        with open(sf) as f:
            s = json.load(f)
        sn = s["season_number"]

        # Season node
        season_node = {
            "id": f"season-{sn}",
            "type": "Season",
            "label": f"S{sn}: {s.get('subtitle', '')}",
            "properties": {
                "number": sn,
                "subtitle": s.get("subtitle", ""),
                "era": s.get("era", ""),
                "winner": s.get("winner", {}).get("name", ""),
                "ftc_vote": s.get("ftc_vote", ""),
                "num_castaways": s.get("num_castaways", 0),
                "num_days": s.get("num_days", 39),
                "prize": s.get("prize_amount", 1000000),
                "air_start": s.get("air_date_start", ""),
                "location": s.get("filming_location", {}).get("location_name", ""),
            }
        }
        seasons.append(season_node)

        # Tribe nodes + edges
        for t in s.get("tribes", []):
            tid = f"tribe-{slug(t.get('tribe_name', ''))}-s{sn}"
            all_tribes.append({
                "id": tid,
                "type": "Tribe",
                "label": t.get("tribe_name", ""),
                "properties": {
                    "color": t.get("tribe_color", ""),
                    "season": sn,
                    "member_count": len(t.get("members", [])),
                }
            })
            all_edges.append({
                "source": f"season-{sn}",
                "target": tid,
                "type": "has_tribe",
            })
            for m in t.get("members", []):
                mname = m.get("name", "") if isinstance(m, dict) else ""
                if mname:
                    mid = f"contestant-{slug(mname)}-s{sn}"
                    all_edges.append({
                        "source": mid,
                        "target": tid,
                        "type": "member_of",
                    })

        # Contestant nodes
        boot = s.get("boot_order", [])
        contestants_this = []
        for i, name in enumerate(boot):
            if not name or name == "TBA":
                continue
            cid = f"contestant-{slug(name)}-s{sn}"
            is_winner = (s.get("winner", {}).get("name", "") == name)
            node = {
                "id": cid,
                "type": "Contestant",
                "label": name,
                "properties": {
                    "season": sn,
                    "placement": i + 1,
                    "of": len(boot),
                    "is_winner": is_winner,
                    "percentile": round((i + 1) / len(boot) * 100),
                }
            }
            contestants_this.append(node)

            # Track for returning player detection
            if name not in all_contestants:
                all_contestants[name] = {"seasons": [], "nodes": []}
            all_contestants[name]["seasons"].append(sn)
            all_contestants[name]["nodes"].append(cid)

            # played_in edge
            all_edges.append({
                "source": cid,
                "target": f"season-{sn}",
                "type": "winner_of" if is_winner else "played_in",
            })

        # Episode nodes + elimination edges
        episodes_this = []
        for ef in sorted(sd.glob("e*.json")):
            with open(ef) as f:
                ep = json.load(f)
            en = ep.get("episode_number", 0)
            eid = f"episode-s{sn}-e{en}"
            episodes_this.append({
                "id": eid,
                "type": "Episode",
                "label": ep.get("episode_title", f"E{en}"),
                "properties": {
                    "season": sn,
                    "number": en,
                    "air_date": ep.get("air_date", ""),
                    "viewership": ep.get("viewership_millions"),
                    "completeness": ep.get("data_completeness", "stub"),
                }
            })
            all_edges.append({
                "source": eid,
                "target": f"season-{sn}",
                "type": "in_season",
            })
            for tc in ep.get("tribal_councils", []):
                pe = tc.get("person_eliminated", {})
                if pe.get("name"):
                    ecid = f"contestant-{slug(pe['name'])}-s{sn}"
                    all_edges.append({
                        "source": ecid,
                        "target": eid,
                        "type": "eliminated_in",
                        "properties": {
                            "method": tc.get("elimination_method", "vote"),
                            "votes": tc.get("vote_count_summary", ""),
                        }
                    })

        season_details[sn] = {
            "contestants": contestants_this,
            "episodes": episodes_this,
        }

    # Returning player cross-season edges
    returning_edges = []
    returning_players = []
    for name, data in all_contestants.items():
        if len(data["seasons"]) >= 2:
            canonical_id = f"person-{slug(name)}"
            returning_players.append({
                "id": canonical_id,
                "type": "Person",
                "label": name,
                "properties": {
                    "times_played": len(data["seasons"]),
                    "seasons": data["seasons"],
                }
            })
            for cid in data["nodes"]:
                returning_edges.append({
                    "source": canonical_id,
                    "target": cid,
                    "type": "same_person",
                })
            # Cross-season edges
            for i in range(len(data["seasons"]) - 1):
                returning_edges.append({
                    "source": f"season-{data['seasons'][i]}",
                    "target": f"season-{data['seasons'][i+1]}",
                    "type": "returning_player",
                    "properties": {"player": name},
                })

    # Build overview graph (seasons + returning player connections)
    # Deduplicate cross-season edges
    seen_cross = set()
    deduped_cross = []
    for e in returning_edges:
        if e["type"] == "returning_player":
            key = (e["source"], e["target"])
            if key not in seen_cross:
                seen_cross.add(key)
                deduped_cross.append(e)

    overview = {
        "nodes": seasons + returning_players,
        "edges": deduped_cross + [e for e in returning_edges if e["type"] == "same_person"],
    }

    # Build full graph data
    graph = {
        "overview": overview,
        "seasons": {},
        "meta": {
            "total_seasons": len(seasons),
            "total_contestants": len(all_contestants),
            "returning_players": len(returning_players),
            "total_tribes": len(all_tribes),
            "total_edges": len(all_edges) + len(returning_edges),
            "generated": "2026-05-21",
        }
    }

    # Per-season subgraphs
    for sn, detail in season_details.items():
        s_node = next(s for s in seasons if s["id"] == f"season-{sn}")
        tribes_this = [t for t in all_tribes if t["properties"]["season"] == sn]
        edges_this = [e for e in all_edges
                      if (f"-s{sn}" in e.get("source", "") or
                          f"-s{sn}" in e.get("target", "") or
                          e.get("source") == f"season-{sn}" or
                          e.get("target") == f"season-{sn}")]
        graph["seasons"][str(sn)] = {
            "nodes": [s_node] + detail["contestants"] + tribes_this + detail["episodes"],
            "edges": edges_this,
        }

    return graph


if __name__ == "__main__":
    graph = build_graph()
    out = DATA / "graph.json"
    with open(out, "w") as f:
        json.dump(graph, f, separators=(",", ":"))
    print(f"Graph extracted to {out}")
    print(f"Overview: {len(graph['overview']['nodes'])} nodes, {len(graph['overview']['edges'])} edges")
    print(f"Seasons: {len(graph['seasons'])} subgraphs")
    print(f"Meta: {json.dumps(graph['meta'], indent=2)}")
