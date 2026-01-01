from datetime import datetime


def filter_entries(entries, text_filter=None, date_filter=None):
    """
    Filtrare multi-criteriu:
    - text_filter: ERROR / TypeError / WARN etc.
    - date_filter: YYYY-MM-DD
    """

    # Filtrare dupa text sau level
    if text_filter:
        f = text_filter.lower()
        entries = [
            e for e in entries
            if f in str(e.get("message", "")).lower()
            or f == str(e.get("level", "")).lower()
        ]

    # Filtrare dupa data
    if date_filter:
        try:
            target_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
            entries = [
                e for e in entries
                if e.get("timestamp_dt") and e["timestamp_dt"].date() == target_date
            ]
        except ValueError:
            print(" Data invalida. Format corect: YYYY-MM-DD")
            return []

    return entries
def print_filter(entries, limit=30):
    """
    Afișează intrările filtrate într-un format compact.
    limit = câte linii afișează maxim (ca să nu-ți umple terminalul).
    """
    if not entries:
        print("\n Nu există rezultate după filtrare.\n")
        return

    print(f"\n✅ Rezultate după filtrare: {len(entries)} înregistrări")
    print("-" * 80)

    shown = 0
    for e in entries:
        ts = e.get("timestamp_dt") or e.get("timestamp") or "-"
        ip = e.get("ip", "-")
        lvl = e.get("level", "-")
        status = e.get("status", "-")
        path = e.get("path", "-")
        msg = e.get("message", "-")

        # taie mesajul dacă e prea lung (să rămână clean)
        msg = str(msg)
       

        print(f"[{ts}] {lvl:<5} {status:<3} IP={ip:<15} PATH={path} MSG={msg}")

        shown += 1
        if shown >= limit:
            break

    if len(entries) > limit:
        print(f"... și încă {len(entries) - limit} rezultate (mărește limit dacă vrei)")
    print("-" * 80 + "\n")

