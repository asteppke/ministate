"""
An example using the state machine module: a mouse that uses a queue to accept events
and uses this queue to process them. Depending on priority we can either run in 
order or add events to the front of the queue.

"""

from collections import defaultdict, deque
from enum import Enum
from ministate import State, StateMachine, Transition

class Priority(Enum):
    NORMAL = 1
    HIGH = 2


class MouseState(State):
    def run(self, event: Transition):
        print(f"running {self.name}, transitioning to {event}")

        return event, Priority.NORMAL


class Idle(MouseState):
    def run(self, event: Transition):
        print(f"sitting at {self.machine.values['position']}")

        # a break helps to recover breath
        self.machine.values["breath"] = min(self.machine.values["breath"] + 1, 10)

        return None, Priority.NORMAL


class Running(MouseState):
    def run(self, event):
        print("state: running")
        self.machine.run_ahead()

        return None, Priority.NORMAL

    def decide_next(self, event):
        # if we measure we continue measuring :)
        if self.machine.values["breath"] == 0:
            # need to breath first
            print("need to breath!")
        if event is None:
            return self.machine.transitions[Transition("relax")]
        return self.machine.transitions[event]


class Mouse(StateMachine):
    def __init__(self, states=None):

        StateMachine.__init__(self, states)

        # this will be our queue for communication with other objects
        self.queue = deque()

        self.values = {"position": 0, "speed": 1.0, "breath": 10}

    def dispatch(self, event, priority=Priority.NORMAL):
        if priority == Priority.NORMAL:
            self.queue.appendleft(event)
        elif priority == Priority.HIGH:
            self.queue.append(event)

    def run(self, print_queue=True):
        if print_queue:
            print([str(e) for e in self.queue])

        done = False
        try:
            event = self.queue.pop()
        except IndexError:
            # if the queue is empty we are done and return
            done = True
            return done

        # switch to next state
        self.current_state = self.transitions[event]

        # and run it
        next_event, priority = self.current_state.run(event)

        # and schedule next state
        if next_event is not None:
            self.dispatch(next_event, priority)

        return done

    def run_ahead(self):
        self.values["speed"] = self.values["breath"] / 10
        self.values["position"] += self.values["speed"]
        self.values["breath"] -= 1


if __name__ == "__main__":
    # a mouse example
    mouse = Mouse(states=[Idle(), Running()])

    # alternatively:
    # mouse.add_state(Idle())
    # mouse.add_state(Running())

    mouse.current_state = mouse.Idle

    # allows to call Transition('name') or Transition.name
    transition_names = ["relax", "start"]
    Transition.set_names(transition_names)

    #  default transitions / events table
    transitions = defaultdict(lambda: mouse.Idle)
    transitions[Transition.start] = mouse.Running
    transitions[Transition.relax] = mouse.Idle

    mouse.transitions = transitions
    print(mouse.states)

    EVENTS = "relax,start,start,relax"

    for ev in map(Transition, EVENTS.split(",")):
        mouse.dispatch(ev)

    while True:
        finished = mouse.run()
        if finished:
            break
