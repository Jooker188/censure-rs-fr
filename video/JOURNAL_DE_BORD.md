# Journal de bord : les coulisses de l'enquête

> Récit chronologique de ce qui s'est passé, de ce qu'on a trouvé et des erreurs corrigées. C'est la matière brute du script (`SCRIPT.md`) : chaque entrée indique la séquence où elle peut servir.
> Heures approximatives, heure de Paris. À compléter au fil du suivi.

---

## Vendredi 6 novembre 2026

### Nuit : préparer les sondes

- **Vérification du contexte** par recherche web : la lettre de Matignon du 22 octobre (révélée par Blast), le refus des opérateurs, l'amendement n°94 voté au Sénat le 27 octobre, le groupe de contact du 30 octobre, l'acte IV les 6 et 7 novembre. **Correction du brief de départ** : 800 000 manifestants le 17 octobre, c'est le chiffre des **organisateurs** ; l'Intérieur en compte 550 000. → séquence 3
- **Données publiques OONI du 17 au 31 octobre.** Sur les connexions fixes, les quatre opérateurs sont testés presque à chaque heure pour les grands réseaux sociaux, et aucun signal de blocage n'apparaît. Verdict : **non prouvé**. Sur le mobile, il n'y a presque aucune mesure : **non testable**. → séquence 7
- **Deux fausses pistes dans OONI**, à raconter :
  - les « anomalies » de Facebook chez Free viennent d'un seul téléphone Android, qui les produit toutes les heures depuis le 10 octobre, donc avant le mouvement ;
  - les « blocages confirmés » du 27 octobre sont une page de blocage **iranienne**, vue par une sonde installée chez un hébergeur. → séquence 7
- **Vers 4 h 45 : premier tour du moniteur sur la box Bouygues.** Tout est accessible. Le **témoin positif** `sputnikglobe.com` est bloqué par le DNS de Bouygues (réponse NXDOMAIN). 1.1.1.1 n'est pas intercepté. Découverte au passage : mon PC utilise un DNS chiffré (1.1.1.1), donc un filtrage DNS de l'opérateur ne l'aurait même pas touché. → séquences 4 et 5
- **Premier tour depuis le VPS** : tout est accessible. `sputnikglobe.com` n'est **pas** bloqué depuis un hébergeur, ce qui montre le contraste avec la box. Reddit répond « interdit » (403) depuis un datacenter : c'est un exemple de « faux blocage ». → séquences 5 et 6
- **OONI sur l'iPhone avec deux SIM**, RED (réseau SFR) et Cdiscount (réseau Bouygues, à confirmer par l'ASN) : `sputnikglobe.com` est bloqué sur les deux, tout le reste est accessible. → séquence 5

### Journée : élargir aux formes 2 et 3

- **Décision : tester aussi le retrait de contenus et la visibilité**, pas seulement la coupure réseau. → séquences 2 et 9
- **Essai de Minet**, l'outil du médialab de Sciences Po : ses collecteurs pour X (erreur 404), Instagram (page HTML) et TikTok (réponse vide) sont **cassés**. Les plateformes changent leurs API plus vite que les outils de recherche ne suivent. → séquence 5 ou 9
- **Choix de Zeeschuimer**, l'extension Firefox des chercheurs d'Amsterdam : elle enregistre ce que le navigateur reçoit déjà quand on fait défiler une page. Elle ne fabrique aucune requête, donc elle résiste aux changements des plateformes. → séquence 5
- **Les recherches sont fixées à l'avance** dans `contenus/RECHERCHES.md`. Les seuls hashtags vérifiés en presse sont #17octobre (environ 800 millions de vues sur TikTok, données Visibrain citées par franceinfo) et #24octobre. Bruit connu : #17octobre sert aussi à la commémoration du 17 octobre 1961. → séquences 5 et 6

### Soir : la collecte sur X

