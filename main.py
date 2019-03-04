from enum import Enum
from operator import attrgetter
from random import random, shuffle, uniform

from sortedcontainers import SortedList
from entity import Entity
from rules import BaseVotingRules
from user import ExtremistUser, NormalUser


ENTHUSIAST_PROB = 0.1
EXTREMIST_PROB = 0.08

EXTREMIST_RADIUS = 0.01
NORMAL_RADIUS = 0.1

EXTREMIST_SPREAD = 0.001


class Post(Entity):
    def __init__(self, opinion):
        super().__init__()
        self.opinion = opinion
        self.score = 0

    def __eq__(self, other):
        return self.score == other.score


def update_loop(user, posts, rules):
    # update_loop mutates posts
    post_count = 0
    processed_posts = SortedList(key=attrgetter("score"))

    for i in range(user.enthusiasm):
        # Pop the highest element on this list
        post = posts.pop()
        post.score += rules.convert(user.vote(post))
        processed_posts.add(post)

    posts.update(processed_posts)


def run(num_users, num_runs):
    extremist_opinion = random()

    # Initialize the posts in a sorted list
    posts = SortedList(key=attrgetter("score"))
    for i in range(num_users * 10):
        posts.add(Post(random()))

    rules = BaseVotingRules()

    users = []
    for i in range(num_users):
        is_enthusiast = random() < ENTHUSIAST_PROB
        enthusiasm = 100 if is_enthusiast else 10
        passionate = random() < EXTREMIST_PROB
        opinion = (
            uniform(
                extremist_opinion - extremist_opinion * EXTREMIST_SPREAD,
                extremist_opinion + extremist_opinion * EXTREMIST_SPREAD,
            )
            if passionate
            else random()
        )
        opinion_radius = EXTREMIST_RADIUS if passionate else NORMAL_RADIUS
        new_user = (
            ExtremistUser(opinion, opinion_radius, enthusiasm)
            if passionate
            else NormalUser(opinion, opinion_radius, enthusiasm)
        )
        users.append(new_user)

    shuffle(users)  # shuffle the users so we "randomly" activate them

    for i in range(num_runs):
        print("Updating:", i + 1)
        for u in users:
            update_loop(u, posts, rules)

    for i in range(20):
        post = posts.pop()
        print("Post Score: {} | Opinion: {}".format(post.score, post.opinion))

    print("Extremist Opinion:", extremist_opinion)
    print("Num. of Extremist Users:", len([u for u in users if u.style == "extremist"]))


def main():
    run(3000, 1)


if __name__ == "__main__":
    main()
