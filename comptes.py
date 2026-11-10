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
FENETRE_T6_H = 72   # T6 : on ne compare que les posts des 72 dernières heures. Au-delà, la recherche
                    # « Récent » de X est incomplète pour tout le monde (vérifié sur les témoins le 07/11).
MIN_SESSIONS = 2    # T6 : un compte n'est « absent » que s'il l'est dans au moins 2 sessions distinctes
AGE_MIN_H = 48      # T7 : un post plus jeune n'a pas fini d'accumuler ses vues
MIN_COMPTES = 8     # T7 : en dessous, pas de conclusion


def fisher_bilateral(a, b, c, d):
    """Test exact de Fisher, tableau [[a, b], [c, d]]."""
    n1, n2, k = a + b, c + d, a + c
    def p(x):
        return math.comb(n1, x) * math.comb(n2, k - x) / math.comb(n1 + n2, k)
    p0 = p(a)
    return min(1.0, sum(p(x) for x in range(max(0, k - n2), min(k, n1) + 1) if p(x) <= p0 * (1 + 1e-9)))


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
    visitees = None      # recherches « from: » réellement ouvertes, d'après le journal du collecteur
    derniere = dt.datetime.min
    for f in fichiers:
        journal = re.sub(r"\.ndjson$", "", f) + ".visites.csv"
        if os.path.exists(journal):
            visitees = visitees or set()
            for v in csv.DictReader(open(journal, newline="", encoding="utf-8")):
                m = re.search(r"from(?::|%3A)@?(\w+)", v["url"], re.I)
                if m:
                    visitees.add(("x", m.group(1).lower()))
        for ligne in open(f, encoding="utf-8"):
            if not ligne.strip():
                continue
            try:
                import json
                item = json.loads(ligne)
                if item["source_platform"] not in importer.PARSEURS:
                    continue
                p = importer.PARSEURS[item["source_platform"]](item)
            except Exception:
                continue
            if not p:
                continue
            src = item.get("source_platform_url", "")
            ctx, cible = importer.contexte_capture(src)
            p["capture"] = dt.datetime.fromtimestamp(item.get("timestamp_collected", 0) / 1000,
                                                      dt.timezone.utc).replace(tzinfo=None)
            derniere = max(derniere, p["capture"])
            cible = cible.lstrip("@")
            if ctx == "profil":
                captures_profil[(p["plateforme"], cible)] += 1
                if p["handle"] == cible and not p["est_repost"]:
                    profils[(p["plateforme"], cible)][p["post_id"]] = p
            elif ctx == "recherche" and p["plateforme"] == "x":
                m = re.fullmatch(r"\s*from:@?(\w+)\s*", importer.requete_de(src), re.I)
                if m and p["handle"] == m.group(1).lower():
                    recherches[("x", m.group(1).lower())][p["post_id"]] = p
    return profils, recherches, captures_profil, cle, visitees, derniere


