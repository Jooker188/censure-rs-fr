# Script : « J'ai vérifié si le gouvernement censure les réseaux sociaux pendant les manifestations »

> **Version 2 (10 novembre).** Le fil rouge : on part de l'hypothèse de ceux qui se disent censurés, on la prend au sérieux, et on cherche la preuve chapitre après chapitre. Cinq fois, on croit la tenir. Cinq fois, elle s'effondre. Le spectateur reste pour la preuve ; à la fin, il repart avec mieux : ce qui s'est vraiment passé, ce que l'État fait déjà, et ce qu'il prépare.
> **Conventions.** 🎙️ texte dit (voix off par défaut) · 🎥 image à l'écran, avec le code du graphique (`video/graphiques/`) ou du plan (`video/PLANS.md`) · 📎 source à afficher, avec son statut · 📝 note de réalisation · **[FACE]** passage à dire face caméra si tu te filmes, en voix off sinon.
> **Règles de ton.** On ne se moque jamais de ceux qui se croient censurés : leur méfiance avait des raisons (la lettre de Matignon est réelle). On dit « je n'ai pas trouvé », jamais « ça n'existe pas ». Le texte est écrit pour être dit : phrases courtes, une idée par phrase.
> **Durée visée** : 23 à 25 minutes, soit environ 3 500 mots dits.
> La version 1 du script (plan en dix séquences) est dans l'historique Git.

---

## Accroche (0:00 – 1:20)

🎥 Montage rapide de posts qui dénoncent une censure, pseudos floutés ou remplacés par une barre noire (captures fournies, voir `PLANS.md`). Bruit de notifications.

🎙️
> « Mon compte est shadowban depuis la manif. »
> « Ils ont censuré la date. »
> « Nos vidéos disparaissent. »
> Pendant les manifestations contre la vie chère, ces messages, je les ai vus passer par centaines. Et franchement, je ne pouvais pas les balayer d'un revers de main.

🎥 Coupe nette. Le titre de l'article de Blast, puis `S03_G01b` (la lettre du 22 octobre).

🎙️
> Parce que le 22 octobre, le Premier ministre a écrit aux quatre grands opérateurs : Orange, SFR, Free et Bouygues. Selon le média Blast, qui a révélé le courrier, il leur demande de se tenir prêts à couper TikTok, Instagram et Snapchat, pendant quelques heures, surtout sur le mobile. Une mesure qui doit être « la plus ciblée possible », et qui n'a, écrit-il, qu'un « caractère exploratoire ».
> Donc la question n'est pas absurde. Le gouvernement s'y est préparé. Mais est-ce qu'il l'a fait ?

