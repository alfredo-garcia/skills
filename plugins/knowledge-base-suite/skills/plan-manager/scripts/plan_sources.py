#!/usr/bin/env python3
"""Weekly plan search: extract everything from the user's sources, filter only by the user's
own preferences, and write every surviving event as a plan. Claude is needed only for page
texts (free-text programmes), browser sources and the `judge` rules of filters.yaml.

    python3 scripts/plan_sources.py fetch  <kb-root> [--today YYYY-MM-DD] [--only id1,id2]
    python3 scripts/plan_sources.py add    <kb-root> --file extracted.json   # events read from texts/browser
    python3 scripts/plan_sources.py judge  <kb-root> --exclude fp1:rule-id,fp2:rule-id
    python3 scripts/plan_sources.py create <kb-root>      # one plan per remaining candidate
    python3 scripts/plan_sources.py seen   <kb-root>      # remember page texts already read
    python3 scripts/plan_sources.py match  <kb-root> --title "…" [--date YYYY-MM-DD] [--city id] [--url …]

Reads: _profile.yaml, plans/_system/{cities,categories,tags}.yaml, plans/trips/trips.yaml,
    plans/sources/items.yaml (each source's `method`, `fetcher`, `params`),
    plans/ideas/filters.yaml (the user's filters and search windows), plans/ideas/items/*.md (dedup).
Writes: plans/sources/_last_run.json and _seen.json (system files); `create` writes
    plans/ideas/items/<id>.md and plans/ideas/index.json entries (status proposed, report_status pending).

Source methods (field `method` in sources/items.yaml):
    api | script  → fetched here by `fetcher` (see FETCHERS), output = structured candidates
    text          → fetched here, output = cleaned page text; the skill extracts its events → `add`
    browser       → not fetched; listed in `browser` for the skill (built-in browser) → `add`
    search        → not fetched; listed in `search` with its queries → `add`
    dead          → skipped
Every candidate is: `known` (already a plan, any status), `filtered` (with the filter's reason),
or a new candidate. Nothing is hidden for being "seen" before: filters decide every week, so
loosening a filter brings its events back. Only the standard library and PyYAML are used.
"""
import argparse
import gzip
import hashlib
import html
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import zlib
from datetime import date, datetime, timedelta

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit(json.dumps({"error": "PyYAML is required: pip install pyyaml"}))

# Honest client name. A site that blocks this script (403) goes to `method: browser`; never disguise it.
UA = "plan-manager/1.0 (personal weekly events reader; Python-urllib)"
TIMEOUT = 25
TEXT_CAP = 15000          # max chars of page text handed to the skill per page

MONTHS = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7,
          "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10, "noviembre": 11,
          "diciembre": 12}
MON3 = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7, "ago": 8,
        "sep": 9, "oct": 10, "nov": 11, "dic": 12}
MONTH_NAME = {v: k for k, v in MONTHS.items() if k != "setiembre"}

STOP = set("""de del la las el los en y e con a al the and of en vivo live tour gira concierto
concert presenta presentan noche show edicion version temporada festival fest feria evento
evento por para un una su sus lo segunda tercera fecha nueva funcion""".split())


# ---------------------------------------------------------------- utilities

