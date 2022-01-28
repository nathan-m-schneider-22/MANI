"""
Not sure how the display is going to function
Leaving function declarations to help guide implementation

"""

# Display class for displaying the state and results of the other components


class Display:
    def __init__(self):
        pass

    # Display the state of the interpreter
    # For example, which letters have been observed, if the interpreter is waiting for a new letter,
    # or on cooldown after just observing a letter
    def display_state(self, state):
        print("Displaying State: ", state)

    # Display a loading screen while the outsourced VA is calling the API
    def display_loading(self):
        print("Displaying Loading")

    # Display the result of the Virtual Assistant
    def display_result(self, result):
        print("Displaying Result: ", result)
