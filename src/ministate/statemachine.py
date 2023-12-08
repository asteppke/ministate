""" A minimalist state machine. """

from abc import ABC, abstractmethod
from typing import List, Optional, Dict


class State(ABC):
    """A State encodes a particular behavior of the state machine,
    and decides the next state given an event."""

    def __init__(self):
        self._machine = None
        self.name = self.__class__.__name__

    @abstractmethod
    def run(self, event: "Event"):
        """Runs action and decides next state for the StateMachine"""

    @property
    def machine(self) -> "StateMachine":
        """A reference to the StateMachine this state belongs to."""
        return self._machine

    @machine.setter
    def machine(self, machine: "StateMachine") -> None:
        """Setting the reference to the StateMachine."""
        self._machine = machine


class StateMachine:
    """A machine where the behavior is given by its current state.
    Processes a list of events to decide on the next state."""

    def __init__(
        self,
        states: Optional[List["State"]] = None,
        transitions: Optional[Dict] = None,
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

    def run(self, event: "Event"):
        """Processes the given event."""
        if self.current_state is not None:
            self.current_state = self.current_state.run(event)


class Event:
    """Template for events"""

    def __init__(self, name: str, cargo=None):
        self.name = name
        self.cargo = cargo

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    # Necessary when __eq__ is defined to allow events to be a dictionary key
    def __hash__(self):
        return hash(self.name)

    @classmethod
    def set_names(cls, event_names: List[str]):
        """Assigns each Event a given name independent of the object."""
        for name in event_names:
            setattr(Event, name, Event(name))
