"""Search Vermont's official tourism listings (plan.vermontvacation.com/listings?search[query]=...; robots allows /listings) and print
each hit's id, name and address. One request every 1.5 s. Private research notes only.
Usage: .venv/bin/python scripts/search_listings.py creemee "sugar house" ..."""
import html, re, sys, time, urllib.parse
import requests
UA = "GreenMountainEatsSourceCheck/1.0 (+https://nickstrom5.github.io/vermont-eats/; nick@eatsranked.com)"
for q in sys.argv[1:]:
    t = requests.get("https://plan.vermontvacation.com/listings?search%5Bquery%5D=" + urllib.parse.quote(q), headers={"User-Agent": UA}, timeout=30).text
    hits = re.findall(r'/listings/(\d+)[^"]*"\s+class="listing-tile-link">(.*?)</a>.*?<p class="tile-address"><span class="address-line-1">(.*?)</span>\s*<span class="address-line-2">(.*?)</span>', t, re.S)
    print(f"== {q}: {len(hits)}")
    for n, name, a1, a2 in hits:
        print(f"  {n}\t{html.unescape(name).strip()}\t{html.unescape(a1).strip()}, {html.unescape(a2).strip()}")
    time.sleep(1.5)
