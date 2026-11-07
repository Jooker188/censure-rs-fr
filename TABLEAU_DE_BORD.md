# Tableau de bord : où on en est

> **Document de pilotage, à lire en premier.** Les autres fichiers donnent le détail ; celui-ci dit quoi faire, où et quand.
> Mis à jour le samedi 7 novembre 2026 (acte IV). Légende : ✅ fait · 🔄 tourne tout seul · 🕒 à faire · ❓ à confirmer · ⛔ non testable · 🧑‍💻 à faire par Claude.

---

## 1. Vue d'ensemble : les 3 formes de censure

| forme | question | tests | état |
|---|---|---|---|
| **1. Couper l'accès** | un réseau social est-il bloqué chez un opérateur ? | moniteur réseau + OONI | 🔄 mesures en cours |
| **2. Retirer des contenus** | des posts sont-ils retenus en France ou retirés ? | T1, T2 (+ T3 base DSA) | 🔄 T2 en cours · 🕒 T1 à démarrer · 🧑‍💻 T3 après le week-end |
| **3. Réduire la visibilité** | des posts ou des comptes sont-ils moins visibles ? | T4 à T9 | 🔄 T8-T9 en cours · 🕒 T5, T6-T7 samedi · 🧑‍💻 T4 après le week-end |

---

## 2. Ce qui tourne tout seul (à ne pas arrêter)

| où | quoi | commande lancée | session | ❓ à confirmer |
|---|---|---|---|---|
| **VPS** | moniteur réseau (forme 1) | `python3 moniteur_reseaux.py --vantage vps --fai "Contabo …"` | `tmux attach -t sonde` | qu'il tourne toujours |
| **VPS** | suivi des contenus X + TikTok (T2, T8, T9) | `python3 contenus.py --corpus corpus.csv --vantage vps --interval 10800` | `tmux attach -t contenus` | qu'il a été relancé avec la **v1.4 ou plus** et le corpus de **981 posts** (X + TikTok) |
| **Tour Windows** | moniteur réseau sur la box Bouygues (forme 1) | `lancer_windows.bat` | fenêtre ouverte | qu'elle tourne toujours (pas de veille) |

**Ton VPS :** il est enregistré en Allemagne (whois DE), mais les bases de géolocalisation le placent à Lauterbourg, en France. On ne sait donc pas quel pays les plateformes lui attribuent. Il sert pour tout **sauf T1**.

---

## 3. Samedi 7 novembre (acte IV) : la journée

| heure | quoi | forme | durée | mode d'emploi |
|---|---|---|---|---|
| matin | **T1** : passage France puis passage États-Unis sur le Mac (voir §5) | 2 | 2 × 35 min | ci-dessous, §5 |
| 13 h | **T5** : recherches France contre États-Unis, série 1 | 3 | 10 min | `contenus/PROTOCOLE_T5.md` |
| 13 h – 19 h | **OONI Probe** sur l'iPhone, en 4G, avec les 2 SIM, vers 14 h, 16 h et 18 h | 1 | 5 min chaque fois | liste de sites dans OONI |
| 15 h – 17 h | **T6/T7** : session des 40 comptes X avec Zeeschuimer | 3 | 40 min | `contenus/PROTOCOLE_T6_T7.md` |
| 16 h | **T5**, série 2 | 3 | 10 min | idem |
| 19 h | **T5**, série 3 | 3 | 10 min | idem |
| soir | **Collecte de l'acte IV** avec Zeeschuimer (X et TikTok) | 2-3 | 30 min | `contenus/RECHERCHES.md`, section « Collecte de l'acte IV » |
| soir | **T1** : nouveau passage France puis États-Unis | 2 | 2 × 35 min | §5 |

Facultatif : le moniteur réseau en 4G sur le Mac, en partage de connexion (forme 1). Voir le README, section « 4G ou 5G ».

---

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

**T1 : passages appariés sur le Mac** (même machine, l'un juste après l'autre)
```bash
python3 contenus.py --corpus contenus/corpus.csv --vantage fixe --une-fois
export HTTPS_PROXY="http://IDENTIFIANT:MOTDEPASSE@HOTE:PORT"   # proxy Webshare US, jamais dans un fichier
curl -s https://1.1.1.1/cdn-cgi/trace | grep loc=                # doit afficher loc=US
python3 contenus.py --corpus contenus/corpus.csv --vantage etranger --leger --une-fois
unset HTTPS_PROXY
```

**Importer de nouveaux exports Zeeschuimer** (toujours avec **tous** les exports)
```bash
python3 importer.py ~/Downloads/zeeschuimer-export-*.ndjson
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
python3 comptes.py session_comptes_*.ndjson                                                      # T6, T7
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
| **T1** | visible depuis l'étranger, retenu en France ? | `contenus.py` | **Mac sans proxy (France) + Mac avec proxy (États-Unis)** | 🕒 à démarrer samedi | Le contrôle RT est vu « retenu » depuis la France : la détection fonctionne. ❓ Il doit être visible depuis les États-Unis. |
| **T2** | un post disparaît-il, avec quel motif, plus souvent que les témoins ? | `contenus.py` | VPS (en continu) + Mac | 🔄 | Premier passage : mouvement, 2 posts indisponibles et 1 supprimé par son auteur ; témoins, 2 comptes suspendus. Rien d'anormal. ❓ Tweet de test **supprimé** ? |
| **T3** | décisions de modération déclarées (base DSA) | à écrire | — | 🧑‍💻 | — |

### Forme 3 : réduire la visibilité

| test | question | outil | état | ce qu'on sait déjà |
|---|---|---|---|---|
| **T4** | déclassements déclarés (base DSA) | à écrire | 🧑‍💻 après le week-end | — |
| **T5** | une recherche est vide en France seulement ? | à la main + proxy US dans Firefox | 🕒 samedi 13 h, 16 h et 19 h | — |
| **T6** | des comptes sont absents de la recherche (search ban) ? | Zeeschuimer + `comptes.py` | 🕒 samedi 15 h – 17 h | 40 comptes prêts dans `contenus/comptes_t6.csv` (15 revendication, 15 mouvement, 10 témoins). Avant de commencer, désactive les 2 filtres de recherche de X. |
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
