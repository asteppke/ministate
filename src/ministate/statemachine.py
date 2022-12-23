""" A quite minimalist state machine. """

from abc import ABC, abstractmethod
from typing import Iterable, List, Optional


class State(ABC):
    """A State has an operation, and decides the next State given an event or transition."""

    def __init__(self):
        self._machine = None
        self.name = self.__class__.__name__

    @abstractmethod
    def run(self, event: "Transition"):
        """Runs action and signals next state to the StateMachine"""

    @property
    def machine(self) -> "StateMachine":
        """A reference to the StateMachine this state belongs to."""
        return self._machine

    @machine.setter
    def machine(self, machine: "StateMachine") -> None:
        """Setting the reference to the StateMachine."""
        self._machine = machine


class StateMachine:
    """Takes a list of transitions to move from State to State."""

    def __init__(
        self,
        states: Optional[List["State"]] = None,
        transitions: Optional[List["Transition"]] = None,
        current_state: Optional["State"] = None,
    ):
        self._states: List["State"] = []
        self.current_state = current_state

        if states is not None:
            for state in states:
                self.add_state(state)

        self.transitions = transitions

    def add_state(self, state: "State"):
        """Adds the state as an attribute to StateMachine,
        i.e. st = StateMachine; st.StateName"""
        state.machine = self  # back-reference in state to machine
        self._states.append(state)
        setattr(self, state.name, state)

    @property
    def states(self) -> List[State]:
        """Returns all possible states."""
        return self._states

    def run_input(self, event: "Transition"):
        """Processes the given event (transition)."""
        if self.current_state is not None:
            self.current_state.run(event)

    def run_all(self, events: Iterable["Transition"]):
        """Processes all given events."""
        for i in events:
            print(f"in: {i}")
            self.run_input(i)


class Transition:
    """Template for transitions or events"""

    def __init__(self, event: str, cargo=None):
        self.event = event
        self.cargo = cargo

    def __str__(self):
        return self.event

    def __eq__(self, other):
        return self.event == other.event

    # Necessary when __eq__ is defined in order
    # to make this class usable as a dictionary key:
    def __hash__(self):
        return hash(self.event)

    @classmethod
    def set_names(cls, transition_names: List[str]):
        """Assigns each Transition a given name independent of the object."""
        for name in transition_names:
            setattr(Transition, name, Transition(name))