def http_get(url, headers=None, data=None, as_json=False):
    h = {"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
         "Accept-Language": "es-ES,es;q=0.9,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
    if headers:
        h.update(headers)
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        h["Content-Type"] = "application/json; charset=utf-8"
    req = urllib.request.Request(url, data=body, headers=h)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        raw = r.read()
        enc = r.headers.get("Content-Encoding", "")
    if enc == "gzip":
        raw = gzip.decompress(raw)
    elif enc == "deflate":
        raw = zlib.decompress(raw)
    text = raw.decode("utf-8", "replace")
    return json.loads(text) if as_json else text


def html_to_text(s):
    s = re.sub(r"(?is)<(script|style|noscript|svg|header|footer|nav|form)\b.*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h[1-6]|tr|section|article)>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def norm(s):
    s = strip_accents(str(s or "")).lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def to_date(v):
    if v in (None, ""):
        return None
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", str(v))
    return date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def infer_year(month, day, today):
    """Day/month without year → the next occurrence (allowing 7 days in the past)."""
    for y in (today.year, today.year + 1):
        try:
            d = date(y, month, day)
        except ValueError:
            return None
        if d >= today - timedelta(days=7):
            return d
    return None


def clean_url(u):
    if not u:
        return ""
    p = urllib.parse.urlsplit(u.strip())
    path = p.path.rstrip("/")
    return f"{p.netloc.lower().removeprefix('www.')}{path}".lower()


def cand(**kw):
    c = {"title": "", "start": None, "end": None, "time": None, "venue": "", "city": None,
         "city_text": "", "price_amount": None, "price_currency": None, "url": "", "image": "",
         "category": None, "category_hint": "", "description": "", "tickets_url": "", "rating": ""}
    c.update({k: v for k, v in kw.items() if v not in (None, "")})
    if c.get("description"):
        c["description"] = re.sub(r"\s+", " ", c["description"]).strip()[:400]
    return c


# ---------------------------------------------------------------- knowledge base

def load_yaml(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or default


def front_matter(path):
    with open(path, encoding="utf-8") as f:
        s = f.read()
    m = re.match(r"---\s*\n(.*?)\n---", s, re.S)
    return yaml.safe_load(m.group(1)) if m else {}


class KB:
    def __init__(self, root):
        self.root = root
        p = lambda *a: os.path.join(root, "plans", *a)
        self.profile = load_yaml(os.path.join(root, "_profile.yaml"), {})
        self.cities = load_yaml(p("_system", "cities.yaml"), {})
        self.trips = (load_yaml(p("trips", "trips.yaml"), {}) or {}).get("trips") or []
        self.sources = load_yaml(p("sources", "items.yaml"), {})
        self.filters = load_yaml(p("ideas", "filters.yaml"), {}) or {}
        self.categories = load_yaml(p("_system", "categories.yaml"), {})
        self.tags = load_yaml(p("_system", "tags.yaml"), {})
        self.index_path = p("ideas", "index.json")
        self.items_dir = p("ideas", "items")
        self.seen_path = p("sources", "_seen.json")
        self.run_path = p("sources", "_last_run.json")
        self.seen = {"candidates": {}, "pages": {}}
        if os.path.exists(self.seen_path):
            with open(self.seen_path, encoding="utf-8") as f:
                self.seen.update(json.load(f))
        self.items = []
        d = p("ideas", "items")
        if os.path.isdir(d):
            for fn in sorted(os.listdir(d)):
                if fn.endswith(".md"):
                    try:
                        self.items.append(front_matter(os.path.join(d, fn)))
                    except Exception as e:  # a broken file must not hide the rest
                        self.items.append({"id": fn[:-3], "_error": str(e)})
        # URLs that are listings (a source's own URL, or shared by 2+ plans) never prove identity
        self.listing_urls = {clean_url(s.get("url")) for s in self.sources.values() if isinstance(s, dict)}
        counts = {}
        for it in self.items:
            u = clean_url((it.get("source") or {}).get("url"))
            counts[u] = counts.get(u, 0) + 1
        self.listing_urls |= {u for u, n in counts.items() if n > 1}
        self.listing_urls.discard("")
        self.city_by_label = {}
        for cid, c in self.cities.items():
            self.city_by_label[norm(cid)] = cid
            self.city_by_label[norm((c or {}).get("label", ""))] = cid

    def city_id(self, text):
        t = norm(text)
        if not t:
            return None
        if t in self.city_by_label:
            return self.city_by_label[t]
        for label, cid in self.city_by_label.items():
            if label and re.search(rf"\b{re.escape(label)}\b", t):
                return cid
        return None


# ---------------------------------------------------------------- dedup

def title_tokens(title, kb):
    city_words = set()
    for cid, c in kb.cities.items():
        city_words |= set(norm(cid).split()) | set(norm((c or {}).get("label", "")).split())
    toks = [t for t in norm(title).split() if t not in STOP and t not in city_words
            and not re.fullmatch(r"(19|20)\d\d", t) and len(t) > 1]
    return set(toks)


def item_dates(it):
    ds = [to_date(s.get("start")) for s in it.get("sessions") or [] if isinstance(s, dict)]
    ds = [d for d in ds if d]
    lo, hi = to_date(it.get("available_from")), to_date(it.get("available_until"))
    sched = to_date((it.get("scheduled") or {}).get("start")) if isinstance(it.get("scheduled"), dict) else None
    return ds, lo, hi, sched


def same_title(a, b):
    if not a or not b:
        return False
    inter = len(a & b)
    small = min(len(a), len(b))
    if small >= 2 and inter == small:          # one title contains the other
        return True
    if small == 1 and inter == 1 and len(next(iter(a & b))) >= 5 and max(len(a), len(b)) <= 3:
        return True
    return inter / len(a | b) >= 0.6


def dates_compatible(c_start, c_end, it, tol=3):
    """True when the candidate's date fits the plan, or when either side has no date."""
    if it.get("timing") == "timeless":
        return True
    ds, lo, hi, sched = item_dates(it)
    if not c_start or not (ds or lo or hi or sched):
        return True
    c_end = c_end or c_start
    for d in ds + ([sched] if sched else []):
        if c_start - timedelta(days=tol) <= d <= c_end + timedelta(days=tol):
            return True
    if lo or hi:
        lo = lo or date.min
        hi = hi or date.max
        return c_start <= hi and c_end >= lo
    return False


def find_match(kb, title, start=None, end=None, city=None, url=None):
    """Return (plan id, reason) of an existing plan that is this candidate, else (None, None)."""
    cu = clean_url(url)
    toks = title_tokens(title, kb)
    for it in kb.items:
        if it.get("_error"):
            continue
        iu = clean_url((it.get("source") or {}).get("url"))
        links = {clean_url(l.get("url")) for l in it.get("links") or [] if isinstance(l, dict)}
        links |= {clean_url((it.get("tickets") or {}).get("url"))}
        links.add(iu)
        links -= kb.listing_urls | {""}
        if cu and cu not in kb.listing_urls and cu in links:
            return it.get("id"), "url"
        if city and it.get("city") and it.get("city") != city:
            continue
        if same_title(toks, title_tokens(it.get("title", ""), kb)) and dates_compatible(start, end, it):
            return it.get("id"), "title+date"
        series = it.get("series")
        if series and start and same_title(toks, title_tokens(series.replace("-", " "), kb)):
            ds, lo, hi, _ = item_dates(it)
            years = {d.year for d in ds} | {d.year for d in (lo, hi) if d}
            if start.year in years:
                return it.get("id"), "series"
    return None, None


def fingerprint(c):
    toks = " ".join(sorted(c.get("_tokens") or []))
    return hashlib.sha1(f"{toks}|{c.get('start') or ''}|{c.get('city') or ''}".encode()).hexdigest()[:16]


# ---------------------------------------------------------------- windows

def windows(kb, today):
    """city id → list of (start, end, scope). Trip cities only around trips; home city paused during trips.
    Lengths come from plans/ideas/filters.yaml → windows (defaults 21 / 120 / 35 days)."""
    wd = {"everyday_days": 21, "big_only_days": 120, "trip_lead_days": 35}
    wd.update((kb.filters.get("windows") or {}))
    out = {}
    trips = [(t.get("city"), to_date(t.get("from")), to_date(t.get("to"))) for t in kb.trips]
    on_trip = [t for t in trips if t[1] and t[2] and t[1] <= today <= t[2]]
    for cid, c in kb.cities.items():
        scope = (c or {}).get("scope", "everyday")
        if scope == "everyday":
            s = max([today] + [t[2] + timedelta(days=1) for t in on_trip])
            out[cid] = [(s, s + timedelta(days=int(wd['everyday_days'])), scope)]
        elif scope == "big-only":
            out[cid] = [(today, today + timedelta(days=int(wd['big_only_days'])), scope)]
        elif scope == "trip-only":
            w = [(max(f, today), t, scope) for (tc, f, t) in trips
                 if tc == cid and f and t and t >= today and f <= today + timedelta(days=int(wd['trip_lead_days']))]
            if w:
                out[cid] = w
    return out


def months_in(ws):
    ms = set()
    for s, e, _ in ws:
        d = date(s.year, s.month, 1)
        while d <= e:
            ms.add((d.year, d.month))
            d = date(d.year + (d.month == 12), d.month % 12 + 1, 1)
    return sorted(ms)


# ---------------------------------------------------------------- fetchers
# Each fetcher(source, params, ctx) returns {"candidates": [...], "texts": [...], "notes": [...]}.
# ctx: kb, today, windows (only for this source's cities), city_ids of the source.

TUBOLETA_CATS = {26838: "concert", 26988: "theater", 27234: "festival", 28412: "sport-event",
                  27801: "exhibition", 27220: "other", 27236: "other", 27425: "talk", 28094: "other"}


def f_tuboleta(src, prm, ctx):
    """Search per city and per category (all of them; products such as gift cards are left out)."""
    base = prm.get("base", "https://tuboleta.com")
    cats = {int(k): v for k, v in (prm.get("category_map") or TUBOLETA_CATS).items()}
    out = []
    for cid in ctx["cities"]:
        tb_city = (prm.get("city_ids") or {}).get(cid)
        if not tb_city:
            continue
        for cat, our_cat in cats.items():
            for page in range(int(prm.get("max_pages", 8))):
                q = {"ciudades": tb_city, "categorias": cat}
                if page:
                    q["page"] = page
                s = http_get(f"{base}/es/resultados-de-busqueda?{urllib.parse.urlencode(q)}")
                arts = [a for a in re.findall(r"(?s)<article.*?</article>", s) if "/es/eventos/" in a]
                new = 0
                for a in arts:
                    href = re.search(r'href="(/es/eventos/[^"]+)"', a).group(1)
                    if any(c["url"].endswith(href) for c in out):
                        continue
                    new += 1
                    info = re.search(r'(?s)class="content-info.*?</div>\s*</div>', a)
                    spans = [html.unescape(re.sub(r"\s+", " ", x)).strip()
                             for x in re.findall(r"<span>(.*?)</span>", info.group(0) if info else a, re.S)]
                    dc = re.search(r'(?s)class="dates-container.*?</div>\s*</div>', a)
                    days = re.findall(r'd-md-none">\s*(\d{1,2})\s+([A-Za-zé]{3})', dc.group(0)) if dc else []
                    ds = [infer_year(MON3[norm(m)[:3]], int(d), ctx["today"]) for d, m in days if norm(m)[:3] in MON3]
                    ds = [d for d in ds if d]
                    if not ds:
                        continue            # undated cards are landings (club pages, parking, gift cards)
                    out.append(cand(title=spans[0] if spans else href, venue=spans[1] if len(spans) > 2 else "",
                                    city_text=spans[-1] if spans else "", start=ds[0],
                                    end=ds[-1] if len(ds) > 1 else None, url=base + href, tickets_url=base + href,
                                    category=our_cat))
                if not new:
                    break
    return {"candidates": out}


def enrich_tuboleta(c):
    """Detail page: og:description has the full date, time, line-up and price ("Desde $187.000")."""
    s = http_get(c["url"])
    m = re.search(r'og:description" content="([^"]*)"', s)
    if m:
        c["description"] = html.unescape(m.group(1))
        p = re.search(r"[Dd]esde \$\s?([\d.]+)", c["description"])
        if p:
            c["price_amount"], c["price_currency"] = int(p.group(1).replace(".", "")), "COP"
        t = re.search(r"(\d{1,2}):(\d{2})\s*([ap])\.?\s?m", c["description"])
        if t and not c.get("time"):
            h = int(t.group(1)) % 12 + (12 if t.group(3) == "p" else 0)
            c["time"] = f"{h:02d}:{t.group(2)}"
    m = re.search(r'og:image" content="([^"]*)"', s)
    if m and not c.get("image"):
        c["image"] = m.group(1)


def f_plan52(src, prm, ctx):
    ep = prm.get("endpoint", "https://plan52manizales.com/wp-json/plan52/v1/eventos")
    lo = min(w[0] for ws in ctx["windows"].values() for w in ws)
    hi = max(w[1] for ws in ctx["windows"].values() for w in ws)
    out, page = [], 1
    while page <= 10:
        d = http_get(f"{ep}?{urllib.parse.urlencode({'desde': lo, 'hasta': hi, 'per_page': 50, 'page': page})}",
                     as_json=True)
        for e in d.get("events", []):
            out.append(cand(title=html.unescape(e.get("title", "")), start=to_date(e.get("fecha_inicio")),
                            end=to_date(e.get("fecha_final")), time=e.get("hora"), venue=e.get("lugar", ""),
                            city_text=e.get("ciudad", ""), url=e.get("link", ""), image=e.get("imagen", ""),
                            category=(prm.get("category_map") or {}).get(e.get("categoria", "")),
                            category_hint=e.get("categoria", ""), description=e.get("descripcion", ""),
                            tickets_url=e.get("link_whatsapp", "") if "http" in str(e.get("link_whatsapp")) else ""))
        if page >= int(d.get("paginas") or 1):
            break
        page += 1
    return {"candidates": out}


def f_wp_rest(src, prm, ctx):
    """Generic WordPress post type: only entries modified in the last `days` days. Dates are
    often in taxonomies or the body, so each one comes back as text for the skill."""
    base = prm["endpoint"]
    since = (ctx["today"] - timedelta(days=int(prm.get("days", 14)))).isoformat() + "T00:00:00"
    items = http_get(f"{base}?{urllib.parse.urlencode({'per_page': 50, 'modified_after': since})}", as_json=True)
    terms = {}
    for tax, ep in (prm.get("taxonomies") or {}).items():
        for t in http_get(f"{ep}?per_page=100&_fields=id,name", as_json=True):
            terms[(tax, t["id"])] = t["name"]
    texts = []
    for e in items:
        extra = {tax: [terms.get((tax, i), i) for i in e.get(tax) or []] for tax in (prm.get("taxonomies") or {})}
        body = html_to_text((e.get("content") or {}).get("rendered", ""))[:1500]
        texts.append({"url": e.get("link"), "title": html.unescape(e["title"]["rendered"]),
                      "modified": e.get("modified"), "terms": extra,
                      "text": f"{json.dumps(extra, ensure_ascii=False)}\n{body}"})
    return {"texts": unseen_texts(texts, ctx)}


def page_text(url):
    s = http_get(url)
    m = re.search(r"(?is)<(article|main)\b.*?</\1>", s)
    t = html_to_text(m.group(0) if m else s)
    t = re.sub(r"(?m)^(Leer más|Compartir.*|Otras publicaciones)$", "", t)
    return re.sub(r"\n+", "\n", t).strip()


def f_wp_sitemap(src, prm, ctx):
    """Sitemap with <lastmod>: only pages under `prefix` changed in the last `days` days."""
    since = ctx["today"] - timedelta(days=int(prm.get("days", 8)))
    sm = http_get(prm["sitemap"])
    urls = re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", sm)
    pref = prm.get("prefix", "")
    texts = []
    for u, lm in sorted(urls, key=lambda x: x[1], reverse=True):
        if (pref and pref not in u) or u.rstrip("/").endswith(pref.rstrip("/")):
            continue
        if to_date(lm) and to_date(lm) < since:
            break
        texts.append({"url": u.replace("http://", "https://"), "modified": lm})
        if len(texts) >= int(prm.get("max", 25)):
            break
    return {"texts": unseen_texts(texts, ctx, lambda t: page_text(t["url"])[:3000])}


def unseen_texts(texts, ctx, load=None):
    """Fill each text (if `load`), hash it, and drop the ones already reviewed unchanged."""
    out = []
    for t in texts:
        try:
            if load:
                t["text"] = load(t)
        except Exception as e:
            t["error"] = str(e)
            out.append(t)
            continue
        t["hash"] = hashlib.sha1(t.get("text", "").encode()).hexdigest()[:16]
        if ctx["kb"].seen["pages"].get(t["url"], {}).get("hash") != t["hash"]:
            out.append(t)
    return out


def f_cinepolis(src, prm, ctx):
    base = prm.get("base", "https://cinepolis.com.co")
    d = http_get(f"{base}/Cartelera.aspx/GetNowPlayingByCity",
                 data={"claveCiudad": prm["city_key"], "esVIP": False}, as_json=True)["d"]
    first = {}
    for c in d.get("Cinemas", []):
        if prm.get("cinema_key") and c.get("Key") != prm["cinema_key"]:
            continue
        for dt in c.get("Dates", []):
            m = re.match(r"(\d{1,2}) (\w+)", dt.get("ShowtimeDate", ""))
            day = infer_year(MONTHS.get(norm(m.group(2)), 1), int(m.group(1)), ctx["today"]) if m else None
            for mv in dt.get("Movies", []):
                k = mv.get("Key") or mv.get("Title")
                if k not in first:
                    first[k] = (day, mv)
    out = []
    for k, (day, mv) in first.items():
        out.append(cand(title=mv.get("Title"), start=day, venue=prm.get("venue", ""), city=ctx["cities"][0],
                        url=f"{base}/pelicula/{mv.get('Key')}", image=mv.get("Poster"), category="cinema",
                        rating=mv.get("Rating"),
                        description=f"{mv.get('RunTime', '')} · {mv.get('Rating', '')} · {mv.get('Director', '')}"))
    # coming soon: static page, <li><a href='pelicula/<key>'>…<figcaption>Title</figcaption>…<span>26</span> de noviembre
    try:
        s = http_get(f"{base}/proximos-estrenos")
        have = {norm(c["title"]) for c in out}
        for m in re.finditer(r"(?s)href='pelicula/([^']+)'.*?src='([^']*)'.*?<figcaption>(.*?)</figcaption>"
                             r".*?diaEstreno'><span>(\d{1,2})</span>\s*de\s*(\w+)", s):
            title = html.unescape(m.group(3)).strip()
            if norm(title) in have:
                continue
            out.append(cand(title=title, start=infer_year(MONTHS.get(norm(m.group(5)), 1), int(m.group(4)),
                                                          ctx["today"]),
                            venue=prm.get("venue", ""), city=ctx["cities"][0], url=f"{base}/pelicula/{m.group(1)}",
                            image=m.group(2), category="cinema", category_hint="estreno"))
    except Exception as e:
        return {"candidates": out, "notes": [f"proximos-estrenos: {e}"]}
    return {"candidates": out}


def enrich_cinepolis(c):
    """Film page: synopsis (Cinépolis publishes no genre; the synopsis lets the judge rules decide)."""
    m = re.search(r'(?s)id="[^"]*ctl_sinopsis"[^>]*>(.*?)</p>', http_get(c["url"]))
    if m:
        syn = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))).strip()
        c["description"] = (syn[:450] + (" · " + c["description"] if c.get("description") else "")).strip()


