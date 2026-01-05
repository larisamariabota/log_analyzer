def write_filter_to_file(entries, limit=30, filename="output_comenzi.csv"):
    """
    Scrie în fișier rezultatele filtrării, cu același format ca în terminal.
    """

    with open(filename, "w", encoding="utf-8") as f:

        if not entries:
            f.write("Nu există rezultate după filtrare.\n")
            return

        f.write(f"Rezultate după filtrare: {len(entries)} înregistrări\n")
        f.write("-" * 80 + "\n")

        shown = 0
        for e in entries:
            ts = e.get("timestamp_dt") or e.get("timestamp") or "-"
            ip = e.get("ip", "-")
            lvl = e.get("level", "-")
            status = e.get("status", "-")
            path = e.get("path", "-")
            msg = e.get("message", "-")

            ts = str(ts)
            ip = str(ip)
            lvl = str(lvl)
            status = "-" if status is None else str(status)
            msg = str(msg)

            f.write(
                f"[{ts}] {lvl:<5} {status:<3} "
                f"IP={ip:<15} PATH={path} MSG={msg}\n"
            )

            shown += 1
            if shown >= limit:
                break

        if len(entries) > limit:
            f.write(f"... și încă {len(entries) - limit} rezultate\n")

        f.write("-" * 80 + "\n")
