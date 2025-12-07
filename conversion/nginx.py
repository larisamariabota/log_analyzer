import re
from datetime import datetime

# doua tipuri de fisiere

# fisier log nginx de acces
nginx_access_detect_regex=re.compile(
      r'^\d{1,3}(\.\d{1,3}){3} .* \[.*\] ".*" \d{3} \d+'
)

#fisier log nginx de error

nginx_error_detect_regex=re.compile(
    r'^\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} \[[a-zA-Z]+\]'
)

def nginx_type(line):
    if nginx_access_detect_regex.match(line) is not None:
        return "access"
    if nginx_error_detect_regex.match(line) is not None:
        return "error"
    return "None"

def parse_nginx(line):
    t=nginx_type(line)
    if t=="None":
        return None
    if t=="access":
        return parse_nginx_access(line)
    if t=="error":
        return parse_nginx_error(line)
    

def is_nginx(line):
    return nginx_access_detect_regex.match(line) is not None or \
           nginx_error_detect_regex.match(line) is not None


parse_regex_nginx_access=re.compile(
  r'^(?P<ip>\d{1,3}(\.\d{1,3}){3}) - - '   # IP - - 
    r'\[(?P<time>\d{2}/[A-Za-z]{3}/\d{4}:'                                # zi/luna/an
    r'\d{2}:\d{2}:\d{2} [+\-]\d{4})\] '                                    # ora + fus orar
    r'"(?P<method>[A-Z]+) (?P<path>[^ ]+) HTTP/(?P<version>\d\.\d)" '     # GET /path HTTP/1.1
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

parse_regex_nginx_error = re.compile(
    r'^(?P<date>\d{4}/\d{2}/\d{2}) '
    r'(?P<time>\d{2}:\d{2}:\d{2}) '
    r'\[(?P<level>[a-z]+)\] '
    r'(?P<pid>\d+)#(?P<tid>\d+): '
    r'\*(?P<conn>\d+) '
    r'(?P<message>[^,]+), '
    r'client: (?P<client>[0-9\.]+), '
    r'server: (?P<server>[^,]*), '
    r'request: "(?P<request>[^"]+)", '
    r'host: "(?P<host>[^"]+)"'
)


def parse_nginx_error(line):
    m = parse_regex_nginx_error.search(line)

    if m is None:
        return None

    # timestamp
    raw_ts = m.group("date") + " " + m.group("time")
    try:
        timestamp = datetime.strptime(raw_ts, "%Y/%m/%d %H:%M:%S")
    except:
        timestamp = None

    # nivel -> normalizat
    level = m.group("level").upper()   # error -> ERROR

    # request split
    req = m.group("request")
    parts = req.split(" ")
    method = parts[0] if len(parts) > 0 else None
    path = parts[1] if len(parts) > 1 else None

    # structura standard
    return {
        "timestamp": timestamp,
        "level": level,
        "message": m.group("message"),

        "ip": m.group("client"),
        "method": method,
        "path": path,

        "status": None,            # nginx error.log NU are cod HTTP
        "user_agent": None,        # nu exista in error.log
        "process": f'{m.group("pid")}#{m.group("tid")}',  # ex: "2314#0"

        "source": "nginx"
    }


    
    
     