def f_respira(src, prm, ctx):
    d = http_get(prm.get("endpoint", "https://api.respira.run/api/v1/eventos-publicos/"), as_json=True)
    d = d.get("results", d) if isinstance(d, dict) else d
    out = []
    for e in d:
        out.append(cand(title=e.get("name"), start=to_date(e.get("start_date")), end=to_date(e.get("end_date")),
                        time=(e.get("start_date") or "")[11:16] or None, city_text=e.get("city", ""),
                        venue=f"{e.get('city', '')}, {e.get('state', '')}",
                        url=f"https://respira.run/eventos/{e.get('slug')}", image=e.get("banner") or e.get("logo"),
                        category="running-race",
                        description=", ".join(str(c.get("name", c)) for c in e.get("categories") or []
                                              if isinstance(c, (dict, str)))))
    return {"candidates": out}


def f_espn_soccer(src, prm, ctx):
    url = (f"https://site.api.espn.com/apis/site/v2/sports/soccer/{prm['league']}/teams/"
           f"{prm['team_id']}/schedule?fixture=true")
    d = http_get(url, as_json=True)
    out = []
    for e in d.get("events", []):
        comp = e["competitions"][0]
        home = [x for x in comp["competitors"] if x.get("homeAway") == "home"]
        if prm.get("home_only", True) and not (home and str(home[0]["team"].get("id")) == str(prm["team_id"])):
            continue
        utc = datetime.strptime(e["date"].replace("Z", ""), "%Y-%m-%dT%H:%M")
        local = utc + timedelta(hours=int(prm.get("utc_offset", -5)))
        out.append(cand(title=e.get("name", ""), start=local.date(), time=local.strftime("%H:%M"),
                        venue=comp.get("venue", {}).get("fullName", ""), city=ctx["cities"][0],
                        url=f"https://www.espn.com.co/futbol/partido/_/juegoId/{e.get('id')}",
                        category="sport-event", description=comp.get("status", {}).get("type", {}).get("detail", "")))
    return {"candidates": out}


