import webbrowser
import os

from loader import load_file
from raport.report_html import generate_html_report

from meniu.statistici import status
from meniu.top_ip import top_ip, top_dangerous_ip
from grouping.profile_by_ip import profile_by_ip
from meniu.spike_error import detect_error_spikes
from meniu.defectiuni import defectiuni_sistem
from meniu.paterns import (
    detect_bruteforce,
    detect_404_scans,
    detect_sensitive_path_access
)


def run_report(logfile, output="raport_complet.html"):
    entries = load_file(logfile)
    if not entries:
        print("Logul este gol!")
        return

    stats = status(entries)
    top_ips_list = top_ip(entries)
    dangerous_list = top_dangerous_ip(entries)
    profiles = profile_by_ip(entries)
    spikes = detect_error_spikes(entries)

    suspicious = (
        detect_bruteforce(entries)
        + detect_404_scans(entries)
        + detect_sensitive_path_access(entries)
    )

    defect = defectiuni_sistem(entries)

    generate_html_report(
        filename=logfile,
        total_lines=len(entries),
        level_stats=stats["levels"],
        top_ips=top_ips_list,
        ip_profiles=profiles,
        spikes=spikes,
        suspicious_events=suspicious,
        top_dangerous_ip=dangerous_list,
        defect=defect,
        output_path=output,
    )

    #  DUPĂ ce raportul a fost creat
    abs_path = os.path.abspath(output)

    print("\nRaport HTML generat cu succes")
    print(f" Locație: {abs_path}")
    print(" Se deschide în browser...")

    webbrowser.open(f"file:///{abs_path}")


