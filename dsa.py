#!/usr/bin/env python3
"""
dsa.py — tests T3 et T4 à partir de la base de transparence du DSA (Commission européenne).

Chaque grande plateforme doit y déclarer chacune de ses décisions de modération
(« statements of reasons ») : retrait, blocage, déclassement, suspension…
La Commission publie un export par jour et par plateforme :
https://transparency.dsa.ec.europa.eu/explore-data/download

Deux mesures :
  1. Correspondance avec nos posts : chez TikTok, l'identifiant déclaré
     (platform_uid) est celui de la vidéo. On cherche donc si une vidéo suivie
     a fait l'objet d'une décision déclarée, et laquelle. Chez X, l'identifiant
     est opaque : la correspondance n'est pas possible.
  2. Tendance : nombre de décisions par jour dont le périmètre inclut la France,
     avant le mouvement (référence) et pendant, par type (retrait, déclassement,
     contenu illégal, catégorie « discours civique », périmètre France seule).

T3 = décisions de retrait, de blocage ou de suspension de compte déclarées ; T4 = déclassements déclarés
(dont, chez TikTok, « non éligible au fil Pour toi »).

Rien dans cette base n'indique qui a demandé une décision : une demande d'une
autorité apparaît au mieux comme « notification » (source_type), sans nom.

  python3 dsa.py --du 2026-10-01 --au 2026-11-08 --corpus contenus/corpus.csv
Sorties : dsa_jours.csv, dsa_correspondances.csv, rapport/dsa.md, dsa_resultats.csv
"""
import argparse
import collections
import csv
import datetime as dt
import io
import math
import os
import re
import sys
import tempfile
import urllib.request
import zipfile

BASE = "https://transparency.dsa.ec.europa.eu/explore-data/download"
PLATEFORMES = {"x": 22, "tiktok": 30, "instagram": 33, "youtube": 27}
NOMS = {"x": "X", "tiktok": "TikTok", "instagram": "Instagram", "youtube": "YouTube"}
DEBUT_MOUVEMENT = dt.date(2026, 10, 17)
UA = {"User-Agent": "censure-rs-fr/1.0 (recherche, export public DSA)"}
COLONNES = ["date", "plateforme", "total", "fr", "fr_seul", "fr_retrait", "fr_declasse", "fr_illegal",
            "fr_civique", "fr_securite", "fr_notification"]

csv.field_size_limit(10 ** 8)


def ouvrir(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=600)


def lister(pid, du, au):
    """{date: id de l'export complet} pour une plateforme, en parcourant les pages de la liste."""
    res, page = {}, 1
    while page < 60:
        html = ouvrir(f"{BASE}?platform_id={pid}&page={page}").read().decode("utf-8", "replace")
        # Chaque ligne : la date, puis les liens full / sha1 / light / sha1light.
        lignes = re.findall(r"(20\d\d-\d\d-\d\d)(.*?)download-file/(\d+)/full", html, re.S)
        if not lignes:
            break
        for d, _, fid in lignes:
            j = dt.date.fromisoformat(d)
            if du <= j <= au:
                res.setdefault(j, fid)
        if min(dt.date.fromisoformat(d) for d, _, _ in lignes) < du:
            break
        page += 1
    return res


def est_declasse(r):
    vis = r.get("decision_visibility", "") + " " + r.get("decision_visibility_other", "")
    return ("DEMOTED" in vis or "not eligible for recommendation" in vis.lower()
            or "for you feed" in vis.lower() or "reduced visibility" in vis.lower())


def est_retrait(r):
    """Retrait ou blocage du contenu, ou suspension du compte (X déclare surtout des suspensions)."""
    vis = r.get("decision_visibility", "")
    return ("REMOVED" in vis or "DISABLED" in vis or r.get("decision_account", "") in
            ("DECISION_ACCOUNT_SUSPENDED", "DECISION_ACCOUNT_TERMINATED"))


