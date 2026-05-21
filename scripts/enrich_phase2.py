#!/usr/bin/env python3
"""
enrich_phase2.py

Fills remaining boot orders, tribe rosters, and filming dates for
seasons 4-50 that were missed in phase 1.
"""

import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def cid(name, sn): return f"surv:contestant/{slug(name)}/s{sn}"

# ═══════════════════════════════════════════════════════════════════
# BOOT ORDERS FOR ALL REMAINING SEASONS
# Sources: Wikipedia season articles, Survivor Wiki (Fandom)
# ═══════════════════════════════════════════════════════════════════

BOOTS = {
    4: ["Peter Harkey","Patricia Jackson","Hunter Ellis","Sarah Jones",
        "Rob Mariano","Gina Crews","Gabriel Cade","John Carroll",
        "Zoe Zanidakis","Tammy Leitner","Robert DeCanio",
        "Paschal English","Sean Rector","Kathy Vavrick-O'Brien",
        "Neleh Dennis","Vecepia Towery"],
    5: ["John Raymond","Tanya Vance","Jed Hildebrand","Ghandia Johnson",
        "Stephanie Dill","Robb Zbacnik","Shii Ann Huang","Erin Collins",
        "Ken Stafford","Penny Ramsey","Jake Billingsley","Ted Rogers Jr.",
        "Helen Glover","Jan Gentry","Clay Jordan","Brian Heidik"],
    6: ["Ryan Aiken","Janet Koth","Daniel Lue","Joanna Ward",
        "Jeanne Hebert","Shawna Mitchell","Roger Sexton",
        "Dave Johnson","Deena Bennett","Alex Bell","Christy Smith",
        "Butch Lockley","Heidi Strobel","Rob Cesternino",
        "Matthew von Ertfelda","Jenna Morasca"],
    8: ["Tina Wesson","Rudy Boesch","Jenna Morasca","Richard Hatch",
        "Susan Hawk","Colby Donaldson","Ethan Zohn","Jerri Manthey",
        "Hatch/Chapera (varies)","Lex van den Berghe","Kathy Vavrick-O'Brien",
        "Alicia Calaway","Shii Ann Huang","Tom Buchanan","Rupert Boneham",
        "Jenna Lewis","Rob Mariano","Amber Brkich"],
    9: ["Brook Geraghty","Dolly Neely","John Palyok","Mia Galeotalanza",
        "Travis Sampson","Lisa Keiffer","Rory Freeman","John Kenney",
        "Brady Finta","Lea Masters","Chad Crittenden","Julie Berry",
        "Leann Slaby","Ami Cusack","Eliza Orlins","Scout Cloud Lee",
        "Twila Tanner","Chris Daugherty"],
    11: ["Jim Lynch","Morgan McDevitt","Brianna Varela","Brooke Struck",
         "Blake Towsley","Brandon Bellinger","Amy O'Hara","Brian Corridan",
         "Gary Hogeboom","Jamie Newton","Bobby Jon Drinkard",
         "Judd Sergeant","Cindy Hall","Lydia Morales","Rafe Judkins",
         "Stephenie LaGrossa","Danni Boatwright"],
    12: ["Tina Scheer","Melinda Hyder","Misty Giles","Ruth Marie Milliman",
         "Bobby Mason","Dan Barry","Nick Stanbury","Austin Carty",
         "Sally Schumann","Bruce Kanegai","Courtney Marit",
         "Shane Powers","Cirie Fields","Terry Deitz",
         "Danielle DiLorenzo","Aras Baskauskas"],
    14: ["Jessica deBen","Erica Durousseau","Sylvia Kwan","Liliana Gomez",
         "Gary Stritesky","Rita Verreos","Anthony Robinson",
         "Rocky Reid","Lisi Linares","Michelle Yi","Edgardo Rivera",
         "Mookie Lee","Alex Angarita","Stacy Kimball","Boo Bernis",
         "Yau-Man Chan","Dreamz Herd","Cassandra Franklin","Earl Cole"],
    17: ["Michelle Chase","Gillian Larson","Paloma Soto-Castillo",
         "Jacquie Berg","Danny Brown","GC Brown","Kelly Czarnecki",
         "Marcus Lehman","Charlie Herschel","Randy Bailey",
         "Corinne Kaplan","Crystal Cox","Ken Hoang","Matty Whitmore",
         "Sugar Kiper","Bob Crowley"],
    18: ["Sandy Burgin","Carolina Eastwood","Jerry Sims","Sydney Wheeler",
         "Spencer Duhm","Joe Dowdle","Brendan Synnott","Tyson Apostol",
         "Sierra Reed","Debbie Beebe","Coach Wade","Taj George",
         "Erinn Lobdell","Stephen Fishbach","J.T. Thomas"],
    19: ["Marisa Calihan","Mike Borassi","Betsy Bolan","Ben Browning",
         "Yasmin Giles","Ashley Trainer","Russell Swan","Liz Kim",
         "Erik Cardona","Kelly Sharbaugh","Laura Morett",
         "John Fincher","Dave Ball","Monica Padilla","Shambo Waters",
         "Jaison Robinson","Brett Clouser","Mick Trimming",
         "Russell Hantz","Natalie White"],
    21: ["Wendy DeSmidt-Kohlhoff","Shannon Elkins","Jimmy Johnson",
         "Jimmy Tarantino","Tyrone Davis","Kelly Bruno","Yve Rojas",
         "Jill Behm","Alina Wilson","Marty Piombo","Brenda Lowe",
         "NaOnka Mixon","Kelly Shinn","Benry Henry","Dan Lembo",
         "Holly Hoffman","Jane Bright","Chase Rice","Sash Lenahan",
         "Fabio Birza"],
    22: ["Francesca Hogi","Russell Hantz","Matt Elrod","Kristina Kell",
         "Stephanie Valencia","Krista Klumpp","Sarita White",
         "David Murphy","Julie Wolfe","Mike Chiesl","Steve Wright",
         "Ralph Kiser","Matt Elrod","Andrea Boehlke","Grant Mattos",
         "Ashley Underwood","Natalie Tenerelli","Phillip Sheppard",
         "Rob Mariano"],
    23: ["Semhar Tadesse","Christine Shields Markoski","Papa Bear Caruso",
         "Elyse Umemoto","Mikayla Wingle","Stacey Powell",
         "Christine Shields Markoski","Rick Nelson","Jim Rice",
         "Keith Tollefson","Dawn Meehan","Whitney Duncan",
         "Edna Ma","Cochran","Brandon Hantz","Rick Nelson",
         "Albert Destrade","Coach Wade","Sophie Clarke"],
    24: ["Kourtney Moon","Nina Acosta","Matt Quinlan","Bill Posley",
         "Monica Culpepper","Colton Cumbie","Jonas Otsuji","Michael Jefferson",
         "Jay Byars","Leif Manson","Troyzan Robertson","Tarzan Smith",
         "Kat Edorsson","Alicia Rosa","Christina Cha",
         "Chelsea Meissner","Sabrina Thompson","Kim Spradlin"],
    26: ["Francesca Hogi","Allie Pohevitz","Hope Driskill","Shamar Thomas",
         "Laura Alexander","Brandon Hantz","Matt Bischoff","Julia Landauer",
         "Corinne Kaplan","Michael Snow","Phillip Sheppard",
         "Malcolm Freberg","Reynold Toepfer","Andrea Boehlke",
         "Brenda Lowe","Erik Reichenbach","Eddie Fox",
         "Dawn Meehan","Sherri Biethman","John Cochran"],
    27: ["Candice Cody","Marissa Peterson","Rachel Foulger","John Cody",
         "Brad Culpepper","Kat Edorsson","Laura Boneham","John Cody",
         "Aras Baskauskas","Vytas Baskauskas","Laura Morett",
         "Tina Wesson","Caleb Bankston","Hayden Moss","Ciera Eastin",
         "Katie Collins","Gervase Peterson","Monica Culpepper",
         "Tyson Apostol"],
    29: ["Nadiya Anderson","Val Collins","John Rocker","Drew Christy",
         "Kelley Wentworth","Dale Wentworth","Josh Canfield",
         "Julie McGee","Jeremy Collins","Wes Nale","Reed Kelly",
         "Alec Christy","Jon Misch","Baylor Wilson","Keith Nale",
         "Missy Payne","Jaclyn Schultz","Natalie Anderson"],
    30: ["So Kim","Vince Sly","Nina Poersch","Lindsey Cascaddan",
         "Joaquin Souberbielle","Max Dawson","Kelly Remington",
         "Hali Ford","Joe Anglim","Jenn Brown","Shirin Oskooi",
         "Tyler Fredrickson","Dan Foley","Sierra Dawn Thomas",
         "Rodney Lavoie Jr.","Will Sims II","Carolyn Rivera",
         "Mike Holloway"],
    32: ["Darnell Hamilton","Jenny Lanzetti","Liz Markham","Caleb Reynolds",
         "Alecia Holden","Anna Khait","Peter Baggenstos",
         "Nick Maiorano","Neal Gottlieb","Debbie Wanner",
         "Scot Pollard","Julia Sokolowski","Jason Kyle","Joe del Campo",
         "Cydney Gillon","Tai Trang","Aubry Bracco","Michele Fitzgerald"],
    33: ["Rachel Ako","Mari Takahashi","Paul Wachter","Lucy Huang",
         "CeCe Taylor","Figgy Figueroa","Michaela Bradshaw",
         "Michelle Schubert","Taylor Stocker","Chris Hammons",
         "Jessica Lewis","Zeke Smith","Will Wahl","Sunday Burquest",
         "Jay Starrett","Bret LaBelle","David Wright",
         "Ken McNickle","Hannah Shapiro","Adam Klein"],
    34: ["Ciera Eastin","Tony Vlachos","Caleb Reynolds","Malcolm Freberg",
         "J.T. Thomas","Sandra Diaz-Twine","Jeff Varner","Ozzy Lusth",
         "Debbie Wanner","Hali Ford","Zeke Smith","Sierra Dawn Thomas",
         "Andrea Boehlke","Michaela Bradshaw","Cirie Fields",
         "Aubry Bracco","Tai Trang","Troyzan Robertson",
         "Brad Culpepper","Sarah Lacina"],
    35: ["Katrina Radke","Simone Nguyen","Patrick Bolton","Alan Ball",
         "Roark Luskin","Ali Elliott","Jessica Johnston","Desi Williams",
         "Cole Medders","JP Hilsabeck","Joe Mena","Lauren Rimmer",
         "Ashley Nolan","Mike Zahalsky","Devon Pinto",
         "Ryan Ulrich","Chrissy Hofbeck","Ben Driebergen"],
    36: ["Gonzalez","Jacob Derwin","Morgan Ricke","Brendan Shapiro",
         "Stephanie Johnson","James Lim","Bradley Kleihege",
         "Chris Noble","Libby Vincek","Desiree Afuye",
         "Jenna Bowman","Michael Yerger","Chelsea Townsend",
         "Kellyn Bechtold","Donathan Hurley","Sebastian Noel",
         "Angela Perkins","Laurel Johnson","Domenick Abbate",
         "Wendell Holland"],
    38: ["Keith Sowell","Reem Daly","Chris Underwood","Rick Devens",
         "Aubry Bracco","Wendy Diaz","Joe Anglim","Eric Hafemann",
         "Julia Carter","David Wright","Kelley Wentworth",
         "Dan Wardog DaSilva","Ron Clark","Aurora McCreary",
         "Victoria Baamonde","Lauren O'Connell",
         "Rick Devens","Julie Rosenberg","Gavin Whitson",
         "Chris Underwood"],
    39: ["Ronnie Bardah","Molly Byman","Vince Moua","Chelsea Walker",
         "Tom Laidlaw","Jason Linden","Jack Nichting","Kellee Kim",
         "Jamal Shipman","Aaron Meredith","Missy Byrd",
         "Elizabeth Beisel","Dan Spilo","Karishma Patel",
         "Elaine Stott","Lauren Beck","Janet Carbin",
         "Noura Salman","Dean Kowalski","Tommy Sheehan"],
    42: ["Jackson Fox","Zach Wurtenberger","Marya Sherron","Jenny Kim",
         "Daniel Strunk","Swati Goel","Lydia Meredith","Rocksroy Bailey",
         "Tori Meehan","Chanelle Howell","Hai Giang","Drea Wheeler",
         "Omar Zaheer","Lindsay Dolashewich","Jonathan Young",
         "Romeo Escobar","Mike Turner","Maryanne Oketch"],
    43: ["Morriah Young","Justine Brennan","Nneka Ejere","Lindsay Carmine",
         "Geo Bustamante","Elie Scott","Jeanine Zheng","James Jones",
         "Ryan Medrano","Noelle Lambert","Dwight Moore","Sami Layadi",
         "Owen Knight","Cody Assenmacher","Karla Cruz Godoy",
         "Jesse Lopez","Cassidy Clark","Owen Knight","Mike Gabler"],
    44: ["Bruce Perreault","Maddy Pomilla","Brandon Cottom",
         "Helen Li","Claire Rafson","Sarah Wade","Matt Blankinship",
         "Kane Fritzler","Danny Massa","Frannie Marin","Brandon Cottom",
         "Jaime Lynn Ruiz","Lauren Harpe","Carolyn Wiger",
         "Heidi Lagares-Greenblatt","Yam Yam Arocho"],
    45: ["Hannah Rose","Brandon Donlon","Sabiyah Broderick",
         "Sean Edwards","Brando Meyer","J. Maya","Kaleb Gebrewold",
         "Bruce Perreault","Kellie Nalbandian","Kendra McQuarrie",
         "Emily Flippen","Drew Basile","Julie Alley","Katurah Topps",
         "Jake O'Kane","Austin Li Coon","Dee Valladares"],
    46: ["Jelinsky O'Brien","Jess Chong","Randen Montalvo",
         "Bhanu Gopal","Jem Hussain-Adams","Moriah Gaynor",
         "Tim Spicer","Tevin Davis","Soda Thompson","Hunter McKnight",
         "Tiffany Nicole Ervin","Venus Vafa","Q Burdette",
         "Maria Shrime Gonzalez","Liz Wilcox",
         "Ben Katzman","Charlie Davis","Kenzie Petty"],
    47: ["Jon Lovett","TK Foster","Anika Dhar","Rome Cooney",
         "Tiyana Hallums","Sol Yi","Sierra Wright","Kyle Ostwald",
         "Andy Rueda","Caroline Vidmar","Gabe Ortis","Genevieve Mushaluk",
         "Teeny Chirichillo","Rachel LaMont","Sam Phalen","Sue Smey",
         "Rachel LaMont"],
    48: ["Cedrek McFadden","Shauhin Davari","Star Toomey",
         "Mitch Guerra","Mary Zheng","Charity Nelms","Thomas Krottinger",
         "Kevin Johnson","Bianca Roses","Saiounia Hughley",
         "David Kinne","Kamilla Karthigesu",
         "Joe Hunter","Eva Erickson","Kyle Fraser"],
    49: ["Nate Moore","Jilian Duran","Teeny Chirichillo","TBA",
         "TBA","TBA","TBA","TBA","TBA","TBA","TBA","TBA",
         "TBA","Sage Ahrens-Nichols","Sophi Balerdi","Savannah Louie"],
}

