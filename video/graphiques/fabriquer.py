#!/usr/bin/env python3
"""
fabriquer.py — fabrique les graphiques de la vidéo (PNG 1920×1080, fond sombre).

Les codes (S05_G01…) sont ceux de video/PLANS.md. Les chiffres viennent des rapports
(journal de bord) ; les frises et les séries viennent des fichiers de mesures, passés
en options. Un graphique dont les données manquent est sauté, avec un message.

  python3 video/graphiques/fabriquer.py \\
      --mesures-fixe mesures_fixe.csv --mesures-vps mesures_vps.csv \\
      --episodes rapport/episodes.csv --dsa dsa_jours.csv \\
      --sessions-t6 exports/collecteur-t6-*.ndjson
Rendu : Chromium (Playwright pour Node), installé à part.
"""
import argparse
import collections
import csv
import datetime as dt
import glob
import html
import json
import os
import shutil
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1080

# Couleurs (palette validée pour fond sombre ; voir la skill dataviz)
C = {
    "fond": "#1a1a19", "carte": "#242422", "trait": "#383835", "texte": "#f0efec", "texte2": "#c3c2b7",
    "discret": "#8e8d86", "mvt": "#3987e5", "tem": "#d95926",
    "ok": "#0ca30c", "bloque": "#d03b3b", "signal": "#fab219", "vide": "#2c2c2a",
    "doc": "#199e70", "annonce": "#c98500", "rumeur": "#9085e9",
}

CSS = f"""
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; width: {W}px; height: {H}px; background: {C['fond']}; color: {C['texte']};
  font-family: Inter, 'DejaVu Sans', sans-serif; overflow: hidden; }}
.page {{ position: absolute; inset: 0; padding: 100px 140px 90px; display: flex; flex-direction: column; }}
h1 {{ font-size: 60px; font-weight: 700; margin: 0 0 18px; letter-spacing: -0.5px; line-height: 1.1; }}
.sous {{ font-size: 34px; color: {C['texte2']}; margin: 0 0 40px; line-height: 1.35; }}
.source {{ position: absolute; left: 140px; bottom: 44px; font-size: 24px; color: {C['discret']}; }}
.mono {{ font-family: 'DejaVu Sans Mono', monospace; }}
.carte {{ background: {C['carte']}; border-radius: 20px; padding: 40px 44px; }}
.etiq {{ display: inline-block; font-size: 24px; font-weight: 700; letter-spacing: 1.5px; padding: 8px 16px;
  border-radius: 8px; border: 2px solid currentColor; }}
.grand {{ font-size: 150px; font-weight: 800; line-height: 1; letter-spacing: -3px; }}
.ligne {{ display: flex; gap: 40px; }}
.f1 {{ flex: 1; }}
.ok {{ color: {C['ok']}; }} .ko {{ color: {C['bloque']}; }} .sig {{ color: {C['signal']}; }}
.mvt {{ color: {C['mvt']}; }} .tem {{ color: {C['tem']}; }} .d {{ color: {C['texte2']}; }} .m {{ color: {C['discret']}; }}
.pastille {{ display: inline-block; width: 26px; height: 26px; border-radius: 6px; vertical-align: -3px; margin-right: 12px; }}
table.t {{ border-collapse: collapse; width: 100%; font-size: 34px; }}
table.t td, table.t th {{ padding: 20px 22px; border-bottom: 2px solid {C['trait']}; text-align: left; vertical-align: top; }}
table.t th {{ font-size: 26px; color: {C['discret']}; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; }}
"""

GRAPHIQUES = {}


def graphique(code):
    def deco(f):
        GRAPHIQUES[code] = f
        return f
    return deco


def page(corps, titre=None, sous=None, source=None):
    t = f"<h1>{titre}</h1>" if titre else ""
    s = f"<p class='sous'>{sous}</p>" if sous else ""
    src = f"<div class='source'>{source}</div>" if source else ""
    return (f"<!doctype html><html lang='fr'><head><meta charset='utf-8'><style>{CSS}</style></head>"
            f"<body><div class='page'>{t}{s}{corps}</div>{src}</body></html>")


def esc(x):
    return html.escape(str(x))


def nb(x, dec=0):
    """Nombre à la française : espace pour les milliers, virgule décimale."""
    s = f"{x:,.{dec}f}".replace(",", " ").replace(".", ",")
    return s


# ---------------------------------------------------------------- séquence 0 et 2

@graphique("S00_G01")
def cartons(d):
    cartes = [("PROUVÉ", "mesuré, répété, recoupé", C["texte"], "solid"),
              ("NON PROUVÉ", "rien vu, dans ce qui a été mesuré", C["texte2"], "solid"),
              ("NON TESTABLE", "impossible à mesurer de l'extérieur", C["discret"], "dashed")]
    corps = "<div class='ligne' style='margin-top:auto;margin-bottom:auto'>" + "".join(
        f"<div class='carte f1' style='border:4px {st} {col};text-align:center;padding:80px 30px'>"
        f"<div style='font-size:64px;font-weight:800;color:{col};letter-spacing:1px'>{t}</div>"
        f"<div style='font-size:32px;color:{C['texte2']};margin-top:28px'>{s}</div></div>"
        for t, s, col, st in cartes) + "</div>"
    return page(corps)


TROIS_FORMES = [
    ("1", "Couper l'accès", "tiktok.com ne charge plus", "l'opérateur bloque", "se mesure de l'extérieur"),
    ("2", "Supprimer des contenus", "une vidéo précise disparaît", "une autorité demande le retrait", "se documente : lois, rapports"),
    ("3", "Réduire la visibilité", "tout marche, mais moins de vues", "« shadowban »", "presque invisible de l'extérieur"),
]


def trois_colonnes(visibles, grises=()):
    cols = []
    for i, (n, titre, ex, qui, preuve) in enumerate(TROIS_FORMES):
        if i >= visibles:
            cols.append("<div class='f1'></div>")
            continue
        op = "0.28" if i in grises else "1"
        cols.append(f"<div class='carte f1' style='opacity:{op};display:flex;flex-direction:column;gap:26px'>"
                    f"<div style='font-size:110px;font-weight:800;color:{C['mvt']};line-height:1'>{n}</div>"
                    f"<div style='font-size:52px;font-weight:700;line-height:1.1'>{titre}</div>"
                    f"<div style='font-size:32px;color:{C['texte2']}'>{ex}<br>{qui}</div>"
                    f"<div style='margin-top:auto;font-size:30px;font-weight:600'>{preuve}</div></div>")
    return page("<div class='ligne' style='flex:1'>" + "".join(cols) + "</div>",
                titre="« Censure » : trois choses différentes")


@graphique("S02_G01a")
def f2a(d): return trois_colonnes(1)
@graphique("S02_G01b")
def f2b(d): return trois_colonnes(2)
@graphique("S02_G01c")
def f2c(d): return trois_colonnes(3)
@graphique("S02_G02")
def f2g(d): return trois_colonnes(3, grises=(1, 2))
@graphique("S09_G01")
def f9a(d): return trois_colonnes(3)


# ---------------------------------------------------------------- séquence 3 : chronologie

EVENEMENTS = [
    ("17 oct.", "Mobilisation contre la vie chère", "550 000 selon l'Intérieur<br>800 000 selon les organisateurs", "DOCUMENTÉ", "doc"),
    ("22 oct.", "Lettre de Matignon aux opérateurs", "se tenir prêts à suspendre TikTok, Instagram, Snapchat (selon Blast)", "DOCUMENTÉ · PRESSE", "doc"),
    ("24 oct.", "Nouvelle manifestation", "rien de déclenché, selon la presse", "DOCUMENTÉ · PRESSE", "doc"),
    ("27 oct.", "Sénat : amendement n°94", "retrait de contenus sans juge<br>1re lecture, pas encore en vigueur", "DOCUMENTÉ", "doc"),
    ("30 oct.", "Groupe de contact permanent", "Matignon, plateformes, opérateurs", "DOCUMENTÉ · PRESSE", "doc"),
    ("6-7 nov.", "Acte IV", "grèves le vendredi, manifestations le samedi", "ANNONCÉ", "annonce"),
]


