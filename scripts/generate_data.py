#!/usr/bin/env python3
"""
generate_data.py

Generates the survivor-knowledge-graph/data/ directory tree from the
research compendium. Each season gets a folder; each episode is a stub
JSON file. Season-level JSON files carry all data we have now; episode
files carry skeleton structures ready for deep-research enrichment.
"""

import json
import os
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "data"
CONTEXT_DIR = Path(__file__).resolve().parent.parent / "context"

# ── helpers ──────────────────────────────────────────────────────────
def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def season_dir_name(num: int, subtitle: str) -> str:
    tag = slug(subtitle) if subtitle else "untitled"
    return f"season-{num:02d}-{tag}"


def contestant_id(name: str, season_num: int) -> str:
    return f"surv:contestant/{slug(name)}/s{season_num}"


def season_id(num: int) -> str:
    return f"surv:season/{num}"


def episode_id(season_num: int, ep_num: int) -> str:
    return f"surv:season/{season_num}/episode/{ep_num}"


def tribe_id(name: str, season_num: int) -> str:
    return f"surv:tribe/{slug(name)}/s{season_num}"


# ── season data (all 50) ─────────────────────────────────────────────

SEASONS = [
    # (num, subtitle, location, aired, winner, ftc_vote, runners_up,
    #  num_castaways, num_days, era, prize, tribes_initial,
    #  notable_facts, data_completeness, boot_order_known)
    (1, "Borneo", "Pulau Tiga, Malaysia", "May-Aug 2000",
     "Richard Hatch", "4-3", ["Kelly Wiglesworth"],
     16, 39, "classic", 1000000,
     [("Tagi", "orange", ["Richard Hatch","Kelly Wiglesworth","Rudy Boesch",
      "Sue Hawk","Sean Kenniff","Dirk Been","Sonja Christopher","Stacey Stillman"]),
      ("Pagong", "yellow", ["Colleen Haskell","Gervase Peterson","Greg Buis",
      "Gretchen Cordy","Jenna Lewis","Joel Klug","B.B. Andersen","Ramona Gray"])],
     ["First season ever","51.7M average viewers for finale","Invented alliance strategy"],
     "detailed",
     ["Sonja Christopher","B.B. Andersen","Stacey Stillman","Ramona Gray",
      "Dirk Been","Joel Klug","Gretchen Cordy","Greg Buis","Jenna Lewis",
      "Gervase Peterson","Colleen Haskell","Sean Kenniff","Rudy Boesch",
      "Sue Hawk","Kelly Wiglesworth","Richard Hatch"]),

    (2, "The Australian Outback", "Queensland, Australia", "Jan-May 2001",
     "Tina Wesson", "4-3", ["Colby Donaldson"],
     16, 42, "classic", 1000000,
     [("Kucha", "teal", []),("Ogakor", "green", [])],
     ["Only 42-day season","First medevac (Michael Skupin)","First female winner"],
     "season-level", []),

    (3, "Africa", "Shaba Reserve, Kenya", "Oct 2001-Jan 2002",
     "Ethan Zohn", "5-2", ["Kim Johnson"],
     16, 39, "classic", 1000000,
     [("Boran", "gold", []),("Samburu", "red", [])],
     ["First tribe swap"], "season-level", []),

    (4, "Marquesas", "Nuku Hiva, French Polynesia", "Feb-May 2002",
     "Vecepia Towery", "4-3", ["Neleh Dennis"],
     16, 39, "classic", 1000000,
     [("Maraamu", "yellow", []),("Rotu", "purple", [])],
     ["First African-American winner","First purple-rock tiebreaker"],
     "season-level", []),

    (5, "Thailand", "Ko Tarutao, Thailand", "Sep-Dec 2002",
     "Brian Heidik", "4-3", ["Clay Jordan"],
     16, 39, "classic", 1000000,
     [("Chuay Gahn", "blue", []),("Sook Jai", "red", [])],
     ["Fake merge twist"], "season-level", []),

    (6, "The Amazon", "Rio Negro, Brazil", "Feb-May 2003",
     "Jenna Morasca", "6-1", ["Matthew von Ertfelda"],
     16, 39, "classic", 1000000,
     [("Jaburu", "yellow", []),("Tambaqui", "blue", [])],
     ["Gender-divided tribes","Youngest female winner (21)"],
     "season-level", []),

    (7, "Pearl Islands", "Panama", "Sep-Dec 2003",
     "Sandra Diaz-Twine", "6-1", ["Lillian Morris"],
     16, 39, "classic", 1000000,
     [("Drake", "orange", ["Sandra Diaz-Twine","Rupert Boneham","Jon Dalton",
      "Burton Roberts","Christa Hastie","Michelle Tesauro","Shawn Cohen","Nicole Delma"]),
      ("Morgan", "purple", ["Andrew Savage","Lillian Morris","Darrah Johnson",
      "Osten Taylor","Ryan Shoulders","Ryan Opheim","Tijuana Bradley","Trish Dunn"])],
     ["Outcast twist","Dead grandma lie","First quit (Osten Taylor)"],
     "detailed", []),

    (8, "All-Stars", "Panama", "Feb-May 2004",
     "Amber Brkich", "4-3", ["Rob Mariano"],
     18, 39, "classic", 1000000,
     [("Chapera", "red", []),("Mogo Mogo", "green", []),("Saboga", "yellow", [])],
     ["First all-returnee season","Rob proposed to Amber at finale"],
     "season-level", []),

    (9, "Vanuatu", "Efate, Vanuatu", "Sep-Dec 2004",
     "Chris Daugherty", "5-2", ["Twila Tanner"],
     18, 39, "classic", 1000000,
     [("Lopevi", "red", []),("Yasur", "gold", [])],
     ["Gender-divided tribes"], "season-level", []),

    (10, "Palau", "Koror, Palau", "Feb-May 2005",
     "Tom Westman", "6-1", ["Katie Gallagher"],
     20, 39, "classic", 1000000,
     [("Koror", "brown", ["Tom Westman","Ian Rosenberger","Katie Gallagher",
      "Caryn Groedel","Coby Archa","Gregg Carey","Janu Tornell",
      "Jennifer Lyon","Willard Smith"]),
      ("Ulong", "blue", ["Stephenie LaGrossa","Bobby Jon Drinkard",
      "Angie Jakusz","Ashlee Ashby","Ibrehem Rahman","James Miller",
      "Jeff Wilson","Jolanda Jones","Kim Mullen"])],
     ["No merge","Ulong decimated to one member","Two eliminated before tribes picked",
      "12-hour endurance challenge"], "detailed", []),

    (11, "Guatemala", "Yaxha, Guatemala", "Sep-Dec 2005",
     "Danni Boatwright", "6-1", ["Stephenie LaGrossa"],
     18, 39, "classic", 1000000,
     [("Yaxha", "yellow", []),("Nakum", "blue", [])],
     ["First Hidden Immunity Idol (pre-vote)","Two returning players (Stephenie, Bobby Jon)"],
     "season-level", []),

    (12, "Panama - Exile Island", "Panama", "Feb-May 2006",
     "Aras Baskauskas", "5-2", ["Danielle DiLorenzo"],
     16, 39, "classic", 1000000,
     [("Casaya", "purple", []),("La Mina", "orange", []),
      ("Bayoneta", "red", []),("Viveros", "blue", [])],
     ["Exile Island introduced","First idol played after votes"],
     "season-level", []),

    (13, "Cook Islands", "Aitutaki, Cook Islands", "Sep-Dec 2006",
     "Yul Kwon", "5-4-0", ["Ozzy Lusth","Becky Lee"],
     20, 39, "classic", 1000000,
     [("Aitutaki", "brown", ["Ozzy Lusth","Billy Garcia","Cecilia Mansilla",
      "Cristina Coria","J.P. Calderon"]),
      ("Manihiki", "blue", ["Nate Gonzalez","Rebecca Borman","Sekou Bunch",
      "Stephannie Favor","Sundra Oakley"]),
      ("Puka Puka", "green", ["Yul Kwon","Becky Lee","Brad Virata",
      "Cao Boi Bui","Jenny Guzon-Bae"]),
      ("Rarotonga", "red", ["Parvati Shallow","Jonathan Penner","Adam Gentry",
      "Candice Woodcock","Jessica Smith"])],
     ["Ethnically divided tribes","First Final Three","Mutiny twist",
      "Aitu Four overcame 4-vs-8","First Asian-American winner"],
     "detailed", []),

    (14, "Fiji", "Vanua Levu, Fiji", "Feb-May 2007",
     "Earl Cole", "9-0-0", ["Dreamz Herd","Cassandra Franklin"],
     19, 39, "classic", 1000000,
     [("Moto", "orange", []),("Ravu", "green", [])],
     ["First unanimous FTC win","Have-vs-have-not twist","First African-American male winner"],
     "season-level", []),

    (15, "China", "Zhelin, Jiujiang, China", "Sep-Dec 2007",
     "Todd Herzog", "4-2-1", ["Courtney Yates","Amanda Kimmel"],
     16, 39, "classic", 1000000,
     [("Fei Long", "red", []),("Zhan Hu", "gold", [])],
     ["Kidnap twist","James voted out with two idols","Todd youngest male winner (22)"],
     "detailed", []),

    (16, "Micronesia - Fans vs. Favorites", "Palau", "Feb-May 2008",
     "Parvati Shallow", "5-3", ["Amanda Kimmel"],
     20, 39, "classic", 1000000,
     [("Malakal", "purple", ["Amanda Kimmel","Ami Cusack","Cirie Fields",
      "Eliza Orlins","James Clement","Jonathan Penner","Jonny Fairplay",
      "Ozzy Lusth","Parvati Shallow","Yau-Man Chan"]),
      ("Airai", "orange", ["Alexis Jones","Chet Welch","Erik Reichenbach",
      "Jason Siska","Joel Anderson","Kathy Sleckman","Mary Sartain",
      "Mikey Bortone","Natalie Bolton","Tracy Hughes-Wolf"])],
     ["Erik gives up immunity necklace","Black Widow Brigade",
      "Last Final Two until S30+","Two medevacs, one quit"],
     "detailed", []),

    (17, "Gabon", "Wonga-Wongue, Gabon", "Sep-Dec 2008",
     "Bob Crowley", "4-3-0", ["Susie Smith","Sugar Kiper"],
     18, 39, "classic", 1000000,
     [("Fang", "red", []),("Kota", "yellow", [])],
     ["Oldest winner (57)"], "season-level", []),

    (18, "Tocantins", "Jalapao, Brazil", "Feb-May 2009",
     "J.T. Thomas", "7-0", ["Stephen Fishbach"],
     16, 39, "classic", 1000000,
     [("Jalapao", "red", []),("Timbira", "black", [])],
     ["First perfect game (unanimous + no votes against)","Exile Island"],
     "season-level", []),

    (19, "Samoa", "Upolu, Samoa", "Sep-Dec 2009",
     "Natalie White", "7-2-0", ["Russell Hantz","Mick Trimming"],
     20, 39, "classic", 1000000,
     [("Foa Foa", "yellow", []),("Galu", "purple", [])],
     ["Russell Hantz dominance edit","Russell found idols without clues"],
     "season-level", []),

    (20, "Heroes vs. Villains", "Upolu, Samoa", "Feb-May 2010",
     "Sandra Diaz-Twine", "6-3-0", ["Parvati Shallow","Russell Hantz"],
     20, 39, "classic", 1000000,
     [("Heroes", "blue", ["Amanda Kimmel","Candice Woodcock","Cirie Fields",
      "Colby Donaldson","James Clement","J.T. Thomas","Rupert Boneham",
      "Stephenie LaGrossa","Sugar Kiper","Tom Westman"]),
      ("Villains", "red", ["Rob Mariano","Coach Wade","Courtney Yates",
      "Danielle DiLorenzo","Jerri Manthey","Parvati Shallow","Randy Bailey",
      "Russell Hantz","Sandra Diaz-Twine","Tyson Apostol"])],
     ["Sandra first two-time winner","J.T. gives idol to Russell",
      "Parvati double idol play","Russell zero jury votes two seasons running"],
     "detailed", []),

    (21, "Nicaragua", "San Juan del Sur, Nicaragua", "Sep-Dec 2010",
     'Jud "Fabio" Birza', "5-4-0", ["Chase Rice","Sash Lenahan"],
     20, 39, "modern", 1000000,
     [("Espada", "blue", []),("La Flor", "yellow", [])],
     ["Medallion of Power (one-off)","Old vs. Young"], "season-level", []),

    (22, "Redemption Island", "Nicaragua", "Feb-May 2011",
     "Rob Mariano", "8-1-0", ["Phillip Sheppard","Natalie Tenerelli"],
     18, 39, "modern", 1000000,
     [("Ometepe", "orange", []),("Zapatera", "purple", [])],
     ["Redemption Island introduced","Boston Rob's 4th time, first win"],
     "season-level", []),

    (23, "South Pacific", "Upolu, Samoa", "Sep-Dec 2011",
     "Sophie Clarke", "6-3-0", ["Coach Wade","Albert Destrade"],
     18, 39, "modern", 1000000,
     [("Savaii", "red", []),("Upolu", "blue", [])],
     ["Redemption Island returns","Coach's cult-like alliance"],
     "season-level", []),

    (24, "One World", "Upolu, Samoa", "Feb-May 2012",
     "Kim Spradlin", "7-2-0", ["Sabrina Thompson","Chelsea Meissner"],
     18, 39, "modern", 1000000,
     [("Manono", "orange", []),("Salani", "teal", [])],
     ["Both tribes on one beach","Kim considered one of best winners ever"],
     "season-level", []),

    (25, "Philippines", "Caramoan, Philippines", "Sep-Dec 2012",
     "Denise Stapley", "6-1-1", ["Lisa Whelchel","Michael Skupin"],
     18, 39, "modern", 1000000,
     [("Matsing", "blue", []),("Tandang", "yellow", []),("Kalabaw", "red", [])],
     ["Three tribes with returning medevacs","Matsing lost 4 straight",
      "Denise attended every Tribal Council"], "detailed", []),

    (26, "Caramoan - Fans vs. Favorites", "Caramoan, Philippines", "Feb-May 2013",
     "John Cochran", "8-0-0", ["Dawn Meehan","Sherri Biethman"],
     20, 39, "modern", 1000000,
     [("Bikal", "purple", []),("Gota", "orange", [])],
     ["Cochran perfect game","Brandon Hantz meltdown/ejection"],
     "season-level", []),

    (27, "Blood vs. Water", "Palaui, Philippines", "Sep-Dec 2013",
     "Tyson Apostol", "7-1-0", ["Monica Culpepper","Gervase Peterson"],
     20, 39, "modern", 1000000,
     [("Galang", "yellow", []),("Tadhana", "red", [])],
     ["Loved ones paired","Redemption Island returns"], "season-level", []),

    (28, "Cagayan - Brawn vs. Brains vs. Beauty", "Cagayan, Philippines", "Feb-May 2014",
     "Tony Vlachos", "8-1", ["Woo Hwang"],
     18, 39, "modern", 1000000,
     [("Aparri", "orange", ["Tony Vlachos","Sarah Lacina","Woo Hwang",
      "Cliff Robinson","Lindsey Ogle","Trish Hegarty"]),
      ("Luzon", "green", ["Spencer Bledsoe","Tasha Fox","Kass McQuillen",
      "Garrett Adelstein","J'Tia Taylor","David Samson"]),
      ("Solana", "purple", ["Jefra Bland","LJ McKanas","Jeremiah Wood",
      "Morgan McLeod","Brice Johnston","Alexis Maxwell"])],
     ["Spy shack","Tyler Perry idol","Woo chose Tony over Kass at F3",
      "Cops-R-Us alliance"], "detailed", []),

    (29, "San Juan del Sur - Blood vs. Water", "Nicaragua", "Sep-Dec 2014",
     "Natalie Anderson", "5-2-1", ["Jaclyn Schultz","Missy Payne"],
     18, 39, "modern", 1000000,
     [("Coyopa", "orange", []),("Hunahpu", "blue", [])],
     ["Pairs of loved ones","Natalie idol play at F5"],
     "season-level", []),

    (30, "Worlds Apart", "Nicaragua", "Feb-May 2015",
     "Mike Holloway", "6-1-1", ["Carolyn Rivera","Will Sims II"],
     18, 39, "modern", 1000000,
     [("Escameca", "blue", []),("Masaya", "white", []),("Nagarote", "yellow", [])],
     ["White/Blue/No Collar","Mike immunity run"], "season-level", []),

    (31, "Cambodia - Second Chance", "Koh Rong, Cambodia", "Sep-Dec 2015",
     "Jeremy Collins", "10-0-0", ["Spencer Bledsoe","Tasha Fox"],
     20, 39, "modern", 1000000,
     [("Ta Keo", "green", []),("Bayon", "gold", [])],
     ["Fan-voted cast","Vote Steal introduced","Idols hidden at challenges",
      "Largest unanimous win at the time","Jeremy meat-shield strategy"],
     "detailed", []),

    (32, "Kaoh Rong - Brains vs. Brawn vs. Beauty", "Koh Rong, Cambodia", "Feb-May 2016",
     "Michele Fitzgerald", "5-2-0", ["Aubry Bracco","Tai Trang"],
     18, 39, "modern", 1000000,
     [("Chanloh", "blue", []),("Gondol", "yellow", []),("To Tang", "red", [])],
     ["Three medevacs","Controversial winner pick"], "season-level", []),

    (33, "Millennials vs. Gen X", "Mamanuca, Fiji", "Sep-Dec 2016",
     "Adam Klein", "10-0-0", ["Hannah Shapiro","Ken McNickle"],
     20, 39, "modern", 1000000,
     [("Vanua", "purple", []),("Takali", "orange", [])],
     ["Legacy Advantage introduced","Adam revealed mother's cancer at FTC"],
     "season-level", []),

    (34, "Game Changers", "Mamanuca, Fiji", "Mar-May 2017",
     "Sarah Lacina", "7-3-0", ["Brad Culpepper","Troyzan Robertson"],
     20, 39, "modern", 1000000,
     [("Mana", "orange", []),("Nuku", "blue", [])],
     ["All-returnee","Cirie eliminated by default (all others immune)"],
     "season-level", []),

    (35, "Heroes vs. Healers vs. Hustlers", "Mamanuca, Fiji", "Sep-Dec 2017",
     "Ben Driebergen", "5-2-1", ["Chrissy Hofbeck","Ryan Ulrich"],
     18, 39, "modern", 1000000,
     [("Levu", "blue", []),("Soko", "yellow", []),("Yawa", "red", [])],
     ["Mandatory F4 fire-making introduced","Ben found 3 idols"],
     "season-level", []),

    (36, "Ghost Island", "Mamanuca, Fiji", "Feb-May 2018",
     "Wendell Holland", "5-5-0 tiebreak 6-5-0", ["Domenick Abbate","Laurel Johnson"],
     20, 39, "modern", 1000000,
     [("Naviti", "purple", []),("Malolo", "orange", [])],
     ["Only tied FTC vote in history","Cursed advantages theme"],
     "season-level", []),

    (37, "David vs. Goliath", "Mamanuca, Fiji", "Sep-Dec 2018",
     "Nick Wilson", "7-3-0", ["Mike White","Angelina Keeley"],
     20, 39, "modern", 1000000,
     [("David", "orange", []),("Goliath", "purple", [])],
     ["Christian Hubicki fan favorite","Pat Cusack medevac","Highly rated season"],
     "detailed", []),

    (38, "Edge of Extinction", "Mamanuca, Fiji", "Feb-May 2019",
     "Chris Underwood", "9-4-0", ["Gavin Whitson","Julie Rosenberg"],
     18, 39, "modern", 1000000,
     [("Kama", "yellow", []),("Manu", "blue", [])],
     ["Edge of Extinction introduced","Chris returned from Edge at F5",
      "Controversial winner"], "season-level", []),

    (39, "Island of the Idols", "Mamanuca, Fiji", "Sep-Dec 2019",
     "Tommy Sheehan", "8-2-0", ["Dean Kowalski","Noura Salman"],
     20, 39, "modern", 1000000,
     [("Lairo", "orange", []),("Vokai", "purple", [])],
     ["Rob and Sandra as mentors","Dan Spilo ejected for inappropriate touching",
      "Last live reunion until S50"], "season-level", []),

    (40, "Winners at War", "Mamanuca, Fiji", "Feb-May 2020",
     "Tony Vlachos", "12-4-0", ["Natalie Anderson","Michele Fitzgerald"],
     20, 39, "modern", 2000000,
     [("Sele", "blue", ["Amber Mariano","Danni Boatwright","Ethan Zohn",
      "Jeremy Collins","Natalie Anderson","Rob Mariano","Adam Klein",
      "Denise Stapley","Ben Driebergen","Parvati Shallow"]),
      ("Dakal", "red", ["Sandra Diaz-Twine","Tony Vlachos","Sarah Lacina",
      "Kim Spradlin-Wolfe","Sophie Clarke","Tyson Apostol","Wendell Holland",
      "Yul Kwon","Nick Wilson","Michele Fitzgerald"])],
     ["All-winners season","$2M prize","Fire Tokens","Edge of Extinction returns",
      "Tony second two-time winner","Denise Queenslayer move",
      "First COVID virtual finale"], "detailed", []),

    (41, "(New Era)", "Mamanuca, Fiji", "Sep-Dec 2021",
     "Erika Casupanan", "7-1-0", ["Deshawn Radden","Xander Hastings"],
     18, 26, "new_era", 1000000,
     [("Luvu", "blue", []),("Ua", "green", []),("Yase", "yellow", [])],
     ["26-day game begins","Shot in the Dark","Beware Advantage",
      "Hourglass twist (one-off)","Do or Die","No rice at start",
      "First Canadian winner","First Filipino winner"], "detailed", []),

    (42, "(New Era)", "Mamanuca, Fiji", "Mar-May 2022",
     "Maryanne Oketch", "7-1-0", ["Mike Turner","Romeo Escobar"],
     18, 26, "new_era", 1000000,
     [("Ika", "blue", []),("Taku", "green", []),("Vati", "orange", [])],
     ["Jackson Fox Day 1 medevac","Maryanne hid extra idol revealed at FTC"],
     "season-level", []),

    (43, "(New Era)", "Mamanuca, Fiji", "Sep-Dec 2022",
     "Mike Gabler", "7-1-0", ["Cassidy Clark","Owen Knight"],
     18, 26, "new_era", 1000000,
     [("Baka", "yellow", []),("Coco", "blue", []),("Vesi", "red", [])],
     ["Gabler donated entire $1M to veterans","Jesse blindside at F6"],
     "season-level", []),

    (44, "(New Era)", "Mamanuca, Fiji", "Mar-May 2023",
     "Yam Yam Arocho", "7-1-0", ["Heidi Lagares-Greenblatt","Carolyn Wiger"],
     18, 26, "new_era", 1000000,
     [("Ratu", "green", []),("Soka", "blue", []),("Tika", "purple", [])],
     ["Birdcage Idol","Bank Your Vote","First Puerto Rican winner","Tika Three"],
     "season-level", []),

    (45, "(New Era)", "Mamanuca, Fiji", "Sep-Dec 2023",
     "Dee Valladares", "5-3-0", ["Austin Li Coon","Jake O'Kane"],
     18, 26, "new_era", 1000000,
     [("Belo", "yellow", []),("Lulu", "blue", []),("Reba", "red", [])],
     ["First 90-minute episodes","Kaleb successful Shot in the Dark",
      "First Cuban-American winner"], "season-level", []),

    (46, "(New Era)", "Mamanuca, Fiji", "Feb-May 2024",
     "Kenzie Petty", "5-3-0", ["Charlie Davis","Ben Katzman"],
     18, 26, "new_era", 1000000,
     [("Nami", "green", []),("Siga", "purple", []),("Yanu", "yellow", [])],
     ["Yanu tribe disaster","Q Burdette asked to be voted out"],
     "season-level", []),

    (47, "(New Era)", "Mamanuca, Fiji", "Sep-Dec 2024",
     "Rachel LaMont", "7-1-0", ["Sam Phalen","Sue Smey"],
     18, 26, "new_era", 1000000,
     [("Gata", "yellow", []),("Lavo", "red", []),("Tuku", "blue", [])],
     ["Rachel won 4 individual immunities","Operation Italy blindside"],
     "season-level", []),

    (48, "(New Era)", "Mamanuca, Fiji", "Feb-May 2025",
     "Kyle Fraser", "5-2-1", ["Eva Erickson","Joe Hunter"],
     18, 26, "new_era", 1000000,
     [("Civa", "blue", []),("Lagi", "purple", []),("Vula", "red", [])],
     ["Kyle perfect voting record","Sixth Black winner"],
     "season-level", []),

    (49, "(New Era)", "Mamanuca, Fiji", "Sep-Dec 2025",
     "Savannah Louie", "5-2-1", ["Sophi Balerdi","Sage Ahrens-Nichols"],
     18, 26, "new_era", 1000000,
     [("Hina", "pink", []),("Kele", "green", []),("Uli", "blue", [])],
     ["Two cast members ejected pre-game","First all-female F3 since S29",
      "No Shot in the Dark played all season"], "season-level", []),

    (50, "In the Hands of the Fans", "Mamanuca, Fiji", "Feb-May 2026",
     "Jonathan Young", "TBA", ["Aubry Bracco","Joe Hunter"],
     24, 26, "new_era", 2000000,
     [("Cila", "red", []),("Kalo", "blue", []),("Vatu", "green", [])],
     ["Fan-voted mechanics","Triple Tribal Council","Double Duo",
      "Power Broker","MrBeast Super Beware coin flip","$2M prize",
      "Largest cast (24)","All returnees","Live LA finale",
      "Probst rapped","Sia Fan Favorite $100K prize"],
     "detailed", []),
]

