def print_ip_profiles(profiles):
    for ip, data in profiles.items():
        print("=" * 50)
        print(f"IP: {ip}")
        print(f"  Total requests: {data['count']}")
        
        print("  Levels:")
        for lvl, n in data["levels"].items():
            print(f"    {lvl}: {n}")

        print("  Status codes:")
        for st, n in data["status_codes"].items():
            print(f"    {st}: {n}")

        print("  Paths:")
        for p in data["paths"]:
            print(f"    {p}")

        print("  Timestamps:")
        for t in data["dates"][:5]:  # doar primele 5 ca să nu fie haos
            print(f"    {t}")
        
        print("=" * 50)
        print()
