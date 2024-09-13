import os
import shutil

def read_terminal_file():
    # Überprüfen, ob die Datei existiert
    if not os.path.isfile('terminal.txt'):
        print("Die Datei 'terminal.txt' wurde nicht gefunden.")
        return

    with open('terminal.txt', 'r') as file:
        for line in file:
            line = line.strip()  # Entfernen von Leerzeichen und Zeilenumbrüchen
            if "dot inst VLS in" in line:
                # Extrahiere den Namen der Variable
                parts = line.split("in")
                if len(parts) > 1:
                    variable_name = parts[1].strip()
                    copy_files_to_variable(variable_name)

def copy_files_to_variable(variable_name):
    # Quelle und Ziel festlegen
    source_folder = os.path.join(os.getcwd(), "datas")
    target_folder = os.path.join(os.getcwd(), variable_name)

    # Überprüfen, ob der Quellordner existiert
    if not os.path.isdir(source_folder):
        print(f"Der Ordner '{source_folder}' wurde nicht gefunden.")
        return

    # Zielordner erstellen, falls nicht vorhanden
    os.makedirs(target_folder, exist_ok=True)

    # Dateien kopieren
    for item in os.listdir(source_folder):
        s = os.path.join(source_folder, item)
        d = os.path.join(target_folder, item)
        if os.path.isfile(s):
            shutil.copy2(s, d)  # Dateien kopieren
            print(f"Datei '{item}' wurde nach '{target_folder}' kopiert.")

    # Benutzer nach dem Installationspfad fragen
    install_path = input("Geben Sie den Installationspfad ein (oder '.' für den aktuellen Ordner): ")
    if install_path == ".":
        install_path = os.getcwd()

    install_files(target_folder, install_path)

def install_files(source_folder, install_path):
    # Dateien vom Quell- zum Zielordner kopieren
    for item in os.listdir(source_folder):
        s = os.path.join(source_folder, item)
        d = os.path.join(install_path, item)
        if os.path.isfile(s):
            shutil.copy2(s, d)  # Dateien kopieren
            print(f"Datei '{item}' wurde in '{install_path}' installiert.")

if __name__ == "__main__":
    read_terminal_file()

input("ENTER drücken, um VLS Terminal zu schließen...")