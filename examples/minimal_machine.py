from collections import defaultdict
from ministate import State, StateMachine, Event


class Adding(State):
    def process(self, event: str):
        print(
            f"running: {self.__class__.__name__}, received: {event}, going to"
            f" {self.model.machine.transitions[self.__class__.__name__][event]}"
        )
        return self.model.machine.transitions[self.__class__.__name__][event]

    def do_math(self):
        self.model.value += 1


class Subtracting(State):
    def process(self, event: str):
        print(
            f"running: {self.__class__.__name__}, received: {event}, going to"
            f" {self.model.machine.transitions[self.__class__.__name__][event]}"
        )
        return self.model.machine.transitions[self.__class__.__name__][event]

    def do_math(self):
        self.model.value -= 1


class Calculator:
    def __init__(self):
        self.value = 0

        self.machine = StateMachine(model=self)
        adding = Adding()
        subtracting = Subtracting()
        self.machine.add_state(adding)
        self.machine.add_state(subtracting)

        self.machine.transitions = {
            "Adding": {Event("more"): adding, Event("less"): subtracting},
            "Subtracting": {Event("less"): subtracting, Event("more"): adding},
        }

        self.machine.current_state = self.machine.Adding

    def add(self):
        self.value += 1

    def subtract(self):
        self.value -= 1

    def process(self, event):
        self.machine.process(event)

    def do_math(self):
        self.machine.current_state.do_math()


# a minimal example
minimal = Calculator()

# allows to call event('name') or Event.name
event_names = ["more", "less"]
Event.set_names(event_names)

# transitions table
print(minimal.machine.states)
print(minimal.machine.transitions)
print(minimal.value)

minimal.machine.process(Event("more"))

minimal.do_math()
minimal.do_math()
minimal.do_math()

print(minimal.value)
minimal.process(Event("less"))

minimal.do_math()
minimal.do_math()
minimal.do_math()

print(minimal.value)
