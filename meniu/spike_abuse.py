from collections import defaultdict
from datetime import datetime, timedelta
from collections import Counter

# -------------------------------------------------------
# SPIKE IP ABUSE
# -------------------------------------------------------

def detect_spike_ip(entries, limit_per_minute=100, limit_per_hour=800):
    """
    Detecteaza spike-uri de trafic si potential abuz pentru fiecare IP.
    """

    activity = defaultdict(lambda: defaultdict(int))  # IP -> minute -> count

    for entry in entries:
        ip = entry.get("ip")
        ts = entry.get("timestamp")

        # Ignoram timestampurile invalide (string, None etc.)
        if not ip or not isinstance(ts, datetime):
            continue

        # Rotunjim timestamp la minut
        minute_key = ts.replace(second=0, microsecond=0)
        activity[ip][minute_key] += 1

    results = []

    for ip, minutes in activity.items():
        minute_list = sorted(minutes.items())

        # Spike per minut
        for minute, count in minute_list:
            if count >= limit_per_minute:
                results.append({
                    "type": "IP Spike per minute",
                    "ip": ip,
                    "count": count,
                    "interval": f"{minute.strftime('%H:%M')} - {(minute + timedelta(minutes=1)).strftime('%H:%M')}",
                    "message": f"IP {ip} a trimis {count} cereri intr-un minut — posibil abuz."
                })

        # Spike per ora
        hourly = defaultdict(int)
        for minute, count in minute_list:
            hour_key = minute.replace(minute=0, second=0, microsecond=0)
            hourly[hour_key] += count

        for hour, c in hourly.items():
            if c >= limit_per_hour:
                results.append({
                    "type": "IP Spike per hour",
                    "ip": ip,
                    "count": c,
                    "interval": f"{hour.strftime('%H:%M')} - {(hour + timedelta(hours=1)).strftime('%H:%M')}",
                    "message": f"IP {ip} a generat {c} cereri intr-o ora — comportament agresiv."
                })

    return results

# -------------------------------------------------------
# SPIKE METHOD
# -------------------------------------------------------

def detect_spike_method(entries, limit_per_minute=150, limit_per_hour=1500):
    """
    Detecteaza spike-uri pe metode HTTP (GET, POST, etc.)
    """

    activity = defaultdict(lambda: defaultdict(int))  # METHOD -> minute -> count

    for entry in entries:
        method = entry.get("method")
        ts = entry.get("timestamp")

        # Ignoram timestampurile invalide
        if not method or not isinstance(ts, datetime):
            continue

        minute_key = ts.replace(second=0, microsecond=0)
        activity[method][minute_key] += 1

    results = []

    for method, minute_data in activity.items():
        minute_list = sorted(minute_data.items())

        # Spike per minut
        for minute, count in minute_list:
            if count >= limit_per_minute:
                results.append({
                    "type": "METHOD Spike per minute",
                    "method": method,
                    "count": count,
                    "interval": f"{minute.strftime('%H:%M')} - {(minute + timedelta(minutes=1)).strftime('%H:%M')}",
                    "message": f"Metoda {method} are {count} cereri intr-un minut — posibil abuz."
                })

        # Spike per ora
        hourly = defaultdict(int)
        for minute, count in minute_list:
            hour_key = minute.replace(minute=0, second=0, microsecond=0)
            hourly[hour_key] += count

        for hour, c in hourly.items():
            if c >= limit_per_hour:
                results.append({
                    "type": "METHOD Spike per hour",
                    "method": method,
                    "count": c,
                    "interval": f"{hour.strftime('%H:%M')} - {(hour + timedelta(hours=1)).strftime('%H:%M')}",
                    "message": f"Metoda {method} a generat {c} cereri intr-o ora — posibil abuz la nivel de API."
                })

    return results

# -------------------------------------------------------
# PRINT REPORT
# -------------------------------------------------------

def print_spike_report(spikes):
    if not spikes:
        print("Nu s-au detectat spike-uri sau comportament abuziv.")
        return

    print("\n================ SPIKE & ABUSE REPORT ================\n")

    for s in spikes:
        print("----------------------------------------")
        print(s["message"])
        print(f"Interval: {s['interval']}")
        print(f"Numar cereri: {s['count']}")
        print(f"Tip: {s['type']}")

        print("\nSugestii de actiune:")
        print(" - Blocheaza temporar IP-ul sau metoda")
        print(" - Aplica rate-limit")
        print(" - Activeaza challenge (CAPTCHA/token)")
        print(" - Logheaza detaliat cererile suspecte")
        print(" - Notifica administratorul")
        print("----------------------------------------\n")

# -------------------------------------------------------
# ERROR SPIKE
# -------------------------------------------------------

def detect_error_spike(entries, min_count=5):
    """
    Detecteaza daca exista spike de erori in intregul fisier log.
    """

    levels = Counter(e.get("level") for e in entries)

    total_errors = levels.get("ERROR", 0)
    total_info = levels.get("INFO", 0)
    total_warn = levels.get("WARN", 0)

    print("\nAnaliza spike de erori")
    print("=" * 40)
    print(f"INFO:  {total_info}")
    print(f"WARN:  {total_warn}")
    print(f"ERROR: {total_errors}")
    print("=" * 40)

    if total_errors >= min_count and total_errors > (total_info + total_warn) / 2:
        print("SPIKE DE ERORI DETECTAT!")
        print(f"ERROR = {total_errors} (anormal de multe)\n")
        return True
    else:
        print("Nu s-a detectat spike de erori.\n")
        return False
