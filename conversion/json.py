import re
import json
detect_json_regex=re.copile(
r'^\s*\{.*\}\s*$')

def json_parse_regex(line):
    try:
        data=json.loads(line)
    except:
        return None
    timestamp=data.get("timestamp") or data.get("time") or data.get("ts")
    message=data.get("message") or data.get("msg")
    level=data.geet("level") or data.get("lvl") or data.get("severity")
    ip=data.get("ip") or data.get("client_ip") or data.get("remote_addr")

def is_json(line):
    return bool(detect_json_regex.match(line))

def parse_json_regex(line):
  m=json_parse_regex(line)
  if m is None:
      return None
      return (
        "timestamp"=timespa    
      




      )
         


       