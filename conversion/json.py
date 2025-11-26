import re
import json

# detectăm dacă linia este JSON
detect_json_regex = re.compile(
    r'^\s*\{.*\}\s*$'
)

def json_parse_regex(line):
    try:
        data = json.loads(line)
    except:
        return None

    timestamp = data.get("timestamp") or data.get("time") or data.get("ts")
    message = data.get("message") or data.get("msg")
    level = data.get("level") or data.get("lvl") or data.get("severity")
    ip = data.get("ip") or data.get("client_ip") or data.get("remote_addr")
    method = data.get("method")
    path = data.get("path")
    status = data.get("status")
    process = data.get("process") or data.get("proc")
    user_agent = data.get("user_agent") or data.get("ua")

    return {
        "timestamp": timestamp,
        "ip": ip,
        "message": message,
        "level": level,
        "path": path,
        "method": method,
        "status": status,
        "user_agent": user_agent,
        "process": process
    }

def is_json(line):
    return bool(detect_json_regex.match(line))

def parse_json(line):
    m = json_parse_regex(line)
    if m is None:
        return None

    return {
        "timestamp": m["timestamp"],
        "ip": m["ip"],
        "message": m["message"],
        "level": m["level"],
        "path": m["path"],
        "method": m["method"],
        "status": m["status"],
        "user_agent": m["user_agent"],
        "process": m["process"],
        "source": "json"
    }
