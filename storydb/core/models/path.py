"""
Path class. Part of the StoryTechnologies project.

August 16, 2019
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""


class Path:
    def __init__(self, navigation_identifier: str, event_identifier: str, description: str):
        self.navigation_identifier = navigation_identifier.strip()
        self.event_identifier = event_identifier.strip()
        self.description = description
