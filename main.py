from loader import load_file
from report_html import generate_html_report
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Statistici generale
from meniu.statistici import status as status    

# Top IP-uri
from meniu.top_ip import top_ip,top_dangerous_ip  

# Profilare IP-uri
from grouping.profile_by_ip import profile_by_ip         

# Spike-uri bazate pe profile_by_ip 
from meniu.spike_abuse import detect_all_spikes

# Suspicious patterns
from meniu.paterns import (
    detect_bruteforce,
    detect_404_scans,
    detect_sensitive_path_access
)


def main():

    logfile = "test_logs/nginx.log"

    # 1) Încarcă logul
    entries = load_file(logfile)
   
    if not entries:
        print("Logul este gol!")
        return

    print(" Log încarcat.")
    
    # generam informatiile generale pentru raport
    # 2) Statistici generale
    stats = status(entries)

    # 3) Top IP-uri
    top_ips_list = top_ip(entries)
    top_dangerous_ip(entries)
    # 4) Profilare IP-uri
    profiles = profile_by_ip(entries)

    # 5) SPIKE-uri ( TOTUL vine din profile_by_ip)
    spikes = detect_all_spikes(entries)

    # 6) Activitate suspectă
    brute = detect_bruteforce(entries)
    scans = detect_404_scans(entries)
    sens = detect_sensitive_path_access(entries)

    suspicious = brute + scans + sens

    # 7) Generare raport HTML
    #raportul html va include toate informatiile colectate mai sus
    generate_html_report(
        filename=logfile,
        total_lines=len(entries),
        level_stats=stats["levels"],     
        top_ips=top_ips_list,                
        ip_profiles=profiles,                
        spikes=spikes,                        # ← NOUL sistem de spike-uri
        suspicious_events=suspicious,      
      
        output_path="raport_complet.html"
    )

    print("\n Raport generat: raport_complet.html")

    spikes = detect_all_spikes(entries)
    print("\n=== SPIKES DEBUG ===")
    for s in spikes:
     print(s)

if __name__ == "__main__":
    main()



 