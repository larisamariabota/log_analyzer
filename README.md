# Log Analyzer
## Autor
- Nume: Bota Maria Larisa
- Grupa: 1.2
- Email: maria-larisa.bota@student.upt.ro
- An academic: 2025–2026

##  Aplicație CLI în Python pentru analiza fișierelor de log (Apache, Nginx, Syslog, JSON, custom).
##  Permite filtrarea intrărilor, generarea de statistici, detectarea anomaliilor (spike-uri de erori, activitate suspectă, alerte de securitate) și exportul rezultatelor în raport HTML. Include și un mod de monitorizare live (dashboard) care citește doar liniile noi din log.

## 📌 Funcționalități

###  Analiză & filtrare
- Suport pentru fișiere de log: **Apache / Nginx / Syslog / JSON / Custom**
- Filtrare după text sau level: `--filter` (ex: `ERROR`, `TypeError`, `timeout`)
- Filtrare după dată: `--date` (format `YYYY-MM-DD`)

###  Statistici & topuri
- Statistici generale despre log: `--stats`
- Top 10 IP-uri (după apariții): `--top_ips`
- Top 10 IP-uri periculoase (în funcție de reguli/heuristici): `--dangerous`

###  Detectare anomalii & securitate
- Detectare spike-uri de erori într-o fereastră de timp: `--spikes`
- Detectare activitate suspectă: `--suspicious`
- Afișare alerte de securitate detectate: `--alert`

###  Dashboard live (monitorizare în timp real)
- Pornește dashboard live (citește doar liniile noi din log): `--watch`
- Setează intervalul de refresh (secunde): `--refresh` (default: `2`)

###  Raportare
- Generare raport HTML complet: `--report html`
- Setarea fișierului de output: `--output` (default: `raport_complet.html`)



### Exemple de comenzi disponibile


```bash
python main.py test/apache.log --report html --output raport.html


python main.py test/nginx_access.log --spikes


python main.py test/apache.log --stats

python main.py test/custom.log --date 2025-01-15

python main.py test/nginx_error.log  --top_ips --dangerous


python main.py test/nginx_error.log --filter ERROR

python main.py test/custom.log --alert


python main.py test/syslog.log --top_ips

python main.py test/json.log --suspicious

##  Screenshots din terminal

Pentru a demonstra funcționarea aplicației, fiecare comandă prezentată mai sus
a fost rulată în terminal, iar output-ul rezultat a fost capturat sub formă
de screenshot.
Toate aceste capturi sunt disponibile în folderul: `terminal_screen/`


## Fisierul output_omenzi.csv
Rezultatele comenzilor sunt salvate și în `output_comenzi.csv`.

