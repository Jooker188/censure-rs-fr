#!/usr/bin/env python3
"""
importer.py — transforme des exports Zeeschuimer (.ndjson) en :

  contenus/posts.csv        une ligne par post, PSEUDONYMISÉE (local, jamais publié)
  contenus/corpus.csv       la liste suivie par contenus.py
  contenus/comptes_t6.csv   la liste de comptes à vérifier pour T6/T7 (local, jamais publié)
  rapport/collecte.md       chiffres agrégés de la collecte (publiable)

Catégorie de chaque post : déduite de la recherche pendant laquelle il a été
capturé (Zeeschuimer garde l'adresse de l'onglet). Règles par défaut :
  revendication  la recherche contient censure, shadowban, suspendu, supprimé, coupé…
  temoin         la recherche contient météo, ligue 1…
  mouvement      tout le reste
Les posts de ajouts_manuels.txt sont toujours inclus (note : revendication,
a_verifier ou mouvement).

Vie privée :
  - le pseudo de l'auteur est remplacé par un code HMAC (clé locale aléatoire,
    contenus/.cle_pseudonyme) ; seuls les comptes listés dans
    contenus/comptes_publics.txt (médias, organisations, personnalités) restent en clair ;
  - le texte n'est conservé que dans posts.csv (local) pour le tri du bruit et
    le calcul des hashtags ; rien de nominatif n'est écrit dans rapport/.

Plateformes : X (validé sur un export réel), TikTok et Instagram (à valider sur
un premier export).

  python3 importer.py exports/*.ndjson --manuels contenus/ajouts_manuels.txt
"""
import argparse
import collections
import csv
import datetime as dt
import glob
import hashlib
import hmac
import json
import os
import re
import secrets
import statistics
import sys
import urllib.parse

DOSSIER = "contenus"
REGLES_CATEGORIE = [
    ("revendication", r"censur|shadow|suspendu|\bbloqu[ée]e?s?\b|supprim|\bcoup[ée]e?s?\b|coupure|ne marche plus"),
    ("temoin", r"m[ée]t[ée]o|ligue ?1|recette|\bfoot\b"),
]
BRUIT = {
    "bruit_1961": re.compile(r"1961|alg[ée]rien|massacre|papon|\bseine\b|harki", re.I),
    "rappel_2018": re.compile(r"\b2018\b|\b2019\b", re.I),
}
APPEL = re.compile(r"\bdemain\b|\bsamedi\b|rdv|rendez[- ]vous|\brejoign|\bon se retrouve|\btous [àa]\b|\bappel\b", re.I)
REVENDICATION_TXT = re.compile(r"censur|shadow ?ban|suspendu|supprim|\bbloqu[ée]e?s?\b|invisibilis|d[ée]class", re.I)
DEBUT_ACTE_IV = dt.datetime(2026, 11, 5)


# ------------------------------------------------------------------ outils
def cle_pseudo():
    p = os.path.join(DOSSIER, ".cle_pseudonyme")
    if not os.path.exists(p):
        os.makedirs(DOSSIER, exist_ok=True)
        with open(p, "w") as f:
            f.write(secrets.token_hex(32))
        os.chmod(p, 0o600)
    return open(p).read().strip().encode()


def pseudo(cle, plateforme, user_id):
    return "u_" + hmac.new(cle, f"{plateforme}:{user_id}".encode(), hashlib.sha256).hexdigest()[:12]


def comptes_publics():
    p = os.path.join(DOSSIER, "comptes_publics.txt")
    if not os.path.exists(p):
        return set()
    return {l.strip().lstrip("@").lower() for l in open(p, encoding="utf-8") if l.strip() and not l.startswith("#")}


def categorie_recherche(q):
    for cat, motif in REGLES_CATEGORIE:
        if re.search(motif, q or "", re.I):
            return cat
    return "mouvement"


def requete_de(url):
    qs = urllib.parse.parse_qs(urllib.parse.urlparse(url or "").query)
    q = (qs.get("q") or qs.get("keyword") or [""])[0]
    if not q:
        m = re.search(r"/(?:tag|tags)/([^/?#]+)", url or "")
        q = "#" + urllib.parse.unquote(m.group(1)) if m else ""
    return q


def contexte_capture(url):
    """search / profil / autre, et le compte visé pour un profil."""
    p = urllib.parse.urlparse(url or "")
    if "/search" in p.path or "/tag/" in p.path or "/explore/" in p.path:
        return "recherche", ""
    seg = [s for s in p.path.split("/") if s]
    if len(seg) == 1 and seg[0] not in ("home", "explore", "notifications", "i"):
        return "profil", seg[0].lstrip("@").lower()
    return "autre", ""


