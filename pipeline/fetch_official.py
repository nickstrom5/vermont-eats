"""Vermont's open official records -> data/raw/official/ (git-ignored, never public). Nothing to fetch yet.

Checked 2026-11-05 (playbook/12-sources.md): the Department of Health's Food and Lodging inspections are search-only
(vtdoh.safefoodinspection.com; its Export link is untested and not to be relied on without Nick's OK); data.vermont.gov has no food or
inspection dataset; the Department of Liquor and Lottery's licensee databases are view-only Power BI pages, and its open data ends in
2020. When a list turns up (a Public Records Act response), add its loader to official.py and its download here, after
check_sources.py clears the host, one request at a time, with no owner or person names requested.
"""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "official")
os.makedirs(OUT, exist_ok=True)
json.dump({}, open(os.path.join(OUT, "meta.json"), "w"))
print("Vermont: no official list to fetch (see the docstring)")
