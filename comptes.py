#!/usr/bin/env python3
"""
comptes.py — tests T6 et T7 (forme 3 : visibilité réduite) sur X, à partir
d'un export Zeeschuimer de la session « comptes » (voir contenus/PROTOCOLE_T6_T7.md).

Pour chaque compte de contenus/comptes_t6.csv, la session contient :
  - le PROFIL du compte (posts qui existent, avec leurs vues) ;
  - la RECHERCHE « from:compte » dans l'onglet Récent (posts visibles en recherche).

T6  Présence dans la recherche : les posts récents du profil apparaissent-ils
    dans la recherche « from:compte » ? Un compte dont les posts existent mais
    n'apparaissent pas est « absent de la recherche » (search ban).
T7  Portée comparée : pour un même compte, les posts sur le mouvement ont-ils
    moins de vues que ses autres posts de la même période ? Comparer un compte à
    lui-même neutralise son nombre d'abonnés. Test du signe sur l'ensemble des comptes.

Sorties :
  rapport/comptes.md          résultats agrégés, comptes désignés par leur code
  resultats_t6_t7.csv         verdicts pour le tableau de analyse_contenus.py

  python3 comptes.py session_comptes.ndjson
"""
import argparse
import collections
import csv
import datetime as dt
import glob
import math
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importer  # noqa: E402  (parseurs Zeeschuimer et pseudonymisation)

MOUVEMENT = re.compile(r"manif|gilets? jaunes?|#?acte ?(?:4|iv)\b|17 ?octobre|24 ?octobre|31 ?octobre|7 ?novembre|"
                       r"bloquons|tout bloquer|gr[èe]ve|cort[èe]ge|vie ch[èe]re|carburant|lecornu|nu[ñn]ez|"
                       r"rassemblement|mobilisation|crs|lacrymo", re.I)
FENETRE_JOURS = 14
AGE_MIN_H = 48      # T7 : un post plus jeune n'a pas fini d'accumuler ses vues
MIN_COMPTES = 8     # T7 : en dessous, pas de conclusion


def binom_bilateral(k, n):
    """p-valeur bilatérale du test du signe (k succès sur n, p = 0,5)."""
    if n == 0:
        return 1.0
    probs = [math.comb(n, i) / 2 ** n for i in range(n + 1)]
    return min(1.0, sum(p for p in probs if p <= probs[k] + 1e-12))


def charger(fichiers):
    cle = importer.cle_pseudo()
    profils = collections.defaultdict(dict)    # handle -> {post_id: post}
    recherches = collections.defaultdict(dict)  # handle -> {post_id: post}
    captures_profil = collections.Counter()
    for f in fichiers:
        for ligne in open(f, encoding="utf-8"):
            if not ligne.strip():
                continue
            try:
                import json
                item = json.loads(ligne)
                if item["source_platform"] not in ("twitter.com", "x.com"):
                    continue
                p = importer.parse_x(item)
            except Exception:
                continue
            if not p:
                continue
            src = item.get("source_platform_url", "")
            ctx, cible = importer.contexte_capture(src)
            p["capture"] = dt.datetime.fromtimestamp(item.get("timestamp_collected", 0) / 1000,
                                                      dt.timezone.utc).replace(tzinfo=None)
            if ctx == "profil":
                captures_profil[cible] += 1
                if p["handle"] == cible and not p["est_repost"]:
                    profils[cible][p["post_id"]] = p
            elif ctx == "recherche":
                m = re.fullmatch(r"\s*from:@?(\w+)\s*", importer.requete_de(src), re.I)
                if m and p["handle"] == m.group(1).lower():
                    recherches[m.group(1).lower()][p["post_id"]] = p
    return profils, recherches, captures_profil, cle


