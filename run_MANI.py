import socket
import threading
from interpreter.interpreter import Interpreter
from display.display import Display
from virtual_assistant.virtual_assistant import VirtualAssistant
import interpreter.streamer as streamer
import argparse
import time
import logging


class MANI:
    def __init__(self, args):
        self.display = Display(start_display=not args['run_logic'])
        self.interpreter = Interpreter(self.display)
        self.virtual_assistant = VirtualAssistant(self.display,mock_va=bool(args['mock_va']))

    def main_loop(self):
        self.display.display_state("sleep")
        while True:
            print("Starting Main Loop")
            self.interpreter.wait_for_input()
            self.display.display_reset()
            input = self.interpreter.capture_full_input()
            if input != "":
                streamer.display_raw_frame = True
                result = self.virtual_assistant.get_result(input)
                streamer.display_raw_frame = False
                self.display.display_state("display", {"response": result})
                self.display.display_result(result)
                # time.sleep(5)

    def teardown(self):
        print("Tearing down")
        self.display.teardown()
        self.interpreter.teardown()
        self.virtual_assistant.teardown()


def main(args):
    print(args)

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
    parser.add_argument('--mock', dest='mock_va', action='store_true',
                        help='use mock responses for VA, not requiring')

    args = vars(parser.parse_args())
    t = threading.Thread(target=main, args=(args,))
    t.daemon = True
    t.start()

    streamer.app.run(host='127.0.0.1', port='5555', debug=True,
            threaded=True, use_reloader=False)
