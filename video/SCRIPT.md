# Script : « J'ai mesuré si le gouvernement coupe les réseaux sociaux »

> **Version 1.** Elle suit `FEUILLE_DE_ROUTE.md`, et chaque séquence porte le même numéro dans les deux fichiers.
> **Conventions.** 🎙️ texte dit · 🎥 image à l'écran · 📎 source à afficher (avec son statut) · 📝 note de réalisation.
> Les crochets `[À COMPLÉTER : …]` et `[RÉSULTAT : …]` signalent ce qui reste à remplir. **Ne tourne pas une phrase qui contient encore un crochet.**
> Le texte est écrit pour être dit : reformule à ta façon, mais garde les nuances (« selon », « documenté », « je ne peux pas savoir »).

---

## Séquence 0 : Accroche (0:00 – 1:00)

🎥 Écran noir, puis la lettre de Matignon en gros plan (capture de la publication de Blast, si elle existe).

🎙️
> Le 22 octobre, Matignon écrit aux quatre grands opérateurs français : Orange, SFR, Free et Bouygues.
> [À COMPLÉTER : citation exacte de la lettre, une phrase maximum]
> Selon le média Blast, qui a révélé le courrier, le gouvernement leur demande de se tenir prêts à suspendre TikTok, Instagram et Snapchat pendant quelques heures, surtout sur le mobile.

🎥 Coupe. Toi face caméra.

🎙️
> Depuis, une question tourne en boucle : est-ce que le gouvernement bride le mouvement social sur les réseaux ?
> Et franchement, en lisant ça, je me suis dit qu'on pouvait le vérifier. Pas le deviner, pas le ressentir : le **mesurer**.
> Alors pendant l'acte IV, j'ai installé des sondes chez moi, sur un serveur chez un hébergeur, hors de chez moi, et sur mon téléphone, et j'ai regardé.

🎥 Plan bref sur un terminal : la ligne `sputnikglobe.com … NXDOMAIN` surlignée. Ne pas l'expliquer.

🎙️
> Et dès la première minute, ma sonde m'a montré ça : un site bloqué, chez moi, en France. On va comprendre ensemble ce que c'est.
> À la fin de cette vidéo, vous aurez une réponse, et elle sera forcément l'une de ces trois-là.

🎥 Trois cartons : **PROUVÉ** · **NON PROUVÉ** · **NON TESTABLE**.

🎙️
> Et oui, « non testable », c'est une vraie réponse. On verra pourquoi.