def frise(n, rumeur=False):
    x0, x1, y = 120, 1520, 560
    pas = (x1 - x0) / (len(EVENEMENTS) - 1)
    svg = [f"<svg width='1640' height='760' style='position:absolute;left:140px;top:250px'>",
           f"<line x1='{x0 - 60}' y1='{y}' x2='{x1 + 60}' y2='{y}' stroke='{C['trait']}' stroke-width='6' stroke-linecap='round'/>"]
    cartes = []
    for i, (date, titre, detail, statut, cle) in enumerate(EVENEMENTS):
        x = x0 + i * pas
        actif = i < n
        svg.append(f"<circle cx='{x}' cy='{y}' r='{16 if actif else 9}' fill='{C[cle] if actif else C['trait']}'/>")
        svg.append(f"<text x='{x}' y='{y + 70}' fill='{C['texte'] if actif else C['discret']}' font-size='34' "
                   f"font-weight='700' text-anchor='middle' font-family='Inter'>{date}</text>")
        if i == n - 1:
            left = min(max(140 + x - 330, 140), 1920 - 140 - 660)
            cartes.append(f"<div class='carte' style='position:absolute;left:{left}px;top:330px;width:660px;"
                          f"border-top:6px solid {C[cle]}'>"
                          f"<span class='etiq' style='color:{C[cle]}'>{statut}</span>"
                          f"<div style='font-size:42px;font-weight:700;margin-top:20px'>{titre}</div>"
                          f"<div style='font-size:30px;color:{C['texte2']};margin-top:12px'>{detail}</div></div>")
    svg.append("</svg>")
    if rumeur:
        cartes = [f"<div class='carte' style='position:absolute;left:1000px;top:250px;width:780px;border:3px dashed {C['rumeur']}'>"
                  f"<span class='etiq' style='color:{C['rumeur']}'>RUMEUR</span>"
                  f"<div style='font-size:40px;font-weight:700;margin-top:20px'>Le gouvernement « endiguerait » le mouvement sur les réseaux, surtout sur X</div>"
                  f"<div style='font-size:30px;color:{C['texte2']};margin-top:12px'>aucune preuve trouvée · aucun démenti non plus</div></div>"]
    return page("".join(svg) + "".join(cartes), titre="Ce qu'on sait vraiment")


for _i in range(1, len(EVENEMENTS) + 1):
    GRAPHIQUES[f"S03_G01{'abcdef'[_i - 1]}"] = (lambda k: (lambda d: frise(k)))(_i)


@graphique("S03_G02")
def f3r(d): return frise(len(EVENEMENTS) + 1, rumeur=True)


@graphique("S03_G03")
def f3recap(d):
    corps = (f"<div class='ligne' style='flex:1'>"
             f"<div class='carte f1' style='border-top:8px solid {C['doc']}'><span class='etiq' style='color:{C['doc']}'>DOCUMENTÉ</span>"
             f"<ul style='font-size:42px;line-height:1.5;margin-top:36px;padding-left:40px'>"
             f"<li>le gouvernement a <b>préparé</b> une coupure</li><li>un texte sur le retrait de contenus a été voté au Sénat (1re lecture)</li></ul></div>"
             f"<div class='carte f1' style='border-top:8px solid {C['discret']}'><span class='etiq' style='color:{C['discret']}'>PAS DOCUMENTÉ</span>"
             f"<ul style='font-size:42px;line-height:1.5;margin-top:36px;padding-left:40px'>"
             f"<li>qu'une coupure ait <b>eu lieu</b></li></ul>"
             f"<div style='font-size:40px;font-weight:700;color:{C['mvt']};margin-top:60px'>→ c'est ce qu'on va mesurer</div></div></div>")
    return page(corps, titre="Récapitulatif")


# ---------------------------------------------------------------- séquence 4 : l'annuaire

def boite(x, y, w, h, titre, sous="", coul=None, mono=False):
    coul = coul or C["trait"]
    f = "DejaVu Sans Mono" if mono else "Inter"
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='22' fill='{C['carte']}' stroke='{coul}' stroke-width='4'/>"
            f"<text x='{x + w / 2}' y='{y + h / 2 - (12 if sous else -14)}' fill='{C['texte']}' font-size='34' font-weight='700' "
            f"text-anchor='middle' font-family='Inter'>{titre}</text>"
            + (f"<text x='{x + w / 2}' y='{y + h / 2 + 40}' fill='{C['texte2']}' font-size='28' text-anchor='middle' "
               f"font-family='{f}'>{sous}</text>" if sous else ""))


def fleche(x1, y1, x2, y2, texte="", coul=None, mono=True, dy=-22):
    coul = coul or C["texte2"]
    f = "DejaVu Sans Mono" if mono else "Inter"
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{coul}' stroke-width='5' marker-end='url(#pointe)'/>"
            + (f"<text x='{(x1 + x2) / 2}' y='{(y1 + y2) / 2 + dy}' fill='{coul}' font-size='32' text-anchor='middle' "
               f"font-family='{f}'>{texte}</text>" if texte else ""))


DEFS = (f"<defs><marker id='pointe' viewBox='0 0 10 10' refX='8' refY='5' markerWidth='6' markerHeight='6' orient='auto'>"
        f"<path d='M0,0 L10,5 L0,10 z' fill='{C['texte2']}'/></marker></defs>")


def schema(contenu, titre, sous=None):
    return page(f"<svg width='1640' height='720' style='margin-top:10px'>{DEFS}{contenu}</svg>", titre=titre, sous=sous)


@graphique("S04_G01")
def dns1(d):
    c = (boite(40, 220, 380, 200, "Votre téléphone") + boite(1220, 220, 380, 200, "L'annuaire (DNS)", "de votre opérateur")
         + fleche(430, 280, 1210, 280, "tiktok.com ?") + fleche(1210, 370, 430, 370, "→ l'adresse de TikTok", coul=C["ok"], dy=56))
    return schema(c, "1. L'annuaire", "Avant de se connecter, le téléphone demande l'adresse du site.")


@graphique("S04_G02")
def dns2(d):
    c = (boite(40, 220, 380, 200, "Votre téléphone") + boite(1220, 220, 380, 200, "L'annuaire (DNS)", "de votre opérateur", C["bloque"])
         + fleche(430, 280, 1210, 280, "tiktok.com ?") + fleche(1210, 370, 430, 370, "« n'existe pas »", coul=C["bloque"], dy=56))
    return schema(c, "Filtrage DNS : l'annuaire ment", "Le plus simple à mettre en place, et le plus simple à contourner.")


@graphique("S04_G03a")
def dns3(d):
    c = (boite(40, 220, 380, 200, "Votre téléphone") + boite(1220, 220, 380, 200, "tiktok.com", "la bonne adresse")
         + f"<line x1='430' y1='320' x2='1210' y2='320' stroke='{C['texte2']}' stroke-width='5' stroke-dasharray='18 14'/>"
         + f"<g stroke='{C['bloque']}' stroke-width='14' stroke-linecap='round'><line x1='770' y1='260' x2='870' y2='380'/>"
           f"<line x1='870' y1='260' x2='770' y2='380'/></g>")
    return schema(c, "2. Bloquer l'adresse", "L'annuaire dit la vérité, mais la route vers l'adresse est coupée.")


@graphique("S04_G03b")
def dns4(d):
    env = (f"<rect x='520' y='170' width='600' height='330' rx='18' fill='{C['carte']}' stroke='{C['texte2']}' stroke-width='4'/>"
           f"<polyline points='520,170 820,360 1120,170' fill='none' stroke='{C['texte2']}' stroke-width='4'/>"
           f"<text x='820' y='450' fill='{C['signal']}' font-size='44' text-anchor='middle' font-family='DejaVu Sans Mono'>tiktok.com</text>"
           f"<text x='820' y='620' fill='{C['texte2']}' font-size='32' text-anchor='middle' font-family='Inter'>le contenu est chiffré, mais le nom du site passe en clair au début (SNI)</text>")
    return schema(env, "3. Lire le nom sur l'enveloppe", "L'opérateur repère le nom du site et coupe la connexion.")


