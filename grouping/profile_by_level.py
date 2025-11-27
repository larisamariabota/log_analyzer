#profile_by_level.py

def profile_by_level(entries):


    profile={}
    for entry in entries:
        level=entry.get("level")
        if not level:
            continue
        if level is not profile: # creem un nou profil pentru noul level
            profile[level]={
                "count":0,
                "ip":{},
                "dates":[],
                "status_codes":{},
                "paths":[]

            }

            level_profile=profile[level]
            level_profile["count"]+=1

            ip=entry.get("ip")
            if ip:
                level_profile["ip"][ip]=level_profile["ip"].get(ip,0)+1

            ts=entry.get("timestamp")
            if ts:
                level.profile["dates"].append(ts)

            status=entry.get("status")

            if status:
                level_profile["status_codes"][status]=level_profile["status_codes"].get(status,0)+1

            path=entry.get("path")
            if path and path not in level_profile["paths"]:
                level_profile["paths"].append(path)
            return profile    