# Vermont sources and calibration (checked 2026-11-05)

## Official sources
| Source | What it has | Can a script read it? | Used |
|---|---|---|---|
| Vermont Department of Health, Food and Lodging Program (healthvermont.gov/environment/food-lodging-program, updated 2026-06-24) | licenses and inspects the food establishments that serve the public; no local health departments | no list | no |
| VDH inspection portal (vtdoh.safefoodinspection.com/Inspection/PublicInspectionSearch.aspx) | inspections May 2016 to the present: last inspection's findings, inspector comments, score | search form only; an untested Export link (Nick's OK first) | linked from every place |
| data.vermont.gov (Socrata catalog, domains=data.vermont.gov) | no food, restaurant or inspection dataset; liquor data only for 2018 and 2019-2020 | n/a | no |
| Department of Liquor and Lottery (liquorcontrol.vermont.gov) | First Class (on-premises beer and wine) and Third Class (spirits) licensees | view-only Power BI pages; no download | no: "Serves alcohol" is "—" |
| VCGI statewide parcels (grand list values) | building values | freely available, no license stated | no (Nick's call) |

So `official.load()` is empty, as Utah's is: 0 official places, no inspection result, no alcohol status. A Public Records Act request
(1 V.S.A. § 315; FoodLodging@vermont.gov) is Nick's call.

## Calibration
- BLS QCEW: 1,494 private NAICS 722 establishments (2025 average, per the prompt). Overture: 3,460 eating and drinking listings in
  Vermont; 3,429 after cleaning; the family's keep rule keeps 1,631; the App Store build ships **1,632 places, 1,576 restaurants**
  (171 towns, 14 counties).
- Google 2021 (private, web build only): 2,165 Vermont food listings, 1,524 matched.
- Website links: 1,442 checked, 914 OK; the rest dropped (`data/vt/website_check.json`).

## Research sources (each place cites its own; data/research/app/*.json)
- The Vermont Department of Tourism's per-business listings, plan.vermontvacation.com/listings/<n> (robots allows /listings), read by
  scripts/read_listings.py, one request per 1.5 s.
- vermontvacation.com "Where to Find a Creemee in Vermont" (© 2026 State of Vermont).
- Seven Days, "What Vermont's Classic American Diners Tell Us…" (2024-07-03, updated 2025-07-30).
- Yankee Magazine (newengland.com), "2025 Vermont Travel Guide" (2025-04-24): Country Girl Diner, Best Diner.
- Tasting Table, oldest restaurant in every state (2025-09-23): Ye Olde Tavern, 1790.
- jamesbeard.org: 2026 semifinalists (01-21) and nominees (03-31), 2025 semifinalists (01-22) and nominees (04-02), the 2022 winners,
  the 2010 America's Classics post for Al's French Frys.
- Not usable: vermontfresh.net (robots disallows ClaudeBot), vermontpublic.org (robots disallows everyone), community.sevendaysvt.com (403).
- No MICHELIN Guide covers Vermont.
