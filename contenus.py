#!/usr/bin/env python3
"""
contenus.py — suivi de l'accessibilité d'une liste de posts publics (X,
TikTok, Instagram, YouTube), depuis plusieurs points de mesure.

Sert deux tests :
  T1  « retenu en France » : un post visible depuis l'étranger (VPS) mais pas
      depuis la France, ou affiché avec une mention de demande légale.
  T2  « disparitions » : un post visible au début qui ne l'est plus, avec le
      motif affiché par la plateforme (supprimé par l'auteur, retiré pour
      violation des règles, compte suspendu, retenu dans le pays…).

Méthodes : uniquement des accès publics, sans connexion à un compte.
  X          oEmbed (publish.twitter.com) + widget d'intégration (syndication)
  TikTok     oEmbed + page publique de la vidéo
  Instagram  page d'intégration publique (/embed/) — expérimental
  YouTube    oEmbed + page publique (statut de lecture)
Une requête toutes les 2 à 5 secondes, un passage toutes les 6 h par défaut.

Bibliothèque standard uniquement, Python >= 3.9.

  python3 contenus.py --corpus corpus.csv --vantage fixe --test
  python3 contenus.py --corpus corpus.csv --vantage vps --interval 10800   # en continu (VPS)
  python3 contenus.py --corpus corpus.csv --vantage fixe --une-fois         # un passage (Mac)
"""
import argparse
import csv
import datetime as dt
import gzip
import json
import math
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

VERSION = "1.3"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")
COLONNES = ["ts_utc", "round_id", "tool_version", "vantage", "loc", "id", "plateforme", "categorie",
            "methode", "http_status", "etat", "mention_legale", "raison_brute", "ms", "url"]

# Vocabulaire fermé des états (voir README)
ETATS = ["visible", "supprime_auteur", "retire_regles", "compte_suspendu", "retenu_pays", "prive",
         "indisponible", "anti_robot", "erreur_reseau", "non_reconnu"]

# Motifs de reconnaissance (anglais et français), du plus spécifique au plus général
MOTIFS = [
    ("retenu_pays", r"withheld|not available in your country|in your country|dans votre pays|"
                    r"retenu|legal demand|legal complaint|government|demande l[ée]gale|réglementation locale|"
                    r"local law|restricted in your region|n'est pas disponible dans votre r[ée]gion"),
    ("compte_suspendu", r"suspended|suspendu|terminated|account .* (?:banned|removed)|compte .* (?:banni|supprim)"),
    ("retire_regles", r"violat|enfrei|community guidelines|r[èe]gles de la communaut|terms of service|"
                      r"removed by (?:youtube|tiktok)|x rules|policy|politique"),
    ("supprime_auteur", r"deleted by the (?:post )?author|removed by the uploader|supprim[ée] par (?:son|l')auteur|"
                        r"no longer available because the youtube account|deleted"),
    ("prive", r"private|privé|protected|protégé|only visible|sign in to confirm your age|age-restricted"),
]
LEGAL = re.compile(r"legal demand|legal complaint|government|demande l[ée]gale|plainte|local law|"
                   r"réglementation locale|court order|décision de justice", re.I)


def classer(texte):
    t = (texte or "").lower()
    for etat, motif in MOTIFS:
        if re.search(motif, t):
            return etat
    return "indisponible"


