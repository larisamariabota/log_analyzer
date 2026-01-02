import re
from datetime import datetime

# doua tipuri de fisiere

# fisier log nginx de acces
nginx_access_detect_regex = re.compile(
    r'^\d{1,3}(?:\.\d{1,3}){3} - - '
    r'\[\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2}\] '
    r'".*" \d{3} \d+'
)




def parse_nginx(line):
    if not is_nginx_access(line):
        return None
    return parse_nginx_access(line)

   

def is_nginx_access(line):
    return nginx_access_detect_regex.match(line) is not None 


parse_regex_nginx_access = re.compile(
    r'^(?P<ip>\d{1,3}(?:\.\d{1,3}){3}) - - '
    r'\[(?P<time>\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2})\] '
    r'"(?P<method>[A-Z]+) (?P<path>[^ ]+) HTTP/(?P<version>\d\.\d)" '
    r'(?P<status>\d{3}) (?P<size>\d+)'
)



def parse_nginx_access(line):
    m = parse_regex_nginx_access.search(line)
    if m is None:
        return None
    
    raw_time = m.group("time")
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
        "source": "nginx"
    }
# 


    
    
     