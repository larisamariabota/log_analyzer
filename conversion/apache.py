# IP - - [data] "METHOD PATH HTTP/vers" status bytes
# exemplu: 192.168.0.10 - - [21/Nov/2025:10:20:45 +0200] "GET /index.html HTTP/1.1" 200 512

import re
from datetime import datetime

# -------------------------------
# detectare log Apache
# -------------------------------
apache_detect_regex = re.compile(
    r'^\d{1,3}(\.\d{1,3}){3} .* \[.*\] ".*" \d{3} \d+'
)

# -------------------------------
# parsare log Apache
# -------------------------------
apache_parse_regex = re.compile(
    r'^(?P<ip>\d{1,3}(\.\d{1,3}){3}) - - '                                 # IP - - 
    r'\[(?P<time>\d{2}/[A-Za-z]{3}/\d{4}:'                                # zi/luna/an
    r'\d{2}:\d{2}:\d{2} [+\-]\d{4})\] '                                    # ora + fus orar
    r'"(?P<method>[A-Z]+) (?P<path>[^ ]+) HTTP/(?P<version>\d\.\d)" '     # GET /path HTTP/1.1
    r'(?P<status>\d{3}) (?P<size>\d+)'                                     # status + size
)


# functia care spune daca o linie e de tip Apache

def is_apache(line):
    return bool(apache_detect_regex.match(line))


# functia care parseaza un log Apache

def parse_apache(line):
    m = apache_parse_regex.search(line)
    if not m:
        return None

    raw_time = m.group("time")  # ex: 21/Nov/2025:10:20:45 +0200
    raw_time = raw_time.split(" ")[0]  # doar data si ora, fara fus

    try:
        timestamp = datetime.strptime(raw_time, "%d/%b/%Y:%H:%M:%S")
    except:
        timestamp = None

    status = int(m.group("status"))

    if status >= 500:
        level = "ERROR"
    elif status >= 400:
        level = "WARN"
    else:
        level = "INFO"

    return {
        "timestamp": timestamp,
        "level": level,
        "message": f'{m.group("method")} {m.group("path")}',

        "ip": m.group("ip"),
        "method": m.group("method"),
        "path": m.group("path"),
        "status": status,
        "size": int(m.group("size")),
        "version": m.group("version"),

        "user_agent": None,
        "process": None,
        "source": "apache"
    }