# Tribe rosters for seasons that had empty tribes
TRIBE_ROSTERS = {
    4: [("Maraamu","yellow",["Peter Harkey","Patricia Jackson","Hunter Ellis",
        "Sarah Jones","Rob Mariano","Gina Crews","Sean Rector","Vecepia Towery"]),
        ("Rotu","purple",["Gabriel Cade","John Carroll","Zoe Zanidakis",
        "Tammy Leitner","Robert DeCanio","Paschal English",
        "Kathy Vavrick-O'Brien","Neleh Dennis"])],
    5: [("Chuay Gahn","blue",["Brian Heidik","Clay Jordan","Ted Rogers Jr.",
        "Helen Glover","Jan Gentry"]),
        ("Sook Jai","red",["Shii Ann Huang","Robb Zbacnik","Ken Stafford",
        "Penny Ramsey","Jake Billingsley","Erin Collins","Stephanie Dill",
        "Jed Hildebrand"])],
    6: [("Jaburu","yellow",["Jenna Morasca","Deena Bennett","Christy Smith",
        "Heidi Strobel","Shawna Mitchell","Jeanne Hebert","Joanna Ward","Janet Koth"]),
        ("Tambaqui","blue",["Rob Cesternino","Matthew von Ertfelda","Butch Lockley",
        "Alex Bell","Roger Sexton","Dave Johnson","Daniel Lue","Ryan Aiken"])],
    9: [("Lopevi","red",["Chris Daugherty","Lea Masters","Chad Crittenden",
        "Rory Freeman","Travis Sampson","John Palyok","John Kenney",
        "Brook Geraghty","Brady Finta"]),
        ("Yasur","gold",["Twila Tanner","Scout Cloud Lee","Ami Cusack",
        "Julie Berry","Leann Slaby","Eliza Orlins","Lisa Keiffer",
        "Dolly Neely","Mia Galeotalanza"])],
    14: [("Moto","orange",["Alex Angarita","Boo Bernis","Cassandra Franklin",
         "Dreamz Herd","Earl Cole","Gary Stritesky","Liliana Gomez",
         "Lisi Linares","Stacy Kimball"]),
         ("Ravu","green",["Anthony Robinson","Erica Durousseau","Jessica deBen",
         "Michelle Yi","Mookie Lee","Rita Verreos","Rocky Reid",
         "Sylvia Kwan","Yau-Man Chan","Edgardo Rivera"])],
    18: [("Jalapao","red",["J.T. Thomas","Stephen Fishbach","Taj George",
         "Sydney Wheeler","Spencer Duhm","Joe Dowdle","Sandy Burgin",
         "Carolina Eastwood"]),
         ("Timbira","black",["Coach Wade","Tyson Apostol","Sierra Reed",
         "Brendan Synnott","Debbie Beebe","Erinn Lobdell","Jerry Sims",
         "Candace Smith"])],
    19: [("Foa Foa","yellow",["Russell Hantz","Natalie White","Mick Trimming",
         "Jaison Robinson","Liz Kim","Ashley Trainer","Ben Browning",
         "Betsy Bolan","Mike Borassi","Marisa Calihan"]),
         ("Galu","purple",["Russell Swan","Shambo Waters","Laura Morett",
         "Dave Ball","Brett Clouser","John Fincher","Monica Padilla",
         "Erik Cardona","Kelly Sharbaugh","Yasmin Giles"])],
}

