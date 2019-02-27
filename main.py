from operator import attrgetter
from random import random, shuffle, uniform

from sortedcontainers import SortedList


ENTHUSIAST_PROB = 0.1
EXTREMIST_PROB = 0.08

EXTREMIST_RADIUS = 0.01
NORMAL_RADIUS = 0.1

EXTREMIST_SPREAD=0.001

class Entity:
    uuid_counter = 0 # is this going to be unique with subclasses?


    @classmethod
    def _get_uuid(cls):
        uuid = cls.uuid_counter
        cls.uuid_counter += 1
        return uuid


class User(Entity):
    def __init__(self, opinion, opinion_radius, enthusiasm, passionate):
        self.uuid = self._get_uuid()
        self.opinion = opinion
        self.opinion_radius = opinion_radius
        self.enthusiasm = enthusiasm
        self.passionate = passionate


    def vote(self, post):
        if abs(post.opinion - self.opinion) <= self.opinion_radius*self.opinion:
            return 1

        return -1 if self.passionate else 0


class Post(Entity):
    def __init__(self, opinion):
        self.uuid = self._get_uuid()
        self.opinion = opinion
        self.score = 0


    def __eq__(self, other):
        return self.score == other.score


def update_loop(user, posts):
    # update_loop mutates posts
    post_count = 0
    processed_posts = SortedList(key=attrgetter('score'))

    for i in range(user.enthusiasm):
        # Pop the highest element on this list
        post = posts.pop()
        post.score += user.vote(post)
        processed_posts.add(post)


    posts.update(processed_posts)


def run(num_users, num_runs):
    extremist_opinion = random()
    
    # Initialize the posts in a sorted list
    posts = SortedList(key=attrgetter('score'))
    for i in range(num_users*10):
        posts.add(Post(random()))

    users = []
    for i in range(num_users):
        is_enthusiast = random() < ENTHUSIAST_PROB
        enthusiasm = 100 if is_enthusiast else 10
        passionate = random() < EXTREMIST_PROB
        opinion = uniform(
            extremist_opinion - extremist_opinion*EXTREMIST_SPREAD,
            extremist_opinion + extremist_opinion*EXTREMIST_SPREAD,
        ) if passionate else random()
        opinion_radius = EXTREMIST_RADIUS if passionate else NORMAL_RADIUS
        users.append(User(
            opinion,
            opinion_radius,
            enthusiasm,
            passionate,
        ))

    shuffle(users) # shuffle the users so we "randomly" activate them

    for i in range(num_runs):
        print('Updating:', i+1)
        for u in users:
            update_loop(u, posts)
        
    for i in range(20):
        post = posts.pop()
        print('Post Score: {} | Opinion: {}'.format(post.score, post.opinion))

    print('Extremist Opinion:', extremist_opinion)
    print('Num. of Extremist Users:', len([u for u in users if u.passionate]))


def main():
    run(3000, 1)


if __name__ == "__main__":
    main()
