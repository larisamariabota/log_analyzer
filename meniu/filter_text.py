def filter_text(entries, text):
    """
    Returnează toate intrările care conțin TEXT oriunde în entry:
    - message
    - path
    - er_agent
    - orice alt câmpip
    
    Căutarea este case-insensitive.
    """
    text = text.lower()
    result = []

    for entry in entries:
       
        # îl transformăm în string pentru a căuta text în TOATE câmpurile
        combined = str(entry).lower()

        if text in combined:
            result.append(entry)

    return result

