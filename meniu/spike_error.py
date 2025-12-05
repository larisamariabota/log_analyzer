from collections import Counter

def detect_error_spike(entries, min_count=5):
    """
    Detectează dacă există spike de erori în întregul fișier log.
    Spike = ERROR apare mult mai des decât alte niveluri.
    """

    # Numărăm nivelurile
    levels = Counter(e.get("level") for e in entries)

    total_errors = levels.get("ERROR", 0)
    total_info = levels.get("INFO", 0)
    total_warn = levels.get("WARN", 0)

    print("\n🔍 Analiză spike de erori")
    print("=" * 40)
    print(f"INFO:  {total_info}")
    print(f"WARN:  {total_warn}")
    print(f"ERROR: {total_errors}")
    print("=" * 40)

    # Regula simplă: ERROR mult mai multe decât INFO/WARN
    if total_errors >= min_count and total_errors > (total_info + total_warn) / 2:
        print("⚠️  SPIKE DE ERORI DETECTAT!")
        print(f" ERROR = {total_errors} (anormal de multe)\n")
        return True
    else:
        print("✔ Nu s-a detectat niciun spike de erori.\n")
        return False
