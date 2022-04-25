import csv

shortcuts = dict()
with open('shortcuts.csv', newline='\n') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        shortcuts[row["Shortcut"]] = row["Query"]

def check_shortcut(input):
    input = input.lower()
    if input in shortcuts.keys():
        return shortcuts[input]
    else:
        return None
