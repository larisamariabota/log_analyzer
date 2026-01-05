def write_alert_table_to_file(spikes, filename="output_comenzi.csv"):
    """
    Scrie în fișier exact tabelul ASCII generat de print_alert_table(spikes).
    """

    with open(filename, "a", encoding="utf-8") as f:

        if not spikes:
            f.write("\n✅ SISTEM OK — nu s-au detectat alerte.\n\n")
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

        f.write("\n🚨 ALERT REPORT — SPIKES DETECTATE\n")
        f.write(line("=") + "\n")
        f.write(fmt(headers) + "\n")
        f.write(line("=") + "\n")

        for r in rows:
            f.write(fmt(r) + "\n")

        f.write(line("=") + "\n\n")
