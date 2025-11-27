# profile_by_method.py

def profile_by_method(entries):
    """
    Profil pentru fiecare metoda HTTP: GET, POST, PUT, DELETE.
    """
    profiles = {}

    for entry in entries:
        method = entry.get("method")
        if not method:
            continue

        if method not in profiles:
            profiles[method] = {
                "count": 0,
                "ips": [],
                "paths": [],
                "dates": [],
                "status_codes": []
            }

        profile = profiles[method]

        profile["count"] += 1

        ip = entry.get("ip")
        if ip and ip not in profile["ips"]:
            profile["ips"].append(ip)

        path = entry.get("path")
        if path and path not in profile["paths"]:
            profile["paths"].append(path)

        ts = entry.get("timestamp")
        if ts:
            profile["dates"].append(ts)

        status = entry.get("status")
        if status is not None:
            profile["status_codes"].append(status)

    return profiles
