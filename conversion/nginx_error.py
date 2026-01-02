import re
from datetime import datetime


def is_nginx_error(line):
    return (
        "error" in line.lower()
        and "client:" in line
        and "request:" in line
    )


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
    if not m:
        return None

    try:
        timestamp = datetime.strptime(
            m.group("date") + " " + m.group("time"),
            "%Y/%m/%d %H:%M:%S"
        )
    except:
        timestamp = None

    req = m.group("request").split(" ")

    return {
        "timestamp": timestamp,
        "level": m.group("level").upper(),
        "message": m.group("message"),
        "ip": m.group("client"),
        "method": req[0] if len(req) > 0 else None,
        "path": req[1] if len(req) > 1 else None,
        "status": None,
        "source": "nginx",
        "process": f"{m.group('pid')}#{m.group('tid')}",
    }
