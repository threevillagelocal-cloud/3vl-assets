"""Build new Google + Facebook titles/descriptions for every listing -> seo_plan.json
Inputs: members.json (fetch.py), seo_src.json (fetch_seo.py). Nothing is written to BD here (see seo_apply.py)."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
EXCLUDE = {"5", "218"}

# first specialty -> a label that reads well in a title
LABEL = {
    "American": "American Restaurant", "Dinner": "Restaurant", "Breakfast": "Breakfast Restaurant", "Italian Food": "Italian Restaurant",
    "Mexican Food": "Mexican Restaurant", "Japanese Food": "Japanese Restaurant", "Asian Food": "Asian Restaurant", "BBQ": "BBQ Restaurant",
    "Healthy Eating": "Healthy Eats", "Wings": "Wings & Sports Bar", "Noodle Bar": "Noodle Bar", "Ice Cream": "Ice Cream Shop",
    "Condominiums": "Real Estate", "General Real Estate": "Real Estate", "Realtors": "Realtor", "Real Estate Salesperson": "Realtor",
    "Fashion": "Fashion Boutique", "Cards": "Card & Gift Shop", "Wine": "Wine Shop", "Bicycles": "Bike Shop", "Collectibles": "Collectibles Shop",
    "Jewelry": "Jewelry Store", "Electronics": "Electronics Store", "Children's Clothing": "Children's Clothing Store",
    "Picture Framing": "Custom Picture Framing", "Massage": "Massage Therapy", "Licensed clinical social worker": "Licensed Clinical Social Worker",
    "Civil rights Attorney": "Civil Rights Attorney", "Holistic": "Holistic Health", "Soccer": "Soccer Programs", "Tennis": "Tennis Programs",
    "Tours": "Tours", "Museums": "Museum", "Festivals": "Festival", "Artist": "Local Artist", "Cheerleading & Gymnastics Training": "Cheer & Gymnastics",
    "Psychologists & Mental Health Counseling": "Mental Health Counseling", "Hair Salons & Barber Shops": "Hair Salon & Barber",
}


def town(c):
    c = (c or "").strip()
    return "Setauket" if c.startswith("Setauket-") else c


def label(svcs, cat):
    s = (svcs or [""])[0].strip()
    s = LABEL.get(s, s)
    s = re.sub(r"\s*\([^)]*\)", "", s).strip()           # drop "(e.g., ...)" notes
    s = re.sub(r"\s*(Services|Service)$", "", s) if len(s) > 28 else s
    return s or (cat or "")


def fit(parts, limit):
    for p in parts:
        if p and len(p) <= limit:
            return p
    return parts[-1][:limit].rsplit(" ", 1)[0]


def clean_desc(t, limit=158):
    t = re.sub(r"\s+", " ", (t or "").replace(" ", " ")).strip()
    t = t.replace("Setauket-East Setauket", "Setauket").replace("Setauket- East Setauket", "Setauket")
    if len(t) <= limit and re.search(r"[.!?)\"]$", t):
        return t
    cut = t[:limit] + " "
    end = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    if end > 80:
        return cut[:end + 1]
    return cut.strip().rsplit(" ", 1)[0].rstrip(",;:-") + "..."


def plan_one(m, s):
    name = (m.get("company") or "").strip()
    t = town(m.get("city")); lab = label(s.get("services"), m.get("category"))
    if lab and lab.lower() in name.lower():
        lab = ""  # "Setauket Frame Shop | Frame Shop..." reads badly
    where = (" in %s" % t) if t else ""
    title = fit([f"{name} | {lab}{where}, NY" if t and lab else "", f"{name} | {lab}{where}" if lab else "",
                 f"{name} | {t}, NY" if t else "", f"{name} | Three Village Local", name], 65)
    og_title = fit([f"{name} | {lab}{where}" if lab else "", f"{name} | {t}" if t else "", name], 70)
    base = s.get("search_description") or ""
    if not base:
        what = (lab or m.get("category") or "local business").lower()
        base = f"{name} is a {what} in {t or 'the Three Village area'}, NY. See photos, hours, reviews and contact info."
    desc = clean_desc(base)
    og_desc = clean_desc(base, 150)
    return {"user_id": m["user_id"], "name": name, "seo_page_title": title, "seo_page_description": desc,
            "seo_social_page_title": og_title, "seo_social_page_description": og_desc}


def main():
    ms = {x["user_id"]: x for x in json.load(open(os.path.join(HERE, "members.json"), encoding="utf-8"))}
    src = {x["user_id"]: x for x in json.load(open(os.path.join(HERE, "seo_src.json"), encoding="utf-8"))}
    plan = [plan_one(ms[u], src.get(u, {})) for u in ms if u not in EXCLUDE]
    json.dump(plan, open(os.path.join(HERE, "seo_plan.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(len(plan), "planned")


if __name__ == "__main__":
    main()
