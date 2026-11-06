#!/usr/bin/env python3
"""
analyse_contenus.py — tableau de verdicts « test × plateforme » pour les
formes de censure 2 (retrait de contenus) et 3 (visibilité réduite).

Entrées :
  contenus_*.csv   produits par contenus.py (un fichier par point de mesure)
  --recherches     (facultatif) relevé manuel du test 5, voir recherches_modele.csv
  --dsa            (facultatif) résultats du test 3/4, produits par dsa.py

Chaque case du tableau prend UNE de ces valeurs :
  RIEN DÉTECTÉ      le test a pu être mené et n'a rien trouvé
  DÉTECTÉ (n)       le test a trouvé n cas, listés en détail plus bas
  NON TESTABLE      le test n'a pas pu être mené (raison donnée)
  À VENIR           données pas encore disponibles

« Détecté » décrit ce que la plateforme affiche ou ce qui diffère entre pays.
Ce n'est une preuve d'intervention de l'État que si la plateforme l'indique
elle-même (mention de demande légale).

  python3 analyse_contenus.py "contenus_*.csv" --recherches recherches.csv
"""
import argparse
import collections
import csv
import datetime as dt
import glob
import os
import sys

PLATEFORMES = ["x", "tiktok", "instagram", "youtube"]
NOMS = {"x": "X", "tiktok": "TikTok", "instagram": "Instagram", "youtube": "YouTube"}
MOTIFS = ["retenu_pays", "compte_suspendu", "retire_regles", "supprime_auteur", "prive"]
NON_VISIBLE = set(MOTIFS) | {"indisponible"}
TECHNIQUE = {"anti_robot", "non_reconnu", "erreur_reseau"}
PAR_PLATEFORME = {"retenu_pays", "compte_suspendu", "retire_regles"}
LIB = {"retenu_pays": "retenu dans le pays", "compte_suspendu": "compte suspendu",
       "retire_regles": "retiré pour violation des règles", "supprime_auteur": "supprimé par l'auteur",
       "prive": "passé en privé", "indisponible": "indisponible sans motif"}


