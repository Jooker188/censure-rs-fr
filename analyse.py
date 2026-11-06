#!/usr/bin/env python3
"""
analyse.py — analyse les CSV produits par moniteur_reseaux.py (v2.x).

Produit dans --out (défaut : rapport/) :
  analyse.md    rapport lisible : contrôles de validité, épisodes, synthèse
  episodes.csv  un épisode = même signal, même hôte, même point de mesure,
                sur des tours consécutifs
  frise.html    frise chronologique (disponibilité par plateforme et par
                point de mesure, événements marqués), autonome, sans réseau
  frise.svg     la même frise, en image

Tout est recalculé à partir des colonnes brutes : les verdicts écrits par le
moniteur ne servent qu'à l'affichage en direct.

Ce script DÉCRIT des signaux réseau. Il ne désigne jamais de cause : une panne,
un incident chez le FAI et un blocage volontaire peuvent produire les mêmes
traces. La conclusion reste humaine (voir README).

Bibliothèque standard uniquement. Python >= 3.9.

  python3 analyse.py mesures_*.csv --evenements evenements.csv
"""
import argparse
import collections
import csv
import datetime as dt
import glob
import html
import ipaddress
import os
import statistics
import sys

# Hôtes dont le certificat n'est pas signé par une autorité publique (Signal
# utilise sa propre autorité pour chat.signal.org) : un « certificat invalide »
# y est normal et n'est pas un signal.
CERT_ATTENDU_INVALIDE = {"chat.signal.org"}

ORDRE_PLATEFORMES = ["x", "tiktok", "instagram", "snapchat", "facebook", "youtube", "discord",
                     "telegram", "bluesky", "whatsapp", "signal", "messenger", "threads", "reddit",
                      "twitch", "bereal", "mastodon"]
NOMS = {"x": "X", "tiktok": "TikTok", "instagram": "Instagram", "snapchat": "Snapchat",
        "facebook": "Facebook", "youtube": "YouTube", "discord": "Discord", "telegram": "Telegram",
        "bluesky": "Bluesky", "whatsapp": "WhatsApp", "signal": "Signal", "messenger": "Messenger",
        "threads": "Threads", "reddit": "Reddit", "twitch": "Twitch", "bereal": "BeReal", "mastodon": "Mastodon",
        "_temoins": "Témoins (sites ordinaires)", "_pos": "Témoin positif (blocage attendu)"}

# Gravité des signaux. « signature » = forme typique d'un blocage réseau
# (mais pas une preuve) ; « echec » = échec sans forme caractéristique.
SIGNATURE = "signature"
ECHEC = "echec"


# ------------------------------------------------------------------ temps
def _dernier_dimanche(annee, mois):
    d = (dt.date(annee, mois + 1, 1) - dt.timedelta(days=1))
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)


def paris(t):
    """datetime UTC naïf -> heure de Paris naïve (règle UE)."""
    debut = dt.datetime.combine(_dernier_dimanche(t.year, 3), dt.time(1))
    fin = dt.datetime.combine(_dernier_dimanche(t.year, 10), dt.time(1))
    return t + dt.timedelta(hours=2 if debut <= t < fin else 1)


def paris_vers_utc(t):
    for h in (1, 2):
        if paris(t - dt.timedelta(hours=h)) == t:
            return t - dt.timedelta(hours=h)
    return t - dt.timedelta(hours=1)


def parse_ts(s):
    return dt.datetime.strptime(s.strip(), "%Y-%m-%dT%H:%M:%SZ")


def fmt(t):
    return paris(t).strftime("%d/%m %H:%M")


JOURS = ["lun.", "mar.", "mer.", "jeu.", "ven.", "sam.", "dim."]


# ------------------------------------------------------------ classification
def bogon(ip):
    try:
        a = ipaddress.ip_address(ip)
    except ValueError:
        return True
    return (a.is_private or a.is_loopback or a.is_unspecified or a.is_reserved or a.is_link_local
            or a.is_multicast or (a.version == 4 and a in ipaddress.ip_network("100.64.0.0/10")))


def classe_resolution(code, ips):
    """code = rcode DNS (NOERROR, NXDOMAIN…), « ERR:xxx » ou erreur getaddrinfo."""
    ips = ips.split() if isinstance(ips, str) else list(ips)
    if ips:
        return "bogon" if any(bogon(i) for i in ips) else "ok"
    c = (code or "").lower()
    if not c:
        return "na"
    if c in ("nxdomain", "nodata", "gai_noname"):
        return "nx"
    if c in ("servfail", "refused"):
        return c
    if "timeout" in c or c == "gai_again":
        return "timeout"
    if c == "noerror":
        return "nx"
    return "erreur"


