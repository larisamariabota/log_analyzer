
def profile_by_ip(entries):
    profile={}
    for entry in entries:
        ip=entry.get("ip")
        if not ip:
            continue
        if ip not in profile:
            # creem un nou profil pentru nouaa adresaIP
            profile[ip]={
                "count":0,
                
            }
