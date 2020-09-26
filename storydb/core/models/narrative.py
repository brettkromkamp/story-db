"""
Narrative class. Part of the StoryTechnologies project.

August 9, 2020
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from storydb.core.models.event import Event
from typing import List, Optional


class Narrative:
    def __init__(self, title: str, description: str) -> None:
        self.title = title
        self.description = description
        self.__timeline = None

    @property
    def timeline(self) -> Optional[List[Event]]:
        return self.__timeline

    @timeline.setter
    def timeline(self, value: List[Event]) -> None:
        self.__timeline = value

    def has_timeline(self) -> bool:
        return self.__timeline is not None
