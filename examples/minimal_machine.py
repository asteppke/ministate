from collections import defaultdict
from ministate import State, StateMachine, Event


class Adding(State):
    def run(self, event: Event):
        print(
            f"running: {self.name}, received: {event}, going to"
            f" {self.machine.transitions[event]}"
        )
        return self.machine.transitions[event]

    def do_math(self):
        self.machine.value += 1


class Subtracting(State):
    def run(self, event: Event):
        print(
            f"running: {self.name}, received: {event}, going to"
            f" {self.machine.transitions[event]}"
        )
        return self.machine.transitions[event]

    def do_math(self):
        self.machine.value -= 1


class MinimalMachine(StateMachine):
    def __init__(self, states=None):
        super().__init__(states)
        self.value = 0

    def do_math(self):
        self.current_state.do_math()


# a minimal example
minimal = MinimalMachine()
minimal.add_state(Adding())
minimal.add_state(Subtracting())
minimal.current_state = minimal.Adding

# allows to call event('name') or Event.name
event_names = ["more", "less"]
Event.set_names(event_names)

# transitions table
transitions = defaultdict(lambda: minimal.Nothing)
transitions[Event.more] = minimal.Adding
transitions[Event.less] = minimal.Subtracting

minimal.transitions = transitions
print(minimal.states)
print(minimal.transitions)
print(minimal.value)

minimal.run(Event("more"))

minimal.do_math()
minimal.do_math()
minimal.do_math()

print(minimal.value)
minimal.run(Event("less"))

minimal.do_math()
minimal.do_math()
minimal.do_math()

print(minimal.value)
