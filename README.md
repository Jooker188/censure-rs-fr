# censure-rs-fr

**Question :** les réseaux sociaux ont-ils été bloqués ou bridés **au niveau du réseau** en France pendant le mouvement social de l'automne 2026 ?

**Réponses possibles :** *prouvé*, *non prouvé* ou *non testable*.

Un résultat nul (« aucun blocage détecté ») est une vraie réponse. Il ne veut pas dire « aucune modération de contenu ».

Ce dépôt contient trois outils en Python, sans dépendance :

- **`moniteur_reseaux.py`** mesure l'accès aux sites ;
- **`analyse.py`** détecte les anomalies et dessine une frise ;
- **`ooni_verif.py`** interroge les mesures publiques d'[OONI](https://ooni.org).

---

## 1. Trois formes de « censure » à ne pas confondre

| forme | exemple | mesurable ici ? |
|---|---|---|
| **1. Blocage réseau** | filtrage DNS chez l'opérateur, blocage d'adresses IP, coupure mobile | **oui** : c'est le périmètre de ce projet |
| **2. Retrait de contenus** | demandes de Pharos, retrait administratif | non. C'est documenté par les textes, pas par des mesures |
| **3. Déclassement par la plateforme** | portée réduite, « shadowban » | non. Hors périmètre, trop fragile à tester sans faux comptes ni automatisation |

---

## 2. Contexte, vérifié le 6 novembre 2026

Légende des statuts : **documenté** (source de presse identifiée), **annoncé** (prévu, pas encore constaté), **rumeur** (rien de vérifiable).

