#!/usr/bin/env python3
"""
enrich_episodes_p2.py

Batch episode title/date/viewership enrichment for seasons 16-40.
Source: Wikipedia episode list pages.
"""

import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

EPISODE_DATA = {
    16: [ # Micronesia
        (1,"Under the Radar","2008-02-07"),(2,"The Sounds of Jungle Love","2008-02-14"),
        (3,"I Should Be Carried on the Chariot-Type Thing!","2008-02-21"),
        (4,"That's Baked, Barbecued and Fried!","2008-02-28"),
        (5,"He's a Ball of Goo!","2008-03-06"),(6,"It Hit Everyone Pretty Hard","2008-03-13"),
        (7,"A Lost Puppy Dog","2008-03-20"),(8,"A Jason-Type Move","2008-03-27"),
        (9,"I'm in Such a Hot Pickle!","2008-04-03"),
        (10,"I Promise...","2008-04-10"),(11,"A Careful Bunch of People","2008-04-17"),
        (12,"If It Smells Like a Rat, Give It Cheese","2008-04-24"),
        (13,"Stir the Pot!","2008-05-01"),
        (14,"I'm Gonna Fix Her!","2008-05-11"),
    ],
    17: [ # Gabon
        (1,"Want to See the Elephant Dung?","2008-09-25"),
        (2,"She Obviously is Post-Op!","2008-10-02"),
        (3,"It All Depends on the Pin-Up Girl","2008-10-09"),
        (4,"This Camp is Cursed","2008-10-16"),(5,"He's a Snake, But He's My Snake","2008-10-23"),
        (6,"It Was Like Christmas Morning!","2008-10-30"),
        (7,"The Brains Behind Everything","2008-11-06"),
        (8,"The Apple in the Garden of Eden","2008-11-13"),
        (9,"Nothing Tastes Better Than Five Hundred Dollars","2008-11-20"),
        (10,"I Was Put on the Planet for This Show","2008-11-27"),
        (11,"The Good Guys Should Win in the End","2008-12-04"),
        (12,"The Good Things in Life Aren't Easy","2008-12-07"),
        (13,"Say Goodbye to Gabon","2008-12-11"),
        (14,"Reunion","2008-12-14"),
    ],
    18: [ # Tocantins
        (1,"Let's Get Rid of the Weak Players Before We Even Start","2009-02-12"),
        (2,"The Poison Apple Needs to Go","2009-02-19"),
        (3,"Mama Said There'd Be Days Like This","2009-02-26"),
        (4,"The Strongest Man Alive","2009-03-05"),
        (5,"You're Going to Want That Tooth","2009-03-12"),
        (6,"One of Those Coach Moments","2009-03-19"),
        (7,"The First 15 Days","2009-03-26"),
        (8,"The Dragon Slayer","2009-04-02"),
        (9,"Outfoxed by an Amateur","2009-04-09"),
        (10,"It's Funny When People Cry","2009-04-16"),
        (11,"They Both Went Bananas","2009-04-23"),
        (12,"The Martyr Approach","2009-04-30"),
        (13,"I Trust You But I Trust Me More","2009-05-07"),
        (14,"The Biggest Fraud in the Game","2009-05-10"),
        (15,"Tocantins Reunion","2009-05-17"),
    ],
    19: [ # Samoa
        (1,"The Puppet Master","2009-09-17"),(2,"Taking Candy from a Baby","2009-09-24"),
        (3,"It's Called a Russell Seed","2009-10-01"),
        (4,"Hungry for a Win","2009-10-08"),(5,"Walking on Thin Ice","2009-10-15"),
        (6,"This Is the Man Test","2009-10-22"),(7,"Houdini Magic","2009-10-29"),
        (8,"All Hell Breaks Loose","2009-11-05"),(9,"Tastes Like Chicken","2009-11-12"),
        (10,"The Day of Reckoning","2009-11-19"),(11,"The First 27 Days","2009-11-26"),
        (12,"Damage Control","2009-12-03"),(13,"Jumping Ship","2009-12-03"),
        (14,"This Game Ain't Over","2009-12-10"),(15,"Two Brains Are Better Than One","2009-12-17"),
    ],
    21: [ # Nicaragua
        (1,"Young at Heart","2010-09-15"),(2,"Fatigue Makes Cowards of Us All","2010-09-22"),
        (3,"Glitter in Their Eyes","2010-09-29"),(4,"Pulling the Trigger","2010-10-06"),
        (5,"Turf Wars","2010-10-13"),(6,"Worst Case Scenario","2010-10-20"),
        (7,"What Goes Around, Comes Around","2010-10-27"),
        (8,"Company Will Be Arriving Soon","2010-11-03"),
        (9,"Running the Camp","2010-11-10"),(10,"Stuck in the Middle","2010-11-17"),
        (11,"We Did it Guys","2010-11-24"),
        (12,"You Started, You're Finishing","2010-12-01"),
        (13,"Not Sure Where I Stand","2010-12-08"),
        (14,"This is Going to Hurt","2010-12-15"),
        (15,"What About Me?","2010-12-19"),
    ],
    22: [ # Redemption Island
        (1,"You're Looking at the New Leader of Your Tribe","2011-02-16"),
        (2,"You Own My Vote","2011-02-23"),(3,"Keep Hope Alive","2011-03-02"),
        (4,"Don't You Work for Me?","2011-03-09"),(5,"We Hate Our Tribe","2011-03-16"),
        (6,"Their Red-Headed Step Child","2011-03-23"),
        (7,"It Don't Take a Smart One","2011-03-30"),
        (8,"This Game Respects Big Moves","2011-04-06"),
        (9,"The Buddy System","2011-04-13"),(10,"Rice Wars","2011-04-20"),
        (11,"A Mystery Package","2011-04-27"),(12,"You Mangled My Nets","2011-05-04"),
        (13,"Too Close For Comfort","2011-05-11"),
        (14,"Seems Like a No Brainer","2011-05-15"),
        (15,"Reunion","2011-05-15"),
    ],
    23: [ # South Pacific
        (1,"I Need Redemption","2011-09-14"),(2,"He Has Demons","2011-09-21"),
        (3,"Reap What You Sow","2011-09-28"),(4,"Survivalism","2011-10-05"),
        (5,"Taste the Victory","2011-10-12"),(6,"Free Agent","2011-10-19"),
        (7,"Trojan Horse","2011-10-26"),(8,"Double Agent","2011-11-02"),
        (9,"Cut Throat","2011-11-09"),(10,"Running the Show","2011-11-16"),
        (11,"A Closer Look","2011-11-23"),(12,"Cult Like","2011-11-30"),
        (13,"Ticking Time Bomb","2011-12-07"),(14,"Then There Were Five","2011-12-14"),
        (15,"Loyalties Will Be Broken","2011-12-18"),
    ],
    24: [ # One World
        (1,"Two Tribes, One Camp, No Rules","2012-02-15"),
        (2,"Total Dysfunction","2012-02-22"),
        (3,"One World is Out the Window","2012-02-29"),
        (4,"Bum-Puzzled","2012-03-07"),(5,"A Bunch of Idiots","2012-03-14"),
        (6,"Thanks for the Souvenir","2012-03-21"),
        (7,"The Beauty in a Merge","2012-03-28"),
        (8,"Just Annihilate Them","2012-04-04"),(9,"Go Out With a Bang","2012-04-11"),
        (10,"I'm No Dummy","2012-04-18"),(11,"Never Say Die","2012-04-25"),
        (12,"It's Gonna Be Chaos","2012-05-02"),
        (13,"It's Human Nature","2012-05-09"),
        (14,"Perception is Not Always Reality","2012-05-13"),
        (15,"Reunion","2012-05-13"),
    ],
    25: [ # Philippines
        (1,"Survivor Smacked Me in the Chops","2012-09-19"),
        (2,"Don't be Blinded by the Headlights","2012-09-26"),
        (3,"This Isn't a 'We' Game","2012-10-03"),
        (4,"Create a Little Chaos","2012-10-10"),
        (5,"Got My Swag Back","2012-10-17"),(6,"Down and Dirty","2012-10-24"),
        (7,"Not the Only Actor on This Island","2012-10-31"),
        (8,"Dead Man Walking","2012-11-07"),(9,"Little Miss Perfect","2012-11-14"),
        (10,"Whiners are Wieners","2012-11-21"),
        (11,"Hell Hath Frozen Over","2012-11-28"),
        (12,"Shot Into Smithereens","2012-12-05"),
        (13,"Gouge My Eyes Out","2012-12-12"),
        (14,"Million Dollar Question","2012-12-16"),
        (15,"Reunion","2012-12-16"),
    ],
    26: [ # Caramoan
        (1,"She Annoys Me Greatly","2013-02-13"),(2,"Honey Badger","2013-02-20"),
        (3,"There's Gonna Be Hell to Pay","2013-02-27"),
        (4,"Kill or Be Killed","2013-03-06"),(5,"Persona Non Grata","2013-03-13"),
        (6,"Operation Thunder Dome","2013-03-20"),(7,"Tubby Lunchbox","2013-03-27"),
        (8,"Blindside Time","2013-04-03"),
        (9,"Cut Off the Head of the Snake","2013-04-10"),
        (10,"Zipping Over the Cuckoo's Nest","2013-04-17"),
        (11,"Come Over to the Dark Side","2013-04-24"),
        (12,"The Beginning of the End","2013-05-01"),
        (13,"Don't Say Anything About My Mom","2013-05-08"),
        (14,"Last Push","2013-05-12"),
    ],
    27: [ # Blood vs. Water
        (1,"Blood Is Thicker Than Anything","2013-09-18"),
        (2,"Rule In Chaos","2013-09-25"),(3,"Opening Pandora's Box","2013-10-02"),
        (4,"One Armed Dude and Three Moms","2013-10-09"),
        (5,"The Dead Can Still Talk","2013-10-16"),
        (6,"One-Man Wrecking Ball","2013-10-23"),
        (7,"Swoop In For The Kill","2013-10-30"),
        (8,"Skin of My Teeth","2013-11-06"),(9,"My Brother's Keeper","2013-11-13"),
        (10,"Big Bad Wolf","2013-11-20"),(11,"Gloves Come Off","2013-11-27"),
        (12,"Rustle Feathers","2013-12-04"),(13,"Out On a Limb","2013-12-11"),
        (14,"It's My Night","2013-12-15"),
    ],
    28: [ # Cagayan
        (1,"Hot Girl With a Grudge","2014-02-26"),(2,"Cops-R-Us","2014-03-05"),
        (3,"Our Time to Shine","2014-03-12"),(4,"Odd One Out","2014-03-19"),
        (5,"We Found Our Zombies","2014-03-26"),(6,"Head of the Snake","2014-04-02"),
        (7,"Mad Treasure Hunt","2014-04-09"),(8,"Bag of Tricks","2014-04-16"),
        (9,"Sitting In My Spy Shack","2014-04-23"),(10,"Chaos Is My Friend","2014-04-30"),
        (11,"Havoc to Wreak","2014-05-07"),
        (12,"Straw That Broke The Camel's Back","2014-05-14"),
        (13,"It's Do or Die","2014-05-21"),(14,"Reunion","2014-05-21"),
    ],
    29: [ # SJDS
        (1,"Suck It Up and Survive","2014-09-24"),
        (2,"Method To This Madness","2014-10-01"),
        (3,"Actions vs. Accusations","2014-10-08"),(4,"We're a Hot Mess","2014-10-15"),
        (5,"Blood is Blood","2014-10-22"),(6,"Make Some Magic Happen","2014-10-29"),
        (7,"Million Dollar Decision","2014-11-05"),
        (8,"Wrinkle In the Plan","2014-11-12"),
        (9,"Gettin' to Crunch Time","2014-11-19"),
        (10,"This Is Where We Build Trust","2014-11-26"),
        (11,"Kind Of Like Cream Cheese","2014-12-03"),
        (12,"Still Holdin' On","2014-12-03"),
        (13,"Let's Make a Move","2014-12-10"),
        (14,"This Is My Time","2014-12-17"),
    ],
    30: [ # Worlds Apart
        (1,"It's Survivor Warfare","2015-02-25"),
        (2,"It Will Be My Revenge","2015-03-04"),
        (3,"Crazy is as Crazy Does","2015-03-11"),
        (4,"Winner Winner, Chicken Dinner","2015-03-18"),
        (5,"We're Finally Playing Some Survivor","2015-03-18"),
        (6,"Odd Woman Out","2015-03-25"),
        (7,"The Line Will Be Drawn Tonight","2015-04-01"),
        (8,"Keep It Real","2015-04-08"),(9,"Livin' On the Edge","2015-04-15"),
        (10,"Bring the Popcorn","2015-04-22"),
        (11,"Survivor Russian Roulette","2015-04-29"),
        (12,"Holding on for Dear Life","2015-05-06"),
        (13,"My Word Is My Bond","2015-05-13"),
        (14,"It's A Fickle, Fickle Game","2015-05-20"),
    ],
    31: [ # Cambodia
        (1,"Second Chance","2015-09-23"),(2,"Survivor MacGyver","2015-09-30"),
        (3,"We Got a Rat","2015-10-07"),(4,"What's the Beef?","2015-10-14"),
        (5,"A Snake in the Grass","2015-10-21"),
        (6,"Bunking with the Devil","2015-10-28"),
        (7,"Play to Win","2015-11-04"),(8,"You Call, We'll Haul","2015-11-11"),
        (9,"Witches Coven","2015-11-18"),
        (10,"Like Selling Your Soul to the Devil","2015-11-25"),
        (11,"My Wheels are Spinning","2015-11-25"),
        (12,"Tiny Little Shanks to the Heart","2015-12-02"),
        (13,"Villains Have More Fun","2015-12-09"),
        (14,"Lie, Cheat and Steal","2015-12-16"),
    ],
    32: [ # Kaoh Rong
        (1,"I'm a Mental Giant","2016-02-17"),(2,"Kindergarten Camp","2016-02-24"),
        (3,"The Circle of Life","2016-03-02"),
        (4,"Signed, Sealed and Delivered","2016-03-09"),
        (5,"The Devils We Know","2016-03-16"),(6,"Play or Go Home","2016-03-23"),
        (7,"It's Merge Time","2016-03-30"),
        (8,"The Jocks vs. the Pretty People","2016-04-06"),
        (9,"It's Psychological Warfare","2016-04-13"),
        (10,"I'm Not Here to Make Good Friends","2016-04-20"),
        (11,"It's a 'Me' Game, Not a 'We' Game","2016-04-27"),
        (12,"Now's the Time to Start Scheming","2016-05-04"),
        (13,"With Me or Not With Me","2016-05-11"),
        (14,"Not Going Down Without a Fight","2016-05-18"),
    ],
    33: [ # MvGX
        (1,"May the Best Generation Win","2016-09-21"),
        (2,"Love Goggles","2016-09-28"),(3,"Your Job is Recon","2016-10-05"),
        (4,"Who's the Sucker at the Table?","2016-10-12"),
        (5,"Idol Search Party","2016-10-19"),(6,"The Truth Works Well","2016-10-26"),
        (7,"I Will Destroy You","2016-11-02"),(8,"I'm the Kingpin","2016-11-09"),
        (9,"Still Throwin' Punches","2016-11-16"),
        (10,"Million Dollar Gamble","2016-11-23"),
        (11,"About to Have a Rumble","2016-11-30"),
        (12,"Slayed the Survivor Dragon","2016-12-07"),
        (13,"I'm Going for a Million Bucks","2016-12-14"),
        (14,"Reunion","2016-12-14"),
    ],
    34: [ # Game Changers
        (1,"The Stakes Have Been Raised","2017-03-08"),
        (2,"Survivor Jackpot","2017-03-15"),
        (3,"The Tables Have Turned","2017-03-22"),(4,"Dirty Deed","2017-03-29"),
        (5,"Vote Early, Vote Often","2017-04-05"),
        (6,"What Happened on Exile, Stays on Exile","2017-04-12"),
        (7,"There's a New Sheriff in Town","2017-04-19"),
        (8,"A Line Drawn in Concrete","2017-04-26"),
        (9,"Reinventing How This Game Is Played","2017-05-03"),
        (10,"It Is Not a High Without a Low","2017-05-10"),
        (11,"Parting Is Such Sweet Sorrow","2017-05-17"),
        (12,"No Good Deed Goes Unpunished","2017-05-24"),
        (13,"Reunion","2017-05-24"),
    ],
    35: [ # HvHvH
        (1,"I'm Not Crazy, I'm Confident","2017-09-27"),
        (2,"I'm a Wild Banshee","2017-10-04"),
        (3,"My Kisses Are Very Private","2017-10-11"),
        (4,"I Don't Like Having Snakes Around","2017-10-18"),
        (5,"The Past Will Eat You Alive","2017-10-25"),
        (6,"This is Why You Play Survivor","2017-11-01"),
        (7,"Get to Gettin'","2017-11-08"),
        (8,"Playing with the Devil","2017-11-15"),
        (9,"Fear of the Unknown","2017-11-22"),
        (10,"Buy One, Get One Free","2017-11-29"),
        (11,"Not Going to Roll Over and Die","2017-12-06"),
        (12,"The Survivor Devil","2017-12-13"),
        (13,"Million Dollar Night","2017-12-20"),
        (14,"Reunion","2017-12-20"),
    ],
}

