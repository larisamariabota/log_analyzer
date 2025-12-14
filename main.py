import argparse
import sys

# pentru Unicode în terminal (Windows)
sys.stdout.reconfigure(encoding="utf-8")

from loader import load_file
from raport.creaza_raport import run_report

# funcțiile tale existente
from meniu.statistici import status
from meniu.top_ip import top_ip
from meniu.spike_error import detect_error_spikes
from meniu.paterns import (
    detect_bruteforce,
    detect_404_scans,
    detect_sensitive_path_access
)


def main():
    parser = argparse.ArgumentParser(
        description="Analizor de log-uri de sistem"
    )

    # =========================
    # ARGUMENT OBLIGATORIU
    # =========================
    parser.add_argument(
        "logfile",
        help="Fisierul de log (apache, nginx, syslog, custom)"
    )

    # =========================
    # OPȚIUNI CLI
    # =========================
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Afiseaza statistici generale"
    )

    parser.add_argument(
        "--top_ips",
        type=int,
        metavar="N",
        help="Afiseaza top N IP-uri"
    )

    parser.add_argument(
        "--spikes",
        action="store_true",
        help="Detecteaza spike-uri de erori"
    )

    parser.add_argument(
        "--suspicious",
        action="store_true",
        help="Detecteaza activitate suspecta (bruteforce, 404, path-uri sensibile)"
    )

    parser.add_argument(
        "--report",
        choices=["html"],
        help="Genereaza raport (html)"
    )

    parser.add_argument(
        "--output",
        default="raport_complet.html",
        help="Fisierul HTML generat"
    )

    args = parser.parse_args()

    # =========================
    # ÎNCARCĂ LOGUL O SINGURĂ DATĂ
    # =========================
    entries = load_file(args.logfile)
    if not entries:
        print("Logul este gol sau nu a putut fi citit.")
        return

    print(f"\n✔ Log incarcat: {args.logfile}")
    print(f"✔ Total inregistrari: {len(entries)}\n")

    # =========================
    # EXECUTĂ COMENZILE CLI
    # =========================

    if args.stats:
        status(entries)

    if args.top_ips:
        print(f"\nTop {args.top_ips} IP-uri:")
        top_ip(entries, args.top_ips)

    if args.spikes:
        detect_error_spikes(entries)

    if args.suspicious:
        print("\n=== ACTIVITATE SUSPECTA ===")
        detect_bruteforce(entries)
        detect_404_scans(entries)
        detect_sensitive_path_access(entries)

    if args.report == "html":
        run_report(args.logfile, args.output)

    print("\n✔ Analiza finalizata.")


if __name__ == "__main__":
    main()




 