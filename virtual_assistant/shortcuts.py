import time

shortcuts = {"BBC": "What is the news from the BBC?",
            "WH": "What is the weather in Hanover, New Hampshire?",
            "POKI": "How many pounds in a kilogram?",
            "HOL": "When is the next federal holiday?",
            "CD": "What is the current date?",
            "DAN": "What is the definition of anthropomorphize?",
            "HLW": "How large is a blue whale?"}


def check_shortcut(input):
    if input in shortcuts.keys():
        return shortcuts[input]

    else:
        return None


# def get_shortcut_answer(input):
#     return answers[input]