def jsonld_events(s):
    out = []
    for b in re.findall(r'(?is)<script[^>]*application/ld\+json[^>]*>(.*?)</script>', s):
        try:
            d = json.loads(b)
        except Exception:
            continue
        stack = d if isinstance(d, list) else [d]
        while stack:
            x = stack.pop()
            if isinstance(x, dict):
                if "@graph" in x:
                    stack.extend(x["@graph"])
                if "Event" in str(x.get("@type", "")):
                    out.append(x)
    return out


def f_jsonld(src, prm, ctx):
    """schema.org Event blocks. `urls` may use {yyyy} and {mes}/{mm} (expanded over the window);
    `page_pattern` (e.g. "{url}/pagina-{n}") pages until events pass the window end."""
    ws = [w for v in ctx["windows"].values() for w in v]
    hi = max(w[1] for w in ws)
    urls = []
    for tpl in prm["urls"]:
        for y, m in months_in(ws):
            u = tpl.format(yyyy=y, mm=f"{m:02d}", mes=MONTH_NAME[m])
            if u not in urls:
                urls.append(u)
    out, seen = [], set()
    for u in urls:
        for n in range(1, int(prm.get("max_pages", 8)) + 1):
            page = u if n == 1 else prm.get("page_pattern", "{url}?page={n}").format(url=u, n=n)
            try:
                evs = jsonld_events(http_get(page))
            except urllib.error.HTTPError:
                break
            if not evs:
                break
            last = None
            for e in evs:
                key = e.get("@id") or e.get("url")
                if key in seen:
                    continue
                seen.add(key)
                loc = e.get("location") or {}
                loc = loc[0] if isinstance(loc, list) and loc else loc
                addr = loc.get("address") or {} if isinstance(loc, dict) else {}
                off = e.get("offers") or {}
                off = off[0] if isinstance(off, list) and off else off
                st = to_date(e.get("startDate"))
                last = st or last
                out.append(cand(title=html.unescape(e.get("name", "")), start=st, end=to_date(e.get("endDate")),
                                time=(str(e.get("startDate"))[11:16] or None),
                                venue=loc.get("name", "") if isinstance(loc, dict) else "",
                                city_text=addr.get("addressLocality", "") if isinstance(addr, dict) else "",
                                price_amount=off.get("price") if isinstance(off, dict) else None,
                                price_currency=off.get("priceCurrency") if isinstance(off, dict) else None,
                                url=e.get("url", ""), image=e.get("image") if isinstance(e.get("image"), str) else "",
                                description=e.get("description", ""), category_hint=str(e.get("@type")),
                                category=prm.get("category") or ("concert" if "Music" in str(e.get("@type")) else None)))
            if last and last > hi:
                break
    return {"candidates": out}


