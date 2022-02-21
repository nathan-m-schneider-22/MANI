"""
Not sure how the display is going to function
Leaving function declarations to help guide implementation

"""
import os

# Display class for displaying the state and results of the other components
import asyncio
import datetime
from tracemalloc import start
import websockets
import json
import threading
import queue
import time
import cv2
import base64

message_queue = queue.Queue()


async def handler(websocket, path):
    while True:
        data = message_queue.get()
        await websocket.send(json.dumps(data))
        await asyncio.sleep(.25)


def start_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websockets.serve(handler, "127.0.0.1", 5000))
    loop.run_forever()


class Display:
    def __init__(self, start_display=True):
        if start_display:
            startup_command = "cd frontend/my-app/ && npm run start &"
            os.system(startup_command)
            time.sleep(8)
        t = threading.Thread(target=start_loop)
        t.start()

    # Display the state of the interpreter
    # For example, which letters have been observed, if the interpreter is waiting for a new letter,
    # or on cooldown after just observing a letter

    def display_image(self, image):
        # print("displaying frame")

        retval, buffer = cv2.imencode('.jpg', image)
        base64jpg = base64.b64encode(buffer)
        base64str = base64jpg.decode('utf-8')
        data = {
            "type": "image",
            "image": base64str
        }
        message_queue.put(data)
        message_queue.put(data)

        
    def display_query(self, state):

        data = {
            "type": "query",
            "content": str(state)
        }
        print("Displaying Query: ", state)
        message_queue.put(data)
        message_queue.put(data)

    # Display a loading screen while the outsourced VA is calling the API
    def display_loading(self):
        data = {
            "type": "loading",
        }
        message_queue.put(data)
        message_queue.put(data)
        print("Displaying Loading")

    def display_reset(self):
        data = {
            "type": "reset",
        }
        print("Displaying reset")
        message_queue.put(data)
        message_queue.put(data)

    # Display the result of the Virtual Assistant

    def display_result(self, result):
        data = {
            "type": "response",
            "content": str(result)
        }
        print("Displaying Result: ", result)
        message_queue.put(data)
        message_queue.put(data)

    def teardown(self):
        pass


def main():
    d = Display(start_display=False)

    i = 0
    while True:
        d.display_query(i)
        i += 1
        time.sleep(1)


if __name__ == "__main__":
    main()