def signaux_ligne(r):
    """Liste de (signal, gravité) pour une ligne cible ou témoin."""
    out = []
    doh_ok = r["doh_rcode"] == "NOERROR" and r["doh_ips"].strip()
    if not doh_ok and r["doh_rcode"] in ("NXDOMAIN", "NODATA"):
        return [("inexistant", None)]  # le domaine n'existe nulle part : ignoré
    if doh_ok:
        isp = classe_resolution(r["isp_rcode"].replace("ERR:", ""), r["isp_ips"])
        sysc = classe_resolution(r["sys_err"], r["sys_ips"])
        p53 = classe_resolution(r["p53_rcode"].replace("ERR:", ""), r["p53_ips"])
        for src, c in (("fai", isp), ("sys", sysc), ("p53", p53)):
            if c in ("nx", "bogon", "refused"):
                out.append((f"dns_{src}_{c}", SIGNATURE))
            elif c in ("servfail", "timeout", "erreur"):
                out.append((f"dns_{src}_{c}", ECHEC))
    if r["tcp_err"]:
        alt_ok = r.get("alt_tcp_err") == "ok" and r.get("alt_tls_err") == "ok"
        suffixe = "_ip_seule" if alt_ok else ""
        g = SIGNATURE if r["tcp_err"] in ("reset", "refused") or alt_ok else ECHEC
        out.append((f"tcp_{r['tcp_err']}{suffixe}", g))
    if r["tls_err"]:
        e = r["tls_err"]
        if e.startswith("cert_invalide"):
            if r["host"] not in CERT_ATTENDU_INVALIDE:
                out.append(("tls_cert_invalide", SIGNATURE))
        elif e in ("reset", "aborted") or "eof" in e.lower():
            out.append((f"tls_{e}", SIGNATURE))
        else:
            out.append((f"tls_{e}", ECHEC))
    if r["http_err"]:
        e = r["http_err"]
        out.append((f"http_{e}", SIGNATURE if e in ("reset", "aborted") else ECHEC))
    return out


def gravite(sigs):
    gs = {g for _, g in sigs}
    return SIGNATURE if SIGNATURE in gs else ECHEC if ECHEC in gs else None


