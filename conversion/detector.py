from .apache import is_apache, parse_apache
from .json import is_json, parse_json
from .nginx_error import is_nginx_error,parse_nginx_error
from.nginx_access import is_nginx_access,parse_nginx_access
from .syslog import is_syslog , parse_syslog
from .custom import parse_custom
def parse_line(line):
  line=line.strip() #sterge statiile inutile de la inceput si sfarsit

 
  if is_nginx_access(line):
    return parse_nginx_access(line)

  elif is_nginx_error(line):
    return parse_nginx_error(line)
  elif is_apache(line):
    return parse_apache(line)
  elif is_nginx_access(line):
    return parse_nginx_access(line)
  elif is_json(line):
    return parse_json(line)
  elif is_syslog(line):
    return parse_syslog(line)
  else:
     return parse_custom(line)
   