# Default episode counts (can be refined per-season later)
DEFAULT_EPISODE_COUNTS = {
    1: 13, 2: 14, 3: 13, 4: 13, 5: 13, 6: 14, 7: 13, 8: 14,
    9: 14, 10: 14, 11: 14, 12: 16, 13: 15, 14: 15, 15: 14,
    16: 14, 17: 14, 18: 15, 19: 15, 20: 14, 21: 15, 22: 15,
    23: 15, 24: 15, 25: 15, 26: 14, 27: 14, 28: 14, 29: 14,
    30: 14, 31: 14, 32: 14, 33: 14, 34: 14, 35: 14, 36: 14,
    37: 14, 38: 14, 39: 14, 40: 16, 41: 13, 42: 13, 43: 13,
    44: 13, 45: 13, 46: 13, 47: 13, 48: 13, 49: 13, 50: 14,
}

# ── episode count & FTC format helpers ───────────────────────────────
def ftc_format_for(num: int) -> str:
    if num <= 12:
        return "final_two"
    if num == 16:
        return "final_two"
    return "final_three"


def mechanics_for_era(era: str, num: int) -> list[dict]:
    base = []
    if era == "classic":
        if num >= 11:
            base.append({"mechanic_name": "Hidden Immunity Idol",
                         "is_one_off": False})
        if num >= 12:
            base.append({"mechanic_name": "Exile Island",
                         "is_one_off": False})
    elif era == "modern":
        base.append({"mechanic_name": "Hidden Immunity Idol",
                     "is_one_off": False})
        if num in (22, 23, 27):
            base.append({"mechanic_name": "Redemption Island",
                         "is_one_off": False})
        if num >= 35:
            base.append({"mechanic_name": "Mandatory F4 Fire-Making",
                         "is_one_off": False})
        if num in (38, 40):
            base.append({"mechanic_name": "Edge of Extinction",
                         "is_one_off": False})
        if num == 40:
            base.append({"mechanic_name": "Fire Tokens",
                         "is_one_off": False})
    elif era == "new_era":
        base.append({"mechanic_name": "Hidden Immunity Idol",
                     "is_one_off": False})
        base.append({"mechanic_name": "Shot in the Dark",
                     "is_one_off": False})
        base.append({"mechanic_name": "Beware Advantage",
                     "is_one_off": False})
        base.append({"mechanic_name": "Mandatory F4 Fire-Making",
                     "is_one_off": False})
        if num == 41:
            base.append({"mechanic_name": "Hourglass",
                         "is_one_off": True})
    return base


