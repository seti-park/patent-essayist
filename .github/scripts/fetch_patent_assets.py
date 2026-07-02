#!/usr/bin/env python3
"""Runner-side patent asset fetcher, round 3.

Strategies (any success is enough; all outputs land in CWD):
  1. WIPO Patentscope: PCT twin's document PDFs (drawings + published app).
  2. Espacenet classic mosaics: per-sheet drawing images for the US grant.
  3. Wayback Machine: save-page-now + snapshot fetch for patentimages PNGs.
"""
import os
import re
import sys
import time

import requests

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
PATENT_NUM = os.environ.get("PATENT_NUM", "12361091")
PUB_ID = os.environ.get("PUB_ID", "US12361091B1")
GRANT_DATE = os.environ.get("GRANT_DATE", "20250715")
PCT_PUB = os.environ.get("PCT_PUB", "WO2026090209")

ok = []


def log(*a):
    print(*a, flush=True)


def save(name, content, min_bytes=2000):
    if content and len(content) >= min_bytes:
        with open(name, "wb") as f:
            f.write(content)
        ok.append(name)
        log(f"  SAVED {name} ({len(content)}b)")
        return True
    return False


# --------------------------------------------------------------- strategy 1
def patentscope():
    log("== strategy 1: WIPO Patentscope (PCT twin)")
    s = requests.Session()
    s.headers.update({"User-Agent": UA})
    base = "https://patentscope.wipo.int"
    r = s.get(f"{base}/search/en/detail.jsf",
              params={"docId": PCT_PUB, "tab": "PCTDocuments"}, timeout=60)
    log(f"  detail page: {r.status_code} {len(r.content)}b final={r.url[:100]}")
    if r.status_code != 200:
        return
    html = r.text
    # collect candidate document links (docs2 service or direct pdf)
    links = re.findall(r'href="([^"]*(?:docs2|\.pdf)[^"]*)"', html)
    log(f"  candidate links: {len(links)}")
    seen = set()
    for i, href in enumerate(links[:25]):
        url = href if href.startswith("http") else base + href
        url = url.replace("&amp;", "&")
        if url in seen:
            continue
        seen.add(url)
        try:
            rr = s.get(url, timeout=120)
            ct = rr.headers.get("content-type", "")
            log(f"  [{i}] {rr.status_code} {ct[:40]} {len(rr.content)}b {url[:110]}")
            if "pdf" in ct.lower() and len(rr.content) > 50000:
                save(f"patentscope-{i:02d}.pdf", rr.content)
        except Exception as e:
            log(f"  [{i}] ERR {str(e)[:80]}")
    # also dump a slice of hrefs for diagnosis if nothing was saved
    if not any(n.startswith("patentscope") for n in ok):
        hrefs = re.findall(r'href="([^"]{10,140})"', html)
        for h in hrefs:
            if any(k in h.lower() for k in ("doc", "pdf", "download")):
                log("  href:", h[:140])


# --------------------------------------------------------------- strategy 2
def espacenet():
    log("== strategy 2: Espacenet classic mosaics")
    s = requests.Session()
    s.headers.update({"User-Agent": UA})
    base = "https://worldwide.espacenet.com"
    url = (f"{base}/publicationDetails/mosaics?CC=US&NR={PATENT_NUM}B1&KC=B1"
           f"&FT=D&ND=3&DB=worldwide.espacenet.com&locale=en_EP")
    r = s.get(url, timeout=60)
    log(f"  mosaics page: {r.status_code} {len(r.content)}b")
    if r.status_code != 200:
        return
    imgs = re.findall(r'src="([^"]*espacenetImage[^"]*)"', r.text)
    # mosaic pagination: look for total pages
    m = re.search(r'PGS=(\d+)', r.text)
    total = int(m.group(1)) if m else len(imgs)
    log(f"  mosaic imgs on page: {len(imgs)}, PGS total: {total}")
    if not imgs and total == 0:
        log("  page head:", re.sub(r"\s+", " ", r.text[:400]))
        return
    # fetch each mosaic page 1..total via the image endpoint pattern
    tpl = None
    if imgs:
        tpl = imgs[0]
    else:
        tpl = (f"/espacenetImage.jpg?flavour=mosaic&locale=en_EP&FT=D&CC=US"
               f"&NR={PATENT_NUM}B1&KC=B1&PGS={total}&PG=1")
    for pg in range(1, max(total, len(imgs)) + 1):
        u = re.sub(r"PG=\d+", f"PG={pg}", tpl)
        u = u if u.startswith("http") else base + u
        u = u.replace("&amp;", "&")
        try:
            rr = s.get(u, timeout=60)
            ct = rr.headers.get("content-type", "")
            if rr.status_code == 200 and "image" in ct:
                save(f"espacenet-mosaic-{pg:02d}.jpg", rr.content, min_bytes=5000)
            else:
                log(f"  pg{pg}: {rr.status_code} {ct[:30]} {len(rr.content)}b")
        except Exception as e:
            log(f"  pg{pg}: ERR {str(e)[:80]}")


# --------------------------------------------------------------- strategy 3
def wayback():
    log("== strategy 3: Wayback Machine for patentimages PNGs")
    s = requests.Session()
    s.headers.update({"User-Agent": UA})
    misses = 0
    for n in range(0, 60):
        if misses >= 3:
            break
        f = f"US{PATENT_NUM}-{GRANT_DATE}-D{n:05d}.png"
        src = f"https://patentimages.storage.googleapis.com/{PUB_ID}/{f}"
        got = False
        for attempt in ("snapshot", "save"):
            try:
                if attempt == "snapshot":
                    u = f"https://web.archive.org/web/2026id_/{src}"
                else:
                    sv = s.get(f"https://web.archive.org/save/{src}",
                               timeout=180, allow_redirects=True)
                    log(f"  save {f}: {sv.status_code}")
                    u = f"https://web.archive.org/web/2026id_/{src}"
                rr = s.get(u, timeout=120)
                if rr.status_code == 200 and rr.content[:4] == b"\x89PNG":
                    save(f, rr.content)
                    got = True
                    break
                log(f"  {attempt} {f}: {rr.status_code} {rr.headers.get('content-type','')[:30]}")
            except Exception as e:
                log(f"  {attempt} {f}: ERR {str(e)[:80]}")
            time.sleep(2)
        misses = 0 if got else misses + 1


for strat in (patentscope, espacenet, wayback):
    try:
        strat()
    except Exception as e:
        log(f"strategy crashed: {e!r}")
    # stop early once we have a real haul
    pdfs = [n for n in ok if n.endswith(".pdf")]
    pngs = [n for n in ok if n.endswith((".png", ".jpg"))]
    if pdfs or len(pngs) >= 10:
        log("haul sufficient, stopping")
        break

log(f"TOTAL SAVED: {len(ok)} -> {ok}")
sys.exit(0 if ok else 1)