def ts(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def etat_combine(lignes):
    """Un état par post, par passage et par point, à partir des méthodes."""
    etats = [l["etat"] for l in lignes]
    legal = any(l["mention_legale"] == "oui" for l in lignes)
    for e in MOTIFS:
        if e in etats:
            return e, legal
    if "visible" in etats:
        return "visible", legal
    if "indisponible" in etats:
        return "indisponible", legal
    return (etats[0] if etats else "non_reconnu"), legal


def lire(fichiers):
    obs = collections.defaultdict(list)  # (vantage, round, id) -> lignes
    info = {}
    for f in fichiers:
        with open(f, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                obs[(r["vantage"], r["round_id"], r["id"])].append(r)
                info[r["id"]] = (r["plateforme"].replace("twitter", "x"), r["categorie"], r["url"])
    passages = collections.defaultdict(dict)  # id -> vantage -> [(t, etat, legal, loc)]
    for (v, rid, pid), ls in obs.items():
        e, legal = etat_combine(ls)
        passages[pid].setdefault(v, []).append((ts(ls[0]["ts_utc"]), e, legal, ls[0]["loc"], ls))
    for pid in passages:
        for v in passages[pid]:
            passages[pid][v].sort(key=lambda x: x[0])
    return passages, info


def points(passages):
    """Sépare les points en France et à l'étranger d'après la localisation Cloudflare."""
    loc = collections.defaultdict(collections.Counter)
    for pid, pv in passages.items():
        for v, lst in pv.items():
            for p in lst:
                loc[v][p[3]] += 1
    fr = [v for v, c in loc.items() if c.most_common(1)[0][0] == "FR"]
    etr = [v for v, c in loc.items() if c.most_common(1)[0][0] not in ("FR", "?")]
    return fr, etr, loc


def test1(passages, info, fr, etr):
    """Retenu en France : non visible (ou mention légale) en France, visible à l'étranger au même moment."""
    res = {p: {"cas": [], "paires": 0, "posts": set(), "tech": collections.Counter()} for p in PLATEFORMES}
    for pid, pv in passages.items():
        plat, cat, url = info[pid]
        if plat not in res or cat == "controle":
            continue
        for vf in fr:
            for (t, e, legal, _, _) in pv.get(vf, []):
                if e in TECHNIQUE:
                    res[plat]["tech"][e] += 1
                    continue
                for ve in etr:
                    proches = [x for x in pv.get(ve, []) if abs((x[0] - t).total_seconds()) <= 3 * 3600]
                    if not proches:
                        continue
                    x = min(proches, key=lambda x: abs((x[0] - t).total_seconds()))
                    if x[1] in TECHNIQUE:
                        res[plat]["tech"][x[1]] += 1
                        continue
                    res[plat]["paires"] += 1
                    res[plat]["posts"].add(pid)
                    if (e != "visible" and x[1] == "visible") or e == "retenu_pays" or legal:
                        res[plat]["cas"].append({"id": pid, "categorie": cat, "url": url, "t": t, "fr": e,
                                                 "etranger": f"{ve}={x[1]}", "legal": legal})
    return res


def test2(passages, info, fr):
    """Disparitions : visible au premier passage testable, puis non visible ensuite (point français)."""
    res = {p: {"mouvement": [0, []], "temoin": [0, []], "deja": 0, "suivis": 0} for p in PLATEFORMES}
    for pid, pv in passages.items():
        plat, cat, url = info[pid]
        if plat not in res or cat == "controle":
            continue
        cat = "temoin" if cat.startswith("temoin") else "mouvement"
        serie = sorted([p for v in fr for p in pv.get(v, []) if p[1] not in TECHNIQUE], key=lambda x: x[0])
        if not serie:
            continue
        if serie[0][1] != "visible":
            res[plat]["deja"] += 1
            continue
        res[plat]["suivis"] += 1
        res[plat][cat][0] += 1
        fin = next((p for p in serie[1:] if p[1] in NON_VISIBLE), None)
        if fin:
            res[plat][cat][1].append({"id": pid, "url": url, "t": fin[0], "motif": fin[1], "legal": fin[2]})
    return res


def test5(path):
    if not path or not os.path.exists(path):
        return None
    lignes = list(csv.DictReader(open(path, newline="", encoding="utf-8-sig")))
    res = {p: {"cas": [], "paires": 0} for p in PLATEFORMES}
    par = collections.defaultdict(dict)
    for r in lignes:
        cle = (r["plateforme"].lower().replace("twitter", "x"), r["requete"].strip().lower(), r["date_heure"][:13])
        par[cle][r["pays"].upper()] = r
    for (plat, req, h), d in par.items():
        if plat not in res or "FR" not in d or len(d) < 2:
            continue
        res[plat]["paires"] += 1
        fr_r = d["FR"]["resultat"]
        autres = [x["resultat"] for k, x in d.items() if k != "FR"]
        if fr_r in ("aucun_resultat", "message_restriction") and "resultats" in autres:
            res[plat]["cas"].append({"requete": req, "heure": h, "categorie": d["FR"].get("categorie", ""),
                                     "fr": fr_r, "capture": d["FR"].get("capture", "")})
    return res


def case_t1(r):
    if not r.get("n_posts"):
        return "NON TESTABLE (aucun post de cette plateforme dans le corpus)"
    if r["paires"] == 0:
        raisons = ", ".join(f"{k} ×{n}" for k, n in r["tech"].most_common(3)) or "aucune comparaison France/étranger"
        return f"NON TESTABLE ({raisons})"
    if r["cas"]:
        posts = {}
        for c in r["cas"]:
            posts.setdefault(c["id"], c)
            if c["legal"] or c["fr"] == "retenu_pays":
                posts[c["id"]] = {**posts[c["id"]], "legal": True}
        mv = sum(1 for c in posts.values() if not c["categorie"].startswith("temoin"))
        lg = sum(1 for c in posts.values() if c["legal"])
        return (f"**DÉTECTÉ ({len(posts)} post(s))** : {mv} du mouvement, {len(posts) - mv} témoin(s) ; "
                f"{lg} avec mention légale")
    return f"RIEN DÉTECTÉ ({len(r['posts'])} posts, {r['paires']} comparaisons)"


def case_t2(r):
    if not r.get("n_posts"):
        return "NON TESTABLE (aucun post de cette plateforme dans le corpus)"
    if r["suivis"] == 0:
        return "NON TESTABLE (aucun post vérifiable depuis la France)"
    def detail(cat):
        n, lst = r[cat]
        if not lst:
            return f"0/{n}"
        c = collections.Counter(x["motif"] for x in lst)
        return f"{len(lst)}/{n} (" + ", ".join(f"{LIB[k]} {v}" for k, v in c.most_common()) + ")"
    mv, tm = r["mouvement"][1], r["temoin"][1]
    if not mv and not tm:
        return f"RIEN DÉTECTÉ ({r['suivis']} posts suivis)"
    plat_mv = sum(1 for x in mv if x["motif"] in PAR_PLATEFORME)
    plat_tm = sum(1 for x in tm if x["motif"] in PAR_PLATEFORME)
    return (f"**DÉTECTÉ** mouvement {detail('mouvement')} ; témoins {detail('temoin')}. "
            f"Retraits par la plateforme : mouvement {plat_mv}, témoins {plat_tm}")


def case_t5(r):
    if r is None:
        return "À VENIR (relevé manuel)"
    if r["paires"] == 0:
        return "NON TESTABLE (aucune recherche faite à la même heure en France et à l'étranger)"
    if r["cas"]:
        return f"**DÉTECTÉ ({len(r['cas'])})** : aucun résultat ou restriction en France seulement"
    return f"RIEN DÉTECTÉ ({r['paires']} comparaisons)"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", nargs="+")
    ap.add_argument("--recherches", default="recherches.csv")
    ap.add_argument("--resultats", nargs="*", default=["dsa_resultats.csv", "resultats_t6_t7.csv"],
                    help="fichiers de verdicts produits par d'autres scripts (test,plateforme,verdict)")
    ap.add_argument("--out", default="rapport/contenus.md")
    ap.add_argument("--corpus", default="contenus/corpus.csv", help="pour la période de chaque post (T2 par période)")
    a = ap.parse_args()
    fichiers = sorted({f for m in a.csv for f in (glob.glob(m) or [m])})
    passages, info = lire(fichiers)
    if not passages:
        sys.exit("Aucune donnée.")
    fr, etr, loc = points(passages)
    t1, t2, t5 = test1(passages, info, fr, etr), test2(passages, info, fr), test5(a.recherches)
    n_posts = collections.Counter(info[pid][0] for pid in passages)
    for p in PLATEFORMES:
        t1[p]["n_posts"] = t2[p]["n_posts"] = n_posts.get(p, 0)
    dsa = {}
    for fr_ in a.resultats:
        if os.path.exists(fr_):
            for r in csv.DictReader(open(fr_, newline="", encoding="utf-8")):
                dsa[(r["test"], r["plateforme"])] = r["verdict"]

    o = ["# Retrait de contenus et visibilité : verdicts par test et par plateforme\n",
         f"Points de mesure : France = {', '.join(fr) or 'aucun'} ; étranger = {', '.join(etr) or 'aucun'} "
         f"(localisation vue par Cloudflare : " + "; ".join(f"{v} → {dict(c)}" for v, c in loc.items()) + ").\n",
         "| test | forme | " + " | ".join(NOMS[p] for p in PLATEFORMES) + " |",
         "|---|---|" + "---|" * len(PLATEFORMES)]
    o.append("| **T1** Retenu en France (visible à l'étranger, pas en France) | 2 | "
             + " | ".join(case_t1(t1[p]) for p in PLATEFORMES) + " |")
    o.append("| **T2** Disparitions (visible puis plus visible), avec motif | 2 | "
             + " | ".join(case_t2(t2[p]) for p in PLATEFORMES) + " |")
    o.append("| **T3** Décisions de modération déclarées (base DSA), France | 2 | "
             + " | ".join(dsa.get(("T3", p), "À VENIR (base DSA)") for p in PLATEFORMES) + " |")
    o.append("| **T4** Déclassements déclarés (base DSA), France | 3 | "
             + " | ".join(dsa.get(("T4", p), "À VENIR (base DSA)") for p in PLATEFORMES) + " |")
    o.append("| **T5** Recherches : aucun résultat en France seulement | 3 | "
             + " | ".join(case_t5(t5[p] if t5 else None) for p in PLATEFORMES) + " |")
    defaut6 = {"x": "À VENIR (session comptes)", "tiktok": "NON TESTABLE (pas de recherche par auteur fiable)",
               "instagram": "NON TESTABLE (pas de recherche par auteur fiable)", "youtube": "NON TESTABLE (hors périmètre)"}
    o.append("| **T6** Comptes absents de la recherche « from: » (search ban) | 3 | "
             + " | ".join(dsa.get(("T6", p), defaut6[p]) for p in PLATEFORMES) + " |")
    defaut7 = {"x": "À VENIR (session comptes)", "tiktok": "À VENIR (profils à capturer)",
               "instagram": "NON TESTABLE (vues non publiques pour les posts)", "youtube": "NON TESTABLE (hors périmètre)"}
    o.append("| **T7** Posts sur le mouvement moins vus que les autres posts du même compte | 3 | "
             + " | ".join(dsa.get(("T7", p), defaut7[p]) for p in PLATEFORMES) + " |")
    o.append("")
    o.append("**Lecture.** DÉTECTÉ décrit ce que la plateforme affiche, ou ce qui diffère entre pays. "
             "L'origine (demande de l'État ou décision de la plateforme) n'est établie **que** par une mention "
             "légale affichée par la plateforme, ou par une demande publiée (Lumen, rapports de transparence). "
             "Une disparition côté « mouvement » ne compte que si elle dépasse nettement celle des témoins.\n")

    o.append("## Détail T1 : retenus en France\n")
    for p in PLATEFORMES:
        vus = set()
        for c in t1[p]["cas"]:
            if c["id"] in vus:
                continue
            vus.add(c["id"])
            o.append(f"- {NOMS[p]} `{c['id']}` ({c['categorie']}) {c['t']:%d/%m %H:%M} UTC : France = {c['fr']}"
                     f"{' (mention légale)' if c['legal'] else ''}, {c['etranger']} — {c['url']}")
    o.append("")
    o.append("## Détail T2 : disparitions\n")
    for p in PLATEFORMES:
        for cat in ("mouvement", "temoin"):
            for c in t2[p][cat][1]:
                o.append(f"- {NOMS[p]} `{c['id']}` ({cat}) {c['t']:%d/%m %H:%M} UTC : {LIB[c['motif']]}"
                         f"{' (mention légale)' if c['legal'] else ''} — {c['url']}")
        if t2[p]["deja"]:
            o.append(f"- {NOMS[p]} : {t2[p]['deja']} post(s) déjà non visibles au premier passage (exclus).")
    o.append("")
    # Contrôles positifs : l'outil voit-il une suppression / une rétention connue ?
    ctrl = [pid for pid in passages if info[pid][1] == "controle"]
    o.append("## Contrôles positifs\n")
    if not ctrl:
        o.append("Aucun contrôle positif dans le corpus : on ne sait pas encore si l'outil détecte une "
                 "suppression ou une rétention (voir contenus/PROTOCOLE_T6_T7.md et ajouts_manuels.txt).\n")
    for pid in sorted(ctrl):
        plat, _, url = info[pid]
        for v, lst in sorted(passages[pid].items()):
            suite = " → ".join(f"{x[0]:%d/%m %H:%M} {x[1]}{' (légal)' if x[2] else ''}" for x in lst)
            o.append(f"- {NOMS.get(plat, plat)} `{pid}` depuis {v} : {suite}")
    o.append("")

    # T2 par période : taux de disparition comparés à âge égal
    periodes = {}
    if os.path.exists(a.corpus):
        for r in csv.DictReader(open(a.corpus, newline="", encoding="utf-8")):
            d = r.get("date_post", "")
            periodes[r["id"]] = ("1. 17-19 oct" if d and d <= "2026-10-19" else "2. 22-26 oct" if d and d <= "2026-10-26"
                                 else "3. 27 oct-4 nov" if d and d < "2026-11-05" else "4. 5 nov et après" if d else "?")
    if periodes:
        o.append("## T2 par période de publication (disparus / suivis)\n")
        o.append("Comparer à âge égal : un post ancien et un post récent n'ont pas le même risque d'être supprimé.\n")
        o.append("| réseau | période | mouvement | revendication | témoins |")
        o.append("|---|---|---|---|---|")
        tab = collections.defaultdict(lambda: [0, 0])
        for pid, pv in passages.items():
            plat, cat, _ = info[pid]
            if cat == "controle":
                continue
            cat = "temoin" if cat.startswith("temoin") else cat
            serie = sorted([x for v in fr for x in pv.get(v, []) if x[1] not in TECHNIQUE], key=lambda x: x[0])
            if not serie or serie[0][1] != "visible":
                continue
            k = (plat, periodes.get(pid, "?"), cat)
            tab[k][1] += 1
            if any(x[1] in NON_VISIBLE for x in serie[1:]):
                tab[k][0] += 1
        for plat in PLATEFORMES:
            for per in sorted({k[1] for k in tab if k[0] == plat}):
                cells = []
                for cat in ("mouvement", "revendication", "temoin"):
                    dn = tab.get((plat, per, cat))
                    cells.append(f"{dn[0]}/{dn[1]}" if dn else "—")
                o.append(f"| {NOMS[plat]} | {per} | " + " | ".join(cells) + " |")
        o.append("")
    if t5:
        o.append("## Détail T5 : recherches\n")
        for p in PLATEFORMES:
            for c in t5[p]["cas"]:
                o.append(f"- {NOMS[p]} « {c['requete']} » ({c['categorie']}) {c['heure']}h : France = {c['fr']} "
                         f"— capture {c['capture']}")
        o.append("")
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    open(a.out, "w", encoding="utf-8").write("\n".join(o))
    print(f"Rapport : {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
