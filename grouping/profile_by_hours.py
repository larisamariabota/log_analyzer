# profile_by_hour.py

def profile_by_hour(entries):
    """
    Grupare pe ore (YYYY-MM-DD HH) pentru spike detection.
    """
    profile = {}

    for entry in entries:
        ts = entry.get("timestamp")
        if not ts:
            continue

        hour_key = ts.strftime("%Y-%m-%d %H")

        if hour_key not in profile:
            profile[hour_key] = 0

        profile[hour_key] += 1

    return profile
