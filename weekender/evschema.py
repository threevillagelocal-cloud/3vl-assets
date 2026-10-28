"""schema.org Event helpers shared by the homepage (nowhome_build.py) and the site-guard event pages.

Only facts the event data already has are used: no guessed prices, organizers or street addresses.
Copies: 3vl-assets/weekender/evschema.py and 3vl-site-guard/scripts/evschema.py; keep the two the same.
"""
import re

# ZIP for a town name (used only when the address itself has no ZIP)
ZIPS = {"stony brook": "11790", "setauket": "11733", "east setauket": "11733", "old field": "11733", "poquott": "11733",
        "port jefferson": "11777", "port jefferson village": "11777", "port jefferson station": "11776",
        "centereach": "11720", "miller place": "11764", "mount sinai": "11766", "st. james": "11780", "saint james": "11780",
        "head of the harbor": "11780", "smithtown": "11787"}
TOWNS = sorted(ZIPS, key=len, reverse=True)

# feeds whose events are run by the feed's own organization (other feeds list events by many groups)
ORGS = {"emmaclark": ("Emma S. Clark Memorial Library", "https://www.emmaclark.org/"),
        "lim": ("The Long Island Museum", "https://longislandmuseum.org/"),
        "limehof": ("Long Island Music and Entertainment Hall of Fame", "https://www.limusichalloffame.org/"),
        "wmho": ("Ward Melville Heritage Organization", "https://wmho.org/")}

OFFLINE = "https://schema.org/OfflineEventAttendanceMode"
ONLINE = "https://schema.org/OnlineEventAttendanceMode"


def _town(s):
    s = (s or "").strip().lower()
    if s.endswith(" village") and s[:-8] in ZIPS:
        s = s[:-8]
    return s if s in ZIPS else ""


def _title(s):
    return " ".join(w if w.lower() in ("of", "the") else w[:1].upper() + w[1:] for w in s.split())


def postal_address(addr, town="", venue=""):
    """'93 N. Country Rd, East Setauket' / '120 Main St, Setauket, NY 11733' / 'Park - 101 East Broadway Port Jefferson NY 11777'
    -> PostalAddress with only the parts we can read. None when there is not even a town."""
    a = (addr or "").strip()
    if " - " in a:
        a = a.split(" - ")[-1].strip()
    z = re.search(r"\b(\d{5})(?:-\d{4})?\s*$", a)
    zp = z.group(1) if z else ""
    if z:
        a = a[:z.start()].strip()
    a = re.sub(r"[,\s]+(NY|New York)\s*$", "", a, flags=re.I).strip(" ,")
    parts = [p.strip() for p in a.split(",") if p.strip()]
    street = loc = ""
    if len(parts) >= 2:
        street, loc = parts[0], parts[1]
    elif len(parts) == 1:
        p = parts[0]
        hit = next((t for t in TOWNS if p.lower().endswith(" " + t) or p.lower() == t), "")
        if hit and p.lower() != hit:
            street, loc = p[:len(p) - len(hit)].strip(), p[len(p) - len(hit):]
        elif hit or not re.match(r"\d", p):
            loc = p
        else:
            street = p
    if not loc:
        loc = town or ""
    if not loc and _town(venue):
        loc = _title(_town(venue))
    if re.search(r"village$", loc, re.I) and _town(loc):
        loc = _title(_town(loc))
    if not loc and not street:
        return None
    out = {"@type": "PostalAddress"}
    if street and re.match(r"\d", street):
        out["streetAddress"] = street
    if loc:
        out["addressLocality"] = loc
    zp = zp or ZIPS.get(_town(loc), "")
    out["addressRegion"] = "NY"
    if zp:
        out["postalCode"] = zp
    out["addressCountry"] = "US"
    return out


def location(venue, addr, town="", url=""):
    """(location dict, attendance mode) or (None, None) when we cannot say where it is."""
    v = (venue or "").strip()
    if v.lower().startswith("online"):
        return ({"@type": "VirtualLocation", "url": url} if url else None), ONLINE
    if v.lower().startswith("off site"):
        return None, None
    ad = postal_address(addr, town, v)
    if not ad:
        return None, None
    name = v or ad.get("addressLocality", "")
    return {"@type": "Place", "name": name, "address": ad}, OFFLINE


def organizer_for_src(src):
    o = ORGS.get(src or "")
    return {"@type": "Organization", "name": o[0], "url": o[1]} if o else None


def is_free(ev):
    """Feed events: 'free' tag is guessed from words, so it only counts when no price or admission is mentioned.
    Hand-entered events (src 3vl) carry checked tags."""
    if "free" not in (ev.get("tags") or []):
        return False
    if ev.get("src") == "3vl":
        return True
    blob = ((ev.get("title") or "") + " " + (ev.get("desc") or "")).lower()
    return bool(re.search(r"\bfree\b", blob)) and not re.search(r"\$\s*\d|admission|per person|ticket|\bfee\b", blob)


def offers(cost="", free=False, url=""):
    """Offer only when the price is stated: free (tag or 'Free'), '$10', '$30 online', 'from $20'."""
    c = (cost or "").strip().lower()
    off = None
    if free or c.startswith("free"):
        off = {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    else:
        m = re.search(r"\$\s*(\d+(?:\.\d\d)?)", c)
        if m and "from" in c:
            off = {"@type": "AggregateOffer", "lowPrice": m.group(1), "priceCurrency": "USD"}
        elif m and not re.search(r"\$\s*\d+(?:\.\d\d)?\D+\$", c):
            off = {"@type": "Offer", "price": m.group(1), "priceCurrency": "USD"}
    if off and url:
        off["url"] = url
    return off


def status(s):
    s = (s or "").lower()
    if "cancel" in s:
        return "https://schema.org/EventCancelled"
    if "postpon" in s:
        return "https://schema.org/EventPostponed"
    if "resched" in s:
        return "https://schema.org/EventRescheduled"
    return "https://schema.org/EventScheduled"