def lignes_export(fichier):
    """Les exports sont un zip de zips de CSV."""
    z = zipfile.ZipFile(fichier)
    for nom in z.namelist():
        donnees = z.read(nom)
        if nom.endswith(".zip"):
            inner = zipfile.ZipFile(io.BytesIO(donnees))
            for n in inner.namelist():
                yield from csv.DictReader(io.TextIOWrapper(inner.open(n), encoding="utf-8", newline=""))
        elif nom.endswith(".csv"):
            yield from csv.DictReader(io.TextIOWrapper(io.BytesIO(donnees), encoding="utf-8", newline=""))


def traiter_jour(plat, jour, fid, ids_corpus, dossier):
    chemin = os.path.join(dossier, f"sor-{plat}-{jour}.zip")
    with ouvrir(f"https://transparency.dsa.ec.europa.eu/explore-data/download-file/{fid}/full") as r, \
            open(chemin, "wb") as f:
        while True:
            b = r.read(1 << 20)
            if not b:
                break
            f.write(b)
    c = collections.Counter()
    corresp = []
    exemples_uid = []
    try:
        for r in lignes_export(chemin):
            c["total"] += 1
            uid = r.get("platform_uid", "")
            if len(exemples_uid) < 3:
                exemples_uid.append(uid)
            portee = r.get("territorial_scope", "")
            if uid in ids_corpus:
                corresp.append({"id": ids_corpus[uid], "date_decision": r.get("application_date", "")[:10],
                                "declaree_le": r.get("created_at", "")[:10],
                                "retrait": int(est_retrait(r)), "declasse": int(est_declasse(r)),
                                "visibilite": r.get("decision_visibility", ""),
                                "visibilite_autre": r.get("decision_visibility_other", "")[:120],
                                "compte": r.get("decision_account", ""),
                                "motif": r.get("decision_ground", "").replace("DECISION_GROUND_", ""),
                                "regle": (r.get("incompatible_content_ground") or r.get("illegal_content_legal_ground", ""))[:80],
                                "categorie_dsa": r.get("category", "").replace("STATEMENT_CATEGORY_", ""),
                                "fr_dans_portee": int('"FR"' in portee), "portee_fr_seule": int(portee == '["FR"]'),
                                "source": r.get("source_type", ""), "automatique": r.get("automated_decision", "")})
            if '"FR"' not in portee:
                continue
            c["fr"] += 1
            c["fr_seul"] += portee == '["FR"]'
            c["fr_retrait"] += est_retrait(r)
            c["fr_declasse"] += est_declasse(r)
            c["fr_illegal"] += r.get("decision_ground", "") == "DECISION_GROUND_ILLEGAL_CONTENT"
            cat = r.get("category", "") + r.get("category_addition", "")
            c["fr_civique"] += "CIVIC_DISCOURSE" in cat
            c["fr_securite"] += "PUBLIC_SECURITY" in cat
            c["fr_notification"] += r.get("source_type", "") in ("SOURCE_ARTICLE_16", "SOURCE_TRUSTED_NOTIFIER",
                                                                  "SOURCE_TYPE_OTHER_NOTIFICATION")
    finally:
        os.remove(chemin)
    return c, corresp, exemples_uid


def charger_corpus(path):
    ids = collections.defaultdict(dict)  # plateforme -> {post_id: id corpus}
    info = {}
    if path and os.path.exists(path):
        for r in csv.DictReader(open(path, newline="", encoding="utf-8")):
            pid = r["id"].split("_", 1)[1] if "_" in r["id"] else r["id"]
            ids[r["plateforme"]][pid] = r["id"]
            info[r["id"]] = r
    return ids, info


def fisher_bilateral(a, b, c, d):
    """Test exact de Fisher, tableau [[a, b], [c, d]]."""
    n1, n2, k = a + b, c + d, a + c
    def p(x):
        return math.comb(n1, x) * math.comb(n2, k - x) / math.comb(n1 + n2, k)
    p0 = p(a)
    return min(1.0, sum(p(x) for x in range(max(0, k - n2), min(k, n1) + 1) if p(x) <= p0 * (1 + 1e-9)))


