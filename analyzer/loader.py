from conversion.detector import parse_line

def load_file(path):
    entries = []                     # facem lista pentru toate liniile parse
    with open(path, "r") as f:      # deschide fisierul in modul read
        for line in f:              # ia fiecare linie pe rand
            line = line.strip()     # sterge spatiile si \n

            if not line:            # daca linia e goala → sari
                continue

            parsed = parse_line(line)   # parseaza linia

            if parsed is not None:      # daca e valida
                entries.append(parsed)  # adaugam dictionarul la lista

    return entries   # return dupa ce am citit TOT fisierul
