# Analyse des mesures

Fichiers analysés : mesures_vps.csv, mesures_fixe.csv. Les heures sont données en heure de Paris.

Ce rapport décrit des signaux réseau. Il ne désigne aucune cause, et une anomalie isolée n'est pas un blocage.

## 1. Contrôles de validité (à lire en premier)

| point | FAI déclaré | tours | période | intervalle médian | trous > 2,5 × intervalle | tours ignorés (témoins KO) | témoin positif bloqué au DNS du FAI | idem au DNS système | AS de sortie | 1.1.1.1 non intercepté |
|---|---|---|---|---|---|---|---|---|---|---|
| vps | Contabo VPS, Contabo Francfort | 987 | 06/11 05:35 → 09/11 15:56 | 5.0 min | 0 | 0 | 0/1974 | 0/1974 | 51167 (987) | 987/987 |
| fixe | Bbox fibre | 369 | 06/11 05:11 → 07/11 11:52 | 5.0 min | 0 | 0 | 738/738 | 0/738 | 5410 (369) | 369/369 |

Comment lire ce tableau :
- **Témoin positif.** Pour un FAI français, le DNS de l'opérateur doit le bloquer dans presque tous les tours. Si ce n'est pas le cas, l'outil ne voit pas le filtrage DNS du FAI depuis ce point : on ne peut alors rien conclure sur le DNS, seulement sur TCP, TLS et HTTP. Depuis un VPS à l'étranger, un résultat proche de 0 est normal.
- **Écart entre DNS du FAI et DNS système.** La machine n'utilise pas le résolveur du FAI (DoH, DNS manuel, antivirus…) : les applications de cette machine ne subiraient pas un filtrage DNS du FAI.
- **AS de sortie.** Un AS inattendu signale un VPN ou une bascule du téléphone entre 4G et Wi-Fi.
- **Trous.** Une période sans mesure ne veut pas dire « accessible ».

## 2. Épisodes (signaux répétés ou isolés)

Un épisode regroupe un même signal, sur le même hôte et le même point de mesure, pendant des tours consécutifs (un tour manquant toléré). On le dit « répété » à partir de 3 tours. Les témoins sont dits « OK » quand les sites ordinaires répondaient pendant tout l'épisode.

| point | plateforme | hôte | signal | gravité | début | fin | tours | répété | témoins OK | autres points (même fenêtre) |
|---|---|---|---|---|---|---|---|---|---|---|
| fixe | YouTube | i.ytimg.com | `tcp_timeout_ip_seule` | signature | 06/11 08:18 | 06/11 08:18 | 1 | non | oui | vps: 0 même signal / 4 sans |
| fixe | Instagram | static.cdninstagram.com | `dns_fai_timeout` | echec | 06/11 09:30 | 06/11 09:30 | 1 | non | oui | vps: 0 même signal / 4 sans |
| fixe | Messenger | www.messenger.com | `tcp_timeout_ip_seule` | signature | 06/11 13:47 | 06/11 13:47 | 1 | non | oui | vps: 0 même signal / 4 sans |
| fixe | Snapchat | www.snapchat.com | `tcp_timeout_ip_seule` | signature | 06/11 19:23 | 06/11 19:23 | 1 | non | oui | vps: 0 même signal / 4 sans |
| fixe | Instagram | i.instagram.com | `tcp_timeout_ip_seule` | signature | 06/11 22:37 | 06/11 22:37 | 1 | non | oui | vps: 0 même signal / 4 sans |
| fixe | Instagram | i.instagram.com | `tcp_timeout_ip_seule` | signature | 06/11 23:51 | 06/11 23:51 | 1 | non | oui | vps: 0 même signal / 4 sans |
| vps | Instagram | www.instagram.com | `dns_p53_nx` | signature | 06/11 18:30 | 06/11 18:44 | 3 | oui | oui | fixe: 0 même signal / 7 sans |
| vps | Instagram | i.instagram.com | `dns_p53_nx` | signature | 06/11 18:30 | 06/11 19:05 | 5 | oui | oui | fixe: 0 même signal / 11 sans |
| vps | Instagram | www.instagram.com | `dns_p53_nx` | signature | 06/11 19:05 | 06/11 19:10 | 2 | non | oui | fixe: 0 même signal / 5 sans |
| vps | Instagram | i.instagram.com | `dns_p53_nx` | signature | 06/11 19:20 | 06/11 19:20 | 1 | non | oui | fixe: 0 même signal / 4 sans |
| vps | Instagram | www.instagram.com | `dns_p53_nx` | signature | 06/11 19:25 | 06/11 19:25 | 1 | non | oui | fixe: 0 même signal / 4 sans |
| vps | Instagram | i.instagram.com | `dns_p53_nx` | signature | 06/11 19:35 | 06/11 20:00 | 4 | oui | oui | fixe: 0 même signal / 9 sans |
| vps | Instagram | www.instagram.com | `dns_p53_nx` | signature | 06/11 19:40 | 06/11 20:10 | 4 | oui | oui | fixe: 0 même signal / 10 sans |
| vps | X | x.com | `dns_p53_nx` | signature | 07/11 13:33 | 07/11 13:38 | 2 | non | oui | fixe: pas de mesure |
| vps | X | x.com | `dns_p53_nx` | signature | 07/11 14:59 | 07/11 14:59 | 1 | non | oui | fixe: pas de mesure |
| vps | X | x.com | `dns_p53_nx` | signature | 07/11 16:03 | 07/11 16:03 | 1 | non | oui | fixe: pas de mesure |
| vps | Telegram | web.telegram.org | `dns_p53_timeout` | echec | 08/11 01:11 | 08/11 01:11 | 1 | non | oui | fixe: pas de mesure |
| vps | Twitch | www.twitch.tv | `dns_p53_timeout` | echec | 08/11 11:58 | 08/11 11:58 | 1 | non | oui | fixe: pas de mesure |
| vps | Instagram | static.cdninstagram.com | `dns_p53_timeout` | echec | 08/11 11:58 | 08/11 11:58 | 1 | non | oui | fixe: pas de mesure |
| vps | Snapchat | www.snapchat.com | `dns_p53_timeout` | echec | 08/11 11:58 | 08/11 11:58 | 1 | non | oui | fixe: pas de mesure |
| vps | Telegram | telegram.org | `dns_p53_timeout` | echec | 08/11 11:58 | 08/11 11:58 | 1 | non | oui | fixe: pas de mesure |
| vps | Facebook | www.facebook.com | `dns_p53_timeout` | echec | 08/11 11:58 | 08/11 11:58 | 1 | non | oui | fixe: pas de mesure |
| vps | TikTok | www.tiktok.com | `tls_timeout` | echec | 08/11 16:09 | 08/11 16:09 | 1 | non | oui | fixe: pas de mesure |
| vps | X | x.com | `dns_p53_nx` | signature | 08/11 16:24 | 08/11 16:24 | 1 | non | oui | fixe: pas de mesure |
| vps | TikTok | tiktokv.com | `tls_timeout` | echec | 08/11 18:40 | 08/11 18:40 | 1 | non | oui | fixe: pas de mesure |
| vps | X | x.com | `dns_p53_nx` | signature | 09/11 08:35 | 09/11 08:35 | 1 | non | oui | fixe: pas de mesure |

