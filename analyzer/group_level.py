# count_by_level.py

def count_by_level(entries):
    """
    Intoarce un dictionar cu numarul de loguri pentru fiecare nivel.
    EX: {"INFO": 120, "ERROR": 45, "WARN": 12}
    """
    counts = {}

    for entry in entries:
        level = entry.get("level")
        if not level:
            continue

        if level not in counts:
            counts[level] = 0

        counts[level] += 1

    return counts


