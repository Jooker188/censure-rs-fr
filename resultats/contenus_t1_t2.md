> Version publique : les liens et identifiants des posts suivis sont retirés (posts de particuliers). Données du 9 novembre 2026.

# Retrait de contenus et visibilité : verdicts par test et par plateforme

Points de mesure : France = fixe, fr_resid, vps ; étranger = us_resid (localisation vue par Cloudflare : fixe → {'FR': 618}; fr_resid → {'FR': 7264, '?': 2924}; us_resid → {'US': 9863}; vps → {'FR': 45000}). Pour T1 : France = fr_resid ; étranger = us_resid.

| test | forme | X | TikTok | Instagram | YouTube |
|---|---|---|---|---|---|
| **T1** Retenu en France (visible à l'étranger, pas en France) | 2 | **DÉTECTÉ (1 post(s))** : 1 du mouvement, 0 témoin(s) ; 1 avec mention légale, dont 1 retenu(s) dans toute l'UE, pas en France seulement (voir le détail) | RIEN DÉTECTÉ (982 posts, 3258 comparaisons) | NON TESTABLE (aucun post de cette plateforme dans le corpus) | NON TESTABLE (aucun post de cette plateforme dans le corpus) |
| **T2** Disparitions (visible puis plus visible), avec motif | 2 | **DÉTECTÉ** mouvement 26/1137 (supprimé par l'auteur 17, indisponible sans motif 8, retenu dans le pays 1) ; témoins 19/798 (compte suspendu 8, supprimé par l'auteur 7, indisponible sans motif 4). Retraits par la plateforme : mouvement 1 (dont 1 retenu(s) dans toute l'UE), témoins 8 → **pas plus que les témoins** : disparitions sans action de l'auteur 8/1137 contre 12/798, p = 0.11 | **DÉTECTÉ** mouvement 4/703 (supprimé par l'auteur 4) ; témoins 0/284. Retraits par la plateforme : mouvement 0, témoins 0 → **pas plus que les témoins** : disparitions sans action de l'auteur 0/703 contre 0/284, p = 1.00 | NON TESTABLE (aucun post de cette plateforme dans le corpus) | NON TESTABLE (aucun post de cette plateforme dans le corpus) |
| **T3** Décisions de modération déclarées (base DSA), France | 2 | RIEN DÉTECTÉ (pas de hausse : tendance France : 3 454 → 2 357 par jour (×0.68) ; toutes décisions, tous pays : ×0.91) ; posts non identifiables | RIEN DÉTECTÉ (aucun de nos posts n'a de retrait déclaré ; tendance France : 132 937 → 591 745 par jour (×4.45) ; toutes décisions, tous pays : ×3.72 → hausse générale de ce que déclare la plateforme, pas propre à la France → périmètre déclaré « toute l'UE » et langue non déclarée : impossible de dire si cette hausse concerne la France) | RIEN DÉTECTÉ (pas de hausse : tendance France : 296 196 → 210 704 par jour (×0.71) ; toutes décisions, tous pays : ×0.71) ; posts non identifiables | RIEN DÉTECTÉ (pas de hausse : tendance France : 147 801 → 156 734 par jour (×1.06) ; toutes décisions, tous pays : ×1.05) ; posts non identifiables |
| **T4** Déclassements déclarés (base DSA), France | 3 | RIEN DÉTECTÉ (pas de hausse : tendance non mesurable) ; posts non identifiables | RIEN DÉTECTÉ (aucun de nos posts n'a de déclassement déclaré ; tendance France : 173 038 → 561 599 par jour (×3.25) ; toutes décisions, tous pays : ×3.72 → hausse générale de ce que déclare la plateforme, pas propre à la France → périmètre déclaré « toute l'UE » et langue non déclarée : impossible de dire si cette hausse concerne la France) | **HAUSSE** des déclassements déclarés (périmètre incluant la France) pendant le mouvement (tendance France : 96 → 296 par jour (×3.10) ; toutes décisions, tous pays : ×0.71 → périmètre déclaré « toute l'UE » et langue non déclarée : impossible de dire si cette hausse concerne la France) ; posts non identifiables | RIEN DÉTECTÉ (pas de hausse : tendance non mesurable) ; posts non identifiables |
| **T5** Recherches : aucun résultat en France seulement | 3 | NON RÉALISÉ (test manuel abandonné le 07/11, voir TABLEAU_DE_BORD.md) | NON RÉALISÉ (test manuel abandonné le 07/11, voir TABLEAU_DE_BORD.md) | NON RÉALISÉ (test manuel abandonné le 07/11, voir TABLEAU_DE_BORD.md) | NON RÉALISÉ (test manuel abandonné le 07/11, voir TABLEAU_DE_BORD.md) |
| **T6** Comptes absents de la recherche « from: » (search ban) | 3 | RIEN DÉTECTÉ (36 comptes vérifiés sur 3 session(s), aucun absent de façon répétée ; 9 absence(s) isolée(s) : mouvement 3 ; revendication 4 ; temoin 2) | NON TESTABLE (pas de recherche par auteur fiable) | NON TESTABLE (pas de recherche par auteur fiable) | NON TESTABLE (hors périmètre) |
| **T7** Posts sur le mouvement moins vus que les autres posts du même compte | 3 | RIEN DÉTECTÉ (pas d'écart significatif) — mouvement : 4/11 comptes, rapport médian 1.76, p = 0.549 ; revendication : 2/9 comptes, rapport médian 2.46, p = 0.180 | NON TESTABLE (seulement 7 compte(s) comparables, il en faut au moins 8) | NON TESTABLE (vues non publiques pour les posts) | NON TESTABLE (hors périmètre) |
| **T8** Indicateurs internes TikTok qui changent pendant le suivi (non documentés) | 3 | NON TESTABLE (TikTok seulement) | RIEN DÉTECTÉ (pas d'écart significatif : mouvement 5/699, témoins 2/284, p = 1.000) | NON TESTABLE (TikTok seulement) | NON TESTABLE (TikTok seulement) |
| **T9** Vues qui stagnent, à popularité et âge égaux | 3 | NON TESTABLE (TikTok seulement) | RIEN DÉTECTÉ (mouvement 188/691, témoins 196/283 à popularité et âge égaux, p = 0.379) | NON TESTABLE (TikTok seulement) | NON TESTABLE (TikTok seulement) |

**Lecture.** DÉTECTÉ décrit ce que la plateforme affiche, ou ce qui diffère entre pays. L'origine (demande de l'État ou décision de la plateforme) n'est établie **que** par une mention légale affichée par la plateforme, ou par une demande publiée (Lumen, rapports de transparence). Une disparition côté « mouvement » ne compte que si elle dépasse nettement celle des témoins.

## Détail T1 : retenus en France

- X `(identifiant retiré)` (mouvement) 09/11 00:10 UTC : France = retenu_pays (mention légale), us_resid=visible ; **retenu dans toute l'UE** selon la plateforme : c'est le périmètre des sanctions européennes contre certains médias d'État russes (RT, Sputnik…), pas une mesure propre à la France ni au mouvement. Lire le texte affiché pour savoir de quel compte il s'agit — (lien retiré)

## Détail T2 : disparitions

- X `(identifiant retiré)` (mouvement) 09/11 14:05 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (mouvement) 09/11 14:31 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (mouvement) 07/11 04:04 UTC : indisponible sans motif — (lien retiré)
- X `(identifiant retiré)` (mouvement) 06/11 23:19 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (mouvement) 08/11 08:34 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (mouvement) 06/11 23:31 UTC : indisponible sans motif — (lien retiré)
- X `(identifiant retiré)` (mouvement) 07/11 15:38 UTC : indisponible sans motif — (lien retiré)
- X `(identifiant retiré)` (mouvement) 07/11 06:38 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (mouvement) 06/11 23:40 UTC : indisponible sans motif — (lien retiré)
- X `(identifiant retiré)` (mouvement) 08/11 12:33 UTC : indisponible sans motif — (lien retiré)
- X `(identifiant retiré)` (mouvement) 08/11 02:47 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (mouvement) 07/11 19:34 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (mouvement) 09/11 09:29 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (mouvement) 07/11 22:36 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (mouvement) 08/11 14:51 UTC : indisponible sans motif — (lien retiré)
- X `(identifiant retiré)` (mouvement) 08/11 09:10 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (mouvement) 08/11 14:50 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (mouvement) 07/11 20:53 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (mouvement) 07/11 22:32 UTC : retenu dans le pays (mention légale) ; **retenu dans toute l'UE** selon la plateforme : c'est le périmètre des sanctions européennes contre certains médias d'État russes (RT, Sputnik…), pas une mesure propre à la France ni au mouvement. Lire le texte affiché pour savoir de quel compte il s'agit — (lien retiré)
- X `(identifiant retiré)` (mouvement) 08/11 15:05 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (mouvement) 08/11 10:00 UTC : indisponible sans motif — (lien retiré)
- X `(identifiant retiré)` (mouvement) 08/11 09:20 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (mouvement) 08/11 18:22 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (mouvement) 08/11 01:01 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (mouvement) 08/11 00:19 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (mouvement) 09/11 02:23 UTC : indisponible sans motif — (lien retiré)
- X `(identifiant retiré)` (temoin) 07/11 10:26 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (temoin) 07/11 16:20 UTC : indisponible sans motif — (lien retiré)
- X `(identifiant retiré)` (temoin) 06/11 23:18 UTC : compte suspendu — (lien retiré)
- X `(identifiant retiré)` (temoin) 06/11 23:25 UTC : compte suspendu — (lien retiré)
- X `(identifiant retiré)` (temoin) 07/11 19:09 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (temoin) 07/11 18:56 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (temoin) 07/11 19:46 UTC : compte suspendu — (lien retiré)
- X `(identifiant retiré)` (temoin) 07/11 21:18 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (temoin) 07/11 20:36 UTC : compte suspendu — (lien retiré)
- X `(identifiant retiré)` (temoin) 07/11 23:29 UTC : indisponible sans motif — (lien retiré)
- X `(identifiant retiré)` (temoin) 09/11 01:47 UTC : indisponible sans motif — (lien retiré)
- X `(identifiant retiré)` (temoin) 07/11 19:18 UTC : compte suspendu — (lien retiré)
- X `(identifiant retiré)` (temoin) 07/11 19:23 UTC : compte suspendu — (lien retiré)
- X `(identifiant retiré)` (temoin) 07/11 19:52 UTC : compte suspendu — (lien retiré)
- X `(identifiant retiré)` (temoin) 07/11 19:58 UTC : compte suspendu — (lien retiré)
- X `(identifiant retiré)` (temoin) 09/11 14:57 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (temoin) 08/11 23:58 UTC : indisponible sans motif — (lien retiré)
- X `(identifiant retiré)` (temoin) 09/11 12:00 UTC : supprimé par l'auteur — (lien retiré)
- X `(identifiant retiré)` (temoin) 08/11 08:15 UTC : supprimé par l'auteur — (lien retiré)
- TikTok `(identifiant retiré)` (mouvement) 08/11 01:59 UTC : supprimé par l'auteur — (lien retiré)
- TikTok `(identifiant retiré)` (mouvement) 08/11 18:46 UTC : supprimé par l'auteur — (lien retiré)
- TikTok `(identifiant retiré)` (mouvement) 08/11 17:20 UTC : supprimé par l'auteur — (lien retiré)
- TikTok `(identifiant retiré)` (mouvement) 08/11 01:09 UTC : supprimé par l'auteur — (lien retiré)

## Contrôles positifs

- X `(identifiant retiré)` depuis fixe : 06/11 23:34 visible
- X `(identifiant retiré)` depuis fr_resid : 07/11 01:25 supprime_auteur → 07/11 14:07 supprime_auteur → 07/11 21:57 supprime_auteur → 08/11 02:21 supprime_auteur → 09/11 01:16 supprime_auteur
- X `(identifiant retiré)` depuis us_resid : 07/11 01:16 supprime_auteur → 07/11 13:16 supprime_auteur → 07/11 19:56 supprime_auteur → 08/11 02:24 supprime_auteur → 08/11 23:29 supprime_auteur
- X `(identifiant retiré)` depuis vps : 06/11 23:24 visible → 07/11 01:43 supprime_auteur → 07/11 04:27 supprime_auteur → 07/11 06:34 supprime_auteur → 07/11 10:08 supprime_auteur → 07/11 13:08 supprime_auteur → 07/11 15:45 supprime_auteur → 07/11 18:35 supprime_auteur → 07/11 20:49 supprime_auteur → 08/11 00:04 supprime_auteur → 08/11 04:04 supprime_auteur → 08/11 07:48 supprime_auteur → 08/11 10:58 supprime_auteur → 08/11 12:40 supprime_auteur → 08/11 18:25 supprime_auteur → 08/11 21:32 supprime_auteur → 08/11 23:15 supprime_auteur → 09/11 02:45 supprime_auteur → 09/11 06:54 supprime_auteur → 09/11 11:22 supprime_auteur → 09/11 11:47 supprime_auteur
- X `(identifiant retiré)` depuis fixe : 06/11 23:04 retenu_pays (légal)
- X `(identifiant retiré)` depuis fr_resid : 07/11 01:48 retenu_pays (légal) → 07/11 13:36 retenu_pays (légal) → 07/11 19:36 retenu_pays (légal) → 07/11 23:19 retenu_pays (légal) → 09/11 01:22 retenu_pays (légal)
- X `(identifiant retiré)` depuis us_resid : 07/11 00:49 visible → 07/11 13:30 visible → 07/11 20:57 visible → 08/11 00:00 visible → 08/11 22:39 visible
- X `(identifiant retiré)` depuis vps : 06/11 23:49 retenu_pays (légal) → 07/11 01:17 retenu_pays (légal) → 07/11 04:08 retenu_pays (légal) → 07/11 06:59 retenu_pays (légal) → 07/11 09:52 retenu_pays (légal) → 07/11 12:45 retenu_pays (légal) → 07/11 16:30 retenu_pays (légal) → 07/11 19:52 retenu_pays (légal) → 07/11 23:37 retenu_pays (légal) → 08/11 03:34 retenu_pays (légal) → 08/11 07:01 retenu_pays (légal) → 08/11 09:37 retenu_pays (légal) → 08/11 12:33 retenu_pays (légal) → 08/11 18:03 retenu_pays (légal) → 08/11 19:42 retenu_pays (légal) → 08/11 22:09 retenu_pays (légal) → 09/11 01:58 retenu_pays (légal) → 09/11 07:03 retenu_pays (légal) → 09/11 10:45 retenu_pays (légal) → 09/11 12:09 retenu_pays (légal)

## T2 par période de publication (disparus / suivis)

Comparer à âge égal : un post ancien et un post récent n'ont pas le même risque d'être supprimé.

| réseau | période | mouvement | revendication | témoins |
|---|---|---|---|---|
| X | 1. jusqu'au 19 oct | 0/40 | 0/1 | 0/40 |
| X | 2. 20-26 oct | 1/40 | 0/8 | 0/40 |
| X | 3. 27 oct-4 nov | 0/7 | 3/103 | 1/60 |
| X | 4. 5 nov et après | 21/878 | 1/60 | 18/658 |
| TikTok | 0. avant sept. 2026 | — | — | 0/183 |
| TikTok | 1. jusqu'au 19 oct | 0/120 | — | 0/24 |
| TikTok | 2. 20-26 oct | 0/99 | — | 0/4 |
| TikTok | 3. 27 oct-4 nov | 1/65 | — | 0/32 |
| TikTok | 4. 5 nov et après | 3/419 | — | 0/41 |