Signaux sur les témoins ordinaires : 6 épisode(s), voir `episodes.csv`. S'ils coïncident avec des signaux sur les cibles, c'est la connexion de mesure qui est en cause.

## 3. Synthèse par plateforme et par point de mesure

Classement **descriptif** : il dit ce que montrent les mesures, pas pourquoi.

| plateforme | vps | fixe |
|---|---|---|
| X | signaux isolés (5), non concluants | aucun signal |
| TikTok | signaux isolés (2), non concluants | aucun signal |
| Instagram | **motif répété compatible avec un blocage** (4 épisode(s)) : à examiner | signaux isolés (3), non concluants |
| Snapchat | signaux isolés (1), non concluants | signaux isolés (1), non concluants |
| Facebook | signaux isolés (1), non concluants | aucun signal |
| YouTube | aucun signal | signaux isolés (1), non concluants |
| Discord | aucun signal | aucun signal |
| Telegram | signaux isolés (2), non concluants | aucun signal |
| Bluesky | aucun signal | aucun signal |
| WhatsApp | aucun signal | aucun signal |
| Signal | aucun signal | aucun signal |
| Messenger | aucun signal | signaux isolés (1), non concluants |
| Threads | aucun signal | aucun signal |
| Reddit | aucun signal | aucun signal |
| Twitch | signaux isolés (1), non concluants | aucun signal |
| BeReal | aucun signal | aucun signal |
| Mastodon | aucun signal | aucun signal |

Critères d'un « motif répété compatible avec un blocage » : signature de blocage (réponse DNS du FAI NXDOMAIN, adresse privée ou REFUSED alors que le DoH répond ; connexion réinitialisée ; certificat invalide), sur au moins 3 tours consécutifs, pendant que les témoins répondent. Il faut ensuite vérifier, à la main, si le même signal apparaît sur un autre point de mesure ou dans OONI.

## 4. Changements d'émetteur de certificat

Aucun.

## 5. Codes HTTP par point de mesure (pour information)

Un 403, un 429 ou une redirection vers la page de connexion est la réponse normale d'une plateforme à un script. Ce n'est pas un blocage réseau. Seul un changement brutal, absent des autres points de mesure, mérite d'être regardé.

