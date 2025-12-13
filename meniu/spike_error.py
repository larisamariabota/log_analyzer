def detect_error_spikes(entries, window_seconds=10, min_count=3):
    """Detectează spike-uri de erori după timestamp_dt normalizat."""

    # 1. Păstrăm DOAR erorile care au timestamp valid
    errors = [e for e in entries if e.get("level") == "ERROR" and e.get("timestamp_dt")]
    errors.sort(key=lambda e: e["timestamp_dt"])

    spikes = []

    n = len(errors)
    if n < min_count:
        return spikes

    start = 0

    # 2. Detectăm ferestre în care apar multe erori
    for i in range(1, n):
        now = errors[i]["timestamp_dt"]
        begin = errors[start]["timestamp_dt"]

        # Mutăm start până când intervalul e sub fereastră
        while (now - begin).total_seconds() > window_seconds:
            start += 1
            begin = errors[start]["timestamp_dt"]

        window_count = i - start + 1

        if window_count >= min_count:
            spikes.append({
                "interval": f"{begin} → {now}",
                "type": "Temporal Error Spike",
                "count": window_count,
                "message": f"{window_count} erori într-o fereastră de {window_seconds}s"
            })

    return spikes






def print_spike_errors(spikes):
    """
    Afișează în consolă spike-urile detectate într-un format lizibil.
    """
    if not spikes:
        print("\n=== SPIKE-URI DE ERORI ===")
        print("Nu s-a detectat niciun spike de erori.\n")
        return

    print("\n=== SPIKE-URI DE ERORI DETECTATE ===")

    for i, s in enumerate(spikes, start=1):
        print(f"\nSpike #{i}")
        print("-" * 40)
        print(f"Interval:     {s.get('interval', 'N/A')}")
        print(f"Tip:          {s.get('type', 'Unknown')}")
        print(f"Număr erori:  {s.get('count', '-')}")
        print(f"Detalii:      {s.get('message', '')}")
        print("-" * 40)

    print("\nTotal spike-uri detectate:", len(spikes), "\n")
