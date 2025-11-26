import re

custom_parse_regex = re.compile(
    r'^(?P<timestamp>\d{4}[-/]\d{2}[-/]\d{2}[ T]\d{2}:\d{2}:\d{2})?\s*' # YYYY-MM-DD HH:MM:SS
    r'(?P<level>INFO|WARN|WARNING|DEBUG|ERROR|CRITICAL|FATAL)?\s*'      # level
    r'(?P<process>[A-Za-z0-9_-]+(?:\[\d+\])?)?:?\s*'                    # process sau process[PID]
    r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3})?\s*'                               # IP optional
    r'(?P<message>.*)$'                                                 # restul liniei
)

def parse_custom(line):
    m = custom_parse_regex.match(line)
    if not m:
        return None

    timestamp = m.group("timestamp")
    level = m.group("level")
    process = m.group("process")
    ip = m.group("ip")
    message = m.group("message").strip()

    # detectăm path separat
    path_match = re.search(r'(/[A-Za-z0-9_\-/\.?=&]+)', message)
    path = path_match.group(1) if path_match else None

    return {
        "timestamp": timestamp,
        "level": level,
        "message": message,
        "ip": ip,
        "method": None,
        "path": path,
        "status": None,
        "user_agent": None,
        "process": process,
        "source": "custom"
    }
