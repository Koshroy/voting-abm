from enum import Enum


class Entity:
    uuid_counter = 0  # is this going to be unique with subclasses?

    @classmethod
    def _get_uuid(cls):
        uuid = cls.uuid_counter
        cls.uuid_counter += 1
        return uuid

    def __init__(self):
        self.uuid = self._get_uuid()


class Vote(Enum):
    LIKE = 1
    NEUTRAL = 0
    DISLIKE = -1
