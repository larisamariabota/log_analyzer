from loader import load_file
from report_html import generate_html_report
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Statistici generale
from meniu.statistici import status    

# Top IP-uri
from meniu.top_ip import top_ip, top_dangerous_ip  

# Profilare IP-uri
from grouping.profile_by_ip import profile_by_ip         

# Spike-uri
from meniu.spike_abuse import detect_all_spikes

# Suspicious patterns
from meniu.paterns import (
    detect_bruteforce,
    detect_404_scans,
    detect_sensitive_path_access
)


def main():

    logfile = "test_logs/json_300.log"

    # 1) Load file
    entries = load_file(logfile)
    if not entries:
        print("Logul este gol!")
        return

    print(" Log încărcat.")

    # 2) Statistici
    stats = status(entries)

    # 3) TOP IP-uri
    top_ips_list = top_ip(entries)

    # >>> AICI SALVĂM lista reală de IP-uri periculoase
    dangerous_list = top_dangerous_ip(entries)

    # 4) Profilare IP
    profiles = profile_by_ip(entries)

    # 5) Spike-uri
    spikes = detect_all_spikes(entries)

    # 6) Activitate suspectă
    brute = detect_bruteforce(entries)
    scans = detect_404_scans(entries)
    sens = detect_sensitive_path_access(entries)

    suspicious = brute + scans + sens

    # 7) Generare raport HTML (corect!)
    generate_html_report(
        filename=logfile,
        total_lines=len(entries),
        level_stats=stats["levels"],
        top_ips=top_ips_list,
        ip_profiles=profiles,
        spikes=spikes,
        suspicious_events=suspicious,
        output_path="raport_complet.html",

        # suplimentare pentru secțiuni premium
        top_dangerous_ip=dangerous_list,
        suspicious_events_full=suspicious
    )

    #print("\n Raport generat: raport_complet.html")

    # debug
    print("\n=== SPIKES DEBUG ===")
    for s in spikes:
        print(s)

    print("\n=== DANGEROUS IPs DEBUG ===")
    print(dangerous_list)

    print("\n=== SUSPICIOUS DEBUG ===")
    for e in suspicious:
      print(e)

if __name__ == "__main__":
    main()





 