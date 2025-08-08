import json
import csv

# Načti JSON soubor
with open("zabbix_export.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Najdi všechny názvy položek (items -> name)
names = []
hosts = data.get("zabbix_export", {}).get("hosts", [])
for host in hosts:
    items = host.get("items", [])
    for item in items:
        name = item.get("name")
        if name:
            names.append([name])  # jako seznam kvůli CSV řádkům

# Ulož do CSV
with open("vystup.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name"])  # hlavička
    writer.writerows(names)

print("Hotovo. Výstup je uložen jako 'vystup.csv'")
