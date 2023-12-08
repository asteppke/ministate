import pytest

from ministate.statemachine import State, StateMachine, Event


def test_empty():
    machine = StateMachine()


class IdleState(State):
    def run(self, event: Event):
        return self
    

class Sleeping(State):
    def run(self, event: Event):
        return self
        
def test_basics():
    idle = IdleState()
    nothing = Event('nothing')
    machine = StateMachine([idle], [nothing], idle)

    machine.run(nothing)

    assert machine.current_state == idle
    
    sleep = Sleeping()
    machine.add_state(sleep)

    assert idle in machine.states
    assert sleep in machine.states