# ------------------------------------------------------------------ HTTP
def get(url, timeout=20, accept="*/*"):
    """Renvoie (status, texte, url_finale, ms). Ne lève pas."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept,
                                               "Accept-Language": "en-US,en;q=0.8,fr;q=0.6",
                                               "Accept-Encoding": "gzip"})
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read(3_000_000)
            if r.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            return r.status, raw.decode("utf-8", "replace"), r.geturl(), int((time.monotonic() - t0) * 1000)
    except urllib.error.HTTPError as e:
        try:
            raw = e.read(500_000)
            if e.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            body = raw.decode("utf-8", "replace")
        except Exception:
            body = ""
        return e.code, body, url, int((time.monotonic() - t0) * 1000)
    except Exception as e:
        return 0, f"{type(e).__name__}: {e}", url, int((time.monotonic() - t0) * 1000)


def court(s, n=200):
    return re.sub(r"\s+", " ", s or "")[:n]


def res(methode, status, etat, raison, ms, legal=None):
    return {"methode": methode, "http_status": status, "etat": etat, "raison_brute": court(raison),
            "ms": ms, "mention_legale": "oui" if (legal if legal is not None else LEGAL.search(raison or "")) else ""}


def reseau_ou_robot(methode, st, body, ms, final=""):
    if st == 0:
        return res(methode, st, "erreur_reseau", body, ms)
    if st == 429 or "/accounts/login" in (final or "") or re.search(
            r"captcha|verify you are human|unusual traffic|confirm you(?:'|’)re not a bot", (body or "")[:20000], re.I):
        return res(methode, st, "anti_robot", "page anti-robot ou connexion exigée " + court(final, 80), ms)
    return None


# ------------------------------------------------------------------ X
def _js_base36(x, frac_digits=12):
    """Approximation de Number.prototype.toString(36) de JavaScript."""
    chiffres = "0123456789abcdefghijklmnopqrstuvwxyz"
    ent, frac = int(x), x - int(x)
    s = ""
    while ent:
        s = chiffres[ent % 36] + s
        ent //= 36
    s = s or "0"
    if frac:
        s += "."
        for _ in range(frac_digits):
            frac *= 36
            d = int(frac)
            s += chiffres[d]
            frac -= d
            if frac == 0:
                break
    return s


def x_token(tid):
    return re.sub(r"(0+|\.)", "", _js_base36((int(tid) / 1e15) * math.pi))


def verifier_x(url):
    m = re.search(r"/status(?:es)?/(\d+)", url)
    if not m:
        return [res("parse", "", "non_reconnu", "identifiant de post introuvable dans l'URL", 0)]
    tid = m.group(1)
    out = []
    # 1. oEmbed officiel
    st, body, _, ms = get("https://publish.twitter.com/oembed?" + urllib.parse.urlencode(
        {"url": f"https://twitter.com/i/status/{tid}", "omit_script": "true", "dnt": "true", "lang": "en"}))
    r = reseau_ou_robot("oembed", st, body, ms)
    if r:
        out.append(r)
    elif st == 200 and '"html"' in body:
        out.append(res("oembed", st, "visible", "", ms))
    else:
        out.append(res("oembed", st, "indisponible" if st in (403, 404) else "non_reconnu", body, ms))
    # 2. widget d'intégration : donne le motif (« tombstone ») quand le post n'est plus visible
    for token in (x_token(tid), "a"):
        st, body, _, ms = get("https://cdn.syndication.twimg.com/tweet-result?" + urllib.parse.urlencode(
            {"id": tid, "lang": "en", "token": token}), accept="application/json")
        if st not in (400, 401, 403) or token == "a":
            break
    r = reseau_ou_robot("syndication", st, body, ms)
    if r:
        out.append(r)
        return out
    try:
        d = json.loads(body) if body.strip().startswith("{") else {}
    except ValueError:
        d = {}
    typ = d.get("__typename", "")
    pays = d.get("withheld_in_countries") or d.get("withheld_scope") or ""
    if typ == "Tweet" and not pays:
        out.append(res("syndication", st, "visible", "", ms))
    elif typ == "Tweet" and pays:
        out.append(res("syndication", st, "retenu_pays", f"withheld_in_countries={pays}", ms, legal=True))
    elif typ == "TweetTombstone" or "tombstone" in d:
        txt = json.dumps(d.get("tombstone", d), ensure_ascii=False)
        texte = (d.get("tombstone") or {}).get("text", {}).get("text", "") or txt
        out.append(res("syndication", st, classer(texte), texte, ms))
    elif st == 404:
        out.append(res("syndication", st, "indisponible", "404 sans motif", ms))
    else:
        out.append(res("syndication", st, "non_reconnu", body, ms))
    return out


# ------------------------------------------------------------------ TikTok
def verifier_tiktok(url):
    out = []
    st, body, _, ms = get("https://www.tiktok.com/oembed?" + urllib.parse.urlencode({"url": url}))
    r = reseau_ou_robot("oembed", st, body, ms)
    if r:
        out.append(r)
    elif st == 200 and '"html"' in body:
        out.append(res("oembed", st, "visible", "", ms))
    else:
        out.append(res("oembed", st, "indisponible" if st in (400, 403, 404) else "non_reconnu", body, ms))
    # page publique : JSON embarqué avec statusCode / statusMsg
    st, body, final, ms = get(url, accept="text/html")
    r = reseau_ou_robot("page", st, body, ms, final)
    if r:
        out.append(r)
        return out
    m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', body, re.S)
    if not m:
        out.append(res("page", st, "non_reconnu", "données de page absentes (" + final + ")", ms))
        return out
    try:
        d = json.loads(m.group(1))["__DEFAULT_SCOPE__"].get("webapp.video-detail", {})
    except (ValueError, KeyError):
        out.append(res("page", st, "non_reconnu", "JSON illisible", ms))
        return out
    code, msg = d.get("statusCode"), d.get("statusMsg", "")
    item = (d.get("itemInfo") or {}).get("itemStruct")
    if code == 0 and item:
        r = res("page", st, "visible", "", ms)
        r["_metriques"] = metriques_tiktok(item)  # T8/T9 : écrit dans un fichier séparé
        out.append(r)
    else:
        texte = f"statusCode={code} statusMsg={msg}"
        out.append(res("page", st, classer(msg) if msg else "indisponible", texte, ms))
    return out


COLONNES_TT = ["ts_utc", "round_id", "vantage", "loc", "id", "categorie", "vues", "likes", "commentaires",
               "partages", "reviewed", "display_penalty_type", "display_policy", "display_ui_type", "video_status",
               "ec_global_verdict", "conclu_refine_reason", "is_prohibited", "is_reviewing", "item_control"]


def metriques_tiktok(item):
    """Compteurs et indicateurs internes NON DOCUMENTÉS d'une vidéo TikTok (enregistrés tels quels)."""
    stt = item.get("stats") or {}
    st2 = item.get("statsV2") or {}
    pc = item.get("penaltyContext") or {}
    def n(k):
        return stt.get(k) if stt.get(k) is not None else st2.get(k, "")
    return {"vues": n("playCount"), "likes": n("diggCount"), "commentaires": n("commentCount"),
            "partages": n("shareCount"),
            **{k: pc.get(k, "") for k in ("reviewed", "display_penalty_type", "display_policy", "display_ui_type",
                                          "video_status", "ec_global_verdict", "conclu_refine_reason")},
            "is_prohibited": item.get("isProhibited", ""), "is_reviewing": item.get("isReviewing", ""),
            "item_control": json.dumps(item.get("item_control") or {}, sort_keys=True, separators=(",", ":"))}


