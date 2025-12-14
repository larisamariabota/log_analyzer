

import html


# ============================================================
#               HTML_SHELL PREMIUM (ESCAPAT)
# ============================================================

HTML_SHELL = r"""<!doctype html>
<html lang="ro">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Raport log — {filename}</title>
  <style>

    :root{{
      --bg:#0b1220;
      --card:#0f172aee;
      --muted:#9aa4b2;
      --text:#e6e9ee;
      --line:#1e293b;
      --accent:#f5c542;
      --accent-2:#7c3aed;

      --danger:#ff4d4d;
      --danger-bg:#3b0f0f66;

      --row-alt:#151d33;
      --row-hover:#1e2a4d;
    }}
    *{{box-sizing:border-box}}
    html,body{{
      margin:0;padding:0;background:
        radial-gradient(1200px 800px at 20% 0%,#101a33,transparent),
        radial-gradient(900px 600px at 90% 10%,#121b38,transparent),
        var(--bg);
      color:var(--text);
      font:500 15px/1.6 Inter, ui-sans-serif;
    }}
    a{{color:inherit}}
    .container{{max-width:1200px;margin:40px auto;padding:0 20px}}
      

    .hero{{
      position:relative;
      border-radius:20px;
      background:
        linear-gradient(135deg, rgba(245,197,66,.12), transparent 40%),
        linear-gradient(180deg, rgba(124,58,237,.10), transparent 60%),
        var(--card);
      border:1px solid rgba(245,197,66,.20);
      box-shadow:0 10px 30px rgba(0,0,0,.35);
      padding:28px 28px 24px;
    }}

    .title{{display:flex; gap:14px; align-items:center; flex-wrap:wrap}}
    .title h1{{margin:0; font-weight:800; font-size:28px}}
    .pill{{
      padding:6px 12px;
      border:1px solid rgba(245,197,66,.32);
      border-radius:999px;
    

      background:linear-gradient(180deg, rgba(245,197,66,.18), rgba(245,197,66,.08));
      color:#ffe7a3;
      font-size:12px; font-weight:700;
    }}

    .grid{{display:grid; grid-template-columns:repeat(12,1fr); gap:18px; margin-top:24px}}

    .card{{
      grid-column:span 12;
      background:var(--card);
      border-radius:16px;
      border:1px solid rgba(245,197,66,.15);
      box-shadow:0 10px 30px rgba(0,0,0,.35);
      overflow:hidden;
    }}

    .card .head{{
      padding:18px 18px 12px;
      border-bottom:1px solid var(--line);
      background:linear-gradient(90deg, rgba(124,58,237,.15), rgba(245,197,66,.12));
    }}

    .card .head h2{{
      margin:0; font-size:17px; letter-spacing:.3px; font-weight:700;
    }}

    .card .body{{padding:12px 18px 18px}}

    .table-wrap{{overflow:auto; border-radius:12px; border:1px solid var(--line);}}
    table{{width:100%; border-collapse:separate; border-spacing:0}}

    thead th{{
      background:linear-gradient(90deg, rgba(124,58,237,.85), rgba(245,197,66,.55));
      color:white;
      padding:12px 14px;
      border-bottom:1px solid rgba(255,255,255,.15);
      white-space:nowrap;
      cursor:pointer;
      text-shadow:0 1px 3px rgba(0,0,0,.5);
    }}

    tbody td{{
      padding:12px 14px;
      border-bottom:1px solid rgba(255,255,255,.06);
    }}

    tbody tr:nth-child(even){{background:var(--row-alt)}}
    tbody tr:hover{{background:var(--row-hover)}}

    /* IP periculos */
    td.ip-danger{{color:var(--danger); font-weight:700}}
    tr.danger-row{{background:var(--danger-bg) !important}}

    @media(min-width:860px){{
      .col-6{{grid-column:span 6}}
      .col-12{{grid-column:span 12}}
    }}

    .gold{{color:var(--accent)}}
    .footer{{margin:26px 0 50px; text-align:center; color:var(--muted)}}
  </style>
</head>

<body>
  <div class="container">
    <section class="hero">
      <div class="title">
        <span class="pill">Security • Report</span>
        <h1>Raport log pentru <span class="gold">{filename}</span></h1>
      </div>
      <div class="meta">
        <div>Total linii: <b>{total_lines}</b></div>
        <div>Generat la: <b><script>document.write(new Date().toLocaleString())</script></b></div>
      </div>
    </section>

    <div class="grid">

      <!-- NIVELURI -->
      <section class="card col-6">
        <div class="head"><h2>Distribuție pe niveluri</h2></div>
        <div class="body">
          <div class="table-wrap">
            <table data-table="levels">
              <thead><tr>
                <th data-sort="text">Nivel</th>
                <th data-sort="num">Count</th>
                <th data-sort="num">Procent</th>
              </tr></thead>
              <tbody>{level_rows}</tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- TOP IP -->
      <section class="card col-6">
        <div class="head"><h2>Top IP-uri</h2></div>
        <div class="body">
          <div class="table-wrap">
            <table data-table="top">
              <thead><tr>
                <th data-sort="text">IP</th>
                <th data-sort="num">CererI</th>
                <th data-sort="num">Procent</th>
              </tr></thead>
              <tbody>{top_ip_rows}</tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- IP PERICULOASE -->
      <section class="card col-12">
        <div class="head"><h2 class="gold">Top IP-uri Periculoase</h2></div>
        <div class="body">
          <div class="table-wrap">
            <table data-table="dangerous">
              <thead><tr>
                <th data-sort="text">IP</th>
                <th data-sort="num">Atacuri</th>
                <th data-sort="text">Tipuri</th>
                <th data-sort="text">Ultima</th>
                <th data-sort="num">Scor risc</th>
              </tr></thead>
              <tbody>{dangerous_rows}</tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- DEFECTIUNI IN SISTEM-->
      <section class="card col-12">
        <div class="head"><h2>Posibile defectiuni in sistem</h2></div>
        <div class="body">
          <div class="table-wrap">
            <table data-table="sus">
              <thead><tr>
                <th data-sort="text">Timestamp</th>
                <th data-sort="text">IP</th>
                <th data-sort="text">Method</th>
                <th data-sort="text">Path</th>
                <th data-sort="num">Status</th>
                <th data-sort="text">Mesaj</th>
                <th data-sort="text">Sursă</th>
              </tr></thead>
             <tbody>{defect_rows}</tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- PROFILURI IP -->
      <section class="card col-12">
        <div class="head"><h2>Profiluri IP (hours • method • path • status)</h2></div>
        <div class="body">
          {profile_rows}
        </div>
      </section>

             <!-- SPIKES -->
      <section class="card col-12">
        <div class="head"><h2>Spike-uri detectate</h2></div>
        <div class="body">
          <div class="table-wrap">
            <table data-table="spikes">
              <thead><tr>
                <th data-sort="text">Interval/Ora</th>
                <th data-sort="text">Nivel</th>
                <th data-sort="num">Count</th>
                <th data-sort="text">Tip spike</th>
              </tr></thead>
             <tbody>
               {spike_rows}
                 </tbody>

            </table>
          </div>
        </div>
      </section>

      <!-- RECOMANDĂRI FINALE -->
      <section class="card col-12">
        <div class="head">
          <h2 class="gold">Recomandări Finale de Securitate</h2>
        </div>
        <div class="body">
          <ul style="line-height:1.8; padding-left:20px; margin:0; color:#eaeaea; list-style:disc;">
            <li><b>Spike-uri de trafic/erori:</b> Verifică logurile de load, monitorizează CPU/RAM și implementează alerte automate.</li>
            <li><b>Recomandare generală:</b> Activează log rotation, verifică versiunile serviciilor și implementează backup automat.</li>
          </ul>
        </div>
      </section>

    </div> <!-- end grid -->

    <div class="footer">
      <span class="gold">©</span> Raport generat automat • Bota Maria Larisa
    </div>
</div>"""
# END HTML_SHELL