# ── generate ─────────────────────────────────────────────────────────
def generate_season_json(s: tuple) -> dict:
    (num, subtitle, location, aired, winner, ftc, runners,
     n_cast, n_days, era, prize, tribes, facts, completeness,
     boot_order) = s

    tribes_data = []
    for t_name, t_color, t_members in tribes:
        tribes_data.append({
            "id": tribe_id(t_name, num),
            "type": "Tribe",
            "tribe_name": t_name,
            "tribe_color": t_color,
            "members": [
                {"id": contestant_id(m, num), "name": m}
                for m in t_members
            ] if t_members else []
        })

    contestants = []
    seen = set()
    for _, _, members in tribes:
        for m in members:
            if m not in seen:
                contestants.append({
                    "id": contestant_id(m, num),
                    "type": "Contestant",
                    "name": m
                })
                seen.add(m)

    runners_data = []
    for i, r in enumerate(runners):
        key = "runner_up" if i == 0 else "second_runner_up"
        runners_data.append((key, {"id": contestant_id(r, num), "name": r}))

    n_eps = DEFAULT_EPISODE_COUNTS.get(num, 13)

    doc = {
        "@context": "../context/season.jsonld",
        "id": season_id(num),
        "type": "Season",
        "season_number": num,
        "subtitle": subtitle,
        "filming_location": {
            "type": "Location",
            "location_name": location
        },
        "air_date_start": aired.split("-")[0].strip() if "-" in aired else aired,
        "air_date_end": aired.split("-")[-1].strip() if "-" in aired else aired,
        "num_castaways": n_cast,
        "num_days": n_days,
        "num_episodes": n_eps,
        "era": era,
        "prize_amount": prize,
        "ftc_format": ftc_format_for(num),
        "ftc_vote": ftc,
        "winner": {"id": contestant_id(winner, num), "name": winner},
    }
    for key, val in runners_data:
        doc[key] = val

    doc["tribes"] = tribes_data
    doc["contestants"] = contestants
    doc["boot_order"] = boot_order if boot_order else []
    doc["mechanics"] = mechanics_for_era(era, num)
    doc["notable_facts"] = facts
    doc["data_completeness"] = completeness
    doc["research_status"] = "initial_pass"

    return doc


