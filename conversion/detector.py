#from .apache import is_apache, parse_apche
from .json import is_json, parse_json
from .nginx import is_nginx, parse_nginx
from .syslog import is_syslog , parse_syslog
from .custom import parse_custom
def parse_line(line):
  line=line.strip() #sterge statiile inutile de la inceput si sfarsit

# if is_apache(line):
# return parse_apache(line)
  if is_nginx(line):
    return parse_nginx(line)
  elif is_json(line):
    return parse_json(line)
  elif is_syslog(line):
    return parse_syslog(line)
  else:
     return parse_custom(line)
  