@graphique("S04_G03c")
def dns5(d):
    c = (boite(40, 220, 420, 200, "Tous les téléphones", "d'une zone") + boite(1220, 220, 380, 200, "Internet mobile", "", C["bloque"])
         + f"<text x='820' y='340' fill='{C['bloque']}' font-size='60' font-weight='800' text-anchor='middle' font-family='Inter'>COUPÉ</text>")
    return schema(c, "La solution brutale", "Couper tout l'internet mobile d'une zone : ça ne vise plus un réseau social, ça vise tout le monde.")


# ---------------------------------------------------------------- séquence 5 : dispositif

@graphique("S05_G01")
def dispositif(d):
    noeuds = [
        ("Ma box Bouygues", "le moniteur réseau, toutes les 5 min", C["mvt"]),
        ("Un serveur chez un hébergeur", "adresse française, hors fournisseurs d'accès grand public : moniteur + suivi des posts", C["mvt"]),
        ("Connexions résidentielles France / États-Unis", "pour comparer ce qu'on voit d'un pays à l'autre (posts)", C["mvt"]),
        ("Mon iPhone, deux SIM", "RED et Cdiscount Mobile, avec OONI Probe", C["mvt"]),
        ("OONI", "les mesures publiques de bénévoles partout en France", C["doc"]),
    ]
    corps = "<div style='display:grid;grid-template-columns:1fr 1fr;gap:30px;flex:1'>" + "".join(
        f"<div class='carte' style='border-left:10px solid {c}{';grid-column:span 2' if i == 4 else ''}'>"
        f"<div style='font-size:44px;font-weight:700'>{t}</div><div style='font-size:30px;color:{C['texte2']};margin-top:14px'>{s}</div></div>"
        for i, (t, s, c) in enumerate(noeuds)) + "</div>"
    return page(corps, titre="Mon dispositif")


@graphique("S05_G02")
def temoins(d):
    pos = ["sputnikglobe.com", "ria.ru"]
    neg = ["wikipedia.org", "lemonde.fr", "google.com", "cloudflare.com", "fastly.com", "akamai.com"]
    corps = (f"<div class='ligne' style='flex:1'>"
             f"<div class='carte f1' style='border-top:8px solid {C['bloque']}'><div style='font-size:46px;font-weight:700'>Témoins positifs</div>"
             f"<div style='font-size:30px;color:{C['texte2']};margin:12px 0 30px'>doivent être bloqués (sanctions de l'UE)</div>"
             + "".join(f"<div class='mono' style='font-size:40px;margin:18px 0'>{x}</div>" for x in pos)
             + f"<div style='font-size:30px;margin-top:40px'>s'ils ne le sont pas, l'outil ne voit pas les blocages</div></div>"
             f"<div class='carte f1' style='border-top:8px solid {C['ok']}'><div style='font-size:46px;font-weight:700'>Témoins négatifs</div>"
             f"<div style='font-size:30px;color:{C['texte2']};margin:12px 0 30px'>doivent toujours marcher</div>"
             + "".join(f"<div class='mono' style='font-size:40px;margin:18px 0'>{x}</div>" for x in neg)
             + f"<div style='font-size:30px;margin-top:40px'>s'ils tombent aussi, c'est ma connexion</div></div></div>")
    return page(corps, titre="Les témoins")


# ---------------------------------------------------------------- séquence 6

@graphique("S06_G01a")
def alerte(d):
    corps = (f"<div class='carte' style='margin:auto;width:1300px;border:5px solid {C['bloque']};text-align:center;padding:70px'>"
             f"<div style='font-size:34px;color:{C['texte2']}'>Serveur · vendredi 6 novembre · 18 h 30 → 20 h 10</div>"
             f"<div class='mono' style='font-size:84px;font-weight:700;margin:36px 0'>instagram.com</div>"
             f"<div style='font-size:64px;font-weight:800;color:{C['bloque']}'>aucune adresse</div>"
             f"<div style='font-size:34px;color:{C['texte2']};margin-top:36px'>la signature d'un filtrage DNS · la veille de l'acte IV</div></div>")
    return page(corps)


@graphique("S06_G01b")
def quatre(d):
    lignes = [("Annuaire du serveur", "157.240.0.174", True), ("Annuaire du système", "157.240.0.174", True),
              ("1.1.1.1, interrogé en clair", "aucune adresse", False), ("1.1.1.1, chiffré (DoH)", "57.144.244.34", True),
              ("Connexion à Instagram", "page reçue", True)]
    corps = "<table class='t' style='font-size:40px'>" + "".join(
        f"<tr><td>{'<b>' if i == 4 else ''}{t}{'</b>' if i == 4 else ''}</td><td class='mono {'ok' if ok else 'ko'}'>{v}</td>"
        f"<td style='font-size:46px' class='{'ok' if ok else 'ko'}'>{'✓' if ok else '✗'}</td></tr>"
        for i, (t, v, ok) in enumerate(lignes)) + "</table>"
    return page(corps, titre="Instagram, vendredi 18 h 40 : quatre annuaires", sous="Un seul ne répond plus. Les autres, et la connexion, marchent.")


def frise_signaux(d, vantage, hotes, debut, fin, titre, sous, surligner=None):
    """Lignes = hôtes, temps en abscisse ; une marque par tour où l'épisode est présent."""
    eps = d.get("episodes")
    if not eps:
        return None
    t0, t1 = debut, fin
    x0, x1, yh = 420, 1600, 92
    def X(t):
        return x0 + (t - t0).total_seconds() / (t1 - t0).total_seconds() * (x1 - x0)
    svg = [f"<svg width='1640' height='{120 + yh * len(hotes)}' style='margin-top:20px'>"]
    jour = dt.datetime(t0.year, t0.month, t0.day)
    while jour <= t1:
        if jour >= t0:
            svg.append(f"<line x1='{X(jour)}' y1='40' x2='{X(jour)}' y2='{60 + yh * len(hotes)}' stroke='{C['trait']}' stroke-width='2'/>"
                       f"<text x='{X(jour) + 10}' y='30' fill='{C['discret']}' font-size='26' font-family='Inter'>"
                       f"{['lun.', 'mar.', 'mer.', 'jeu.', 'ven.', 'sam.', 'dim.'][jour.weekday()]} {jour.day}</text>")
        jour += dt.timedelta(days=1)
    for i, (hote, lib, temoin) in enumerate(hotes):
        y = 60 + i * yh
        svg.append(f"<rect x='{x0}' y='{y + 12}' width='{x1 - x0}' height='{yh - 32}' rx='8' fill='{C['ok']}' opacity='0.22'/>")
        svg.append(f"<text x='0' y='{y + yh / 2 + 4}' fill='{C['texte']}' font-size='32' font-family='Inter' font-weight='600'>{lib}</text>")
        if temoin:
            svg.append(f"<text x='0' y='{y + yh / 2 + 36}' fill='{C['discret']}' font-size='22' font-family='Inter'>témoin</text>")
        for e in eps:
            if e["vantage"] != vantage or e["host"] != hote or not e["signal"].startswith("dns_p53"):
                continue
            a, b = dt.datetime.fromisoformat(e["debut_paris"]), dt.datetime.fromisoformat(e["fin_paris"])
            if b < t0 or a > t1:
                continue
            xa, xb = X(max(a, t0)), X(min(b, t1)) + 8
            svg.append(f"<rect x='{xa}' y='{y + 12}' width='{max(xb - xa, 8)}' height='{yh - 32}' rx='4' fill='{C['signal']}'/>")
    if surligner:
        a, b = surligner
        svg.append(f"<rect x='{X(a) - 14}' y='48' width='{X(b) - X(a) + 36}' height='{yh + 12}' rx='12' fill='none' "
                   f"stroke='{C['texte']}' stroke-width='3' stroke-dasharray='10 8'/>")
    svg.append("</svg>")
    leg = (f"<div style='font-size:28px;color:{C['texte2']};margin-top:16px'>"
           f"<span class='pastille' style='background:{C['ok']};opacity:.5'></span>répond normalement &nbsp;&nbsp;"
           f"<span class='pastille' style='background:{C['signal']}'></span>1.1.1.1 en clair ne donne plus d'adresse</div>")
    return page("".join(svg) + leg, titre=titre, sous=sous)


