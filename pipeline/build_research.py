"""Writes data/research/app/*.json (hand-checked Vermont guides), data/research/michelin.json, jbf.json and closed.json from the
compact lists below. Ported from ut-eats/pipeline/build_research.py.

Each entry cites the page that names it, read on 2026-11-05: an official Vermont tourism listing (plan.vermontvacation.com/listings/<n>,
the Department of Tourism's per-business pages, read by scripts/read_listings.py; robots allows /listings), the Department's own
article (vermontvacation.com), or a page dated 2025-26 on a robots-checked host (check_sources.py). The address comes from the map
listing we already hold for that name in that town (site/vermont.json); a name that isn't found exactly once in its town (or at the
street number given) is left out and listed in data/research/app/LEADS.md. A place the map data doesn't show as a place to eat is
added only with a street address from its official listing or our own map data (ADDR).
Usage: ../.venv/bin/python build_research.py   (then vermont.py)"""
import json, os, re
from brands import brand_of
from common import norm_name
ROOT = os.path.join(os.path.dirname(__file__), "..")
R = os.path.join(ROOT, "data", "research")
d = json.load(open(os.path.join(ROOT, "site", "vermont.json")))
C, M = d["cols"], d["meta"]
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", (s or "").lower().replace("'", "").replace("’", ""))).strip()

# each dated on its face, or an official tourism page (read 2026-11-05)
L = lambda n: f"https://plan.vermontvacation.com/listings/{n}"                                        # official tourism listing, (c) 2026
VV_CREEMEE = "https://vermontvacation.com/top-creemee-stops/"                                          # Vermont Dept. of Tourism, (c) 2026
NE25 = "https://newengland.com/travel/vermont/2025-vermont-travel-guide/"                              # Yankee Magazine, 2025-04-24
SD_DINERS = ("https://sevendaysvt.com/food-drink/what-vermonts-classic-american-diners-tell-us-about-the-current-state-of-restaurants"
             "-41288880")                                                                             # Seven Days, 2024-07-03, updated 2025-07-30
TT_OLDREST = "https://www.tastingtable.com/1975409/oldest-restaurant-every-state-still-open/"          # 2025-09-23
JBF26 = "https://www.jamesbeard.org/stories/james-beard-award-semifinalists-2026"                   # 2026-01-21
JBF26N = "https://www.jamesbeard.org/stories/james-beard-awards-restaurant-and-chef-nominees-2026"  # 2026-03-31
JBF25 = "https://www.jamesbeard.org/stories/the-2025-james-beard-award-semifinalists"               # 2025-01-22
JBF25N = "https://www.jamesbeard.org/stories/2025-james-beard-awards-restaurant-and-chef-nominees"   # 2025-04-02
JBF22W = "https://www.jamesbeard.org/stories/the-2022-james-beard-award-winners"                    # 2022 winners
JBF10_ALS = "https://www.jamesbeard.org/blog/jbf-awards-2010-americas-classic-awards-als-french-frys-south-burlington-vt"  # 2010 America's Classics

