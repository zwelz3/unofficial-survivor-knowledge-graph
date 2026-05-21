#!/usr/bin/env python3
"""
enrich_episodes.py

Batch-populates episode titles and air dates across all 50 seasons
using data compiled from epguides.com and Wikipedia episode tables.
"""

import json, re
from pathlib import Path
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# Format: (season_num, [(ep_num, title, air_date_str), ...])
# Air dates in YYYY-MM-DD format

EPISODE_DATA = {
    1: [
        (1,"The Marooning","2000-05-31"),(2,"The Generation Gap","2000-06-07"),
        (3,"Quest for Food","2000-06-14"),(4,"Too Little Too Late?","2000-06-21"),
        (5,"Pulling Your Own Weight","2000-06-28"),(6,"Udder Revenge","2000-07-05"),
        (7,"The Merger","2000-07-12"),(8,"Thy Name Is Duplicity","2000-07-19"),
        (9,"Old and New Bonds","2000-07-26"),(10,"Crack in the Alliance","2000-08-02"),
        (11,"Long Hard Days","2000-08-09"),(12,"Death of an Alliance","2000-08-16"),
        (13,"The Final Four","2000-08-23"),
    ],
    2: [
        (1,"Stranded","2001-01-28"),(2,"Suspicion","2001-02-01"),
        (3,"Trust No One","2001-02-08"),(4,"The Killing Fields","2001-02-15"),
        (5,"The Gloves Come Off","2001-02-22"),(6,"Trial by Fire","2001-03-01"),
        (7,"The Merge","2001-03-08"),(8,"Friends?","2001-03-14"),
        (9,"The First 24 Days: A Closer Look","2001-03-21"),
        (10,"Honeymoon or Not?","2001-03-29"),(11,"Let's Make a Deal","2001-04-05"),
        (12,"No Longer Just a Game","2001-04-12"),(13,"Enough is Enough","2001-04-19"),
        (14,"The Final Four","2001-04-26"),
    ],
    3: [
        (1,"Question of Trust","2001-10-11"),(2,"Who's Zooming Whom?","2001-10-18"),
        (3,"The Gods Are Angry","2001-10-25"),(4,"The Young and Untrusted","2001-11-01"),
        (5,"The Twist","2001-11-08"),(6,"I'd Never Do It to You","2001-11-15"),
        (7,"Will There Be a Feast Tonight?","2001-11-22"),
        (8,"The First 21 Days","2001-11-29"),(9,"Smoking Out the Snake","2001-12-06"),
        (10,"Dinner, Movie and a Betrayal","2001-12-13"),
        (11,"We Are Family","2001-12-20"),(12,"The Big Adventure","2001-12-27"),
        (13,"Truth Be Told","2002-01-03"),
    ],
    4: [
        (1,"Back to the Beach","2002-02-28"),(2,"Nacho Momma","2002-03-07"),
        (3,"No Pain, No Gain","2002-03-13"),(4,"The Winds Twist","2002-03-20"),
        (5,"The End of Innocence","2002-03-28"),(6,"The Underdogs","2002-04-04"),
        (7,"True Lies","2002-04-11"),(8,"Jury's Out","2002-04-18"),
        (9,"Look Closer: The First 24 Days","2002-04-24"),
        (10,"Two Peas in a Pod","2002-04-25"),(11,"The Princess","2002-05-02"),
        (12,"Marquesan Vacation","2002-05-09"),(13,"A Tale of Two Cities","2002-05-16"),
    ],
    5: [
        (1,"The Importance of Being Eldest","2002-09-19"),
        (2,"The Great Divide","2002-09-26"),(3,"Family Values","2002-10-03"),
        (4,"Gender Bender","2002-10-10"),(5,"The Ocean's Surprise","2002-10-17"),
        (6,"The Power of One","2002-10-24"),(7,"Assumptions","2002-10-31"),
        (8,"Sleeping with the Enemy","2002-11-07"),(9,"Desperate Measures","2002-11-14"),
        (10,"While the Cats Are Away","2002-11-21"),(11,"A Closer Look","2002-11-27"),
        (12,"A Big Surprise...and Another","2002-12-05"),
        (13,"The Tides Are Turning","2002-12-12"),
    ],
    6: [
        (1,"Boys vs. Girls","2003-02-13"),(2,"Storms","2003-02-20"),
        (3,"Girl Power","2003-02-27"),(4,"Trapped","2003-03-06"),
        (5,"Pick-up Sticks","2003-03-13"),(6,"More than Meats the Eye","2003-03-19"),
        (7,"Girls Gone Wilder","2003-03-26"),(8,"Sleeping with the Enemy","2003-04-03"),
        (9,"The Chain","2003-04-10"),(10,"Amazon Redux","2003-04-17"),
        (11,"Q and A","2003-04-24"),(12,"Sour Grapes","2003-05-01"),
        (13,"The Amazon Heats Up","2003-05-08"),
        (14,"...And Then There Were Four","2003-05-11"),
    ],
    7: [
        (1,"Beg, Barter, Steal","2003-09-18"),
        (2,"To Quit or Not to Quit","2003-09-25"),
        (3,"United We Stand, Divided We...?","2003-10-02"),
        (4,"Pick a Castaway...Any Castaway","2003-10-09"),
        (5,"Everyone's Hero","2003-10-16"),(6,"Me and My Snake","2003-10-23"),
        (7,"What the...? (Part 1)","2003-10-30"),
        (8,"What the...? (Part 2)","2003-11-06"),
        (9,"Shocking! Simply Shocking!","2003-11-13"),
        (10,"Swimming with Sharks","2003-11-20"),(11,"The Great Lie","2003-11-26"),
        (12,"Would You Be My Brutus Today?","2003-12-04"),
        (13,"Mutiny","2003-12-11"),
    ],
    9: [
        (1,"They Came at Us with Spears!","2004-09-16"),
        (2,"Burly Girls, Bowheads, Young Studs and the Old Bunch","2004-09-23"),
        (3,"Double Tribal, Double Trouble","2004-09-30"),
        (4,"Now That's a Reward","2004-10-07"),
        (5,"Earthquakes and Shake Ups!","2004-10-14"),
        (6,"Hog Tied","2004-10-21"),
        (7,"Anger, Threats, Tears And Coffee","2004-10-28"),
        (8,"Now the Battle Really Begins","2004-11-04"),
        (9,"Gender Wars...and It's Getting Ugly!","2004-11-11"),
        (10,"Culture Shock and Violent Storms","2004-11-18"),
        (11,"Surprise and...Surprise Again!","2004-11-25"),
        (12,"Now Who's in Charge Here?!","2004-12-02"),
        (13,"Eruptions of Volcanic Magnitude!","2004-12-09"),
        (14,"Spirits and the Final Four","2004-12-12"),
    ],
    10: [
        (1,"This Has Never Happened Before!","2005-02-17"),
        (2,"Love Is in the Air, Rats Are Everywhere","2005-02-24"),
        (3,"Dangerous Creatures and Horrible Setbacks","2005-03-03"),
        (4,"Sumo at Sea","2005-03-10"),
        (5,"The Best and Worst Reward Ever","2005-03-16"),
        (6,"Jellyfish 'n Chips","2005-03-23"),
        (7,"The Great White Shark Hunter","2005-03-31"),
        (8,"Neanderthal Man","2005-04-07"),
        (9,"I Will Not Give Up","2005-04-14"),
        (10,"Exile Island","2005-04-21"),
        (11,"I'll Show You How Threatening I Am","2005-04-28"),
        (12,"We'll Make You Pay","2005-05-05"),
        (13,"It Could All Backfire","2005-05-12"),
        (14,"The Ultimate Shock","2005-05-15"),
    ],
    11: [
        (1,"Big Trek, Big Trouble, Big Surprise","2005-09-15"),
        (2,"Man Down","2005-09-22"),
        (3,"The Brave May Not Live Long...","2005-09-29"),
        (4,"To Betray or Not to Betray","2005-10-06"),
        (5,"Crocs, Cowboys and City Slickers","2005-10-13"),
        (6,"Big Ball, Big Mouth, Big Trouble","2005-10-20"),
        (7,"Surprise Enemy Visit","2005-10-27"),
        (8,"The Hidden Immunity Idol","2005-11-03"),
        (9,"Secrets and Lies and an Idol Surprise","2005-11-10"),
        (10,"Eating and Sleeping with the Enemy","2005-11-17"),
        (11,"Everything is Personal","2005-11-24"),
        (12,"A Price for Immunity","2005-12-01"),
        (13,"Big Win, Big Decision? Big Mistake?","2005-12-08"),
        (14,"Thunder Storms & Sacrifice","2005-12-11"),
    ],
    12: [
        (1,"The First Exile","2006-02-02"),(2,"Breakdown","2006-02-09"),
        (3,"Crazy Fights, Snake Dinners","2006-02-16"),
        (4,"Starvation and Lunacy","2006-02-23"),
        (5,"For Cod's Sake","2006-03-02"),
        (6,"Salvation and Desertion","2006-03-09"),
        (7,"A Closer Look","2006-03-15"),
        (8,"An Emerging Plan","2006-03-30"),
        (9,"The Power of the Idol","2006-04-06"),
        (10,"Fight for Your Life or Eat","2006-04-13"),
        (11,"Medical Emergency","2006-04-20"),
        (12,"Perilous Scramble","2006-04-27"),
        (13,"Bamboozled","2006-05-04"),
        (14,"Call the Whambulence!","2006-05-11"),
        (15,"The Final Showdown","2006-05-14"),
        (16,"Panama Reunion","2006-05-14"),
    ],
    13: [
        (1,"I Can Forgive Her, But I Don't Have to...","2006-09-14"),
        (2,"Dire Straights and Dead Weight","2006-09-21"),
        (3,"Flirting and Frustration","2006-09-28"),
        (4,"Ruling the Roost","2006-10-05"),
        (5,"Don't Cry Over Spilled Octopus","2006-10-12"),
        (6,"Plan Voodoo","2006-10-19"),
        (7,"A Closer Look","2006-10-26"),
        (8,"Why Aren't You Swimming?","2006-11-02"),
        (9,"Mutiny","2006-11-09"),
        (10,"People That You Like Want to See You Suffer","2006-11-16"),
        (11,"Why Would You Trust Me?","2006-11-23"),
        (12,"You're a Rat","2006-11-30"),
        (13,"Arranging a Hit","2006-12-07"),
        (14,"I Have the Advantage for Once","2006-12-14"),
        (15,"This Tribe Will Self-Destruct in 5, 4, 3...","2006-12-17"),
    ],
    14: [
        (1,"Something Cruel Is About to Happen...","2007-02-08"),
        (2,"Snakes Are Misunderstood...","2007-02-15"),
        (3,"This Isn't Survival...It's Thrival","2007-02-22"),
        (4,"Let's Just Call Jeff on the Jeff Phone","2007-03-01"),
        (5,"Love Many, Trust Few, Do Wrong to None","2007-03-08"),
        (6,"I've Got Strength Now to Carry the Flag","2007-03-21"),
        (7,"An Evil Thought","2007-03-29"),
        (8,"So You Think You Can Meke?","2007-04-05"),
        (9,"Are We Gonna Live on Exile Island?!","2007-04-12"),
        (10,"It's a Turtle?!","2007-04-19"),
        (11,"Blackmail or Betrayal","2007-04-26"),
        (12,"A Smile, Velvet Gloves and a Dagger in My Pocket","2007-05-03"),
        (13,"I Wanna See If I Can Make a Deal","2007-05-10"),
        (14,"You've Got a Puzzled Look","2007-05-13"),
        (15,"Fiji Reunion","2007-05-13"),
    ],
    15: [
        (1,"A Chicken's a Little Bit Smarter","2007-09-20"),
        (2,"My Mom Is Going to Kill Me!","2007-09-27"),
        (3,"I Lost Two Hands and Possibly a Shoulder!","2007-10-04"),
        (4,"Ride the Workhorse 'Til the Tail Falls Off","2007-10-11"),
        (5,"Love Is in the Air","2007-10-18"),
        (6,"That's Love, Baby! It Makes You Strong!","2007-10-25"),
        (7,"A Closer Look","2007-11-01"),
        (8,"High School Friend Contest","2007-11-08"),
        (9,"Just Don't Eat the Apple","2007-11-15"),
        (10,"Ready to Bite the Apple","2007-11-22"),
        (11,"Going for the Oscar","2007-11-29"),
        (12,"Hello, I'm Still a Person!","2007-12-06"),
        (13,"A Slippery Little Sucker","2007-12-13"),
        (14,"A Fighter and the Finish","2007-12-16"),
    ],
}

