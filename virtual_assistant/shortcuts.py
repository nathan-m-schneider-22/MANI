import time

shortcuts = {"BBC": "What is the news from the BBC?"}
answers = {"BBC": "Unable to connect to the BBC"}


def check_shortcut(input):
    if input in shortcuts.keys():
        return shortcuts[input]

    else:
        return None


def get_shortcut_answer(input):
    return answers[input]
