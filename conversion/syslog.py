import re

detect_syslog_regex = re.compile(
    r'^(?:<\d+>)?[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\S+'
)

def is_syslog(line):
    return bool(detect_syslog_regex.match(line))

parse_syslog_regex = re.compile(
    r'^(?:<(?P<pri>\d+)>)?'                                    
    r'(?P<time>[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+' 
    r'(?P<host>\S+)\s+'                                         
    r'(?P<process>[^:]+):\s+'                                   
    r'(?P<message>.*)$'                                         
)

def parse_syslog(line):
    m = parse_syslog_regex.match(line)
    if not m:
        return None

    raw_time = m.group("time")
    message  = m.group("message")

    # extragem IP dacă apare în mesaj
    ip_match = re.search(r'\b\d{1,3}(?:\.\d{1,3}){3}\b', message)
    ip = ip_match.group(0) if ip_match else None

    return {
        "timestamp": raw_time,
        "level": None,
        "message": message,

        "ip": ip,
        "method": None,
        "path": None,
        "status": None,
        "user_agent": None,

        "process": m.group("process"),
        "source": "syslog"
    }


    