# ---------------------------------------------------------------- lecture
def lire(fichiers):
    lignes, metas = [], []
    for f in fichiers:
        with open(f, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                if not r.get("round_id") or not r.get("ts_utc"):
                    continue
                for k in ("isp_rcode", "isp_ips", "p53_rcode", "p53_ips", "alt_tcp_err", "alt_tls_err",
                          "http_err", "tls_err", "tcp_err", "sys_err", "sys_ips", "doh_rcode", "doh_ips",
                          "http_status", "tls_issuer", "kind", "platform", "note"):
                    r[k] = r.get(k) or ""
                r["_t"] = parse_ts(r["ts_utc"])
                r["_src"] = os.path.basename(f)
                (metas if r["kind"] == "meta" else lignes).append(r)
    return lignes, metas


def lire_evenements(path):
    if not path or not os.path.exists(path):
        return []
    evs = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d = dt.datetime.fromisoformat(r["debut"])
            fi = dt.datetime.fromisoformat(r["fin"]) if r.get("fin") else None
            evs.append({**r, "_d": paris_vers_utc(d), "_f": paris_vers_utc(fi) if fi else None})
    return evs


# ---------------------------------------------------------------- analyse
def construire(lignes, metas):
    """Organise par point de mesure et par tour."""
    tours = collections.defaultdict(dict)  # vantage -> round_id -> infos
    for r in lignes:
        v, rid = r["vantage"], r["round_id"]
        t = tours[v].setdefault(rid, {"t": r["_t"], "lignes": [], "meta": None})
        t["t"] = min(t["t"], r["_t"])
        t["lignes"].append(r)
    for m in metas:
        if m["round_id"] in tours.get(m["vantage"], {}):
            tours[m["vantage"]][m["round_id"]]["meta"] = m
    for v, ts in tours.items():
        for rid, t in ts.items():
            neg = [x for x in t["lignes"] if x["kind"] == "temoin_neg"]
            for x in t["lignes"]:
                x["_sigs"] = signaux_ligne(x)
                x["_g"] = gravite(x["_sigs"])
            ko = [x for x in neg if x["_g"]]
            # Tour invalide si au moins la moitié des témoins échouent :
            # c'est la connexion de mesure qui est en cause, pas une cible.
            t["connexion_ko"] = bool(neg) and len(ko) * 2 >= len(neg)
            t["temoins_ko"] = len(ko)
            t["temoins_n"] = len(neg)
    return tours


def episodes(tours):
    """Regroupe les signaux identiques sur des tours consécutifs (1 tour
    manquant toléré)."""
    eps = []
    for v, ts in tours.items():
        ordre = sorted(ts, key=lambda rid: ts[rid]["t"])
        idx = {rid: i for i, rid in enumerate(ordre)}
        ouverts = {}
        for rid in ordre:
            t = ts[rid]
            if t["connexion_ko"]:
                continue  # tour invalide : ni ouvert ni prolongé (listé dans les contrôles)
            presents = set()
            for x in t["lignes"]:
                if x["kind"] == "temoin_pos":
                    continue
                for sig, g in x["_sigs"]:
                    if g is None:
                        continue
                    k = (x["host"], sig)
                    presents.add(k)
                    e = ouverts.get(k)
                    if e and idx[rid] - e["dernier_idx"] <= 2:
                        e["fin"] = t["t"]
                        e["dernier_idx"] = idx[rid]
                        e["n"] += 1
                        e["n_temoins_ok"] += 0 if t["connexion_ko"] else 1
                    else:
                        if e:
                            eps.append(e)
                        ouverts[k] = {"vantage": v, "fai": x["fai"], "platform": x["platform"] or x["kind"],
                                      "kind": x["kind"], "host": x["host"], "signal": sig, "gravite": g,
                                      "debut": t["t"], "fin": t["t"], "n": 1, "dernier_idx": idx[rid],
                                      "n_temoins_ok": 0 if t["connexion_ko"] else 1,
                                      "exemple": f"isp={x['isp_rcode']}:{x['isp_ips']} sys={x['sys_err'] or x['sys_ips']} "
                                                 f"doh={x['doh_ips']} tcp={x['tcp_err']} tls={x['tls_err']} "
                                                 f"alt={x.get('alt_tcp_err', '')}/{x.get('alt_tls_err', '')}"}
        eps.extend(ouverts.values())
    # comparaison avec les autres points de mesure sur la même fenêtre
    for e in eps:
        autres = []
        for v2, ts2 in tours.items():
            if v2 == e["vantage"]:
                continue
            ok = ko = 0
            for t in ts2.values():
                if e["debut"] - dt.timedelta(minutes=10) <= t["t"] <= e["fin"] + dt.timedelta(minutes=10):
                    for x in t["lignes"]:
                        if x["host"] == e["host"]:
                            if any(s == e["signal"] for s, _ in x["_sigs"]):
                                ko += 1
                            else:
                                ok += 1
            autres.append(f"{v2}: {'pas de mesure' if ok + ko == 0 else f'{ko} même signal / {ok} sans'}")
        e["autres_points"] = " ; ".join(autres) or "aucun autre point"
        e["repete"] = e["n"] >= 3
        e["temoins_ok"] = e["n_temoins_ok"] == e["n"]
    eps.sort(key=lambda e: (e["vantage"], e["debut"]))
    return eps


def changements_issuer(tours):
    """Changements d'organisation émettrice du certificat, par hôte et point."""
    out = []
    for v, ts in tours.items():
        prec = {}
        for rid in sorted(ts, key=lambda r: ts[r]["t"]):
            for x in ts[rid]["lignes"]:
                org = x["tls_issuer"].split("/")[0] if x["tls_issuer"] else ""
                if not org:
                    continue
                if x["host"] in prec and prec[x["host"]] != org:
                    vu = []
                    for v2, ts2 in tours.items():
                        if v2 == v:
                            continue
                        for t2 in ts2.values():
                            if abs((t2["t"] - ts[rid]["t"]).total_seconds()) < 7200:
                                if any(y["host"] == x["host"] and y["tls_issuer"].startswith(org) for y in t2["lignes"]):
                                    vu.append(v2)
                                    break
                    out.append({"vantage": v, "host": x["host"], "t": ts[rid]["t"], "avant": prec[x["host"]],
                                "apres": org, "vu_ailleurs": ", ".join(sorted(set(vu))) or "non"})
                prec[x["host"]] = org
    return out


def controles(tours, fichiers_meta):
    """Contrôles de validité par point de mesure."""
    res = {}
    for v, ts in tours.items():
        ordre = sorted(ts.values(), key=lambda t: t["t"])
        deltas = [(b["t"] - a["t"]).total_seconds() for a, b in zip(ordre, ordre[1:])]
        med = statistics.median(deltas) if deltas else 0
        trous = [(a["t"], b["t"]) for a, b in zip(ordre, ordre[1:])
                 if med and (b["t"] - a["t"]).total_seconds() > 2.5 * med]
        pannes, cur = [], None
        for t in ordre:
            if t["connexion_ko"]:
                cur = [t["t"], t["t"]] if cur is None else [cur[0], t["t"]]
            elif cur:
                pannes.append(cur)
                cur = None
        if cur:
            pannes.append(cur)
        pos_total = pos_fai = pos_sys = 0
        for t in ordre:
            for x in t["lignes"]:
                if x["kind"] == "temoin_pos":
                    pos_total += 1
                    noms = {s for s, _ in x["_sigs"]}
                    pos_fai += any(s.startswith("dns_fai_") for s in noms)
                    pos_sys += any(s.startswith("dns_sys_") for s in noms)
        asns = collections.Counter()
        p53 = collections.Counter()
        for t in ordre:
            m = t["meta"]
            if not m:
                continue
            kv = dict(p.split("=", 1) for p in m["note"].split() if "=" in p)
            asns[kv.get("asn", "?")] += 1
            pid = kv.get("p53_id", "")
            p53["ok" if pid.startswith("NOERROR:") else pid or "?"] += 1
        fais = collections.Counter(x["fai"] for t in ordre for x in t["lignes"][:1])
        resolveurs = collections.Counter(x.get("isp_resolver", "") for t in ordre for x in t["lignes"][:1])
        res[v] = {
            "n": len(ordre), "debut": ordre[0]["t"], "fin": ordre[-1]["t"], "intervalle": med,
            "trous": trous, "connexion_ko": sum(t["connexion_ko"] for t in ordre), "pannes": pannes,
            "pos_total": pos_total, "pos_fai": pos_fai, "pos_sys": pos_sys,
            "asns": asns, "p53": p53, "fais": fais, "resolveurs": resolveurs,
            "versions": collections.Counter(x["tool_version"] for t in ordre for x in t["lignes"][:1]),
        }
    return res


def statut_cellule(t, hotes):
    """Statut d'une plateforme pendant un tour."""
    if t["connexion_ko"]:
        return "connexion_ko", []
    pire, ko = None, []
    for x in hotes:
        if x["_g"]:
            ko.append(f"{x['host']} ({', '.join(s for s, g in x['_sigs'] if g)})")
            if x["_g"] == SIGNATURE or pire is None:
                pire = x["_g"]
    return (pire or "ok"), ko


def statut_temoin_pos(t, hotes):
    if not hotes:
        return None, []
    det = [x["host"] for x in hotes if any(s.startswith(("dns_fai_", "dns_sys_")) for s, _ in x["_sigs"])]
    return ("pos_detecte" if len(det) == len(hotes) else "pos_partiel" if det else "pos_non_detecte"), det


def grille(tours):
    """vantage -> liste de lignes (clé, libellé, [(t0, t1, statut, détail)])."""
    out = {}
    for v, ts in tours.items():
        ordre = sorted(ts.values(), key=lambda t: t["t"])
        if not ordre:
            continue
        med = statistics.median([(b["t"] - a["t"]).total_seconds() for a, b in zip(ordre, ordre[1:])] or [300])
        plats = sorted({x["platform"] for t in ordre for x in t["lignes"] if x["kind"] == "cible"},
                       key=lambda p: (ORDRE_PLATEFORMES.index(p) if p in ORDRE_PLATEFORMES else 99, p))
        rangs = []
        for cle in plats + ["_temoins", "_pos"]:
            cells = []
            for i, t in enumerate(ordre):
                t1 = ordre[i + 1]["t"] if i + 1 < len(ordre) else t["t"] + dt.timedelta(seconds=med)
                t1 = min(t1, t["t"] + dt.timedelta(seconds=1.5 * med))
                if cle == "_temoins":
                    h = [x for x in t["lignes"] if x["kind"] == "temoin_neg"]
                    st, d = ("connexion_ko", [x["host"] for x in h if x["_g"]]) if t["connexion_ko"] else \
                        (("ok", []) if not any(x["_g"] for x in h) else ("echec", [x["host"] for x in h if x["_g"]]))
                elif cle == "_pos":
                    st, d = statut_temoin_pos(t, [x for x in t["lignes"] if x["kind"] == "temoin_pos"])
                else:
                    st, d = statut_cellule(t, [x for x in t["lignes"] if x["kind"] == "cible" and x["platform"] == cle])
                if st:
                    cells.append([t["t"], t1, st, d, 1])
            # fusion des cellules contiguës de même statut
            runs = []
            for c in cells:
                if runs and runs[-1][2] == c[2] and (c[0] - runs[-1][1]).total_seconds() < 1.5 * med:
                    runs[-1][1] = c[1]
                    runs[-1][4] += 1
                    runs[-1][3] = sorted(set(runs[-1][3]) | set(c[3]))[:6]
                else:
                    runs.append(c)
            rangs.append((cle, NOMS.get(cle, cle), runs))
        fai = ordre[0]["lignes"][0]["fai"] if ordre[0]["lignes"] else ""
        out[v] = {"fai": fai, "rangs": rangs}
    return out


# ------------------------------------------------------------------ frise
COULEURS = {  # palette « status » + neutres ; toujours accompagnée d'un libellé
    "ok": ("var(--ok)", "accessible"),
    "echec": ("var(--serious)", "échec (timeout, erreur), témoins OK"),
    "signature": ("var(--critical)", "signature de blocage (DNS menteur, reset, certificat invalide), témoins OK"),
    "connexion_ko": ("var(--muted)", "connexion de mesure en panne (témoins KO) : tour ignoré"),
    "pos_detecte": ("var(--ink2)", "témoin positif : blocage détecté (attendu)"),
    "pos_partiel": ("var(--warning)", "témoin positif : blocage détecté sur une partie des domaines"),
    "pos_non_detecte": ("var(--warning)", "témoin positif : blocage NON détecté (outil aveugle sur ce point)"),
}


def frise_svg(g, evs, debut, fin, largeur=1400):
    gauche, droite, haut = 230, 20, 120
    h_rang, gap = 16, 3
    w = largeur - gauche - droite
    span = (fin - debut).total_seconds() or 1

    def x(t):
        return gauche + max(0, min(w, (t - debut).total_seconds() / span * w))

    blocs = []
    y = haut
    for v, d in g.items():
        blocs.append(("titre", v, d["fai"], y))
        y += 22
        for cle, lib, runs in d["rangs"]:
            blocs.append(("rang", cle, lib, y, runs))
            y += h_rang + gap
        y += 14
    hauteur = y + 150
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largeur} {hauteur}" '
         f'role="img" aria-labelledby="frise-titre" font-family="system-ui, -apple-system, Segoe UI, sans-serif">',
         '<title id="frise-titre">Disponibilité des réseaux sociaux par point de mesure</title>',
         STYLE_SVG,
         f'<rect class="fond" x="0" y="0" width="{largeur}" height="{hauteur}"/>']
    # bandes d'événements (périodes) et graduations
    for e in evs:
        if e["_f"] and e["_f"] > debut and e["_d"] < fin:
            x0, x1 = x(max(e["_d"], debut)), x(min(e["_f"], fin))
            o.append(f'<rect class="bande" x="{x0:.1f}" y="{haut - 8}" width="{max(1, x1 - x0):.1f}" '
                     f'height="{y - haut}"><title>{html.escape(e["libelle"])} ({html.escape(e["statut"])})</title></rect>')
    # axe horaire (heure de Paris)
    pas_h = max(1, int(span / 3600 / 24) + 1)
    pas_h = next(p for p in (1, 2, 3, 6, 12, 24, 48) if p >= pas_h * 1)
    if span / 3600 / pas_h > 28:
        pas_h = next(p for p in (3, 6, 12, 24, 48, 168) if span / 3600 / p <= 28)
    tp = paris(debut).replace(minute=0, second=0)
    while (tp.hour % pas_h):
        tp += dt.timedelta(hours=1)
    while paris_vers_utc(tp) <= fin:
        tu = paris_vers_utc(tp)
        if tu >= debut:
            xx = x(tu)
            jour = tp.hour == 0
            o.append(f'<line class="{"grille-j" if jour else "grille"}" x1="{xx:.1f}" x2="{xx:.1f}" y1="{haut - 10}" y2="{y - 10}"/>')
            lab = f"{JOURS[tp.weekday()]} {tp.day:02d}/{tp.month:02d}" if jour or tp == paris(debut).replace(minute=0, second=0) else f"{tp.hour:02d}h"
            o.append(f'<text class="axe" x="{xx:.1f}" y="{haut - 14}" text-anchor="middle">{lab}</text>')
        tp += dt.timedelta(hours=pas_h)
    # libellés d'événements : ponctuels (point + ligne) et périodes (crochet)
    niveaux = []
    for e in sorted(evs, key=lambda e: e["_d"]):
        if e["_f"]:
            if not (e["_f"] > debut and e["_d"] < fin):
                continue
            xx = x(max(e["_d"], debut))
        elif debut <= e["_d"] <= fin:
            xx = x(e["_d"])
        else:
            continue
        lab = e["libelle"] if len(e["libelle"]) <= 70 else e["libelle"][:69] + "…"
        larg = 6 * len(lab) + 16
        a_droite = xx + larg <= largeur - 10
        g0, g1 = (xx, xx + larg) if a_droite else (xx - larg, xx)
        n = 0
        while n < len(niveaux) and any(not (g1 < a or g0 > b) for a, b in niveaux[n]):
            n += 1
        if n == len(niveaux):
            niveaux.append([])
        niveaux[n].append((g0, g1))
        yl = 22 + n * 16
        tip = f'<title>{html.escape(fmt(e["_d"]))} : {html.escape(e["libelle"])} ({html.escape(e["statut"])})</title>'
        if e["_f"]:
            x1 = x(min(e["_f"], fin))
            o.append(f'<path class="ev-per" d="M{xx:.1f},{yl + 5} v-5 H{x1:.1f} v5"/>')
        else:
            o.append(f'<line class="ev" x1="{xx:.1f}" x2="{xx:.1f}" y1="{yl + 4}" y2="{y - 10}"/>')
            o.append(f'<circle class="ev-pt" cx="{xx:.1f}" cy="{yl}" r="5">{tip}</circle>')
        tx, anc = (xx + 8, "start") if a_droite else (xx - 8, "end")
        o.append(f'<text class="ev-lab" x="{tx:.1f}" y="{yl + (-3 if e["_f"] else 4)}" text-anchor="{anc}">'
                 f'{html.escape(lab)}{tip}</text>')
    # rangs
    for b in blocs:
        if b[0] == "titre":
            o.append(f'<text class="vantage" x="12" y="{b[3] + 14}">Point « {html.escape(b[1])} » — {html.escape(b[2])}</text>')
            continue
        _, cle, lib, yy, runs = b
        o.append(f'<text class="rang" x="{gauche - 8}" y="{yy + 12}" text-anchor="end">{html.escape(lib)}</text>')
        o.append(f'<rect class="vide" x="{gauche}" y="{yy}" width="{w}" height="{h_rang}" rx="2"/>')
        for t0, t1, st, det, n in runs:
            x0, x1 = x(t0), x(t1)
            coul, lib_st = COULEURS.get(st, ("var(--muted)", st))
            detail = (" — " + html.escape("; ".join(det))) if det else ""
            o.append(f'<rect x="{x0:.1f}" y="{yy}" width="{max(1.5, x1 - x0 - 0.5):.1f}" height="{h_rang}" '
                     f'style="fill:{coul}" rx="2"><title>{html.escape(lib)} : {html.escape(lib_st)}, '
                     f'{fmt(t0)} → {fmt(t1)} ({n} tour{"s" if n > 1 else ""}){detail}</title></rect>')
    # légende
    ly = y + 10
    o.append(f'<text class="vantage" x="12" y="{ly}">Légende</text>')
    for i, (k, (coul, lib)) in enumerate([(k, COULEURS[k]) for k in
                                          ("ok", "echec", "signature", "connexion_ko", "pos_detecte", "pos_non_detecte")]):
        cx = 12 + (i % 2) * 640
        cy = ly + 14 + (i // 2) * 22
        o.append(f'<rect x="{cx}" y="{cy}" width="22" height="12" rx="2" style="fill:{coul}"/>')
        o.append(f'<text class="leg" x="{cx + 30}" y="{cy + 10}">{html.escape(lib)}</text>')
    o.append(f'<rect class="vide" x="12" y="{ly + 14 + 3 * 22}" width="22" height="12" rx="2"/>'
             f'<text class="leg" x="42" y="{ly + 24 + 3 * 22}">pas de mesure (machine éteinte, en veille, hors ligne)</text>')
    o.append(f'<text class="leg" x="672" y="{ly + 24 + 3 * 22}">Heures de Paris. Fond bleuté et crochet : période d\'événement. '
             f'Survoler une case pour le détail.</text>')
    o.append("</svg>")
    return "\n".join(o)


STYLE_SVG = """<style>
svg { --surface:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#b9b8b0; --grid:#e1e0d9; --axis:#c3c2b7;
      --ok:#7cc77c; --warning:#fab219; --serious:#ec835a; --critical:#d03b3b; --band:rgba(42,120,214,0.08); --ev:#2a78d6; }
@media (prefers-color-scheme: dark) { svg:where(:not([data-theme="light"] svg)) {
      --surface:#1a1a19; --ink:#f0efec; --ink2:#c3c2b7; --muted:#4a4a46; --grid:#2c2c2a; --axis:#383835;
      --ok:#2f7a2f; --band:rgba(57,135,229,0.14); --ev:#3987e5; } }
[data-theme="dark"] svg { --surface:#1a1a19; --ink:#f0efec; --ink2:#c3c2b7; --muted:#4a4a46; --grid:#2c2c2a;
      --axis:#383835; --ok:#2f7a2f; --band:rgba(57,135,229,0.14); --ev:#3987e5; }
.fond { fill: var(--surface); }
.vide { fill: none; stroke: var(--grid); stroke-width: 1; }
.grille { stroke: var(--grid); stroke-width: 1; }
.grille-j { stroke: var(--axis); stroke-width: 1.5; }
.axe { fill: var(--ink2); font-size: 11px; }
.rang { fill: var(--ink); font-size: 12px; }
.vantage { fill: var(--ink); font-size: 14px; font-weight: 600; }
.leg { fill: var(--ink2); font-size: 12px; }
.bande { fill: var(--band); }
.ev { stroke: var(--ev); stroke-width: 1.5; stroke-dasharray: 3 3; }
.ev-pt { fill: var(--ev); stroke: var(--surface); stroke-width: 2; }
.ev-lab { fill: var(--ink2); font-size: 11px; }
.ev-per { fill: none; stroke: var(--ev); stroke-width: 1.5; }
rect:hover { stroke: var(--ink); stroke-width: 1; }
</style>"""


def frise_html(svg, titre, evs_hors):
    lignes = "".join(f"<li>{html.escape(e['debut'])} — {html.escape(e['libelle'])} "
                     f"<em>({html.escape(e['statut'])})</em></li>" for e in evs_hors)
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Frise des mesures</title>
<style>
:root {{ --surface:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --surface:#1a1a19; --ink:#f0efec; --ink2:#c3c2b7; }} }}
:root[data-theme="dark"] {{ --surface:#1a1a19; --ink:#f0efec; --ink2:#c3c2b7; }}
body {{ background:var(--surface); color:var(--ink); font-family:system-ui,-apple-system,Segoe UI,sans-serif;
       margin:0; padding:16px; }}
.defile {{ overflow-x:auto; }} svg {{ min-width:900px; width:100%; height:auto; }}
p, li {{ color:var(--ink2); max-width:75ch; line-height:1.5; }}
</style></head><body>
<h1>{html.escape(titre)}</h1>
<p>Chaque ligne est une plateforme, mesurée depuis un point de mesure. Une case rouge ou orange décrit un
<strong>signal réseau</strong>. Elle ne dit rien de sa cause : une panne, un incident chez le FAI et un
blocage peuvent laisser les mêmes traces.</p>
<div class="defile">{svg}</div>
{"<h2>Événements hors de la période mesurée</h2><ul>" + lignes + "</ul>" if lignes else ""}
</body></html>"""


# ---------------------------------------------------------------- rapport
def rapport(fichiers, tours, ctrl, eps, chg, evs, statuts_http):
    o = ["# Analyse des mesures\n",
         f"Fichiers analysés : {', '.join(os.path.basename(f) for f in fichiers)}. Les heures sont données en heure de Paris.\n",
         "Ce rapport décrit des signaux réseau. Il ne désigne aucune cause, et une anomalie isolée n'est pas un blocage.\n",
         "## 1. Contrôles de validité (à lire en premier)\n",
         "| point | FAI déclaré | tours | période | intervalle médian | trous > 2,5 × intervalle | tours ignorés (témoins KO) | "
         "témoin positif bloqué au DNS du FAI | idem au DNS système | AS de sortie | 1.1.1.1 non intercepté |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for v, c in ctrl.items():
        pf = f"{c['pos_fai']}/{c['pos_total']}" if c["pos_total"] else "—"
        ps = f"{c['pos_sys']}/{c['pos_total']}" if c["pos_total"] else "—"
        asn = ", ".join(f"{a} ({n})" for a, n in c["asns"].most_common(4))
        p53 = f"{c['p53'].get('ok', 0)}/{sum(c['p53'].values())}"
        o.append(f"| {v} | {', '.join(c['fais'])} | {c['n']} | {fmt(c['debut'])} → {fmt(c['fin'])} | "
                 f"{c['intervalle'] / 60:.1f} min | {len(c['trous'])} | {c['connexion_ko']} | {pf} | {ps} | {asn} | {p53} |")
    o.append("")
    o.append("Comment lire ce tableau :")
    o.append("- **Témoin positif.** Pour un FAI français, le DNS de l'opérateur doit le bloquer dans presque tous les tours. "
             "Si ce n'est pas le cas, l'outil ne voit pas le filtrage DNS du FAI depuis ce point : on ne peut alors rien "
             "conclure sur le DNS, seulement sur TCP, TLS et HTTP. Depuis un VPS à l'étranger, un résultat proche de 0 est normal.")
    o.append("- **Écart entre DNS du FAI et DNS système.** La machine n'utilise pas le résolveur du FAI (DoH, DNS manuel, "
             "antivirus…) : les applications de cette machine ne subiraient pas un filtrage DNS du FAI.")
    o.append("- **AS de sortie.** Un AS inattendu signale un VPN ou une bascule du téléphone entre 4G et Wi-Fi.")
    o.append("- **Trous.** Une période sans mesure ne veut pas dire « accessible ».\n")
    for v, c in ctrl.items():
        if c["pannes"]:
            o.append(f"Pannes de la connexion de mesure pour « {v} » (témoins KO, tours ignorés) : "
                     + " ; ".join(f"{fmt(a)} → {fmt(b)}" for a, b in c["pannes"][:15]) + "\n")
        if c["trous"]:
            o.append(f"Trous pour « {v} » : " + " ; ".join(f"{fmt(a)} → {fmt(b)}" for a, b in c["trous"][:15])
                     + (" …" if len(c["trous"]) > 15 else "") + "\n")

    o.append("## 2. Épisodes (signaux répétés ou isolés)\n")
    o.append("Un épisode regroupe un même signal, sur le même hôte et le même point de mesure, pendant des tours "
             "consécutifs (un tour manquant toléré). On le dit « répété » à partir de 3 tours. Les témoins sont dits "
             "« OK » quand les sites ordinaires répondaient pendant tout l'épisode.\n")
    cibles = [e for e in eps if e["kind"] == "cible"]
    if not cibles:
        o.append("**Aucun signal sur les réseaux sociaux.**\n")
    else:
        o.append("| point | plateforme | hôte | signal | gravité | début | fin | tours | répété | témoins OK | autres points (même fenêtre) |")
        o.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for e in cibles:
            o.append(f"| {e['vantage']} | {NOMS.get(e['platform'], e['platform'])} | {e['host']} | `{e['signal']}` | "
                     f"{e['gravite']} | {fmt(e['debut'])} | {fmt(e['fin'])} | {e['n']} | {'oui' if e['repete'] else 'non'} | "
                     f"{'oui' if e['temoins_ok'] else 'non'} | {e['autres_points']} |")
        o.append("")
    tem = [e for e in eps if e["kind"] == "temoin_neg"]
    if tem:
        o.append(f"Signaux sur les témoins ordinaires : {len(tem)} épisode(s), voir `episodes.csv`. "
                 "S'ils coïncident avec des signaux sur les cibles, c'est la connexion de mesure qui est en cause.\n")

    o.append("## 3. Synthèse par plateforme et par point de mesure\n")
    o.append("Classement **descriptif** : il dit ce que montrent les mesures, pas pourquoi.\n")
    o.append("| plateforme | " + " | ".join(ctrl) + " |")
    o.append("|---|" + "---|" * len(ctrl))
    plats = sorted({e["platform"] for e in cibles} | {x["platform"] for ts in tours.values() for t in ts.values()
                                                      for x in t["lignes"] if x["kind"] == "cible"},
                   key=lambda p: (ORDRE_PLATEFORMES.index(p) if p in ORDRE_PLATEFORMES else 99, p))
    for p in plats:
        cells = []
        for v in ctrl:
            es = [e for e in cibles if e["platform"] == p and e["vantage"] == v]
            forts = [e for e in es if e["repete"] and e["temoins_ok"] and e["gravite"] == SIGNATURE]
            echecs = [e for e in es if e["repete"] and e["temoins_ok"] and e["gravite"] == ECHEC]
            if forts:
                cells.append(f"**motif répété compatible avec un blocage** ({len(forts)} épisode(s)) : à examiner")
            elif echecs:
                cells.append(f"échecs répétés sans signature ({len(echecs)})")
            elif es:
                cells.append(f"signaux isolés ({len(es)}), non concluants")
            else:
                cells.append("aucun signal")
        o.append(f"| {NOMS.get(p, p)} | " + " | ".join(cells) + " |")
    o.append("")
    o.append("Critères d'un « motif répété compatible avec un blocage » : signature de blocage (réponse DNS du FAI "
             "NXDOMAIN, adresse privée ou REFUSED alors que le DoH répond ; connexion réinitialisée ; certificat invalide), "
             "sur au moins 3 tours consécutifs, pendant que les témoins répondent. Il faut ensuite vérifier, à la main, "
             "si le même signal apparaît sur un autre point de mesure ou dans OONI.\n")

    o.append("## 4. Changements d'émetteur de certificat\n")
    if not chg:
        o.append("Aucun.\n")
    else:
        o.append("Les CDN changent souvent de certificat. Un changement vu aussi depuis un autre point de mesure est "
                 "probablement une rotation normale.\n")
        o.append("| point | hôte | heure | avant | après | vu ailleurs (±2 h) |")
        o.append("|---|---|---|---|---|---|")
        for c in chg[:200]:
            o.append(f"| {c['vantage']} | {c['host']} | {fmt(c['t'])} | {c['avant']} | {c['apres']} | {c['vu_ailleurs']} |")
        o.append("")

    o.append("## 5. Codes HTTP par point de mesure (pour information)\n")
    o.append("Un 403, un 429 ou une redirection vers la page de connexion est la réponse normale d'une plateforme à un "
             "script. Ce n'est pas un blocage réseau. Seul un changement brutal, absent des autres points de mesure, mérite "
             "d'être regardé.\n")
    o.append("| point | hôte | codes (nombre) |")
    o.append("|---|---|---|")
    for (v, h), cnt in sorted(statuts_http.items()):
        o.append(f"| {v} | {h} | {', '.join(f'{k or 'aucun'} ({n})' for k, n in cnt.most_common())} |")
    o.append("")

    o.append("## 6. Événements de référence\n")
    o.append("| début | fin | événement | statut | source |")
    o.append("|---|---|---|---|---|")
    for e in evs:
        o.append(f"| {e['debut']} | {e.get('fin') or ''} | {e['libelle']} | {e['statut']} | {e['source']} |")
    o.append("")
    return "\n".join(o)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", nargs="+", help="fichiers mesures_*.csv (jokers acceptés)")
    ap.add_argument("--evenements", default="evenements.csv")
    ap.add_argument("--out", default="rapport")
    ap.add_argument("--debut", help="début de la frise, heure de Paris (AAAA-MM-JJTHH:MM)")
    ap.add_argument("--fin", help="fin de la frise, heure de Paris")
    a = ap.parse_args()
    fichiers = sorted({f for motif in a.csv for f in (glob.glob(motif) or [motif])})
    lignes, metas = lire(fichiers)
    if not lignes:
        sys.exit("Aucune mesure lue.")
    tours = construire(lignes, metas)
    ctrl = controles(tours, metas)
    eps = episodes(tours)
    chg = changements_issuer(tours)
    evs = lire_evenements(a.evenements)
    statuts_http = collections.defaultdict(collections.Counter)
    for r in lignes:
        if r.get("role") == "web":
            statuts_http[(r["vantage"], r["host"])][r["http_status"] or (r["http_err"] and "err:" + r["http_err"]) or ""] += 1

    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "analyse.md"), "w", encoding="utf-8") as f:
        f.write(rapport(fichiers, tours, ctrl, eps, chg, evs, statuts_http))
    champs = ["vantage", "fai", "platform", "kind", "host", "signal", "gravite", "debut_paris", "fin_paris", "n",
              "repete", "temoins_ok", "autres_points", "exemple"]
    with open(os.path.join(a.out, "episodes.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=champs, extrasaction="ignore")
        w.writeheader()
        for e in eps:
            w.writerow({**e, "debut_paris": paris(e["debut"]).isoformat(), "fin_paris": paris(e["fin"]).isoformat()})

    debut = paris_vers_utc(dt.datetime.fromisoformat(a.debut)) if a.debut else min(c["debut"] for c in ctrl.values())
    fin = paris_vers_utc(dt.datetime.fromisoformat(a.fin)) if a.fin else max(c["fin"] for c in ctrl.values()) + dt.timedelta(minutes=10)
    g = grille(tours)
    svg = frise_svg(g, evs, debut, fin)
    with open(os.path.join(a.out, "frise.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    hors = [e for e in evs if (e["_f"] or e["_d"]) < debut or e["_d"] > fin]
    with open(os.path.join(a.out, "frise.html"), "w", encoding="utf-8") as f:
        f.write(frise_html(svg, "Accessibilité des réseaux sociaux : mesures", hors))
    n_forts = sum(1 for e in eps if e["kind"] == "cible" and e["repete"] and e["temoins_ok"] and e["gravite"] == SIGNATURE)
    print(f"{len(lignes)} mesures, {sum(len(t) for t in tours.values())} tours, {len(eps)} épisodes "
          f"({n_forts} motif(s) répété(s) compatible(s) avec un blocage). Rapport : {a.out}/analyse.md, {a.out}/frise.html",
          file=sys.stderr)


if __name__ == "__main__":
    main()
