# Reprise du projet : où on en est (10 novembre 2026)

> Note de passation pour reprendre le projet dans une nouvelle conversation. À lire en premier, avec `TABLEAU_DE_BORD.md` (pilotage des mesures) et `video/SCRIPT.md` (la vidéo).
> **Branche de travail : `main`** (ancienne `claude/zen-pasteur-l3whxh`, renommée le 12/11/2026 ; le dépôt est public).

---

## 1. Le projet en deux phrases

Une vidéo YouTube et un outil open source qui répondent à la question « Le gouvernement bride-t-il le mouvement social sur les réseaux sociaux ? », pendant l'acte IV des 6 et 7 novembre 2026. Chaque réponse doit être **prouvé / non prouvé / non testable**, pour trois formes de censure : (1) couper l'accès, (2) retirer des contenus, (3) réduire la visibilité.

## 2. Règles à respecter (non négociables)

- Ne jamais désigner une cause (« le gouvernement ») à partir d'un simple échec réseau. On dit « tel signal, à telle heure, chez tel opérateur ».
- Rigueur et neutralité : on ne juge ni le mouvement ni l'amendement sur le fond. On ne se moque pas de ceux qui se disent censurés.
- Vérifier l'actualité par recherche web et distinguer **documenté / annoncé / rumeur**.
- **Données personnelles** : ne jamais publier de pseudo de particulier. `contenus/corpus.csv`, `contenus/comptes_t6.csv`, `contenus/posts.csv`, `exports/*.ndjson`, `.cle_pseudonyme`, `liens_t7.html` restent hors du dépôt (voir `.gitignore`). Les rapports n'utilisent que des codes (`u_…`).
- **Secrets** : jamais de cookie, de jeton ni d'identifiant Webshare dans la conversation ou le dépôt (ils sont dans `~/.proxy_fr` et `~/.proxy_us` sur le VPS, en `chmod 600`).
- Pas de faux comptes. Pas de contournement anti-robot dans l'outil publié.
- Ne pas modifier une règle d'analyse après avoir vu le résultat ; si on le fait (c'est arrivé une fois, pour T6), on le dit dans la vidéo et on vérifie avec une session de plus.
- L'utilisateur veut des explications simples, étape par étape, et des commandes prêtes à copier.

## 3. Les résultats (tous les tests sont terminés)