def to_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return ""


# ------------------------------------------------------------------ parseurs
def parse_x(item):
    d = item["data"]
    if d.get("__typename") == "TweetWithVisibilityResults":
        d = d.get("tweet", d)
    leg = d.get("legacy") or {}
    u = ((d.get("core") or {}).get("user_results") or {}).get("result") or {}
    if u.get("__typename") == "UserUnavailable" or not leg:
        return None
    ucore = u.get("core") or {}
    rel = u.get("relationship_counts") or {}
    ent = leg.get("entities") or {}
    texte = ((d.get("note_tweet") or {}).get("note_tweet_results", {}).get("result", {}).get("text")
             or leg.get("full_text", ""))
    try:
        date = dt.datetime.strptime(leg["created_at"], "%a %b %d %H:%M:%S %z %Y").astimezone(dt.timezone.utc).replace(tzinfo=None)
    except (KeyError, ValueError):
        date = None
    return {
        "post_id": d.get("rest_id") or leg.get("id_str"), "plateforme": "x",
        "user_id": u.get("rest_id") or leg.get("user_id_str"), "handle": (ucore.get("screen_name") or "").lower(),
        "abonnes": to_int(rel.get("followers") or (u.get("legacy") or {}).get("followers_count")),
        "verifie": "oui" if u.get("is_blue_verified") or (u.get("verification") or {}).get("verified") else "",
        "date": date, "texte": texte, "lang": leg.get("lang", ""),
        "vues": to_int((d.get("views") or {}).get("count")), "likes": to_int(leg.get("favorite_count")),
        "partages": to_int(leg.get("retweet_count")), "reponses": to_int(leg.get("reply_count")),
        "citations": to_int(leg.get("quote_count")),
        "est_reponse": "oui" if leg.get("in_reply_to_status_id_str") else "",
        "est_repost": "oui" if leg.get("retweeted_status_result") or texte.startswith("RT @") else "",
        "hashtags": " ".join(sorted({h["text"].lower() for h in ent.get("hashtags", [])})),
        "media": "oui" if (leg.get("extended_entities") or {}).get("media") else "",
        "sensible": "oui" if leg.get("possibly_sensitive") else "",
        "url": f"https://x.com/i/status/{d.get('rest_id') or leg.get('id_str')}",
    }


def parse_tiktok(item):  # structure itemStruct de TikTok — à valider sur un export réel
    d = item["data"]
    a = d.get("author") or {}
    st = d.get("stats") or d.get("statsV2") or {}
    ast = d.get("authorStats") or {}
    texte = d.get("desc", "")
    tags = {c.get("title", "").lower() for c in d.get("challenges") or []} | \
           {t.get("hashtagName", "").lower() for t in d.get("textExtra") or [] if t.get("hashtagName")}
    try:
        date = dt.datetime.fromtimestamp(int(d.get("createTime")), dt.timezone.utc).replace(tzinfo=None)
    except (TypeError, ValueError):
        date = None
    handle = a.get("uniqueId", "") if isinstance(a, dict) else str(a)
    return {
        "post_id": d.get("id"), "plateforme": "tiktok", "user_id": (a.get("id") if isinstance(a, dict) else handle),
        "handle": handle.lower(), "abonnes": to_int(ast.get("followerCount")),
        "verifie": "oui" if isinstance(a, dict) and a.get("verified") else "", "date": date, "texte": texte,
        "lang": d.get("textLanguage", ""), "vues": to_int(st.get("playCount")), "likes": to_int(st.get("diggCount")),
        "partages": to_int(st.get("shareCount")), "reponses": to_int(st.get("commentCount")), "citations": "",
        "est_reponse": "", "est_repost": "", "hashtags": " ".join(sorted(t for t in tags if t)),
        "media": "oui", "sensible": "",
        "url": f"https://www.tiktok.com/@{handle}/video/{d.get('id')}",
    }


