import time

shortcuts = {"bc": "What is the news from the BBC?",
             "wh": "What is the weather in Hanover, New Hampshire?",
             "poki": "How many pounds in a kilogram?",
             "hol": "When is the next federal holiday?",
             "cd": "What is the current date?",
             "dan": "What is the definition of anthropomorphize?",
             "hlw": "How large is a blue whale?",
             "cal": "What'on on my calendar"}


def check_shortcut(input):
    if input.lower() in shortcuts.keys():
        return shortcuts[input]
    else:
        return None
