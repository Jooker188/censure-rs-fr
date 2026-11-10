# Tests OONI sur l'iPhone, 6 et 7 novembre 2026

Retrouvés le 10 novembre dans les données publiques d'OONI (api.ooni.io) : mesures faites avec OONI Probe pour iOS (version 6.3.0), en réseau mobile, sur les réseaux des deux SIM, aux heures des tests. Les mesures OONI sont anonymes : l'attribution repose sur l'appareil, le réseau, l'heure et la liste de sites testée (celle préparée pour l'enquête : TikTok, Instagram, X, Snapchat, Facebook, Telegram, BeReal, Twitch, Wikipédia, `sputnikglobe.com`…).

**Réseaux confirmés par l'ASN** : la SIM RED passe par le réseau de **SFR** (AS15557), la SIM Cdiscount Mobile par celui de **Bouygues Telecom** (AS5410).

| quand (Paris) | réseau | mesures | réseaux sociaux et messageries testés | dont en anomalie | `sputnikglobe.com` (témoin positif) | autres anomalies |
|---|---|---|---|---|---|---|
| ven. 6 05 h 24 | Bouygues (AS5410) · SIM Cdiscount Mobile | 114 | 19 | **0** | bloqué ([mesure](https://explorer.ooni.org/m/20261106042447.553233_FR_webconnectivity_592add5deb190c11)) | 8 |
| ven. 6 05 h 32 | SFR (AS15557) · SIM RED | 53 | 9 | **0** | bloqué ([mesure](https://explorer.ooni.org/m/20261106043219.033761_FR_webconnectivity_90f10bf286991d0d)) | 4 |
| ven. 6 13 h 02 | SFR (AS15557) · SIM RED | 10 | 8 | **0** | bloqué ([mesure](https://explorer.ooni.org/m/20261106120247.330254_FR_webconnectivity_fb757ed9f1b8cd11)) | 0 |
| ven. 6 18 h 58 | SFR (AS15557) · SIM RED | 10 | 8 | **0** | bloqué ([mesure](https://explorer.ooni.org/m/20261106175803.997174_FR_webconnectivity_b6a996e1fe8be547)) | 0 |
| ven. 6 19 h 00 | Bouygues (AS5410) · SIM Cdiscount Mobile | 10 | 8 | **0** | bloqué ([mesure](https://explorer.ooni.org/m/20261106180004.396168_FR_webconnectivity_e1a02f384b66bbeb)) | 0 |
| sam. 7 01 h 48 | Bouygues (AS5410) · SIM Cdiscount Mobile | 21 | 19 | **0** | bloqué ([mesure](https://explorer.ooni.org/m/20261107004820.335808_FR_webconnectivity_bf1b491bd52bf105)) | 0 |
| sam. 7 13 h 30 | Bouygues (AS5410) · SIM Cdiscount Mobile | 18 | 16 | **0** | bloqué ([mesure](https://explorer.ooni.org/m/20261107123026.778837_FR_webconnectivity_86f3c781ce51fc81)) | 0 |
| sam. 7 13 h 32 | SFR (AS15557) · SIM RED | 21 | 19 | **0** | bloqué ([mesure](https://explorer.ooni.org/m/20261107123253.940946_FR_webconnectivity_ba5a5e40892d6240)) | 0 |
| sam. 7 15 h 19 | Bouygues (AS5410) · SIM Cdiscount Mobile | 17 | 15 | **0** | bloqué ([mesure](https://explorer.ooni.org/m/20261107141955.849310_FR_webconnectivity_3c765ba1fead8701)) | 0 |

**Lecture.**
- Aucun réseau social ni aucune messagerie n'a été vu en anomalie, sur aucun des deux réseaux mobiles, vendredi comme samedi après-midi (13 h 30 – 15 h 20, pendant les cortèges).
- Le témoin positif `sputnikglobe.com` a été vu bloqué à chaque passage, sur les deux réseaux : les tests savaient voir un blocage DNS.
- Les « autres anomalies » du vendredi matin viennent du test complet par défaut de l'appli (des centaines de sites du monde entier) : sites de paris en ligne non agréés en France, sites de streaming illégal, quelques sites étrangers. Rien qui concerne un réseau social.
- Limite : ce sont des tests ponctuels, pas une mesure continue. Rien n'a été testé samedi après 15 h 20.
