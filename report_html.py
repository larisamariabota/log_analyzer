import html
from datetime import timedelta

# ============================================================
#                  TEMPLATE HTML (ESCAPED)
# ============================================================

HTML_SHELL = """
<!doctype html>
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

      <section class="card col-6">
        <div class="head"><h2>Distribuție pe niveluri</h2></div>
        <div class="body">
          <div class="table-wrap"><table>
            <thead><tr>
              <th>Nivel</th><th>Count</th><th>Procent</th>
            </tr></thead>
            <tbody>{level_rows}</tbody>
          </table></div>
        </div>
      </section>

      <section class="card col-6">
        <div class="head"><h2>Top IP-uri</h2></div>
        <div class="body">
          <div class="table-wrap"><table>
            <thead><tr>
              <th>IP</th><th>Cereri</th><th>Procent</th>
            </tr></thead>
            <tbody>{top_ip_rows}</tbody>
          </table></div>
        </div>
      </section>

      <section class="card col-12">
        <div class="head"><h2 class="gold">Top IP-uri Periculoase</h2></div>
        <div class="body">
          <div class="table-wrap"><table>
            <thead><tr>
              <th>IP</th><th>Atacuri</th><th>Tipuri</th><th>Ultima</th><th>Risc</th>
            </tr></thead>
            <tbody>{dangerous_rows}</tbody>
          </table></div>
        </div>
      </section>

      <section class="card col-12">
        <div class="head"><h2>Posibile defecțiuni în sistem</h2></div>
        <div class="body">
          <div class="table-wrap"><table>
            <thead><tr>
              <th>Timestamp</th><th>IP</th><th>Method</th><th>Path</th><th>Status</th><th>Mesaj</th><th>Sursă</th>
            </tr></thead>
            <tbody>{defect_rows}</tbody>
          </table></div>
        </div>
      </section>

      <section class="card col-12">
        <div class="head"><h2>Spike-uri detectate</h2></div>
        <div class="body">
          <div class="table-wrap"><table>
            <thead><tr>
              <th>Interval</th><th>Tip</th><th>Count</th><th>Mesaj</th>
            </tr></thead>
            <tbody>{spike_rows}</tbody>
          </table></div>
        </div>
      </section>

      <section class="card col-12">
        <div class="head"><h2 class="gold">Recomandări finale</h2></div>
        <div class="body">
          <ul>{recommendations}</ul>
        </div>
      </section>

    </div>
    <div class="footer">
      <span class="gold">©</span> Raport generat automat • Bota Maria Larisa
    </div>
  </div>
</body>
</html>
"""


# ============================================================
#                DISTRIBUȚIE PE NIVELURI
# ============================================================

def _level_rows(level_stats):
    rows = ""
    total = sum(level_stats.values()) if level_stats else 1
    for lvl, count in level_stats.items():
        pct = (count / total) * 100
        rows += f"<tr><td>{lvl}</td><td>{count}</td><td>{pct:.2f}%</td></tr>"
    return rows


# ============================================================
#                     TOP IP
# ============================================================

def _top_ip_rows(top_ips, total=None):
    rows = ""
    total = total or sum(c for _, c in top_ips) or 1
    for ip, count in top_ips:
        pct = (count / total) * 100
        rows += f"<tr><td>{ip}</td><td>{count}</td><td>{pct:.2f}%</td></tr>"
    return rows


# ============================================================
#                   IP-URI PERICULOASE
# ============================================================

def _dangerous_rows(dangerous_list):
    if not dangerous_list:
        return "<tr><td colspan='5'>Niciun IP periculos</td></tr>"

    rows = ""
    for ip, data in dangerous_list:
        types_str = f"ERR:{data.get('errors',0)} • ADMIN:{data.get('admin_scans',0)} • FAIL:{data.get('failed_login',0)}"
        last = data.get("last_seen")
        if last:
            try:
                last = last.strftime("%Y-%m-%d %H:%M:%S")
            except:
                last = str(last)

        rows += (
            f"<tr class='danger-row'>"
            f"<td class='ip-danger'>{ip}</td>"
            f"<td>{data.get('total_requests',0)}</td>"
            f"<td>{types_str}</td>"
            f"<td>{last}</td>"
            f"<td>{data.get('score',0)}</td>"
            f"</tr>"
        )
    return rows


# ============================================================
#                   DEFECȚIUNI SISTEM
# ============================================================

def _defect_rows(events):
    if not events:
        return "<tr><td colspan='7'>Nicio defecțiune sistem detectată</td></tr>"

    rows = ""
    for e in events:
        rows += (
            "<tr class='danger-row'>"
            f"<td>{e.get('timestamp','-')}</td>"
            f"<td>{e.get('ip','-')}</td>"
            f"<td>{e.get('method','-')}</td>"
            f"<td>{e.get('path','-')}</td>"
            f"<td>{e.get('status','-')}</td>"
            f"<td>{e.get('message','-')}</td>"
            f"<td>{e.get('source','-')}</td>"
            "</tr>"
        )
    return rows


# ============================================================
#                       SPIKE-URI
# ============================================================

def spike_rows(spikes):
    if not spikes:
        return "<tr><td colspan='4'>Niciun spike detectat</td></tr>"

    rows = ""
    for s in spikes:
        rows += (
            "<tr>"
            f"<td>{s.get('interval','-')}</td>"
            f"<td>{s.get('type','-')}</td>"
            f"<td>{s.get('count','-')}</td>"
            f"<td>{html.escape(str(s.get('message','-')))}</td>"
            "</tr>"
        )
    return rows


# ============================================================
#                   RECOMANDĂRI
# ============================================================

def _generate_recommendations(dangerous, spikes, defect):
    rec = []
    if dangerous:
        rec.append("<li><b>IP-uri periculoase:</b> Recomand blocare firewall.</li>")
    if defect:
        rec.append("<li><b>Defecțiuni sistem:</b> Monitorizare + analiză server.</li>")
    if spikes:
        rec.append("<li><b>Spike-uri detectate:</b> Posibil overload/DoS.</li>")

    rec.append("<li><b>General:</b> Activează log rotation și backup automat.</li>")
    return "\n".join(rec)


# ============================================================
#                GENERARE RAPORT FINAL
# ============================================================

def generate_html_report(
        filename,
        total_lines,
        level_stats,
        top_ips,
        ip_profiles,
        spikes,
        suspicious_events,      # ignorat
        output_path="raport.html",
        *,
        top_dangerous_ip=None,
        defect=None
    ):

    top_dangerous_ip = top_dangerous_ip or []
    defect = defect or []

    html_out = HTML_SHELL.format(
        filename=filename,
        total_lines=total_lines,
        level_rows=_level_rows(level_stats),
        top_ip_rows=_top_ip_rows(top_ips),
        dangerous_rows=_dangerous_rows(top_dangerous_ip),
        defect_rows=_defect_rows(defect),
        spike_rows=spike_rows(spikes),
        recommendations=_generate_recommendations(top_dangerous_ip, spikes, defect)
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_out)

    print(f"✔ Raport HTML generat: {output_path}")

