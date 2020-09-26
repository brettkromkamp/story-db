"""
Entity class. Part of the StoryTechnologies project.

August 15, 2019
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from typing import List

from slugify import slugify  # type: ignore
from topicdb.core.models.attribute import Attribute  # type: ignore

from storydb.core.models.resource import Resource


class Entity:
    def __init__(
        self, identifier: str, instance_of: str, name: str = "Undefined", description: str = None,
    ):
        self.__identifier = slugify(str(identifier.strip()))
        self.__instance_of = slugify(str(instance_of.strip()))

        self.name = name
        self.description = description

        self.__resources: List[Resource] = []
        self.__attributes: List[Attribute] = []

    @property
    def identifier(self) -> str:
        return self.__identifier

    @property
    def instance_of(self) -> str:
        return self.__instance_of

    @property
    def resources(self) -> List[Resource]:
        return self.__resources

    def add_resource(self, resource: Resource) -> None:
        self.__resources.append(resource)

    def add_resources(self, resources: List[Resource]) -> None:
        self.__resources = [*self.__resources, *resources]

    @property
    def attributes(self) -> List[Attribute]:
        return self.__attributes

    def add_attribute(self, attribute: Attribute) -> None:
        self.__attributes.append(attribute)

    def add_attributes(self, attributes: List[Attribute]) -> None:
        self.__attributes = [*self.__attributes, *attributes]
