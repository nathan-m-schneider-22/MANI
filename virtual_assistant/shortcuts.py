shortcuts = {
    "a": "What time is it?",
    "www": "What is the weather like now?",
    "ttt": "What time is it?"
}


def check_shortcut(input):
    if input in shortcuts.keys():
        return shortcuts[input]

    else:
        return None
