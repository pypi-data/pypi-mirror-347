"""
Smoke-test for inat2wiki.parse_observation.get_commons_url
=========================================================

Goal right now
--------------

* Make sure the function **does not crash** (the old geojson==None bug).
* Make sure it returns a string that starts with the Wikimedia upload URL.

Adding more cases later
-----------------------

1.   Copy another observation file into tests/fixtures/.
2.   Append its file-name to the FIXTURES list – **nothing else to change**.
"""

import json
from pathlib import Path

import pytest

from inat2wiki.parse_observation import get_commons_url


# ----------------------------------------------------------------------
# 1️⃣  List the fixture files we want to test.  Just add new names later.
# ----------------------------------------------------------------------
FIXTURES = [
    "observation_279666022.json",  # obscured / private coordinates
    "observation_144917694.json",
    # "some_other_observation.json",   # put new fixtures here
]


# ----------------------------------------------------------------------
# 2️⃣  Parametrised test – runs once for every file named above
# ----------------------------------------------------------------------
@pytest.mark.parametrize("fixture_file", FIXTURES)
def test_get_commons_url_returns_upload_link(fixture_file):
    here = Path(__file__).parent  # tests/
    fp = here / "fixtures" / fixture_file
    obs = json.loads(fp.read_text())  # dict from JSON

    first_photo = obs["photos"][0]

    url = get_commons_url(obs, first_photo, obs["id"])

    # single, clear assertion: is it a Wikimedia upload URL?
    assert url.startswith("https://commons.wikimedia.org/wiki/Special:Upload")