# (name as the source writes it or as our listing spells it, town as our listing has it, street number to pick the location (or
# None), note, founded, founded_note, [sources])
BTV, SB = "Burlington", "South Burlington"
GUIDES = {
 "classic diner": [   # Seven Days' diner survey (updated July 2025), Yankee's Best of New England 2025, the tourism listings
  ("Country Girl Diner", "Chester", "46", "A 1944 Silk City diner car on Route 103, Yankee's Best Diner in Vermont for 2025.", None, None, [NE25, L(520)]),
  ("Henry's Diner", BTV, "155", "Bank Street's diner since the 1920s, with breakfast all day.", None, None, [L(798), SD_DINERS]),
  ("Burl's Downtown Kitchenette", BTV, "189", "A refurbished 1950s diner car with Southern-leaning plates and breakfast all day.", None, None, [L(837)]),
  ("Birdseye Diner", "Castleton", "590", "A 1940s Silk City car that came to Castleton in 1968.", None, None, [SD_DINERS]),
  ("Martha's Diner", "Coventry", "585", "A 1953 Fodero dining car, run by one family since 1985.", None, None, [SD_DINERS]),
  ("Athens Diner", "Colchester", "46", "A 1953 Worcester Lunch Car, once Libby's Blue Line.", None, None, [SD_DINERS]),
  ("Blue Benn", "Bennington", "314", "A 1948 Silk City car on North Street.", None, None, [SD_DINERS]),
  ("Parkway Diner", SB, None, "A 1950s Worcester Lunch Car on Williston Road for about 70 years.", None, None, [SD_DINERS]),
 ],
 "fry stand": [
  ("Al's French Frys", SB, None, "Fries, burgers and dogs on Williston Road; a James Beard America's Classic (2010).", 1946,
   "Al's official Vermont tourism listing: serving burgers, dogs and frys since 1946.", [L(1208), JBF10_ALS]),
 ],
 "maple creemee": [   # the Department of Tourism's "Where to Find a Creemee in Vermont" and the listings that name maple creemees
  ("Morse Farm Maple Sugarworks", "Montpelier", None, "A family sugarworks since the 1960s: maple creemees, and sugar on snow in March.", None, None, [VV_CREEMEE, L(179)]),
  ("Canteen Creemee Company", "Waitsfield", "5123", "Creemees in homemade flavors like basil and honey lemon.", None, None, [VV_CREEMEE]),
  ("The Maple Angus", "Rutland", "389", "Smooth maple creemees; a dish comes with a drizzle of syrup.", None, None, [VV_CREEMEE]),
  ("The Village Scoop", "Colchester", "419", "Drive-through and walk-up windows, with tables under a big maple.", None, None, [VV_CREEMEE]),
  ("LegenDairy Maple & Ice Cream", "Williamstown", "32", "Dozens of creemee and ice cream flavors.", None, None, [VV_CREEMEE]),
  ("Silloway Maple", "Randolph", None, "A family sugarhouse near I-89 Exit 4; maple creemees from its own syrup in summer.", None, None, [L(115)]),
  ("Woodstock Scoops", "Woodstock", None, "A Central Street ice cream shop with Vermont maple creemees.", None, None, [L(1429)]),
 ],
 "cider mill": [
  ("Cold Hollow Cider Mill", "Waterbury", "3600", "A working cider mill: the rack-and-cloth press, cider donuts made daily and a café.", None, None, [L(86)]),
  ("Champlain Orchards", "Shoreham", None, "A pick-your-own orchard over Lake Champlain with cider donuts, pies and hard cider.", None, None, [L(1307)]),
  ("Cobble Knoll Orchard", "Benson", None, "A family orchard with fresh cider and cider donuts in the fall.", None, None, [L(3756)]),
  ("Hackett's Orchard", "South Hero", None, "A farm market with cider donuts, fresh-pressed cider and cider slush; open in the fall.", None, None, [L(9499)]),
 ],
 "farm pizza": [
  ("Woodbelly Pizza", "Middlesex", "961", "Naturally leavened, wood-fired pizza from local ingredients at Camp Meade.", None, None, [L(622)]),
  ("Barnyard Wood Crafted Pizza", SB, "1705", "Wood-fired pizza and calzones.", None, None, [L(606)]),
  ("Crossmolina Farm", "Corinth", None, "A family farm with pizza and live music on summer Saturday evenings.", None, None, [L(8714)]),
  ("Roo's Farm", "Weathersfield", None, "Wood-fired pizza from its own organic farm, Friday and Saturday nights in season.", None, None, [L(11709)]),
  ("Parker Pie Company", "Glover", "161", "A Northeast Kingdom pizza place built on shared tables and local producers.", None, None, [L(660)]),
  ("Folino's Pizza", "Shelburne", "6305", "Neapolitan-style pies from a wood-fired oven.", None, None, [L(1378)]),
  ("American Flatbread", "Stowe", "1190", "Wood-fired flatbread made with ingredients from local farms.", None, None, [L(1569)]),
 ],
 "sugarhouse": [
  ("Morse Farm Maple Sugarworks", "Montpelier", None, "A family sugarworks since the 1960s: tours, tastings and sugar on snow in March.", None, None, [L(179), VV_CREEMEE]),
  ("Bragg Farm Sugar House & Gift Shop", "East Montpelier", None, "A family sugarhouse with maple tours, tastings and a maple ice cream parlor.", None, None, [L(75)]),
  ("Palmer's Sugarhouse", "Shelburne", None, "A family sugarhouse for over 50 years; sugar on snow in March and April.", None, None, [L(966)]),
  ("Silloway Maple", "Randolph", None, "A family sugarhouse open year-round for tours and samples; creemees in summer.", None, None, [L(115)]),
 ],
 "brewery kitchen": [   # breweries whose own listing names their kitchen or menu (Hill Farmstead-style food-truck taprooms are out)
  ("Lawson's Finest Liquids", "Waitsfield", "155", "The Sip of Sunshine brewery's timber-frame taproom, with charcuterie, pretzels and small plates.", None, None, [L(151)]),
  ("Snow Republic Brewery", "Dover", "33", "A veteran-owned brewery with a taproom and kitchen in West Dover.", None, None, [L(1516)]),
  ("Outer Limits Brewing", "Cavendish", "60", "A family brewery in Proctorsville with a small wood-fired menu.", None, None, [L(1070)]),
  ("Whirligig", "St. Johnsbury", "397", "A Railroad Street restaurant that brews its own sours and wild ales.", None, None, [L(12699)]),
  ("Two Heroes Brewery & Public House", "South Hero", "252", "A brewpub in a red barn with a full menu and live music.", None, None, [L(8839)]),
  ("Harpoon Brewery Taproom and Beer Garden", "Windsor", "336", "Harpoon's Riverbend Taps, inside the brewery, with food to match.", None, None, [L(959)]),
  ("American Flatbread", BTV, "115", "Flatbread from the hearth and beer from its own Mothership Brewery.", None, None, [L(8046)]),
  ("Jasper Murdock's Alehouse", "Norwich", "325", "The Norwich Inn's pub, with English-style ales brewed on site.", None, None, [L(22)]),
 ],
 "historic inn": [
  ("Ye Olde Tavern", "Manchester", "5183", "Dinner by the fire in a tavern open since 1790.", 1790,
   "Tasting Table's oldest restaurant in every state (September 2025): Vermont's is Ye Olde Tavern, 1790.", [TT_OLDREST]),
  ("Jasper Murdock's Alehouse", "Norwich", "325", "The Norwich Inn's pub and dining room; the inn has stood on Main Street since 1797.", 1797,
   "The Norwich Inn's official Vermont tourism listing: on Main Street since 1797, in its Victorian building since 1890.", [L(22)]),
  ("Barnard Inn Restaurant", "Barnard", "5518", "Fine dining and a cocktail lounge in a 1796 house.", None, None, [L(1213)]),
  ("The Quechee Inn at Marshland Farm", "Hartford", None, "Candlelit dining at a 1793 farmstead inn in Quechee.", None, None, [L(253)]),
  ("McGrath's Irish Pub", "Killington", "709", "The Irish pub of the Inn at Long Trail, a rustic inn on Sherburne Pass.", None, None, [L(18)]),
  ("Old Stagecoach Inn", "Waterbury", None, "A former stagecoach stop, now a village inn and pub.", None, None, [L(234)]),
  ("The Landgrove", "Landgrove", None, "A 200-year-old inn with a chef-led restaurant, VildaHaus.", None, None, [L(13359)]),
  ("Red Clover Inn", "Mendon", None, "An 1840s farmstead inn with a restaurant in the Killington Valley.", None, None, [L(44)]),
 ],
}
# street addresses for places the map data doesn't show as a place to eat: from the official listing, or our own map listing for it
ADDR = {("Parkway Diner", SB): "1696 Williston Rd", ("Al's French Frys", SB): "1251 Williston Rd",
        ("Morse Farm Maple Sugarworks", "Montpelier"): "1168 County Rd", ("Silloway Maple", "Randolph"): "1303 Boudro Rd",
        ("Woodstock Scoops", "Woodstock"): "20 Central St", ("Champlain Orchards", "Shoreham"): "3597 VT Route 74 W",
        ("Cobble Knoll Orchard", "Benson"): "1672 East Rd", ("Hackett's Orchard", "South Hero"): "76 South St",
        ("Crossmolina Farm", "Corinth"): "1776 Center Rd", ("Roo's Farm", "Weathersfield"): "1465 VT Route 106",
        ("Bragg Farm Sugar House & Gift Shop", "East Montpelier"): "1005 VT Route 14 N",
        ("Palmer's Sugarhouse", "Shelburne"): "332 Shelburne-Hinesburg Rd", ("The Quechee Inn at Marshland Farm", "Hartford"): "1119 Quechee Main St",
        ("Old Stagecoach Inn", "Waterbury"): "18 N Main St", ("The Landgrove", "Landgrove"): "132 Landgrove Rd",
        ("Red Clover Inn", "Mendon"): "7 Woodward Rd"}
