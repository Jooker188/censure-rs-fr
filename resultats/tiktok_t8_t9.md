# TikTok : indicateurs internes (T8) et croissance des vues (T9)

Généré le 2026-11-09 15:09 UTC à partir de 984 vidéos suivies.

## T8 : changements d'indicateurs internes pendant le suivi

⚠️ Champs **non documentés** par TikTok : on constate qu'ils changent, on ne leur donne pas de sens.

| groupe | vidéos suivies (≥ 2 observations) | vidéos avec au moins un changement |
|---|---|---|
| mouvement | 699 | 5 |
| temoin | 284 | 2 |

**Verdict T8 (TikTok)** : RIEN DÉTECTÉ (pas d'écart significatif : mouvement 5/699, témoins 2/284, p = 1.000)

| indicateur | changement | mouvement | témoins |
|---|---|---|---|
| conclu_refine_reason |  → 1101 | 1 | 1 |
| conclu_refine_reason | 1101 →  | 0 | 1 |
| conclu_refine_reason | 1101 → 20031101 | 1 | 0 |
| display_penalty_type |  → 0 | 1 | 1 |
| display_penalty_type | 0 →  | 0 | 1 |
| display_policy |  → 0 | 1 | 1 |
| display_policy | 0 →  | 0 | 1 |
| display_ui_type |  → 0 | 1 | 1 |
| display_ui_type | 0 →  | 0 | 1 |
| ec_global_verdict |  → 1 | 1 | 0 |
| ec_global_verdict | 1 → 3 | 2 | 0 |
| is_prohibited | False →  | 2 | 0 |
| is_reviewing | False →  | 2 | 0 |
| item_control | {"can_comment":true,"can_creator_redirect":true,"can_music_redirect":true,"can_repost":true,"can_share":true} → {} | 1 | 0 |
| item_control | {"can_repost":true} → {"can_comment":true,"can_creator_redirect":true,"can_music_redirect":true,"can_repost":true,"can_share":true} | 1 | 1 |
| item_control | {"can_repost":true} → {} | 1 | 0 |
| reviewed |  → 0 | 1 | 1 |
| reviewed | 0 →  | 0 | 1 |
| reviewed | 1 → 0 | 1 | 0 |
| video_status |  → 10 | 1 | 1 |
| video_status | 10 →  | 0 | 1 |

## T9 : stagnation des vues, à popularité et âge égaux

Stagnation : moins de 1% de vues en plus sur au moins 24 h de suivi. Popularité et âge mesurés à la première observation.

| popularité | âge | mouvement : stagnent / suivies | témoins : stagnent / suivies | p (Fisher) |
|---|---|---|---|---|
| 100 k – 1 M | 3 – 14 j | 10/14 | 5/9 | 0.657 |
| 100 k – 1 M | < 3 j | 3/36 | 0/5 | 1.000 |
| 100 k – 1 M | > 14 j | 41/52 | 37/54 | 0.274 |
| < 100 k | 3 – 14 j | 18/67 | 14/24 | 0.012 |
| < 100 k | < 3 j | 11/368 | 3/34 | 0.106 |
| < 100 k | > 14 j | 59/93 | 6/16 | 0.059 |
| > 1 M | 3 – 14 j | 1/2 | 0/1 | 1.000 |
| > 1 M | < 3 j | 1/5 | 0/1 | 1.000 |
| > 1 M | > 14 j | 44/54 | 131/139 | 0.011 |

Test global, tranche par tranche combinées (Cochran-Mantel-Haenszel), sur les tranches où les deux groupes sont présents : mouvement 188/691 stagnent, témoins 196/283 ; stagnations du mouvement observées 188, attendues à traitement égal 192.3, p = 0.3787.


**Verdict T9 (TikTok)** : RIEN DÉTECTÉ (mouvement 188/691, témoins 196/283 à popularité et âge égaux, p = 0.379)

**Lecture.** T8 et T9 décrivent des différences de traitement ou de diffusion. Ils ne disent ni ce que signifient les indicateurs internes, ni qui a décidé. La modération ordinaire (contenus violents, signalements) peut produire les mêmes écarts.
