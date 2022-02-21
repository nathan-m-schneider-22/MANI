import time

shortcuts = {"bbc": "What is the news from the BBC?",
             "co": "Whats the number of active covid cases in new hampshire?"}


def check_shortcut(input):
    if input.lower() in shortcuts.keys():
        return shortcuts[input]
    else:
        return None
