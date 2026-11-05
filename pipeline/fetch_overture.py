"""Download the Overture Maps extracts that vermont.py reads -> data/vt/

- overture_vt_bbox.parquet     every place in Vermont's bounding box (name, category, address, point)
- overture_vt_sources.parquet  which datasets each Vermont eating/drinking listing came from (Meta, Foursquare, ...)
- vt_shapes.json               simplified state and county outlines for the map
- vt_state_detail.geojson      the state outline at full detail, for the in-state test

Reads the public Overture bucket over S3 with DuckDB (no account needed). Ported from ut-eats/pipeline/fetch_overture.py.
Vermont: land division areas; Vermont's follows the state line through Lake Champlain, so the islands (Grand Isle, North Hero, Isle
La Motte) and the Vermont half of the lake are one polygon; the "counties" are Vermont's 14. Small islands are kept (min area 0.000005 deg2, about 5 ha), and the script checks the
islands and the towns across the Connecticut River, the New York line and the Canadian border (Norwich is in Vermont, Hanover and
Lebanon in New Hampshire; Plattsburgh in New York; Stanstead in Quebec).
"""
import os, json, time
import duckdb
from shapely import wkb
from shapely.geometry import mapping, Polygon

RELEASE = "2026-10-21.0"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "vt")
# Vermont (42.73°N–45.02°N, 71.46°W–73.44°W) plus a margin for the border towns (Derby Line, the Upper Valley, Bennington's New York
# neighbours) and Lake Champlain's New York shore
BBOX = "bbox.xmin BETWEEN -73.6 AND -71.3 AND bbox.ymin BETWEEN 42.6 AND 45.1"
EAT = "('restaurant','casual_eatery','bar','fast_food_restaurant','coffee_shop','cafe','smoothie_juice_bar','brewery','food_court')"
os.makedirs(OUT, exist_ok=True)

con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs; INSTALL spatial; LOAD spatial; SET s3_region='us-west-2';")
places = f"s3://overturemaps-us-west-2/release/{RELEASE}/theme=places/type=place/*.parquet"

t = time.time()
if not os.path.exists(f"{OUT}/overture_vt_bbox.parquet"):
    con.execute(f"""
COPY (
  SELECT id, names.primary AS name, basic_category AS cat, taxonomy.primary AS tax, taxonomy.hierarchy AS hier, confidence,
         operating_status AS status, brand.names.primary AS brand, addresses[1].freeform AS street, addresses[1].locality AS city,
         addresses[1].postcode AS zip, addresses[1].region AS region, ST_Y(geometry) AS lat, ST_X(geometry) AS lon, websites[1] AS web,
         phones[1] AS phone
  FROM read_parquet('{places}', hive_partitioning=1) WHERE {BBOX}
) TO '{OUT}/overture_vt_bbox.parquet' (FORMAT PARQUET)""")
    print("places in bbox", round(time.time() - t), "s", flush=True)
if not os.path.exists(f"{OUT}/overture_vt_sources.parquet"):
    con.execute(f"""
COPY (
  SELECT id, list_transform(sources, lambda x: x.dataset) AS ds, list_transform(sources, lambda x: x.update_time) AS ut,
         list_transform(sources, lambda x: x.record_id) AS rid,
         len(socials) AS n_soc, len(websites) AS n_web, len(phones) AS n_ph
  FROM read_parquet('{places}', hive_partitioning=1)
  WHERE {BBOX} AND basic_category IN {EAT}
) TO '{OUT}/overture_vt_sources.parquet' (FORMAT PARQUET)""")
    print("sources", round(time.time() - t), "s", flush=True)

areas = f"s3://overturemaps-us-west-2/release/{RELEASE}/theme=divisions/type=division_area/*.parquet"
rows = con.execute(f"""
  SELECT subtype, names.primary AS name, ST_AsWKB(geometry) AS g
  FROM read_parquet('{areas}', hive_partitioning=1)
  WHERE country = 'US' AND region = 'US-VT' AND subtype IN ('region', 'county') AND class = 'land'
    AND bbox.xmin > -73.7 AND bbox.xmax < -71.2 AND bbox.ymin > 42.5 AND bbox.ymax < 45.2""").fetchall()