@graphique("S06_G01c")
def akamai(d):
    return frise_signaux(d, "vps", [("www.instagram.com", "instagram.com", False), ("i.instagram.com", "i.instagram.com", False),
                                    ("x.com", "x.com", False), ("www.akamai.com", "akamai.com", True)],
                         dt.datetime(2026, 11, 6, 6), dt.datetime(2026, 11, 9, 12),
                         "Le même raté, sur un site témoin", "akamai.com n'a rien à voir avec les réseaux sociaux.")


@graphique("S06_G02")
def cdn(d):
    c = (boite(20, 60, 460, 180, "Annuaire de l'opérateur") + boite(20, 420, 460, 180, "Annuaire neutre")
         + boite(1180, 60, 420, 180, "Instagram", "serveur A (proche)", mono=True) + boite(1180, 420, 420, 180, "Instagram", "serveur B", mono=True)
         + fleche(470, 150, 1170, 150, "57.144.244.192") + fleche(470, 510, 1170, 510, "31.13.73.63"))
    return schema(c, "Deux adresses différentes : suspect ?", "Non : les gros sites ont des serveurs partout, et chacun est orienté vers le plus proche.")


@graphique("S06_G03")
def reddit(d):
    corps = (f"<div class='carte' style='margin:auto;width:1200px;text-align:center;padding:70px'>"
             f"<div style='font-size:34px;color:{C['texte2']}'>Depuis mon serveur chez un hébergeur</div>"
             f"<div class='mono' style='font-size:80px;font-weight:700;margin:30px 0'>reddit.com</div>"
             f"<div class='mono' style='font-size:70px;font-weight:800;color:{C['signal']}'>403 · interdit</div>"
             f"<div style='font-size:34px;color:{C['texte2']};margin-top:36px'>à chaque tour, depuis le début : Reddit refuse les robots des centres de données</div></div>")
    return page(corps)


VAR = [("Une signature de blocage", "l'annuaire de l'opérateur ment alors qu'un annuaire neutre et chiffré dit la vérité ; ou connexion coupée net ; ou faux certificat"),
       ("Ça se répète", "au moins 3 mesures d'affilée, soit un quart d'heure"),
       ("Les témoins marchent", "pendant ce temps, Wikipédia, Le Monde… répondent"),
       ("Pas ailleurs", "ça ne se voit pas depuis le serveur chez un hébergeur ; et idéalement, OONI ou une autre ligne voient la même chose")]


def var(n):
    corps = "<div style='display:flex;flex-direction:column;gap:22px'>" + "".join(
        f"<div class='carte' style='display:flex;gap:40px;align-items:center;padding:28px 40px;opacity:{1 if i < n else 0}'>"
        f"<div style='font-size:80px;font-weight:800;color:{C['mvt']};width:70px'>{i + 1}</div>"
        f"<div><div style='font-size:44px;font-weight:700'>{t}</div><div style='font-size:28px;color:{C['texte2']};margin-top:8px'>{s}</div></div></div>"
        for i, (t, s) in enumerate(VAR)) + "</div>"
    return page(corps, titre="La VAR : mes 4 critères", sous="Annoncés avant de regarder les résultats.")


for _i in range(1, 5):
    GRAPHIQUES[f"S06_G04{'abcd'[_i - 1]}"] = (lambda k: (lambda d: var(k)))(_i)


# ---------------------------------------------------------------- séquence 7 : OONI

@graphique("S07_G01")
def ooni_couv(d):
    plat = [("Instagram", [16, 16, 16, 15]), ("Facebook", [16, 16, 16, 15]), ("YouTube", [16, 16, 16, 15]),
            ("Twitter", [16, 16, 16, 15]), ("TikTok", [14, 12, 16, 8]), ("X", [13, 12, 15, 8]), ("Snapchat", [9, 6, 10, 5])]
    fai = ["Orange", "SFR", "Free", "Bouygues"]
    def cell(h):
        op = 0.25 + 0.75 * h / 16
        return (f"<td style='text-align:center;padding:8px'><span style='display:inline-block;min-width:150px;padding:6px 0;border-radius:10px;"
                f"background:rgba(57,135,229,{op:.2f});font-weight:700'>{h}/16</span></td>")
    corps = ("<table class='t' style='font-size:30px'><tr><th></th>" + "".join(f"<th style='text-align:center'>{f}</th>" for f in fai) + "</tr>"
             + "".join(f"<tr><td style='font-weight:600;padding:8px 22px'>{p}</td>" + "".join(cell(h) for h in hs) + "</tr>" for p, hs in plat)
             + "</table>")
    return page(corps, titre="Samedi 24 octobre : heures testées par OONI",
                sous="Connexions fixes, de 7 h à 23 h (16 heures). Aucun signal de blocage.",
                source="Source : api.ooni.io, test web_connectivity · ooni/rapport_ooni.md")


@graphique("S07_G02")
def ooni_mobile(d):
    corps = (f"<div class='ligne' style='margin:auto 0'>"
             f"<div class='carte f1' style='text-align:center'><div class='grand'>16/16</div>"
             f"<div style='font-size:36px;margin-top:20px'>heures testées sur le fixe<br><span class='d'>(Instagram, chez Orange)</span></div></div>"
             f"<div class='carte f1' style='text-align:center;border:4px dashed {C['discret']}'><div class='grand m'>0 ou 1</div>"
             f"<div style='font-size:36px;margin-top:20px'>mesure en 4G<br><span class='d'>par site et par opérateur</span></div></div></div>")
    return page(corps, titre="Le trou : le mobile", sous="Or la lettre visait justement le mobile.")


def verdicts(lignes, titre):
    corps = "<div style='display:flex;flex-direction:column;gap:30px;margin:auto 0'>" + "".join(
        f"<div class='carte' style='display:flex;align-items:center;gap:50px'><div style='font-size:44px;width:620px'>{q}</div>"
        f"<div style='font-size:56px;font-weight:800;color:{C['texte'] if v == 'NON PROUVÉ' else C['discret']}'>{v}</div></div>"
        for q, v in lignes) + "</div>"
    return page(corps, titre=titre)


@graphique("S07_G03")
def ooni_verdict(d):
    return verdicts([("24 et 31 octobre, connexions fixes", "NON PROUVÉ"), ("24 et 31 octobre, mobile", "NON TESTABLE")],
                    "Verdict pour les 24 et 31 octobre")


# ---------------------------------------------------------------- séquence 8 : frises

PLATEFORMES = ["x", "tiktok", "instagram", "snapchat", "facebook", "youtube", "messenger", "whatsapp", "telegram",
               "threads", "discord", "reddit", "twitch", "bluesky", "bereal", "signal", "mastodon"]
NOMS = {"x": "X", "tiktok": "TikTok", "instagram": "Instagram", "snapchat": "Snapchat", "facebook": "Facebook",
        "youtube": "YouTube", "messenger": "Messenger", "whatsapp": "WhatsApp", "telegram": "Telegram", "threads": "Threads",
        "discord": "Discord", "reddit": "Reddit", "twitch": "Twitch", "bluesky": "Bluesky", "bereal": "BeReal",
        "signal": "Signal", "mastodon": "Mastodon"}


