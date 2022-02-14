from interpreter.interpreter import Interpreter
from display.display import Display
from virtual_assistant.virtual_assistant import VirtualAssistant
import argparse


class MANI:
    def __init__(self, args):
        self.display = Display(start_display=not args.run_logic)
        self.interpreter = Interpreter(self.display)
        self.virtual_assistant = VirtualAssistant(self.display)

    def main_loop(self):
        print("For this demo, since the google assistant only runs on the raspberry pi and we don't yet have a camera for the raspberry pi, we are going to take terminal input and see if that works")
        while True:
            input = input("ask the assistant something")
            result = self.virtual_assistant.get_result(input)
            if result:
                print(result)
            else:
                print("Sorry no response")

    def teardown(self):
        self.display.teardown()
        self.interpreter.teardown()
        self.virtual_assistant.teardown()


def main(args):
    mani_instance = MANI(args)
    try:
        mani_instance.main_loop()
    except:
        mani_instance.teardown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--logic', dest='run_logic', action='store_true',
                        help='run only the core logic, no display')

    args = parser.parse_args()
    main(args)