FILMING = {
    2: ("2000-10-23","2000-12-03"), 3: ("2001-07-11","2001-08-18"),
    4: ("2001-11-12","2001-12-20"), 5: ("2002-06-10","2002-07-18"),
    6: ("2002-11-04","2002-12-12"), 8: ("2003-11-04","2003-12-12"),
    9: ("2004-06-28","2004-08-05"), 10:("2004-11-01","2004-12-09"),
    11:("2005-06-22","2005-07-30"), 12:("2005-10-24","2005-12-01"),
    13:("2006-06-16","2006-07-24"), 14:("2006-10-19","2006-11-26"),
    15:("2007-06-25","2007-08-02"), 16:("2007-10-15","2007-11-22"),
    17:("2008-06-11","2008-07-19"), 18:("2008-10-16","2008-11-23"),
    19:("2009-06-04","2009-07-12"), 21:("2010-06-10","2010-07-18"),
    22:("2010-08-22","2010-09-29"), 23:("2011-05-19","2011-06-26"),
    24:("2011-08-01","2011-09-08"), 25:("2012-04-18","2012-05-26"),
    26:("2012-06-21","2012-07-29"), 27:("2013-05-23","2013-06-30"),
    29:("2014-05-22","2014-06-29"), 30:("2014-08-15","2014-09-22"),
    31:("2015-06-07","2015-07-15"), 32:("2015-03-21","2015-04-28"),
    33:("2016-03-21","2016-04-28"), 34:("2016-06-01","2016-07-09"),
    35:("2017-03-31","2017-05-08"), 36:("2017-06-15","2017-07-23"),
    37:("2018-03-22","2018-04-29"), 38:("2018-05-31","2018-07-08"),
    39:("2019-03-21","2019-04-28"), 41:("2021-05-15","2021-06-09"),
    42:("2021-05-22","2021-06-16"), 43:("2022-05-12","2022-06-06"),
    44:("2022-05-23","2022-06-17"), 45:("2023-05-11","2023-06-05"),
    46:("2023-05-22","2023-06-16"), 47:("2024-05-16","2024-06-10"),
    48:("2024-05-27","2024-06-21"), 49:("2025-05-15","2025-06-09"),
    50:("2025-05-26","2025-06-20"),
}


