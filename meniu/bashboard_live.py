# meniu/watch_live.py
import os
import time

from conversion.detector import parse_line  # funcția ta care parsează o linie
from meniu.top_ip import top_ip, top_dangerous_ip
from meniu.spike_abuse import detect_all_spikes, print_alert_table
from meniu.statistici import status


def clear():
    #os.system("comanda") // curata ecranul
      #nt e pentru windows, cls= comanda de curatatre ecran pentru wiindows, altefel clear e pt linix si mac
    os.system("cls" if os.name == "nt" else "clear")

# adag in watch_log_live optiunile pentru fiecare functionalitate
def watch_log_live(
    logfile: str,
    refresh: int = 2,
    stats: bool = False,
    top_ips: bool = False,
    dangerous: bool = False,
    alert: bool = False,
    suspicous:bool=False,
    filter:bool=False,
    data:bool=False
):

    with open(logfile, "r", encoding="utf-8", errors="ignore") as f: # deschid fisierul in  modul citire, endcoding utf-8 e pt caractere speciale
        # plecăm de la final (doar ce apare de ACUM)
        f.seek(0, os.SEEK_END)

        total_new = 0 # contor pentru liniile noi aparute

        try:
            while True: # intram in bucla infinita pentru a face refres in interval de 2 secumde
                new_entries = []

                # citim TOT ce s-a adăugat de la ultimul refresh
                while True:
                    line = f.readline()
                    if not line:
                        break
                    line = line.strip()
                    if not line:
                        continue

                    parsed = parse_line(line) # adacem linia la dictionar standard 
                    if parsed:
                        new_entries.append(parsed)

                clear()
                print(f" WATCH MODE — {logfile}")
                print("=" * 80)
                print(f"Linii noi (ultimul refresh): {len(new_entries)} | Total linii noi: {total_new}")
                print("=" * 80)

                if not new_entries:
                    print("(Nu au apărut linii noi.)")
                else:
                    total_new += len(new_entries)

                    # Rulezi DOAR ce ai cerut, pe batch-ul nou
                    if stats:
                        print("\n--- STATS (doar linii noi) ---")
                        status(new_entries)

                    if top_ips:
                        print("\n--- TOP IP (doar linii noi) ---")
                        if dangerous:
                            top_dangerous_ip(new_entries)
                        else:
                            top_ips(new_entries)

                    if alert:
                        print("\n--- ALERT (doar linii noi) ---")
                        spikes = detect_all_spikes(new_entries)
                        print_alert_table(spikes)

                print("\nCtrl+C pentru stop.")
                time.sleep(refresh)

        except KeyboardInterrupt: # daca voom apasa Crtl+C vom oprii bucl infinita
            print("\nOprit (Ctrl+C).")

