# -*- coding: utf-8 -*-
import datetime
import html

# ============================================================
#  TEMPLATE HTML PREMIUM - FARA format(), FARA conflicte CSS
# ============================================================

HTML_SHELL = """
<!DOCTYPE html>
<html lang="ro">
<head>
<meta charset="UTF-8">
<title>Raport Complet Loguri</title>
<style>
:root{
  --bg:#0b1321;
  --card:#0f1a2f;
  --muted:#9aa6b2;
  --line:#1f2b45;
  --info:#3498db;
  --warn:#f1c40f;
  --err:#e67e22;
  --fatal:#e74c3c;
}
*{
  box-sizing:border-box;
}
body{
  margin:0;
  font-family:Arial, Helvetica, sans-serif;
  background:var(--bg);
  color:#e9eef5;
}
.wrapper{
  max-width:1200px;
  margin:0 auto;
  padding:20px;
}
.card{
  background:var(--card);
  padding:20px;
  margin-bottom:20px;
  border-radius:10px;
  border:1px solid var(--line);
}
h1,h2{
  margin:0 0 10px 0;
}
.table{
  width:100%;
  border-collapse:collapse;
  font-size:14px;
}
.table th,.table td{
  border-bottom:1px solid var(--line);
  padding:8px;
}
.bar{
  height:10px;
  background:#14213a;
  border-radius:6px;
  overflow:hidden;
}
.bar span{
  display:block;
  height:100%;
}
.note{
  color:var(--muted);
  font-size:13px;
}
</style>
</head>

<body>
<div class="wrapper">

<h1>Raport complet analiza loguri</h1>
<p>Fisier: <b>{filename}</b></p>
<p>Generat la: {generated_at}</p>
<p>Total linii procesate: {total_lines}</p>

<div class="card">
<h2>Distributie pe niveluri</h2>
{levels_kpis}
{levels_bar}
</div>

<div class="card">
<h2>Top IP-uri</h2>
<table class="table">
<thead><tr><th>#</th><th>IP</th><th>Cereri</th></tr></thead>
<tbody>
{top_ip_rows}
</tbody>
</table>
</div>

<div class="card">
<h2>Spike-uri detectate</h2>
<table class="table">
<thead><tr><th>Tip</th><th>Interval</th><th>Count</th><th>Mesaj</th></tr></thead>
<tbody>
{spike_rows}
</tbody>
</table>
</div>

<div class="card">
<h2>Activitate suspecta</h2>
<table class="table">
<thead><tr><th>Tip</th><th>Interval</th><th>Count</th><th>Mesaj</th></tr></thead>
<tbody>
{suspicious_rows}
</tbody>
</table>
</div>

<div class="card">
<h2>Profilare IP</h2>
<table class="table">
<thead><tr><th>IP</th><th>Total</th><th>Status codes</th><th>Paths</th></tr></thead>
<tbody>
{ip_profiles_rows}
</tbody>
</table>
</div>

<div class="card">
<h2>Recomandari finale</h2>
<ul>
{recommendations}
</ul>
</div>

</div>
</body>
</html>
"""

# ============================================================
#   HELPER FUNCTIONS
# ============================================================

def _fmt(n):
    try:
        return f"{int(n):,}".replace(",", " ")
    except:
        return str(n)

def _levels_kpis(level_counts):
    out = ""
    for lvl, count in level_counts.items():
        out += f"<p>{lvl}: {_fmt(count)}</p>"
    return out

def _levels_bar_graph(level_counts):
    total = sum(level_counts.values()) or 1
    colors = {
        "INFO":"var(--info)",
        "WARN":"var(--warn)",
        "ERROR":"var(--err)",
        "FATAL":"var(--fatal)"
    }
    spans = ""
    for lvl, count in level_counts.items():
        pct = (count / total) * 100
        color = colors.get(lvl, "#95a5a6")
        spans += f'<span style="width:{pct}%; background:{color};"></span>'
    return f'<div class="bar">{spans}</div>'

def _top_ip_rows(data):
    if not data:
        return "<tr><td colspan='3'>Nu exista IP-uri</td></tr>"
    rows = ""
    for i,(ip,count) in enumerate(data,1):
        rows += f"<tr><td>{i}</td><td>{ip}</td><td>{_fmt(count)}</td></tr>"
    return rows

def _spike_rows(spikes):
    if not spikes:
        return "<tr><td colspan='4'>Nu exista spike-uri.</td></tr>"
    rows = ""
    for s in spikes:
        rows += f"<tr><td>{s['type']}</td><td>{s['interval']}</td><td>{s['count']}</td><td>{html.escape(s['message'])}</td></tr>"
    return rows

def _suspicious_rows(events):
    if not events:
        return "<tr><td colspan='4'>Nu exista activitate suspecta.</td></tr>"
    rows = ""
    for e in events:
        rows += f"<tr><td>{e['type']}</td><td>{e['interval']}</td><td>{e['count']}</td><td>{html.escape(e['message'])}</td></tr>"
    return rows

def _ip_profiles_rows(profiles):
    if not profiles:
        return "<tr><td colspan='4'>Nu exista profiluri.</td></tr>"
    rows = ""
    for ip,data in profiles.items():
        sc = ", ".join(f"{k}:{v}" for k,v in data["status_codes"].items())
        paths = ", ".join(data["paths"][:3]) + ("..." if len(data["paths"])>3 else "")
        rows += f"<tr><td>{ip}</td><td>{data['count']}</td><td>{sc}</td><td>{paths}</td></tr>"
    return rows

def _default_rec(level_stats, spikes, suspicious):
    rec = []
    if level_stats.get("ERROR",0) > 0:
        rec.append("Investigati erorile frecvente.")
    if spikes:
        rec.append("Au fost detectate spike-uri de trafic.")
    if suspicious:
        rec.append("Activitate suspecta detectata — posibil atac.")
    if not rec:
        rec.append("Sistem stabil, fara probleme majore.")
    return "\n".join(f"<li>{r}</li>" for r in rec)

# ============================================================
#   GENERAREA RAPORTULUI HTML
# ============================================================

def generate_html_report(
    filename,
    total_lines,
    level_stats,
    top_ips,
    ip_profiles,
    spikes,
    suspicious_events,
    output_path="raport_complet.html"
):
    generated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # convertim datele în HTML
    levels_kpis = _levels_kpis(level_stats)
    levels_bar = _levels_bar_graph(level_stats)
    top_ip_rows = _top_ip_rows(top_ips)
    spike_rows = _spike_rows(spikes)
    suspicious_rows = _suspicious_rows(suspicious_events)
    ip_profiles_rows = _ip_profiles_rows(ip_profiles)
    recommendations = _default_rec(level_stats, spikes, suspicious_events)

    # pornim template-ul
    html_out = HTML_SHELL

    # înlocuim placeholder-ele manual (nu folosim format!)
    html_out = html_out.replace("{filename}", filename)
    html_out = html_out.replace("{generated_at}", generated_at)
    html_out = html_out.replace("{total_lines}", str(total_lines))
    html_out = html_out.replace("{levels_kpis}", levels_kpis)
    html_out = html_out.replace("{levels_bar}", levels_bar)
    html_out = html_out.replace("{top_ip_rows}", top_ip_rows)
    html_out = html_out.replace("{spike_rows}", spike_rows)
    html_out = html_out.replace("{suspicious_rows}", suspicious_rows)
    html_out = html_out.replace("{ip_profiles_rows}", ip_profiles_rows)
    html_out = html_out.replace("{recommendations}", recommendations)

    # salvam
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_out)

    print("\nRaport HTML generat cu succes:", output_path)
