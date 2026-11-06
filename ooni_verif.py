#!/usr/bin/env python3
"""
ooni_verif.py — Vérifie la couverture des mesures publiques OONI pour un pays
et une période, sur les réseaux sociaux, les témoins négatifs et un témoin
positif (domaine déjà bloqué par les FAI).

Ne prouve rien à lui seul : il dit si OONI avait des sondes au bon endroit au
bon moment, et ce qu'elles ont vu. « anomaly » chez OONI n'est PAS un blocage
confirmé (faux positifs fréquents) ; « confirmed » = empreinte de page de
blocage connue.

Bibliothèque standard uniquement. Python >= 3.9.

Exemples :
  python3 ooni_verif.py
  python3 ooni_verif.py --since 2026-10-17 --until 2026-10-31 \
      --focus 2026-10-24,2026-10-31 --mobile
"""
import argparse
import datetime as dt
import json
import os
import sys
import time
import urllib.parse
import urllib.request

API = "https://api.ooni.io"

# Domaines tels qu'ils figurent dans les listes de test OONI (vérifié dans
# l'agrégation FR d'octobre 2026). Une entrée absente = pas de données.
CIBLES = [
    "x.com", "twitter.com", "www.tiktok.com", "www.instagram.com",
    "i.instagram.com", "www.snapchat.com", "www.facebook.com",
    "www.youtube.com", "discord.com", "t.me", "telegram.org", "bsky.app",
    "www.whatsapp.com", "signal.org",
]
TEMOINS_NEG = ["www.wikipedia.org", "www.lemonde.fr"]
# Médias soumis aux sanctions UE (bloqués par DNS par les 4 grands FAI d'après
# OONI en oct. 2026) : prouve que la méthode « voit » un blocage DNS réel.
TEMOINS_POS = ["sputnikglobe.com", "ria.ru"]

ASN = {
    3215: "Orange", 15557: "SFR", 12322: "Free", 51207: "Free Mobile",
    5410: "Bouygues",
}


# --------------------------------------------------------------------------
# Heure de Paris sans dépendance (règle UE : heure d'été du dernier dimanche
# de mars 01:00 UTC au dernier dimanche d'octobre 01:00 UTC).
def _dernier_dimanche(annee, mois):
    d = dt.date(annee, mois + 1, 1) - dt.timedelta(days=1) if mois < 12 \
        else dt.date(annee, 12, 31)
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)


def paris(ts_utc):
    """datetime UTC (aware ou naïf) -> datetime naïf heure de Paris."""
    if ts_utc.tzinfo is not None:
        ts_utc = ts_utc.astimezone(dt.timezone.utc).replace(tzinfo=None)
    y = ts_utc.year
    debut = dt.datetime.combine(_dernier_dimanche(y, 3), dt.time(1))
    fin = dt.datetime.combine(_dernier_dimanche(y, 10), dt.time(1))
    return ts_utc + dt.timedelta(hours=2 if debut <= ts_utc < fin else 1)


# --------------------------------------------------------------------------
def get(path, cache_dir=None, **params):
    url = API + path + "?" + urllib.parse.urlencode(params)
    key = None
    if cache_dir:
        import hashlib
        key = os.path.join(cache_dir, hashlib.sha256(url.encode()).hexdigest()[:24] + ".json")
        if os.path.exists(key):
            with open(key, encoding="utf-8") as f:
                return json.load(f)
    for essai in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ooni_verif/1.0 (recherche)"})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.load(r)
            break
        except Exception as e:  # réseau / 5xx
            if essai == 3:
                raise RuntimeError(f"{url}: {e}") from e
            time.sleep(2 ** (essai + 1))
    if key:
        with open(key, "w", encoding="utf-8") as f:
            json.dump(data, f)
    return data


def asn_int(v):
    """L'API renvoie l'ASN en int (agrégation) ou en 'AS3215' (mesures)."""
    return int(str(v).upper().removeprefix("AS")) if str(v).upper().removeprefix("AS").isdigit() else v


def agg(args, **p):
    base = dict(probe_cc=args.cc, test_name="web_connectivity")
    base.update(p)
    return get("/api/v1/aggregation", args.cache, **base)["result"]


def jours(since, until):
    d = dt.date.fromisoformat(since)
    fin = dt.date.fromisoformat(until)
    while d <= fin:
        yield d
        d += dt.timedelta(days=1)


