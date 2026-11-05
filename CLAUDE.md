# Green Mountain Eats (vt-eats) — notes for Claude Code sessions

Built 2026-11-05 by a side session for Nick's "build Utah, Vermont, Virginia, West Virginia and Wyoming", ported from `../ut-eats/`
(itself from `../md-eats/`) with every fix to that day (the 10-29 all-states QA P0/P1s, Nevada's `name_key()` ids, the narrowed loan
rule, the exact-outline county lookup, the out-of-county truck rule, the web map frame and Back key, Utah's street-word merge fix).
Local only: git-ignored data, no repo, no remote, nothing published. Sources and calibration: `playbook/12-sources.md`. Brand:
`playbook/05-naming.md` — **provisional**, every choice waits for Nick ("Green Mountain Eats: Vermont Restaurants", Home Screen "Green
Mountain Eats"; "Vermont Eats" belongs to the Eat Vermont app; a maple creemee icon, concept A, on spruce; the landscape palette from
`state-prompts/VERMONT_PROMPT.md`: spruce #1E4D2B, maple amber #A0521D, barn red #9E2A2B, syrup gold #D9A441 fill only; a Green
Mountains ridgeline band rising to Camel's Hump).

## Vermont is different
- **No official list a script may read.** The Department of Health's Food and Lodging inspections are search-only
  (vtdoh.safefoodinspection.com, May 2016 on; its Export link is untested and needs Nick's OK), data.vermont.gov has no food or
  inspection dataset, and the Department of Liquor and Lottery's licensee databases are view-only Power BI pages (its open data ends
  in 2020). `official.load()` returns an empty table; the pipeline runs on it (0 official places, "Serves alcohol" unknown everywhere,
  no inspection results). A Public Records Act request is Nick's call.
- **Counties:** Vermont's 14 from Overture's land division areas. Vermont's outline follows the state line through Lake Champlain, so the
  islands and the Vermont half of the lake are one polygon; `fetch_overture.py` checks the islands and the border towns (Norwich in,
  Hanover and Lebanon NH, Plattsburgh NY and Stanstead QC out). **One detail file** (`detail-vermont.json`), as the prompt asks; the
  site groups guide pages by county.
- **Towns:** villages map to their towns (`common.canon_city`: Manchester Center is Manchester, White River Junction and Quechee are
  Hartford, Proctorsville is Cavendish); Essex Junction is its own city.
- **Honors:** no MICHELIN Guide covers Vermont. James Beard: Al's French Frys (America's Classics 2010), Saap (Best Chef: Northeast
  winner 2022), and the 2025-26 finalists and semifinalists (May Day, Grey Jay, Wolf Tree, Canteen Creemee, The Crooked Ram, Ondis,
  Juniper, Leslie McCrorey Wells's Pizzeria Verità, Trattoria Delia and Sotto Enoteca, Café Monette). Fancy's and Honey Road aren't in
  our map data (`data/research/app/LEADS.md`).
- **Guides** (tags in `vermont.py` TAGS; bits 1..128): diners & fry stands (Seven Days, updated July 2025; Yankee 2025; JBF), maple
  creemees (the Department of Tourism's creemee page), cider mills, wood-fired & farm pizza, sugarhouses, brewery kitchens, historic inns
  & taverns (the Department of Tourism's per-business listings, read by `scripts/read_listings.py`; Tasting Table for Ye Olde Tavern),
  oldest (Ye Olde Tavern 1790, Jasper Murdock's at the Norwich Inn 1797, Al's French Frys 1946). Many are seasonal.
- **Adult rule:** "dejavu" alone in a website no longer counts (it hid Morristown's Deja Vu Cafe via a Cash App link); the chain's
  domain is dejavu.com.
- **Ranking:** "Featured first" (honors, then founding year), as everywhere until Nick decides on the all-factor Ranked score
  (`eats-ranked-score-all-states-proposal-2026-11-05.md` in the shared notes). The export already carries its inputs (hand-checked,
  honors, founding year, chain count); no health-grade wording anywhere.

## Rebuild
```bash
cd pipeline
../.venv/bin/python check_sources.py URL...   # a new host first
../.venv/bin/python fetch_overture.py && ../.venv/bin/python fetch_extras.py && ../.venv/bin/python fetch_official.py
../.venv/bin/python geocode_official.py && ../.venv/bin/python geocode_census.py && ../.venv/bin/python listings.py
../.venv/bin/python calibrate.py && ../.venv/bin/python vermont.py && ../.venv/bin/python build_research.py && ../.venv/bin/python vermont.py
VT_APP=1 ../.venv/bin/python vermont.py && cd .. && cp data/app/places.json data/app/detail-*.json VermontEats/Resources/
.venv/bin/python pipeline/check_websites.py --retry-transient   # link verification; re-export after
.venv/bin/python scripts/make-site.py && .venv/bin/python scripts/publish_app_data.py && .venv/bin/python scripts/publish_app_data.py --check
.venv/bin/python scripts/qa-site.py --static
```
(`listings.py` must run before `calibrate.py`, and `vermont.py` once before `build_research.py`, which matches names against
`site/vermont.json`.) The `.venv` is on the python.org framework Python 3.12 (Homebrew's python@3.12 is gone), with md-eats' versions.
`data/ucsd/meta-Vermont.json.gz` (Google 2021, private, web build only) comes from mcauleylab.ucsd.edu's googlelocal set.
`scripts/read_listings.py` and `scripts/search_listings.py` read the Department of Tourism's listings (one request per 1.5 s) into
`data/research/raw/` (private).

## App, site, screenshots
- App: `VermontEats/` (XcodeGen `project.yml`, bundle `com.vermonteats.ios`, display "Green Mountain Eats"), tests in `VermontEatsTests/` (data guards:
  adult venues, blocklisted and multi-URL websites, bad and legal names, non-restaurants, listed twice, no Google data; MICHELIN; the
  outline with Hanover and Plattsburgh). Run tests: `DEVELOPER_DIR="/Applications/Xcode 1.app/Contents/Developer" xcodebuild test ...
  CODE_SIGNING_ALLOWED=NO` on a temporary simulator. Archive only with Xcode 1.app (now 27.2, 27B52); Xcode.app is a beta.
  Run `xcodegen generate` after the export whenever the set of `Resources/*.json` files changes (an app built without them still
  compiles but opens on "Couldn't open the list").
- Site: `scripts/make-site.py` writes `docs/` (16 pages; one city page, Burlington) and
  `playbook/site-numbers.json`; `scripts/explore.js` is the web app; `scripts/qa-site.py` the QA. Site URL for now:
  nickstrom5.github.io/vermont-eats (no CNAME). Rebuild the site before the unit tests: `ShareLinkTests` reads the web app's ids from `docs/`.
- OTA data: `docs/data/app/` via `scripts/publish_app_data.py` (`../OTA-DATA.md`).
- Screenshots: `scripts/capture-screenshots.sh <sim>` (ScreenshotMode pins downtown Burlington; Montpelier for creemees, Waitsfield
  for brewery kitchens, Woodstock for inns), then `scripts/site-images.sh`, then make-site + qa-site. App Store frames:
  `scripts/appstore-screenshots.py`. Icons: `scripts/icon-concepts.swift` (A maple creemee, B syrup jug, C apple pie with cheddar; all
  pass `state-prompts/icon-style/check.swift`; C reads as a box at 60 px, B is the clearest alternate) and `scripts/make-brand.swift`.
- Not ported: the App Store listing writer and the private Google-2021 leaderboard. `site/` holds the leaderboard's data and is
  git-ignored with `data/`.

## Fixes after the first build (2026-11-05)
- **UI test:** the "my location" map check used Baltimore's Inner Harbor (from md-eats); now this state's own downtown.
- **Last full run** 2026-11-05: app 1,632 places / 1,576 restaurants, 49 unit tests on iPhone 17 Pro Max (iOS 27.0), the detail
  and 6 iPad screens re-captured after the ZIP fix, `qa-site.py --static` OK, OTA 2026-11-05.1 (local only).
- **ZIPs:** the export (`pipeline/vermont.py`, the place's `z` and the address-strip pattern) still kept only Maryland's 206xx-219xx, carried
  from md-eats, so the app showed addresses without a ZIP and ZIP search found little. Now this state's own range (050xx-054xx and 056xx-059xx); the
  detail screenshot was re-captured.
- **Web app:** `scripts/explore.js`'s place panel named Utah's "Department of Alcoholic Beverage Services" as the liquor licensor (a
  ut-eats leftover); it now says what the app's PlaceDetailView says.

## Rules
No commits, pushes, public repos, App Store Connect or DNS changes without Nick's yes each time; never submit for review or accept
agreements; never publish Google-derived data. Support email nick@eatsranked.com. Commit author "Nick Soderstrom"
<329204362+nickstrom5@users.noreply.github.com> via `-c user.name -c user.email`.
