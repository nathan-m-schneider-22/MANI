import imp

from numpy import short
from .shortcuts import check_shortcut
from .outsourced_assistant import call_outsourced_API
import time
# A virtual assistant class to handle VA functionality


class VirtualAssistant:
    def __init__(self, display,mock_va = False):
        self.display_instance = display
        self.mock_va = mock_va


    def get_result(self, input):
        print("Checking shortcut")
        shortcut = check_shortcut(input)
        self.display_instance.display_loading()

        if shortcut != None:
            print("Found: ", shortcut)
            input = shortcut

        self.display_instance.display_state("send", {"input": input})
        if self.mock_va:
            time.sleep(3)
            print("Using mock VA response")
            return "Mock VA response"
        else:
            result = call_outsourced_API(input)
            print("Result: ", result)
            result = result[0].upper() + result[1:]
            return result


    def teardown(self):
        pass
