import html

HTML_SHELL = """
<!DOCTYPE html>
<html lang="ro">
<head>
<meta charset="UTF-8">
<title>Raport Log-uri</title>
<style>
body {{
    font-family: Arial, sans-serif;
    background: #f4f4f4;
    margin: 0;
    padding: 20px;
}}

h1, h2, h3 {{
    color: #333;
}}

.container {{
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px #aaa;
    margin-bottom: 30px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}}

th {{
    background: #333;
    color: white;
    padding: 8px;
    text-align: left;
}}

td {{
    padding: 8px;
    border-bottom: 1px solid #ccc;
}}

tr:nth-child(even) {{
    background: #f2f2f2;
}}

.alert {{
    color: red;
    font-weight: bold;
}}
</style>
</head>
<body>

<h1> Raport Analiză Log-uri </h1>

<div class="container">
<h2>Informații generale</h2>
<p><b>Fișier analizat:</b> {filename}</p>
<p><b>Total linii:</b> {total_lines}</p>
</div>

<div class="container">
<h2>Distribuție Niveluri Log</h2>
<table>
<tr><th>Nivel</th><th>Număr</th><th>Procent</th></tr>
{level_rows}
</table>
</div>

<div class="container">
<h2>Top IP-uri</h2>
<table>
<tr><th>IP</th><th>Număr cereri</th></tr>
{top_ip_rows}
</table>
</div>

<div class="container">
<h2>Profilare IP-uri</h2>
<table>
<tr><th>IP</th><th>Total</th><th>Erori</th><th>404</th><th>Rute accesate</th></tr>
{profile_rows}
</table>
</div>

<div class="container">
<h2>Spike-uri detectate</h2>
<table>
<tr><th>Tip</th><th>Interval</th><th>Count</th><th>Mesaj</th></tr>
{spike_rows}
</table>
</div>

<div class="container">
<h2>Activitate suspectă</h2>
<table>
<tr><th>Tip</th><th>IP</th><th>Count</th><th>Interval</th><th>Mesaj</th></tr>
{suspicious_rows}
</table>
</div>

</body>
</html>
"""


# ============================================================
# TABEL NIVELURI
# ============================================================

def _level_rows(level_stats):
    rows = ""
    total = sum(level_stats.values()) if level_stats else 1

    for lvl, count in level_stats.items():
        pct = (count / total) * 100
        rows += f"<tr><td>{lvl}</td><td>{count}</td><td>{pct:.2f}%</td></tr>"

    return rows


# ============================================================
# TABEL TOP IP-uri
# ============================================================

def _top_ip_rows(top_ips):
    rows = ""
    for ip, count in top_ips:
        rows += f"<tr><td>{ip}</td><td>{count}</td></tr>"
    return rows


# ============================================================
# TABEL PROFIL IP
# ============================================================

def _profile_rows(profiles):
    rows = ""

    for ip, data in profiles.items():
        errors = data["levels"].get("ERROR", 0)
        hits_404 = data["status_codes"].get(404, 0)
        paths = ", ".join(data["paths"]) if data["paths"] else "-"

        rows += (
            f"<tr>"
            f"<td>{ip}</td>"
            f"<td>{data['count']}</td>"
            f"<td>{errors}</td>"
            f"<td>{hits_404}</td>"
            f"<td>{paths}</td>"
            f"</tr>"
        )

    return rows


# ============================================================
# TABEL SPIKE-URI (compatibil cu spike_abuse.py NOU)
# ============================================================

def _spike_rows(spikes):
    rows = ""

    for s in spikes:
        interval = s.get("interval", "N/A")
        count = s.get("count", "-")
        msg = html.escape(s.get("message", ""))

        rows += (
            f"<tr>"
            f"<td>{s.get('type', 'Unknown')}</td>"
            f"<td>{interval}</td>"
            f"<td>{count}</td>"
            f"<td>{msg}</td>"
            f"</tr>"
        )

    return rows


# ============================================================
# TABEL ACTIVITATE SUSPECTĂ
# ============================================================

def _suspicious_rows(events):
    rows = ""

    for e in events:
        rows += (
            f"<tr>"
            f"<td>{e.get('type','')}</td>"
            f"<td>{e.get('ip','')}</td>"
            f"<td>{e.get('count','')}</td>"
            f"<td>{e.get('interval','N/A')}</td>"
            f"<td>{html.escape(e.get('message',''))}</td>"
            f"</tr>"
        )

    return rows


# ============================================================
# FUNCTIA PRINCIPALĂ DE GENERARE HTML
# ============================================================

def generate_html_report(
        filename,
        total_lines,
        level_stats,
        top_ips,
        ip_profiles,
        spikes,
        suspicious_events,
        output_path="raport.html"
    ):

    html_out = HTML_SHELL.format(
        filename=filename,
        total_lines=total_lines,
        level_rows=_level_rows(level_stats),
        top_ip_rows=_top_ip_rows(top_ips),
        profile_rows=_profile_rows(ip_profiles),
        spike_rows=_spike_rows(spikes),
        suspicious_rows=_suspicious_rows(suspicious_events)
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_out)

    print(f"Raport HTML generat cu succes: {output_path}")