SWEET = "Bakery & Sweets"
CUISINE = {("Morse Farm Maple Sugarworks", "Montpelier"): SWEET, ("Silloway Maple", "Randolph"): SWEET, ("Woodstock Scoops", "Woodstock"): SWEET,
           ("The Maple Angus", "Rutland"): SWEET, ("The Village Scoop", "Colchester"): SWEET, ("LegenDairy Maple & Ice Cream", "Williamstown"): SWEET,
           ("Canteen Creemee Company", "Waitsfield"): SWEET, ("Cold Hollow Cider Mill", "Waterbury"): SWEET, ("Champlain Orchards", "Shoreham"): SWEET,
           ("Cobble Knoll Orchard", "Benson"): SWEET, ("Hackett's Orchard", "South Hero"): SWEET, ("Bragg Farm Sugar House & Gift Shop", "East Montpelier"): SWEET,
           ("Palmer's Sugarhouse", "Shelburne"): SWEET, ("Crossmolina Farm", "Corinth"): "Pizza", ("Roo's Farm", "Weathersfield"): "Pizza",
           ("Al's French Frys", SB): "Burgers", ("Parkway Diner", SB): "Breakfast & Diner", ("Blue Benn", "Bennington"): "Breakfast & Diner",
           ("Old Stagecoach Inn", "Waterbury"): "Bar & Pub", ("The Quechee Inn at Marshland Farm", "Hartford"): "American & Other",
           ("The Landgrove", "Landgrove"): "American & Other", ("Red Clover Inn", "Mendon"): "American & Other"}
