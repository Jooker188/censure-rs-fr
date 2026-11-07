# Feuille de route de la vidéo

> Document de pilotage. Il fixe **ce que la vidéo doit faire**, **les règles d'écriture** et **l'état d'avancement** de chaque séquence.
> Le script (`SCRIPT.md`) suit cette feuille de route séquence par séquence. Les coulisses de l'enquête (découvertes, erreurs corrigées, anecdotes) sont dans `JOURNAL_DE_BORD.md`. Quand tu modifies l'une, mets l'autre à jour.

---

## 1. La vidéo en une phrase

> « J'ai mesuré, pendant l'acte IV, si l'accès aux réseaux sociaux était coupé en France. Voici ce que je peux prouver, ce que je ne peux pas prouver, et ce que personne ne peut savoir de l'extérieur. »

- **Titre de travail.** « J'ai mesuré si le gouvernement coupe les réseaux sociaux ». Ce titre tient quel que soit le résultat.
- **Titres à éviter.** Tout titre qui annonce une conclusion avant les données, comme « Le gouvernement censure TikTok » ou « La censure est prouvée ».
- **Durée cible.** 22 à 26 minutes.
- **Public.** Des gens curieux, sans bagage technique, venant des deux bords politiques. La vidéo doit rester crédible pour quelqu'un qui croit à la censure comme pour quelqu'un qui n'y croit pas.

## 2. Ce que le spectateur doit retenir

1. « Censure » recouvre **trois choses différentes** : couper l'accès, supprimer des contenus, réduire la visibilité.
2. **Ce qui est documenté** : la lettre du 22 octobre, la réponse des opérateurs, l'amendement voté au Sénat, le précédent de la Nouvelle-Calédonie. Le reste relève de la rumeur, et la vidéo le dit.
3. **Un blocage réseau se voit** : le témoin positif (`sputnikglobe.com`) le montre.
4. **Une panne ne prouve pas un blocage**, et un blocage ne dit pas qui l'a décidé.
5. **Les verdicts, forme par forme**, avec leurs limites.
6. **Tout le monde peut vérifier** : le code est sur GitHub, et OONI Probe est gratuit.

## 3. Règles d'écriture

Ces règles s'appliquent à chaque phrase du script.

| règle | concrètement |
|---|---|
| **Statut de chaque fait** | Chaque affirmation d'actualité porte son statut à l'écran : *documenté*, *annoncé* ou *rumeur*, avec la source affichée. |
| **Pas de cause sans preuve** | On ne dit jamais « le gouvernement a coupé » à partir d'un échec réseau. On dit « tel signal, à telle heure, chez tel opérateur ». |
| **Critères annoncés avant les résultats** | On présente la grille de lecture (la « VAR ») **avant** de montrer les données, et on ne la modifie pas après. |
| **Incertitude dite à voix haute** | « Un week-end, trois points de mesure, c'est mince. » Le spectateur doit l'entendre, pas seulement le lire. |
| **Neutralité sur le fond** | On ne juge pas le mouvement social. On ne juge pas l'amendement sur le fond : on cite ses partisans et ses critiques. |
| **Pas de sponsor VPN** | Un sponsor qui vend du contournement de censure créerait un conflit d'intérêts avec la conclusion. |
| **Vocabulaire précis** | Préférer « bloqué » ou « inaccessible » à « censuré », et « filtrage DNS » à « coupure ». Pour « bridé », dire qu'on ne peut pas le mesurer. |
| **Vie privée** | Ne montrer ni l'adresse IPv6 de ta box, ni ton IP publique, ni ta localisation précise, ni des comptes de particuliers. Floute si nécessaire. |

## 4. Mécaniques de narration retenues

Elles viennent des vidéos de référence (Seb et Cyrus North), adaptées au sujet.

