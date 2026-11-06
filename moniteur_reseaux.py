#!/usr/bin/env python3
"""
moniteur_reseaux.py (v2) — mesure passive et à faible fréquence de
l'accessibilité de réseaux sociaux depuis une connexion française.

Pour chaque domaine et à chaque tour, il découpe la connexion en étapes afin
de savoir OÙ elle échoue :
  1. DNS système (getaddrinfo, ce que voient les applications)
  2. DNS du FAI, interrogé directement en UDP (code de réponse exact :
     NXDOMAIN, SERVFAIL, REFUSED…)
  3. DNS public 1.1.1.1 en UDP/53 (peut être intercepté par le FAI)
  4. DNS public en DoH (HTTPS, non interceptable sans casser TLS) = référence
  5. TCP:443 vers l'IP du DNS système, puis TLS avec SNI (certificat vérifié)
  6. Si 5 échoue : même essai vers l'IP DoH (distingue blocage IP / SNI)
  7. HTTP GET / (sites « web » seulement), lecture limitée à 16 Ko

Chaque tour ajoute aussi une ligne « meta » : AS du réseau de sortie, et un
test d'interception du DNS public (id.server sur 1.1.1.1). Votre adresse IP
publique n'est PAS enregistrée.

Bibliothèque standard uniquement, Python >= 3.9. Aucune connexion à un
compte, aucune interaction avec les plateformes au-delà d'une page publique.

Exemples :
  python3 moniteur_reseaux.py --vantage fixe --fai "Orange fibre" --once
  python3 moniteur_reseaux.py --vantage 4g --fai "Bouygues 4G" --interval 600
"""
import argparse
import concurrent.futures as cf
import csv
import datetime as dt
import hashlib
import ipaddress
import json
import os
import random
import secrets
import socket
import ssl
import struct
import sys
import threading
import time
import urllib.parse
import urllib.request

VERSION = "2.0"

# (plateforme, hôte, rôle). rôle : web = DNS+TCP+TLS+HTTP ; infra = DNS+TCP+TLS
# Les hôtes « infra » sont ceux qu'utilisent les applications mobiles ; liste
# non exhaustive, à compléter avec --extra après observation du journal DNS
# de votre téléphone.
CIBLES = [
    ("x", "x.com", "web"), ("x", "api.x.com", "infra"),
    ("x", "pbs.twimg.com", "infra"), ("x", "video.twimg.com", "infra"),
    ("tiktok", "www.tiktok.com", "web"), ("tiktok", "tiktokv.com", "infra"),
    ("tiktok", "tiktokcdn.com", "infra"),
    ("instagram", "www.instagram.com", "web"), ("instagram", "i.instagram.com", "infra"),
    ("instagram", "static.cdninstagram.com", "infra"),
    ("snapchat", "www.snapchat.com", "web"), ("snapchat", "app.snapchat.com", "infra"),
    ("facebook", "www.facebook.com", "web"), ("facebook", "static.xx.fbcdn.net", "infra"),
    ("youtube", "www.youtube.com", "web"), ("youtube", "i.ytimg.com", "infra"),
    ("discord", "discord.com", "web"), ("discord", "gateway.discord.gg", "infra"),
    ("telegram", "t.me", "web"), ("telegram", "web.telegram.org", "infra"),
    ("bluesky", "bsky.app", "web"), ("bluesky", "bsky.social", "infra"),
    ("whatsapp", "www.whatsapp.com", "web"), ("whatsapp", "web.whatsapp.com", "infra"),
    ("signal", "signal.org", "web"), ("signal", "chat.signal.org", "infra"),
]
# Témoins négatifs : doivent fonctionner. Les CDN génériques servent à
# repérer une panne d'hébergeur (Akamai, Fastly, Cloudflare, Google).
TEMOINS_NEG = [
    ("temoin", "www.wikipedia.org", "web"), ("temoin", "www.lemonde.fr", "web"),
    ("temoin_cdn", "www.akamai.com", "web"), ("temoin_cdn", "www.fastly.com", "web"),
    ("temoin_cdn", "www.cloudflare.com", "web"), ("temoin_cdn", "www.google.com", "web"),
]
# Témoin positif : domaines bloqués par DNS chez Orange, SFR, Free, Bouygues
# (sanctions UE contre les médias d'État russes ; observé par OONI en
# oct. 2026). DNS uniquement : aucune connexion n'est ouverte vers eux.
TEMOINS_POS = [("temoin_pos", "sputnikglobe.com", "dns"), ("temoin_pos", "ria.ru", "dns")]

