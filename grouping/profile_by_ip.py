# profile_by_ip.py

def profile_by_ip(entries):
    """
    Creeaza un profil complet pentru fiecare IP din loguri.
    """
    profiles = {}

    for entry in entries:  # parcurgem fiecare intrare
        ip = entry.get("ip")
        if not ip:
            continue

        if ip not in profiles:  # cand am gasit un nou ip il intializam
            profiles[ip] = {
                "count": 0,
                "levels": {},
                "dates": [],
                "status_codes": {},
                "paths": []
            }

        profile = profiles[ip]

        profile["count"] += 1

        level = entry.get("level")
        if level:
            profile["levels"][level] = profile["levels"].get(level, 0) + 1

        ts = entry.get("timestamp")
        if ts:
            profile["dates"].append(ts)

        status = entry.get("status")
        if status is not None:
            profile["status_codes"][status] = profile["status_codes"].get(status, 0) + 1

        path = entry.get("path")
        if path and path not in profile["paths"]:
            profile["paths"].append(path)

    return profiles

