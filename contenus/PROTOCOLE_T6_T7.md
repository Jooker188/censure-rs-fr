# T6 et T7 : session « comptes » (X pour T6 et T7, TikTok pour T7)

> **Version automatique (recommandée)** : `caffeinate -i python3 collecteur.py --plan t6`, puis `python3 comptes.py exports/collecteur-t6-DATE.ndjson`. Le collecteur visite les 40 comptes X (profil + recherche `from:`) et les 25 créateurs TikTok (profil seulement), soit environ 1 h. La version manuelle ci-dessous reste valable.

**Question.** Les comptes qui parlent du mouvement, et surtout ceux qui disent être censurés, sont-ils :
- **T6** : absents de la recherche, alors que leurs posts existent sur leur profil (« search ban ») ?
- **T7** : moins vus quand ils parlent du mouvement que quand ils parlent d'autre chose ?

**Ce que ça ne dira pas.** Qui a réduit la visibilité. Voir la section « Lecture » de `rapport/comptes.md`.

## Avant la première session

1. **Collecte les témoins** si ce n'est pas fait (XT1 et XT2 dans `RECHERCHES.md`). Exporte-les, puis relance l'import avec **tous** les exports :
   ```
   python3 importer.py exports/*.ndjson
   ```
   Le fichier `contenus/comptes_t6.csv` contient alors trois groupes : `revendication`, `mouvement` et `temoin`.
2. **Règle la recherche de X**, sinon c'est ton réglage qui filtre les résultats et pas X : Paramètres → Confidentialité et sécurité → Contenu que vous voyez → **Paramètres de recherche** → décoche **« Masquer le contenu sensible »** et **« Retirer les comptes bloqués et masqués »**.

## La session (environ 1 minute par compte)

1. Dans Zeeschuimer : active **X/Twitter** et clique sur **« Delete all items »**.
2. Ouvre `contenus/comptes_t6.csv` dans un tableur. Pour **chaque ligne**, en alternant les groupes :
   1. ouvre l'adresse de la colonne **`profil`** et fais défiler pendant environ 20 secondes, soit une vingtaine de posts ;
   2. ouvre l'adresse de la colonne **`recherche`** (`from:compte`, onglet Récent) et fais défiler pendant environ 20 secondes ;
   3. mets `oui` dans la colonne **`fait`**.
3. Exporte en **.ndjson (original)** sous le nom `session_comptes_AAAA-MM-JJ_HHh.ndjson`, puis **désactive la capture**.
4. Lance l'analyse :
   ```
   python3 comptes.py session_comptes_*.ndjson
   ```

## Quand la faire

- **Samedi, pendant l'acte IV** (par exemple entre 15 h et 17 h), puisqu'une réduction de visibilité peut être temporaire.
- **Si possible une deuxième fois** dimanche soir ou lundi, pour voir si quelque chose a changé.

## Règles

- `contenus/comptes_t6.csv` contient des pseudonymes en clair : **il reste sur ta machine**, il n'est jamais publié ni montré à l'écran.
- Le rapport `rapport/comptes.md` ne contient que des codes (`u_…`) et des chiffres agrégés.
- Pour montrer un compte précis dans la vidéo, il faut **l'accord de la personne**.
- Petits volumes uniquement : environ 30 comptes par session, pas plus d'une ou deux sessions par jour. Tu utilises ton vrai compte, et X peut le suspendre en cas d'usage intensif.

## Comment `comptes.py` décide

- **T6** : on compare les posts originaux du profil (hors réponses et reposts) aux posts trouvés par `from:compte`, sur la même période.
  - **absent** : aucun post dans la recherche alors que le profil en a ;
  - **partiellement absent** : au moins la moitié des posts du profil manquent dans la recherche (à partir de 3 posts) ;
  - **présent** : sinon.
- **T7** : pour chaque compte, on calcule la médiane des vues de ses posts sur le mouvement divisée par la médiane des vues de ses autres posts. Seuls comptent les posts de plus de 48 h et de moins de 30 jours, avec au moins 2 posts de chaque sorte. On fait ensuite un test du signe sur tous les comptes. Le résultat est **DÉTECTÉ** seulement avec au moins 8 comptes comparables, une p-valeur inférieure à 0,05 et une majorité de rapports inférieurs à 1.
