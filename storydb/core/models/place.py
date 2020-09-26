"""
Place class. Part of the StoryTechnologies project.

August 15, 2019
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from typing import List

from storydb.core.models.entity import Entity
from storydb.core.models.path import Path
from storydb.core.models.resource import Resource


class Place(Entity):
    def __init__(
        self, identifier: str, name: str = "Undefined", description: str = None, environment: Resource = None,
    ):
        super().__init__(identifier, instance_of="place", name=name, description=description)
        self.environment = environment
        self.paths: List[Path] = []

        self.auto_rotate = False
        self.view_labels = False

    def add_path(self, path: Path) -> None:
        self.paths.append(path)

    def add_paths(self, paths: List[Path]) -> None:
        self.paths = [*self.paths, *paths]