# Adresses IP en dur : le DoH ne doit pas dépendre du DNS qu'il contrôle.
DOH = ["https://1.1.1.1/dns-query", "https://8.8.8.8/resolve", "https://cloudflare-dns.com/dns-query"]
PUB53 = "1.1.1.1"
UA = "Mozilla/5.0 (X11; Linux x86_64) moniteur_reseaux/" + VERSION

COLONNES = [
    "ts_utc", "round_id", "tool_version", "vantage", "fai", "kind", "platform", "host", "role",
    "sys_ips", "sys_err",
    "isp_resolver", "isp_rcode", "isp_ips", "isp_ms",
    "p53_rcode", "p53_ips",
    "doh_rcode", "doh_ips",
    "dns_verdict",
    "tcp_ip", "tcp_ms", "tcp_err",
    "tls_ms", "tls_err", "tls_issuer", "tls_version",
    "alt_ip", "alt_tcp_err", "alt_tls_err",
    "http_status", "http_ms", "http_bytes", "http_err", "http_location_host",
    "fail_stage", "note",
]

RCODES = {0: "NOERROR", 1: "FORMERR", 2: "SERVFAIL", 3: "NXDOMAIN", 4: "NOTIMP", 5: "REFUSED"}


# ------------------------------------------------------------------ DNS brut
def _qname(name):
    out = b""
    for part in name.rstrip(".").split("."):
        out += bytes([len(part)]) + part.encode("idna")
    return out + b"\x00"


def _skip_name(buf, i):
    while True:
        n = buf[i]
        if n == 0:
            return i + 1
        if n & 0xC0 == 0xC0:
            return i + 2
        i += n + 1


def dns_udp(server, name, qtype=1, qclass=1, timeout=4.0, port=53):
    """Requête DNS UDP minimale. Renvoie (rcode_str, [réponses], ms) ou lève."""
    tid = secrets.randbits(16)
    pkt = struct.pack(">HHHHHH", tid, 0x0100, 1, 0, 0, 0) + _qname(name) + struct.pack(">HH", qtype, qclass)
    fam = socket.AF_INET6 if ":" in server else socket.AF_INET
    s = socket.socket(fam, socket.SOCK_DGRAM)
    s.settimeout(timeout)
    t0 = time.monotonic()
    try:
        s.sendto(pkt, (server, port))
        while True:
            buf, _ = s.recvfrom(4096)
            if len(buf) >= 12 and struct.unpack(">H", buf[:2])[0] == tid:
                break
    finally:
        s.close()
    ms = int((time.monotonic() - t0) * 1000)
    _, flags, qd, an, _, _ = struct.unpack(">HHHHHH", buf[:12])
    rcode = RCODES.get(flags & 0xF, str(flags & 0xF))
    i = 12
    for _ in range(qd):
        i = _skip_name(buf, i) + 4
    res = []
    for _ in range(an):
        i = _skip_name(buf, i)
        rtype, _, _, rdlen = struct.unpack(">HHIH", buf[i:i + 10])
        i += 10
        rdata = buf[i:i + rdlen]
        i += rdlen
        if rtype == 1 and rdlen == 4:
            res.append(socket.inet_ntoa(rdata))
        elif rtype == 16:  # TXT
            j, txt = 0, b""
            while j < len(rdata):
                ln = rdata[j]
                txt += rdata[j + 1:j + 1 + ln]
                j += ln + 1
            res.append(txt.decode(errors="replace"))
    if rcode == "NOERROR" and qtype == 1 and not res:
        rcode = "NODATA"
    return rcode, res, ms