# --------------------------------------------------------------------------
def section_quotidienne(args, out):
    since = args.since
    until = (dt.date.fromisoformat(args.until) + dt.timedelta(days=1)).isoformat()
    out.append(f"## 1. Volume quotidien, {args.cc}, tous FAI\n")
    out.append("Format des cellules : `mesures / anomalies / confirmées`. "
               "Un tiret signifie aucune mesure ce jour-là.\n")
    jl = list(jours(args.since, args.until))
    out.append("| domaine | " + " | ".join(d.strftime("%d/%m") for d in jl) + " |")
    out.append("|---|" + "---|" * len(jl))
    for dom in CIBLES + TEMOINS_NEG + TEMOINS_POS:
        rows = agg(args, since=since, until=until, domain=dom, axis_x="measurement_start_day")
        by = {r["measurement_start_day"][:10]: r for r in rows}
        cells = []
        for d in jl:
            r = by.get(d.isoformat())
            cells.append("—" if not r else f"{r['measurement_count']}/{r['anomaly_count']}/{r['confirmed_count']}")
        out.append(f"| {dom} | " + " | ".join(cells) + " |")
    out.append("")


def section_focus(args, out, anomalies):
    out.append("## 2. Couverture horaire des jours ciblés, par FAI\n")
    out.append("Plage diurne : de 07:00 à 23:00, heure de Paris, soit 16 heures. "
               "Une cellule `h/16 (n, a)` se lit ainsi : h heures diurnes ont au moins une "
               "mesure, n est le nombre de mesures sur la journée et a le nombre d'anomalies. "
               "On considère que la couverture permet d'exclure une coupure de 2 h ou plus "
               "seulement si aucune fenêtre de 2 h consécutives n'est vide (colonne « trou max »).\n")
    for jour in args.focus:
        d0 = dt.date.fromisoformat(jour)
        # Journée de Paris = [J-1 22:00 UTC, J 23:00 UTC] selon DST : on prend
        # large en UTC puis on filtre en heure de Paris.
        since = (d0 - dt.timedelta(days=1)).isoformat()
        until = (d0 + dt.timedelta(days=1)).isoformat()
        jours_fr = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
        out.append(f"### {jours_fr[d0.weekday()]} {d0.strftime('%d/%m/%Y')}\n")
        out.append("| domaine | " + " | ".join(f"{v} (AS{k})" for k, v in ASN.items()) + " | trou max (tous FAI) |")
        out.append("|---|" + "---|" * (len(ASN) + 1))
        for dom in CIBLES + TEMOINS_NEG + TEMOINS_POS:
            rows = agg(args, since=since, until=until, domain=dom,
                       axis_x="measurement_start_day", axis_y="probe_asn", time_grain="hour")
            par_asn = {}
            heures_tous = set()
            for r in rows:
                t = dt.datetime.fromisoformat(r["measurement_start_day"].replace("Z", "+00:00"))
                tp = paris(t)
                if tp.date() != d0:
                    continue
                if r["measurement_count"] > 0 and 7 <= tp.hour < 23:
                    heures_tous.add(tp.hour)
                a = par_asn.setdefault(r["probe_asn"], {"h": set(), "n": 0, "a": 0})
                a["n"] += r["measurement_count"]
                a["a"] += r["anomaly_count"]
                if r["measurement_count"] > 0 and 7 <= tp.hour < 23:
                    a["h"].add(tp.hour)
            cells = []
            for k in ASN:
                a = par_asn.get(k)
                cells.append("—" if not a else f"{len(a['h'])}/16 ({a['n']}, {a['a']})")
            out.append(f"| {dom} | " + " | ".join(cells) + f" | {trou_max(heures_tous)} h |")
        out.append("")
        # liste des anomalies sur les cibles ce jour-là
        for dom in CIBLES:
            res = get("/api/v1/measurements", args.cache, probe_cc=args.cc, domain=dom,
                      since=since, until=until, anomaly="true", limit=200)["results"]
            for m in res:
                t = dt.datetime.fromisoformat(m["measurement_start_time"].replace("Z", "+00:00"))
                if paris(t).date() != d0:
                    continue
                s = m.get("scores") or {}
                anomalies.append({
                    "jour": jour, "paris": paris(t).strftime("%H:%M"), "domaine": dom,
                    "asn": asn_int(m["probe_asn"]), "confirmed": m.get("confirmed"),
                    "type": (s.get("analysis") or {}).get("blocking_type"),
                    "uid": m["measurement_uid"],
                })


