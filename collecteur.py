#!/usr/bin/env python3
"""
collecteur.py — automatise les sessions Zeeschuimer : un vrai navigateur
(Playwright, Chromium), avec TA session, ouvre une liste de pages, fait
défiler, et enregistre les posts que les plateformes envoient au navigateur.
Le fichier produit a le format des exports Zeeschuimer : importer.py et
comptes.py le lisent sans changement.

Plans :
  acte4   recherches de l'acte IV (X et TikTok), section « Collecte de l'acte IV »
          de contenus/RECHERCHES.md, plus les témoins
  t6      session T6/T7 : pour chaque compte X de contenus/comptes_t6.csv, le profil
          puis la recherche « from:compte » (onglet Récent) ; pour chaque créateur
          TikTok, le profil seulement (T7)

Première fois :
  pip install playwright
  python3 -m playwright install chromium
  python3 collecteur.py --connexion        # ouvre le navigateur : connecte-toi à X et TikTok, puis Entrée

Si la connexion échoue dans le navigateur piloté (X et TikTok repèrent souvent
Playwright au moment du login), reprendre la session de ton Firefox habituel,
déjà connecté, au lieu de te connecter :
  pip install minet
  python3 -m playwright install firefox
  python3 collecteur.py --plan t6 --cookies-firefox

Ensuite :
  python3 collecteur.py --plan acte4
  python3 collecteur.py --plan t6

⚠️ C'est de l'automatisation avec ton compte : contraire aux conditions
d'utilisation de X et TikTok, avec un risque de restriction du compte.
Rythme volontairement lent (pauses de plusieurs secondes), navigateur visible.
Aucun contournement de captcha : en cas de vérification, le script s'arrête
sur la page et te laisse la main.
"""
import argparse
import csv
import datetime as dt
import json
import os
import random
import re
import sys
import time
import urllib.parse

PROFIL = os.path.expanduser("~/.censure-rs-fr-navigateur")
SORTIE = "exports"


def x_recherche(q):
    return "https://x.com/search?q=" + urllib.parse.quote(q, safe="") + "&f=live"


PLAN_ACTE4 = [
    # X, mouvement
    x_recherche('"gilets jaunes" since:2026-11-07'),
    x_recherche('#acte4 OR #acteIV OR #7novembre since:2026-11-07'),
    x_recherche('"tout bloquer" OR "bloquons tout" since:2026-11-07'),
    x_recherche('#RadioLondres since:2026-11-07'),
    # X, revendication
    x_recherche('(censure OR censuré OR shadowban OR shadowbanned OR "shadow ban") '
                '(manif OR "gilets jaunes" OR #acte4 OR #7novembre) since:2026-11-07'),
    x_recherche('(TikTok OR Instagram OR Snapchat) (coupé OR coupure OR bloqué OR "ne marche plus") '
                '(manif OR "gilets jaunes" OR #acte4 OR #7novembre) since:2026-11-07'),
    # X, témoins datés du 7
    x_recherche('météo lang:fr since:2026-11-07 until:2026-11-08'),
    x_recherche('"ligue 1" lang:fr since:2026-11-07 until:2026-11-08'),
    # X, hashtags génériques (filtrés à l'import : marqueur du mouvement exigé)
    x_recherche('(#manif OR #manifestation) lang:fr since:2026-11-07'),
    # TikTok, pages de hashtag
    "https://www.tiktok.com/tag/acte4",
    "https://www.tiktok.com/tag/7novembre",
    "https://www.tiktok.com/tag/6novembre",
    "https://www.tiktok.com/tag/5novembre",
    "https://www.tiktok.com/tag/giletsjaunes",
    "https://www.tiktok.com/tag/toutbloquer",
    # TikTok, hashtags génériques repérés en naviguant (filtrés à l'import)
    "https://www.tiktok.com/tag/manif",
    "https://www.tiktok.com/tag/manifestation",
    "https://www.tiktok.com/tag/revolution",
    # TikTok, témoins
    "https://www.tiktok.com/tag/meteo",
    "https://www.tiktok.com/tag/ligue1",
    "https://www.tiktok.com/tag/recette",
    "https://www.tiktok.com/tag/foot",
]

# Réponses qui portent des posts (mêmes familles que Zeeschuimer)
X_ENDPOINTS = ("SearchTimeline", "UserTweets", "UserOriginalsTimeline", "UserTweetsAndReplies", "TweetDetail")
TT_ENDPOINTS = ("/api/challenge/item_list", "/api/search/general/full", "/api/search/item/full", "/api/post/item_list")


