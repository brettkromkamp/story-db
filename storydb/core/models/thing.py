"""
Thing class. Part of the StoryTechnologies project.

August 15, 2019
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from typing import List

from storydb.core.models.entity import Entity


class Thing(Entity):
    def __init__(self, identifier, name="Undefined", description=None, animation: str = None):
        super().__init__(identifier, instance_of="thing", name=name, description=description)
        self.animation = animation
        self.__tags: List[str] = []

    @property
    def tags(self) -> List[str]:
        return self.__tags

    def add_tag(self, tag: str) -> None:
        self.__tags.append(tag.strip())

    def add_tags(self, tags: List[str]) -> None:  # Missing the stripping of the individual tags
        self.__tags = [*self.__tags, *tags]