def trou_max(heures):
    """Plus longue suite d'heures diurnes (7..22) sans aucune mesure."""
    best = cur = 0
    for h in range(7, 23):
        cur = 0 if h in heures else cur + 1
        best = max(best, cur)
    return best


def section_anomalies(out, anomalies):
    out.append("## 3. Anomalies sur les réseaux sociaux pendant les jours ciblés\n")
    if not anomalies:
        out.append("Aucune anomalie OONI sur les domaines cibles ces jours-là.\n")
        return
    out.append("Une anomalie OONI n'est pas un blocage. Chacune est à ouvrir dans "
               "OONI Explorer avant toute interprétation. Un motif ne compte que s'il se répète "
               "chez un même FAI pendant la même fenêtre horaire.\n")
    out.append("| jour | heure Paris | domaine | FAI | type | confirmée | mesure |")
    out.append("|---|---|---|---|---|---|---|")
    for a in sorted(anomalies, key=lambda x: (x["jour"], x["paris"])):
        fai = ASN.get(a["asn"], f"AS{a['asn']}")
        url = f"https://explorer.ooni.org/m/{a['uid']}"
        out.append(f"| {a['jour']} | {a['paris']} | {a['domaine']} | {fai} | {a['type']} | "
                   f"{a['confirmed']} | [lien]({url}) |")
    out.append("")


def section_mobile(args, out):
    """Échantillonne les mesures brutes pour lire annotations.network_type
    (wifi / mobile), absent de l'API d'agrégation."""
    out.append("## 4. Part des mesures prises en réseau mobile (jours ciblés)\n")
    out.append("La colonne `network_type` vient des mesures brutes. On échantillonne au plus "
               f"{args.mobile_max} mesures par domaine et par jour. Les sondes OONI en ligne de "
               "commande ne renseignent souvent pas ce champ (valeur « ? »).\n")
    out.append("| jour | domaine | FAI | mobile | wifi | ? |")
    out.append("|---|---|---|---|---|---|")
    for jour in args.focus:
        d0 = dt.date.fromisoformat(jour)
        since = (d0 - dt.timedelta(days=1)).isoformat()
        until = (d0 + dt.timedelta(days=1)).isoformat()
        for dom in ["www.tiktok.com", "www.instagram.com", "www.snapchat.com", "x.com", "twitter.com"]:
            res = get("/api/v1/measurements", args.cache, probe_cc=args.cc, domain=dom,
                      since=since, until=until, limit=args.mobile_max)["results"]
            cpt = {}
            for m in res:
                t = dt.datetime.fromisoformat(m["measurement_start_time"].replace("Z", "+00:00"))
                if paris(t).date() != d0:
                    continue
                try:
                    raw = get("/api/v1/raw_measurement", args.cache, measurement_uid=m["measurement_uid"])
                    nt = (raw.get("annotations") or {}).get("network_type") or "?"
                except RuntimeError:
                    nt = "?"
                c = cpt.setdefault(asn_int(m["probe_asn"]), {"mobile": 0, "wifi": 0, "?": 0})
                c[nt if nt in c else "?"] += 1
            for asn, c in sorted(cpt.items(), key=lambda kv: -sum(kv[1].values())):
                out.append(f"| {jour} | {dom} | {ASN.get(asn, f'AS{asn}')} | {c['mobile']} | {c['wifi']} | {c['?']} |")
    out.append("")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cc", default="FR")
    ap.add_argument("--since", default="2026-10-17")
    ap.add_argument("--until", default="2026-10-31", help="inclus")
    ap.add_argument("--focus", default="2026-10-24,2026-10-31",
                    help="jours (heure de Paris) à examiner heure par heure")
    ap.add_argument("--mobile", action="store_true",
                    help="échantillonne les mesures brutes pour compter wifi/mobile (lent)")
    ap.add_argument("--mobile-max", type=int, default=150)
    ap.add_argument("--out", default="ooni/rapport_ooni.md")
    ap.add_argument("--cache", default="ooni/cache")
    args = ap.parse_args()
    args.focus = [j.strip() for j in args.focus.split(",") if j.strip()]
    os.makedirs(args.cache, exist_ok=True)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    out = [f"# Mesures OONI, {args.cc}, du {args.since} au {args.until}\n",
           f"Rapport généré le {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC "
           f"par `ooni_verif.py`. Source : {API} (test `web_connectivity`).\n"]
    section_quotidienne(args, out)
    anomalies = []
    section_focus(args, out, anomalies)
    section_anomalies(out, anomalies)
    if args.mobile:
        section_mobile(args, out)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"Rapport écrit : {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
