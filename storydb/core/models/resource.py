"""
Resource class. Part of the StoryTechnologies project.

August 15, 2019
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from typing import Optional, Union

from storydb.core.storydberror import StoryDbError


class Resource:
    def __init__(
        self, instance_of: str, title: str = "Undefined", reference: str = "", data: Optional[Union[str, bytes]] = None,
    ):
        if instance_of not in {"image", "video", "audio", "3d-scene", "text", "note"}:
            raise StoryDbError("Unsupported resource type")
        self.title = title
        self.reference = reference.strip()
        self.instance_of = instance_of.strip()

        if data:
            self.__data = data if isinstance(data, bytes) else bytes(data, encoding="utf-8")
        else:
            self.__data = None

    @property
    def data(self) -> Optional[bytes]:
        return self.__data

    @data.setter
    def data(self, value: Union[str, bytes]) -> None:
        self.__data = value if isinstance(value, bytes) else bytes(value, encoding="utf-8")

    def has_data(self) -> bool:
        return self.__data is not None
