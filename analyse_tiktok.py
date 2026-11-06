#!/usr/bin/env python3
"""
analyse_tiktok.py — tests propres à TikTok (forme 3 : visibilité réduite), à
partir des fichiers tiktok_metriques_*.csv écrits par contenus.py (v1.3+).

T8  Indicateurs internes : une vidéo change-t-elle d'indicateur pendant le
    suivi (reviewed, display_penalty_type, display_policy, video_status…) ?
    Comparaison mouvement / témoins (test exact de Fisher).
    Ces champs NE SONT PAS DOCUMENTÉS par TikTok : on constate des changements,
    on ne leur donne pas de sens.

T9  Croissance des vues : à popularité et âge égaux, les vidéos du mouvement
    cessent-elles plus souvent de gagner des vues que les témoins ?
    « Stagnation » = moins de 1 % de vues en plus sur au moins 24 h.
    Test : Cochran-Mantel-Haenszel sur les tranches popularité × âge.
    Une vidéo qui stagne peut simplement avoir fini son buzz : seule une
    différence nette avec les témoins comparables compte.

Sorties : rapport/tiktok.md, resultats_t8_t9.csv (pour analyse_contenus.py)

  python3 analyse_tiktok.py "tiktok_metriques_*.csv" --corpus contenus/corpus.csv
"""
import argparse
import collections
import csv
import datetime as dt
import glob
import math
import os
import statistics
import sys

INDICATEURS = ["reviewed", "display_penalty_type", "display_policy", "display_ui_type", "video_status",
               "ec_global_verdict", "conclu_refine_reason", "is_prohibited", "is_reviewing", "item_control"]
SEUIL_STAGNATION = 0.01   # +1 % de vues
DUREE_MIN_H = 24
TRANCHES_VUES = [(0, 100_000, "< 100 k"), (100_000, 1_000_000, "100 k – 1 M"), (1_000_000, 10 ** 13, "> 1 M")]
TRANCHES_AGE = [(0, 3, "< 3 j"), (3, 14, "3 – 14 j"), (14, 10 ** 5, "> 14 j")]


def fisher(a, b, c, d):
    """p-valeur bilatérale du test exact de Fisher pour [[a, b], [c, d]]."""
    n, r1, c1 = a + b + c + d, a + b, a + c
    if n == 0:
        return 1.0
    def p(k):
        return math.comb(r1, k) * math.comb(n - r1, c1 - k) / math.comb(n, c1)
    p0 = p(a)
    return min(1.0, sum(p(k) for k in range(max(0, c1 - (n - r1)), min(r1, c1) + 1) if p(k) <= p0 + 1e-12))


def cmh(strates):
    """Test de Cochran-Mantel-Haenszel (avec correction de continuité) sur des strates
    [(a, n1, c, n2)] : a stagnent sur n1 (mouvement), c sur n2 (témoins).
    Renvoie (observé, attendu, p) pour le groupe mouvement."""
    obs = att = var = 0.0
    for a_, n1, c_, n2 in strates:
        n, m1 = n1 + n2, a_ + c_
        if n1 == 0 or n2 == 0 or n < 2:
            continue
        obs += a_
        att += n1 * m1 / n
        var += n1 * n2 * m1 * (n - m1) / (n * n * (n - 1))
    if var == 0:
        return obs, att, 1.0
    chi2 = (max(0.0, abs(obs - att) - 0.5)) ** 2 / var
    return obs, att, math.erfc(math.sqrt(chi2 / 2))


def groupe(cat):
    return "temoin" if cat.startswith("temoin") else None if cat == "controle" else "mouvement"


def lire(fichiers, corpus):
    dates = {}
    if corpus and os.path.exists(corpus):
        for r in csv.DictReader(open(corpus, newline="", encoding="utf-8")):
            if r.get("date_post"):
                dates[r["id"]] = dt.datetime.fromisoformat(r["date_post"])
    series = collections.defaultdict(list)
    for f in fichiers:
        for r in csv.DictReader(open(f, newline="", encoding="utf-8")):
            r["_t"] = dt.datetime.strptime(r["ts_utc"], "%Y-%m-%dT%H:%M:%SZ")
            try:
                r["_vues"] = int(r["vues"])
            except (TypeError, ValueError):
                r["_vues"] = None
            series[r["id"]].append(r)
    for s in series.values():
        s.sort(key=lambda r: r["_t"])
    return series, dates