| mécanique | où elle est utilisée |
|---|---|
| **Source primaire en accroche** | Séquence 0 : la lettre de Matignon. |
| **Objet mystère qui revient plus tard** | Séquence 0 : la capture « sputnikglobe.com → NXDOMAIN ». Elle est expliquée en séquence 5. |
| **Définir son terme avant d'analyser** | Séquence 2 : les trois formes de censure. |
| **Annoncer son point de vue et sa légitimité, sans exagérer** | Séquence 1. |
| **Récapitulatifs d'étape** | Fin des séquences 3, 6 et 8. |
| **Retournement sur le vocabulaire** | Séquence 6 : une panne racontée avec les mots de la rumeur, puis démontée. |
| **VAR avec critères annoncés** | Séquence 6 pour l'annonce des critères, séquences 7 et 8 pour l'application. |
| **Changement de ton** | Séquence 9 : pourquoi le sujet compte (Nouvelle-Calédonie, libertés). |
| **Conclusion par cas** | Séquence 10 : un verdict par forme de censure. |
| **Appel à participer** | Séquence 10 : GitHub et OONI Probe. |

## 5. Plan et état d'avancement

Légende des statuts : ✅ prêt · ✏️ texte à relire ou tester · ⏳ dépend des données de l'acte IV · 🎥 à tourner · 🖼️ visuel à produire.

| # | séquence | durée | rôle | état | ce qu'il manque |
|---|---|---|---|---|---|
| 0 | Accroche | 0:00 – 1:00 | lettre de Matignon, question, promesse, objet mystère | ✏️ 🎥 | citation exacte de la lettre (Blast) ; capture NXDOMAIN |
| 1 | Qui parle, d'où | 1:00 – 1:45 | légitimité et point de vue | ✏️ 🎥 | — |
| (S) | Sponsor (facultatif) | 1:45 – 2:45 | — | — | à décider, pas de VPN |
| 2 | Les trois formes de censure | 2:45 – 4:15 | définition | ✏️ 🖼️ | schéma en trois colonnes |
| 3 | Ce qu'on sait vraiment | 4:15 – 8:00 | chronologie sourcée | ✏️ 🖼️ | captures des articles ; texte de l'amendement n°94 ; décision du Conseil d'État sur la Nouvelle-Calédonie |
| 4 | Comment on coupe un réseau social | 8:00 – 10:30 | DNS, IP, SNI expliqués | ✏️ 🖼️ | animation « annuaire » |
| 5 | Mon dispositif | 10:30 – 13:00 | box, VPS, iPhone, OONI ; le mystère résolu | ✏️ 🎥 🖼️ | photos du dispositif ; capture OONI de sputnikglobe sur les deux SIM |
| 6 | Le piège et la VAR | 13:00 – 14:45 | retournement et critères | ✏️ 🖼️ | exemple réel tiré de tes données (panne ou `ips_differentes`) |
| 7 | Le passé : 24 et 31 octobre | 14:45 – 16:45 | résultats OONI | ✅ 🖼️ | captures d'OONI Explorer et du rapport |
| 8 | L'acte IV en direct | 16:45 – 19:30 | frise et VAR par plateforme | ⏳ | `analyse.py` sur les CSV ; `ooni_verif.py` sur les 6 et 7 novembre |
| 9 | Contenus et shadowban | 19:30 – 23:30 | forme 2 en bref, puis forme 3 en trois expériences (`reviewed`, T8, T9) et la base DSA (T4), puis pourquoi ça compte | ✏️ ⏳ | résultats T1, T2, T8, T9, T3, T4 ; capture du champ `reviewed` ; graphique des courbes de vues |
| 10 | Verdicts et fin | 23:30 – 25:30 | tableau final et appel à participer | ⏳ | verdicts de la séquence 8 |

## 6. Ce qui dépend des données de l'acte IV