KINDS = {k: [k] for k in ("classic diner", "fry stand", "maple creemee", "cider mill", "farm pizza", "sugarhouse", "brewery kitchen",
                          "historic inn")}

# no MICHELIN Guide covers Vermont (guide.michelin.com finds no Vermont restaurant; the Northeast Cities edition doesn't reach it)
MICHELIN = []
MI_MATCH = {}
MI_UT = None
# James Beard (facts with sources): Vermont's wins (America's Classics 2010, Best Chef: Northeast 2022) and its 2025-26 nominees
# (finalists) and semifinalists; jamesbeard.org pages read 2026-11-05
WELLS = "Outstanding Restaurateur semifinalist 2026 (Leslie McCrorey Wells)"
JBF = [{"name": "Al's French Frys", "city": SB, "address": "1251 Williston Rd", "honors": ["America's Classics 2010"], "sources": [JBF10_ALS]},
       {"name": "Saap", "city": "Randolph", "honors": ["Best Chef: Northeast winner 2022 (Nisachon Morgan)"], "sources": [JBF22W]},
       {"name": "The Crooked Ram", "city": "Manchester", "honors": ["Best Chef: Northeast semifinalist 2026 (Tiara Adorno)"], "sources": [JBF26]},
       {"name": "Ondis", "city": "Montpelier", "honors": ["Best Chef: Northeast semifinalist 2026 (Max Vogel)"], "sources": [JBF26]},
       {"name": "Juniper Bar & Restaurant", "city": BTV, "honors": ["Outstanding Professional in Cocktail Service semifinalist 2026 (Kate Wise)"],
        "sources": [JBF26], "match_names": ["JUNIPER"]},
       {"name": "Pizzeria Verità", "city": BTV, "honors": [WELLS], "sources": [JBF26], "match_names": ["PIZZERIA VERITA"]},
       {"name": "Trattoria Delia", "city": BTV, "honors": [WELLS], "sources": [JBF26]},
       {"name": "Sotto Enoteca", "city": BTV, "honors": [WELLS], "sources": [JBF26]},
       {"name": "Café Monette", "city": "St. Albans", "honors": ["Best New Restaurant semifinalist 2026"], "sources": [JBF26]},
       {"name": "The Grey Jay", "city": BTV, "address": "135 Pearl St", "honors": ["Outstanding Restaurateur finalist 2025 (Allison Gibson and Cara Tobin)"],
        "sources": [JBF25N, JBF25], "match_names": ["GRAY JAY"]},
       {"name": "May Day", "city": BTV, "honors": ["Best Chef: Northeast finalist 2025 (Avery Buck)"], "sources": [JBF25N, JBF25]},
       {"name": "Canteen Creemee Company", "city": "Waitsfield", "honors": ["Best Chef: Northeast semifinalist 2025 (Charlie Menard)"], "sources": [JBF25],
        "match_names": ["CANTEEN CREEMEE"]},
       {"name": "Wolf Tree", "city": "Hartford", "honors": ["Outstanding Bar finalist 2025"], "sources": [JBF25N, JBF25]}]
# closed, each with a source (none verified this pass)
CLOSED = []


def key(s):
    """The name key without a leading "the": "Varsity" is our "The Varsity"."""
    return re.sub(r"^the ", "", norm(s))