def f_text(src, prm, ctx):
    """Page text for the skill. `urls` may use {yyyy}/{mes}/{mm}; `hub` + `link_regex` (with {mes})
    discovers a monthly article. Unchanged pages since the last review are skipped."""
    ws = [w for v in ctx["windows"].values() for w in v]
    urls, notes = [], []
    for y, m in months_in(ws):
        for tpl in prm.get("urls", []):
            urls.append(tpl.format(yyyy=y, mm=f"{m:02d}", mes=MONTH_NAME[m]))
        if prm.get("hub"):
            hub = http_get(prm["hub"])
            rx = prm["link_regex"].format(mes=MONTH_NAME[m], yyyy=y)
            found = re.findall(rf'href="([^"]*{rx})"', hub)
            if found:
                urls.append(urllib.parse.urljoin(prm["hub"], found[0]))
            else:
                notes.append(f"{MONTH_NAME[m]} {y}: no article linked from the hub yet; search the web for it")
    texts = []
    for u in dict.fromkeys(urls):
        try:
            t = page_text(u)
        except Exception as e:
            notes.append(f"{u}: {e}")
            continue
        h = hashlib.sha1(t.encode()).hexdigest()[:16]
        if ctx["kb"].seen["pages"].get(u, {}).get("hash") == h:
            notes.append(f"{u}: unchanged since last review")
            continue
        texts.append({"url": u, "hash": h, "text": t[:TEXT_CAP], "truncated": len(t) > TEXT_CAP})
    return {"texts": texts, "notes": notes}


def f_dated_list(src, prm, ctx):
    """An article listing '<d> [y <d>] de <mes>: Name, City; Name, City.' (e.g. a year's concert list)."""
    ws = [w for v in ctx["windows"].values() for w in v]
    out = []
    for y in sorted({y for y, _ in months_in(ws)}):
        url = prm["url"].format(yyyy=y)
        try:
            t = page_text(url)
        except urllib.error.HTTPError:
            continue
        t = re.sub(r":\s*\n\s*", ": ", t)
        for m in re.finditer(r"(?m)^\s*(\d{1,2})(?:\s*(?:y|-|al)\s*(\d{1,2}))? de (\w+):\s*(.+)$", t):
            mon = MONTHS.get(norm(m.group(3)))
            if not mon:
                continue
            for part in m.group(4).rstrip(".").split(";"):
                if "," not in part:
                    continue
                name, city = part.rsplit(",", 1)
                for nm in re.split(r"\s+y\s+(?=[A-ZÁÉÍÓÚ])", name.strip()) if prm.get("split_and") else [name.strip()]:
                    try:
                        st = date(y, mon, int(m.group(1)))
                        en = date(y, mon, int(m.group(2))) if m.group(2) else None
                    except ValueError:
                        continue
                    out.append(cand(title=nm.strip(), start=st, end=en, city_text=city.strip(), url=url,
                                    category=prm.get("category", "concert")))
    return {"candidates": out}


ENRICH = {"tuboleta": enrich_tuboleta, "cinepolis": enrich_cinepolis}

FETCHERS = {"tuboleta": f_tuboleta, "plan52": f_plan52, "wp-rest": f_wp_rest, "wp-sitemap": f_wp_sitemap,
            "cinepolis": f_cinepolis, "respira": f_respira, "espn-soccer": f_espn_soccer, "jsonld": f_jsonld,
            "text": f_text, "dated-list": f_dated_list}




# ---------------------------------------------------------------- preferences (plans/ideas/filters.yaml)
# The script extracts everything; the user's own filters are the only thing that removes a candidate.
#   exclude: exact rules, applied here      { id, when: {...}, reason }
#   judge:   rules that need understanding  { id, when: {...}, rule, reason } → answered by the skill
#   big_only: what counts as a big event in big-only cities { venues: [...], sources: [...] }
# `when` keys (all given keys must hold): category, city, scope, source, title_any, venue_any,
# rating, price_over, weekday (0=Mon…6=Sun).

