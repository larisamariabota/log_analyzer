import argparse
import sys
# biblioteca sys e folosita pentru a aparea diacritece in terminal
# bibliotecca argparse e folosita pentru a prelua argumentele din terminal si a le transforma  in variabile python
# pentru Unicode în terminal (Windows)
sys.stdout.reconfigure(encoding="utf-8")

from conversion.loader import load_file
from raport.creaza_raport import run_report


from meniu.statistici import status
from meniu.top_ip import top_ip
from meniu.spike_error import detect_error_spikes

from meniu.paterns import (
    detect_bruteforce,  
    detect_404_scans,
    detect_sensitive_path_access,
    print_suspicious_report,
)


def main():
    parser = argparse.ArgumentParser(
        description="Analizor de log-uri de sistem"
    )

    # 1. DEFINIREA TUTUROR ARGUMENTELOR
    parser.add_argument("logfile", help="Fisierul de log (apache, nginx, syslog, custom)")
    parser.add_argument("--stats", action="store_true", help="Afiseaza statistici generale")
    parser.add_argument("--top_ips", type=int, metavar="N", help="Afiseaza top IP-uri")
    parser.add_argument("--spikes", action="store_true", help="Detecteaza spike-uri de erori")
    parser.add_argument("--suspicious", action="store_true", help="Detecteaza activitate suspecta")
    parser.add_argument("--report", choices=["html"], help="Genereaza raport (html)")
    parser.add_argument("--output", default="raport_complet.html", help="Fisierul HTML generat")

    # 2. O SINGURĂ CITIRE A ARGUMENTELOR
    args = parser.parse_args()

    # 3. ÎNCĂRCAREA DATELOR (O singură dată, după ce știm fișierul)
    entries = load_file(args.logfile)
    if not entries:
        print("Logul este gol sau nu a putut fi citit.")
        return

    print(f"\n✔ Log incarcat: {args.logfile}")
    print(f"✔ Total inregistrari: {len(entries)}\n")
    
    if args.top_ips:top_ip(entries)

    if args.stats: status(entries)

    if args.top_ips: top_ip(entries)
    
    if args.spikes: detect_error_spikes(entries)
    
    result_bruteforce=detect_bruteforce(entries)
    if args.suspicious:
        print_suspicious_report(result_bruteforce)
        detect_404_scans(entries)
        detect_sensitive_path_access(entries)

    if args.report == "html": run_report(args.logfile, args.output)


    

if __name__ == "__main__":
    main()