def tendance(jours, plat, champ):
    ref = [j[champ] for j in jours if j["plateforme"] == plat and j["date"] < DEBUT_MOUVEMENT]
    mvt = [j[champ] for j in jours if j["plateforme"] == plat and j["date"] >= DEBUT_MOUVEMENT]
    if not ref or not mvt:
        return None
    mr, mm = sum(ref) / len(ref), sum(mvt) / len(mvt)
    return mr, mm, (mm / mr if mr else None), len(ref), len(mvt)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--du", default="2026-10-01")
    ap.add_argument("--au", default=str(dt.date.today() - dt.timedelta(days=1)))
    ap.add_argument("--plateformes", nargs="+", default=list(PLATEFORMES))
    ap.add_argument("--corpus", default="contenus/corpus.csv")
    ap.add_argument("--reprendre", action="store_true", help="ne retélécharge pas les jours déjà dans dsa_jours.csv")
    ap.add_argument("--hors-ligne", action="store_true", help="refait seulement le rapport à partir de dsa_jours.csv")
    a = ap.parse_args()
    du, au = dt.date.fromisoformat(a.du), dt.date.fromisoformat(a.au)
    ids, info = charger_corpus(a.corpus)

    deja = set()
    jours = []
    corresp = []
    if (a.reprendre or a.hors_ligne) and os.path.exists("dsa_jours.csv"):
        for r in csv.DictReader(open("dsa_jours.csv", newline="", encoding="utf-8")):
            jours.append({**{k: int(r[k]) for k in COLONNES[2:]}, "date": dt.date.fromisoformat(r["date"]),
                          "plateforme": r["plateforme"]})
            deja.add((r["plateforme"], r["date"]))
        if os.path.exists("dsa_correspondances.csv"):
            corresp = list(csv.DictReader(open("dsa_correspondances.csv", newline="", encoding="utf-8")))
    uid_ex = {}
    with tempfile.TemporaryDirectory() as tmp:
        for plat in ([] if a.hors_ligne else a.plateformes):
            liste = lister(PLATEFORMES[plat], du, au)
            print(f"{NOMS[plat]} : {len(liste)} jour(s) disponibles entre {du} et {au}", file=sys.stderr)
            for jour in sorted(liste):
                if (plat, str(jour)) in deja:
                    continue
                try:
                    c, cs, ex = traiter_jour(plat, jour, liste[jour], ids.get(plat, {}), tmp)
                except Exception as e:
                    print(f"  {plat} {jour} : échec ({e})", file=sys.stderr)
                    continue
                uid_ex.setdefault(plat, ex)
                jours.append({**{k: c[k] for k in COLONNES[2:]}, "date": jour, "plateforme": plat})
                corresp += cs
                print(f"  {plat} {jour} : {c['total']} décisions, {c['fr']} avec la France, "
                      f"{len(cs)} sur nos posts", file=sys.stderr)
                # écriture au fil de l'eau : une interruption ne perd rien
                ecrire(jours, corresp)
    ecrire(jours, corresp)
    rapport(jours, corresp, ids, info, a.plateformes, uid_ex)


