# Test 5 : recherches comparées France / étranger (à faire à la main)

**Question.** Une recherche sur le mouvement renvoie-t-elle « aucun résultat », ou un message de restriction, **en France seulement**, alors qu'elle fonctionne depuis l'étranger au même moment ?

**Pourquoi à la main.** Aspirer automatiquement les pages de recherche est interdit par les conditions d'utilisation des plateformes, et serait fragile. Quelques recherches manuelles avec captures sont plus solides pour la vidéo.

## Préparation (une fois)

1. **Vue depuis la France** : Firefox en fenêtre privée, **sans être connecté**, sur ta box.
2. **Vue depuis l'étranger, de préférence hors UE** :
   - **Le plus simple** : un **VPN** dans un deuxième navigateur (ou une extension VPN de navigateur), avec une sortie au Royaume-Uni, en Suisse ou aux États-Unis.
   - **Ou** un second serveur hors de France, via un tunnel SOCKS : dans un terminal, lance `ssh -N -D 1080 utilisateur@IP_DU_SERVEUR` et laisse-le ouvert. Puis, dans un **deuxième profil Firefox** (`about:profiles`) : Paramètres → Réseau → Paramètres de connexion → « Configuration manuelle » → **Hôte SOCKS** `127.0.0.1`, port `1080`, SOCKS v5, et coche **« Utiliser un DNS distant lorsque SOCKS v5 est actif »**.
   - ⚠️ **Le VPS actuel ne convient pas** : son adresse est vue comme française.
   - **Vérifie** que https://1.1.1.1/cdn-cgi/trace affiche un `loc=` différent de `FR` (par exemple `GB`, `CH` ou `US`). Note le pays dans la colonne `pays` de `recherches.csv`.
3. **Choisis tes requêtes une fois pour toutes, et garde les mêmes à chaque série** :
   - 3 hashtags ou mots-clés du mouvement (par exemple le nom de l'acte, le hashtag principal, le mot d'ordre) ;
   - 2 requêtes témoins sans lien avec la politique (par exemple un match de foot du week-end, une recette).

## À chaque série (samedi vers 13 h, 16 h et 19 h)

Pour chaque plateforme où la recherche marche **sans compte** (TikTok, YouTube), et pour chaque requête :
1. Lance la même recherche dans les deux navigateurs, à moins de 5 minutes d'écart.
2. Fais une capture d'écran de chaque résultat, nommée `date_heure_pays_plateforme_requete.png`.
3. Ajoute une ligne par pays dans `recherches.csv` (voir `recherches_modele.csv`). La colonne `resultat` prend une seule de ces valeurs :
   - `resultats` : la page affiche des résultats ;
   - `aucun_resultat` : la page dit qu'il n'y a aucun résultat ;
   - `message_restriction` : la page affiche un message (contenu restreint, recherche indisponible, règles…).

**X et Instagram** exigent une connexion pour chercher : ils sont **non testables** sans compte. Facultatif : tu peux utiliser **ton vrai compte**, jamais un faux, dans les deux navigateurs, et le noter dans la colonne `categorie` (`mouvement_compte` ou `temoin_compte`).

## Lecture

- Seuls `aucun_resultat` et `message_restriction` **en France uniquement** comptent.
- Des résultats simplement **différents** entre les deux pays ne veulent rien dire, car les recherches sont localisées.
- `analyse_contenus.py --recherches recherches.csv` fait la comparaison automatiquement.