# ------------------------------------------------------------------ Instagram
def verifier_instagram(url):
    m = re.search(r"/(?:p|reel|reels|tv)/([A-Za-z0-9_-]+)", url)
    if not m:
        return [res("parse", "", "non_reconnu", "code du post introuvable dans l'URL", 0)]
    st, body, final, ms = get(f"https://www.instagram.com/p/{m.group(1)}/embed/captioned/", accept="text/html")
    r = reseau_ou_robot("embed", st, body, ms, final)
    if r:
        return [r]
    if st == 200 and re.search(r'class="(?:EmbeddedMedia|Caption|EmbeddedMediaImage)', body):
        return [res("embed", st, "visible", "", ms)]
    m2 = re.search(r"(not available[^<]{0,200}|n'est pas disponible[^<]{0,200}|isn't available[^<]{0,200})", body, re.I)
    if m2 or st == 404:
        texte = m2.group(1) if m2 else "404"
        return [res("embed", st, classer(texte), texte, ms)]
    return [res("embed", st, "non_reconnu", "page d'intégration sans marqueur connu (" + final + ")", ms)]


# ------------------------------------------------------------------ YouTube
def verifier_youtube(url):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})", url)
    if not m:
        return [res("parse", "", "non_reconnu", "identifiant vidéo introuvable", 0)]
    vid = m.group(1)
    out = []
    st, body, _, ms = get("https://www.youtube.com/oembed?" + urllib.parse.urlencode(
        {"url": f"https://www.youtube.com/watch?v={vid}", "format": "json"}))
    r = reseau_ou_robot("oembed", st, body, ms)
    if r:
        out.append(r)
    elif st == 200:
        out.append(res("oembed", st, "visible", "", ms))
    else:
        out.append(res("oembed", st, "prive" if st == 401 else "indisponible", body, ms))
    st, body, _, ms = get(f"https://www.youtube.com/watch?v={vid}&hl=en", accept="text/html")
    r = reseau_ou_robot("page", st, body, ms)
    if r:
        out.append(r)
        return out
    m = re.search(r'"playabilityStatus":\{"status":"([A-Z_]+)"(.{0,1500})', body)
    if not m:
        out.append(res("page", st, "non_reconnu", "statut de lecture absent", ms))
        return out
    statut, reste = m.group(1), m.group(2)
    raison = re.search(r'"reason":(?:"([^"]*)"|\{"simpleText":"([^"]*)")', reste)
    raison = (raison.group(1) or raison.group(2)) if raison else ""
    sous = re.search(r'"subreason":\{"(?:simpleText|runs)":(?:"([^"]*)"|\[\{"text":"([^"]*)")', reste)
    raison = (raison + " | " + ((sous.group(1) or sous.group(2)) if sous else "")).strip(" |")
    if statut == "OK":
        out.append(res("page", st, "visible", "", ms))
    elif statut == "LOGIN_REQUIRED":
        out.append(res("page", st, "prive" if "private" in raison.lower() else "anti_robot"
                       if "bot" in raison.lower() else "prive", f"{statut}: {raison}", ms))
    else:
        out.append(res("page", st, classer(raison), f"{statut}: {raison}", ms))
    return out


