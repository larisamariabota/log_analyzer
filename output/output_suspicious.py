def write_bruteforce_reports_to_file(results, filename="output_comenzi.csv"):
    with open(filename, "a", encoding="utf-8") as f:
        if not results:
            f.write("In doua minute nu s-a atins limita de zece incercari esuate de login, nu e suspect\n")
            f.write("-" * 30 + "\n")
            return

        f.write("\n---------- In doua minute s-a atins limita de zece incercari de login esuate, e suspect ----------\n\n")
        for r in results:
            f.write(f"IP:{r['ip']}, Interval:{r['interval']}, Numar incercari:{r['count']}\n")
            f.write("Recomandari:\n")
            f.write("  - Blocheaza IP-ul\n")
            f.write("  - Verifica autentificarile\n")
            f.write("-" * 30 + "\n")


def write_404_scan_reports_to_file(results, filename="output_comenzi.csv"):
    with open(filename, "a", encoding="utf-8") as f:
        if not results:
            f.write("In doua mintute nu s-a atins limita de zece erori 404, nu e suspect\n")
            f.write("-" * 30 + "\n")
            return

        for r in results:
            f.write(r["message"] + "\n")
            f.write(f"In intervalul {r['interval']}\n")
            f.write("Recomandari:\n")
            f.write(f" 1. BLOCARE IP: Adăugați IP-ul în lista neagră (ex: iptables -A INPUT -s {r['ip']} -j DROP).\n")
            f.write(" 2. RATE LIMITING: Activați modulele de limitare a cererilor (ex: ngx_http_limit_req_module pentru Nginx).\n")
            f.write(" 3. ANALIZĂ PATH-URI: Verificați în loguri ce fișiere a căutat (/.env, /wp-admin, /.git?).\n")
            f.write(" 4. PROTECȚIE CLOUD: Dacă atacul persistă, activați modul 'Under Attack' în Cloudflare/WAF.\n")
            f.write(" 5. HONEYPOT: Creați pagini capcană (ex: /phpmyadmin) care blochează automat IP-ul.\n")
            f.write("-" * 30 + "\n")


def write_sensitive_path_to_file(resul, filename="output_comenzi.csv"):
    with open(filename, "a", encoding="utf-8") as f:
        if not resul:
            # aici la tine mesajul e cam invers în print (spune “s-au detectat” când nu există)
            # îl fac logic pentru fișier:
            f.write("Nu s-au detectat accesuri repetate la path-uri sensibile.\n")
            f.write("-" * 30 + "\n")
            return

        f.write("\n--- DETECTARE ACCES PATH-URI SENSIBILE ---\n")
        for r in resul:
            f.write(f"Tip alerta: {r.get('type','-')}\n")
            f.write(f"Mesaj: {r.get('message','-')}\n")
            f.write(f"Interval detectat: {r.get('interval','-')}\n")
            f.write(f"Numar total incercari: {r.get('count','-')}\n")
            f.write("Recomandare: Verificati daca IP-ul are drepturi de admin sau trebuie blocat.\n")
            f.write("-" * 30 + "\n")