| forme | test | résultat |
|---|---|---|
| 1. couper l'accès | moniteur réseau (box Bouygues du 6 à 5 h au 7 à 11 h 52 ; VPS tout le week-end) | aucune coupure ; témoin positif `sputnikglobe.com` bloqué 738/738 ; fausse alerte Instagram vendredi 18 h 30 (raté du résolveur 1.1.1.1:53, vu aussi sur `akamai.com`) |
| 1 | OONI public 17–31 octobre | fixe : non prouvé ; mobile : non testable (presque aucune mesure) |
| 1 | OONI sur l'iPhone (retrouvé dans les données publiques) | RED = SFR (AS15557), Cdiscount = Bouygues (AS5410) ; samedi 13 h 30 et 15 h 19 : aucun réseau social en anomalie, `sputnikglobe.com` bloqué. `ooni/rapport_iphone.md` |
| 2. retirer | T1 retenu en France | X : 1 seul post, un tweet de **RT** (sanctions UE) ; TikTok : rien |
| 2 | T2 disparitions | pas plus que les témoins (X : sans action de l'auteur 8/1 137 contre 12/798) |
| 2/3 | T3/T4 base DSA (1er oct. – 8 nov.) | TikTok : **0 de nos 987 vidéos** retirée ou déclassée ; saut ×7 le 29 oct. = toute l'Europe ; Instagram : pic « discours civique » du 20 au 27 oct., UE entière, langue non déclarée → question ouverte |
| 3. visibilité | T6 search ban (X, 4 sessions) | 3 comptes absents deux fois (2 « censurés » sur 14, **1 témoin** sur 10) ; toutes les absences tombent dans les 2 sessions longues → pas plus que les témoins |
| 3 | T7 vues comparées | posts sur la manif **plus** vus : X ×2,5 (mouvement), ×1,2 (« censurés ») ; TikTok ×1,35 (25 comptes) |
| 3 | T8 indicateurs TikTok | rien (5/699 contre 2/284) ; le marquage `reviewed` (39 % contre 19 % le 6/11) **ne tient plus** avec tous les témoins (34 % contre 30 %, p = 0,13) |
| 3 | T9 vues qui stagnent | rien (188 observées, 192 attendues) |
| 3 | T5 recherches comparées | non réalisé |

Faits vérifiés sur les sources primaires (10/11) : amendement n°94 rect. bis (senat.fr, retrait en 24 h, « personnalité qualifiée », blocage possible) ; lettre du 22 octobre (Lecornu, via Blast et Clubic, texte intégral non public) ; Conseil d'État 1er avril 2025 (n° 494511, 494583, 495174). Détails dans `video/FEUILLE_DE_ROUTE.md`, section 8.

## 4. Où sont les choses

| quoi | où |
|---|---|
| Outils de mesure et d'analyse | racine : `moniteur_reseaux.py`, `analyse.py`, `ooni_verif.py`, `contenus.py`, `importer.py`, `collecteur.py`, `comptes.py`, `analyse_tiktok.py`, `analyse_contenus.py`, `dsa.py` |
| Résultats publiables (sans donnée personnelle) | `resultats/` : réseau (`reseau_analyse.md`, `reseau_episodes.csv`, `frise.svg`), contenus (`contenus_t1_t2.md`, version sans liens), T6/T7 (`comptes_t6_t7_samedi.md`, `grille_t6_4sessions.json`), T8/T9, DSA (`dsa_t3_t4.md`, `dsa_jours.csv`), OONI iPhone |
| OONI | `ooni/rapport_ooni.md` (17–31 oct.), `ooni/rapport_iphone.md` (tests de l'acte IV) |
| Journal de l'enquête (anecdotes, erreurs corrigées) | `video/JOURNAL_DE_BORD.md` |
| Script de la vidéo, **version 2** | `video/SCRIPT.md` : fil des **cinq fausses preuves**, 3 chapitres, verdict en trois réponses |
| Liste des plans à filmer | `video/PLANS.md` (⚠️ numérotée selon la version 1 du script ; les codes des graphiques restent valables) |
| Graphiques de la vidéo (54 PNG 1920×1080) | `video/graphiques/` + générateur `fabriquer.py` |
| Mascotte LaFeuille (12 poses, kit de visages) | `video/mascotte/` (utiliser les fichiers `apercus/`, qui contiennent le visage) |
| Posts « je suis censuré » recadrés (pseudos floutés) | `video/tweets/` ; captures d'origine à mettre dans `video/tweets/captures/` (ignoré par Git) |
| Miniatures | `video/miniatures/` : E1 (Macron), E2 (Lecornu), D1, D2, C1, C2… ; générateurs `fabriquer_miniatures*.py` ; polices dans `polices/` ; crédits photo dans `photos/CREDITS.md` |

**Données qui ne sont pas dans le dépôt** (personnelles ou volumineuses) :
- **Mac** : `contenus/corpus.csv`, `contenus/comptes_t6.csv`, `contenus/posts.csv`, `.cle_pseudonyme`, `exports/*.ndjson` (sessions T6 et Zeeschuimer).
- **Tour Windows** : `mesures_fixe.csv`.
- **VPS** : `mesures_vps.csv`, `contenus_vps.csv`, `contenus_fr_resid.csv`, `contenus_us_resid.csv`, `tiktok_metriques_vps.csv`. Les sessions tmux `contenus`, `t1fr`, `t1us` et le moniteur réseau tournent encore (prévu jusqu'au ~21 novembre).

## 5. Décisions en attente (à demander à l'utilisateur)

1. **Miniature** : E1 (Macron, plus reconnaissable mais il n'a pas signé la lettre) ou E2 (Lecornu, exact, regard caméra), ou D1 (sans photo). Recommandation : E2.
2. **Avatars qui montrent un visage** dans les posts de l'accroche : les flouter aussi ou non (les pseudos sont déjà floutés).
3. **Voix** : ElevenLabs (connecteur claude.ai ou clé d'API), voix clonée de l'utilisateur ou voix de synthèse, et/ou quelques passages face caméra (`[FACE]` dans le script). Penser à la case « contenu synthétique » de YouTube.

## 6. Prochaines étapes

1. **Cartons « FAUSSE PREUVE N°1 à 5 »** et carton d'ouverture « 5 PREUVES ? », dans le style des miniatures (police Anton, jaune `#FFD60A`, LaFeuille en pose « choc » puis « sceptique »). Codes `FP_1` à `FP_5` dans le script.
2. **Mettre `video/PLANS.md` à jour** avec la structure du script v2.
3. **Piste à vérifier** : un avertissement TikTok aux Français depuis le 28 octobre (« La situation évolue rapidement dans ton pays… », capture dans `video/tweets/T_tiktok_avertissement.png`, publié par un compte de particulier, peut-être parodique). L'Espresso (30/10/2026) rapporte un message semblable en Italie, ce qui collerait avec le saut européen de TikTok dans la base DSA le 29 octobre. Ce serait une mesure de TikTok, pas de l'État. À confirmer avant d'en parler.
4. **Avant le tournage** : relancer une recherche d'actualité (suite de l'amendement à l'Assemblée nationale, nouveaux faits).
5. **Fin du suivi (~21 novembre)** : récupérer les CSV du VPS, relancer `analyse_contenus.py`, `analyse_tiktok.py`, `dsa.py --reprendre`, puis arrêter le VPS et les proxies.
6. **Avant publication** : passer le dépôt en public, mettre à jour la conclusion du `README.md` avec les résultats, compléter la description YouTube (annexe B du script).

## 7. Refaire les graphiques et les miniatures en local

```bash
pip install pillow
```
Dans le dossier du dépôt (le `node_modules` créé est ignoré par Git) :
```bash
npm install playwright && npx playwright install chromium
```
Les graphiques utilisent les polices Inter et DejaVu (à installer si absentes ; les miniatures embarquent les leurs). Miniatures :
```bash
python3 video/miniatures/fabriquer_miniatures_photo.py
``` Exemple, depuis le dossier du dépôt, avec les données du VPS et de la tour :
```bash
python3 video/graphiques/fabriquer.py --mesures-fixe mesures_fixe.csv --mesures-vps mesures_vps.csv --episodes resultats/reseau_episodes.csv --dsa resultats/dsa_jours.csv --donnees-t6 resultats/grille_t6_4sessions.json
```
