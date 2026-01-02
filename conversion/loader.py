from conversion.detector import parse_line
from datetime import datetime

def normalize_timestamp(ts):
    """Întoarce datetime din orice format suportat."""
    if isinstance(ts, datetime):
        return ts
    if not isinstance(ts, str):
        return None

    ts = ts.strip().strip("[]") 
 
 
    formats = [
        "%Y-%m-%dT%H:%M:%S",        # JSON format
        "%Y-%m-%d %H:%M:%S",        # custom
        "%d/%b/%Y:%H:%M:%S",        # Apache / Nginx
        "%b %d %H:%M:%S",           # Syslog
        "%Y-%m-%d",                 # doar data
        "%H:%M:%S",                 # doar ora
    ]

    for fmt in formats:
        try:
            return datetime.strptime(ts, fmt)
        except:
            pass

    return None


def load_file(path):
    entries = []
    with open(path, "r", encoding="utf-8") as f: # encoding utf-8 in caz de caractere speciale 
        for line in f:

            if not line:
                continue

            parsed = parse_line(line)
            if parsed is None:
                continue

            # Convertim timestamp-ul în datetime
            ts = parsed.get("timestamp")
            parsed["timestamp_dt"] = normalize_timestamp(ts)

            entries.append(parsed)

    return entries

