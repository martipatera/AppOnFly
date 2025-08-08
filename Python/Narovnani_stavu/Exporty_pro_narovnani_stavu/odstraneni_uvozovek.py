import csv
import tempfile
import os

input_file = r'C:\Users\pater\Desktop\Složky\AppOnFly\Python\Narovnani_stavu\Exporty_pro_narovnani_stavu\hyper-v_slozky.csv'  # Cesta k původnímu CSV souboru, který chceme upravit

# Vytvoření dočasného souboru pro bezpečnou úpravu obsahu
# 'w' = write mód, delete=False = soubor se po zavření nesmaže
# newline='' = správná práce s novými řádky
# encoding='utf-8' = správné čtení českých znaků
with tempfile.NamedTemporaryFile('w', delete=False, newline='', encoding='utf-8') as tmpfile:
    writer = csv.writer(tmpfile)  # připravíme writer pro zápis do dočasného souboru

    # Otevřeme původní soubor pro čtení
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)  # připravíme reader pro čtení CSV řádek po řádku
        
        # Pro každý řádek v souboru
        for row in reader:
            # Odstraníme uvozovky z každé buňky v řádku
            cleaned_row = [cell.strip('"') for cell in row]

            # Zapíšeme upravený řádek do dočasného souboru
            writer.writerow(cleaned_row)

# Přepíšeme původní soubor obsahem dočasného souboru
os.replace(tmpfile.name, input_file)

# Výpis do konzole
print(f"Soubor '{input_file}' byl úspěšně přepsán bez uvozovek.")