def t6(handle, prof, rech, visitee=None, derniere=None):
    """visitee : True/False si le journal du collecteur dit si la recherche a été ouverte,
    None sinon (session manuelle ou ancien collecteur)."""
    originaux = [p for p in prof.values() if not p["est_reponse"] and p["date"]]
    if not originaux:
        return "non_verifie", "aucun post original capturé sur le profil", 0, 0
    capt = max(p["capture"] for p in prof.values())
    if not rech:
        # Recherche vide : était-elle vraiment ouverte, ou la session s'est-elle arrêtée avant ?
        if visitee is False:
            return "non_verifie", "recherche jamais ouverte (session interrompue)", 0, 0
        if visitee is None and derniere is not None and capt >= derniere - dt.timedelta(seconds=90):
            return "non_verifie", "dernier compte de la session : recherche peut-être jamais ouverte", 0, 0
    borne = capt - dt.timedelta(hours=FENETRE_T6_H)
    if rech:
        borne = max(borne, min(p["date"] for p in rech.values() if p["date"]))
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
    profils, recherches, captures_profil, cle, visitees, derniere = charger(fichiers)
    liste = list(csv.DictReader(open(a.comptes, newline="", encoding="utf-8")))
    groupes = {(l.get("plateforme") or "x", l["handle"]): l for l in liste}

    # T6 : chaque fichier contenant des recherches « from: » est une session, évaluée séparément.
    sessions = []
    for f in fichiers:
        s_ = charger([f])
        if any(k[0] == "x" for k in s_[1]):
            sessions.append((os.path.basename(f), s_))

    res = []
    for (plat, handle), l in groupes.items():
        prof = profils.get((plat, handle), {})
        par_session = []
        if plat == "x":
            for nom, (pr, re_, _, _, vis, der) in sessions:
                p_, r_ = pr.get((plat, handle), {}), re_.get((plat, handle), {})
                visitee = None if vis is None else (plat, handle) in vis
                e_ = t6(handle, p_, r_, visitee, der) if (p_ or r_) else ("non_verifie", "compte non visité", 0, 0)
                par_session.append((nom, e_[0], e_[1]))
            verif = [x for x in par_session if x[1] != "non_verifie"]
            manque = [x for x in verif if x[1] in ("absent", "partiel")]
            if not verif:
                etat, detail = "non_verifie", (par_session[0][2] if par_session else "compte non visité")
            elif len(manque) >= MIN_SESSIONS:
                etat, detail = "absent_repete", f"absent ou partiel dans {len(manque)}/{len(verif)} sessions"
            elif manque and len(verif) >= MIN_SESSIONS:
                etat, detail = "isole", f"absent dans 1 session sur {len(verif)} ({manque[0][2]}), présent dans les autres"
            elif manque:
                etat, detail = "a_confirmer", f"{manque[0][2]} (une seule session vérifiée)"
            else:
                etat, detail = "present", f"présent dans {len(verif)} session(s)"
        else:
            etat, detail = "sans_objet", "T6 non testable sur TikTok"
        r, n_mv, n_aut = t7(prof)
        res.append({"plateforme": plat, "groupe": l["groupe"], "auteur": l["auteur"], "t6": etat, "t6_detail": detail,
                    "t6_sessions": par_session, "t7_ratio": r, "t7_n_mouvement": n_mv, "t7_n_autres": n_aut})

    o = ["# Visibilité des comptes (T6 et T7) : résultats agrégés\n",
         f"Généré le {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC. Comptes désignés par un code ; "
         "aucun nom n'est publié.\n",
         "## T6 : présence dans la recherche « from:compte » (onglet Récent)\n",
         f"Sessions : {', '.join(n for n, _ in sessions) or 'aucune'}. On compare les posts originaux des "
         f"{FENETRE_T6_H} dernières heures du profil à la recherche. Un compte n'est compté « absent » que s'il "
         f"l'est dans au moins {MIN_SESSIONS} sessions : une recherche vide une seule fois est le plus souvent "
         "une erreur passagère de X (vu sur des témoins).\n",
         "| groupe | comptes vérifiés | présents | absents (répété) | absents une seule fois | à confirmer | non vérifiés |",
         "|---|---|---|---|---|---|---|"]
    verdicts = []
    res_x = [x for x in res if x["plateforme"] == "x"]
    par_g = collections.defaultdict(collections.Counter)
    for x in res_x:
        par_g[x["groupe"]][x["t6"]] += 1
    cles = ("present", "absent_repete", "isole", "a_confirmer")
    for g, c in sorted(par_g.items()):
        o.append(f"| {g} | {sum(c[k] for k in cles)} | {c['present']} | {c['absent_repete']} | {c['isole']} | "
                 f"{c['a_confirmer']} | {c['non_verifie']} |")
    n_verif = sum(c[k] for c in par_g.values() for k in cles)
    n_abs = sum(c["absent_repete"] for c in par_g.values())
    n_iso = sum(c["isole"] + c["a_confirmer"] for c in par_g.values())
    iso_g = " ; ".join(f"{g} {c['isole'] + c['a_confirmer']}" for g, c in sorted(par_g.items()) if c["isole"] + c["a_confirmer"])
    if n_verif == 0:
        v6 = "NON TESTABLE (aucun compte vérifié : profil et recherche « from: » à capturer)"
    elif n_abs == 0:
        v6 = (f"RIEN DÉTECTÉ ({n_verif} comptes vérifiés sur {len(sessions)} session(s), aucun absent de façon répétée"
              + (f" ; {n_iso} absence(s) isolée(s) : {iso_g})" if n_iso else ")"))
    else:
        detail = " ; ".join(f"{g} : {c['absent_repete']}/{sum(c[k] for k in cles)}" for g, c in sorted(par_g.items()))
        v6 = f"**DÉTECTÉ ({n_abs} compte(s) absents de la recherche dans plusieurs sessions)** — {detail}"
        # Comparaison avec les témoins (même principe que T2) : un groupe ne compte que s'il dépasse les témoins
        tm = par_g.get("temoin")
        if tm:
            n_tm, a_tm = sum(tm[k] for k in cles), tm["absent_repete"]
            comp = []
            for g, c in sorted(par_g.items()):
                if g == "temoin":
                    continue
                n_g, a_g = sum(c[k] for k in cles), c["absent_repete"]
                if n_g and n_tm:
                    p = fisher_bilateral(a_g, n_g - a_g, a_tm, n_tm - a_tm)
                    plus = a_g / n_g > a_tm / n_tm and p < 0.05
                    comp.append(f"{g} {a_g}/{n_g} contre témoins {a_tm}/{n_tm}, p = {p:.2f}"
                                + (" (plus que les témoins)" if plus else ""))
            if comp:
                aucun = all("plus que les témoins" not in x for x in comp)
                v6 += (" → **pas plus que chez les témoins** : " if aucun else " → ") + " ; ".join(comp)
    verdicts.append({"test": "T6", "plateforme": "x", "verdict": v6})
    o.append(f"\n**Verdict T6 (X)** : {v6}\n")
    o.append("Détail par compte :\n")
    for x in sorted(res_x, key=lambda x: (x["groupe"], x["t6"])):
        o.append(f"- `{x['auteur']}` ({x['groupe']}) : {x['t6']} — {x['t6_detail']}"
                 + ("" if len(x["t6_sessions"]) < 2 else " [" + ", ".join(e for _, e, _ in x["t6_sessions"]) + "]"))
    o.append("\nT6 n'est pas testable sur TikTok : sa recherche ne permet pas de lister les vidéos d'un compte, "
             "et ses pages de hashtag sont triées par popularité.\n")

    o.append("## T7 : portée comparée (vues des posts sur le mouvement / vues des autres posts du même compte)\n")
    o.append(f"Posts originaux de plus de {AGE_MIN_H} h et de moins de 30 jours ; au moins 2 posts dans chaque catégorie. "
             "Un rapport inférieur à 1 veut dire que les posts sur le mouvement sont moins vus que les autres posts du même compte.\n")
    v7s = {}
    for plat, nom in (("x", "X"), ("tiktok", "TikTok")):
        rp = [x for x in res if x["plateforme"] == plat]
        if not rp:
            continue
        o.append(f"### {nom}\n")
        o.append("| groupe | comptes comparables | rapport médian | comptes avec rapport < 1 | p (test du signe) |")
        o.append("|---|---|---|---|---|")
        v7_parts, v7_signal, n7_tot = [], False, 0
        for g in sorted({x["groupe"] for x in rp}):
            rs = [x["t7_ratio"] for x in rp if x["groupe"] == g and x["t7_ratio"] is not None]
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
            v7 = ("**DÉTECTÉ (posts sur le mouvement significativement moins vus que les autres posts des mêmes comptes)** — "
                  + " ; ".join(v7_parts))
        else:
            v7 = "RIEN DÉTECTÉ (pas d'écart significatif) — " + " ; ".join(v7_parts)
        verdicts.append({"test": "T7", "plateforme": plat, "verdict": v7})
        v7s[nom] = v7
        o.append(f"\n**Verdict T7 ({nom})** : {v7}\n")
    v7 = " | ".join(f"{k} : {v}" for k, v in v7s.items()) or "NON TESTABLE (aucun profil capturé)"
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
