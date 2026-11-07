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

- 🕒 Tests OONI sur l'iPhone, avec les deux SIM, vers 10 h, 13 h 30, 15 h 30, 17 h 30 et 20 h. Noter ici les heures réelles et les anomalies éventuelles (avec les liens OONI Explorer).
- 🕒 Noter ici tout événement marquant : une annonce, une panne, un post viral sur la censure.

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
