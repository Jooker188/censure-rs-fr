# Liste des plans

> Pour chaque séquence du script (`SCRIPT.md`) : ce qu'on voit à l'écran, qui le fabrique et comment.
> **Avant de filmer un plan, vérifie qu'il est dans cette liste.** Au montage, chaque phrase du script doit avoir une image.

## Les 5 types de plans

| code | type | qui | avec quoi |
|---|---|---|---|
| **F** | face caméra | toi | appareil photo + micro-cravate |
| **E** | écran (démonstration) | toi | OBS sur la tour, **sans le son** (la voix off s'enregistre après, voir plus bas) |
| **C** | plan de coupe (la tour, la box, le téléphone, tes mains) | toi | appareil photo, sans parler, 10 à 15 s par plan |
| **G** | graphique, tableau, schéma, animation | Claude | images PNG ou vidéos 1920×1080, à poser telles quelles dans le montage |
| **T** | capture du téléphone | toi | enregistrement de l'écran de l'iPhone (Centre de contrôle → bouton d'enregistrement) |

**Noms de fichiers**, pour qu'on s'y retrouve au montage :
- face caméra : `S05_F_prise2.mp4`, une séquence par fichier ;
- écran : `S05_E03_terminal-vps.mp4`, où `S05_E03` est le code du plan dans cette liste ;
- plan de coupe : `S05_C01_box.mp4`.

**Pour chaque plan écran :**
- démarre l'enregistrement 3 s avant d'agir, et arrête-le 3 s après ;
- bouge la souris lentement, et fais défiler doucement ;
- refais le plan si une notification apparaît.

**Voix off** : relance le plan écran sur la tour, et commente-le en te filmant avec l'appareil photo et le micro. Nomme le fichier `S05_VO_E03.mp4`.

**À flouter au montage**, à chaque apparition :
- l'adresse IPv6 de la box ;
- les adresses IP de la tour et du VPS ;
- tout pseudo de particulier ;
- les identifiants Webshare.

**À ne jamais filmer** : `contenus/corpus.csv`, `contenus/comptes_t6.csv`, `contenus/posts.csv`, `~/.proxy_fr`, `~/.proxy_us`, le détail par compte de `rapport/comptes.md`, les fichiers `exports/*.ndjson`.

---

## Séquence 0 : Accroche

| code | type | quoi | comment |
|---|---|---|---|
| S00_E01 | E | l'article sur la lettre de Matignon (Blast, ou Clubic à défaut) | navigateur avec un zoom à 150 %, défilement lent jusqu'au passage sur la lettre |
| S00_F | F | « Depuis, une question tourne en boucle… » jusqu'à « …l'une de ces trois-là » | |
| S00_E02 | E | **l'objet mystère** : la ligne `sputnikglobe.com … NXDOMAIN` | sur la tour, dans le dossier du dépôt : `py -3 moniteur_reseaux.py --vantage fixe --fai "Bouygues fibre" --once --out demo_tournage.csv`. Filme le tableau qui s'affiche. Au montage : zoom sur la ligne sputnik, IPv6 floutée |
| S00_G01 | G | trois cartons : PROUVÉ · NON PROUVÉ · NON TESTABLE | Claude |

## Séquence 1 : Qui parle, d'où

| code | type | quoi | comment |
|---|---|---|---|
| S01_F | F | toute la séquence, ton posé | |
| S01_C01 | C | tes mains sur le clavier, le terminal en fond | facultatif : à intercaler pour couper la face caméra |
| S01_E01 | E | la page GitHub du dépôt | quand il sera public |

## Séquence 2 : Les trois formes de censure

| code | type | quoi | comment |
|---|---|---|---|
| S02_G01 | G | schéma en trois colonnes (couper l'accès / supprimer des contenus / réduire la visibilité), qui apparaissent une par une | Claude, en animation |
| S02_G02 | G | le même schéma, colonnes 2 et 3 grisées | Claude |
| S02_F | F | l'intro (« Avant d'aller plus loin… ») et la conclusion (« Cette vidéo mesure la première… ») | le reste en voix off sur le schéma |

## Séquence 3 : Ce qu'on sait vraiment

| code | type | quoi | comment |
|---|---|---|---|
| S03_G01 | G | frise chronologique qui se construit date par date, avec une étiquette DOCUMENTÉ / ANNONCÉ / RUMEUR | Claude, une image par date |
| S03_E01 | E | article ICI (17 octobre, chiffres de participation) | navigateur, 5 s par article sur le passage clé |
| S03_E02 | E | articles Clubic et actu17 (lettre du 22 octobre, réponse des opérateurs) | |
| S03_E03 | E | article Journal du Coin (24 octobre) | |
| S03_E04 | E | articles Public Sénat et Maire-info (amendement n°94) | |
| S03_E05 | E | **le texte de l'amendement n°94 sur senat.fr** : https://www.senat.fr/amendements/2026-2027/87/Amdt_94.html | défile jusqu'à l'« Objet » et surligne la phrase sur le blocage |
| S03_E06 | E | article L'Informé (groupe de contact, 30 octobre) | |
| S03_E07 | E | article Sortiraparis (acte IV) | |
| S03_G02 | G | bulle « RUMEUR » à part de la frise | Claude |
| S03_G03 | G | récapitulatif : documenté / pas documenté | Claude |
| S03_F | F | intro, passage sur la rumeur, récapitulatif | les dates en voix off sur la frise |

## Séquence 4 : Comment on coupe un réseau social

| code | type | quoi | comment |
|---|---|---|---|
| S04_G01 | G | animation « l'annuaire » : on demande tiktok.com, l'annuaire répond une adresse | Claude |
| S04_G02 | G | l'annuaire qui ment (« n'existe pas » en rouge) | Claude |
| S04_G03 | G | blocage de l'adresse (route coupée), puis lecture du nom sur l'enveloppe (SNI) | Claude |
| S04_F | F | « Un détail qui a son importance… » (l'aveu du DNS chiffré), petit sourire | |
| S04_E01 | E | **le réglage DNS chiffré de la tour** : Paramètres Windows → Réseau et Internet → ta connexion → Attribution du serveur DNS (1.1.1.1, chiffré) | illustre l'aveu, sans montrer comment le changer : pas de tutoriel |

## Séquence 5 : Mon dispositif

| code | type | quoi | comment |
|---|---|---|---|
| S05_G01 | G | schéma du dispositif : box Bouygues, serveur chez un hébergeur, connexion aux États-Unis, iPhone avec 2 SIM, OONI | Claude |
| S05_C01 | C | la box Bouygues, voyants allumés | |
| S05_C02 | C | la tour, avec la fenêtre du moniteur ouverte à l'écran | |
| S05_C03 | C | l'iPhone, tiroir SIM ou réglages des deux lignes (sans les numéros) | |
| S05_E01 | E | le moniteur qui tourne : un tour complet qui défile | même commande que S00_E02 |
| S05_E02 | E | le VPS en SSH : `tmux ls` puis la fenêtre du moniteur | **IP floutée** |
| S05_E03 | E | **l'anecdote « Lauterbourg »** : `curl ipinfo.io` (ville Lauterbourg) puis `whois` (pays DE) | sur le VPS ; **IP floutée** |
| S05_E04 | E | retour de l'objet mystère `sputnikglobe.com → NXDOMAIN` | réutilise S00_E02 |
| S05_T01 | T | OONI Probe sur l'iPhone : un test lancé, puis le résultat sputnikglobe en anomalie, **avec l'ASN visible**, sur chacune des deux SIM | enregistrement d'écran iOS ; donne aussi l'ASN, pour compléter le script |
| S05_E05 | E | les mêmes mesures dans OONI Explorer (explorer.ooni.org) | lien depuis l'appli : « Partager » → ouvrir sur la tour |
| S05_E06 | E | depuis le VPS : sputnikglobe **accessible** | une ligne du terminal du VPS (`python3 moniteur_reseaux.py --vantage vps --fai hebergeur --once --out demo_tournage.csv`) |
| S05_G02 | G | les témoins négatifs (Wikipédia, Le Monde…) qui s'affichent en liste | Claude |

## Séquence 6 : Le piège, et la VAR

| code | type | quoi | comment |
|---|---|---|---|
| S06_F | F | toute la séquence, ton de confidence | |
| S06_G01 | G | la fausse alerte : « Instagram n'existe plus », vendredi 18 h 30 – 20 h 10, puis les quatre annuaires (3 verts, 1 rouge), puis le même raté sur `akamai.com` | Claude, à partir des mesures du VPS |
| S06_G02 | G | Instagram : deux annuaires, deux adresses différentes, deux serveurs proches | Claude |
| S06_G03 | G | Reddit « 403 interdit » depuis le serveur | Claude, à partir des mesures du VPS |
| S06_G04 | G | **la VAR** : les quatre critères qui s'affichent un par un | Claude |

## Séquence 7 : Le passé, les 24 et 31 octobre

| code | type | quoi | comment |
|---|---|---|---|
| S07_E01 | E | OONI Explorer : recherche France, 24 octobre, quelques mesures qui défilent | navigateur |
| S07_G01 | G | les chiffres : 45 000 à 61 000 mesures par jour, couverture heure par heure par opérateur | Claude, à partir de `ooni/rapport_ooni.md` |
| S07_E02 | E | **fausse piste 1** : la page OONI d'une mesure Facebook « bloqué » chez Free (le téléphone Android) | lien dans `ooni/rapport_ooni.md` |
| S07_E03 | E | **fausse piste 2** : la mesure du 27 octobre avec la page de blocage iranienne | idem |
| S07_G02 | G | le trou du mobile : « 0 ou 1 mesure en 4G » | Claude |
| S07_G03 | G | verdict : fixe non prouvé, mobile non testable | Claude |

## Séquence 8 : L'acte IV en direct

| code | type | quoi | comment |
|---|---|---|---|
| S08_G01 | G | la frise de la box, en plein écran (zoom au montage) | Claude |
| S08_G02 | G | compteur « 738 / 738 » pour le témoin positif | Claude |
| S08_G03 | G | les 6 taches isolées, passées à la VAR | Claude |
| S08_G04 | G | le week-end du VPS : la fausse alerte Instagram de vendredi (rappel), et les ratés isolés sur `x.com` samedi après-midi | Claude |
| S08_T01 | T | OONI de samedi sur l'iPhone : l'historique des tests de la journée | enregistrement d'écran iOS |
| S08_G05 | G | verdict : aucune coupure observée | Claude |

## Séquence 9 : Contenus et shadowban

| code | type | quoi | comment |
|---|---|---|---|
| S09_G01 | G | retour du schéma en trois colonnes, colonnes 2 et 3 en couleur | Claude |
| S09_G02 | G | les deux contrôles positifs : tweet supprimé → « supprimé » ; tweet de RT → « retenu » en France, visible aux États-Unis | Claude, à partir des mesures |
| S09_E01 | E | le tweet de RT ouvert dans le navigateur, depuis la France : message « retenu » | navigateur, sur la tour |
| S09_G03 | G | T2 : 2,3 % contre 2,4 %, puis 8 contre 12 | Claude |
| S09_E02 | E | le site de la base DSA (transparency.dsa.ec.europa.eu), page des téléchargements | navigateur |
| S09_G04 | G | « 987 vidéos cherchées, 0 trouvée » | Claude |
| S09_E03 | E | le tweet « stats anormalement basses… », **pseudo flouté** | capture dans le navigateur |
| S09_G05 | G | la liste des questions (traitée à part ? ça change ? moins diffusée ? cachée dans la recherche ? que déclarent les plateformes ?) | Claude |
| S09_E04 | E | **le champ `reviewed`** : une vidéo TikTok de **recette** d'un grand compte (pas un particulier), F12 → onglet Réseau, puis la réponse qui contient `reviewed`, surlignée avec Ctrl+F | navigateur ; bien choisir une vidéo témoin |
| S09_G06 | G | `reviewed` en 3 temps : chiffre brut (3 M contre 20 000 vues), puis photo de vendredi (39 % contre 19 %, 43 témoins), puis avec 141 témoins (34 % contre 30 %) | Claude |
| S09_G07 | G | T8 : 5/699 contre 2/284 | Claude |
| S09_G08 | G | T9 : courbes de vues, mouvement contre témoins de même popularité | Claude |
| S09_G09 | G | T6 : « 12 comptes absents » en rouge, puis la comparaison des 3 sessions, puis « 0 absent de façon répétée » | Claude (codes `u_…` seulement) |
| S09_G10 | G | T7 : ×1,8 et ×2,5 | Claude |
| S09_G11 | G | DSA : le saut de TikTok le 29 octobre (toute l'Europe), puis le pic d'Instagram du 20 au 27 octobre | Claude, à partir de la base DSA |
| S09_E05 | E | le communiqué du Conseil d'État du 1er avril 2025 sur TikTok en Nouvelle-Calédonie (conseil-etat.fr) | à la place des images d'archives, dont les droits sont compliqués ; surligne les trois conditions |
| S09_F | F | intro du shadowban, verdict, et passage « pourquoi ça compte » | |

## Séquence 10 : Verdicts et fin

| code | type | quoi | comment |
|---|---|---|---|
| S10_G01 | G | le tableau final, ligne par ligne | Claude |
| S10_F | F | la question, les limites, l'appel à participer, la phrase de fin | |
| S10_E01 | E | la page GitHub du dépôt | quand il sera public |
| S10_T01 | T | l'appli OONI Probe : écran d'accueil, puis bouton « Lancer » | enregistrement d'écran iOS |
| S10_E02 | E | dernier retour de `sputnikglobe.com → NXDOMAIN` | réutilise S00_E02 |

---

## Récapitulatif : ce que tu dois filmer

**Face caméra (F)** : une prise par séquence, de 0 à 10.

**Écran sur la tour (E)**, à regrouper en 3 sessions OBS :
1. **Terminal** : S00_E02 (réutilisé en S05_E04 et S10_E02), S05_E01, S05_E02, S05_E03, S05_E06.
2. **Navigateur, articles** : S00_E01, S03_E01 à S03_E07, S09_E02, S09_E05.
3. **Navigateur, plateformes** :
   - OONI Explorer : S05_E05, S07_E01 à S07_E03 ;
   - X : S09_E01 (RT), S09_E03 (tweet flouté) ;
   - TikTok : S09_E04 (`reviewed`) ;
   - Windows et GitHub : S04_E01 (réglage DNS), S01_E01 et S10_E01 (GitHub).

**Téléphone (T)** : S05_T01, S08_T01, S10_T01, en une seule fois.

**Plans de coupe (C)** : S01_C01, S05_C01 à S05_C03, en 10 minutes.

## Ce que Claude fabrique (G)

✅ **54 images PNG en 1920×1080**, dans `video/graphiques/`, nommées par leur code (`S05_G01.png`…). Fond sombre, mêmes couleurs partout : vert = ça marche, jaune = signal isolé, rouge = bloqué, bleu = mouvement, orange = témoins.

- Quand un code a des lettres (`S03_G01a` à `S03_G01f`, `S06_G04a` à `d`…), ce sont les **étapes d'une animation** : pose-les à la suite dans Resolve, avec un fondu enchaîné court (6 images) entre chaque.
- Pour les refaire après de nouvelles données (session T6 de lundi, par exemple) : `python3 video/graphiques/fabriquer.py --help` (options : mesures, épisodes, base DSA, sessions T6).
- `S09_G09c` (T6) et `S09_G10` (T7) sont à jour avec la session de lundi. `S09_G09b` (la grille session par session) est à jour avec les 4 sessions.

## Ce qui manque encore dans le script avant de tourner

| séquence | quoi | qui |
|---|---|---|
| 5 | les réseaux de tes deux SIM, d'après l'ASN affiché dans OONI | toi (plan S05_T01) |
| 8 | résultats OONI de samedi sur l'iPhone | toi |
| 9 | T6 et T7 de la session de lundi | après ta session T7 TikTok |

**Ne tourne pas une phrase qui contient encore un crochet.** Pour ton essai d'aujourd'hui, prends les séquences 1 et 2 : elles sont complètes.
