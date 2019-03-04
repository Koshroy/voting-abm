from enum import Enum

from entity import Entity, Vote


class User(Entity):
    def __init__(self, opinion, opinion_radius, enthusiasm):
        super().__init__()
        self.opinion = opinion
        self.opinion_radius = opinion_radius
        self.enthusiasm = enthusiasm

    def _in_opinion_radius(self, post):
        return abs(post.opinion - self.opinion) <= self.opinion_radius * self.opinion

    def vote(self, post):
        return Vote.NEUTRAL


class NormalUser(User):
    def vote(self, post):
        return Vote.LIKE if self._in_opinion_radius(post) else Vote.NEUTRAL

    @property
    def style(self):
        return "normal"


class ExtremistUser(User):
    def vote(self, post):
        return Vote.LIKE if self._in_opinion_radius(post) else Vote.DISLIKE

    @property
    def style(self):
        return "extremist"
