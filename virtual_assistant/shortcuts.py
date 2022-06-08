import csv
import re

shortcuts = dict()
with open('shortcuts.csv', newline='\n') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        shortcuts[row["Shortcut"]] = row["Query"]

def check_shortcut(input):
    input = input.lower()
    for key in shortcuts.keys():
        expression = re.fullmatch(key, input)
        if expression != None: 
            input = shortcuts[key].format(*expression.groups())
            return input
    else:
        return None