- **Le post « #RadioLondres »** : un appel à détourner ce hashtag « pour parler en morse des cortèges » et « éviter d'être shadowbanned ». C'est la rumeur formulée par quelqu'un, une **affirmation, pas une preuve**. → séquences 0 et 9 (pseudo flouté)
- **Le post « stats anormalement basses »** sur la manif du 31 octobre, « je pense que la date est censurée ». C'est l'hypothèse du shadowban, qu'on a découpée en tests (présence dans la recherche, portée comparée). → séquence 9
- **Création d'une catégorie « revendication »** pour les posts qui affirment une censure, séparée du mouvement et des témoins.
- **La recherche « compte suspendu », « tweet supprimé »… + manif ne donne aucun résultat.** C'est une information, pas une preuve. → séquence 9
- **Erreur de méthode corrigée** : les premiers témoins (« météo », « ligue 1 ») ne dataient que du jour même, alors que les posts du mouvement remontent au 17 octobre. Ajout de témoins datés comme le mouvement (XT3 à XT5). → séquence 6 (« comparer à âge égal »)
- **Bilan X : 616 posts** (223 mouvement, 153 revendication, 240 témoins).

### Soir : la collecte sur TikTok

- **Les pages de hashtag sont très bruitées** : 230 vidéos sur 521 ne portaient pas le hashtag de la page. TikTok en ajoute des « proches » quand on fait défiler (72 sur 118 pour #giletsjaunes, 53 sur 58 pour #toutbloquer). Elles sont écartées à l'import. → séquence 5 ou 6
- **Découverte des indicateurs internes de TikTok** (`penaltyContext`, `reviewed`), visibles dans les données que reçoit le navigateur et non documentés.
- **Le marquage `reviewed` suit d'abord la popularité** : médiane de 1,6 million de vues pour les vidéos marquées, contre 43 000 pour les autres.
- **Avec des témoins aussi populaires** (#recette, #foot), à popularité égale, les vidéos du mouvement sont plus souvent marquées : 39 % contre 19 % au-dessus d'un million de vues (p ≈ 0,04), et 16 % contre 2 % entre 100 000 et un million (p ≈ 0,003). **C'est une différence réelle, pas une preuve** : on ne sait pas ce que veut dire « reviewed », et la modération ordinaire de l'actualité et des images de manifestation suffit à l'expliquer. → séquence 9, passage clé « observer n'est pas attribuer »
- **Bilan : 981 posts suivis** (X + TikTok).

### Nuit : le suivi des contenus démarre

- **Contrôles positifs**, sur le même principe que `sputnikglobe.com` :
  - un tweet de test publié, puis **supprimé après le premier passage** ;
  - un tweet de RT, que l'outil voit bien « retenu dans le pays » depuis la France. Le détecteur détecte. → séquences 5 et 6
- **Premier passage** : côté mouvement, 2 posts indisponibles et 1 supprimé par son auteur ; côté témoins, 2 comptes suspendus. Rien d'anormal à ce stade.
- **Faux positif corrigé** : les pages TikTok étaient classées « anti-robot » parce qu'elles contiennent le mot « captcha » dans leurs scripts. → anecdote possible
- **Le VPS n'est pas là où je croyais.** Le registre le déclare en Allemagne (whois DE), Cloudflare le sert depuis Francfort, mais les bases de géolocalisation le placent à **Lauterbourg, en Alsace**, à quelques kilomètres de la frontière. Les plateformes pourraient donc le voir comme français. Conséquence : pour comparer la France et l'étranger (T1), passage par des **proxies résidentiels** en France et aux États-Unis. → séquence 5 (anecdote déjà dans le script)
- **Décision : mode minimal jusqu'à lundi.** On garde ce qui tourne tout seul : le moniteur réseau sur la tour et sur le VPS, et le suivi des contenus avec T1 via les proxies. Sont **non réalisés**, par manque de temps et d'énergie : la recherche comparée (T5), la visibilité des comptes X (T6 et T7), et la collecte des posts de l'acte IV lui-même. → séquence 10 (limites)

---

## Samedi 7 novembre 2026 (acte IV)

- **Nuit, vers 3 h : session T6/T7 n°1 (« avant »)**, lancée avec le collecteur automatique. La connexion dans le navigateur piloté échoue : X et TikTok repèrent l'automatisation au moment du login. Solution : reprendre la session du Firefox habituel. **X l'accepte** (20 à 40 posts par page). **TikTok la refuse** : le profil s'affiche, mais la liste des vidéos ne se charge pas (« Une erreur est survenue »). Ce n'est pas un blocage des comptes, c'est le navigateur automatisé qui est refusé. → T7 TikTok à faire à la main, ou non réalisé. → anecdote possible sur la difficulté de mesurer les plateformes de l'extérieur.
- **Résultats de la session n°1 (« avant »), avec T7 TikTok fait à la main avec Zeeschuimer :**
  - **T6 : rien détecté.** 34 comptes X vérifiés, tous présents dans la recherche `from:`, y compris ceux qui disent être censurés. 6 comptes n'ont pas pu être vérifiés.
  - **T7 : non testable pour l'instant**, sur X comme sur TikTok : 7 comptes comparables au lieu des 8 minimum. Beaucoup de comptes militants ne parlent que du mouvement, et la règle des 48 heures écarte les posts récents.
  - **Décision : on ne modifie pas les seuils après avoir vu le résultat** (principe de la VAR). À la place, une session lundi soir : les posts des 5 au 7 novembre auront plus de 48 heures, et on fera défiler davantage les profils (`--defilements 12`). → séquence 6 ou 9 : bon exemple de rigueur, « je n'ai pas changé les règles quand le résultat ne m'arrangeait pas ».

- **Tests OONI sur l'iPhone** (retrouvés le 10/11 dans les données publiques d'OONI, détail et liens dans `ooni/rapport_iphone.md`) : vendredi 5 h 24 – 5 h 32, 13 h 02, 18 h 58 – 19 h 00 ; samedi 1 h 48, **13 h 30 – 13 h 32 et 15 h 19**. Sur les deux réseaux mobiles (SFR pour RED, Bouygues pour Cdiscount), **aucun réseau social ni aucune messagerie en anomalie** ; `sputnikglobe.com` bloqué à chaque passage. Les tests de 10 h, 17 h 30 et 20 h n'ont pas eu lieu. Anecdote : je ne retrouvais plus mes résultats, ils étaient en fait publics, et c'est comme ça qu'on les a retrouvés. → séquences 5 et 8
- 🕒 Noter ici tout événement marquant : une annonce, une panne, un post viral sur la censure.

## Lundi 9 novembre : premiers résultats

- **Forme 1, box Bouygues (tour Windows), du vendredi 6 à 5 h 11 au samedi 7 à 11 h 52** : 369 tours de mesure toutes les 5 minutes, **sans trou**, toujours sur le réseau Bouygues (AS5410), sans aucun tour invalide. Le **témoin positif** est bloqué par le DNS de Bouygues dans **738 vérifications sur 738** : l'outil voyait parfaitement un blocage DNS. 1.1.1.1 n'a jamais été intercepté. Le certificat d'aucun réseau social n'a changé.
  - **Résultat : aucun motif de blocage.** Seulement 6 signaux isolés, chacun sur un seul tour : un délai de connexion vers un serveur précis d'un CDN (Instagram, Snapchat, Messenger, YouTube), et une fois une lenteur du DNS. Rien qui se répète, rien qui touche une plateforme plus qu'une autre.
  - **Limite** : la tour a été éteinte samedi à 11 h 52, donc **avant les manifestations de l'après-midi**. Pour samedi après-midi : le moniteur du VPS et les données OONI publiques.
  - → séquence 8 : « Vendredi et samedi matin, chez moi, sur Bouygues : rien. Le témoin bloqué l'a été 738 fois sur 738, donc mon outil voyait. »
- **`reviewed` recalculé sur tout le corpus (984 vidéos)** : la différence de vendredi **ne tient plus**. Au-dessus d'un million de vues, 21/61 vidéos du mouvement marquées (34 %) contre 43/141 témoins (30 %), p = 0,62. Entre 100 000 et 1 million : 15/104 (14 %) contre 2/68 (3 %), p = 0,017. En dessous de 100 000 : 1 % des deux côtés. Toutes tranches confondues (Cochran-Mantel-Haenszel) : 40 observées contre 34 attendues, **p = 0,13, pas significatif**. La photo de vendredi ne reposait que sur 43 témoins au-dessus d'un million. → séquence 9, la leçon « trop peu de témoins »
- **Forme 1, VPS (987 tours jusqu'au 9 novembre)** : aucune coupure. Une **fausse alerte** est intéressante à raconter : vendredi entre 18 h 30 et 20 h 10, Instagram « n'existe plus » pour 1.1.1.1 interrogé en clair, alors que le résolveur du VPS et le DNS chiffré répondent normalement et que la connexion marche. Le même signal touche `www.akamai.com`, un témoin, les 7 et 8 novembre. C'est donc un raté du résolveur, pas un blocage. → séquence 8, « un signal isolé n'est pas un motif »
- **Décision : on arrête de creuser la forme 1.** Le verdict est « aucune coupure observée », avec ses limites (pas de mobile en continu, pas de tour samedi après-midi).

### Forme 2 : retraits de contenus

- **Les contrôles positifs marchent** : le tweet de test est vu « supprimé par l'auteur » partout dès le passage suivant, et le tweet de RT est vu « retenu » depuis la France et visible depuis les États-Unis à chaque passage.
- **T1, X : un seul post « retenu en France ».** Vérification : c'est un tweet de **RT en français**, retenu « au Royaume-Uni et dans l'Union européenne en réponse à une demande légale ». Il s'agit des sanctions européennes contre les médias d'État russes, en vigueur depuis 2022, comme `sputnikglobe.com` dans la forme 1. Il est entré dans le corpus parce qu'il parlait de l'acte IV. Ce n'est pas une mesure contre le mouvement. Le rapport l'annote maintenant automatiquement (« retenu dans toute l'UE »). → séquence 8 ou 9 : « mon seul post censuré… c'était RT »
- **T1, TikTok** : rien, sur 982 vidéos et 3 258 comparaisons France / États-Unis.
- **T2, X** : 26 posts du mouvement disparus sur 1 137, contre 19 témoins sur 798, soit 2,3 % des deux côtés. Côté mouvement, il s'agit surtout de suppressions par l'auteur (17). Les disparitions sans action de l'auteur sont **8 sur 1 137 contre 12 sur 798 témoins** (p = 0,11), donc pas plus que chez les témoins. Les 8 retraits par la plateforme côté témoins sont des comptes suspendus (spam probable).
- **T2, TikTok** : 4 vidéos du mouvement disparues sur 703, toutes supprimées par leur auteur ; aucune côté témoins.

### Forme 3 : visibilité

- **T6 : une erreur de mesure, et je la raconte.** La session de samedi soir annonçait 12 comptes « absents de la recherche ». Avant d'y croire, on a comparé avec les deux autres sessions du même jour. **Tous les comptes qu'on avait pu y vérifier étaient présents** (2 n'avaient pas pu être vérifiés plus tôt), et deux témoins (un compte foot et un compte sans rapport avec le mouvement) étaient touchés autant que les comptes militants. Deux causes :
  1. certaines recherches revenaient vides par intermittence, au milieu de recherches réussies, ce qui ressemble à une limitation passagère de X ;
  2. avec plus de défilement, on comparait des posts vieux de plusieurs semaines, que la recherche « Récent » de X ne retrouve plus pour personne (vérifié : la couverture est presque complète sur 3 jours, puis chute pour tous les comptes).
  - Correction : on compare sur 72 h, et un compte n'est « absent » que s'il l'est dans au moins 2 sessions. **Résultat : 36 comptes vérifiés sur 3 sessions, aucun absent de façon répétée, 9 absences isolées** (mouvement 3, revendication 4, témoins 2), dont 2 à confirmer lundi soir parce qu'elles n'ont été vérifiées qu'une fois.
  - **Honnêteté** : cette règle a été écrite après avoir vu le résultat. On le dit, on montre les deux versions, et la session de lundi soir servira de vérification indépendante. → séquence 9 : « mon outil a cru voir un shadowban, voilà pourquoi ce n'en était pas un »
- **Mardi 10 novembre : session T6/T7 n°4 (lundi soir) et T7 TikTok** (30 créateurs du mouvement et 10 témoins, à la main avec Zeeschuimer). 10 recherches X reviennent vides, dont deux comptes de foot (témoins).
  - **T6, toutes sessions (4)** : l'outil dit **DÉTECTÉ, 3 comptes absents dans au moins 2 sessions** : 2 comptes qui se disent censurés sur 14, **1 témoin** sur 10, 0 compte du mouvement sur 13. Même taux chez les témoins (Fisher p = 1). Les recherches vides sont fréquentes (6 samedi soir, 10 lundi, sur une quarantaine de comptes), et un compte de foot apparaît dans les deux listes. **On ne change pas la règle une seconde fois** : le verdict reste tel quel, avec la comparaison aux témoins ajoutée (même principe que T2). Lecture : pas plus que chez les témoins ; et un éventuel filtre serait celui de X, sans indice d'une demande de l'État. → séquence 9
  - **Grille session par session** (calculée sur le Mac, sans pseudo, `grille_t6.json`) : 15 comptes ont été absents au moins une fois, et **toutes ces absences tombent dans les deux sessions longues** (samedi 21 h et lundi 18 h, défilement poussé), **aucune** dans les deux premières (samedi 4 h et 16 h). L'effet vient de la session (limitation de X quand on enchaîne beaucoup de pages), pas des comptes. → séquence 9, graphique `S09_G09b`
  - **T7, X** : comptes du mouvement ×2,50 (12 comptes, 2 sous 1, p = 0,039, donc significatif **dans le sens « plus vus »**) ; comptes qui se disent censurés ×1,18 (13 comptes, 6 sous 1, p = 1). **Rien détecté.**
  - **T7, TikTok** : enfin testable, avec 25 comptes comparables : ×1,35, 8 sous 1, p = 0,11. **Rien détecté.**
- **T7, X** : avec la session du soir, 11 comptes du mouvement deviennent comparables. Leurs posts sur le mouvement sont en fait **plus** vus que leurs autres posts (rapport médian 1,76, p = 0,55 ; pour les comptes qui se disent censurés, 2,46). **Rien détecté.** T7 TikTok : toujours 7 comptes, non testable avant la session de lundi soir.
- **T8, TikTok** : les indicateurs internes changent pour 5 vidéos du mouvement sur 699 et 2 témoins sur 284. Pas d'écart (p = 1).
- **T3/T4, base DSA de la Commission** (`dsa.py`, exports publics du 1er octobre au 8 novembre, 4 plateformes, environ 150 jours lus) :
  - **Découverte** : chez TikTok, l'identifiant déclaré est celui de la vidéo. On a donc cherché nos 987 vidéos suivies parmi des dizaines de millions de décisions déclarées. **Aucune** n'a de retrait ni de déclassement déclaré.
  - **Fausse piste à raconter** : le nombre de décisions déclarées par TikTok est multiplié par 7 d'un coup le 29 octobre. Ce n'est pas la France : la hausse touche toutes les décisions, dans toute l'Europe. TikTok a changé sa façon de déclarer.
  - **Instagram** : pic de déclassements dans la catégorie « discours civique » entre le 20 et le 27 octobre (500 à 740 par jour, contre ~100 avant et après). Ces décisions sont prises par Instagram lui-même, sans signalement, et valent pour toute l'UE. La langue des contenus n'est pas déclarée. Le calendrier coïncide avec le mouvement, mais **rien ne permet de le relier à la France**. On le montre comme une question ouverte.
  - **X et YouTube** : pas de hausse. Chez X, les décisions concernant la France baissent même (×0,7). L'identifiant de X est opaque, donc pas de correspondance possible avec nos posts.
  - Limite : la base contient ce que les plateformes déclarent elles-mêmes, et ne dit jamais qui a demandé une décision.
- **T9, TikTok** : à popularité et âge égaux, les vidéos du mouvement **ne stagnent pas plus** que les témoins (188 observées contre 192 attendues, p = 0,38). Dans les deux tranches où l'écart est net, ce sont les témoins qui stagnent le plus.

## Dimanche 8 novembre et après

- 🕒 Résultats du moniteur réseau (`analyse.py`) et des données OONI publiques du week-end.
- 🕒 Résultats de T1, T2, T8 et T9, puis de T3 et T4 (base DSA).

---

## Images à garder pour la vidéo

- [ ] Le terminal du premier tour du moniteur : `sputnikglobe.com` en NXDOMAIN (adresse IPv6 de la box floutée)
- [ ] Les captures OONI de l'iPhone : `sputnikglobe.com` en anomalie, avec l'ASN visible
- [ ] Les erreurs de Minet (X 404, Instagram HTML, TikTok vide)
- [ ] Le post « #RadioLondres » et le post « stats anormalement basses » (pseudos floutés)
- [ ] Le tableau `reviewed` à popularité égale (dans ce journal)
- [ ] La sortie d'ipinfo « Lauterbourg » à côté du whois « DE » (adresse IP floutée)
- [ ] Le rapport du tableau de verdicts test × plateforme (à générer à la fin)
