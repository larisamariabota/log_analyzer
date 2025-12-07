import re
from datetime import datetime

CUSTOM_REGEX = re.compile(
    r'\[(?P<timestamp>.*?)\]\s+'
    r'IP=(?P<ip>\S+)\s+'
    r'LEVEL=(?P<level>\S+)\s+'
    r'MSG="(?P<message>.*?)"\s+'
    r'PATH=(?P<path>\S+)\s+'
    r'STATUS=(?P<status>\d+)'
)

def parse_custom(line):
    match = CUSTOM_REGEX.search(line)
    if not match:
        return None

    data = match.groupdict()

    # CONVERSIE TIMESTAMP LA DATETIME
    try:
        data["timestamp"] = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
    except:
        data["timestamp"] = None

    data["status"] = int(data["status"])

    # CUSTOM LOG NU ARE METHOD → punem None
    data["method"] = None

    # sursa
    data["source"] = "custom"

    return data



