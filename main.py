import argparse
import sys
# biblioteca sys e folosita pentru a aparea diacritece in terminal
# bibliotecca argparse e folosita pentru a prelua argumentele din terminal si a le transforma  in variabile python
# pentru Unicode în terminal (Windows)
sys.stdout.reconfigure(encoding="utf-8")

from conversion.loader import load_file
from raport.creaza_raport import run_report

from meniu.bashboard_live import watch_log_live 
from meniu.statistici import status
from meniu.top_ip import top_ip,top_dangerous_ip
from meniu.spike_error import detect_error_spikes, print_spike_errors
from meniu.multi_task import filter_entries, print_filter
from meniu.spike_abuse import detect_all_spikes, print_alert_table


from meniu.paterns import (
    detect_bruteforce,  
    detect_404_scans,
    detect_sensitive_path_access,
    print_bruteforce_reports,
    print_404_scan_reports,
    print_sensitive_path
)

from output.output_ips import write_top_dangerous_ip_to_file, write_top_ip_to_file
from output.output_alert import write_alert_table_to_file
from output.output_spike import write_spike_to_file
from output.output_status import write_status_to_file
from output.output_filter_data import write_filter_to_file
from output.output_suspicious import write_bruteforce_reports_to_file,write_404_scan_reports_to_file,write_sensitive_path_to_file



def main():
    parser = argparse.ArgumentParser(
        description="Analizor de log-uri de sistem"
    )

    # 1. DEFINIREA TUTUROR ARGUMENTELOR
       # prima pozitie =comanda din terminal ,action= store_true//daca e comanda, atuci variabila e true, help= descrie e face comanda, e obtional
    parser.add_argument("--watch", action="store_true", help="Porneste dashboard live (citeste doar liniile noi)")
    parser.add_argument("--refresh", type=int, default=2, help="Refresh dashboard in secunde (default 2)")
    parser.add_argument("logfile", help="Fisierul de log (apache, nginx, syslog, custom)")
    parser.add_argument("--stats", action="store_true", help="Afiseaza statistici generale")
    parser.add_argument("--dangerous",action="store_true", help="Afiseaza top 10 IP-uri periculoase")
    parser.add_argument("--top_ips", action="store_true", help="Afiseaza top 10 IP-uri")
    parser.add_argument("--spikes", action="store_true", help="Detecteaza spike-uri de erori")
    parser.add_argument("--suspicious", action="store_true", help="Detecteaza activitate suspecta")
    parser.add_argument("--filter", help="Filtreaza dupa text sau level (ex: ERROR, TypeError)")
    parser.add_argument("--date", help="Filtreaza dupa data (YYYY-MM-DD)")
    parser.add_argument("--alert", action="store_true", help="Afiseaza alertele de securitate detectate")
    parser.add_argument("--report", choices=["html"], help="Genereaza raport (html)")
    parser.add_argument("--output", default="raport_complet.html", help="Fisierul HTML generat")
    parser.add_argument("--serve", action="store_true", help="Porneste un link in browser pentru raport")

    # 2. O SINGURĂ CITIRE A ARGUMENTELOR
    #parser.parse_args() //parseaza argumentele din terminal si le transfornma in variabile python
    args = parser.parse_args()   #args devine un obiect cu toate argumentele ca atribute

    # 3. ÎNCĂRCAREA DATELOR (O singură dată, după ce știm fișierul)
    entries = load_file(args.logfile)
    if not entries:
        print("Logul este gol sau nu a putut fi citit.")
        return

    print(f"\n✔ Log incarcat: {args.logfile}")
    print(f"✔ Total inregistrari: {len(entries)}\n")
    
    if args.top_ips:
       if args.dangerous: 
          top_dangerous_ip(entries)
          write_top_dangerous_ip_to_file(entries)
       else: 
          top_ip(entries)
          write_top_ip_to_file(entries)


    if args.stats:
       status(entries)
       write_status_to_file(entries)
   

    if args.spikes:
       spikes=detect_error_spikes(entries)
       print_spike_errors(spikes)
       write_spike_to_file(spikes)
      

    if args.alert:
        spike=detect_all_spikes(entries)
        print_alert_table(spike)  
        write_alert_table_to_file(spike)

    if args.suspicious:
        # initializam listele pentru rezultatele detectiilor
      result_bruteforce=detect_bruteforce(entries)
      result_404=detect_404_scans(entries)
      sensitive_path=detect_sensitive_path_access(entries)

      print_bruteforce_reports(result_bruteforce),
      print_404_scan_reports(result_404),
      print_sensitive_path(sensitive_path),
      write_bruteforce_reports_to_file(result_bruteforce),
      write_404_scan_reports_to_file(result_404),
      write_sensitive_path_to_file(sensitive_path)


    if args.report == "html":
      run_report(args.logfile, args.output)
      print(f"✔ Raport HTML generat cu succes: {args.output}")

    if args.serve:
        import http.server, socketserver, os

        port = 8000
        os.chdir(os.path.dirname(args.output) or ".")
        print(f"🌐 Link: http://localhost:{port}/{os.path.basename(args.output)}")

        with socketserver.TCPServer(("0.0.0.0", port), http.server.SimpleHTTPRequestHandler) as httpd:
            httpd.serve_forever()


     


    filtered_entries = entries

# aplicam filtrele DOAR daca sunt date
    if args.filter or args.date:
     filtered_entries = filter_entries(
            entries,
            text_filter=args.filter,
            date_filter=args.date
        )
     print_filter(filtered_entries)
     write_filter_to_file(filtered_entries)

     if args.watch:
       watch_log_live(
        args.logfile,
        refresh=args.refresh,
        stats=args.stats,
        top=args.top_ips,
        dangerous=args.dangerous,
        alert=args.alert,
        suspicious=args.suspiciuos
    )
    return

if __name__ == "__main__":
    main()