import html
from datetime import timedelta


# ============================================================
#                DISTRIBUȚIE PE NIVELURI
# ============================================================

def _level_rows(level_stats):
    rows = ""
    total = sum(level_stats.values()) if level_stats else 1
    for lvl, count in (level_stats or {}).items():
        pct = (count / total) * 100
        rows += f"<tr><td>{html.escape(str(lvl))}</td><td>{count}</td><td>{pct:.2f}%</td></tr>"
    return rows


# ============================================================
#                     TOP IP
# ============================================================

def _top_ip_rows(top_ips, total=None):
    rows = ""
    total = total or sum(c for _, c in top_ips) or 1
    for ip, count in (top_ips or []):
        pct = (count / total) * 100
        rows += (
            f"<tr>"
            f"<td>{html.escape(str(ip))}</td>"
            f"<td>{count}</td>"
            f"<td>{pct:.2f}%</td>"
            f"</tr>"
        )
    return rows


# ============================================================
#              IP-uri PERICULOASE
# ============================================================

def _dangerous_rows(dangerous_list):
    if not dangerous_list:
        return "<tr><td colspan='5'>Niciun IP periculos</td></tr>"

    rows = ""
    for ip, data in dangerous_list:

        ip = html.escape(str(ip))
        total = data.get("total_requests", 0)
        errors = data.get("errors", 0)
        scans = data.get("admin_scans", 0)
        failed = data.get("failed_login", 0)
        risk = data.get("score", 0)

        types_str = f"ERR:{errors} • ADMIN:{scans} • FAIL:{failed}"

        last = "-"
        if data.get("last_seen"):
            try:
                last = data["last_seen"].strftime("%Y-%m-%d %H:%M:%S")
            except:
                last = str(data["last_seen"])

        rows += (
            f"<tr class='danger-row'>"
            f"<td class='ip-danger'>{ip}</td>"
            f"<td>{total}</td>"
            f"<td>{types_str}</td>"
            f"<td>{last}</td>"
            f"<td>{risk}</td>"
            f"</tr>"
        )

    return rows


# ============================================================
#            DEFEȚIUNI SISTEM — RÂNDURI HTML
# ============================================================

