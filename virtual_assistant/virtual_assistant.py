import imp

from numpy import short
from .shortcuts import check_shortcut, get_shortcut_answer
from .outsourced_assistant import call_outsourced_API
import time
# A virtual assistant class to handle VA functionality


class VirtualAssistant:
    def __init__(self, display):
        self.display_instance = display

    def get_result(self, input):

        shortcut = check_shortcut(input)
        self.display_instance.display_state("send", {"input": shortcut})
        self.display_instance.display_loading()

        if shortcut != None:
            input = shortcut
            answer = get_shortcut_answer(input)
            if answer:
                time.sleep(2)  # TAKE OUT IN FINAL VERSION
                return answer
        time.sleep(2)  # TAKE OUT IN FINAL VERSION
        result = call_outsourced_API(input)
        return result

    def teardown(self):
        pass
