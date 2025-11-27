from loader import load_file
from grouping.profile_by_ip import profile_by_ip
from printer import print_ip_profiles

if __name__ == "__main__":
    lista = load_file("test_logs/apache_300.log")
    grouped = profile_by_ip(lista)
    print_ip_profiles(grouped)


 