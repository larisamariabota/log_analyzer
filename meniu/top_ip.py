def top_ip(entries):
    ip_count = {}

    # numărăm cererile per IP
    for entry in entries:
        ip = entry.get("ip")
        if ip:
            ip_count[ip] = ip_count.get(ip, 0) + 1

    # sortăm descrescător după cereri
    sorted_ips = sorted(ip_count.items(), key=lambda x: x[1], reverse=True)
    top_10 = sorted_ips[:10]
        # === GRAFIC ASCII: Top 10 IP-uri (după cereri) ===
    rows = []
    for ip, count in top_10:
        rows.append({
            "ip": ip,
            "requests": count
        })

    print_ascii_bars(
        rows,
        "GRAFIC — Top 10 IP-uri după numărul de cereri",
        key="requests"
    )

    total_logs = len(entries)

    print("Top 10 IP-uri după numărul de cereri\n" + "="*45)

    for i, (ip, count) in enumerate(top_10, start=1):
        pct = (count / total_logs * 100) if total_logs else 0

        # clasificare simplă
        if count > 1000:
            status = "Trafic EXCESIV (posibil BOT)"
        elif count > 200:
            status = "Trafic ridicat"
        else:
            status = "Normal"

        print(f"{i}. {ip}")
        print(f" • {count} cereri totale")
        print(f" • {pct:.2f}% din traficul total")
        print(f" Status: {status}\n")

    return top_10


# top 10 ip periculoase
def top_dangerous_ip(entries):
    stats = {}

    # colectăm informațiile
    for entry in entries:
        ip = entry.get("ip")
        if not ip:
            continue

        msg = entry.get("message", "").lower()
        level = entry.get("level", "")
        ts = entry.get("timestamp_dt")   # TIMPUL NORMALIZAT
        
        if ip not in stats:
            stats[ip] = {
                "score": 0,
                "errors": 0,
                "404": 0,
                "admin_scans": 0,
                "failed_login": 0,
                "total_requests": 0,
                "last_seen": None  
            }

        stats[ip]["total_requests"] += 1

        # salvăm cel mai recent timestamp
        if ts:
            if stats[ip]["last_seen"] is None or ts > stats[ip]["last_seen"]:
                stats[ip]["last_seen"] = ts

        # ERROR / WARN cresc riscul
        if level in ("ERROR", "WARN"):
            stats[ip]["errors"] += 1
            stats[ip]["score"] += 1

        # detectare 404
        if "404" in msg:
            stats[ip]["404"] += 1
            stats[ip]["score"] += 1

        # detectare acces /admin
        if "/admin" in msg:
            stats[ip]["admin_scans"] += 1
            stats[ip]["score"] += 2

        # detectare brute force
        if "failed login" in msg:
            stats[ip]["failed_login"] += 1
            stats[ip]["score"] += 2

    # sortare după scor
    sorted_ips = sorted(stats.items(), key=lambda x: x[1]["score"], reverse=True)
    top_10 = sorted_ips[:10]
        # === GRAFIC ASCII: TOP 10 IP-uri periculoase (după scor) ===
    rows = []
    for ip, data in top_10:
        rows.append({"ip": ip, "score": data["score"]})

    print_ascii_bars(rows, "GRAFIC — Top 10 IP-uri periculoase (scor risc)", key="score")

    print(" Datele despre aceste IP-uri\n" + "="*40)

    for i, (ip, data) in enumerate(top_10, start=1):

        total = data["total_requests"]
        pct_404 = (data["404"] / total * 100) if total else 0

        # FORMATĂM TIMPUL PENTRU AFIȘARE
        if data["last_seen"]:
            last_seen_str = data["last_seen"].strftime("%Y-%m-%d %H:%M:%S")
        else:
            last_seen_str = "-"

        print(f"{i}. {ip} ({total} cereri)")
        
        if data['404'] > 0:
            print(f" • {data['404']} erori 404 ({pct_404:.1f}%)")

        if data['admin_scans'] > 0:
            print(f" • {data['admin_scans']} încercări /admin (scanare)")

        if data['failed_login'] > 0:
            print(f" • {data['failed_login']} failed login (brute force)")

        if data['errors'] > 0:
            print(f" • {data['errors']} mesaje ERROR/WARN")

        print(f" • Ultima activitate: {last_seen_str}")

        # recomandare status
        if data["score"] >= 10:
            status = "BLOCAT imediat"
        elif data["score"] >= 5:
            status = "ALERTĂ RIDICATĂ"
        else:
            status = "Monitorizare"

        print(f" Status: {status}\n")

    return top_10
# functiile care deseanaza grasfice ascii
 #  functia _bar returneaza un string cu bare pt 
def _bar(value, max_value, width=24, ch="█"):
    if max_value <= 0:
        return ""
    n = int((value / max_value) * width)
    return ch * n

def print_ascii_bars(rows, title, key="score", width=28):
    max_v = max(r.get(key, 0) for r in rows) if rows else 0  # max_v este  valoarea maxima pt fiecare ip 
    print("\n" + title)
    print("-" * 60)
    for r in rows:
        ip = r.get("ip", "-")
        v = r.get(key, 0)
        print(f"{ip:<15} | {_bar(v, max_v, width=width):<{width}} {v} \n")
    print("-" * 60 + "\n")
