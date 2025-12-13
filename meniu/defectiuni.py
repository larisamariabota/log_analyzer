from collections import Counter
from datetime import timedelta

def defectiuni_sistem(entries, min_errors=5, window_seconds=10):
    failures = []

    # sortăm după timp
    entries = sorted(entries, key=lambda e: e["timestamp_dt"])

    # filtrăm erorile serverului
    server_errors = [e for e in entries if e.get("status") in (500, 501, 502, 503, 504)]

    # ----------------------------------------------------------
    # 1) SPIKE DE 500/503
    # ----------------------------------------------------------
    start = 0
    for i in range(len(server_errors)):
        while server_errors[i]["timestamp_dt"] - server_errors[start]["timestamp_dt"] > timedelta(seconds=window_seconds):
            start += 1

        count = i - start + 1
        if count >= min_errors:
            failures.append({
                "timestamp": f"{server_errors[start]['timestamp_dt']} → {server_errors[i]['timestamp_dt']}",
                "ip": server_errors[i].get("ip", "-"),
                "method": server_errors[i].get("method", "-"),
                "path": server_errors[i].get("path", "-"),
                "status": server_errors[i].get("status", "-"),
                "message": f"{count} erori 500/503 într-un interval scurt — posibil cădere server.",
                "source": "Server Error Spike",
                "risk": 1
            })
            break

    # ----------------------------------------------------------
    # 2) PATH FAILURE (mult 500 pe același endpoint)
    # ----------------------------------------------------------
    path_count = Counter(e["path"] for e in server_errors)
    for path, cnt in path_count.items():
        if cnt >= min_errors:
            # găsim PRIMA apariție ca să luăm info reale
            first = next(e for e in server_errors if e["path"] == path)
            failures.append({
                "timestamp": first.get("timestamp_dt", "-"),
                "ip": first.get("ip", "-"),
                "method": first.get("method", "-"),
                "path": path,
                "status": first.get("status", "-"),
                "message": f"{cnt} erori server pe {path} — endpoint posibil căzut.",
                "source": "Path Failure",
                "risk": 1
            })

    # ----------------------------------------------------------
    # 3) REPETITIVE ERROR MESSAGE
    # ----------------------------------------------------------
    msg_count = Counter(e["message"] for e in server_errors)
    for msg, cnt in msg_count.items():
        if cnt >= min_errors:
            first = next(e for e in server_errors if e["message"] == msg)
            failures.append({
                "timestamp": first.get("timestamp_dt", "-"),
                "ip": first.get("ip", "-"),
                "method": first.get("method", "-"),
                "path": first.get("path", "-"),
                "status": first.get("status", "-"),
                "message": f"Mesajul '{msg}' apare de {cnt} ori — componentă sistem defectă.",
                "source": "Repetitive Error",
                "risk": 1
            })

    return failures

