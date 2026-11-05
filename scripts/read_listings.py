"""Read Vermont's official tourism listings (plan.vermontvacation.com/listings/<n>; robots allows /listings) -> data/research/raw/
listings.json: name, address line, town, hours line and description, one polite request every 1.5 s. Private research notes only.
Usage: .venv/bin/python scripts/read_listings.py 86 75 ..."""
import html, json, os, re, sys, time
import requests
UA = "GreenMountainEatsSourceCheck/1.0 (+https://nickstrom5.github.io/vermont-eats/; nick@eatsranked.com)"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "research", "raw", "listings.json")
have = json.load(open(OUT)) if os.path.exists(OUT) else {}
for n in sys.argv[1:]:
    if n in have:
        continue
    r = requests.get(f"https://plan.vermontvacation.com/listings/{n}", headers={"User-Agent": UA}, timeout=30)
    t = r.text
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)))
    m = re.search(r'single-listing-content">\s*<h4>(.*?)</h4>\s*(?:<div class=.text-muted.>(.*?)</div>)?\s*(?:<div class="listing-seasons text-muted">(.*?)</div>)?', t, re.S)
    clean = lambda x: html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x or "")).strip()) or None
    name, addr, season = (clean(m.group(1)), clean(m.group(2)), clean(m.group(3))) if m else (None, None, None)
    i = txt.find(name) if name else -1
    have[n] = {"status": r.status_code, "name": name, "addr": addr, "season": season, "text": txt[i:i + 1600] if i >= 0 else ""}
    print(n, r.status_code, name, "|", addr, "|", season, flush=True)
    json.dump(have, open(OUT, "w"), indent=1, ensure_ascii=False)
    time.sleep(1.5)
