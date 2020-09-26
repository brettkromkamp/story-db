"""
Place class. Part of the StoryTechnologies project.

August 17, 2019
Brett Alistair Kromkamp (brett.kromkamp@gmail.com)
"""


class TimeInterval:
    def __init__(self, from_time_point: str, to_time_point: str) -> None:
        self.from_time_point = from_time_point
        self.to_time_point = to_time_point
