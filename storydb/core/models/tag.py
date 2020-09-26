"""
Tag class. Part of the StoryTechnologies project.

August 15, 2019
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""


class Tag:
    def __init__(self, tag: str, description: str = None) -> None:
        self.tag = tag
        self.description = description
