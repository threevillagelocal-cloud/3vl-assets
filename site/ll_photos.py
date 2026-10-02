"""/locallistings (BD web page 43): point the card photos at our own small copies.
Run after EVERY weekly update of the page:  python site/ll_photos.py   (add --dry to only show what would change)

House photos -> 800px copy, agent headshots (shown at 64px) -> 160px copy, both at
https://threevillagelocal-cloud.github.io/3vl-share/t/<fnv1a(url)>-<width>.webp (same naming as sm() / 3vl-share t/gen.py).
Each <img> keeps the original in data-o and falls back to it if the copy is ever missing.
The first card's photo loads at once (no lazy, high priority) and the first two cards skip the fade-in,
so the top of the page is not held back. Copies are made here, pushed to 3vl-share and confirmed served
BEFORE the page is changed. gen.py keeps them alive afterwards (it reads data-o / data-w from the live page)."""
import html, json, os, re, subprocess, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SHARE_T = os.path.normpath(os.path.join(HERE, "..", "..", "3vl-share", "t"))
sys.path.insert(0, os.path.join(HERE, "share-img"))
sys.path.insert(0, SHARE_T)
from bdkey import key
import gen

API = "https://www.threevillagelocal.com/api/v2/"
BASE = "https://threevillagelocal-cloud.github.io/3vl-share/t/"
FALLBACK = "this.onerror=null;this.src=this.dataset.o"
DRY = "--dry" in sys.argv


def api(path, data=None, method=None):
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    r = urllib.request.Request(API + path, data=body, method=method or ("POST" if data is not None else "GET"),
                               headers={"X-Api-Key": key(), "User-Agent": "Mozilla/5.0 3VL-maint",
                                        "Content-Type": "application/x-www-form-urlencoded"})
    return json.loads(urllib.request.urlopen(r, timeout=300).read().decode("utf-8", "replace"))


def attr(tag, name):
    m = re.search(r'\s%s="([^"]*)"' % name, tag)
    return m.group(1) if m else None


def setattr_(tag, name, val):
    if attr(tag, name) is not None:
        return re.sub(r'(\s%s=")[^"]*(")' % name, lambda m: m.group(1) + val + m.group(2), tag, count=1)
    return tag[:-1] + ' %s="%s">' % (name, val)


def homes_ld(content):
    """Search-engine data for the cards (schema.org ItemList of Offers), read from the card text itself. No backslashes: BD strips them."""
    def txt(card, cls):
        m = re.search(r'class="%s">([^<]*)<' % cls, card)
        return html.unescape(m.group(1)).strip() if m else ""
    items = []
    for card in re.split(r'class="bdai-listing-card(?: bdai-reveal)?"', content)[1:]:
        title, price = txt(card, "bdai-listing-card-title"), re.sub(r"[^\d]", "", txt(card, "bdai-listing-price"))
        link = re.search(r'<a href="([^"]+)"', card)
        if not title or not price or not link:
            continue
        street, _, rest = title.partition("|")
        mz = re.match(r"\s*(.*?)\s*(\d{5})\s*$", rest)
        home = {"@type": "SingleFamilyResidence", "name": title.replace(" | ", ", "),
                "address": {"@type": "PostalAddress", "streetAddress": street.strip(), "addressRegion": "NY", "addressCountry": "US"}}
        if mz:
            home["address"]["addressLocality"], home["address"]["postalCode"] = mz.group(1), mz.group(2)
        det = txt(card, "bdai-listing-address")
        for key, pat in (("numberOfBedrooms", r"([\d.]+)\s*Bed"), ("numberOfBathroomsTotal", r"([\d.]+)\s*Bath")):
            m = re.search(pat, det)
            if m:
                home[key] = float(m.group(1)) if "." in m.group(1) else int(m.group(1))
        m = re.search(r"([\d,]+)\s*SqFt", det)
        if m:
            home["floorSize"] = {"@type": "QuantitativeValue", "value": int(m.group(1).replace(",", "")), "unitCode": "FTK"}
        m = re.search(r'<img[^>]+>', card)
        pic = m and (attr(m.group(0), "data-o") or attr(m.group(0), "src"))
        if pic:
            home["image"] = html.unescape(pic)
        offer = {"@type": "Offer", "price": int(price), "priceCurrency": "USD", "url": html.unescape(link.group(1)), "itemOffered": home}
        agent, firm = txt(card, "bdai-realtor-name"), txt(card, "bdai-realtor-company")
        if agent:
            offer["offeredBy"] = {"@type": "RealEstateAgent", "name": agent + (" - " + firm if firm else "")}
        items.append({"@type": "ListItem", "position": len(items) + 1, "item": offer})
    if not items:
        return ""
    ld = json.dumps({"@context": "https://schema.org", "@type": "ItemList", "name": "Homes for sale this week in the Three Village area",
                     "numberOfItems": len(items), "itemListElement": items}, ensure_ascii=False, separators=(",", ":"))
    return "" if "\\" in ld else '<script type="application/ld+json">' + ld + "</script>"


