import argparse
import sys
# biblioteca sys e folosita pentru a aparea diacritece in terminal
# bibliotecca argparse e folosita pentru a prelua argumentele din terminal si a le transforma  in variabile python
# pentru Unicode în terminal (Windows)
sys.stdout.reconfigure(encoding="utf-8")

from conversion.loader import load_file
from raport.creaza_raport import run_report


from meniu.statistici import status
from meniu.top_ip import top_ip,top_dangerous_ip
from meniu.spike_error import detect_error_spikes, print_spike_errors
from meniu.multi_task import filter_entries, print_filter


from meniu.paterns import (
    detect_bruteforce,  
    detect_404_scans,
    detect_sensitive_path_access,
    print_bruteforce_reports,
    print_404_scan_reports,
    print_sensitive_path
)


def main():
    parser = argparse.ArgumentParser(
        description="Analizor de log-uri de sistem"
    )

    # 1. DEFINIREA TUTUROR ARGUMENTELOR
    parser.add_argument("logfile", help="Fisierul de log (apache, nginx, syslog, custom)")
    parser.add_argument("--stats", action="store_true", help="Afiseaza statistici generale")
    parser.add_argument("--dangerous",action="store_true", help="Afiseaza top 10 IP-uri periculoase")
    parser.add_argument("--top_ips", action="store_true", help="Afiseaza top 10 IP-uri")
    parser.add_argument("--spikes", action="store_true", help="Detecteaza spike-uri de erori")
    parser.add_argument("--suspicious", action="store_true", help="Detecteaza activitate suspecta")
    parser.add_argument("--filter", help="Filtreaza dupa text sau level (ex: ERROR, TypeError)")
    parser.add_argument("--date", help="Filtreaza dupa data (YYYY-MM-DD)")
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
    
    if args.top_ips:
       if args.dangerous: top_dangerous_ip(entries)
       else: top_ip(entries)
      
    if args.stats: status(entries)
    
   
    if args.spikes:
       spikes=detect_error_spikes(entries)
       print_spike_errors(spikes)
      


    if args.suspicious:
        # initializam listele pentru rezultatele detectiilor
      result_bruteforce=detect_bruteforce(entries)
      result_404=detect_404_scans(entries)
      sensitive_path=detect_sensitive_path_access(entries)

      print_bruteforce_reports(result_bruteforce),
      print_404_scan_reports(result_404),
      print_sensitive_path(sensitive_path)

    if args.report == "html": run_report(args.logfile, args.output)

    filtered_entries = entries

# aplicam filtrele DOAR daca sunt date
    if args.filter or args.date:
     filtered_entries = filter_entries(
            entries,
            text_filter=args.filter,
            date_filter=args.date
        )
     print_filter(filtered_entries)
     
if __name__ == "__main__":
    main()






