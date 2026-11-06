# Recherches utilisées pour collecter les posts

> Ce fichier fixe **les recherches faites, sur quel réseau, quand et comment**. Il sert à reproduire la collecte et à l'expliquer dans la vidéo.
> Règle : **on ne change pas une recherche en cours de route**. Si on en ajoute une, on la note avec sa date d'ajout.

## Méthode commune

- **Outil** : [Zeeschuimer](https://github.com/digitalmethodsinitiative/zeeschuimer) (extension Firefox des chercheurs de l'université d'Amsterdam). Il enregistre les posts que le navigateur affiche pendant qu'on fait défiler les résultats.
- **Compte** : mon vrai compte, jamais un faux. ⚠️ Les résultats sont **personnalisés** : un autre compte verrait d'autres posts. C'est un échantillon, pas un comptage de tout ce qui a été publié.
- **Défilement** : 1 à 2 minutes par recherche.
- **Export** : en `.ndjson (original)`, un fichier par réseau et par catégorie. Noms de fichiers : `mouvement_x.ndjson`, `temoin_x.ndjson`, `revendication_x.ndjson`, `mouvement_tiktok.ndjson`, etc.
- **Avant chaque catégorie**, on vide les données dans Zeeschuimer. **Après**, on désactive la capture.
- **Les témoins** sont des recherches neutres, collectées exactement de la même façon, qui servent de point de comparaison.
- **Les hashtags réels du mouvement** seront affinés à partir des données : `importer.py` listera les hashtags qui reviennent le plus souvent avec ceux de départ. Les nouvelles recherches qui en sortent seront ajoutées en bas, avec leur date.

## Statut des recherches de départ

| recherche | statut | source |
|---|---|---|
| `#17octobre` | **vérifié** : environ 800 millions de vues sur TikTok (données Visibrain) | [franceinfo](https://franceinfo.fr/vrai-ou-fake/manifestations-contre-la-vie-chere-des-videos-ont-elles-disparu-des-reseaux-sociaux_8268335.html) |
| `#24octobre` | **vérifié** : environ 121 millions de vues sur TikTok (données Visibrain) | même source |
| « égalité réelle » | mot d'ordre de l'acte IV (documenté) ; à tester comme recherche | [Sud Radio](https://www.sudradio.fr/sud-radio/acte-4-des-gilets-jaunes-90-mobilisations-sous-haute-surveillance-ce-samedi-7-novembre) |
| « tout bloquer » | mot d'ordre de l'appel d'origine (documenté) ; à tester comme recherche | [ICI](https://www.ici.fr/infos/economie-social/prix-des-carburants-sur-tik-tok-des-jeunes-appellent-a-relancer-le-mouvement-des-gilets-jaunes-le-17-octobre-9122130) |
| « gilets jaunes », `#acte4`, `#acteIV`, `#7novembre` | à tester (aucune source sur un hashtag officiel de l'acte IV) | — |

**⚠️ Bruit connu.** Ces recherches ramènent aussi des posts sans rapport avec le mouvement :
- `#17octobre` sert aussi à commémorer le **massacre du 17 octobre 1961** ;
- `#31octobre`, c'est **Halloween** (non utilisé pour cette raison) ;
- « gilets jaunes » ramène aussi des posts sur le mouvement de 2018.

Les filtres de date **ne suppriment pas** le bruit de `#17octobre`, puisque la commémoration de 1961 a lieu les mêmes jours. Ce tri se fait à l'import, d'après les autres mots du post (« 1961 », « Algériens »…). Sur TikTok et Instagram, qui n'ont pas de filtre de date, tout le tri se fait à l'import.

---

## X

Sur X, les filtres de date marchent. `f=live` correspond à l'onglet **« Récent »**, qui affiche **les posts les plus récents d'abord**.

**Pourquoi `until:` seulement pour X1 et X2.** Ces deux recherches visent des actes **passés**. Sans `until:`, « Récent » afficherait d'abord les posts d'aujourd'hui qui reparlent du 17 octobre, et il faudrait faire défiler trois semaines de posts pour atteindre ceux du jour même. Le `until:` place la recherche sur les jours de l'acte. On veut ces posts anciens pour vérifier s'ils sont toujours en ligne. Les recherches X3 à X6 suivent l'actualité : elles n'ont qu'un `since:` et restent ouvertes jusqu'à aujourd'hui.

### Mouvement

| # | requête | adresse |
|---|---|---|
| X1 | `#17octobre since:2026-10-15 until:2026-10-19` | `https://x.com/search?q=%2317octobre%20since%3A2026-10-15%20until%3A2026-10-19&f=live` |
| X2 | `#24octobre since:2026-10-22 until:2026-10-26` | `https://x.com/search?q=%2324octobre%20since%3A2026-10-22%20until%3A2026-10-26&f=live` |
| X3 | `"gilets jaunes" since:2026-11-01` | `https://x.com/search?q=%22gilets%20jaunes%22%20since%3A2026-11-01&f=live` |
| X4 | `#acte4 OR #acteIV OR #7novembre` | `https://x.com/search?q=%23acte4%20OR%20%23acteIV%20OR%20%237novembre&f=live` |
| X5 | `"égalité réelle" since:2026-11-01` | `https://x.com/search?q=%22%C3%A9galit%C3%A9%20r%C3%A9elle%22%20since%3A2026-11-01&f=live` |
| X6 | `"tout bloquer" OR "bloquons tout" since:2026-11-01` | `https://x.com/search?q=%22tout%20bloquer%22%20OR%20%22bloquons%20tout%22%20since%3A2026-11-01&f=live` |

### Témoins

| # | requête | adresse |
|---|---|---|
| XT1 | `météo lang:fr since:2026-10-15` | `https://x.com/search?q=m%C3%A9t%C3%A9o%20lang%3Afr%20since%3A2026-10-15&f=live` |
| XT2 | `"ligue 1" lang:fr since:2026-10-15` | `https://x.com/search?q=%22ligue%201%22%20lang%3Afr%20since%3A2026-10-15&f=live` |
| XT3 | `météo lang:fr since:2026-10-15 until:2026-10-19` | `https://x.com/search?q=m%C3%A9t%C3%A9o%20lang%3Afr%20since%3A2026-10-15%20until%3A2026-10-19&f=live` |
| XT4 | `"ligue 1" lang:fr since:2026-10-22 until:2026-10-26` | `https://x.com/search?q=%22ligue%201%22%20lang%3Afr%20since%3A2026-10-22%20until%3A2026-10-26&f=live` |
| XT5 | `météo lang:fr since:2026-10-28 until:2026-11-03` | `https://x.com/search?q=m%C3%A9t%C3%A9o%20lang%3Afr%20since%3A2026-10-28%20until%3A2026-11-03&f=live` |

**Pourquoi XT3 et XT4 (ajoutées le 06/11).** XT1 et XT2 n'ont ramené que des posts du jour même : ces sujets produisent tellement de posts qu'on ne remonte pas plus loin en 2 minutes. Or les témoins doivent avoir **le même âge** que les posts du mouvement (X1 et X2 datent des 17 et 24 octobre). Sinon, la comparaison des disparitions (T2) et des vues est faussée. XT3 et XT4 visent donc les mêmes jours que X1 et X2.

---

## TikTok

TikTok n'a pas de filtre de date, et son moteur ne reconnaît pas les opérateurs `OR` ni les guillemets. On fait **une recherche par terme**. Pour chaque hashtag, deux entrées sont possibles : la **page du hashtag** (`/tag/`) ou la **recherche** (`/search`). Commence par la page du hashtag. Si elle n'affiche rien, prends la recherche.

### Mouvement

| # | terme | page du hashtag | recherche |
|---|---|---|---|
| T1 | `#17octobre` | `https://www.tiktok.com/tag/17octobre` | `https://www.tiktok.com/search?q=%2317octobre` |
| T2 | `#24octobre` | `https://www.tiktok.com/tag/24octobre` | `https://www.tiktok.com/search?q=%2324octobre` |
| T3 | `#giletsjaunes` | `https://www.tiktok.com/tag/giletsjaunes` | `https://www.tiktok.com/search?q=gilets%20jaunes` |
| T4 | `#acte4` | `https://www.tiktok.com/tag/acte4` | `https://www.tiktok.com/search?q=acte%204` |
| T5 | `#egalitereelle` | `https://www.tiktok.com/tag/egalitereelle` | `https://www.tiktok.com/search?q=%C3%A9galit%C3%A9%20r%C3%A9elle` |
| T6 | `#toutbloquer` | `https://www.tiktok.com/tag/toutbloquer` | `https://www.tiktok.com/search?q=tout%20bloquer` |

### Témoins

| # | terme | adresse |
|---|---|---|
| TT1 | `#meteo` | `https://www.tiktok.com/tag/meteo` |
| TT2 | `#ligue1` | `https://www.tiktok.com/tag/ligue1` |

---

## Instagram

Instagram n'a pas de filtre de date. Ses pages de hashtags ont changé de format ces dernières années : essaie d'abord l'adresse de recherche par mot-clé, puis l'ancienne page de hashtag. Zeeschuimer ne capture que les **posts et les Reels**.

### Mouvement

| # | terme | recherche par mot-clé | ancienne page de hashtag |
|---|---|---|---|
| I1 | `#17octobre` | `https://www.instagram.com/explore/search/keyword/?q=%2317octobre` | `https://www.instagram.com/explore/tags/17octobre/` |
| I2 | `#24octobre` | `https://www.instagram.com/explore/search/keyword/?q=%2324octobre` | `https://www.instagram.com/explore/tags/24octobre/` |
| I3 | `#giletsjaunes` | `https://www.instagram.com/explore/search/keyword/?q=%23giletsjaunes` | `https://www.instagram.com/explore/tags/giletsjaunes/` |
| I4 | `#acte4` | `https://www.instagram.com/explore/search/keyword/?q=%23acte4` | `https://www.instagram.com/explore/tags/acte4/` |
| I5 | `#egalitereelle` | `https://www.instagram.com/explore/search/keyword/?q=%23egalitereelle` | `https://www.instagram.com/explore/tags/egalitereelle/` |
| I6 | `#toutbloquer` | `https://www.instagram.com/explore/search/keyword/?q=%23toutbloquer` | `https://www.instagram.com/explore/tags/toutbloquer/` |

### Témoins

| # | terme | adresse |
|---|---|---|
| IT1 | `#meteo` | `https://www.instagram.com/explore/search/keyword/?q=%23meteo` |
| IT2 | `#ligue1` | `https://www.instagram.com/explore/search/keyword/?q=%23ligue1` |

---

## YouTube

Hors Zeeschuimer. Plus tard, éventuellement, via l'API officielle avec une clé gratuite, et les mêmes termes.

---

## Catégorie « revendication » : posts qui affirment une censure

**But.** Collecter les posts qui **affirment** une censure : « mes tweets sont censurés », « mon compte a été suspendu », « TikTok est coupé ». Ces posts servent deux fois :
1. **Documenter la rumeur** : ce qui est affirmé, par qui (type de compte), à quel moment.
2. **Vérifier les affirmations précises.** Quand un post désigne un compte ou un post précis (« ma vidéo a été supprimée »), on l'ajoute dans `ajouts_manuels.txt` avec la note `a_verifier`. `contenus.py` vérifie alors s'il est vraiment indisponible, depuis la France et depuis l'Allemagne, et avec quel motif.

**À ne pas mélanger.** Ces posts sont exportés **à part** (`revendication_x.ndjson`, etc.), et ne vont ni dans « mouvement » ni dans « témoin ». Leur taux de retrait n'est pas comparable à celui des autres posts.

**Statut.** Une affirmation de censure n'est **pas une preuve** de censure. Dans la vidéo, on les présente comme des affirmations, confrontées aux mesures.

### X (onglet Récent)

| # | requête | adresse |
|---|---|---|
| X8 | `(censure OR censuré OR shadowban OR shadowbanned OR "shadow ban") (manif OR "gilets jaunes" OR #acte4 OR #7novembre OR #17octobre OR #24octobre) since:2026-10-15` | `https://x.com/search?q=%28censure%20OR%20censur%C3%A9%20OR%20shadowban%20OR%20shadowbanned%20OR%20%22shadow%20ban%22%29%20%28manif%20OR%20%22gilets%20jaunes%22%20OR%20%23acte4%20OR%20%237novembre%20OR%20%2317octobre%20OR%20%2324octobre%29%20since%3A2026-10-15&f=live` |
| X9 | `("compte suspendu" OR "compte bloqué" OR "tweet supprimé" OR "vidéo supprimée" OR "post supprimé") (manif OR "gilets jaunes" OR #acte4 OR #7novembre) since:2026-10-15` | `https://x.com/search?q=%28%22compte%20suspendu%22%20OR%20%22compte%20bloqu%C3%A9%22%20OR%20%22tweet%20supprim%C3%A9%22%20OR%20%22vid%C3%A9o%20supprim%C3%A9e%22%20OR%20%22post%20supprim%C3%A9%22%29%20%28manif%20OR%20%22gilets%20jaunes%22%20OR%20%23acte4%20OR%20%237novembre%29%20since%3A2026-10-15&f=live` |
| X10 | `(TikTok OR Instagram OR Snapchat) (coupé OR coupure OR bloqué OR "ne marche plus") (manif OR "gilets jaunes" OR #acte4 OR #7novembre) since:2026-10-15` | `https://x.com/search?q=%28TikTok%20OR%20Instagram%20OR%20Snapchat%29%20%28coup%C3%A9%20OR%20coupure%20OR%20bloqu%C3%A9%20OR%20%22ne%20marche%20plus%22%29%20%28manif%20OR%20%22gilets%20jaunes%22%20OR%20%23acte4%20OR%20%237novembre%29%20since%3A2026-10-15&f=live` |

### TikTok

| # | terme | adresse |
|---|---|---|
| T7 | `censure manif` | `https://www.tiktok.com/search?q=censure%20manif` |
| T8 | `shadowban gilets jaunes` | `https://www.tiktok.com/search?q=shadowban%20gilets%20jaunes` |
| T9 | `#censure` | `https://www.tiktok.com/tag/censure` |

### Instagram

| # | terme | adresse |
|---|---|---|
| I7 | `#censure` | `https://www.instagram.com/explore/search/keyword/?q=%23censure` |
| I8 | `#shadowban` | `https://www.instagram.com/explore/search/keyword/?q=%23shadowban` |

⚠️ Sur TikTok et Instagram, `#censure` et `#shadowban` ramènent beaucoup de posts sans lien avec le mouvement (créateurs qui se plaignent de leurs vues, autres pays). Le tri se fait à l'import.

---

## Journal de collecte (à remplir à chaque session)

| date et heure | réseau | n° de recherche | durée de défilement | items (compteur Zeeschuimer) | fichier exporté | remarques (peu de résultats, bruit, blocage…) |
|---|---|---|---|---|---|---|
| 06/11 soir | X | X1 à X8, X10 | 1 à 2 min | 390 (376 posts uniques) | `zeeschuimer-export-twitter.com-2026-11-06T213811.ndjson` | X5 (« égalité réelle ») : 1 seul post. Un seul fichier pour toutes les catégories (la catégorie est déduite de la recherche). |
| 06/11 soir | X | X9 | — | 0 | — | **Aucun résultat.** Personne dans cette recherche n'écrit « compte suspendu » ou « tweet supprimé » à propos de la manif. Ce n'est pas une preuve : la requête est peut-être trop restrictive. |
| 06/11 soir | X | XT1, XT2 | 1 à 2 min | 100 posts | `zeeschuimer-export-twitter.com-2026-11-06T214653.ndjson` | Tous du 06/11 : âge différent des posts du mouvement, d'où XT3 et XT4. |
| 06/11 soir | X | XT3, XT4 | 1 à 2 min | 80 posts | `zeeschuimer-export-twitter.com-2026-11-06T214907.ndjson` | Témoins datés comme X1 et X2 (40 posts du 17 au 19 octobre, 40 du 22 au 26 octobre). Il manque encore des témoins pour la période du 27 octobre au 4 novembre, où se trouvent la plupart des posts « revendication » (103 sur 153). |
| 06/11 soir | X | XT5 | 1 à 2 min | 60 posts | `zeeschuimer-export-twitter.com-2026-11-06T223505.ndjson` | Comble le trou du 27 octobre au 4 novembre. **Bilan X : 616 posts (223 mouvement, 153 revendication, 240 témoins), avec des témoins sur les quatre périodes.** |

## Recherches ajoutées après coup

| date d'ajout | réseau | requête | pourquoi (par exemple : hashtag fréquent dans les données) |
|---|---|---|---|
| 2026-11-06 | X (X7) | `#RadioLondres since:2026-11-01` → `https://x.com/search?q=%23RadioLondres%20since%3A2026-11-01&f=live` | Vu dans un post qui appelle à détourner ce hashtag pour parler des cortèges et « éviter d'être shadowbanned ». ⚠️ Hashtag ancien, utilisé depuis des années pour d'autres choses (par exemple les soirs d'élection) : beaucoup de bruit. |
| 2026-11-06 | TikTok, Instagram | `#radiolondres` → `https://www.tiktok.com/tag/radiolondres` ; `https://www.instagram.com/explore/search/keyword/?q=%23radiolondres` | Même raison. |
| 2026-11-06 | (constat) | `#acte4`, `#7novembre` | Leur usage est confirmé par un post réel (X4 n'est plus une supposition). |

## Ajouts manuels

Les posts repérés à la main, par exemple un post qui annonce de la censure ou qui appelle à la contourner, vont dans `ajouts_manuels.txt`, une adresse par ligne. `importer.py` les inclut **toujours** dans le corpus, quel que soit l'échantillon tiré, avec la marque `manuel`.

**Limite de méthode à dire dans la vidéo.** Si le mouvement passe à un vocabulaire codé (morse, hashtags détournés), une collecte par mots-clés en rate une partie. Ce n'est pas de la censure, c'est une limite de la collecte.

## Pour la vidéo

- Montrer ce fichier à l'écran : les recherches ont été **fixées à l'avance**, elles ne sont pas choisies pour arranger le résultat.
- Le dire clairement : « un échantillon personnalisé par mon compte, pas un comptage de tout ce qui a été publié ».
- Chiffres à reporter ici après l'import : nombre de posts par réseau et par catégorie, hashtags associés les plus fréquents, part du bruit (par exemple les posts sur 1961).
