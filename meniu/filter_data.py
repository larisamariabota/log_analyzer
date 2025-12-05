def filter_errors(entries):
    errors=[]
    for entry in entries:
            level=entry.get("level")
            if level in("ERROR" ,"WARN"):
                 errors.append(entry)
    return errors

# returneaza doar datele de dupa o anumita data

def filter_after_date(entries,data):
         filtered=[]
         for entry in entries:
                ts=entry.get("timestamp")   # extrag doar gupul de timestmp
                if ts and ts>data:
                       filtered.append(entry)
         return filtered

#returneaza dupa interval de date

def filter_date_range(entries, start_date, end_date):
       filtered=[]
       for entry in entries:
                ts=entry.get("timestamp")
                if ts and start_date <= ts <= end_date:
                          filtered.append(entry)
                return filtered
       
              