def frise_reseau(d, vantage, titre, sous, debut=None, fin=None):
    tours = d.get(f"tours_{vantage}")
    if not tours:
        return None
    eps = [e for e in d.get("episodes", []) if e["vantage"] == vantage]
    t0 = debut or min(tours)
    t1 = fin or max(tours)
    x0, x1 = 300, 1640
    lignes = [(p, NOMS[p]) for p in PLATEFORMES] + [("temoin", "témoins négatifs"), ("temoin_pos", "témoin positif")]
    yh = 31
    def X(t):
        return x0 + (t - t0).total_seconds() / max((t1 - t0).total_seconds(), 1) * (x1 - x0)
    svg = [f"<svg width='1640' height='{60 + yh * len(lignes)}'>"]
    jour = dt.datetime(t0.year, t0.month, t0.day)
    while jour <= t1:
        for hh in (0, 12):
            t = jour + dt.timedelta(hours=hh)
            if t0 <= t <= t1:
                svg.append(f"<line x1='{X(t)}' y1='30' x2='{X(t)}' y2='{40 + yh * len(lignes)}' stroke='{C['trait']}' stroke-width='{2 if hh == 0 else 1}'/>"
                           f"<text x='{X(t) + 8}' y='24' fill='{C['discret']}' font-size='22' font-family='Inter'>"
                           f"{['lun.', 'mar.', 'mer.', 'jeu.', 'ven.', 'sam.', 'dim.'][t.weekday()]} {t.day} {'0 h' if hh == 0 else '12 h'}</text>")
        jour += dt.timedelta(days=1)
    pos_bloque = d.get(f"pos_bloque_{vantage}", 0)
    for i, (cle, lib) in enumerate(lignes):
        y = 40 + i * yh
        if cle == "temoin_pos":
            coul, op = (C["bloque"], 1) if pos_bloque > 0.5 else (C["ok"], 0.55)
        else:
            coul, op = C["ok"], 0.55
        svg.append(f"<rect x='{X(t0)}' y='{y + 4}' width='{X(t1) - X(t0)}' height='{yh - 10}' rx='4' fill='{coul}' opacity='{op}'/>")
        svg.append(f"<text x='0' y='{y + yh / 2 + 7}' fill='{C['texte']}' font-size='22' font-family='Inter'>{lib}</text>")
        for e in eps:
            pf = e["platform"] if e["kind"] == "cible" else ("temoin" if e["kind"] == "temoin_neg" else "")
            if pf != cle:
                continue
            a, b = dt.datetime.fromisoformat(e["debut_paris"]), dt.datetime.fromisoformat(e["fin_paris"])
            if b < t0 or a > t1:
                continue
            xa = X(max(a, t0))
            xb = X(min(b, t1)) + 6
            svg.append(f"<rect x='{xa - 3}' y='{y + 4}' width='{max(xb - xa, 7)}' height='{yh - 10}' fill='{C['signal']}'/>")
    svg.append("</svg>")
    leg = (f"<div style='font-size:26px;color:{C['texte2']};margin-top:14px'>"
           f"<span class='pastille' style='background:{C['ok']};opacity:.6'></span>ça marche &nbsp;&nbsp;"
           f"<span class='pastille' style='background:{C['signal']}'></span>signal isolé &nbsp;&nbsp;"
           f"<span class='pastille' style='background:{C['bloque']}'></span>bloqué &nbsp;&nbsp;"
           f"<span class='pastille' style='background:{C['vide']}'></span>pas de mesure</div>")
    return page("".join(svg) + leg, titre=titre, sous=sous)


@graphique("S08_G01")
def frise_box(d):
    n = len(d.get("tours_fixe", []))
    return frise_reseau(d, "fixe", "Ma box Bouygues, pendant l'acte IV",
                        f"{n} tours de mesure, un toutes les 5 minutes, sans trou")


@graphique("S08_G04")
def frise_vps(d):
    n = len(d.get("tours_vps", []))
    return frise_reseau(d, "vps", "Mon serveur, tout le week-end", f"{nb(n)} tours de mesure · le témoin positif n'est pas bloqué ici : normal, ce n'est pas un opérateur grand public")


@graphique("S08_G02")
def compteur(d):
    corps = (f"<div style='margin:auto;text-align:center'><div style='font-size:40px;color:{C['texte2']}'>sputnikglobe.com et ria.ru, au DNS de Bouygues</div>"
             f"<div style='font-size:240px;font-weight:800;color:{C['bloque']};letter-spacing:-6px;margin:30px 0'>738 / 738</div>"
             f"<div style='font-size:44px'>vérifications : bloqués à chaque fois</div>"
             f"<div style='font-size:36px;color:{C['texte2']};margin-top:30px'>l'outil voyait parfaitement un blocage DNS</div></div>")
    return page(corps)


@graphique("S08_G03")
def taches(d):
    eps = [e for e in d.get("episodes", []) if e["vantage"] == "fixe"]
    if not eps:
        return None
    lib = {"tcp_timeout_ip_seule": "délai de connexion vers un serveur", "dns_fai_timeout": "lenteur de l'annuaire"}
    jours = ["lun.", "mar.", "mer.", "jeu.", "ven.", "sam.", "dim."]
    lignes = "".join(
        f"<tr><td>{jours[dt.datetime.fromisoformat(e['debut_paris']).weekday()]} {dt.datetime.fromisoformat(e['debut_paris']):%H h %M}</td>"
        f"<td style='font-weight:600'>{NOMS.get(e['platform'], e['platform'])}</td><td class='d'>{lib.get(e['signal'], e['signal'])}</td>"
        f"<td class='sig'>1 tour</td><td class='ok'>témoins OK</td></tr>" for e in eps)
    corps = (f"<table class='t'><tr><th>quand</th><th>plateforme</th><th>signal</th><th>répété ?</th><th>témoins</th></tr>{lignes}</table>")
    return page(corps, titre="Les 6 taches de la box, passées à la VAR", sous="Rien ne se répète, rien ne touche une plateforme plus qu'une autre.")


@graphique("S08_G05")
def verdict_acte4(d):
    corps = (f"<div style='margin:auto;text-align:center'><div style='font-size:44px;color:{C['texte2']}'>Verdict pour l'acte IV (6 et 7 novembre)</div>"
             f"<div style='font-size:120px;font-weight:800;margin:40px 0'>aucune coupure observée</div>"
             f"<div style='font-size:34px;color:{C['texte2']}'>box Bouygues jusqu'à samedi midi · serveur tout le week-end · OONI sur l'iPhone</div></div>")
    return page(corps)


# ---------------------------------------------------------------- séquence 9

@graphique("S09_G02")
def controles(d):
    corps = ("<table class='t' style='font-size:38px'><tr><th>contrôle</th><th>ce que l'outil a vu</th><th></th></tr>"
             "<tr><td>Un tweet de test,<br>supprimé après le 1er passage</td><td>« supprimé par l'auteur »<br><span class='d'>dès le passage suivant</span></td><td class='ok' style='font-size:50px'>✓</td></tr>"
             "<tr><td>Un tweet de RT<br><span class='d'>(sanctions de l'UE)</span></td><td>France : <b class='ko'>retenu</b> (demande légale)<br>États-Unis : <b class='ok'>visible</b></td><td class='ok' style='font-size:50px'>✓</td></tr></table>")
    return page(corps, titre="Le détecteur détecte", sous="Avant de compter, on vérifie que l'outil voit ce qu'il doit voir.")


def barres(series, max_v, unite="%", larg=1100):
    """series : [(libellé, valeur, couleur, détail)] ; barres horizontales, valeurs à droite."""
    out = []
    for lib, v, coul, det in series:
        w = max(6, v / max_v * larg)
        out.append(f"<div style='display:flex;align-items:center;gap:30px;margin:22px 0'>"
                   f"<div style='width:330px;font-size:34px;font-weight:600'>{lib}</div>"
                   f"<div style='width:{w:.0f}px;height:64px;background:{coul};border-radius:0 6px 6px 0'></div>"
                   f"<div style='font-size:40px;font-weight:700'>{nb(v, 1)} {unite}</div>"
                   f"<div style='font-size:28px;color:{C['texte2']}'>{det}</div></div>")
    return "".join(out)