def t8(series):
    """Vidéos dont au moins un indicateur change entre deux observations."""
    changes, suivies = [], collections.Counter()
    vus = collections.defaultdict(set)
    for vid, s in series.items():
        g = groupe(s[0]["categorie"])
        if not g or len(s) < 2:
            continue
        suivies[g] += 1
        for k in INDICATEURS:
            vals = [r.get(k, "") for r in s]
            for prec, cour, r in zip(vals, vals[1:], s[1:]):
                if prec != cour:
                    changes.append({"id": vid, "groupe": g, "indicateur": k, "avant": prec, "apres": cour,
                                    "t": r["_t"], "point": r["vantage"]})
                    vus[g].add(vid)
    return changes, suivies, vus


def t9(series, dates):
    """Stagnation des vues par tranche de popularité et d'âge."""
    lignes = []
    for vid, s in series.items():
        g = groupe(s[0]["categorie"])
        obs = [r for r in s if r["_vues"] is not None]
        if not g or len(obs) < 2:
            continue
        debut, fin = obs[0], obs[-1]
        h = (fin["_t"] - debut["_t"]).total_seconds() / 3600
        if h < DUREE_MIN_H or not debut["_vues"]:
            continue
        croissance = (fin["_vues"] - debut["_vues"]) / debut["_vues"]
        age = (debut["_t"] - dates[vid]).days if vid in dates else None
        tv = next(l for a, b, l in TRANCHES_VUES if a <= debut["_vues"] < b)
        ta = next((l for a, b, l in TRANCHES_AGE if age is not None and a <= age < b), "âge inconnu")
        lignes.append({"id": vid, "groupe": g, "tranche_vues": tv, "tranche_age": ta, "heures": h,
                       "croissance_jour": croissance / (h / 24), "stagne": croissance < SEUIL_STAGNATION})
    return lignes


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", nargs="+")
    ap.add_argument("--corpus", default="contenus/corpus.csv")
    a = ap.parse_args()
    fichiers = sorted({f for m in a.csv for f in (glob.glob(m) or [m])})
    series, dates = lire(fichiers, a.corpus)
    if not series:
        sys.exit("Aucune donnée TikTok.")
    changes, suivies, vus = t8(series)
    croiss = t9(series, dates)

    o = ["# TikTok : indicateurs internes (T8) et croissance des vues (T9)\n",
         f"Généré le {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC à partir de {len(series)} vidéos suivies.\n",
         "## T8 : changements d'indicateurs internes pendant le suivi\n",
         "⚠️ Champs **non documentés** par TikTok : on constate qu'ils changent, on ne leur donne pas de sens.\n",
         "| groupe | vidéos suivies (≥ 2 observations) | vidéos avec au moins un changement |", "|---|---|---|"]
    for g in ("mouvement", "temoin"):
        o.append(f"| {g} | {suivies[g]} | {len(vus[g])} |")
    a_, b_ = len(vus["mouvement"]), suivies["mouvement"] - len(vus["mouvement"])
    c_, d_ = len(vus["temoin"]), suivies["temoin"] - len(vus["temoin"])
    p8 = fisher(a_, b_, c_, d_)
    if suivies["mouvement"] == 0 or suivies["temoin"] == 0:
        v8 = "NON TESTABLE (il faut au moins deux passages sur des vidéos du mouvement et des témoins)"
    elif a_ + c_ == 0:
        v8 = f"RIEN DÉTECTÉ (aucun changement sur {suivies['mouvement'] + suivies['temoin']} vidéos suivies)"
    elif p8 < 0.05 and a_ / max(1, suivies["mouvement"]) > c_ / max(1, suivies["temoin"]):
        v8 = (f"**DÉTECTÉ** : {a_}/{suivies['mouvement']} vidéos du mouvement ont changé d'indicateur, "
              f"contre {c_}/{suivies['temoin']} témoins (p = {p8:.3f}). Sens des indicateurs inconnu")
    else:
        v8 = (f"RIEN DÉTECTÉ (pas d'écart significatif : mouvement {a_}/{suivies['mouvement']}, "
              f"témoins {c_}/{suivies['temoin']}, p = {p8:.3f})")
    o.append(f"\n**Verdict T8 (TikTok)** : {v8}\n")
    if changes:
        o.append("| indicateur | changement | mouvement | témoins |")
        o.append("|---|---|---|---|")
        cc = collections.Counter((c["indicateur"], f"{c['avant']} → {c['apres']}", c["groupe"]) for c in changes)
        for (ind, ch) in sorted({(k[0], k[1]) for k in cc}):
            o.append(f"| {ind} | {ch} | {cc.get((ind, ch, 'mouvement'), 0)} | {cc.get((ind, ch, 'temoin'), 0)} |")
        o.append("")

    o.append("## T9 : stagnation des vues, à popularité et âge égaux\n")
    o.append(f"Stagnation : moins de {SEUIL_STAGNATION:.0%} de vues en plus sur au moins {DUREE_MIN_H} h de suivi. "
             "Popularité et âge mesurés à la première observation.\n")
    o.append("| popularité | âge | mouvement : stagnent / suivies | témoins : stagnent / suivies | p (Fisher) |")
    o.append("|---|---|---|---|---|")
    strat = collections.defaultdict(lambda: {"mouvement": [0, 0], "temoin": [0, 0]})
    for l in croiss:
        k = (l["tranche_vues"], l["tranche_age"])
        strat[k][l["groupe"]][1] += 1
        strat[k][l["groupe"]][0] += int(l["stagne"])
    strates, nm_tot, nt_tot, sm_tot, st_tot = [], 0, 0, 0, 0
    for (tv, ta), d in sorted(strat.items()):
        (sm, nm), (stt, nt) = d["mouvement"], d["temoin"]
        o.append(f"| {tv} | {ta} | {sm}/{nm} | {stt}/{nt} | {'—' if not (nm and nt) else f'{fisher(sm, nm - sm, stt, nt - stt):.3f}'} |")
        if nm and nt:  # seules les tranches où les deux groupes sont présents comptent
            strates.append((sm, nm, stt, nt))
            nm_tot, nt_tot, sm_tot, st_tot = nm_tot + nm, nt_tot + nt, sm_tot + sm, st_tot + stt
    obs, att, p9 = cmh(strates)
    o.append(f"\nTest global, tranche par tranche combinées (Cochran-Mantel-Haenszel), sur les tranches où les deux "
             f"groupes sont présents : mouvement {sm_tot}/{nm_tot} stagnent, témoins {st_tot}/{nt_tot} ; "
             f"stagnations du mouvement observées {obs:.0f}, attendues à traitement égal {att:.1f}, p = {p9:.4f}.\n")
    if nm_tot < 10 or nt_tot < 10:
        v9 = (f"NON TESTABLE (trop peu de vidéos comparables suivies ≥ {DUREE_MIN_H} h : "
              f"mouvement {nm_tot}, témoins {nt_tot} ; il en faut au moins 10 de chaque)")
    elif p9 < 0.05 and obs > att:
        v9 = (f"**DÉTECTÉ** : à popularité et âge égaux, les vidéos du mouvement stagnent plus souvent "
              f"({sm_tot}/{nm_tot}) que les témoins ({st_tot}/{nt_tot}) ; observé {obs:.0f}, attendu {att:.1f}, p = {p9:.4f}")
    else:
        v9 = (f"RIEN DÉTECTÉ (mouvement {sm_tot}/{nm_tot}, témoins {st_tot}/{nt_tot} à popularité et âge égaux, "
              f"p = {p9:.3f})")
    o.append(f"\n**Verdict T9 (TikTok)** : {v9}\n")
    o.append("**Lecture.** T8 et T9 décrivent des différences de traitement ou de diffusion. Ils ne disent ni ce "
             "que signifient les indicateurs internes, ni qui a décidé. La modération ordinaire (contenus violents, "
             "signalements) peut produire les mêmes écarts.\n")
    os.makedirs("rapport", exist_ok=True)
    open(os.path.join("rapport", "tiktok.md"), "w", encoding="utf-8").write("\n".join(o))
    with open("resultats_t8_t9.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["test", "plateforme", "verdict"])
        w.writeheader()
        w.writerow({"test": "T8", "plateforme": "tiktok", "verdict": v8})
        w.writerow({"test": "T9", "plateforme": "tiktok", "verdict": v9})
    print(f"T8 : {v8}\nT9 : {v9}\nÉcrits : rapport/tiktok.md, resultats_t8_t9.csv", file=sys.stderr)


if __name__ == "__main__":
    main()
