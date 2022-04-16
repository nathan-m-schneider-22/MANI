shortcuts = {"bc": "What is the news from the BBC?",
             "wh": "What is the weather in Hanover, New Hampshire?",
             "poki": "How many pounds in a kilogram?",
             "hol": "When is the next federal holiday?",
             "cd": "What is the current date?",
             "dan": "What is the definition of anthropomorphize?",
             "hlw": "How large is a blue whale?",
             "cal": "What'on on my calendar",
             "cnn": "Whats the news from CNN?",
             "gs": "What is the nearest grocery store?",
             "gl": "Turn on the garage lights",
             "al": "Arm the house alarm",
             "am": "Add milk to my shopping list",
             "tse": "Set the thermostat to 68 degrees",
             "asam": "Set an alarm for 7 AM"}


def check_shortcut(input):
    input = input.lower()
    if input in shortcuts.keys():
        return shortcuts[input]
    else:
        return None