def find_dir(sn):
    for d in DATA.iterdir():
        if d.name.startswith(f"season-{sn:02d}-"):
            return d
    return None

def enrich(sn, sd, episodes):
    count = 0
    for ep_num, title, air_date in episodes:
        ep_file = sd / f"e{ep_num:02d}.json"
        if not ep_file.exists(): continue
        with open(ep_file) as f:
            ep = json.load(f)
        changed = False
        if not ep.get("episode_title"):
            ep["episode_title"] = title; changed = True
        if not ep.get("air_date"):
            ep["air_date"] = air_date; changed = True
        if ep.get("data_completeness") == "stub" and changed:
            ep["data_completeness"] = "season-level"
            ep["research_status"] = "initial_pass"
        if ep_num == len(episodes): ep["is_finale"] = True
        if changed:
            with open(ep_file, "w") as f:
                json.dump(ep, f, indent=2, ensure_ascii=False)
            count += 1
    return count

def main():
    total = 0
    for sn, episodes in sorted(EPISODE_DATA.items()):
        sd = find_dir(sn)
        if not sd: print(f"  [!] S{sn:02d}: not found"); continue
        c = enrich(sn, sd, episodes)
        if c > 0:
            print(f"  [+] S{sn:02d}: {c} episodes enriched")
            total += c
        else:
            print(f"  [=] S{sn:02d}: already done")
    print(f"\nTotal: {total} episodes enriched")

if __name__ == "__main__":
    main()
