
from typing import Optional
import pytest

from ministate.statemachine import State, StateMachine, Event


class Idle(State):
    def __init__(self):
        super().__init__()

    def process(self, event: "Event") -> Optional["State"]:
        print(f"Idle state processing event: {event.name}")
        if event.name in self.model.machine.transitions[self.name]:
            return self.model.machine.transitions[self.name][event.name]
        return self


class Receiving(State):
    def __init__(self):
        super().__init__()

    def process(self, event: "Event") -> Optional["State"]:
        print(f"Processing state processing event: {event.name}")
        if event.name == "message_received":
            self.model.process_message(event.cargo)
            return self.model.machine.Receiving
        elif event.name == "stop_processing":
            return self.model.machine.Idle
        return self


class MessageProcessor:
    def __init__(self):
        self.machine = StateMachine(self)
        idle = Idle()
        receiving = Receiving()
        self.machine.add_state(idle)
        self.machine.add_state(receiving)
        self.machine.transitions = {
            "Idle": {"start_receiving": receiving},
            "Processing": {"stop_processing": idle},
        }
        self.machine.current_state = idle

    def process_message(self, message: str):
        print(f"Processing message: {message}")

    def process(self, event: Event):
        self.machine.process(event)


# Example usage:
processor = MessageProcessor()

# Define events
Event.set_names(["start_receiving", "message_received", "stop_processing"])

# Simulate processing
processor.process(Event("start_receiving"))
# Output: Idle state processing event: start_receiving

processor.process(Event("message_received", "Hello, World!"))
# Output: Processing state processing event: message_received
# Processing message: Hello, World!

processor.process(Event("message_received", "Another message"))
# Output: Processing state processing event: message_received
# Processing message: Another message

processor.process(Event("stop_processing"))
# Output: Processing state processing event: stop_processing
assert processor.machine.current_state == processor.machine.Idle