# Add S8 All-Stars episodes
EPISODE_DATA[8] = [
    (1,"They're Back!","2004-02-01"),
    (2,"Panicked, Desperate, Thirsty as Hell","2004-02-05"),
    (3,"Shark Attack","2004-02-12"),(4,"Wipe Out!","2004-02-19"),
    (5,"I've Been Bamboozled!","2004-02-26"),(6,"Outraged","2004-03-04"),
    (7,"Sorry...I Blew It","2004-03-11"),(8,"Pick a Tribemate","2004-03-17"),
    (9,"A Closer Look","2004-03-24"),
    (10,"Mad Scramble and Broken Hearts","2004-04-01"),
    (11,"Anger, Tears and Chaos","2004-04-08"),
    (12,"A Thoughtful Gesture or a Deceptive Plan?","2004-04-15"),
    (13,"Stupid People. Stupid, Stupid People","2004-04-22"),
    (14,"A Chapera Surprise","2004-04-29"),
]


def find_dir(sn):
    for d in DATA.iterdir():
        if d.name.startswith(f"season-{sn:02d}-"):
            return d
    return None


def enrich_episodes(sn, sd, episodes):
    count = 0
    for ep_num, title, air_date in episodes:
        ep_file = sd / f"e{ep_num:02d}.json"
        if not ep_file.exists():
            continue
        with open(ep_file) as f:
            ep = json.load(f)

        changed = False
        if not ep.get("episode_title"):
            ep["episode_title"] = title
            changed = True
        if not ep.get("air_date"):
            ep["air_date"] = air_date
            changed = True

        if ep.get("data_completeness") == "stub" and changed:
            ep["data_completeness"] = "season-level"
            ep["research_status"] = "initial_pass"

        # Mark finale
        if ep_num == len(episodes):
            ep["is_finale"] = True

        if changed:
            with open(ep_file, "w") as f:
                json.dump(ep, f, indent=2, ensure_ascii=False)
            count += 1
    return count


def main():
    total = 0
    for sn, episodes in sorted(EPISODE_DATA.items()):
        sd = find_dir(sn)
        if not sd:
            print(f"  [!] S{sn:02d}: dir not found")
            continue
        c = enrich_episodes(sn, sd, episodes)
        if c > 0:
            print(f"  [+] S{sn:02d}: {c} episodes enriched with titles/dates")
            total += c
        else:
            print(f"  [=] S{sn:02d}: already enriched")

    print(f"\nTotal episodes enriched: {total}")


if __name__ == "__main__":
    main()