def _defect_rows(events):
    if not events:
        return "<tr><td colspan='7'>Nicio defecțiune sistem detectată</td></tr>"
   # aici doar trranspunem lista din dectiuni.py, randuri HTML
    rows = ""
    for e in events:
        rows += (
            f"<tr class='danger-row'>"
            f"<td>{html.escape(str(e.get('timestamp','-')))}</td>"
            f"<td>{html.escape(str(e.get('ip','-')))}</td>"
            f"<td>{html.escape(str(e.get('method','-')))}</td>"
            f"<td>{html.escape(str(e.get('path','-')))}</td>"
            f"<td>{html.escape(str(e.get('status','-')))}</td>"
            f"<td>{html.escape(str(e.get('message','-')))}</td>"
            f"<td>{html.escape(str(e.get('source','-')))}</td>"
            f"</tr>"
        )
    return rows



# ============================================================
#                       PROFILE IP
# ============================================================

def _group_table(mapping, headers):
    if not mapping:
        return "<p><i>Date indisponibile</i></p>"

    h1, h2 = headers
    html_out = [
        f"<div class='table-wrap'><table><thead><tr>"
        f"<th>{html.escape(h1)}</th><th>{html.escape(h2)}</th>"
        f"</tr></thead><tbody>"
    ]

    for k, v in mapping.items():
        html_out.append(f"<tr><td>{html.escape(str(k))}</td><td>{html.escape(str(v))}</td></tr>")

    html_out.append("</tbody></table></div>")
    return "".join(html_out)


def _profile_rows(ip_profiles):
    if not ip_profiles:
        return "<p><i>Nu există profiluri</i></p>"

    chunks = []
    for ip, data in ip_profiles.items():
        ip_h = html.escape(str(ip))
        cnt = data.get("count", 0)
        errors = (data.get("levels") or {}).get("ERROR", 0)
        hits_404 = (data.get("status_codes") or {}).get(404, 0)
        paths = ", ".join(map(str, data.get("paths") or [])) or "-"

        card = (
            f"<h3 style='margin-top:20px'>{ip_h}</h3>"
            f"<p>Total: <b>{cnt}</b> • ERROR: <b>{errors}</b> • 404: <b>{hits_404}</b></p>"
            f"<p style='color:#d9dde6'>Rute: {html.escape(paths)}</p>"
        )

        parts = []
        chunks.append(card + "".join(parts))

    return "".join(chunks)


# ============================================================
#                   SPIKE-URI
# ============================================================

def spike_rows(spikes):
    if not spikes:
        return "<tr><td colspan='4'>Niciun spike detectat</td></tr>"

    rows = ""
    for s in spikes:
        interval = s.get("interval", "N/A")
        count = s.get("count", "-")
        msg = html.escape(s.get("message", ""))

        rows += (
            f"<tr>"
            f"<td>{html.escape(str(interval))}</td>"
            f"<td>{html.escape(str(s.get('type','Unknown')))}</td>"
            f"<td>{html.escape(str(count))}</td>"
            f"<td>{msg}</td>"
            f"</tr>"
        )
    return rows


# ============================================================
#                   RECOMANDĂRI
# ============================================================

def _generate_recommendations(dangerous, spikes, defect):
    rec = []

    if dangerous:
        rec.append("<li><b>IP-uri periculoase detectate:</b> Recomand blocare firewall.</li>")

    if defect:
        rec.append("<li><b>Defecțiuni sistem:</b> Recomand analiză server + monitorizare resurse.</li>")

    if spikes:
        rec.append("<li><b>Spike-uri de trafic:</b> Posibil DoS sau overload.</li>")

    rec.append("<li><b>General:</b> Activează log rotation + backup.</li>")

    return "\n".join(rec) #Convertește lista într-un singur text HTML concatenat cu newline.


# ============================================================
#                GENERARE RAPORT FINAL
# ============================================================
# generam variabilele pentru HTML_SHELL pe care le commpletam cu date reale, si le folosim in fnctiile pentru generare raport
def generate_html_report(
        filename,
        total_lines,
        level_stats,
        top_ips,
        ip_profiles,
        spikes,
        
        output_path="raport.html",
        *,
        top_dangerous_ip=None,
        defect=None
    ):

    top_dangerous_ip = top_dangerous_ip or []
    defect = defect or []           # ← LISTA REALĂ de defecțiuni
   
    #HTML_SHELL este sablonul principal, completat cu datele reale, 
    # aceste variabile merg in interiorul codului HTML si se actualizeaza in timp real
     
    html_out = HTML_SHELL.format(
        filename=filename,
        total_lines=total_lines,
        level_rows=_level_rows(level_stats or {}),
        top_ip_rows=_top_ip_rows(top_ips or [], total_lines),
        dangerous_rows=_dangerous_rows(top_dangerous_ip),
        profile_rows=_profile_rows(ip_profiles or {}),
        spike_rows=spike_rows(spikes or []),

        recommendations=_generate_recommendations(top_dangerous_ip, spikes, defect),
       defect_rows=_defect_rows(defect)
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_out)

    print(f"✔ Raport HTML generat cu succes: {output_path}")



