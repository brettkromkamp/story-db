"""
ResolveMode enumeration. Part of the StoryTechnologies project.

August 17, 2019
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""

from enum import Enum


class ResolveMode(Enum):
    RESOLVE_SUB_EVENTS = 1
    DONT_RESOLVE_SUB_EVENTS = 2
    RESOLVE_CAUSES = 3
    DONT_RESOLVE_CAUSES = 4
    RESOLVE_EFFECTS = 5
    DONT_RESOLVE_EFFECTS = 6

    def __str__(self):
        return self.name