VERIFS = {"x": verifier_x, "twitter": verifier_x, "tiktok": verifier_tiktok,
          "instagram": verifier_instagram, "youtube": verifier_youtube}


# ------------------------------------------------------------------ boucle
def lire_corpus(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        lignes = [r for r in csv.DictReader(f) if (r.get("url") or "").startswith("http")]
    ids = set()
    for r in lignes:
        r["plateforme"] = r["plateforme"].strip().lower()
        if r["id"] in ids:
            sys.exit(f"identifiant en double dans le corpus : {r['id']}")
        ids.add(r["id"])
        if r["plateforme"] not in VERIFS:
            sys.exit(f"plateforme inconnue pour {r['id']} : {r['plateforme']}")
    return lignes


def localisation():
    st, body, _, _ = get("https://1.1.1.1/cdn-cgi/trace", timeout=10)
    kv = dict(l.split("=", 1) for l in body.splitlines() if "=" in l)
    return kv.get("loc", "?")


def un_passage(corpus, a, ecrire=True):
    rid = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    loc = localisation()
    ordre = list(corpus)
    random.shuffle(ordre)
    lignes = []
    f = w = None
    ftt = wtt = None
    if ecrire:  # écriture au fil de l'eau : une coupure ne fait perdre que le post en cours
        neuf = not os.path.exists(a.out) or os.path.getsize(a.out) == 0
        f = open(a.out, "a", newline="", encoding="utf-8")
        w = csv.DictWriter(f, fieldnames=COLONNES)
        if neuf:
            w.writeheader()
            f.flush()
        out_tt = os.path.join(os.path.dirname(a.out), "tiktok_metriques_" + a.vantage + ".csv")
        neuf_tt = not os.path.exists(out_tt) or os.path.getsize(out_tt) == 0
        ftt = open(out_tt, "a", newline="", encoding="utf-8")
        wtt = csv.DictWriter(ftt, fieldnames=COLONNES_TT)
        if neuf_tt:
            wtt.writeheader()
    try:
        for i, p in enumerate(ordre):
            try:
                resultats = VERIFS[p["plateforme"]](p["url"])
            except Exception as e:  # ne jamais perdre un passage
                resultats = [res("crash", "", "non_reconnu", repr(e), 0)]
            ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            metriques = [r.pop("_metriques") for r in resultats if "_metriques" in r]
            nouvelles = [{"ts_utc": ts, "round_id": rid, "tool_version": VERSION, "vantage": a.vantage, "loc": loc,
                          "id": p["id"], "plateforme": p["plateforme"], "categorie": p.get("categorie", ""),
                          "url": p["url"], **r} for r in resultats]
            lignes.extend(nouvelles)
            for m in metriques:
                m.update(ts_utc=ts, round_id=rid, vantage=a.vantage, loc=loc, id=p["id"],
                         categorie=p.get("categorie", ""))
                if a.test:
                    print(f"  [T8/T9] {p['id']} vues={m['vues']} reviewed={m['reviewed']} "
                          f"display_penalty_type={m['display_penalty_type']} video_status={m['video_status']}",
                          file=sys.stderr)
                if wtt:
                    wtt.writerow(m)
                    ftt.flush()
            if w:
                w.writerows(nouvelles)
                f.flush()
            if not a.test:
                print(f"  {i + 1}/{len(ordre)} {p['id']} {p['plateforme']}: "
                      + ", ".join(f"{r['methode']}={r['etat']}" for r in resultats), file=sys.stderr)
            time.sleep(random.uniform(2, 5))
    finally:
        if f:
            f.close()
        if ftt:
            ftt.close()
    return loc, lignes


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus", default="corpus.csv")
    ap.add_argument("--vantage", required=True, help="fixe, vps, 4g…")
    ap.add_argument("--out", help="défaut : contenus_<vantage>.csv")
    ap.add_argument("--interval", type=int, default=21600, help="secondes entre deux passages (défaut 6 h)")
    ap.add_argument("--test", action="store_true",
                    help="diagnostic : 2 posts par plateforme, affichage détaillé, rien n'est écrit")
    ap.add_argument("--une-fois", action="store_true",
                    help="un seul passage complet, écrit dans le CSV, puis s'arrête (point de mesure intermittent)")
    a = ap.parse_args()
    a.out = a.out or f"contenus_{a.vantage}.csv"
    corpus = lire_corpus(a.corpus)
    print(f"contenus v{VERSION} | point={a.vantage} | {len(corpus)} posts | sortie={a.out}", file=sys.stderr)

    if a.test:
        par = {}
        for p in corpus:
            par.setdefault(p["plateforme"], [])
            if len(par[p["plateforme"]]) < 2:
                par[p["plateforme"]].append(p)
        echantillon = [p for v in par.values() for p in v]
        loc, lignes = un_passage(echantillon, a, ecrire=False)
        print(f"\nLocalisation vue par Cloudflare : {loc}\n")
        print(f"{'id':6} {'plateforme':10} {'méthode':12} {'HTTP':5} {'état':16} {'légal':6} raison")
        for l in lignes:
            print(f"{l['id']:6} {l['plateforme']:10} {l['methode']:12} {str(l['http_status']):5} {l['etat']:16} "
                  f"{l['mention_legale']:6} {l['raison_brute'][:90]}")
        print("\nÀ vérifier : chaque plateforme doit avoir au moins une méthode en « visible » pour un post "
              "que tu vois dans ton navigateur. « anti_robot » ou « non_reconnu » partout = méthode inopérante.")
        return
    while True:
        t0 = time.time()
        print(f"{dt.datetime.now():%Y-%m-%d %H:%M} passage sur {len(corpus)} posts…", file=sys.stderr)
        loc, lignes = un_passage(corpus, a)
        if a.une_fois:
            print(f"terminé (loc={loc}, {len(lignes)} lignes). Passage unique : arrêt.", file=sys.stderr)
            return
        print(f"terminé (loc={loc}, {len(lignes)} lignes). Prochain passage dans {a.interval // 3600} h.", file=sys.stderr)
        time.sleep(max(60, a.interval * random.uniform(0.95, 1.05) - (time.time() - t0)))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\narrêt.", file=sys.stderr)
