# Log Analyzer
## Autor
- Nume: Bota Maria Larisa
- Grupa: 1.2
- Email: maria-larisa.bota@student.upt.ro
- An academic: 2025–2026

##  Aplicație CLI în Python pentru analiza fișierelor de log (Apache, Nginx, Syslog, JSON, custom).
##  Permite filtrarea intrărilor, generarea de statistici, detectarea anomaliilor (spike-uri de erori, activitate suspectă, alerte de securitate) și exportul rezultatelor în raport HTML. Include și un mod de monitorizare live (dashboard) care citește doar liniile noi din log.

## 📌 Funcționalități

### 🔎 Analiză & filtrare
- Suport pentru fișiere de log: **Apache / Nginx / Syslog / JSON / Custom**
- Filtrare după text sau level: `--filter` (ex: `ERROR`, `TypeError`, `timeout`)
- Filtrare după dată: `--date` (format `YYYY-MM-DD`)

### 📊 Statistici & topuri
- Statistici generale despre log: `--stats`
- Top 10 IP-uri (după apariții): `--top_ips`
- Top 10 IP-uri periculoase (în funcție de reguli/heuristici): `--dangerous`

### 🚨 Detectare anomalii & securitate
- Detectare spike-uri de erori într-o fereastră de timp: `--spikes`
- Detectare activitate suspectă: `--suspicious`
- Afișare alerte de securitate detectate: `--alert`

### 🖥️ Dashboard live (monitorizare în timp real)
- Pornește dashboard live (citește doar liniile noi din log): `--watch`
- Setează intervalul de refresh (secunde): `--refresh` (default: `2`)

### 📄 Raportare
- Generare raport HTML complet: `--report html`
- Setarea fișierului de output: `--output` (default: `raport_complet.html`)



### Opțiuni disponibile

- `logfile` (pozitional): Fișierul de log (apache, nginx, syslog, custom)
- `--stats`: Afișează statistici generale
- `--top_ips`: Afișează top 10 IP-uri
- `--dangerous`: Afișează top 10 IP-uri periculoase
- `--spikes`: Detectează spike-uri de erori
- `--suspicious`: Detectează activitate suspectă
- `--alert`: Afișează alertele de securitate detectate
- `--filter <text>`: Filtrează după text sau level (ex: `ERROR`, `TypeError`)
- `--date <YYYY-MM-DD>`: Filtrează după dată
- `--report html`: Generează raport HTML
- `--output <file.html>`: Numele fișierului HTML generat (default: `raport_complet.html`)
- `--watch`: Pornește dashboard live (citește doar liniile noi)
- `--refresh <secunde>`: Refresh dashboard (default: `2`)
## ✅ Combinări uzuale

### Monitorizare live cu refresh mai rapid
```bash
python main.py test_logs/nginx_error.log --watch --refresh 1