| date | fait | statut |
|---|---|---|
| 17 oct. | Mobilisation nationale contre la vie chère, partie d'appels sur les réseaux sociaux. **550 000 manifestants selon le ministère de l'Intérieur, 800 000 selon les organisateurs.** | documenté ([ICI](https://www.ici.fr/infos/societe/direct-mobilisation-du-17-octobre-150000-personnes-attendues-dans-les-rues-ce-samedi-hors-agglomeration-parisienne-4822424)) |
| 22 oct. | Lettre de Matignon aux quatre opérateurs (Orange, SFR, Free, Bouygues) leur demandant de se tenir prêts à suspendre TikTok, Instagram et Snapchat pendant quelques heures. Cible principale : le mobile et certaines zones. X aurait été ajouté après l'envoi. Les opérateurs ont répondu que c'était impossible à court terme et ont réclamé un acte signé et publié. Révélée par Blast, non démentie. | documenté ([Clubic](https://www.clubic.com/actualite-635851-le-gouvernement-voulait-pouvoir-couper-les-reseaux-sociaux-pendant-la-manifestation-du-24-octobre-une-lettre-le-prouve.html), [Journal du Geek](https://www.journaldugeek.com/2026/10/26/apres-les-manifestations-le-gouvernement-se-prepare-a-la-coupure-de-tiktok-instagram-et-snapchat/), [actu17](https://actu17.fr/societe/reseaux-sociaux-de-la-coupure-preparee-a-la-menace-de-blocage-le-gouvernement-serre-la-vis.html)) |
| 24 oct. | Manifestation. La presse ne rapporte aucune coupure déclenchée. | documenté ([Journal du Coin](https://journalducoin.com/technologies/coupure-reseaux-sociaux-france-matignon-bitchat-crypto)) |
| 27 oct. au soir | Le Sénat adopte l'amendement gouvernemental n°94 au projet de loi « casseurs-payeurs », par 219 voix contre 115. Il prévoit le retrait administratif, sans juge et via Pharos, de contenus appelant aux violences ou aux pillages. Le délai, d'abord fixé à 1 heure, a été porté à 24 heures. **Selon la presse, faute de retrait, le blocage et le déréférencement des sites concernés seraient possibles.** Ce point relève donc aussi de la forme 1 et doit être vérifié dans le texte adopté. Le texte n'est adopté qu'en première lecture. | documenté par la presse ([Public Sénat](https://www.publicsenat.fr/actualites/politique/derive-autoritaire-la-gauche-senatoriale-vent-debout-apres-ladoption-dun-amendement-sur-le-blocage-de-certains-contenus-sur-les-reseaux-sociaux), [Maire-info](https://www.maire-info.com/violences-urbaines/le-projet-de-loi-a-casseurs-payeurs-a-nettement-durci-adopta-en-premia-re-lecture-par-le-sa-nata-art26-31227), [CNews](https://www.cnews.fr/france/2026-10-28/projet-de-loi-casseurs-payeurs-vers-un-blocage-des-contenus-appelant-aux-pillages)) ; texte officiel non consulté |
| 30 oct. | Réunion à Matignon du « groupe de contact permanent » (plateformes, opérateurs, administration), pour la première fois depuis 2022. | documenté ([L'Informé](https://www.linforme.com/tech-telecom/article/reseaux-sociaux-le-groupe-de-contact-permanent-a-nouveau-reuni_13067.html)) |
| 6 et 7 nov. | « Acte IV » : grèves et blocages le 6, manifestations le 7. À Paris, rendez-vous annoncé à 14 h place de la Concorde, sous réserve de l'accord de la préfecture. | annoncé ([Sortiraparis](https://www.sortiraparis.com/actualites/a-paris/articles/356694-gilets-jaunes-acte-iv-les-6-et-7-novembre-greve-et-manifestation-le-point-a-paris)) |
| — | Le gouvernement « endiguerait » le mouvement sur les réseaux, notamment sur X. | **rumeur** : ni confirmée ni démentie, aucune preuve trouvée |

Précédent juridique : en mai 2024, TikTok a été coupé en Nouvelle-Calédonie. Le Conseil d'État a jugé cette coupure illégale en 2025.

---

## 3. Méthode

### 3.1 Le moniteur (`moniteur_reseaux.py`)

Toutes les 5 minutes environ (avec un aléa de ±10 %), pour chaque domaine, il découpe la connexion en étapes. Le but est de savoir **où** elle échoue.

| étape | ce qui est mesuré | pourquoi |
|---|---|---|
| DNS système | `getaddrinfo`, c'est-à-dire ce que voient les applications de la machine | l'expérience réelle |
| DNS du FAI | requête UDP directe au résolveur de la box ou de l'opérateur, avec le code de réponse exact (NXDOMAIN, REFUSED…) | **c'est là qu'agirait un filtrage DNS d'opérateur** |
| 1.1.1.1 sur le port 53 | DNS public en clair | ce trafic peut être intercepté par le FAI ; une réponse différente du DoH signale une interception |
| **DoH** (1.1.1.1, 8.8.8.8) | DNS chiffré dans HTTPS, interrogé par adresse IP | **la référence** : un FAI ne peut pas le falsifier sans casser TLS |
| TCP et TLS | connexion sur le port 443 vers l'adresse IP du DNS système, avec SNI et certificat vérifié | distingue un blocage d'IP, un reset ou une interception |
| contre-essai | en cas d'échec, la même connexion vers une adresse IP obtenue en DoH | distingue un blocage d'IP d'un filtrage par SNI |
| HTTP | `GET /`, en lisant 16 Ko au plus (sites « web » seulement) | le site répond-il réellement ? |
| ligne `meta` | AS de sortie (via Cloudflare puis RIPEstat, **l'adresse IP n'est pas enregistrée**) et test d'interception de 1.1.1.1 | vérifie qu'on mesure bien le bon réseau |

**Cibles :** X, TikTok, Instagram, Snapchat, Facebook, YouTube, Discord, Telegram, Bluesky, WhatsApp, Signal, Messenger, Threads, Reddit, Twitch, BeReal et Mastodon. Pour chaque plateforme, on mesure le site web et, quand on les connaît, un ou deux domaines utilisés par l'application mobile. Ces domaines ne sont qu'une sélection : complète la liste avec `--extra plateforme:hôte` après avoir observé le journal DNS de ton téléphone.

**Témoins négatifs** (ils doivent répondre) : `www.wikipedia.org`, `www.lemonde.fr`, et quatre CDN génériques (`www.akamai.com`, `www.fastly.com`, `www.cloudflare.com`, `www.google.com`). Si la moitié d'entre eux échouent, le tour est déclaré **invalide** : la panne vient de la connexion de mesure, et le tour est exclu.

**Témoin positif** (il doit être bloqué) : `sputnikglobe.com` et `ria.ru`. Ce sont des médias d'État russes visés par les sanctions de l'UE, bloqués par DNS chez Orange, SFR, Free et Bouygues selon OONI en octobre 2026. Le moniteur se limite à des requêtes DNS, sans jamais s'y connecter. **Si l'outil ne détecte pas ce blocage-là depuis un point de mesure, il ne peut rien conclure sur le DNS depuis ce point.**

### 3.2 L'analyse (`analyse.py`)

Le script recalcule tout à partir des colonnes brutes.

- **Signaux de type « signature »**, c'est-à-dire la forme typique d'un blocage réseau sans en être une preuve :
  - le DNS du FAI ou le DNS système répond NXDOMAIN, NODATA, REFUSED ou une adresse privée (`127.0.0.1`, `0.0.0.0`…), alors que le DoH répond ;
  - 1.1.1.1 en clair ment alors que le DoH répond ;
  - la connexion est réinitialisée (reset) en TCP, TLS ou HTTP ;
  - le certificat est invalide (hors `chat.signal.org`, dont l'autorité de certification est privée) ;
  - la connexion échoue vers l'adresse IP du DNS système mais réussit vers celle du DoH.
- **Signaux de type « échec »** : timeouts et erreurs sans forme caractéristique.
- **Épisodes** : un même signal, sur le même hôte et le même point de mesure, pendant des tours consécutifs. Pour chaque épisode, l'analyse indique ce que voyaient les autres points de mesure au même moment.
- **« Motif répété compatible avec un blocage »** : une signature sur au moins 3 tours consécutifs (environ 15 minutes) pendant que les témoins répondent. C'est le **seul** classement qui mérite un examen manuel. L'outil ne conclut jamais « blocage ».
- **Autres sorties** : changements d'émetteur de certificat (une rotation chez un CDN se voit aussi depuis les autres points de mesure), codes HTTP pour information, trous de mesure et pannes de la connexion de mesure.
- **Frise** (`rapport/frise.html`) : disponibilité par plateforme et par point de mesure, en heure de Paris, avec les événements de `evenements.csv`. Le détail s'affiche au survol.

### 3.3 Règles d'interprétation

1. **Une différence de DNS n'est pas une preuve.** Les CDN de Meta, TikTok ou X renvoient des adresses différentes selon le résolveur (verdict `ips_differentes`). Ce qui compte : un certificat valide sur l'adresse obtenue veut dire que tout va bien.
2. **Seuls comptent les motifs répétés**, absents des témoins et cohérents entre plusieurs mesures (autre point de mesure, OONI).
3. **On ne désigne jamais de cause** à partir d'un échec réseau. Une panne de la plateforme, un incident chez le FAI et un blocage volontaire peuvent laisser des traces identiques. Le témoin positif montre à quoi ressemble un blocage connu ; il ne dit pas qui a décidé un éventuel nouveau blocage.
4. **Une 4G lente près d'une manifestation est attendue** : la foule sature les antennes. Le **bridage de débit est classé « non testable »** avec ce dispositif.
5. **Un week-end de mesures depuis 2 ou 3 points est un échantillon mince.**

---

## 4. Reproduire

Il faut **Python 3.9 ou plus récent**, sans autre dépendance. Désactive tout VPN, iCloud Private Relay ou DNS personnalisé, ou note-le.

### Windows (connexion fixe)

1. Installe Python depuis [python.org](https://www.python.org/downloads/) en cochant « Add python.exe to PATH ».
2. Télécharge le dépôt (bouton *Code*, puis *Download ZIP*) et dézippe-le.
3. Double-clique sur **`lancer_windows.bat`** : il fait un tour de test, puis lance la mesure continue.
4. Ne mets **pas** le PC en veille. Le script empêche lui-même la mise en veille automatique, et tu peux éteindre l'écran ou verrouiller la session.

### macOS ou Linux

Lance d'abord un tour de test, puis la mesure continue :

```bash
python3 moniteur_reseaux.py --vantage fixe --fai "Orange fibre" --once
```

```bash
python3 moniteur_reseaux.py --vantage fixe --fai "Orange fibre"
```

Sur macOS, le script empêche la mise en veille automatique avec `caffeinate`, mais **fermer le capot du portable arrête la mesure**.

### VPS (point de contrôle hors des FAI français)

```bash
tmux new -s sonde
```

```bash
python3 moniteur_reseaux.py --vantage vps --fai "Contabo VPS"
```

Ensuite Ctrl+B puis D pour se détacher, et `tmux attach -t sonde` pour revenir.

### 4G ou 5G (via le partage de connexion du téléphone)

1. **Sur le téléphone, désactive le DNS privé.** Sur Android : Paramètres → Réseau → DNS privé → Désactivé. Sinon, l'ordinateur mesure ton DNS chiffré et pas celui de l'opérateur.
2. Active le partage de connexion, coupe le Wi-Fi de l'ordinateur et branche-le sur le téléphone.
3. Lance `--vantage 4g --fai "Opérateur 4G" --once`, puis vérifie dans la ligne `META` que l'AS est bien celui de l'opérateur mobile.
4. Pour économiser les données, passe à `--interval 600` (environ 300 Ko par tour).

### Vérifier le tour de test

- **Ligne `résolveur FAI=`** : l'adresse de la box ou de l'opérateur, pas `1.1.1.1` ni `8.8.8.8`. Sinon, ajoute `--resolver <IP>`.
- **`sputnikglobe.com` et `ria.ru`** : `fai:nxdomain` ou `fai:bogon` (blocage détecté).
- **Les autres lignes** : `coherent` ou `ips_differentes`, avec l'étape KO à `aucun`.

### En complément : OONI Probe sur le téléphone

Installe [OONI Probe](https://ooni.org/install/), ouvre *Websites* puis *Choose websites* et ajoute les URL cibles, puis lance les tests **en 4G** pendant les heures qui t'intéressent. Ces mesures deviennent publiques et vérifiables par d'autres.

### Analyser

```bash
python3 analyse.py "mesures_*.csv" --evenements evenements.csv
```

Le script produit `rapport/analyse.md`, `rapport/episodes.csv` et `rapport/frise.html`. Les options `--debut` et `--fin` (heure de Paris) cadrent la frise.

### Vérifier OONI

Pour le rapport sur la période du 17 au 31 octobre :

```bash
python3 ooni_verif.py --since 2026-10-17 --until 2026-10-31 --focus 2026-10-24,2026-10-31 --mobile
```

Pour l'acte IV, après coup :

```bash
python3 ooni_verif.py --since 2026-11-05 --until 2026-11-08 --focus 2026-11-06,2026-11-07 --mobile
```

### Format des données

`mesures_<vantage>.csv` contient une ligne par hôte et par tour, plus une ligne `meta` par tour. Les colonnes principales :

- **identification** : `ts_utc`, `round_id`, `vantage`, `fai`, `kind` (`cible`, `temoin_neg`, `temoin_pos` ou `meta`), `host` ;
- **DNS** : `sys_ips` et `sys_err`, `isp_rcode` et `isp_ips`, `p53_rcode` et `p53_ips`, `doh_rcode` et `doh_ips` ;
- **connexion** : `tcp_err`, `tls_err`, `tls_issuer`, `alt_*` (contre-essai), `http_status`, `http_err`, `fail_stage`.

**Avant de publier un CSV**, relis-le. Il ne contient pas ton adresse IP publique, mais il contient le nom de ton FAI et, pour certains, l'adresse IPv6 de ta box dans `isp_resolver`. Remplace-la si tu préfères ne pas la diffuser.

---

## 5. Résultats OONI du 17 au 31 octobre 2026

Le rapport complet est dans [`ooni/rapport_ooni.md`](ooni/rapport_ooni.md), généré le 6 novembre 2026. Il porte sur le test `web_connectivity` en France.

**Volume.** Il y a des mesures **chaque jour** du 17 au 31 octobre, entre 45 600 et 61 500 par jour, tous sites confondus.

**Connexions fixes (Wi-Fi), 24 et 31 octobre.**
- **Instagram, Facebook, YouTube et twitter.com** sont mesurés **à toutes les heures diurnes** (16 sur 16, de 7 h à 23 h) chez Orange, SFR, Free et Bouygues, sauf Bouygues le 24 (15 sur 16).
- **x.com et TikTok** sont mesurés entre 7 et 16 heures diurnes sur 16, selon l'opérateur. Tous opérateurs confondus, il n'y a jamais plus d'une heure sans mesure.
- **Snapchat** est moins couvert : entre 5 et 10 heures sur 16 selon l'opérateur, avec au plus une heure sans mesure tous opérateurs confondus.

**Anomalies sur les réseaux sociaux ces deux jours-là.** Aucune n'est *confirmée*, et aucune ne forme de motif répété chez un même grand opérateur qui coïnciderait avec ces journées.
- Les anomalies DNS sur facebook.com chez Free (`127.0.0.1`) viennent d'une sonde Android qui les produit **toutes les heures depuis au moins le 10 octobre**, donc avant la mobilisation. Les autres mesures chez Free, au même moment, sont normales. C'est probablement un bloqueur installé sur l'appareil, mais ce n'est pas prouvé.
- Les autres anomalies sont isolées, ou viennent d'hébergeurs et de VPN : OVH (AS16276), AS212238, AS25369.
- Les deux anomalies « confirmées » du 27 octobre (Instagram, Facebook) viennent d'une sonde hébergée chez OVH dont le DNS renvoyait l'empreinte d'une **page de blocage iranienne** (`10.10.x.x`). C'est un artefact de configuration, pas un blocage français.

**Témoin positif.** `sputnikglobe.com` et `ria.ru` sont vus bloqués par DNS chez les quatre opérateurs. OONI détecte donc bien ce type de blocage quand il existe.

**Mobile.** Dans les échantillons examinés, il y a **0 ou 1 mesure étiquetée « mobile »** par site, par opérateur et par jour. Free Mobile (AS51207) ne compte qu'environ 2 300 mesures en 15 jours, tous sites confondus. Pour les autres opérateurs, l'agrégation d'OONI ne distingue pas le fixe du mobile.

**Conclusion OONI pour le 24 et le 31 octobre :**
- **Connexions fixes des quatre grands opérateurs, pour X, TikTok, Instagram et Snapchat : non prouvé.** Aucun signal de blocage réseau, avec une couverture horaire suffisante pour qu'une coupure DNS de plusieurs heures chez l'un d'eux ait très probablement laissé des traces. Ça ne couvre pas un blocage très court ni un blocage limité à une zone.
- **Réseaux mobiles : non testable.** Les mesures sont trop rares, alors que la lettre visait justement le mobile.

---

## 6. Ce que ces données ne peuvent pas dire

- Elles ne disent rien du **retrait de contenus** (Pharos, demandes aux plateformes) ni du **déclassement** algorithmique.
- Elles ne disent pas **qui** a causé un éventuel échec, ni **pourquoi**.
- Elles ne disent rien des **opérateurs, zones et heures non mesurés**. Un point de mesure, c'est un opérateur, un lieu et une connexion.
- Elles ne permettent pas de détecter un **bridage de débit**, qu'on ne distingue pas de la saturation des antennes près d'un rassemblement.
- Elles ne permettent pas de détecter un **blocage sur IPv6 seulement** : le moniteur teste l'IPv4.
- Elles ne disent pas si les **applications mobiles** sont bloquées par un domaine non mesuré : la liste des domaines d'application est partielle.
- Elles ne permettent pas de détecter un blocage **plus court que l'intervalle de mesure** (5 à 10 minutes), ni un blocage pendant un **trou de mesure**.
- Le point « fixe » de l'auteur utilise un **DNS chiffré (1.1.1.1)** au niveau du système : sa colonne « DNS système » ne reflète pas l'expérience d'un client Bouygues ordinaire. Le filtrage DNS de l'opérateur y est mesuré par l'interrogation directe du résolveur de la box (`isp_rcode`).
- Elles ne disent rien d'une **demande** de blocage qui n'a pas été appliquée : la lettre du 22 octobre relève des textes, pas des mesures.

---

## 7. Éthique et périmètre

Les mesures sont passives, peu fréquentes (une page publique toutes les 5 minutes environ) et portent sur des sites publics. Le projet n'utilise aucun compte, aucun faux profil, aucune automatisation sur les plateformes et aucun test de portée de contenus. Aucune mesure ne vise une personne. L'adresse IP publique du point de mesure n'est pas enregistrée.

---

## 8. Conclusion (à compléter après l'acte IV)

| question | 24 et 31 oct. (OONI) | acte IV, 6 et 7 nov. (moniteur et OONI) |
|---|---|---|
| Blocage réseau sur les connexions fixes des grands opérateurs | **non prouvé** | en cours de mesure |
| Blocage réseau sur le mobile | **non testable** | selon la couverture 4G obtenue |
| Retrait administratif de contenus | hors mesure : documenté par les textes (amendement n°94) | hors mesure |
| Déclassement par les plateformes | hors périmètre | hors périmètre |
