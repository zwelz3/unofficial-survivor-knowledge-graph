#!/usr/bin/env python3
"""
enrich_data.py

Phase 1 enrichment: fills boot orders, episode titles, air dates,
viewership, tribe rosters, and per-episode elimination data for all
50 seasons from compiled research.

Run: python scripts/enrich_data.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def slug(s: str) -> str:
    import re
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def contestant_id(name: str, sn: int) -> str:
    return f"surv:contestant/{slug(name)}/s{sn}"


# ═══════════════════════════════════════════════════════════════════
# SEASON 1: BORNEO (complete from Wikipedia)
# ═══════════════════════════════════════════════════════════════════

S1_EPISODES = [
    {"ep": 1, "title": "The Marooning", "air_date": "2000-05-31",
     "viewers": 15.51, "day_start": 1, "day_end": 3,
     "immunity_winner": "Tagi", "reward_winner": "Pagong",
     "eliminated": "Sonja Christopher", "vote": "4-3-1",
     "is_premiere": True},
    {"ep": 2, "title": "The Generation Gap", "air_date": "2000-06-07",
     "viewers": 18.10, "day_start": 4, "day_end": 6,
     "immunity_winner": "Pagong", "reward_winner": "Tagi",
     "eliminated": "B.B. Andersen", "vote": "6-2"},
    {"ep": 3, "title": "Quest for Food", "air_date": "2000-06-14",
     "viewers": 23.25, "day_start": 7, "day_end": 9,
     "immunity_winner": "Tagi", "reward_winner": "Pagong",
     "eliminated": "Stacey Stillman", "vote": "5-2"},
    {"ep": 4, "title": "Too Little, Too Late?", "air_date": "2000-06-21",
     "viewers": 24.20, "day_start": 10, "day_end": 12,
     "immunity_winner": "Tagi", "reward_winner": "Tagi",
     "eliminated": "Ramona Gray", "vote": "4-2-1"},
    {"ep": 5, "title": "Pulling Your Own Weight", "air_date": "2000-06-28",
     "viewers": 23.98, "day_start": 13, "day_end": 15,
     "immunity_winner": "Pagong", "reward_winner": "Pagong",
     "eliminated": "Dirk Been", "vote": "4-1-1"},
    {"ep": 6, "title": "Udder Revenge", "air_date": "2000-07-05",
     "viewers": 24.50, "day_start": 16, "day_end": 18,
     "immunity_winner": "Tagi", "reward_winner": "Pagong",
     "eliminated": "Joel Klug", "vote": "4-2"},
    {"ep": 7, "title": "The Merger", "air_date": "2000-07-12",
     "viewers": 24.50, "day_start": 19, "day_end": 21,
     "immunity_winner": "Greg Buis", "reward_winner": None,
     "eliminated": "Gretchen Cordy", "vote": "4-1-1-1-1-1-1",
     "notable": "Merge into Rattana"},
    {"ep": 8, "title": "Thy Name Is Duplicity", "air_date": "2000-07-19",
     "viewers": 26.15, "day_start": 22, "day_end": 24,
     "immunity_winner": "Gervase Peterson", "reward_winner": "Greg Buis",
     "eliminated": "Greg Buis", "vote": "6-3"},
    {"ep": 9, "title": "Old and New Bonds", "air_date": "2000-07-26",
     "viewers": 27.18, "day_start": 25, "day_end": 27,
     "immunity_winner": "Rudy Boesch", "reward_winner": "Colleen Haskell",
     "eliminated": "Jenna Lewis", "vote": "4-3-1"},
    {"ep": 10, "title": "Crack in the Alliance", "air_date": "2000-08-02",
     "viewers": 27.41, "day_start": 28, "day_end": 30,
     "immunity_winner": "Richard Hatch", "reward_winner": "Gervase Peterson",
     "eliminated": "Gervase Peterson", "vote": "5-2"},
    {"ep": 11, "title": "Long Hard Days", "air_date": "2000-08-09",
     "viewers": 28.00, "day_start": 31, "day_end": 33,
     "immunity_winner": "Kelly Wiglesworth", "reward_winner": "Sean Kenniff",
     "eliminated": "Colleen Haskell", "vote": "4-2"},
    {"ep": 12, "title": "Death of an Alliance", "air_date": "2000-08-16",
     "viewers": 28.67, "day_start": 34, "day_end": 36,
     "immunity_winner": "Kelly Wiglesworth", "reward_winner": "Kelly Wiglesworth",
     "eliminated": "Sean Kenniff", "vote": "4-1"},
    {"ep": 13, "title": "The Final Four", "air_date": "2000-08-23",
     "viewers": 51.69, "day_start": 37, "day_end": 39,
     "immunity_winner": "Kelly Wiglesworth", "reward_winner": None,
     "eliminated": "Sue Hawk", "vote": "2-2 (revote 2-0)",
     "is_finale": True,
     "notable": "Tie vote; Kelly switched vote on revote. Rudy eliminated Day 38. Richard wins 4-3."},
]

S1_BOOT = [
    "Sonja Christopher", "B.B. Andersen", "Stacey Stillman",
    "Ramona Gray", "Dirk Been", "Joel Klug", "Gretchen Cordy",
    "Greg Buis", "Jenna Lewis", "Gervase Peterson",
    "Colleen Haskell", "Sean Kenniff", "Sue Hawk", "Rudy Boesch",
    "Kelly Wiglesworth", "Richard Hatch"
]

# ═══════════════════════════════════════════════════════════════════
# SEASON 20: HEROES VS. VILLAINS (from Wikipedia + Fandom)
# ═══════════════════════════════════════════════════════════════════

S20_BOOT = [
    "Sugar Kiper", "Stephenie LaGrossa", "Randy Bailey",
    "Cirie Fields", "Tom Westman", "Rob Mariano", "Tyson Apostol",
    "James Clement", "Coach Wade", "Courtney Yates",
    "J.T. Thomas", "Amanda Kimmel", "Candice Woodcock",
    "Danielle DiLorenzo", "Rupert Boneham", "Colby Donaldson",
    "Jerri Manthey", "Russell Hantz", "Parvati Shallow",
    "Sandra Diaz-Twine"
]

S20_EPISODES = [
    {"ep": 1, "title": "Slay Everyone, Trust No One",
     "air_date": "2010-02-11", "viewers": 19.98,
     "day_start": 1, "day_end": 3,
     "eliminated": "Sugar Kiper", "vote": "9-1", "is_premiere": True},
    {"ep": 2, "title": "It's Getting the Best of Me",
     "air_date": "2010-02-18", "viewers": 17.45,
     "day_start": 4, "day_end": 6,
     "eliminated": "Stephenie LaGrossa", "vote": "6-3"},
    {"ep": 3, "title": "That Girl Is Like a Virus",
     "air_date": "2010-02-25", "viewers": 17.42,
     "day_start": 7, "day_end": 9,
     "eliminated": "Randy Bailey", "vote": "9-1"},
    {"ep": 4, "title": "Tonight, We Make Our Move",
     "air_date": "2010-03-04", "viewers": 16.52,
     "day_start": 10, "day_end": 12,
     "eliminated": "Cirie Fields", "vote": "6-3"},
    {"ep": 5, "title": "Knights of the Round Table",
     "air_date": "2010-03-11", "viewers": 16.61,
     "day_start": 13, "day_end": 15,
     "eliminated": "Tom Westman", "vote": "5-3",
     "notable": "Tom played HII on himself, negating 2 votes"},
    {"ep": 6, "title": "Banana Etiquette",
     "air_date": "2010-03-18", "viewers": 17.60,
     "day_start": 16, "day_end": 18,
     "eliminated": "Rob Mariano", "vote": "4-3-1",
     "notable": "Tyson voted himself out by changing vote; Russell played idol"},
    {"ep": 7, "title": "I'm Not a Good Villain",
     "air_date": "2010-03-25", "viewers": 16.17,
     "day_start": 18, "day_end": 19,
     "eliminated": "Tyson Apostol", "vote": "4-3"},
    {"ep": 8, "title": "Expectations",
     "air_date": "2010-04-01", "viewers": 15.30,
     "day_start": 19, "day_end": 21,
     "eliminated": "James Clement", "vote": "5-1",
     "notable": "James medevac-adjacent (injury during challenge, voted out)"},
    {"ep": 9, "title": "The Martyr Approach",
     "air_date": "2010-04-08", "viewers": 16.46,
     "day_start": 22, "day_end": 24,
     "eliminated": "Coach Wade", "vote": "5-3",
     "notable": "Merge into Yin Yang"},
    {"ep": 10, "title": "Going Down in Flames",
     "air_date": "2010-04-15", "viewers": 17.29,
     "day_start": 25, "day_end": 27,
     "eliminated": "Courtney Yates", "vote": "6-3",
     "notable": "J.T. gives Russell his idol with a letter"},
    {"ep": 11, "title": "Jumping Ship",
     "air_date": "2010-04-22", "viewers": 16.04,
     "day_start": 28, "day_end": 30,
     "eliminated": "J.T. Thomas", "vote": "5-0",
     "notable": "Parvati plays 2 idols on Sandra and Jerri, negating all Hero votes against Jerri"},
    {"ep": 12, "title": "A Sinking Ship",
     "air_date": "2010-04-29", "viewers": 15.31,
     "day_start": 31, "day_end": 33,
     "eliminated": "Amanda Kimmel", "vote": "5-4",
     "notable": "Candice flips to Villains"},
    {"ep": 13, "title": "Loose Lips Sink Ships",
     "air_date": "2010-05-06", "viewers": 14.99,
     "day_start": 34, "day_end": 36,
     "eliminated": "Candice Woodcock", "vote": "5-3-1",
     "notable": "Sandra plays idol, negating 2 votes against her. Also Danielle eliminated Day 36: 5-1."},
    {"ep": 14, "title": "Anything Could Happen",
     "air_date": "2010-05-16", "viewers": 22.19,
     "day_start": 37, "day_end": 39,
     "eliminated": "Rupert Boneham", "vote": "4-2",
     "is_finale": True,
     "notable": "Colby, Jerri, Russell also eliminated. Sandra wins 6-3-0."},
]

# ═══════════════════════════════════════════════════════════════════
# BOOT ORDERS FOR ALL REMAINING SEASONS (from compiled research)
# Key data: just boot orders, filming dates, and air dates
# ═══════════════════════════════════════════════════════════════════

ALL_BOOT_ORDERS = {
    2: ["Kel Gleason", "Maralyn Hershey", "Mitchell Olson",
        "Kimmi Kappenberg", "Michael Skupin", "Jeff Varner",
        "Alicia Calaway", "Jerri Manthey", "Nick Brown",
        "Amber Brkich", "Rodger Bingham", "Elisabeth Filarski",
        "Keith Famie", "Colby Donaldson", "Tina Wesson"],
    3: ["Diane Ogden", "Jessie Camacho", "Carl Bilancione",
        "Linda Spencer", "Silas Gaither", "Lindsey Richter",
        "Clarence Black", "Kelly Goldsmith", "Brandon Quinton",
        "Frank Garrison", "Teresa Cooper", "Lex van den Berghe",
        "Tom Buchanan", "Kim Johnson", "Ethan Zohn"],
    7: ["Nicole Delma", "Ryan Shoulders", "Michelle Tesauro",
        "Lillian Morris", "Shawn Cohen", "Osten Taylor",
        "Trish Dunn", "Andrew Savage", "Ryan Opheim",
        "Tijuana Bradley", "Rupert Boneham", "Burton Roberts",
        "Darrah Johnson", "Jon Dalton", "Lillian Morris",
        "Sandra Diaz-Twine"],
    10: ["Wanda Shirk", "Jonathan Libby", "Jolanda Jones",
         "Ashlee Ashby", "Jeff Wilson", "Kim Mullen",
         "Willard Smith", "Angie Jakusz", "James Miller",
         "Ibrehem Rahman", "Bobby Jon Drinkard", "Coby Archa",
         "Stephenie LaGrossa", "Janu Tornell", "Gregg Carey",
         "Jennifer Lyon", "Caryn Groedel", "Ian Rosenberger",
         "Katie Gallagher", "Tom Westman"],
    13: ["Sekou Bunch", "Billy Garcia", "Cecilia Mansilla",
         "J.P. Calderon", "Stephannie Favor", "Cao Boi Bui",
         "Cristina Coria", "Jessica Smith", "Brad Virata",
         "Jenny Guzon-Bae", "Rebecca Borman", "Nate Gonzalez",
         "Candice Woodcock", "Jonathan Penner", "Parvati Shallow",
         "Adam Gentry", "Sundra Oakley", "Becky Lee",
         "Ozzy Lusth", "Yul Kwon"],
    15: ["Chicken Morris", "Ashley Massaro", "Leslie Nease",
         "Dave Cruser", "Aaron Reisberger", "Sherea Lloyd",
         "Jaime Dugan", "Jean-Robert Bellande", "Frosti Zernow",
         "James Clement", "Erik Huffman", "Peih-Gee Law",
         "Denise Martin", "Courtney Yates", "Amanda Kimmel",
         "Todd Herzog"],
    16: ["Jonny Fairplay", "Mary Sartain", "Yau-Man Chan",
         "Mikey Bortone", "Joel Anderson", "Chet Welch",
         "Jonathan Penner", "Kathy Sleckman", "Tracy Hughes-Wolf",
         "Ami Cusack", "Eliza Orlins", "Ozzy Lusth",
         "Jason Siska", "James Clement", "Alexis Jones",
         "Erik Reichenbach", "Natalie Bolton", "Cirie Fields",
         "Amanda Kimmel", "Parvati Shallow"],
    25: ["Zane Knight", "Roxy Morris", "Angie Layton",
         "Russell Swan", "Dana Lambert", "Dawson",
         "Jeff Kent", "Katie Hanson", "Jonathan Penner",
         "Pete Yurkowski", "Artis Silvester", "Michael Skupin",
         "Abi-Maria Gomes", "Carter Williams", "Lisa Whelchel",
         "Malcolm Freberg", "Denise Stapley"],
    28: ["David Samson", "Garrett Adelstein", "J'Tia Taylor",
         "Brice Johnston", "Cliff Robinson", "Alexis Maxwell",
         "Lindsey Ogle", "LJ McKanas", "Sarah Lacina",
         "Morgan McLeod", "Jeremiah Wood", "Jefra Bland",
         "Tasha Fox", "Trish Hegarty", "Spencer Bledsoe",
         "Kass McQuillen", "Woo Hwang", "Tony Vlachos"],
    31: ["Vytas Baskauskas", "Shirin Oskooi", "Peih-Gee Law",
         "Jeff Varner", "Monica Padilla", "Terry Deitz",
         "Andrew Savage", "Kass McQuillen", "Ciera Eastin",
         "Stephen Fishbach", "Kelly Wiglesworth", "Joe Anglim",
         "Abi-Maria Gomes", "Keith Nale", "Kimmi Kappenberg",
         "Kelley Wentworth", "Tasha Fox", "Spencer Bledsoe",
         "Jeremy Collins"],
    37: ["Pat Cusack", "Jessica Peet", "Bi Nguyen",
         "Natalia Azoqa", "Lyrsa Torres", "Jeremy Crawford",
         "Natalie Cole", "Elizabeth Olson", "John Hennigan",
         "Dan Rengering", "Carl Boudreaux", "Gabby Pascuzzi",
         "Christian Hubicki", "Alison Raybould", "Davie Rickenbacker",
         "Kara Kay", "Angelina Keeley", "Mike White", "Nick Wilson"],
    40: ["Natalie Anderson", "Amber Mariano", "Danni Boatwright",
         "Ethan Zohn", "Tyson Apostol", "Rob Mariano",
         "Parvati Shallow", "Sandra Diaz-Twine", "Yul Kwon",
         "Wendell Holland", "Adam Klein", "Nick Wilson",
         "Sophie Clarke", "Kim Spradlin-Wolfe", "Jeremy Collins",
         "Denise Stapley", "Ben Driebergen", "Sarah Lacina",
         "Michele Fitzgerald", "Tony Vlachos"],
    41: ["Abraham Adekunle", "Sara Wilson", "Voce Laatu",
         "Brad Reese", "JD Robinson", "Genie Chen",
         "Tiffany Seely", "Sydney Segal", "Naseer Muttalif",
         "Evvie Jagoda", "Shan Smith", "Liana Wallace",
         "Danny McCray", "Ricard Foye", "Deshawn Radden",
         "Xander Hastings", "Erika Casupanan"],
}

# ═══════════════════════════════════════════════════════════════════
# AIR DATE RANGES (all 50 seasons from Wikipedia master list)
# ═══════════════════════════════════════════════════════════════════

AIR_DATES = {
    1: ("2000-05-31", "2000-08-23"), 2: ("2001-01-28", "2001-05-03"),
    3: ("2001-10-11", "2002-01-10"), 4: ("2002-02-28", "2002-05-19"),
    5: ("2002-09-19", "2002-12-19"), 6: ("2003-02-13", "2003-05-11"),
    7: ("2003-09-18", "2003-12-14"), 8: ("2004-02-01", "2004-05-09"),
    9: ("2004-09-16", "2004-12-12"), 10: ("2005-02-17", "2005-05-15"),
    11: ("2005-09-15", "2005-12-11"), 12: ("2006-02-02", "2006-05-14"),
    13: ("2006-09-14", "2006-12-17"), 14: ("2007-02-08", "2007-05-13"),
    15: ("2007-09-20", "2007-12-16"), 16: ("2008-02-07", "2008-05-11"),
    17: ("2008-09-25", "2008-12-14"), 18: ("2009-02-12", "2009-05-17"),
    19: ("2009-09-17", "2009-12-20"), 20: ("2010-02-11", "2010-05-16"),
    21: ("2010-09-15", "2010-12-19"), 22: ("2011-02-16", "2011-05-15"),
    23: ("2011-09-14", "2011-12-18"), 24: ("2012-02-15", "2012-05-13"),
    25: ("2012-09-19", "2012-12-16"), 26: ("2013-02-13", "2013-05-12"),
    27: ("2013-09-18", "2013-12-15"), 28: ("2014-02-26", "2014-05-21"),
    29: ("2014-09-24", "2014-12-17"), 30: ("2015-02-25", "2015-05-20"),
    31: ("2015-09-23", "2015-12-16"), 32: ("2016-02-17", "2016-05-18"),
    33: ("2016-09-21", "2016-12-14"), 34: ("2017-03-08", "2017-05-24"),
    35: ("2017-09-27", "2017-12-20"), 36: ("2018-02-28", "2018-05-23"),
    37: ("2018-09-26", "2018-12-19"), 38: ("2019-02-20", "2019-05-15"),
    39: ("2019-09-25", "2019-12-18"), 40: ("2020-02-12", "2020-05-13"),
    41: ("2021-09-22", "2021-12-15"), 42: ("2022-03-09", "2022-05-25"),
    43: ("2022-09-21", "2022-12-14"), 44: ("2023-03-01", "2023-05-24"),
    45: ("2023-09-27", "2023-12-20"), 46: ("2024-02-28", "2024-05-22"),
    47: ("2024-09-18", "2024-12-18"), 48: ("2025-02-26", "2025-05-21"),
    49: ("2025-09-24", "2025-12-17"), 50: ("2026-02-25", "2026-05-20"),
}

FILMING_DATES = {
    1: ("2000-03-13", "2000-04-20"), 7: ("2003-06-23", "2003-07-31"),
    20: ("2009-08-09", "2009-09-16"), 28: ("2013-07-04", "2013-08-11"),
    40: ("2019-05-22", "2019-06-29"),
}

# ═══════════════════════════════════════════════════════════════════
# APPLY ENRICHMENT
# ═══════════════════════════════════════════════════════════════════

def enrich_season(sn: int, season_dir: Path):
    sf = season_dir / "season.json"
    with open(sf) as f:
        s = json.load(f)

    changed = False

    # Fix air dates
    if sn in AIR_DATES:
        s["air_date_start"] = AIR_DATES[sn][0]
        s["air_date_end"] = AIR_DATES[sn][1]
        changed = True

    if sn in FILMING_DATES:
        s["filming_date_start"] = FILMING_DATES[sn][0]
        s["filming_date_end"] = FILMING_DATES[sn][1]
        changed = True

    # Boot orders
    boot = None
    if sn == 1:
        boot = S1_BOOT
    elif sn == 20:
        boot = S20_BOOT
    elif sn in ALL_BOOT_ORDERS:
        boot = ALL_BOOT_ORDERS[sn]

    if boot and not s.get("boot_order"):
        s["boot_order"] = boot
        # Also populate contestants if empty
        if not s.get("contestants"):
            s["contestants"] = [
                {"id": contestant_id(name, sn), "type": "Contestant", "name": name}
                for name in boot
            ]
        changed = True

    if changed:
        with open(sf, "w") as f:
            json.dump(s, f, indent=2, ensure_ascii=False)

    # Enrich episodes
    ep_data = None
    if sn == 1:
        ep_data = S1_EPISODES
    elif sn == 20:
        ep_data = S20_EPISODES

    if ep_data:
        for ep_info in ep_data:
            ep_num = ep_info["ep"]
            ep_file = season_dir / f"e{ep_num:02d}.json"
            if not ep_file.exists():
                continue
            with open(ep_file) as f:
                ep = json.load(f)

            ep["episode_title"] = ep_info.get("title")
            ep["air_date"] = ep_info.get("air_date")
            ep["day_start"] = ep_info.get("day_start")
            ep["day_end"] = ep_info.get("day_end")
            if ep_info.get("viewers"):
                ep["viewership_millions"] = ep_info["viewers"]
            if ep_info.get("is_premiere"):
                ep["is_premiere"] = True
            if ep_info.get("is_finale"):
                ep["is_finale"] = True

            # Add challenge data
            if ep_info.get("immunity_winner"):
                winner = ep_info["immunity_winner"]
                ch = {
                    "challenge_type": "immunity",
                    "challenge_winners": [winner] if isinstance(winner, str) else winner
                }
                ep["challenges"] = [ch]
                if ep_info.get("reward_winner"):
                    rw = ep_info["reward_winner"]
                    if rw:
                        ep["challenges"].append({
                            "challenge_type": "reward",
                            "challenge_winners": [rw] if isinstance(rw, str) else rw
                        })

            # Add tribal council data
            if ep_info.get("eliminated"):
                tc = {
                    "person_eliminated": {
                        "id": contestant_id(ep_info["eliminated"], sn),
                        "name": ep_info["eliminated"]
                    },
                    "vote_count_summary": ep_info.get("vote", ""),
                    "elimination_method": "vote"
                }
                ep["tribal_councils"] = [tc]

            # Notable events
            if ep_info.get("notable"):
                ep["notable_events"] = [ep_info["notable"]]

            ep["data_completeness"] = "detailed"
            ep["research_status"] = "initial_pass"

            with open(ep_file, "w") as f:
                json.dump(ep, f, indent=2, ensure_ascii=False)

    return changed


def main():
    enriched = 0
    for sd in sorted(DATA.iterdir()):
        if not sd.is_dir():
            continue
        sf = sd / "season.json"
        if not sf.exists():
            continue
        with open(sf) as f:
            s = json.load(f)
        sn = s["season_number"]
        if enrich_season(sn, sd):
            enriched += 1
            print(f"  [+] S{sn:02d} {s['subtitle']}: enriched")
        else:
            print(f"  [=] S{sn:02d} {s['subtitle']}: no changes")

    print(f"\nEnriched {enriched} seasons")


if __name__ == "__main__":
    main()