def rule_applies(c, when):
    when = when or {}
    lst = lambda k: [str(x) for x in (when.get(k) if isinstance(when.get(k), list) else [when.get(k)])]
    for k in ("category", "city", "scope", "source", "rating"):
        if k in when and str(c.get(k)) not in lst(k):
            return False
    if "title_any" in when and not any(norm(w) in norm(c.get("title")) for w in lst("title_any")):
        return False
    if "venue_any" in when and not any(norm(w) in norm(c.get("venue")) for w in lst("venue_any")):
        return False
    if "price_over" in when and not (c.get("price_amount") and float(c["price_amount"]) > float(when["price_over"])):
        return False
    if "weekday" in when:
        d = to_date(c.get("start"))
        if not d or str(d.weekday()) not in lst("weekday"):
            return False
    return True


def exclusion(c, kb):
    """Reason the user's filters exclude this candidate, or None."""
    f = kb.filters
    if c.get("scope") == "big-only":
        big = f.get("big_only") or {}
        if big and c.get("source") not in (big.get("sources") or []) \
                and not any(norm(v) in norm(c.get("venue")) for v in big.get("venues") or []):
            return "big_only: no es un recinto grande"
    for r in f.get("exclude") or []:
        if rule_applies(c, r.get("when")):
            return f"{r.get('id')}: {r.get('reason', '')}".strip()
    return None


def judge_rules(c, kb):
    return [{"id": r.get("id"), "rule": r.get("rule")} for r in kb.filters.get("judge") or []
            if rule_applies(c, r.get("when"))]


# ---------------------------------------------------------------- commands

def in_window(c, ws):
    s = to_date(c.get("start"))
    if not s:
        return True                     # undated: let the skill decide
    e = to_date(c.get("end")) or s
    return any(s <= w[1] and e >= w[0] for w in ws)


def source_windows(kb, src, wins, today):
    cities = [c for c in src.get("cities") or [] if c in wins]
    sw = {c: wins[c] for c in cities}
    if src.get("big_events"):
        days = int((kb.filters.get("windows") or {}).get("big_only_days", 120))
        sw = {c: ([(w[0], max(w[1], today + timedelta(days=days)), w[2]) for w in ws]
                  if ws[0][2] == "everyday" else ws) for c, ws in sw.items()}
    return cities, sw


def process(c, kb, report, cities, swins, wins, src):
    """Place one raw candidate: known plan, out of window, filtered, merged into another, or new."""
    c["city"] = c.get("city") or kb.city_id(c.get("city_text")) or (
        cities[0] if len(cities) == 1 and not c.get("city_text") else None)
    if c["city"] not in cities:
        return
    if not in_window(c, swins[c["city"]]):
        report["out_of_window"] += 1
        return
    if not c.get("category"):
        cats = src.get("categories") or []
        c["category"] = cats[0] if len(cats) == 1 else "other"
    if c["category"] not in kb.categories:
        c["category"] = "other"
    c["start"] = to_date(c["start"]).isoformat() if to_date(c.get("start")) else None
    c["end"] = to_date(c["end"]).isoformat() if to_date(c.get("end")) else None
    c["scope"] = wins[c["city"]][0][2]
    tok = title_tokens(c["title"], kb)
    mid, why = find_match(kb, c["title"], to_date(c["start"]), to_date(c["end"]), c["city"], c.get("url"))
    if mid:
        report["known"].append({"source": c["source"], "title": c["title"], "start": c["start"], "plan": mid, "by": why})
        return
    why_not = exclusion(c, kb)
    if why_not:
        report["filtered"].append({"source": c["source"], "title": c["title"], "start": c["start"],
                                   "city": c["city"], "category": c["category"], "reason": why_not})
        return
    for x in report["candidates"]:
        if x["city"] == c["city"] and same_title(tok, set(x["_tokens"])):
            xs, cs = to_date(x["start"]), to_date(c["start"])
            if xs and cs and abs((xs - cs).days) <= 3 and x["source"] == c["source"]:
                x.setdefault("sessions", [{"start": x["start"], "time": x.get("time")}])
                x["sessions"].append({"start": c["start"], "time": c.get("time")})
                return                   # another date of the same show
            if (not xs or not cs or xs == cs) and x["source"] != c["source"]:
                for k, v in c.items():   # same event from another source: keep the first, fill gaps
                    if v not in (None, "", []) and x.get(k) in (None, "", []):
                        x[k] = v
                x.setdefault("also_sources", []).append({"source": c["source"], "url": c.get("url")})
                return
    c["_tokens"] = sorted(tok)
    c["fp"] = fingerprint(c)
    report["candidates"].append(c)


def finish(report, kb, enrich=True):
    """Enrich new candidates (detail pages), re-check price filters, attach judge rules, save."""
    fetcher_of = {sid: (s or {}).get("fetcher") for sid, s in kb.sources.items() if isinstance(s, dict)}
    keep = []
    for c in report["candidates"]:
        fn = ENRICH.get(fetcher_of.get(c["source"]) or "")
        if enrich and fn and not c.get("_enriched"):
            try:
                fn(c)
            except Exception as e:
                c["enrich_error"] = str(e)
            c["_enriched"] = True
        why_not = exclusion(c, kb)
        if why_not:
            report["filtered"].append({"source": c["source"], "title": c["title"], "start": c["start"],
                                       "city": c["city"], "category": c["category"], "reason": why_not})
            continue
        c["judge"] = judge_rules(c, kb)
        keep.append(c)
    report["candidates"] = keep
    with open(kb.run_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1, default=str)
    return report


