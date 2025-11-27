
from analyzer.loader import load_file
from analyzer.group_level import count_by_level
if __name__ == "__main__":
  lista=[]
  lista=load_file("test_logs/syslog_500.log")

  grouped=count_by_level(lista)
  print(grouped)
 