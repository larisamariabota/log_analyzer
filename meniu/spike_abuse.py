# spike_abuse.py

from collections import Counter
from grouping.profile_by_ip import profile_by_ip
# (dacă ai alt path pentru profile_by_ip, modifici aici)

# ============================================================
# 1 SPIKE TRAFIC PE IP
# ============================================================

def spike_traffic(profiles, factor=2.5):
    """
    Detectează IP-uri cu trafic anormal de mare.
    profiles = rezultatul din profile_by_ip(entries)
    """
    counts = [p["count"] for p in profiles.values()]
    if not counts:
        return []

    avg = sum(counts) / len(counts)

    spikes = []
    for ip, data in profiles.items():
        if data["count"] >= avg * factor:
            spikes.append({
                "type": "Traffic Spike",
                "ip": ip,
                "count": data["count"],
                "message": f"IP {ip} are {data['count']} cereri → peste media de {avg:.2f} (SPIKE trafic)."
            })

    return spikes


# ============================================================
#  SPIKE DE ERORI (ERROR)
# ============================================================

def spike_errors(profiles, min_errors=10):
    """
    Detectează IP-uri care produc multe ERROR.
    """
    spikes = []

    for ip, data in profiles.items():
        errors = data["levels"].get("ERROR", 0)
        if errors >= min_errors:
            spikes.append({
                "type": "Error Spike",
                "ip": ip,
                "count": errors,
                "message": f"IP {ip} are {errors} erori → posibil atac sau server instabil."
            })

    return spikes


# ============================================================
#  SPIKE 404 (scanare automată)
# ============================================================

def spike_404(profiles, min_404=10):
    """
    Detectează IP-uri cu multe coduri 404 → scanner.
    """
    spikes = []

    for ip, data in profiles.items():
        hits_404 = data["status_codes"].get(404, 0)
        if hits_404 >= min_404:
            spikes.append({
                "type": "404 Spike",
                "ip": ip,
                "count": hits_404,
                "message": f"IP {ip} a generat {hits_404} erori 404 → posibil scanner (brute-scan)."
            })

    return spikes


# ============================================================
# SPIKE ACCES PATH-URI SENSIBILE
# ============================================================

SENSITIVE_PATHS = [
    "/admin", "/admin/login", "/admin/secret",
    "/phpmyadmin", "/config", "/backup", "/setup"
]

def spike_sensitive_paths(profiles, min_hits=3):
    """
    Detectează IP-uri care accesează intens rute sensibile.
    """
    spikes = []

    for ip, data in profiles.items():
        hits = sum(1 for p in data["paths"] if p in SENSITIVE_PATHS)

        if hits >= min_hits:
            spikes.append({
                "type": "Sensitive Path Spike",
                "ip": ip,
                "count": hits,
                "message": f"IP {ip} a accesat {hits} rute sensibile → posibil atac targetat."
            })

    return spikes


# ============================================================
# 5 SPIKE GLOBAL ERORI ÎN TOT LOGUL
# ============================================================

def spike_global_errors(entries, min_errors=20):
    """
    ERROR > (WARN + INFO) * 2 → spike global de erori.
    """
    levels = Counter(e.get("level") for e in entries if e.get("level"))

    errors = levels.get("ERROR", 0)
    warn = levels.get("WARN", 0)
    info = levels.get("INFO", 0)

    if errors >= min_errors and errors > (warn + info) * 2:
        return [{
            "type": "Global Error Spike",
            "count": errors,
            "message": f"Spike global: {errors} erori → sistem afectat."
        }]

    return []


# ============================================================
# 6FUNCTIA FINALĂ: rulează TOATE spike-urile
# ============================================================

def detect_all_spikes(entries):
    """
    Folosește profile_by_ip pentru spike-uri inteligente.
    """

    # Generăm profilul direct aici
    profiles = profile_by_ip(entries)

    spikes = []
    spikes += spike_traffic(profiles)
    spikes += spike_errors(profiles)
    spikes += spike_404(profiles)
    spikes += spike_sensitive_paths(profiles)
    spikes += spike_global_errors(entries)

    return spikes


# ============================================================
# 7️ PRINT REPORT 
# ============================================================

def print_alert_table(spikes):
    if not spikes:
        print("\n✅ SISTEM OK — nu s-au detectat alerte.\n")
        return

    headers = ["TIP", "IP", "COUNT", "DESCRIERE"]

    rows = []
    for s in spikes:
        rows.append([
            s.get("type", "-"),
            s.get("ip", "-"),
            str(s.get("count", "-")),
            s.get("message", "").split("→")[0].strip()[:30]
        ])

    # calcul lățimi coloane
    widths = [len(h) for h in headers]
    for r in rows:
        for i, cell in enumerate(r):
            widths[i] = max(widths[i], len(cell))

    def line(ch="="):
        return "+" + "+".join(ch * (w + 2) for w in widths) + "+"

    def fmt(r):
        return "|" + "|".join(f" {r[i]:<{widths[i]}} " for i in range(len(r))) + "|"

    print("\n🚨 ALERT REPORT — SPIKES DETECTATE")
    print(line("="))
    print(fmt(headers))
    print(line("="))

    for r in rows:
        print(fmt(r))

    print(line("="))
    print()