def dns_doh(name, timeout=6.0):
    """Résolution A en DoH (JSON). Renvoie (rcode_str, [ips])."""
    last = None
    for base in DOH:
        url = base + "?" + urllib.parse.urlencode({"name": name, "type": "A"})
        try:
            req = urllib.request.Request(url, headers={"accept": "application/dns-json", "User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                d = json.load(r)
            ips = [a["data"] for a in d.get("Answer", []) if a.get("type") == 1]
            rc = RCODES.get(d.get("Status", -1), str(d.get("Status")))
            if rc == "NOERROR" and not ips:
                rc = "NODATA"
            return rc, ips
        except Exception as e:
            last = e
    return "ERR:" + classe_err(last), []


def resolveur_systeme():
    try:
        with open("/etc/resolv.conf", encoding="utf-8") as f:
            for line in f:
                p = line.split()
                if len(p) >= 2 and p[0] == "nameserver":
                    return p[1]
    except OSError:
        pass
    return ""


# ------------------------------------------------------------- utilitaires
def classe_err(e):
    if e is None:
        return ""
    if isinstance(e, socket.gaierror):
        return {socket.EAI_NONAME: "gai_noname", socket.EAI_AGAIN: "gai_again"}.get(e.errno, f"gai_{e.errno}")
    if isinstance(e, ssl.SSLCertVerificationError):
        return "cert_invalide:" + (e.verify_message or "").replace(" ", "_")
    if isinstance(e, ssl.SSLError):
        return "tls:" + (e.reason or type(e).__name__)
    if isinstance(e, (socket.timeout, TimeoutError)):
        return "timeout"
    if isinstance(e, ConnectionResetError):
        return "reset"
    if isinstance(e, ConnectionRefusedError):
        return "refused"
    if isinstance(e, ConnectionAbortedError):
        return "aborted"
    if isinstance(e, urllib.error.URLError):
        return classe_err(e.reason) if isinstance(e.reason, BaseException) else "url:" + str(e.reason)
    if isinstance(e, OSError) and e.errno:
        import errno
        return errno.errorcode.get(e.errno, str(e.errno)).lower()
    return type(e).__name__


def bogon(ip):
    try:
        a = ipaddress.ip_address(ip)
    except ValueError:
        return True
    return (a.is_private or a.is_loopback or a.is_unspecified or a.is_reserved
            or a.is_link_local or a.is_multicast
            or (a.version == 4 and a in ipaddress.ip_network("100.64.0.0/10")))


def verdict_dns(sys_ips, sys_err, doh_rc, doh_ips):
    doh_ok = doh_rc == "NOERROR" and doh_ips
    if sys_err and not sys_ips:
        return "local_echec" if doh_ok else "echec_global"
    if any(bogon(i) for i in sys_ips) and not any(bogon(i) for i in doh_ips):
        return "bogon"
    if not doh_ok:
        return "doh_indisponible"
    return "coherent" if set(sys_ips) & set(doh_ips) else "ips_differentes"


def issuer_str(cert):
    try:
        d = {k: v for rdn in cert.get("issuer", ()) for k, v in rdn}
        return f"{d.get('organizationName', '')}/{d.get('commonName', '')}"
    except Exception:
        return ""


def tcp_tls(ip, host, timeout, certs_dir):
    """Renvoie dict tcp_ms, tcp_err, tls_ms, tls_err, issuer, version, sock (ou None)."""
    r = {"tcp_ms": "", "tcp_err": "", "tls_ms": "", "tls_err": "", "issuer": "", "version": "", "sock": None}
    t0 = time.monotonic()
    try:
        raw = socket.create_connection((ip, 443), timeout=timeout)
    except Exception as e:
        r["tcp_err"] = classe_err(e)
        return r
    r["tcp_ms"] = int((time.monotonic() - t0) * 1000)
    ctx = ssl.create_default_context()
    t1 = time.monotonic()
    try:
        s = ctx.wrap_socket(raw, server_hostname=host)
        r["tls_ms"] = int((time.monotonic() - t1) * 1000)
        r["issuer"] = issuer_str(s.getpeercert())
        r["version"] = s.version() or ""
        r["sock"] = s
    except Exception as e:
        r["tls_err"] = classe_err(e)
        raw.close()
        if isinstance(e, ssl.SSLCertVerificationError) and certs_dir:
            r["issuer"] = sauver_cert_invalide(ip, host, timeout, certs_dir)
    return r


def sauver_cert_invalide(ip, host, timeout, certs_dir):
    """Certificat refusé : on le récupère sans vérification pour pouvoir
    l'examiner ensuite (openssl x509 -inform der -in …). Possible indice
    d'interception (MITM) ou de page de blocage."""
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with socket.create_connection((ip, 443), timeout=timeout) as raw:
            with ctx.wrap_socket(raw, server_hostname=host) as s:
                der = s.getpeercert(binary_form=True)
        h = hashlib.sha256(der).hexdigest()[:16]
        os.makedirs(certs_dir, exist_ok=True)
        with open(os.path.join(certs_dir, f"{host}_{h}.der"), "wb") as f:
            f.write(der)
        return "INVALIDE:sha256=" + h
    except Exception as e:
        return "INVALIDE:" + classe_err(e)


def http_get(sock, host, timeout):
    r = {"status": "", "ms": "", "bytes": "", "err": "", "loc": ""}
    t0 = time.monotonic()
    try:
        sock.settimeout(timeout)
        req = (f"GET / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {UA}\r\n"
               "Accept: text/html\r\nAccept-Encoding: identity\r\nConnection: close\r\n\r\n")
        sock.sendall(req.encode())
        buf = b""
        while len(buf) < 16384:
            chunk = sock.recv(4096)
            if not chunk:
                break
            buf += chunk
        r["ms"] = int((time.monotonic() - t0) * 1000)
        r["bytes"] = len(buf)
        head = buf.split(b"\r\n\r\n", 1)[0].decode("latin-1", "replace").split("\r\n")
        if head and head[0].startswith("HTTP/"):
            parts = head[0].split()
            r["status"] = parts[1] if len(parts) > 1 else ""
        for line in head[1:]:
            if line.lower().startswith("location:"):
                r["loc"] = urllib.parse.urlsplit(line.split(":", 1)[1].strip()).hostname or "(relatif)"
        if not r["status"]:
            r["err"] = "reponse_non_http"
    except Exception as e:
        r["err"] = classe_err(e)
        r["ms"] = int((time.monotonic() - t0) * 1000)
    finally:
        try:
            sock.close()
        except Exception:
            pass
    return r


# ---------------------------------------------------------------- mesures
def mesurer(cible, kind, ctx):
    platform, host, role = cible
    row = dict.fromkeys(COLONNES, "")
    row.update(ts_utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               round_id=ctx["round_id"], tool_version=VERSION, vantage=ctx["vantage"], fai=ctx["fai"],
               kind=kind, platform=platform, host=host, role=role, isp_resolver=ctx["resolver"])
    to = ctx["timeout"]

    # 1. DNS système (IPv4 pour rester comparable au DoH)
    sys_ips = []
    try:
        infos = socket.getaddrinfo(host, 443, socket.AF_INET, socket.SOCK_STREAM)
        sys_ips = sorted({i[4][0] for i in infos})
    except Exception as e:
        row["sys_err"] = classe_err(e)
    row["sys_ips"] = " ".join(sys_ips)

    # 2. résolveur du FAI en direct
    if ctx["resolver"]:
        try:
            rc, ips, ms = dns_udp(ctx["resolver"], host, timeout=to)
            row.update(isp_rcode=rc, isp_ips=" ".join(sorted(ips)), isp_ms=ms)
        except Exception as e:
            row["isp_rcode"] = "ERR:" + classe_err(e)
    # 3. 1.1.1.1 port 53
    try:
        rc, ips, _ = dns_udp(PUB53, host, timeout=to)
        row.update(p53_rcode=rc, p53_ips=" ".join(sorted(ips)))
    except Exception as e:
        row["p53_rcode"] = "ERR:" + classe_err(e)
    # 4. DoH
    doh_rc, doh_ips = dns_doh(host, timeout=to + 2)
    row.update(doh_rcode=doh_rc, doh_ips=" ".join(sorted(doh_ips)))
    row["dns_verdict"] = verdict_dns(sys_ips, row["sys_err"], doh_rc, doh_ips)

    if role == "dns":  # témoin positif : jamais de connexion
        v = row["dns_verdict"]
        row["fail_stage"] = ("dns" if v in ("local_echec", "bogon")
                             else "aucun" if v in ("coherent", "ips_differentes") else "indetermine")
        return row
    if not sys_ips:
        row["fail_stage"] = "dns"
        return row

    # 5. TCP + TLS vers l'IP système
    ip = sys_ips[0]
    row["tcp_ip"] = ip
    t = tcp_tls(ip, host, to, ctx["certs_dir"])
    row.update(tcp_ms=t["tcp_ms"], tcp_err=t["tcp_err"], tls_ms=t["tls_ms"], tls_err=t["tls_err"],
               tls_issuer=t["issuer"], tls_version=t["version"])

    # 6. Contre-essai vers une IP DoH si échec
    if (t["tcp_err"] or t["tls_err"]) and doh_ips:
        alt = next((i for i in doh_ips if i not in sys_ips), doh_ips[0])
        a = tcp_tls(alt, host, to, None)
        row.update(alt_ip=alt, alt_tcp_err=a["tcp_err"] or "ok", alt_tls_err=a["tls_err"] or ("ok" if not a["tcp_err"] else ""))
        if a["sock"]:
            a["sock"].close()

    if t["tcp_err"]:
        row["fail_stage"] = "tcp"
        return row
    if t["tls_err"]:
        row["fail_stage"] = "tls"
        return row

    # 7. HTTP
    if role == "web":
        h = http_get(t["sock"], host, to * 2)
        row.update(http_status=h["status"], http_ms=h["ms"], http_bytes=h["bytes"], http_err=h["err"],
                   http_location_host=h["loc"])
        row["fail_stage"] = "http" if h["err"] else "aucun"
    else:
        t["sock"].close()
        row["fail_stage"] = "aucun"
    return row


def ligne_meta(ctx):
    """AS de sortie (via Cloudflare trace + RIPEstat, IP non conservée) et
    test d'interception du DNS public (id.server CH TXT sur 1.1.1.1)."""
    row = dict.fromkeys(COLONNES, "")
    row.update(ts_utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               round_id=ctx["round_id"], tool_version=VERSION, vantage=ctx["vantage"], fai=ctx["fai"],
               kind="meta", host="_meta", isp_resolver=ctx["resolver"])
    notes = []
    try:
        rc, txt, _ = dns_udp(PUB53, "id.server", qtype=16, qclass=3, timeout=ctx["timeout"])
        notes.append(f"p53_id={rc}:{'|'.join(txt)}")
    except Exception as e:
        notes.append("p53_id=ERR:" + classe_err(e))
    if not ctx["no_asn"]:
        try:
            req = urllib.request.Request("https://1.1.1.1/cdn-cgi/trace", headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=ctx["timeout"]) as r:
                kv = dict(l.split("=", 1) for l in r.read().decode().splitlines() if "=" in l)
            notes.append(f"cf_colo={kv.get('colo', '')}")
            ip = kv.get("ip", "")
            asn = ctx["asn_cache"].get(ip)
            if asn is None and ip:
                u = "https://stat.ripe.net/data/network-info/data.json?" + urllib.parse.urlencode({"resource": ip})
                with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=10) as r:
                    asn = ",".join(json.load(r)["data"].get("asns", []))
                ctx["asn_cache"] = {ip: asn}  # une seule entrée, jamais écrite sur disque
            notes.append(f"asn={asn}")
            notes.append("ipv=" + ("6" if ":" in ip else "4"))
        except Exception as e:
            notes.append("asn=ERR:" + classe_err(e))
    row["note"] = " ".join(notes)
    return row


# ------------------------------------------------------------------ boucle
_lock = threading.Lock()


def ecrire(path, rows):
    neuf = not os.path.exists(path) or os.path.getsize(path) == 0
    with _lock, open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLONNES)
        if neuf:
            w.writeheader()
        w.writerows(rows)
        f.flush()
        os.fsync(f.fileno())


