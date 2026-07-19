#!/usr/bin/env python3
"""
Scraper kpopofficial.com -> comebacks.json
Lancé par la GitHub Action (cron quotidien) ou à la main :
  python3 scripts/update_data.py

Récupère le planning annuel, garde les sorties récentes (J-14) et à venir,
puis visite chaque fiche album pour la tracklist, les photos et les réseaux.
Stdlib uniquement, pas de dépendances.
"""
import json
import re
import sys
import time
import html as ht
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = "https://kpopofficial.com/kpop-comebacks/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; nonowarwood-comeback-tracker; +https://nonowarwood.github.io/comebacks/)"}
KST = timezone(timedelta(hours=9))
OUT = Path(__file__).resolve().parent.parent / "comebacks.json"

MONTHS = {m: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"])}

TYPE_RE = re.compile(
    r"((?:\d+(?:st|nd|rd|th)\s+)?(?:Japan\s+|Japanese\s+|Summer\s+|Winter\s+|Special\s+|Pre-release\s+|Debut\s+)*"
    r"(?:Mini Album|Full Album|Single Album|Studio Album|Album|EP|Digital Single|Single|OST|Repackage|Mixtape|Comeback))",
    re.I)


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def clean(s):
    s = ht.unescape(s)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).replace("‘", "'").replace("’", "'") \
            .replace("“", '"').replace("”", '"').strip()


def parse_when(text):
    """'August 7, 2026 · Friday · 1 PM KST' -> datetime KST (heure par défaut : minuit)."""
    m = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December)"
                  r"\s+(\d{1,2}),\s*(\d{4})", text)
    if not m:
        return None
    month, day, year = MONTHS[m.group(1)], int(m.group(2)), int(m.group(3))
    hour, minute = 0, 0
    t = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(AM|PM)", text, re.I)
    if t:
        hour = int(t.group(1)) % 12
        minute = int(t.group(2) or 0)
        if t.group(3).upper() == "PM":
            hour += 12
    return datetime(year, month, day, hour, minute, tzinfo=KST)


def split_title(h3_text, album_meta):
    """'Stray Kids Mini Album – THIS & THAT (2026)' + 'Mini Album – THIS & THAT'
    -> artist, type, album_title"""
    text = re.sub(r"\s*\(\d{4}\)\s*$", "", h3_text)
    rtype, album = "", None
    if album_meta:
        parts = album_meta.split(" – ", 1)
        rtype = parts[0].strip()
        album = parts[1].strip() if len(parts) > 1 else None
    left = text.split(" – ", 1)[0]
    if rtype and left.lower().endswith(rtype.lower()):
        artist = left[: -len(rtype)].strip()
    else:
        m = TYPE_RE.search(left)
        if m:
            artist = left[: m.start()].strip()
            rtype = rtype or m.group(1).strip()
        else:
            artist = left.strip()
    return artist or left.strip(), rtype, album