# ------------------------------------------------------------------ extraction
def tweets_de(obj):
    """Tous les objets « tweet_results.result » d'une réponse GraphQL de X (hors tweets cités)."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "tweet_results" and isinstance(v, dict) and isinstance(v.get("result"), dict):
                r = v["result"]
                if r.get("__typename") == "TweetWithVisibilityResults":
                    r = r.get("tweet", r)
                if r.get("rest_id") and r.get("legacy"):
                    yield r
            elif k != "quoted_status_result":
                yield from tweets_de(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from tweets_de(v)


def videos_de(obj):
    """Vidéos d'une réponse de l'API web de TikTok (itemList, item_list, ou data[].item)."""
    if not isinstance(obj, dict):
        return
    for cle in ("itemList", "item_list"):
        for it in obj.get(cle) or []:
            if isinstance(it, dict) and it.get("id") and "liveRoomInfo" not in it:
                yield it
    for d in obj.get("data") or []:
        it = d.get("item") if isinstance(d, dict) else None
        if isinstance(it, dict) and it.get("id") and "liveRoomInfo" not in it:
            yield it


class Capture:
    def __init__(self, chemin):
        self.f = open(chemin, "a", encoding="utf-8")
        # Journal des pages réellement ouvertes : distingue « recherche vide » et « recherche jamais ouverte »
        self.journal = open(re.sub(r"\.ndjson$", "", chemin) + ".visites.csv", "a", encoding="utf-8")
        if self.journal.tell() == 0:
            self.journal.write("ts_utc,url,posts,alerte\n")
        self.vus = set()
        self.n_page = 0
        self.page_url = ""

    def ecrire(self, plateforme, item_id, data, source_url):
        cle = (plateforme, self.page_url, item_id)
        if cle in self.vus:
            return
        self.vus.add(cle)
        self.n_page += 1
        self.f.write(json.dumps({
            "item_id": str(item_id), "source_platform": plateforme, "source_platform_url": self.page_url,
            "source_url": source_url, "timestamp_collected": int(time.time() * 1000),
            "user_agent": "collecteur.py", "data": data}, ensure_ascii=False) + "\n")
        self.f.flush()

    def sur_reponse(self, reponse):
        url = reponse.url
        try:
            if "x.com/i/api/graphql/" in url and any(e in url for e in X_ENDPOINTS):
                for t in tweets_de(reponse.json()):
                    self.ecrire("twitter.com", t["rest_id"], t, url)
            elif "tiktok.com" in url and any(e in url for e in TT_ENDPOINTS):
                for v in videos_de(reponse.json()):
                    self.ecrire("tiktok.com", v["id"], v, url)
        except Exception:
            pass  # réponse non JSON ou interrompue : on ignore


# ------------------------------------------------------------------ session Firefox
def cookies_firefox(domaine, url):
    """Cookies de ta session Firefox pour un site, lus localement avec « minet cookies firefox ».
    Ils ne sont ni affichés ni écrits sur le disque : ils passent directement au navigateur piloté."""
    import subprocess
    try:
        sortie = subprocess.run(["minet", "cookies", "firefox", "--url", url], capture_output=True,
                                text=True, timeout=60).stdout.strip()
    except FileNotFoundError:
        sys.exit("Minet manque pour lire les cookies de Firefox : pip install minet")
    return analyser_cookies(sortie, domaine)


def analyser_cookies(entete, domaine):
    """« nom=valeur; nom2=valeur2 » → cookies au format Playwright pour le domaine donné."""
    cookies = []
    if not entete:
        return cookies
    for morceau in entete.splitlines()[-1].split(";"):
        if "=" not in morceau:
            continue
        nom, valeur = morceau.strip().split("=", 1)
        if nom:
            cookies.append({"name": nom, "value": valeur, "domain": "." + domaine, "path": "/",
                            "secure": True, "sameSite": "Lax"})
    return cookies


# ------------------------------------------------------------------ navigation
def pause(a, b):
    time.sleep(random.uniform(a, b))


def visiter(page, capture, url, defilements, journal):
    capture.page_url = url
    capture.n_page = 0
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=60_000)
    except Exception as e:
        journal.append((url, 0, f"erreur de chargement : {e}"))
        return
    pause(4, 7)
    sans_nouveau = 0
    # Souris au centre de la colonne principale : sans ça, la molette peut agir sur une zone
    # qui ne défile pas (X ne charge alors que le premier lot de 20 posts).
    try:
        page.mouse.move(640 + random.randint(-40, 40), 500 + random.randint(-40, 40))
    except Exception:
        pass
    for i in range(defilements):
        avant = capture.n_page
        try:
            page.mouse.wheel(0, random.randint(1800, 2600))
            pause(0.8, 1.5)
            # Deuxième geste, comme un humain qui va en bas de la page : déclenche le lot suivant.
            if i % 2:
                page.keyboard.press("End")
            else:
                page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
        except Exception:
            pass
        pause(2.5, 5)
        if capture.n_page == avant:
            sans_nouveau += 1
            if sans_nouveau >= 4:
                break
        else:
            sans_nouveau = 0
    contenu = (page.content() or "")[:200_000].lower()
    alerte = ""
    if any(m in contenu for m in ("captcha", "verify you are human", "confirm you’re not a bot", "rate limit")) \
            and capture.n_page == 0:
        alerte = "vérification ou limite affichée : à regarder dans la fenêtre"
    journal.append((url, capture.n_page, alerte))
    capture.journal.write(f"{dt.datetime.now(dt.timezone.utc):%Y-%m-%dT%H:%M:%SZ},{url},{capture.n_page},{alerte}\n")
    capture.journal.flush()
    print(f"  {capture.n_page:4d} posts  {urllib.parse.unquote(url)[:110]} {alerte}", file=sys.stderr)


def plan_t6(max_comptes, plateformes=("x", "tiktok")):
    lignes = [l for l in csv.DictReader(open(os.path.join("contenus", "comptes_t6.csv"), newline="", encoding="utf-8"))
              if (l.get("plateforme") or "x") in plateformes]
    # alterner les groupes pour que l'heure ne biaise pas la comparaison
    par = {}
    for l in lignes:
        par.setdefault(l["groupe"], []).append(l)
    ordre = []
    while any(par.values()) and len(ordre) < max_comptes:
        for g in list(par):
            if par[g] and len(ordre) < max_comptes:
                ordre.append(par[g].pop(0))
    urls = []
    for l in ordre:
        urls += [l["profil"]] + ([l["recherche"]] if l.get("recherche") else [])
    return urls


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plan", choices=["acte4", "t6"])
    ap.add_argument("--connexion", action="store_true", help="ouvre le navigateur pour te connecter, une seule fois")
    ap.add_argument("--cookies-firefox", action="store_true",
                    help="reprend la session de ton Firefox (déjà connecté à X et TikTok) au lieu de se connecter "
                         "dans le navigateur piloté ; nécessite minet et « python3 -m playwright install firefox »")
    ap.add_argument("--max-comptes", type=int, default=100)
    ap.add_argument("--plateformes", default="x,tiktok",
                    help="plateformes à visiter, pour les deux plans (ex. « x » : TikTok refuse le navigateur piloté)")
    ap.add_argument("--defilements", type=int, help="nombre de défilements par page (défaut : 12 pour acte4, 6 pour t6)")
    a = ap.parse_args()
    if a.cookies_firefox and not a.plan:
        sys.exit("Avec --cookies-firefox, indique un plan : --plan t6 ou --plan acte4")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("Playwright manque : pip install playwright && python3 -m playwright install chromium")

    with sync_playwright() as p:
        if a.cookies_firefox:
            # Session reprise de ton Firefox habituel : aucune connexion dans le navigateur piloté.
            navigateur = p.firefox.launch(headless=False)
            ctx = navigateur.new_context(locale="fr-FR", viewport={"width": 1280, "height": 900})
            total = 0
            for domaine, url in (("x.com", "https://x.com"), ("tiktok.com", "https://www.tiktok.com")):
                cookies = cookies_firefox(domaine, url)
                if cookies:
                    ctx.add_cookies(cookies)
                total += len(cookies)
                print(f"  {len(cookies)} cookie(s) de session repris pour {domaine}", file=sys.stderr)
            if total == 0:
                sys.exit("Aucun cookie trouvé : es-tu connecté à X et TikTok dans Firefox ?")
            page = ctx.new_page()
        else:
            ctx = p.chromium.launch_persistent_context(PROFIL, headless=False, locale="fr-FR",
                                                       viewport={"width": 1280, "height": 900})
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
        if not a.cookies_firefox and (a.connexion or not a.plan):
            page.goto("https://x.com/login")
            input("Connecte-toi à X dans la fenêtre, puis à TikTok (onglet suivant), puis appuie sur Entrée ici… ")
            t = ctx.new_page()
            t.goto("https://www.tiktok.com/login")
            input("Connecté à TikTok ? Entrée pour terminer. ")
            ctx.close()
            print(f"Session enregistrée dans {PROFIL} (jamais publié).", file=sys.stderr)
            return
        os.makedirs(SORTIE, exist_ok=True)
        nom = os.path.join(SORTIE, f"collecteur-{a.plan}-{dt.datetime.now():%Y-%m-%dT%H%M}.ndjson")
        capture = Capture(nom)
        page.on("response", capture.sur_reponse)
        plateformes = a.plateformes.split(",")
        if a.plan == "acte4":
            urls = [u for u in PLAN_ACTE4 if ("tiktok" if "tiktok.com" in u else "x") in plateformes]
        else:
            urls = plan_t6(a.max_comptes, plateformes)
        defil = a.defilements or (12 if a.plan == "acte4" else 6)
        print(f"Plan {a.plan} : {len(urls)} pages, {defil} défilements maximum par page → {nom}", file=sys.stderr)
        journal = []
        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}]", file=sys.stderr, end="")
            visiter(page, capture, url, defil, journal)
            pause(8, 15)
        ctx.close()
    total = sum(n for _, n, _ in journal)
    vides = [u for u, n, _ in journal if n == 0]
    print(f"\nTerminé : {total} posts enregistrés dans {nom}.", file=sys.stderr)
    if vides:
        print(f"{len(vides)} page(s) sans aucun post (normal pour un profil sans posts récents ; "
              f"anormal si c'est presque tout) :", file=sys.stderr)
        for u in vides[:15]:
            print("   ", urllib.parse.unquote(u)[:120], file=sys.stderr)
    print("Ensuite : python3 importer.py ~/Downloads/zeeschuimer-export-*.ndjson exports/*.ndjson", file=sys.stderr)


if __name__ == "__main__":
    main()
