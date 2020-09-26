"""
StoryDbError class. Part of the StoryTechnologies project.

August 15, 2019
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""


class StoryDbError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