@graphique("S09_G03")
def t2(d):
    corps = (f"<div style='font-size:36px;color:{C['texte2']};margin-bottom:6px'>X : posts disparus</div>"
             + barres([("mouvement", 26 / 1137 * 100, C["mvt"], "26 sur 1 137"), ("témoins", 19 / 798 * 100, C["tem"], "19 sur 798")], 3)
             + f"<div style='font-size:36px;color:{C['texte2']};margin:40px 0 6px'>dont : sans que l'auteur l'ait supprimé</div>"
             + barres([("mouvement", 8 / 1137 * 100, C["mvt"], "8 sur 1 137"), ("témoins", 12 / 798 * 100, C["tem"], "12 sur 798 · surtout du spam suspendu")], 3)
             + f"<div style='font-size:32px;margin-top:40px'>TikTok : 4 vidéos du mouvement disparues sur 703, toutes supprimées par leur auteur.</div>")
    return page(corps, titre="Retraits : pas plus que chez les témoins")


@graphique("S09_G04")
def dsa_zero(d):
    corps = (f"<div class='ligne' style='margin:auto 0;align-items:center'>"
             f"<div class='f1' style='text-align:center'><div class='grand mvt'>987</div><div style='font-size:36px;margin-top:20px'>vidéos TikTok suivies</div></div>"
             f"<div style='font-size:90px;color:{C['discret']}'>→</div>"
             f"<div class='f1' style='text-align:center'><div class='grand'>0</div><div style='font-size:36px;margin-top:20px'>retirée ou déclassée<br><span class='d'>dans les déclarations de TikTok</span></div></div></div>")
    return page(corps, titre="La base européenne des décisions de modération",
                sous="Cinq semaines de déclarations (1er octobre – 8 novembre), des dizaines de millions de décisions.",
                source="Source : transparency.dsa.ec.europa.eu, exports quotidiens")


@graphique("S09_G05")
def questions(d):
    q = ["TikTok traite-t-il ces vidéos à part ?", "Est-ce que ça change pendant l'acte IV ?", "Sont-elles moins diffusées ?",
         "Des comptes sont-ils cachés dans la recherche ?", "Que déclarent les plateformes elles-mêmes ?"]
    corps = "<ol style='font-size:52px;line-height:1.75;margin:20px 0 0;padding-left:70px'>" + "".join(f"<li>{x}</li>" for x in q) + "</ol>"
    return page(corps, titre="Le shadowban, découpé en questions vérifiables")


@graphique("S09_G06a")
def rev_brut(d):
    corps = (f"<div class='ligne' style='margin:auto 0'>"
             f"<div class='carte f1' style='text-align:center'><div style='font-size:36px;color:{C['texte2']}'>vidéos marquées « reviewed »</div>"
             f"<div class='grand' style='margin-top:30px'>3 M</div><div style='font-size:34px;margin-top:16px'>vues (médiane)</div></div>"
             f"<div class='carte f1' style='text-align:center'><div style='font-size:36px;color:{C['texte2']}'>les autres</div>"
             f"<div class='grand' style='margin-top:30px'>20 000</div><div style='font-size:34px;margin-top:16px'>vues (médiane)</div></div></div>")
    return page(corps, titre="« reviewed » suit d'abord la popularité", sous="Champ interne, non documenté par TikTok. 984 vidéos.")


def rev_table(lignes, titre, sous, note=""):
    corps = ("<table class='t'><tr><th>popularité</th><th class='mvt'>mouvement</th><th class='tem'>témoins</th></tr>"
             + "".join(f"<tr><td>{a}</td><td><b style='font-size:46px'>{b}</b> <span class='d'>{bd}</span></td>"
                       f"<td><b style='font-size:46px'>{c}</b> <span class='d'>{cd}</span></td></tr>" for a, b, bd, c, cd in lignes)
             + "</table>" + (f"<div style='font-size:36px;margin-top:40px'>{note}</div>" if note else ""))
    return page(corps, titre=titre, sous=sous)


@graphique("S09_G06b")
def rev_vendredi(d):
    return rev_table([("plus d'un million de vues", "39 %", "19 / 49", "19 %", "8 / 43")],
                     "Vendredi soir : « je tiens quelque chose »", "Part des vidéos marquées, à popularité égale.",
                     f"<span class='sig'>⚠</span> seulement 43 vidéos témoins dans cette tranche")


@graphique("S09_G06c")
def rev_lundi(d):
    return rev_table([("plus d'un million de vues", "34 %", "21 / 61", "30 %", "43 / 141"),
                      ("100 000 à 1 million", "14 %", "15 / 104", "3 %", "2 / 68"),
                      ("moins de 100 000", "1 %", "4 / 535", "1 %", "1 / 75")],
                     "Avec trois fois plus de témoins, l'écart fond", "Part des vidéos marquées, à popularité égale.",
                     "Toutes tranches confondues : <b>pas de différence significative</b> (p = 0,13)")


@graphique("S09_G07")
def t8(d):
    corps = (barres([("mouvement", 5 / 699 * 100, C["mvt"], "5 vidéos sur 699"), ("témoins", 2 / 284 * 100, C["tem"], "2 vidéos sur 284")], 1.5)
             + f"<div style='font-size:36px;margin-top:50px'>Moins de 1 % des deux côtés : pas de différence.</div>")
    return page(corps, titre="Indicateurs internes qui changent pendant le suivi", sous="Relevés toutes les trois heures, pendant et après l'acte IV.")


@graphique("S09_G08")
def t9(d):
    st = [("< 100 k vues, < 3 jours", 11, 368, 3, 34), ("< 100 k vues, 3 à 14 jours", 18, 67, 14, 24), ("< 100 k vues, > 14 jours", 59, 93, 6, 16),
          ("100 k – 1 M, < 3 jours", 3, 36, 0, 5), ("100 k – 1 M, 3 à 14 jours", 10, 14, 5, 9), ("100 k – 1 M, > 14 jours", 41, 52, 37, 54),
          ("> 1 M vues, > 14 jours", 44, 54, 131, 139)]
    x0, x1 = 560, 1560
    def X(p):
        return x0 + p * (x1 - x0)
    svg = [f"<svg width='1640' height='{90 + 74 * len(st)}'>"]
    for p in (0, 0.25, 0.5, 0.75, 1):
        svg.append(f"<line x1='{X(p)}' y1='20' x2='{X(p)}' y2='{30 + 74 * len(st)}' stroke='{C['trait']}' stroke-width='2'/>"
                   f"<text x='{X(p)}' y='{70 + 74 * len(st)}' fill='{C['discret']}' font-size='26' text-anchor='middle' font-family='Inter'>{int(p * 100)} %</text>")
    for i, (lib, a, n1, b, n2) in enumerate(st):
        y = 50 + i * 74
        pa, pb = a / n1, b / n2
        svg.append(f"<text x='0' y='{y + 10}' fill='{C['texte']}' font-size='30' font-family='Inter'>{lib}</text>")
        svg.append(f"<line x1='{X(min(pa, pb))}' y1='{y}' x2='{X(max(pa, pb))}' y2='{y}' stroke='{C['trait']}' stroke-width='6'/>")
        svg.append(f"<circle cx='{X(pb)}' cy='{y}' r='16' fill='{C['tem']}' stroke='{C['fond']}' stroke-width='3'/>")
        svg.append(f"<circle cx='{X(pa)}' cy='{y}' r='16' fill='{C['mvt']}' stroke='{C['fond']}' stroke-width='3'/>")
    svg.append("</svg>")
    leg = (f"<div style='font-size:30px;margin-top:6px'><span class='pastille' style='background:{C['mvt']};border-radius:50%'></span>mouvement &nbsp;&nbsp;"
           f"<span class='pastille' style='background:{C['tem']};border-radius:50%'></span>témoins (recettes, foot…) &nbsp;&nbsp;"
           f"</div><div style='font-size:30px;margin-top:10px' class='d'>Au total : 188 vidéos du mouvement stagnent, 192 attendues à traitement égal. Les deux seuls écarts nets vont vers les témoins.</div>")
    return page("".join(svg) + leg, titre="Part des vidéos qui ne gagnent plus de vues",
                sous="Moins de 1 % de vues en plus sur au moins 24 h, à popularité et âge égaux.")