def generate_episode_json(season_num: int, subtitle: str,
                          ep_num: int) -> dict:
    return {
        "@context": "../../context/episode.jsonld",
        "id": episode_id(season_num, ep_num),
        "type": "Episode",
        "episode_number": ep_num,
        "episode_title": None,
        "air_date": None,
        "season": season_id(season_num),
        "day_start": None,
        "day_end": None,
        "is_premiere": ep_num == 1,
        "is_finale": False,
        "is_double_episode": False,
        "duration_minutes": None,
        "viewership_millions": None,
        "challenges": [],
        "tribal_councils": [],
        "idol_plays": [],
        "advantages_found": [],
        "twists": [],
        "tribe_states": [],
        "notable_quotes": [],
        "notable_events": [],
        "data_completeness": "stub",
        "research_status": "not_started"
    }


def main():
    BASE.mkdir(parents=True, exist_ok=True)
    for s in SEASONS:
        num, subtitle = s[0], s[1]
        dirname = season_dir_name(num, subtitle)
        season_path = BASE / dirname
        season_path.mkdir(parents=True, exist_ok=True)

        # write season.json
        season_doc = generate_season_json(s)
        with open(season_path / "season.json", "w") as f:
            json.dump(season_doc, f, indent=2, ensure_ascii=False)

        # write episode stubs
        n_eps = DEFAULT_EPISODE_COUNTS.get(num, 13)
        for ep in range(1, n_eps + 1):
            ep_doc = generate_episode_json(num, subtitle, ep)
            with open(season_path / f"e{ep:02d}.json", "w") as f:
                json.dump(ep_doc, f, indent=2, ensure_ascii=False)

        print(f"  [+] S{num:02d} {subtitle}: {n_eps} episodes")

    print(f"\nGenerated {len(SEASONS)} seasons in {BASE}")


if __name__ == "__main__":
    main()
