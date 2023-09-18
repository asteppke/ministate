"""
An example using the state machine module: a mouse that uses a queue to accept transitions
and uses this queue to process them. Depending on priority we can either run in 
order or add transitions to the front of the queue.

"""

from collections import defaultdict, deque
from enum import Enum
from ministate import State, StateMachine, Transition

class Priority(Enum):
    NORMAL = 1
    HIGH = 2


class MouseState(State):
    def run(self, transition: Transition):
        print(f"running {self.name}, transitioning to {transition}")

        return transition, Priority.NORMAL


class Idle(MouseState):
    def run(self, transition: Transition):
        #print(f"sitting at {self.machine.values['position']}")

        # a break helps to recover breath
        self.machine.values["breath"] = min(self.machine.values["breath"] + 2, 10)

        return None, Priority.NORMAL


class Running(MouseState):
    def run(self, transition):
        self.machine.run_ahead()

        next_transition = self.decide_next(transition)

        return next_transition, Priority.HIGH

    def decide_next(self, transition):
        # if we run we continue running :)
        if self.machine.values["breath"] <= 0:
            # need to breath first
            print("Need to breathe!")
            return Transition("relax")
        if transition is None:
            return Transition('relax')
        else:
            return Transition("start")


class Mouse(StateMachine):
    def __init__(self, states=None):

        StateMachine.__init__(self, states)

        # this will be our queue for communication with other objects
        self.queue = deque()

        self.values = {"position": 0, "speed": 1.0, "breath": 10}

    def dispatch(self, transition, priority=Priority.NORMAL):
        if priority == Priority.NORMAL:
            self.queue.append(transition)
        elif priority == Priority.HIGH:
            self.queue.appendleft(transition)

    def run(self, print_queue=True):
        print(f"state: {self.current_state.name}")
        if print_queue:
            print([str(e) for e in self.queue])

        done = False
        try:
            transition = self.queue.popleft()
        except IndexError:
            # if the queue is empty we are done and return
            done = True
            return done

        # switch to next state
        self.current_state = self.transitions[transition]

        # and run it
        next_transition, priority = self.current_state.run(transition)

        # and schedule next state
        if next_transition is not None:
            self.dispatch(next_transition, priority)

        return done

    def run_ahead(self):
        self.values["speed"] = self.values["breath"] / 10
        self.values["position"] += self.values["speed"]
        self.values["breath"] -= 1
        print(f"Mouse at {self.values['position']}, with speed {self.values['speed']} and breath {self.values['breath']}.")
        

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

    #  default transitions table
    transitions = defaultdict(lambda: mouse.Idle)
    transitions[Transition.start] = mouse.Running
    transitions[Transition.relax] = mouse.Idle

    mouse.transitions = transitions
    print(mouse.states)

    TRANSITIONS = "relax,start,start,start,relax"

    for ev in map(Transition, TRANSITIONS.split(",")):
        mouse.dispatch(ev)

    while True:
        finished = mouse.run()
        if finished:
            break
