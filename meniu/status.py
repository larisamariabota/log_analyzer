from collections import Collection
# aceasta biblioteca numara elementele dintr o colectie si returneaza un dictionar cu elementele si nr de aparitii

from datetime import datetime

def status(entries):
     print("Analiză Log-uri")
     print("=" * 60)
     if not entries:
        print("⚠️  Nu s-au găsit înregistrări.")
        return 
     
     total_entries=len(entries) # numarul toatl de linii din dictionarul standard 
     print(f"Total inregistrari:{total_entries}") # am pus f pt a afisa variabila

     timestamp=[entry.get("timestamp") for entry in entries if entry.get("timestamp")]  #extragem toate timestampurile din dictionar
     if timestamp:
         first_date=min(timestamp)
         last_date=max(timestamp)
         print(f"Periaoda analizata:{first_date}-{last_date}")
      
     levels={}
     for entry in entries:
            level=entry.get("level")
            if level:
                    levels[level]=levels.get(level,0)+1


# afișăm cu procent
     print("Distribuție pe niveluri:")
     for level, count in levels.items():
       procent = (count / total_entries) * 100
     print(f"  {level:<6}: {count} ({procent:.2f}%)")  #:<6 aliniaza la stanga cu 6 spatii, 2f =2 zecimale
     print("="*60)
          
     