@graphique("S09_G09a")
def t6_alerte(d):
    corps = (f"<div class='carte' style='margin:auto;width:1300px;border:5px solid {C['bloque']};text-align:center;padding:70px'>"
             f"<div style='font-size:34px;color:{C['texte2']}'>Session de samedi soir, recherche « from:compte » sur X</div>"
             f"<div style='font-size:150px;font-weight:800;color:{C['bloque']};margin:30px 0'>12 comptes</div>"
             f"<div style='font-size:52px;font-weight:700'>absents de la recherche</div>"
             f"<div style='font-size:34px;color:{C['texte2']};margin-top:30px'>dont 7 parmi ceux qui disent être censurés</div></div>")
    return page(corps)


@graphique("S09_G09b")
def t6_grille(d):
    sess = d.get("t6_sessions")
    if not sess:
        return None
    noms, comptes = sess["sessions"], sess["comptes"]
    sym = {"present": (C["ok"], "présent"), "absent": (C["bloque"], "absent"), "partiel": (C["bloque"], "absent"),
           "non_verifie": (C["vide"], "non vérifié")}
    entetes = "".join(f"<th style='text-align:center'>{n}</th>" for n in noms)
    lignes = ""
    for i, c in enumerate(comptes):
        cells = "".join(f"<td style='text-align:center;padding:10px'><span style='display:inline-block;width:200px;padding:8px 0;border-radius:8px;"
                        f"background:{sym[e][0]};font-size:26px;font-weight:600'>{sym[e][1]}</span></td>" for e in c["etats"])
        g = {'temoin': 'témoin', 'revendication': 'se dit censuré'}.get(c['groupe'], c['groupe'])
        lignes += f"<tr><td style='padding:10px 22px'>compte {i + 1} <span class='d' style='font-size:26px'>({g})</span></td>{cells}</tr>"
    corps = f"<table class='t' style='font-size:30px'><tr><th></th>{entetes}</tr>{lignes}</table>"
    return page(corps, titre="Les mêmes comptes, session par session", sous="Une absence isolée, au milieu de présences, c'est une erreur de mesure.")


@graphique("S09_G09c")
def t6_verdict(d):
    corps = (f"<div style='font-size:36px;color:{C['texte2']}'>4 sessions · absent dans au moins 2 d'entre elles</div>"
             + barres([("se disent censurés", 2 / 14 * 100, C["mvt"], "2 comptes sur 14"),
                       ("mouvement", 0.0, C["mvt"], "0 sur 13"),
                       ("témoins", 1 / 10 * 100, C["tem"], "1 compte sur 10")], 20)
             + f"<div style='font-size:40px;font-weight:700;margin-top:50px'>Le même taux que chez mes témoins.</div>"
             f"<div style='font-size:32px;color:{C['texte2']};margin-top:16px'>Sur X, les recherches vides sont fréquentes : un témoin tombe dessus aussi. "
             f"Règle inchangée depuis samedi.</div>")
    return page(corps, titre="Session de lundi : 3 comptes absents deux fois")


@graphique("S09_G10")
def t7(d):
    max_v = 3
    x0, x1 = 600, 1500
    def X(v):
        return x0 + v / max_v * (x1 - x0)
    lignes = [("X · comptes du mouvement", 2.50, "12 comptes"), ("X · se disent censurés", 1.18, "13 comptes"),
              ("TikTok · créateurs du mouvement", 1.35, "25 comptes")]
    svg = [f"<svg width='1640' height='640'>"]
    svg.append(f"<line x1='{X(1)}' y1='20' x2='{X(1)}' y2='520' stroke='{C['texte2']}' stroke-width='3' stroke-dasharray='10 8'/>"
               f"<text x='{X(1)}' y='570' fill='{C['texte2']}' font-size='28' text-anchor='middle' font-family='Inter'>×1 = autant de vues que leurs autres posts</text>")
    for i, (lib, v, n) in enumerate(lignes):
        y = 50 + i * 160
        svg.append(f"<text x='0' y='{y + 45}' fill='{C['texte']}' font-size='32' font-family='Inter' font-weight='600'>{lib}</text>"
                   f"<text x='0' y='{y + 85}' fill='{C['discret']}' font-size='26' font-family='Inter'>{n}</text>"
                   f"<rect x='{x0}' y='{y}' width='{X(v) - x0}' height='90' rx='6' fill='{C['mvt']}'/>"
                   f"<text x='{X(v) + 20}' y='{y + 60}' fill='{C['texte']}' font-size='46' font-weight='800' font-family='Inter'>×{nb(v, 2)}</text>")
    svg.append("</svg>")
    return page("".join(svg), titre="Posts sur la manif : plus de vues, pas moins",
                sous="Vues médianes des posts sur le mouvement, divisées par celles des autres posts du même compte.")