📎 Blast, via [Clubic](https://www.clubic.com/actualite-635851-le-gouvernement-voulait-pouvoir-couper-les-reseaux-sociaux-pendant-la-manifestation-du-24-octobre-une-lettre-le-prouve.html) — *documenté (presse, non démenti)*

📝 Le plan sur `sputnikglobe.com` est l'objet mystère : il revient en séquence 5. Floute l'adresse IPv6 de ta box.

---

## Séquence 1 : Qui parle, d'où (1:00 – 1:45)

🎥 Face caméra, ton posé.

🎙️
> Deux mots sur moi pour que vous sachiez d'où je parle. Je suis développeur, avec un bagage en sécurité informatique. Je ne suis ni journaliste ni juriste, et je ne vais pas vous dire ce qu'il faut penser du mouvement social. Ce n'est pas le sujet.
> Ce que je mesure, c'est le réseau. Pas les intentions de qui que ce soit. Si un site ne répond pas, je peux vous dire où et quand ça coince. Je ne peux pas vous dire pourquoi ni qui l'a décidé, et je vous le dirai à chaque fois.
> Tout le code est en ligne, le lien est en description. Si je me trompe, vous pourrez le vérifier.

📝 Mécanique empruntée à Cyrus North : annoncer sa légitimité sans exagérer, et dire son point de vue.

---

## Séquence (S) : Sponsor, facultatif (1:45 – 2:45)

📝 À décider. **Pas de VPN** (voir la feuille de route, section 3). Si tu n'as pas de sponsor, supprime la séquence et décale les durées.

---

## Séquence 2 : Les trois formes de censure (2:45 – 4:15)

🎥 Schéma en trois colonnes qui apparaissent l'une après l'autre.

🎙️
> Avant d'aller plus loin, il faut définir le mot, parce que « censure », sur les réseaux, ça peut vouloir dire trois choses très différentes.
>
> **Un : couper l'accès.** Vous tapez tiktok.com et ça ne charge pas. C'est le réseau, votre opérateur, qui bloque. C'est ce que demandait la lettre.
>
> **Deux : supprimer des contenus.** TikTok marche, mais une vidéo précise disparaît parce qu'une autorité a demandé son retrait. En France, c'est le rôle de Pharos, la plateforme du ministère de l'Intérieur.
>
> **Trois : réduire la visibilité.** Tout marche, rien n'est supprimé, mais vos publications sont moins montrées. C'est ce qu'on appelle le shadowban.
>
> Ces trois choses ne se prouvent pas de la même façon. La première se mesure de l'extérieur, avec des outils. La deuxième se documente avec des textes de loi et des rapports. La troisième, de l'extérieur, ne se voit presque pas.
> Cette vidéo mesure la première. Pour les deux autres, je vous dirai ce qu'on sait et ce qu'on ne peut pas savoir.

🎥 Les colonnes 2 et 3 passent en grisé ; la colonne 1 reste en couleur.

📝 Mécanique empruntée à Seb : définir son terme avant d'analyser.

---

## Séquence 3 : Ce qu'on sait vraiment (4:15 – 8:00)

🎥 Une frise horizontale qui se construit date par date. Chaque événement porte une étiquette de statut : **DOCUMENTÉ**, **ANNONCÉ** ou **RUMEUR**.

🎙️
> Commençons par les faits, en séparant ce qui est sourcé de ce qui circule.

**17 octobre**
> Grande mobilisation contre la vie chère, partie d'appels sur les réseaux sociaux. 550 000 manifestants selon le ministère de l'Intérieur, 800 000 selon les organisateurs. Je vous donne les deux chiffres, parce que chacun choisit le sien.

📎 [ICI](https://www.ici.fr/infos/societe/direct-mobilisation-du-17-octobre-150000-personnes-attendues-dans-les-rues-ce-samedi-hors-agglomeration-parisienne-4822424) — *documenté*

**22 octobre**
> La lettre de Matignon aux opérateurs. Selon la presse, elle vise un filtrage DNS, surtout sur le mobile et dans certaines zones, pendant quelques heures. TikTok, Instagram et Snapchat sont cités. Pour X, les sources ne sont pas d'accord : certaines disent qu'il a été ajouté après l'envoi.
> Et la réponse des opérateurs, toujours selon la presse : impossible à mettre en place à court terme. Ils auraient aussi réclamé un acte officiel, signé et publié.

📎 [Clubic](https://www.clubic.com/actualite-635851-le-gouvernement-voulait-pouvoir-couper-les-reseaux-sociaux-pendant-la-manifestation-du-24-octobre-une-lettre-le-prouve.html), [actu17](https://actu17.fr/societe/reseaux-sociaux-de-la-coupure-preparee-a-la-menace-de-blocage-le-gouvernement-serre-la-vis.html) — *documenté (presse)*

**24 octobre**
> Nouvelle manifestation. Rien n'a été déclenché, en tout cas selon la presse. On le vérifiera nous-mêmes un peu plus tard.

📎 [Journal du Coin](https://journalducoin.com/technologies/coupure-reseaux-sociaux-france-matignon-bitchat-crypto) — *documenté (presse)*

**27 octobre**
> Le Sénat adopte un amendement du gouvernement, le n°94, dans le projet de loi dit « casseurs-payeurs ». Il permet de faire retirer, sans passer par un juge, des contenus qui appellent à la violence ou au pillage.
> Le ministre de l'Intérieur dit qu'il ne s'agit pas de fermer les réseaux sociaux, mais de retirer des contenus précis. La gauche sénatoriale parle de « dérive autoritaire ».
> [À COMPLÉTER : ce que dit le texte adopté sur le blocage d'un site qui ne retire pas un contenu, et sur le délai (1 heure ou 24 heures). À vérifier dans le texte officiel, pas seulement dans la presse.]
> Et précision importante : c'est une première lecture. Ce n'est pas encore la loi.

📎 [Public Sénat](https://www.publicsenat.fr/actualites/politique/derive-autoritaire-la-gauche-senatoriale-vent-debout-apres-ladoption-dun-amendement-sur-le-blocage-de-certains-contenus-sur-les-reseaux-sociaux), [Maire-info](https://www.maire-info.com/violences-urbaines/le-projet-de-loi-a-casseurs-payeurs-a-nettement-durci-adopta-en-premia-re-lecture-par-le-sa-nata-art26-31227) — *documenté (presse)*, texte officiel à consulter

**30 octobre**
> Matignon réunit un « groupe de contact permanent » avec les plateformes et les opérateurs. Selon L'Informé, c'est la première fois depuis 2022.

📎 [L'Informé](https://www.linforme.com/tech-telecom/article/reseaux-sociaux-le-groupe-de-contact-permanent-a-nouveau-reuni_13067.html) — *documenté (presse)*

**6 et 7 novembre**
> L'acte IV : grèves et blocages le vendredi, manifestations le samedi. C'est le week-end que j'ai mesuré.

📎 [Sortiraparis](https://www.sortiraparis.com/actualites/a-paris/articles/356694-gilets-jaunes-acte-iv-les-6-et-7-novembre-greve-et-manifestation-le-point-a-paris) — *annoncé*

🎥 Une bulle grise, à part de la frise, étiquetée **RUMEUR**.

🎙️
> Et puis il y a ce qui circule : le gouvernement « endiguerait » le mouvement sur les réseaux, surtout sur X. Je n'ai trouvé aucune preuve. Je n'ai pas trouvé de démenti non plus. Donc pour l'instant, c'est une rumeur. Ni vraie, ni fausse : non vérifiée.

🎥 Récapitulatif d'étape à l'écran.

🎙️
> Petit récapitulatif. Ce qui est **documenté** : le gouvernement a **préparé** une coupure, et il a fait voter un texte sur le retrait de contenus. Ce qui ne l'est pas : qu'une coupure ait **eu lieu**. C'est précisément ça qu'on va mesurer.

📝 Lis chaque date lentement et laisse la source à l'écran au moins 3 secondes. **Avant le tournage, relance une recherche d'actualité** : de nouveaux faits ont pu arriver.

---

## Séquence 4 : Comment on coupe un réseau social (8:00 – 10:30)

🎥 Animation : un annuaire téléphonique.

🎙️
> Pour comprendre ce qu'on mesure, il faut savoir comment un opérateur peut bloquer un site. Il y a principalement trois façons de faire.
>
> **La plus simple : l'annuaire.** Quand vous tapez tiktok.com, votre téléphone ne sait pas où c'est. Il demande à un annuaire, le DNS, qui lui répond avec une adresse, un peu comme un numéro de téléphone. Et par défaut, cet annuaire, c'est celui de votre opérateur.
> Pour bloquer un site, l'opérateur n'a qu'à faire mentir son annuaire : « ce site n'existe pas », ou une fausse adresse. C'est ce qu'on appelle un filtrage DNS, et c'est ce que la lettre aurait demandé.

🎥 L'annuaire répond « n'existe pas » en rouge.

🎙️
> **Deuxième façon : bloquer l'adresse elle-même.** L'annuaire dit la vérité, mais la route vers l'adresse est coupée.
> **Troisième façon, plus fine : lire le nom sur l'enveloppe.** Même quand la connexion est chiffrée, le nom du site demandé passe en clair au début. L'opérateur peut le repérer et couper la connexion.
> Et il y a la solution brutale : couper tout l'internet mobile d'une zone. Mais ça ne vise plus un réseau social, ça vise tout le monde.

🎥 Toi face caméra, petit sourire.

🎙️
> Un détail qui a son importance. Le filtrage DNS, c'est le plus facile à mettre en place, mais aussi le plus facile à contourner : il suffit d'utiliser un autre annuaire. D'ailleurs, petit aveu : en préparant cette vidéo, j'ai découvert que mon propre PC utilisait un annuaire chiffré, et pas celui de mon opérateur. Un filtrage DNS ne l'aurait même pas touché.
> Mais la plupart des gens gardent les réglages par défaut de leur box et de leur téléphone. Eux, ils seraient touchés.

📝 Ne donne pas de tutoriel de contournement : ce n'est pas le sujet, et ça peut être perçu comme militant. Le constat suffit.

---

## Séquence 5 : Mon dispositif, et le mystère résolu (10:30 – 13:00)

🎥 Schéma : la maison (box Bouygues), un serveur chez un hébergeur (adresse française, hors des fournisseurs d'accès grand public), un point hors de France, un iPhone avec deux SIM, et le logo OONI.

🎙️
> Voilà mon dispositif. Chez moi, sur ma box, une sonde que j'ai écrite tourne en continu. Toutes les cinq minutes, elle visite X, TikTok, Instagram, Snapchat et une quinzaine d'autres réseaux, et elle note **où** ça coince : à l'annuaire, à la connexion, au chiffrement, ou à la page elle-même.
> La même sonde tourne sur un serveur loué chez un hébergeur. Son adresse est française, mais il ne passe par aucun fournisseur d'accès grand public. Si un site tombe aussi depuis ce serveur, ce n'est pas un blocage de mon opérateur, c'est une panne de la plateforme.
> Et pour les contenus, mon outil vérifie aussi chaque post depuis une connexion résidentielle aux États-Unis, en plus de la France. On verra plus loin à quoi ça sert.
> Petite anecdote honnête : au début, je croyais ce serveur en Allemagne. En vérifiant, il était vu comme français par les plateformes. C'est exactement le genre de détail qu'il faut vérifier avant de conclure.
> Et sur mon téléphone, j'ai deux cartes SIM, RED et Cdiscount Mobile. [À COMPLÉTER : réseaux confirmés par l'ASN, a priori SFR et Bouygues.] Avec elles, j'ai lancé OONI Probe, une application libre utilisée par des chercheurs du monde entier pour documenter la censure. Ses mesures sont publiques.

🎥 Retour du plan mystère de la séquence 0 : `sputnikglobe.com → NXDOMAIN`.

🎙️
> Et maintenant, le site bloqué du début. sputnikglobe.com, c'est un média d'État russe. Depuis les sanctions européennes, les opérateurs français le bloquent. C'est un blocage parfaitement connu et assumé.
> Et c'est exactement pour ça que je l'ai mis dans ma sonde. C'est mon **témoin positif**. Si mon outil ne voit pas ce blocage-là, il ne verra pas non plus un blocage de TikTok. Et il le voit : chez Bouygues, l'annuaire répond « n'existe pas ».

🎥 Captures d'OONI Explorer : sputnikglobe en anomalie sur les deux SIM, ASN visible. [À COMPLÉTER : liens OONI]

🎙️
> Même chose sur mes deux lignes mobiles avec OONI. Alors que depuis mon serveur chez un hébergeur, qui n'utilise pas l'annuaire d'un fournisseur d'accès grand public, aucun blocage. Voilà à quoi ressemble un vrai blocage réseau en France aujourd'hui. Gardez cette image en tête.
> J'ai aussi des **témoins négatifs** : Wikipédia, Le Monde, des sites ordinaires. S'ils tombent en même temps que TikTok, ce n'est pas TikTok qui est visé, c'est ma connexion qui a un problème.

📝 Le témoin positif est le pivot de la vidéo, prends ton temps. Si un point de mesure ne voit pas sputnikglobe bloqué alors qu'il devrait, dis-le ici et explique ce que ça change.

---

## Séquence 6 : Le piège, et la VAR (13:00 – 14:45)

🎥 Face caméra, ton de confidence.

🎙️
> Avant de vous montrer les résultats, je vais vous raconter un petit truc.
> Vendredi 6 novembre, 18 h 30. La veille de l'acte IV. Mon serveur me signale qu'Instagram n'a plus d'adresse : l'annuaire répond qu'il n'a rien pour ce nom. Et ça dure une heure quarante. C'est exactement la signature d'un filtrage DNS, celle que demandait la lettre.
> Ça fait peur, non ? « La veille de la manif, Instagram bloqué. »
> Sauf que mon outil n'interroge pas un annuaire, mais quatre. Un seul ne donnait plus d'adresse : 1.1.1.1, interrogé en clair. Les trois autres donnaient la bonne adresse, et la connexion à Instagram a marché pendant tout ce temps. Et surtout, le même raté a touché un site témoin, `akamai.com`, qui n'a rien à voir avec les réseaux sociaux, le lendemain et le surlendemain.
> Ce n'était pas Instagram qui était visé. C'était un annuaire qui avait des ratés. C'est moi qui vous l'ai raconté avec les mots qui font peur.

🎥 Les quatre annuaires côte à côte : trois au vert, un au rouge, puis la même bande rouge sur `akamai.com`.

🎙️
> Autre exemple : depuis Paris, mon annuaire me donne pour Instagram une adresse différente de celle que donne un annuaire neutre. Suspect ? Non. Les gros sites ont des serveurs partout, et chacun est orienté vers le plus proche. Et depuis mon serveur chez un hébergeur, Reddit me répond « interdit », simplement parce que Reddit n'aime pas les robots dans les centres de données.
> Une anomalie, ce n'est pas un blocage. C'est pour ça qu'il faut des règles, et qu'il faut les annoncer **avant** de regarder les résultats.

🎥 La « VAR » : quatre critères qui s'affichent un par un.

🎙️
> Voilà mes quatre critères. Pour que je parle de blocage réseau, il faut :
> **Un.** Une signature typique : l'annuaire de l'opérateur ment alors qu'un annuaire neutre et chiffré dit la vérité, ou la connexion est brutalement coupée, ou le certificat de sécurité est faux.
> **Deux.** Que ça se répète, au moins trois mesures d'affilée, donc un quart d'heure.
> **Trois.** Que les témoins, eux, marchent pendant ce temps.
> **Quatre.** Que ça ne se voie pas depuis l'étranger ni depuis un serveur hors des fournisseurs d'accès grand public, et idéalement que d'autres mesures, OONI ou une autre ligne, montrent la même chose.
> Si les quatre sont réunis, je parlerai de « blocage observé ». Même là, je ne vous dirai pas qui l'a décidé.

📝 Mécaniques empruntées : le retournement sur le vocabulaire (Cyrus North) et la VAR avec critères annoncés (Seb). **Le retournement doit se faire en moins d'une minute et être explicite** : on ne laisse jamais le spectateur sur une fausse impression.

---

## Séquence 7 : Le passé, les 24 et 31 octobre (14:45 – 16:45)

🎥 Le site OONI Explorer, puis des extraits de `ooni/rapport_ooni.md`.

🎙️
> Mes sondes n'existaient pas le 24 octobre, le jour visé par la lettre. Mais des bénévoles font tourner OONI partout en France, tout le temps, et leurs données sont publiques. Alors je suis allé voir.
> Du 17 au 31 octobre, il y a des mesures en France tous les jours, entre 45 000 et 61 000 par jour.
> Le 24 et le 31 octobre, sur les connexions fixes, Instagram, Facebook, YouTube et Twitter ont été testés à quasiment toutes les heures de la journée, 15 ou 16 heures sur 16, chez Orange, SFR, Free et Bouygues. TikTok, X et Snapchat un peu moins souvent, mais tous opérateurs confondus, il ne s'est jamais écoulé plus d'une heure sans test.
> Résultat : aucun signal de blocage. Et sputnikglobe, lui, est bien vu bloqué chez les quatre. Donc les mesures savaient voir un blocage.

🎥 Deux « fausses pistes », présentées comme des petites enquêtes.

🎙️
> J'ai quand même trouvé des choses bizarres. Chez Free, Facebook ressort « bloqué » toutes les heures. Sauf qu'en regardant de près, c'est un seul téléphone Android qui voit ça, et il le voit déjà depuis le 10 octobre, avant même le mouvement. Les autres mesures chez Free sont normales. Ça ressemble surtout à un bloqueur installé sur ce téléphone.
> Mieux encore : le 27 octobre, OONI marque Instagram et Facebook comme « blocage confirmé » en France. Sauf que la page de blocage reconnue, c'est… une page de blocage **iranienne**, vue par une sonde installée chez un hébergeur. C'est une erreur de configuration, pas une censure française.

🎥 Changement de ton.

🎙️
> Par contre, il y a un trou énorme : le mobile. Sur ces deux journées, je trouve 0 ou 1 mesure faite en 4G par site et par opérateur. Or la lettre visait justement le mobile.
> Donc pour le 24 et le 31 octobre : sur les connexions fixes, **non prouvé**. Sur le mobile, **non testable**. Personne n'a mesuré.

🎥 Récapitulatif d'étape.

📝 Chiffres issus de `ooni/rapport_ooni.md`, généré le 6 novembre. Vérifie qu'ils n'ont pas changé si tu relances le script : OONI publie parfois des mesures en retard.

---

## Séquence 8 : L'acte IV en direct (16:45 – 19:30) ⏳

🎥 La frise (`rapport/frise.html`) en plein écran, avec un zoom progressif sur samedi après-midi.

🎙️
> Et maintenant, mes propres mesures, pendant l'acte IV.
> Ma box Bouygues a mesuré de vendredi 5 h à samedi midi : 369 tours de mesure, un toutes les cinq minutes, sans un seul trou. Mon serveur, lui, a tourné tout le week-end et continue encore : près de mille tours. Et sur mon téléphone, avec mes deux lignes, j'ai lancé OONI plusieurs fois samedi.
> Comment lire cette frise : chaque ligne est un réseau social, chaque couleur un état. Vert, ça marche. Rouge, signature de blocage. Gris, c'est ma connexion qui avait un problème. Blanc, pas de mesure.

**Variante retenue : signaux isolés (B)**
> Et c'est vert. Sur ma box, le témoin positif, `sputnikglobe.com`, a été vu bloqué 738 fois sur 738 : l'outil voyait parfaitement un blocage. Les réseaux sociaux, eux, n'ont jamais été bloqués.
> Il y a quand même quelques petites taches. Six, sur ma box : un serveur d'Instagram ou de YouTube qui met trop de temps à répondre, une seule fois, et plus rien au tour suivant. On les passe à la VAR : ça ne se répète pas, ça ne touche pas une plateforme plus qu'une autre. Ce n'est pas un motif.

🎥 Sur la frise du VPS : la bande rouge d'Instagram vendredi soir, et les petites taches sur `x.com` samedi après-midi.

> Sur mon serveur, vous reconnaissez la fausse alerte Instagram de vendredi soir. Le même annuaire a eu deux ou trois autres ratés pendant le week-end, dont un sur `x.com` samedi après-midi, en pleine manifestation, pendant un ou deux tours de mesure seulement. Même signature, même annuaire, et les trois autres répondaient normalement. On les passe à la VAR : ce ne sont pas des motifs.

🎙️
> Limite : ma box s'est arrêtée samedi midi, donc avant les cortèges de l'après-midi. Pour l'après-midi, j'ai mon serveur, qui est chez un hébergeur et pas chez un opérateur grand public, et les tests OONI de mon téléphone. Ni l'un ni l'autre n'a vu de blocage. [À CONFIRMER : résultats OONI de samedi sur l'iPhone, à regarder dans l'appli.]
> **Verdict pour l'acte IV : aucune coupure observée.**

🎥 Récapitulatif d'étape.

📝 Ne réécris pas les critères de la séquence 6 pour qu'ils collent aux résultats. Les captures OONI de samedi sont à ajouter ici si l'une d'elles montre autre chose que `sputnikglobe.com`.

---

## Séquence 9 : Le shadowban, et ce que je ne peux pas mesurer (19:30 – 23:30)

🎥 Retour du schéma en trois colonnes ; les colonnes 2 et 3 reprennent leur couleur.

**9a. Supprimer des contenus (forme 2), en bref**

🎙️
> Supprimer des contenus, d'abord. J'ai suivi environ 1 800 posts et vidéos sur le mouvement, et 1 100 posts sans rapport, sur X et TikTok. Mon outil passait toutes les trois heures, depuis la France et depuis les États-Unis.
> Est-ce que ça marche ? J'ai publié un tweet puis je l'ai supprimé : l'outil l'a vu « supprimé » au passage suivant. Et un tweet de RT, la chaîne russe interdite dans l'UE : l'outil le voit « retenu » depuis la France, visible depuis les États-Unis. Le détecteur détecte.
> Résultat. Sur X, 26 posts du mouvement ont disparu sur 1 137, soit 2,3 %. Côté témoins, 2,4 %. Pareil. Et la plupart du temps, c'est l'auteur qui a supprimé son post. Si on ne garde que les disparitions où l'auteur n'y est pour rien, c'est 8 côté mouvement, contre 12 côté témoins, qui sont surtout des comptes de spam suspendus. Sur TikTok, 4 vidéos disparues, supprimées par leurs auteurs.
> Et un post, un seul, retenu en France mais visible aux États-Unis. Je me suis dit : ça y est. Je vais voir… c'est un tweet de RT en français, qui parlait de l'acte IV. Retenu « au Royaume-Uni et dans l'Union européenne », comme tous les tweets de RT depuis les sanctions de 2022. Ce n'est pas le mouvement qui est visé, c'est RT.

🎥 Le tombstone « This Post from @RTenfrancais has been withheld in United Kingdom, European Union… » à côté de la même URL vue depuis les États-Unis.

> Et côté textes : l'amendement voté au Sénat organise le retrait sans juge. Voté en première lecture, pas encore en vigueur.
> Dernière vérification : depuis le règlement européen DSA, les plateformes doivent déclarer chacune de leurs décisions de modération dans une base publique. J'ai téléchargé cinq semaines de cette base. Et chez TikTok, j'ai eu une bonne surprise : l'identifiant déclaré, c'est celui de la vidéo. J'ai donc pu chercher mes 987 vidéos parmi des dizaines de millions de décisions. Résultat : aucune n'a été retirée ni déclassée.

**9b. Le shadowban (forme 3)**

🎥 Le tweet « les stats sont anormalement basses… je pense que la date est censurée », pseudo flouté.

🎙️
> Et puis il y a ce que beaucoup d'entre vous pensent : le shadowban. « Ma vidéo sur la manif a fait trois fois moins de vues, c'est la preuve. »
> Le problème, c'est qu'une vidéo peut faire moins de vues pour mille raisons. Et je me suis interdit de créer de faux comptes pour tester. Alors j'ai découpé la question en morceaux qu'on peut vraiment vérifier.

🎥 Liste des questions qui s'affiche : traitée à part ? / ça change pendant l'acte IV ? / moins diffusée ? / que déclarent les plateformes ? / cachée dans la recherche ?

🎙️ **Expérience 1 : le marquage `reviewed` de TikTok**
> Quand vous ouvrez TikTok, votre navigateur reçoit plus d'informations que ce qui s'affiche. Parmi elles, des indicateurs internes que TikTok ne documente pas. L'un d'eux s'appelle `reviewed`, « examiné ».

🎥 Capture des données reçues par le navigateur, avec le champ `reviewed` surligné. Puis le tableau.

> Premier chiffre : les vidéos marquées « examinées » ont en médiane 3 millions de vues, contre 20 000 pour les autres. Suspect ?
> Non, c'est le piège : plus une vidéo est vue, plus elle a de chances d'être examinée. Alors comparons à popularité égale, avec des vidéos de recettes et de foot aussi populaires.
> Et là, le vendredi soir, je croyais tenir quelque chose. Au-dessus d'un million de vues, 39 % des vidéos du mouvement étaient marquées, contre 19 % pour les autres. Le genre de chiffre qui fait une miniature.
> Sauf que je n'avais que 43 vidéos témoins dans cette tranche. Alors j'en ai ajouté, jusqu'à 141. Et l'écart a fondu : 34 % contre 30 %. Il reste une différence entre 100 000 et un million de vues, 14 % contre 3 %, mais c'est une tranche sur trois. Sur l'ensemble, à popularité égale, la différence n'est plus significative.
> Leçon : avec trop peu de témoins, on voit des écarts qui n'existent pas.
> Et même s'il en restait un, voilà ce qu'il ne prouverait pas. Un : personne ne sait ce que veut dire « examiné », TikTok ne le documente pas. Deux : la modération ordinaire suffirait à l'expliquer, parce que les vidéos de manifestation, avec parfois des images violentes, sont plus signalées que des recettes. Trois : rien n'indique qui a demandé quoi.

🎙️ **Expérience 2 : est-ce que ça change pendant l'acte IV ? (T8)**
> J'ai ensuite surveillé ces indicateurs sur près de 1 000 vidéos, toutes les trois heures, pendant et après l'acte IV. Si TikTok avait serré la vis pendant la manif, on verrait les indicateurs changer sur les vidéos du mouvement.
> Résultat : ils changent pour 5 vidéos du mouvement sur 699, et 2 témoins sur 284. Moins de 1 % des deux côtés. Pas de différence.

🎙️ **Expérience 3 : les courbes de vues (T9)**
🎥 Graphique : croissance des vues, mouvement contre témoins de même popularité et de même âge.
> Si une vidéo est mise de côté, elle reste en ligne mais cesse de gagner des vues. J'ai comparé les courbes à popularité et âge égaux.
> Résultat : selon les tranches, ce sont tantôt les vidéos du mouvement qui stagnent un peu plus, tantôt les recettes et le foot. Et les deux seuls écarts nets vont dans le sens inverse de la rumeur : ce sont les témoins qui stagnent le plus. Au total, 188 vidéos du mouvement ont stagné, alors qu'on en attendait 192 si elles étaient traitées comme les autres. Pas de différence.

🎙️ **Expérience 4 : les comptes cachés dans la recherche (T6), et mon erreur**
🎥 Le tableau de la session de samedi soir : « 12 comptes absents de la recherche » en rouge.
> Sur X, j'ai vérifié une quarantaine de comptes : ceux qui disent être censurés, des comptes du mouvement, et des témoins. Pour chacun, je regarde son profil, puis je cherche ses posts dans la recherche de X. Si les posts existent mais n'apparaissent pas dans la recherche, c'est le fameux « search ban ».
> Samedi soir, mon outil me sort ça : 12 comptes absents. Dont 7 de ceux qui disent être censurés. Ça y est, je le tiens ?
> Non. Je regarde les deux autres sessions du même jour, celle de la nuit et celle de l'après-midi : ces mêmes comptes étaient tous là. Et parmi les « absents », il y a un compte de foot. Deux erreurs de ma part : X renvoie parfois une recherche vide, au milieu de recherches qui marchent, et en faisant défiler plus loin, je comparais des posts vieux de plusieurs semaines, que la recherche de X ne retrouve plus pour personne.
> Alors j'ai corrigé la règle : on compare les trois derniers jours, et un compte n'est « absent » que s'il l'est dans deux sessions. Je vous le dis franchement : cette règle, je l'ai écrite après avoir vu le résultat. C'est pour ça que j'ai refait une session le lundi, pour vérifier avec la nouvelle règle.
> Et là, surprise : 3 comptes sont absents dans deux sessions. Deux comptes qui disent être censurés… et un de mes témoins, qui n'a rien à voir avec le mouvement.
> Deux sur quatorze d'un côté, un sur dix de l'autre : c'est le même taux. Sur X, les recherches qui reviennent vides sont si fréquentes qu'en quatre sessions, certains comptes tombent dessus deux fois, par hasard. Mon témoin en est la preuve.
> Et cette fois, je n'ai pas changé la règle : je vous montre le résultat tel quel, à côté du témoin. Verdict : pas plus d'absents chez ceux qui se disent censurés que chez mes témoins. Et si ces deux comptes sont vraiment filtrés, X le fait avec ses propres filtres automatiques, contre le spam par exemple. Rien n'indique une demande de l'État.

🎙️ **Expérience 5 : les vues des posts sur la manif (T7)**
> Dernière idée : comparer un compte à lui-même. Si vos posts sur la manif sont bridés, ils devraient faire moins de vues que vos autres posts. Sur X, pour 12 comptes du mouvement, leurs posts sur la manif font en médiane **2,5 fois plus** de vues que leurs autres posts. Pour ceux qui disent être censurés, 1,2 fois plus : autant que le reste. Et sur TikTok, sur 25 comptes : 1,35 fois plus.
> Parler de la manif ne fait pas perdre de vues. En moyenne, ça en fait plutôt gagner.

🎙️ **Ce que déclarent les plateformes (T4)**
> Retour dans la base européenne, pour les déclassements cette fois. Chez TikTok, le 29 octobre, le nombre de décisions est multiplié par sept d'un coup. Ça ressemble à une preuve… sauf que ça touche toute l'Europe, toutes les décisions : TikTok a simplement changé sa façon de déclarer.
> Et chez Instagram, il y a un vrai pic : du 20 au 27 octobre, trois fois plus de contenus déclassés dans la catégorie « discours civique ». Pile pendant le mouvement. Mais ces décisions valent pour toute l'Union européenne, Instagram ne dit pas dans quelle langue étaient les contenus, et c'est Instagram qui les a prises de lui-même, sans signalement. Je ne peux pas vous dire si ça concerne la France. C'est une question ouverte, et je la laisse ouverte.
> Limite : ce sont leurs propres déclarations, et la base ne dit jamais qui a demandé quoi.

🎙️ **Ce que je n'ai pas pu tester**
> Je n'ai pas testé si les recherches par hashtag renvoyaient moins de résultats en France qu'à l'étranger, faute de temps. Je n'ai pas mesuré la portée réelle avec des comptes tests, je me l'étais interdit. Instagram et YouTube, je ne les ai pas suivis. Et surtout, aucune de ces expériences ne dit **qui** décide.

🎙️ **Le verdict**
> Donc, le shadowban décidé par l'État, ça ne se prouve pas de l'extérieur : non testable. Une première mesure semblait montrer que TikTok examine plus souvent les vidéos du mouvement ; avec plus de témoins, l'écart a presque disparu. Les vidéos du mouvement ne perdent pas de vues, leurs indicateurs ne bougent pas pendant l'acte IV, les comptes qui se disent censurés ne disparaissent pas plus de la recherche que mes témoins, et les posts sur la manif font plus de vues, pas moins. Aucune de mes vidéos n'est déclarée déclassée dans la base européenne. Reste le pic d'Instagram, qu'on ne peut pas relier à la France. Pour aller plus loin, il faudrait les données internes des plateformes. Le règlement européen prévoit justement un accès pour les chercheurs.

🎥 Changement de ton. Images d'archives de la Nouvelle-Calédonie en 2024 (droits à vérifier).

🎙️
> Et si vous vous demandez pourquoi je me suis donné autant de mal pour mesurer un truc qui, peut-être, ne s'est pas produit : parce que ça s'est déjà produit. En mai 2024, en Nouvelle-Calédonie, pendant les émeutes, le gouvernement a coupé TikTok. Et le Conseil d'État a jugé cette coupure illégale [À COMPLÉTER : date exacte de la décision].
> Couper un réseau, ce n'est pas un scénario de science-fiction. C'est un outil qui existe, qui a déjà servi, et qui a été préparé le mois dernier. Alors savoir le voir, ça me semble utile, que vous soyez pour ou contre le mouvement.

📝 Le passage sur `reviewed` est le moment « VAR » de la forme 3 : le chiffre brut, puis le piège de la popularité, puis le faux écart dû au manque de témoins, puis les limites. Garde ce rythme. Les pseudos sont toujours floutés, et aucun compte de particulier n'est montré.

---

## Séquence 10 : Verdicts et fin (23:30 – 25:30) ⏳

🎥 Le tableau final, ligne par ligne.

🎙️
> Alors, le gouvernement bride-t-il le mouvement social sur les réseaux ? Ma réponse dépend de ce que vous entendez par là.

| si votre question est… | la réponse | pourquoi |
|---|---|---|
| Est-ce que l'accès a été coupé le 24 ou le 31 octobre ? | **Non prouvé** sur le fixe, **non testable** sur le mobile | données OONI publiques |
| Est-ce que l'accès a été coupé pendant l'acte IV ? | **Non prouvé** : aucune coupure observée (box Bouygues jusqu'à samedi midi, serveur, OONI sur deux lignes mobiles [à confirmer]) | mes sondes et OONI |
| Est-ce qu'une coupure a été envisagée ? | **Documenté** | lettre du 22 octobre, selon la presse |
| Est-ce que des contenus peuvent être retirés sans juge ? | **Documenté dans un texte voté au Sénat**, pas encore en vigueur | amendement n°94 |
| Est-ce que des posts du mouvement ont été retirés ? | **Non prouvé** : pas plus de disparitions que chez les témoins ; le seul post retenu en France est un tweet de RT | séquence 9 |
| Est-ce qu'il y a un shadowban d'État ? | **Non testable** de l'extérieur. Ce qui se mesure (recherche, vues, indicateurs) ne montre pas de bridage | séquence 9 |

🎙️
> Et je vous dois les limites. Un week-end, trois points de mesure, deux opérateurs mobiles : c'est mince. Je ne vois pas ce qui se passe chez Orange ou Free en 4G, ni dans une autre ville, ni pendant les heures où mes sondes ne tournaient pas. Je ne peux pas mesurer un ralentissement volontaire, parce qu'une 4G saturée par une foule ressemble exactement à ça.

🎥 La page GitHub, puis l'application OONI Probe.

🎙️
> Mais vous pouvez m'aider à faire mieux. Le code est sur GitHub : n'importe qui peut le lancer chez soi. Et surtout, installez OONI Probe, c'est gratuit, et lancez un test pendant les prochaines mobilisations, en 4G. Plus il y a de mesures, moins il y a de place pour les rumeurs, dans un sens comme dans l'autre.

🎥 Retour une dernière fois sur l'image `sputnikglobe.com → NXDOMAIN`.

🎙️
> Et retenez cette image. C'est ça, un blocage réseau, en France, aujourd'hui. Le jour où TikTok ou Instagram ressembleront à ça dans les mesures, vous le saurez. Et vous n'aurez pas besoin de me croire sur parole : vous pourrez le voir vous-mêmes.

📝 La fin reprend l'objet mystère du début, comme le fait Seb. Mets en description le lien du dépôt, les liens OONI et la liste complète des sources.

---

## Annexe : description YouTube (brouillon)

```
Pendant l'acte IV, j'ai mesuré si l'accès aux réseaux sociaux était bloqué en France :
sondes réseau (box Bouygues, serveur chez un hébergeur), OONI Probe sur deux réseaux mobiles,
et les données publiques OONI des 24 et 31 octobre.

Code et données : [lien GitHub]
OONI Probe : https://ooni.org/install/

Sources :
- Lettre de Matignon (Blast, via Clubic) : …
- Amendement n°94, Sénat : …
- [compléter avec toutes les sources de la séquence 3]

Chapitres :
00:00 Accroche
01:00 Qui je suis
02:45 Les trois formes de censure
04:15 Ce qu'on sait vraiment
08:00 Comment on coupe un réseau social
10:30 Mon dispositif
13:00 Le piège et la VAR
14:45 24 et 31 octobre : les données OONI
16:45 L'acte IV en direct
19:30 Ce que je ne peux pas mesurer
21:30 Verdicts
```
