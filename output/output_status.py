from collections import Counter
from datetime import datetime

def write_status_to_file(entries, filename="output_comenzi.csv"):
    """
    Scrie în fișier exact analiza generată de status().
    """

    with open(filename, "a", encoding="utf-8") as f:

        f.write("\nAnaliza generala Log-uri\n")
        f.write("=" * 60 + "\n")

        if not entries:
            f.write("Nu s-au gasit inregistrari.\n")
            return

        total = len(entries)
        f.write(f"Total inregistrari: {total}\n")

        # ---------------------------------------
        # Perioada analizata
        # ---------------------------------------
        timestamps = [entry.get("timestamp") for entry in entries]
        timestamps = [t for t in timestamps if isinstance(t, datetime)]

        if timestamps:
            start = min(timestamps)
            end = max(timestamps)
            f.write(f"Perioada analizata: {start} -> {end}\n")
        else:
            f.write("Perioada analizata: nu exista timestamp-uri valide.\n")

        # ---------------------------------------
        # Distributie pe niveluri
        # ---------------------------------------
        levels = Counter(e.get("level") for e in entries if e.get("level"))
        f.write("Distributie pe niveluri:\n")
        for lvl, count in levels.items():
            pct = (count / total) * 100
            f.write(f"  {lvl:<6} : {count} ({pct:.2f}%)\n")
        f.write("-" * 60 + "\n")

        # ---------------------------------------
        # Distributie pe coduri HTTP
        # ---------------------------------------
        http_codes = Counter(e.get("status") for e in entries if e.get("status"))
        f.write("Distributie pe coduri HTTP:\n")
        if not http_codes:
            f.write("  Nu exista coduri HTTP in log.\n")
        else:
            for code, count in http_codes.items():
                pct = (count / total) * 100
                f.write(f"  {code}: {count} ({pct:.2f}%)\n")
        f.write("-" * 60 + "\n")

        # ---------------------------------------
        # Distributie metode HTTP
        # ---------------------------------------
        methods = Counter(e.get("method") for e in entries if e.get("method"))
        f.write("Distributie metode HTTP:\n")
        if methods:
            for m, count in methods.items():
                pct = (count * 100) / total
                f.write(f"  {m:<6}: {count} ({pct:.2f}%)\n")
        else:
            f.write("  Nu exista metode HTTP in log.\n")
        f.write("-" * 60 + "\n")

        # ---------------------------------------
        # Top rute accesate
        # ---------------------------------------
        paths = Counter(e.get("path") for e in entries if e.get("path"))
        f.write("Top rute accesate:\n")
        if paths:
            for path, count in paths.most_common(10):
                pct = (count * 100) / total
                f.write(f"  {path:<20} {count} ({pct:.2f}%)\n")
        else:
            f.write("  Nu exista rute in log.\n")
        f.write("-" * 60 + "\n")

        # ---------------------------------------
        # IP-uri unice
        # ---------------------------------------
        ips = Counter(e.get("ip") for e in entries if e.get("ip"))
        f.write(f"IP-uri unice: {len(ips)}\n")

        if ips:
            f.write("Top 10 IP-uri dupa numar de cereri:\n")
            for ip, count in ips.most_common(10):
                pct = (count * 100) / total
                f.write(f"  {ip:<15} {count} cereri ({pct:.2f}%)\n")
        f.write("-" * 60 + "\n")

        # ---------------------------------------
        # Surse log
        # ---------------------------------------
        sources = Counter(e.get("source") for e in entries if e.get("source"))
        f.write("Distributie pe surse log:\n")
        if sources:
            for src, count in sources.items():
                pct = (count * 100) / total
                f.write(f"  {src:<10} {count} ({pct:.2f}%)\n")
        else:
            f.write("  Nu exista surse detectate.\n")
        f.write("-" * 60 + "\n")

        # ---------------------------------------
        # Trafic pe ore
        # ---------------------------------------
        hours = Counter(
            e.get("timestamp").hour
            for e in entries
            if isinstance(e.get("timestamp"), datetime)
        )
        f.write("Trafic pe ore:\n")
        if hours:
            for hour, count in sorted(hours.items()):
                pct = (count * 100) / total
                f.write(f"  {hour:02d}:00  {count} inregistrari ({pct:.2f}%)\n")
        else:
            f.write("  Nu exista timestamp-uri.\n")

        f.write("=" * 60 + "\n\n")