def t6(handle, prof, rech):
    originaux = [p for p in prof.values() if not p["est_reponse"] and p["date"]]
    if not originaux:
        return "non_verifie", "aucun post original capturé sur le profil", 0, 0
    capt = max(p["capture"] for p in prof.values())
    if rech:
        borne = min(p["date"] for p in rech.values() if p["date"])
    else:
        borne = capt - dt.timedelta(days=FENETRE_JOURS)
    fenetre = [p for p in originaux if p["date"] >= borne and p["date"] <= capt - dt.timedelta(minutes=30)]
    if not fenetre:
        return "non_verifie", "aucun post original dans la fenêtre comparée", 0, 0
    absents = [p for p in fenetre if p["post_id"] not in rech]
    if not rech:
        return "absent", f"{len(fenetre)} post(s) sur le profil, 0 dans la recherche", len(fenetre), len(fenetre)
    if len(fenetre) >= 3 and len(absents) / len(fenetre) >= 0.5:
        return "partiel", f"{len(absents)}/{len(fenetre)} post(s) du profil absents de la recherche", len(fenetre), len(absents)
    return "present", f"{len(fenetre) - len(absents)}/{len(fenetre)} post(s) retrouvés dans la recherche", len(fenetre), len(absents)


def t7(prof):
    posts = [p for p in prof.values() if not p["est_reponse"] and isinstance(p["vues"], int) and p["date"]
             and (p["capture"] - p["date"]).total_seconds() >= AGE_MIN_H * 3600
             and (p["capture"] - p["date"]).days <= 30]
    mv = [p["vues"] for p in posts if MOUVEMENT.search(p["texte"] + " " + p["hashtags"])]
    autres = [p["vues"] for p in posts if not MOUVEMENT.search(p["texte"] + " " + p["hashtags"])]
    if len(mv) < 2 or len(autres) < 2:
        return None, len(mv), len(autres)
    med_a = statistics.median(autres)
    return (statistics.median(mv) / med_a if med_a else None), len(mv), len(autres)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ndjson", nargs="+")
    ap.add_argument("--comptes", default=os.path.join(importer.DOSSIER, "comptes_t6.csv"))
    a = ap.parse_args()
    fichiers = sorted({f for m in a.ndjson for f in (glob.glob(m) or [m])})
    profils, recherches, captures_profil, cle = charger(fichiers)
    liste = list(csv.DictReader(open(a.comptes, newline="", encoding="utf-8")))
    groupes = {l["handle"]: l for l in liste}

    res = []
    for handle, l in groupes.items():
        prof, rech = profils.get(handle, {}), recherches.get(handle, {})
        etat, detail, n_fen, n_abs = t6(handle, prof, rech) if (prof or rech) else ("non_verifie", "compte non visité", 0, 0)
        r, n_mv, n_aut = t7(prof)
        res.append({"groupe": l["groupe"], "auteur": l["auteur"], "t6": etat, "t6_detail": detail,
                    "t7_ratio": r, "t7_n_mouvement": n_mv, "t7_n_autres": n_aut,
                    "recherche_visitee": handle in recherches or bool(rech)})

    o = ["# Visibilité des comptes (T6 et T7) : résultats agrégés\n",
         f"Généré le {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC. Comptes désignés par un code ; "
         "aucun nom n'est publié.\n",
         "## T6 : présence dans la recherche « from:compte » (onglet Récent)\n",
         "| groupe | comptes vérifiés | présents | absents de la recherche | partiellement absents | non vérifiés |",
         "|---|---|---|---|---|---|"]
    verdicts = []
    par_g = collections.defaultdict(collections.Counter)
    for x in res:
        par_g[x["groupe"]][x["t6"]] += 1
    for g, c in sorted(par_g.items()):
        verif = c["present"] + c["absent"] + c["partiel"]
        o.append(f"| {g} | {verif} | {c['present']} | {c['absent']} | {c['partiel']} | {c['non_verifie']} |")
    tot = {g: (c["present"] + c["absent"] + c["partiel"], c["absent"] + c["partiel"]) for g, c in par_g.items()}
    n_verif = sum(v for v, _ in tot.values())
    n_abs = sum(a_ for _, a_ in tot.values())
    if n_verif == 0:
        v6 = "NON TESTABLE (aucun compte vérifié : profil et recherche « from: » à capturer)"
    elif n_abs == 0:
        v6 = f"RIEN DÉTECTÉ ({n_verif} comptes vérifiés, tous présents dans la recherche)"
    else:
        detail = " ; ".join(f"{g} : {a_}/{v}" for g, (v, a_) in sorted(tot.items()))
        v6 = f"**DÉTECTÉ ({n_abs} compte(s) absents ou partiellement absents de la recherche)** — {detail}"
    verdicts.append({"test": "T6", "plateforme": "x", "verdict": v6})
    o.append(f"\n**Verdict T6 (X)** : {v6}\n")
    o.append("Détail par compte :\n")
    for x in sorted(res, key=lambda x: (x["groupe"], x["t6"])):
        o.append(f"- `{x['auteur']}` ({x['groupe']}) : {x['t6']} — {x['t6_detail']}")
    o.append("")

    o.append("## T7 : portée comparée (vues des posts sur le mouvement / vues des autres posts du même compte)\n")
    o.append(f"Posts originaux de plus de {AGE_MIN_H} h et de moins de 30 jours ; au moins 2 posts dans chaque catégorie. "
             "Un rapport inférieur à 1 veut dire que les posts sur le mouvement sont moins vus que les autres posts du même compte.\n")
    o.append("| groupe | comptes comparables | rapport médian | comptes avec rapport < 1 | p (test du signe) |")
    o.append("|---|---|---|---|---|")
    v7_parts, v7_signal, n7_tot = [], False, 0
    for g in sorted({x["groupe"] for x in res}):
        rs = [x["t7_ratio"] for x in res if x["groupe"] == g and x["t7_ratio"] is not None]
        if not rs:
            o.append(f"| {g} | 0 | — | — | — |")
            continue
        k = sum(1 for r in rs if r < 1)
        p = binom_bilateral(k, len(rs))
        o.append(f"| {g} | {len(rs)} | {statistics.median(rs):.2f} | {k}/{len(rs)} | {p:.3f} |")
        if g != "temoin":
            n7_tot += len(rs)
            v7_parts.append(f"{g} : {k}/{len(rs)} comptes, rapport médian {statistics.median(rs):.2f}, p = {p:.3f}")
            if len(rs) >= MIN_COMPTES and p < 0.05 and k > len(rs) / 2:
                v7_signal = True
    if n7_tot < MIN_COMPTES:
        v7 = f"NON TESTABLE (seulement {n7_tot} compte(s) comparables, il en faut au moins {MIN_COMPTES})"
    elif v7_signal:
        v7 = "**DÉTECTÉ (posts sur le mouvement significativement moins vus que les autres posts des mêmes comptes)** — " + " ; ".join(v7_parts)
    else:
        v7 = "RIEN DÉTECTÉ (pas d'écart significatif) — " + " ; ".join(v7_parts)
    verdicts.append({"test": "T7", "plateforme": "x", "verdict": v7})
    o.append(f"\n**Verdict T7 (X)** : {v7}\n")
    o.append("**Lecture.** T6 et T7 décrivent une visibilité, pas son origine. Moins de vues peut venir d'un moindre "
             "intérêt du public. Un compte absent de la recherche peut l'être à cause de filtres automatiques de X "
             "(spam, signalements). Seule une déclaration de « contenu déclassé » dans la base DSA (T4) indique une "
             "décision de la plateforme, et rien n'y indique une demande de l'État.\n")
    os.makedirs("rapport", exist_ok=True)
    open(os.path.join("rapport", "comptes.md"), "w", encoding="utf-8").write("\n".join(o))
    with open("resultats_t6_t7.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["test", "plateforme", "verdict"])
        w.writeheader()
        w.writerows(verdicts)
    print(f"T6 : {v6}\nT7 : {v7}\nÉcrits : rapport/comptes.md, resultats_t6_t7.csv", file=sys.stderr)


if __name__ == "__main__":
    main()
