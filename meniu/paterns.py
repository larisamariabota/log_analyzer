from collections import defaultdict
from datetime import datetime, timedelta

# -------------------------------------------------------
# DETECTARE BRUTE-FORCE LOGIN
# -------------------------------------------------------

def detect_bruteforce(entries, fail_limit=10, window_minutes=2):
         
         # daca un ip are mai mult de fail_limit incercari esuate de login in window_minutes, acesta este suspect

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

        # detectam incercari esuate de login, punem in dictionarul login_attempts doar ip si timestamp care indeplinesc conditiile
        if method == "POST" and "/login" in path.lower() and status in (401, 403):
            login_attempts[ip].append(ts)

    results = []

    for ip, timestamps in login_attempts.items():
        timestamps = sorted(timestamps) # sortam timpii pentru ai masura cronologic, pt fiecare ip
          
        for i in range(len(timestamps)):
            start = timestamps[i]
            end = start + timedelta(minutes=window_minutes)
            count = sum(1 for t in timestamps if start <= t <= end) # count numacate erori au avut loc in 2 min
            
            if count >= fail_limit: # daca nr de errori a atins limita, il trimitem in result
                results.append({
                    "type": "Brute-force login",
                    "ip": ip,
                    "count": count,
                    "interval": f"{start.strftime('%H:%M:%S')} - {end.strftime('%H:%M:%S')}",
                    "message": f"IP {ip} are {count} incercari de login esuate — posibil BRUTE FORCE."
                })
                break

    return results

def print_bruteforce_reports(results):
    if not results:
        print("In doua minute nu s-a atins limita de zece incercari esuate de login, nu e suspect")
        return
    print("\n ----------In doua minute s-a atins limita de zece incercari de login esuate, e suspect --------\n")
    for r in results:
        print(f"IP:{r['ip']},Interval:{r['interval']},Numar incercari:{r['count']}\n")
        print("Recomandari:")
        print("  -Blocheaza IP-ul")
        print("  -Verifica autentificarile")
        print("-" * 30)

# -------------------------------------------------------
# DETECTARE SPAM 404 (SCANARI)
# -------------------------------------------------------

#eror 404 inseamna ca resursa nu a fost gasita de server
def detect_404_scans(entries, limit_404=10, window_minutes=2):
    errors = defaultdict(list)   # se creaza un nou dictionar cu liste goale

    for entry in entries:
        ip = entry.get("ip")
        ts = entry.get("timestamp")
        status = entry.get("status")

       
        if not ip or not ts or status != 404:
            continue

       
        errors[ip].append(ts)

    result = []

    for ip, timestamps in errors.items():
        timestamps = sorted(timestamps)

        for i in range(len(timestamps)):
            start = timestamps[i]

            end = start + timedelta(minutes=window_minutes)

            count = sum(1 for t in timestamps if start <= t <= end)

            if count >= limit_404:
                result.append({
                    "type": "404 Scan",
                    "ip": ip,
                    "count": count,
                    "interval": f"{start.strftime('%H:%M:%S')} - {end.strftime('%H:%M:%S')}",
                    "message": f"IP {ip} a generat {count} erori 404— posibil scanare automata."
                })
                break

    return result

def print_404_scan_reports(results):
    if not results:
        print(" In doua mintute nu s-a atins limita de zece erori 404, nu e suspect")
        return
    
    for r in results:
        print(r["message"])
        print(f"In intervalul {r['interval']}")
        print("Recomandari:")
        print(" 1. BLOCARE IP: Adăugați IP-ul în lista neagră (ex: iptables -A INPUT -s " + r['ip'] + " -j DROP).")
        print(" 2. RATE LIMITING: Activați modulele de limitare a cererilor (ex: ngx_http_limit_req_module pentru Nginx).")
        print(" 3. ANALIZĂ PATH-URI: Verificați în loguri ce fișiere a căutat (căuta după /.env, /wp-admin sau /.git?).")
        print(" 4. PROTECȚIE CLOUD: Dacă atacul persistă, activați modul 'Under Attack' în Cloudflare sau WAF-ul folosit.")
        print(" 5. HONEYPOT: Creați pagini 'capcană' (ex: /phpmyadmin) care să blocheze automat orice IP care le accesează.")
        print("-" * 30)

# -------------------------------------------------------
# DETECTARE ACCES PATH-URI SENSIBILE
# -------------------------------------------------------

SENSITIVE_PATHS = [
    "/admin", "/admin/login", "/wp-login.php", "/phpmyadmin",
    "/config", "/config.php", "/backup", "/backup.zip",
    "/server-status", "/login/reset", "/login?action=reset"
]
# un path reprezinta calea catre o resursa pe un server web
def detect_sensitive_path_access(entries, limit=5):
    access = defaultdict(int)    # defaultdict este pentru a initializa automat valorile la 0
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

    resul = []

    for ip, count in access.items():
        if count >= limit:
            resul.append({
                "path":path,
                "type": "Sensitive path access",
                "ip": ip,
                "count": count,
                "interval": f"{access_timestamps[ip][0].strftime('%H:%M:%S')} - {access_timestamps[ip][-1].strftime('%H:%M:%S')}",
                "message": f"IP {ip} acceseaza PATH-URI CRITICE ({count} accesari) ."
            })

    return resul


def print_sensitive_path(resul):
    if not resul:
   
      print("S-au detectata acccesuri repetate la path-ri sensibile:")
   
    print("\n--- DETECTARE ACCES PATH-URI SENSIBILE ---")
    for r in resul:
      
        print(f"Tip alerta: {r['type']}")
        print(f"Mesaj: {r['message']}")
        print(f"Interval detectat: {r['interval']}")
        print(f"Numar total incercari: {r['count']}")
        print("Recomandare: Verificati daca IP-ul are drepturi de admin sau trebuie blocat.")
        print("-" * 30)
    

    