def cmd_fetch(kb, today, only):
    wins = windows(kb, today)
    report = {"today": today.isoformat(), "windows": {k: [[str(a), str(b), sc] for a, b, sc in v]
                                                      for k, v in wins.items()},
              "candidates": [], "known": [], "filtered": [], "out_of_window": 0, "texts": [],
              "browser": [], "search": [], "errors": [], "sources": {}, "judged": False, "created": []}
    for sid, src in kb.sources.items():
        if not isinstance(src, dict) or (only and sid not in only):
            continue
        method = src.get("method") or "browser"
        cities, swins = source_windows(kb, src, wins, today)
        if method == "dead":
            continue
        if not cities:
            report["sources"][sid] = "no active window for its cities"
            continue
        if method in ("browser", "search"):
            report[method].append({"source": sid, "name": src.get("name"), "url": src.get("url"),
                                   "cities": cities, "queries": (src.get("params") or {}).get("queries"),
                                   "windows": {c: [[str(a), str(b)] for a, b, _ in w] for c, w in swins.items()},
                                   "note": src.get("note", "")})
            continue
        fn = FETCHERS.get(src.get("fetcher") or "")
        if not fn:
            report["errors"].append({"source": sid, "error": f"unknown fetcher {src.get('fetcher')!r}"})
            continue
        ctx = {"kb": kb, "today": today, "cities": cities, "windows": swins}
        try:
            res = fn(src, src.get("params") or {}, ctx)
        except Exception as e:  # report and go on: the skill falls back to the browser for this source
            report["errors"].append({"source": sid, "error": f"{type(e).__name__}: {e}",
                                     "fallback": "browser", "url": src.get("url")})
            continue
        before = len(report["candidates"])
        for c in res.get("candidates", []):
            c["source"] = sid
            process(c, kb, report, cities, swins, wins, src)
        for t in res.get("texts", []):
            t["source"] = sid
            t["cities"] = cities
            report["texts"].append(t)
        report["sources"][sid] = {"method": method, "new": len(report["candidates"]) - before,
                                  "texts": len(res.get("texts", [])), "notes": res.get("notes", [])}
    return finish(report, kb)


def load_run(kb):
    if not os.path.exists(kb.run_path):
        sys.exit(json.dumps({"error": "no _last_run.json; run fetch first"}))
    with open(kb.run_path, encoding="utf-8") as f:
        return json.load(f)


def cmd_add(kb, today, path):
    """Add candidates the skill read from `texts` or `browser` sources (JSON list of candidate
    objects with at least title, start, source; city or city_text). Same dedup and filters."""
    report = load_run(kb)
    wins = windows(kb, to_date(report["today"]) or today)
    with open(path, encoding="utf-8") as f:
        items = json.load(f)
    before = len(report["candidates"])
    for raw in items:
        src = kb.sources.get(raw.get("source")) or {"cities": list(wins)}
        cities, swins = source_windows(kb, src, wins, today)
        c = cand(**{k: v for k, v in raw.items() if k != "sessions"})
        c["source"] = raw.get("source", "manual")
        if raw.get("sessions"):
            c["sessions"] = raw["sessions"]
        process(c, kb, report, cities, swins, wins, src)
    finish(report, kb, enrich=False)
    return {"added": len(report["candidates"]) - before, "candidates": len(report["candidates"]),
            "filtered": len(report["filtered"]), "known": len(report["known"])}


def cmd_judge(kb, exclude):
    """Record the skill's answers to the judge rules: `exclude` = list of (fp, rule id).
    Every other candidate with judge rules passes."""
    report = load_run(kb)
    rules = {r.get("id"): r for r in kb.filters.get("judge") or []}
    ex = {}
    for fp, rid in exclude:
        ex.setdefault(fp, rid)
    keep = []
    for c in report["candidates"]:
        if c["fp"] in ex:
            r = rules.get(ex[c["fp"]], {})
            report["filtered"].append({"source": c["source"], "title": c["title"], "start": c["start"],
                                       "city": c["city"], "category": c["category"],
                                       "reason": f"{ex[c['fp']]}: {r.get('reason', '')}".strip()})
        else:
            keep.append(c)
    report["candidates"] = keep
    report["judged"] = True
    with open(kb.run_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1, default=str)
    return {"excluded": len(ex), "candidates": len(keep)}


TZ_BY_COUNTRY = {"CO": "America/Bogota", "ES": "Europe/Madrid", "FR": "Europe/Paris", "MX": "America/Mexico_City",
                 "US": "America/New_York", "PT": "Europe/Lisbon"}


def stamp(day, hhmm, tzname):
    from zoneinfo import ZoneInfo
    h, m = (int(x) for x in (hhmm or "00:00").split(":")[:2])
    d = to_date(day)
    return datetime(d.year, d.month, d.day, h, m, tzinfo=ZoneInfo(tzname)).isoformat()


def ystr(v):
    return "''" if v in (None, "") else "'" + str(v).replace("'", "''") + "'"


SMALL = set("de del la las el los y e o u a al en con por para sin vs x".split())


def tidy_title(t, kb=None):
    """Ticketing titles come as 'ARTIST | TOUR - CITY': sentence-style case, en dash, no trailing city."""
    t = re.sub(r"\s+", " ", html.unescape(t or "")).strip()
    if kb:
        for c in kb.cities.values():
            lab = (c or {}).get("label", "")
            if lab:
                t = re.sub(rf"\s*[-–|]\s*{re.escape(lab)}\s*$", "", t, flags=re.I)
                t = re.sub(rf"\s*[-–|]\s*{re.escape(strip_accents(lab))}\s*$", "", t, flags=re.I)
    t = re.sub(r"\s*\|\s*", " – ", t)
    letters = [ch for ch in t if ch.isalpha()]
    if letters and sum(ch.isupper() for ch in letters) / len(letters) > 0.7:
        words = t.lower().split(" ")
        out = []
        for i, w in enumerate(words):
            if re.fullmatch(r"[ivx]+", w) and len(w) <= 4 and w != "x":
                out.append(w.upper())
            elif i and w in SMALL and words[i - 1] not in ("–", "-", ":"):
                out.append(w)
            else:
                out.append(w[:1].upper() + w[1:])
        t = " ".join(out)
    return t.strip(" -–|")