def parse_instagram(item):  # structure « media » d'Instagram — à valider sur un export réel
    d = item["data"]
    u = d.get("user") or d.get("owner") or {}
    cap = d.get("caption") or {}
    texte = cap.get("text", "") if isinstance(cap, dict) else str(cap)
    try:
        date = dt.datetime.fromtimestamp(int(d.get("taken_at")), dt.timezone.utc).replace(tzinfo=None)
    except (TypeError, ValueError):
        date = None
    return {
        "post_id": d.get("pk") or d.get("id"), "plateforme": "instagram", "user_id": u.get("pk") or u.get("id"),
        "handle": (u.get("username") or "").lower(), "abonnes": "", "verifie": "oui" if u.get("is_verified") else "",
        "date": date, "texte": texte, "lang": "",
        "vues": to_int(d.get("play_count") or d.get("view_count") or d.get("ig_play_count")),
        "likes": to_int(d.get("like_count")), "partages": "", "reponses": to_int(d.get("comment_count")),
        "citations": "", "est_reponse": "", "est_repost": "",
        "hashtags": " ".join(sorted({h.lower() for h in re.findall(r"#(\w+)", texte)})),
        "media": "oui", "sensible": "", "url": f"https://www.instagram.com/p/{d.get('code')}/",
    }


PARSEURS = {"twitter.com": parse_x, "x.com": parse_x, "tiktok.com": parse_tiktok, "instagram.com": parse_instagram}


# ------------------------------------------------------------------ import
def importer(fichiers, cle, publics):
    posts = {}
    captures = []  # (contexte, compte_visé, post) pour T6/T7
    erreurs = collections.Counter()
    for f in fichiers:
        for ligne in open(f, encoding="utf-8"):
            if not ligne.strip():
                continue
            try:
                item = json.loads(ligne)
                p = PARSEURS[item["source_platform"]](item)
            except Exception as e:
                erreurs[type(e).__name__] += 1
                continue
            if not p or not p["post_id"]:
                erreurs["post_illisible"] += 1
                continue
            src = item.get("source_platform_url", "")
            ctx, cible = contexte_capture(src)
            q = requete_de(src)
            p["recherche"] = q if ctx == "recherche" else ""
            p["capture"] = dt.datetime.fromtimestamp(item.get("timestamp_collected", 0) / 1000, dt.timezone.utc).replace(tzinfo=None)
            captures.append((ctx, cible, q, p))
            if ctx != "recherche":
                continue
            cat = categorie_recherche(q)
            cle_p = (p["plateforme"], p["post_id"])
            if cle_p in posts:  # même post vu par plusieurs recherches
                posts[cle_p]["recherches"].add(q)
                if cat == "revendication":
                    posts[cle_p]["categorie"] = cat
                continue
            p["categorie"] = cat
            p["recherches"] = {q}
            posts[cle_p] = p
    for p in posts.values():
        p["auteur"] = p["handle"] if p["handle"] in publics else pseudo(cle, p["plateforme"], p["user_id"])
        p["type_compte"] = "public" if p["handle"] in publics else "particulier_ou_inconnu"
        for nom, rx in BRUIT.items():
            p[nom] = "oui" if rx.search(p["texte"] or "") else ""
        p["appel"] = "oui" if APPEL.search(p["texte"] or "") else ""
        p["affirme_censure"] = "oui" if REVENDICATION_TXT.search(p["texte"] or "") else ""
        p["periode"] = ("acte_IV" if p["date"] and p["date"] >= DEBUT_ACTE_IV else "acte_precedent") \
            if p["categorie"] != "temoin" else "temoin"
    return posts, captures, erreurs


def lire_manuels(path):
    out = []
    if path and os.path.exists(path):
        for l in open(path, encoding="utf-8"):
            l = l.strip()
            if not l or l.startswith("#"):
                continue
            parts = l.split()
            url, note = parts[0], (parts[1] if len(parts) > 1 else "mouvement")
            plat = "x" if re.search(r"(x|twitter)\.com/", url) else "tiktok" if "tiktok.com" in url else \
                "instagram" if "instagram.com" in url else "youtube" if "youtu" in url else ""
            m = re.search(r"/status/(\d+)|/video/(\d+)|/(?:p|reel)/([\w-]+)|(?:v=|youtu\.be/)([\w-]{11})", url)
            pid = next((g for g in m.groups() if g), "") if m else ""
            if plat and pid:
                out.append({"plateforme": plat, "post_id": pid, "url": url if plat != "x" else f"https://x.com/i/status/{pid}",
                            "note": note})
    return out