MONTH_ABBR = {m[:3].upper(): i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"])}


def parse_year_page(src):
    """Les sorties sont des <li class="gspbgrid_item ... type-album"> avec
    lien titré, jour + mois abrégé en metas, et visuel."""
    entries = []
    for m in re.finditer(r'<li class="gspbgrid_item[^"]*type-album[^"]*">(.*?)</li>', src, re.S):
        block = m.group(1)
        link = re.search(r'<a class="gspbgrid_item_link" title="([^"]+)" href="([^"]+)"', block)
        if not link:
            continue
        h3_text, url = clean(link.group(1)), link.group(2)
        metas = [clean(x) for x in re.findall(r'<span class="gspb_meta_value">(.*?)</span>', block, re.S)]
        when = next((parse_when(x) for x in metas if parse_when(x)), None)
        if when is None:
            day = next((int(x) for x in metas if re.fullmatch(r"\d{1,2}", x)), None)
            mon = next((MONTH_ABBR[x] for x in metas if x in MONTH_ABBR), None)
            ym = re.search(r"\((\d{4})\)", h3_text)
            if day and mon and ym:
                when = datetime(int(ym.group(1)), mon, day, tzinfo=KST)
        title_track = next((re.sub(r'^Title\s*–\s*', "", x).strip('"') for x in metas if x.startswith("Title –")), None)
        album_meta = next((x for x in metas if " – " in x and not x.startswith("Title –") and not parse_when(x)), None)
        imgs = re.findall(r'data-orig-file="([^"]+)"', block) or \
               re.findall(r'src="(https://kpopofficial\.com/wp-content/uploads/[^"]+)"', block)
        artist, rtype, album = split_title(h3_text, album_meta)
        entries.append({
            "artist": artist, "type": rtype or "Comeback", "title": album,
            "titleTrack": title_track, "date": when.isoformat() if when else None,
            "img": imgs[0] if imgs else None, "url": url,
        })
    return entries


def parse_album_page(src):
    """Fiche album -> artiste exact, date+heure, tracklist, photos, réseaux."""
    out = {"tracklist": [], "photos": [], "links": []}
    txt = re.sub(r"<script.*?</script>", "", src, flags=re.S)
    txt = re.sub(r"<style.*?</style>", "", txt, flags=re.S)
    body = txt[txt.find("Album Details"):] if "Album Details" in txt else txt
    plain = [l.strip() for l in re.sub(r"<[^>]+>", "\n", ht.unescape(body)).split("\n") if l.strip()]
    for label, key in (("Artist", "artist"), ("Title Track", "titleTrack")):
        if label in plain:
            v = plain[plain.index(label) + 1]
            if "To Be Announced" not in v:
                out[key] = v.replace("“", '"').replace("”", '"').strip('"')
    if "Album" in plain:
        v = plain[plain.index("Album") + 1]
        if " – " in v:
            rtype, title = v.split(" – ", 1)
            out["type"], out["title"] = rtype.strip(), title.strip()
    if "Release Date" in plain:
        when = parse_when(plain[plain.index("Release Date") + 1])
        if when:
            out["date"] = when.isoformat()
    if "Tracklist" in plain:
        i = plain.index("Tracklist") + 1
        while i < len(plain) and plain[i] not in ("Buy Album", "Official Source", "Comeback Schedule"):
            line = plain[i].replace("“", '"').replace("”", '"')
            if "To Be Announced" not in line and len(line) < 120:
                out["tracklist"].append(re.sub(r"^\d+[.)]\s*", "", line))
            i += 1
    photos = re.findall(r'data-orig-file="(https://kpopofficial\.com/wp-content/uploads/[^"]+)"', src)
    seen = []
    for p in photos:
        if p not in seen and "LOGO" not in p and "logo" not in p:
            seen.append(p)
    out["photos"] = seen[:8]
    zone = src[src.find("Official Source"): src.find("Official Source") + 4000] if "Official Source" in src else ""
    for u in re.findall(r'href="(https://(?:x\.com|twitter\.com|www\.instagram\.com|www\.youtube\.com|www\.tiktok\.com)/[^"]+)"', zone):
        if u not in out["links"]:
            out["links"].append(u)
    return out


def main():
    src = fetch(BASE)
    entries = parse_year_page(src)
    now = datetime.now(KST)
    keep_from = now - timedelta(days=14)
    kept, seen = [], set()
    for e in entries:
        if not e["date"]:
            continue
        when = datetime.fromisoformat(e["date"])
        if when < keep_from:
            continue
        key = (e["artist"].lower(), e["date"], (e["title"] or "").lower())
        if key in seen:
            continue
        seen.add(key)
        kept.append(e)
    kept.sort(key=lambda e: e["date"])

    detail_from = keep_from
    fetched = 0
    for e in kept:
        if fetched >= 60:
            break
        if datetime.fromisoformat(e["date"]) < detail_from:
            continue
        try:
            detail = parse_album_page(fetch(e["url"]))
            # la date de la fiche ne sert qu'à préciser l'heure du même jour
            d = detail.pop("date", None)
            if d and d[:10] == e["date"][:10]:
                e["date"] = d
            e.update(detail)
            fetched += 1
            time.sleep(0.4)
        except Exception as ex:
            print(f"  ! fiche {e['url']}: {ex}", file=sys.stderr)
    kept.sort(key=lambda e: e["date"])

    data = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": BASE,
        "entries": kept,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    print(f"{len(kept)} sorties gardées, {fetched} fiches album lues -> {OUT.name}")


if __name__ == "__main__":
    main()