def cmd_create(kb, now):
    """Write one plan per remaining candidate (status proposed, report_status pending) + index entries."""
    report = load_run(kb)
    if any(c.get("judge") for c in report["candidates"]) and not report.get("judged"):
        return {"error": "some candidates need the judge rules first (command judge)",
                "pending": [{"fp": c["fp"], "title": c["title"], "description": c.get("description", "")[:300],
                             "judge": c["judge"]} for c in report["candidates"] if c.get("judge")]}
    with open(kb.index_path, encoding="utf-8") as f:
        index = json.load(f)
    defaults = (kb.filters.get("defaults") or {}).get("audience") or {}
    today, created = now.date().isoformat(), []
    for c in report["candidates"]:
        if c.get("plan"):
            continue
        mid, _ = find_match(kb, c["title"], to_date(c["start"]), to_date(c["end"]), c["city"], c.get("url"))
        if mid:                           # created meanwhile (another source, or by hand)
            c["plan"] = mid
            continue
        city = kb.cities.get(c["city"]) or {}
        tzname = TZ_BY_COUNTRY.get(str(city.get("country", "")).upper()) or str(kb.profile.get("timezone") or "UTC")
        words = [w for w in norm(tidy_title(c["title"], kb)).split() if w not in ("de", "la", "el", "los", "las", "y", "en")][:8]
        base = "-".join(words) or "plan"
        if norm(c["city"]) not in base:
            base += "-" + c["city"]
        pid = base
        if pid in index or os.path.exists(os.path.join(kb.items_dir, pid + ".md")):
            pid = f"{base}-{today}"
        tags = []
        big_venues = (kb.filters.get("big_only") or {}).get("venues") or []
        if c.get("scope") == "big-only" or any(norm(v) in norm(c.get("venue")) for v in big_venues):
            tags.append("big-event")
        if c.get("time") and c["time"] >= "19:00":
            tags.append("night")
        if c.get("price_amount") == 0:
            tags.append("free")
        tags = [t for t in tags if t in kb.tags]
        aud = defaults.get(c["category"]) or defaults.get("default") or ["friends", "couple"]
        sess = c.get("sessions") or ([{"start": c["start"], "time": c.get("time")}] if c.get("start") else [])
        L = ["---", f"id: {pid}", "domain: ideas", f"created: {ystr(now.isoformat())}", f"updated: {ystr(now.isoformat())}",
             "report_status: pending", f"title: {ystr(tidy_title(c['title'], kb))}", f"category: {c['category']}", "timing: dated",
             f"audience: [{', '.join(aud)}]", f"tags: [{', '.join(tags)}]", "status: proposed", "priority: normal",
             f"city: {c['city']}",
             f"place: {{name: {ystr(c.get('venue'))}, address: '', neighborhood: '', maps_url: ''}}"]
        if c["category"] == "cinema" and c.get("start"):
            L.append(f"available_from: {ystr(c['start'])}")
        elif sess:
            L.append("sessions:")
            for x in sess:
                note = "" if x.get("time") else "Hora sin confirmar"
                L.append(f"- {{start: {ystr(stamp(x['start'], x.get('time'), tzname))}, end: null, note: {ystr(note)}}}")
        if c.get("end") and c.get("end") != c.get("start") and not c.get("sessions") and c["category"] != "cinema":
            L.append(f"available_until: {ystr(c['end'])}")
        tu = c.get("tickets_url") or ""
        L.append(f"tickets: {{required: {'true' if tu else 'false'}, url: {ystr(tu)}, on_sale: null, state: none}}")
        if c.get("price_amount") not in (None, ""):
            L += [f"price_amount: {c['price_amount']}", f"price_currency: {c.get('price_currency') or 'COP'}"]
        links = [{"label": "Fuente", "url": c.get("url")}] + [{"label": a["source"], "url": a["url"]}
                                                              for a in c.get("also_sources") or [] if a.get("url")]
        L.append("links:")
        L += [f"- {{label: {ystr(l['label'])}, url: {ystr(l['url'])}}}" for l in links if l["url"]]
        L.append(f"source: {{type: search, url: {ystr(c.get('url'))}, found: {ystr(today)}, original: null}}")
        L += ["---", "", c.get("description") or "", ""]
        with open(os.path.join(kb.items_dir, pid + ".md"), "w", encoding="utf-8") as f:
            f.write("\n".join(L))
        index[pid] = {"report_status": "pending", "created": now.isoformat(), "updated": now.isoformat(),
                      "title": tidy_title(c["title"], kb)}
        kb.items.append(front_matter(os.path.join(kb.items_dir, pid + ".md")))
        c["plan"] = pid
        created.append(pid)
    with open(kb.index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    report["created"] = report.get("created", []) + created
    with open(kb.run_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1, default=str)
    return {"created": len(created), "ids": created}


def cmd_seen(kb, today):
    """Remember the page texts of the last fetch as read, so unchanged pages are not read again."""
    report = load_run(kb)
    for t in report.get("texts", []):
        if t.get("hash"):
            kb.seen["pages"][t["url"]] = {"hash": t["hash"], "seen": today.isoformat()}
    kb.seen.pop("candidates", None)       # candidates are never hidden: filters decide every week
    kb.seen["updated"] = today.isoformat()
    with open(kb.seen_path, "w", encoding="utf-8") as f:
        json.dump(kb.seen, f, ensure_ascii=False, indent=1)
    return {"seen_pages": len(kb.seen["pages"])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["fetch", "add", "judge", "create", "seen", "match"])
    ap.add_argument("root")
    ap.add_argument("--today")
    ap.add_argument("--only", help="fetch: comma-separated source ids")
    ap.add_argument("--file", help="add: JSON list of candidates")
    ap.add_argument("--exclude", default="", help="judge: comma-separated fp:rule-id pairs to exclude")
    ap.add_argument("--title")
    ap.add_argument("--date")
    ap.add_argument("--end")
    ap.add_argument("--city")
    ap.add_argument("--url")
    a = ap.parse_args()
    kb = KB(a.root)
    tz = str(kb.profile.get("timezone") or "")
    try:
        from zoneinfo import ZoneInfo
        now = datetime.now(ZoneInfo(tz)) if tz else datetime.now().astimezone()
    except Exception:
        now = datetime.now().astimezone()
    now = now.replace(microsecond=0)
    today = to_date(a.today) or now.date()
    out = None
    if a.command == "fetch":
        r = cmd_fetch(kb, today, set(a.only.split(",")) if a.only else None)
        out = {k: r[k] for k in ("today", "windows", "sources", "errors", "browser", "search", "out_of_window")}
        out.update({"known": len(r["known"]), "filtered": len(r["filtered"]), "new_candidates": len(r["candidates"]),
                    "need_judgment": sum(1 for c in r["candidates"] if c.get("judge")),
                    "texts": [{"source": t["source"], "url": t["url"], "chars": len(t.get("text", ""))} for t in r["texts"]],
                    "full_result": os.path.relpath(kb.run_path, a.root)})
    elif a.command == "add":
        out = cmd_add(kb, today, a.file)
    elif a.command == "judge":
        pairs = [tuple(x.split(":", 1)) for x in a.exclude.split(",") if ":" in x]
        out = cmd_judge(kb, pairs)
    elif a.command == "create":
        out = cmd_create(kb, now)
    elif a.command == "seen":
        out = cmd_seen(kb, today)
    else:
        if not a.title and not a.url:
            sys.exit("match needs --title or --url")
        mid, why = find_match(kb, a.title or "", to_date(a.date), to_date(a.end), a.city, a.url)
        out = {"match": mid, "by": why}
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