def ecrire(jours, corresp):
    with open("dsa_jours.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLONNES)
        w.writeheader()
        for j in sorted(jours, key=lambda j: (j["plateforme"], j["date"])):
            w.writerow({**j, "date": str(j["date"])})
    champs = ["id", "date_decision", "declaree_le", "retrait", "declasse", "visibilite", "visibilite_autre", "compte",
              "motif", "regle", "categorie_dsa", "fr_dans_portee", "portee_fr_seule", "source", "automatique"]
    with open("dsa_correspondances.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=champs, extrasaction="ignore")
        w.writeheader()
        w.writerows(corresp)


def rapport(jours, corresp, ids, info, plateformes, uid_ex):
    o = ["# Base de transparence du DSA : décisions déclarées par les plateformes (T3, T4)\n",
         f"Généré le {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC. Source : exports quotidiens publics "
         "de la Commission européenne (transparency.dsa.ec.europa.eu). Référence = avant le "
         f"{DEBUT_MOUVEMENT:%d/%m} ; mouvement = à partir du {DEBUT_MOUVEMENT:%d/%m}.\n"]
    verdicts = []
    for plat in plateformes:
        js = [j for j in jours if j["plateforme"] == plat]
        if not js:
            for t in ("T3", "T4"):
                verdicts.append({"test": t, "plateforme": plat, "verdict": "NON TESTABLE (aucun export DSA lu)"})
            continue
        dmin, dmax = min(j["date"] for j in js), max(j["date"] for j in js)
        o.append(f"## {NOMS[plat]}\n")
        o.append(f"{len(js)} jours lus, du {dmin:%d/%m} au {dmax:%d/%m}.\n")
        o.append("| décisions par jour (périmètre incluant la France) | référence | mouvement | rapport |")
        o.append("|---|---|---|---|")
        tend = {"total": tendance(jours, plat, "total")}
        n_fr = sum(j["fr"] for j in js)
        part_fr_seul = sum(j["fr_seul"] for j in js) / n_fr if n_fr else 0
        for champ, lib in (("fr", "toutes"), ("fr_retrait", "retraits, blocages, suspensions"),
                           ("fr_declasse", "déclassements"), ("fr_illegal", "motif : contenu illégal"),
                           ("fr_civique", "catégorie « discours civique »"), ("fr_securite", "catégorie « sécurité publique »"),
                           ("fr_seul", "périmètre France seule"), ("fr_notification", "suite à une notification")):
            t = tendance(jours, plat, champ)
            tend[champ] = t
            if t:
                mr, mm, rap, nr, nm = t
                if champ == "fr":
                    o.append(f"| (jours lus) | {nr} | {nm} | |")
                o.append(f"| {lib} | {mr:,.0f} | {mm:,.0f} | {'—' if rap is None else f'{rap:.2f}'} |".replace(",", " "))
        o.append(f"\nPart des décisions « France » dont le périmètre est la France seule : {part_fr_seul:.1%} "
                 "(le reste vaut pour toute l'UE ou plusieurs pays).\n")
        # Correspondances avec nos posts
        cs = [c for c in corresp if c["id"].startswith(plat + "_")]
        n_corpus = len(ids.get(plat, {}))
        correspondance_possible = plat == "tiktok" or bool(cs)
        groupes = collections.defaultdict(lambda: {"n": 0, "retrait": set(), "declasse": set()})
        for pid, r in info.items():
            if r["plateforme"] != plat or r.get("categorie") == "controle":
                continue
            g = "temoin" if r["categorie"].startswith("temoin") else "mouvement"
            groupes[g]["n"] += 1
        for c in cs:
            r = info.get(c["id"], {})
            if r.get("categorie") == "controle":
                continue
            g = "temoin" if r.get("categorie", "").startswith("temoin") else "mouvement"
            if int(c["retrait"]):
                groupes[g]["retrait"].add(c["id"])
            if int(c["declasse"]):
                groupes[g]["declasse"].add(c["id"])
        if correspondance_possible and n_corpus:
            o.append(f"**Nos posts dans la base** ({n_corpus} posts {NOMS[plat]} suivis) :\n")
            o.append("| groupe | posts suivis | avec un retrait déclaré | avec un déclassement déclaré |")
            o.append("|---|---|---|---|")
            for g in ("mouvement", "temoin"):
                d = groupes[g]
                o.append(f"| {g} | {d['n']} | {len(d['retrait'])} | {len(d['declasse'])} |")
            o.append("")
            for c in sorted(cs, key=lambda c: c["date_decision"]):
                r = info.get(c["id"], {})
                o.append(f"- `{c['id']}` ({r.get('categorie', '?')}, {r.get('periode', '')}) décision du "
                         f"{c['date_decision']} : {'retrait' if int(c['retrait']) else ''}"
                         f"{'déclassement' if int(c['declasse']) else ''}{'autre' if not (int(c['retrait']) or int(c['declasse'])) else ''}"
                         f" — {c['visibilite_autre'] or c['visibilite']} ; règle : {c['regle'] or '—'} ; "
                         f"catégorie : {c['categorie_dsa']} ; {c['source'].replace('SOURCE_', '').lower()} ; "
                         f"{'France seule' if int(c['portee_fr_seule']) else 'périmètre européen'}")
            o.append("")
        elif n_corpus:
            o.append(f"Correspondance avec nos posts impossible : l'identifiant déclaré par {NOMS[plat]} n'est pas "
                     f"celui du post (exemple : `{(uid_ex.get(plat) or ['?'])[0][:12]}…`).\n")

        def verdict(cle, lib, champ):
            mv, tm = groupes["mouvement"], groupes["temoin"]
            t = tend.get(champ)
            hausse = t and t[2] and t[2] >= 1.5
            txt_t = (f"tendance France : {t[0]:,.0f} → {t[1]:,.0f} par jour (×{t[2]:.2f})".replace(",", " ")
                     if t and t[2] else "tendance non mesurable")
            # Une hausse qui touche toutes les décisions, tous pays, n'est pas propre à la France
            tt_ = tend.get("total")
            if t and t[2] and tt_ and tt_[2]:
                txt_t += f" ; toutes décisions, tous pays : ×{tt_[2]:.2f}"
                if t[2] >= 1.5 and tt_[2] >= 1.5:
                    txt_t += " → hausse générale de ce que déclare la plateforme, pas propre à la France"
            if hausse and part_fr_seul < 0.05:
                txt_t += (" → périmètre déclaré « toute l'UE » et langue non déclarée : impossible de dire "
                          "si cette hausse concerne la France")
            if correspondance_possible and n_corpus:
                a_, c_ = len(mv[cle]), len(tm[cle])
                p = fisher_bilateral(a_, mv["n"] - a_, c_, tm["n"] - c_) if mv["n"] and tm["n"] else 1.0
                taux = f"mouvement {a_}/{mv['n']}, témoins {c_}/{tm['n']}, p = {p:.3f}"
                if a_ == 0 and c_ == 0:
                    v = f"RIEN DÉTECTÉ (aucun de nos posts n'a de {lib} déclaré ; {txt_t})"
                elif p < 0.05 and mv["n"] and a_ / mv["n"] > (c_ / tm["n"] if tm["n"] else 0):
                    v = f"**DÉTECTÉ (plus de {lib}s déclarés pour le mouvement : {taux})** ; {txt_t}"
                else:
                    v = f"RIEN DÉTECTÉ (pas d'écart : {taux}) ; {txt_t}"
            else:
                if not t:
                    v = "NON TESTABLE (pas assez de jours avant et pendant)"
                elif hausse:
                    v = f"**HAUSSE** des {lib}s déclarés (périmètre incluant la France) pendant le mouvement ({txt_t}) ; posts non identifiables"
                else:
                    v = f"RIEN DÉTECTÉ (pas de hausse : {txt_t}) ; posts non identifiables"
            return v

        v3 = verdict("retrait", "retrait", "fr_retrait")
        v4 = verdict("declasse", "déclassement", "fr_declasse")
        verdicts += [{"test": "T3", "plateforme": plat, "verdict": v3}, {"test": "T4", "plateforme": plat, "verdict": v4}]
        o.append(f"**Verdict T3 ({NOMS[plat]})** : {v3}\n")
        o.append(f"**Verdict T4 ({NOMS[plat]})** : {v4}\n")
    o.append("**Lecture.** La base dit ce que la plateforme déclare avoir décidé, et sur quelle règle. Elle ne dit "
             "jamais qui l'a demandé. Une hausse générale peut venir de l'actualité (plus de contenus, plus de "
             "signalements). Les déclarations sont faites par les plateformes elles-mêmes : une décision non "
             "déclarée n'y figure pas.\n")
    os.makedirs("rapport", exist_ok=True)
    open(os.path.join("rapport", "dsa.md"), "w", encoding="utf-8").write("\n".join(o))
    with open("dsa_resultats.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["test", "plateforme", "verdict"])
        w.writeheader()
        w.writerows(verdicts)
    for v in verdicts:
        print(f"{v['test']} {v['plateforme']} : {v['verdict']}", file=sys.stderr)
    print("Écrits : dsa_jours.csv, dsa_correspondances.csv, rapport/dsa.md, dsa_resultats.csv", file=sys.stderr)


if __name__ == "__main__":
    main()
