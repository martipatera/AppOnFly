import json
import csv
import re
from collections import Counter

subjects = []
descriptions = []

with open("Python/tickets.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)


with open("Python/tickets_short.csv", "w", encoding="utf-8", newline="") as csv_file:
    write = csv.writer(csv_file)
    write.writerow(["subject","description"])

# pretty = json.dumps(data["tickets"][0], indent=2, ensure_ascii=False) #json.dumps prevadi JSON na string

# print (pretty) #print pouze pro orientaci v .json

    for ticket in data["tickets"]:

        write.writerow([ticket.get("subject", ""), ticket.get("description", "")]) #zapise subject a description do radku, pokud nic neni tak zapise ""


with open ("Python/tickets_short.csv", "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
                subject = row["subject"].strip().lower()
                description = row["description"].lower()
                descriptions += re.findall(r"\b\w{4,}\b", description) #jen slova s 4 a vice pismen
                if subject:
                        subjects.append(subject)

subject_counter = Counter(subjects)
description_counter = Counter(descriptions)

with open("Python/tickets_count.csv", "w", encoding="utf-8", newline="") as csv_file:
    write = csv.writer(csv_file)
    write.writerow(["subject","count"])

    for subject, count in subject_counter.most_common():
        
        write.writerow([subject, count])