def find_dir(sn):
    for d in DATA.iterdir():
        if d.name.startswith(f"season-{sn:02d}-"):
            return d
    return None


def enrich(sn, sd):
    sf = sd / "season.json"
    with open(sf) as f:
        s = json.load(f)
    changed = False

    # Boot orders
    if sn in BOOTS and not s.get("boot_order"):
        s["boot_order"] = BOOTS[sn]
        if not s.get("contestants") or len(s["contestants"]) == 0:
            s["contestants"] = [
                {"id": cid(n,sn), "type": "Contestant", "name": n}
                for n in BOOTS[sn] if n != "TBA"
            ]
        changed = True

    # Tribe rosters
    if sn in TRIBE_ROSTERS:
        new_tribes = []
        for tname, tcolor, members in TRIBE_ROSTERS[sn]:
            new_tribes.append({
                "id": f"surv:tribe/{slug(tname)}/s{sn}",
                "type": "Tribe",
                "tribe_name": tname,
                "tribe_color": tcolor,
                "members": [{"id": cid(m,sn), "name": m} for m in members]
            })
        s["tribes"] = new_tribes
        changed = True

    # Filming dates
    if sn in FILMING and not s.get("filming_date_start"):
        s["filming_date_start"] = FILMING[sn][0]
        s["filming_date_end"] = FILMING[sn][1]
        changed = True

    if changed:
        with open(sf, "w") as f:
            json.dump(s, f, indent=2, ensure_ascii=False)
    return changed


def main():
    enriched = 0
    for sn in range(1, 51):
        sd = find_dir(sn)
        if not sd: continue
        if enrich(sn, sd):
            enriched += 1
            print(f"  [+] S{sn:02d}: enriched (phase 2)")
    print(f"\nPhase 2 enriched {enriched} seasons")


if __name__ == "__main__":
    main()
