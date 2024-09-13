import re
import time
import sys  # Importiere sys für exit()

# Variablen-Dictionary zum Speichern der Variablen
variables = {}

# Überprüfen, ob das Skript mit "!" beginnt
with open('source.txt', 'r', encoding='utf-8') as file:
    first_line = file.readline().strip()  # Erste Zeile lesen und Leerzeichen entfernen

if first_line.startswith("!"):
    # Wenn die erste Zeile ein "!" ist, schreibe den vorgegebenen Text in die Datei
    with open('source.txt', 'w', encoding='utf-8') as file:
        file.write("#include vls/libs/standarts\n")
        file.write('print_s("Hello World!")\n')
        file.write('var name = "Jonathan"\n')
        file.write('var alter = 12\n')
        file.write('print_s("Name: " + name)\n')
        file.write('print_n(alter)\n')
        file.write('print_sn("PI is: 3.141592653979323")\n')
    print("Inhalt wurde in die Datei geschrieben.")

# Datei öffnen und den Inhalt lesen
with open('source.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Text in einer Variablen speichern
lines = text.splitlines()  # Text in Zeilen aufteilen

# Überprüfen, ob die erste Zeile eine der gewünschten Includes ist
if lines:
    first_line = lines[0].strip()  # Erste Zeile lesen und Leerzeichen entfernen
    valid_includes = [
        "#include vls/libs/standarts",
        "#include n",
        "#include libs/dotLibary",
        "#include assets/extras/standart"
    ]

    is_lib_standarts_included = first_line == "#include vls/libs/standarts"

    if first_line in valid_includes:
        print("Text wird weiter gelesen...")

    # Überprüfen auf print_n(), print_s(), print_sn(), wait(), close() und var-Deklarationen
    for line in lines:
        line = line.strip()  # Leerzeichen entfernen

        # Variablen-Deklaration
        if line.startswith("var "):
            match = re.match(r'var (\w+) = "(.*)"', line)
            if match:
                var_name = match.group(1)
                var_value = match.group(2)
                variables[var_name] = var_value
                # print(f"{var_name}' gesetzt auf '{var_value}'")
                continue

            match = re.match(r'var (\w+) = (\d+)', line)
            if match:
                var_name = match.group(1)
                var_value = int(match.group(2))
                variables[var_name] = var_value
                # print(f"Variable '{var_name}' gesetzt auf {var_value}")
                continue

        # Ausgabe der Variablen
        if "print_n(" in line:
            if not is_lib_standarts_included:
                print("Error 1: Funktion wird von einer Library abgerufen, die nicht 'includet' ist!")
            else:
                match = re.search(r'print_n\((\w+|\d+)\)', line)  # Akzeptiere auch Zahlen
                if match:
                    var_name = match.group(1)
                    if var_name.isdigit():  # Überprüfe, ob es eine Zahl ist
                        print(f"Die Zahl ist: {var_name}")
                    elif var_name in variables:
                        print(f"Die Zahl ist: {variables[var_name]}")
                    else:
                        print(f"Error: Variable '{var_name}' ist nicht definiert!")
                else:
                    print("Error 1001: print_n() erwartet eine Zahl!")

        elif "print_s(" in line:
            if not is_lib_standarts_included:
                print("Error 1: Funktion wird von einer Library abgerufen, die nicht 'includet' ist!")
            else:
                match = re.search(r'print_s\("([^"]+)"\)', line)
                if match:
                    text_to_print = match.group(1)
                    # Ersetze Variablen im Text
                    for var_name, var_value in variables.items():
                        text_to_print = text_to_print.replace(var_name, str(var_value))
                    print(text_to_print)
                else:
                    # Überprüfung auf Variablenaufruf
                    match = re.search(r'print_s\((\w+|\d+)\)', line)  # Akzeptiere auch Zahlen
                    if match:
                        var_name = match.group(1)
                        if var_name.isdigit():  # Überprüfe, ob es eine Zahl ist
                            print(var_name)
                        elif var_name in variables:
                            print(variables[var_name])
                        else:
                            print(f"Error: Variable '{var_name}' ist nicht definiert!")
                    else:
                        print("Error 1002: print_s erwartet NUR Buchstaben!")

        elif "print_sn(" in line:
            if not is_lib_standarts_included:
                print("Error 1: Funktion wird von einer Library abgerufen, die nicht 'includet' ist!")
            else:
                match = re.search(r'print_sn\("([^"]*)"\)', line)
                if match:
                    text_to_print = match.group(1)
                    # Ersetze Variablen im Text
                    for var_name, var_value in variables.items():
                        text_to_print = text_to_print.replace(var_name, str(var_value))
                    print(text_to_print)

        elif "wait(" in line:
            match = re.search(r'wait\((\d+)\)\s*(timeshow (true|false))?', line)
            if match:
                seconds = int(match.group(1))
                timeshow = match.group(2)  # 'timeshow true' oder 'timeshow false'

                if timeshow == "timeshow true":
                    print(f"Warte für {seconds} Sekunden...")

                time.sleep(seconds)  # Warten für die angegebene Zeit
            else:
                print("Error: wait() erwartet eine Zahl!")

        elif "close(this)" in line:
            print("Fenster wird geschlossen...")
            sys.exit()  # Beendet das Skript

        elif "close()" in line:
            print("Error 345: Was soll geschlossen werden?")

    if not is_lib_standarts_included and any("print_" in line for line in lines):
        print("Error 1: Funktion wird von einer Library abgerufen, die nicht 'includet' ist!")

    if first_line not in valid_includes:
        print("Error 0, kein 'include' am Anfang, oder falsches 'including'")
else:
    print("Error 0, die Datei ist leer.")

# Warten auf Benutzereingabe, bevor das Fenster geschlossen wird
input("Drücke Enter, um das Fenster zu schließen...")