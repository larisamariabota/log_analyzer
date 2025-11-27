# profile_by_path.py

def profile_by_path(entries):
    """
    Profil pentru fiecare ruta accesata (/login, /admin, /search).
    """
    profiles = {}

    for entry in entries:
        path = entry.get("path")
        if not path:
            continue

        if path not in profiles:
            profiles[path] = {
                "count": 0,
                "ips": [],
                "methods": [],
                "status_codes": {},
                "dates": []
            }

        profile = profiles[path]

        profile["count"] += 1

        ip = entry.get("ip")
        if ip and ip not in profile["ips"]:
            profile["ips"].append(ip)

        method = entry.get("method")
        if method and method not in profile["methods"]:
            profile["methods"].append(method)

        status = entry.get("status")
        if status is not None:
            profile["status_codes"][status] = profile["status_codes"].get(status, 0) + 1

        ts = entry.get("timestamp")
        if ts:
            profile["dates"].append(ts)

    return profiles
