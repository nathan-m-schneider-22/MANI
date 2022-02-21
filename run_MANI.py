from interpreter.interpreter import Interpreter
from display.display import Display
from virtual_assistant.virtual_assistant import VirtualAssistant
import argparse
import time


class MANI:
    def __init__(self, args):
        self.display = Display(start_display=not args.run_logic)
        self.interpreter = Interpreter(self.display)
        self.virtual_assistant = VirtualAssistant(self.display)

    def main_loop(self):
        while True:
            print("Starting Main Loop")
            self.interpreter.wait_for_input()
            self.display.display_reset()
            input = self.interpreter.capture_full_input()
            if input != "":
                result = self.virtual_assistant.get_result(input)
                self.display.display_state("display", {"response": result})
                self.display.display_result(result)

    def teardown(self):
        print("Tearing down")
        self.display.teardown()
        self.interpreter.teardown()
        self.virtual_assistant.teardown()


def main(args):
    mani_instance = MANI(args)
    try:
        mani_instance.main_loop()
    except Exception as e:
        mani_instance.teardown()
        raise(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--logic', dest='run_logic', action='store_true',
                        help='run only the core logic, no display')

    args = parser.parse_args()
    main(args)
