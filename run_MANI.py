from interpreter.interpreter import Interpreter
from display.display import Display
from virtual_assistant.virtual_assistant import VirtualAssistant


class MANI:
    def __init__(self):
        self.display = Display()
        self.interpreter = Interpreter(self.display)
        self.virtual_assistant = VirtualAssistant(self.display)

    def main_loop(self):
        while True:
            print("Starting Main Loop")
            self.interpreter.wait_for_input()
            input = self.interpreter.capture_full_input()
            result = self.virtual_assistant.get_result(input)
            self.display.display_result(result)

    def teardown(self):
        self.display.teardown()
        self.interpreter.teardown()
        self.virtual_assistant.teardown()


def main():
    mani_instance = MANI()
    try:
        mani_instance.main_loop()
    except:
        mani_instance.teardown()


if __name__ == "__main__":
    main()
