"""Banner reach number for the VIP Member Dashboard (owner exception 11/13/2026 to the no-raw-traffic rule, this one stat only).
N = sitewide GA4 screenPageViews, last 30 days (30daysAgo..yesterday). Every page shows the rotating VIP banners.
Writes data/banner_reach.json {"views": N, "start", "end", "fetched"}. Meant to run nightly (GitHub Action or the guard).
Run: python site/member-dashboard/banner_reach.py [--key path/to/service-account.json]
The key is read, never printed. Change the number source here only; the label lives in build.py BANNER_LABEL."""
import datetime as dt, json, os, sys

from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

HERE = os.path.dirname(os.path.abspath(__file__))
PROPERTY = "properties/485326487"
KEY = os.environ.get("GA4_KEY") or os.path.join(HERE, "..", "..", "..", "3vl-news-monitor", "service-account.json")
if "--key" in sys.argv:
    KEY = sys.argv[sys.argv.index("--key") + 1]
OUT = os.path.join(HERE, "data", "banner_reach.json")


def main():
    cred = service_account.Credentials.from_service_account_file(KEY, scopes=["https://www.googleapis.com/auth/analytics.readonly"])
    s = AuthorizedSession(cred)
    r = s.post("https://analyticsdata.googleapis.com/v1beta/%s:runReport" % PROPERTY, json={
        "dateRanges": [{"startDate": "30daysAgo", "endDate": "yesterday", "name": "cur"},
                       {"startDate": "60daysAgo", "endDate": "31daysAgo", "name": "prev"}],
        "metrics": [{"name": "screenPageViews"}]}, timeout=60)
    r.raise_for_status()
    vals = {}
    for row in r.json().get("rows") or []:   # with 2 date ranges GA4 adds a dateRange dimension
        dims = [d.get("value") for d in row.get("dimensionValues", [])]
        vals[dims[0] if dims else "cur"] = int(row["metricValues"][0]["value"])
    views, prev = vals.get("cur", 0), vals.get("prev", 0)
    if views <= 0:
        sys.exit("GA4 returned no page views; keeping the previous file")
    pct = round((views - prev) * 100.0 / prev) if prev else None
    # homepage views per day (for each member's spotlight days in the dashboard reach tile)
    r2 = s.post("https://analyticsdata.googleapis.com/v1beta/%s:runReport" % PROPERTY, json={
        "dateRanges": [{"startDate": "60daysAgo", "endDate": "yesterday"}], "dimensions": [{"name": "date"}],
        "dimensionFilter": {"filter": {"fieldName": "pagePath", "inListFilter": {"values": ["/", "/home"]}}},
        "metrics": [{"name": "screenPageViews"}], "limit": 100}, timeout=60)
    r2.raise_for_status()
    home = {}
    for row in r2.json().get("rows") or []:
        d = row["dimensionValues"][0]["value"]
        home["%s-%s-%s" % (d[:4], d[4:6], d[6:])] = int(row["metricValues"][0]["value"])   # true change, last 30 days vs the 30 before
    y = dt.date.today() - dt.timedelta(days=1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"views": views, "prev_views": prev, "change_pct": pct, "start": (y - dt.timedelta(days=29)).isoformat(), "end": y.isoformat(),
               "fetched": dt.datetime.now().isoformat(timespec="minutes"), "source": "GA4 screenPageViews, sitewide", "home_daily": home},
              open(OUT, "w", encoding="utf-8"), indent=1)
    print("banner reach", views, "prev", prev, "change %", pct)


if __name__ == "__main__":
    main()
