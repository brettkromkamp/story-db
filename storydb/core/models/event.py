"""
Event class. Part of the StoryTechnologies project.

August 15, 2019
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from __future__ import annotations

from typing import Dict, Set

from storydb.core.models.entity import Entity
from storydb.core.models.participant import Participant
from storydb.core.models.place import Place
from storydb.core.models.thing import Thing
from storydb.core.models.timeinterval import TimeInterval


class Event(Entity):
    def __init__(
        self,
        identifier: str,
        action_property: str,
        rank: int = 0,
        name: str = "Undefined",
    ):
        super().__init__(identifier, instance_of="event", name=name)

        self.rank = rank

        # What?

        # Describes an action that happens or a property that is true in a temporal interval
        self.action_property = action_property
        # Sub-events which are the components of a totality (i.e., main event)
        self.events: Dict[str, Event] = {}

        # Who?
        self.participants: Dict[str, Participant] = {}
        self.things: Dict[str, Thing] = {}

        # When?
        self.when: TimeInterval = None

        # Where?
        self.where: Place = None

        # Why (cause)?
        self.why: Dict[str, Event] = {}

        self.effects: Dict[str, Event] = {}

        self.entities_tags: Dict[
            str, Set[str]
        ] = {}  # The tags-to-entities (participants and things) mapping for the event

    def add_event(self, event: Event) -> None:
        self.events[event.identifier] = event

    def add_participant(self, participant: Participant) -> None:
        self.participants[participant.identifier] = participant

    def add_thing(self, thing: Thing) -> None:
        self.things[thing.identifier] = thing

    def add_cause(self, cause: Event) -> None:
        self.why[cause.identifier] = cause

    def add_effect(self, effect: Event) -> None:
        self.effects[effect.identifier] = effect

    def what(self) -> Dict:
        return {"action-property": self.action_property, "events": self.events}

    def why(self) -> Dict[str, Event]:
        return self.why
