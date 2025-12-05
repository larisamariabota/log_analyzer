from datetime import datetime
from collections import Counter, defaultdict

def status(entries):
    print("\n📊 Analiză generală Log-uri")
    print("=" * 60)

    if not entries:
        print("Nu s-au găsit înregistrări.")
        return

    total = len(entries)
    print(f"Total înregistrări: {total}")

    # ---------------------------------------
    # Perioada analizată
    # ---------------------------------------
    timestamps = [e.get("timestamp") for e in entries if e.get("timestamp")]
    if timestamps:
        print(f"Perioada analizată: {min(timestamps)} → {max(timestamps)}")
    print("-" * 60)

    # ---------------------------------------
    # Distribuție pe niveluri (INFO, ERROR…)
    # ---------------------------------------
    levels = Counter(e.get("level") for e in entries if e.get("level"))
    print("📌 Distribuție pe niveluri:")
    for lvl, count in levels.items():
        pct = (count / total) * 100
        print(f"  {lvl:<6} : {count} ({pct:.2f}%)")
    print("-" * 60)

    # ---------------------------------------
    # Distribuție pe coduri HTTP
    # ---------------------------------------
    http_codes = Counter(e.get("status") for e in entries if e.get("status"))
    print("🌐 Distribuție pe coduri HTTP:")
    if not http_codes:
        print("  Nu există coduri HTTP în log.")
    else:
        for code, count in http_codes.items():
            pct = (count / total) * 100
            print(f"  {code}: {count} ({pct:.2f}%)")
    print("-" * 60)

    # ---------------------------------------
    # Distribuție metode HTTP
    # ---------------------------------------
    methods = Counter(e.get("method") for e in entries if e.get("method"))
    print("🔧 Distribuție metode HTTP:")
    if methods:
        for m, count in methods.items():
            pct = count * 100 / total
            print(f"  {m:<6}: {count} ({pct:.2f}%)")
    else:
        print("  Nu există metode HTTP în log.")
    print("-" * 60)

    # ---------------------------------------
    # Rute accesate (TOP 10 endpoints)
    # ---------------------------------------
    paths = Counter(e.get("path") for e in entries if e.get("path"))
    print("📍 Top rute accesate:")
    if paths:
        for path, count in paths.most_common(10):
            pct = count * 100 / total
            print(f"  {path:<20} {count} ({pct:.2f}%)")
    else:
        print("  Nu există rute în log.")
    print("-" * 60)

    # ---------------------------------------
    # IP-uri unice + primele 10
    # ---------------------------------------
    ips = Counter(e.get("ip") for e in entries if e.get("ip"))
    print(f"🧿 IP-uri unice: {len(ips)}")

    if ips:
        print("Top 10 IP-uri după număr de cereri:")
        for ip, count in ips.most_common(10):
            pct = count * 100 / total
            print(f"  {ip:<15} {count} cereri ({pct:.2f}%)")
    print("-" * 60)

    # ---------------------------------------
    # Distribuție pe surse (apache/nginx/syslog…)
    # ---------------------------------------
    sources = Counter(e.get("source") for e in entries if e.get("source"))
    print("📡 Distribuție pe surse log:")
    if sources:
        for src, count in sources.items():
            pct = count * 100 / total
            print(f"  {src:<10} {count} ({pct:.2f}%)")
    else:
        print("  Nu există surse detectate.")
    print("-" * 60)

    # ---------------------------------------
    # Trafic pe ore (câte loguri pe fiecare oră)
    # ---------------------------------------
    hours = Counter(e.get("timestamp").hour for e in entries if e.get("timestamp"))
    print("⏰ Trafic pe ore:")
    if hours:
        for hour, count in sorted(hours.items()):
            pct = count * 100 / total
            print(f"  {hour:02d}:00  {count} înregistrări ({pct:.2f}%)")
    else:
        print("  Nu există timestamp-uri.")
    print("=" * 60)

    return {
        "total": total,
        "levels": levels,
        "http_codes": http_codes,
        "methods": methods,
        "paths": paths,
        "ips": ips,
        "sources": sources,
        "hours": hours,
    }

     