| donnée | outil | quand | utilisée en |
|---|---|---|---|
| CSV de la box (Bbox) et du VPS (hébergeur, adresse française) | `analyse.py "mesures_*.csv"` | dimanche | séquences 8 et 10 |
| Mesures OONI publiques des 6 et 7 novembre | `ooni_verif.py --since 2026-11-05 --until 2026-11-08 --focus 2026-11-06,2026-11-07 --mobile` | dimanche ou lundi (délai de publication) | séquences 8 et 10 |
| Tes tests OONI sur iPhone (RED / SFR et Cdiscount / Bouygues ?) | liens OONI Explorer et ASN relevés | au fil du week-end | séquences 5 et 8 |
| Le témoin positif sur chaque point de mesure | `rapport/analyse.md`, section 1 | dimanche | séquence 5 |

**Les trois cas possibles pour la séquence 8 :**
- **Aucun signal.** Verdict : *non prouvé* pour le blocage réseau sur les opérateurs et aux heures mesurés.
- **Signaux isolés.** On les montre, on explique pourquoi ils ne suffisent pas, et le verdict reste *non prouvé*.
- **Motif répété compatible avec un blocage.** Avant d'en parler, on recoupe avec le VPS, OONI et la presse. Même confirmé, on dit « blocage réseau observé chez X de telle heure à telle heure », **sans désigner de responsable** sans source.

## 7. Éléments visuels à produire

- [ ] Capture « `sputnikglobe.com` → NXDOMAIN » (tour de test du moniteur, adresse IPv6 floutée)
- [ ] Captures OONI Explorer : sputnikglobe sur RED et sur Cdiscount (ASN visible)
- [ ] Capture de la lettre de Matignon publiée par Blast, si elle est publique
- [ ] Captures des articles : Clubic, Public Sénat, Maire-info, L'Informé, Sortiraparis
- [ ] Schéma « trois formes de censure »
- [ ] Animation « le DNS comme annuaire » : annuaire honnête, puis annuaire qui ment
- [ ] Schéma du dispositif : box, serveur chez un hébergeur (adresse française), point hors de France (VPN ou second serveur), iPhone avec deux SIM, OONI
- [ ] Frise (`rapport/frise.html`), capturée en haute définition
- [ ] Tableau des verdicts
- [ ] Extraits de `ooni/rapport_ooni.md` (couverture horaire du 24 et du 31 octobre)

## 8. Faits à vérifier avant le tournage

- [ ] **La lettre du 22 octobre** : texte exact, destinataires, plateformes citées (la présence de X fait débat).
- [ ] **L'amendement n°94** : le texte adopté prévoit-il le **blocage d'un site** en l'absence de retrait ? Quel délai (1 heure ou 24 heures) ? Quelle est la suite à l'Assemblée ?
- [ ] **La Nouvelle-Calédonie** : date de la coupure de TikTok (mai 2024) et date de la décision du Conseil d'État (2025), dans les textes officiels.
- [ ] **Les chiffres du 17 octobre** : 550 000 selon le ministère de l'Intérieur, 800 000 selon les organisateurs. Garder les deux, attribués à chacun.
- [ ] **Le réseau de Cdiscount Mobile** : Bouygues ? Le confirmer par l'ASN dans OONI.
- [ ] **Le « Vrai ou fake » de franceinfo** sur les vidéos disparues : le lire avant de le citer.
- [ ] **Toute nouvelle actualité après le 6 novembre** : relancer une recherche avant le tournage.

## 9. Avant de publier

- [ ] Chaque fait à l'écran a sa source et son statut.
- [ ] Aucune phrase n'attribue une cause sans source.
- [ ] Les limites sont dites à voix haute (séquences 6, 9 et 10).
- [ ] Données personnelles floutées : IPv6 de la box, IP, localisation.
- [ ] Le dépôt GitHub est passé en public, et le README est à jour avec les résultats.
- [ ] Le lien du dépôt et les liens OONI sont en description.
- [ ] Relecture par quelqu'un qui n'est pas d'accord avec toi.
