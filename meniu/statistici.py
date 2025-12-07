from datetime import datetime
from collections import Counter

def status(entries):
    print("\nAnaliza generala Log-uri")
    print("=" * 60)

    if not entries:
        print("Nu s-au gasit inregistrari.")
        return

    total = len(entries)
    print(f"Total inregistrari: {total}")

    # ---------------------------------------
    # Perioada analizata
    # ---------------------------------------
    timestamps = [entry.get("timestamp") for entry in entries]
    timestamps = [t for t in timestamps if isinstance(t, datetime)]

    if timestamps:
        start = min(timestamps)
        end = max(timestamps)
        print(f"Perioada analizata: {start} -> {end}")
    else:
        print("Perioada analizata: nu exista timestamp-uri valide.")

    # ---------------------------------------
    # Distributie pe niveluri
    # ---------------------------------------
    levels = Counter(e.get("level") for e in entries if e.get("level"))
    print("Distributie pe niveluri:")
    for lvl, count in levels.items():
        pct = (count / total) * 100
        print(f"  {lvl:<6} : {count} ({pct:.2f}%)")
    print("-" * 60)

    # ---------------------------------------
    # Distributie pe coduri HTTP
    # ---------------------------------------
    http_codes = Counter(e.get("status") for e in entries if e.get("status"))
    print("Distributie pe coduri HTTP:")
    if not http_codes:
        print("  Nu exista coduri HTTP in log.")
    else:
        for code, count in http_codes.items():
            pct = (count / total) * 100
            print(f"  {code}: {count} ({pct:.2f}%)")
    print("-" * 60)

    # ---------------------------------------
    # Distributie metode HTTP
    # ---------------------------------------
    methods = Counter(e.get("method") for e in entries if e.get("method"))
    print("Distributie metode HTTP:")
    if methods:
        for m, count in methods.items():
            pct = (count * 100) / total
            print(f"  {m:<6}: {count} ({pct:.2f}%)")
    else:
        print("  Nu exista metode HTTP in log.")
    print("-" * 60)

    # ---------------------------------------
    # Top rute accesate
    # ---------------------------------------
    paths = Counter(e.get("path") for e in entries if e.get("path"))
    print("Top rute accesate:")
    if paths:
        for path, count in paths.most_common(10):
            pct = (count * 100) / total
            print(f"  {path:<20} {count} ({pct:.2f}%)")
    else:
        print("  Nu exista rute in log.")
    print("-" * 60)

    # ---------------------------------------
    # IP-uri unice
    # ---------------------------------------
    ips = Counter(e.get("ip") for e in entries if e.get("ip"))
    print(f"IP-uri unice: {len(ips)}")

    if ips:
        print("Top 10 IP-uri dupa numar de cereri:")
        for ip, count in ips.most_common(10):
            pct = (count * 100) / total
            print(f"  {ip:<15} {count} cereri ({pct:.2f}%)")
    print("-" * 60)

    # ---------------------------------------
    # Surse log
    # ---------------------------------------
    sources = Counter(e.get("source") for e in entries if e.get("source"))
    print("Distributie pe surse log:")
    if sources:
        for src, count in sources.items():
            pct = (count * 100) / total
            print(f"  {src:<10} {count} ({pct:.2f}%)")
    else:
        print("  Nu exista surse detectate.")
    print("-" * 60)

    # ---------------------------------------
    # Trafic pe ore
    # ---------------------------------------
    hours = Counter(
        e.get("timestamp").hour
        for e in entries
        if isinstance(e.get("timestamp"), datetime)
    )
    print("Trafic pe ore:")
    if hours:
        for hour, count in sorted(hours.items()):
            pct = (count * 100) / total
            print(f"  {hour:02d}:00  {count} inregistrari ({pct:.2f}%)")
    else:
        print("  Nu exista timestamp-uri.")
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


     