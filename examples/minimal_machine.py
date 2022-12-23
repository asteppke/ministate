from collections import defaultdict
from ministate import State, StateMachine, Transition


class Nothing(State):
    def run(self, event: Transition):
        print(f"running {self.name}, transitioning to {event}")
        return event


class MinimalMachine(StateMachine):
    def __init__(self, states=None):

        StateMachine.__init__(self, states)


# a minimal example
minimal = MinimalMachine()
minimal.add_state(Nothing())
minimal.current_state = minimal.Nothing

# allows to call Transition('name') or Transition.name
transition_names = ["sleep"]
Transition.set_names(transition_names)

events = """sleep"""

# default transitions / events table
transitions = defaultdict(lambda: minimal.Nothing)
transitions[Transition.sleep] = minimal.Nothing

minimal.transitions = transitions
print(minimal.states)

minimal.run_input(Transition("sleep"))
