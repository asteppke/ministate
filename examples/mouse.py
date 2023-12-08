"""
An example using the state machine module: a mouse that uses a queue to accept events
and uses this queue to process them. Depending on priority we can either run in 
order or add events to the front of the queue.

"""

from collections import defaultdict, deque
from enum import Enum
from ministate import State, StateMachine, Event

class Priority(Enum):
    NORMAL = 1
    HIGH = 2


class MouseState(State):
    def run(self, event: Event):
        print(f"running: {self.name}, received: {event}, going to {self.machine.transitions[event]}")

        return self.machine.transitions[event], Priority.NORMAL


class Idle(MouseState):
    def run(self, transition: Event):
        # a break helps to recover breath
        self.machine.values["breath"] = min(self.machine.values["breath"] + 2, 10)

        return None, Priority.NORMAL


class Running(MouseState):
    def run(self, event):
        self.machine.run_ahead()

        next_event = self.decide_next(event)

        return next_event, Priority.HIGH

    def decide_next(self, event):
        # if we run we continue running :)
        if self.machine.values["breath"] <= 0:
            # need to breath first
            print("Need to breathe!")
            return Event("relax")
        if event is None:
            return Event('relax')
        else:
            return Event("start")


class Mouse(StateMachine):
    def __init__(self, states=None):

        StateMachine.__init__(self, states)

        # this will be our queue for communication with other objects
        self.queue = deque()

        self.values = {"position": 0, "speed": 1.0, "breath": 10}

    def dispatch(self, event, priority=Priority.NORMAL):
        if priority == Priority.NORMAL:
            self.queue.append(event)
        elif priority == Priority.HIGH:
            self.queue.appendleft(event)

    def run(self, print_queue=True):
        print(f"state: {self.current_state.name}")
        if print_queue:
            print([str(e) for e in self.queue])

        done = False
        try:
            event = self.queue.popleft()
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
        print(f"Mouse at {self.values['position']}, with speed {self.values['speed']} and breath {self.values['breath']}.")
        

if __name__ == "__main__":
    # a mouse example
    mouse = Mouse(states=[Idle(), Running()])

    # alternatively:
    # mouse.add_state(Idle())
    # mouse.add_state(Running())

    mouse.current_state = mouse.Idle

    # allows to call Event('name') or Event.name
    event_names = ["relax", "start"]
    Event.set_names(event_names)

    #  default transitions table
    transitions = defaultdict(lambda: mouse.Idle)
    transitions[Event.start] = mouse.Running
    transitions[Event.relax] = mouse.Idle

    mouse.transitions = transitions
    print(mouse.states)

    EVENTS = "relax,start,start,start,relax"

    for ev in map(Event, EVENTS.split(",")):
        mouse.dispatch(ev)

    while True:
        finished = mouse.run()
        if finished:
            break