def rings(geom, tol, min_area):
    geom = geom.simplify(tol, preserve_topology=True)
    polys = [p for p in getattr(geom, "geoms", [geom]) if p.geom_type == "Polygon" and p.area >= min_area]
    return [[[round(x, 3), round(y, 3)] for x, y in p.exterior.coords] for p in polys]


out = {"state": None, "counties": []}
for sub, name, g in rows:
    geom = wkb.loads(bytes(g)).buffer(0)
    if sub == "region":
        json.dump(mapping(geom.simplify(0.0005, preserve_topology=True)), open(f"{OUT}/vt_state_detail.geojson", "w"))
        out["state"] = [[r] for r in rings(geom, 0.002, 0.000005)]
    else:
        out["counties"].append({"name": name, "c": rings(geom, 0.004, 0.00002)})
# full-detail county polygons for assigning each place to a county (not shipped)
json.dump({name: mapping(wkb.loads(bytes(g)).buffer(0).simplify(0.0003, preserve_topology=True))
           for sub, name, g in rows if sub == "county"}, open(f"{OUT}/vt_counties_detail.geojson", "w"))
json.dump(out, open(f"{OUT}/vt_shapes.json", "w"), separators=(",", ":"))
print("outlines: state", len(out["state"] or []), "rings +", len(out["counties"]), "counties;", round(time.time() - t), "s total")
# islands, shores and border towns: each must fall on the right side of the detailed state outline
from shapely.geometry import shape, Point
st = shape(json.load(open(f"{OUT}/vt_state_detail.geojson")))
for nm, lon, lat, want in [("Isle La Motte", -73.3430, 44.8860, True), ("North Hero", -73.2720, 44.8300, True), ("Grand Isle", -73.2960, 44.7190, True),
                           ("Burlington waterfront", -73.2220, 44.4770, True), ("Plattsburgh, NY", -73.4520, 44.6990, False),
                           ("Norwich", -72.3080, 43.7160, True), ("Hanover, NH", -72.2890, 43.7020, False), ("Lebanon, NH", -72.2520, 43.6420, False),
                           ("White River Junction", -72.3200, 43.6490, True), ("Brattleboro", -72.5580, 42.8510, True), ("Hinsdale, NH", -72.4860, 42.7860, False),
                           ("Bennington", -73.1970, 42.8780, True), ("Hoosick Falls, NY", -73.3520, 42.9000, False), ("Williamstown, MA", -73.2040, 42.7120, False),
                           ("Derby Line", -72.0996, 45.0030, True), ("Stanstead, QC", -72.0900, 45.0200, False), ("Newport", -72.2050, 44.9360, True),
                           ("Bellows Falls", -72.4440, 43.1340, True), ("Walpole, NH", -72.4260, 43.0790, False)]:
    ok = st.contains(Point(lon, lat))
    print(f"  {nm}: {'inside' if ok else 'outside'}{'' if ok == want else '  <-- WRONG'}")
print("counties:", len(out["counties"]), sorted(c["name"] for c in out["counties"]))

# the neighbours' land (New York, New Hampshire, Massachusetts, Quebec): listings.py widens Vermont's outline ~300 m for lake shores,
# but only where no neighbour's land is, so a Hanover, NH or Plattsburgh, NY listing on the far side of the line stays out
nb = con.execute(f"""
  SELECT region, ST_AsWKB(geometry) FROM read_parquet('{areas}', hive_partitioning=1)
  WHERE ((country = 'US' AND region IN ('US-NY', 'US-NH', 'US-MA')) OR (country = 'CA' AND region = 'CA-QC'))
    AND subtype = 'region' AND class = 'land'""").fetchall()
from shapely.ops import unary_union
from shapely.geometry import box
near = box(-73.7, 42.5, -71.2, 45.2)
nbg = unary_union([wkb.loads(bytes(g)).buffer(0).intersection(near) for _, g in nb])
json.dump(mapping(nbg.simplify(0.0002, preserve_topology=True)), open(f"{OUT}/vt_neighbors.geojson", "w"))
print("neighbours:", sorted(r for r, _ in nb))
