from conversion.detector import parse_line
from conversion.apache import is_apache
from conversion.nginx import is_nginx
from conversion.json import is_json
from conversion.syslog import is_syslog

def detect_type(line):
    if is_apache(line):
        return "apache"
    elif is_nginx(line):
        return "nginx"
    elif is_json(line):
        return "json"
    elif is_syslog(line):
        return "syslog"
    else:
        return "custom"

def analyze_file(path):
    print(f"\n=== Analizez fișierul: {path} ===")

    with open(path, "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            log_type = detect_type(line)
            parsed = parse_line(line)

            print(f"\nLinia {i+1}:")
            print(f"  Tip detectat: {log_type}")
            print(f"  Parsed: {parsed}")

            if i == 9:    # primele 10 linii
                break

if __name__ == "__main__":
    filepath = input("Introdu numele fișierului log: ")
    analyze_file(filepath)