def main():
    r = api("list_seo/get/43")
    page = r["message"][0] if isinstance(r["message"], list) else r["message"]
    content = page["content"]
    man = json.load(open(gen.MAN))
    need, first = {}, [True]

    def fix(tag, width):
        orig = attr(tag, "data-o") or attr(tag, "src")
        u = gen.norm(orig)
        if gen.skip(u):
            return tag
        k = gen.fnv(u)
        name = "%s-%d.webp" % (k, width)
        if not os.path.exists(os.path.join(SHARE_T, name)):
            need[(k, width)] = u
        tag = setattr_(tag, "data-o", orig)
        tag = setattr_(tag, "data-w", str(width))
        tag = setattr_(tag, "onerror", FALLBACK)
        tag = setattr_(tag, "src", BASE + name)
        if width == 800 and first[0]:
            first[0] = False
            tag = re.sub(r'\sloading="lazy"', "", tag)
            tag = setattr_(tag, "fetchpriority", "high")
        return tag

    def card_photo(m):
        return m.group(1) + fix(m.group(2), 800)

    def headshot(m):
        return m.group(1) + fix(m.group(2), 160)

    new = re.sub(r'(<div class="bdai-bleed-card">(?:<a [^>]*>)?)(<img[^>]+>)', card_photo, content)
    new = re.sub(r'(<div class="bdai-realtor-photo">)(<img[^>]+>)', headshot, new)
    # first two cards: no fade-in
    if 'class="bdai-listing-card"' not in new:
        new = new.replace('class="bdai-listing-card bdai-reveal"', 'class="bdai-listing-card"', 2)
    # image descriptions: the address on the house photo, the agent's name on the headshot
    parts = re.split(r'(class="bdai-listing-card(?: bdai-reveal)?")', new)   # [before, sep, card, sep, card, ...]
    for i in range(2, len(parts), 2):
        t = re.search(r'class="bdai-listing-card-title">([^<]*)<', parts[i])
        n = re.search(r'class="bdai-realtor-name">([^<]*)<', parts[i])
        if t:
            parts[i] = parts[i].replace('alt="house front"', 'alt="%s, home for sale"' % t.group(1).replace(" | ", ", ").replace('"', "").strip(), 1)
        if n:
            parts[i] = parts[i].replace('alt="agent headshot"', 'alt="%s"' % n.group(1).replace('"', "").strip(), 1)
    new = "".join(parts)
    cards = new.count('class="bdai-listing-card bdai-reveal"') + new.count('class="bdai-listing-card"')
    print("cards %d | photos pointed at copies %d | copies to make %d" % (cards, new.count(' data-o="'), len(need)))
    # head: the first house photo starts downloading with the page itself, plus the search-engine data for every card
    top = re.search(re.escape(BASE) + r"[0-9a-f]{8}-800\.webp", new)
    head = ('<link rel="preload" as="image" href="%s" fetchpriority="high">' % top.group(0) if top else "") + homes_ld(new)
    print("search data: %d homes" % head.count('"ListItem"'))
    if new == content and (page.get("content_head") or "").strip() == head:
        print("nothing to change")
        return
    if DRY:
        return
    for (k, w), u in need.items():
        for width, b in gen.make(u, [w]).items():
            open(os.path.join(SHARE_T, "%s-%d.webp" % (k, width)), "wb").write(b)
            print("  made %s-%d.webp %d KB  <- %s" % (k, width, len(b) // 1024, u[-50:]))
        man.setdefault(k, {"u": u})["seen"] = gen.TODAY
    if need:
        json.dump(man, open(gen.MAN, "w"), indent=0, sort_keys=True)
        repo = os.path.dirname(SHARE_T)
        subprocess.run(["git", "pull", "--rebase", "--autostash", "-q"], cwd=repo, check=True)
        subprocess.run(["git", "add", "t"], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "Listing page photo copies"], cwd=repo, check=True)
        subprocess.run(["git", "push", "-q"], cwd=repo, check=True)
    # never point the page at a file that is not being served yet
    urls = sorted(set(re.findall(re.escape(BASE) + r"[0-9a-f]{8}-\d+\.webp", new)))
    for attempt in range(40):
        bad = []
        for u in urls:
            try:
                urllib.request.urlopen(urllib.request.Request(u, method="HEAD", headers=gen.UA), timeout=20)
            except Exception:
                bad.append(u)
        if not bad:
            break
        print("  waiting for %d copies to be served..." % len(bad))
        time.sleep(15)
    if bad:
        sys.exit("ABORT: copies not served, page left unchanged: %s" % bad[:3])
    res = api("list_seo/update", {"seo_id": 43, "content": new, "content_head": head}, "PUT")
    print("page update:", res.get("status"), str(res.get("message"))[:120])
    print("NOW: refresh the site cache (web pages) and check the live page.")


if __name__ == "__main__":
    main()
