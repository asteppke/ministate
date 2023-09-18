""" A minimalist state machine. """

from abc import ABC, abstractmethod
from typing import Iterable, List, Optional


class State(ABC):
    """A State has an operation, and decides the next State given a transition."""

    def __init__(self):
        self._machine = None
        self.name = self.__class__.__name__

    @abstractmethod
    def run(self, transition: "Transition"):
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
    """Takes a list of transitions to move from state to state."""

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
        """Adds the state as an attribute to StateMachine, i.e. st = StateMachine; st.StateName"""
        state.machine = self  # back-reference in state to machine
        self._states.append(state)
        setattr(self, state.name, state)

    @property
    def states(self) -> List[State]:
        """Returns all possible states."""
        return self._states

    def run_input(self, transition: "Transition"):
        """Processes the given transition."""
        if self.current_state is not None:
            self.current_state.run(transition)

    def run_all(self, transitions: Iterable["Transition"]):
        """Processes all given transitions."""
        for i in transitions:
            self.run_input(i)


class Transition:
    """Template for transitions"""

    def __init__(self, name: str, cargo=None):
        self.name = name
        self.cargo = cargo

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    # Necessary when __eq__ is defined to allow transitions to be a dictionary key
    def __hash__(self):
        return hash(self.name)

    @classmethod
    def set_names(cls, transition_names: List[str]):
        """Assigns each Transition a given name independent of the object."""
        for name in transition_names:
            setattr(Transition, name, Transition(name))