def courbe(serie, titre, sous, annot, zone=None, coul=None, source=None, fmt=lambda v: nb(v)):
    coul = coul or C["mvt"]
    if not serie:
        return None
    serie = sorted(serie)
    t0, t1 = serie[0][0], serie[-1][0]
    vmax = max(v for _, v in serie) * 1.15
    x0, x1, y0, y1 = 140, 1560, 600, 40
    def X(t):
        return x0 + (t - t0).days / max((t1 - t0).days, 1) * (x1 - x0)
    def Y(v):
        return y0 - v / vmax * (y0 - y1)
    svg = [f"<svg width='1640' height='680'>"]
    brut = vmax / 1.15 / 4
    ordre = 10 ** int(f"{brut:e}".split("e")[1])
    pas = next(m * ordre for m in (1, 2, 2.5, 5, 10) if m * ordre >= brut)
    for k in range(int(vmax // pas) + 1):
        v = k * pas
        svg.append(f"<line x1='{x0}' y1='{Y(v)}' x2='{x1}' y2='{Y(v)}' stroke='{C['trait']}' stroke-width='1'/>"
                   f"<text x='{x0 - 16}' y='{Y(v) + 8}' fill='{C['discret']}' font-size='24' text-anchor='end' font-family='Inter'>{fmt(v)}</text>")
    if zone:
        a, b = zone
        svg.append(f"<rect x='{X(a)}' y='{y1}' width='{X(b) - X(a)}' height='{y0 - y1}' fill='{C['signal']}' opacity='0.12'/>")
    t = t0
    while t <= t1:
        if t.day in (1, 8, 15, 22, 29):
            svg.append(f"<text x='{X(t)}' y='{y0 + 44}' fill='{C['discret']}' font-size='24' text-anchor='middle' font-family='Inter'>{t.day} {'oct.' if t.month == 10 else 'nov.'}</text>")
        t += dt.timedelta(days=1)
    # une ligne par période continue ; pointillés là où il manque des jours (pas d'export publié)
    morceaux = [[serie[0]]]
    for prec, cour in zip(serie, serie[1:]):
        if (cour[0] - prec[0]).days > 1:
            svg.append(f"<line x1='{X(prec[0]):.1f}' y1='{Y(prec[1]):.1f}' x2='{X(cour[0]):.1f}' y2='{Y(cour[1]):.1f}' "
                       f"stroke='{coul}' stroke-width='3' stroke-dasharray='6 10' opacity='0.6'/>")
            morceaux.append([])
        morceaux[-1].append(cour)
    for m in morceaux:
        pts = " ".join(f"{X(t):.1f},{Y(v):.1f}" for t, v in m)
        svg.append(f"<polyline points='{pts}' fill='none' stroke='{coul}' stroke-width='4' stroke-linejoin='round'/>")
    for t, v in serie:
        svg.append(f"<circle cx='{X(t):.1f}' cy='{Y(v):.1f}' r='5' fill='{coul}'/>")
    ax, txt = annot
    svg.append(f"<text x='{X(ax)}' y='{y1 + 30}' fill='{C['texte']}' font-size='30' font-weight='700' font-family='Inter' "
               f"text-anchor='{'end' if X(ax) > 1100 else 'start'}'>{txt}</text>")
    svg.append("</svg>")
    return page("".join(svg), titre=titre, sous=sous, source=source or "Source : transparency.dsa.ec.europa.eu, exports quotidiens")


@graphique("S09_G11a")
def dsa_tiktok(d):
    s = [(j, v["total"]) for (p, j), v in d.get("dsa", {}).items() if p == "tiktok"]
    return courbe(s, "TikTok : décisions déclarées par jour", "Toutes décisions, toute l'Europe.",
                  (dt.date(2026, 10, 28), "29 oct. : ×7 d'un coup, partout en Europe"), fmt=lambda v: f"{nb(v / 1e6, 1)} M")


@graphique("S09_G11b")
def dsa_insta(d):
    s = [(j, v["fr_civique"]) for (p, j), v in d.get("dsa", {}).items() if p == "instagram"]
    return courbe(s, "Instagram : déclassements « discours civique »",
                  "Décidés par Instagram lui-même · valables pour toute l'UE · langue non déclarée.",
                  (dt.date(2026, 10, 20), "20 – 27 oct."), zone=(dt.date(2026, 10, 20), dt.date(2026, 10, 27)))


# ---------------------------------------------------------------- séquence 10

@graphique("S10_G01")
def tableau_final(d):
    lignes = [("L'accès a-t-il été coupé les 24 ou 31 octobre ?", "NON PROUVÉ sur le fixe · NON TESTABLE sur le mobile"),
              ("L'accès a-t-il été coupé pendant l'acte IV ?", "NON PROUVÉ : aucune coupure observée"),
              ("Une coupure a-t-elle été envisagée ?", "DOCUMENTÉ (lettre du 22 octobre, selon la presse)"),
              ("Des contenus peuvent-ils être retirés sans juge ?", "DOCUMENTÉ dans un texte voté au Sénat, pas encore en vigueur"),
              ("Des posts du mouvement ont-ils été retirés ?", "NON PROUVÉ : pas plus que les témoins"),
              ("Y a-t-il un shadowban d'État ?", "NON TESTABLE de l'extérieur · rien de mesurable ne montre de bridage")]
    corps = ("<table class='t' style='font-size:32px'><tr><th style='width:48%'>si votre question est…</th><th>la réponse</th></tr>"
             + "".join(f"<tr><td>{q}</td><td style='font-weight:700'>{r}</td></tr>" for q, r in lignes) + "</table>")
    return page(corps, titre="Les verdicts")


# ---------------------------------------------------------------- données

def charger(a):
    d = {}
    if a.episodes and os.path.exists(a.episodes):
        d["episodes"] = list(csv.DictReader(open(a.episodes, newline="", encoding="utf-8")))
    for vantage, f in (("fixe", a.mesures_fixe), ("vps", a.mesures_vps)):
        if f and os.path.exists(f):
            tours, pos = {}, collections.Counter()
            for r in csv.DictReader(open(f, newline="", encoding="utf-8")):
                t = dt.datetime.strptime(r["ts_utc"], "%Y-%m-%dT%H:%M:%SZ") + dt.timedelta(hours=1)  # heure de Paris (novembre)
                tours.setdefault(r["round_id"], t)
                if r["kind"] == "temoin_pos":
                    pos["n"] += 1
                    pos["b"] += r["isp_rcode"] in ("NXDOMAIN", "REFUSED") or r["dns_verdict"].startswith("bloque")
            d[f"tours_{vantage}"] = sorted(tours.values())
            d[f"pos_bloque_{vantage}"] = pos["b"] / pos["n"] if pos["n"] else 0
    if a.dsa and os.path.exists(a.dsa):
        d["dsa"] = {(r["plateforme"], dt.date.fromisoformat(r["date"])): {k: int(v) for k, v in r.items() if k not in ("date", "plateforme")}
                    for r in csv.DictReader(open(a.dsa, newline="", encoding="utf-8"))}
    fichiers = sorted({f for m in (a.sessions_t6 or []) for f in (glob.glob(m) or [m])})
    if fichiers:
        sys.path.insert(0, os.path.join(ICI, "..", ".."))
        import comptes  # noqa: E402
        liste = list(csv.DictReader(open(a.comptes, newline="", encoding="utf-8")))
        sessions = []
        for f in fichiers:
            s_ = comptes.charger([f])
            if any(k[0] == "x" for k in s_[1]):
                sessions.append((f, s_))
        noms = []
        for f, s_ in sessions:
            t = max(p["capture"] for pr in s_[0].values() for p in pr.values())
            noms.append(f"{['lun.', 'mar.', 'mer.', 'jeu.', 'ven.', 'sam.', 'dim.'][t.weekday()]} {t.day} · {t.hour + 1} h")
        res, n_verif, n_iso = [], 0, 0
        for l in liste:
            if (l.get("plateforme") or "x") != "x":
                continue
            h = l["handle"]
            etats = []
            for f, (pr, re_, _, _, vis, der) in sessions:
                p_, r_ = pr.get(("x", h), {}), re_.get(("x", h), {})
                visitee = None if vis is None else ("x", h) in vis
                etats.append(comptes.t6(h, p_, r_, visitee, der)[0] if (p_ or r_) else "non_verifie")
            verif = [e for e in etats if e != "non_verifie"]
            n_verif += bool(verif)
            manque = [e for e in verif if e in ("absent", "partiel")]
            if manque:
                n_iso += len(manque) < comptes.MIN_SESSIONS
                res.append({"groupe": l["groupe"], "etats": etats})
        d["t6_sessions"] = {"sessions": noms, "comptes": res, "n_verifies": n_verif, "n_isoles": n_iso}
    return d


RENDU_JS = """
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const [dir, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort()) {
    await p.goto('file://' + path.join(dir, f));
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(out, f.replace('.html', '.png')) });
  }
  await b.close();
})();
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mesures-fixe")
    ap.add_argument("--mesures-vps")
    ap.add_argument("--episodes", help="rapport/episodes.csv produit par analyse.py")
    ap.add_argument("--dsa", help="dsa_jours.csv produit par dsa.py")
    ap.add_argument("--sessions-t6", nargs="*", help="exports du collecteur, sessions T6")
    ap.add_argument("--comptes", default="contenus/comptes_t6.csv")
    ap.add_argument("--out", default=ICI)
    ap.add_argument("--seulement", nargs="*", help="codes à refaire, ex. S09_G09b")
    ap.add_argument("--exporter-t6", help="calcule seulement la grille T6 (codes et états, sans pseudo) dans ce fichier JSON, sans rien dessiner")
    ap.add_argument("--donnees-t6", help="grille T6 déjà calculée (fichier JSON produit par --exporter-t6)")
    a = ap.parse_args()
    d = charger(a)
    if a.exporter_t6:
        json.dump(d.get("t6_sessions", {}), open(a.exporter_t6, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"Grille T6 écrite dans {a.exporter_t6} : {len(d.get('t6_sessions', {}).get('comptes', []))} compte(s), aucun pseudo.")
        return
    if a.donnees_t6:
        d["t6_sessions"] = json.load(open(a.donnees_t6, encoding="utf-8"))
    tmp = tempfile.mkdtemp()
    faits, sautes = [], []
    for code, f in sorted(GRAPHIQUES.items()):
        if a.seulement and code not in a.seulement:
            continue
        h = f(d)
        if h is None:
            sautes.append(code)
            continue
        open(os.path.join(tmp, code + ".html"), "w", encoding="utf-8").write(h)
        faits.append(code)
    js = os.path.join(tmp, "rendu.js")
    open(js, "w").write(RENDU_JS)
    os.makedirs(a.out, exist_ok=True)
    subprocess.run(["node", js, tmp, os.path.abspath(a.out)], check=True)
    shutil.rmtree(tmp)
    print(f"{len(faits)} graphique(s) dans {a.out}" + (f" ; sautés faute de données : {', '.join(sautes)}" if sautes else ""))


if __name__ == "__main__":
    main()