def find(name, town, num):
    k = key(name)
    hits = [i for i, n in enumerate(C["name"]) if C["city"][i] is not None and M["cities"][C["city"][i]] == town
            and (key(n) == k or key(n).startswith(k + " ") or k.startswith(key(n) + " ") or key(n).replace(" ", "") == k.replace(" ", "")
                 or (key(n).split()[:2] == k.split()[:2] and len(k.split()) >= 2))]
    if num:
        hits = [i for i in hits if (C["addr"][i] or "").split(" ")[0] == num]
    return hits


leads, n_out = [], {}
for kind, rows in GUIDES.items():
    out = []
    for name, town, num, note, founded, fnote, srcs in rows:
        hits = find(name, town, num)
        if not hits and (name, town) in ADDR:
            out.append({"name": name, "address": ADDR[(name, town)], "city": town, "zip": None, "kinds": KINDS[kind], "dishes": [], "note": note,
                        "founded": founded, "founded_note": fnote, "website": None, "open": True, "evidence_date": "2026-10",
                        "sources": srcs, "match_names": []} | ({"cuisine": CUISINE[(name, town)]} if (name, town) in CUISINE else {}))
            continue
        if len(hits) != 1:
            leads.append(f"- {kind}: {name} ({town}{', ' + num if num else ''}) — {len(hits)} matches in our data; not added"); continue
        i = hits[0]
        out.append({"name": C["name"][i], "address": C["addr"][i], "city": town, "zip": str(C["zip"][i]) if C["zip"][i] else None,
                    "kinds": KINDS[kind], "dishes": [], "note": note, "founded": founded, "founded_note": fnote, "website": None, "open": True,
                    "evidence_date": "2026-10", "sources": srcs, "match_names": [name.upper()] if norm(name) != norm(C["name"][i]) else []})
        if brand_of(norm_name(name)):   # a chain shows under its own spelling at every branch, whatever the listing says
            out[-1]["display"] = name
        if (name, town) in CUISINE:
            out[-1]["cuisine"] = CUISINE[(name, town)]
    fn = re.sub(r"[^a-z]+", "_", kind).strip("_")
    json.dump(out, open(f"{R}/app/{fn}.json", "w"), indent=1, ensure_ascii=False)
    n_out[kind] = len(out)

MI_ADDR = {}
json.dump({"restaurants": [{"name": n, "address": MI_ADDR.get(n), "city": t, "zip": None, "distinction": dist, "cuisine": cu, "green_star": False,
                             "michelin_url": MI_UT, "sources": [MI_UT], "match_names": [x.upper() for x in MI_MATCH.get(n, [])], "open": True}
                            for n, t, dist, cu in MICHELIN]}, open(f"{R}/michelin.json", "w"), indent=1, ensure_ascii=False)
json.dump([dict({"address": None}, **j, zip=None, open=True) for j in JBF], open(f"{R}/jbf.json", "w"), indent=1, ensure_ascii=False)
json.dump(CLOSED, open(f"{R}/closed.json", "w"), indent=1, ensure_ascii=False)
open(f"{R}/app/LEADS.md", "w").write("# Vermont research leads (not yet verified)\n\nWritten by pipeline/build_research.py.\n\n" + "\n".join(leads) + """

## Waiting for a source we may use, or for the map data
- Honors: Fancy's (Burlington; Paul Trombly, Best Chef: Northeast finalist 2026) and Honey Road (Burlington; Outstanding Restaurateur
  finalist 2025 with Grey Jay) aren't in our map data.
- Diners: Chelsea Royal Diner (Brattleboro): its tourism listing says open year-round, but Seven Days (updated July 2025) says the old
  diner didn't survive the pandemic and was bought the summer before; left out until a 2025-26 page says it serves again. Miss
  Lyndonville Diner (flood-damaged, not reopening per Seven Days) and Springfield Diner (closing, for sale) are out. P&H Truck Stop
  (Wells River) isn't in our map data. Wayside Restaurant (Berlin) is only mentioned in passing.
- Historic inns: The Tillerman (Bristol; Yankee's Best Historic Inn 2025) and the Grafton Inn's 1802 Tavern (the tourism article is a
  2020 Seven Days reprint without an address) wait for an address on a 2025-26 page.
- Farm-to-table: vermontfresh.net (the Vermont Fresh Network's member search) disallows Claude's fetcher in robots.txt, so no board.
- Brewery kitchens: Foam Brewers' Deep City and Prohibition Pig need a 2025-26 page naming their kitchens; Hill Farmstead only hosts
  food trucks (the prompt), so it stays out.
- Blocked or unusable hosts: vermontpublic.org (robots disallows everyone), vermontfresh.net (robots disallows ClaudeBot),
  community.sevendaysvt.com (403).
""")
print(n_out, "| leads:", len(leads))
for l in leads: print(l)
