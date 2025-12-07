from collections import defaultdict
from datetime import datetime, timedelta

# -------------------------------------------------------
# DETECTARE BRUTE-FORCE LOGIN
# -------------------------------------------------------

def detect_bruteforce(entries, fail_limit=10, window_minutes=2):
    login_attempts = defaultdict(list)  # ip -> lista timestamps

    for entry in entries:
        ip = entry.get("ip")
        method = entry.get("method")
        status = entry.get("status")
        path = entry.get("path")
        ts = entry.get("timestamp")

        if not ip or not ts:
            continue

        # Verificam path-ul (poate fi None)
        if not isinstance(path, str):
            continue

        # detectam incercari esuate de login
        if method == "POST" and "/login" in path.lower() and status in (401, 403):
            login_attempts[ip].append(ts)

    results = []

    for ip, timestamps in login_attempts.items():
        timestamps = sorted(timestamps)

        for i in range(len(timestamps)):
            start = timestamps[i]
            end = start + timedelta(minutes=window_minutes)
            count = sum(1 for t in timestamps if start <= t <= end)

            if count >= fail_limit:
                results.append({
                    "type": "Brute-force login",
                    "ip": ip,
                    "count": count,
                    "interval": f"{start.strftime('%H:%M:%S')} - {end.strftime('%H:%M:%S')}",
                    "message": f"IP {ip} are {count} incercari de login esuate — posibil BRUTE FORCE."
                })
                break

    return results


# -------------------------------------------------------
# DETECTARE SPAM 404 (SCANARI)
# -------------------------------------------------------

def detect_404_scans(entries, limit_404=30, window_minutes=2):
    errors = defaultdict(list)

    for entry in entries:
        ip = entry.get("ip")
        ts = entry.get("timestamp")
        status = entry.get("status")

        # verificam timestamp-ul
        if not ip or not ts or status != 404:
            continue

        # convertim la datetime dacă este string
        if isinstance(ts, str):
            try:
                ts = datetime.fromisoformat(ts)
            except:
                continue

        errors[ip].append(ts)

    results = []

    for ip, timestamps in errors.items():
        timestamps = sorted(timestamps)

        for i in range(len(timestamps)):
            start = timestamps[i]

            if isinstance(start, str):
                try:
                    start = datetime.fromisoformat(start)
                except:
                    continue

            end = start + timedelta(minutes=window_minutes)

            count = sum(1 for t in timestamps if start <= t <= end)

            if count >= limit_404:
                results.append({
                    "type": "404 Scan",
                    "ip": ip,
                    "count": count,
                    "interval": f"{start.strftime('%H:%M:%S')} - {end.strftime('%H:%M:%S')}",
                    "message": f"IP {ip} a generat {count} erori 404 — posibil scanare automata."
                })
                break

    return results



# -------------------------------------------------------
# DETECTARE ACCES PATH-URI SENSIBILE
# -------------------------------------------------------

SENSITIVE_PATHS = [
    "/admin", "/admin/login", "/wp-login.php", "/phpmyadmin",
    "/config", "/config.php", "/backup", "/backup.zip",
    "/server-status", "/login/reset", "/login?action=reset"
]

def detect_sensitive_path_access(entries, limit=5):
    access = defaultdict(int)
    access_timestamps = defaultdict(list)

    for entry in entries:
        ip = entry.get("ip")
        path = entry.get("path")
        ts = entry.get("timestamp")

        if not ip or not ts:
            continue

        # Path poate fi None → trebuie verificat
        if not isinstance(path, str):
            continue

        p = path.lower()

        if any(s in p for s in SENSITIVE_PATHS):
            access[ip] += 1
            access_timestamps[ip].append(ts)

    results = []

    for ip, count in access.items():
        if count >= limit:
            results.append({
                "type": "Sensitive path access",
                "ip": ip,
                "count": count,
                "interval": f"{access_timestamps[ip][0].strftime('%H:%M:%S')} - {access_timestamps[ip][-1].strftime('%H:%M:%S')}",
                "message": f"IP {ip} acceseaza PATH-URI CRITICE ({count} accesari) — posibil atacator."
            })

    return results


# -------------------------------------------------------
# PRINT REPORT
# -------------------------------------------------------

def print_suspicious_report(results):
    if not results:
        print("Nu s-au detectat pattern-uri suspecte.")
        return

    print("\n=========== SUSPICIOUS ACTIVITY REPORT ===========\n")

    for r in results:
        print("--------------------------------------")
        print(r["message"])
        print(f"Tip: {r['type']}")
        print(f"Interval: {r['interval']}")
        print(f"Numar cereri: {r['count']}")
        print("\nRecomandari:")
        print(" - Blocheaza IP-ul")
        print(" - Aplica rate-limit")
        print(" - Verifica autentificarile si endpoint-urile")
        print(" - Logheaza cererile suspecte")
        print(" - Notifica administratorul")
        print("--------------------------------------\n")