| point | hôte | codes (nombre) |
|---|---|---|
| fixe | bere.al | 302 (369) |
| fixe | bsky.app | 200 (369) |
| fixe | discord.com | 200 (369) |
| fixe | mastodon.social | 200 (369) |
| fixe | signal.org | 200 (369) |
| fixe | t.me | 302 (369) |
| fixe | telegram.org | 200 (369) |
| fixe | www.akamai.com | 302 (369) |
| fixe | www.cloudflare.com | 200 (369) |
| fixe | www.facebook.com | 200 (369) |
| fixe | www.fastly.com | 200 (369) |
| fixe | www.google.com | 200 (369) |
| fixe | www.instagram.com | 200 (368), 500 (1) |
| fixe | www.lemonde.fr | 200 (369) |
| fixe | www.messenger.com | 200 (368), aucun (1) |
| fixe | www.reddit.com | 200 (369) |
| fixe | www.snapchat.com | 200 (368), aucun (1) |
| fixe | www.threads.net | 301 (369) |
| fixe | www.tiktok.com | 200 (364), 302 (5) |
| fixe | www.twitch.tv | 200 (369) |
| fixe | www.whatsapp.com | 200 (369) |
| fixe | www.wikipedia.org | 200 (369) |
| fixe | www.youtube.com | 200 (369) |
| fixe | x.com | 200 (369) |
| vps | bere.al | 302 (987) |
| vps | bsky.app | 200 (987) |
| vps | discord.com | 200 (987) |
| vps | mastodon.social | 200 (987) |
| vps | signal.org | 200 (987) |
| vps | t.me | 302 (987) |
| vps | telegram.org | 200 (982), 404 (5) |
| vps | www.akamai.com | 302 (986), aucun (1) |
| vps | www.cloudflare.com | 200 (987) |
| vps | www.facebook.com | 302 (727), 200 (260) |
| vps | www.fastly.com | 200 (987) |
| vps | www.google.com | 200 (987) |
| vps | www.instagram.com | 200 (987) |
| vps | www.lemonde.fr | 200 (987) |
| vps | www.messenger.com | 200 (987) |
| vps | www.reddit.com | 403 (987) |
| vps | www.snapchat.com | 200 (987) |
| vps | www.threads.net | 301 (987) |
| vps | www.tiktok.com | 200 (968), 302 (18), aucun (1) |
| vps | www.twitch.tv | 200 (987) |
| vps | www.whatsapp.com | 200 (987) |
| vps | www.wikipedia.org | 200 (987) |
| vps | www.youtube.com | 200 (987) |
| vps | x.com | 200 (987) |

## 6. Événements de référence

| début | fin | événement | statut | source |
|---|---|---|---|---|
| 2026-10-17T00:00 | 2026-10-17T23:59 | Mobilisation nationale : 550 000 manifestants selon l'Intérieur, 800 000 selon les organisateurs | documenté (presse) | https://www.ici.fr/infos/societe/direct-mobilisation-du-17-octobre-150000-personnes-attendues-dans-les-rues-ce-samedi-hors-agglomeration-parisienne-4822424 |
| 2026-10-22T12:00 |  | Lettre de Matignon aux 4 opérateurs : se tenir prêts à suspendre TikTok, Instagram, Snapchat (X ajouté selon certaines sources) | documenté (presse : Blast ; non démenti) | https://www.clubic.com/actualite-635851-le-gouvernement-voulait-pouvoir-couper-les-reseaux-sociaux-pendant-la-manifestation-du-24-octobre-une-lettre-le-prouve.html |
| 2026-10-24T00:00 | 2026-10-24T23:59 | Manifestation du 24 octobre (aucune coupure déclenchée selon la presse) | documenté (presse) | https://journalducoin.com/technologies/coupure-reseaux-sociaux-france-matignon-bitchat-crypto |
| 2026-10-27T21:00 |  | Sénat : amendement gouvernemental n°94 (projet de loi casseurs-payeurs) adopté, 219 voix contre 115 | documenté (presse) | https://www.publicsenat.fr/actualites/politique/derive-autoritaire-la-gauche-senatoriale-vent-debout-apres-ladoption-dun-amendement-sur-le-blocage-de-certains-contenus-sur-les-reseaux-sociaux |
| 2026-10-30T12:00 |  | Groupe de contact permanent (plateformes, opérateurs, administration) réuni à Matignon | documenté (presse : L'Informé) | https://www.linforme.com/tech-telecom/article/reseaux-sociaux-le-groupe-de-contact-permanent-a-nouveau-reuni_13067.html |
| 2026-11-06T00:00 | 2026-11-06T23:59 | Acte IV : grèves et blocages | annoncé (presse) | https://www.sortiraparis.com/actualites/a-paris/articles/356694-gilets-jaunes-acte-iv-les-6-et-7-novembre-greve-et-manifestation-le-point-a-paris |
| 2026-11-07T00:00 | 2026-11-07T23:59 | Acte IV : manifestations dans toute la France | annoncé (presse) | https://www.sortiraparis.com/actualites/a-paris/articles/356694-gilets-jaunes-acte-iv-les-6-et-7-novembre-greve-et-manifestation-le-point-a-paris |
| 2026-11-07T14:00 |  | Paris : rassemblement annoncé place de la Concorde (sous réserve d'accord de la préfecture) | annoncé (presse) | https://www.sortiraparis.com/actualites/a-paris/articles/356694-gilets-jaunes-acte-iv-les-6-et-7-novembre-greve-et-manifestation-le-point-a-paris |