📎 [Blast](https://www.blast-info.fr/articles/2026/information-exclusive-blast-le-premier-ministre-a-prepare-la-coupure-des-reseaux-sociaux-pour-le-24-octobre-9D8cgrU5S5iiW14Sb9nMzQ), [Clubic](https://www.clubic.com/actualite-635851-le-gouvernement-voulait-pouvoir-couper-les-reseaux-sociaux-pendant-la-manifestation-du-24-octobre-une-lettre-le-prouve.html) — *documenté (presse, non démenti)*. Les deux citations viennent de la lettre, rapportées par Clubic d'après Blast ; le texte intégral n'est pas public.

🎥 Terminal : la ligne `sputnikglobe.com … NXDOMAIN` surlignée (`S00_E02`). Ne pas l'expliquer.

🎙️
> Alors j'ai passé le week-end de l'acte IV à chercher la preuve. Dans le réseau, dans les posts, dans les algorithmes, et jusque dans les registres de l'Union européenne.
> Et dès la première minute, ma sonde a trouvé ça : un site bloqué, en France.
> Cinq fois pendant cette enquête, j'ai cru tenir la preuve. Je vais vous les montrer, une par une.

🎥 Carton : **5 PREUVES ?** avec cinq cases vides.

📝 C'est la promesse de la vidéo : cinq « presque preuves ». Chaque chapitre en livre au moins une. La case se remplit d'une croix à chaque fois (graphique récurrent à fabriquer : `FP_1` à `FP_5`).

---

## Les règles du jeu (1:20 – 2:40)

🎙️ **[FACE]**
> Deux mots sur moi. Je suis développeur, avec un bagage en sécurité informatique. Je ne suis ni journaliste ni juriste, et je ne vais pas vous dire quoi penser du mouvement. Ce n'est pas le sujet.
> Ce que je sais faire, c'est mesurer. Et pour ne pas me raconter d'histoires, je me suis fixé des règles avant de regarder les résultats.

🎥 `S00_G01` : les trois cartons PROUVÉ · NON PROUVÉ · NON TESTABLE.

🎙️
> Un : à la fin, chaque question aura une de ces trois réponses. Et oui, « non testable », c'est une vraie réponse.

🎥 `S05_G02` : les témoins.

🎙️
> Deux : des témoins. Des sites qui doivent toujours marcher, comme Wikipédia. Et des sites qui doivent toujours être bloqués : `sputnikglobe.com`, par exemple, un média d'État russe interdit dans l'Union européenne. Si mon outil ne voit pas ce blocage-là, il ne verra pas non plus un blocage de TikTok.

🎥 `S06_G04a` → `S06_G04d` : la VAR, critère par critère.

🎙️
> Trois : pour que je parle de blocage, il faut une signature typique, que ça se répète, que les témoins marchent pendant ce temps, et que ça ne se voie pas ailleurs. Ces règles, je ne les change pas en cours de route. Et vous verrez que c'est plus dur à tenir qu'on ne croit.
> Tout le code est en ligne, le lien est en description. Si je me trompe, vous pourrez le vérifier.

---

## Ce qu'on sait déjà (2:40 – 5:30)

🎥 `S02_G01a` → `S02_G01c` : les trois formes de censure.

🎙️
> D'abord, le mot « censure » peut vouloir dire trois choses. Un : couper l'accès, TikTok ne charge plus. Deux : supprimer des contenus précis. Trois : réduire la visibilité, le fameux shadowban. Ce seront nos trois chapitres, du plus brutal au plus discret.

🎥 `S03_G01a` → `S03_G01f` : la frise qui se construit.

🎙️
> Ensuite, les faits.
> **17 octobre** : grande mobilisation contre la vie chère. 550 000 manifestants selon l'Intérieur, 800 000 selon les organisateurs.
> **22 octobre** : la lettre aux opérateurs. Selon la presse, les opérateurs répondent que c'est impossible à mettre en place à court terme, et réclament un acte officiel, signé et publié.
> **24 octobre** : nouvelle manifestation. Rien n'est déclenché, toujours selon la presse.
> **27 octobre** : le Sénat adopte un amendement du gouvernement, le n°94. Et je l'ai lu. L'administration, c'est-à-dire Pharos, pourra demander aux plateformes de retirer **en 24 heures** les contenus qui appellent à des violences, des vols ou des dégradations. Pas de juge : une « personnalité qualifiée » vérifie. Et le gouvernement l'écrit noir sur blanc : « En l'absence de retrait, l'autorité administrative pourra solliciter le blocage et le déréférencement des sites. » C'est une première lecture : ce n'est pas encore la loi.
> **30 octobre** : Matignon réunit un groupe de contact avec les plateformes et les opérateurs, une première depuis 2022 selon L'Informé.
> **6 et 7 novembre** : l'acte IV. C'est le week-end que j'ai mesuré.

📎 [ICI](https://www.ici.fr/infos/societe/direct-mobilisation-du-17-octobre-150000-personnes-attendues-dans-les-rues-ce-samedi-hors-agglomeration-parisienne-4822424) — *documenté* · [actu17](https://actu17.fr/societe/reseaux-sociaux-de-la-coupure-preparee-a-la-menace-de-blocage-le-gouvernement-serre-la-vis.html), [Journal du Coin](https://journalducoin.com/technologies/coupure-reseaux-sociaux-france-matignon-bitchat-crypto) — *documenté (presse)* · [Amendement n°94 rect. bis](https://www.senat.fr/amendements/2026-2027/87/Amdt_94.html) — *documenté (texte officiel)* · [Public Sénat](https://www.publicsenat.fr/actualites/politique/derive-autoritaire-la-gauche-senatoriale-vent-debout-apres-ladoption-dun-amendement-sur-le-blocage-de-certains-contenus-sur-les-reseaux-sociaux) — *documenté (presse)* · [L'Informé](https://www.linforme.com/tech-telecom/article/reseaux-sociaux-le-groupe-de-contact-permanent-a-nouveau-reuni_13067.html) — *documenté (presse)* · [Sortiraparis](https://www.sortiraparis.com/actualites/a-paris/articles/356694-gilets-jaunes-acte-iv-les-6-et-7-novembre-greve-et-manifestation-le-point-a-paris) — *annoncé*

🎥 `S03_G02` : la bulle RUMEUR.

🎙️
> Et puis il y a ce qui circule : le gouvernement « endiguerait » le mouvement sur les réseaux, surtout sur X. Pour l'instant, je n'ai trouvé ni preuve, ni démenti. C'est ce qu'on va chercher.

🎥 `S03_G03` : le récapitulatif.

🎙️
> Donc : préparer une coupure, c'est documenté. Faire voter un texte pour retirer des contenus sans juge, c'est documenté. Mais qu'une censure ait **eu lieu**, ça, personne ne l'a montré. Allons voir.

📝 Avant le tournage, relance une recherche d'actualité : la suite à l'Assemblée nationale a pu avancer.

---

## Chapitre 1 : Couper l'accès (5:30 – 11:30)

### Comment on coupe un réseau social

🎥 `S04_G01`, `S04_G02`, `S04_G03a`, `S04_G03b`, `S04_G03c`.

🎙️
> Pour bloquer TikTok, un opérateur a plusieurs options. La plus simple, c'est l'annuaire. Avant de se connecter, votre téléphone demande l'adresse de tiktok.com à un annuaire, le DNS, et par défaut c'est celui de votre opérateur. Pour bloquer, il suffit de le faire mentir : « ce site n'existe pas ». C'est exactement ce que la lettre aurait demandé.
> Il peut aussi couper la route vers l'adresse, ou repérer le nom du site au début de la connexion et la couper. Et il y a la solution brutale : couper tout l'internet mobile d'une zone.

### Mon dispositif, et le mystère résolu

🎥 `S05_G01`, puis plans de coupe : la box, la tour, l'iPhone (`S05_C01` à `S05_C03`).

🎙️
> Chez moi, sur ma box Bouygues, une sonde que j'ai écrite visite toutes les cinq minutes X, TikTok, Instagram, Snapchat et une quinzaine d'autres réseaux. Elle note où ça coince : à l'annuaire, à la connexion, au chiffrement ou à la page.
> La même sonde tourne sur un serveur loué chez un hébergeur, hors des fournisseurs d'accès grand public. Petite anecdote : je croyais ce serveur en Allemagne ; en vérifiant, les plateformes le voient comme français. Le genre de détail qu'il faut vérifier avant de conclure.
> Et sur mon téléphone, deux cartes SIM : RED, qui passe par le réseau de SFR, et Cdiscount Mobile, qui passe par celui de Bouygues. Avec elles, j'ai lancé OONI Probe, une application libre utilisée par des chercheurs du monde entier pour documenter la censure. Ses mesures sont publiques.

🎥 Retour de l'objet mystère `S00_E02`, puis `S08_G02` (738 / 738).

🎙️
> Et maintenant, le site bloqué du début. `sputnikglobe.com`, c'est un média d'État russe, interdit dans l'Union européenne depuis les sanctions. Les opérateurs français le bloquent, à l'annuaire. C'est mon témoin. Et de vendredi matin à samedi midi, ma box l'a vu bloqué 738 fois sur 738. Mon outil sait voir un blocage. Gardez cette image en tête : c'est à ça que ressemble une vraie censure réseau en France aujourd'hui.

### Avant l'acte IV : les 24 et 31 octobre

🎥 OONI Explorer (`S07_E01`), puis `S07_G01`.

🎙️
> Mes sondes n'existaient pas encore le 24 octobre, le jour visé par la lettre. Mais des bénévoles font tourner OONI partout en France, et leurs données sont publiques. Le 24 et le 31 octobre, sur les connexions fixes, Instagram, Facebook, YouTube et Twitter ont été testés presque à chaque heure, chez les quatre opérateurs. Aucun signal de blocage. Et `sputnikglobe.com` est bien vu bloqué chez les quatre.
> Il y a quand même eu deux fausses alertes : Facebook « bloqué » chez Free, qui vient en fait d'un seul téléphone qui voit ça depuis le 10 octobre, avant le mouvement. Et un « blocage confirmé » d'Instagram, reconnu grâce à… une page de blocage iranienne, vue par une sonde installée chez un hébergeur.

🎥 `S07_G02`.

🎙️
> Par contre, sur le mobile, presque personne n'a mesuré : zéro ou une mesure en 4G par site et par opérateur. Pour le 24 et le 31 octobre : sur le fixe, non prouvé. Sur le mobile, non testable.

### L'acte IV, et la fausse preuve n°1

🎥 `S06_G01a` en plein écran, son d'alerte.

🎙️
> Arrive l'acte IV. Vendredi 6 novembre, 18 h 30, la veille des manifestations. Mon serveur me signale qu'Instagram n'a plus d'adresse : l'annuaire répond qu'il n'a rien pour ce nom. Et ça dure une heure quarante. C'est exactement la signature d'un filtrage DNS, celle que demandait la lettre.
> La veille de la manif, Instagram bloqué. Je tiens ma preuve ?

🎥 `S06_G01b`, puis `S06_G01c`.

🎙️
> Sauf que mon outil n'interroge pas un annuaire, mais quatre. Un seul ne donnait plus d'adresse : 1.1.1.1, interrogé en clair. Les trois autres donnaient la bonne, et la connexion à Instagram a marché pendant tout ce temps. Et le même raté a touché `akamai.com`, un site témoin qui n'a rien à voir avec les réseaux sociaux, le lendemain et le surlendemain. Ce n'était pas Instagram qui était visé : c'était un annuaire qui avait des ratés.

🎥 Carton `FP_1` : **FAUSSE PREUVE N°1** — un annuaire en panne.

### Ce que j'ai vraiment mesuré

🎥 `S08_G01`, puis `S08_G03`, puis `S08_G04`.

🎙️
> Et pour le reste du week-end ? Ma box a mesuré de vendredi 5 h à samedi midi : 369 tours de mesure, sans un seul trou. Six petites taches, chacune sur un seul tour, et sur des plateformes différentes. On les passe à la VAR : rien ne se répète. Mon serveur, lui, a tourné tout le week-end, avec quelques autres ratés du même annuaire, dont un sur `x.com` samedi après-midi, pendant un ou deux tours seulement.
> Et le plus important : samedi à 13 h 30 puis à 15 h 20, en pleine manifestation, j'ai lancé OONI sur mes deux lignes mobiles. TikTok, Instagram, X, Snapchat, Facebook, WhatsApp, Telegram, Signal : tout répondait. Et `sputnikglobe.com`, lui, était bloqué à chaque fois. Ces mesures sont publiques, les liens sont en description.

🎥 `S08_G05`.

🎙️
> Verdict du chapitre 1 : là où j'ai mesuré, pas de coupure. Et ce n'est pas un « je n'ai rien vu » au hasard : mon outil voyait les blocages, il l'a prouvé 738 fois.
> Limite : ma box s'est arrêtée samedi midi, et je n'ai pas de mesure mobile après 15 h 20. Je ne vois pas Orange ni Free en 4G, ni les autres villes.
> Bon. Ils n'ont pas coupé les réseaux. Mais pour faire taire un mouvement, pas besoin de tout couper : il suffit de faire disparaître les bons posts.

📎 Mesures : `rapport_reseau/` (box et serveur), `ooni/rapport_ooni.md` (24 et 31 octobre), `ooni/rapport_iphone.md` (tests de l'iPhone, liens OONI Explorer) — *mesuré*

---

## Chapitre 2 : Faire disparaître des posts (11:30 – 15:00)

🎥 Défilement de posts du mouvement, floutés (plan de coupe écran).

🎙️
> J'ai récupéré environ 1 800 posts et vidéos sur le mouvement, sur X et TikTok, et 1 100 posts sans rapport, de la météo, du foot, des recettes : mes témoins. Et pendant des jours, mon outil a vérifié toutes les trois heures si chacun était encore là, depuis la France, et depuis les États-Unis.

🎥 `S09_G02`.

🎙️
> D'abord, est-ce que ça marche ? J'ai publié un tweet, puis je l'ai supprimé : l'outil l'a vu « supprimé » au passage suivant. Et j'ai ajouté un tweet de RT, la chaîne russe interdite dans l'Union européenne : l'outil le voit « retenu » depuis la France, et visible depuis les États-Unis. Le détecteur détecte.

### La fausse preuve n°2

🎥 La ligne du rapport : « 1 post retenu en France, du mouvement, avec mention légale ». Zoom.

🎙️
> Et au bout de quelques jours, il me sort ça. Un post du mouvement. Retenu en France, visible aux États-Unis. Avec une mention légale. Exactement ce qu'on cherche : un contenu sur la manif, masqué en France sur demande des autorités.
> Je clique.

🎥 Le message de X : « This Post from @RTenfrancais has been withheld in United Kingdom, European Union in response to a legal demand », à côté de la même URL vue depuis les États-Unis (`S09_E01`).

🎙️
> C'est un tweet de RT en français. Il parlait de l'acte IV, donc il est entré dans mon corpus. Et il est retenu « au Royaume-Uni et dans l'Union européenne », comme tous les tweets de RT depuis les sanctions de 2022. Ce n'est pas le mouvement qui est visé. C'est RT.

🎥 Carton `FP_2` : **FAUSSE PREUVE N°2** — RT, sous sanctions européennes.

### Ce que disent les chiffres

🎥 `S09_G03`.

🎙️
> Alors, les disparitions. Sur X, 26 posts du mouvement ont disparu sur 1 137, soit 2,3 %. Côté témoins : 2,4 %. Pareil. Et la plupart du temps, c'est l'auteur qui a supprimé son post. Si on ne garde que les disparitions où l'auteur n'y est pour rien, c'est 8 côté mouvement, contre 12 côté témoins, surtout des comptes de spam suspendus. Sur TikTok, 4 vidéos disparues, toutes supprimées par leurs auteurs.

🎥 Le site de la base DSA (`S09_E02`), puis `S09_G04`.

🎙️
> Dernière vérification. Depuis le règlement européen sur les services numériques, le DSA, les plateformes doivent déclarer chacune de leurs décisions de modération dans une base publique. J'en ai téléchargé cinq semaines. Et chez TikTok, bonne surprise : l'identifiant déclaré, c'est celui de la vidéo. J'ai donc cherché mes 987 vidéos parmi des dizaines de millions de décisions. Aucune n'a été retirée.
> Verdict du chapitre 2 : non prouvé. Les posts du mouvement ne disparaissent pas plus que les autres.
> Mais il reste la forme la plus discrète. Celle dont tout le monde parle. Celle qui ne laisse pas de trace : le shadowban.

📎 Mesures : `rapport/contenus.md`, `rapport/dsa.md` — *mesuré* · [Base de transparence du DSA](https://transparency.dsa.ec.europa.eu/explore-data/download) — *déclarations des plateformes*

---

## Chapitre 3 : Le shadowban (15:00 – 21:30)

🎥 Le post « les stats sont anormalement basses… je pense que la date est censurée », pseudo flouté.

🎙️
> « Ma vidéo sur la manif a fait trois fois moins de vues que d'habitude. » C'est le témoignage que j'ai le plus lu. Et c'est le plus dur à vérifier : une vidéo peut faire moins de vues pour mille raisons. Et je me suis interdit de créer de faux comptes pour tester.
> Alors j'ai découpé la question en morceaux qu'on peut vraiment vérifier.

🎥 `S09_G05`.

### La fausse preuve n°3 : le marquage « examiné »

🎥 Les données reçues par le navigateur, champ `reviewed` surligné (`S09_E04`), puis `S09_G06a`.

🎙️
> Quand vous ouvrez TikTok, votre navigateur reçoit plus d'informations que ce qui s'affiche. Parmi elles, des indicateurs internes que TikTok ne documente pas. L'un s'appelle `reviewed` : « examiné ».
> Premier chiffre : les vidéos marquées ont en médiane 3 millions de vues, contre 20 000 pour les autres. Normal : plus une vidéo est vue, plus elle a de chances d'être examinée. Alors comparons à popularité égale, avec des recettes et du foot aussi populaires.

🎥 `S09_G06b`.

🎙️
> Et là, vendredi soir, je crois tenir quelque chose. Au-dessus d'un million de vues, 39 % des vidéos du mouvement sont marquées, contre 19 % des autres. Deux fois plus. Le genre de chiffre qui fait une miniature.

🎥 `S09_G06c`.

🎙️
> Sauf que je n'avais que 43 vidéos témoins dans cette tranche. J'en ai ajouté, jusqu'à 141. Et l'écart a fondu : 34 % contre 30 %. Sur l'ensemble, à popularité égale, la différence n'est plus significative.
> Avec trop peu de témoins, on voit des écarts qui n'existent pas. Et même s'il en était resté un, personne ne sait ce que veut dire « examiné », et rien n'indique qui l'aurait demandé.

🎥 Carton `FP_3` : **FAUSSE PREUVE N°3** — trop peu de témoins.

### Est-ce que ça change pendant l'acte IV ? Est-ce que les vues stagnent ?

🎥 `S09_G07`, puis `S09_G08`.

🎙️
> J'ai surveillé ces indicateurs sur près de 1 000 vidéos, toutes les trois heures, pendant et après l'acte IV. Ils changent pour 5 vidéos du mouvement sur 699, et 2 témoins sur 284. Moins de 1 % des deux côtés.
> Et si une vidéo est mise de côté, elle cesse de gagner des vues. J'ai donc comparé les courbes, à popularité et âge égaux. Selon les tranches, ce sont tantôt les vidéos du mouvement qui stagnent un peu plus, tantôt les recettes et le foot. Et les deux seuls écarts nets vont dans l'autre sens : ce sont les témoins qui stagnent le plus. Au total, 188 vidéos du mouvement ont stagné, pour 192 attendues. Pas de différence.

### La fausse preuve n°4 : les comptes cachés dans la recherche

🎥 `S09_G09a`.

🎙️
> Sur X, la rumeur la plus précise, c'est le « search ban » : vos posts existent, mais n'apparaissent plus quand on vous cherche. J'ai vérifié une quarantaine de comptes : ceux qui disent être censurés, des comptes du mouvement, et des témoins. Pour chacun, je compare son profil à la recherche « from: ».
> Samedi soir, mon outil me sort ça : 12 comptes absents de la recherche. Dont 7 parmi ceux qui disent être censurés. Cette fois, c'est la bonne ?
> Je regarde les deux autres sessions du même jour : ces comptes étaient tous là. Deux erreurs de ma part : X renvoie parfois une recherche vide, au milieu de recherches qui marchent, et en faisant défiler plus loin, je comparais des posts vieux de plusieurs semaines, que la recherche de X ne retrouve plus pour personne.
> Alors j'ai corrigé la règle : on compare les trois derniers jours, et un compte n'est « absent » que s'il l'est dans deux sessions. Et je vous le dis franchement : cette règle, je l'ai écrite après avoir vu le résultat. Alors j'ai refait une session le lundi, pour la mettre à l'épreuve.

🎥 `S09_G09c`.

🎙️
> Résultat : 3 comptes absents dans deux sessions. Deux qui disent être censurés… et un de mes témoins. Deux sur quatorze d'un côté, un sur dix de l'autre : le même taux.

🎥 `S09_G09b` : les deux premières colonnes toutes vertes, les deux dernières tachées de rouge.

🎙️
> Et regardez où tombent les absences : uniquement dans les deux sessions les plus longues, celles où je faisais défiler beaucoup plus loin. Jamais dans les deux premières. Ce n'est pas le compte qui pose problème : c'est la session. Cette fois, je n'ai pas rechangé la règle. Je vous montre le résultat tel quel, à côté du témoin.

🎥 Carton `FP_4` : **FAUSSE PREUVE N°4** — les sessions trop longues.

### Le retournement : les posts sur la manif font plus de vues

🎥 `S09_G10`.

🎙️
> Dernière idée, la plus simple : comparer un compte à lui-même. Si vos posts sur la manif sont bridés, ils devraient faire moins de vues que vos autres posts.
> Sur X, pour 12 comptes du mouvement, leurs posts sur la manif font en médiane **deux fois et demie plus** de vues que leurs autres posts. Pour ceux qui disent être censurés, 1,2 fois plus. Et sur TikTok, sur 25 comptes : 1,35 fois plus.
> Parler de la manif ne fait pas perdre de vues. En moyenne, ça en fait gagner.

### La fausse preuve n°5, et la seule question ouverte

🎥 `S09_G11a`.

🎙️
> Retour dans la base européenne, pour les déclassements cette fois. Chez TikTok, le 29 octobre, le nombre de décisions est multiplié par sept, d'un coup. En pleine mobilisation.
> Sauf que ça touche toute l'Europe, et toutes les décisions. TikTok a simplement changé sa façon de déclarer.

🎥 Carton `FP_5` : **FAUSSE PREUVE N°5** — TikTok déclare autrement, partout.

🎥 `S09_G11b`.

🎙️
> Mais il y a une chose que je ne sais pas expliquer, et je vous la montre quand même. Chez Instagram, du 20 au 27 octobre, trois fois plus de contenus déclassés dans la catégorie « discours civique ». Pile pendant le mouvement.
> Sauf que ces décisions valent pour toute l'Union européenne, qu'Instagram ne dit pas dans quelle langue étaient les contenus, et que c'est Instagram qui les a prises de lui-même, sans signalement. Je ne peux pas dire si ça concerne la France. C'est une question ouverte, et je la laisse ouverte.
> Verdict du chapitre 3 : un shadowban décidé par l'État, ça ne se prouve pas de l'extérieur. Non testable. Mais tout ce que j'ai pu mesurer, la recherche, les vues, les indicateurs, les déclarations, ne montre aucun bridage du mouvement.

📎 Mesures : `rapport/tiktok.md`, `rapport/comptes.md`, `rapport/dsa.md` — *mesuré* (champs TikTok *non documentés*)

---

## Le verdict (21:30 – 24:30)

🎙️ **[FACE]**
> Bon. Je sais ce que vous vous dites. Vingt minutes, cinq fausses preuves… tout ça pour ça ?
> Non. Parce que j'ai trouvé trois choses.

🎥 Récapitulatif rapide des cinq cartons `FP_1` à `FP_5`, une seconde chacun.

🎙️
> La première, c'est que la censure du mouvement, je l'ai cherchée partout, et que là où j'ai pu regarder, je ne l'ai pas trouvée. Pas de coupure. Pas de posts qui disparaissent plus que les autres. Pas de comptes cachés plus que mes témoins. Et des posts sur la manif qui font plus de vues, pas moins.

🎥 `S08_G02` (738 / 738), puis le tweet de RT retenu.

🎙️
> La deuxième, c'est que la censure par l'État existe déjà en France, et qu'elle se voit. `sputnikglobe.com`, bloqué 738 fois sur 738. RT, masqué dans toute l'Union européenne. C'est la seule censure que j'ai vue de mes yeux ce week-end. Elle est légale, assumée, décidée au niveau européen. Mais elle prouve une chose : quand l'État bloque, ça laisse des traces, et on peut les mesurer.

🎥 La lettre, l'amendement (`S03_E05`), le communiqué du Conseil d'État (`S09_E05`).

🎙️
> La troisième, c'est la plus importante. Ce n'est pas arrivé. Mais tout est prêt pour que ça arrive.
> Une lettre qui demande aux opérateurs d'être prêts à couper. Un texte, voté au Sénat, qui permet de faire retirer des contenus en 24 heures sans juge, puis de bloquer les sites qui refusent.
> Et un précédent. En mai 2024, en Nouvelle-Calédonie, pendant les émeutes, le gouvernement a coupé TikTok. Le 1er avril 2025, le Conseil d'État a jugé cette coupure illégale, parce qu'elle avait été décidée pour une durée indéterminée. Mais il a aussi écrit qu'une coupure peut être légale, à trois conditions : qu'elle soit indispensable, qu'il n'y ait pas de solution moins radicale, et que sa durée soit limitée dès le départ. Et c'est sur cette décision que Matignon s'est appuyé en octobre, selon le compte rendu révélé par Blast.

📎 [Conseil d'État, décisions n° 494511, 494583 et 495174 du 1er avril 2025, communiqué](https://conseil-etat.fr/content/download/227070/document/Communiqu%C3%A9%20de%20presse%20-%20TikTok%20en%20Nouvelle-Cal%C3%A9donie%20-%20web.pdf) — *documenté (décision de justice)* · compte rendu de la réunion du 23 octobre : Blast, via Clubic — *documenté (presse)*

🎥 `S10_G01` : le tableau final.

🎙️
> Alors, le gouvernement censure-t-il les réseaux sociaux pendant les manifestations ?
> Pendant l'acte IV, là où j'ai mesuré : non, et je peux le montrer. Pour le shadowban d'État : impossible à prouver de l'extérieur, mais rien de mesurable ne va dans ce sens. Et pour demain : les outils sont prêts, et le texte arrive à l'Assemblée.
> Et je vous dois les limites. Un week-end, deux opérateurs mobiles, quelques heures de tests en 4G : c'est mince. Je ne vois pas Orange ni Free en 4G, ni les autres villes. Et un ralentissement volontaire ressemblerait exactement à une 4G saturée par une foule.

🎙️ **[FACE]**
> Et si je retiens une chose de cette enquête, c'est celle-là : moi, avec des témoins et des règles fixées à l'avance, je me suis fait avoir cinq fois. Imaginez une capture d'écran sur X.

🎥 La page GitHub (`S10_E01`), puis l'application OONI Probe (`S10_T01`).

🎙️
> Alors aidez-moi à faire mieux. Le code est sur GitHub, n'importe qui peut le lancer chez soi. Et installez OONI Probe, c'est gratuit : lancez un test pendant les prochaines mobilisations, en 4G. Plus il y a de mesures, moins il y a de place pour les rumeurs, dans un sens comme dans l'autre.

🎥 Dernière image : `sputnikglobe.com → NXDOMAIN` (`S10_E02`).

🎙️
> Et retenez cette image. C'est ça, un blocage, en France, aujourd'hui. Le jour où TikTok ou Instagram ressembleront à ça, on le verra. Ensemble. Et vous n'aurez pas besoin de me croire sur parole.

📝 La fin reprend l'objet mystère du début. Le spectateur n'a pas eu « sa » preuve, mais il repart avec trois réponses nettes et une raison de rester vigilant : c'est la récompense promise par le titre.

---

## Annexe A : titre et miniature

- **Titre** : « J'ai vérifié si le gouvernement censure les réseaux sociaux pendant les manifestations ». Variante courte : « Le gouvernement censure-t-il les manifs sur les réseaux ? J'ai vérifié ».
- **À éviter** : tout titre qui affirme une censure (« La preuve que… », « Le gouvernement censure… »). La vidéo le démentirait.
- **Miniature** : piste B (la lettre de Matignon, « ILS L'ONT FAIT ? », une sonde en attente), avec la mascotte et un vrai post flouté. Brouillons dans `video/miniatures/`.

## Annexe B : description YouTube (brouillon)

```
Pendant l'acte IV, j'ai cherché la preuve que le gouvernement censure les réseaux sociaux :
coupures réseau (box Bouygues, serveur, OONI sur deux réseaux mobiles), posts supprimés
(1 800 posts suivis sur X et TikTok), shadowban (recherche, vues, indicateurs internes de TikTok)
et déclarations des plateformes dans la base européenne du DSA.

Code et données : [lien GitHub]
Mes tests OONI de l'acte IV : [liens de ooni/rapport_iphone.md]
OONI Probe : https://ooni.org/install/

Sources :
- Lettre du 22 octobre (Blast) : https://www.blast-info.fr/articles/2026/information-exclusive-blast-le-premier-ministre-a-prepare-la-coupure-des-reseaux-sociaux-pour-le-24-octobre-9D8cgrU5S5iiW14Sb9nMzQ
- Amendement n°94, Sénat : https://www.senat.fr/amendements/2026-2027/87/Amdt_94.html
- Conseil d'État, 1er avril 2025 (TikTok, Nouvelle-Calédonie) : [lien du communiqué]
- [compléter avec les sources de « Ce qu'on sait déjà »]

Chapitres :
00:00 Ils disent être censurés
01:20 Les règles du jeu
02:40 Ce qu'on sait déjà
05:30 Chapitre 1 : couper l'accès
11:30 Chapitre 2 : faire disparaître des posts
15:00 Chapitre 3 : le shadowban
21:30 Le verdict
```
