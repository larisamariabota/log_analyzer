# profile_by_status.py

def profile_by_status(entries):
    """
    Profil pentru fiecare cod HTTP: 200, 301, 404, 500 etc.
    """
    profiles = {}

    for entry in entries:
        status = entry.get("status")
        if status is None:
            continue

        if status not in profiles:
            profiles[status] = {
                "count": 0,
                "ips": [],
                "paths": [],
                "dates": [],
                "methods": []
            }

        profile = profiles[status]

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

        method = entry.get("method")
        if method and method not in profile["methods"]:
            profile["methods"].append(method)

    return profiles
