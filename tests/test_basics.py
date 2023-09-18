import pytest

from ministate.statemachine import State, StateMachine, Transition


def test_empty():
    machine = StateMachine()


class IdleState(State):
    def run(self, transition: Transition):
        return self
    
def test_basics():
    idle = IdleState()
    nothing = Transition('nothing')
    machine = StateMachine([idle], [nothing], idle)

    machine.run_input(nothing)

    assert machine.current_state == idle
    