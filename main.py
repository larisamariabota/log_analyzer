from loader import load_file
from report_html import generate_html_report

# ------------------------------------
#  IMPORTĂ FUNCȚIILE TALE REALE
#  (MODIFICI DOAR NUMELE FUNCȚIILOR)
# ------------------------------------

# Statistici generale
from meniu.statistici import status as compute_stats    

# Top IP-uri
from meniu.top_ip import top_ip as top_ip       

# Profilare IP
from grouping.profile_by_ip import profile_by_ip         

# Spike-uri pe erori (VERIFICĂ numele funcției din fișierul tău!)
from meniu.spike_error import detect_error_spike         

# Spike-uri trafic (IP și METHOD)
from meniu.spike_abuse import detect_spike_ip, detect_spike_method

# Suspicious patterns
from meniu.paterns import (
    detect_bruteforce,
    detect_404_scans,
    detect_sensitive_path_access
)

# ------------------------------------
#               MAIN
# ------------------------------------

def main():

    logfile = "test_logs/apache_300.log"

    # 1) Încarcă logul
    entries = load_file(logfile)
   
    if not entries:
        print("Logul este gol!")
        return

    print(" Log încarcat.")

    # 2) Statistici generale
    stats = compute_stats(entries)

    # 3) Top IP-uri
    top_ips_list = top_ip(entries)

    # 4) Profilare IP-uri
    profiles = profile_by_ip(entries)

    # 5) Spike-uri
    # 5) SPIKE-uri
    spike_errors = detect_error_spike(entries)
    spike_ip = detect_spike_ip(entries)
    spike_method = detect_spike_method(entries)

# Convertim booleanul din detect_error_spike intr-o lista
    if spike_errors:
     spike_errors_list = [{
        "type": "ERROR Spike",
        "count": stats["levels"].get("ERROR", 0),
        "interval": "Global",
        "message": "Spike de erori detectat in sistem."
    }]
    else:
     spike_errors_list = []

# Listele se aduna corect
    all_spikes = spike_errors_list + spike_ip + spike_method

    # 6) Activitate suspectă
    brute = detect_bruteforce(entries)
    scans = detect_404_scans(entries)
    sens = detect_sensitive_path_access(entries)

    suspicious = brute + scans + sens

    # 7) Generare raport HTML
    generate_html_report(
        filename=logfile,
        total_lines=len(entries),
        level_stats=stats["levels"],
        top_ips=top_ips_list,
        ip_profiles=profiles,
        spikes=all_spikes,
        suspicious_events=suspicious,
        output_path="raport_complet.html"
    )

    print("\nRaport generat: raport_complet.html")


if __name__ == "__main__":
    main()




 