def un_tour(ctx, cibles):
    ctx["round_id"] = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    rows = [ligne_meta(ctx)]
    ordre = list(cibles)
    random.shuffle(ordre)  # évite qu'un site soit toujours mesuré en premier
    with cf.ThreadPoolExecutor(max_workers=ctx["workers"]) as ex:
        futs = [ex.submit(mesurer, c, k, ctx) for c, k in ordre]
        for f in cf.as_completed(futs):
            try:
                rows.append(f.result())
            except Exception as e:  # ne jamais perdre un tour entier
                rows.append({**dict.fromkeys(COLONNES, ""), "ts_utc": ctx["round_id"], "note": "crash:" + repr(e)})
    ecrire(ctx["out"], rows)
    return rows


def afficher(rows):
    print(f"{'host':28} {'verdict DNS':17} {'isp':9} {'doh':9} {'étape KO':9} {'tcp/tls/http':28} issuer")
    for r in sorted(rows, key=lambda r: (r["kind"], r["platform"], r["host"])):
        if r["kind"] == "meta":
            print("META", r["note"])
            continue
        err = r["tcp_err"] or r["tls_err"] or r["http_err"] or r["http_status"]
        print(f"{r['host'][:28]:28} {r['dns_verdict']:17} {r['isp_rcode'][:9]:9} {r['doh_rcode'][:9]:9} "
              f"{r['fail_stage']:9} {str(err)[:28]:28} {r['tls_issuer'][:30]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vantage", required=True, help="nom du point de mesure : fixe, 4g, vps…")
    ap.add_argument("--fai", required=True, help='opérateur et accès, ex. "Free fibre", "SFR 4G"')
    ap.add_argument("--out", help="fichier CSV (défaut : mesures_<vantage>.csv)")
    ap.add_argument("--interval", type=int, default=300, help="secondes entre deux tours (défaut 300)")
    ap.add_argument("--resolver", default=None,
                    help="IP du résolveur du FAI/de la box (défaut : 1er nameserver de /etc/resolv.conf)")
    ap.add_argument("--extra", action="append", default=[],
                    help="hôte supplémentaire plateforme:hôte[:web|infra], répétable")
    ap.add_argument("--timeout", type=float, default=8.0)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--once", action="store_true", help="un seul tour, affiché à l'écran")
    ap.add_argument("--no-asn", action="store_true", help="ne pas interroger 1.1.1.1/cdn-cgi/trace ni RIPEstat")
    ap.add_argument("--certs-dir", default="certs_invalides")
    a = ap.parse_args()

    cibles = [(c, "cible") for c in CIBLES] + [(c, "temoin_neg") for c in TEMOINS_NEG] \
        + [(c, "temoin_pos") for c in TEMOINS_POS]
    for e in a.extra:
        p = e.split(":")
        cibles.append(((p[0], p[1], p[2] if len(p) > 2 else "infra"), "cible"))

    resolver = a.resolver if a.resolver is not None else resolveur_systeme()
    ctx = dict(vantage=a.vantage, fai=a.fai, resolver=resolver, timeout=a.timeout, workers=a.workers,
               out=a.out or f"mesures_{a.vantage}.csv", certs_dir=a.certs_dir, no_asn=a.no_asn,
               asn_cache={}, round_id="")
    print(f"moniteur v{VERSION} | point={a.vantage} | fai={a.fai} | résolveur FAI={resolver or '(aucun : --resolver)'} "
          f"| {len(cibles)} hôtes | sortie={ctx['out']}", file=sys.stderr)
    if resolver in ("1.1.1.1", "1.0.0.1", "8.8.8.8", "8.8.4.4", "9.9.9.9"):
        print("ATTENTION : le résolveur système est un DNS public, pas celui du FAI. "
              "Le test DNS ne mesure alors pas le filtrage du FAI.", file=sys.stderr)

    if a.once:
        afficher(un_tour(ctx, cibles))
        return
    while True:
        t0 = time.time()
        try:
            rows = un_tour(ctx, cibles)
            ko = [r["host"] for r in rows if r.get("fail_stage") not in ("aucun", "", None) and r["kind"] != "temoin_pos"]
            print(f"{ctx['round_id']} {len(rows) - 1} hôtes, échecs : {', '.join(ko) or 'aucun'}", file=sys.stderr)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print("tour en erreur :", repr(e), file=sys.stderr)
        # léger aléa (±10 %) pour ne pas se caler sur une horloge ronde
        attente = max(10, a.interval * random.uniform(0.9, 1.1) - (time.time() - t0))
        time.sleep(attente)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\narrêt.", file=sys.stderr)
