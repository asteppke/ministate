"""A minimalist state machine."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict


class State(ABC):
    """A State encodes a particular behavior of the state machine,
    and decides the next state given the transitions table and the event."""

    def __init__(self):
        self._model = None
        self.name = self.__class__.__name__

    @abstractmethod
    def process(self, event: "Event") -> "State":
        """Runs action and decides next state for the StateMachine"""

    @property
    def model(self) -> object:
        """A reference to the model this state belongs to."""
        return self._model

    @model.setter
    def model(self, model: object) -> None:
        """Setting the reference to the model."""
        self._model = model


class Event:
    """Template for events. Each event has a name and an optional cargo."""

    def __init__(self, name: str, cargo=None):
        self.name = name
        self.cargo = cargo

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Event({self.name}, {self.cargo})"

    def __eq__(self, other):
        return self.name == other.name

    # Necessary when __eq__ is defined to allow events to be a dictionary key
    def __hash__(self) -> int:
        return hash(self.name)

    @classmethod
    def set_names(cls, event_names: List[str]):
        """Assigns each Event a given name independent of the object."""
        for name in event_names:
            setattr(Event, name, Event(name))


class StateMachine:
    """A machine where the behavior is given by its current state.
    Processes incoming events and switches to the next state."""

    def __init__(
        self,
        model: Optional[object] = None,
        states: Optional[List[State]] = None,
        transitions: Optional[Dict[str, Dict[str | type[Event], type[State]]]] = None,
        current_state: Optional[State] = None,
    ):
        self._states: List[State] = []
        # default to self if no model is given
        self.model = model if model is not None else self
        self.current_state = current_state

        if states is not None:
            for state in states:
                self.add_state(state)

        self.transitions = transitions if transitions is not None else {}

    def add_state(self, state: State):
        """Adds the state as an attribute to StateMachine, i.e. st = StateMachine; st.StateName"""
        state.model = self.model  # back-reference in state to the model
        self._states.append(state)
        setattr(self, state.name, state)

    @property
    def states(self) -> List[State]:
        """Returns all possible states."""
        return self._states

    def process(self, event: "Event"):
        """Processes the given event and switches to next state."""
        if self.current_state is not None:
            self.current_state = self.current_state.process(event)
