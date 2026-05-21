#!/usr/bin/env python3
"""Final episode enrichment: S36-S50 with titles, dates, viewership."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

D = {
    36: [(1,"Can You Reverse the Curse?","2018-02-28",7.92),(2,"Only Time Will Tell","2018-03-07",7.61),
         (3,"Trust Your Gut","2018-03-14",7.72),(4,"Fate is the Homie","2018-03-21",7.36),
         (5,"SeaBass","2018-03-28",7.72),(6,"A Numbers Game","2018-04-04",7.32),
         (7,"It's Like a Survivor Economy","2018-04-11",7.85),(8,"Fear Keeps You Sharp","2018-04-18",7.58),
         (9,"The Sea Slug Slugger","2018-04-25",7.52),(10,"It's Like the Perfect Crime","2018-05-02",7.55),
         (11,"The Finish Line Is in Sight","2018-05-09",7.19),(12,"Always Be Moving","2018-05-16",7.38),
         (13,"A Perfect Game","2018-05-23",7.39),(14,"Reunion","2018-05-23",5.61)],
    37: [(1,"Appearances Are Deceiving","2018-09-26",7.72),(2,"The Chicken Has Flown the Coop","2018-10-03",7.33),
         (3,"I Am Goliath Strong","2018-10-10",7.21),(4,"Time to Bring About the Charmpocalypse","2018-10-17",7.15),
         (5,"Jackets and Eggs","2018-10-24",7.20),(6,"Aren't Brochachos Just Adorable?","2018-10-31",6.73),
         (7,"There's Gonna Be Tears Shed","2018-11-07",7.57),(8,"You Get What You Give","2018-11-14",7.46),
         (9,"Breadth-First Search","2018-11-21",7.22),(10,"Tribal Lines Are Blurred","2018-11-28",7.48),
         (11,"So Smart They're Dumb","2018-12-05",7.40),(12,"Are You Feeling Lucky?","2018-12-12",7.57),
         (13,"With Great Power Comes Great Responsibility","2018-12-19",7.81),(14,"Reunion","2018-12-19",5.88)],
    38: [(1,"It Smells Like Success","2019-02-20",7.28),(2,"One of Us Is Going to Win","2019-02-27",6.73),
         (3,"Betrayals Are Going to Get Exposed","2019-03-06",6.92),(4,"I Need a Dance Partner","2019-03-13",6.53),
         (5,"It's Like the Worst Cocktail Party Ever","2019-03-20",6.63),
         (6,"There's Always a Twist","2019-03-27",6.86),(7,"I'm the Puppet Master","2019-04-03",6.47),
         (8,"Y'all Making Me Crazy","2019-04-10",6.49),(9,"Blood of a Blindside","2019-04-17",6.41),
         (10,"Faulty Vote","2019-04-24",6.42),(11,"Awkward","2019-05-01",6.57),
         (12,"Idol or Bust","2019-05-08",6.37),(13,"Survivor at 40: Greatest Moments and Players","2019-05-08",5.82),
         (14,"I See the Million Dollars","2019-05-15",6.95)],
    39: [(1,"I Vote You Out and That's It","2019-09-25",6.68),(2,"YOLO, Let's Play!","2019-10-02",6.45),
         (3,"Honesty Would Be Chill","2019-10-09",6.49),(4,"Plan Z","2019-10-16",6.44),
         (5,"Don't Bite the Hand That Feeds You","2019-10-23",6.43),
         (6,"Voce del Popolo","2019-10-30",5.75),(7,"I Was Born at Night, but Not Last Night","2019-11-06",6.52),
         (8,"We Made It to the Merge!","2019-11-13",6.36),(9,"Two for the Price of One","2019-11-20",6.39),
         (10,"Bring On the Bacon","2019-11-27",5.98),(11,"A Little Bit of Hustle","2019-12-04",6.14),
         (12,"One, Two, Three, Four, I Declare a Thumb War","2019-12-11",6.39),
         (13,"Mama, Look at Me Now","2019-12-18",6.32),(14,"Reunion","2019-12-18",5.03)],
    40: [(1,"Greatest of the Greats","2020-02-12",6.68),(2,"It's Like a Survivor Economy","2020-02-19",6.14),
         (3,"Out for Blood","2020-02-26",5.90),(4,"I Like Revenge","2020-03-04",5.82),
         (5,"The Buddy System on Steroids","2020-03-11",6.07),(6,"Quick on the Draw","2020-03-18",5.93),
         (7,"We're in the Majors","2020-03-25",5.68),(8,"This is Where the Battle Begins","2020-04-01",5.69),
         (9,"War is Not Pretty","2020-04-08",5.87),(10,"The Full Circle","2020-04-15",5.67),
         (11,"This Is Extortion","2020-04-22",5.56),(12,"Friendly Fire","2020-04-29",5.75),
         (13,"The Penultimate Step of the War","2020-05-06",5.54),
         (14,"It All Boils Down to This","2020-05-13",5.70),
         (15,"Reunion","2020-05-13",4.34),(16,"Reunion (Extended)","2020-05-13",None)],
    41: [(1,"A New Era","2021-09-22",6.25),(2,"Juggling Chainsaws","2021-09-29",5.90),
         (3,"My Million Dollar Mistake","2021-10-06",5.79),
         (4,"They Hate Me Because They Ain't Me","2021-10-13",5.67),
         (5,"The Strategist or The Loyalist","2021-10-20",5.62),
         (6,"Ready to Play Like a Lion","2021-10-27",5.32),
         (7,"There's Gonna Be Blood","2021-11-03",5.47),(8,"Betraydar","2021-11-10",5.56),
         (9,"Who's Who in the Zoo","2021-11-17",5.76),
         (10,"Baby with a Machine Gun","2021-11-24",5.54),
         (11,"Do or Die","2021-12-01",5.63),(12,"Truth Kamikaze","2021-12-08",5.70),
         (13,"One Thing Left to Do... Win","2021-12-15",5.62)],
    42: [(1,"Feels Like a Rollercoaster","2022-03-09",4.96),(2,"Good and Guilty","2022-03-16",5.06),
         (3,"Go for the Gusto","2022-03-23",5.35),(4,"Vibe of the Tribe","2022-03-30",5.63),
         (5,"I'm Survivor Rich","2022-04-06",5.58),(6,"You Can't Hide on Survivor","2022-04-13",5.12),
         (7,"The Devil You Do or The Devil You Don't","2022-04-13",5.12),
         (8,"You Better Be Wearing a Seatbelt","2022-04-20",5.43),
         (9,"Game of Chicken","2022-04-27",5.72),(10,"Tell a Good Lie, Not a Stupid Lie","2022-05-04",5.62),
         (11,"Battle Royale","2022-05-11",5.38),(12,"Caterpillar to a Butterfly","2022-05-18",5.70),
         (13,"It Comes Down to This","2022-05-25",5.11)],
    43: [(1,"LIVIN","2022-09-21",5.05),(2,"Lovable Curmudgeon","2022-09-28",4.57),
         (3,"I'll Sign the Divorce Papers","2022-10-05",5.15),(4,"Show No Mercy","2022-10-12",5.03),
         (5,"Stop with All the Niceness","2022-10-19",4.91),(6,"Mergatory","2022-10-26",5.17),
         (7,"Bull in a China Shop","2022-11-02",4.64),(8,"Proposterous","2022-11-09",4.73),
         (9,"What About the Big Girls","2022-11-16",5.15),(10,"Get That Money, Baby","2022-11-23",4.89),
         (11,"Hiding in Plain Sight","2022-11-30",5.31),(12,"Telenovela","2022-12-07",5.34),
         (13,"Snap Some Necks and Cash Some Checks","2022-12-14",4.98)],
    44: [(1,"I Can't Wait to See Jeff","2023-03-01",4.76),(2,"Two Dorky Magnets","2023-03-08",4.95),
         (3,"Sneaky Little Snake","2023-03-15",4.99),(4,"I'm Felicia","2023-03-22",5.19),
         (5,"The Third Turd","2023-03-29",5.25),(6,"Survivor with a Capital S","2023-04-05",5.19),
         (7,"Let's Not Be Cute About It","2023-04-12",5.34),
         (8,"Don't Get Cocky, Kid","2023-04-19",5.29),
         (9,"Under the Wing of a Dragon","2023-04-26",5.22),
         (10,"Full Tilt Boogie","2023-05-03",4.96),(11,"I'm Not Worthy","2023-05-10",4.78),
         (12,"I'm the Bandit","2023-05-17",4.71),(13,"Absolute Banger Season","2023-05-24",4.41)],
    45: [(1,"We Can Do Hard Things","2023-09-27",5.24),
         (2,"Brought a Bazooka to a Tea Party","2023-10-04",4.88),
         (3,"No Man Left Behind","2023-10-11",5.09),(4,"Music to My Ears","2023-10-18",4.92),
         (5,"I Don't Want to Be the Worm","2023-10-25",5.03),
         (6,"I'm Not Batman, I'm the Canadian","2023-11-01",4.86),
         (7,"The Thorn in My Thumb","2023-11-08",4.53),
         (8,"Following a Dead Horse to Water","2023-11-15",5.14),
         (9,"Sword of Damocles","2023-11-22",4.90),(10,"How Am I the Mobster?","2023-11-29",5.02),
         (11,"This Game Rips Your Heart Out","2023-12-06",4.84),
         (12,"The Ex-Girlfriend at the Wedding","2023-12-13",5.33),
         (13,"Living the Survivor Dream","2023-12-20",4.73)],
    46: [(1,"This is Where the Legends are Made","2024-02-28",4.90),
         (2,"Scorpio Energy","2024-03-06",4.43),(3,"Wackadoodles Win","2024-03-13",4.78),
         (4,"Don't Touch the Oven","2024-03-20",4.68),(5,"Tiki Man","2024-03-27",4.72),
         (6,"Cancel Christmas","2024-04-03",5.05),(7,"Episode Several","2024-04-10",4.64),
         (8,"Hide 'N Seek","2024-04-17",4.84),(9,"Spicy Jeff","2024-04-24",4.91),
         (10,"Run the Red Light","2024-05-01",4.79),
         (11,"My Messy, Sweet Little Friend","2024-05-08",4.69),
         (12,"Mamma Bear","2024-05-15",4.71),(13,"Friends Going to War","2024-05-22",4.51)],
    47: [(1,"One Glorious and Perfect Episode","2024-09-18",4.72),
         (2,"Epic Boss Girl Move","2024-09-25",4.47),(3,"Belly of the Beast","2024-10-02",4.34),
         (4,"Is That Blood in Your Hair","2024-10-09",4.14),
         (5,"The Scales Be Tippin","2024-10-16",4.02),(6,"Feel the FOMO","2024-10-23",4.35),
         (7,"Our Pickle on Blast","2024-10-30",4.24),(8,"He's All That","2024-11-06",4.64),
         (9,"Nightmare Fuel","2024-11-13",4.43),(10,"Loyal to the Soil","2024-11-20",4.42),
         (11,"Flipping the Win Switch","2024-11-27",4.50),(12,"Operation: Italy","2024-12-04",4.60),
         (13,"Bob and Weave","2024-12-11",4.89)],
    48: [(1,"The Get to Know You Game","2025-02-26",4.27),(2,"Humble Traits","2025-03-05",4.31),
         (3,"Committing to the Bit","2025-03-12",4.63),(4,"The House Party's Over","2025-03-19",4.70),
         (5,"Master Class in Deception","2025-03-26",4.77),(6,"Doing the Damn Thing","2025-04-02",4.77),
         (7,"Survivor Smack Talk","2025-04-09",4.89),(8,"A Rift Between All of Us","2025-04-16",4.79),
         (9,"Welcome to the Party","2025-04-23",4.58),(10,"My Enemies Are Plottin'","2025-04-30",4.59),
         (11,"Coconut Etiquette","2025-05-07",4.43),(12,"Icarus Time","2025-05-14",4.90),
         (13,"Only One of Yous Can Win","2025-05-21",4.56)],
    49: [(1,"Act One of a Horror Film","2025-09-24",4.03),(2,"Cinema","2025-10-01",4.03),
         (3,"Loveable Losers","2025-10-08",4.23),(4,"Go Kick Rocks, Bro","2025-10-15",4.27),
         (5,"I'm a Wolf, Baby","2025-10-22",4.36),(6,"The Devil's Shoes","2025-10-29",4.25),
         (7,"Blood Will Be Drawn","2025-11-05",4.37),(8,"Hot Grim Reaper","2025-11-12",3.90),
         (9,"If You're Loyal to All, You're Loyal to None","2025-11-19",4.17),
         (10,"Huge Dose of Bamboozle","2025-11-26",4.25),(11,"Cherry On Top","2025-12-03",4.41),
         (12,"The Die Is Cast","2025-12-10",4.77),(13,"A Fever Dream","2025-12-17",4.45)],
    50: [(1,"Epic Party","2026-02-25",5.06),(2,"Therapy Carousel","2026-03-04",4.95),
         (3,"Did You Vote For a Swap?","2026-03-11",4.88),(4,"Knife to the Heart","2026-03-18",5.22),
         (5,"Open Wounds","2026-03-25",5.10),(6,"The Blood Moon","2026-04-01",None),
         (7,"That's Not How I Play Survivor","2026-04-08",None),
         (8,"TBA","2026-04-15",None),(9,"TBA","2026-04-22",None),
         (10,"TBA","2026-04-29",None),(11,"TBA","2026-05-06",None),
         (12,"TBA","2026-05-13",None),(13,"TBA","2026-05-20",None),
         (14,"Reunion","2026-05-20",None)],
}

def find_dir(sn):
    for d in DATA.iterdir():
        if d.name.startswith(f"season-{sn:02d}-"): return d
    return None

def main():
    total = 0
    for sn, eps in sorted(D.items()):
        sd = find_dir(sn)
        if not sd: print(f"  [!] S{sn}: not found"); continue
        count = 0
        for ep_num, title, air_date, viewers in eps:
            ef = sd / f"e{ep_num:02d}.json"
            if not ef.exists(): continue
            with open(ef) as f: ep = json.load(f)
            ch = False
            if not ep.get("episode_title") and title != "TBA":
                ep["episode_title"] = title; ch = True
            if not ep.get("air_date"):
                ep["air_date"] = air_date; ch = True
            if viewers and not ep.get("viewership_millions"):
                ep["viewership_millions"] = viewers; ch = True
            if ep.get("data_completeness") == "stub" and ch:
                ep["data_completeness"] = "season-level"
                ep["research_status"] = "initial_pass"
            if ep_num == len(eps): ep["is_finale"] = True
            if ch:
                with open(ef, "w") as f: json.dump(ep, f, indent=2, ensure_ascii=False)
                count += 1
        if count: print(f"  [+] S{sn:02d}: {count} episodes"); total += count
        else: print(f"  [=] S{sn:02d}: done")
    print(f"\nTotal: {total}")

if __name__ == "__main__": main()
