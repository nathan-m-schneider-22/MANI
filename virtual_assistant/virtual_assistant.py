import imp
from .shortcuts import check_shortcut
from .outsourced_assistant import call_outsourced_API
# A virtual assistant class to handle VA functionality


class VirtualAssistant:
    def __init__(self, display):
        self.display_instance = display

    def get_result(self, input):
        shortcut = check_shortcut(input)
        if shortcut != None:
            input = shortcut
        self.display_instance.display_loading()
        result = call_outsourced_API(input)
        return result

    def teardown(self):
        pass
