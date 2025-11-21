# IP - - [data] "METHOD PATH HTTP/vers" status bytes este formatul tipic de fisier log apche
# 192.168.0.10 - - [21/Nov/2025:10:20:45 +0200] "GET /index.html HTTP/1.1" 200 512  // exemplu clar de apche

import re
from datetime import datetime

# regex pentru detectarea unui log apache simplu
apache_detect_regex = re.compile(
    r'^\d{1,3}(\.\d{1,3}){3} .* \[.*\] ".*" \d{3} \d+'
)

# regex pentru extragerea campurilor dintr-un log apache
apache_parse_regex = re.compile(
    r'^[0-9]{1,3}(\.[0-9]{1,3})(\.[0-9]{1,3})(\.[0-9]{1,3})'   #o sa recunoasta un grup de 4 separate de"." 
    r'\[[^\]]+\]'  # o sa recunoasca daca exista secventa cu [] si elemente intre paranteze 
    r'"(?P<method>[A-Z]+) (?P<path>[^ ]+) [^"]+" '
    r'(?P<status>\d{3}) (?P<size>\d+)'
)

def is_apache(line):
    """
    returneaza true daca linia pare a fi dintr-un log apache
    """
    return bool(apache_detect_regex.match(line))


def parse_apache(line):
    """
    parseaza o linie de log apache si o transform in structura standard
    """

    m = apache_parse_regex.search(line)
    if not m:
        return None

    # extragem timestamp
    raw_time = m.group("time")
    # exemplu: 21/Nov/2025:10:20:45 +0200
    # luam doar partea cu data si ora
    raw_time = raw_time.split(" ")[0]

    try:
        timestamp = datetime.strptime(raw_time, "%d/%b/%Y:%H:%M:%S")
    except:
        timestamp = None

    status = int(m.group("status"))

    # determinam level pe baza codului http
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
        "user_agent": None,     # apache basic nu contine user-agent
        "process": None,        # apache nu are proces in log

        "source": "apache"
    }