def ecrire(posts, manuels, a):
    os.makedirs(DOSSIER, exist_ok=True)
    champs = ["plateforme", "post_id", "categorie", "periode", "recherches", "date", "auteur", "type_compte",
              "abonnes", "verifie", "lang", "vues", "likes", "partages", "reponses", "citations", "est_reponse",
              "est_repost", "media", "sensible", "hashtags", "appel", "affirme_censure", "bruit_1961",
              "rappel_2018", "texte", "url"]
    with open(os.path.join(DOSSIER, "posts.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=champs, extrasaction="ignore")
        w.writeheader()
        for p in sorted(posts.values(), key=lambda p: (p["plateforme"], p["categorie"], str(p["date"]))):
            w.writerow({**p, "recherches": " | ".join(sorted(p["recherches"])),
                        "date": p["date"].strftime("%Y-%m-%dT%H:%M:%SZ") if p["date"] else ""})
    # corpus suivi par contenus.py : hors bruit 1961 évident, hors reposts
    corpus = []
    vus = set()
    for p in sorted(posts.values(), key=lambda p: (p["plateforme"], p["categorie"], p["post_id"])):
        if p["bruit_1961"] and p["categorie"] != "temoin" and "17octobre" in p["hashtags"] and "giletsjaunes" not in p["hashtags"]:
            continue
        if p["est_repost"]:
            continue
        cat = "temoin" if p["categorie"] == "temoin" else p["categorie"]
        corpus.append({"id": f"{p['plateforme'][0]}{len(corpus) + 1:04d}", "plateforme": p["plateforme"], "url": p["url"],
                       "categorie": cat, "periode": p["periode"], "type_compte": p["type_compte"],
                       "date_post": p["date"].strftime("%Y-%m-%d") if p["date"] else "", "note": "zeeschuimer"})
        vus.add((p["plateforme"], p["post_id"]))
    for m in manuels:
        if (m["plateforme"], m["post_id"]) in vus:
            for c in corpus:
                if c["url"].endswith(m["post_id"]) or m["post_id"] in c["url"]:
                    c["note"] = "manuel+" + m["note"]
                    if m["note"] in ("revendication", "a_verifier"):
                        c["categorie"] = "revendication"
            continue
        corpus.append({"id": f"m{len(corpus) + 1:04d}", "plateforme": m["plateforme"], "url": m["url"],
                       "categorie": "revendication" if m["note"] in ("revendication", "a_verifier") else "mouvement",
                       "periode": "", "type_compte": "", "date_post": "", "note": "manuel+" + m["note"]})
    with open(os.path.join(DOSSIER, "corpus.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "plateforme", "url", "categorie", "periode", "type_compte", "date_post", "note"])
        w.writeheader()
        w.writerows(corpus)
    return corpus


def comptes_t6(posts, a):
    """Liste de comptes à vérifier (T6/T7), locale. Tous les comptes « revendication »,
    puis un échantillon de comptes « mouvement » et « témoin » (les plus actifs d'abord)."""
    par = collections.defaultdict(lambda: {"n": 0, "cats": set()})
    for p in posts.values():
        if p["est_repost"]:
            continue
        c = par[(p["plateforme"], p["handle"], p["auteur"])]
        c["n"] += 1
        c["cats"].add(p["categorie"])
        c["abonnes"] = p["abonnes"]
    lignes = []
    for groupe, quota in (("revendication", a.comptes_revendication), ("mouvement", a.comptes_mouvement),
                          ("temoin", a.comptes_temoin)):
        cands = [(k, v) for k, v in par.items() if groupe in v["cats"]
                 and not any(l["handle"] == k[1] for l in lignes)]
        cands.sort(key=lambda kv: -kv[1]["n"])
        for (plat, handle, auteur), v in cands[:quota]:
            if plat != "x":
                continue
            lignes.append({"groupe": groupe, "plateforme": plat, "auteur": auteur, "handle": handle,
                           "abonnes": v["abonnes"], "posts_collectes": v["n"],
                           "profil": f"https://x.com/{handle}",
                           "recherche": "https://x.com/search?q=" + urllib.parse.quote(f"from:{handle}", safe="") + "&f=live",
                           "fait": ""})
    with open(os.path.join(DOSSIER, "comptes_t6.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()) if lignes else ["groupe"])
        w.writeheader()
        w.writerows(lignes)
    return lignes


def rapport(posts, corpus, comptes, erreurs, a):
    o = ["# Collecte de posts : chiffres agrégés\n",
         f"Généré le {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC par `importer.py`. "
         "Échantillon issu de recherches faites avec un compte réel (résultats personnalisés) : "
         "ce ne sont **pas** des comptages de tout ce qui a été publié.\n"]
    if erreurs:
        o.append(f"Éléments illisibles ignorés : {dict(erreurs)}\n")
    o.append("## Par réseau et par catégorie\n")
    o.append("| réseau | catégorie | posts | auteurs distincts | période des posts | médiane des vues | part de réponses | bruit « 1961 » | appels à se rassembler |")
    o.append("|---|---|---|---|---|---|---|---|---|")
    g = collections.defaultdict(list)
    for p in posts.values():
        g[(p["plateforme"], p["categorie"])].append(p)
    for (plat, cat), lst in sorted(g.items()):
        dates = [p["date"] for p in lst if p["date"]]
        vues = [p["vues"] for p in lst if isinstance(p["vues"], int)]
        o.append(f"| {plat} | {cat} | {len(lst)} | {len({p['auteur'] for p in lst})} | "
                 f"{min(dates):%d/%m} → {max(dates):%d/%m} | {int(statistics.median(vues)) if vues else '—'} | "
                 f"{sum(1 for p in lst if p['est_reponse']) * 100 // len(lst)} % | "
                 f"{sum(1 for p in lst if p['bruit_1961'])} | {sum(1 for p in lst if p['appel'])} |")
    o.append("")
    o.append("## Par recherche\n")
    o.append("| réseau | recherche | catégorie | posts |")
    o.append("|---|---|---|---|")
    pr = collections.Counter((p["plateforme"], q, p["categorie"]) for p in posts.values() for q in p["recherches"])
    for (plat, q, cat), n in sorted(pr.items()):
        o.append(f"| {plat} | `{q}` | {cat} | {n} |")
    o.append("")
    o.append("## Hashtags les plus fréquents (hors ceux recherchés)\n")
    for plat in sorted({p["plateforme"] for p in posts.values()}):
        for cat in ("mouvement", "revendication", "temoin"):
            lst = [p for p in posts.values() if p["plateforme"] == plat and p["categorie"] == cat]
            if not lst:
                continue
            cherches = {h.lower().lstrip("#") for p in lst for q in p["recherches"] for h in re.findall(r"#(\w+)", q)}
            c = collections.Counter(h for p in lst for h in p["hashtags"].split() if h not in cherches)
            o.append(f"- **{plat} / {cat}** : " + ", ".join(f"#{h} ({n})" for h, n in c.most_common(20)))
    o.append("")
    o.append("## Corpus suivi et comptes à vérifier\n")
    cc = collections.Counter((c["plateforme"], c["categorie"]) for c in corpus)
    o.append("Posts suivis par `contenus.py` (sans les reposts ni le bruit évident lié à 1961) : "
             + ", ".join(f"{p}/{c} : {n}" for (p, c), n in sorted(cc.items())) + ".")
    gc = collections.Counter(l["groupe"] for l in comptes)
    o.append(f"\nComptes à vérifier pour T6 et T7 : " + ", ".join(f"{k} : {v}" for k, v in gc.items())
             + ". La liste nominative reste locale (`contenus/comptes_t6.csv`).\n")
    os.makedirs("rapport", exist_ok=True)
    open(os.path.join("rapport", "collecte.md"), "w", encoding="utf-8").write("\n".join(o))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ndjson", nargs="+")
    ap.add_argument("--manuels", default=os.path.join(DOSSIER, "ajouts_manuels.txt"))
    ap.add_argument("--comptes-revendication", type=int, default=15)
    ap.add_argument("--comptes-mouvement", type=int, default=15)
    ap.add_argument("--comptes-temoin", type=int, default=10)
    a = ap.parse_args()
    fichiers = sorted({f for m in a.ndjson for f in (glob.glob(m) or [m])})
    cle = cle_pseudo()
    posts, captures, erreurs = importer(fichiers, cle, comptes_publics())
    if not posts:
        sys.exit("Aucun post issu d'une recherche dans ces fichiers.")
    corpus = ecrire(posts, lire_manuels(a.manuels), a)
    comptes = comptes_t6(posts, a)
    rapport(posts, corpus, comptes, erreurs, a)
    c = collections.Counter(p["categorie"] for p in posts.values())
    print(f"{len(posts)} posts uniques ({dict(c)}), corpus : {len(corpus)}, comptes T6/T7 : {len(comptes)}.\n"
          f"Écrits : contenus/posts.csv, contenus/corpus.csv, contenus/comptes_t6.csv, rapport/collecte.md", file=sys.stderr)
    if "temoin" not in c:
        print("ATTENTION : aucun post témoin. Fais les recherches témoins (XT1, XT2) avant de lancer le suivi.",
              file=sys.stderr)


if __name__ == "__main__":
    main()
