# Tableau de bord : où on en est

> **Document de pilotage, à lire en premier.** Les autres fichiers donnent le détail ; celui-ci dit quoi faire, où et quand.
> Mis à jour le samedi 7 novembre 2026 (acte IV). Légende : ✅ fait · 🔄 tourne tout seul · 🕒 à faire · ❓ à confirmer · ⛔ non testable · 🧑‍💻 à faire par Claude.

---

## ⚑ Décision du 07/11 : mode minimal jusqu'à lundi

On garde **uniquement ce qui tourne tout seul** : le moniteur réseau sur la tour et sur le VPS, et le suivi des contenus sur le VPS (T2, T8, T9). Plus les analyses que Claude fait de son côté : OONI public, base DSA (T3, T4).
**Non réalisés :** T1 (sauf si le proxy est lancé sur le VPS, 5 min, facultatif), T5, T6, T7, et la collecte des posts de l'acte IV. Dans la vidéo, on les présente comme « non testés », avec la raison : temps et effort disponibles, un seul week-end.
**À faire :** dimanche soir, envoyer les `mesures_*.csv` de la tour (puis l'éteindre) ; lundi, récupérer sur le VPS `contenus_vps.csv`, `tiktok_metriques_vps.csv` et `mesures_vps.csv`, et les envoyer.

---

## 1. Vue d'ensemble : les 3 formes de censure

| forme | question | tests | état |
|---|---|---|---|
| **1. Couper l'accès** | un réseau social est-il bloqué chez un opérateur ? | moniteur réseau + OONI | 🔄 mesures en cours |
| **2. Retirer des contenus** | des posts sont-ils retenus en France ou retirés ? | T1, T2 (+ T3 base DSA) | 🔄 T2 en cours · 🕒 T1 à démarrer · 🧑‍💻 T3 après le week-end |
| **3. Réduire la visibilité** | des posts ou des comptes sont-ils moins visibles ? | T4 à T9 | 🔄 T8-T9 en cours · 🕒 T5, T6-T7 samedi · 🧑‍💻 T4 après le week-end |

---

## 2. Ce qui tourne tout seul (à ne pas arrêter)

**5 programmes en tout : 1 sur la tour Windows, 4 sur le VPS.**

| # | où | nom de la session | ce qu'il mesure | forme | commande de lancement (dans la session) |
|---|---|---|---|---|---|
| 1 | tour Windows | fenêtre `lancer_windows.bat` | blocage réseau sur la box Bouygues | 1 | double-clic sur `lancer_windows.bat` |
| 2 | VPS | `sonde` | blocage réseau depuis le serveur | 1 | `python3 moniteur_reseaux.py --vantage vps --fai "Contabo"` |
| 3 | VPS | `contenus` | posts X et TikTok qui disparaissent ; indicateurs TikTok (T2, T8, T9) | 2 et 3 | `python3 contenus.py --corpus corpus.csv --vantage vps --interval 10800` |
| 4 | VPS | `t1fr` | les mêmes posts, vus depuis la France via le proxy (T1) | 2 | `. ~/.proxy_fr && python3 contenus.py --corpus corpus.csv --vantage fr_resid --leger --interval 43200` |
| 5 | VPS | `t1us` | les mêmes posts, vus depuis les États-Unis via le proxy (T1) | 2 | `. ~/.proxy_us && python3 contenus.py --corpus corpus.csv --vantage us_resid --leger --interval 43200` |

**Vérifier d'un coup que les 4 programmes du VPS tournent** (sur le VPS, hors de tmux) :
```bash
ps -eo args | grep -E "[m]oniteur_reseaux.py|[c]ontenus.py"
```
→ 4 lignes attendues (`--vantage vps` deux fois, `fr_resid`, `us_resid`). S'il en manque une : `tmux attach -t NOM`, colle la commande de la ligne correspondante, puis **Ctrl+B puis D** pour ressortir sans l'arrêter.

**Ton VPS :** il est enregistré en Allemagne (whois DE), mais les bases de géolocalisation le placent à Lauterbourg, en France. On ne sait donc pas quel pays les plateformes lui attribuent. C'est pour ça que T1 passe par les proxies `t1fr` et `t1us`.

---|---|---|---|---|
| **VPS** | moniteur réseau (forme 1) | `python3 moniteur_reseaux.py --vantage vps --fai "Contabo …"` | `tmux attach -t sonde` | ✅ confirmé le 07/11 |
| **VPS** | suivi des contenus X + TikTok (T2, T8, T9) | `python3 contenus.py --corpus corpus.csv --vantage vps --interval 10800` | `tmux attach -t contenus` | ✅ confirmé le 07/11 (v1.4+, 981 posts) |
| **Tour Windows** | moniteur réseau sur la box Bouygues (forme 1) | `lancer_windows.bat` | fenêtre ouverte | ✅ confirmé le 07/11 |

**Ton VPS :** il est enregistré en Allemagne (whois DE), mais les bases de géolocalisation le placent à Lauterbourg, en France. On ne sait donc pas quel pays les plateformes lui attribuent. Il sert pour tout **sauf T1**.

---

## 3. Samedi 7 novembre (acte IV) : la journée, automatisée

| quand | quoi | ce que tu fais | durée de ta part |
|---|---|---|---|
| **maintenant** | **T1 automatique** sur le VPS (proxy résidentiel France et États-Unis) | les commandes du §5, une seule fois | 5 min |
| **maintenant** | **installer le collecteur** sur le Mac et te connecter une fois | `pip install playwright`, puis `python3 -m playwright install chromium`, puis `python3 collecteur.py --connexion` | 5 min |
| **15 h – 17 h** | **T6/T7** : le collecteur visite les 40 comptes tout seul | `python3 collecteur.py --plan t6`, Mac allumé, environ 40 min sans rien faire | 1 min |
| **soir** | **collecte de l'acte IV** (X et TikTok) | `python3 collecteur.py --plan acte4`, environ 30 min sans rien faire | 1 min |
| **soir** | **import et mise à jour du VPS** | §5 « Importer » puis « Mettre à jour le VPS » | 5 min |
| toute la journée | **OONI** sur l'iPhone | laisse les tests automatiques activés ; un test manuel à 16 h si tu y penses | 0 à 5 min |
| — | **T5** (recherches à la main) | **abandonné** : le plus fragile des tests, et T6 mesure la visibilité dans la recherche de façon plus solide | 0 |

Si le collecteur affiche une vérification (captcha) ou s'arrête sur une erreur, reprends la version manuelle avec Zeeschuimer (`contenus/PROTOCOLE_T6_T7.md`, `contenus/RECHERCHES.md`).

## 4. Dimanche et les jours suivants

| quand | quoi | qui |
|---|---|---|
| dimanche | importer la collecte de l'acte IV, copier le nouveau corpus sur le VPS, relancer `contenus.py` | toi (§6) |
| dimanche | 2e session **T6/T7** (pour voir si quelque chose a changé) | toi |
| dimanche | m'envoyer les `mesures_*.csv` (moniteur réseau), puis lancer `analyse.py` | toi → 🧑‍💻 |
| dimanche ou lundi | `ooni_verif.py` sur les 6 et 7 novembre (données publiques OONI) | 🧑‍💻 |
| après le week-end | **T3/T4** : base européenne DSA | 🧑‍💻 |
| chaque jour pendant 2 semaines | **T1** : passages appariés France puis États-Unis (§5) | toi |
| à partir de lundi | passer le suivi du VPS de 3 h à 6 h (Ctrl+C, puis relancer sans `--interval`) | toi |
| dans 2 semaines | analyses finales, verdicts, séquences 8 et 10 du script | ensemble |

---

## 5. Commandes à retenir

**T1 : automatique sur le VPS, avec deux sorties résidentielles Webshare (France et États-Unis)**

Sur le VPS, une seule fois. Crée deux fichiers d'identifiants, lisibles par toi seul. Ils ne doivent jamais aller dans le dépôt.
```bash
printf 'export HTTPS_PROXY="http://TONUSER-fr-rotate:TONMOTDEPASSE@p.webshare.io:80"\n' > ~/.proxy_fr && chmod 600 ~/.proxy_fr
printf 'export HTTPS_PROXY="http://TONUSER-us-rotate:TONMOTDEPASSE@p.webshare.io:80"\n' > ~/.proxy_us && chmod 600 ~/.proxy_us
(. ~/.proxy_fr; curl -s https://1.1.1.1/cdn-cgi/trace | grep loc=)    # doit afficher loc=FR
(. ~/.proxy_us; curl -s https://1.1.1.1/cdn-cgi/trace | grep loc=)    # doit afficher loc=US
```
Puis deux sessions qui tournent toutes seules, une passe toutes les 12 h, en mode léger :
```bash
tmux new -s t1fr    # puis :  . ~/.proxy_fr && python3 contenus.py --corpus corpus.csv --vantage fr_resid --leger --interval 43200   (Ctrl+B puis D)
tmux new -s t1us    # puis :  . ~/.proxy_us && python3 contenus.py --corpus corpus.csv --vantage us_resid --leger --interval 43200   (Ctrl+B puis D)
```
Analyse : `--france fr_resid --etranger us_resid`. Volume estimé : environ 10 Mo par passage, soit environ 0,6 Go en deux semaines pour les deux sorties. Vérifie que ton forfait Webshare le permet.

**T1, version manuelle (si le proxy France ne marche pas) : passages appariés sur le Mac**
```bash
python3 contenus.py --corpus contenus/corpus.csv --vantage fixe --une-fois
export HTTPS_PROXY="http://IDENTIFIANT:MOTDEPASSE@HOTE:PORT"   # proxy Webshare US, jamais dans un fichier
curl -s https://1.1.1.1/cdn-cgi/trace | grep loc=                # doit afficher loc=US
python3 contenus.py --corpus contenus/corpus.csv --vantage etranger --leger --une-fois
unset HTTPS_PROXY
```

**Importer** (toujours avec **tous** les exports : Zeeschuimer et collecteur)
```bash
python3 importer.py ~/Downloads/zeeschuimer-export-*.ndjson exports/*.ndjson
```

**Mettre à jour le VPS après un import**
```bash
scp contenus.py contenus/corpus.csv smeshr-deploy@IP_DU_VPS:~/
# sur le VPS : tmux attach -t contenus → attendre « terminé » → Ctrl+C → relancer la même commande → Ctrl+B puis D
```

**Analyses** (à la fin, avec les CSV de tous les points dans le dossier)
```bash
python3 analyse.py "mesures_*.csv" --evenements evenements.csv                                   # forme 1
python3 analyse_contenus.py "contenus_*.csv" --corpus contenus/corpus.csv --france fixe --etranger etranger   # T1, T2, tableau final
python3 comptes.py exports/collecteur-t6-*.ndjson                                                # T6, T7
python3 analyse_tiktok.py "tiktok_metriques_*.csv" --corpus contenus/corpus.csv                  # T8, T9
```

---

## 6. État détaillé de chaque test

### Forme 1 : couper l'accès

| test | outil | où | état | ce qu'on sait déjà |
|---|---|---|---|---|
| Moniteur réseau | `moniteur_reseaux.py` | tour Windows (box Bouygues), VPS | 🔄 | Tour de test de vendredi : tout est accessible. Le témoin positif `sputnikglobe.com` est bien bloqué par le DNS de Bouygues. 1.1.1.1 n'est pas intercepté. Ton PC utilise un DNS chiffré, ce qui n'empêche pas la mesure du DNS de l'opérateur. |
| OONI sur iPhone | OONI Probe | RED (SFR) et Cdiscount (Bouygues ?) | ✅ vendredi · 🕒 samedi | `sputnikglobe.com` est bloqué sur les deux SIM, tout le reste est accessible. ❓ Relever l'ASN de chaque ligne. |
| OONI public, 24 et 31 octobre | `ooni_verif.py` | — | ✅ | **Fixe : non prouvé** (aucun signal, bonne couverture). **Mobile : non testable** (presque aucune mesure). |
| OONI public, 6 et 7 novembre | `ooni_verif.py` | — | 🧑‍💻 dimanche ou lundi | — |

### Forme 2 : retirer des contenus

| test | question | outil | où | état | ce qu'on sait déjà |
|---|---|---|---|---|---|
| **T1** | visible depuis l'étranger, retenu en France ? | `contenus.py` | **VPS via proxy résidentiel France + VPS via proxy résidentiel États-Unis** (automatique) | 🕒 à démarrer (5 min, §5) | Le contrôle RT est vu « retenu » depuis la France : la détection fonctionne. ❓ Il doit être visible depuis les États-Unis. |
| **T2** | un post disparaît-il, avec quel motif, plus souvent que les témoins ? | `contenus.py` | VPS (en continu) + Mac | 🔄 | Premier passage : mouvement, 2 posts indisponibles et 1 supprimé par son auteur ; témoins, 2 comptes suspendus. Rien d'anormal. ✅ Tweet de test supprimé : le prochain passage doit le voir disparaître. |
| **T3** | décisions de modération déclarées (base DSA) | à écrire | — | 🧑‍💻 | — |

### Forme 3 : réduire la visibilité

| test | question | outil | état | ce qu'on sait déjà |
|---|---|---|---|---|
| **T4** | déclassements déclarés (base DSA) | à écrire | 🧑‍💻 après le week-end | — |
| **T5** | une recherche est vide en France seulement ? | à la main + proxy US dans Firefox | ⛔ abandonné le 07/11 (fragile, couvert en partie par T6) | — |
| **T6** | des comptes sont absents de la recherche (search ban) ? | `collecteur.py --plan t6` + `comptes.py` | 🕒 samedi 15 h – 17 h (automatique) | 40 comptes prêts dans `contenus/comptes_t6.csv` (15 revendication, 15 mouvement, 10 témoins). Avant de commencer, désactive les 2 filtres de recherche de X. |
| **T7** | posts sur le mouvement moins vus que les autres posts du même compte ? | même session que T6 | 🕒 samedi | — |
| **T8** | indicateurs internes TikTok qui changent ? | `contenus.py` (VPS) + `analyse_tiktok.py` | 🔄 (≥ 2 passages nécessaires) | Photo du 06/11 : à popularité égale, les vidéos du mouvement sont **plus souvent marquées `reviewed`** que les témoins (39 % contre 19 % au-dessus d'un million de vues). C'est significatif, mais le champ n'est pas documenté et ce n'est **pas une preuve** (voir §7). |
| **T9** | vues qui stagnent, à popularité et âge égaux ? | idem | 🔄 (≥ 24 h nécessaires) | — |

---

## 7. Ce qu'on a appris en chemin (utile pour la vidéo)

- **Une différence de DNS n'est pas un blocage.** Les CDN renvoient des adresses différentes selon le résolveur.
- **Les témoins positifs** (`sputnikglobe.com` pour le réseau, le tweet de RT et le tweet supprimé pour les contenus) prouvent que les outils **voient** un blocage quand il y en a un.
- **Les recherches sont fixées à l'avance** (`contenus/RECHERCHES.md`) : on ne les a pas choisies pour arranger le résultat.
- **TikTok mélange des vidéos hors sujet** dans les pages de hashtag (230 vidéos écartées).
- **Le champ `reviewed` de TikTok suit la popularité.** Même à popularité égale, les vidéos du mouvement sont plus souvent marquées. Explication la plus simple : TikTok examine davantage l'actualité et les manifestations, qui sont aussi plus signalées. Rien n'indique une demande de l'État.
- **La géolocalisation d'une adresse IP est une estimation.** Le VPS est « en Allemagne » pour le registre et « à Lauterbourg » pour les bases de géolocalisation.
- **Les limites à dire :** échantillons personnalisés par ton compte, un seul week-end, peu de points de mesure, et aucun test ne dit **qui** a décidé.

---

## 8. Où trouver le détail

| sujet | fichier |
|---|---|
| méthode complète, limites, reproduction | `README.md` |
| recherches de collecte et journal | `contenus/RECHERCHES.md` |
| protocole T5 | `contenus/PROTOCOLE_T5.md` |
| protocole T6/T7 | `contenus/PROTOCOLE_T6_T7.md` |
| plan et script de la vidéo | `video/FEUILLE_DE_ROUTE.md`, `video/SCRIPT.md` |
| événements de la frise | `evenements.csv` |
| résultats OONI d'octobre | `ooni/rapport_ooni.md` |
