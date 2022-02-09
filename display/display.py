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

message_queue = queue.Queue()


async def handler(websocket, path):
    while True:
        data = message_queue.get()
        print(data)

        await websocket.send(json.dumps(data))
        await asyncio.sleep(.25)


def start_loop():

    asyncio.set_event_loop(asyncio.new_event_loop())
    # new_loop.run_until_complete(start_server)
    # new_loop.run_forever()
    start_server = websockets.serve(handler, "127.0.0.1", 5000)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


class Display:
    def __init__(self, start_display=True):
        if start_display:
            startup_command = "cd frontend/my-app/ && npm run start &"
            os.system(startup_command)
        t = threading.Thread(target=start_loop)
        t.start()

    # Display the state of the interpreter
    # For example, which letters have been observed, if the interpreter is waiting for a new letter,
    # or on cooldown after just observing a letter

    def display_state(self, state):

        data = {
            "type": "screen update",
            "content": str(state)
        }
        message_queue.put(data)
        print("Displaying State: ", state)

    # Display a loading screen while the outsourced VA is calling the API
    def display_loading(self):
        print("Displaying Loading")

    # Display the result of the Virtual Assistant
    def display_result(self, result):
        print("Displaying Result: ", result)

    def teardown(self):
        pass
